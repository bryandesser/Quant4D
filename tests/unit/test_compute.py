"""
Unit tests for callbacks.compute — pure functions, no Qt.

The dataset is a deliberately non-square scan of non-square patterns with an
off-diagonal beam centre.  Each function is checked against a slow,
obviously-correct reference written out in the test.
"""
import numpy as np
import pytest

from callbacks import compute
from callbacks.compute import backend

NFY, NFX, NPY, NPX = 3, 5, 8, 12
CENTER = (5.3, 2.6)       # (x, y)


@pytest.fixture(scope="module")
def data():
    rng = np.random.default_rng(7)
    return rng.random((NFY * NFX, NPY * NPX), dtype=np.float32)


@pytest.fixture(scope="module")
def k():
    return compute.radial_index((NPY, NPX), CENTER, 0.5)


def _cube(data):
    return data.reshape(NFY * NFX, NPY, NPX)


# --------------------------------------------------------------------- project
def test_project_matches_matmul(data):
    w = np.random.default_rng(1).random((NPY * NPX, 3)).astype(np.float32)
    np.testing.assert_allclose(compute.project(data, w), data @ w, rtol=1e-5)
    np.testing.assert_allclose(compute.project(data, w[:, 0]), data @ w[:, 0], rtol=1e-5)


def test_project_integer_data_does_not_overflow():
    d = np.full((4, 300), 250, dtype=np.uint8)
    out = compute.project(d, np.ones(300, dtype=bool))
    assert out.dtype == np.float32
    np.testing.assert_array_equal(out, 250 * 300)


def test_project_chunks_give_the_same_answer(data, monkeypatch):
    ints = (data * 1000).astype(np.uint16)
    w = np.arange(NPY * NPX, dtype=np.float32)
    whole = compute.project(ints, w)
    monkeypatch.setattr(backend, "CHUNK_BYTES", 1)      # one frame per chunk
    np.testing.assert_array_equal(compute.project(ints, w), whole)


def test_project_rejects_mismatched_weights(data):
    with pytest.raises(ValueError, match="do not match"):
        compute.project(data, np.ones(5))


def test_project_frames_matches_matmul(data, monkeypatch):
    w = np.linspace(0.0, 1.0, NFY * NFX)
    np.testing.assert_allclose(compute.project_frames(data, w), w @ data, rtol=1e-5)
    ints = (data * 1000).astype(np.uint16)
    whole = compute.project_frames(ints, w)
    np.testing.assert_allclose(whole, w @ ints.astype(np.float64), rtol=1e-5)
    monkeypatch.setattr(backend, "CHUNK_BYTES", 1)      # one frame per chunk
    np.testing.assert_allclose(compute.project_frames(ints, w), whole, rtol=1e-6)
    with pytest.raises(ValueError):
        compute.project_frames(data, np.ones(3))


def test_resolve_device_none_is_cpu():
    assert compute.resolve_device(None) is None


def test_gpu_request_falls_back_to_cpu_without_cuda(data, monkeypatch):
    monkeypatch.setattr(backend, "_TORCH_AVAILABLE", False)
    mask = np.ones((NPY, NPX), bool)
    np.testing.assert_allclose(compute.masked_sum(data, mask, "cuda:0"), data.sum(axis=1), rtol=1e-5)


# --------------------------------------------------------------------- annular
def test_radial_index_is_centred_on_xy(k):
    assert k.shape == (NPY, NPX)
    assert k[3, 5] == 0                                  # pixel (x=5, y=3) is nearest the centre
    assert k[0, 11] == int(np.hypot(11 - 5.3, 0 - 2.6) / 0.5)


def test_ring_integrals_sum_to_annular_image(data, k):
    rings = compute.ring_integrals(data, k)
    assert rings.shape == (NFY * NFX, k.max() + 1)
    for ri, ro in ((0, k.max()), (2, 7), (5, 5)):
        mask = compute.annular_mask(k, ri, ro)
        expected = _cube(data)[:, mask].sum(axis=1)
        np.testing.assert_allclose(rings[:, ri:ro + 1].sum(axis=1), expected, rtol=1e-5)
        np.testing.assert_allclose(compute.masked_sum(data, mask), expected, rtol=1e-5)


