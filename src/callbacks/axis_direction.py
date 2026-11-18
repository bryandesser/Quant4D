"""Image orientation: reverse X/Y, rotate the view, and the axis-direction arrows.

Ported from MATLAB Quant4D's ``axis_direction_callbacks``.  Each space
(diffraction, real) has its own controls in the Settings window:

* ``RvsXDfrn``/``RvsYDfrn``, ``RvsXReal``/``RvsYReal`` — reverse the axis
  direction (MATLAB ``XDir``/``YDir``).  As in MATLAB, *Reverse Y* on means
  y increases downwards (the usual image orientation, and the default).
* ``RotDfrn``/``RotReal`` — rotate the view by 0, 90, 180 or -90 degrees,
  positive clockwise on screen.
* ``ShowDfrnAxes``/``ShowRealAxes`` — draw small kx/ky (rx/ry) arrows in the
  bottom-left corner of every image of that space, showing where +x and +y
  point.  In CoM and DPC modes the diffraction images also show the scan
  directions (rx/ry) once the scan direction is locked; they are drawn in a
  warning colour until the scan direction has been aligned.

Diffraction settings also apply to the import Preview (a diffraction
pattern), real-space settings to the CoM colour wheel.

Matplotlib cannot rotate an axes view, so each image axes gets a mutable
affine transform inserted between its data limits and the screen
(:func:`install_view_transform`).  Flips and rotation live in that transform,
not in the axis limits, so code that sets limits does not undo them, and
everything drawn in data coordinates (image, annotations, mouse picking)
follows automatically.
"""
from __future__ import annotations

from typing import Any

import numpy as np
from matplotlib.transforms import Affine2D, ScaledTranslation

__all__ = ["install_view_transform", "set_view", "screen_directions", "view_settings",
           "mirrored", "clockwise_angle", "rotate_about", "axisDirectionCallbacks", "ROTATIONS"]

ROTATIONS = (0, 90, 180, -90)
COLOR_X, COLOR_Y, COLOR_WARN = "r", "g", "orange"
_LABELS = {"Dfrn": ("kx", "ky"), "Real": ("rx", "ry")}


# ---------------------------------------------------------------------------
# The view transform (no Qt)
# ---------------------------------------------------------------------------
def install_view_transform(ax) -> Affine2D:
    """Insert the orientation transform into *ax*; idempotent.  Call again after ``ax.cla()``."""
    view = getattr(ax, "_q4d_view", None)
    if view is None:
        view = ax._q4d_view = Affine2D()
        ax._q4d_rot = 0
        ax.callbacks.connect("xlim_changed", _update_aspect)
        ax.callbacks.connect("ylim_changed", _update_aspect)
    if not ax.transData.contains_branch(view):        # new axes, or reset by cla()
        ax.transData = ax.transScale + (ax.transLimits + view + ax.transAxes)
    return view


def set_view(ax, reverse_x: bool = False, reverse_y: bool = True, rotation: float = 0) -> None:
    """Orient *ax*: reverse x and/or y (MATLAB XDir/YDir; y-down is ``reverse_y=True``), then
    rotate the view by *rotation* degrees, clockwise on screen."""
    if rotation not in ROTATIONS:
        raise ValueError(f"rotation must be one of {ROTATIONS}, not {rotation}")
    view = install_view_transform(ax)
    sx = -1 if reverse_x else 1
    sy = 1 if reverse_y else -1          # imshow already puts y downwards
    view.clear().translate(-0.5, -0.5).scale(sx, sy).rotate_deg(-rotation).translate(0.5, 0.5)
    ax._q4d_rot = rotation
    _update_aspect(ax)
    ax.stale = True


