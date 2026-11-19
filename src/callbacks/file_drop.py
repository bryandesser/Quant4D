"""Drop a dataset file on any pyQuant4D window to open it in the Import window.

One :class:`FileDropFilter` is installed on the application, so a drop is
caught whichever widget is under the cursor (the path field, an image canvas,
a panel).  The windows accept drops; the filter takes only local files, and
only while importing is possible.  The first file is opened; any others are
mentioned in the import notes.

The drop handler never calls ``self.sender()``: it runs from an event, not a
slot (cf. the Linux segfault fixed in 664d923).
"""
from __future__ import annotations

import os

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

__all__ = ["FileDropFilter", "droppedFiles", "installFileDrop", "openDroppedFiles"]

_DRAG_EVENTS = (qtc.QEvent.DragEnter, qtc.QEvent.DragMove, qtc.QEvent.Drop)


def droppedFiles(mime: qtc.QMimeData | None) -> list[str]:
    """The local files (not folders) in a drag's data, in order."""
    if mime is None or not mime.hasUrls():
        return []
    paths = (url.toLocalFile() for url in mime.urls() if url.isLocalFile())
    return [p for p in paths if p and os.path.isfile(p)]


class FileDropFilter(qtc.QObject):
    """Application event filter turning file drops on *windows* into :attr:`filesDropped`.

    *accepting* says whether a drop would be used now (e.g. not while an
    import is running).  Drops on other windows (file dialogs, message boxes,
    another main window) are left alone.
    """
    filesDropped = qtc.pyqtSignal(list)

    def __init__(self, windows, accepting=lambda: True, parent=None):
        super().__init__(parent)
        self._windows = list(windows)
        self._accepting = accepting

    def eventFilter(self, obj, event):
        if event.type() not in _DRAG_EVENTS or not isinstance(obj, qtw.QWidget):
            return False
        if not any(obj.window() is w for w in self._windows):
            return False
        files = droppedFiles(event.mimeData())
        if not files or not self._accepting():
            return False
        event.setDropAction(qtc.Qt.CopyAction)
        event.accept()
        if event.type() == qtc.QEvent.Drop:
            self.filesDropped.emit(files)
        return True


def openDroppedFiles(self, files: list[str]) -> None:
    """Open the first dropped file in the Import window, as if picked with Select."""
    if not files:
        return
    from callbacks.import_io import importSelectFile  # noqa: E402
    iw = self.ImportWindow
    if not iw.isVisible():
        self.ShowImportWdw.trigger()
    importSelectFile(self, path=files[0])
    if len(files) > 1:
        others = ", ".join(os.path.basename(f) for f in files[1:])
        iw.ImpNotes.append(f"\n{len(files)} files were dropped; only the first is opened (not: {others}).")
    iw.raise_()
    iw.activateWindow()


def installFileDrop(self) -> FileDropFilter:
    """Let every window accept file drops and open them through :func:`openDroppedFiles`."""
    windows = [self, self.ImportWindow, self.SettingsWindow, self.SaveWindow]
    windows += [fig for fig in self.Fig.values() if isinstance(fig, qtw.QWidget)]
    for w in windows:
        w.setAcceptDrops(True)
    drop = FileDropFilter(windows, parent=self,
                          accepting=lambda: self.ShowImportWdw.isEnabled() and self.ImportWindow.isEnabled())
    drop.filesDropped.connect(lambda files: openDroppedFiles(self, files))
    qtw.QApplication.instance().installEventFilter(drop)
    self.fileDrop = drop
    return drop
