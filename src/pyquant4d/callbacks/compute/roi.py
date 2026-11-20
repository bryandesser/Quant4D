"""Diffraction pattern for a real-space region of interest."""
from __future__ import annotations

from typing import Any

import numpy as np

from .backend import project_frames

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
    """``data[i] * w[i]`` for the frames with non-zero weight, a block at a time, in the data's
    float precision (float32 for most data).  A contiguous selection (the full image, a
    rectangle's rows) is read as slices, which are views: no copy of the dataset."""
    selected = np.flatnonzero(w)
    if selected.size == 0:
        return
    dtype = np.result_type(data.dtype, np.float32)
    contiguous = selected[-1] - selected[0] + 1 == selected.size
    for k in range(0, selected.size, rows_per_block):
        if contiguous:
            start = int(selected[0]) + k
            stop = min(start + rows_per_block, int(selected[-1]) + 1)
            block, ww = np.asarray(data[start:stop], dtype=dtype), w[start:stop]
        else:
            idx = selected[k:k + rows_per_block]
            block, ww = np.asarray(data[idx], dtype=dtype), w[idx]
        if not np.all(ww == 1.0):
            block = block * ww.astype(dtype)[:, None]
        yield block


def _max_numpy(data, w, n_pixels):
    out = np.full(n_pixels, -np.inf)
    for block in _selected_blocks(data, w):
        np.maximum(out, block.max(axis=0), out=out)
    return out


def _std_numpy(data, w, n_pixels):
    """Two passes (mean, then squared deviations from it): accurate in float32 blocks, with
    float64 accumulators, and without a float64 copy of the data."""
    n = int(np.count_nonzero(w))
    if n < 2:
        return np.zeros(n_pixels)
    s1 = np.zeros(n_pixels)
    for block in _selected_blocks(data, w):
        s1 += block.sum(axis=0, dtype=np.float64)
    mean = s1 / n
    m2 = np.zeros(n_pixels)
    for block in _selected_blocks(data, w):
        d = block - mean.astype(block.dtype)
        m2 += np.einsum("ij,ij->j", d, d, dtype=np.float64)
    return np.sqrt(m2 / (n - 1))


def _max_std_on_device(data, w, mode, device) -> Any:
    """``max``/``std`` on the device holding the dataset (the GPU), or ``None`` to use NumPy."""
    from . import backend
    dev = backend.resolve_device(device)
    if dev is None:
        return None
    torch = backend.torch
    selected = np.flatnonzero(w)

    def run():
        t = backend._resident.get(data, dev)
        if t is None:
            return None
        sel = torch.from_numpy(selected.astype(np.int64)).to(dev)
        ww = torch.from_numpy(w[selected].astype(np.float32)).to(dev)
        n = int(selected.size)
        step = max(1, backend._frames_per_chunk(data.shape[1], 4))
        blocks = ((k, t.index_select(0, sel[k:k + step]) * ww[k:k + step, None]) for k in range(0, n, step))
        if mode == "max":
            out: Any = None
            for _, b in blocks:
                m = b.amax(dim=0)
                out = m if out is None else torch.maximum(out, m)
            return out.double().cpu().numpy()
        if n < 2:
            return np.zeros(data.shape[1])
        s1 = torch.zeros(data.shape[1], dtype=torch.float64, device=dev)
        for _, b in blocks:
            s1 += b.sum(dim=0, dtype=torch.float64)
        mean = (s1 / n).float()
        m2 = torch.zeros(data.shape[1], dtype=torch.float64, device=dev)
        for k in range(0, n, step):
            d = t.index_select(0, sel[k:k + step]) * ww[k:k + step, None] - mean
            m2 += (d * d).sum(dim=0, dtype=torch.float64)
        return torch.sqrt(m2 / (n - 1)).cpu().numpy()

    return backend._on_device(data, dev, run)


def combine_frames(data: np.ndarray, weights: np.ndarray, mode: str = "sum", device: Any = None) -> np.ndarray:
    """Combine the diffraction patterns of the frames selected by *weights*.

    Modes (MATLAB Quant4D's diffraction dropdown; MATLAB defaults to ``sum``, pyQuant4D to ``mean``):

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

    if mode in ("max", "std"):
        # per pixel over the selected frames: on the device holding the dataset if there is one
        out = _max_std_on_device(data, w, mode, device)
        if out is not None:
            return np.asarray(out, dtype=float)
        return _max_numpy(data, w, n_pixels) if mode == "max" else _std_numpy(data, w, n_pixels)

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
