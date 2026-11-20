"""Importing a py4DSTEM (EMD 1.0) file: its calibration sets the transmitted beam.

The file is opened through the Import window like any HDF5 file; the
DataCube is picked as the largest dataset, and after import the beam centre,
detector scale (mrad/px) and convergence angle come from the file.
"""
import numpy as np
import pytest

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, wait_until

BEAM_XY = (10.0, 7.0)          # off the pattern centre (11.5, 7.5)
Q_MRAD, SEMI = 0.5, 4.0          # disk radius 8 px


def _write(path, data, **cal):
    from callbacks.io.emd import EmdCalibration, EmdImage, write_emd
    from callbacks.io.export import full_region
    write_emd(str(path), data, (SCAN_X, SCAN_Y), (DET_X, DET_Y),
              full_region((SCAN_X, SCAN_Y)), full_region((DET_X, DET_Y)),
              EmdCalibration(**cal), {"ADF": EmdImage(np.ones((SCAN_Y, SCAN_X)))})
    return path


@pytest.fixture()
def emd_file(tmp_path, synthetic_data):
    return _write(tmp_path / "cube.emd", synthetic_data, beam_xy=BEAM_XY, q_pixel_size=Q_MRAD,
                  q_units="mrad", probe_semiangle_mrad=SEMI)


def _open(win, qapp, path):
    iw = win.ImportWindow
    if not iw.isVisible():
        win.ShowImportWdw.trigger()
    iw.ImpFilePath.setText(str(path))
    iw.ImpFilePath.editingFinished.emit()
    qapp.processEvents()
    assert iw.HDF5Button.isChecked()
    return iw


def _import(win, qapp, shape):
    win.ImportWindow.ImportDataButton.click()
    assert wait_until(qapp, lambda: win.Data is not None and win.Data.shape == shape
                      and win.Fig.Dfrn.Image is not None), "import did not finish"
    qapp.processEvents()


def _beam(win):
    return (win.TBX.value(), win.TBY.value(), win.TBR.value(), win.Alpha.value(), win.mradPx.value())


def test_notes_describe_the_datacube(app, qapp, emd_file):
    iw = _open(app, qapp, emd_file)
    assert iw.ImpSubImg.currentText() == "/pyquant4d_root/datacube/data"
    notes = iw.ImpFileMetaNotes.toPlainText()
    assert "py4DSTEM DataCube (written by pyQuant4D)" in notes
    assert "Beam centre (x, y) = (10.00, 7.00) px" in notes and "0.5 mrad/px" in notes
    assert "4 mrad" in notes and "Images: ADF" in notes and "applied" in notes


def test_calibration_sets_the_beam(app, qapp, emd_file, synthetic_data):
    _open(app, qapp, emd_file)
    _import(app, qapp, (SCAN_X * SCAN_Y, DET_X * DET_Y))
    assert app.DetrMode.currentData() == "AlignMod"
    x, y, r, alpha, mrad = _beam(app)
    assert (x, y) == pytest.approx(BEAM_XY)
    assert r == pytest.approx(SEMI / Q_MRAD) and alpha == pytest.approx(SEMI) and mrad == pytest.approx(Q_MRAD)
    assert np.allclose(app.B0, BEAM_XY)
    assert np.allclose(app.Data, synthetic_data)


def test_partial_binned_import_converts_the_calibration(app, qapp, emd_file):
    iw = _open(app, qapp, emd_file)
    iw.ImpPxPart.setChecked(True)
    iw.ImpPxPart.clicked.emit(True)
    iw.IPxD.setValue(2)
    iw.IPxX1.setValue(2)
    iw.IPxY1.setValue(1)
    qapp.processEvents()
    px, py = iw.INPxX.value(), iw.INPxY.value()
    _import(app, qapp, (SCAN_X * SCAN_Y, px * py))
    x, y, r, alpha, mrad = _beam(app)
    assert (x, y) == pytest.approx(((10 - 2 + 0.5) / 2 - 0.5, (7 - 1 + 0.5) / 2 - 0.5))
    assert mrad == pytest.approx(2 * Q_MRAD) and alpha == pytest.approx(SEMI) and r == pytest.approx(SEMI / (2 * Q_MRAD))


def test_angle_only_keeps_the_fitted_radius(app, qapp, tmp_path, synthetic_data):
    path = _write(tmp_path / "angle.h5", synthetic_data, beam_xy=BEAM_XY, probe_semiangle_mrad=SEMI)
    _open(app, qapp, path)
    _import(app, qapp, (SCAN_X * SCAN_Y, DET_X * DET_Y))
    x, y, r, alpha, mrad = _beam(app)
    assert (x, y) == pytest.approx(BEAM_XY) and alpha == pytest.approx(SEMI)
    assert mrad == pytest.approx(SEMI / r, abs=1e-3)          # scale from the (auto-aligned) radius


