"""
Integration tests — Section 4.2 (import pipeline).

Synthetic files from conftest are opened through the real Import window and
the imported data is compared with what was written.  Deeper format coverage
(DM, MRC, EMPAD, Medipix, partial import) is in tests/unit/test_readers.py and
tests/manual/smoke_pipeline.py.
"""
import numpy as np
import pytest

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, import_raw, wait_until


def _open(app, qapp, path, button):
    iw = app.ImportWindow
    app.ShowImportWdw.trigger()
    iw.ImpFilePath.setText(str(path))
    iw.ImpFilePath.editingFinished.emit()
    getattr(iw, button).click()
    qapp.processEvents()
    return iw


class TestRawImport:
    def test_raw_loads_exactly(self, app, qapp, sample_raw_file, synthetic_data):
        import_raw(app, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
        assert app.Data.shape == (SCAN_X * SCAN_Y, DET_X * DET_Y)
        assert np.array_equal(np.asarray(app.Data), synthetic_data)
        assert (app.D.NFrX, app.D.NFrY, app.D.NPxX, app.D.NPxY) == (SCAN_X, SCAN_Y, DET_X, DET_Y)
        assert app.Fig.Dfrn.Image.shape == (DET_Y, DET_X)
        assert app.Fig.Real.Image.shape == (SCAN_Y, SCAN_X)

    def test_size_estimate_matches_file(self, app, qapp, sample_raw_file):
        iw = _open(app, qapp, sample_raw_file, "CustomButton")
        iw.ImpDataType.setCurrentIndex(iw.ImpDataType.findData("f4"))
        for name in ("DataOffset", "FrHead", "FrFoot"):
            getattr(iw, name).setValue(0)
        for name, val in (("DNPxX", DET_X), ("DNPxY", DET_Y), ("DNFrX", SCAN_X), ("DNFrY", SCAN_Y)):
            getattr(iw, name).setValue(val)
        qapp.processEvents()
        assert app.T.EstSize == app.T.FileSize == sample_raw_file.stat().st_size
        assert iw.ImpEstFilesize.text(), "estimated size not shown"
        assert "0, 128, 0" in iw.ImpEstFilesize.styleSheet(), "a matching estimate is shown in green"
        iw.DNFrY.setValue(SCAN_Y + 1)
        qapp.processEvents()
        assert app.T.EstSize > app.T.FileSize and "255, 0, 0" in iw.ImpEstFilesize.styleSheet()

    def test_scan_size_from_file_name(self, app, qapp, sample_raw_file):
        """The fixture file is named ..._x6_y4.raw; the scan size is taken from it."""
        iw = _open(app, qapp, sample_raw_file, "CustomButton")
        assert (iw.DNFrX.value(), iw.DNFrY.value()) == (SCAN_X, SCAN_Y)


class TestHDF5Import:
    def test_hdf5_loads_exactly(self, app, qapp, sample_hdf5_file, synthetic_data):
        iw = _open(app, qapp, sample_hdf5_file, "HDF5Button")
        dims = tuple(getattr(iw, n).value() for n in ("DNPxX", "DNPxY", "DNFrX", "DNFrY"))
        assert dims == (DET_X, DET_Y, SCAN_X, SCAN_Y), f"dimensions read from the file: {dims}"
        iw.ImportDataButton.click()
        assert wait_until(qapp, lambda: app.Data is not None and app.Data.shape == synthetic_data.shape)
        assert np.allclose(np.asarray(app.Data), synthetic_data)


class TestImportCancel:
    def test_cancel_before_import(self, app, qapp, sample_raw_file):
        _open(app, qapp, sample_raw_file, "CustomButton")
        assert app.ImportWindow.isVisible()
        app.ImportWindow.ImportCancelButton.click()
        qapp.processEvents()
        assert not app.ImportWindow.isVisible()
        assert app.Data is None, "cancel must not load anything"

    def test_cancel_returns_to_previous_mode(self, app, qapp, sample_raw_file):
        import_raw(app, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
        app.DetrMode.setCurrentIndex(app.DetrMode.findData("AnnMod"))
        qapp.processEvents()
        app.ShowImportWdw.trigger()
        qapp.processEvents()
        assert app.DetrMode.currentData() == "PrvwMod", "opening the Import window enters preview mode"
        app.ImportWindow.ImportCancelButton.click()
        qapp.processEvents()
        assert app.DetrMode.currentData() == "AnnMod"
        assert app.Data is not None, "cancelling a second import must keep the loaded dataset"


class TestInvalidInput:
    def test_missing_file_refused(self, app, qapp, tmp_path):
        iw = app.ImportWindow
        app.ShowImportWdw.trigger()
        iw.ImpFilePath.setText(str(tmp_path / "nope.raw"))
        iw.ImportDataButton.click()
        qapp.processEvents()
        assert app.Data is None

    @pytest.mark.parametrize("dtype", ["u2", "i4"])
    def test_other_dtypes(self, app, qapp, tmp_path, dtype):
        data = (np.arange(SCAN_X * SCAN_Y * DET_X * DET_Y) % 97).reshape(SCAN_X * SCAN_Y, -1).astype("<" + dtype)
        path = tmp_path / f"int_x{SCAN_X}_y{SCAN_Y}.raw"
        data.tofile(path)
        import_raw(app, qapp, path, SCAN_X, SCAN_Y, DET_X, DET_Y, dtype=dtype)
        assert np.array_equal(np.asarray(app.Data), data)


class TestCompressedHDF5:
    """Chunked/compressed datasets have no data offset; they must be read through h5py."""

    @pytest.mark.parametrize("layout", ["4d", "3d"])
    def test_compressed(self, app, qapp, tmp_path, synthetic_data, layout):
        h5py = pytest.importorskip("h5py")
        shape = (SCAN_Y, SCAN_X, DET_Y, DET_X) if layout == "4d" else (SCAN_Y * SCAN_X, DET_Y, DET_X)
        path = tmp_path / f"{layout}.h5"
        with h5py.File(path, "w") as f:
            f.create_group("meta").attrs["note"] = "not data"
            f.create_dataset("entry/data", data=synthetic_data.reshape(shape), chunks=True, compression="gzip")
        iw = _open(app, qapp, path, "HDF5Button")
        assert iw.ImpSubImg.currentText() == "/entry/data"
        assert "not \"contiguous\"" in iw.ImpFileMetaNotes.toPlainText()
        if layout == "3d":     # the scan is guessed from the frame count: 24 -> 4 x 6
            assert iw.DNFrX.value() * iw.DNFrY.value() == SCAN_X * SCAN_Y
            iw.DNFrX.setValue(SCAN_X)
            iw.DNFrY.setValue(SCAN_Y)
        assert (iw.DNPxX.value(), iw.DNPxY.value()) == (DET_X, DET_Y)
        iw.ImportDataButton.click()
        assert wait_until(qapp, lambda: app.Data is not None and app.Data.shape == synthetic_data.shape)
        assert np.array_equal(np.asarray(app.Data), synthetic_data), "compressed HDF5 imported wrongly"


class TestMemoryWarning:
    def test_asked_once_on_import(self, app, qapp, sample_raw_file, monkeypatch):
        """Typing dimensions only notes it; clicking Import asks once, and Cancel keeps the window."""
        import callbacks.importCallbacks as ic
        import callbacks.import_io as io_
        asked = []
        monkeypatch.setattr(io_, "notifDLG", lambda *a, **k: asked.append(a[3]) or "")
        monkeypatch.setattr(ic, "notifDLG", lambda *a, **k: asked.append(a[3]) or "Cancel")
        app.C.MemTot = 1024                      # pretend the computer has 1 KiB
        iw = _open(app, qapp, sample_raw_file, "CustomButton")
        iw.ImpDataType.setCurrentIndex(iw.ImpDataType.findData("f4"))
        for name, val in (("DNPxX", DET_X), ("DNPxY", DET_Y), ("DNFrX", SCAN_X), ("DNFrY", SCAN_Y)):
            getattr(iw, name).setValue(val)
        qapp.processEvents()
        assert asked == [] and "larger than the system memory" in iw.ImpNotes.toPlainText()
        iw.ImportDataButton.click()
        qapp.processEvents()
        assert len(asked) == 1 and app.Data is None and iw.isVisible()
