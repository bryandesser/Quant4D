"""CPU/GPU dispatch for the one operation every detector reduces to.

Annular integration, virtual apertures, centre-of-mass and segmented DPC are
all weighted sums over the diffraction pixels of every frame, i.e. a single
matrix product ``data @ weights``.  :func:`project` performs that product on
the CPU (BLAS) or on a torch device.

GPU strategy
------------
The first GPU call uploads the dataset once, as ``float32``, and keeps it on
the device; every later call only sends the (small) weights and brings back the
(small) result.  If the dataset does not fit in the device's free memory it is
*streamed* instead: uploaded and multiplied a bounded chunk at a time on every
call.  Either way no temporary copy larger than :data:`CHUNK_BYTES` is made on
the host.  If the device runs out of memory part-way, the resident copy is
dropped and the call is retried by streaming, then on the CPU.

The resident copy is keyed on the identity of the NumPy array, so loading a new
dataset replaces it automatically.  Code that modifies the dataset **in place**
(byte swapping, zeroing NaNs) must call :func:`release_device_data` afterwards,
as must code that unloads the dataset.
"""
from __future__ import annotations

import weakref
from typing import Any, Optional

import numpy as np

try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:  # torch is an optional dependency (pip install pyquant4d[gpu])
    torch = None  # type: ignore[assignment]
    _TORCH_AVAILABLE = False

__all__ = ["resolve_device", "project", "project_frames", "release_device_data", "device_data_info"]

#: Upper bound on the size of any temporary copy of the data, in bytes.
CHUNK_BYTES = 256 * 1024 ** 2

#: Fraction of the device's free memory the resident dataset may occupy.  The
#: rest is left for the weights, the products and whatever else uses the GPU.
RESIDENT_FRACTION = 0.8


# ---------------------------------------------------------------------------
# Device selection
# ---------------------------------------------------------------------------
def resolve_device(device: Any) -> Optional[Any]:
    """Return a ``torch.device`` for *device*, or ``None`` to use NumPy.

    ``None`` is returned when *device* is ``None``, when torch is not
    installed, or when a CUDA device is requested but CUDA is not available,
    so callers can pass the user's GPU setting straight through.  Asking for
    ``"cpu"`` explicitly runs the torch code path on the CPU, which is how that
    path is tested on machines without a GPU.
    """
    if device is None or not _TORCH_AVAILABLE:
        return None
    dev = torch.device(device)
    if dev.type == "cuda" and not torch.cuda.is_available():
        return None
    return dev


def _free_bytes(dev: Any) -> int:
    """Memory currently available on *dev*."""
    if dev.type == "cuda":
        return int(torch.cuda.mem_get_info(dev)[0])
    import psutil
    return int(psutil.virtual_memory().available)


def _is_out_of_memory(exc: BaseException) -> bool:
    oom = getattr(torch, "OutOfMemoryError", None) or getattr(torch.cuda, "OutOfMemoryError", ())
    return (bool(oom) and isinstance(exc, oom)) or "out of memory" in str(exc).lower()


