"""Unit tests for callbacks.io.export — no Qt."""
import os
import re

import numpy as np
import pytest
from PIL import Image

from pyquant4d.callbacks.io import export as ex
from pyquant4d.callbacks.io.export import Region

NFX, NFY, NPX, NPY = 5, 3, 12, 8
SCAN, DET = (NFX, NFY), (NPX, NPY)


@pytest.fixture()
def cube():
    return np.arange(NFY * NFX * NPY * NPX, dtype=np.uint16).reshape(NFY, NFX, NPY, NPX)


@pytest.fixture()
def data(cube):
    return cube.reshape(NFY * NFX, NPY * NPX)


def _export_all(data, frames, pixels):
    return np.concatenate(list(ex.iter_exported_frames(data, SCAN, DET, frames, pixels)))


# ------------------------------------------------------------------- regions
def test_full_region_round_trips(data, cube):
    got = _export_all(data, ex.full_region(SCAN), ex.full_region(DET))
    assert got.dtype == data.dtype
    np.testing.assert_array_equal(got.reshape(cube.shape), cube)


def test_sampling_and_binning(data, cube):
    frames, pixels = Region((1, 0), (2, 2), 2), Region((2, 1), (3, 2), 3)
    ref = cube[0:3:2, 1:4:2, 1:7, 2:11].reshape(2, 2, 2, 3, 3, 3).sum(axis=(3, 5))
    got = _export_all(data, frames, pixels)
    assert got.dtype == np.uint32, "binned integer data should be widened"
    np.testing.assert_array_equal(got.reshape(ref.shape), ref)
    assert ex.exported_shape(frames, pixels) == ref.shape


@pytest.mark.parametrize("dtype, binned, expected", [
    (np.float32, True, np.float32), (np.uint16, False, np.uint16), (np.uint8, True, np.uint32),
    (np.int16, True, np.int32), (np.uint64, True, np.uint64), (np.float64, True, np.float64),
])
def test_exported_dtype(dtype, binned, expected):
    assert ex.exported_dtype(dtype, Region((0, 0), (1, 1), 2 if binned else 1)) == np.dtype(expected)


def test_binning_cannot_overflow():
    d = np.full((1, 4), 255, dtype=np.uint8)
    got = _export_all_2x2(d)
    assert got.item() == 4 * 255


def _export_all_2x2(d):
    return np.concatenate(list(ex.iter_exported_frames(d, (1, 1), (2, 2), ex.full_region((1, 1)), Region((0, 0), (1, 1), 2))))


def test_region_check_accepts_exact_fits():
    Region((0, 0), (3, 1), 2).check(SCAN, binned=False)     # positions 0, 2, 4 of a 5-wide scan
    Region((0, 0), (6, 4), 2).check(DET, binned=True)       # 12 x 8 pixels in 2 x 2 bins


@pytest.mark.parametrize("region, binned", [
    (Region((4, 0), (2, 1), 1), False),      # runs past the last frame
    (Region((1, 0), (3, 1), 2), False),      # positions 1, 3, 5: 5 is past the end
    (Region((10, 0), (2, 1), 2), True),      # binned block reaches beyond x = 11
    (Region((0, 0), (0, 1), 1), True),       # empty
    (Region((-1, 0), (1, 1), 1), True),      # negative start
])
def test_region_check_rejects(region, binned):
    with pytest.raises(ValueError):
        region.check(DET if binned else SCAN, binned)


def test_blocks_stay_within_chunk_limit(data, monkeypatch):
    monkeypatch.setattr(ex, "CHUNK_BYTES", 1)
    blocks = list(ex.iter_exported_frames(data, SCAN, DET, ex.full_region(SCAN), ex.full_region(DET)))
    assert all(b.shape[0] == 1 for b in blocks) and len(blocks) == NFX * NFY


# ------------------------------------------------------------------- writers
@pytest.mark.parametrize("order, code", [("l", "<"), ("b", ">")])
def test_write_raw_byte_order(tmp_path, data, cube, order, code):
    path = str(tmp_path / "x.raw")
    shape = ex.write_raw(path, data, SCAN, DET, ex.full_region(SCAN), ex.full_region(DET), order)
    assert shape == cube.shape
    np.testing.assert_array_equal(np.fromfile(path, dtype=code + "u2").reshape(shape), cube)
    assert not os.path.exists(path + ".part")


