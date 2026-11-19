"""Bryan's third interactive-testing round of 2026-11-20."""
import numpy as np
import pytest
from matplotlib.backend_bases import MouseEvent

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, import_raw, set_mode


def _drag(fig, start, end, release=True):
    canvas = fig.canvas
    canvas.draw()
    p0, p1 = fig.ax.transData.transform(start), fig.ax.transData.transform(end)
    canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, *p0))
    canvas.callbacks.process("button_press_event", MouseEvent("button_press_event", canvas, *p0, button=1))
    canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, *p1))
    if release:
        canvas.callbacks.process("button_release_event", MouseEvent("button_release_event", canvas, *p1, button=1))


# ---------------------------------------------------------------------- first window layout
def test_image_windows_start_beside_settings_at_the_top(app, qapp, sample_raw_file):
    import_raw(app, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
    qapp.processEvents()
    sw, F = app.SettingsWindow, app.Fig
    top = sw.screen().availableGeometry().top()
    assert F.Dfrn.frameGeometry().left() > sw.frameGeometry().right() - 5          # right of Settings
    assert F.Real.frameGeometry().left() > F.Dfrn.frameGeometry().left() + 100     # then real space
    # (side by side when the screen is wide enough; this offscreen one is 800 px)
    for id in ("Dfrn", "DfrnMask", "Real", "RealMask", "CoMX", "iCoM"):
        assert F[id].frameGeometry().top() <= top + 5, id                          # all at the top
    assert F.DfrnMask.geometry() == F.Dfrn.geometry() and F.RealMask.geometry() == F.Real.geometry()
    assert F.Dfrn.width() == F.Real.width() and sw.WdwWDfrn.value() == sw.WdwWReal.value()
    moved = F.Real.geometry().translated(40, 40)
    F.Real.setGeometry(moved)
    from callbacks.window_manager import placeImageWindows
    placeImageWindows(app)                                     # once only: a later import keeps it
    assert F.Real.geometry() == moved


# ---------------------------------------------------------------------- Real on top in CoM/DPC
def test_real_space_comes_up_last_in_com(loaded_app, qapp, monkeypatch):
    calls = []
    for id in ("CoMPhMag", "iCoM", "dCoM", "Real"):
        fig = loaded_app.Fig[id]
        monkeypatch.setattr(fig, "show", lambda _id=id, _f=fig: (calls.append(("show", _id)), type(_f).show(_f)))
    monkeypatch.setattr(loaded_app.Fig.Real, "raise_",
                        lambda _f=loaded_app.Fig.Real: (calls.append(("raise", "Real")), type(_f).raise_(_f)))
    set_mode(loaded_app, qapp, "AnnMod")
    calls.clear()
    set_mode(loaded_app, qapp, "CoMMod")
    shown = [c for c in calls if c[0] == "show"]
    assert {c[1] for c in shown} >= {"CoMPhMag", "iCoM", "dCoM", "Real"}
    assert shown[-1] == ("show", "Real") and calls[-1] == ("raise", "Real")
    set_mode(loaded_app, qapp, "AnnMod")


# ---------------------------------------------------------------------- Settings > Windows tabs
def test_window_tabs_have_identical_layouts(loaded_app, qapp):
    sw = loaded_app.SettingsWindow
    sw.show()
    sw.SettingsTabGroup.setCurrentWidget(sw.WindowsTab)
    rects = []
    for tab, grid in ((sw.DfrnWindowTab, sw.DfrnWindowGrid), (sw.RealWindowTab, sw.RealWindowGrid)):
        sw.WindowResizeTabGroup.setCurrentWidget(tab)
        qapp.processEvents()
        rects.append([grid.itemAt(i).geometry().getRect() for i in range(grid.count())])
    assert rects[0] == rects[1]
    assert sw.DfScale.geometry().right() < sw.DfScaleUnits.geometry().left()      # no overlap


# ---------------------------------------------------------------------- Scale units: px
class TestScalePixels:
    def test_px_sets_the_detector_units(self, loaded_app, qapp):
        sw = loaded_app.SettingsWindow
        assert not sw.MiscTab.isAncestorOf(sw.DCUnit) and not sw.DCUnit.isVisible()
        assert [sw.DfScaleUnits.itemData(i) for i in range(sw.DfScaleUnits.count())] == ["mrad", "invA", "px"]
        mrad = loaded_app.mradPx.value()
        try:
            sw.DfScaleUnits.setCurrentIndex(sw.DfScaleUnits.findData("px"))
            qapp.processEvents()
            assert sw.DCUnit.currentData() == "px"
            assert not sw.DfScale.isEnabled() and sw.DfScale.value() == 1.0
            assert loaded_app.mradPx.value() == mrad                       # the calibration is kept
            assert loaded_app.AnnRi_NF.suffix().strip() == "px"
            sw.DfScaleUnits.setCurrentIndex(sw.DfScaleUnits.findData("invA"))
            qapp.processEvents()
            assert sw.DCUnit.currentData() == "mrad" and sw.DfScale.isEnabled()
            sw.DCUnit.setCurrentIndex(sw.DCUnit.findData("px"))             # set elsewhere: the dropdown follows
            assert sw.DfScaleUnits.currentData() == "px"
        finally:
            sw.DfScaleUnits.setCurrentIndex(sw.DfScaleUnits.findData("mrad"))
            qapp.processEvents()
        assert sw.DCUnit.currentData() == "mrad" and sw.DfScale.value() == pytest.approx(mrad, abs=1e-4)


# ---------------------------------------------------------------------- histogram padding
def test_histogram_padded_in_alignment(loaded_app, qapp):
    set_mode(loaded_app, qapp, "AlignMod")
    sw = loaded_app.SettingsWindow
    im = loaded_app.Fig[sw.DispImage.currentData()].Image
    lo, hi = sw.HistAxes.axes.get_xlim()
    assert lo < np.nanmin(im) and hi > np.nanmax(im)
    set_mode(loaded_app, qapp, "AnnMod")


# ---------------------------------------------------------------------- cross alignment
class TestCrossAlign:
    def test_two_lines_set_the_beam_at_their_crossing(self, loaded_app, qapp):
        w = loaded_app
        set_mode(w, qapp, "AlignMod")
        b_before = np.array(w.B0, float)
        w.TBCrossAlign.click()
        qapp.processEvents()
        lines = w._crossAlignState["lines"]
        assert w.TBCrossAlign.isChecked() and len(lines) == 2
        assert np.allclose(w.B0, b_before)                       # the lines start crossing at the beam
        # move one end of each line: the beam follows the new crossing
        _drag(w.Fig.Dfrn, lines[0].ends[0], lines[0].ends[0] + [2, 0])
        _drag(w.Fig.Dfrn, lines[1].ends[1], lines[1].ends[1] + [0, 3])
        from annotationsClasses.interactiveLine import intersection
        p = intersection(lines[0].ends, lines[1].ends)
        assert np.allclose(w.B0, p, atol=1e-3)
        assert np.allclose([w.TBX.value(), w.TBY.value()], p, atol=0.01)
        assert np.allclose(w.A.tb.center, p, atol=1e-3)
        # dragging the line itself moves it whole (slope kept)
        mid = lines[0].ends.mean(axis=0)
        slope = np.diff(lines[0].ends, axis=0)
        _drag(w.Fig.Dfrn, mid, mid + [1, -1])
        assert np.allclose(np.diff(lines[0].ends, axis=0), slope)
        w.TBCrossAlign.click()                                    # finish
        qapp.processEvents()
        assert w._crossAlignState is None and not w.TBCrossAlign.isChecked()
        assert all(line.line.axes is None for line in lines)

    def test_leaving_alignment_removes_the_lines(self, loaded_app, qapp):
        w = loaded_app
        set_mode(w, qapp, "AlignMod")
        w.TBCrossAlign.click()
        lines = w._crossAlignState["lines"]
        set_mode(w, qapp, "AnnMod")
        assert w._crossAlignState is None and not w.TBCrossAlign.isChecked()
        assert all(line.line.axes is None for line in lines)

    def test_intersection(self):
        from annotationsClasses.interactiveLine import intersection
        assert np.allclose(intersection(np.array([[0, 0], [2, 2]]), np.array([[0, 2], [2, 0]])), [1, 1])
        assert intersection(np.array([[0, 0], [1, 0]]), np.array([[0, 1], [1, 1]])) is None


# ---------------------------------------------------------------------- custom detectors
@pytest.fixture()
def cust(loaded_app, qapp):
    set_mode(loaded_app, qapp, "CustMod")
    yield loaded_app
    while loaded_app.A.Custom:
        loaded_app.CDT.selectRow(0)
        loaded_app.CDDelMask.click()
        qapp.processEvents()
    set_mode(loaded_app, qapp, "AnnMod")


def _new(app, qapp, button):
    getattr(app, button).click()
    qapp.processEvents()
    return list(app.A.Custom.values())[-1]


def test_polygon_outline_moves_with_the_drag(cust, qapp):
    from annotationsClasses.interactivePolygon import InteractivePolygon
    fig = cust.Fig.Dfrn
    poly = InteractivePolygon(fig.ax, [[10, 10], [20, 10], [15, 20]], color="r")
    outline, = fig.ax.plot([10, 20], [10, 10], ":")
    poly.companions = lambda: [outline]
    poly.connect()
    try:
        _drag(fig, (15, 13), (16, 14), release=False)
        assert poly.dragging and outline.get_animated()     # not baked into the drag's background
        fig.canvas.callbacks.process("button_release_event", MouseEvent("button_release_event", fig.canvas, 0, 0,
                                                                         button=1))
        assert not outline.get_animated()
    finally:
        poly.remove()
        outline.remove()


class TestCentreAxis:
    def test_button(self, cust, qapp):
        assert cust.CDAxis.isCheckable() and cust.CDAxis.toolTip() and cust.CDAxis.isVisible()
        assert cust.CDAxis.geometry().bottom() <= cust.CDMirror.geometry().top()     # just above Mirror
        cmask = _new(cust, qapp, "CDNewCircle")
        assert cust.CDAxis.isEnabled() and not cust.CDAxis.isChecked() and cmask.axis is None

    @pytest.mark.parametrize("button", ["CDNewWedge", "CDNewGrid"])
    def test_free_axis_moves_grid_and_wedge(self, cust, qapp, button):
        cmask = _new(cust, qapp, button)
        before = (np.array(cmask.p1), np.array(cmask.p2), cmask.mask.copy())
        n = len(cmask.handles)
        cust.CDAxis.click()
        qapp.processEvents()
        assert cmask.axisFree and len(cmask.handles) == n + 1
        handle = cmask.handles[-1]
        assert np.allclose(handle.point.get_offsets()[0], cust.B0)
        _drag(cust.Fig.Dfrn, cust.B0, np.asarray(cust.B0) + [3, 2])
        assert np.allclose(cmask.axis, np.asarray(cust.B0) + [3, 2])
        assert np.allclose(cmask.p1, before[0] + [3, 2]) and np.allclose(cmask.p2, before[1] + [3, 2])
        if button == "CDNewWedge":                                 # (the grid fills this small pattern)
            assert not np.array_equal(cmask.mask, before[2])
        cust.CDAxis.click()                                        # lock: the point goes, the axis stays
        qapp.processEvents()
        assert not cmask.axisFree and len(cmask.handles) == n
        assert np.allclose(cmask.axis, np.asarray(cust.B0) + [3, 2])

    def test_circle_keeps_its_place_and_mirrors_about_the_axis(self, cust, qapp):
        cmask = _new(cust, qapp, "CDNewCircle")
        cmask.p1 = np.asarray(cust.B0, float) + [4, 0]
        cust.CDMirror.click()
        cust.CDAxis.click()
        qapp.processEvents()
        p1 = np.array(cmask.p1)
        _drag(cust.Fig.Dfrn, cust.B0, np.asarray(cust.B0) + [1, 1])
        assert np.allclose(cmask.p1, p1)
        mirror = 2 * (np.asarray(cust.B0) + [1, 1]) - p1
        ring = cmask.artists[0].get_xydata()
        assert np.allclose(ring.mean(axis=0), mirror, atol=0.5)

    def test_bandpass_centred_on_its_axis(self, cust, qapp):
        cmask = _new(cust, qapp, "CDNewBandpass")
        assert cmask.handles[0].interactions == "resize"           # no longer dragged around itself
        cust.CDAxis.click()
        qapp.processEvents()
        _drag(cust.Fig.Dfrn, cmask.p1, np.asarray(cmask.p1) + [2, -1])
        assert np.allclose(cmask.p1, np.asarray(cust.B0) + [2, -1])
        assert np.allclose(cmask.handles[0].center, cmask.p1)

    @pytest.mark.parametrize("button", ["CDNewWedge", "CDNewBandpass", "CDNewCircle"])
    def test_right_click_resets_to_the_beam(self, cust, qapp, monkeypatch, button):
        from PyQt5 import QtWidgets as qtw
        monkeypatch.setattr(qtw.QMenu, "popup", lambda *a, **k: None)
        cmask = _new(cust, qapp, button)
        before = (np.array(cmask.p1), None if cmask.p2 is None else np.array(cmask.p2))
        cust.CDAxis.click()
        qapp.processEvents()
        start = np.array(cmask.p1) if button == "CDNewBandpass" else np.asarray(cust.B0, float)
        _drag(cust.Fig.Dfrn, start, start + [3, -2])
        canvas = cust.Fig.Dfrn.canvas
        xy = cust.Fig.Dfrn.ax.transData.transform(start + [3, -2])
        canvas.callbacks.process("button_press_event", MouseEvent("button_press_event", canvas, *xy, button=3))
        menu = cust._axisMenu
        reset = [a for a in menu.actions() if a.text() == "Reset to beam centre"][0]
        assert reset.isEnabled()
        reset.trigger()
        qapp.processEvents()
        assert np.allclose(cmask.p1, before[0])                        # back where it started
        if before[1] is not None:
            assert np.allclose(cmask.p2, before[1])
        if button != "CDNewBandpass":
            assert cmask.axis is None                                  # follows the beam again
        assert cmask.axisFree and np.allclose(cmask.handles[-1].point.get_offsets()[0], cust.B0)
        assert not axisMenuEnabled(cust, cmask)

    def test_not_for_polygons_and_selection_follows(self, cust, qapp):
        wedge = _new(cust, qapp, "CDNewWedge")
        cust.CDAxis.click()
        qapp.processEvents()
        cust.CDT.selectRow(0)
        qapp.processEvents()
        assert cust.CDAxis.isChecked() == wedge.axisFree
        mask = _new(cust, qapp, "CDNewMath")
        assert not cust.CDAxis.isEnabled() and not mask.axisFree


def axisMenuEnabled(app, cmask):
    from callbacks.customDetectorCallbacks import axisMenu
    menu = axisMenu(app, cmask)                 # (kept: its actions go with it)
    return menu.actions()[0].isEnabled()
