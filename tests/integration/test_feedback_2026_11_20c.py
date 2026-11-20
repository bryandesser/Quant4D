"""Bryan's third interactive-testing round of 2026-11-20."""
import numpy as np
import pytest
from matplotlib.backend_bases import MouseEvent
from PyQt5 import QtCore as qtc

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
    assert F.Dfrn.frameGeometry().top() <= top + 5 and F.Real.frameGeometry().top() <= top + 5
    # the others staggered behind the primary image of their column, each one step further out
    from callbacks.window_manager import STAGGER
    for space in ("Dfrn", "Real"):
        corners = [(F[id].x(), F[id].y()) for id in STAGGER[space]]
        assert len(set(corners)) == len(corners), space                             # none hidden exactly
        steps = np.diff(np.array(corners), axis=0)
        assert (np.abs(steps[:, 0]) > 0).all(), space
        assert (steps[:, 1] >= 0).all() and steps[0, 1] > 0, space
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


# ---------------------------------------------------------------------- live histogram drags
def _hist_events(canvas, ax, points, release=False, frac=None, press=True):
    """Press at the first of data *points* (unless *press* is False: a drag going on), move through the
    rest, and release if asked; with *frac*, at that height of the axes instead."""
    def screen(x, y):
        px, py = ax.transData.transform((x, y))
        return (px, ax.transAxes.transform((0, frac))[1]) if frac is not None else (px, py)
    for i, (x, y) in enumerate(points):
        px, py = screen(x, y)
        down = press and i == 0
        kind = "button_press_event" if down else "motion_notify_event"
        canvas.callbacks.process(kind, MouseEvent(kind, canvas, px, py, **({"button": 1} if down else {})))
    if release:
        px, py = screen(*points[-1])
        canvas.callbacks.process("button_release_event",
                                 MouseEvent("button_release_event", canvas, px, py, button=1))


@pytest.mark.parametrize("grab", ["hi", "lo", "body"])
def test_sliders_follow_a_histogram_drag(loaded_app, qapp, grab):
    w, sw = loaded_app, loaded_app.SettingsWindow
    set_mode(w, qapp, "AnnMod")
    sw.DispImage.setCurrentIndex(sw.DispImage.findData("Dfrn"))       # (always has a range of values)
    sw.show()                                  # the histogram at its real size (grab tolerances are in pixels)
    sw.SettingsTabGroup.setCurrentWidget(sw.DisplayTab)
    sw.DispBrightnessReset.click()
    sw.DispContrastReset.click()
    qapp.processEvents()
    canvas, box = sw.HistAxes, w.A.histBox
    canvas.draw()
    ax = canvas.axes
    y, top = 0.0, 0.9                       # near the top of the box: away from the gamma handle
    lo, hi = box._lo, box._hi
    span = hi - lo
    assert ax.transData.transform((hi, 0))[0] - ax.transData.transform((lo, 0))[0] > 100   # wide enough to grab
    start = {"hi": hi, "lo": lo, "body": lo + 0.3 * span}[grab]
    step = {"hi": -0.3, "lo": 0.3, "body": 0.15}[grab] * span
    image_before = w.Fig.Dfrn.contrast, w.Fig.Dfrn.brightness
    try:
        _hist_events(canvas, ax, [(start, y), (start + step, y)], frac=top)    # pressed, moved: not released
        qapp.processEvents()
        assert box._drag_mode == grab                                     # still dragging
        assert (sw.DispBrightness.value(), sw.DispContrast.value()) != (50, 50)
        assert (sw.DispBrightness_NF.value(), sw.DispContrast_NF.value()) == \
            (sw.DispBrightness.value(), sw.DispContrast.value())
        assert (w.Fig.Dfrn.contrast, w.Fig.Dfrn.brightness) != image_before   # the image follows too
        first = sw.DispBrightness.value(), sw.DispContrast.value()
        _hist_events(canvas, ax, [(start + 1.5 * step, y)], release=True, frac=top, press=False)
        qapp.processEvents()
        assert box._drag_mode is None
        assert (sw.DispBrightness.value(), sw.DispContrast.value()) != first or grab == "body"
    finally:
        box._drag_mode = None
        sw.DispBrightnessReset.click()
        sw.DispContrastReset.click()
        qapp.processEvents()


def test_gamma_slider_follows_the_gamma_handle(loaded_app, qapp):
    w, sw = loaded_app, loaded_app.SettingsWindow
    set_mode(w, qapp, "AnnMod")
    sw.DispImage.setCurrentIndex(sw.DispImage.findData("Real"))
    sw.show()
    sw.SettingsTabGroup.setCurrentWidget(sw.DisplayTab)
    sw.DispGammaReset.click()
    qapp.processEvents()
    canvas, box = sw.HistAxes, w.A.histBox
    canvas.draw()
    (hx,), (hy,) = box._handle_gamma.get_data()
    y0, y1 = box._gamma_y
    try:
        _hist_events(canvas, canvas.axes, [(hx, hy), (hx, y0 + 0.25 * (y1 - y0))])   # not released
        qapp.processEvents()
        assert box._drag_mode == "gamma"
        assert sw.DispGamma.value() == pytest.approx(2.0, abs=0.05)
        assert sw.DispGamma_NF.value() == pytest.approx(2.0, abs=0.02)
    finally:
        box._drag_mode = None
        sw.DispGammaReset.click()
        qapp.processEvents()


