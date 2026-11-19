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
from callbacks.signals import all_signals_blocked, signals_blocked  # noqa: E402
try:
    from callbacks.imfindcircles import imfindcircles
except ImportError:
    imfindcircles = None


def transBeamCallbacks(self, sender=None):
    """Transmitted-beam step: *sender* says why (``DetrMode`` entering Align mode, ``UpdateImages``,
    ``TBAutoAlign``, ``TBCrossAlign``; ``None`` just refreshes).  Passed explicitly, never read from
    ``self.sender()``, because this is also called outside a Qt slot (see :func:`moveTransBeam`)."""
    from callbacks.datasetOptCallbacks import datasetOptCallbacks  # noqa: E402
    from callbacks.window_manager import enableWindows  # noqa: E402
    match sender:
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
            # (a py4DSTEM file's calibration then sets the beam; with centre, scale and angle all
            # given there is nothing to fit)
            if not self.P.TransBeamInit:
                datasetOptCallbacks(self)  # checks for nans and asks if user wants to swap byteorder
                cal = fileCalibration(self)
                if cal is None or not _completeCalibration(cal):
                    autoAlign(self)
                if cal is not None:
                    applyCalibration(self, cal)

            enableWindows(self, True)  # Enable windows

        case self.UpdateImages:  # Update images
            # Create a summed image of all diffraction patterns simply for alignment and calibration
            self.Fig.DfrnMask.Image = np.ones(dfrn_shape(self.D), self.D.DataType)
            self.Fig.Real.Image = np.reshape(self.Data.sum(axis=1), real_shape(self.D))

        case self.TBAutoAlign:  # Auto-align
            autoAlign(self)

        case self.TBCrossAlign:  # Align transmitted beam via two crossed lines
            crossAlign(self, self.TBCrossAlign.isChecked())

    # Update dependent variables (not via self.sender(): this also runs outside a slot)
    moveTransBeam(self, sender=None)


_FROM_SIGNAL = object()


def moveTransBeam(self, sender=_FROM_SIGNAL):
    """ Function to sync UIs/ROIs depending on the central beam location

    Connected slots leave *sender* unset and it is read from ``self.sender()``.  Direct calls from
    outside a Qt slot (matplotlib events, auto-alignment) pass ``sender=None``: ``QObject.sender()``
    is only valid while a slot runs, and outside one it can return a dangling pointer (segfault on
    Linux).
    """
    from callbacks.detector import detrCoordCallbacks  # noqa: E402

    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    b0 = np.array([self.TBX.value(), self.TBY.value()])
    r = np.maximum(self.TBR.value(), np.finfo(np.single).eps)
    a = self.Alpha.value()
    mrad_per_px = a / r
    nPix = self.D.NPx

    src = self.sender() if sender is _FROM_SIGNAL else sender
    match src:
        case self.TBX | self.TBX_NF:
            b0[0] = max(0, src.value())  # Force X >= 0
        case self.TBY | self.TBY_NF:
            b0[1] = max(0, src.value())  # Force Y >= 0
        case self.TBR | self.TBR_NF:
            r = src.value()  # Radius
        case self.Alpha:
            a = src.value()
            mrad_per_px = a / r  # Calculate the diffraction scale
        case self.mradPx:
            mrad_per_px = src.value()
            a = mrad_per_px * r  # Manually set the diffraction scale
        case self.A.tb if src is not None:   # dragged (the annotation holds its radii and centre); None is no sender
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
        self.AnnRi.setRange(0, int(np.ceil(self.P.RMax / float(self.D.annWidth))))   # in rings
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
        showDfScale(self)                    # Settings > Windows > Diffraction, in its unit

        # Annular integration step (MATLAB's AnnularStep): one pixel, but at most 250 rings out to the
        # farthest corner (finer makes the pre-computed annular images slow), shown in mrad
        self.D.annWidth = float(max(1.0, self.P.RMax / 250.0))
        self.AnnStep.setValue(self.D.annWidth * float(self.mradPx.value()))   # the scale as shown (rounded)

        # Update transmitted beam annotation
        if (src is not self.A.tb) and (self.A.tb is not None):
            self.A.tb.center = b0
            self.A.tb.radius = np.array([r])
            self.A.tb.redraw()

    detrCoordCallbacks(self, source=None)    # mrad values follow the scale (not via self.sender(): see above)
    from callbacks.scale_bar import refreshScaleBars  # noqa: E402
    refreshScaleBars(self, "Dfrn")      # the scale (mrad/px) may have changed


