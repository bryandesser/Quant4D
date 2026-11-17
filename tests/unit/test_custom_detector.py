"""
Unit tests for the custom detector maths: callbacks.compute.custom and
callbacks.compute.mask_math.  Pure functions, no Qt.

Masks are (NPxY, NPxX) arrays indexed [y, x]; points are (x, y), 0-based.
The pattern is deliberately non-square so x/y swaps show up.
"""
import numpy as np
import pytest

from callbacks.compute import custom as cm
from callbacks.compute.mask_math import MaskMathError, evaluate_mask_formula, mask_ids

NY, NX = 20, 30
SHAPE = (NY, NX)
B0 = np.array([14.0, 9.0])
YY, XX = np.mgrid[0:NY, 0:NX]


def _disc(c, r):
    return np.hypot(XX - c[0], YY - c[1]) <= r


# ---------------------------------------------------------------------------
# custom.py
# ---------------------------------------------------------------------------
def test_combine_parts():
    a, b = _disc((5, 5), 3), _disc((7, 5), 3)
    assert np.array_equal(cm.combine_parts([a, b], "Union"), a | b)
    assert np.array_equal(cm.combine_parts([a, b], "Intersection"), a & b)
    assert np.array_equal(cm.combine_parts([a, b], "Additive"), a.astype(float) + b)


def test_circle_detector_and_mirror():
    p, r = B0 + [5, 2], 3
    assert np.array_equal(cm.circle_detector(SHAPE, p, r, B0), _disc(p, r))
    mirror = 2 * B0 - p
    both = cm.circle_detector(SHAPE, p, r, B0, mirrored=True)
    assert np.array_equal(both.astype(bool), _disc(p, r) | _disc(mirror, r))
    # overlapping mirror: intersection/additive differ from union
    q = B0 + [1, 0]
    assert np.array_equal(cm.circle_detector(SHAPE, q, 3, B0, True, "Intersection").astype(bool),
                          _disc(q, 3) & _disc(2 * B0 - q, 3))
    assert cm.circle_detector(SHAPE, q, 3, B0, True, "Additive").max() == 2


def test_grid_points_lattice():
    p1, p2 = B0 + [6, 0], B0 + [0, 5]
    pts = cm.grid_points(SHAPE, B0, p1, p2, 1.5)
    assert any(np.allclose(p, B0) for p in pts), "transmitted beam is a lattice site"
    for p in pts:   # every site is an integer combination of the basis vectors
        i, j = (p - B0) / [6, 5]
        assert np.isclose(i, round(i)) and np.isclose(j, round(j))
    # every site with its disc overlapping the pattern is present
    expected = {(i, j) for i in range(-5, 6) for j in range(-5, 6)
                if -1.5 <= 14 + 6 * i <= NX - 1 + 1.5 and -1.5 <= 9 + 5 * j <= NY - 1 + 1.5}
    got = {tuple(np.round((p - B0) / [6, 5]).astype(int)) for p in pts}
    assert got == expected


def test_grid_no_center_checkerboard():
    p1, p2 = B0 + [6, 0], B0 + [0, 5]
    pts = cm.grid_points(SHAPE, B0, p1, p2, 1.5, no_center=True)
    ij = np.round((pts - B0) / [6, 5]).astype(int)
    assert not any(np.allclose(p, B0) for p in pts)
    assert np.all((ij[:, 0] + ij[:, 1]) % 2 == 1), "only sites where i and j differ in parity remain"


def test_grid_detector_modes():
    pts = np.array([[5.0, 5.0], [7.0, 5.0]])
    a, b = _disc(pts[0], 2), _disc(pts[1], 2)
    assert np.array_equal(cm.grid_detector(SHAPE, pts, 2, "Union").astype(bool), a | b)
    assert np.array_equal(cm.grid_detector(SHAPE, pts, 2, "Intersection").astype(bool), a & b)
    assert np.array_equal(cm.grid_detector(SHAPE, pts, 2, "Additive"), a.astype(float) + b)


def test_bandpass():
    m = cm.bandpass_detector(SHAPE, B0, 3, 7).astype(bool)
    r = np.hypot(XX - B0[0], YY - B0[1])
    assert m[r < 2.9].sum() == 0 and m[r > 7.1].sum() == 0
    assert m[(r > 3.1) & (r < 6.9)].all()


def test_wedge_mirrored_and_not():
    p1, p2 = B0 + [8, 0.5], B0 + [8, 4]           # a narrow wedge pointing +x, slightly +y
    single = cm.wedge_detector(SHAPE, B0, p1, p2, mirrored=False).astype(bool)
    assert single[9, 22] or single[10, 22]
    assert not single[9, 5], "un-mirrored wedge must not reach the -x side"
    both = cm.wedge_detector(SHAPE, B0, p1, p2, mirrored=True).astype(bool)
    assert both[8, 5] or both[9, 5] or both[7, 5], "mirrored copy points -x"
    assert both[int(B0[1]), int(B0[0])], "apex is included"
    # order of the handles does not matter
    assert np.array_equal(single, cm.wedge_detector(SHAPE, B0, p2, p1, mirrored=False).astype(bool))


def test_polygon_and_invert():
    m = cm.polygon_detector(SHAPE, [(2, 2), (10, 2), (10, 8), (2, 8)]).astype(bool)
    assert m[5, 5] and not m[15, 20]
    w = np.array([[0.0, 0.5], [1.0, 0.25]])
    assert np.allclose(cm.invert_mask(w), 1.0 - w)
    assert np.allclose(cm.invert_mask(2 * w), 2 - 2 * w), "inversion is max - mask, as in MATLAB"


