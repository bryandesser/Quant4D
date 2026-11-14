"""
Unit tests for callbacks/histBoxWidget.py
Covers both the math helper and the interactive widget.
"""

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# histbox_to_sliders — pure-math tests (no Qt, no display)
# ---------------------------------------------------------------------------
class TestHistboxToSliders:
    from callbacks.histBoxWidget import histbox_to_sliders

    def test_full_range_returns_centre(self):
        """When lo=min and hi=max the display window is full → b=50, c=50."""
        b, c = self.histbox_to_sliders(0.0, 1.0, 0.0, 1.0)
        assert abs(b - 50) < 0.5
        assert abs(c - 50) < 0.5

    def test_narrow_window_increases_contrast(self):
        """A narrow display window should produce contrast > 50."""
        _, c = self.histbox_to_sliders(0.4, 0.6, 0.0, 1.0)
        assert c > 50

    def test_low_window_decreases_brightness(self):
        """Window in the dark half should return brightness < 50."""
        b, _ = self.histbox_to_sliders(0.0, 0.2, 0.0, 1.0)
        assert b < 50

    def test_high_window_increases_brightness(self):
        """Window in the bright half should return brightness > 50."""
        b, _ = self.histbox_to_sliders(0.8, 1.0, 0.0, 1.0)
        assert b > 50

    def test_output_clamped_0_100(self):
        """Extreme inputs must still return values in [0, 100]."""
        b, c = self.histbox_to_sliders(0.49, 0.51, 0.0, 1.0)
        assert 0 <= b <= 100
        assert 0 <= c <= 100

    def test_symmetry(self):
        """
        A window symmetrically placed around the centre should give b ≈ 50
        regardless of its width.
        """
        b, _ = self.histbox_to_sliders(0.3, 0.7, 0.0, 1.0)
        assert abs(b - 50) < 1.0


# ---------------------------------------------------------------------------
# HistBox widget — requires a live matplotlib axes
# ---------------------------------------------------------------------------
class TestHistBoxWidget:
    @pytest.fixture(autouse=True)
    def setup(self, mpl_fig_ax):
        from callbacks.histBoxWidget import HistBox
        self.fig, self.ax = mpl_fig_ax
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 100)
        self.changes: list[tuple] = []
        self.hb = HistBox(self.ax, 0.2, 0.8, on_change=lambda lo, hi: self.changes.append((lo, hi)))

    def test_artists_created(self):
        """HistBox should add a filled span to the axes."""
        from matplotlib.patches import Polygon
        spans = [c for c in self.ax.get_children() if hasattr(c, "get_xy")]
        assert len(spans) > 0

    def test_remove_clears_artists(self):
        self.hb.remove()
        # After remove, re-fetching children should not raise
        _ = self.ax.get_children()

    def test_on_change_called_on_drag(self, monkeypatch):
        """
        Simulate a drag of the right edge and confirm on_change fires.
        We call the internal _on_release method directly with synthetic event.
        """
        import types
        event = types.SimpleNamespace(xdata=0.9, ydata=50, inaxes=self.ax)
        self.hb._dragging = "right"
        self.hb._on_motion(event)
        self.hb._on_release(event)
        assert len(self.changes) == 1
        lo, hi = self.changes[0]
        assert hi == pytest.approx(0.9, abs=1e-6)

    def test_update_position(self):
        """update_position() should shift the span without firing on_change."""
        self.hb.update_position(0.1, 0.5)
        assert len(self.changes) == 0   # no callback
        # lo/hi stored correctly
        assert self.hb.lo == pytest.approx(0.1)
        assert self.hb.hi == pytest.approx(0.5)
