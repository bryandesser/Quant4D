"""Scale bars on the image windows.

A :class:`ScaleBar` is a matplotlib artist that works out its length when it
is drawn: the display size of one image pixel (so zooming, window resizing,
rotated or flipped views and saving at another DPI all stay right), a target of
about a fifth of the axes width, rounded down to 1, 2 or 5 x 10^n in a
readable unit.  It sits in the bottom-right corner of the axes, in screen
coordinates, white with a black outline so it shows on any colour map.

* Real space: the scan step of the loaded data (Settings > Windows >
  Real-space); pixels while it is not set.
* Diffraction: mrad once the transmitted beam is set or a file calibrated it,
  and the detector coordinates are in mrad (Settings > Windows > Diffraction); pixels otherwise.

Settings > Windows > Diffraction / Real-space: **Show scale bar** turns them on
and off.
"""
from __future__ import annotations

import math
from typing import Callable, Optional

from matplotlib.artist import Artist
from matplotlib.patches import Rectangle
from matplotlib.patheffects import withStroke
from matplotlib.text import Text
from matplotlib.transforms import IdentityTransform

__all__ = ["ScaleBar", "nice_length", "ensureScaleBar", "refreshScaleBars", "connectScaleBars",
           "realScale", "dfrnScale", "SPACES"]

_METRES = {"pm": 1e-12, "A": 1e-10, "nm": 1e-9, "um": 1e-6, "mm": 1e-3}
_DISPLAY = [("pm", 1e-12), ("nm", 1e-9), ("µm", 1e-6), ("mm", 1e-3)]      # units a bar is labelled in
SPACES = {"Dfrn": "Dfrn", "DfrnMask": "Dfrn", "iCoM": "Real", "dCoM": "Real", "CoMY": "Real", "CoMX": "Real",
          "CoMMag": "Real", "CoMPh": "Real", "CoMPhMag": "Real", "RealMask": "Real", "Real": "Real"}


def _floor125(x: float) -> float:
    """The largest 1, 2 or 5 x 10^n not above *x* (x > 0)."""
    exp = math.floor(math.log10(x))
    base = 10.0 ** exp
    for m in (5, 2, 1):
        if m * base <= x * (1 + 1e-9):
            return m * base
    return base


def nice_length(target: float, units: str) -> tuple[float, str, float]:
    """A round bar length not above *target* (in *units*): ``(number shown, unit shown, length in units)``.

    Lengths (pm, Å, nm, µm, mm) are relabelled in pm, nm, µm or mm so the
    number stays between 1 and 1000; other units (mrad, px) keep theirs.
    """
    if target <= 0 or not math.isfinite(target):
        raise ValueError(f"no scale bar for a target length of {target}")
    if units in _METRES:
        metres = target * _METRES[units]
        unit, size = next(((u, s) for u, s in reversed(_DISPLAY) if metres >= s), _DISPLAY[0])
        shown = _floor125(metres / size)
        return shown, unit, shown * size / _METRES[units]
    shown = _floor125(target)
    return shown, ("px" if units in ("pixels", "px", "") else units), shown


