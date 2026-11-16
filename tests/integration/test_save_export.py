"""
Integration tests — Section 4.9 (Save / Export).

Each test writes to a pytest tmp_path and reads back to verify correctness.
No real data file is required — the synthetic dataset from conftest is used.
"""

import numpy as np
import pytest
from pytestqt.qt_compat import qt_api
Qt = qt_api.QtCore.Qt
from pathlib import Path


class TestSaveTIFF:
    def test_save_tiff_float32(self, app, qtbot, tmp_path):
        """saveCallbacks should write a 32-bit float TIFF."""
        import tifffile

        out = tmp_path / "real.tif"
        # Set the save path in the UI
        app.SaveWindow.SavePath.setText(str(out.parent))
        app.SaveWindow.SaveName.setText("real")
        # Trigger save
        qtbot.mouseClick(app.SaveWindow.SaveTIFF,
                         Qt.LeftButton)
        qtbot.wait(200)

        assert out.exists(), f"TIFF not created at {out}"
        arr = tifffile.imread(out)
        assert arr.dtype == np.float32
        assert arr.ndim == 2

    def test_save_png(self, app, qtbot, tmp_path):
        from PIL import Image

        out = tmp_path / "real.png"
        app.SaveWindow.SavePath.setText(str(out.parent))
        app.SaveWindow.SaveName.setText("real")
        qtbot.mouseClick(app.SaveWindow.SavePNG,
                         Qt.LeftButton)
        qtbot.wait(200)

        assert out.exists()
        img = Image.open(out)
        assert img.size[0] > 0


class TestExportHDF5:
    def test_hdf5_structure(self, app, qtbot, tmp_path):
        h5py = pytest.importorskip("h5py")

        out = tmp_path / "export.h5"
        app.SaveWindow.ExportPath.setText(str(out.parent))
        app.SaveWindow.ExportName.setText("export")
        qtbot.mouseClick(app.SaveWindow.ExportHDF5,
                         Qt.LeftButton)
        qtbot.wait(500)

        assert out.exists()
        with h5py.File(out, "r") as f:
            assert "data" in f
            assert "metadata" in f

    def test_hdf5_values_match(self, app, qtbot, tmp_path):
        h5py = pytest.importorskip("h5py")

        out = tmp_path / "values.h5"
        app.SaveWindow.ExportPath.setText(str(out.parent))
        app.SaveWindow.ExportName.setText("values")
        qtbot.mouseClick(app.SaveWindow.ExportHDF5,
                         Qt.LeftButton)
        qtbot.wait(500)

        with h5py.File(out, "r") as f:
            stored = f["data"][:]

        np.testing.assert_allclose(
            stored.reshape(app.D.Data.shape),
            app.D.Data,
            rtol=1e-5
        )


class TestSaveVect:
    def test_com_tiffs_written(self, app, qtbot, tmp_path):
        """saveVect should produce CoMX.tif and CoMY.tif as float32."""
        import tifffile

        # Put synthetic CoM data in place
        app.D.CoMX = np.random.rand(8, 8).astype(np.float32)
        app.D.CoMY = np.random.rand(8, 8).astype(np.float32)

        app.SaveWindow.SavePath.setText(str(tmp_path))
        app.SaveWindow.SaveName.setText("stem")
        qtbot.mouseClick(app.SaveWindow.SaveVect,
                         Qt.LeftButton)
        qtbot.wait(200)

        for name in ("stem_CoMX.tif", "stem_CoMY.tif"):
            p = tmp_path / name
            assert p.exists(), f"Missing {name}"
            arr = tifffile.imread(p)
            assert arr.dtype == np.float32
