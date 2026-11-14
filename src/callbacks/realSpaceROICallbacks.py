"""
Real-Space ROI callbacks for pyQuant4D.

Handles all interactions with the real-space ROI controls:
  - RealROIShape dropdown  (full / point / ellipse / rectangle / poly / file)
  - FrameX / FrameY spinboxes  (probe position for point-ROI)
  - UpdateImages button  (force diffraction-pattern recalculation)
  - Live ROI move signals  (from InteractiveCircle / Rectangle / Polygon / Point)

Porting notes
-------------
Replaced MATLAB-only constructs:
  drawpolygon(ax,...)  → matplotlib.widgets.PolygonSelector (async callback)
  createMask(roi,img)  → _roi_to_mask(roi, shape, typ)
  centroid(polyshape(pos))   → np.mean(roi.vertices, axis=0)
  True(shape)/False(shape)   → np.ones/np.zeros(..., bool)
  gather(reshape(...))       → (mask_flat @ self.Data / n_sum).reshape(...)
  structfun / setExSrc       → explicit Python loops with getattr/setattr
  addlistener(roi, ...)      → roi.updateXxx.connect(lambda ...)
  ancestor(roi,'figure')     → roi.axis.figure
"""

from __future__ import annotations

import numpy as np
from matplotlib.path import Path
from matplotlib.widgets import PolygonSelector
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

from callbacks.allFunctions import (
    enableWindows, notifDLG, toUpdateImage, plotAllPatterns, importMask
)
from annotationsClasses.interactiveCircle import InteractiveCircle        # fixed: lowercase 'i'
from annotationsClasses.interactiveRectangle import InteractiveRectangle
from annotationsClasses.interactivePolygon import InteractivePolygon
from annotationsClasses.interactivePoint import InteractivePoint


# ---------------------------------------------------------------------------
# Mask helper
# ---------------------------------------------------------------------------

def _roi_to_mask(roi, shape, typ: str) -> np.ndarray:
    """
    Rasterise *roi* onto a boolean grid of *shape* = (ny, nx).

    Coordinates are in data-space (pixels of the real-space image), where
    x = column index and y = row index, matching matplotlib's default for
    imshow with origin='upper'.
    """
    ny, nx = shape
    yy, xx = np.mgrid[0:ny, 0:nx]
    pts = np.column_stack([xx.ravel().astype(float),
                           yy.ravel().astype(float)])

    if typ == 'ellipse':
        # InteractiveCircle: use the outermost radius
        dist = np.linalg.norm(pts - roi.center, axis=1)
        return (dist <= roi.radius[-1]).reshape(ny, nx)

    elif typ == 'rectangle':
        # InteractiveRectangle: rotation is always 0, so just check bounds
        theta = np.radians(roi.rotation)        # 0.0 for axis-aligned
        c, s = np.cos(theta), np.sin(theta)
        R_inv = np.array([[c, s], [-s, c]])
        local = (pts - roi.center) @ R_inv.T
        return np.all(np.abs(local) <= roi.size / 2.0, axis=1).reshape(ny, nx)

    elif typ == 'poly':
        # InteractivePolygon: point-in-polygon test
        path = Path(np.vstack([roi.vertices, roi.vertices[0]]))
        return path.contains_points(pts).reshape(ny, nx)

    # Fallback — should not be reached for well-typed calls
    return np.ones((ny, nx), bool)


# ---------------------------------------------------------------------------
# Main callback dispatcher
# ---------------------------------------------------------------------------

