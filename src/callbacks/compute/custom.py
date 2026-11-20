"""Custom detector masks (Custom mode), ported from MATLAB Quant4D's
``custom_detector_callbacks``.

Every function returns a diffraction-space mask of shape ``(NPxY, NPxX)``;
points are ``(x, y)`` in 0-based pixel coordinates and ``b0`` is the
transmitted-beam centre.  A pixel belongs to a shape when its centre lies
inside it.  Masks are boolean, except where "Additive" combination counts
overlaps, or a file/maths mask carries grey levels.
"""
from __future__ import annotations

from typing import Any, Iterable, Optional, Sequence

import numpy as np

from callbacks.compute.backend import project
from callbacks.compute.masks import polygon_mask
from callbacks.layout import pixel_grids

__all__ = [
    "INTRA_MODES", "INTER_MODES",
    "combine_parts", "circle_detector", "grid_points", "grid_detector", "bandpass_detector",
    "wedge_detector", "polygon_detector", "invert_mask", "combine_masks", "color_mix",
]

INTRA_MODES = ("Union", "Intersection", "Additive")
INTER_MODES = ("Color Mix", "Union", "Intersection", "Additive", "Current-only")


def combine_parts(parts: Sequence[np.ndarray], mode: str) -> np.ndarray:
    """Combine the components of one mask: logical OR/AND, or (Additive) their sum."""
    parts = [np.asarray(p) for p in parts]
    if mode == "Additive":
        return np.sum([p.astype(float) for p in parts], axis=0)
    if mode == "Intersection":
        return np.logical_and.reduce([p.astype(bool) for p in parts])
    return np.logical_or.reduce([p.astype(bool) for p in parts])


def _disc(shape, center, radius) -> np.ndarray:
    xx, yy = pixel_grids(shape, center)
    return xx ** 2 + yy ** 2 <= float(radius) ** 2


def circle_detector(shape, center, radius, b0, mirrored=False, intra="Union") -> np.ndarray:
    """A circular aperture; *mirrored* adds its copy reflected through *b0*."""
    mask = _disc(shape, center, radius)
    if mirrored:
        mirror = 2 * np.asarray(b0, float) - np.asarray(center, float)
        mask = combine_parts([mask, _disc(shape, mirror, radius)], intra)
    return mask


def grid_points(shape, b0, p1, p2, radius, no_center=False, n_rep: int = 100) -> np.ndarray:
    """Centres of a lattice of apertures, ``b0 + i*(p1-b0) + j*(p2-b0)``.

    With *no_center* ("GridNoCenter") only sites where exactly one of ``i``,
    ``j`` is odd are kept, which removes the transmitted beam and every second
    lattice site (for superlattice reflections).  Sites more than one radius
    outside the pattern are dropped.

    Returns
    -------
    np.ndarray, shape (n, 2) of (x, y)
    """
    ny, nx = int(shape[0]), int(shape[1])
    i, j = np.meshgrid(np.arange(-n_rep, n_rep + 1), np.arange(-n_rep, n_rep + 1), indexing="ij")
    reps = np.column_stack([i.ravel(), j.ravel()])
    if no_center:
        parity = reps % 2
        reps = reps[parity[:, 0] != parity[:, 1]]
    basis = np.array([np.asarray(p1, float) - b0, np.asarray(p2, float) - b0])
    pts = reps @ basis + np.asarray(b0, float)
    pts = np.unique(np.round(pts.astype(np.float32), 4), axis=0).astype(float)   # drop coincident sites
    r = float(radius)
    keep = (pts[:, 0] >= -r - 1) & (pts[:, 1] >= -r - 1) & (pts[:, 0] <= nx + r) & (pts[:, 1] <= ny + r)
    return pts[keep]


def grid_detector(shape, points, radius, intra="Union") -> np.ndarray:
    """Apertures of *radius* at every point; Additive counts overlaps, Intersection keeps them."""
    count = np.zeros((int(shape[0]), int(shape[1])), dtype=np.int32)
    r = float(radius)
    for x, y in np.asarray(points, float).reshape(-1, 2):
        x0, x1 = max(0, int(np.floor(x - r))), min(shape[1], int(np.ceil(x + r)) + 1)
        y0, y1 = max(0, int(np.floor(y - r))), min(shape[0], int(np.ceil(y + r)) + 1)
        if x0 >= x1 or y0 >= y1:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1]
        count[y0:y1, x0:x1] += (xx - x) ** 2 + (yy - y) ** 2 <= r * r
    if intra == "Additive":
        return count.astype(float)
    if intra == "Intersection":
        return count > 1
    return count > 0


