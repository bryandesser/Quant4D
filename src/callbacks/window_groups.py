"""Group the image windows of one space into a single tabbed window.

Settings > Windows > Diffraction / Real-space > **Group into tabs** collects that
space's image windows into one :class:`GroupWindow`, a tab each (unticked, the
default: every image floats in its own window).  Each tab *is* the image
window (a QMainWindow embedded as a widget), so its toolbar, status bar, scale
bar, zoom and annotations come with it.

* Drag a tab out of the tab bar, double-click it, or right-click > Float to
  **tear it off**: the image floats in its own window.  Closing a torn-off
  window returns the image to the group (hidden, like closing a tab), so
  showing it again puts it back in a tab.
* Showing, hiding and activating an image (Show buttons, Window menu,
  shortcuts, mode changes) go through :class:`ImageWindow`'s ``show``,
  ``hide``, ``isVisible`` and ``activateWindow``, which ask the group when the
  image is grouped: "shown" means in a tab (or torn off), and activating it
  selects its tab.
* Unticking the box floats every image again where it was before grouping
  (torn-off ones stay where they are); hidden images stay hidden.
"""
from __future__ import annotations

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw

__all__ = ["GroupWindow", "TearOffTabBar", "spaceIds", "setGrouped", "connectWindowGroups"]

SPACE_NAMES = {"Dfrn": "Diffraction", "Real": "Real-space"}


def spaceIds(self, space: str) -> list:
    """The image windows a group of *space* holds, in the app's image order (not Preview/ColorWheel)."""
    return [id for id, sp in zip(self.G.ImgID, self.G.ImgSpace) if sp == space and self.Fig[id] is not None]


class TearOffTabBar(qtw.QTabBar):
    """A tab bar whose tabs can be dragged out (or double-clicked) to float them."""
    tearOff = qtc.pyqtSignal(int, qtc.QPoint)
    closeRequested = qtc.pyqtSignal(int)

    MARGIN = 30          # px past the bar before a drag counts as tearing off

    def __init__(self, parent=None):
        super().__init__(parent)
        self._press = None

    def mousePressEvent(self, e):
        if e.button() == qtc.Qt.LeftButton:
            self._press = self.tabAt(e.pos())
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self._press is not None and self._press >= 0 and e.buttons() & qtc.Qt.LeftButton:
            if not self.rect().adjusted(-self.MARGIN, -self.MARGIN, self.MARGIN, self.MARGIN).contains(e.pos()):
                index, self._press = self._press, None
                self.tearOff.emit(index, e.globalPos())
                return
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        self._press = None
        super().mouseReleaseEvent(e)

    def mouseDoubleClickEvent(self, e):
        index = self.tabAt(e.pos())
        if index >= 0:
            self.tearOff.emit(index, e.globalPos())
            return
        super().mouseDoubleClickEvent(e)

    def contextMenuEvent(self, e):
        index = self.tabAt(e.pos())
        if index < 0:
            return
        menu = qtw.QMenu(self)
        floating = menu.addAction("Float in its own window")
        close = menu.addAction("Close")
        chosen = menu.exec_(e.globalPos())
        if chosen is floating:
            self.tearOff.emit(index, e.globalPos())
        elif chosen is close:
            self.closeRequested.emit(index)


