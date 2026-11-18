from callbacks.axis_direction import axisDirectionCallbacks
from callbacks.plotting import plotImage, toUpdateImage
from callbacks.utils import isDiffToPrev, refreshCanvas
from callbacks.window_manager import enableWindows
from annotationsClasses.interactiveAnnulus import InteractiveAnnulus
from annotationsClasses.interactivePoint import InteractivePoint
import numpy as np
from callbacks.layout import dfrn_shape, real_shape
from callbacks.signals import all_signals_blocked, signals_blocked  # noqa: E402
from callbacks import compute  # noqa: E402
from callbacks.compute.backend import _TORCH_AVAILABLE  # noqa: E402,F401  (monkeypatched by tests)


# ---------------------------------------------------------------------------
# Thin object-based wrappers around callbacks.compute, kept for the GPU tests
# and for code that still calls them with an app-like object
# ---------------------------------------------------------------------------


def integrateAnnular(obj, mask):
    """Sum the intensity within *mask* for every probe position.

    ``obj.D.Data`` is the ``(N_pos, N_pix)`` dataset and ``obj.D.GPU`` the CUDA
    device (or *None* for CPU).  Returns an array of shape ``(N_pos,)``.
    See :func:`callbacks.compute.masked_sum`.
    """
    return compute.masked_sum(obj.D.Data, mask, getattr(obj.D, "GPU", None))


def calcCoM(obj, mask, cx, cy):
    """Intensity-weighted centre of mass within *mask* for every probe position.

    *cx*, *cy* are the X and Y coordinate grids of the diffraction pixels.
    Returns ``(com_x, com_y)``, each of shape ``(N_pos,)``.
    See :func:`callbacks.compute.weighted_mean_position`.
    """
    return compute.weighted_mean_position(obj.D.Data, mask, cx, cy, getattr(obj.D, "GPU", None))