DF_SCALE_UNITS = (("mrad/px", "mrad"), ("1/Å/px", "invA"), ("px", "px"))   # px: uncalibrated (detector values in pixels)


def _invA_per_mrad(self) -> "float | None":
    from callbacks.io.emd import mrad_per_inverse_angstrom  # noqa: E402
    kv = getattr(self.D, "kV", None) if self.D is not None else None
    return 1.0 / mrad_per_inverse_angstrom(kv) if kv and kv > 0 else None


def showDfScale(self) -> None:
    """Settings > Windows > Diffraction > Scale: the main window's mrad/px, in the unit chosen
    (``px``: 1, not editable, like an uncalibrated real-space scan step)."""
    sw = self.SettingsWindow
    unit = sw.DfScaleUnits.currentData()
    f = _invA_per_mrad(self) if unit == "invA" else 1.0
    with signals_blocked(sw.DfScale):
        sw.DfScale.setDecimals(4 if f == 1.0 else 6)
        sw.DfScale.setValue(1.0 if unit == "px" else float(self.mradPx.value()) * (f or 1.0))
    sw.DfScale.setEnabled(unit != "px")


def dfScaleUnitChanged(self) -> None:
    """The Scale unit sets the unit of every detector value: pixels for ``px``, mrad otherwise."""
    sw = self.SettingsWindow
    showDfScale(self)
    want = "px" if sw.DfScaleUnits.currentData() == "px" else "mrad"
    if sw.DCUnit.currentData() != want:
        sw.DCUnit.setCurrentIndex(sw.DCUnit.findData(want))     # its slots recalculate the detectors


def dcUnitChanged(self) -> None:
    """Detector units set elsewhere (a reset, a script): the Scale unit follows."""
    sw = self.SettingsWindow
    unit, shown = sw.DCUnit.currentData(), sw.DfScaleUnits.currentData()
    if (unit == "px") != (shown == "px"):
        with signals_blocked(sw.DfScaleUnits):
            sw.DfScaleUnits.setCurrentIndex(sw.DfScaleUnits.findData("px" if unit == "px" else "mrad"))
        showDfScale(self)


def dfScaleEdited(self) -> None:
    """The Scale field was edited: set mrad/px from it (which recalculates through moveTransBeam)."""
    if self.blockAllSignals:
        return
    sw = self.SettingsWindow
    f = _invA_per_mrad(self) if sw.DfScaleUnits.currentData() == "invA" else 1.0
    if f and sw.DfScaleUnits.currentData() != "px":
        self.mradPx.setValue(sw.DfScale.value() / f)


def connectDfScale(self) -> None:
    """Scale field and its unit; called once from ``slotsSignals``."""
    sw = self.SettingsWindow
    with signals_blocked(sw.DfScaleUnits):
        sw.DfScaleUnits.clear()
        for text, unit in DF_SCALE_UNITS:
            sw.DfScaleUnits.addItem(text, unit)
    sw.DfScale.setMaximum(1e6)
    sw.DfScale.valueChanged.connect(lambda *_: dfScaleEdited(self))
    sw.DfScaleUnits.currentIndexChanged.connect(lambda *_: dfScaleUnitChanged(self))
    sw.DCUnit.currentIndexChanged.connect(lambda *_: dcUnitChanged(self))
    dcUnitChanged(self)


def fileCalibration(self):
    """The calibration of the imported py4DSTEM file in pixels of the imported pattern, or None."""
    from callbacks.io.emd import calibration_for_region  # noqa: E402
    if self.D is None or self.D.Calib is None:
        return None
    return calibration_for_region(self.D.Calib, (self.D.PxX1, self.D.PxY1), self.D.PxD)


