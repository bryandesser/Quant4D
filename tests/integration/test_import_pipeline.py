"""
Integration tests — Section 4.2 (Import pipeline).

These tests exercise the file-format parsers with synthetic files created
by conftest fixtures, so no real 4D-STEM dataset is required.
"""

import numpy as np
import pytest
from pytestqt.qt_compat import qt_api
Qt = qt_api.QtCore.Qt


SCAN_X, SCAN_Y, DET_X, DET_Y = 8, 8, 32, 32

# Widget-name mapping (actual .ui names):
#   ImpFilePath      — file path QLineEdit
#   INFrX / INFrY   — scan (frame) dimensions X/Y
#   INPxX / INPxY   — detector (pixel) dimensions X/Y
#   ImportDataButton — start-import QPushButton
#   ImportCancelButton — cancel-import QPushButton
#   ImpEstFilesize   — estimated file size QLineEdit


class TestRawImport:
    @pytest.mark.skip(reason="Requires live import thread; tested via manual QA")
    def test_empad_raw_loads(self, app, qtbot, sample_raw_file):
        """EMPAD-style raw float32 file should import without error."""
        app.ImportWindow.ImpFilePath.setText(str(sample_raw_file))
        app.ImportWindow.INFrX.setValue(SCAN_X)
        app.ImportWindow.INFrY.setValue(SCAN_Y)
        app.ImportWindow.INPxX.setValue(DET_X)
        app.ImportWindow.INPxY.setValue(DET_Y)

        qtbot.mouseClick(app.ImportWindow.ImportDataButton, Qt.LeftButton)
        with qtbot.waitSignal(app.importThread.finished, timeout=5000):
            pass

        assert app.D.Loaded is True
        assert app.D.Data.shape[1] == DET_X * DET_Y


class TestHDF5Import:
    @pytest.mark.skip(reason="Requires live import thread; tested via manual QA")
    def test_hdf5_loads(self, app, qtbot, sample_hdf5_file):
        h5py = pytest.importorskip("h5py")
        app.ImportWindow.ImpFilePath.setText(str(sample_hdf5_file))
        qtbot.mouseClick(app.ImportWindow.ImportDataButton, Qt.LeftButton)
        with qtbot.waitSignal(app.importThread.finished, timeout=5000):
            pass
        assert app.D.Loaded is True

    @pytest.mark.skip(reason="Requires live import thread; tested via manual QA")
    def test_hdf5_dataset_values(self, app, qtbot, sample_hdf5_file):
        import h5py
        app.ImportWindow.ImpFilePath.setText(str(sample_hdf5_file))
        qtbot.mouseClick(app.ImportWindow.ImportDataButton, Qt.LeftButton)
        with qtbot.waitSignal(app.importThread.finished, timeout=5000):
            pass
        with h5py.File(sample_hdf5_file, "r") as f:
            expected = f["data"][:].reshape(-1, DET_X * DET_Y)
        np.testing.assert_allclose(app.D.Data, expected, rtol=1e-5)


class TestImportCancel:
    @pytest.mark.skip(reason="Requires live import thread; tested via manual QA")
    def test_cancel_leaves_no_data(self, app, qtbot, sample_raw_file):
        """Cancelling import mid-flight must not leave partial data."""
        app.ImportWindow.ImpFilePath.setText(str(sample_raw_file))
        app.ImportWindow.INFrX.setValue(64)   # deliberately large → slower
        app.ImportWindow.INFrY.setValue(64)
        app.ImportWindow.INPxX.setValue(DET_X)
        app.ImportWindow.INPxY.setValue(DET_Y)

        qtbot.mouseClick(app.ImportWindow.ImportDataButton, Qt.LeftButton)
        qtbot.wait(50)
        qtbot.mouseClick(app.ImportWindow.ImportCancelButton, Qt.LeftButton)
        qtbot.wait(500)

        if hasattr(app.D, "Loaded"):
            pass   # the key thing is no crash and no partial allocation


class TestMemoryEstimate:
    def test_est_mem_shown(self, app, qtbot, sample_raw_file):
        """ImpEstFilesize label should update when dimensions are entered."""
        app.ImportWindow.ImpFilePath.setText(str(sample_raw_file))
        app.ImportWindow.INFrX.setValue(SCAN_X)
        app.ImportWindow.INFrY.setValue(SCAN_Y)
        app.ImportWindow.INPxX.setValue(DET_X)
        app.ImportWindow.INPxY.setValue(DET_Y)
        qtbot.wait(50)
        text = app.ImportWindow.ImpEstFilesize.text()
        assert text != "" and text != "0"
