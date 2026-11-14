"""
virtualApertureCallbacks.py
---------------------------
Virtual aperture mode (VrApMod): a draggable circular aperture drawn on the
diffraction pattern that the user can position, resize, and replicate with
n-fold rotation symmetry and optional mirror symmetry.

The union mask of all aperture instances is applied to the 4D-STEM data to
form a virtual bright-field / dark-field real-space image.

UI controls
-----------
  VrApR          : aperture radius (spinbox, in diffraction-pixel units)
  VrApSymm       : n-fold rotational symmetry count (1, 2, 3, 4, 6)
  VrApInvert     : invert mask (complement) — virtual dark-field
  VrApMirror     : add mirror-reflected copy of the full aperture set
  VrApMirrRot    : angle of the mirror line through the beam centre (degrees)
  VrApMirrRot_NF : numerical-field companion to VrApMirrRot
  VrApRotStep    : step size for rotation-increment buttons (not yet wired)

Annotation attributes (self.A.*)
---------------------------------
  VrAp     : InteractiveCircle — primary aperture (and clones drawn beside it)
  VrApMirL : Line2D — mirror-symmetry axis line
  VrApMirP : InteractivePoint — drag handle to rotate the mirror line
"""

from annotationsClasses.interactiveCircle import InteractiveCircle
from annotationsClasses.interactivePoint import InteractivePoint
import numpy as np