def _completeCalibration(cal) -> bool:
    return cal.beam_xy is not None and cal.q_units == "mrad" and bool(cal.probe_semiangle_mrad)


def applyCalibration(self, cal):
    """Set the transmitted beam from a file's calibration (imported pixels).

    The beam centre is taken as given.  With the detector scale (mrad/px) and
    the convergence semi-angle both known, the disk radius follows
    (semi-angle / scale); with the scale only, the semi-angle follows from the
    current (fitted) radius; with the semi-angle only, it is set and the
    scale follows from the radius.  The scale is then semi-angle / radius,
    both fields rounded to 0.01, so it matches the file to about 0.1 %.
    """
    has_q = cal.q_units == "mrad" and cal.q_pixel_size > 0
    semi = cal.probe_semiangle_mrad
    with all_signals_blocked(self):
        if cal.beam_xy is not None:
            nPx = dfrn_shape(self.D)       # (height, width)
            x = float(np.clip(cal.beam_xy[0], 0, nPx[1] - 1))
            y = float(np.clip(cal.beam_xy[1], 0, nPx[0] - 1))
            for w, v in ((self.TBX, x), (self.TBX_NF, x), (self.TBY, y), (self.TBY_NF, y)):
                w.setValue(v)
        if has_q and semi:
            r = float(semi) / float(cal.q_pixel_size)
            self.TBR.setValue(r)
            self.TBR_NF.setValue(r)
            self.Alpha.setValue(float(semi))
        elif has_q:
            self.Alpha.setValue(float(cal.q_pixel_size) * float(self.TBR.value()))
        elif semi:
            self.Alpha.setValue(float(semi))
    moveTransBeam(self, sender=None)


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
    moveTransBeam(self, sender=None)


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


def crossAlign(self, on=None):
    """Beam centre at the crossing of two lines (MATLAB's ``cross_align``): the X button shows two
    lines on the diffraction pattern, each with two draggable end points (drag the line to move it),
    for the user to lay along two Kikuchi lines; the beam centre follows their intersection while
    they are dragged.  Click X again (or leave Alignment mode) to finish.

    *on*: True / False to start / finish; None toggles."""
    from annotationsClasses.interactiveLine import InteractiveLine, intersection  # noqa: E402
    state = getattr(self, "_crossAlignState", None)
    if on is None:
        on = state is None
    if not on:
        if state is not None:
            for line in state["lines"]:
                line.remove()
            self._crossAlignState = None
        with signals_blocked(self.TBCrossAlign):
            self.TBCrossAlign.setChecked(False)
        return
    if state is not None or self.Data is None:
        return

    # two lines crossing at the current beam centre, at ±45°, half the pattern long
    ax = self.Fig.Dfrn.ax
    b0 = np.asarray(self.B0, float)
    h = np.array([self.D.NPxX, self.D.NPxY], float) / 4
    lines = [InteractiveLine(ax, [b0 - h, b0 + h], color="r"),
             InteractiveLine(ax, [b0 + h * [-1, 1], b0 + h * [1, -1]], color="r")]

    def moved():
        p = intersection(lines[0].ends, lines[1].ends)
        if p is None:                                   # parallel: no crossing
            return
        p = p.clip(0, np.array([self.D.NPxX, self.D.NPxY]) - 1)
        with all_signals_blocked(self):
            for box, v in ((self.TBX, p[0]), (self.TBX_NF, p[0]), (self.TBY, p[1]), (self.TBY_NF, p[1])):
                box.setValue(float(v))
        moveTransBeam(self, sender=None)

    for line in lines:
        line.connect()
        line.updateLine.connect(moved)
    self._crossAlignState = {"lines": lines}
    with signals_blocked(self.TBCrossAlign):
        self.TBCrossAlign.setChecked(True)
    self.Fig.Dfrn.show()
    self.Fig.Dfrn.activateWindow()
