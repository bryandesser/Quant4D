"""
Integration tests — Section 4.6 (real-space ROI).

Each ROI shape is selected through ``RealROIShape``; the real-space mask is
checked geometrically and the diffraction pattern shown must be the ROI-
weighted mean of the patterns inside it.
"""
import numpy as np
import pytest
from matplotlib.backend_bases import KeyEvent

import callbacks.realSpaceROICallbacks as rs
from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y


def _select(app, qapp, shape):
    app.RealROIShape.setCurrentIndex(app.RealROIShape.findData(shape))
    qapp.processEvents()
    assert app.RealROIShape.currentData() == shape


def _weighted_mean(app, weights):
    w = np.asarray(weights, float).ravel()
    return (w @ np.asarray(app.Data, float) / w.sum()).reshape(DET_Y, DET_X)


@pytest.fixture()
def roi_app(loaded_app, qapp):
    loaded_app.DetrMode.setCurrentIndex(loaded_app.DetrMode.findData("AnnMod"))
    if loaded_app.RealROIInvert.isChecked():
        loaded_app.RealROIInvert.click()
    _select(loaded_app, qapp, "full")
    yield loaded_app
    if loaded_app.RealROIInvert.isChecked():
        loaded_app.RealROIInvert.click()
    _select(loaded_app, qapp, "full")


class TestFullROI:
    def test_full_is_mean_of_all_frames(self, roi_app):
        assert np.asarray(roi_app.Fig.RealMask.Image, bool).all()
        assert np.allclose(roi_app.Fig.Dfrn.Image, np.asarray(roi_app.Data, float).mean(axis=0).reshape(DET_Y, DET_X),
                           rtol=1e-5)


class TestPointROI:
    @pytest.mark.parametrize("fx, fy", [(3, 2), (0, 0), (SCAN_X - 1, SCAN_Y - 1)])
    def test_single_frame(self, roi_app, qapp, fx, fy):
        _select(roi_app, qapp, "point")
        roi_app.FrameX.setValue(fx)
        roi_app.FrameY.setValue(fy)
        qapp.processEvents()
        assert np.allclose(roi_app.Fig.Dfrn.Image, np.asarray(roi_app.Data)[fy * SCAN_X + fx].reshape(DET_Y, DET_X))


class TestShapeROIs:
    @pytest.mark.parametrize("shape", ["rectangle", "ellipse"])
    def test_mask_and_pattern(self, roi_app, qapp, shape):
        _select(roi_app, qapp, shape)
        mask = np.asarray(roi_app.Fig.RealMask.Image, bool)
        assert mask.shape == (SCAN_Y, SCAN_X)
        assert 0 < mask.sum() < mask.size, f"{shape} ROI selects nothing or everything"
        if shape == "rectangle":
            rows, cols = np.nonzero(mask.any(axis=1))[0], np.nonzero(mask.any(axis=0))[0]
            assert mask[rows.min():rows.max() + 1, cols.min():cols.max() + 1].all(), "rectangle has holes"
        assert np.allclose(roi_app.Fig.Dfrn.Image, _weighted_mean(roi_app, mask), rtol=1e-5)

    def test_invert_flips_mask(self, roi_app, qapp):
        _select(roi_app, qapp, "rectangle")
        mask = np.asarray(roi_app.Fig.RealMask.Image, bool).copy()
        roi_app.RealROIInvert.click()
        qapp.processEvents()
        assert np.array_equal(np.asarray(roi_app.Fig.RealMask.Image, bool), ~mask)
        assert np.allclose(roi_app.Fig.Dfrn.Image, _weighted_mean(roi_app, ~mask), rtol=1e-5)


class TestPolygonROI:
    def _start(self, app, qapp, monkeypatch):
        name = app.G.Img[app.G.Img.id == "Real"].name.item()
        monkeypatch.setattr(rs, "notifDLG", lambda *a, **k: name)    # "draw on which image?"
        _select(app, qapp, "poly")
        assert app.A._tmp_selector is not None

    def test_polygon_drawn(self, roi_app, qapp, monkeypatch):
        from callbacks import compute
        self._start(roi_app, qapp, monkeypatch)
        verts = [(0.2, 0.1), (4.6, 0.4), (1.0, 2.8)]
        roi_app.A._tmp_selector.onselect(verts)
        qapp.processEvents()
        mask = compute.polygon_mask((SCAN_Y, SCAN_X), verts)
        assert np.array_equal(np.asarray(roi_app.Fig.RealMask.Image, bool), mask)
        assert np.allclose(roi_app.Fig.Dfrn.Image, _weighted_mean(roi_app, mask), rtol=1e-5)

    def test_escape_cancels(self, roi_app, qapp, monkeypatch):
        _select(roi_app, qapp, "rectangle")                 # a non-full ROI before drawing
        self._start(roi_app, qapp, monkeypatch)
        canvas = roi_app.Fig.Real.canvas
        canvas.callbacks.process("key_press_event", KeyEvent("key_press_event", canvas, "escape"))
        qapp.processEvents()
        assert roi_app.A._tmp_selector is None
        assert roi_app.RealROIShape.currentData() == "full"
        assert np.asarray(roi_app.Fig.RealMask.Image, bool).all(), "cancelled polygon must leave the full ROI"
        assert np.allclose(roi_app.Fig.Dfrn.Image, _weighted_mean(roi_app, np.ones((SCAN_Y, SCAN_X))), rtol=1e-5)
        assert roi_app.isEnabled(), "windows left disabled after cancelling"
