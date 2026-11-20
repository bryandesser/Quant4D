"""
Every draggable annotation survives a drag.  A drag moves the annotation and makes it emit
its signal (updateCircle / positionChanged / updateRect); the handlers then read its geometry.
Dragging the transmitted beam used to raise (its radius is an array).
"""
import numpy as np
import pytest

from conftest import set_mode


def _drag(qapp, ann, signal):
    assert ann is not None, "no annotation drawn"
    if hasattr(ann, "center"):
        ann.center = np.asarray(ann.center, float) + [1.0, 0.5]
    if hasattr(ann, "radius"):
        ann.radius = np.asarray(ann.radius, float) + 0.5
    if hasattr(ann, "semiaxes"):
        ann.semiaxes = np.asarray(ann.semiaxes, float) + 0.5
        ann.rotation = float(ann.rotation) + 20.0
    if hasattr(ann, "vertices"):
        ann.vertices = np.asarray(ann.vertices, float) + [0.5, 0.25]
    getattr(ann, signal).emit()
    qapp.processEvents()


def test_alignment_and_detectors(loaded_app, qapp):
    w = loaded_app
    set_mode(w, qapp, "AlignMod")
    _drag(qapp, w.A.tb, "updateCircle")
    set_mode(w, qapp, "AnnMod")
    w.AnnRi.setValue((1, 6))
    qapp.processEvents()
    _drag(qapp, w.A.adf, "updateCircle")
    set_mode(w, qapp, "DPCMod")
    _drag(qapp, w.A.SegDetrP0, "positionChanged")
    set_mode(w, qapp, "CoMMod")
    if not w.ScanDirUnlock.isChecked():
        w.ScanDirUnlock.click()
        qapp.processEvents()
    _drag(qapp, w.A.ScanDirXcirc, "positionChanged")
    _drag(qapp, w.A.ScanDirYcirc, "positionChanged")
    w.ScanDirUnlock.click()
    qapp.processEvents()
    set_mode(w, qapp, "VrApMod")
    _drag(qapp, w.A.VrAp, "updateCircle")
    w.VrApMirror.click()
    qapp.processEvents()
    _drag(qapp, w.A.VrApMirP, "positionChanged")
    w.VrApMirror.click()
    set_mode(w, qapp, "AnnMod")


@pytest.mark.parametrize("button", ["CDNewCircle", "CDNewGrid", "CDNewBandpass", "CDNewWedge"])
def test_custom_detector_handles(loaded_app, qapp, button):
    set_mode(loaded_app, qapp, "CustMod")
    getattr(loaded_app, button).click()
    qapp.processEvents()
    cmask = list(loaded_app.A.Custom.values())[-1]
    for h in cmask.handles:
        _drag(qapp, h, "updateCircle" if hasattr(h, "updateCircle") else "positionChanged")
    loaded_app.CDDelMask.click()
    set_mode(loaded_app, qapp, "AnnMod")


@pytest.mark.parametrize("shape", ["point", "ellipse", "rectangle"])
def test_real_space_roi(loaded_app, qapp, shape):
    set_mode(loaded_app, qapp, "AnnMod")
    loaded_app.RealROIShape.setCurrentIndex(loaded_app.RealROIShape.findData(shape))
    qapp.processEvents()
    roi = loaded_app.A.RealROI.get("Real")
    _drag(qapp, roi, next(s for s in ("updateRect", "updateEllipse", "updateCircle", "positionChanged") if hasattr(roi, s)))
    loaded_app.RealROIShape.setCurrentIndex(loaded_app.RealROIShape.findData("full"))
    qapp.processEvents()


def _artists(ann):
    arts = list(getattr(ann, "circ", None) or [])
    for name in ("point", "patch", "handles"):
        a = getattr(ann, name, None)
        if a is not None:
            arts.append(a)
    return arts


def _drawn(qapp, fig, ann):
    """True if the annotation changes the rendered pixels of an ordinary (non-blitted) redraw."""
    arts = _artists(ann)
    assert arts and not any(a.get_animated() for a in arts), "animated artists are left out of redraws"
    fig.canvas.draw()
    shown = np.asarray(fig.canvas.buffer_rgba()).copy()
    vis = [a.get_visible() for a in arts]
    for a in arts:
        a.set_visible(False)
    fig.canvas.draw()
    hidden = np.asarray(fig.canvas.buffer_rgba()).copy()
    for a, v in zip(arts, vis):
        a.set_visible(v)
    fig.canvas.draw()
    return not np.array_equal(shown, hidden)


def test_annotations_visible_without_a_click(loaded_app, qapp):
    """Annotations were created 'animated', so a normal redraw skipped them: the transmitted
    beam was invisible after import until it was clicked."""
    w = loaded_app
    set_mode(w, qapp, "AlignMod")
    assert _drawn(qapp, w.Fig.Dfrn, w.A.tb), "transmitted beam not drawn"
    set_mode(w, qapp, "AnnMod")
    w.AnnRi.setValue((1, 6))
    qapp.processEvents()
    assert _drawn(qapp, w.Fig.Dfrn, w.A.adf), "annular detector not drawn"
    set_mode(w, qapp, "VrApMod")
    assert _drawn(qapp, w.Fig.Dfrn, w.A.VrAp), "virtual aperture not drawn"
    set_mode(w, qapp, "AnnMod")
    for shape in ("ellipse", "rectangle", "point"):
        w.RealROIShape.setCurrentIndex(w.RealROIShape.findData(shape))
        qapp.processEvents()
        assert _drawn(qapp, w.Fig.Real, w.A.RealROI["Real"]), f"{shape} ROI not drawn"
    w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("full"))
    qapp.processEvents()


def test_custom_polygon_is_editable_and_rotatable(loaded_app, qapp):
    """The custom-detector polygon: the drawing tool's outline is removed once the polygon is
    closed, and the mask follows its rotation handle."""
    from matplotlib.backend_bases import MouseEvent
    from pyquant4d.callbacks import compute
    from conftest import DET_X, DET_Y, just_outside, turned
    w = loaded_app
    set_mode(w, qapp, "CustMod")
    w.CDNewPolygon.click()
    qapp.processEvents()
    verts = [(4.0, 6.0), (16.0, 6.0), (16.0, 9.0), (4.0, 9.0)]
    selector = w._cdSelector
    selector.onselect(verts)
    qapp.processEvents()
    try:
        cmask = list(w.A.Custom.values())[-1]
        h = cmask.handles[0]
        fig = w.Fig.Dfrn
        assert not [a for a in selector.artists if a in fig.ax.get_children()], "drawing tool's outline left behind"
        canvas = fig.canvas
        canvas.draw()
        centre = h.vertices.mean(axis=0)
        start = just_outside(fig.ax, h.vertices[1], centre)        # just outside a vertex: rotate
        p0, p1 = fig.ax.transData.transform(start), fig.ax.transData.transform(turned(start, centre, 90.0))
        canvas.callbacks.process("button_press_event", MouseEvent("button_press_event", canvas, *p0, button=1))
        canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, *p1))
        canvas.callbacks.process("button_release_event", MouseEvent("button_release_event", canvas, *p1, button=1))
        qapp.processEvents()
        np.testing.assert_allclose(np.ptp(cmask.vertices, axis=0), (3.0, 12.0), atol=1e-9)     # turned a quarter
        np.testing.assert_array_equal(np.asarray(cmask.mask, bool),
                                      compute.polygon_mask((DET_Y, DET_X), cmask.vertices))
    finally:
        w.CDDelMask.click()
        qapp.processEvents()
        set_mode(w, qapp, "AnnMod")