def virtualApertureCallbacks(self):  # noqa: C901
    # Deferred import to avoid circular dependency with allFunctions.py
    # (allFunctions imports this module; importing allFunctions here at
    # module level would create a cycle).
    from callbacks.allFunctions import plotImage, isDiffToPrev  # noqa: E402

    if self.blockAllSignals:
        return

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    def _remove_vr_annotations():
        """Remove all existing virtual aperture annotations."""
        if self.A.VrAp is not None:
            # InteractiveCircle stores artists in .circ (list of Line2D) and .point (scatter)
            for line in self.A.VrAp.circ:
                try:
                    line.remove()
                except ValueError:
                    pass
            try:
                self.A.VrAp.point.remove()
            except ValueError:
                pass
            self.A.VrAp = None

        if self.A.VrApMirL is not None:
            try:
                self.A.VrApMirL.remove()
            except ValueError:
                pass
            self.A.VrApMirL = None

        if self.A.VrApMirP is not None:
            self.A.VrApMirP.remove()
            self.A.VrApMirP = None

    def _rotate_pt(pt, angle_deg, centre):
        """Rotate *pt* by *angle_deg* degrees around *centre*."""
        c, s = np.cos(np.radians(angle_deg)), np.sin(np.radians(angle_deg))
        offset = np.array(pt) - np.array(centre)
        rotated = np.array([c * offset[0] - s * offset[1],
                            s * offset[0] + c * offset[1]])
        return rotated + np.array(centre)

    def _mirror_pt(pt, angle_deg, centre):
        """Reflect *pt* across a line through *centre* at *angle_deg* degrees."""
        offset = np.array(pt) - np.array(centre)
        a2 = 2.0 * np.radians(angle_deg)
        mirrored = np.array([np.cos(a2) * offset[0] + np.sin(a2) * offset[1],
                             np.sin(a2) * offset[0] - np.cos(a2) * offset[1]])
        return mirrored + np.array(centre)

    def _circle_mask(centre_xy, radius, shape):
        """
        Boolean mask (shape = (NPxX, NPxY)) that is True inside a circle.

        Parameters
        ----------
        centre_xy : array-like, (x, y)
        radius    : float, in diffraction pixels
        shape     : (NPxX, NPxY)
        """
        xg, yg = np.mgrid[0:shape[0], 0:shape[1]]
        return ((xg - centre_xy[0]) ** 2 + (yg - centre_xy[1]) ** 2
                <= radius ** 2)

    # ------------------------------------------------------------------
    # draw — build fresh annotations
    # ------------------------------------------------------------------

    def drawVrAp():
        """
        Draw the virtual aperture annotation(s) on the diffraction pattern.

        Creates:
          self.A.VrAp     : InteractiveCircle at the primary position
          (additional clone circles are drawn directly into the axes for
          symmetry / mirror copies — they are removed by clearing all circles
          whose line objects are tagged as 'VrApClone')
          self.A.VrApMirL : Line2D mirror axis (if mirror enabled)
          self.A.VrApMirP : InteractivePoint drag handle on mirror axis
        """
        ax = self.Fig.Dfrn.ax
        b0 = self.B0
        r = float(self.VrApR.value())
        nsym = int(self.VrApSymm.currentData() or 1)
        mirror = self.VrApMirror.isChecked()
        mirr_ang = float(self.VrApMirrRot.value())

        _remove_vr_annotations()

        # Remove leftover clone circles from a previous draw
        for ln in list(ax.lines):
            if getattr(ln, '_vrAp_clone', False):
                ln.remove()

        # Primary aperture — draggable, resizable
        xy = np.asarray(self.P.VrApXY, dtype=float)
        self.A.VrAp = InteractiveCircle(
            axis=ax,
            center=xy,
            radius=r,
            color='w',
            interactions='all'
        )
        self.A.VrAp.connect()
        self.A.VrAp.updateCircle.connect(lambda: moveVrAp())

        # Rotational symmetry clones (k = 1 … nsym-1)
        theta_circ = np.linspace(0, 2 * np.pi, 361)
        for k in range(1, nsym):
            rot_ang = 360.0 * k / nsym
            cloned_ctr = _rotate_pt(xy, rot_ang, b0)
            cx = cloned_ctr[0] + r * np.cos(theta_circ)
            cy = cloned_ctr[1] + r * np.sin(theta_circ)
            ln, = ax.plot(cx, cy, color='w', linewidth=1.0,
                          linestyle='--', zorder=5)
            ln._vrAp_clone = True  # mark for cleanup

        # Mirror copies (reflect each symmetry position across the mirror line)
        if mirror:
            for k in range(nsym):
                rot_ang = 360.0 * k / nsym
                orig_ctr = _rotate_pt(xy, rot_ang, b0)
                mir_ctr = _mirror_pt(orig_ctr, mirr_ang, b0)
                cx = mir_ctr[0] + r * np.cos(theta_circ)
                cy = mir_ctr[1] + r * np.sin(theta_circ)
                ln, = ax.plot(cx, cy, color='w', linewidth=1.0,
                              linestyle=':', zorder=5)
                ln._vrAp_clone = True

            # Mirror axis line across the diffraction-pattern extent
            axis_len = max(self.D.NPxX, self.D.NPxY)
            rad_m = np.radians(mirr_ang)
            self.A.VrApMirL, = ax.plot(
                [b0[0] - axis_len * np.cos(rad_m),
                 b0[0] + axis_len * np.cos(rad_m)],
                [b0[1] - axis_len * np.sin(rad_m),
                 b0[1] + axis_len * np.sin(rad_m)],
                color='#AAAAAA', linewidth=1.0, linestyle='--', zorder=4
            )

            # Drag handle to rotate the mirror line
            mirr_tip_x = b0[0] + 0.6 * self.P.RMax * np.cos(rad_m)
            mirr_tip_y = b0[1] + 0.6 * self.P.RMax * np.sin(rad_m)
            pt_art = ax.scatter(mirr_tip_x, mirr_tip_y,
                                color='#AAAAAA', s=50, zorder=8)
            self.A.VrApMirP = InteractivePoint(pt_art)
            self.A.VrApMirP.connect()
            self.A.VrApMirP.positionChanged.connect(lambda: moveVrAp())

        self.Fig.Dfrn.canvas.draw_idle()

    # ------------------------------------------------------------------
    # move — handle interactive changes
    # ------------------------------------------------------------------

    def moveVrAp():
        """
        Respond to any change in the virtual aperture parameters.

        Senders handled:
          self.A.VrAp       — circle dragged/resized
          self.A.VrApMirP   — mirror axis handle dragged
          self.VrApR        — radius spinbox
          self.VrApSymm     — symmetry combobox
          self.VrApInvert   — invert checkbox
          self.VrApMirror   — mirror checkbox
          self.VrApMirrRot / VrApMirrRot_NF — mirror angle
        """
        b0 = self.B0

        # --- sync primary circle → UI fields (if annotation was dragged) ---
        if (self.A.VrAp is not None
                and self.sender() is self.A.VrAp):
            new_ctr = self.A.VrAp.center.copy()
            new_r = float(self.A.VrAp.radius[0])

            self.P.VrApXY = new_ctr

            self.VrApR.blockSignals(True)
            self.VrApR.setValue(new_r)
            self.VrApR.blockSignals(False)

        # --- sync mirror-drag handle → mirror-angle UI ---
        elif (self.A.VrApMirP is not None
              and self.sender() is self.A.VrApMirP):
            xy = self.A.VrApMirP.position
            new_ang = float(
                np.degrees(np.arctan2(xy[1] - b0[1], xy[0] - b0[0]))
            ) % 180.0  # mirror angle is defined mod 180°
            self.VrApMirrRot.blockSignals(True)
            self.VrApMirrRot_NF.blockSignals(True)
            self.VrApMirrRot.setValue(int(round(new_ang)))
            self.VrApMirrRot_NF.setValue(new_ang)
            self.VrApMirrRot.blockSignals(False)
            self.VrApMirrRot_NF.blockSignals(False)

        # --- sync radius spinbox → stored position ---
        elif self.sender() is self.VrApR:
            pass  # VrApXY unchanged; radius read fresh in calcVrAp

        # Redraw with updated values
        drawVrAp()

        # --- compute image ---
        if _toUpdateImage():
            if isDiffToPrev(self, 'VrAp',
                            [list(self.P.VrApXY),
                             self.VrApR.value(),
                             self.VrApSymm.currentData(),
                             self.VrApInvert.isChecked(),
                             self.VrApMirror.isChecked(),
                             self.VrApMirrRot.value()]):
                calcVrAp()
            plotImage(self, 'Real')

    # ------------------------------------------------------------------
    # calcVrAp — build the mask and compute the virtual image
    # ------------------------------------------------------------------

    def calcVrAp():
        """
        Build the combined virtual aperture mask and compute the real-space image.

        Steps:
          1. For each rotational symmetry copy (k = 0 … nsym-1):
               a. Rotate the primary aperture centre around B0
               b. Add a circle mask at that position
          2. If mirror is enabled: reflect all centres and add more circles
          3. Optionally invert the mask
          4. Dot-product the boolean mask with self.Data → one value per scan pixel
          5. Store result as self.Fig.Real.Image
        """
        b0 = self.B0
        r = float(self.VrApR.value())
        nsym = int(self.VrApSymm.currentData() or 1)
        invert = self.VrApInvert.isChecked()
        mirror = self.VrApMirror.isChecked()
        mirr_ang = float(self.VrApMirrRot.value())
        xy = np.asarray(self.P.VrApXY, dtype=float)
        shape = (self.D.NPxX, self.D.NPxY)

        # Collect all aperture centre positions
        centres = []
        for k in range(nsym):
            rot_ang = 360.0 * k / nsym
            centres.append(_rotate_pt(xy, rot_ang, b0))

        if mirror:
            mirrored = [_mirror_pt(c, mirr_ang, b0) for c in centres]
            centres.extend(mirrored)

        # Build union mask (shape: NPxX × NPxY, then flattened)
        mask = np.zeros(shape, dtype=bool)
        for ctr in centres:
            mask |= _circle_mask(ctr, r, shape)

        if invert:
            mask = ~mask

        mask_flat = mask.flatten()   # (NPxX*NPxY,)

        if not mask_flat.any():
            self.Fig.Real.Image = np.zeros((self.D.NFrY, self.D.NFrX),
                                           dtype=self.D.DataType)
            return

        # Virtual image: sum intensity within mask per scan position
        # self.Data shape: (NFrX*NFrY, NPxX*NPxY)
        virtual = self.Data[:, mask_flat].sum(axis=1)   # (NFrX*NFrY,)
        self.Fig.Real.Image = virtual.reshape(self.D.NFrY, self.D.NFrX)

        # Store the mask for display in the DfrnMask window
        self.Fig.DfrnMask.Image = mask.astype(self.D.DataType)

    # ------------------------------------------------------------------
    # helper: should we recompute the image now?
    # ------------------------------------------------------------------

    def _toUpdateImage():
        calc = self.SettingsWindow.CalcPolicy.currentData()
        return (calc == 2) or (self.sender() in [self.UpdateImages,
                                                 self.DetrMode])

    # ------------------------------------------------------------------
    # Main dispatch
    # ------------------------------------------------------------------

    match self.sender():
        case self.DetrMode:
            # Entering VrApMod: draw the aperture and compute for the first time
            drawVrAp()
            calcVrAp()
            plotImage(self, 'Real')

        case (self.VrApR | self.VrApSymm | self.VrApInvert
              | self.VrApMirror | self.VrApMirrRot | self.VrApMirrRot_NF):
            moveVrAp()

        case self.A.VrAp | self.A.VrApMirP:
            moveVrAp()

        case self.UpdateImages:
            calcVrAp()
            plotImage(self, 'Real')

        case _:
            # Fallback: treat any unrecognised sender as a redraw trigger
            moveVrAp()
