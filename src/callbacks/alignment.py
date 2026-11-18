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
from callbacks.layout import dfrn_grids, dfrn_shape, real_shape
from annotationsClasses.interactiveCircle import InteractiveCircle
from annotationsClasses.interactivePoint import InteractivePoint
from callbacks.signals import all_signals_blocked  # noqa: E402
try:
    from callbacks.imfindcircles import imfindcircles
except ImportError:
    imfindcircles = None


def transBeamCallbacks(self):
    from callbacks.datasetOptCallbacks import datasetOptCallbacks  # noqa: E402
    from callbacks.window_manager import enableWindows  # noqa: E402
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
            if not self.SettingsWindow.DispLock.isChecked():
                self.SettingsWindow.DispImage.setCurrentIndex(self.SettingsWindow.DispImage.findData("Dfrn"))
            self.Fig.Dfrn.activateWindow()

            # If this is the initializing alignment, then do swap byte check and auto-align
            if not self.P.TransBeamInit:
                datasetOptCallbacks(self)  # checks for nans and asks if user wants to swap byteorder
                autoAlign(self)

            enableWindows(self, True)  # Enable windows

        case self.UpdateImages:  # Update images
            # Create a summed image of all diffraction patterns simply for alignment and calibration
            self.Fig.DfrnMask.Image = np.ones(dfrn_shape(self.D), self.D.DataType)
            self.Fig.Real.Image = np.reshape(self.Data.sum(axis=1), real_shape(self.D))

        case self.TBAutoAlign:  # Auto-align
            autoAlign(self)

        case self.TBCrossAlign:  # Align transmitted beam via two crossed lines
            crossAlign(self)

    # Update dependent variables
    moveTransBeam(self)


def moveTransBeam(self):
    """ Function to sync UIs/ROIs depending on the central beam location """
    from callbacks.detector import detrCoordCallbacks  # noqa: E402

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
            b0[0] = max(0, self.sender().value())  # Force X >= 0
        case self.TBY | self.TBY_NF:
            b0[1] = max(0, self.sender().value())  # Force Y >= 0
        case self.TBR | self.TBR_NF:
            r = self.sender().value()  # Radius
        case self.Alpha:
            a = self.sender().value()
            mrad_per_px = a / r  # Calculate the diffraction scale
        case self.mradPx:
            mrad_per_px = self.sender().value()
            a = mrad_per_px * r  # Manually set the diffraction scale
        case self.A.tb:   # dragged: the annotation holds an array of radii (one here) and its own centre array
            b0 = np.array(self.A.tb.center, dtype=float)
            r = float(np.ravel(self.A.tb.radius)[-1])

    # Restrict transmitted beam location/size
    b0 = b0.clip([0, 0], nPix - 1)   # 0-based: valid pixel centres are 0 .. N-1
    self.B0 = b0
    self.P.RMax = np.ceil(np.linalg.norm(abs(self.P.DfCtr - b0) + self.P.DfCtr))  # Find the max allowed radius
    r = np.clip(r, np.finfo(np.single).eps, self.P.RMax)  # 0 < r <= RMax

    # avoid triggering a valueChanged loop by blocking signals
    with all_signals_blocked(self):
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

    detrCoordCallbacks(self)


