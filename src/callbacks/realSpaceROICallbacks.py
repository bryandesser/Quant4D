"""
Real-Space ROI callbacks for pyQuant4D.

Handles all interactions with the real-space ROI controls:
  - RealROIShape dropdown  (full / point / ellipse / rectangle / poly / file)
  - FrameX / FrameY spinboxes  (probe position for point-ROI)
  - UpdateImages button  (force diffraction-pattern recalculation)
  - Live ROI move signals  (from InteractiveEllipse / Rectangle / Polygon / Point)

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
from matplotlib.widgets import PolygonSelector
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

from callbacks.import_io import importMask
from callbacks.plotting import plotAllPatterns, toUpdateImage
from callbacks.utils import notifDLG
from callbacks.window_manager import enableWindows
from annotationsClasses.interactiveRectangle import InteractiveRectangle
from annotationsClasses.interactivePolygon import InteractivePolygon
from annotationsClasses.interactiveEllipse import InteractiveEllipse
from annotationsClasses.interactivePoint import InteractivePoint
from callbacks.signals import all_signals_blocked, signals_blocked  # noqa: E402
from callbacks import compute  # noqa: E402
from callbacks.layout import dfrn_shape  # noqa: E402


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
    if typ == 'ellipse':        # InteractiveEllipse
        return compute.ellipse_mask(shape, roi.center, roi.semiaxes, roi.rotation)
    if typ == 'rectangle':      # InteractiveRectangle
        return compute.rectangle_mask(shape, roi.center, roi.size, roi.rotation)
    if typ == 'poly':           # InteractivePolygon
        return compute.polygon_mask(shape, roi.vertices)

    # Fallback — should not be reached for well-typed calls
    return np.ones((int(shape[0]), int(shape[1])), bool)


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

            names = list(self.G.Img.name[rs_mask])
            if len(names) == 1:         # only one real-space image shown: nothing to choose
                sel = names[0]
            else:
                message = (
                    "Select a Real-space Image to draw a polygon ROI.\n\n"
                    "Click to place vertices; click the first vertex to close the\n"
                    "polygon. Press <Esc> to cancel drawing."
                )
                sel = notifDLG(self, self, 'list', message,
                               'Draw Polygon ROI', self.G.Img.name[rs_mask])

            if sel is None:
                # not blocked: the full ROI must actually be applied, not just shown in the combo
                self.RealROIShape.setCurrentIndex(self.RealROIShape.findData('full'))
                return

            # Bring the selected image to front for drawing
            id_sel = self.G.Img[self.G.Img.name.isin([sel])].id.item()
            ax_sel = self.Fig[id_sel].ax
            self.Fig[id_sel].show()
            self.Fig[id_sel].activateWindow()

            enableWindows(self, False)

            def _poly_done(vertices):
                """The polygon was closed (or drawing cancelled with an empty list)."""
                if _done[0]:
                    return
                _done[0] = True
                try:
                    ax_sel.figure.canvas.mpl_disconnect(_esc_cid[0])
                except Exception:
                    pass
                selector = getattr(self.A, '_tmp_selector', None)
                if selector is not None:
                    # The selector's own outline and vertex handles must go too: left on the axes
                    # they stayed behind as a second, uneditable copy of the polygon.
                    try:
                        selector.disconnect_events()
                        for art in selector.artists:
                            art.remove()
                    except Exception:
                        pass
                    self.A._tmp_selector = None
                    ax_sel.figure.canvas.draw_idle()

                enableWindows(self, True)

                if not vertices or len(vertices) < 3:
                    # cancelled: apply the full ROI (with signals blocked the previous ROI's mask stayed)
                    self.RealROIShape.setCurrentIndex(self.RealROIShape.findData('full'))
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

            def _on_select(vertices):
                # PolygonSelector calls this from inside its own release handler (and again on every
                # later release): finish once, after that handler has returned.
                qtc.QTimer.singleShot(0, lambda v=list(vertices): _poly_done(v))

            _done = [False]
            _esc_cid = [ax_sel.figure.canvas.mpl_connect(
                'key_press_event', _on_esc
            )]
            # matplotlib's stub types onselect as (x, y); PolygonSelector actually passes the vertex list
            self.A._tmp_selector = PolygonSelector(
                ax_sel, _on_select,  # pyright: ignore[reportArgumentType]
                props=dict(color=c_mpl, linewidth=1.5),
            )
            return   # remainder handled asynchronously in _poly_done

        # --- All other shapes: draw synchronously -----------------------
        # Default sizes are fractions of the real-space (scan) extent
        rg = np.array([self.D.NFrX, self.D.NFrY], dtype=float)
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
                    color=c_mpl, s=50, zorder=5,     # not animated: ordinary redraws must draw it
                )
                roi = InteractivePoint(pt_artist)

            elif typ == 'ellipse':
                roi = InteractiveEllipse(
                    ax,
                    center=p.copy(),
                    semiaxes=float(np.min(0.1 * rg)) * np.array([1.5, 1.0]),   # MATLAB: 0.1 of the scan; visibly elliptical
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
            signal = getattr(roi, 'updateRect', None) or getattr(roi, 'updateEllipse', None) \
                or getattr(roi, 'positionChanged', None)
            if signal is not None:
                signal.connect(lambda *, _roi=roi: moveRealROI(roi_src=_roi))

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
        if roi_src is not None and not any(roi_src is v for v in roi_dict.values()):
            return          # a replaced ROI (e.g. after switching shape) is not the current one

        # Pick the primary ROI to read geometry from
        roi = roi_dict.get('Real') or next(
            (v for v in roi_dict.values() if v is not None), None
        )

        x = self.FrameX.value()
        y = self.FrameY.value()

        if from_spinbox == 'x':
            x = max(0, self.FrameX.value())
        elif from_spinbox == 'y':
            y = max(0, self.FrameY.value())
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
        with all_signals_blocked(self):
            self.FrameX.setValue(x)
            self.FrameY.setValue(y)

        # --- Sync ROI geometry across all real-space panels --------------
        if roi is not None:
            for img_id, other_roi in roi_dict.items():
                if other_roi is None or other_roi is roi:
                    continue
                for prop in ('center', 'size', 'semiaxes', 'rotation', 'vertices', 'position'):
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
            # Probe coordinates are 0-based (x = column, y = row), same as the display
            yi = max(0, min(y, ny - 1))
            xi = max(0, min(x, nx - 1))
            mask_real[yi, xi] = True

        elif typ == 'file':
            mask_real = np.asarray(self.Mask.RealROIFile, float)   # grey levels weight the frames

        elif roi is not None:
            mask_real = _roi_to_mask(roi, (ny, nx), typ)

        else:
            mask_real = np.ones((ny, nx), bool)   # fallback

        # --- Optionally invert -------------------------------------------
        mask_real = mask_real.astype(float)
        if self.RealROIInvert.isChecked():
            mask_real = mask_real.max() - mask_real

        self.Fig.RealMask.Image = mask_real

        # --- Diffraction pattern of the selected frames (Pattern dropdown: sum, mean, max, …) ----
        self.Fig.Dfrn.Image = diffractionPattern(self, mask_real)

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
            self.Mask.RealROIFile = importMask(self, 'Real')
            if self.Mask.RealROIFile is None:
                val = 'full'
                with signals_blocked(self.RealROIShape):
                    self.RealROIShape.setCurrentIndex(
                        self.RealROIShape.findData('full')
                    )

        # Enable / disable point-only panel widgets
        is_point = (val == 'point')
        setPatternModesFor(self, is_point)
        for w in (self.FrameX, self.FrameY,
                  self.FrameXLabel, self.FrameYLabel, self.FrameLabel):
            w.setEnabled(is_point)

        self.RealROIInvert.setEnabled(val != 'full')
        with signals_blocked(self.RealROIInvert):
            self.RealROIInvert.setChecked(
                self.RealROIInvert.isChecked() and self.RealROIInvert.isEnabled()
            )

        drawRealROI(val)

    # -- Probe-position spinboxes ----------------------------------------
    elif sender is self.FrameX:
        moveRealROI(from_spinbox='x')

    elif sender is self.FrameY:
        moveRealROI(from_spinbox='y')

    # -- Any other sender (e.g. the ROI invert checkbox) -----------------
    else:
        moveRealROI()


DEFAULT_COMBINE = "mean"


def connectPatternCombine(self) -> None:
    """Add the "Pattern" dropdown (how a region's diffraction patterns are combined: sum, mean,
    max, std, sqrt, ln, log10 — MATLAB Quant4D's diffraction dropdown) to the diffraction
    window's toolbar; called once from ``slotsSignals``.  Default: mean (Bryan, 2026-11-18;
    MATLAB's default is sum)."""
    combo = qtw.QComboBox()
    combo.setObjectName("DfrnCombine")
    for mode in compute.COMBINE_MODES:
        combo.addItem(mode, mode)
    combo.setCurrentIndex(combo.findData(DEFAULT_COMBINE))
    combo.setToolTip("Set how patterns are combined in real space. NOTE: max() and std() can be "
                     "significantly slower when interacting with a real-space ROI!")
    toolbar = self.Fig.Dfrn.toolbar
    toolbar.addSeparator()
    toolbar.addWidget(qtw.QLabel(" Pattern: "))
    toolbar.addWidget(combo)
    self.DfrnCombine = combo
    combo.currentIndexChanged.connect(lambda *_: realSpaceROICallbacks(self))


def diffractionPattern(self, weights):
    """The diffraction image for real-space *weights*, combined as the "Pattern" dropdown says."""
    mode = self.DfrnCombine.currentData() if hasattr(self, "DfrnCombine") else DEFAULT_COMBINE
    return compute.combine_frames(self.Data, weights, mode, self.D.GPU).reshape(dfrn_shape(self.D))


def setPatternModesFor(self, single_frame: bool) -> None:
    """``std`` over one frame is meaningless (all zeros): grey it out for a point ROI, falling back
    to the default if it was selected."""
    combo = getattr(self, "DfrnCombine", None)
    if combo is None:
        return
    item = combo.model().item(combo.findData("std"))
    item.setEnabled(not single_frame)
    item.setToolTip("Not available for a point ROI (a single frame has no spread)" if single_frame else "")
    if single_frame and combo.currentData() == "std":
        with signals_blocked(combo):
            combo.setCurrentIndex(combo.findData(DEFAULT_COMBINE))