class GroupWindow(qtw.QMainWindow):
    """One space's image windows as tabs."""

    def __init__(self, app, space: str):
        super().__init__()
        self.app, self.space = app, space
        self.setWindowTitle(f"{SPACE_NAMES[space]} images")
        self.setObjectName(f"{space}Group")
        self.tabs = qtw.QTabWidget(self)
        self.bar = TearOffTabBar(self.tabs)
        self.tabs.setTabBar(self.bar)
        self.tabs.setTabsClosable(True)
        self.tabs.setDocumentMode(True)
        self.setCentralWidget(self.tabs)
        self.members = spaceIds(app, space)
        self.torn = set()                   # ids floating on their own
        self.saved = {}                     # id -> geometry before grouping (restored on ungroup)
        self.bar.tearOff.connect(lambda i, pos: qtc.QTimer.singleShot(0, lambda: self.tearOff(self._idAt(i), pos)))
        self.bar.closeRequested.connect(lambda i: self.app.Fig[self._idAt(i)].hide())
        self.tabs.tabCloseRequested.connect(lambda i: self.app.Fig[self._idAt(i)].hide())
        self.tabs.currentChanged.connect(self._tabChanged)
        self.shortcut = qtw.QShortcut(qtg.QKeySequence("Ctrl+W"), self)
        self.shortcut.activated.connect(self._closeCurrent)
        self.setAttribute(qtc.Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)

    # ------------------------------------------------------------------ helpers
    def _idAt(self, index: int):
        widget = self.tabs.widget(index)
        return getattr(widget, "id", None)

    def _tabIndex(self, fig) -> int:
        return self.tabs.indexOf(fig)

    def _insertTab(self, fig) -> None:
        if self._tabIndex(fig) >= 0:
            return
        order = self.members.index(fig.id)
        pos = sum(1 for i in range(self.tabs.count()) if self.members.index(self._idAt(i)) < order)
        self.tabs.insertTab(pos, fig, fig.windowTitle())
        fig.shortcut.setEnabled(False)      # the group's Ctrl+W closes the current tab

    def _park(self, fig) -> None:
        """Keep *fig* in the group, hidden and out of the tabs."""
        index = self._tabIndex(fig)
        if index >= 0:
            self.tabs.removeTab(index)
        fig.setParent(self, qtc.Qt.Widget)
        qtw.QMainWindow.hide(fig)

    def _closeCurrent(self) -> None:
        id = self._idAt(self.tabs.currentIndex())
        if id is not None:
            self.app.Fig[id].hide()

    def _tabChanged(self, index: int) -> None:
        id = self._idAt(index)
        if id is None:
            return
        from callbacks.window_manager import showImageContent  # noqa: E402
        showImageContent(self.app, id)                       # a tab not shown was not redrawn
        sw = self.app.SettingsWindow
        if not sw.DispLock.isChecked() and sw.DispImage.findData(id) >= 0 and sw.DispImage.currentData() != id:
            sw.DispImage.setCurrentIndex(sw.DispImage.findData(id))   # the selected tab is the selected image

    # ------------------------------------------------------------------ membership API (ImageWindow)
    def isShown(self, fig) -> bool:
        if fig.id in self.torn:
            return qtw.QMainWindow.isVisible(fig)
        return self._tabIndex(fig) >= 0 and qtw.QMainWindow.isVisible(self)

    def showMember(self, fig) -> None:
        if fig.id in self.torn:
            qtw.QMainWindow.show(fig)
        else:
            self._insertTab(fig)
            qtw.QMainWindow.show(self)
        fig._syncMenuAction(True)

    def hideMember(self, fig) -> None:
        if fig.id in self.torn:                 # closing a torn-off image returns it to the group
            self.torn.discard(fig.id)
            qtw.QMainWindow.hide(fig)
        self._park(fig)
        fig._syncMenuAction(False)
        if self.tabs.count() == 0:
            qtw.QMainWindow.hide(self)

    def selectMember(self, fig) -> None:
        if fig.id in self.torn:
            qtw.QMainWindow.raise_(fig)
            qtw.QMainWindow.activateWindow(fig)
            return
        if self._tabIndex(fig) >= 0:
            self.tabs.setCurrentWidget(fig)
        self.raise_()
        qtw.QMainWindow.activateWindow(self)

    def tearOff(self, id, global_pos=None) -> None:
        """Float image *id* in its own window (at *global_pos*, if given)."""
        if id is None or id in self.torn:
            return
        fig = self.app.Fig[id]
        size = self.tabs.currentWidget().size() if self.tabs.currentWidget() is not None else fig.size()
        index = self._tabIndex(fig)
        if index >= 0:
            self.tabs.removeTab(index)
        fig.setParent(None)
        fig.setWindowFlags(qtc.Qt.Window)
        fig.shortcut.setEnabled(True)
        self.torn.add(id)
        if global_pos is not None:
            fig.setGeometry(qtc.QRect(global_pos - qtc.QPoint(40, 10), size))
        else:
            fig.resize(size)
        qtw.QMainWindow.show(fig)
        fig._syncMenuAction(True)
        if self.tabs.count() == 0:
            qtw.QMainWindow.hide(self)

    # ------------------------------------------------------------------ whole group
    def adopt(self) -> None:
        """Move this space's windows in: shown ones as tabs, the others parked."""
        first = None
        for id in self.members:
            fig = self.app.Fig[id]
            shown = qtw.QMainWindow.isVisible(fig)
            self.saved[id] = fig.geometry()
            if shown and first is None:
                first = fig.frameGeometry()
            fig.group = self
            if shown:
                self._insertTab(fig)
            else:
                self._park(fig)
        if first is not None:
            self.setGeometry(first.adjusted(0, 0, 0, self.tabs.tabBar().sizeHint().height()))
            qtw.QMainWindow.show(self)
        else:
            self.resize(self.app.Fig[self.members[0]].size())
        for id in self.members:
            self.app.Fig[id].windowTitleChanged.connect(self._retitle)

    def _retitle(self, title: str) -> None:
        fig = self.sender()
        index = self._tabIndex(fig) if fig is not None else -1
        if index >= 0:
            self.tabs.setTabText(index, title)

    def release(self) -> None:
        """Float every image again: tabs and torn-off ones shown, the rest hidden."""
        for id in self.members:
            fig = self.app.Fig[id]
            try:
                fig.windowTitleChanged.disconnect(self._retitle)
            except TypeError:
                pass
            shown = self.isShown(fig)
            torn = id in self.torn
            index = self._tabIndex(fig)
            if index >= 0:
                self.tabs.removeTab(index)
            fig.group = None
            if not torn:
                fig.setParent(None)
                fig.setWindowFlags(qtc.Qt.Window)
                if id in self.saved:
                    fig.setGeometry(self.saved[id])
            fig.shortcut.setEnabled(True)
            if shown:
                qtw.QMainWindow.show(fig)
            else:
                qtw.QMainWindow.hide(fig)
            fig._syncMenuAction(shown)
        self.torn.clear()
        qtw.QMainWindow.hide(self)

    def closeEvent(self, a0) -> None:
        """Closing the group window hides its tabbed images (torn-off ones stay)."""
        for i in reversed(range(self.tabs.count())):
            self.app.Fig[self._idAt(i)].hide()
        a0.ignore()
        qtw.QMainWindow.hide(self)


