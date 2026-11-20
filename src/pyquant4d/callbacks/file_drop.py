"""Drop a dataset file on any pyQuant4D window to open it in the Import window.

One :class:`FileDropFilter` is installed on the application, so a drop is
caught whichever widget is under the cursor (the path field, an image canvas,
a panel).  The windows accept drops; the filter takes only local files, and
only while importing is possible.  The first file is opened; any others are
mentioned in the import notes.

The drop handler never calls ``self.sender()``: it runs from an event, not a
slot (cf. the Linux segfault fixed in 664d923).

Troubleshooting: on Windows, a program run as Administrator cannot receive
drops from Explorer (User Interface Privilege Isolation shows a no-entry
cursor); pyQuant4D says so on the console at startup.  Set the environment
variable ``PYQUANT4D_DEBUG_DROP=1`` to print every drag event the filter sees
and what it decided.
"""
from __future__ import annotations

import os
import sys

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

__all__ = ["FileDropFilter", "droppedFiles", "installFileDrop", "openDroppedFiles", "runningElevated"]

_DEBUG = os.environ.get("PYQUANT4D_DEBUG_DROP", "") not in ("", "0")


def _debug(*parts) -> None:
    if _DEBUG:
        print("[pyQuant4D drop]", *parts, file=sys.stderr, flush=True)


def runningElevated() -> bool:
    """True on Windows when running as Administrator (Explorer then cannot drop files on us)."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


_DRAG_EVENTS = (qtc.QEvent.Type.DragEnter, qtc.QEvent.Type.DragMove, qtc.QEvent.Type.Drop)


def droppedFiles(mime: qtc.QMimeData | None) -> list[str]:
    """The local files (not folders) in a drag's data, in order, with the system's separators
    (Qt gives ``C:/...`` on Windows, which then showed in the Import window's path field)."""
    if mime is None or not mime.hasUrls():
        return []
    paths = (os.path.normpath(url.toLocalFile()) for url in mime.urls() if url.isLocalFile())
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
        mime = event.mimeData()
        files = droppedFiles(mime)
        accepting = bool(files) and self._accepting()
        if event.type() != qtc.QEvent.Type.DragMove:
            _debug(f"{'enter' if event.type() == qtc.QEvent.Type.DragEnter else 'drop'} on "
                   f"{type(obj).__name__} {obj.objectName()!r}: urls={[u.toString() for u in mime.urls()] if mime else []} "
                   f"files={files} accepting={accepting}")
        if not accepting:
            return False
        event.setDropAction(qtc.Qt.DropAction.CopyAction)
        event.accept()
        if event.type() == qtc.QEvent.Type.Drop:
            self.filesDropped.emit(files)
        return True


def openDroppedFiles(self, files: list[str]) -> None:
    """Open the first dropped file in the Import window, as if picked with Select."""
    if not files:
        return
    from .import_io import importSelectFile  # noqa: E402
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
    app = qtw.QApplication.instance()
    assert app is not None, "a QApplication is needed"
    app.installEventFilter(drop)
    self.fileDrop = drop
    if runningElevated():
        print("pyQuant4D is running as Administrator: Windows does not let Explorer drop files on it. "
              "Start it from a normal (not elevated) prompt to use drag and drop.", file=sys.stderr, flush=True)
    _debug(f"filter installed on {len(windows)} windows")
    return drop
