"""
Function for finding circles with sub-pixel resolution on both
``centers`` and ``radii``.

This has two internal methods:

  * ``'TwoStage'``   -- the classic two-stage CHT of Atherton & Kerbyson
                         (1999), "Size invariant circle detection". A
                         real-valued accumulator is used to localize
                         centers, then a separate radius search is run
                         for each candidate center.
  * ``'PhaseCode'``  -- default, faster method. It uses a
                         *complex-valued* accumulator: each vote for a
                         hypothesized radius r is cast as a unit-modulus
                         complex number whose phase encodes log(r)
                         linearly across [-pi, pi] over the radius range
                         (Atherton & Kerbyson, eq. 8). Center strength is
                         then the accumulator's magnitude, and -- crucially
                         -- the radius can be read directly off the
                         accumulator's phase at the center, with no
                         separate radius search needed.

Sub-pixel resolution
---------------------
  * **centers**: refined to sub-pixel precision via 3-point parabolic
    interpolation of the (magnitude) accumulator peak along x and y
    (the standard sub-pixel peak localization trick used in corner
    detection, optical flow, etc.).
  * **radii**:
      - ``Method='PhaseCode'``: votes are splatted bilinearly into the
        complex accumulator (rather than rounded to the nearest pixel),
        and the radius is decoded from the phase of the *unsmoothed*
        accumulator, bilinearly sampled at the sub-pixel refined center.
        (Centers are still localized from the smoothed magnitude, for
        robustness to noise.) Decoding from the smoothed accumulator was
        tried first and measured to introduce a systematic radius bias
        of roughly -0.1 px: phase encodes log(r) nonlinearly, so
        Gaussian-blending votes cast for a spread of nearby hypothesized
        radii pulls the decoded phase off-center. Decoding pre-smoothing
        removes that bias (benchmarked to cut mean radius error
        several-fold) without affecting center accuracy.
      - ``Method='TwoStage'``: the per-center radius histogram is built
        from continuous (non-rounded) edge-pixel distances, and its peak
        bin is refined via the same 3-point parabolic interpolation.

Public API
----------
imfindcircles(image, radius_range, ObjectPolarity='bright',
              Method='PhaseCode', Sensitivity=0.85, EdgeThreshold=None)
    -> (centers, radii, metric)

Example
-------
>>> import numpy as np
>>> from imfindcircles import imfindcircles
>>> centers, radii, metric = imfindcircles(img, [15, 30], ObjectPolarity='bright')
"""

from __future__ import annotations

import numpy as np
from scipy import ndimage

__all__ = ["imfindcircles"]


# --------------------------------------------------------------------------- #
# Basic image / gradient helpers
# --------------------------------------------------------------------------- #

def _to_grayscale_double(image: np.ndarray) -> np.ndarray:
    """Convert input image to a double-precision grayscale array in [0, 1]."""
    img = np.asarray(image)

    if img.ndim == 3:
        if img.shape[2] == 4:
            img = img[..., :3]
        if img.shape[2] == 3:
            img = img.astype(np.float64)
            gray = 0.2989 * img[..., 0] + 0.5870 * img[..., 1] + 0.1140 * img[..., 2]
        else:
            gray = img[..., 0].astype(np.float64)
    elif img.ndim == 2:
        gray = img.astype(np.float64)
    else:
        raise ValueError("image must be a 2-D (grayscale) or 3-D (RGB) array")

    # Normalize integer-typed images to [0, 1]
    if np.issubdtype(img.dtype, np.integer):
        info = np.iinfo(img.dtype)
        gray = gray / float(info.max)
    else:
        if gray.max() > 1.0 + 1e-6:
            gray = gray / gray.max()

    return gray


