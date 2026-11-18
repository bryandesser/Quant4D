"""Centre-of-mass (CoM) imaging and the images derived from a deflection field."""
from __future__ import annotations

from typing import Any

import numpy as np

from callbacks.compute.backend import project
from callbacks.layout import pixel_grids

__all__ = ["center_of_mass", "weighted_mean_position", "rotate_field", "magnitude_phase", "integrate_field", "divergence",
           "curl", "scan_rotation_by_curl", "fourier_radius", "fourier_bandpass"]

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


def curl(fx: np.ndarray, fy: np.ndarray) -> np.ndarray:
    """Curl of a 2-D vector field: ``d(fy)/dx - d(fx)/dy`` (x along columns, y along rows)."""
    return np.gradient(fy, axis=1) - np.gradient(fx, axis=0)


def _mean_abs_curl(curl_p, div_p, angles_deg, batch=64):
    """Mean |curl| of the field turned by each angle: ``cos·curl + sin·div`` of the unturned field
    (curl and divergence are linear, so one pair of derivatives serves every angle)."""
    ok = np.isfinite(curl_p) & np.isfinite(div_p)
    c_p, d_p = curl_p[ok].astype(np.float64), div_p[ok].astype(np.float64)
    out = np.empty(len(angles_deg))
    for k in range(0, len(angles_deg), batch):
        a = np.radians(np.asarray(angles_deg[k:k + batch], float))[:, None]
        out[k:k + batch] = np.abs(np.cos(a) * c_p + np.sin(a) * d_p).mean(axis=1)
    return out


def scan_rotation_by_curl(fx: np.ndarray, fy: np.ndarray, prefer_deg: float = 0.0,
                          step_deg: float = 0.01) -> tuple[float, bool, float]:
    """Scan rotation (and Y flip) that makes a deflection field curl-free (MATLAB Quant4D's AutoCurl).

    A CoM/DPC deflection field is the gradient of a potential, so it has no curl once it is
    expressed in the scan's frame.  *fx*, *fy* are the field in the detector frame, before the
    scan rotation and Y flip (``rotate_field(fx, fy * (-1 if flip else 1), angle)`` is the field
    in the scan frame).  Every angle (1° steps, refined to *step_deg*) is tried with and without
    the flip; the smallest mean |curl| wins.  A field and its negative have the same curl, so
    the angle is found only up to 180°: of the two, the one nearer *prefer_deg* (the current scan
    direction) is returned.

    Returns
    -------
    angle_deg : float in [0, 360)
    flip : bool
        Whether the scan's Y direction is flipped.
    mean_abs_curl : float
        The remaining mean |curl| (relative to the field's mean magnitude it tells how good the fit is).
    """
    fx = np.asarray(fx, dtype=np.float64)
    fy = np.asarray(fy, dtype=np.float64)
    if fx.ndim != 2 or fx.shape != fy.shape or min(fx.shape) < 3:
        raise ValueError("the deflection images must be 2-D, of the same shape, at least 3 x 3")
    if not (np.isfinite(fx) & np.isfinite(fy)).any():
        raise ValueError("the deflection images have no finite values")
    best = None
    for flip in (False, True):
        py = -fy if flip else fy
        curl_p, div_p = curl(fx, py), divergence(fx, py)
        coarse = np.arange(0.0, 180.0, 1.0)                 # θ and θ+180 have the same |curl|
        m = _mean_abs_curl(curl_p, div_p, coarse)
        a0 = coarse[int(np.argmin(m))]
        fine = np.arange(a0 - 1.0, a0 + 1.0 + step_deg / 2, step_deg)
        mf = _mean_abs_curl(curl_p, div_p, fine)
        k = int(np.argmin(mf))
        if best is None or mf[k] < best[2]:
            best = (float(fine[k]), flip, float(mf[k]))
    angle, flip, residual = best
    # of angle and angle + 180, the nearer to the preferred (current) direction
    candidates = np.array([angle, angle + 180.0]) % 360.0
    dist = np.abs((candidates - prefer_deg + 180.0) % 360.0 - 180.0)
    return float(candidates[int(np.argmin(dist))]), flip, residual


def fourier_radius(shape) -> np.ndarray:
    """Distance of every Fourier component from zero frequency, in pixels of the transform
    (``fft2`` order): ``hypot(kx, ky)`` with ``kx`` in -nx/2 .. nx/2 - 1, likewise ``ky``."""
    ny, nx = int(shape[0]), int(shape[1])
    kx, ky = np.meshgrid(np.fft.fftfreq(nx) * nx, np.fft.fftfreq(ny) * ny)
    return np.hypot(kx, ky)


def fourier_bandpass(image: np.ndarray, low: float, high: float) -> np.ndarray:
    """Keep the spatial frequencies with ``low <= |k| <= high`` (pixels of the Fourier transform), as
    MATLAB Quant4D's iCoM/dCoM bandpass filter.  A filter that keeps everything returns *image*."""
    image = np.asarray(image, dtype=np.float64)
    kr = fourier_radius(image.shape)
    keep = (kr >= low) & (kr <= high)
    if keep.all():
        return image
    return np.fft.ifft2(np.fft.fft2(image) * keep).real
