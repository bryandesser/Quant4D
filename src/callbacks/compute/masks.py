"""Rasterised shapes.

All masks are boolean ``(ny, nx)`` arrays; points and sizes are ``(x, y)`` in
0-based pixel coordinates, pixel ``(x, y)`` being tested at its centre.
"""
from __future__ import annotations

from typing import Iterable

import numpy as np
from matplotlib.path import Path

from callbacks.layout import pixel_grids

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


def ellipse_mask(shape: tuple[int, int], center, radius: float) -> np.ndarray:
    """Circular region of interest.

    Named for the ROI type it serves; the interactive ROI is a circle, so this
    is :func:`circle_mask` evaluated on distances rather than squared distances.
    """
    xx, yy = pixel_grids(shape, center)
    return np.hypot(xx, yy) <= radius


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