def bandpass_detector(shape, center, r1, r2) -> np.ndarray:
    """The ring between two circles about *center* (either radius may be the larger)."""
    lo, hi = sorted((float(r1), float(r2)))
    xx, yy = pixel_grids(shape, center)
    d2 = xx ** 2 + yy ** 2
    return (d2 >= lo * lo) & (d2 <= hi * hi)


def wedge_detector(shape, b0, p1, p2, mirrored=True) -> np.ndarray:
    """A wedge from *b0* to the edges of the pattern, between the directions of *p1* and *p2*.

    The two handles are taken in the order that gives an opening angle below
    180 degrees; *mirrored* adds the opposite wedge.
    """
    d = np.array([np.asarray(p1, float) - b0, np.asarray(p2, float) - b0])
    a = np.sort(np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 360.0)
    if a[1] - a[0] > 180.0:
        a = np.array([a[1], a[0] + 360.0])
    xx, yy = pixel_grids(shape, b0)
    ang = np.degrees(np.arctan2(yy, xx)) % 360.0

    def sector(lo, hi):
        return ((ang - lo) % 360.0) <= (hi - lo)

    mask = sector(a[0], a[1])
    if mirrored:
        mask |= sector(a[0] + 180.0, a[1] + 180.0)
    mask[(xx == 0) & (yy == 0)] = True        # the apex
    return mask


def polygon_detector(shape, vertices) -> np.ndarray:
    """A user-drawn polygon."""
    return polygon_mask(shape, vertices)


def invert_mask(mask: np.ndarray) -> np.ndarray:
    """``max(mask) - mask``: swaps 0 and 1 for a binary mask, flips grey levels otherwise."""
    m = np.asarray(mask, dtype=float)
    return m.max() - m if m.size else m


def combine_masks(masks: Sequence[np.ndarray], weights: Sequence[float], mode: str,
                  ids: Optional[Sequence[str]] = None, current: Optional[str] = None,
                  shape: Optional[tuple] = None) -> np.ndarray:
    """Combine the enabled, non-zero-weight custom masks into the detector.

    Each mask is multiplied by its weight first.  ``Union``/``Intersection``
    give a binary result (OR/AND of the weighted masks), ``Additive`` sums
    them, ``Current-only`` uses the mask whose id is *current*, and
    ``Color Mix`` behaves like Union here (the colours are applied by
    :func:`color_mix`).
    """
    weighted = [np.asarray(m, float) * w for m, w in zip(masks, weights)]
    if not weighted:
        if shape is None:
            raise ValueError("combine_masks needs `shape` when there are no masks")
        return np.zeros(shape, dtype=float)
    out = np.zeros_like(weighted[0])
    for k, m in enumerate(weighted):
        if mode == "Additive":
            out = out + m
        elif mode == "Current-only":
            if ids is not None and ids[k] == current:
                out = m
        elif mode == "Intersection":
            out = m.astype(bool) if k == 0 else (out.astype(bool) & m.astype(bool))
        else:                                   # Union, Color Mix
            out = out.astype(bool) | m.astype(bool)
    return np.asarray(out, dtype=float)


def color_mix(data: np.ndarray, masks: Sequence[np.ndarray], weights: Sequence[float],
              colors: Iterable, device: Any = None) -> tuple[np.ndarray, np.ndarray]:
    """Colour-coded detector: each mask's image is drawn in that mask's colour.

    Returns
    -------
    rgb_mask : np.ndarray, shape (NPxY, NPxX, 3)
        Sum of the weighted masks, each times its RGB colour.
    rgb_real : np.ndarray, shape (n_frames, 3)
        Sum of the masks' images, each times its colour, scaled as a whole to
        ``[0, 1]``.
    """
    shape = np.asarray(masks[0]).shape
    color_masks = np.stack([np.asarray(m, float).ravel() * w for m, w in zip(masks, weights)])   # (k, n_pixels)
    colors = np.asarray(list(colors), float).reshape(-1, 3)                                      # (k, 3)
    rgb_mask = (colors.T @ color_masks).T.reshape(*shape, 3)
    images = project(data, color_masks.T, device)                                                # (n_frames, k)
    rgb_real = np.asarray(images, float) @ colors                                                # (n_frames, 3)
    lo, hi = float(np.nanmin(rgb_real)), float(np.nanmax(rgb_real))
    rgb_real = (rgb_real - lo) / (hi - lo) if hi > lo else np.zeros_like(rgb_real)
    return rgb_mask, rgb_real