class ScaleBar(Artist):
    """A scale bar drawn in the bottom-right corner of its axes.

    *scale* returns ``(units per image pixel, units)`` (e.g. ``(0.023, "nm")``),
    or None to draw nothing.
    """
    zorder = 10

    def __init__(self, scale: Callable[[], Optional[tuple[float, str]]], fraction: float = 0.2):
        super().__init__()
        self.scale, self.fraction = scale, fraction
        self.label = ""                        # last text drawn (for tests and the status)
        self.length_px = 0.0                   # last length drawn, in display pixels

    def draw(self, renderer):
        self.label, self.length_px = "", 0.0
        ax = self.axes
        if not self.get_visible() or ax is None:
            return
        scale = self.scale()
        if not scale or not scale[0] or scale[0] <= 0:
            return
        per_pixel, units = float(scale[0]), str(scale[1])
        p0, p1 = ax.transData.transform([(0.0, 0.0), (1.0, 0.0)])
        display_per_pixel = math.hypot(*(p1 - p0))          # same for every rotation/flip (square pixels)
        box = ax.bbox
        if display_per_pixel <= 0 or box.width <= 0:
            return
        units_per_display = per_pixel / display_per_pixel
        try:
            shown, unit, length = nice_length(self.fraction * box.width * units_per_display, units)
        except ValueError:
            return
        width = length / units_per_display
        pt = renderer.points_to_pixels(1.0)
        margin, height = 8 * pt, 4 * pt
        x1, y0 = box.x1 - margin, box.y0 + margin
        bar = Rectangle((x1 - width, y0), width, height, transform=IdentityTransform(),
                        facecolor="white", edgecolor="black", linewidth=0.8)
        text = Text((x1 - width / 2), y0 + height + 2 * pt, f"{shown:g} {unit}", transform=IdentityTransform(),
                    ha="center", va="bottom", color="white", fontsize=9, fontweight="bold",
                    path_effects=[withStroke(linewidth=2, foreground="black")])
        for artist in (bar, text):
            artist.set_figure(self.figure)
            artist.set_clip_on(False)
            artist.draw(renderer)
        self.label, self.length_px = text.get_text(), width
        self.stale = False


# ---------------------------------------------------------------------------
# Wiring to the app
# ---------------------------------------------------------------------------
def realScale(self) -> Optional[tuple[float, str]]:
    d = self.D
    if d is None:
        return None
    if d.ScanUnits == "pixels":
        return 1.0, "px"                       # not calibrated: positions of the loaded scan
    return float(d.ScanStep), d.ScanUnits


def dfrnScale(self) -> Optional[tuple[float, str]]:
    d = self.D
    if d is None:
        return None
    calibrated = bool(self.P.TransBeamInit) or (d.Calib is not None and d.Calib.q_units == "mrad")
    if calibrated and self.SettingsWindow.DCUnit.currentData() == "mrad" and self.mradPx.value() > 0:
        return float(self.mradPx.value()), "mrad"
    return 1.0, "px"


def _toggle(self, space: str):
    sw = self.SettingsWindow
    return sw.ScaleBarDfrn if space == "Dfrn" else sw.ScaleBarReal


def ensureScaleBar(self, id: str) -> Optional[ScaleBar]:
    """Give image window *id* its scale bar (again after ``ax.cla()``); None for windows without one."""
    space = SPACES.get(id)
    fig = self.Fig[id]
    if space is None or fig is None:
        return None
    ax = fig.ax
    bar = getattr(fig, "scaleBar", None)
    if bar is None or bar.axes is not ax or bar not in ax.artists:
        bar = ScaleBar((lambda: dfrnScale(self)) if space == "Dfrn" else (lambda: realScale(self)))
        ax.add_artist(bar)
        fig.scaleBar = bar
    bar.set_visible(_toggle(self, space).isChecked())
    return bar


def refreshScaleBars(self, space: Optional[str] = None) -> None:
    """Redraw the scale bars of one space (``"Dfrn"``/``"Real"``) or both, e.g. after a calibration change."""
    for id, sp in SPACES.items():
        if space not in (None, sp):
            continue
        fig = self.Fig[id]
        if fig is None or getattr(fig, "scaleBar", None) is None:
            continue
        ensureScaleBar(self, id)
        fig.canvas.draw_idle()


def connectScaleBars(self) -> None:
    """Connect the Show scale bar boxes and the calibration controls; called once from ``slotsSignals``."""
    sw = self.SettingsWindow
    sw.ScaleBarDfrn.toggled.connect(lambda *_: refreshScaleBars(self, "Dfrn"))
    sw.ScaleBarReal.toggled.connect(lambda *_: refreshScaleBars(self, "Real"))
    sw.DCUnit.currentIndexChanged.connect(lambda *_: refreshScaleBars(self, "Dfrn"))
