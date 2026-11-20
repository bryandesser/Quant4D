"""Loading mask images from file (real-space ROI masks and diffraction masks)."""
from __future__ import annotations

import os

import numpy as np
from PIL import Image

__all__ = ["MASK_EXTENSIONS", "load_mask_image"]

MASK_EXTENSIONS = (".tif", ".tiff", ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".npy")


def load_mask_image(path: str, shape: tuple[int, int]) -> tuple[np.ndarray, list[str]]:
    """Read a mask image and fit it to an image of ``shape = (ny, nx)``.

    * Colour images are converted to greyscale; 16-bit and floating-point
      images keep their values.
    * An image of shape ``(nx, ny)`` is transposed to fit (and said so).
    * NaN/Inf become 0, and the maximum is scaled to 1 (if it is not 0 or 1).

    Returns
    -------
    mask : np.ndarray of float64, shape ``shape``
    notes : list of str
        What was changed, for telling the user.

    Raises
    ------
    ValueError
        Unsupported file type, or an image that does not fit.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext not in MASK_EXTENSIONS:
        raise ValueError(f"file type '{ext}' is not supported (use {', '.join(MASK_EXTENSIONS)})")
    if ext == ".npy":
        im = np.asarray(np.load(path, allow_pickle=False), dtype=np.float64)
    else:
        with Image.open(path) as img:
            if img.mode in ("RGB", "RGBA", "P", "LA", "CMYK", "YCbCr", "1"):
                img = img.convert("L")
            im = np.asarray(img, dtype=np.float64)
    if im.ndim != 2:
        raise ValueError(f"expected a 2-D image, got shape {im.shape}")

    notes = []
    ny, nx = int(shape[0]), int(shape[1])
    if im.shape != (ny, nx):
        if im.shape == (nx, ny):
            im = im.T
            notes.append(f"Image of shape {(nx, ny)} transposed to fit the data's shape {(ny, nx)}.")
        else:
            raise ValueError(f"image of shape (rows, columns) = {im.shape} does not fit the data's {(ny, nx)}")

    bad = ~np.isfinite(im)
    if bad.any():
        im = np.where(bad, 0.0, im)
        notes.append(f"{int(bad.sum())} NaN/Inf value(s) set to 0.")
    top = float(im.max())
    if top not in (0.0, 1.0):
        im = im / top
        notes.append(f"The maximum was {top:g}; scaled to 1.")
    return im, notes