def test_write_raw_rejects_bad_byte_order(tmp_path, data):
    with pytest.raises(ValueError):
        ex.write_raw(str(tmp_path / "x.raw"), data, SCAN, DET, ex.full_region(SCAN), ex.full_region(DET), "x")


def test_write_hdf5_is_contiguous_with_metadata(tmp_path, data, cube):
    h5py = pytest.importorskip("h5py")
    path = str(tmp_path / "x.h5")
    frames, pixels = Region((0, 0), (3, 2), 2), ex.full_region(DET)
    ex.write_hdf5(path, data, SCAN, DET, frames, pixels, "b", {"beam_center_xy": np.array([5.5, 3.0]), "skip": None})
    with h5py.File(path) as f:
        d = f["data"]
        assert d.shape == (2, 3, NPY, NPX) and d.dtype.str == ">u2"
        assert d.chunks is None and d.compression is None and d.id.get_offset() > 0
        np.testing.assert_array_equal(d[()], cube[0:3:2, 0:5:2])
        assert d.attrs["axes"] == "ry, rx, py, px"
        assert list(f["metadata"].attrs) == ["beam_center_xy"]


def test_write_hdf5_offset_reads_back_as_raw(tmp_path, data, cube):
    """pyQuant4D imports HDF5 by offset, so the bytes must be a plain C-order array."""
    h5py = pytest.importorskip("h5py")
    path = str(tmp_path / "x.h5")
    ex.write_hdf5(path, data, SCAN, DET, ex.full_region(SCAN), ex.full_region(DET))
    with h5py.File(path) as f:
        offset = f["data"].id.get_offset()
    raw = np.fromfile(path, dtype="<u2", count=cube.size, offset=offset)
    np.testing.assert_array_equal(raw.reshape(cube.shape), cube)


def test_dims_suffix_is_what_the_importer_reads():
    frames, pixels = Region((0, 0), (64, 32), 1), Region((0, 0), (128, 96), 1)
    suffix = ex.dims_suffix(frames, pixels)
    m = re.search(r'(\d+)x(\d+)x(\d+)x(\d+)', "scan" + suffix + ".raw")     # pattern used by import_io
    assert tuple(int(v) for v in m.groups()) == (128, 96, 64, 32)          # NPxX, NPxY, NFrX, NFrY


# -------------------------------------------------------------------- images
def test_save_tiff_is_float32_and_exact(tmp_path):
    im = np.random.default_rng(0).normal(size=(7, 11)) * 1e6
    path = str(tmp_path / "x.tif")
    ex.save_tiff(path, im)
    back = np.array(Image.open(path))
    assert back.dtype == np.float32 and back.shape == (7, 11)
    np.testing.assert_array_equal(back, im.astype(np.float32))
    with pytest.raises(ValueError):
        ex.save_tiff(path, np.zeros((2, 2, 2)))


def test_rgb_as_displayed_applies_cmap_limits_and_alpha(mpl_fig_ax, tmp_path):
    fig, ax = mpl_fig_ax
    img = ax.imshow(np.array([[0.0, 0.5], [1.0, 2.0]]), cmap="gray")
    img.set_clim(0, 1)
    img.set_alpha(np.array([[1.0, 1.0], [0.5, 1.0]]))
    rgb = ex.rgb_as_displayed(img)
    assert rgb.shape == (2, 2, 3) and rgb.dtype == np.uint8
    assert tuple(rgb[0, 0]) == (0, 0, 0)
    assert abs(int(rgb[0, 1, 0]) - 128) <= 1
    assert abs(int(rgb[1, 0, 0]) - 128) <= 1            # white at half opacity over black
    assert tuple(rgb[1, 1]) == (255, 255, 255)          # clipped at the upper limit
    path = str(tmp_path / "x.png")
    ex.save_png(path, rgb)
    np.testing.assert_array_equal(np.array(Image.open(path)), rgb)