def annularDetectorCallbacks(self):

    def limitAnnUI():
        """Update annular detector UI limits/labels when coordinate options change."""
        with signals_blocked(self.AnnRi_NF, self.AnnRo_NF):
            self.AnnRi_NF.setSuffix(" " + self.SettingsWindow.DCUnit.currentData())
            self.AnnRo_NF.setSuffix(" " + self.SettingsWindow.DCUnit.currentData())
            # radii are whole rings (annWidth pixels each): the range is RMax rings and one step is one
            # ring, in the display unit.  (The range left out annWidth and was overwritten in pixels
            # on import, and a quarter-pixel step rounded back to the same ring, so the arrows
            # barely moved and then stuck.)
            ring = self.D.annWidth * self.DfPxR
            for box in (self.AnnRi_NF, self.AnnRo_NF):
                box.setRange(0, self.P.NRings * ring)
                box.setSingleStep(ring)
            ri, ro = self.AnnRi.value()             # and the values in the (possibly new) unit
            self.AnnRi_NF.setValue(ri * ring)
            self.AnnRo_NF.setValue(ro * ring)

    def enableAnnUI():
        """Enable/disable UI elements based on current detector mode."""
        dmod = self.DetrMode.currentData()

        # Segmented panel only active in DPC mode
        self.dpcControls.setEnabled(dmod == "DPCMod")

        # The scan-direction panel is available in CoM/DPC modes.  The unlock
        # button sits inside that panel, so the panel itself must stay enabled
        # for the button to be clickable; only the controls it guards follow
        # its checked state.
        in_com = dmod in ["CoMMod", "DPCMod"]
        unlocked = in_com and self.ScanDirUnlock.isChecked()
        self.comControls.setEnabled(in_com)
        self.ScanDirUnlock.setEnabled(in_com)
        self.AutoCurl.setEnabled(in_com)
        for ctrl in (self.ScanDir, self.ScanDir_NF, self.ScanDirYFlip):
            ctrl.setEnabled(unlocked)

        # Highlight scan direction panel if not yet aligned
        if (dmod in ["CoMMod", "DPCMod"]) and (not self.P.ScanDirInit):
            bc = self.C.WarnC.name()
        else:
            bc = self.C.BgC.name()
        self.comControls.setStyleSheet("background-color:" + bc)

    # ------------------------------------------------------------------
    # drawSegDetr — segmented-detector annotations on the diffraction pattern
    # ------------------------------------------------------------------
    def drawSegDetr():
        """
        Draw (or move) the segmented detector overlay on the diffraction pattern.

          self.A.SegDetrL  : list of Line2D — one per segment divider
          self.A.SegDetrL0 : Line2D — the thicker reference divider at DetRot
          self.A.SegDetrCir: list of Line2D — the NRung-1 interior circles
          self.A.SegDetrP0 : InteractivePoint — rotation handle at the outer tip of the reference line

        Existing artists are updated in place (the handle may be the one being dragged: replacing it
        would end the drag); only a change of the number of segments/rungs makes new lines.
        """
        ax = self.Fig.Dfrn.ax
        ri_idx, ro_idx = self.AnnRi.value()
        ri_px = ri_idx * self.D.annWidth
        ro_px = ro_idx * self.D.annWidth
        nseg = int(self.NSeg.value())
        nrung = int(self.NRung.value())
        dr = self.DetRot.value()          # degrees
        b0 = np.asarray(self.B0, float)   # (x, y) beam centre in pixels

        seg_angles = np.radians(np.linspace(dr, dr + 360.0, nseg + 1)[:-1])
        rung_radii = np.linspace(ri_px, ro_px, nrung + 1)[1:-1] if nrung > 1 else np.array([])
        theta = np.linspace(0, 2 * np.pi, 361)

        def spoke(a):
            return ([b0[0] + ri_px * np.cos(a), b0[0] + ro_px * np.cos(a)],
                    [b0[1] + ri_px * np.sin(a), b0[1] + ro_px * np.sin(a)])

        if len(self.A.SegDetrL or []) != nseg or len(self.A.SegDetrCir or []) != len(rung_radii) \
                or self.A.SegDetrL0 is None:
            removeSegDetr(self, keep_handle=True)
            self.A.SegDetrL = [ax.plot([], [], color='w', linewidth=1.5, zorder=5, solid_capstyle='round')[0]
                               for _ in range(nseg)]
            self.A.SegDetrL0, = ax.plot([], [], color='w', linewidth=3.0, zorder=5, solid_capstyle='round')
            self.A.SegDetrCir = [ax.plot([], [], color='w', linewidth=1.0, zorder=5)[0] for _ in rung_radii]
        for line, a in zip(self.A.SegDetrL, seg_angles):
            line.set_data(*spoke(a))
        self.A.SegDetrL0.set_data(*spoke(np.radians(dr)))
        for circ, r in zip(self.A.SegDetrCir, rung_radii):
            circ.set_data(b0[0] + r * np.cos(theta), b0[1] + r * np.sin(theta))

        tip = b0 + ro_px * np.array([np.cos(np.radians(dr)), np.sin(np.radians(dr))])
        if self.A.SegDetrP0 is None:
            pt_artist = ax.scatter(tip[0], tip[1], color='w', s=60, zorder=6, animated=False)
            self.A.SegDetrP0 = InteractivePoint(pt_artist)
            self.A.SegDetrP0.connect()
            # dragging the handle turns the detector; the dividers and rings follow it while dragged
            self.A.SegDetrP0.companions = lambda: segArtists(self, handle=False)
            self.A.SegDetrP0.positionChanged.connect(lambda: moveAnnDetr())
        elif not self.A.SegDetrP0.dragging:
            self.A.SegDetrP0.point.set_offsets([tip])
        if self.A.adf is not None:
            self.A.adf.companions = lambda: segArtists(self) if self.DetrMode.currentData() == "DPCMod" else []

        refreshCanvas(self.Fig.Dfrn.canvas, self.A.adf, self.A.SegDetrP0)

    # ------------------------------------------------------------------
    # drawScanDir — scan-direction arrows on the diffraction pattern
    # ------------------------------------------------------------------
    def drawScanDir():
        """
        Draw (or move) the scan X/Y direction arrows used to align the scan direction.

        Two arrows from the beam centre along the scan X and Y axes, each labelled and with a drag
        handle at its tip.  Dragging the X handle sets ScanDir; dragging the Y handle sets
        ScanDir from its angle less 90° (or plus, with Y flipped).  Updated in place: replacing a
        handle while it is dragged would end the drag, and the labels were added anew on every
        change, piling up on the pattern.
        """
        ax = self.Fig.Dfrn.ax
        sd = self.ScanDir.value()      # scan rotation in degrees
        syf = 1 - 2 * self.ScanDirYFlip.isChecked()   # Y flip: +1 or -1
        b0 = np.asarray(self.B0, float)
        arrow_len = max(20.0, 0.25 * self.P.RMax)
        tips = {"X": b0 + arrow_len * np.array([np.cos(np.radians(sd)), np.sin(np.radians(sd))]),
                "Y": b0 + arrow_len * np.array([np.cos(np.radians(sd + 90.0 * syf)),
                                                 np.sin(np.radians(sd + 90.0 * syf))])}
        colours = {"X": '#FF8C00', "Y": '#00BFFF'}

        for k in ("X", "Y"):
            tip, colour = tips[k], colours[k]
            line = getattr(self.A, f"ScanDir{k}line")
            if line is None:
                line, = ax.plot([], [], color=colour, linewidth=2.0, zorder=7, solid_capstyle='round')
                setattr(self.A, f"ScanDir{k}line", line)
            line.set_data([b0[0], tip[0]], [b0[1], tip[1]])
            label = getattr(self.A, f"ScanDir{k}text")
            if label is None:
                label = ax.text(0, 0, k, color=colour, fontsize=8, fontweight='bold', zorder=8,
                                ha='center', va='center')
                setattr(self.A, f"ScanDir{k}text", label)
            label.set_position(tuple(b0 + 1.15 * (tip - b0)))       # just beyond the handle
            handle = getattr(self.A, f"ScanDir{k}circ")
            if handle is None:
                pt = ax.scatter(tip[0], tip[1], color=colour, s=50, zorder=9, animated=False)
                handle = InteractivePoint(pt)
                handle.connect()
                handle.companions = lambda: scanArtists(self)
                handle.positionChanged.connect(lambda: moveAnnDetr())
                setattr(self.A, f"ScanDir{k}circ", handle)
            elif not handle.dragging:
                handle.point.set_offsets([tip])

        refreshCanvas(self.Fig.Dfrn.canvas, self.A.ScanDirXcirc, self.A.ScanDirYcirc)

    # ------------------------------------------------------------------
    # moveAnnDetr — live-update detectors when parameters change
    # ------------------------------------------------------------------
    def moveAnnDetr():

        def moveAnnR():
            """Update annular/round detector radii."""
            innerRadius, outerRadius = self.AnnRi.value()
            scale = self.DfPxR

            match self.sender():
                case self.A.adf:
                    innerRadius, outerRadius = (
                        self.A.adf.radius / self.D.annWidth
                    ).astype(int)
                case self.AnnRi_NF:
                    innerRadius = round(
                        self.AnnRi_NF.value() / self.D.annWidth / scale
                    )
                case self.AnnRo_NF:
                    outerRadius = round(
                        self.AnnRo_NF.value() / self.D.annWidth / scale
                    )

            # Swap if inner > outer (user dragged past each other)
            if innerRadius > outerRadius:
                innerRadius, outerRadius = outerRadius, innerRadius

            innerRadius = max(0, innerRadius)
            outerRadius = min(self.P.NRings, outerRadius)

            # Block signals to avoid update loops
            with signals_blocked(self.AnnRi, self.AnnRi_NF, self.AnnRo_NF):
                self.AnnRi.setValue((innerRadius, outerRadius))
                self.AnnRi_NF.setValue(innerRadius * self.D.annWidth * scale)
                self.AnnRo_NF.setValue(outerRadius * self.D.annWidth * scale)

            # Sync the InteractiveAnnulus if the sender was not the annotation
            if self.sender() is not self.A.adf:
                self.A.adf.radius = (
                    np.array([innerRadius, outerRadius])
                    .clip(np.finfo(np.single).eps, self.P.NRings)
                    * self.D.annWidth
                )
                self.A.adf.redraw()

            # Refresh real-space image
            if len(self.Fig.Real.ax.images) == 0:
                self.Fig.Real.Image = self.Data.sum(axis=1).reshape(real_shape(self.D))
                plotImage(self, 'Real')
            # otherwise the image follows in moveAnnDetr, when the calculation policy allows
            # (this used to update it unconditionally and show it without brightness/contrast)

            self.ImageAx.Real.autoscale()
            self.Fig.Real.canvas.draw()

            # the DPC segments span the annulus: they follow its radii
            if self.DetrMode.currentData() == "DPCMod":
                drawSegDetr()

        def moveSeg():
            """
            Update segmented detector geometry.

            If the sender is SegDetrP0 (the drag handle), derive the new
            DetRot from the handle's position, update the UI, then redraw.
            Otherwise just redraw with the current UI values.
            """
            # If drag handle moved → compute new rotation from point position
            if (self.A.SegDetrP0 is not None
                    and self.sender() is self.A.SegDetrP0):
                xy = self.A.SegDetrP0.position  # (x, y) in data coords
                b0 = self.B0
                new_rot = float(
                    np.degrees(np.arctan2(xy[1] - b0[1], xy[0] - b0[0]))
                ) % 360.0

                with signals_blocked(self.DetRot, self.DetRot_NF):
                    self.DetRot.setValue(int(round(new_rot)))
                    self.DetRot_NF.setValue(new_rot)

            # Redraw all SegDetr annotations with updated parameters
            drawSegDetr()

        def moveScan():
            """
            Live-update scan direction from drag handle or UI spinner.

            If the sender is ScanDirXcirc: derive new ScanDir from the angle
            of that handle relative to B0.
            If the sender is ScanDirYcirc: derive ScanDir = angle - 90° (corrected
            for the Y-flip setting, since the Y arrow is always perpendicular to X).
            Then redraw both arrows with the updated ScanDir value.
            """
            b0 = self.B0
            syf = 1 - 2 * self.ScanDirYFlip.isChecked()

            if (self.A.ScanDirXcirc is not None
                    and self.sender() is self.A.ScanDirXcirc):
                # X handle moved: its angle is the new ScanDir
                xy = self.A.ScanDirXcirc.position
                new_sd = float(
                    np.degrees(np.arctan2(xy[1] - b0[1], xy[0] - b0[0]))
                ) % 360.0
                with signals_blocked(self.ScanDir, self.ScanDir_NF):
                    self.ScanDir.setValue(int(round(new_sd)))
                    self.ScanDir_NF.setValue(new_sd)

            elif (self.A.ScanDirYcirc is not None
                  and self.sender() is self.A.ScanDirYcirc):
                # Y handle moved: its angle is ScanDir + 90*syf → subtract to get ScanDir
                xy = self.A.ScanDirYcirc.position
                y_ang = float(
                    np.degrees(np.arctan2(xy[1] - b0[1], xy[0] - b0[0]))
                )
                new_sd = (y_ang - 90.0 * syf) % 360.0
                with signals_blocked(self.ScanDir, self.ScanDir_NF):
                    self.ScanDir.setValue(int(round(new_sd)))
                    self.ScanDir_NF.setValue(new_sd)

            # Redraw scan direction arrows with updated angle
            drawScanDir()

        # --- dispatch ---
        dmod = self.DetrMode.currentData()
        ri, ro = self.AnnRi.value()
        dr = self.DetRot.value()
        sd = self.ScanDir.value()
        syf = 1 - 2 * self.ScanDirYFlip.isChecked()

        match self.sender():
            case self.A.adf | self.AnnRi | self.AnnRi_NF | self.AnnRo_NF:
                moveAnnR()
            case (self.DetRot | self.DetRot_NF | self.NRung | self.NSeg
                  | self.A.SegDetrCir | self.A.SegDetrL
                  | self.A.SegDetrL0 | self.A.SegDetrP0):
                moveSeg()
            case (self.ScanDirUnlock | self.ScanDirYFlip
                  | self.ScanDir | self.ScanDir_NF
                  | self.A.ScanDirXline | self.A.ScanDirYline
                  | self.A.ScanDirXcirc | self.A.ScanDirYcirc):
                moveScan()
            case self.DetrMode | self.UpdateImages:
                moveAnnR()
                if self.ScanDirUnlock.isChecked():
                    moveScan()

        # --- image updates ---
        if toUpdateImage(self):
            # Recompute BF/DF only if annular radii changed
            if isDiffToPrev(self, 'AnnR', [ri, ro]):
                # 2D distance matrix is recalculated in integrateAnnular;
                # here just recompute the real-space image from cached adfImages
                mask_ann = compute.annular_mask(self.A.k, ri, ro)
                self.Fig.DfrnMask.Image = mask_ann.astype(self.D.DataType)
                self.Fig.Real.Image = self.adfImages[
                    :, :, ri: ro + 1
                ].sum(axis=2)

            # CoM or DPC computation
            if dmod in ["CoMMod", "DPCMod"]:
                # everything the CoM/DPC images depend on, including the mode itself
                if isDiffToPrev(self, 'CoM_P', [dmod, ri, ro, sd, syf, dr,
                                                self.NSeg.value(), self.NRung.value()]):
                    if dmod == "CoMMod":
                        calcCoM(ri, ro, sd, syf)
                    else:                        # DPCMod
                        calcDPC(ri, ro, dr, sd, syf)

            plotAllPatterns()

    # ------------------------------------------------------------------
    # drawAnnDetr — initialise the annular detector annotations
    # ------------------------------------------------------------------
    def drawAnnDetr():
        """Initialise the annular detector InteractiveAnnulus annotation."""
        c = self.B0
        r1 = self.AnnRi.value()[0] * self.D.annWidth
        r2 = self.AnnRi.value()[1] * self.D.annWidth

        if self.A.adf is None:
            self.A.adf = InteractiveAnnulus(self.Fig.Dfrn.ax, c, r1, r2, color='r')
            self.A.adf.connect()
            self.A.adf.updateCircle.connect(lambda: moveAnnDetr())

    # ------------------------------------------------------------------
    # integrateAnnular — build the adfImages cube
    # ------------------------------------------------------------------
    def integrateAnnular():
        """
        Build self.adfImages: (NFrY, NFrX, n_rings) cube of annular integrals.
        Only rerun when the transmitted-beam centre or the ring width (Annular Integration Step)
        changes; the detector radii keep their size in pixels when the ring width changes.
        """
        old_width = self.Prev.annWidth
        width_changed = isDiffToPrev(self, "annWidth", float(self.D.annWidth))
        if isDiffToPrev(self, "B0", self.B0) or width_changed:
            # ring number of every pixel, (NPxY, NPxX), and the integral of
            # every ring for every probe position
            self.A.k = compute.radial_index(dfrn_shape(self.D), self.B0, self.D.annWidth)
            k = self.A.k
            self.adfImages = compute.ring_integrals(self.Data, k, self.D.GPU).reshape(
                self.D.NFrY, self.D.NFrX, -1
            )

            self.P.NRings = int(k.max())
            self.Prev.AnnR = self.Prev.CoM_P = None         # images from the old rings are stale

            # Update UI slider limits (and keep the radii in pixels when the ring width changed)
            with all_signals_blocked(self):
                ri, ro = self.AnnRi.value()
                self.AnnRi.setMaximum(self.P.NRings)
                if width_changed and old_width:
                    scale = float(old_width) / float(self.D.annWidth)
                    ri, ro = int(round(ri * scale)), int(round(ro * scale))
                self.AnnRi.setValue((min(ri, self.P.NRings), min(ro, self.P.NRings)))
            limitAnnUI()
            if self.A.adf is not None:              # the rings drawn on the pattern
                ri, ro = self.AnnRi.value()
                self.A.adf.radius = np.array([ri, ro], float).clip(np.finfo(np.single).eps) * self.D.annWidth
                self.A.adf.redraw()

    # ------------------------------------------------------------------
    # calcCoM — intensity-weighted centre-of-mass calculation (CoMMod)
    # ------------------------------------------------------------------
    def calcCoM(ri, ro, sd, syf):
        """
        Compute CoM X/Y deflection images and derived iCoM/dCoM.

        Parameters
        ----------
        ri, ro : int
            Inner and outer annular radii indices (in units of annWidth).
        sd : float
            Scan-direction rotation angle in degrees.
        syf : int
            Y-flip factor: +1 (no flip) or -1 (flipped).
        """
        mask = compute.annular_mask(self.A.k, ri, ro)
        if not mask.any():
            return

        com_x, com_y = compute.center_of_mass(self.Data, mask, self.B0, self.D.GPU)
        com_x, com_y = compute.rotate_field(com_x, com_y * syf, sd)   # into the scan frame
        setDeflectionImages(com_x, com_y)

    def setDeflectionImages(fx, fy):
        """Store a per-frame deflection field and every image derived from it."""
        shape = real_shape(self.D)
        self.Fig.CoMX.Image = np.asarray(fx).reshape(shape)
        self.Fig.CoMY.Image = np.asarray(fy).reshape(shape)
        self.Fig.CoMMag.Image, self.Fig.CoMPh.Image = compute.magnitude_phase(
            self.Fig.CoMX.Image, self.Fig.CoMY.Image)
        # phase shaded by magnitude: the phase image, its opacity set from CoMMag in plotImage
        self.Fig.CoMPhMag.Image = self.Fig.CoMPh.Image.copy()
        integratedImages(self)      # iCoM and dCoM, with the bandpass filter (Settings > Windows)

    # ------------------------------------------------------------------
    # calcDPC — segment-integral DPC calculation (DPCMod)
    # ------------------------------------------------------------------
    def calcDPC(ri, ro, dr, sd, syf):
        """
        Compute DPC X/Y deflection images from segmented-detector integrals.

        The annulus is divided into NRung rings and NSeg wedges (first wedge at
        rotation dr).  Each segment's integrated intensity is assigned to the
        segment's nominal centre of mass, giving a coarse-grained centre of mass
        in pixels (see compute.segment_weights).  The field is then taken into
        the scan frame exactly as for CoM.

        Results are stored in the same Fig.CoMX / CoMY / CoMMag / CoMPh slots so
        the existing plotAllPatterns() and display pipeline work without changes.

        Parameters
        ----------
        ri, ro : int
            Annular radii indices.
        dr : float
            Detector rotation angle in degrees.
        sd : float
            Scan-direction rotation angle in degrees.
        syf : int
            Y-flip factor: +1 (no flip) or -1 (flipped).
        """
        ann_mask = compute.annular_mask(self.A.k, ri, ro)
        if not ann_mask.any():
            return

        weights = compute.segment_weights(
            ann_mask, self.B0,
            ri * self.D.annWidth, ro * self.D.annWidth,
            int(self.NSeg.value()), int(self.NRung.value()), dr,
        )
        dpc_x, dpc_y = compute.segmented_dpc(self.Data, weights, self.D.GPU)
        dpc_x, dpc_y = compute.rotate_field(dpc_x, dpc_y * syf, sd)   # into the scan frame
        setDeflectionImages(dpc_x, dpc_y)

    # ------------------------------------------------------------------
    # autoCurl — scan direction from the curl of the deflection field (MATLAB's AutoCurl)
    # ------------------------------------------------------------------
    def autoCurl():
        """Set the scan direction and Y flip that make the CoM/DPC field curl-free, recompute the
        images and close the scan-direction alignment (as MATLAB Quant4D's "Auto" button)."""
        from callbacks.utils import notifDLG
        from callbacks.window_manager import busyIndicator
        dmod = self.DetrMode.currentData()
        if dmod not in ("CoMMod", "DPCMod"):
            return
        ri, ro = self.AnnRi.value()
        dr, sd = self.DetRot.value(), float(self.ScanDir.value())
        syf = 1 - 2 * self.ScanDirYFlip.isChecked()

        def compute_field(sd, syf):
            if dmod == "CoMMod":
                calcCoM(ri, ro, sd, syf)
            else:
                calcDPC(ri, ro, dr, sd, syf)
            # remember what the images now show (the next update need not recompute them)
            isDiffToPrev(self, 'CoM_P', [dmod, ri, ro, sd, syf, dr, self.NSeg.value(), self.NRung.value()])

        from PyQt5 import QtCore as qtc, QtWidgets as qtw
        qtw.QApplication.setOverrideCursor(qtc.Qt.CursorShape.WaitCursor)
        try:
            with busyIndicator(self):
                if self.Fig.CoMX.Image is None or isDiffToPrev(
                        self, 'CoM_P', [dmod, ri, ro, sd, syf, dr, self.NSeg.value(), self.NRung.value()]):
                    compute_field(sd, syf)
                if self.Fig.CoMX.Image is None:
                    return
                # back to the detector frame: undo the current rotation and Y flip
                u, v = compute.rotate_field(self.Fig.CoMX.Image, self.Fig.CoMY.Image, -sd)
                try:
                    angle, flip, _ = compute.scan_rotation_by_curl(u, v * syf, prefer_deg=sd)
                except ValueError as exc:
                    notifDLG(self, self, "warn", f"The scan direction could not be estimated: {exc}\n"
                                                 "Try changing the detector and repeating.",
                             "Automatic Curl Minimization Failed")
                    return
                with signals_blocked(self.ScanDir, self.ScanDir_NF, self.ScanDirYFlip):
                    self.ScanDir.setValue(angle)
                    self.ScanDir_NF.setValue(angle)
                    self.ScanDirYFlip.setChecked(flip)
                compute_field(angle, 1 - 2 * flip)
        finally:
            qtw.QApplication.restoreOverrideCursor()

        # the alignment is done: lock the scan direction again
        self.P.ScanDirInit = 1
        if self.ScanDirUnlock.isChecked():
            with signals_blocked(self.ScanDirUnlock):
                self.ScanDirUnlock.setChecked(False)
            from callbacks.startup import unlockScanDir
            unlockScanDir(self)
        removeScanDir(self)
        enableAnnUI()
        plotAllPatterns()
        axisDirectionCallbacks(self, ("Dfrn",))

    # ------------------------------------------------------------------
    # plotAllPatterns — refresh visible image windows
    # ------------------------------------------------------------------
    def plotAllPatterns():
        """Refresh the primary, mask, and (if in CoM/DPC mode) CoM images."""
        ids = [
            iID
            for iType, iID in zip(self.G.ImgType, self.G.ImgID)
            if iType in ["Primary", "Mask"]
        ]
        if self.DetrMode.currentData() in ["CoMMod", "DPCMod"]:
            ids += [
                iID
                for iType, iID in zip(self.G.ImgType, self.G.ImgID)
                if (iID != "ColorWheel") and (iType == "CoM")
            ]
        for id in ids:
            if self.Fig[id].isVisible():
                plotImage(self, id)

    # ------------------------------------------------------------------
    # Main dispatch
    # ------------------------------------------------------------------
    if self.blockAllSignals:
        return

    b0 = self.B0
    dmod = self.DetrMode.currentData()

    match self.sender():
        case self.SettingsWindow.DCSys | self.SettingsWindow.DCPos | self.SettingsWindow.DCUnit:
            limitAnnUI()
        case self.DetrMode:
            limitAnnUI()
            self.ScanDirUnlock.setChecked(False)
            enableAnnUI()
            integrateAnnular()
            if dmod in ("CoMMod", "DPCMod") and not self.P.CoMRadiusInit:
                # first CoM/DPC visit with this dataset: the detector starts at the centre (inner radius 0)
                self.P.CoMRadiusInit = True
                with signals_blocked(self.AnnRi):
                    self.AnnRi.setValue((0, self.AnnRi.value()[1]))
                limitAnnUI()
            drawAnnDetr()
            if dmod == "DPCMod":
                drawSegDetr()
            moveAnnDetr()
            enableWindows(self, True)
        case (self.AnnRi | self.AnnRi_NF | self.AnnRo_NF
              | self.DetRot | self.DetRot_NF | self.NSeg | self.NRung
              | self.ScanDir | self.ScanDir_NF | self.ScanDirYFlip
              | self.UpdateImages):
            moveAnnDetr()
            if self.sender() in (self.ScanDir, self.ScanDir_NF, self.ScanDirYFlip):
                axisDirectionCallbacks(self, ("Dfrn",))     # scan-direction arrows
        case self.AutoCurl:
            autoCurl()
        case self.AnnStep:      # new ring width: integrate again, the detector keeps its size
            integrateAnnular()
            if dmod == "DPCMod":
                drawSegDetr()
            moveAnnDetr()
        case self.ScanDirUnlock:
            self.P.ScanDirInit = 1
            enableAnnUI()
            removeScanDir(self)
            if self.ScanDirUnlock.isChecked():
                drawScanDir()
            axisDirectionCallbacks(self, ("Dfrn",))     # scan arrows hide while aligning


