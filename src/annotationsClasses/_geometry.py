"""Small helpers shared by the rotatable annotations (ellipse, rectangle, polygon)."""
from __future__ import annotations

import numpy as np

# Pick radius for handles in screen pixels: independent of the shape's size, the zoom and
# the orientation of the view (reversed axes, rotated view).
HANDLE_PICK_PX = 8.0


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
