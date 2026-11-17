"""Centre-of-mass (CoM) imaging and the images derived from a deflection field."""
from __future__ import annotations

from typing import Any

import numpy as np

from callbacks.compute.backend import project
from callbacks.layout import pixel_grids

__all__ = ["center_of_mass", "weighted_mean_position", "rotate_field", "magnitude_phase", "integrate_field", "divergence"]

_EPS = float(np.finfo(np.float32).eps)


def center_of_mass(data: np.ndarray, mask: np.ndarray, center, device: Any = None,
                   ) -> tuple[np.ndarray, np.ndarray]:
    """Intensity-weighted centre of mass of every frame, relative to *center*.

    Parameters
    ----------
    data : np.ndarray, shape (n_frames, n_pixels)
    mask : np.ndarray of bool, shape (NPxY, NPxX)
        Detector pixels to include.
    center : (x, y)
        Origin of the coordinates, normally the transmitted-beam centre.

    Returns
    -------
    com_x, com_y : np.ndarray, shape (n_frames,)
        ``com_x`` is the shift along detector columns (display x) and ``com_y``
        along detector rows (display y, pointing down the screen).  Frames with
        no intensity inside the mask give 0.
    """
    mask = np.asarray(mask, dtype=bool)
    xx, yy = pixel_grids(mask.shape, center)
    return weighted_mean_position(data, mask, xx, yy, device)


def weighted_mean_position(data: np.ndarray, mask: np.ndarray, x: np.ndarray, y: np.ndarray,
                           device: Any = None) -> tuple[np.ndarray, np.ndarray]:
    """Intensity-weighted mean of the per-pixel coordinates *x*, *y* within *mask*.

    The general form of :func:`center_of_mass` for caller-supplied coordinate
    grids; *mask*, *x* and *y* all have one entry per diffraction pixel.
    """
    m = np.asarray(mask, dtype=bool).ravel().astype(np.float32)
    x_flat = np.asarray(x, dtype=np.float32).ravel()
    y_flat = np.asarray(y, dtype=np.float32).ravel()
    weights = np.stack([m * x_flat, m * y_flat, m], axis=1)     # (n_pixels, 3)
    sums = project(data, weights, device)
    norm = np.clip(sums[:, 2], _EPS, None)
    return sums[:, 0] / norm, sums[:, 1] / norm


def rotate_field(fx: np.ndarray, fy: np.ndarray, angle_deg: float) -> tuple[np.ndarray, np.ndarray]:
    """Rotate the vector field ``(fx, fy)`` by *angle_deg* (counter-clockwise for x right, y up)."""
    c, s = np.cos(np.radians(angle_deg)), np.sin(np.radians(angle_deg))
    fx = np.asarray(fx, dtype=np.float64)
    fy = np.asarray(fy, dtype=np.float64)
    return c * fx - s * fy, s * fx + c * fy


def magnitude_phase(fx: np.ndarray, fy: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Magnitude and direction (radians, ``arctan2(fy, fx)``) of a vector field."""
    return np.hypot(fx, fy), np.arctan2(fy, fx)


def integrate_field(fx: np.ndarray, fy: np.ndarray) -> np.ndarray:
    """Fourier integration of a 2-D vector field (iCoM / iDPC).

    Returns the scalar image whose gradient best matches ``(fx, fy)``, with its
    mean set to zero.  ``fx`` varies along columns (axis 1), ``fy`` along rows
    (axis 0).
    """
    ny, nx = fx.shape
    KX, KY = np.meshgrid(np.fft.fftfreq(nx), np.fft.fftfreq(ny))
    k2 = KX ** 2 + KY ** 2
    k2[0, 0] = 1.0      # avoid 0/0; the numerator is 0 there, so the mean comes out as 0
    return np.fft.ifft2(
        (KX * np.fft.fft2(fx) + KY * np.fft.fft2(fy)) / (2j * np.pi * k2)
    ).real


def divergence(fx: np.ndarray, fy: np.ndarray) -> np.ndarray:
    """Divergence of a 2-D vector field (dCoM / dDPC): ``d(fx)/dx + d(fy)/dy``."""
    return np.gradient(fx, axis=1) + np.gradient(fy, axis=0)