# ------------------------------------------------------------------------- CoM
def test_center_of_mass_reference(data, k):
    mask = compute.annular_mask(k, 1, 9)
    cx, cy = compute.center_of_mass(data, mask, CENTER)
    for f, frame in enumerate(_cube(data)):
        tot = sx = sy = 0.0
        for y in range(NPY):
            for x in range(NPX):
                if mask[y, x]:
                    tot += frame[y, x]
                    sx += frame[y, x] * (x - CENTER[0])
                    sy += frame[y, x] * (y - CENTER[1])
        assert cx[f] == pytest.approx(sx / tot, rel=1e-4, abs=1e-5)
        assert cy[f] == pytest.approx(sy / tot, rel=1e-4, abs=1e-5)


def test_center_of_mass_of_a_single_spot():
    d = np.zeros((1, NPY * NPX), np.float32)
    d[0, 6 * NPX + 9] = 3.0                              # spot at x=9, y=6
    cx, cy = compute.center_of_mass(d, np.ones((NPY, NPX), bool), (0, 0))
    assert (cx[0], cy[0]) == pytest.approx((9, 6))


def test_center_of_mass_empty_frame_is_zero():
    cx, cy = compute.center_of_mass(np.zeros((2, NPY * NPX), np.float32), np.ones((NPY, NPX), bool), CENTER)
    assert not cx.any() and not cy.any()


def test_rotate_field_quarter_turn():
    fx, fy = compute.rotate_field(np.array([1.0, 0.0]), np.array([0.0, 1.0]), 90)
    np.testing.assert_allclose(fx, [0, -1], atol=1e-12)
    np.testing.assert_allclose(fy, [1, 0], atol=1e-12)


def test_integrate_field_recovers_a_periodic_potential():
    ny, nx = 16, 24
    y, x = np.mgrid[0:ny, 0:nx]
    phi = np.sin(2 * np.pi * x / nx) + 0.5 * np.cos(2 * np.pi * 2 * y / ny)
    fx = np.fft.ifft2(2j * np.pi * np.fft.fftfreq(nx)[None, :] * np.fft.fft2(phi)).real    # exact d/dx
    fy = np.fft.ifft2(2j * np.pi * np.fft.fftfreq(ny)[:, None] * np.fft.fft2(phi)).real    # exact d/dy
    out = compute.integrate_field(fx, fy)
    np.testing.assert_allclose(out, phi - phi.mean(), atol=1e-10)


def test_divergence_of_a_linear_field():
    y, x = np.mgrid[0:6, 0:9].astype(float)
    np.testing.assert_allclose(compute.divergence(2 * x, 3 * y), 5.0)


# ------------------------------------------------------------------------- DPC
def _dpc_reference(data, k, center, ri, ro, ann_width, nseg, nrung, dr):
    """Segment by segment: integrate each segment, place it at its analytic centroid."""
    ann = ((k >= ri) & (k <= ro)).ravel()
    yy, xx = np.mgrid[0:NPY, 0:NPX]
    x, y = (xx - center[0]).ravel(), (yy - center[1]).ravel()
    ang = np.degrees(np.arctan2(y, x)) % 360.0
    rad = np.hypot(x, y)
    edges = np.linspace(ri * ann_width, ro * ann_width, nrung + 1)
    width = 360.0 / nseg
    starts = np.array([dr + i * width for i in range(nseg)]) % 360.0
    half = np.pi / nseg
    X = np.zeros(data.shape[0])
    Y = np.zeros_like(X)
    N = np.zeros_like(X)
    for r in range(nrung):
        lo_r, hi_r = edges[r], edges[r + 1]
        r_c = (2 / 3) * (hi_r ** 3 - lo_r ** 3) / (hi_r ** 2 - lo_r ** 2) * np.sin(half) / half
        rung = (rad >= lo_r) & (rad < hi_r)
        for s in range(nseg):
            lo, hi = starts[s], (starts[s] + width) % 360.0
            wedge = (ang >= lo) & (ang < hi) if lo < hi else (ang >= lo) | (ang < hi)
            sel = ann & rung & wedge
            mid = np.radians((starts[s] + 0.5 * width) % 360.0)
            seg = data[:, sel].astype(np.float64).sum(axis=1)       # this segment's signal
            X += r_c * np.cos(mid) * seg
            Y += r_c * np.sin(mid) * seg
            N += seg
    N = N.clip(np.finfo(np.float32).eps, None)
    return X / N, Y / N


