"""
Unit tests for callbacks.layout — the canonical (ry, rx, py, px) convention.

Every test uses a deliberately non-square scan *and* a non-square detector
with an off-diagonal beam centre, so that any x/y transposition changes the
answer instead of hiding behind symmetry.
"""
import pathlib
import re
from types import SimpleNamespace

import numpy as np
import pytest

from quant4d.callbacks.layout import (
    as_4d, check_layout, dfrn_grids, dfrn_shape, ensure_c_contiguous, real_shape,
)

NFRX, NFRY, NPXX, NPXY = 5, 3, 12, 8


@pytest.fixture()
def D():
    return SimpleNamespace(NFrX=NFRX, NFrY=NFRY, NPxX=NPXX, NPxY=NPXY)


@pytest.fixture()
def spots(D):
    """One hot pixel per frame, written in file order (rx fast, then px fast).

    Frame (ry, rx) has its spot at px = 2 + rx, py = 1 + ry.
    """
    data = np.zeros((NFRY * NFRX, NPXY * NPXX), dtype=np.float32)
    for ry in range(NFRY):
        for rx in range(NFRX):
            data[ry * NFRX + rx, (1 + ry) * NPXX + (2 + rx)] = 1.0
    return data


def test_shapes(D):
    assert real_shape(D) == (NFRY, NFRX)
    assert dfrn_shape(D) == (NPXY, NPXX)


def test_grids_are_row_col(D):
    xx, yy = dfrn_grids(D, origin=(4, 2))
    assert xx.shape == yy.shape == (NPXY, NPXX)
    assert xx[0, 7] == 3 and yy[0, 7] == -2
    assert xx[5, 0] == -4 and yy[5, 0] == 3


def test_as_4d_is_a_view_in_raster_order(D, spots):
    cube = as_4d(spots, D)
    assert cube.shape == (NFRY, NFRX, NPXY, NPXX)
    assert np.shares_memory(cube, spots)
    assert cube[2, 4, 3, 6] == 1.0          # ry=2, rx=4 -> py=3, px=6
    assert cube[2, 4].sum() == 1.0


def test_check_layout_rejects_wrong_shape(D, spots):
    with pytest.raises(ValueError, match="expected"):
        check_layout(spots.T, D)


def test_com_weights_follow_display_axes(D, spots):
    """CoM-X must track the spot's column (px) and CoM-Y its row (py)."""
    xx, yy = dfrn_grids(D)
    com_x = (spots @ xx.ravel()).reshape(real_shape(D))
    com_y = (spots @ yy.ravel()).reshape(real_shape(D))
    ry, rx = np.mgrid[0:NFRY, 0:NFRX]
    np.testing.assert_array_equal(com_x, 2 + rx)
    np.testing.assert_array_equal(com_y, 1 + ry)


def test_matlab_style_grid_is_wrong(D, spots):
    """Guard: the column-major construction the port used to use disagrees."""
    xg, _ = np.mgrid[0:NPXX, 0:NPXY]
    com_x_old = (spots @ xg.flatten()).reshape(real_shape(D))
    _, rx = np.mgrid[0:NFRY, 0:NFRX]
    assert not np.array_equal(com_x_old, 2 + rx)


def test_radial_mask_is_centred_on_beam(D, spots):
    """A small disc about (x, y) = (4, 2) selects only the frame whose spot is there."""
    xx, yy = dfrn_grids(D, origin=(4, 2))
    mask = np.hypot(xx, yy) < 0.5
    bf = spots[:, mask.ravel()].sum(axis=1).reshape(real_shape(D))
    expected = np.zeros(real_shape(D))
    expected[1, 2] = 1.0                    # ry=1 -> py=2, rx=2 -> px=4
    np.testing.assert_array_equal(bf, expected)


def test_pacbed_reshape(D, spots):
    pacbed = spots.sum(axis=0).reshape(dfrn_shape(D))
    assert pacbed[1:1 + NFRY, 2:2 + NFRX].sum() == NFRX * NFRY


def test_ensure_c_contiguous():
    a = np.arange(12.0).reshape(3, 4)
    assert ensure_c_contiguous(a) is a
    f = np.asfortranarray(a)
    c = ensure_c_contiguous(f)
    assert c.flags["C_CONTIGUOUS"] and np.array_equal(c, a)


# ---------------------------------------------------------------------------
# Source guard: hand-rolled (x, y) grids / NPx-as-shape must not come back
# ---------------------------------------------------------------------------
_SRC = pathlib.Path(__file__).resolve().parents[2] / "src" / "quant4d" / "callbacks"
_BAD = [
    r"np\.(mgrid|ogrid)\[[^\]]*NPxX[^\]]*NPxY",   # (x, y)-ordered pixel grid
    r"reshape\(\s*self\.D\.NPx\s*\)",             # NPx is (x, y), not a shape
    r"np\.(ones|zeros)\(\s*self\.D\.NPx\b",
]


@pytest.mark.parametrize("pattern", _BAD)
def test_no_transposed_layout_idioms(pattern):
    assert _SRC.is_dir(), _SRC                     # (a moved package would make this pass vacuously)
    hits = [
        f"{p.name}:{i}"
        for p in _SRC.rglob("*.py") if p.name != "layout.py"   # its docstring quotes the idiom
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1)
        if re.search(pattern, line) and not line.lstrip().startswith("#")
    ]
    assert not hits, hits
