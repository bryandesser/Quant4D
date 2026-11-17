from callbacks.allFunctions import enableWindows, plotImage, isDiffToPrev
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
            self.AnnRi_NF.setRange(0, self.P.RMax * self.DfPxR)
            self.AnnRo_NF.setRange(0, self.P.RMax * self.DfPxR)
            self.AnnRi_NF.setSingleStep(0.25 * self.DfPxR)
            self.AnnRo_NF.setSingleStep(0.25 * self.DfPxR)

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
        for ctrl in (self.ScanDir, self.ScanDir_NF, self.ScanDirYFlip):
            ctrl.setEnabled(unlocked)

        # Highlight scan direction panel if not yet aligned
        if (dmod in ["CoMMod", "DPCMod"]) and (not self.P.ScanDirInit):
            bc = self.C.WarnC.name()
        else:
            bc = self.C.BgC.name()
        self.comControls.setStyleSheet("background-color:" + bc)

    # ------------------------------------------------------------------
    # drawSegDetr — draw segmented-detector annotations on diffraction ax
    # ------------------------------------------------------------------
    def drawSegDetr():
        """
        Draw segmented detector overlay on the diffraction pattern.

        Creates:
          self.A.SegDetrL  : list of Line2D objects — one per segment divider
          self.A.SegDetrL0 : Line2D — highlighted reference line at DetRot=0
          self.A.SegDetrCir: list of Line2D objects — NRung-1 interior circles
          self.A.SegDetrP0 : InteractivePoint — drag handle at outer tip of ref line
        """
        ax = self.Fig.Dfrn.ax

        # --- remove existing SegDetr annotations ---
        for attr in ('SegDetrL', 'SegDetrCir'):
            obj = getattr(self.A, attr)
            if obj is not None:
                for item in obj:
                    try:
                        item.remove()
                    except ValueError:
                        pass
                setattr(self.A, attr, None)
        for attr in ('SegDetrL0',):
            obj = getattr(self.A, attr)
            if obj is not None:
                try:
                    obj.remove()
                except ValueError:
                    pass
                setattr(self.A, attr, None)
        if self.A.SegDetrP0 is not None:
            self.A.SegDetrP0.remove()
            self.A.SegDetrP0 = None

        # --- read current parameters ---
        ri_idx, ro_idx = self.AnnRi.value()
        ri_px = ri_idx * self.D.annWidth
        ro_px = ro_idx * self.D.annWidth
        nseg = int(self.NSeg.value())
        nrung = int(self.NRung.value())
        dr = self.DetRot.value()          # degrees
        b0 = self.B0                      # (x, y) beam centre in pixels

        if ro_px <= 0:
            return  # nothing to draw yet

        # --- segment divider lines (NSeg lines from inner to outer radius) ---
        seg_angles = np.linspace(dr, dr + 360.0, nseg + 1)[:-1]  # NSeg angles
        lines = []
        for ang in seg_angles:
            rad = np.radians(ang)
            x = [b0[0] + ri_px * np.cos(rad), b0[0] + ro_px * np.cos(rad)]
            y = [b0[1] + ri_px * np.sin(rad), b0[1] + ro_px * np.sin(rad)]
            line, = ax.plot(x, y, color='w', linewidth=1.5, zorder=5,
                            solid_capstyle='round')
            lines.append(line)
        self.A.SegDetrL = lines if lines else None

        # --- highlighted reference line at DetRot (thicker, used as rotation origin) ---
        rad0 = np.radians(dr)
        x0 = [b0[0] + ri_px * np.cos(rad0), b0[0] + ro_px * np.cos(rad0)]
        y0 = [b0[1] + ri_px * np.sin(rad0), b0[1] + ro_px * np.sin(rad0)]
        self.A.SegDetrL0, = ax.plot(x0, y0, color='w', linewidth=3.0,
                                    zorder=5, solid_capstyle='round')

        # --- interior rung circles (NRung > 1 → NRung-1 concentric rings) ---
        rung_circles = []
        if nrung > 1:
            rung_radii = np.linspace(ri_px, ro_px, nrung + 1)[1:-1]
            theta = np.linspace(0, 2 * np.pi, 361)
            for r in rung_radii:
                cx = b0[0] + r * np.cos(theta)
                cy = b0[1] + r * np.sin(theta)
                circ, = ax.plot(cx, cy, color='w', linewidth=1.0, zorder=5)
                rung_circles.append(circ)
        self.A.SegDetrCir = rung_circles if rung_circles else None

        # --- interactive rotation handle at outer tip of reference line ---
        pt_artist = ax.scatter(
            b0[0] + ro_px * np.cos(rad0),
            b0[1] + ro_px * np.sin(rad0),
            color='w', s=60, zorder=6, animated=False
        )
        self.A.SegDetrP0 = InteractivePoint(pt_artist)
        self.A.SegDetrP0.connect()
        # When drag handle moves → update detector rotation and redraw
        self.A.SegDetrP0.positionChanged.connect(lambda: moveAnnDetr())

        self.Fig.Dfrn.canvas.draw_idle()

    # ------------------------------------------------------------------
    # drawScanDir — draw scan-direction arrows on diffraction pattern
    # ------------------------------------------------------------------
    def drawScanDir():
        """
        Draw scan X/Y direction indicators on the diffraction pattern.

        Two arrows (Line2D) emanate from the beam centre along the scan X
        and Y axes; each has an InteractivePoint drag handle at its tip.
        Dragging the X handle updates ScanDir; dragging the Y handle updates
        ScanDir – 90° (since Y is always perpendicular to X).

        Annotations stored:
          self.A.ScanDirXline  : Line2D — X-direction arrow
          self.A.ScanDirYline  : Line2D — Y-direction arrow
          self.A.ScanDirXcirc  : InteractivePoint — drag handle at X tip
          self.A.ScanDirYcirc  : InteractivePoint — drag handle at Y tip
        """
        ax = self.Fig.Dfrn.ax

        # --- remove existing scan-direction annotations ---
        for attr in ('ScanDirXline', 'ScanDirYline'):
            obj = getattr(self.A, attr)
            if obj is not None:
                try:
                    obj.remove()
                except ValueError:
                    pass
                setattr(self.A, attr, None)
        for attr in ('ScanDirXcirc', 'ScanDirYcirc'):
            obj = getattr(self.A, attr)
            if obj is not None:
                obj.remove()
                setattr(self.A, attr, None)

        # --- parameters ---
        sd = self.ScanDir.value()      # scan rotation in degrees
        syf = 1 - 2 * self.ScanDirYFlip.isChecked()   # Y flip: +1 or -1
        b0 = self.B0                   # beam centre (x, y)
        # Arrow length: 25% of max scattering radius, min 20 px
        arrow_len = max(20.0, 0.25 * self.P.RMax * self.D.annWidth)

        rad_x = np.radians(sd)
        rad_y = np.radians(sd + 90.0 * syf)

        # Tip positions
        tip_x = np.array([b0[0] + arrow_len * np.cos(rad_x),
                          b0[1] + arrow_len * np.sin(rad_x)])
        tip_y = np.array([b0[0] + arrow_len * np.cos(rad_y),
                          b0[1] + arrow_len * np.sin(rad_y)])

        # --- X-direction line (orange) ---
        self.A.ScanDirXline, = ax.plot(
            [b0[0], tip_x[0]], [b0[1], tip_x[1]],
            color='#FF8C00', linewidth=2.0, zorder=7,
            solid_capstyle='round'
        )
        ax.annotate('X', xy=(tip_x[0], tip_x[1]),
                    color='#FF8C00', fontsize=8, zorder=8,
                    ha='center', va='center')

        # --- Y-direction line (cyan) ---
        self.A.ScanDirYline, = ax.plot(
            [b0[0], tip_y[0]], [b0[1], tip_y[1]],
            color='#00BFFF', linewidth=2.0, zorder=7,
            solid_capstyle='round'
        )
        ax.annotate('Y', xy=(tip_y[0], tip_y[1]),
                    color='#00BFFF', fontsize=8, zorder=8,
                    ha='center', va='center')

        # --- Drag handle: X tip ---
        pt_x = ax.scatter(tip_x[0], tip_x[1],
                          color='#FF8C00', s=50, zorder=9, animated=False)
        self.A.ScanDirXcirc = InteractivePoint(pt_x)
        self.A.ScanDirXcirc.connect()
        self.A.ScanDirXcirc.positionChanged.connect(lambda: moveAnnDetr())

        # --- Drag handle: Y tip ---
        pt_y = ax.scatter(tip_y[0], tip_y[1],
                          color='#00BFFF', s=50, zorder=9, animated=False)
        self.A.ScanDirYcirc = InteractivePoint(pt_y)
        self.A.ScanDirYcirc.connect()
        self.A.ScanDirYcirc.positionChanged.connect(lambda: moveAnnDetr())

        self.Fig.Dfrn.canvas.draw_idle()

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
            outerRadius = min(self.P.RMax, outerRadius)

            # Block signals to avoid update loops
            with signals_blocked(self.AnnRi, self.AnnRi_NF, self.AnnRo_NF):
                self.AnnRi.setValue((innerRadius, outerRadius))
                self.AnnRi_NF.setValue(innerRadius * self.D.annWidth * scale)
                self.AnnRo_NF.setValue(outerRadius * self.D.annWidth * scale)

            # Sync the InteractiveAnnulus if the sender was not the annotation
            if self.sender() is not self.A.adf:
                self.A.adf.radius = (
                    np.array([innerRadius, outerRadius])
                    .clip(np.finfo(np.single).eps, self.P.RMax)
                    * self.D.annWidth
                )
                self.A.adf.redraw()

            # Refresh real-space image
            if len(self.Fig.Real.ax.images) == 0:
                self.Fig.Real.Image = self.Data.sum(axis=1).reshape(real_shape(self.D))
                self.ImageAx.Real = self.Fig.Real.ax.imshow(self.Fig.Real.Image)
            else:
                self.Fig.Real.Image = self.adfImages[
                    :, :, innerRadius: outerRadius + 1
                ].sum(axis=2)
                self.ImageAx.Real.set_data(self.Fig.Real.Image)

            self.ImageAx.Real.autoscale()
            self.Fig.Real.canvas.draw()

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
        Only rerun when the transmitted-beam centre changes.
        """
        if isDiffToPrev(self, "B0", self.B0):
            # ring number of every pixel, (NPxY, NPxX), and the integral of
            # every ring for every probe position
            self.A.k = compute.radial_index(dfrn_shape(self.D), self.B0, self.D.annWidth)
            k = self.A.k
            self.adfImages = compute.ring_integrals(self.Data, k, self.D.GPU).reshape(
                self.D.NFrY, self.D.NFrX, -1
            )

            # Update UI slider limits
            with all_signals_blocked(self):
                self.AnnRi.setMaximum(k.max())
                self.AnnRi_NF.setMaximum(k.max() * self.D.annWidth)
                self.AnnRo_NF.setMaximum(k.max() * self.D.annWidth)

            self.P.RMax = k.max()

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
        self.Fig.iCoM.Image = compute.integrate_field(self.Fig.CoMX.Image, self.Fig.CoMY.Image)
        self.Fig.dCoM.Image = compute.divergence(self.Fig.CoMX.Image, self.Fig.CoMY.Image)

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
        case self.SettingsWindow.DCSys:
            limitAnnUI()
        case self.DetrMode:
            limitAnnUI()
            self.ScanDirUnlock.setChecked(False)
            enableAnnUI()
            integrateAnnular()
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
        case self.ScanDirUnlock:
            self.P.ScanDirInit = 1
            enableAnnUI()
            # Remove any existing scan-direction annotations before redrawing
            for attr in ('ScanDirXline', 'ScanDirYline'):
                obj = getattr(self.A, attr)
                if obj is not None:
                    try:
                        obj.remove()
                    except ValueError:
                        pass
                    setattr(self.A, attr, None)
            for attr in ('ScanDirXcirc', 'ScanDirYcirc'):
                obj = getattr(self.A, attr)
                if obj is not None:
                    obj.remove()
                    setattr(self.A, attr, None)
            if self.ScanDirUnlock.isChecked():
                drawScanDir()
            self.SettingsWindow.ShowDfrnAxes.click()


# ------------------------------------------------------------------
# Module-level helpers
# ------------------------------------------------------------------

def toUpdateImage(self):
    """
    Return True if images should be recomputed now.

    Rules:
      calc == 2  → always update (active policy)
      calc == 1  → reduced (not yet implemented; treated as always)
      sender is UpdateImages or DetrMode → manual trigger
    """
    calc = self.SettingsWindow.CalcPolicy.currentData()
    return (calc == 2) or (self.sender() in [self.UpdateImages, self.DetrMode])
