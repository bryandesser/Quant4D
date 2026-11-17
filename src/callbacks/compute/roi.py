"""Diffraction pattern for a real-space region of interest."""
from __future__ import annotations

import numpy as np

__all__ = ["roi_pattern"]

_EPS = float(np.finfo(np.float32).eps)


def roi_pattern(data: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Weighted-average diffraction pattern over the frames selected by *weights*.

    Parameters
    ----------
    data : np.ndarray, shape (n_frames, n_pixels)
    weights : np.ndarray, shape (NFrY, NFrX) or (n_frames,)
        Weight of each frame; a 0/1 mask gives the mean pattern of the selected
        frames.

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
    return np.asarray(w @ data) / total
