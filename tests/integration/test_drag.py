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
    _drag(qapp, roi, next(s for s in ("updateRect", "updateCircle", "positionChanged") if hasattr(roi, s)))
    loaded_app.RealROIShape.setCurrentIndex(loaded_app.RealROIShape.findData("full"))
    qapp.processEvents()