def test_inverse_angstrom_converted_at_the_voltage(app, qapp, tmp_path, synthetic_data):
    """A py4DSTEM scale in 1/Å becomes mrad with the relativistic wavelength at the field's voltage."""
    from callbacks.io.emd import electron_wavelength_A
    k = 0.02                                                     # 1/Å per pixel
    path = _write(tmp_path / "inv_a.h5", synthetic_data, beam_xy=BEAM_XY, q_pixel_size=k,
                  q_units="A^-1", probe_semiangle_mrad=SEMI)
    iw = _open(app, qapp, path)
    iw.ImpAccVolt.setValue(300)
    qapp.processEvents()
    at300 = 1000 * k * electron_wavelength_A(300)
    assert f"= {at300:.4g} mrad/px at 300 kV" in iw.ImpFileMetaNotes.toPlainText()
    iw.ImpAccVolt.setValue(200)                                 # the notes follow the voltage
    qapp.processEvents()
    at200 = 1000 * k * electron_wavelength_A(200)
    notes = iw.ImpFileMetaNotes.toPlainText()
    assert f"= {at200:.4g} mrad/px at 200 kV" in notes and notes.count("py4DSTEM DataCube") == 1
    _import(app, qapp, (SCAN_X * SCAN_Y, DET_X * DET_Y))
    x, y, r, alpha, mrad = _beam(app)
    assert app.D.kV == 200
    # the scale is angle / radius, both shown to 0.01: within ~0.1 % of the file
    assert mrad == pytest.approx(at200, rel=2e-3) and alpha == pytest.approx(SEMI)
    assert r == pytest.approx(SEMI / at200, rel=1e-3)


def test_plain_hdf5_is_unchanged(app, qapp, sample_hdf5_file):
    iw = _open(app, qapp, sample_hdf5_file)
    assert "py4DSTEM" not in iw.ImpFileMetaNotes.toPlainText()
    _import(app, qapp, (SCAN_X * SCAN_Y, DET_X * DET_Y))
    assert app.D.Calib is None
    assert app.Alpha.value() == pytest.approx(12)              # the default angle


def test_other_dataset_of_the_file_is_not_calibrated(app, qapp, emd_file):
    """Picking the ADF image (not the DataCube) does not carry the DataCube's calibration."""
    from callbacks.import_io import gatherImportOptions
    iw = _open(app, qapp, emd_file)
    assert gatherImportOptions(app, True).Calib is not None
    iw.ImpSubImg.setCurrentIndex(iw.ImpSubImg.findText("/pyquant4d_root/datacube/ADF/data"))
    qapp.processEvents()
    assert gatherImportOptions(app, True).Calib is None
    assert "py4DSTEM" not in iw.ImpFileMetaNotes.toPlainText()


def test_round_trip_through_export(loaded_app, qapp, tmp_path):
    """Export as py4DSTEM EMD, import the file again: same beam, scale and angle."""
    from callbacks.guiClass import MainWindow
    from conftest import set_mode
    set_mode(loaded_app, qapp, "AnnMod")
    saved = _beam(loaded_app)
    # a beam auto-alignment would not find, so the import has to take it from the file
    loaded_app.TBX.setValue(9.0)
    loaded_app.TBY.setValue(6.0)
    loaded_app.Alpha.setValue(17.5)
    qapp.processEvents()
    before = _beam(loaded_app)
    assert before[:2] == pytest.approx((9.0, 6.0)) and before[3] == pytest.approx(17.5)
    sw = loaded_app.SaveWindow
    loaded_app.ShowSaveWdw.trigger()
    sw.SaveDir.setText(str(tmp_path))
    sw.SaveTabGroup.setCurrentWidget(sw.ExportTab)
    sw.ExpFormat.setCurrentIndex(sw.ExpFormat.findData("emd"))
    sw.ExpFilename.setText("roundtrip")
    sw.ExpDimSuff.setChecked(False)
    sw.ExpFrPart.setChecked(False)
    sw.ExpPxPart.setChecked(False)
    sw.ExpPxPart.clicked.emit(False)
    sw.SaveExport.click()
    qapp.processEvents()
    sw.ExpFormat.setCurrentIndex(sw.ExpFormat.findData("h5"))
    path = tmp_path / "roundtrip.h5"
    assert path.exists()

    win = MainWindow()
    win.show()
    try:
        _open(win, qapp, path)
        _import(win, qapp, loaded_app.Data.shape)
        x, y, r, alpha, mrad = _beam(win)
        assert (x, y) == pytest.approx(before[:2])
        assert alpha == pytest.approx(before[3]) and mrad == pytest.approx(before[4], abs=0.01)
        assert r == pytest.approx(before[2], rel=0.02)         # radius = angle / scale (scale shown to 0.01)
    finally:
        win.close()
        loaded_app.TBX.setValue(saved[0])
        loaded_app.TBY.setValue(saved[1])
        loaded_app.Alpha.setValue(saved[3])
        qapp.processEvents()


