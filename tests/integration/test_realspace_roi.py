"""
Integration tests — Section 4.6 (real-space ROI).

Each ROI shape is selected through ``RealROIShape``; the real-space mask is
checked geometrically and the diffraction pattern shown must be the ROI-
weighted mean of the patterns inside it.
"""
import numpy as np
import pytest
from matplotlib.backend_bases import KeyEvent

import pyquant4d.callbacks.realSpaceROICallbacks as rs
from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, just_outside, turned


def _select(app, qapp, shape):
    app.RealROIShape.setCurrentIndex(app.RealROIShape.findData(shape))
    qapp.processEvents()
    assert app.RealROIShape.currentData() == shape


def _weighted_mean(app, weights):
    """The region's pattern with the default combination, the (weighted) mean."""
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


class TestPatternCombination:
    """The "Pattern" dropdown on the diffraction window (MATLAB's diffraction dropdown)."""

    @pytest.mark.parametrize("mode", ["sum", "mean", "max", "std", "sqrt", "ln", "log10"])
    def test_modes(self, roi_app, qapp, mode):
        from pyquant4d.callbacks import compute
        _select(roi_app, qapp, "rectangle")
        mask = np.asarray(roi_app.Fig.RealMask.Image, float)
        roi_app.DfrnCombine.setCurrentIndex(roi_app.DfrnCombine.findData(mode))
        qapp.processEvents()
        try:
            expected = compute.combine_frames(np.asarray(roi_app.Data), mask, mode).reshape(DET_Y, DET_X)
            assert np.allclose(roi_app.Fig.Dfrn.Image, expected, rtol=1e-5)
        finally:
            roi_app.DfrnCombine.setCurrentIndex(roi_app.DfrnCombine.findData("mean"))
            qapp.processEvents()

    def test_default_is_mean_everywhere(self, roi_app, qapp):
        """After import (Align mode) and with the full ROI the pattern is the same mean."""
        assert roi_app.DfrnCombine.currentData() == "mean"
        roi_app.DetrMode.setCurrentIndex(roi_app.DetrMode.findData("AlignMod"))
        qapp.processEvents()
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
        from pyquant4d.callbacks import compute
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


def _click(fig, x, y, button=1):
    from matplotlib.backend_bases import MouseEvent
    canvas = fig.canvas
    px, py = fig.ax.transData.transform((x, y))
    for name in ("motion_notify_event", "button_press_event", "button_release_event"):
        kw = {"button": button} if "button" in name else {}
        canvas.callbacks.process(name, MouseEvent(name, canvas, px, py, **kw))


def _drag_to(fig, start, end):
    from matplotlib.backend_bases import MouseEvent
    canvas = fig.canvas
    canvas.draw()
    p0, p1 = fig.ax.transData.transform(start), fig.ax.transData.transform(end)
    canvas.callbacks.process("button_press_event", MouseEvent("button_press_event", canvas, *p0, button=1))
    canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, *p1))
    canvas.callbacks.process("button_release_event", MouseEvent("button_release_event", canvas, *p1, button=1))


class TestPointStaysVisibleWhileDragged:
    """The point ROI vanished while dragged: it was animated (left out of ordinary redraws) and its
    blitted copy was never put on screen, so only the redraws triggered by the move were shown."""

    def test_point_on_screen_during_drag(self, roi_app, qapp):
        from matplotlib.backend_bases import MouseEvent
        _select(roi_app, qapp, "point")
        roi_app.FrameX.setValue(1)
        roi_app.FrameY.setValue(1)
        qapp.processEvents()
        fig, roi = roi_app.Fig.Real, roi_app.A.RealROI["Real"]
        canvas = fig.canvas
        canvas.draw()
        blits = []
        saved_blit = canvas.blit
        canvas.blit = lambda *a, **k: (blits.append(1), saved_blit(*a, **k))
        try:
            p0, p1 = fig.ax.transData.transform((1, 1)), fig.ax.transData.transform((4, 2))
            canvas.callbacks.process("button_press_event", MouseEvent("button_press_event", canvas, *p0, button=1))
            blits.clear()
            canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, *p1))
            qapp.processEvents()                        # any redraw the move asked for happens now
            assert roi.dragging
            assert blits, "the moved point is never put on screen"
            canvas.draw()                               # a full redraw mid-drag must still show it
            with_point = np.asarray(canvas.buffer_rgba()).copy()
            roi.point.set_visible(False)
            canvas.draw()
            without = np.asarray(canvas.buffer_rgba()).copy()
            roi.point.set_visible(True)
            assert not np.array_equal(with_point, without), "point not drawn while dragged"
            canvas.callbacks.process("button_release_event", MouseEvent("button_release_event", canvas, *p1, button=1))
            qapp.processEvents()
            assert (roi_app.FrameX.value(), roi_app.FrameY.value()) == (4, 2)
        finally:
            canvas.blit = saved_blit