# ---------------------------------------------------------------------- window size = display area
def test_set_size_is_the_display_area(loaded_app, qapp):
    w, sw = loaded_app, loaded_app.SettingsWindow
    set_mode(w, qapp, "AnnMod")
    sw.DispImage.setCurrentIndex(sw.DispImage.findData("Real"))
    w.Fig.CoMX.hide()
    qapp.processEvents()
    sw.WdwWReal.setValue(150)
    sw.WdwHReal.setValue(120)
    sw.WdwSetReal.click()
    qapp.processEvents()
    canvas = w.Fig.Real.canvas
    assert (canvas.width(), canvas.height()) == (150, 120)          # the image area itself
    assert w.Fig.Real.width() > 150 and w.Fig.Real.height() > 120  # decorations on top
    sw.WdwWReal.setValue(140)
    sw.WdwHReal.setValue(140)
    sw.WdwSetAllReal.click()
    qapp.processEvents()
    for id in ("Real", "RealMask", "CoMX"):                          # hidden ones too
        assert w.Fig[id].imageSize() == qtc.QSize(140, 140), id
    w.Fig.CoMX.show()                                                # and exactly so once shown
    qapp.processEvents()
    assert (w.Fig.CoMX.canvas.width(), w.Fig.CoMX.canvas.height()) == (140, 140)
    w.Fig.CoMX.hide()
    # a display area with the scan's aspect ratio: the image fills it, no black bars
    sw.WdwWReal.setValue(30 * SCAN_X)
    sw.WdwHReal.setValue(30 * SCAN_Y)
    sw.WdwSetReal.click()
    qapp.processEvents()
    w.Fig.Real.canvas.draw()
    bbox = w.Fig.Real.ax.get_window_extent()
    assert (round(bbox.width), round(bbox.height)) == (30 * SCAN_X, 30 * SCAN_Y)
    # resizing a window by hand fills the fields with its display area
    w.Fig.Real.resize(w.Fig.Real.width() + 10, w.Fig.Real.height())
    qapp.processEvents()
    assert (sw.WdwWReal.value(), sw.WdwHReal.value()) == (30 * SCAN_X + 10, 30 * SCAN_Y)


# ---------------------------------------------------------------------- drags over several motions
def _drag_steps(fig, start, end, n=4):
    canvas, ax = fig.canvas, fig.ax
    canvas.draw()
    pts = [ax.transData.transform(np.asarray(start) + (np.asarray(end) - start) * k / n) for k in range(n + 1)]
    canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, *pts[0]))
    canvas.callbacks.process("button_press_event", MouseEvent("button_press_event", canvas, *pts[0], button=1))
    for p in pts[1:]:
        canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, *p))
    canvas.callbacks.process("button_release_event", MouseEvent("button_release_event", canvas, *pts[-1], button=1))


def test_point_follows_the_mouse_over_many_motions(cust, qapp):
    """InteractivePoint kept a view of its offsets as the drag's start, so every motion added its
    move to an already-moved start and the point ran ahead of the mouse."""
    cmask = _new(cust, qapp, "CDNewWedge")
    start = np.array(cmask.p1, float)
    _drag_steps(cust.Fig.Dfrn, start, start + [3, 2])
    assert np.allclose(cmask.p1, start + [3, 2], atol=1e-6)
    assert np.allclose(cmask.handles[0].point.get_offsets()[0], cmask.p1)
    p = cmask.handles[0].position
    p += 5                                                       # a copy: the point does not move
    assert np.allclose(cmask.handles[0].point.get_offsets()[0], cmask.p1)


@pytest.mark.parametrize("button", ["CDNewBandpass", "CDNewGrid", "CDNewWedge"])
def test_axis_drag_leaves_nothing_behind(cust, qapp, button):
    """Moving a mask by its axis over several motions: everything ends where a fresh drawing would put it."""
    from callbacks.customDetectorCallbacks import _axis, _draw
    cmask = _new(cust, qapp, button)
    cust.CDAxis.click()
    qapp.processEvents()
    fig = cust.Fig.Dfrn
    start = _axis(cust, cmask)
    before = [np.array(getattr(cmask, a), float) for a in ("p1", "p2") if getattr(cmask, a) is not None]
    _drag_steps(fig, start, start + [3, 2])
    qapp.processEvents()
    assert np.allclose(_axis(cust, cmask), start + [3, 2], atol=1e-6)
    now = [np.array(getattr(cmask, a), float) for a in ("p1", "p2") if getattr(cmask, a) is not None]
    for b, a in zip(before, now):
        assert np.allclose(a, b + [3, 2], atol=1e-6)
    centres = [h.center for h in cmask.handles if hasattr(h, "center")]   # the apertures followed the axis
    for c, a in zip(centres, now):
        assert np.allclose(c, a, atol=1e-6)
    fig.canvas.draw()
    shown = np.asarray(fig.canvas.buffer_rgba()).copy()
    _draw(cust, cmask)                                            # the same state, drawn afresh
    fig.canvas.draw()
    fresh = np.asarray(fig.canvas.buffer_rgba()).copy()
    assert (np.abs(shown.astype(int) - fresh.astype(int)).sum(-1) > 30).sum() == 0
