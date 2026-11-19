"""Drag and drop a dataset file onto any window (callbacks.file_drop).

Drops are simulated by sending QDragEnterEvent/QDropEvent to a widget; they
pass through the application event filter exactly as a real drop does.
(``test_drag.py`` is about mouse drags on the images.)
"""
import numpy as np
import pytest
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y


def _mime(*paths):
    mime = qtc.QMimeData()
    mime.setUrls([qtc.QUrl.fromLocalFile(str(p)) for p in paths])
    return mime


def _drag_enter(widget, *paths) -> bool:
    mime = _mime(*paths)                           # kept alive: the event does not own it
    ev = qtg.QDragEnterEvent(qtc.QPoint(2, 2), qtc.Qt.CopyAction, mime,
                             qtc.Qt.LeftButton, qtc.Qt.NoModifier)
    qtw.QApplication.sendEvent(widget, ev)
    return ev.isAccepted()


def _drop(qapp, widget, *paths) -> bool:
    """Drag over *widget* and drop, as Qt does: the drop goes to the widget that took the drag."""
    if not _drag_enter(widget, *paths):
        return False
    mime = _mime(*paths)                           # kept alive: the event does not own it
    ev = qtg.QDropEvent(qtc.QPointF(2, 2), qtc.Qt.CopyAction, mime,
                        qtc.Qt.LeftButton, qtc.Qt.NoModifier)
    qtw.QApplication.sendEvent(widget, ev)
    qapp.processEvents()
    return ev.isAccepted()


@pytest.fixture()
def emd_file(tmp_path, synthetic_data):
    from callbacks.io.emd import EmdCalibration, EmdImage, write_emd
    from callbacks.io.export import full_region
    p = tmp_path / "py4dstem.emd"
    write_emd(str(p), synthetic_data, (SCAN_X, SCAN_Y), (DET_X, DET_Y),
              full_region((SCAN_X, SCAN_Y)), full_region((DET_X, DET_Y)),
              EmdCalibration(beam_xy=(10.0, 7.0)), {"ADF": EmdImage(np.ones((SCAN_Y, SCAN_X)))})
    return p


def _hdf5_geometry(iw):
    return (iw.DNFrX.value(), iw.DNFrY.value(), iw.DNPxX.value(), iw.DNPxY.value())


class TestDroppedFiles:
    def test_local_files_only(self, tmp_path):
        from callbacks.file_drop import droppedFiles
        f = tmp_path / "a.raw"
        f.write_bytes(b"\0")
        mime = _mime(f, tmp_path, tmp_path / "missing.h5")
        mime.setUrls(mime.urls() + [qtc.QUrl("https://example.com/x.h5")])
        assert droppedFiles(mime) == [str(f)]
        assert droppedFiles(None) == [] and droppedFiles(qtc.QMimeData()) == []


class TestDropOpensImport:
    def test_drop_on_main_window(self, app, qapp, sample_hdf5_file):
        assert _drag_enter(app, sample_hdf5_file)
        assert _drop(qapp, app, sample_hdf5_file)
        iw = app.ImportWindow
        assert iw.isVisible()
        assert iw.ImpFilePath.text() == str(sample_hdf5_file)
        assert iw.HDF5Button.isChecked()
        assert _hdf5_geometry(iw) == (SCAN_X, SCAN_Y, DET_X, DET_Y)
        assert iw.ImportDataButton.isEnabled()

    def test_drop_on_an_image_canvas(self, app, qapp, sample_hdf5_file):
        canvas = [w for w in app.Fig.Dfrn.findChildren(qtw.QWidget) if "Canvas" in type(w).__name__][0]
        assert _drop(qapp, canvas, sample_hdf5_file)
        assert app.ImportWindow.ImpFilePath.text() == str(sample_hdf5_file)

    def test_drop_on_path_field_replaces_the_path(self, app, qapp, sample_hdf5_file, sample_raw_file):
        iw = app.ImportWindow
        app.ShowImportWdw.trigger()
        iw.ImpFilePath.setText(str(sample_raw_file))
        assert _drop(qapp, iw.ImpFilePath, sample_hdf5_file)
        assert iw.ImpFilePath.text() == str(sample_hdf5_file)      # not text inserted into the field

    @pytest.mark.parametrize("ext", [".hdf5", ".emd"])
    def test_hdf5_extensions(self, app, qapp, sample_hdf5_file, tmp_path, ext):
        p = tmp_path / f"copy{ext}"
        p.write_bytes(sample_hdf5_file.read_bytes())
        _drop(qapp, app.SettingsWindow, p)
        assert app.ImportWindow.HDF5Button.isChecked()
        assert _hdf5_geometry(app.ImportWindow) == (SCAN_X, SCAN_Y, DET_X, DET_Y)

    def test_py4dstem_file_selects_the_datacube(self, app, qapp, sample_hdf5_file, emd_file):
        iw = app.ImportWindow
        _drop(qapp, app, sample_hdf5_file)
        _drop(qapp, app, emd_file)                     # a new file: the dataset list starts again
        items = [iw.ImpSubImg.itemText(i) for i in range(iw.ImpSubImg.count())]
        assert "/data" not in items
        assert iw.ImpSubImg.currentText() == "/pyquant4d_root/datacube/data"
        assert _hdf5_geometry(iw) == (SCAN_X, SCAN_Y, DET_X, DET_Y)

    def test_only_the_first_file_is_opened(self, app, qapp, sample_hdf5_file, sample_raw_file):
        _drop(qapp, app, sample_hdf5_file, sample_raw_file)
        iw = app.ImportWindow
        assert iw.ImpFilePath.text() == str(sample_hdf5_file)
        assert "only the first is opened" in iw.ImpNotes.toPlainText()
        assert sample_raw_file.name in iw.ImpNotes.toPlainText()


class TestDropRefused:
    def test_folder_is_refused(self, app, qapp, tmp_path):
        assert not _drag_enter(app, tmp_path)
        assert not _drop(qapp, app, tmp_path)
        assert not app.ImportWindow.isVisible()

    def test_refused_while_importing(self, app, qapp, sample_hdf5_file):
        app.ImportWindow.setEnabled(False)             # as during an import
        try:
            assert not _drag_enter(app, sample_hdf5_file)
            assert not _drop(qapp, app, sample_hdf5_file)
        finally:
            app.ImportWindow.setEnabled(True)
        assert app.ImportWindow.ImpFilePath.text() != str(sample_hdf5_file)

    def test_other_windows_left_alone(self, app, qapp, sample_hdf5_file):
        other = qtw.QWidget()
        other.setAcceptDrops(True)
        assert not _drop(qapp, other, sample_hdf5_file)
        assert app.ImportWindow.ImpFilePath.text() != str(sample_hdf5_file)
        other.deleteLater()


def test_select_and_typed_path_still_work(app, qapp, sample_hdf5_file, monkeypatch):
    """The Select button and a typed path go through the same code with an explicit source."""
    import callbacks.import_io as io
    iw = app.ImportWindow
    app.ShowImportWdw.trigger()
    monkeypatch.setattr(io, "_chooseFile", lambda self: str(sample_hdf5_file))
    iw.ImpFileSelect.click()
    qapp.processEvents()
    assert iw.ImpFilePath.text() == str(sample_hdf5_file) and iw.HDF5Button.isChecked()
    monkeypatch.setattr(io, "_chooseFile", lambda self: None)      # cancelled: nothing changes
    iw.ImpFileSelect.click()
    assert iw.ImpFilePath.text() == str(sample_hdf5_file)