@pytest.mark.parametrize("nseg, nrung, dr", [(4, 1, 0), (4, 3, 45), (8, 2, 30), (6, 1, 200), (3, 4, 359.5)])
def test_segmented_dpc_matches_segment_by_segment_reference(data, k, nseg, nrung, dr):
    ri, ro, ann_width = 1, 9, 0.5
    w = compute.segment_weights(compute.annular_mask(k, ri, ro), CENTER, ri * ann_width, ro * ann_width, nseg, nrung, dr)
    got_x, got_y = compute.segmented_dpc(data, w)
    ref_x, ref_y = _dpc_reference(data, k, CENTER, ri, ro, ann_width, nseg, nrung, dr)
    np.testing.assert_allclose(got_x, ref_x, rtol=1e-4, atol=1e-5)
    np.testing.assert_allclose(got_y, ref_y, rtol=1e-4, atol=1e-5)


def test_sector_centroid_radius_known_values():
    # quadrant of a full disc of radius R: 4*sqrt(2)*R / (3*pi)
    assert compute.sector_centroid_radius(0, 3.0, 4) == pytest.approx(4 * np.sqrt(2) * 3.0 / (3 * np.pi))
    # half disc: 4R / (3*pi)
    assert compute.sector_centroid_radius(0, 2.0, 2) == pytest.approx(4 * 2.0 / (3 * np.pi))
    # a full ring is centred on the detector
    assert compute.sector_centroid_radius(1.0, 2.0, 1) == pytest.approx(0, abs=1e-12)
    # thin, narrow sector sits at its mean radius
    assert compute.sector_centroid_radius(9.99, 10.01, 3600) == pytest.approx(10.0, rel=1e-4)


def test_segment_weights_have_the_centroid_radius_of_their_rung(k):
    ri_px, ro_px, nseg, nrung = 0.5, 4.5, 4, 2
    w = compute.segment_weights(compute.annular_mask(k, 1, 9), CENTER, ri_px, ro_px, nseg, nrung, 10)
    on = w[:, 2].astype(bool)
    assert not w[~on, :2].any()
    yy, xx = np.mgrid[0:NPY, 0:NPX]
    rad = np.hypot(xx - CENTER[0], yy - CENTER[1]).ravel()
    mid = (ri_px + ro_px) / 2
    for lo, hi in ((ri_px, mid), (mid, ro_px)):
        sel = on & (rad >= lo) & (rad < hi)
        assert sel.any()
        np.testing.assert_allclose(np.hypot(w[sel, 0], w[sel, 1]),
                                   compute.sector_centroid_radius(lo, hi, nseg), rtol=1e-6)


def test_rungs_change_the_dpc_signal(data, k):
    mask = compute.annular_mask(k, 1, 9)
    one = compute.segmented_dpc(data, compute.segment_weights(mask, CENTER, 0.5, 4.5, 4, 1))
    three = compute.segmented_dpc(data, compute.segment_weights(mask, CENTER, 0.5, 4.5, 4, 3))
    assert not np.allclose(one[0], three[0])


