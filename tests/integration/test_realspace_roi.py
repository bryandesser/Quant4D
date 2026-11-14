"""
Integration tests — Section 4.6 (Real-space ROI).

Checks that each ROI type produces the correct diffraction-pattern update
and that mask shapes are geometrically correct.
"""

import numpy as np
import pytest


SCAN_X, SCAN_Y, DET_X, DET_Y = 8, 8, 32, 32


def _select_roi(app, qtbot, roi_name):
    combo = app.RealROIShape
    idx = combo.findText(roi_name)
    assert idx >= 0, f"ROI type {roi_name!r} not in combo"
    combo.setCurrentIndex(idx)
    qtbot.wait(100)


def _dfrn_data(app):
    """Return the data array currently shown on the diffraction axes."""
    imgs = app.Fig.Dfrn.ax.get_images()
    assert imgs
    return imgs[0].get_array()


class TestFullROI:
    def test_full_roi_is_all_frames_sum(self, app, qtbot):
        _select_roi(app, qtbot, "Full")
        expected = app.D.Data.sum(axis=0).reshape(DET_X, DET_Y)
        actual = _dfrn_data(app)
        np.testing.assert_allclose(actual, expected, rtol=1e-4)


class TestPointROI:
    def test_single_frame(self, app, qtbot):
        _select_roi(app, qtbot, "Point")
        fx, fy = 3, 4
        app.FrameX.setValue(fx)
        app.FrameY.setValue(fy)
        qtbot.wait(50)
        idx = fy * SCAN_X + fx
        expected = app.D.Data[idx].reshape(DET_X, DET_Y)
        actual = _dfrn_data(app)
        np.testing.assert_allclose(actual, expected, rtol=1e-4)


class TestRectangleROI:
    def test_mask_is_rectangle(self, app, qtbot):
        _select_roi(app, qtbot, "Rectangle")
        qtbot.wait(100)
        mask = app.D.ROIMask
        assert mask is not None
        assert mask.shape == (SCAN_Y, SCAN_X)
        # Rectangle should be a connected region
        rows = np.where(mask.any(axis=1))[0]
        cols = np.where(mask.any(axis=0))[0]
        # All rows/cols in range should be True (axis-aligned rectangle)
        assert mask[rows.min():rows.max() + 1, cols.min():cols.max() + 1].all()

    def test_invert_roi_flips_mask(self, app, qtbot):
        _select_roi(app, qtbot, "Rectangle")
        qtbot.wait(50)
        orig_mask = app.D.ROIMask.copy()
        qtbot.mouseClick(app.InvertROI,
                         pytest.importorskip("PyQt6.QtCore").Qt.MouseButton.LeftButton)
        qtbot.wait(50)
        np.testing.assert_array_equal(app.D.ROIMask, ~orig_mask)


class TestPolygonROI:
    def test_escape_cancels(self, app, qtbot):
        """Pressing Escape during polygon drawing should cancel without crash."""
        _select_roi(app, qtbot, "Polygon")
        qtbot.wait(50)
        from PyQt6.QtCore import Qt
        qtbot.keyClick(app, Qt.Key.Key_Escape)
        qtbot.wait(50)
        # No unhandled exception = pass