def realSpaceROICallbacks(self):
    """
    Dispatcher connected to every Real-Space ROI-related UI signal.

    Qt ``sender()`` determines which widget fired; inner functions
    ``drawRealROI`` and ``moveRealROI`` do the actual work.
    """
    if self.blockAllSignals:
        return

    sender = self.sender()

    # ======================================================================
    # Inner functions
    # ======================================================================

    def drawRealROI(typ: str):
        """
        Remove any existing ROIs and draw fresh ones of the requested *typ*
        on every visible real-space image panel.
        """
        # Remove all existing ROIs
        roi_dict = getattr(self.A, 'RealROI', {})
        for roi in roi_dict.values():
            if roi is not None:
                try:
                    roi.remove()
                except Exception:
                    pass
        self.A.RealROI = {}

        # Also clean up any pending selector from an interrupted polygon draw
        if hasattr(self.A, '_tmp_selector') and self.A._tmp_selector is not None:
            try:
                self.A._tmp_selector.disconnect_events()
            except Exception:
                pass
            self.A._tmp_selector = None

        c = qtg.QColor(255, 127, 127)                       # salmon red
        c_mpl = (c.redF(), c.greenF(), c.blueF())           # (R, G, B) floats

        # --- Polygon: interactive drawing is asynchronous ----------------
        if typ == 'poly':
            img_names = [self.SettingsWindow.DispImage.itemText(ii)
                         for ii in range(self.SettingsWindow.DispImage.count())]
            rs_mask = (
                (self.G.Img.space == 'Real') &
                (self.G.Img.type != 'Mask') &
                self.G.Img.name.isin(img_names)
            )

            message = (
                "Select a Real-space Image to draw a polygon ROI.\n\n"
                "Click to place vertices; click the first vertex to close the\n"
                "polygon. Press <Esc> to cancel drawing."
            )
            sel = notifDLG(self, self, 'list', message,
                           'Draw Polygon ROI', self.G.Img.name[rs_mask])

            if sel is None:
                self.RealROIShape.blockSignals(True)
                self.RealROIShape.setCurrentIndex(
                    self.RealROIShape.findData('full')
                )
                self.RealROIShape.blockSignals(False)
                return

            # Bring the selected image to front for drawing
            id_sel = self.G.Img[self.G.Img.name.isin([sel])].id.item()
            ax_sel = self.Fig[id_sel].ax
            self.Fig[id_sel].show()
            self.Fig[id_sel].activateWindow()

            enableWindows(self, False)

            def _poly_done(vertices):
                """Callback fired by PolygonSelector when polygon is closed."""
                try:
                    ax_sel.figure.canvas.mpl_disconnect(_esc_cid[0])
                except Exception:
                    pass
                if hasattr(self.A, '_tmp_selector') and self.A._tmp_selector is not None:
                    try:
                        self.A._tmp_selector.disconnect_events()
                    except Exception:
                        pass
                    self.A._tmp_selector = None

                enableWindows(self, True)

                if not vertices or len(vertices) < 3:
                    self.RealROIShape.blockSignals(True)
                    self.RealROIShape.setCurrentIndex(
                        self.RealROIShape.findData('full')
                    )
                    self.RealROIShape.blockSignals(False)
                    return

                poly_verts = np.array(vertices, dtype=float)
                real_ids = self.G.Img[
                    (self.G.Img.space == 'Real') &
                    (self.G.Img.type != 'Mask')
                ].id

                for img_id in real_ids:
                    roi = InteractivePolygon(
                        self.Fig[img_id].ax,
                        vertices=poly_verts,
                        color=c_mpl,
                    )
                    roi.connect()
                    roi.updatePoly.connect(
                        lambda *, _roi=roi: moveRealROI(roi_src=_roi)
                    )
                    self.A.RealROI[img_id] = roi

                moveRealROI()

            def _on_esc(event):
                if event.key == 'escape':
                    _poly_done([])   # empty → revert to 'full'

            _esc_cid = [ax_sel.figure.canvas.mpl_connect(
                'key_press_event', _on_esc
            )]
            self.A._tmp_selector = PolygonSelector(
                ax_sel, _poly_done,
                props=dict(color=c_mpl, linewidth=1.5),
            )
            return   # remainder handled asynchronously in _poly_done

        # --- All other shapes: draw synchronously -----------------------
        # Use diffraction axes extents as a scale reference
        rg = np.array([
            np.ptp(self.Fig.Dfrn.ax.get_xlim()),
            np.ptp(self.Fig.Dfrn.ax.get_ylim()),
        ])
        p = np.array([self.FrameX.value(), self.FrameY.value()], dtype=float)

        real_ids = self.G.Img[
            (self.G.Img.space == 'Real') &
            (self.G.Img.type != 'Mask')
        ].id

        for img_id in real_ids:
            ax = self.Fig[img_id].ax

            if typ == 'full':
                xl, xr = sorted(ax.get_xlim())
                yl, yr = sorted(ax.get_ylim())
                roi = InteractiveRectangle(
                    ax,
                    center=np.array([(xl + xr) / 2.0, (yl + yr) / 2.0]),
                    size=np.array([xr - xl, yr - yl]),
                    color=c_mpl, interactions='none',
                )
                roi.patch.set_alpha(0.0)
                roi.handles.set_visible(False)

            elif typ == 'point':
                pt_artist = ax.scatter(
                    p[0], p[1],
                    color=c_mpl, s=50, zorder=5, animated=True,
                )
                roi = InteractivePoint(pt_artist)

            elif typ == 'ellipse':
                roi = InteractiveCircle(
                    ax,
                    center=p.copy(),
                    radius=float(np.min(0.1 * rg)),
                    color=c_mpl,
                )

            elif typ == 'rectangle':
                roi = InteractiveRectangle(
                    ax,
                    center=p.copy(),
                    size=0.2 * rg,
                    color=c_mpl, interactions='all',
                )

            elif typ == 'file':
                xl, xr = sorted(ax.get_xlim())
                yl, yr = sorted(ax.get_ylim())
                roi = InteractiveRectangle(
                    ax,
                    center=np.array([(xl + xr) / 2.0, (yl + yr) / 2.0]),
                    size=np.array([xr - xl, yr - yl]),
                    color=c_mpl, interactions='none',
                )
                roi.patch.set_alpha(0.0)
                roi.handles.set_visible(False)

            else:
                continue

            roi.connect()

            # Wire the roi's update signal back to moveRealROI.
            # Using default-argument capture so each lambda closes over
            # its own roi object, not the loop variable.
            if hasattr(roi, 'updateRect'):
                roi.updateRect.connect(lambda *, _roi=roi: moveRealROI(roi_src=_roi))
            elif hasattr(roi, 'updateCircle'):
                roi.updateCircle.connect(lambda *, _roi=roi: moveRealROI(roi_src=_roi))
            elif hasattr(roi, 'positionChanged'):
                roi.positionChanged.connect(lambda *, _roi=roi: moveRealROI(roi_src=_roi))

            self.A.RealROI[img_id] = roi

        moveRealROI()

    # ----------------------------------------------------------------------

    def moveRealROI(from_spinbox: str | None = None,
                    roi_src=None):
        """
        Recalculate the diffraction pattern for the current real-space ROI.

        Parameters
        ----------
        from_spinbox : ``'x'`` | ``'y'`` | ``None``
            Set when the call originated from FrameX or FrameY spinboxes.
        roi_src : ROI object | None
            The annotation object that triggered this update, or ``None``
            when called from other contexts.
        """
        roi_dict = getattr(self.A, 'RealROI', {})

        # Pick the primary ROI to read geometry from
        roi = roi_dict.get('Real') or next(
            (v for v in roi_dict.values() if v is not None), None
        )

        x = self.FrameX.value()
        y = self.FrameY.value()

        if from_spinbox == 'x':
            x = max(1, self.FrameX.value())
        elif from_spinbox == 'y':
            y = max(1, self.FrameY.value())
        elif roi_src is not None:
            roi = roi_src
            typ = self.RealROIShape.currentData()
            try:
                if typ in ('rectangle', 'full', 'file'):
                    x, y = float(roi.center[0]), float(roi.center[1])
                elif typ == 'point':
                    x, y = float(roi.position[0]), float(roi.position[1])
                elif typ == 'ellipse':
                    x, y = float(roi.center[0]), float(roi.center[1])
                elif typ == 'poly':
                    cx, cy = np.mean(roi.vertices, axis=0)
                    x, y = float(cx), float(cy)
            except (AttributeError, TypeError):
                pass   # keep current x, y

        x, y = int(round(x)), int(round(y))

        # --- For point ROI: move the annotation when spinbox drives it ---
        if from_spinbox in ('x', 'y') and self.RealROIShape.currentData() == 'point':
            for r in roi_dict.values():
                if r is not None and hasattr(r, 'position'):
                    try:
                        r.position = np.array([x, y], dtype=float)
                        r.redraw()
                    except Exception:
                        pass

        # --- Update UI spinboxes (block to avoid re-entrant signals) ----
        self.blockAllSignals = True
        self.FrameX.setValue(x)
        self.FrameY.setValue(y)
        self.blockAllSignals = False

        # --- Sync ROI geometry across all real-space panels --------------
        if roi is not None:
            for img_id, other_roi in roi_dict.items():
                if other_roi is None or other_roi is roi:
                    continue
                for prop in ('center', 'size', 'rotation', 'vertices', 'position'):
                    if hasattr(roi, prop) and hasattr(other_roi, prop):
                        try:
                            setattr(other_roi, prop,
                                    getattr(roi, prop).copy()
                                    if hasattr(getattr(roi, prop), 'copy')
                                    else getattr(roi, prop))
                            other_roi.redraw()
                        except Exception:
                            pass

        # --- Build the real-space mask -----------------------------------
        ny, nx = self.D.NFrY, self.D.NFrX
        typ = self.RealROIShape.currentData()

        if typ == 'full':
            mask_real = np.ones((ny, nx), bool)

        elif typ == 'point':
            mask_real = np.zeros((ny, nx), bool)
            # Convert 1-based probe coordinates → 0-based row/col indices
            yi = max(0, min(y - 1, ny - 1))
            xi = max(0, min(x - 1, nx - 1))
            mask_real[yi, xi] = True

        elif typ == 'file':
            mask_real = np.asarray(self.Image.RealROIFile, bool)

        elif roi is not None:
            mask_real = _roi_to_mask(roi, (ny, nx), typ)

        else:
            mask_real = np.ones((ny, nx), bool)   # fallback

        # --- Optionally invert -------------------------------------------
        mask_real = mask_real.astype(float)
        if self.RealROIInvert.isChecked():
            mask_real = mask_real.max() - mask_real

        self.Image.RealMask = mask_real

        # --- Weighted-average diffraction pattern for selected frames ----
        # self.Data is (NFr, NPx), so (mask_flat) @ self.Data sums over frames
        mask_flat = mask_real.ravel()
        n_sum = float(mask_flat.sum())
        if n_sum < np.finfo(np.float32).eps:
            n_sum = float(np.finfo(np.float32).eps)

        self.Image.Dfrn = (
            (mask_flat @ self.Data) / n_sum
        ).reshape(self.D.NPxY, self.D.NPxX)

        plotAllPatterns(self)

    # ======================================================================
    # Dispatch to inner functions based on UI sender
    # ======================================================================

    # -- Force diffraction update from the current ROI --------------------
    if sender is self.UpdateImages:
        roi_dict = getattr(self.A, 'RealROI', {})
        if not roi_dict or all(v is None for v in roi_dict.values()):
            # No ROI drawn yet — trigger shape selection to draw one
            self.RealROIShape.currentIndexChanged.emit(
                self.RealROIShape.currentIndex()
            )
        else:
            moveRealROI()

    # -- Shape dropdown changed -------------------------------------------
    elif sender is self.RealROIShape:
        val = self.RealROIShape.currentData()

        if val == 'file':
            self.Image.RealROIFile = importMask(self, 'Real')
            if self.Image.RealROIFile is None:
                val = 'full'
                self.RealROIShape.blockSignals(True)
                self.RealROIShape.setCurrentIndex(
                    self.RealROIShape.findData('full')
                )
                self.RealROIShape.blockSignals(False)

        # Enable / disable point-only panel widgets
        is_point = (val == 'point')
        for w in (self.FrameX, self.FrameY,
                  self.FrameXLabel, self.FrameYLabel, self.FrameLabel):
            w.setEnabled(is_point)

        self.RealROIInvert.setEnabled(val != 'full')
        self.RealROIInvert.blockSignals(True)
        self.RealROIInvert.setChecked(
            self.RealROIInvert.isChecked() and self.RealROIInvert.isEnabled()
        )
        self.RealROIInvert.blockSignals(False)

        drawRealROI(val)

    # -- Probe-position spinboxes ----------------------------------------
    elif sender is self.FrameX:
        moveRealROI(from_spinbox='x')

    elif sender is self.FrameY:
        moveRealROI(from_spinbox='y')

    # -- Any other sender (e.g. the ROI invert checkbox) -----------------
    else:
        moveRealROI()
