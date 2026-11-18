"""Custom detector mode: zoom kept while dragging, passive outlines follow a drag, hidden masks
are not interactive, and masks can be duplicated."""
import numpy as np
import pytest
from matplotlib.backend_bases import MouseEvent

from conftest import set_mode


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


def _press_move(fig, start, end):
    canvas = fig.canvas
    canvas.draw()
    p0, p1 = fig.ax.transData.transform(start), fig.ax.transData.transform(end)
    canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, *p0))
    canvas.callbacks.process("button_press_event", MouseEvent("button_press_event", canvas, *p0, button=1))
    canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, *p1))
    return p1


def _release(fig, p1):
    fig.canvas.callbacks.process("button_release_event",
                                 MouseEvent("button_release_event", fig.canvas, *p1, button=1))


def test_zoom_kept_while_dragging(cust, qapp):
    cmask = _new(cust, qapp, "CDNewCircle")
    fig = cust.Fig.Dfrn
    c = np.asarray(cmask.p1, float)
    fig.ax.set_xlim(c[0] - 4, c[0] + 4)
    fig.ax.set_ylim(c[1] + 4, c[1] - 4)
    zoom = (fig.ax.get_xlim(), fig.ax.get_ylim())
    p1 = _press_move(fig, c, c + [1.0, 0.5])
    _release(fig, p1)
    qapp.processEvents()
    assert (fig.ax.get_xlim(), fig.ax.get_ylim()) == zoom, "the drag reset the zoom"


def test_mirrored_copy_drawn_with_the_dragged_aperture(cust, qapp, monkeypatch):
    cmask = _new(cust, qapp, "CDNewCircle")
    cmask.p1 = np.asarray(cmask.p1, float) + [3.0, 0.0]
    cust.CDMirror.click()
    qapp.processEvents()
    assert cmask.mirrored and cmask.artists
    fig = cust.Fig.Dfrn
    drawn = []
    saved = fig.ax.draw_artist
    monkeypatch.setattr(fig.ax, "draw_artist", lambda a: (drawn.append(a), saved(a))[1])
    start = np.asarray(cmask.handles[0].center, float)
    p1 = _press_move(fig, start, start + [1.0, 1.0])
    try:
        assert cmask.handles[0].dragging
        assert any(a in drawn for a in cmask.artists), "mirrored copy not drawn while dragging"
        b0 = np.asarray(cust.B0, float)
        x, y = cmask.artists[0].get_data()
        copy_centre = np.array([np.mean(x), np.mean(y)])
        np.testing.assert_allclose(copy_centre, 2 * b0 - np.asarray(cmask.p1, float), atol=0.2)
    finally:
        _release(fig, p1)
        qapp.processEvents()


def test_disabled_masks_stay_hidden_and_inert(cust, qapp):
    a = _new(cust, qapp, "CDNewCircle")
    row = list(cust.A.Custom).index(a.id)
    cust.CDT.item(row, 3).setCheckState(0)            # untick "enabled"
    qapp.processEvents()
    assert not a.enabled
    h = a.handles[0]
    assert not h.point.get_visible() and not h.circ[0].get_visible()
    _new(cust, qapp, "CDNewGrid")                      # adding another mask, then moving the mouse
    fig = cust.Fig.Dfrn
    p1 = _press_move(fig, np.asarray(a.p1, float), np.asarray(a.p1, float) + [2.0, 0.0])
    _release(fig, p1)
    qapp.processEvents()
    h = a.handles[0]
    assert not h.point.get_visible(), "a disabled mask's handle reappeared"
    assert not h.dragging


def test_duplicate(cust, qapp):
    a = _new(cust, qapp, "CDNewBandpass")
    cust.CDT.selectRow(list(cust.A.Custom).index(a.id))
    qapp.processEvents()
    cust.CDInvert.click()
    cust.CDT.item(list(cust.A.Custom).index(a.id), 5).setText("0.5")       # weight
    qapp.processEvents()
    assert a.inverted and a.weight == 0.5
    cust.CDT.selectRow(list(cust.A.Custom).index(a.id))
    qapp.processEvents()
    assert cust.CDDuplicate.isEnabled()
    cust.CDDuplicate.click()
    qapp.processEvents()
    b = list(cust.A.Custom.values())[-1]
    assert b is not a and b.id != a.id and b.type == a.type
    for name in ("weight", "inverted", "mirrored", "intra", "color", "r1", "r2"):
        assert getattr(b, name) == getattr(a, name), name
    np.testing.assert_array_equal(b.p1, a.p1)
    assert b.p1 is not a.p1, "the copy shares its geometry with the original"
    np.testing.assert_array_equal(b.mask, a.mask)
