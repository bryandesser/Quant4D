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
from matplotlib.backend_tools import Cursors
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

EDGE_PX = 6          # an edge grab is at least this many screen pixels either side of the line


class HistBox(AxesWidget):
    """Interactive shaded box on a histogram axes for brightness/contrast control.

    The box represents the display window [lo, hi].  The user can:
      * drag the **left edge** to move ``lo``
      * drag the **right edge** to move ``hi``
      * drag the **body** to shift the whole window

    Each edge carries a round handle at mid-height, and the cursor shows what a
    drag will do: a horizontal resize arrow over an edge, a move cross over the
    body.  A third handle sits on the gamma curve at the middle of the window
    (where the curve is at 0.5^gamma of the height): dragging it up or down sets
    gamma through ``on_gamma(gamma)`` (vertical resize cursor).

    When a drag ends (mouse-button-release) ``on_change(lo, hi)`` is called.

    Parameters
    ----------
    ax        : matplotlib Axes – the histogram axes
    lo, hi    : float – initial low / high display limits (data units)
    on_change : callable(lo, hi) – called when limits change; may be None
    edge_tol  : float – fraction of axes width treated as an edge grab (default 0.03);
                at least ``EDGE_PX`` screen pixels
    color     : str   – face colour of the shaded region
    alpha     : float – transparency of the shaded region
    """

    def __init__(self, ax, lo: float, hi: float,
                 on_change=None,
                 on_gamma=None,
                 edge_tol: float = 0.03,
                 color: str = "steelblue",
                 alpha: float = 0.25):
        super().__init__(ax)

        self._lo = float(lo)
        self._hi = float(hi)
        self._on_change = on_change
        self._on_gamma = on_gamma
        self._gamma = 1.0
        self._gamma_y = None            # (y0, y1) data limits the gamma curve spans; None: no curve yet
        self.gamma_range = (0.01, 10.0)
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

        # --- round handles at mid-height (axes fraction, so linear and log scales alike) ---
        handle = dict(marker="o", markersize=8, markerfacecolor="white", markeredgecolor="steelblue",
                      markeredgewidth=1.5, linestyle="none", zorder=5, transform=ax.get_xaxis_transform())
        self._handle_lo, = ax.plot([self._lo], [0.5], **handle)
        self._handle_hi, = ax.plot([self._hi], [0.5], **handle)
        # --- gamma handle, on the curve (data coordinates); hidden until set_gamma places it ---
        self._handle_gamma, = ax.plot([], [], marker="o", markersize=8, markerfacecolor="gold",
                                      markeredgecolor="k", markeredgewidth=1.2, linestyle="none", zorder=6)
        self._cursor = None      # the cursor last set (None: the canvas default)

        # drag state
        self._drag_mode = None   # 'lo', 'hi', 'body', or None
        self._drag_x0 = None   # data-x at mouse-press
        self._drag_lo0 = None   # lo at drag start
        self._drag_hi0 = None   # hi at drag start

        self.connect_event('button_press_event', self._on_press)  # pyright: ignore[reportArgumentType] (stub types the event name wrongly)
        self.connect_event('button_release_event', self._on_release)  # pyright: ignore[reportArgumentType] (stub types the event name wrongly)
        self.connect_event('motion_notify_event', self._on_motion)  # pyright: ignore[reportArgumentType] (stub types the event name wrongly)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update_position(self, lo: float, hi: float) -> None:
        """Reposition the box without triggering the on_change callback."""
        self._lo = float(lo)
        self._hi = float(hi)
        self._redraw()

    def remove(self) -> None:
        """Remove all artists from the axes and stop listening to the mouse."""
        try:
            self.disconnect_events()
        except Exception:
            pass
        try:
            self._rect.remove()
        except Exception:
            pass
        try:
            self._line_lo.remove()
        except Exception:
            pass
        for artist in (self._line_hi, self._handle_lo, self._handle_hi, self._handle_gamma):
            try:
                artist.remove()
            except Exception:
                pass
        self._set_cursor(None)

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
        self._handle_lo.set_xdata([self._lo])
        self._handle_hi.set_xdata([self._hi])
        self._place_gamma()
        self.ax.figure.canvas.draw_idle()

    # ------------------------------------------------------------------ gamma
    def set_gamma(self, gamma: float, y0: float, y1: float) -> None:
        """Place the gamma handle for *gamma* on a curve spanning data heights *y0* .. *y1*."""
        self._gamma = float(gamma)
        self._gamma_y = (float(y0), float(y1))
        self._place_gamma()
        self.ax.figure.canvas.draw_idle()

    def _gamma_xy(self):
        if self._gamma_y is None:
            return None
        y0, y1 = self._gamma_y
        return (self._lo + self._hi) / 2.0, y0 + 0.5 ** self._gamma * (y1 - y0)

    def _place_gamma(self) -> None:
        xy = self._gamma_xy()
        self._handle_gamma.set_data(([xy[0]], [xy[1]]) if xy else ([], []))

    def _gamma_hit(self, event) -> bool:
        xy = self._gamma_xy()
        if xy is None or event.x is None or event.y is None:
            return False
        hx, hy = self.ax.transData.transform(xy)
        return abs(event.x - hx) <= 2 * EDGE_PX and abs(event.y - hy) <= 2 * EDGE_PX

    def _gamma_from(self, ydata: float) -> float:
        y0, y1 = self._gamma_y
        frac = float(np.clip((ydata - y0) / (y1 - y0), 1e-6, 1 - 1e-6)) if y1 != y0 else 0.5
        return float(np.clip(np.log(frac) / np.log(0.5), *self.gamma_range))

    def _set_cursor(self, cursor) -> None:
        """Show *cursor* (a matplotlib ``Cursors``) over the histogram, or the default for None."""
        if cursor == self._cursor:
            return
        self._cursor = cursor
        try:
            self.ax.figure.canvas.set_cursor(cursor if cursor is not None else Cursors.POINTER)
        except Exception:        # a canvas without cursor support (e.g. Agg in tests)
            pass

    def cursor_for(self, mode):
        return {"lo": Cursors.RESIZE_HORIZONTAL, "hi": Cursors.RESIZE_HORIZONTAL,
                "body": Cursors.MOVE, "gamma": Cursors.RESIZE_VERTICAL}.get(mode)

    def _axes_x_tol(self) -> float:
        """Edge-grab tolerance in data units: a fraction of the axes, at least EDGE_PX screen pixels."""
        xl = self.ax.get_xlim()
        tol = self._edge_tol * abs(xl[1] - xl[0])
        width_px = self.ax.bbox.width
        if width_px > 0:
            tol = max(tol, EDGE_PX * abs(xl[1] - xl[0]) / width_px)
        return tol

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
        mode = "gamma" if self._gamma_hit(event) else self._classify_hit(event.xdata)
        if mode is None:
            return
        self._drag_mode = mode
        self._drag_x0 = event.xdata
        self._drag_lo0 = self._lo
        self._drag_hi0 = self._hi

    def _on_motion(self, event) -> None:
        if self._drag_mode is None:          # hovering: say what a drag here would do
            mode = None
            if event.inaxes is self.ax:
                mode = "gamma" if self._gamma_hit(event) else self._classify_hit(event.xdata)
            self._set_cursor(self.cursor_for(mode))
            return
        if event.inaxes is not self.ax:
            return
        if self._drag_mode == "gamma":
            if event.ydata is not None and self._gamma_y is not None:
                self._gamma = self._gamma_from(event.ydata)
                self._place_gamma()
                self.ax.figure.canvas.draw_idle()
                if callable(self._on_gamma):
                    self._on_gamma(self._gamma)          # live, like the gamma slider
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
            assert self._drag_hi0 is not None and self._drag_lo0 is not None   # set on press
            span = self._drag_hi0 - self._drag_lo0
            new_lo = np.clip(self._drag_lo0 + dx, lo_bound, hi_bound - span)
            self._lo = float(new_lo)
            self._hi = float(new_lo + span)

        self._redraw()
        if callable(self._on_change):
            self._on_change(self._lo, self._hi)         # live: the sliders and the image follow the drag

    def _on_release(self, event) -> None:
        if self._drag_mode is None or event.button != 1:
            return
        mode, self._drag_mode = self._drag_mode, None
        if mode != "gamma" and callable(self._on_change):
            self._on_change(self._lo, self._hi)         # the final position (Reduced policy waits for it)
