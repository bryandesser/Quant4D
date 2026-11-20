"""Rasterised shapes.

All masks are boolean ``(ny, nx)`` arrays; points and sizes are ``(x, y)`` in
0-based pixel coordinates, pixel ``(x, y)`` being tested at its centre.
"""
from __future__ import annotations

from typing import Iterable

import numpy as np
from matplotlib.path import Path

from ..layout import pixel_grids

__all__ = ["circle_mask", "circles_mask", "ellipse_mask", "rectangle_mask", "polygon_mask"]


def circle_mask(shape: tuple[int, int], center, radius: float) -> np.ndarray:
    """Pixels whose centre lies within *radius* of *center* (boundary included)."""
    xx, yy = pixel_grids(shape, center)
    return xx ** 2 + yy ** 2 <= radius ** 2


def circles_mask(shape: tuple[int, int], centers: Iterable, radius: float) -> np.ndarray:
    """Union of equal-radius circles (e.g. the symmetry copies of a virtual aperture)."""
    mask = np.zeros((int(shape[0]), int(shape[1])), dtype=bool)
    for c in centers:
        mask |= circle_mask(shape, c, radius)
    return mask


def ellipse_mask(shape: tuple[int, int], center, radius, rotation_deg: float = 0.0) -> np.ndarray:
    """Elliptical region of interest.

    *radius* is a scalar (a disc, identical to :func:`circle_mask`) or the semi-axes
    ``(a, b)``: *a* along the ellipse's own x axis, which is rotated by *rotation_deg*
    from the image x axis towards +y (the convention of :func:`rectangle_mask`).
    """
    r = np.asarray(radius, dtype=float).ravel()
    a, b = (float(r[0]), float(r[0])) if r.size == 1 else (float(r[0]), float(r[1]))
    xx, yy = pixel_grids(shape, center)
    if a == b:                                   # a disc: no rotation, exact same test as circle_mask
        return xx ** 2 + yy ** 2 <= a ** 2
    c, s = np.cos(np.radians(rotation_deg)), np.sin(np.radians(rotation_deg))
    local_x = c * xx + s * yy
    local_y = -s * xx + c * yy
    tiny = np.finfo(float).tiny
    return (local_x / max(a, tiny)) ** 2 + (local_y / max(b, tiny)) ** 2 <= 1.0


def rectangle_mask(shape: tuple[int, int], center, size, rotation_deg: float = 0.0) -> np.ndarray:
    """Rectangle of ``size = (width, height)`` centred on *center*, rotated by *rotation_deg*."""
    xx, yy = pixel_grids(shape, center)
    c, s = np.cos(np.radians(rotation_deg)), np.sin(np.radians(rotation_deg))
    local_x = c * xx + s * yy
    local_y = -s * xx + c * yy
    half_w, half_h = float(size[0]) / 2.0, float(size[1]) / 2.0
    return (np.abs(local_x) <= half_w) & (np.abs(local_y) <= half_h)


def polygon_mask(shape: tuple[int, int], vertices) -> np.ndarray:
    """Pixels whose centre lies inside the polygon with the given ``(x, y)`` vertices."""
    ny, nx = int(shape[0]), int(shape[1])
    xx, yy = pixel_grids(shape)
    pts = np.column_stack([xx.ravel(), yy.ravel()])
    vertices = np.asarray(vertices, dtype=float)
    path = Path(np.vstack([vertices, vertices[0]]))
    return path.contains_points(pts).reshape(ny, nx)