# ------------------------------------------------------------------
# Module-level helpers
# ------------------------------------------------------------------


def segArtists(self, handle=True) -> list:
    """The segmented-detector artists (dividers, reference divider, rung circles[, handle])."""
    arts = list(self.A.SegDetrL or []) + [self.A.SegDetrL0] + list(self.A.SegDetrCir or [])
    if handle and self.A.SegDetrP0 is not None:
        arts.append(self.A.SegDetrP0.point)
    return [a for a in arts if a is not None]


def scanArtists(self) -> list:
    """The scan-direction arrows, labels and both handles (each handle blits the others)."""
    arts = [self.A.ScanDirXline, self.A.ScanDirYline, self.A.ScanDirXtext, self.A.ScanDirYtext]
    arts += [h.point for h in (self.A.ScanDirXcirc, self.A.ScanDirYcirc) if h is not None]
    return [a for a in arts if a is not None]


def _removeArtist(art) -> None:
    try:
        art.remove()
    except (ValueError, AttributeError, NotImplementedError):
        pass


def removeSegDetr(self, keep_handle=False) -> None:
    """Remove the segmented-detector overlay (and its rotation handle unless *keep_handle*)."""
    for line in list(self.A.SegDetrL or []) + list(self.A.SegDetrCir or []) + [self.A.SegDetrL0]:
        if line is not None:
            _removeArtist(line)
    self.A.SegDetrL = self.A.SegDetrCir = self.A.SegDetrL0 = None
    if not keep_handle and self.A.SegDetrP0 is not None:
        self.A.SegDetrP0.remove()
        self.A.SegDetrP0 = None


