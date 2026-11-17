"""Annular (bright-field / dark-field) integration."""
from __future__ import annotations

from typing import Any

import numpy as np

from callbacks.compute.backend import project
from callbacks.layout import pixel_grids

__all__ = ["radial_index", "ring_matrix", "ring_integrals", "annular_mask", "masked_sum"]


def radial_index(shape: tuple[int, int], center, ann_width: float) -> np.ndarray:
    """Ring number of every diffraction pixel.

    Parameters
    ----------
    shape : (NPxY, NPxX)
    center : (x, y)
        Transmitted-beam centre in 0-based pixel coordinates.
    ann_width : float
        Width of one ring in pixels.

    Returns
    -------
    np.ndarray of int32, shape (NPxY, NPxX)
        ``floor(distance from center / ann_width)``.
    """
    xx, yy = pixel_grids(shape, center)
    return np.int32(np.sqrt(xx ** 2 + yy ** 2) / ann_width)


def ring_matrix(k: np.ndarray, dtype=np.float32) -> np.ndarray:
    """One-hot ``(n_pixels, n_rings)`` matrix: column *r* selects the pixels of ring *r*."""
    k = np.asarray(k).ravel()
    return (k[:, None] == np.arange(0, k.max() + 1)[None, :]).astype(dtype)


def ring_integrals(data: np.ndarray, k: np.ndarray, device: Any = None) -> np.ndarray:
    """Integrate every ring for every frame.

    Returns
    -------
    np.ndarray, shape (n_frames, n_rings)
        Summing columns ``ri .. ro`` gives the image for an annular detector
        spanning those rings, so the radii can be changed without touching the
        data again.
    """
    return project(data, ring_matrix(k), device)


def annular_mask(k: np.ndarray, ri: int, ro: int) -> np.ndarray:
    """Boolean mask of the pixels in rings ``ri .. ro`` inclusive, same shape as *k*."""
    return (k >= ri) & (k <= ro)


def masked_sum(data: np.ndarray, mask: np.ndarray, device: Any = None) -> np.ndarray:
    """Sum the pixels selected by *mask* for every frame (a virtual detector image).

    Parameters
    ----------
    mask : array-like of bool, shape (NPxY, NPxX) or (n_pixels,)

    Returns
    -------
    np.ndarray, shape (n_frames,)
    """
    return project(data, np.asarray(mask, dtype=bool).ravel(), device)
