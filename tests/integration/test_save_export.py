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
        from callbacks.io.export import rgb_as_displayed
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
