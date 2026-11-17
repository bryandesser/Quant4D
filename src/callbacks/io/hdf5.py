"""Reading 4D-STEM data from an HDF5 dataset through h5py.

The offset-based reader (:mod:`callbacks.io.raw`) only works for datasets
stored contiguously and uncompressed.  Chunked or compressed datasets (the
usual case for files written by py4DSTEM, HyperSpy, LiberTEM and pyQuant4D's
own exporter with compression) have no single data offset, so they are read
through h5py instead, with the same cropping/binning/sampling as any other
format: :class:`H5Frames` presents the dataset as the ``(n_frames, n_pixels)``
array :func:`callbacks.io.raw.read_frames` expects.

Dataset layouts (C order, as h5py reports them):

* 4-D ``(ry, rx, py, px)`` — scan and pattern;
* 3-D ``(n, py, px)`` — a stack of frames, the scan given separately;
* 2-D ``(py, px)`` — a single pattern.
"""
from __future__ import annotations

from typing import Any

import numpy as np

__all__ = ["H5Frames", "dims4"]


def dims4(shape: tuple[int, ...]) -> tuple[int, int, int, int]:
    """``(ny, nx, py, px)`` of a 2-, 3- or 4-D dataset; missing leading scan axes are 1.

    A 3-D stack ``(n, py, px)`` gives ``(1, n, py, px)``: n frames along x.
    """
    if not 2 <= len(shape) <= 4:
        raise ValueError(f"expected a 2-, 3- or 4-D dataset, got shape {tuple(shape)}")
    full = (1,) * (4 - len(shape)) + tuple(int(s) for s in shape)
    return full[0], full[1], full[2], full[3]


class H5Frames:
    """An h5py dataset seen as a read-only ``(n_frames, n_pixels)`` array.

    Indexing with an integer, a slice or an increasing integer array reads
    only those frames.  Frames of one scan row (the blocks the readers ask
    for) come from a single hyperslab read.
    """

    def __init__(self, dataset: Any):
        self.ds = dataset
        ny, nx, py, px = dims4(dataset.shape)
        self.scan_shape = tuple(int(s) for s in dataset.shape[:-2]) or (1,)
        self.shape = (ny * nx, py * px)
        self.dtype = np.dtype(dataset.dtype)
        self._pattern = (py, px)

    def close(self) -> None:
        """Close the HDF5 file the dataset belongs to."""
        try:
            self.ds.file.close()
        except (AttributeError, ValueError):
            pass

    def __len__(self) -> int:
        return self.shape[0]

    def __getitem__(self, idx) -> np.ndarray:
        if isinstance(idx, (int, np.integer)):
            return self._read(np.array([int(idx)]))[0]
        if isinstance(idx, slice):
            return self._read(np.arange(*idx.indices(self.shape[0])))
        return self._read(np.asarray(idx, dtype=np.int64).ravel())

    def _read(self, flat: np.ndarray) -> np.ndarray:
        n = self.shape[0]
        if flat.size == 0:
            return np.empty((0, self.shape[1]), self.dtype)
        if flat.min() < 0 or flat.max() >= n:
            raise IndexError(f"frame index out of range 0..{n - 1}")
        if self.ds.ndim == 2:                        # a single pattern
            return np.repeat(np.asarray(self.ds[()]).reshape(1, -1), flat.size, axis=0)
        multi = np.unravel_index(flat, self.scan_shape)
        lead, last = multi[:-1], multi[-1]
        if all((a == a[0]).all() for a in lead):      # one scan row: one hyperslab
            lo, hi = int(last.min()), int(last.max()) + 1
            key = tuple(int(a[0]) for a in lead) + (slice(lo, hi),)
            block = np.asarray(self.ds[key])
            out = block[last - lo]
        else:                                        # spans rows: read frame by frame
            out = np.stack([np.asarray(self.ds[tuple(int(a[i]) for a in multi)]) for i in range(flat.size)])
        return out.reshape(flat.size, -1)
