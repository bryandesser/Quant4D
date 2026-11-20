"""Scale bars on the image windows, their Settings toggles, and scan steps read from MRC/DM files."""
import numpy as np
import pytest

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, set_mode

REAL_IDS = ["Real", "RealMask"]
DFRN_IDS = ["Dfrn", "DfrnMask"]


def _label(win, qapp, id):
    win.Fig[id].canvas.draw()
    qapp.processEvents()
    return win.Fig[id].scaleBar.label


@pytest.fixture()
def annular(loaded_app, qapp):
    set_mode(loaded_app, qapp, "AnnMod")
    sw = loaded_app.SettingsWindow
    saved = (sw.RsStep.value(), sw.RsUnits.currentIndex(), sw.DCUnit.currentIndex())
    yield loaded_app
    sw.ScaleBarReal.setChecked(True)
    sw.ScaleBarDfrn.setChecked(True)
    sw.RsUnits.setCurrentIndex(saved[1])
    sw.RsStep.setValue(saved[0])
    sw.DCUnit.setCurrentIndex(saved[2])
    qapp.processEvents()


def test_toggles_on_by_default(app):
    assert app.SettingsWindow.ScaleBarReal.isChecked() and app.SettingsWindow.ScaleBarDfrn.isChecked()


def test_real_space_in_pixels_until_calibrated(annular, qapp):
    w, sw = annular, annular.SettingsWindow
    sw.RsUnits.setCurrentIndex(sw.RsUnits.findData("pixels"))
    qapp.processEvents()
    for id in REAL_IDS:
        assert _label(w, qapp, id).endswith(" px"), id
    sw.RsUnits.setCurrentIndex(sw.RsUnits.findData("nm"))
    sw.RsStep.setValue(0.5)
    qapp.processEvents()
    for id in REAL_IDS:
        assert _label(w, qapp, id).endswith(" nm") or _label(w, qapp, id).endswith(" pm"), id


def test_real_toggle(annular, qapp):
    w, sw = annular, annular.SettingsWindow
    sw.ScaleBarReal.setChecked(False)
    qapp.processEvents()
    assert all(_label(w, qapp, id) == "" for id in REAL_IDS)
    assert _label(w, qapp, "Dfrn") != ""                # diffraction keeps its own
    sw.ScaleBarReal.setChecked(True)
    qapp.processEvents()
    assert all(_label(w, qapp, id) != "" for id in REAL_IDS)


def test_diffraction_in_mrad_or_pixels(annular, qapp):
    w, sw = annular, annular.SettingsWindow
    assert w.P.TransBeamInit
    sw.DCUnit.setCurrentIndex(sw.DCUnit.findData("mrad"))
    qapp.processEvents()
    for id in DFRN_IDS:
        assert _label(w, qapp, id).endswith(" mrad"), id
    sw.DCUnit.setCurrentIndex(sw.DCUnit.findData("px"))
    qapp.processEvents()
    for id in DFRN_IDS:
        assert _label(w, qapp, id).endswith(" px"), id


def test_diffraction_toggle(annular, qapp):
    w, sw = annular, annular.SettingsWindow
    sw.ScaleBarDfrn.setChecked(False)
    qapp.processEvents()
    assert all(_label(w, qapp, id) == "" for id in DFRN_IDS)
    assert _label(w, qapp, "Real") != ""


def test_bar_length_matches_the_scale(annular, qapp):
    """The drawn length in display pixels is the label's value over the scale, in display pixels."""
    w, sw = annular, annular.SettingsWindow
    sw.DCUnit.setCurrentIndex(sw.DCUnit.findData("mrad"))
    qapp.processEvents()
    bar = w.Fig.Dfrn.scaleBar
    label = _label(w, qapp, "Dfrn")
    value = float(label.split()[0])
    ax = w.Fig.Dfrn.ax
    p0, p1 = ax.transData.transform([(0, 0), (1, 0)])
    assert bar.length_px == pytest.approx(value / w.mradPx.value() * np.hypot(*(p1 - p0)), rel=1e-6)


