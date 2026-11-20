"""
Integration tests — Section 4.9 (save images / export dataset).

Files are written through the Save window into a pytest tmp_path and read
back.  Partial/binned/big-endian export and re-import are covered by
tests/manual/smoke_pipeline.py.
"""
import numpy as np
import pytest
from PIL import Image

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, set_mode


@pytest.fixture()
def save_window(loaded_app, qapp, tmp_path):
    sw = loaded_app.SaveWindow
    loaded_app.ShowSaveWdw.trigger()
    sw.SaveDir.setText(str(tmp_path))
    sw.SaveImgPrefix.setText("t_")
    sw.SavePrfxRi.setChecked(False)
    sw.SavePrfxRo.setChecked(False)
    qapp.processEvents()
    return sw


def _select_images(sw, ids):
    sw.SaveImgList.clearSelection()
    for i in range(sw.SaveImgList.count()):
        item = sw.SaveImgList.item(i)
        item.setSelected(item.text() in ids)


def _save(sw, qapp, ids, tif=False, png=False, annot=False):
    sw.SaveTabGroup.setCurrentWidget(sw.SaveImgTab)
    _select_images(sw, ids)
    sw.SaveImgTIF.setChecked(tif)
    sw.SaveImgPNG.setChecked(png)
    sw.SaveImgPNGAnnot.setChecked(annot)
    assert sw.SaveExport.text() == "Save Images"
    sw.SaveExport.click()
    qapp.processEvents()


class TestSaveImages:
    def test_tiff_is_raw_float32(self, loaded_app, qapp, save_window, tmp_path):
        set_mode(loaded_app, qapp, "AnnMod")
        _save(save_window, qapp, ["Real", "Dfrn"], tif=True)
        real = np.array(Image.open(tmp_path / "t_Real.tif"))
        dfrn = np.array(Image.open(tmp_path / "t_Dfrn.tif"))
        assert real.dtype == np.float32 and real.shape == (SCAN_Y, SCAN_X)
        assert np.allclose(real, loaded_app.Fig.Real.Image)
        assert dfrn.shape == (DET_Y, DET_X) and np.allclose(dfrn, loaded_app.Fig.Dfrn.Image)

    def test_png_as_displayed(self, loaded_app, qapp, save_window, tmp_path):
        set_mode(loaded_app, qapp, "AnnMod")
        _save(save_window, qapp, ["Real"], png=True)
        png = np.array(Image.open(tmp_path / "t_Real.png"))
        assert png.shape == (SCAN_Y, SCAN_X, 3), "one pixel per probe position"
        from pyquant4d.callbacks.io.export import rgb_as_displayed
        assert np.array_equal(png, rgb_as_displayed(loaded_app.ImageAx.Real))

    def test_annotated_png_is_the_figure(self, loaded_app, qapp, save_window, tmp_path):
        _save(save_window, qapp, ["Dfrn"], png=True, annot=True)
        png = np.array(Image.open(tmp_path / "t_Dfrn.png"))
        assert png.shape[0] > DET_Y and png.shape[2] in (3, 4)

    def test_detector_angles_in_name(self, loaded_app, qapp, save_window, tmp_path):
        set_mode(loaded_app, qapp, "AnnMod")
        save_window.SavePrfxRi.setChecked(True)
        save_window.SavePrfxRo.setChecked(True)
        _save(save_window, qapp, ["Real"], tif=True)
        names = [p.name for p in tmp_path.iterdir()]
        assert len(names) == 1 and "_ri" in names[0] and "_ro" in names[0], names

    def test_com_images_saved(self, loaded_app, qapp, save_window, tmp_path):
        set_mode(loaded_app, qapp, "CoMMod")
        _save(save_window, qapp, ["CoMX", "CoMY"], tif=True)
        for i in ("CoMX", "CoMY"):
            arr = np.array(Image.open(tmp_path / f"t_{i}.tif"))
            assert arr.dtype == np.float32 and np.allclose(arr, loaded_app.Fig[i].Image)
        set_mode(loaded_app, qapp, "AnnMod")

    def test_missing_folder_writes_nothing(self, loaded_app, qapp, save_window, tmp_path):
        save_window.SaveDir.setText(str(tmp_path / "missing"))
        _save(save_window, qapp, ["Real"], tif=True)
        assert not (tmp_path / "missing").exists()