def removeScanDir(self) -> None:
    """Remove the scan-direction arrows, their labels and handles."""
    for k in ("X", "Y"):
        for kind in ("line", "text"):
            art = getattr(self.A, f"ScanDir{k}{kind}")
            if art is not None:
                _removeArtist(art)
                setattr(self.A, f"ScanDir{k}{kind}", None)
        handle = getattr(self.A, f"ScanDir{k}circ")
        if handle is not None:
            handle.remove()
            setattr(self.A, f"ScanDir{k}circ", None)


def annStepChanged(self) -> None:
    """Annular Integration Step (mrad) edited: the ring width in pixels; in Annular/CoM/DPC modes the
    annular images are integrated again (in Alignment mode that happens on leaving it)."""
    if self.blockAllSignals or self.Data is None:
        return
    mrad_per_px = float(self.mradPx.value())
    if mrad_per_px <= 0:
        return
    self.D.annWidth = float(self.AnnStep.value()) / mrad_per_px
    if self.DetrMode.currentData() in ("AnnMod", "CoMMod", "DPCMod"):
        annularDetectorCallbacks(self)


def placeAnnStep(self, dmod) -> None:
    """The Annular Integration Step sits on the Alignment tab in Alignment mode (to be set before the
    annular images are computed) and on the Annular/CoM/DPC tab otherwise, as in MATLAB."""
    panel = self.AnnStepPanel
    if dmod == "AlignMod":
        target = _alignmentStepLayout(self)
        if target.indexOf(panel) == -1:
            target.addWidget(panel)
    elif dmod in ("AnnMod", "CoMMod", "DPCMod"):
        target = self.AnnularDetectorTab.layout()
        if target.indexOf(panel) == -1:
            target.insertWidget(target.indexOf(self.annularControls) + 1, panel)