def _beamCandidates(self, broad=False):
    """Circles found on the pattern used for alignment: ``(centers (n, 2), radii (n,))``, best first.

    *broad* searches every radius up to a quarter of the pattern even after the first alignment
    (for picking another disk than the one auto-alignment chose)."""
    from callbacks.imfindcircles import imfindcircles

    nPx = dfrn_shape(self.D)   # (height, width) tuple
    rmax_abs = max(1, self.P.RMax)

    # ── Choose the input pattern ──────────────────────────────────────────
    roi_shape = self.RealROIShape.currentData()   # 'full', 'point', …
    if roi_shape == 'full' or self.Fig.Dfrn.Image is None:
        # Full PACBED: sum every probe position
        pacbed = np.nansum(self.Data, axis=0).reshape(nPx).astype(np.float64)
    else:
        # ROI-weighted average: already computed and stored in Fig.Dfrn.Image
        pacbed = np.asarray(self.Fig.Dfrn.Image, dtype=np.float64).reshape(nPx)

    # ── Radius search range ───────────────────────────────────────────────
    tbr = self.TBR.value()
    if self.P.TransBeamInit and tbr > 1 and not broad:
        # Use ±50 % of the current beam-disc radius, clamped to sensible values
        rmin = max(1, int(np.floor(0.5 * tbr)))
        rmax = min(rmax_abs, int(np.ceil(1.5 * tbr)))
    else:
        # First-time call (or picking): up to a quarter of the pattern
        rmin = 1
        rmax = max(2, int(np.ceil(min(nPx) / 4)))
    if rmax <= rmin:
        rmax = rmin + 1

    # ── Run circle finder ─────────────────────────────────────────────────
    sensitivity = 0.9 if broad else 0.85            # more candidates when the user picks one
    for method in ('PhaseCode', 'TwoStage'):          # PhaseCode can fail on a narrow range
        try:
            centers, radii, _ = imfindcircles(pacbed, [rmin, rmax], ObjectPolarity='bright',
                                              Method=method, Sensitivity=sensitivity)
            return np.asarray(centers, float).reshape(-1, 2), np.asarray(radii, float).ravel()
        except Exception:
            continue
    return np.zeros((0, 2)), np.zeros(0)


def _setBeam(self, cx, cy, r=None):
    nPx = dfrn_shape(self.D)
    cx = float(np.clip(cx, 0, nPx[1] - 1))
    cy = float(np.clip(cy, 0, nPx[0] - 1))
    with all_signals_blocked(self):
        self.TBX.setValue(cx)
        self.TBX_NF.setValue(cx)
        self.TBY.setValue(cy)
        self.TBY_NF.setValue(cy)
        if r is not None:
            r = float(np.clip(r, np.finfo(np.single).eps, max(1, self.P.RMax)))
            self.TBR.setValue(r)
            self.TBR_NF.setValue(r)
    moveTransBeam(self)


def autoAlign(self, near=None):
    """
    Auto-detect the transmitted beam centre (and radius) using the
    Circular Hough Transform (imfindcircles.py).

    Input pattern: the sum of all probe positions (full real-space ROI), otherwise the pattern of
    the real-space ROI (``self.Fig.Dfrn.Image``), so e.g. a point ROI aligns on that frame.

    Without *near* the strongest circle is taken.  With *near* = (x, y) (the user double-clicked
    the diffraction pattern in Alignment mode, because auto-alignment chose the wrong disk) the
    circle nearest that point is taken; if none is found near it, the beam centre goes to the
    point and keeps its radius.  Returns True if a detected circle was used.
    """
    centers, radii = _beamCandidates(self, broad=near is not None)
    if near is None:
        if len(centers) == 0:
            return False    # no circle found — leave B0 unchanged
        _setBeam(self, centers[0, 0], centers[0, 1], radii[0])   # sorted by descending metric
        return True

    near = np.asarray(near, float)
    if len(centers):
        d = np.hypot(*(centers - near).T)
        k = int(np.argmin(d))
        if d[k] <= max(1.5 * radii[k], 3.0):           # the click is on (or just beside) that disk
            _setBeam(self, centers[k, 0], centers[k, 1], radii[k])
            return True
    _setBeam(self, near[0], near[1])                   # nothing detected there: centre on the click
    return False


def connectBeamPick(self) -> None:
    """Alignment mode: double-click a disk on the diffraction pattern to make it the transmitted beam
    (refit to the detected circle nearest the click); called once from slotsSignals."""
    def on_press(event):
        if (event.dblclick and event.button == 1 and event.inaxes is self.Fig.Dfrn.ax
                and event.xdata is not None and self.DetrMode.currentData() == "AlignMod"
                and self.Data is not None):
            autoAlign(self, near=(event.xdata, event.ydata))
    self.Fig.Dfrn.canvas.mpl_connect("button_press_event", on_press)
    self.TBAutoAlign.setToolTip("Find the transmitted beam automatically.  If it picks the wrong disk, "
                                "double-click the right one on the diffraction pattern.")


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

        new_x = float(np.clip(event.xdata, 0, self.D.NPxX - 1))
        new_y = float(np.clip(event.ydata, 0, self.D.NPxY - 1))

        with all_signals_blocked(self):
            self.TBX.setValue(new_x)
            self.TBX_NF.setValue(new_x)
            self.TBY.setValue(new_y)
            self.TBY_NF.setValue(new_y)

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