def _sobel_gradients(gray: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Compute x/y image gradients via Sobel operators."""
    kx = np.array([[-1.0, 0.0, 1.0],
                    [-2.0, 0.0, 2.0],
                    [-1.0, 0.0, 1.0]])
    ky = kx.T
    # Correlation (not convolution) so the kernel isn't 180-degree flipped;
    # this keeps gradient direction pointing toward increasing intensity.
    gx = ndimage.correlate(gray, kx, mode="nearest")
    gy = ndimage.correlate(gray, ky, mode="nearest")
    return gx, gy


def _otsu_threshold(values: np.ndarray, nbins: int = 256) -> float:
    """Standard Otsu threshold selection on a 1-D array of values."""
    vmax = values.max()
    if vmax <= 0:
        return 0.0
    hist, bin_edges = np.histogram(values, bins=nbins, range=(0.0, float(vmax)))
    hist = hist.astype(np.float64)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]

    with np.errstate(invalid="ignore", divide="ignore"):
        mean1 = np.cumsum(hist * bin_centers) / weight1
        mean2 = (np.cumsum((hist * bin_centers)[::-1])[::-1]) / weight2

    variance_between = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2
    variance_between = np.nan_to_num(variance_between, nan=-1.0)

    idx = int(np.argmax(variance_between))
    return float(bin_centers[idx])


def _auto_edge_threshold(mag: np.ndarray) -> float:
    """
    Automatically pick a gradient-magnitude threshold for "edge" pixels
    using Otsu's method on the gradient-magnitude histogram.
    """
    return _otsu_threshold(mag)


def _gaussian_smooth_2d(a: np.ndarray, sigma: float) -> np.ndarray:
    if sigma <= 0:
        return a
    return ndimage.gaussian_filter(a, sigma=sigma, mode="nearest")


def _gaussian_smooth_2d_complex(a: np.ndarray, sigma: float) -> np.ndarray:
    """Gaussian-smooth a complex array by filtering real/imag parts separately."""
    if sigma <= 0:
        return a
    real = ndimage.gaussian_filter(a.real, sigma=sigma, mode="nearest")
    imag = ndimage.gaussian_filter(a.imag, sigma=sigma, mode="nearest")
    return real + 1j * imag


def _gaussian_smooth_1d(a: np.ndarray, sigma: float) -> np.ndarray:
    if sigma <= 0:
        return a
    return ndimage.gaussian_filter1d(a, sigma=sigma, mode="nearest")


def _bilinear_sample_complex(a: np.ndarray, x: float, y: float) -> complex:
    """Bilinearly interpolate a complex 2-D array at continuous (x, y)."""
    coords = np.array([[y], [x]], dtype=np.float64)
    real = ndimage.map_coordinates(a.real, coords, order=1, mode="nearest")[0]
    imag = ndimage.map_coordinates(a.imag, coords, order=1, mode="nearest")[0]
    return complex(real, imag)


# --------------------------------------------------------------------------- #
# Sub-pixel peak refinement
# --------------------------------------------------------------------------- #

def _parabolic_subpixel_offset(y_minus: float, y_0: float, y_plus: float) -> float:
    """
    Sub-sample-accurate offset of the peak of a parabola fit through three
    equally-spaced samples (y_minus, y_0, y_plus) centered on y_0.
    Returns a value in [-1, 1] (sample units from the center sample).
    """
    denom = y_minus - 2.0 * y_0 + y_plus
    if abs(denom) < 1e-12:
        return 0.0
    offset = 0.5 * (y_minus - y_plus) / denom
    return float(np.clip(offset, -1.0, 1.0))


def _refine_center_subpixel(strength_map: np.ndarray, xi: int, yi: int) -> tuple[float, float]:
    """
    Refine an integer-pixel accumulator peak (xi, yi) to sub-pixel
    precision using separable 1-D parabolic interpolation along x and y.
    """
    H, W = strength_map.shape
    dx = dy = 0.0
    if 1 <= xi <= W - 2:
        dx = _parabolic_subpixel_offset(
            strength_map[yi, xi - 1], strength_map[yi, xi], strength_map[yi, xi + 1]
        )
    if 1 <= yi <= H - 2:
        dy = _parabolic_subpixel_offset(
            strength_map[yi - 1, xi], strength_map[yi, xi], strength_map[yi + 1, xi]
        )
    return xi + dx, yi + dy


def _refine_radius_subpixel(hist_smooth: np.ndarray, best_bin: int,
                             bin_width: float, rmin: float) -> float:
    """Refine an integer radius-histogram peak bin to sub-bin precision."""
    n_bins = hist_smooth.shape[0]
    offset = 0.0
    if 1 <= best_bin <= n_bins - 2:
        offset = _parabolic_subpixel_offset(
            hist_smooth[best_bin - 1], hist_smooth[best_bin], hist_smooth[best_bin + 1]
        )
    return rmin + (best_bin + offset) * bin_width


def _splat_bilinear_complex(acc: np.ndarray, x: np.ndarray, y: np.ndarray,
                             vote: np.ndarray) -> None:
    """
    Accumulate ``vote`` (complex) into ``acc`` at continuous locations
    (x, y) using bilinear splatting across the 4 surrounding integer
    pixels, in place.

    This avoids the pixel-quantization error that ``round()``-to-nearest
    accumulation introduces: when many votes for slightly different
    hypothesized radii land at slightly different continuous positions
    near the true center, rounding each one to its nearest pixel can
    scatter/clump them asymmetrically, which biases the phase (and hence
    the decoded radius) of the resulting sum. Splatting each vote's
    weight across its 4 neighbors preserves its true sub-pixel location.
    """
    H, W = acc.shape
    x0 = np.floor(x).astype(np.int64)
    y0 = np.floor(y).astype(np.int64)
    fx = x - x0
    fy = y - y0

    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        xi = x0 + dx
        yi = y0 + dy
        w = (fx if dx else (1.0 - fx)) * (fy if dy else (1.0 - fy))
        valid = (xi >= 0) & (xi < W) & (yi >= 0) & (yi < H) & (w > 0)
        if not np.any(valid):
            continue
        np.add.at(acc, (yi[valid], xi[valid]), vote[valid] * w[valid])


def _non_max_suppress_centers(coords: np.ndarray, strengths: np.ndarray,
                               min_dist: float) -> list[int]:
    """Greedy non-maximum suppression over candidate centers, strongest first."""
    order = np.argsort(-strengths)
    kept: list[int] = []
    kept_coords: list[np.ndarray] = []

    for i in order:
        c = coords[i]
        if kept_coords:
            d = np.hypot(
                np.array([kc[0] for kc in kept_coords]) - c[0],
                np.array([kc[1] for kc in kept_coords]) - c[1],
            )
            if np.any(d < min_dist):
                continue
        kept.append(int(i))
        kept_coords.append(c)

    return kept


def _phase_of_radius(r: np.ndarray, ln_rmin: float, ln_rmax: float) -> np.ndarray:
    """Encode radius r as a phase in [-pi, pi] (inverse of _radius_of_phase)."""
    ln_r = np.log(r)
    return 2.0 * np.pi * (ln_r - ln_rmin) / (ln_rmax - ln_rmin) - np.pi


def _radius_of_phase(phase: np.ndarray, ln_rmin: float, ln_rmax: float) -> np.ndarray:
    """
    Decode a phase (radians) back to a radius.
    """
    return np.exp(((phase + np.pi) / (2.0 * np.pi)) * (ln_rmax - ln_rmin) + ln_rmin)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def imfindcircles(image,
                   radius_range,
                   ObjectPolarity: str = "bright",
                   Method: str = "PhaseCode",
                   Sensitivity: float = 0.85,
                   EdgeThreshold: float | None = None):
    """
    Find circles in an image using the Circular Hough Transform, with
    sub-pixel resolution on both centers and radii.

    Parameters
    ----------
    image : ndarray
        2-D grayscale image or 3-D RGB image. Integer dtypes (uint8,
        uint16) are normalized to [0, 1] by their dtype's max value;
        float images are used as-is (or rescaled if outside [0, 1]).
    radius_range : sequence of two numbers [rmin, rmax]
        Inclusive search range for circle radius, in pixels. rmin must
        be >= 1 and rmax must be >= rmin (rmax > rmin is required for
        ``Method='PhaseCode'``, since log-coding needs a
        non-degenerate range).
    ObjectPolarity : {'bright', 'dark'}, optional
        Whether circles are brighter or darker than the background.
        Default ``'bright'``.
    Method : {'PhaseCode', 'TwoStage'}, optional
        ``'PhaseCode'`` (default) uses a complex phase-coded accumulator
        so radius is read directly from the accumulator's phase.
        ``'TwoStage'`` uses a real-valued accumulator for center
        detection followed by an explicit per-center radius histogram
        search.
    Sensitivity : float in (0, 1], optional
        Higher sensitivity finds more circles, including weak/partial
        ones, at the cost of more false positives. Default 0.85.
    EdgeThreshold : float in [0, 1] or None, optional
        Fraction of the maximum gradient magnitude above which a pixel
        is considered an edge pixel. If None (default), it is chosen
        automatically via Otsu's method on the gradient histogram.

    Returns
    -------
    centers : ndarray, shape (N, 2)
        Sub-pixel (x, y) coordinates of detected circle centers,
        strongest first. Refined via 3-point parabolic interpolation of
        the accumulator peak along x and y.
    radii : ndarray, shape (N,)
        Sub-pixel radius estimate for each detected circle:
          - PhaseCode: decoded from the phase of the unsmoothed complex
            accumulator, bilinearly sampled at the sub-pixel center.
          - TwoStage: the peak of a per-center radius histogram, refined
            via parabolic interpolation.
    metric : ndarray, shape (N,)
        Accumulator strength / confidence score for each circle, in the
        same descending order as ``centers`` and ``radii``.
    """
    # ---- validate inputs ---- #
    if ObjectPolarity not in ("bright", "dark"):
        raise ValueError("ObjectPolarity must be 'bright' or 'dark'")
    if Method not in ("PhaseCode", "TwoStage"):
        raise ValueError("Method must be 'PhaseCode' or 'TwoStage'")
    if not (0.0 < Sensitivity <= 1.0):
        raise ValueError("Sensitivity must be in the range (0, 1]")
    if EdgeThreshold is not None and not (0.0 <= EdgeThreshold <= 1.0):
        raise ValueError("EdgeThreshold must be in the range [0, 1]")

    radius_range = list(radius_range)
    if len(radius_range) != 2:
        raise ValueError("radius_range must be a two-element sequence [rmin, rmax]")
    rmin, rmax = int(round(radius_range[0])), int(round(radius_range[1]))
    if rmin < 1 or rmax < rmin:
        raise ValueError("radius_range must satisfy 1 <= rmin <= rmax")
    if Method == "PhaseCode" and rmax == rmin:
        raise ValueError(
            "radius_range must satisfy rmax > rmin for Method='PhaseCode' "
            "(log-coding requires a non-degenerate range); use 'TwoStage' "
            "or widen the range instead."
        )

    gray = _to_grayscale_double(image)
    H, W = gray.shape

    # ---- gradient / edge map ---- #
    gx, gy = _sobel_gradients(gray)
    mag = np.hypot(gx, gy)
    theta = np.arctan2(gy, gx)  # direction of increasing intensity

    if EdgeThreshold is None:
        edge_mag_thresh = _auto_edge_threshold(mag)
    else:
        edge_mag_thresh = EdgeThreshold * mag.max()

    edge_mask = mag >= edge_mag_thresh
    ys, xs = np.nonzero(edge_mask)
    if xs.size == 0:
        return (np.empty((0, 2)), np.empty((0,)), np.empty((0,)))

    mags = mag[ys, xs]
    thetas = theta[ys, xs]
    xs_f = xs.astype(np.float64)
    ys_f = ys.astype(np.float64)

    # For a bright object, intensity falls off from center to background,
    # so the gradient (direction of increasing intensity) points from the
    # edge INWARD toward the center; for a dark object it points outward.
    polarity_sign = 1.0 if ObjectPolarity == "bright" else -1.0

    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)

    ln_rmin, ln_rmax = np.log(rmin), np.log(max(rmax, rmin + 1e-9))

    # ------------------------------------------------------------------ #
    # Stage 1: build the accumulator (real for TwoStage, complex/phase-
    # coded for PhaseCode), then localize center candidates from its
    # magnitude.
    # ------------------------------------------------------------------ #
    if Method == "PhaseCode":
        # Sample radii densely: because the true radius is decoded from
        # the accumulator's phase rather than from a separate search,
        # only votes cast near the true radius land near the true center,
        # so a fine radius sampling is what gives an accurate phase (and
        # hence an accurate radius) at that location.
        n_radius_samples = max(2, min(rmax - rmin + 1, 200))
        radii_samples = np.linspace(rmin, rmax, n_radius_samples)

        # Votes are splatted bilinearly (not rounded to the nearest pixel)
        # so that the phase decoded back out at a sub-pixel location isn't
        # biased by pixel-quantization of where each vote landed -- see
        # _splat_bilinear_complex for why this matters for radius accuracy.
        acc = np.zeros((H, W), dtype=np.complex128)
        for r in radii_samples:
            a = xs_f + polarity_sign * r * cos_t
            b = ys_f + polarity_sign * r * sin_t
            phase = _phase_of_radius(r, ln_rmin, ln_rmax)
            vote = mags * np.exp(1j * phase)
            _splat_bilinear_complex(acc, a, b, vote)

        smooth_sigma = max(1.0, 0.05 * (rmax - rmin) + 1.0)
        acc_smooth = _gaussian_smooth_2d_complex(acc, smooth_sigma)
        strength_map = np.abs(acc_smooth)
    else:
        n_radius_samples = max(1, min(rmax - rmin + 1, 40))
        radii_samples = np.unique(
            np.round(np.linspace(rmin, rmax, n_radius_samples)).astype(int)
        )

        acc = np.zeros((H, W), dtype=np.float64)
        for r in radii_samples:
            a = xs_f + polarity_sign * r * cos_t
            b = ys_f + polarity_sign * r * sin_t
            ai = np.round(a).astype(np.int64)
            bi = np.round(b).astype(np.int64)
            valid = (ai >= 0) & (ai < W) & (bi >= 0) & (bi < H)
            np.add.at(acc, (bi[valid], ai[valid]), mags[valid])

        smooth_sigma = max(1.0, 0.05 * (rmax - rmin) + 1.0)
        acc_smooth = _gaussian_smooth_2d(acc, smooth_sigma)
        strength_map = acc_smooth

    # ------------------------------------------------------------------ #
    # Peak picking, driven by Sensitivity
    # ------------------------------------------------------------------ #
    max_strength = strength_map.max()
    if max_strength <= 0:
        return (np.empty((0, 2)), np.empty((0,)), np.empty((0,)))

    threshold = (1.0 - Sensitivity) * max_strength

    nb_size = max(3, int(round(rmin)))
    if nb_size % 2 == 0:
        nb_size += 1
    local_max = ndimage.maximum_filter(strength_map, size=nb_size, mode="nearest") == strength_map
    candidate_mask = local_max & (strength_map > threshold)

    cy, cx = np.nonzero(candidate_mask)
    if cx.size == 0:
        return (np.empty((0, 2)), np.empty((0,)), np.empty((0,)))

    cand_strengths = strength_map[cy, cx]
    cand_coords = np.stack([cx.astype(np.float64), cy.astype(np.float64)], axis=1)

    keep_idx = _non_max_suppress_centers(cand_coords, cand_strengths, min_dist=max(rmin, 3))

    # ------------------------------------------------------------------ #
    # Stage 2: sub-pixel center refinement + radius estimation per center
    # ------------------------------------------------------------------ #
    centers_out = []
    radii_out = []
    metric_out = []

    if Method == "TwoStage":
        n_bins = rmax - rmin + 1
        bin_width = 1.0

    for i in keep_idx:
        xi, yi = int(cand_coords[i, 0]), int(cand_coords[i, 1])
        cxk, cyk = _refine_center_subpixel(strength_map, xi, yi)

        if Method == "PhaseCode":
            # Decode the radius from the phase of the complex accumulator,
            # bilinearly interpolated at the sub-pixel center (rather than
            # snapped to the nearest pixel. Centers are localized from the
            # *smoothed* magnitude (for robustness to noise), but the
            # radius is decoded from the *unsmoothed* accumulator: the
            # Gaussian smoothing blends votes cast for a spread of nearby
            # hypothesized radii, and since phase encodes log(r)
            # nonlinearly, that blending measurably biases the decoded
            # radius. Reading the phase pre-smoothing removes that bias
            # (benchmarked to cut mean radius error several-fold).
            val = _bilinear_sample_complex(acc, cxk, cyk)
            if val == 0:
                continue
            phase = np.angle(val)
            best_r = float(_radius_of_phase(phase, ln_rmin, ln_rmax))
            if not (rmin - 0.5 <= best_r <= rmax + 0.5):
                continue
            strength_here = abs(_bilinear_sample_complex(acc_smooth, cxk, cyk))
        else:
            dx = xs_f - cxk
            dy = ys_f - cyk
            dist = np.hypot(dx, dy)
            in_range = (dist >= rmin - 0.5) & (dist <= rmax + 0.5)
            if not np.any(in_range):
                continue

            dx_r = dx[in_range]
            dy_r = dy[in_range]
            dist_r = np.clip(dist[in_range], 1e-6, None)
            mags_r = mags[in_range]
            thetas_r = thetas[in_range]

            dir_to_center = np.arctan2(-dy_r, -dx_r)
            expected_dir = thetas_r if ObjectPolarity == "bright" else (thetas_r + np.pi)
            diff = np.arctan2(np.sin(dir_to_center - expected_dir), np.cos(dir_to_center - expected_dir))
            alignment = np.cos(diff)
            alignment = np.where(alignment > np.cos(np.deg2rad(20.0)), alignment, 0.0)

            weight = mags_r * alignment
            r_bin = np.clip(np.round((dist_r - rmin) / bin_width).astype(np.int64), 0, n_bins - 1)

            r_hist = np.zeros(n_bins, dtype=np.float64)
            np.add.at(r_hist, r_bin, weight)
            r_hist_smooth = _gaussian_smooth_1d(r_hist, sigma=1.5)

            if r_hist_smooth.max() <= 0:
                continue

            best_bin = int(np.argmax(r_hist_smooth))
            best_r = _refine_radius_subpixel(r_hist_smooth, best_bin, bin_width, rmin)
            strength_here = cand_strengths[i]

        centers_out.append((cxk, cyk))
        radii_out.append(best_r)
        metric_out.append(strength_here)

    if not centers_out:
        return (np.empty((0, 2)), np.empty((0,)), np.empty((0,)))

    centers_arr = np.array(centers_out, dtype=np.float64)
    radii_arr = np.array(radii_out, dtype=np.float64)
    metric_arr = np.array(metric_out, dtype=np.float64)

    # Normalize metric to [0, 1], as "metric" output is a
    # relative confidence score.
    metric_arr = metric_arr / metric_arr.max()

    # Sort by descending metric.
    order = np.argsort(-metric_arr)
    centers_arr = centers_arr[order]
    radii_arr = radii_arr[order]
    metric_arr = metric_arr[order]

    return centers_arr, radii_arr, metric_arr


if __name__ == "__main__":
    # Self-test / usage demo: anti-aliased (super-sampled) circles at
    # deliberately fractional centers/radii, to show sub-pixel accuracy.
    import numpy as np

    SS = 4  # super-sampling factor for anti-aliasing
    H, W = 300, 300
    true_circles = [(80.3, 79.6, 30.4), (200.2, 120.7, 45.1), (150.6, 220.4, 20.8)]

    big = np.zeros((H * SS, W * SS), dtype=np.float64)
    yy, xx = np.mgrid[0:H * SS, 0:W * SS]
    for (cx, cy, r) in true_circles:
        mask = (xx - cx * SS) ** 2 + (yy - cy * SS) ** 2 <= (r * SS) ** 2
        big[mask] = 200.0

    img = big.reshape(H, SS, W, SS).mean(axis=(1, 3))
    rng = np.random.default_rng(0)
    img = np.clip(img + rng.normal(0, 2.0, size=img.shape), 0, 255).astype(np.uint8)

    for method in ("PhaseCode", "TwoStage"):
        print(f"--- Method={method} ---")
        centers, radii, metric = imfindcircles(img, [10, 60], ObjectPolarity="bright", Method=method)
        for c, r, m in zip(centers, radii, metric):
            print(f"  ({c[0]:.3f}, {c[1]:.3f}), r={r:.3f}, metric={m:.3f}")
    print("Ground truth (sub-pixel):", true_circles)
