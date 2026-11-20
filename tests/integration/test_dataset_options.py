"""
Integration tests — Settings → Info: swap diffraction/real X/Y, swap byte order.

Swapping X/Y reinterprets the flat data with the two sizes exchanged (for a
dataset whose dimensions were entered the wrong way round); the data itself is
untouched, as in MATLAB Quant4D.
"""
import numpy as np
import pytest

import pyquant4d.callbacks.datasetOptCallbacks as dso
from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, import_raw, set_mode, wait_until


@pytest.fixture()
def fresh(app, qapp, sample_raw_file):
    import_raw(app, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
    set_mode(app, qapp, "AnnMod")
    app.AnnRi.setValue((0, 6))
    qapp.processEvents()
    return app


def _annular_reference(app):
    mask = np.asarray(app.Fig.DfrnMask.Image, bool)
    return np.asarray(app.Data, float)[:, mask.ravel()].sum(axis=1).reshape(app.D.NFrY, app.D.NFrX)


def test_swap_diffraction_xy(fresh, qapp, synthetic_data):
    fresh.SettingsWindow.SwapDfrnXY.click()
    qapp.processEvents()
    assert (fresh.D.NPxX, fresh.D.NPxY) == (DET_Y, DET_X)
    assert np.array_equal(np.asarray(fresh.Data), synthetic_data), "swapping X/Y must not move data"
    assert fresh.Fig.Dfrn.Image.shape == (DET_X, DET_Y)
    assert np.allclose(fresh.Fig.Dfrn.Image, synthetic_data.mean(axis=0).reshape(DET_X, DET_Y), rtol=1e-5)
    assert np.allclose(fresh.Fig.Real.Image, _annular_reference(fresh), rtol=1e-5)
    for mode in ("CoMMod", "DPCMod", "VrApMod", "CustMod", "AnnMod"):     # every mode copes with the new shape
        set_mode(fresh, qapp, mode)
    fresh.SettingsWindow.SwapDfrnXY.click()
    qapp.processEvents()
    assert (fresh.D.NPxX, fresh.D.NPxY) == (DET_X, DET_Y)
    assert "Diffraction (X⨯Y): 24⨯16" in fresh.SettingsWindow.DataInfo.toPlainText()


def test_swap_real_xy_keeps_beam_alignment(fresh, qapp, synthetic_data):
    b0 = np.array(fresh.B0, float).copy()
    fresh.SettingsWindow.SwapRealXY.click()
    qapp.processEvents()
    assert (fresh.D.NFrX, fresh.D.NFrY) == (SCAN_Y, SCAN_X)
    assert fresh.Fig.Real.Image.shape == (SCAN_X, SCAN_Y)
    assert np.allclose(fresh.B0, b0), "swapping the scan must keep the transmitted-beam alignment"
    assert np.allclose(fresh.Fig.Real.Image, _annular_reference(fresh), rtol=1e-5)
    fresh.FrameX.setValue(SCAN_Y - 1)            # point ROI over the new scan width
    fresh.FrameY.setValue(SCAN_X - 1)
    qapp.processEvents()


@pytest.mark.parametrize("answer, swapped", [("Yes", True), ("No. Revert", False)])
def test_swap_byte_order(fresh, qapp, synthetic_data, monkeypatch, answer, swapped):
    monkeypatch.setattr(dso, "notifDLG", lambda *a, **k: answer)
    fresh.SettingsWindow.SwapByteOrder.click()
    qapp.processEvents()
    bits = np.asarray(fresh.Data).view(np.uint32)
    expected = synthetic_data.byteswap() if swapped else synthetic_data
    assert np.array_equal(bits, expected.view(np.uint32))
    assert fresh.D.ByteOrder == ("b" if swapped else "l")
    assert fresh.Data.dtype.isnative, "kept in native byte order for the compute and GPU paths"


def test_swap_byte_order_lazy(app, qapp, sample_raw_file, synthetic_data, monkeypatch):
    """A lazily loaded dataset is a read-only memory map: swap by reinterpreting, not in place."""
    iw = app.ImportWindow
    app.ShowImportWdw.trigger()
    iw.ImpFilePath.setText(str(sample_raw_file))
    iw.ImpFilePath.editingFinished.emit()
    iw.CustomButton.click()
    qapp.processEvents()
    iw.ImpDataType.setCurrentIndex(iw.ImpDataType.findData("f4"))
    for name, val in (("DNPxX", DET_X), ("DNPxY", DET_Y), ("DNFrX", SCAN_X), ("DNFrY", SCAN_Y)):
        getattr(iw, name).setValue(val)
    qapp.processEvents()
    assert iw.ImpMemType.isEnabled(), "lazy loading should be offered for native float data"
    iw.ImpMemType.setCurrentIndex(1)
    iw.ImportDataButton.click()
    assert wait_until(qapp, lambda: app.Data is not None and app.Fig.Dfrn.Image is not None)
    assert isinstance(app.Data, np.memmap) and not app.Data.flags.writeable
    monkeypatch.setattr(dso, "notifDLG", lambda *a, **k: "Yes")
    app.SettingsWindow.SwapByteOrder.click()
    qapp.processEvents()
    values = np.asarray(app.Data).astype("<f4")              # the file's bytes, read the other way round
    assert np.array_equal(values.view(np.uint32), synthetic_data.byteswap().view(np.uint32))
    assert app.D.ByteOrder == "b"
