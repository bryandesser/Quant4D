"""Settings > Windows > Group into tabs (callbacks.window_groups), with tear-off."""
import pytest
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, import_raw, set_mode


@pytest.fixture()
def win(app, qapp, sample_raw_file):
    import_raw(app, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
    set_mode(app, qapp, "AnnMod")
    app.Fig.RealMask.show()
    qapp.processEvents()
    yield app
    for box in (app.SettingsWindow.GroupReal, app.SettingsWindow.GroupDfrn):
        box.setChecked(False)
    qapp.processEvents()


def _group(win, qapp, space="Real"):
    box = win.SettingsWindow.GroupReal if space == "Real" else win.SettingsWindow.GroupDfrn
    box.setChecked(True)
    qapp.processEvents()
    return win.windowGroups[space]


def _tabs(group):
    return [group.tabs.widget(i).id for i in range(group.tabs.count())]


def test_floating_by_default(app):
    sw = app.SettingsWindow
    assert not sw.GroupReal.isChecked() and not sw.GroupDfrn.isChecked()
    assert sw.GroupReal.toolTip() and sw.RealWindowTab.isAncestorOf(sw.GroupReal)
    assert sw.DfrnWindowTab.isAncestorOf(sw.GroupDfrn)


def test_group_collects_the_shown_windows_of_one_space(win, qapp):
    group = _group(win, qapp)
    assert _tabs(group) == ["RealMask", "Real"]                 # the app's image order
    assert group.isVisible() and group.windowTitle() == "Real-space images"
    assert not win.Fig.Real.isWindow() and win.Fig.Real.isVisible()
    assert win.Fig.Dfrn.isWindow() and win.Fig.Dfrn.isVisible()     # the other space keeps floating
    assert not win.Fig.CoMX.isVisible()                             # hidden ones stay hidden


def test_show_hide_and_activate_go_through_the_group(win, qapp):
    group = _group(win, qapp)
    win.Fig.RealMask.hide()
    assert _tabs(group) == ["Real"] and not win.Fig.RealMask.isVisible()
    assert not win.actionShow_Real_Space_Mask.isChecked()
    win.actionShow_Real_Space_Mask.trigger()                        # the Window menu shows it again
    qapp.processEvents()
    assert _tabs(group) == ["RealMask", "Real"] and win.actionShow_Real_Space_Mask.isChecked()
    win.Fig.RealMask.activateWindow()
    assert group.tabs.currentWidget() is win.Fig.RealMask
    win.Fig.Real.activateWindow()
    qapp.processEvents()
    assert win.SettingsWindow.DispImage.currentData() == "Real"    # the selected tab is the selected image


def test_tab_switch_keeps_menu_ticks(win, qapp):
    group = _group(win, qapp)
    group.tabs.setCurrentWidget(win.Fig.RealMask)
    group.tabs.setCurrentWidget(win.Fig.Real)
    qapp.processEvents()
    assert win.actionShow_Real_Space_Mask.isChecked() and win.actionShow_Real_Space_Image.isChecked()


def test_closing_the_last_tab_hides_the_group(win, qapp):
    group = _group(win, qapp)
    for id in ("Real", "RealMask"):
        win.Fig[id].hide()
    assert group.tabs.count() == 0 and not group.isVisible()
    win.Fig.Real.show()
    assert group.isVisible() and _tabs(group) == ["Real"]


def test_tear_off_and_back(win, qapp):
    group = _group(win, qapp)
    group.tearOff("Real", qtc.QPoint(200, 200))
    fig = win.Fig.Real
    assert fig.isWindow() and fig.isVisible() and _tabs(group) == ["RealMask"]
    fig.activateWindow()                                             # raises the torn-off window
    fig.close()                                                      # closing returns it to the group, hidden
    qapp.processEvents()
    assert not fig.isVisible() and not fig.isWindow() and "Real" not in group.torn
    fig.show()
    assert _tabs(group) == ["RealMask", "Real"]


def _press_drag_release(bar, index, to):
    centre = bar.tabRect(index).center()
    for kind, pos, buttons in ((qtc.QEvent.MouseButtonPress, centre, qtc.Qt.LeftButton),
                               (qtc.QEvent.MouseMove, to, qtc.Qt.LeftButton),
                               (qtc.QEvent.MouseButtonRelease, to, qtc.Qt.NoButton)):
        ev = qtg.QMouseEvent(kind, qtc.QPointF(pos), qtc.QPointF(bar.mapToGlobal(pos)), qtc.Qt.LeftButton,
                             buttons, qtc.Qt.NoModifier)
        qtw.QApplication.sendEvent(bar, ev)


def test_drag_a_tab_out_tears_it_off(win, qapp):
    group = _group(win, qapp)
    index = _tabs(group).index("RealMask")
    _press_drag_release(group.bar, index, qtc.QPoint(5, 400))     # far below the bar
    qapp.processEvents()
    assert "RealMask" in group.torn and win.Fig.RealMask.isWindow()


def test_double_click_tears_off(win, qapp):
    group = _group(win, qapp)
    index = _tabs(group).index("Real")
    pos = group.bar.tabRect(index).center()
    ev = qtg.QMouseEvent(qtc.QEvent.MouseButtonDblClick, qtc.QPointF(pos), qtc.QPointF(group.bar.mapToGlobal(pos)),
                         qtc.Qt.LeftButton, qtc.Qt.LeftButton, qtc.Qt.NoModifier)
    qtw.QApplication.sendEvent(group.bar, ev)
    qapp.processEvents()
    assert "Real" in group.torn


def test_ungroup_floats_everything_back(win, qapp):
    before = win.Fig.RealMask.geometry()
    group = _group(win, qapp)
    group.tearOff("Real", qtc.QPoint(300, 300))
    win.Fig.CoMX  # hidden, parked in the group
    win.SettingsWindow.GroupReal.setChecked(False)
    qapp.processEvents()
    assert "Real" not in getattr(win, "windowGroups", {})
    for id in ("Real", "RealMask"):
        assert win.Fig[id].isWindow() and win.Fig[id].isVisible() and win.Fig[id].group is None
    assert win.Fig.RealMask.geometry() == before
    assert win.Fig.CoMX.isWindow() and not win.Fig.CoMX.isVisible()


def test_mode_changes_add_and_remove_tabs(win, qapp):
    group = _group(win, qapp)
    set_mode(win, qapp, "CoMMod")
    for id in ("CoMPhMag", "iCoM", "dCoM"):
        assert id in _tabs(group), id
    set_mode(win, qapp, "AnnMod")
    assert not any(id in _tabs(group) for id in ("CoMPhMag", "iCoM", "dCoM"))


def test_images_still_draw_in_tabs(win, qapp):
    group = _group(win, qapp)
    group.tabs.setCurrentWidget(win.Fig.Real)
    qapp.processEvents()
    win.Fig.Real.canvas.draw()
    assert win.Fig.Real.scaleBar.label                               # the scale bar draws inside the tab
    win.Fig.Real.toolbar.set_message("x=1, y=2\n3")
    assert win.Fig.Real.statusBar().currentMessage() == "x=1, y=2  3"


def test_group_both_spaces(win, qapp):
    _group(win, qapp, "Real")
    dfrn = _group(win, qapp, "Dfrn")
    win.Fig.DfrnMask.show()
    assert set(_tabs(dfrn)) == {"Dfrn", "DfrnMask"} and win.windowGroups["Real"] is not dfrn
