"""Small helpers shared by the rotatable annotations (ellipse, rectangle, polygon)."""
from __future__ import annotations

import numpy as np

# Pick radius for handles in screen pixels: independent of the shape's size, the zoom and
# the orientation of the view (reversed axes, rotated view).
HANDLE_PICK_PX = 8.0

# Rectangles and polygons rotate as MATLAB's images.roi shapes do: just outside a corner/vertex
# (beyond HANDLE_PICK_PX, up to this many screen pixels, and outside the shape) the cursor turns
# into a rotation arrow and dragging turns the shape about its centre.
ROTATE_PICK_PX = 22.0


def rotation_matrix(deg: float) -> np.ndarray:
    """Rotation by *deg* from +x towards +y (data coordinates)."""
    c, s = np.cos(np.radians(deg)), np.sin(np.radians(deg))
    return np.array([[c, -s], [s, c]])


def to_local(points, center, deg: float) -> np.ndarray:
    """Data points in the shape's own frame (origin at *center*, axes rotated by *deg*)."""
    return (np.atleast_2d(np.asarray(points, float)) - np.asarray(center, float)) @ rotation_matrix(deg)


def nearest_handle(axis, points, event):
    """``(index, distance in screen pixels)`` of the handle nearest to a mouse *event*."""
    pts = np.atleast_2d(np.asarray(points, float))
    if pts.size == 0 or event.x is None or event.y is None:
        return -1, np.inf
    px = axis.transData.transform(pts)
    d = np.hypot(px[:, 0] - event.x, px[:, 1] - event.y)
    i = int(np.argmin(d))
    return i, float(d[i])


def corner_action(axis, corners, event, inside: bool, rotatable: bool = True) -> tuple[str | None, int]:
    """What a press at *event* does to a shape with these *corners* (vertices):
    ``('corner', i)`` on corner *i*, ``('rotate', i)`` just outside it (and outside the shape),
    otherwise ``(None, -1)``."""
    i, d = nearest_handle(axis, corners, event)
    if d <= HANDLE_PICK_PX:
        return 'corner', i
    if rotatable and d <= ROTATE_PICK_PX and not inside:
        return 'rotate', i
    return None, -1


def turn(center, press, now) -> float:
    """Degrees turned about *center* from the point *press* to the point *now* (data coordinates)."""
    a0 = np.arctan2(press[1] - center[1], press[0] - center[0])
    a1 = np.arctan2(now[1] - center[1], now[0] - center[0])
    return float((np.degrees(a1 - a0) + 180.0) % 360.0 - 180.0)    # in [-180, 180)


# ---------------------------------------------------------------------------- rotation cursor
_rotate_cursor = None


def _make_rotate_cursor():
    """A curved double-headed arrow (Qt has no rotation cursor); None without a Qt GUI application."""
    try:
        from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw
    except ImportError:         # pragma: no cover
        return None
    if not isinstance(qtw.QApplication.instance(), qtw.QApplication):
        return None
    size = 32
    pm = qtg.QPixmap(size, size)
    pm.fill(qtc.Qt.GlobalColor.transparent)
    p = qtg.QPainter(pm)
    p.setRenderHint(qtg.QPainter.RenderHint.Antialiasing)
    cx, cy, r = 16.0, 18.0, 10.0
    start, span = 25.0, 130.0                         # degrees, anticlockwise from +x (screen up is +)

    def point(angle_deg, radius=r):
        a = np.radians(angle_deg)
        return np.array([cx + radius * np.cos(a), cy - radius * np.sin(a)])

    def arrowhead(angle_deg, direction):
        """Head at the arc end *angle_deg*, pointing along the arc (direction +1: anticlockwise)."""
        tip = point(angle_deg + direction * 8.0)
        return qtg.QPolygonF([qtc.QPointF(*tip), qtc.QPointF(*point(angle_deg, r + 4.5)),
                              qtc.QPointF(*point(angle_deg, r - 4.5))])

    for colour, width in ((qtc.Qt.GlobalColor.white, 4.5), (qtc.Qt.GlobalColor.black, 1.8)):
        p.setPen(qtg.QPen(colour, width, qtc.Qt.PenStyle.SolidLine, qtc.Qt.PenCapStyle.RoundCap,
                          qtc.Qt.PenJoinStyle.RoundJoin))
        p.setBrush(qtc.Qt.BrushStyle.NoBrush)
        p.drawArc(qtc.QRectF(cx - r, cy - r, 2 * r, 2 * r), int(start * 16), int(span * 16))
        p.setBrush(colour)
        p.drawPolygon(arrowhead(start, -1.0))
        p.drawPolygon(arrowhead(start + span, 1.0))
    p.end()
    return qtg.QCursor(pm, size // 2, size // 2)


def set_rotate_cursor(canvas) -> None:
    """Show the rotation cursor on a Qt canvas (the hand cursor on other canvases)."""
    global _rotate_cursor
    if hasattr(canvas, "setCursor"):
        if _rotate_cursor is None:
            _rotate_cursor = _make_rotate_cursor()
        if _rotate_cursor is not None:
            canvas.setCursor(_rotate_cursor)
            return
    from matplotlib.backend_tools import Cursors
    canvas.set_cursor(Cursors.HAND)
