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
  VrApR          : aperture radius slider, diffraction pixels
  VrApR_NF       : the radius in the display unit (px or mrad)
  VrApX/Y(_NF)   : aperture centre in the current coordinate system (Settings →
                   detector coordinates): Cartesian X/Y relative to the reference
                   point, or polar distance/angle about the beam centre
  VrApReset      : back onto the transmitted beam, with its radius
  VrApSymm       : n-fold rotational symmetry count (1, 2, 3, 4, 6)
  VrApInvert     : invert mask (complement) — virtual dark-field
  VrApMirror     : add mirror-reflected copy of the full aperture set
  VrApMirrRot    : angle of the mirror line through the beam centre (degrees)
  VrApMirrRot_NF : numerical-field companion to VrApMirrRot
  VrApRotStep    : step size of the rotation buttons VrApRotCW / VrApRotCCW

Annotation attributes (self.A.*)
---------------------------------
  VrAp     : InteractiveCircle — primary aperture (and clones drawn beside it)
  VrApMirL : Line2D — mirror-symmetry axis line
  VrApMirP : InteractivePoint — drag handle to rotate the mirror line
"""

from annotationsClasses.interactiveCircle import InteractiveCircle
from annotationsClasses.interactivePoint import InteractivePoint
import numpy as np
from callbacks.layout import dfrn_shape, real_shape
from callbacks import compute  # noqa: E402
from callbacks.signals import signals_blocked  # noqa: E402


def _polar(self) -> bool:
    return self.SettingsWindow.DCSys.currentText() == "Polar"


def vrApToControls(self, xy) -> tuple[float, float]:
    """Aperture centre (pixels) -> the two values shown in VrApX/Y (current coordinate system)."""
    s = float(self.DfPxR)
    if _polar(self):
        d = np.asarray(xy, float) - np.asarray(self.B0, float)
        return float(np.hypot(*d) * s), float(np.degrees(np.arctan2(d[1], d[0])))
    d = np.asarray(xy, float) - np.asarray(self.RB0, float)
    return float(d[0] * s), float(d[1] * s)


def vrApFromControls(self, a: float, b: float) -> np.ndarray:
    """Inverse of :func:`vrApToControls`, clamped to the diffraction pattern."""
    s = float(self.DfPxR)
    if _polar(self):
        xy = np.asarray(self.B0, float) + a / s * np.array([np.cos(np.radians(b)), np.sin(np.radians(b))])
    else:
        xy = np.asarray(self.RB0, float) + np.array([a, b]) / s
    ny, nx = dfrn_shape(self.D)
    return np.clip(xy, 0, [nx - 1, ny - 1])


def syncVrApControls(self) -> None:
    """Set the limits, labels, units and values of VrApX/Y/R and their number fields."""
    if self.D is None:
        return
    s = float(self.DfPxR)
    unit = " " + (self.SettingsWindow.DCUnit.currentData() or "px")
    ny, nx = dfrn_shape(self.D)
    if _polar(self):
        rmax = float(np.hypot(nx, ny)) * s
        limits = ((0.0, rmax), (-180.0, 180.0))
        labels, units = ("Distance", "Rotation"), (unit, " °")
    else:
        r0 = np.asarray(self.RB0, float)
        limits = ((-r0[0] * s, (nx - 1 - r0[0]) * s), (-r0[1] * s, (ny - 1 - r0[1]) * s))
        labels, units = ("X", "Y"), (unit, unit)
    values = vrApToControls(self, self.P.VrApXY)
    widgets = (self.VrApX, self.VrApX_NF, self.VrApY, self.VrApY_NF, self.VrApR_NF)
    with signals_blocked(*widgets):
        for k, (slider, field) in enumerate(((self.VrApX, self.VrApX_NF), (self.VrApY, self.VrApY_NF))):
            lo, hi = limits[k]
            for w in (slider, field):
                w.setRange(lo, hi)
                w.setValue(min(max(values[k], lo), hi))
            field.setSuffix(units[k])
            field.setSingleStep(0.25 * s if units[k] != " °" else 1.0)
        self.VrApR_NF.setRange(0, self.VrApR.maximum() * s)
        self.VrApR_NF.setValue(float(self.VrApR.value()) * s)
        self.VrApR_NF.setSuffix(unit)
        self.VrApR_NF.setSingleStep(0.25 * s)
    self.VrApXLabel.setText(labels[0])
    self.VrApYLabel.setText(labels[1])


def virtualApertureCallbacks(self):  # noqa: C901
    from callbacks.plotting import plotImage  # noqa: E402
    from callbacks.utils import isDiffToPrev  # noqa: E402

    if self.blockAllSignals:
        return

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    def _remove_vr_annotations(keep_primary=False, keep_mirror=False):
        """Remove the virtual aperture annotations, except the one being dragged: replacing the
        annotation that is emitting (self.sender()) mid-drag would end the drag, and freeing a
        QObject while it emits crashes."""
        if self.A.VrAp is not None and not keep_primary:
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

        if self.A.VrApMirP is not None and not keep_mirror:
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

    # ------------------------------------------------------------------
    # draw — build fresh annotations
    # ------------------------------------------------------------------

    def drawVrAp(keep_primary=False, keep_mirror=False):
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

        _remove_vr_annotations(keep_primary, keep_mirror)

        # Remove leftover clone circles from a previous draw
        for ln in list(ax.lines):
            if getattr(ln, '_vrAp_clone', False):
                ln.remove()

        # Primary aperture — draggable, resizable (kept as is while it is being dragged)
        xy = np.asarray(self.P.VrApXY, dtype=float)
        if self.A.VrAp is None:
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

            # Drag handle to rotate the mirror line (kept as is while it is being dragged)
            if self.A.VrApMirP is None:
                mirr_tip_x = b0[0] + 0.6 * self.P.RMax * np.cos(rad_m)
                mirr_tip_y = b0[1] + 0.6 * self.P.RMax * np.sin(rad_m)
                pt_art = ax.scatter(mirr_tip_x, mirr_tip_y,
                                    color='#AAAAAA', s=50, zorder=8)
                self.A.VrApMirP = InteractivePoint(pt_art)
                self.A.VrApMirP.connect()
                self.A.VrApMirP.positionChanged.connect(lambda: moveVrAp())
        elif self.A.VrApMirP is not None:       # mirror switched off while its handle was kept
            self.A.VrApMirP.remove()
            self.A.VrApMirP = None

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

            with signals_blocked(self.VrApR):
                self.VrApR.setValue(new_r)

        # --- sync mirror-drag handle → mirror-angle UI ---
        elif (self.A.VrApMirP is not None
              and self.sender() is self.A.VrApMirP):
            xy = self.A.VrApMirP.position
            new_ang = float(
                np.degrees(np.arctan2(xy[1] - b0[1], xy[0] - b0[0]))
            ) % 180.0  # mirror angle is defined mod 180°
            with signals_blocked(self.VrApMirrRot, self.VrApMirrRot_NF):
                self.VrApMirrRot.setValue(int(round(new_ang)))
                self.VrApMirrRot_NF.setValue(new_ang)

        # --- typed/slid position, in the current coordinate system ---
        elif self.sender() in (self.VrApX, self.VrApX_NF, self.VrApY, self.VrApY_NF):
            a = float(self.sender().value()) if self.sender() in (self.VrApX, self.VrApX_NF) else float(self.VrApX_NF.value())
            b = float(self.sender().value()) if self.sender() in (self.VrApY, self.VrApY_NF) else float(self.VrApY_NF.value())
            self.P.VrApXY = vrApFromControls(self, a, b)

        # --- radius typed in the display unit ---
        elif self.sender() is self.VrApR_NF:
            with signals_blocked(self.VrApR):
                self.VrApR.setValue(float(self.VrApR_NF.value()) / float(self.DfPxR))

        # --- back onto the transmitted beam, with its radius ---
        elif self.sender() is self.VrApReset:
            self.P.VrApXY = np.asarray(self.B0, float).copy()
            with signals_blocked(self.VrApR):
                self.VrApR.setValue(float(self.TBR.value()))

        # --- rotation buttons: turn the aperture about the beam centre (clockwise as displayed) ---
        elif self.sender() in (self.VrApRotCW, self.VrApRotCCW):
            from callbacks.axis_direction import clockwise_angle, rotate_about  # noqa: E402
            angle = clockwise_angle(self, float(self.VrApRotStep.currentData()), self.sender() is self.VrApRotCW)
            self.P.VrApXY = rotate_about(np.asarray(self.P.VrApXY, float), b0, angle)

        # --- sync radius spinbox → stored position ---
        elif self.sender() is self.VrApR:
            pass  # VrApXY unchanged; radius read fresh in calcVrAp

        # decide before redrawing: the redraw replaces the annotation that may be self.sender()
        update = _toUpdateImage()

        # Redraw with updated values, keeping whichever annotation is being dragged
        sender = self.sender()
        drawVrAp(keep_primary=sender is self.A.VrAp, keep_mirror=sender is self.A.VrApMirP)
        syncVrApControls(self)

        # --- compute image ---
        if update:
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
        shape = dfrn_shape(self.D)

        # Collect all aperture centre positions
        centres = []
        for k in range(nsym):
            rot_ang = 360.0 * k / nsym
            centres.append(_rotate_pt(xy, rot_ang, b0))

        if mirror:
            mirrored = [_mirror_pt(c, mirr_ang, b0) for c in centres]
            centres.extend(mirrored)

        # Union of all aperture copies, (NPxY, NPxX)
        mask = compute.circles_mask(shape, centres, r)
        if invert:
            mask = ~mask

        if not mask.any():
            self.Fig.Real.Image = np.zeros(real_shape(self.D),
                                           dtype=self.D.DataType)
            return

        # Virtual image: sum intensity within the mask for every probe position
        self.Fig.Real.Image = compute.masked_sum(self.Data, mask, self.D.GPU).reshape(real_shape(self.D))

        # Store the mask for display in the DfrnMask window
        self.Fig.DfrnMask.Image = mask.astype(self.D.DataType)

    # ------------------------------------------------------------------
    # helper: should we recompute the image now?
    # ------------------------------------------------------------------

    def _toUpdateImage():
        from callbacks.plotting import toUpdateImage  # noqa: E402
        return toUpdateImage(self)

    # ------------------------------------------------------------------
    # Main dispatch
    # ------------------------------------------------------------------

    match self.sender():
        case self.DetrMode:
            # Entering VrApMod: draw the aperture and compute for the first time
            drawVrAp()
            syncVrApControls(self)
            calcVrAp()
            plotImage(self, 'Real')

        case (self.VrApR | self.VrApSymm | self.VrApInvert
              | self.VrApMirror | self.VrApMirrRot | self.VrApMirrRot_NF
              | self.VrApRotCW | self.VrApRotCCW
              | self.VrApX | self.VrApX_NF | self.VrApY | self.VrApY_NF | self.VrApR_NF | self.VrApReset):
            moveVrAp()

        case self.A.VrAp | self.A.VrApMirP:
            moveVrAp()

        case self.UpdateImages:
            calcVrAp()
            plotImage(self, 'Real')

        case _:
            # Fallback: treat any unrecognised sender as a redraw trigger
            moveVrAp()