def test_voltage_recorded_in_the_file_fills_the_field(app, qapp, tmp_path, synthetic_data):
    from callbacks.io.emd import EmdCalibration, write_emd
    from callbacks.io.export import full_region
    path = tmp_path / "kv.h5"
    write_emd(str(path), synthetic_data, (SCAN_X, SCAN_Y), (DET_X, DET_Y),
              full_region((SCAN_X, SCAN_Y)), full_region((DET_X, DET_Y)),
              EmdCalibration(beam_xy=BEAM_XY), metadata={"accelerating_voltage_kV": 120.0})
    iw = _open(app, qapp, path)
    assert iw.ImpAccVolt.value() == 120.0
    assert "Accelerating voltage: 120 kV" in iw.ImpFileMetaNotes.toPlainText()


def test_scan_step_follows_sampling_on_import_and_export(app, qapp, tmp_path, synthetic_data):
    """0.5 nm steps, imported every 2nd position -> 1 nm; exported every 2nd of those -> 2 nm.
    Cropping (start points) leaves the step alone."""
    h5py = pytest.importorskip("h5py")
    from callbacks.io.emd import read_emd_info
    path = _write(tmp_path / "step.emd", synthetic_data, r_pixel_size=0.5, r_units="nm")
    iw = _open(app, qapp, path)
    assert "Scan step: 0.5 nm" in iw.ImpFileMetaNotes.toPlainText()
    iw.ImpFrPart.setChecked(True)
    iw.ImpFrPart.clicked.emit(True)
    iw.IFrD.setValue(2)
    iw.IFrX1.setValue(1)
    qapp.processEvents()
    fx, fy = iw.INFrX.value(), iw.INFrY.value()
    _import(app, qapp, (fx * fy, DET_X * DET_Y))
    assert (app.D.ScanStep, app.D.ScanUnits) == (1.0, "nm")

    sw = app.SaveWindow
    app.ShowSaveWdw.trigger()
    sw.SaveDir.setText(str(tmp_path))
    sw.SaveTabGroup.setCurrentWidget(sw.ExportTab)
    sw.ExpFormat.setCurrentIndex(sw.ExpFormat.findData("emd"))
    sw.ExpFilename.setText("step_out")
    sw.ExpDimSuff.setChecked(False)
    sw.ExpFrPart.setChecked(True)
    sw.ExpFrPart.clicked.emit(True)
    sw.EFrD.setValue(2)
    qapp.processEvents()
    assert "Scan step: 2 nm" in sw.ExpNotes.toPlainText()
    sw.SaveExport.click()
    qapp.processEvents()
    cal = read_emd_info(str(tmp_path / "step_out.h5")).calibration
    assert (cal.r_pixel_size, cal.r_units) == (2.0, "nm")
    with h5py.File(tmp_path / "step_out.h5") as f:
        meta = f["pyquant4d_root/metadatabundle/pyquant4d"]
        assert meta["scan_step"][()] == 2.0 and meta["accelerating_voltage_kV"][()] == app.D.kV


def test_plain_file_scan_step_in_source_positions(app, qapp, sample_hdf5_file):
    iw = _open(app, qapp, sample_hdf5_file)
    iw.ImpFrPart.setChecked(True)
    iw.ImpFrPart.clicked.emit(True)
    iw.IFrD.setValue(2)
    qapp.processEvents()
    fx, fy = iw.INFrX.value(), iw.INFrY.value()
    _import(app, qapp, (fx * fy, DET_X * DET_Y))
    assert (app.D.ScanStep, app.D.ScanUnits) == (2.0, "pixels")


def test_typed_path_clears_the_dataset_list(app, qapp, sample_hdf5_file, emd_file):
    iw = _open(app, qapp, emd_file)
    iw.ImpSubImg.setCurrentIndex(iw.ImpSubImg.findText("/pyquant4d_root/datacube/ADF/data"))
    qapp.processEvents()
    iw.ImpFilePath.editingFinished.emit()             # same path again (focus change): choice kept
    qapp.processEvents()
    assert iw.ImpSubImg.currentText() == "/pyquant4d_root/datacube/ADF/data"
    _open(app, qapp, sample_hdf5_file)                # a different file typed in: list starts again
    items = [iw.ImpSubImg.itemText(i) for i in range(iw.ImpSubImg.count())]
    assert items == ["/data"]


def test_scale_field_has_four_decimals(app):
    assert app.mradPx.decimals() == 4