def _alignmentStepLayout(self):
    """The layout holding the Alignment tab's help icon (and, in Alignment mode, the step)."""
    from PyQt5 import QtWidgets as qtw
    for lay in self.AlignmentTab.findChildren(qtw.QHBoxLayout):
        if lay.indexOf(self.AlignmentHelpIcon) != -1:
            return lay
    raise LookupError("Alignment tab layout with the help icon not found")


# ------------------------------------------------------------------
# iCoM / dCoM bandpass filter (Settings > Windows)
# ------------------------------------------------------------------
def bandpassLimits(self) -> tuple:
    """(low, high) of the iCoM/dCoM bandpass filter, pixels of the scan's Fourier transform."""
    sw = self.SettingsWindow
    lo, hi = sw.BandpassFilterLow.value(), sw.BandpassFilterHigh.value()
    return min(lo, hi), max(lo, hi)


def integratedImages(self) -> None:
    """iCoM and dCoM (iDPC/dDPC) from the CoM X/Y images, bandpass-filtered as set."""
    fx, fy = self.Fig.CoMX.Image, self.Fig.CoMY.Image
    if fx is None or fy is None:
        return
    lo, hi = bandpassLimits(self)
    self.Fig.iCoM.Image = compute.fourier_bandpass(compute.integrate_field(fx, fy), lo, hi)
    self.Fig.dCoM.Image = compute.fourier_bandpass(compute.divergence(fx, fy), lo, hi)


