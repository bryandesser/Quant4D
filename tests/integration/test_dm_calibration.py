"""A DM3/DM4 file's detector calibration sets the diffraction scale after import; its origin does not
set the beam centre (auto-alignment does)."""
import numpy as np
import pytest

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, wait_until
from dm_writer import _DMWriter

SCAN = [(0.023, "nm", 0.0), (0.023, "nm", 0.0)]


def _dm(path, synthetic_data, detector=None, voltage=None):
    cube = synthetic_data.reshape(SCAN_Y, SCAN_X, DET_Y, DET_X)
    cals = (list(detector) + SCAN) if detector else None
    path.write_bytes(_DMWriter(4, True).file([("SI", cube, "f4", cals, voltage)]))
    return path


def _import(win, qapp, path, binning=1):
    iw = win.ImportWindow
    if not iw.isVisible():
        win.ShowImportWdw.trigger()
    iw.ImpFilePath.setText(str(path))
    iw.ImpFilePath.editingFinished.emit()
    qapp.processEvents()
    assert iw.DM34Button.isChecked()
    npx = DET_X * DET_Y
    if binning > 1:
        iw.ImpPxPart.setChecked(True)
        iw.ImpPxPart.clicked.emit(True)
        iw.IPxD.setValue(binning)
        qapp.processEvents()
        npx = iw.INPxX.value() * iw.INPxY.value()
    notes = iw.ImpFileMetaNotes.toPlainText()
    iw.ImportDataButton.click()
    assert wait_until(qapp, lambda: win.Data is not None and win.Data.shape == (SCAN_X * SCAN_Y, npx)
                      and win.Fig.Dfrn.Image is not None), "import did not finish"
    qapp.processEvents()
    return notes


def _centre(win):
    return win.TBX.value(), win.TBY.value()


def test_mrad_scale_applied_centre_from_auto_alignment(app, qapp, tmp_path, synthetic_data):
    _import(app, qapp, _dm(tmp_path / "plain.dm4", synthetic_data))
    auto = _centre(app)
    assert app.D.Calib is None

    notes = _import(app, qapp, _dm(tmp_path / "cal.dm4", synthetic_data,
                                   [(0.57, "mrad", 2.0), (0.57, "mrad", 3.0)]))
    assert "Applied as the diffraction scale" in notes
    # the scale is the angle (shown to 0.01 mrad) over the fitted radius: small here (random data)
    assert app.mradPx.value() == pytest.approx(0.57, rel=1e-2)
    assert _centre(app) == pytest.approx(auto)                    # not the DM origin (2, 3)
    assert app.D.Calib.beam_xy is None


def test_inverse_nm_converted_at_the_file_voltage(app, qapp, tmp_path, synthetic_data):
    from quant4d.callbacks.io.emd import electron_wavelength_A
    notes = _import(app, qapp, _dm(tmp_path / "k.dm4", synthetic_data,
                                   [(0.5, "1/nm", 0.0), (0.5, "1/nm", 0.0)], voltage=200000.0))
    assert "converted to mrad at the Accelerating Voltage" in notes
    assert app.D.kV == 200
    expected = 0.5 * 0.1 * 1000 * electron_wavelength_A(200)
    assert app.mradPx.value() == pytest.approx(expected, rel=1e-2)


def test_binned_import_doubles_the_scale(app, qapp, tmp_path, synthetic_data):
    _import(app, qapp, _dm(tmp_path / "b.dm4", synthetic_data, [(0.57, "mrad", 0.0), (0.57, "mrad", 0.0)]),
            binning=2)
    assert app.mradPx.value() == pytest.approx(2 * 0.57, rel=1e-2)


def test_unusable_units_ignored(app, qapp, tmp_path, synthetic_data):
    notes = _import(app, qapp, _dm(tmp_path / "u.dm4", synthetic_data, [(5.0, "um", 0.0), (5.0, "um", 0.0)]))
    assert "not used" in notes and app.D.Calib is None
    assert app.Alpha.value() == pytest.approx(12)


def test_diffraction_scale_bar_in_mrad(app, qapp, tmp_path, synthetic_data):
    _import(app, qapp, _dm(tmp_path / "s.dm4", synthetic_data, [(0.57, "mrad", 0.0), (0.57, "mrad", 0.0)]))
    sw = app.SettingsWindow
    sw.DCUnit.setCurrentIndex(sw.DCUnit.findData("mrad"))
    qapp.processEvents()
    app.Fig.Dfrn.canvas.draw()
    assert app.Fig.Dfrn.scaleBar.label.endswith(" mrad")
    assert np.isfinite(app.mradPx.value())