class TestExportDataset:
    def _export(self, sw, qapp, tmp_path, fmt, byte_order="l"):
        sw.SaveDir.setText(str(tmp_path))
        sw.SaveTabGroup.setCurrentWidget(sw.ExportTab)
        sw.ExpFormat.setCurrentIndex(sw.ExpFormat.findData(fmt))
        sw.ExpByteOrder.setCurrentIndex(sw.ExpByteOrder.findData(byte_order))
        sw.ExpFilename.setText("export")
        sw.ExpDimSuff.setChecked(fmt == "raw")
        sw.ExpFrPart.setChecked(False)
        sw.ExpPxPart.setChecked(False)
        sw.ExpPxPart.clicked.emit(False)
        assert sw.SaveExport.text() == "Export Dataset"
        path = sw.ExpNotes.toPlainText().splitlines()[0].replace("File: ", "")
        sw.SaveExport.click()
        qapp.processEvents()
        return path

    def test_hdf5(self, loaded_app, qapp, save_window, tmp_path):
        h5py = pytest.importorskip("h5py")
        path = self._export(save_window, qapp, tmp_path, "h5")
        with h5py.File(path) as f:
            assert np.array_equal(f["data"][()], np.asarray(loaded_app.Data).reshape(SCAN_Y, SCAN_X, DET_Y, DET_X))
            meta = dict(f["metadata"].attrs)
        assert np.allclose(meta["beam_center_xy"], loaded_app.B0)

    @pytest.mark.parametrize("order, dtype", [("l", "<f4"), ("b", ">f4")])
    def test_raw(self, loaded_app, qapp, save_window, tmp_path, order, dtype):
        path = self._export(save_window, qapp, tmp_path, "raw", order)
        assert path.endswith(f"_{DET_X}x{DET_Y}x{SCAN_X}x{SCAN_Y}.raw"), path
        got = np.fromfile(path, dtype=dtype).reshape(SCAN_X * SCAN_Y, DET_X * DET_Y)
        assert np.array_equal(got, np.asarray(loaded_app.Data))


