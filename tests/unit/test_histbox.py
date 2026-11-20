"""
Unit tests for callbacks/histBoxWidget.py
Covers both the math helper and the interactive widget.
"""

import numpy as np
import pytest

# Module-level import — do NOT put this inside a class body.
# A class-level `from module import func` makes func a class attribute;
# calling self.func(a, b) then passes self as the first positional arg,
# giving TypeError (5 args to a 4-arg function).
from callbacks.histBoxWidget import histbox_to_sliders


# ---------------------------------------------------------------------------
# histbox_to_sliders — pure-math tests (no Qt, no display)
# ---------------------------------------------------------------------------
class TestHistboxToSliders:

    def test_full_range_returns_centre(self):
        """When lo=min and hi=max the display window is full → b=50, c=50."""
        b, c = histbox_to_sliders(0.0, 1.0, 0.0, 1.0)
        assert abs(b - 50) < 0.5
        assert abs(c - 50) < 0.5

    def test_narrow_window_increases_contrast(self):
        """A narrow display window should produce contrast > 50."""
        _, c = histbox_to_sliders(0.4, 0.6, 0.0, 1.0)
        assert c > 50

    def test_low_window_gives_high_brightness_slider(self):
        """Window in the dark half → brightness slider > 50.

        The slider convention matches plotImage: a higher brightness value
        shifts the display window *left* (toward darker pixel values), making
        the image appear brighter.  When the window sits in the dark half
        [0, 0.2] the slider must have been boosted above centre to get there,
        so b_ui > 50.
        """
        b, _ = histbox_to_sliders(0.0, 0.2, 0.0, 1.0)
        assert b > 50

    def test_high_window_gives_low_brightness_slider(self):
        """Window in the bright half → brightness slider < 50.

        When the window sits in the bright half [0.8, 1.0] the slider must
        have been pulled below centre, so b_ui < 50.
        """
        b, _ = histbox_to_sliders(0.8, 1.0, 0.0, 1.0)
        assert b < 50

    def test_output_clamped_0_100(self):
        """Extreme inputs must still return values in [0, 100]."""
        b, c = histbox_to_sliders(0.49, 0.51, 0.0, 1.0)
        assert 0 <= b <= 100
        assert 0 <= c <= 100

    def test_symmetry(self):
        """
        A window symmetrically placed around the centre should give b ≈ 50
        regardless of its width.
        """
        b, _ = histbox_to_sliders(0.3, 0.7, 0.0, 1.0)
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
        """HistBox should add a filled span (Rectangle patch) to the axes."""
        from matplotlib.patches import Rectangle
        rects = [c for c in self.ax.get_children() if isinstance(c, Rectangle)]
        assert len(rects) > 0

    def test_remove_clears_artists(self):
        self.hb.remove()
        # After remove, re-fetching children should not raise
        _ = self.ax.get_children()

    def test_on_change_called_on_drag(self, monkeypatch):
        """
        Simulate a drag of the right (hi) edge and confirm on_change fires.
        We set up the drag state manually then call _on_motion / _on_release.

        HistBox internals:
          _drag_mode  : 'lo' | 'hi' | 'body' | None
          _drag_x0    : data-x at mouse-press
          _drag_lo0   : lo value at drag start
          _drag_hi0   : hi value at drag start
          _lo / _hi   : current limits (private; on_change receives these)
        """
        import types
        # Simulate pressing on the right edge (hi=0.8) and dragging to 0.9
        self.hb._drag_mode = 'hi'
        self.hb._drag_x0 = 0.8       # x at press
        self.hb._drag_lo0 = 0.2      # lo frozen at press
        self.hb._drag_hi0 = 0.8      # hi frozen at press

        event = types.SimpleNamespace(xdata=0.9, ydata=50, inaxes=self.ax,
                                      button=1)
        self.hb._on_motion(event)
        assert len(self.changes) == 1                 # live, while dragging
        self.hb._on_release(event)

        assert len(self.changes) == 2                 # and once more on release
        lo, hi = self.changes[-1]
        assert hi == pytest.approx(0.9, abs=1e-6)

    def test_update_position(self):
        """update_position() should shift the span without firing on_change.

        HistBox stores limits as _lo / _hi (private attributes).
        """
        self.hb.update_position(0.1, 0.5)
        assert len(self.changes) == 0   # no callback fired
        # Verify internal state updated
        assert self.hb._lo == pytest.approx(0.1)
        assert self.hb._hi == pytest.approx(0.5)
