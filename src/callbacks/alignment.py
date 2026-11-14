"""Transmitted-beam alignment callbacks (auto-align, cross-align)."""
import os
import sys
import traceback
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *
from annotationsClasses.interactiveCircle import InteractiveCircle
from annotationsClasses.interactivePoint import InteractivePoint
try:
    from callbacks.imfindcircles import imfindcircles
except ImportError:
    imfindcircles = None


def transBeamCallbacks(self):
    match self.sender():
        case self.DetrMode:  # Entering mode
            # Create transmitted beam annotation, allow for disk as large as the entire diffraction pattern
            if self.A.tb is None:
                self.A.tb = InteractiveCircle(
                    center=self.B0,
                    radius=self.TBR.value(),
                    axis=self.Fig.Dfrn.ax,
                    color="r",
                    interactions="all")
                self.A.tb.connect()
                self.A.tb.updateCircle.connect(lambda: moveTransBeam(self))
                self.Fig.Dfrn.canvas.draw_idle()
                self.Fig.Dfrn.canvas.flush_events()

            # Select `Dfrn` image and bring window to the front
            self.SettingsWindow.DispImage.setCurrentIndex(self.SettingsWindow.DispImage.findData("Dfrn"))
            self.Fig.Dfrn.activateWindow()

            # If this is the initializing alignment, then do swap byte check and auto-align
            if not self.P.TransBeamInit:
                datasetOptCallbacks(self)  # checks for nans and asks if user wants to swap byteorder
                autoAlign(self)

            enableWindows(self, True)  # Enable windows

        case self.UpdateImages:  # Update images
            # Create a summed image of all diffraction patterns simply for alignment and calibration
            self.Fig.DfrnMask.Image = np.ones(self.D.NPx, self.D.DataType)
            self.Fig.Real.Image = np.reshape(self.Data.sum(axis=1), self.D.NFr)

        case self.TBAutoAlign:  # Auto-align
            autoAlign(self)

        case self.TBCrossAlign:  # Align transmitted beam via two crossed lines
            crossAlign(self)

    # Update dependent variables
    moveTransBeam(self)


def moveTransBeam(self):
    """ Function to sync UIs/ROIs depending on the central beam location """

    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    b0 = np.array([self.TBX.value(), self.TBY.value()])
    r = np.maximum(self.TBR.value(), np.finfo(np.single).eps)
    a = self.Alpha.value()
    mrad_per_px = a / r
    nPix = self.D.NPx

    match self.sender():
        case self.TBX | self.TBX_NF:
            b0[0] = max(1, self.sender().value())  # Force X >= 1
        case self.TBY | self.TBY_NF:
            b0[1] = max(1, self.sender().value())  # Force Y >= 1
        case self.TBR | self.TBR_NF:
            r = self.sender().value()  # Radius
        case self.Alpha:
            a = self.sender().value()
            mrad_per_px = a / r  # Calculate the diffraction scale
        case self.mradPx:
            mrad_per_px = self.sender().value()
            a = mrad_per_px * r  # Manually set the diffraction scale
        case self.A.tb:
            b0 = self.A.tb.center
            r = self.A.tb.radius

    # Restrict transmitted beam location/size
    b0 = b0.clip([1, 1], nPix)
    self.B0 = b0
    self.P.RMax = np.ceil(np.linalg.norm(abs(self.P.DfCtr - b0) + self.P.DfCtr))  # Find the max allowed radius
    r = np.clip(r, np.finfo(np.single).eps, self.P.RMax)  # 0 < r <= RMax

    # avoid triggering a valueChanged loop by blocking signals
    self.blockAllSignals = True

    # Update UI limits
    self.TBR.setRange(0, self.P.RMax)
    self.TBR_NF.setRange(0, self.P.RMax)
    self.AnnRi.setRange(0, self.P.RMax)
    self.VrApR.setRange(0, self.P.RMax)

    # Update UI values
    self.TBR.setValue(r)
    self.TBX.setValue(b0[0])
    self.TBY.setValue(b0[1])
    self.TBR_NF.setValue(r)
    self.TBX_NF.setValue(b0[0])
    self.TBY_NF.setValue(b0[1])
    self.Alpha.setValue(a)
    self.mradPx.setValue(mrad_per_px)

    # Update transmitted beam annotation
    if (self.sender() is not self.A.tb) and (self.A.tb is not None):
        self.A.tb.center = b0
        self.A.tb.radius = np.array([r])
        self.A.tb.redraw()

    # unblock trigger signals
    self.blockAllSignals = False

    detrCoordCallbacks(self)


