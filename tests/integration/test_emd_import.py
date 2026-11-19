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
    path = _write(tmp_path / "angle.h5", synthetic_data, beam_xy=BEAM_XY, q_pixel_size=0.02,
                  q_units="A^-1", probe_semiangle_mrad=SEMI)
    iw = _open(app, qapp, path)
    assert "not used" in iw.ImpFileMetaNotes.toPlainText()
    _import(app, qapp, (SCAN_X * SCAN_Y, DET_X * DET_Y))
    x, y, r, alpha, mrad = _beam(app)
    assert (x, y) == pytest.approx(BEAM_XY) and alpha == pytest.approx(SEMI)
    assert mrad == pytest.approx(SEMI / r, abs=0.01)          # scale from the (auto-aligned) radius


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
