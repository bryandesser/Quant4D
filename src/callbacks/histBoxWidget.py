"""
histBoxWidget.py
================
Provides:
  - HistBox  : a draggable shaded-span widget overlaid on the histogram axes.
               Calls an ``on_change(lo, hi)`` callback whenever the user
               drags either edge or the whole box.
  - histbox_to_sliders : converts absolute intensity limits back to the
               brightness (0–100) and contrast (0–100) slider values used
               by displayCallbacks.
"""

import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.widgets import AxesWidget


# ---------------------------------------------------------------------------
# histbox_to_sliders
# ---------------------------------------------------------------------------

def histbox_to_sliders(lo: float, hi: float,
                       minVal: float, maxVal: float) -> tuple[float, float]:
    """Convert absolute display limits to brightness / contrast slider values.

    Inverts the mapping applied in ``plotImage``::

        brightness = (fig.brightness - 50) / 100            # –0.5 … +0.5
        contrast   = log2(max(eps, fig.contrast / 50)) / 2  # log scale

        limitLow  = minVal – (brightness – contrast) * intensityRange
        limitHigh = maxVal – (brightness + contrast) * intensityRange

    Parameters
    ----------
    lo, hi      : float  – the dragged window limits (same units as the image)
    minVal, maxVal : float – the image's raw min / max (passed to plotImage)

    Returns
    -------
    b_ui : float  – brightness slider value in [0, 100]  (clamped)
    c_ui : float  – contrast  slider value in [0, 100]  (clamped)
    """
    intensity_range = maxVal - minVal
    if intensity_range == 0:
        return 50.0, 50.0

    # brightness: derived from (lo + hi) sum
    # lo + hi = minVal + maxVal – 2*brightness*intensityRange
    brightness = (minVal + maxVal - lo - hi) / (2.0 * intensity_range)
    b_ui = float(np.clip(brightness * 100.0 + 50.0, 0.0, 100.0))

    # contrast: derived from (hi – lo) difference
    # hi – lo = intensityRange – 2*contrast*intensityRange
    # contrast = (1 – (hi – lo)/intensityRange) / 2
    # contrast = log2(c_ui / 50) / 2  →  c_ui = 50 * 2^(2*contrast)
    span = hi - lo
    raw_contrast = (1.0 - span / intensity_range) / 2.0
    c_ui = float(np.clip(50.0 * 2.0 ** (2.0 * raw_contrast), 0.0, 100.0))

    return b_ui, c_ui


# ---------------------------------------------------------------------------
# HistBox
# ---------------------------------------------------------------------------

class HistBox(AxesWidget):
    """Interactive shaded box on a histogram axes for brightness/contrast control.

    The box represents the display window [lo, hi].  The user can:
      * drag the **left edge** to move ``lo``
      * drag the **right edge** to move ``hi``
      * drag the **body** to shift the whole window

    When a drag ends (mouse-button-release) ``on_change(lo, hi)`` is called.

    Parameters
    ----------
    ax        : matplotlib Axes – the histogram axes
    lo, hi    : float – initial low / high display limits (data units)
    on_change : callable(lo, hi) – called when limits change; may be None
    edge_tol  : float – fraction of axes width treated as an edge grab (default 0.03)
    color     : str   – face colour of the shaded region
    alpha     : float – transparency of the shaded region
    """

    def __init__(self, ax, lo: float, hi: float,
                 on_change=None,
                 edge_tol: float = 0.03,
                 color: str = "steelblue",
                 alpha: float = 0.25):
        super().__init__(ax)

        self._lo = float(lo)
        self._hi = float(hi)
        self._on_change = on_change
        self._edge_tol = edge_tol

        # --- shaded rectangle ---
        ylim = ax.get_ylim()
        self._rect = Rectangle(
            (self._lo, ylim[0]),
            width=self._hi - self._lo,
            height=ylim[1] - ylim[0],
            facecolor=color,
            alpha=alpha,
            edgecolor="steelblue",
            linewidth=1.0,
            zorder=3,
        )
        ax.add_patch(self._rect)

        # --- edge markers (thin vertical lines) ---
        self._line_lo, = ax.plot(
            [self._lo, self._lo], ylim,
            color="steelblue", linewidth=1.5, zorder=4
        )
        self._line_hi, = ax.plot(
            [self._hi, self._hi], ylim,
            color="steelblue", linewidth=1.5, zorder=4
        )

        # drag state
        self._drag_mode = None   # 'lo', 'hi', 'body', or None
        self._drag_x0 = None   # data-x at mouse-press
        self._drag_lo0 = None   # lo at drag start
        self._drag_hi0 = None   # hi at drag start

        self.connect_event('button_press_event', self._on_press)
        self.connect_event('button_release_event', self._on_release)
        self.connect_event('motion_notify_event', self._on_motion)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update_position(self, lo: float, hi: float) -> None:
        """Reposition the box without triggering the on_change callback."""
        self._lo = float(lo)
        self._hi = float(hi)
        self._redraw()

    def remove(self) -> None:
        """Remove all artists from the axes."""
        try:
            self._rect.remove()
        except Exception:
            pass
        try:
            self._line_lo.remove()
        except Exception:
            pass
        try:
            self._line_hi.remove()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _redraw(self) -> None:
        ylim = self.ax.get_ylim()
        self._rect.set_x(self._lo)
        self._rect.set_width(self._hi - self._lo)
        self._rect.set_height(ylim[1] - ylim[0])
        self._rect.set_y(ylim[0])
        for line, x in ((self._line_lo, self._lo), (self._line_hi, self._hi)):
            line.set_xdata([x, x])
            line.set_ydata(ylim)
        self.ax.figure.canvas.draw_idle()

    def _axes_x_tol(self) -> float:
        """Edge-grab tolerance in data units."""
        xl = self.ax.get_xlim()
        return self._edge_tol * abs(xl[1] - xl[0])

    def _classify_hit(self, xdata: float) -> str | None:
        """Return 'lo', 'hi', 'body', or None depending on where the click landed."""
        tol = self._axes_x_tol()
        if abs(xdata - self._lo) < tol:
            return 'lo'
        if abs(xdata - self._hi) < tol:
            return 'hi'
        if self._lo < xdata < self._hi:
            return 'body'
        return None

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_press(self, event) -> None:
        if event.inaxes is not self.ax or event.button != 1:
            return
        mode = self._classify_hit(event.xdata)
        if mode is None:
            return
        self._drag_mode = mode
        self._drag_x0 = event.xdata
        self._drag_lo0 = self._lo
        self._drag_hi0 = self._hi

    def _on_motion(self, event) -> None:
        if self._drag_mode is None or event.inaxes is not self.ax:
            return
        dx = event.xdata - self._drag_x0
        xl = self.ax.get_xlim()
        lo_bound, hi_bound = min(xl), max(xl)

        if self._drag_mode == 'lo':
            new_lo = np.clip(self._drag_lo0 + dx, lo_bound, self._hi)
            self._lo = float(new_lo)
        elif self._drag_mode == 'hi':
            new_hi = np.clip(self._drag_hi0 + dx, self._lo, hi_bound)
            self._hi = float(new_hi)
        else:  # 'body'
            span = self._drag_hi0 - self._drag_lo0
            new_lo = np.clip(self._drag_lo0 + dx, lo_bound, hi_bound - span)
            self._lo = float(new_lo)
            self._hi = float(new_lo + span)

        self._redraw()

    def _on_release(self, event) -> None:
        if self._drag_mode is None or event.button != 1:
            return
        self._drag_mode = None
        if callable(self._on_change):
            self._on_change(self._lo, self._hi)
