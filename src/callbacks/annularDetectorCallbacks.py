from callbacks.allFunctions import enableWindows, plotImage, isDiffToPrev
from annotationsClasses.interactiveAnnulus import InteractiveAnnulus
from annotationsClasses.interactivePoint import InteractivePoint
import numpy as np
try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False


def annularDetectorCallbacks(self):

    def limitAnnUI():
        """Update annular detector UI limits/labels when coordinate options change."""
        self.AnnRi_NF.blockSignals(True)
        self.AnnRo_NF.blockSignals(True)
        self.AnnRi_NF.setSuffix(" " + self.SettingsWindow.DCUnit.currentData())
        self.AnnRo_NF.setSuffix(" " + self.SettingsWindow.DCUnit.currentData())
        self.AnnRi_NF.setRange(0, self.P.RMax * self.DfPxR)
        self.AnnRo_NF.setRange(0, self.P.RMax * self.DfPxR)
        self.AnnRi_NF.setSingleStep(0.25 * self.DfPxR)
        self.AnnRo_NF.setSingleStep(0.25 * self.DfPxR)
        self.AnnRi_NF.blockSignals(False)
        self.AnnRo_NF.blockSignals(False)

    def enableAnnUI():
        """Enable/disable UI elements based on current detector mode."""
        dmod = self.DetrMode.currentData()

        # Segmented panel only active in DPC mode
        self.dpcControls.setEnabled(dmod == "DPCMod")

        # Scan direction controls follow the unlock checkbox
        self.comControls.setEnabled(self.ScanDirUnlock.isChecked())
        self.ScanDirUnlock.setEnabled(dmod in ["CoMMod", "DPCMod"])

        # Highlight scan direction panel if not yet aligned
        if (dmod in ["CoMMod", "DPCMod"]) and (not self.P.ScanDirInit):
            bc = self.C.WarnC.name()
        else:
            bc = self.C.BgC.name()
        self.ScanDirGrid.setStyleSheet("background-color:" + bc)
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
            self.AnnRi.blockSignals(True)
            self.AnnRi_NF.blockSignals(True)
            self.AnnRo_NF.blockSignals(True)

            self.AnnRi.setValue((innerRadius, outerRadius))
            self.AnnRi_NF.setValue(innerRadius * self.D.annWidth * scale)
            self.AnnRo_NF.setValue(outerRadius * self.D.annWidth * scale)

            self.AnnRi.blockSignals(False)
            self.AnnRi_NF.blockSignals(False)
            self.AnnRo_NF.blockSignals(False)

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
                self.Image.Real = self.Data.sum(axis=1).reshape(
                    self.D.NFrY, self.D.NFrX
                )
                self.ImageAx.Real = self.Fig.Real.ax.imshow(self.Image.Real)
            else:
                self.Image.Real = self.adfImages[
                    :, :, innerRadius: outerRadius + 1
                ].sum(axis=2)
                self.ImageAx.Real.set_data(self.Image.Real)

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

                self.DetRot.blockSignals(True)
                self.DetRot_NF.blockSignals(True)
                self.DetRot.setValue(int(round(new_rot)))
                self.DetRot_NF.setValue(new_rot)
                self.DetRot.blockSignals(False)
                self.DetRot_NF.blockSignals(False)

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
                self.ScanDir.blockSignals(True)
                self.ScanDir_NF.blockSignals(True)
                self.ScanDir.setValue(int(round(new_sd)))
                self.ScanDir_NF.setValue(new_sd)
                self.ScanDir.blockSignals(False)
                self.ScanDir_NF.blockSignals(False)

            elif (self.A.ScanDirYcirc is not None
                  and self.sender() is self.A.ScanDirYcirc):
                # Y handle moved: its angle is ScanDir + 90*syf → subtract to get ScanDir
                xy = self.A.ScanDirYcirc.position
                y_ang = float(
                    np.degrees(np.arctan2(xy[1] - b0[1], xy[0] - b0[0]))
                )
                new_sd = (y_ang - 90.0 * syf) % 360.0
                self.ScanDir.blockSignals(True)
                self.ScanDir_NF.blockSignals(True)
                self.ScanDir.setValue(int(round(new_sd)))
                self.ScanDir_NF.setValue(new_sd)
                self.ScanDir.blockSignals(False)
                self.ScanDir_NF.blockSignals(False)

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
                mask_ann = (self.A.k >= ri) & (self.A.k <= ro)
                self.Image.DfrnMask = mask_ann.astype(self.D.DataType).T
                self.Image.Real = self.adfImages[
                    :, :, ri: ro + 1
                ].sum(axis=2)

            # CoM or DPC computation
            if dmod in ["CoMMod", "DPCMod"]:
                if isDiffToPrev(self, 'CoM_P', [ri, ro, sd, syf, dr]):
                    if dmod == "CoMMod":
                        calcCoM(ri, ro, sd, syf)
                    else:                        # DPCMod
                        calcDPC(ri, ro, dr)

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
            self.A.adf = InteractiveAnnulus(
                center=c, radius=(r1, r2),
                axis=self.Fig.Dfrn.ax,
                color='r', interactions='resize'
            )
            self.A.adf.connect()
            self.A.adf.updateAnnulus.connect(lambda: moveAnnDetr())

    # ------------------------------------------------------------------
    # integrateAnnular — build the adfImages cube
    # ------------------------------------------------------------------
    def integrateAnnular():
        """
        Build self.adfImages: (NFrY, NFrX, n_rings) cube of annular integrals.
        Only rerun when the transmitted-beam centre changes.
        """
        if isDiffToPrev(self, "B0", self.B0):
            xgrid, ygrid = np.ogrid[
                -self.B0[0]: self.D.NPxX - self.B0[0],
                -self.B0[1]: self.D.NPxY - self.B0[1],
            ]
            self.A.k = np.int32(
                np.sqrt(xgrid ** 2 + ygrid ** 2) / self.D.annWidth
            )
            k = self.A.k.flatten()

            distance = np.arange(0, k.max() + 1)
            adfMask = np.where(
                (k.reshape(1, len(k)) >= distance.reshape(len(distance), 1))
                & (k.reshape(1, len(k)) < distance.reshape(len(distance), 1) + 0.5),
                True,
                False,
            ).T

            # GPU path: use torch CUDA tensor for the large matrix multiply
            if _TORCH_AVAILABLE and self.D.GPU is not None and torch.cuda.is_available():
                device = torch.device(self.D.GPU)
                Data_t = torch.from_numpy(np.ascontiguousarray(self.Data)).to(device, dtype=torch.float32)
                adfMask_t = torch.from_numpy(np.ascontiguousarray(adfMask)).to(device, dtype=torch.float32)
                self.adfImages = (Data_t @ adfMask_t).cpu().numpy()
                del Data_t, adfMask_t
            else:
                self.adfImages = self.Data @ adfMask
            self.adfImages = np.reshape(
                self.adfImages, (self.D.NFrY, self.D.NFrX, -1)
            )

            # Update UI slider limits
            self.blockAllSignals = True
            self.AnnRi.setMaximum(k.max())
            self.AnnRi_NF.setMaximum(k.max() * self.D.annWidth)
            self.AnnRo_NF.setMaximum(k.max() * self.D.annWidth)
            self.blockAllSignals = False

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
        def integrateCoM():
            """Tikhonov-regularised Fourier integration of CoM → iCoM phase."""
            ny, nx = self.Fig.CoMX.Image.shape
            kx = np.fft.fftfreq(nx)
            ky = np.fft.fftfreq(ny)
            KX, KY = np.meshgrid(kx, ky)
            k2 = KX ** 2 + KY ** 2
            k2[0, 0] = 1.0  # prevent /0; DC → 0 after IFFT

            FCoMX = np.fft.fft2(self.Fig.CoMX.Image)
            FCoMY = np.fft.fft2(self.Fig.CoMY.Image)

            # Fourier integration: phase = IFFT[(kx·FCoMX + ky·FCoMY) / (2πi·k²)]
            self.Fig.iCoM.Image = np.fft.ifft2(
                (KX * FCoMX + KY * FCoMY) / (2j * np.pi * k2)
            ).real

            # dCoM: divergence of CoM field
            dCoMX = np.gradient(self.Fig.CoMX.Image, axis=1)
            dCoMY = np.gradient(self.Fig.CoMY.Image, axis=0)
            self.Fig.dCoM.Image = dCoMX + dCoMY

        # Annular mask in diffraction space
        mask = ((self.A.k >= ri) & (self.A.k <= ro)).flatten()
        if not mask.any():
            return

        # Pixel coordinate grids relative to transmitted beam
        xgrid, ygrid = np.mgrid[0: self.D.NPxX, 0: self.D.NPxY]
        xweight = (xgrid.flatten() - self.B0[0]).astype(np.float32)
        yweight = (ygrid.flatten() - self.B0[1]).astype(np.float32)

        # GPU path: move masked data + weight vectors to CUDA for dot products
        if _TORCH_AVAILABLE and self.D.GPU is not None and torch.cuda.is_available():
            device = torch.device(self.D.GPU)
            data_m_t = torch.from_numpy(np.ascontiguousarray(self.Data[:, mask])).to(device, dtype=torch.float32)
            xw_t = torch.from_numpy(xweight[mask]).to(device)
            yw_t = torch.from_numpy(yweight[mask]).to(device)
            norm_t = data_m_t.sum(dim=1).clamp(min=torch.finfo(torch.float32).tiny)
            CoMX_flat = (data_m_t @ xw_t / norm_t).cpu().numpy()
            CoMY_flat = (data_m_t @ yw_t / norm_t).cpu().numpy() * syf
            del data_m_t, xw_t, yw_t, norm_t
        else:
            data_m = self.Data[:, mask].astype(np.float32)   # (NFr, n_masked)
            norm = data_m.sum(axis=1).clip(np.finfo(np.float32).eps, None)
            CoMX_flat = (data_m @ xweight[mask]) / norm
            CoMY_flat = (data_m @ yweight[mask]) / norm * syf

        # Apply scan-direction rotation
        c, s = np.cos(np.radians(sd)), np.sin(np.radians(sd))
        CoM = np.array([[c, -s], [s, c]]) @ np.vstack([CoMX_flat, CoMY_flat])

        self.Fig.CoMX.Image = CoM[0].reshape(self.D.NFrY, self.D.NFrX)
        self.Fig.CoMY.Image = CoM[1].reshape(self.D.NFrY, self.D.NFrX)
        self.Fig.CoMMag.Image = np.hypot(self.Fig.CoMX.Image, self.Fig.CoMY.Image)
        self.Fig.CoMPh.Image = np.arctan2(self.Fig.CoMY.Image, self.Fig.CoMX.Image)

        integrateCoM()

    # ------------------------------------------------------------------
    # calcDPC — segment-integral DPC calculation (DPCMod)
    # ------------------------------------------------------------------
    def calcDPC(ri, ro, dr):
        """
        Compute DPC X/Y deflection images from segmented-detector integrals.

        For NSeg segments at rotation dr, each segment subtends 360/NSeg degrees.
        The DPC vector is the cos/sin-weighted sum of per-segment intensities,
        normalised by the total annular intensity — analogous to CoM but discrete.

        Results are stored in the same Fig.CoMX / CoMY / CoMMag / CoMPh slots so
        the existing plotAllPatterns() and display pipeline work without changes.

        Parameters
        ----------
        ri, ro : int
            Annular radii indices.
        dr : float
            Detector rotation angle in degrees.
        """
        nseg = int(self.NSeg.value())
        nrung = int(self.NRung.value())

        # Annular mask (combined across all rungs)
        ann_mask = ((self.A.k >= ri) & (self.A.k <= ro)).flatten()
        if not ann_mask.any():
            return

        # Pixel angle map (degrees, 0–360), computed relative to beam centre
        xgrid, ygrid = np.mgrid[0: self.D.NPxX, 0: self.D.NPxY]
        px_angle = np.degrees(
            np.arctan2(
                ygrid.flatten() - self.B0[1],
                xgrid.flatten() - self.B0[0],
            )
        ) % 360.0  # (NPx,) in [0, 360)

        # Build radial rung boundaries in pixel units
        ri_px = ri * self.D.annWidth
        ro_px = ro * self.D.annWidth
        rung_edges = np.linspace(ri_px, ro_px, nrung + 1)   # nrung+1 edges

        # Pixel radial distance (continuous, in pixel units)
        px_radius = np.sqrt(
            (xgrid.flatten() - self.B0[0]) ** 2
            + (ygrid.flatten() - self.B0[1]) ** 2
        )

        # Segment angular boundaries (degrees, in [dr, dr+360))
        seg_width = 360.0 / nseg
        seg_starts = np.array([dr + i * seg_width for i in range(nseg)]) % 360.0

        # Accumulate DPC X/Y deflection across all rung × segment combinations
        DPC_X = np.zeros(self.D.NFrY * self.D.NFrX, dtype=np.float32)
        DPC_Y = np.zeros(self.D.NFrY * self.D.NFrX, dtype=np.float32)
        norm = np.zeros(self.D.NFrY * self.D.NFrX, dtype=np.float32)

        for rung_i in range(nrung):
            r_lo = rung_edges[rung_i]
            r_hi = rung_edges[rung_i + 1]
            rung_mask = (px_radius >= r_lo) & (px_radius < r_hi)

            for seg_i in range(nseg):
                # Mid-angle of this segment (pointing direction)
                mid_ang_deg = (seg_starts[seg_i] + 0.5 * seg_width) % 360.0
                mid_ang_rad = np.radians(mid_ang_deg)
                cos_w = np.cos(mid_ang_rad)
                sin_w = np.sin(mid_ang_rad)

                # Angular mask: pixels whose angle falls within this segment
                ang_lo = seg_starts[seg_i]
                ang_hi = (ang_lo + seg_width) % 360.0

                if ang_lo < ang_hi:
                    ang_mask = (px_angle >= ang_lo) & (px_angle < ang_hi)
                else:
                    # Segment wraps through 0°
                    ang_mask = (px_angle >= ang_lo) | (px_angle < ang_hi)

                # Combined mask: annulus ∩ rung ∩ segment
                seg_mask = ann_mask & rung_mask & ang_mask

                if not seg_mask.any():
                    continue

                # Segment integral for every scan position:  (NFr,)
                if _TORCH_AVAILABLE and self.D.GPU is not None and torch.cuda.is_available():
                    device = torch.device(self.D.GPU)
                    seg_t = torch.from_numpy(np.ascontiguousarray(
                        self.Data[:, seg_mask])).to(device, dtype=torch.float32)
                    seg_sum = seg_t.sum(dim=1).cpu().numpy()
                    del seg_t
                else:
                    data_seg = self.Data[:, seg_mask].astype(np.float32)
                    seg_sum = data_seg.sum(axis=1)  # (NFr,)

                # Weighted contribution to DPC vector
                DPC_X += cos_w * seg_sum
                DPC_Y += sin_w * seg_sum
                norm += seg_sum

        # Normalise — avoid /0 at pixels with zero total intensity
        eps = np.finfo(np.float32).eps
        safe_norm = norm.clip(eps, None)
        DPC_X /= safe_norm
        DPC_Y /= safe_norm

        # Reshape to real-space images and store in the shared CoM slots
        self.Fig.CoMX.Image = DPC_X.reshape(self.D.NFrY, self.D.NFrX)
        self.Fig.CoMY.Image = DPC_Y.reshape(self.D.NFrY, self.D.NFrX)
        self.Fig.CoMMag.Image = np.hypot(self.Fig.CoMX.Image, self.Fig.CoMY.Image)
        self.Fig.CoMPh.Image = np.arctan2(self.Fig.CoMY.Image, self.Fig.CoMX.Image)

        # iCoM/dCoM from the DPC field (same Fourier integration as for CoM)
        ny, nx = self.D.NFrY, self.D.NFrX
        kx = np.fft.fftfreq(nx)
        ky = np.fft.fftfreq(ny)
        KX, KY = np.meshgrid(kx, ky)
        k2 = KX ** 2 + KY ** 2
        k2[0, 0] = 1.0
        FDPC_X = np.fft.fft2(self.Fig.CoMX.Image)
        FDPC_Y = np.fft.fft2(self.Fig.CoMY.Image)
        self.Fig.iCoM.Image = np.fft.ifft2(
            (KX * FDPC_X + KY * FDPC_Y) / (2j * np.pi * k2)
        ).real
        dDPC_X = np.gradient(self.Fig.CoMX.Image, axis=1)
        dDPC_Y = np.gradient(self.Fig.CoMY.Image, axis=0)
        self.Fig.dCoM.Image = dDPC_X + dDPC_Y

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
        case self.DCSys:
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
