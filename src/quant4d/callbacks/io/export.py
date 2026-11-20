"""Writing images and datasets to disk.

Pure functions only: nothing here touches Qt or the application object, so
every function can be tested on its own.  The Save window callbacks in
:mod:`callbacks.save_export` read the widgets and call into this module.

Conventions (see :mod:`callbacks.layout`)
-----------------------------------------
* ``data`` is the flat ``(frame, pixel)`` dataset, ``frame = ry*NFrX + rx`` and
  ``pixel = py*NPxX + px``.
* Regions are given as ``(x, y)`` start points and ``(x, y)`` counts, 0-based.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterator, Optional

import numpy as np
from PIL import Image

__all__ = [
    "Region", "full_region", "exported_shape", "exported_dtype", "iter_exported_frames",
    "write_hdf5", "write_raw", "dims_suffix", "save_tiff", "save_png", "rgb_as_displayed",
]

#: Upper bound on the size of any temporary block read from the dataset, in bytes.
CHUNK_BYTES = 256 * 1024 ** 2


# ---------------------------------------------------------------------------
# Regions
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Region:
    """A rectangular part of a 2-D grid, optionally binned or sampled.

    Attributes
    ----------
    start : (x, y)
        First point taken, 0-based.
    count : (x, y)
        Number of output points along x and y.
    step : int
        For the diffraction pattern, the binning distance: each output pixel is
        the sum of a ``step x step`` block, so the region covers
        ``count * step`` input pixels.  For the scan, the sampling interval:
        every ``step``-th probe position is kept, so the region spans
        ``(count - 1) * step + 1`` input positions.
    """
    start: tuple[int, int]
    count: tuple[int, int]
    step: int = 1

    def check(self, size: tuple[int, int], binned: bool) -> None:
        """Raise ``ValueError`` unless the region lies inside a grid of ``size = (nx, ny)``."""
        if self.step < 1 or min(self.count) < 1 or min(self.start) < 0:
            raise ValueError(f"invalid region {self}")
        for axis, name in ((0, "x"), (1, "y")):
            span = self.count[axis] * self.step if binned else (self.count[axis] - 1) * self.step + 1
            if self.start[axis] + span > size[axis]:
                raise ValueError(
                    f"region {self} reaches {name} = {self.start[axis] + span - 1}, "
                    f"beyond the last index {size[axis] - 1}"
                )


def full_region(size: tuple[int, int]) -> Region:
    """The whole of a grid of ``size = (nx, ny)``."""
    return Region((0, 0), (int(size[0]), int(size[1])), 1)


def exported_shape(frames: Region, pixels: Region) -> tuple[int, int, int, int]:
    """Shape of the exported dataset: ``(NFrY, NFrX, NPxY, NPxX)``."""
    return frames.count[1], frames.count[0], pixels.count[1], pixels.count[0]


def exported_dtype(dtype, pixels: Region) -> np.dtype:
    """Data type written for a dataset of *dtype*.

    Unchanged unless the diffraction pattern is binned, in which case integer
    data is widened (to at least 32 bits) so that the sums cannot overflow.
    """
    dtype = np.dtype(dtype)
    if pixels.step == 1 or dtype.kind == "f":
        return dtype
    wide = {"u": np.uint32, "i": np.int32}.get(dtype.kind)
    return np.result_type(dtype, wide) if wide is not None else dtype


def iter_exported_frames(data: np.ndarray, scan: tuple[int, int], detector: tuple[int, int],
                         frames: Region, pixels: Region) -> Iterator[np.ndarray]:
    """Yield the exported dataset one scan row at a time, or less if a row is too large.

    Parameters
    ----------
    data : np.ndarray, shape (NFrY*NFrX, NPxY*NPxX)
    scan, detector : (nx, ny)
        Size of the scan and of the diffraction pattern of *data*.
    frames, pixels : Region
        Which probe positions (sampled) and which detector pixels (binned).

    Yields
    ------
    np.ndarray, shape (n, NPxY_out, NPxX_out)
        Consecutive exported frames in raster order (x fastest), with the
        dtype given by :func:`exported_dtype`.
    """
    frames.check(scan, binned=False)
    pixels.check(detector, binned=True)
    for _, _, block in _iter_blocks(data, scan, detector, frames, pixels):
        yield block


def _iter_blocks(data, scan, detector, frames: Region, pixels: Region):
    """Like :func:`iter_exported_frames`, also yielding the output scan row and column of each block."""
    nfx, nfy = scan
    npx, npy = detector
    out_dtype = exported_dtype(data.dtype, pixels)
    b = pixels.step
    x0, y0 = pixels.start
    cx, cy = pixels.count

    xs = frames.start[0] + frames.step * np.arange(frames.count[0])
    per_block = max(1, CHUNK_BYTES // max(1, npx * npy * data.dtype.itemsize))
    for j in range(frames.count[1]):
        ry = frames.start[1] + frames.step * j
        rows = ry * nfx + xs
        for k in range(0, rows.size, per_block):
            block = np.asarray(data[rows[k:k + per_block]]).reshape(-1, npy, npx)
            block = block[:, y0:y0 + cy * b, x0:x0 + cx * b]
            if b > 1:
                block = block.reshape(-1, cy, b, cx, b).sum(axis=(2, 4), dtype=out_dtype)
            yield j, k, np.ascontiguousarray(block, dtype=out_dtype)


# ---------------------------------------------------------------------------
# Dataset writers
# ---------------------------------------------------------------------------
def _with_byteorder(dtype: np.dtype, byte_order: str) -> np.dtype:
    """*dtype* in byte order ``'l'`` (little endian) or ``'b'`` (big endian)."""
    if byte_order not in ("l", "b"):
        raise ValueError(f"byte order must be 'l' or 'b', not {byte_order!r}")
    return np.dtype(dtype).newbyteorder("<" if byte_order == "l" else ">")


def write_raw(path: str, data: np.ndarray, scan, detector, frames: Region, pixels: Region,
              byte_order: str = "l") -> tuple[int, int, int, int]:
    """Write the selection as a headerless binary file, frame after frame.

    Frames are in raster order (x fastest) and each frame is stored row by row,
    i.e. the C-order layout of an array of shape ``(NFrY, NFrX, NPxY, NPxX)``.

    Returns the shape written.
    """
    shape = exported_shape(frames, pixels)
    dtype = _with_byteorder(exported_dtype(data.dtype, pixels), byte_order)
    tmp = path + ".part"
    with open(tmp, "wb") as fh:
        for block in iter_exported_frames(data, scan, detector, frames, pixels):
            fh.write(block.astype(dtype, copy=False).tobytes())
    os.replace(tmp, path)
    return shape


def write_hdf5(path: str, data: np.ndarray, scan, detector, frames: Region, pixels: Region,
               byte_order: str = "l", metadata: Optional[dict] = None,
               dataset: str = "data") -> tuple[int, int, int, int]:
    """Write the selection to an HDF5 file.

    The dataset ``/data`` has shape ``(NFrY, NFrX, NPxY, NPxX)``, is stored
    contiguously and uncompressed (so Quant4D can import it again by
    offset), and *metadata* is written as attributes of the group
    ``/metadata``.

    Returns the shape written.
    """
    import h5py

    shape = exported_shape(frames, pixels)
    dtype = _with_byteorder(exported_dtype(data.dtype, pixels), byte_order)
    tmp = path + ".part"
    with h5py.File(tmp, "w") as f:
        dset = f.create_dataset(dataset, shape=shape, dtype=dtype)   # contiguous, no compression
        dset.attrs["axes"] = "ry, rx, py, px"
        frames.check(scan, binned=False)
        pixels.check(detector, binned=True)
        for row, col, block in _iter_blocks(data, scan, detector, frames, pixels):
            dset[row, col:col + block.shape[0]] = block
        meta = f.create_group("metadata")
        for key, value in (metadata or {}).items():
            if value is None:
                continue
            meta.attrs[key] = value
    os.replace(tmp, path)
    return shape


def dims_suffix(frames: Region, pixels: Region) -> str:
    """``_<NPxX>x<NPxY>x<NFrX>x<NFrY>``: the naming scheme the importer reads back."""
    return "_{}x{}x{}x{}".format(pixels.count[0], pixels.count[1], frames.count[0], frames.count[1])


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------
def save_tiff(path: str, image: np.ndarray) -> None:
    """Save a 2-D image as a single-precision floating point TIFF."""
    image = np.asarray(image, dtype=np.float32)
    if image.ndim != 2:
        raise ValueError(f"expected a 2-D image, got shape {image.shape}")
    Image.fromarray(image, mode="F").save(path, format="TIFF")


def rgb_as_displayed(axes_image, background=(0.0, 0.0, 0.0)) -> np.ndarray:
    """The pixels of a matplotlib ``AxesImage`` exactly as drawn, one per data point.

    Applies the image's colormap, colour limits and (per-pixel) transparency,
    composited over *background* (the image windows are black).

    Returns
    -------
    np.ndarray of uint8, shape (ny, nx, 3)
    """
    rgba = np.asarray(axes_image.to_rgba(axes_image.get_array(), bytes=False), dtype=float)
    alpha = axes_image.get_alpha()
    a = rgba[..., 3] if alpha is None else rgba[..., 3] * np.broadcast_to(np.asarray(alpha, float), rgba.shape[:2])
    rgb = rgba[..., :3] * a[..., None] + np.asarray(background, float) * (1.0 - a[..., None])
    return np.round(np.clip(rgb, 0.0, 1.0) * 255).astype(np.uint8)


def save_png(path: str, rgb: np.ndarray) -> None:
    """Save an ``(ny, nx, 3)`` uint8 image as PNG."""
    Image.fromarray(np.asarray(rgb, dtype=np.uint8), mode="RGB").save(path, format="PNG")
