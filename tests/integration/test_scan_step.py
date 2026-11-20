"""Real-space calibration (callbacks.scan_step): the file's scan step in the Import
window, the loaded data's step in Settings > Misc, and how sampling scales them."""
import pytest

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, wait_until


def _open(win, qapp, path):
    iw = win.ImportWindow
    if not iw.isVisible():
        win.ShowImportWdw.trigger()
    iw.ImpFilePath.setText(str(path))
    iw.ImpFilePath.editingFinished.emit()
    qapp.processEvents()
    return iw


def _sample(iw, qapp, step):
    iw.ImpFrPart.setChecked(True)
    iw.ImpFrPart.clicked.emit(True)
    iw.IFrD.setValue(step)
    qapp.processEvents()
    return iw.INFrX.value() * iw.INFrY.value()


def _import(win, qapp, frames):
    win.ImportWindow.ImportDataButton.click()
    assert wait_until(qapp, lambda: win.Data is not None and win.Data.shape == (frames, DET_X * DET_Y)
                      and win.Fig.Dfrn.Image is not None), "import did not finish"
    qapp.processEvents()


def _set_units(combo, code):
    combo.setCurrentIndex(combo.findData(code))


def test_unit_codes():
    from callbacks.scan_step import unitCode
    assert [unitCode(u) for u in ("A", "Å", "angstrom", "nm", "µm", "um", "pixels", "px", "")] == \
        ["A", "A", "A", "nm", "um", "um", "pixels", "pixels", "pixels"]
    assert unitCode("m") == "m"                       # unknown units are kept


def test_import_field_starts_uncalibrated(app, qapp, sample_hdf5_file):
    iw = _open(app, qapp, sample_hdf5_file)
    assert iw.ImpScanUnits.currentData() == "pixels" and iw.ImpScanStep.value() == 1.0
    assert not iw.ImpScanStep.isEnabled()
    _set_units(iw.ImpScanUnits, "nm")
    assert iw.ImpScanStep.isEnabled()
    assert [iw.ImpScanUnits.itemText(i) for i in range(iw.ImpScanUnits.count())] == ["px", "pm", "Å", "nm", "µm"]


def test_calibrated_file_fills_the_field_and_a_new_file_resets_it(app, qapp, tmp_path, synthetic_data,
                                                                  sample_hdf5_file):
    from callbacks.io.emd import EmdCalibration, write_emd
    from callbacks.io.export import full_region
    path = tmp_path / "angstrom.h5"
    write_emd(str(path), synthetic_data, (SCAN_X, SCAN_Y), (DET_X, DET_Y), full_region((SCAN_X, SCAN_Y)),
              full_region((DET_X, DET_Y)), EmdCalibration(r_pixel_size=2.5, r_units="A"))
    iw = _open(app, qapp, path)
    assert (iw.ImpScanStep.value(), iw.ImpScanUnits.currentText()) == (2.5, "Å")
    _open(app, qapp, sample_hdf5_file)                   # a file without a calibration
    assert iw.ImpScanUnits.currentData() == "pixels"


def test_typed_step_times_sampling_shown_in_misc_and_info(app, qapp, sample_hdf5_file):
    iw = _open(app, qapp, sample_hdf5_file)
    _set_units(iw.ImpScanUnits, "nm")
    iw.ImpScanStep.setValue(0.25)
    frames = _sample(iw, qapp, 2)
    _import(app, qapp, frames)
    assert (app.D.ScanStepFile, app.D.ScanStep, app.D.ScanUnits) == (0.25, 0.5, "nm")
    sw = app.SettingsWindow
    assert (sw.RsStep.value(), sw.RsUnits.currentText()) == (0.5, "nm") and sw.RsStep.isEnabled()
    info = sw.DataInfo.toPlainText()
    assert f"Real-space (X\u2A2FY): {iw.INFrX.value()}\u2A2F{iw.INFrY.value()}" in info   # was (Y, X)
    assert "Scan Step: 0.5 nm (file 0.25 nm × sampling 2)" in sw.DataInfo.toPlainText()


def test_misc_edit_changes_the_export(app, qapp, sample_hdf5_file, tmp_path):
    iw = _open(app, qapp, sample_hdf5_file)
    _set_units(iw.ImpScanUnits, "nm")
    iw.ImpScanStep.setValue(0.25)
    _import(app, qapp, SCAN_X * SCAN_Y)
    sw, save = app.SettingsWindow, app.SaveWindow
    sw.RsStep.setValue(0.8)                           # corrected after import
    qapp.processEvents()
    assert app.D.ScanStep == 0.8 and app.D.ScanStepFile == 0.8
    assert "Scan Step: 0.8 nm" in sw.DataInfo.toPlainText()
    app.ShowSaveWdw.trigger()
    save.SaveDir.setText(str(tmp_path))
    save.SaveTabGroup.setCurrentWidget(save.ExportTab)
    save.ExpFormat.setCurrentIndex(save.ExpFormat.findData("emd"))
    save.ExpFrPart.setChecked(True)
    save.ExpFrPart.clicked.emit(True)
    save.EFrD.setValue(2)
    qapp.processEvents()
    assert "Scan step: 1.6 nm" in save.ExpNotes.toPlainText()
    _set_units(sw.RsUnits, "A")                       # the notes follow the units too
    qapp.processEvents()
    assert "Scan step: 1.6 A" in save.ExpNotes.toPlainText()
    _set_units(sw.RsUnits, "pixels")                  # back to uncalibrated: one file position
    qapp.processEvents()
    assert (app.D.ScanStep, app.D.ScanUnits) == (1.0, "pixels") and not sw.RsStep.isEnabled()
    assert "Scan step: 2 pixels" in save.ExpNotes.toPlainText()
