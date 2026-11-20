"""Segmented-detector differential phase contrast (DPC)."""
from __future__ import annotations

from typing import Any

import numpy as np

from .backend import project
from ..layout import pixel_grids

__all__ = ["sector_centroid_radius", "segment_weights", "segmented_dpc"]

_EPS = float(np.finfo(np.float32).eps)


def sector_centroid_radius(r_lo: float, r_hi: float, n_segments: int) -> float:
    """Distance from the detector centre to the centroid of one annular sector.

    The sector spans radii ``r_lo .. r_hi`` and an angle of ``360 / n_segments``
    degrees; its centroid lies on the bisector at

    ``(2/3) * (r_hi**3 - r_lo**3) / (r_hi**2 - r_lo**2) * sin(a/2) / (a/2)``

    with ``a`` the opening angle in radians.  A single segment (a full ring)
    has its centroid at the centre, so the result is 0.
    """
    if r_hi <= r_lo:
        return 0.0
    half = np.pi / n_segments
    radial = (2.0 / 3.0) * (r_hi ** 3 - r_lo ** 3) / (r_hi ** 2 - r_lo ** 2)
    return float(radial * np.sin(half) / half)


def segment_weights(detector_mask: np.ndarray, center, r_inner: float, r_outer: float,
                    n_segments: int, n_rungs: int = 1, rotation_deg: float = 0.0) -> np.ndarray:
    """Per-pixel weights that turn a dataset into DPC sums in one matrix product.

    The detector is an annulus ``r_inner <= r < r_outer`` (pixels, about
    *center*) divided radially into *n_rungs* rings of equal width and
    azimuthally into *n_segments* equal wedges, the first starting at
    *rotation_deg*.  Each of the ``n_rungs * n_segments`` segments reports the
    intensity that falls on it, and that signal is assigned to the segment's
    nominal centre of mass (the geometric centroid of the annular sector, see
    :func:`sector_centroid_radius`).  So every pixel is weighted by the
    centroid position of the segment it belongs to, and the result is a
    coarse-grained centre of mass in pixels: with many small segments it
    converges to :func:`callbacks.compute.center_of_mass`.

    Parameters
    ----------
    detector_mask : np.ndarray of bool, shape (NPxY, NPxX)
        Pixels that may belong to the detector (the annular ring selection);
        intersected with the radial limits above.
    center : (x, y)
    r_inner, r_outer : float
    n_segments, n_rungs : int
    rotation_deg : float

    Returns
    -------
    np.ndarray of float32, shape (n_pixels, 3)
        Columns are the x weight, the y weight (both in pixels) and the
        detector membership (used for normalisation).
    """
    detector_mask = np.asarray(detector_mask, dtype=bool)
    xx, yy = pixel_grids(detector_mask.shape, center)
    x, y = xx.ravel(), yy.ravel()
    radius = np.hypot(x, y)
    angle = np.degrees(np.arctan2(y, x)) % 360.0
    on_detector = detector_mask.ravel() & (radius >= r_inner) & (radius < r_outer)

    width = 360.0 / n_segments
    edges = np.linspace(r_inner, r_outer, n_rungs + 1)
    wx = np.zeros(x.size, dtype=np.float32)
    wy = np.zeros(x.size, dtype=np.float32)
    for r in range(n_rungs):
        in_rung = on_detector & (radius >= edges[r]) & (radius < edges[r + 1])
        r_c = sector_centroid_radius(edges[r], edges[r + 1], n_segments)
        for i in range(n_segments):
            lo = (rotation_deg + i * width) % 360.0
            hi = (lo + width) % 360.0
            if lo < hi:
                in_wedge = (angle >= lo) & (angle < hi)
            else:                               # wedge wraps through 0 degrees
                in_wedge = (angle >= lo) | (angle < hi)
            mid = np.radians((lo + 0.5 * width) % 360.0)
            sel = in_rung & in_wedge
            wx[sel] = r_c * np.cos(mid)
            wy[sel] = r_c * np.sin(mid)
    return np.stack([wx, wy, on_detector.astype(np.float32)], axis=1)


def segmented_dpc(data: np.ndarray, weights: np.ndarray, device: Any = None,
                  ) -> tuple[np.ndarray, np.ndarray]:
    """DPC deflection ``(dpc_x, dpc_y)`` per frame, in pixels.

    The sum over segments of (segment signal x segment centroid), divided by
    the total signal on the detector.

    *weights* comes from :func:`segment_weights`.  Frames with no signal on the
    detector give 0.
    """
    sums = project(data, weights, device)
    norm = np.clip(sums[:, 2], _EPS, None)
    return sums[:, 0] / norm, sums[:, 1] / norm