class TestPolygonDrawnWithTheMouse:
    """The PolygonSelector's own outline stayed on the image after the polygon was closed: dragging
    the ROI then left that uneditable copy behind (also after switching back to Full Image)."""

    VERTS = [(0.5, 0.5), (4.5, 0.5), (2.5, 3.0)]

    def _draw(self, app, qapp, monkeypatch):
        def no_dialog(*a, **k):
            raise AssertionError("only one real-space image: no need to ask which")
        monkeypatch.setattr(rs, "notifDLG", no_dialog)
        _select(app, qapp, "poly")
        fig = app.Fig.Real
        fig.canvas.draw()
        for x, y in self.VERTS + [self.VERTS[0]]:
            _click(fig, x, y)
        qapp.processEvents()
        return fig

    def test_closed_polygon_leaves_one_editable_roi(self, roi_app, qapp, monkeypatch):
        from matplotlib.lines import Line2D
        from pyquant4d.callbacks import compute
        fig = self._draw(roi_app, qapp, monkeypatch)
        assert roi_app.A._tmp_selector is None
        roi = roi_app.A.RealROI["Real"]
        np.testing.assert_allclose(roi.vertices, self.VERTS, atol=0.05)
        assert len(roi.handles.get_offsets()) == 3, "vertices must be editable"
        assert not [a for a in fig.ax.lines if isinstance(a, Line2D) and a.get_visible()], \
            "the selector's outline is still on the image"
        _drag_to(fig, self.VERTS[1], (5.0, 2.0))                       # move one vertex
        qapp.processEvents()
        np.testing.assert_allclose(roi.vertices[1], (5.0, 2.0), atol=0.05)
        mask = compute.polygon_mask((SCAN_Y, SCAN_X), roi.vertices)
        assert np.array_equal(np.asarray(roi_app.Fig.RealMask.Image, bool), mask)
        _select(roi_app, qapp, "full")
        assert not [p for p in fig.ax.patches if p.get_visible() and p.get_edgecolor()[3] > 0
                    and p is not getattr(roi_app.A.RealROI["Real"], "patch", None)], "polygon left behind"
        assert not [a for a in fig.ax.lines if a.get_visible()]


class TestRotatableShapes:
    def test_polygon_roi_rotates(self, roi_app, qapp, monkeypatch):
        from pyquant4d.callbacks import compute
        name = roi_app.G.Img[roi_app.G.Img.id == "Real"].name.item()
        monkeypatch.setattr(rs, "notifDLG", lambda *a, **k: name)
        _select(roi_app, qapp, "poly")
        roi_app.A._tmp_selector.onselect([(0.5, 1.5), (4.5, 1.5), (4.5, 2.5), (0.5, 2.5)])
        qapp.processEvents()
        roi = roi_app.A.RealROI["Real"]
        fig = roi_app.Fig.Real
        fig.canvas.draw()
        centre = roi.vertices.mean(axis=0)
        start = just_outside(fig.ax, roi.vertices[1], centre)      # just outside a vertex: rotate
        _drag_to(fig, start, turned(start, centre, -90.0))
        qapp.processEvents()
        assert roi.rotation == pytest.approx(-90.0)
        np.testing.assert_allclose(roi.vertices.mean(axis=0), centre)
        np.testing.assert_allclose(np.ptp(roi.vertices, axis=0), (1.0, 4.0), atol=1e-9)   # long side now along y
        expected = compute.polygon_mask((SCAN_Y, SCAN_X), roi.vertices)
        assert np.array_equal(np.asarray(roi_app.Fig.RealMask.Image, bool), expected)

    def test_ellipse_roi_is_an_ellipse(self, roi_app, qapp):
        from pyquant4d.callbacks import compute
        _select(roi_app, qapp, "ellipse")
        roi = roi_app.A.RealROI["Real"]
        assert roi.semiaxes[0] != roi.semiaxes[1], "should start as an ellipse, not a circle"
        assert len(roi.handles.get_offsets()) == 2
        roi.semiaxes = np.array([2.5, 1.0])
        roi.center = np.array([2.5, 1.5])
        roi.rotation = 90.0
        roi.updateEllipse.emit()
        qapp.processEvents()
        expected = compute.ellipse_mask((SCAN_Y, SCAN_X), (2.5, 1.5), (2.5, 1.0), 90.0)
        assert np.array_equal(np.asarray(roi_app.Fig.RealMask.Image, bool), expected)

    def test_rectangle_roi_rotates(self, roi_app, qapp):
        from pyquant4d.callbacks import compute
        _select(roi_app, qapp, "rectangle")
        roi = roi_app.A.RealROI["Real"]
        roi.center, roi.size = np.array([2.5, 1.5]), np.array([3.0, 1.0])      # corners clear of the image edge
        roi.redraw()
        fig = roi_app.Fig.Real
        fig.canvas.draw()
        start = just_outside(fig.ax, roi.handles.get_offsets()[2], roi.center)
        _drag_to(fig, start, turned(start, roi.center, 90.0))           # a quarter turn
        qapp.processEvents()
        assert roi.rotation % 360 == pytest.approx(90.0)
        expected = compute.rectangle_mask((SCAN_Y, SCAN_X), (2.5, 1.5), (3.0, 1.0), 90.0)
        assert np.array_equal(np.asarray(roi_app.Fig.RealMask.Image, bool), expected)


