"""Diffraction pattern for a real-space region of interest."""
from __future__ import annotations

from typing import Any

import numpy as np

from callbacks.compute.backend import project_frames

__all__ = ["roi_pattern", "combine_frames", "COMBINE_MODES"]

#: How the patterns of a real-space region are combined (MATLAB Quant4D's diffraction dropdown).
COMBINE_MODES = ("sum", "mean", "max", "std", "sqrt", "ln", "log10")

_EPS = float(np.finfo(np.float32).eps)


def roi_pattern(data: np.ndarray, weights: np.ndarray, device: Any = None) -> np.ndarray:
    """Weighted-average diffraction pattern over the frames selected by *weights*.

    Parameters
    ----------
    data : np.ndarray, shape (n_frames, n_pixels)
    weights : np.ndarray, shape (NFrY, NFrX) or (n_frames,)
        Weight of each frame; a 0/1 mask gives the mean pattern of the selected
        frames.
    device :
        Torch device, or ``None`` for NumPy.  Only used for large selections.

    Returns
    -------
    np.ndarray, shape (n_pixels,)
        ``weights @ data / weights.sum()``.  All-zero weights give zeros.
    """
    w = np.asarray(weights, dtype=float).ravel()
    if w.shape[0] != data.shape[0]:
        raise ValueError(f"{w.shape[0]} weights for {data.shape[0]} frames")
    total = max(float(w.sum()), _EPS)

    selected = np.flatnonzero(w)
    if selected.size <= data.shape[0] // 4 and np.all(w[selected] == 1.0):
        # A small 0/1 selection (a point or a small shape): read only those
        # frames instead of multiplying through the whole dataset.
        rows = np.asarray(data[selected], dtype=np.result_type(data.dtype, np.float32))
        return rows.sum(axis=0) / total
    return project_frames(data, w, device) / total


def _weighted_sum(data, w, device):
    selected = np.flatnonzero(w)
    if selected.size <= data.shape[0] // 4 and np.all(w[selected] == 1.0):
        rows = np.asarray(data[selected], dtype=np.result_type(data.dtype, np.float32))
        return rows.sum(axis=0)
    return np.asarray(project_frames(data, w, device), dtype=float)


def _selected_blocks(data, w, rows_per_block=256):
    """``data[i] * w[i]`` for the frames with non-zero weight, a block at a time."""
    selected = np.flatnonzero(w)
    for k in range(0, selected.size, rows_per_block):
        idx = selected[k:k + rows_per_block]
        yield np.asarray(data[idx], dtype=np.float64) * w[idx, None]


def combine_frames(data: np.ndarray, weights: np.ndarray, mode: str = "sum", device: Any = None) -> np.ndarray:
    """Combine the diffraction patterns of the frames selected by *weights*.

    Modes (MATLAB Quant4D's diffraction dropdown; default there: ``sum``):

    * ``sum`` — ``weights @ data``;  ``mean`` — that divided by ``weights.sum()``;
    * ``sqrt``, ``ln``, ``log10`` — of the sum (``sqrt`` of negatives is 0; the logarithms are
      of the magnitude and clipped at 0, as MATLAB's ``clip(real(log(x)), 0, Inf)``);
    * ``max``, ``std`` — per pixel over the selected frames, each weighted (``std`` with N-1,
      0 for a single frame).  MATLAB multiplies the whole dataset by the mask, so frames outside
      the region count as zeros there; here only the region's frames are used.

    Returns an array of shape ``(n_pixels,)``.
    """
    w = np.asarray(weights, dtype=float).ravel()
    if w.shape[0] != data.shape[0]:
        raise ValueError(f"{w.shape[0]} weights for {data.shape[0]} frames")
    if mode not in COMBINE_MODES:
        raise ValueError(f"mode must be one of {COMBINE_MODES}, not {mode!r}")
    n_pixels = data.shape[1]
    if not np.any(w):
        return np.zeros(n_pixels)

    if mode == "max":
        out = np.full(n_pixels, -np.inf)
        for block in _selected_blocks(data, w):
            np.maximum(out, block.max(axis=0), out=out)
        return out
    if mode == "std":
        n, s1, s2 = 0, np.zeros(n_pixels), np.zeros(n_pixels)
        for block in _selected_blocks(data, w):
            n += block.shape[0]
            s1 += block.sum(axis=0)
            s2 += np.square(block).sum(axis=0)
        if n < 2:
            return np.zeros(n_pixels)
        return np.sqrt(np.maximum(s2 - s1 * s1 / n, 0) / (n - 1))

    total = _weighted_sum(data, w, device)
    if mode == "mean":
        return total / max(float(w.sum()), _EPS)
    if mode == "sqrt":
        return np.sqrt(np.maximum(total, 0))
    if mode in ("ln", "log10"):
        with np.errstate(divide="ignore"):
            logged = (np.log if mode == "ln" else np.log10)(np.abs(total))
        return np.clip(logged, 0, None)
    return total