def test_annotated_png_has_the_bar(annular, qapp, tmp_path):
    from PIL import Image
    w = annular
    w.Fig.Real.fig.savefig(tmp_path / "with.png", dpi=100)
    w.SettingsWindow.ScaleBarReal.setChecked(False)
    qapp.processEvents()
    w.Fig.Real.fig.savefig(tmp_path / "without.png", dpi=100)
    a, b = (np.asarray(Image.open(tmp_path / n).convert("L"), float) for n in ("with.png", "without.png"))
    assert a.shape == b.shape and np.abs(a - b).max() > 100


# ---------------------------------------------------------------------- scan step from MRC and DM files
def _open(win, qapp, path):
    iw = win.ImportWindow
    if not iw.isVisible():
        win.ShowImportWdw.trigger()
    iw.ImpFilePath.setText(str(path))
    iw.ImpFilePath.editingFinished.emit()
    qapp.processEvents()
    return iw


def test_mrc_stays_uncalibrated(app, qapp, tmp_path, synthetic_data):
    """MRC headers carry no scan step: the field stays in pixels (Bryan, 2026-11-20)."""
    h = bytearray(1024)
    h[0:40] = np.array([DET_X, DET_Y, SCAN_X * SCAN_Y, 2, 0, 0, 0, DET_X, DET_Y, SCAN_X * SCAN_Y], "<i4").tobytes()
    h[40:52] = np.array([DET_X * 1.0, DET_Y * 1.0, 3.0 * SCAN_X * SCAN_Y], "<f4").tobytes()   # even with a z cell
    h[208:212] = b"MAP "
    h[212:214] = b"\x44\x44"
    path = tmp_path / "x.mrc"
    path.write_bytes(bytes(h) + synthetic_data.astype("<f4").tobytes())
    iw = _open(app, qapp, path)
    assert iw.MRCButton.isChecked() and iw.ImpScanUnits.currentData() == "pixels"


def test_dm_calibration_fills_scan_step_and_voltage(app, qapp, tmp_path, synthetic_data):
    from dm_writer import _DMWriter
    cube = synthetic_data.reshape(SCAN_Y, SCAN_X, DET_Y, DET_X)
    cals = [(0.57, "mrad", 12.0), (0.57, "mrad", 8.0), (0.023, "nm", 0.0), (0.023, "nm", 0.0)]
    path = tmp_path / "si.dm4"
    path.write_bytes(_DMWriter(4, True).file([("SI", cube, "f4", cals, 200000.0)]))
    iw = _open(app, qapp, path)
    assert iw.DM34Button.isChecked()
    assert iw.ImpScanStep.value() == pytest.approx(0.023) and iw.ImpScanUnits.currentText() == "nm"
    assert iw.ImpAccVolt.value() == 200.0
    notes = iw.ImpFileMetaNotes.toPlainText()
    assert "Scan step: 0.023 nm" in notes and "Detector: 0.57 mrad/px" in notes
    assert "Applied as the diffraction scale" in notes and "not from the DM origin" in notes
    assert "Accelerating voltage: 200 kV" in notes
    iw.ImportDataButton.click()
    from conftest import wait_until
    assert wait_until(qapp, lambda: app.Data is not None and app.Fig.Dfrn.Image is not None)
    qapp.processEvents()
    assert (app.D.ScanStep, app.D.ScanUnits) == (pytest.approx(0.023), "nm")
    assert _label(app, qapp, "Real").split()[1] in ("pm", "nm")


def test_dm_without_calibration_leaves_fields(app, qapp, tmp_path, synthetic_data):
    from dm_writer import _DMWriter
    path = tmp_path / "plain.dm3"
    path.write_bytes(_DMWriter(3, True).file([("SI", synthetic_data.reshape(SCAN_Y, SCAN_X, DET_Y, DET_X), "f4")]))
    iw = _open(app, qapp, path)
    assert iw.ImpScanUnits.currentData() == "pixels" and iw.ImpAccVolt.value() == 300.0
    assert "DM calibration" not in iw.ImpFileMetaNotes.toPlainText()