def resetBandpass(self) -> None:
    """New dataset: the filter keeps every spatial frequency of the scan (0 .. the corner of its FFT)."""
    from callbacks.layout import real_shape
    ny, nx = real_shape(self.D)
    kmax = int(np.ceil(np.hypot(nx // 2, ny // 2)))
    sw = self.SettingsWindow
    with signals_blocked(sw.BandpassFilter, sw.BandpassFilterLow, sw.BandpassFilterHigh):
        for w in (sw.BandpassFilterLow, sw.BandpassFilterHigh):
            w.setRange(0, kmax)
        sw.BandpassFilter.setRange(0, kmax)
        sw.BandpassFilter.setValue((0, kmax))
        sw.BandpassFilterLow.setValue(0)
        sw.BandpassFilterHigh.setValue(kmax)


def bandpassCallbacks(self, source=None) -> None:
    """Range slider and spin boxes kept in step; iCoM/dCoM recomputed from the stored CoM images."""
    from callbacks.plotting import plotImage
    sw = self.SettingsWindow
    source = source if source is not None else self.sender()
    with signals_blocked(sw.BandpassFilter, sw.BandpassFilterLow, sw.BandpassFilterHigh):
        if source is sw.BandpassFilter:
            lo, hi = sw.BandpassFilter.value()
            sw.BandpassFilterLow.setValue(int(lo))
            sw.BandpassFilterHigh.setValue(int(hi))
        else:
            lo, hi = bandpassLimits(self)
            sw.BandpassFilter.setValue((lo, hi))
            sw.BandpassFilterLow.setValue(lo)
            sw.BandpassFilterHigh.setValue(hi)
    if self.DetrMode.currentData() in ("CoMMod", "DPCMod") and self.Fig.CoMX.Image is not None:
        integratedImages(self)
        for id in ("iCoM", "dCoM"):
            if self.Fig[id].isVisible():
                plotImage(self, id)


def connectBandpass(self) -> None:
    sw = self.SettingsWindow
    sw.BandpassFilter.valueChanged.connect(lambda *_: bandpassCallbacks(self))
    sw.BandpassFilterLow.valueChanged.connect(lambda *_: bandpassCallbacks(self))
    sw.BandpassFilterHigh.valueChanged.connect(lambda *_: bandpassCallbacks(self))