def _update_aspect(ax) -> None:
    """Equal data scale on screen: when rotated by ±90° the box takes the transposed shape."""
    if getattr(ax, "_q4d_rot", 0) % 180:
        (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
        xs, ys = abs(x1 - x0), abs(y1 - y0)
        if xs > 0 and ys > 0:
            ax.set_aspect((xs / ys) ** 2, adjustable="box")
    else:
        ax.set_aspect("equal", adjustable="box")


def screen_directions(ax, vectors) -> np.ndarray:
    """Unit screen directions (pixels, y up) of data-space direction *vectors* ``(n, 2)`` on *ax*."""
    vectors = np.atleast_2d(np.asarray(vectors, float))
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    origin = np.array([(x0 + x1) / 2, (y0 + y1) / 2])
    step = 0.01 * max(abs(x1 - x0), abs(y1 - y0), 1.0)
    d = ax.transData.transform(origin + step * vectors) - ax.transData.transform(origin)
    return d / np.maximum(np.linalg.norm(d, axis=1, keepdims=True), 1e-12)


def mirrored(reverse_x: bool, reverse_y: bool) -> bool:
    """True if the view is a mirror image of the default (y down): rotations look reversed."""
    return bool(reverse_x) != (not reverse_y)


def clockwise_angle(self, step: float, clockwise: bool) -> float:
    """Angle in diffraction pixel coordinates (y down) that turns something *clockwise* (or not)
    as currently displayed: a mirrored view reverses the sense, as in MATLAB Quant4D."""
    rx, ry, _ = view_settings(self, "Dfrn")
    angle = step if clockwise else -step
    return -angle if mirrored(rx, ry) else angle


def rotate_about(points, center, angle_deg: float) -> np.ndarray:
    """Rotate (x, y) *points* about *center* by *angle_deg* in pixel coordinates (y down:
    positive is clockwise in the default view)."""
    c, s = np.cos(np.radians(angle_deg)), np.sin(np.radians(angle_deg))
    q = np.asarray(points, float) - np.asarray(center, float)
    return q @ np.array([[c, s], [-s, c]]) + np.asarray(center, float)


# ---------------------------------------------------------------------------
# App glue
# ---------------------------------------------------------------------------
def _controls(self, space):
    sw = self.SettingsWindow
    return (getattr(sw, f"RvsX{space}"), getattr(sw, f"RvsY{space}"),
            getattr(sw, f"Rot{space}"), getattr(sw, f"Show{space}Axes"))


def view_settings(self, space: str) -> tuple[bool, bool, int]:
    """``(reverse_x, reverse_y, rotation)`` chosen for ``"Dfrn"`` or ``"Real"``."""
    rx, ry, rot, _ = _controls(self, space)
    return rx.isChecked(), ry.isChecked(), int(rot.currentData() or 0)


def _ids(self, space):
    """Image windows oriented by *space*'s controls."""
    ids = [i for i, s in zip(self.G.ImgID, self.G.ImgSpace) if s == space]
    return ids + (["Preview"] if space == "Dfrn" else ["ColorWheel"])


def connectAxisDirection(self) -> None:
    """Fill the rotation combos, set MATLAB's defaults and connect; called once from ``slotsSignals``."""
    from callbacks.signals import signals_blocked
    for space in ("Dfrn", "Real"):
        rx, ry, rot, show = _controls(self, space)
        with signals_blocked(rx, ry, rot, show):
            rot.clear()
            for deg in ROTATIONS:
                rot.addItem(f"{deg}°", deg)
            rot.setCurrentIndex(0)
            for button, tip in ((rx, "Reverse the X direction"), (ry, "Reverse the Y direction (on: y increases downwards)"),
                                (show, "Show axis directions on the images")):
                button.setCheckable(True)
                button.setToolTip(tip)
            rx.setChecked(False)
            ry.setChecked(True)             # y downwards, as in MATLAB Quant4D
            show.setChecked(True)
        rot.setToolTip("Rotate the view (clockwise)")
        for button in (rx, ry, show):
            button.clicked.connect(lambda *_: axisDirectionCallbacks(self))
        rot.currentIndexChanged.connect(lambda *_: axisDirectionCallbacks(self))
    for fig in self.Fig.values():
        if fig is not None:
            install_view_transform(fig.ax)


def axisDirectionCallbacks(self, spaces=("Dfrn", "Real")) -> None:
    """Apply both spaces' orientation to their image windows and redraw the direction arrows."""
    for space in spaces:
        rx, ry, rot = view_settings(self, space)
        show = _controls(self, space)[3].isChecked()
        for id in _ids(self, space):
            fig = self.Fig[id]
            if fig is None:
                continue
            set_view(fig.ax, rx, ry, rot)
            _drawArrows(self, fig, space, show)
            fig.canvas.draw_idle()


def _scanArrowsVisible(self) -> bool:
    return (self.SettingsWindow.ShowDfrnAxes.isChecked() and not self.ScanDirUnlock.isChecked()
            and self.DetrMode.currentData() in ("CoMMod", "DPCMod"))


def _drawArrows(self, fig, space, show) -> None:
    """kx/ky (rx/ry) arrows in the corner; on diffraction images also the scan directions."""
    for art in getattr(fig, "axisArrows", []):
        try:
            art.remove()
        except (ValueError, AttributeError, NotImplementedError):
            pass
    fig.axisArrows = []
    if not show:
        return
    ax = fig.ax
    dirs = screen_directions(ax, [(1, 0), (0, 1)])
    fig.axisArrows += _gizmo(ax, dirs, _LABELS[space], (COLOR_X, COLOR_Y), offset=(22, 22), length=4, half=12)
    if space == "Dfrn" and fig.id != "Preview" and _scanArrowsVisible(self):
        sd = np.radians(self.ScanDir.value())
        flip = 1 - 2 * self.ScanDirYFlip.isChecked()
        scan = [(np.cos(sd), np.sin(sd)), (np.cos(sd + flip * np.pi / 2), np.sin(sd + flip * np.pi / 2))]
        colors = (COLOR_X, COLOR_Y) if self.P.ScanDirInit else (COLOR_WARN, COLOR_WARN)
        fig.axisArrows += _gizmo(ax, screen_directions(ax, scan), _LABELS["Real"], colors,
                                 offset=(2.8 * 22, 22), length=1, half=9)


def _gizmo(ax, dirs, labels, colors, offset, length, half) -> list[Any]:
    """Two arrows from a common origin along screen directions *dirs*, MATLAB's layout:
    points ``[origin, x tip, y tip, x label, y label] = [-t -t; l -t; -t l; t -t; -t t]``
    in the frame of the two directions, around *offset* (points from the axes' lower-left)."""
    fig = ax.figure
    corner = Affine2D().scale(1 / 72) + fig.dpi_scale_trans + ScaledTranslation(0, 0, ax.transAxes)
    frame = np.column_stack(dirs[:2])                  # columns: screen dirs of the two axes
    pts = np.array([[-half, -half], [length, -half], [-half, length], [half, -half], [-half, half]], float)
    pts = pts @ frame.T + np.asarray(offset, float)
    arts = []
    for k in range(2):
        tip, lab = pts[1 + k], pts[3 + k]
        arts.append(ax.annotate("", xy=tuple(tip), xycoords=corner, xytext=tuple(pts[0]), textcoords=corner,
                                arrowprops=dict(arrowstyle="-|>", color=colors[k], lw=1, shrinkA=0, shrinkB=0,
                                                mutation_scale=7), annotation_clip=False))
        arts.append(ax.text(lab[0], lab[1], labels[k], transform=corner, color=colors[k], fontweight="bold",
                            fontsize=8, ha="center", va="center", clip_on=False))
    return arts