def setGrouped(self, space: str, on: bool) -> None:
    """Group (or float again) the image windows of *space*."""
    groups = self.__dict__.setdefault("windowGroups", {})
    group = groups.get(space)
    if on and group is None:
        group = groups[space] = GroupWindow(self, space)
        group.adopt()
    elif not on and group is not None:
        group.release()
        del groups[space]
        group.deleteLater()


def matchWindowTabs(self) -> None:
    """Settings > Windows > Diffraction and Real-space: the same layout on both tabs, so nothing
    shifts when switching between them.  The texts differ ("Set All Diffraction" / "Set All Real",
    the unit lists), and the grids sized their columns from each widget's size hint; now the widgets
    in the same cell get the same minimum width and their hints are ignored, so the columns come
    from those minimums and the equal column stretch alone."""
    from PyQt5.QtWidgets import QLayout, QSizePolicy
    sw = self.SettingsWindow
    # the Scale / Scan Step boxes take any value up to 1e6: their hint asked for more width than
    # the window has
    for box in (sw.DfScale, sw.RsStep):
        box.setMinimumWidth(70)

    def cells(grid):
        out = {}
        for i in range(grid.count()):
            item = grid.itemAt(i)
            out[grid.getItemPosition(i)] = item.widget() if item.widget() is not None else item.layout()
        return out

    def match(a, b):
        if isinstance(a, QLayout):                      # a nested layout (the W / H fields): pair by index
            for i in range(min(a.count(), b.count())):
                wa, wb = a.itemAt(i).widget(), b.itemAt(i).widget()
                if wa is not None and wb is not None:
                    match(wa, wb)
            return
        if a.sizePolicy().horizontalPolicy() == QSizePolicy.Fixed:     # the axis buttons: already alike
            return
        width = max(a.minimumWidth() or a.minimumSizeHint().width(),
                    b.minimumWidth() or b.minimumSizeHint().width())
        for w in (a, b):
            w.setMinimumWidth(width)
            policy = w.sizePolicy()
            policy.setHorizontalPolicy(QSizePolicy.Ignored)
            w.setSizePolicy(policy)

    real = cells(sw.RealWindowGrid)
    for cell, a in cells(sw.DfrnWindowGrid).items():
        b = real.get(cell)
        if b is not None:
            match(a, b)


def connectWindowGroups(self) -> None:
    """The Group into tabs boxes; called once from ``slotsSignals``."""
    sw = self.SettingsWindow
    sw.GroupDfrn.toggled.connect(lambda on: setGrouped(self, "Dfrn", on))
    sw.GroupReal.toggled.connect(lambda on: setGrouped(self, "Real", on))