def _frames_per_chunk(n_pixels: int, itemsize: int) -> int:
    return max(1, CHUNK_BYTES // max(1, n_pixels * itemsize))


# ---------------------------------------------------------------------------
# The dataset kept on the device
# ---------------------------------------------------------------------------
class _Resident:
    """One dataset held on a device, remembered by the identity of its NumPy array."""

    def __init__(self) -> None:
        self.ref: Optional[weakref.ref] = None
        self.key: Optional[tuple] = None
        self.tensor: Any = None
        self.too_big: Optional[tuple] = None    # (key, weakref) of a dataset known not to fit

    @staticmethod
    def key_for(data: np.ndarray, dev: Any) -> tuple:
        return (id(data), data.shape, data.dtype.str, str(dev))

    def get(self, data: np.ndarray, dev: Any) -> Any:
        """The tensor for *data* on *dev*, uploading it if needed; ``None`` if it cannot be held."""
        key = self.key_for(data, dev)
        if self.tensor is not None and self.key == key and self.ref is not None and self.ref() is data:
            return self.tensor
        if self._known_too_big(data, key):
            return None

        self.release()      # a different dataset or device: free the old copy before measuring
        needed = data.shape[0] * data.shape[1] * 4
        if needed > RESIDENT_FRACTION * _free_bytes(dev):
            self.mark_too_big(data, dev)
            return None
        try:
            tensor = torch.empty(data.shape, dtype=torch.float32, device=dev)
            step = _frames_per_chunk(data.shape[1], 4)
            for start in range(0, data.shape[0], step):
                block = np.ascontiguousarray(data[start:start + step])
                tensor[start:start + step] = torch.from_numpy(block).to(dev, dtype=torch.float32)
        except RuntimeError as exc:
            if not _is_out_of_memory(exc):
                raise
            tensor = None
            self.release()
            self.mark_too_big(data, dev)
            return None
        self.ref, self.key, self.tensor = weakref.ref(data), key, tensor
        return tensor

    def _known_too_big(self, data: np.ndarray, key: tuple) -> bool:
        return self.too_big is not None and self.too_big[0] == key and self.too_big[1]() is data

    def mark_too_big(self, data: np.ndarray, dev: Any) -> None:
        """Remember that *data* does not fit on *dev*, so later calls stream it straight away."""
        self.too_big = (self.key_for(data, dev), weakref.ref(data))

    def release(self) -> None:
        had = self.tensor is not None
        self.ref = self.key = self.tensor = self.too_big = None
        if had and _TORCH_AVAILABLE and torch.cuda.is_available():
            torch.cuda.empty_cache()


_resident = _Resident()


def release_device_data() -> None:
    """Drop the copy of the dataset held on the GPU, if any, and free its memory.

    Call this when the dataset is unloaded and after any in-place change to it;
    the next GPU call uploads the current contents again.  Safe to call at any
    time, with or without torch.
    """
    _resident.release()


def device_data_info() -> Optional[dict]:
    """Describe the dataset currently held on a device, or ``None`` if there is none.

    Returns ``{"device", "shape", "bytes"}``.
    """
    t = _resident.tensor
    if t is None:
        return None
    return {"device": str(t.device), "shape": tuple(t.shape), "bytes": int(t.numel() * t.element_size())}


# ---------------------------------------------------------------------------
# data @ weights  (sums over pixels, one value per frame)
# ---------------------------------------------------------------------------
def project(data: np.ndarray, weights: np.ndarray, device: Any = None) -> np.ndarray:
    """Weighted sums over the diffraction pixels of every frame: ``data @ weights``.

    Parameters
    ----------
    data : np.ndarray, shape (n_frames, n_pixels)
        The dataset; may be a ``np.memmap`` and may have an integer dtype.
    weights : np.ndarray, shape (n_pixels,) or (n_pixels, m)
        One weight per pixel, or *m* weight vectors as columns.
    device :
        Torch device, or ``None`` for NumPy (see :func:`resolve_device`).

    Returns
    -------
    np.ndarray, shape (n_frames,) or (n_frames, m)
        Floating point: ``float32`` on a torch device and for
        ``float32``/small-integer data in NumPy, ``float64`` otherwise.
        Integer data is never summed in its own dtype, so the result cannot
        overflow.
    """
    weights = np.asarray(weights)
    if data.ndim != 2 or weights.shape[0] != data.shape[1]:
        raise ValueError(
            f"weights of shape {weights.shape} do not match data of shape {data.shape}; "
            "expected weights.shape[0] == data.shape[1]"
        )

    dev = resolve_device(device)
    if dev is not None:
        result = _on_device(data, dev, lambda: _project_torch(data, weights, dev))
        if result is not None:
            return result
    return _project_numpy(data, weights)


def _project_numpy(data: np.ndarray, weights: np.ndarray) -> np.ndarray:
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


def _project_torch(data: np.ndarray, weights: np.ndarray, dev: Any) -> np.ndarray:
    w = torch.from_numpy(np.ascontiguousarray(weights, dtype=np.float32)).to(dev)
    resident = _resident.get(data, dev)
    if resident is not None:
        return (resident @ w).cpu().numpy()

    out = np.empty((data.shape[0],) + weights.shape[1:], dtype=np.float32)
    for start, block in _stream(data, dev):
        out[start:start + block.shape[0]] = (block @ w).cpu().numpy()
    return out


# ---------------------------------------------------------------------------
# frame_weights @ data  (sums over frames, one value per pixel)
# ---------------------------------------------------------------------------
def project_frames(data: np.ndarray, frame_weights: np.ndarray, device: Any = None) -> np.ndarray:
    """Weighted sum of frames: ``frame_weights @ data``, shape ``(n_pixels,)``.

    The counterpart of :func:`project` along the other axis; used for the
    diffraction pattern of a real-space region.  Same dtype rules as
    :func:`project`.
    """
    frame_weights = np.asarray(frame_weights).ravel()
    if data.ndim != 2 or frame_weights.shape[0] != data.shape[0]:
        raise ValueError(f"{frame_weights.shape[0]} frame weights for data of shape {data.shape}")

    dev = resolve_device(device)
    if dev is not None:
        result = _on_device(data, dev, lambda: _project_frames_torch(data, frame_weights, dev))
        if result is not None:
            return result
    return _project_frames_numpy(data, frame_weights)


def _project_frames_numpy(data: np.ndarray, frame_weights: np.ndarray) -> np.ndarray:
    out_dtype = np.result_type(data.dtype, np.float32)
    w = np.ascontiguousarray(frame_weights, dtype=out_dtype)
    if data.dtype == out_dtype:
        return np.asarray(w @ data)         # weights in the data's own dtype: no copy of the data

    total = np.zeros(data.shape[1], dtype=out_dtype)
    step = _frames_per_chunk(data.shape[1], out_dtype.itemsize)
    for start in range(0, data.shape[0], step):
        block = np.asarray(data[start:start + step], dtype=out_dtype)
        total += w[start:start + step] @ block
    return total


def _project_frames_torch(data: np.ndarray, frame_weights: np.ndarray, dev: Any) -> np.ndarray:
    w = torch.from_numpy(np.ascontiguousarray(frame_weights, dtype=np.float32)).to(dev)
    resident = _resident.get(data, dev)
    if resident is not None:
        return (w @ resident).cpu().numpy()

    total = torch.zeros(data.shape[1], dtype=torch.float32, device=dev)
    for start, block in _stream(data, dev):
        total += w[start:start + block.shape[0]] @ block
    return total.cpu().numpy()


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def _stream(data: np.ndarray, dev: Any):
    """Yield ``(start, float32 tensor on dev)`` for consecutive blocks of frames."""
    step = _frames_per_chunk(data.shape[1], 4)
    for start in range(0, data.shape[0], step):
        block = np.ascontiguousarray(data[start:start + step])
        yield start, torch.from_numpy(block).to(dev, dtype=torch.float32)


def _on_device(data: np.ndarray, dev: Any, compute):
    """Run *compute*; on running out of device memory retry by streaming, then give up.

    Returns the result, or ``None`` when the device cannot do it at all (the
    caller then falls back to NumPy).
    """
    for attempt in range(2):
        try:
            return compute()
        except RuntimeError as exc:
            if not _is_out_of_memory(exc):
                raise
            # First failure: drop the resident copy and mark this dataset as too
            # big, so the retry streams it.  Second failure: not even one chunk fits.
            _resident.release()
            _resident.mark_too_big(data, dev)
            if dev.type == "cuda":
                torch.cuda.empty_cache()
    return None
