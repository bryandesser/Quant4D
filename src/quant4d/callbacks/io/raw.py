"""Reading 4D-STEM data stored as consecutive frames in a binary file.

Covers every format Quant4D imports by offset (raw/EMPAD, Medipix, MRC,
DM3/DM4, contiguous HDF5): the file holds ``n_frames`` records of
``[header][NPxY x NPxX elements][footer]`` starting at ``offset``.

Only the requested part of the file is read, a bounded block at a time, and
it can be cropped, binned (diffraction) and sampled (scan) on the way in, so a
dataset larger than memory can still be opened in reduced form.
"""
from __future__ import annotations

from typing import Callable, Literal, Optional

import numpy as np

from .export import Region, _iter_blocks, exported_shape

__all__ = ["frame_record_dtype", "open_frames", "read_frames", "float_type_for"]


def frame_record_dtype(dtype, n_pixels: int, header: int = 0, footer: int = 0,
                       byte_order: str = "l") -> np.dtype:
    """Structured dtype of one frame record: header bytes, the pixels, footer bytes."""
    order: Literal["<", ">", "="] = "<" if byte_order == "l" else ">" if byte_order == "b" else "="
    elem = np.dtype(dtype).newbyteorder(order) if np.dtype(dtype).itemsize > 1 else np.dtype(dtype)
    return np.dtype([("header", "u1", (header,)), ("data", elem, (n_pixels,)), ("footer", "u1", (footer,))])


def open_frames(path: str, offset: int, n_frames: int, n_pixels: int, dtype,
                header: int = 0, footer: int = 0, byte_order: str = "l") -> np.ndarray:
    """Memory-map the frames of a file as a read-only ``(n_frames, n_pixels)`` array (no data is read)."""
    rec = frame_record_dtype(dtype, n_pixels, header, footer, byte_order)
    return np.memmap(path, dtype=rec, mode="r", offset=offset, shape=(n_frames,))["data"]


def float_type_for(dtype) -> np.dtype:
    """Floating-point type the dataset is held in: float64 for 64-bit data, otherwise float32."""
    return np.dtype(np.float64 if np.dtype(dtype).itemsize > 4 else np.float32)


def read_frames(frames_on_disk: np.ndarray, scan: tuple[int, int], detector: tuple[int, int],
                frames: Optional[Region] = None, pixels: Optional[Region] = None,
                progress: Optional[Callable[[float], None]] = None) -> np.ndarray:
    """Read (part of) a dataset into memory as floating point, in native byte order.

    Parameters
    ----------
    frames_on_disk : array-like, shape (n_frames, n_pixels)
        Usually from :func:`open_frames`.
    scan, detector : (nx, ny)
        Size of the scan and of the diffraction pattern on disk.
    frames, pixels : Region, optional
        Which probe positions (start, count, sampling interval) and which
        detector pixels (start, count, binning by summation).  Default: all.
    progress : callable, optional
        Called with the fraction done after each block.

    Returns
    -------
    np.ndarray, shape (NFrY_out * NFrX_out, NPxY_out * NPxX_out)
    """
    from .export import full_region

    frames = frames or full_region(scan)
    pixels = pixels or full_region(detector)
    frames.check(scan, binned=False)
    pixels.check(detector, binned=True)
    ny, nx, py, px = exported_shape(frames, pixels)
    out_dtype = float_type_for(frames_on_disk.dtype)
    out = np.empty((ny * nx, py * px), dtype=out_dtype)

    # Bin in floating point: convert each block before summing.
    as_float = _FloatView(frames_on_disk, out_dtype)
    done = 0
    for row, col, block in _iter_blocks(as_float, scan, detector, frames, pixels):
        start = row * nx + col
        out[start:start + block.shape[0]] = block.reshape(block.shape[0], -1)
        done += block.shape[0]
        if progress is not None:
            progress(done / out.shape[0])
    return out


class _FloatView:
    """Wraps an on-disk array so that indexing returns native floating point."""

    def __init__(self, arr, dtype):
        self.arr, self.dtype = arr, np.dtype(dtype)
        self.shape = arr.shape

    def __getitem__(self, idx):
        return np.asarray(self.arr[idx], dtype=self.dtype)