class TestExportEmd:
    """py4DSTEM EMD export: the dataset, its calibration and the images selected on the Save Images tab."""

    def _export(self, sw, qapp, tmp_path, ids, binning=1):
        _select_images(sw, ids)
        sw.SaveDir.setText(str(tmp_path))
        sw.SaveTabGroup.setCurrentWidget(sw.ExportTab)
        sw.ExpFormat.setCurrentIndex(sw.ExpFormat.findData("emd"))
        sw.ExpByteOrder.setCurrentIndex(sw.ExpByteOrder.findData("l"))
        sw.ExpFilename.setText("export")
        sw.ExpDimSuff.setChecked(False)
        sw.ExpFrPart.setChecked(False)
        sw.ExpPxPart.setChecked(binning > 1)
        sw.ExpPxPart.clicked.emit(binning > 1)
        if binning > 1:
            sw.EPxX1.setValue(0)
            sw.EPxY1.setValue(0)
            sw.EPxD.setValue(binning)
            sw.ENPxX.setValue(DET_X // binning)
            sw.ENPxY.setValue(DET_Y // binning)
        qapp.processEvents()
        notes = sw.ExpNotes.toPlainText()
        path = notes.splitlines()[0].replace("File: ", "")
        sw.SaveExport.click()
        qapp.processEvents()
        return path, notes

    @pytest.fixture()
    def annular(self, loaded_app, qapp, save_window):
        set_mode(loaded_app, qapp, "AnnMod")
        yield loaded_app
        sw = save_window
        sw.ExpPxPart.setChecked(False)
        sw.ExpPxPart.clicked.emit(False)
        sw.EPxD.setValue(1)
        sw.ExpFormat.setCurrentIndex(sw.ExpFormat.findData("h5"))

    def test_format_listed_with_h5_extension(self, annular, qapp, save_window, tmp_path):
        assert save_window.ExpFormat.findData("emd") >= 0
        path, notes = self._export(save_window, qapp, tmp_path, ["Real"])
        assert path.endswith("export.h5"), path
        assert "py4DSTEM calibration: beam (x, y)" in notes
        assert "Images (selected on the Save Images tab): Real" in notes

    def test_dataset_calibration_and_images(self, annular, qapp, save_window, tmp_path):
        h5py = pytest.importorskip("h5py")
        from pyquant4d.callbacks.io.emd import is_emd, read_emd_info
        app = annular
        path, _ = self._export(save_window, qapp, tmp_path, ["Real", "Dfrn"])
        assert is_emd(path)
        info = read_emd_info(path)
        assert info.shape == (SCAN_Y, SCAN_X, DET_Y, DET_X)
        cal = info.calibration
        assert np.allclose(cal.beam_xy, app.B0)
        assert (cal.q_pixel_size, cal.q_units) == (pytest.approx(app.mradPx.value()), "mrad")
        assert cal.probe_semiangle_mrad == pytest.approx(app.Alpha.value())
        assert sorted(info.images) == ["/pyquant4d_root/datacube/Dfrn", "/pyquant4d_root/datacube/Real"]
        with h5py.File(path) as f:
            dc = f["pyquant4d_root/datacube"]
            assert np.array_equal(dc["data"][()], np.asarray(app.Data).reshape(SCAN_Y, SCAN_X, DET_Y, DET_X))
            assert np.allclose(dc["Real/data"][()], app.Fig.Real.Image)
            assert np.allclose(dc["Dfrn/data"][()], app.Fig.Dfrn.Image)
            assert dc["Real"].attrs["python_class"] == "VirtualImage"
            assert dc["Dfrn"].attrs["python_class"] == "DiffractionSlice"
            meta = f["pyquant4d_root/metadatabundle/pyquant4d"]
            assert np.allclose(meta["beam_center_xy"][()], app.B0)

    def test_binned_calibration(self, annular, qapp, save_window, tmp_path):
        from pyquant4d.callbacks.io.emd import read_emd_info
        app = annular
        path, _ = self._export(save_window, qapp, tmp_path, ["Dfrn"], binning=2)
        info = read_emd_info(path)
        assert info.shape == (SCAN_Y, SCAN_X, DET_Y // 2, DET_X // 2)
        assert info.calibration.q_pixel_size == pytest.approx(2 * app.mradPx.value())
        assert np.allclose(info.calibration.beam_xy, (np.asarray(app.B0, float) + 0.5) / 2 - 0.5)

    def test_uncomputed_images_skipped(self, annular, qapp, save_window, tmp_path, monkeypatch):
        h5py = pytest.importorskip("h5py")
        monkeypatch.setattr(annular.Fig.RealMask, "Image", None)       # not computed yet
        path, notes = self._export(save_window, qapp, tmp_path, ["Real", "RealMask"])
        assert "Not embedded" in notes and notes.rstrip().endswith("RealMask")
        with h5py.File(path) as f:
            assert "Real" in f["pyquant4d_root/datacube"]
            assert "RealMask" not in f["pyquant4d_root/datacube"]

    @pytest.mark.parametrize("normalise, top", [(False, 4.0), (True, 1.0)])
    def test_binned_mask_raw_by_default(self, annular, qapp, save_window, tmp_path, normalise, top):
        h5py = pytest.importorskip("h5py")
        save_window.ExpNormMasks.setChecked(normalise)
        try:
            path, notes = self._export(save_window, qapp, tmp_path, ["DfrnMask"], binning=2)
        finally:
            save_window.ExpNormMasks.setChecked(False)
        assert ("normalised, 0 to 1" if normalise else "raw sums, 0 to 4") in notes
        with h5py.File(path) as f:
            mask = f["pyquant4d_root/datacube/DfrnMask/data"][()]
        expected = annular.Fig.DfrnMask.Image.reshape(DET_Y // 2, 2, DET_X // 2, 2).sum(axis=(1, 3))
        assert np.allclose(mask, expected / (4.0 if normalise else 1.0))
        assert mask.max() == pytest.approx(top)

    def test_normalise_off_by_default(self, annular, save_window):
        assert not save_window.ExpNormMasks.isChecked()

    def test_py4dstem_reads_the_export(self, annular, qapp, save_window, tmp_path):
        py4DSTEM = pytest.importorskip("py4DSTEM")
        app = annular
        path, _ = self._export(save_window, qapp, tmp_path, ["Real"])
        dc = py4DSTEM.read(path)
        bx, by = (float(v) for v in app.B0)
        assert dc.calibration.get_origin_mean() == pytest.approx((by, bx))     # py4DSTEM (row, column)
        assert np.allclose(dc.tree("Real").data, app.Fig.Real.Image)
