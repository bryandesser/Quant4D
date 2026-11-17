"""Canonical array layout for pyQuant4D.

One convention, used everywhere
-------------------------------
The probe rasters left-to-right (``rx``, fast axis) and then steps down one
row (``ry``, slow axis).  Each diffraction pattern is stored row by row, so
within a frame ``px`` is the fast axis and ``py`` the slow one.  In C order
the dataset is therefore conceptually::

    (ry, rx, py, px)          shape (NFrY, NFrX, NPxY, NPxX)

``self.Data`` holds exactly that memory, flattened to two dimensions::

    (frame, pixel)            shape (NFrY * NFrX, NPxY * NPxX)
    frame = ry * NFrX + rx
    pixel = py * NPxX + px

Images handed to matplotlib are ``(rows, cols) == (y, x)`` and are drawn with
the origin in the upper-left corner, matching the microscope display.  UI
coordinates such as ``TBX``/``TBY``, ``FrameX``/``FrameY`` and the annotation
centres are ``(x, y)``, i.e. ``(column, row)``, and are **0-based**: pixel
``i`` is centred on coordinate ``i`` and spans ``[i - 0.5, i + 0.5]``, so the
valid range is ``0 .. N - 1`` and the exact image centre is ``(N - 1) / 2``.

MATLAB is column-major, so the original code built its pixel grids as
``(x, y)`` arrays and flattened them column-first.  Doing the same in NumPy
(``np.mgrid[0:NPxX, 0:NPxY].flatten()``) silently transposes the grid relative
to the data.  Always build grids and reshape images through the helpers in
this module rather than by hand.

Note that ``D.NPx`` is ``[NPxX, NPxY]`` (an ``(x, y)`` size vector, used for
clipping UI coordinates) and is **not** a valid image shape.  Use
:func:`dfrn_shape` instead.
"""
from __future__ import annotations

import numpy as np

__all__ = [
    "real_shape",
    "dfrn_shape",
    "dfrn_grids",
    "pixel_grids",
    "as_4d",
    "check_layout",
    "ensure_c_contiguous",
]


def real_shape(D) -> tuple[int, int]:
    """Shape of a real-space image: ``(NFrY, NFrX)``."""
    return int(D.NFrY), int(D.NFrX)


def dfrn_shape(D) -> tuple[int, int]:
    """Shape of a diffraction-space image: ``(NPxY, NPxX)``."""
    return int(D.NPxY), int(D.NPxX)


def dfrn_grids(D, origin=(0.0, 0.0)) -> tuple[np.ndarray, np.ndarray]:
    """Pixel coordinate grids for diffraction space.

    Parameters
    ----------
    D :
        Dataset parameters exposing ``NPxX`` and ``NPxY``.
    origin : (x, y)
        Point the coordinates are measured from, e.g. the transmitted-beam
        centre ``self.B0``.

    Returns
    -------
    xx, yy : np.ndarray, each of shape ``(NPxY, NPxX)``
        ``xx[py, px] == px - origin[0]`` and ``yy[py, px] == py - origin[1]``.
        ``xx.ravel()`` / ``yy.ravel()`` line up with the pixel axis of
        ``self.Data``.
    """
    return pixel_grids(dfrn_shape(D), origin)


def pixel_grids(shape, origin=(0.0, 0.0)) -> tuple[np.ndarray, np.ndarray]:
    """``(xx, yy)`` coordinate grids for an image of *shape* ``(ny, nx)``.

    ``xx[y, x] == x - origin[0]`` and ``yy[y, x] == y - origin[1]``; *origin* is
    an ``(x, y)`` point.  This is the shape-only form of :func:`dfrn_grids`.
    """
    ny, nx = int(shape[0]), int(shape[1])
    yy, xx = np.mgrid[0:ny, 0:nx]
    return xx - float(origin[0]), yy - float(origin[1])


def check_layout(data, D) -> None:
    """Raise ``ValueError`` if *data* is not the ``(frame, pixel)`` array *D* describes."""
    (nfy, nfx), (npy, npx) = real_shape(D), dfrn_shape(D)
    expected = (nfy * nfx, npy * npx)
    if tuple(data.shape) != expected:
        raise ValueError(
            f"Dataset has shape {tuple(data.shape)}, expected {expected} "
            f"= (NFrY*NFrX, NPxY*NPxX) for a {nfy}x{nfx} scan of {npy}x{npx} patterns."
        )


def as_4d(data, D) -> np.ndarray:
    """View the flat ``(frame, pixel)`` array as ``(ry, rx, py, px)`` without copying."""
    check_layout(data, D)
    return data.reshape(*real_shape(D), *dfrn_shape(D))


def ensure_c_contiguous(arr: np.ndarray) -> np.ndarray:
    """Return *arr* unchanged if it is C-contiguous, otherwise a C-contiguous copy."""
    return arr if arr.flags["C_CONTIGUOUS"] else np.ascontiguousarray(arr)