def autoAlign(self):
    """
    Auto-detect the transmitted beam centre (and radius) using the
    Circular Hough Transform (imfindcircles.py).

    Input pattern
    -------------
    * No real-space ROI active (RealROIShape == 'full'):
        PACBED = sum of ALL probe positions.
    * Real-space ROI active:
        Weighted average over the probe positions selected by the ROI
        (uses self.Fig.RealMask.Image as weights), so e.g. a single
        point ROI gives the pattern of exactly that probe position.

    In either case ``self.Fig.Dfrn.Image`` already holds the correct
    pattern (it is updated whenever the ROI changes), so we read it
    directly rather than re-computing the sum.
    """
    from callbacks.imfindcircles import imfindcircles

    nPx = self.D.NPx           # (height, width) tuple
    rmax_abs = max(1, self.P.RMax)

    # ── Choose the input pattern ──────────────────────────────────────────
    roi_shape = self.RealROIShape.currentData()   # 'full', 'point', …

    if roi_shape == 'full' or self.Fig.Dfrn.Image is None:
        # Full PACBED: sum every probe position
        pacbed = np.nansum(self.Data, axis=0).reshape(nPx).astype(np.float64)
    else:
        # ROI-weighted average: already computed and stored in Fig.Dfrn.Image
        # (shape = nPx, normalised by the number of included probe positions)
        pacbed = np.asarray(self.Fig.Dfrn.Image, dtype=np.float64).reshape(nPx)

    # ── Radius search range ───────────────────────────────────────────────
    tbr = self.TBR.value()
    if tbr > 1:
        # Use ±50 % of the current beam-disc radius, clamped to sensible values
        rmin = max(1, int(np.floor(0.5 * tbr)))
        rmax = min(rmax_abs, int(np.ceil(1.5 * tbr)))
    else:
        # First-time call: search over the central quarter of the pattern
        rmin = 1
        rmax = max(2, int(np.ceil(min(nPx) / 4)))

    if rmax <= rmin:
        rmax = rmin + 1

    # ── Run circle finder ─────────────────────────────────────────────────
    try:
        centers, radii, metric = imfindcircles(
            pacbed, [rmin, rmax],
            ObjectPolarity='bright',
            Method='PhaseCode',
            Sensitivity=0.85,
        )
    except Exception:
        # PhaseCode requires rmax > rmin; fall back to TwoStage if needed
        try:
            centers, radii, metric = imfindcircles(
                pacbed, [rmin, rmax],
                ObjectPolarity='bright',
                Method='TwoStage',
                Sensitivity=0.85,
            )
        except Exception:
            return   # give up gracefully — leave B0/TBR unchanged

    if len(centers) == 0:
        return  # no circle found — leave B0 unchanged

    # Best match: imfindcircles already sorts by descending metric
    cx, cy = float(centers[0, 0]), float(centers[0, 1])
    r = float(radii[0])

    # Clamp to valid pixel range
    cx = np.clip(cx, 1, nPx[1])
    cy = np.clip(cy, 1, nPx[0])
    r = np.clip(r, np.finfo(np.single).eps, rmax_abs)

    self.blockAllSignals = True
    self.TBX.setValue(cx)
    self.TBX_NF.setValue(cx)
    self.TBY.setValue(cy)
    self.TBY_NF.setValue(cy)
    self.TBR.setValue(r)
    self.TBR_NF.setValue(r)
    self.blockAllSignals = False

    moveTransBeam(self)


def crossAlign(self):
    """
    Manual beam-centre alignment via an interactive cross-hair cursor.

    Draws two draggable lines (H + V) on the diffraction window that
    follow the mouse.  A single left-click fixes the intersection as the
    new B0 (TBX, TBY) and removes the cursor.

    A second call to crossAlign (e.g. user presses the button again)
    while a cursor is already active will remove it without updating B0.
    """
    canvas = self.Fig.Dfrn.canvas
    ax = self.Fig.Dfrn.ax

    # ── toggle off if already active ────────────────────────────────────
    if hasattr(self, '_crossAlignState') and self._crossAlignState is not None:
        _state = self._crossAlignState
        for cid in _state['cids']:
            canvas.mpl_disconnect(cid)
        for line in _state['lines']:
            try:
                line.remove()
            except Exception:
                pass
        canvas.draw_idle()
        self._crossAlignState = None
        return

    # ── create crosshair lines ───────────────────────────────────────────
    xl = ax.get_xlim()
    yl = ax.get_ylim()
    b0 = self.B0

    h_line = ax.axhline(b0[1], color='yellow', linewidth=1,
                        linestyle='--', alpha=0.8, zorder=10)
    v_line = ax.axvline(b0[0], color='yellow', linewidth=1,
                        linestyle='--', alpha=0.8, zorder=10)
    canvas.draw_idle()

    def _on_move(event):
        if event.inaxes is not ax or event.xdata is None:
            return
        h_line.set_ydata([event.ydata, event.ydata])
        v_line.set_xdata([event.xdata, event.xdata])
        canvas.draw_idle()

    def _on_click(event):
        if event.inaxes is not ax or event.xdata is None:
            return
        if event.button != 1:   # left-click only
            return

        new_x = float(np.clip(event.xdata, 1, self.D.NPx[1]))
        new_y = float(np.clip(event.ydata, 1, self.D.NPx[0]))

        self.blockAllSignals = True
        self.TBX.setValue(new_x)
        self.TBX_NF.setValue(new_x)
        self.TBY.setValue(new_y)
        self.TBY_NF.setValue(new_y)
        self.blockAllSignals = False

        # Tear down the crosshair
        crossAlign(self)   # second call → removes state
        moveTransBeam(self)

    cids = [
        canvas.mpl_connect('motion_notify_event', _on_move),
        canvas.mpl_connect('button_press_event', _on_click),
    ]

    self._crossAlignState = {
        'cids': cids,
        'lines': [h_line, v_line],
    }
