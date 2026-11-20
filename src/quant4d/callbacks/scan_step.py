"""Real-space calibration: the scan step.

Two fields (Bryan's choice, option D):

* **Import window, Scan Step** — the step of the *file* (distance between
  neighbouring probe positions), filled in from a calibrated py4DSTEM or
  Quant4D file, ``px`` (uncalibrated) otherwise.  Partial import multiplies
  it by the sampling step; cropping leaves it unchanged.
* **Settings > Windows > Real-space, Scan Step** — the step of the *loaded* data
  (``D.ScanStep``/``D.ScanUnits``), editable after import.  Export multiplies
  it by the export sampling.

Units are stored as py4DSTEM spells them (``"A"`` for Å); ``"pixels"`` means
uncalibrated: one probe position of the file.
"""
from __future__ import annotations

from .signals import signals_blocked

__all__ = ["UNITS", "unitCode", "fillUnits", "setImportStep", "importStep",
           "showScanStep", "scanStepChanged", "connectScanStep", "describeScanStep"]

# (code stored and written to files, text shown)
UNITS = [("pixels", "px"), ("pm", "pm"), ("A", "Å"), ("nm", "nm"), ("um", "µm")]
_ALIASES = {"pixels": "pixels", "pixel": "pixels", "px": "pixels", "": "pixels",
            "pm": "pm", "a": "A", "å": "A", "angstrom": "A", "angstroms": "A",
            "nm": "nm", "um": "um", "µm": "um", "μm": "um", "micron": "um"}


def unitCode(units: str) -> str:
    """The stored code for a unit as a file or a user spells it (unknown units are kept)."""
    return _ALIASES.get(str(units).strip().lower(), str(units).strip())


def _text(code: str) -> str:
    return dict(UNITS).get(code, code)


def fillUnits(combo) -> None:
    with signals_blocked(combo):
        combo.clear()
        for code, text in UNITS:
            combo.addItem(text, code)


def _setUnits(combo, units: str) -> None:
    code = unitCode(units)
    i = combo.findData(code)
    if i < 0:                                   # a unit not in the list (e.g. "m"): add it
        combo.addItem(code, code)
        i = combo.count() - 1
    combo.setCurrentIndex(i)


def _syncImportField(self) -> None:
    iw = self.ImportWindow
    calibrated = (iw.ImpScanUnits.currentData() or "pixels") != "pixels"
    iw.ImpScanStep.setEnabled(calibrated)
    if not calibrated:
        with signals_blocked(iw.ImpScanStep):
            iw.ImpScanStep.setValue(1.0)


def setImportStep(self, step: float = 1.0, units: str = "pixels") -> None:
    """Fill the Import window's Scan Step (a new file: its calibration, or uncalibrated)."""
    iw = self.ImportWindow
    with signals_blocked(iw.ImpScanStep, iw.ImpScanUnits):
        _setUnits(iw.ImpScanUnits, units)
        iw.ImpScanStep.setValue(float(step) if unitCode(units) != "pixels" else 1.0)
    _syncImportField(self)


def importStep(self) -> tuple[float, str]:
    """``(step, units)`` of the file, from the Import window."""
    iw = self.ImportWindow
    units = iw.ImpScanUnits.currentData() or "pixels"
    return (1.0 if units == "pixels" else float(iw.ImpScanStep.value())), units


def describeScanStep(d) -> str:
    """'1 nm (file 0.5 nm x sampling 2)' for the Info tab."""
    units = _text(d.ScanUnits)
    line = f"{d.ScanStep:g} {units}"
    if d.FrD > 1 or d.ScanStepFile != d.ScanStep:
        line += f" (file {d.ScanStepFile:g} {units} × sampling {d.FrD})"
    return line


def showScanStep(self) -> None:
    """Show the loaded data's step in Settings > Windows > Real-space (after import)."""
    sw = self.SettingsWindow
    if self.D is None:
        return
    with signals_blocked(sw.RsStep, sw.RsUnits):
        _setUnits(sw.RsUnits, self.D.ScanUnits)
        sw.RsStep.setValue(float(self.D.ScanStep))
        sw.RsStep.setEnabled(self.D.ScanUnits != "pixels")


def scanStepChanged(self) -> None:
    """The loaded data's step was edited in Settings > Windows > Real-space."""
    sw = self.SettingsWindow
    if self.D is None:
        return
    units = sw.RsUnits.currentData() or "pixels"
    if units == "pixels":
        # back to uncalibrated: one position of the file per sampling step
        step = float(self.D.FrD)
        with signals_blocked(sw.RsStep):
            sw.RsStep.setValue(step)
    else:
        step = float(sw.RsStep.value())
    sw.RsStep.setEnabled(units != "pixels")
    self.D.ScanStep, self.D.ScanUnits = step, units
    self.D.ScanStepFile = step / max(1, self.D.FrD)
    from .import_io import getImportInfo  # noqa: E402
    sw.DataInfo.setPlainText(getImportInfo(self))
    from .save_export import refreshExportNotes  # noqa: E402
    refreshExportNotes(self)
    from .scale_bar import refreshScaleBars  # noqa: E402
    refreshScaleBars(self, "Real")
    from .annularDetectorCallbacks import showBandpass  # noqa: E402
    showBandpass(self)                  # 1/Å and mrad of the bandpass filter follow the step


def connectScanStep(self) -> None:
    """Fill the unit lists and connect both fields; called once from ``slotsSignals``."""
    iw, sw = self.ImportWindow, self.SettingsWindow
    fillUnits(iw.ImpScanUnits)
    fillUnits(sw.RsUnits)
    _syncImportField(self)
    iw.ImpScanUnits.currentIndexChanged.connect(lambda *_: _syncImportField(self))
    sw.RsStep.valueChanged.connect(lambda *_: scanStepChanged(self))
    sw.RsUnits.currentIndexChanged.connect(lambda *_: scanStepChanged(self))