def test_finely_segmented_dpc_converges_to_center_of_mass():
    """Many small segments on a smooth pattern reproduce the true centre of mass."""
    ny = nx = 96
    c = (47.5, 47.5)
    yy, xx = np.mgrid[0:ny, 0:nx]
    shifts = [(0.0, 0.0), (2.5, -1.0), (-3.0, 4.0)]
    frames = np.stack([np.exp(-(((xx - c[0] - sx) ** 2 + (yy - c[1] - sy) ** 2) / (2 * 9.0 ** 2))).ravel()
                       for sx, sy in shifts]).astype(np.float32)
    kk = compute.radial_index((ny, nx), c, 0.5)
    mask = compute.annular_mask(kk, 0, 79)                # disc of radius 40 px
    com = compute.center_of_mass(frames, mask, c)
    coarse = compute.segmented_dpc(frames, compute.segment_weights(mask, c, 0.0, 40.0, 4, 1))
    fine = compute.segmented_dpc(frames, compute.segment_weights(mask, c, 0.0, 40.0, 32, 20))
    for axis in (0, 1):
        np.testing.assert_allclose(fine[axis], com[axis], atol=0.05)
        # and the fine detector is closer to the truth than four quadrants
        assert np.abs(fine[axis] - com[axis]).max() < np.abs(coarse[axis] - com[axis]).max()


# ----------------------------------------------------------------------- masks
def test_circle_mask_centre_is_xy():
    m = compute.circle_mask((NPY, NPX), (9, 2), 1.0)
    ys, xs = np.nonzero(m)
    assert sorted(zip(xs.tolist(), ys.tolist())) == [(8, 2), (9, 1), (9, 2), (9, 3), (10, 2)]


def test_circles_mask_is_the_union():
    a = compute.circle_mask((NPY, NPX), (2, 2), 1.5)
    b = compute.circle_mask((NPY, NPX), (9, 5), 1.5)
    np.testing.assert_array_equal(compute.circles_mask((NPY, NPX), [(2, 2), (9, 5)], 1.5), a | b)


def test_rectangle_mask_width_is_along_x():
    m = compute.rectangle_mask((NPY, NPX), (6, 4), (6, 2))
    ys, xs = np.nonzero(m)
    assert (xs.min(), xs.max(), ys.min(), ys.max()) == (3, 9, 3, 5)


def test_rectangle_mask_rotated_quarter_turn_swaps_sides():
    m = compute.rectangle_mask((NPY, NPX), (6, 4), (6, 2), 90)
    ys, xs = np.nonzero(m)
    assert (xs.min(), xs.max(), ys.min(), ys.max()) == (5, 7, 1, 7)


def test_polygon_mask_triangle():
    m = compute.polygon_mask((NPY, NPX), [(1, 1), (9, 1), (1, 6)])
    assert m[2, 2] and m[1 + 1, 6] and not m[6, 9] and not m[0, 0]


def test_ellipse_mask_is_a_disc():
    np.testing.assert_array_equal(compute.ellipse_mask((NPY, NPX), (5, 4), 2.0), compute.circle_mask((NPY, NPX), (5, 4), 2.0))


# ------------------------------------------------------------------------- ROI
def test_roi_pattern_point_is_that_frame(data):
    w = np.zeros((NFY, NFX))
    w[2, 3] = 1
    np.testing.assert_allclose(compute.roi_pattern(data, w), data[2 * NFX + 3], rtol=1e-6)


def test_roi_pattern_full_is_the_mean(data):
    np.testing.assert_allclose(compute.roi_pattern(data, np.ones((NFY, NFX))), data.mean(axis=0), rtol=1e-5)


def test_roi_pattern_small_and_large_selections_agree(data):
    small = np.zeros(NFY * NFX)
    small[[1, 4]] = 1                                    # takes the "read only those frames" path
    np.testing.assert_allclose(compute.roi_pattern(data, small), data[[1, 4]].mean(axis=0), rtol=1e-5)
    weighted = np.linspace(0.1, 1.0, NFY * NFX)          # takes the matrix-product path
    np.testing.assert_allclose(compute.roi_pattern(data, weighted), weighted @ data / weighted.sum(), rtol=1e-5)


def test_roi_pattern_empty_selection_is_zero(data):
    assert not compute.roi_pattern(data, np.zeros((NFY, NFX))).any()


def test_roi_pattern_rejects_wrong_frame_count(data):
    with pytest.raises(ValueError):
        compute.roi_pattern(data, np.ones(4))