class TestSwitchingShapes:
    """Switching ROI shape removed the old annotation's artists but left its mouse handlers
    connected: every hover/click then ran the old annotation (errors drawing artists no longer
    in a figure; a ghost rectangle emitting moves into the ellipse ROI)."""

    @staticmethod
    def _mouse_sweep(app, qapp, errors):
        from matplotlib.backend_bases import MouseEvent
        fig = app.Fig.Real
        canvas, ax = fig.canvas, fig.ax
        canvas.draw()
        for x, y in ((1.0, 1.0), (SCAN_X / 2, SCAN_Y / 2), (SCAN_X - 1.5, SCAN_Y - 1.0)):
            px, py = ax.transData.transform((x, y))
            for name in ("motion_notify_event", "button_press_event", "motion_notify_event", "button_release_event"):
                kw = {"button": 1} if "button" in name else {}
                canvas.callbacks.process(name, MouseEvent(name, canvas, px, py, **kw))
        qapp.processEvents()

    @pytest.mark.parametrize("order", [("ellipse", "rectangle"), ("rectangle", "ellipse"),
                                       ("point", "ellipse"), ("point", "rectangle"),
                                       ("ellipse", "point", "rectangle", "ellipse")])
    def test_no_ghost_annotations(self, roi_app, qapp, order):
        canvas = roi_app.Fig.Real.canvas
        errors = []
        saved = canvas.callbacks.exception_handler
        canvas.callbacks.exception_handler = lambda exc: errors.append(repr(exc))
        n_before = len(canvas.callbacks.callbacks.get("motion_notify_event", {}))
        try:
            for shape in order:
                _select(roi_app, qapp, shape)
                self._mouse_sweep(roi_app, qapp, errors)
            assert not errors, errors[:3]
            n_after = len(canvas.callbacks.callbacks.get("motion_notify_event", {}))
            assert n_after <= n_before + 1, f"mouse handlers pile up: {n_before} -> {n_after}"
            mask = np.asarray(roi_app.Fig.RealMask.Image, bool)
            assert 0 < mask.sum() <= mask.size
        finally:
            canvas.callbacks.exception_handler = saved


class TestPointPattern:
    def test_std_unavailable_for_a_point(self, roi_app, qapp):
        combo = roi_app.DfrnCombine
        _select(roi_app, qapp, "rectangle")
        combo.setCurrentIndex(combo.findData("std"))
        qapp.processEvents()
        _select(roi_app, qapp, "point")
        assert combo.currentData() == "mean", "std over one frame is all zeros"
        assert not combo.model().item(combo.findData("std")).isEnabled()
        _select(roi_app, qapp, "rectangle")
        assert combo.model().item(combo.findData("std")).isEnabled()

    def test_flat_image_does_not_divide_by_zero(self, roi_app, qapp):
        """A flat pattern (e.g. std of one frame) made the histogram's gamma curve divide by 0."""
        import warnings
        from pyquant4d.callbacks.plotting import plotImage
        sw = roi_app.SettingsWindow
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Dfrn"))
        qapp.processEvents()
        saved = roi_app.Fig.Dfrn.Image
        roi_app.Fig.Dfrn.Image = np.zeros_like(saved)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", RuntimeWarning)
                plotImage(roi_app, "Dfrn")
        finally:
            roi_app.Fig.Dfrn.Image = saved
            plotImage(roi_app, "Dfrn")