def test_combine_masks_modes():
    a, b = _disc((5, 5), 3).astype(float), _disc((7, 5), 3).astype(float)
    assert np.array_equal(cm.combine_masks([a, b], [1, 1], "Union").astype(bool), (a + b) > 0)
    assert np.array_equal(cm.combine_masks([a, b], [1, 1], "Color Mix").astype(bool), (a + b) > 0)
    assert np.array_equal(cm.combine_masks([a, b], [1, 1], "Intersection").astype(bool), (a * b) > 0)
    assert np.allclose(cm.combine_masks([a, b], [2, -1], "Additive"), 2 * a - b)
    assert np.allclose(cm.combine_masks([a, b], [1, 3], "Current-only", ids=["A", "B"], current="B"), 3 * b)
    assert not cm.combine_masks([a, b], [1, 1], "Current-only", ids=["A", "B"], current=None, shape=SHAPE).any()


def test_color_mix():
    rng = np.random.default_rng(3)
    data = rng.random((6, NY * NX))
    a, b = _disc((5, 5), 3).astype(float), _disc((20, 12), 4).astype(float)
    colors = [(1, 0, 0), (0, 0, 1)]
    rgb_mask, rgb_real = cm.color_mix(data, [a, b], [1, 0.5], colors)
    assert rgb_mask.shape == (NY, NX, 3) and rgb_real.shape == (6, 3)
    assert np.allclose(rgb_mask[..., 0], a) and np.allclose(rgb_mask[..., 2], 0.5 * b)
    raw = np.stack([data @ a.ravel(), np.zeros(6), data @ (0.5 * b).ravel()], axis=1)
    assert np.allclose(rgb_real, (raw - raw.min()) / (raw.max() - raw.min()))


# ---------------------------------------------------------------------------
# mask_math.py  (MATLAB semantics; masks are given in Python (y, x) layout)
# ---------------------------------------------------------------------------
@pytest.fixture
def masks():
    rng = np.random.default_rng(1)
    return {"A": (rng.random(SHAPE) > 0.5).astype(float),
            "B": (rng.random(SHAPE) > 0.5).astype(float),
            "AB": rng.random(SHAPE)}


def test_mask_ids():
    assert mask_ids("A & (B | AB)") == ["A", "B", "AB"]
    assert mask_ids("max(A, 0.5*B) + pi") == ["A", "B"]


@pytest.mark.parametrize("formula, expect", [
    ("A & (B | AB)", lambda m: (m["A"] > 0) & ((m["B"] > 0) | (m["AB"] > 0))),
    ("~A", lambda m: m["A"] == 0),
    ("A .* B + 2", lambda m: m["A"] * m["B"] + 2),
    ("A.^2 - B ./ 2", lambda m: m["A"] ** 2 - m["B"] / 2),
    ("max(A, 0.5*AB)", lambda m: np.maximum(m["A"], 0.5 * m["AB"])),
    ("AB > 0.5", lambda m: m["AB"] > 0.5),
    ("1", lambda m: np.ones(SHAPE)),
    ("-2^2 + 0*A", lambda m: np.full(SHAPE, -4.0)),
    ("xor(A, B)", lambda m: (m["A"] > 0) ^ (m["B"] > 0)),
])
def test_elementwise(masks, formula, expect):
    assert np.allclose(evaluate_mask_formula(formula, masks, SHAPE), expect(masks))


def test_matlab_orientation(masks):
    """MATLAB arrays are X-by-Y: A(i, :) is the column x = i-1, and fliplr flips y."""
    a = masks["A"]
    out = evaluate_mask_formula("fliplr(A)", masks, SHAPE)
    assert np.allclose(out, a[::-1, :])
    out = evaluate_mask_formula("flipud(A)", masks, SHAPE)
    assert np.allclose(out, a[:, ::-1])
    out = evaluate_mask_formula("[A(1:3, :) ; 0*A(4:end, :)]", masks, SHAPE)
    expected = a.copy()
    expected[:, 3:] = 0
    assert np.allclose(out, expected)
    assert np.allclose(evaluate_mask_formula("A(end, end) + 0*A", masks, SHAPE), a[-1, -1])


def test_transpose_requires_square(masks):
    with pytest.raises(MaskMathError):
        evaluate_mask_formula("A'", masks, SHAPE)      # 30x20 transposed is 20x30: size mismatch


@pytest.mark.parametrize("formula", ["C + 1", "A(100, 1)", "A +", "A(1:2, :)", "sqrt(-A - 1)", "eval('1')"])
def test_errors(masks, formula):
    with pytest.raises(MaskMathError):
        evaluate_mask_formula(formula, masks, SHAPE)


def test_round_half_away_from_zero(masks):
    out = evaluate_mask_formula("round(2.5) + round(-0.5) + 0*A", masks, SHAPE)
    assert np.allclose(out, 3 - 1)


def test_math_gpu_free_and_no_eval(masks):
    """The evaluator never touches Python eval: attribute access and builtins are syntax errors."""
    for formula in ("__import__('os')", "A.__class__", "open('x')"):
        with pytest.raises(MaskMathError):
            evaluate_mask_formula(formula, masks, SHAPE)
