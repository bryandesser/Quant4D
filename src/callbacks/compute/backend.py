"""CPU/GPU dispatch for the one operation every detector reduces to.

Annular integration, virtual apertures, centre-of-mass and segmented DPC are
all weighted sums over the diffraction pixels of every frame, i.e. a single
matrix product ``data @ weights``.  :func:`project` performs that product on
the CPU (BLAS) or on a CUDA device, in bounded-size chunks where a temporary
copy of the data would otherwise be needed.
"""
from __future__ import annotations

from typing import Any, Optional

import numpy as np

try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:  # torch is an optional dependency (pip install pyquant4d[gpu])
    torch = None  # type: ignore[assignment]
    _TORCH_AVAILABLE = False

__all__ = ["resolve_device", "project"]

#: Upper bound on the size of any temporary copy of the data, in bytes.
CHUNK_BYTES = 256 * 1024 ** 2


def resolve_device(device: Any) -> Optional[Any]:
    """Return a ``torch.device`` for *device*, or ``None`` to run on the CPU.

    ``None`` is returned when *device* is ``None``, when torch is not
    installed, or when CUDA is not available, so callers can pass the user's
    GPU setting straight through.
    """
    if device is None or not _TORCH_AVAILABLE or not torch.cuda.is_available():
        return None
    return torch.device(device)


def _frames_per_chunk(n_pixels: int, itemsize: int) -> int:
    return max(1, CHUNK_BYTES // max(1, n_pixels * itemsize))


def project(data: np.ndarray, weights: np.ndarray, device: Any = None) -> np.ndarray:
    """Weighted sums over the diffraction pixels of every frame: ``data @ weights``.

    Parameters
    ----------
    data : np.ndarray, shape (n_frames, n_pixels)
        The dataset; may be a ``np.memmap`` and may have an integer dtype.
    weights : np.ndarray, shape (n_pixels,) or (n_pixels, m)
        One weight per pixel, or *m* weight vectors as columns.
    device :
        CUDA device, or ``None`` for CPU (see :func:`resolve_device`).

    Returns
    -------
    np.ndarray, shape (n_frames,) or (n_frames, m)
        Floating point: ``float32`` for data of up to 32 bits per value on the
        GPU and for ``float32``/small-integer data on the CPU, ``float64``
        otherwise.  Integer data is never summed in its own dtype, so the
        result cannot overflow.
    """
    weights = np.asarray(weights)
    if data.ndim != 2 or weights.shape[0] != data.shape[1]:
        raise ValueError(
            f"weights of shape {weights.shape} do not match data of shape {data.shape}; "
            "expected weights.shape[0] == data.shape[1]"
        )

    dev = resolve_device(device)
    if dev is not None:
        return _project_gpu(data, weights, dev)

    out_dtype = np.result_type(data.dtype, np.float32)
    w = np.ascontiguousarray(weights, dtype=out_dtype)
    if data.dtype == out_dtype:
        return np.asarray(data @ w)         # straight into BLAS, no copy of the data

    # Integer (or otherwise mismatched) data: convert a bounded block at a time
    # rather than letting NumPy make a floating-point copy of the whole dataset.
    out = np.empty((data.shape[0],) + w.shape[1:], dtype=out_dtype)
    step = _frames_per_chunk(data.shape[1], out_dtype.itemsize)
    for start in range(0, data.shape[0], step):
        block = np.asarray(data[start:start + step], dtype=out_dtype)
        out[start:start + step] = block @ w
    return out


def _project_gpu(data: np.ndarray, weights: np.ndarray, dev: Any) -> np.ndarray:
    w = torch.from_numpy(np.ascontiguousarray(weights, dtype=np.float32)).to(dev)
    out = np.empty((data.shape[0],) + weights.shape[1:], dtype=np.float32)
    step = _frames_per_chunk(data.shape[1], 4)
    for start in range(0, data.shape[0], step):
        block = torch.from_numpy(np.ascontiguousarray(data[start:start + step])).to(dev, dtype=torch.float32)
        out[start:start + step] = (block @ w).cpu().numpy()
        del block
    return out
