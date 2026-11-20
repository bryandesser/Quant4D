"""Unit tests for callbacks.io.dm_header and callbacks.io.raw — no Qt.

DM files are generated here by a small writer that follows the published tag
layout, so the reader is checked against files whose contents are known
exactly, in both DM3 and DM4 flavours and both byte orders.
"""
import struct

import numpy as np
import pytest

from pyquant4d.callbacks.io.dm_header import read_dm_header
from pyquant4d.callbacks.io.export import Region
from pyquant4d.callbacks.io.raw import float_type_for, frame_record_dtype, open_frames, read_frames

from dm_writer import _DMWriter  # noqa: E402  (tests/dm_writer.py, shared with the integration tests)


@pytest.mark.parametrize("version", [3, 4])
@pytest.mark.parametrize("little", [True, False])
def test_dm_header_finds_images_offsets_and_dims(tmp_path, version, little):
    rng = np.random.default_rng(version)
    thumb = rng.integers(0, 255, (6, 5)).astype("u2")
    cube = rng.random((3, 4, 7, 9)).astype("f4")          # (ry, rx, ky, kx)
    path = tmp_path / f"x.dm{version}"
    path.write_bytes(_DMWriter(version, little).file([("thumb", thumb, "u2"), ("Diffraction SI", cube, "f4")]))

    info = read_dm_header(str(path))
    assert (info.version, info.little_endian) == (version, little)
    assert [im.name for im in info.images] == ["thumb", "Diffraction SI"]
    big = info.largest()
    assert big.name == "Diffraction SI" and big.dims == (9, 7, 4, 3) and big.dtype == "f4"
    order = "<" if little else ">"
    on_disk = np.fromfile(path, dtype=order + "f4", count=cube.size, offset=big.offset)
    np.testing.assert_array_equal(on_disk.reshape(cube.shape), cube)
    small = info.images[0]
    assert small.dims == (5, 6) and small.dtype == "u2"
    np.testing.assert_array_equal(np.fromfile(path, dtype=order + "u2", count=30, offset=small.offset).reshape(6, 5), thumb)


@pytest.mark.parametrize("version", [3, 4])
@pytest.mark.parametrize("little", [True, False])
def test_dm_header_reads_calibrations_and_voltage(tmp_path, version, little):
    cube = np.zeros((3, 4, 7, 9), "f4")
    cals = [(0.57, "mrad", 4.0), (0.57, "mrad", 3.0), (0.023, "nm", 0.0), (0.023, "nm", 0.0)]
    path = tmp_path / f"cal.dm{version}"
    path.write_bytes(_DMWriter(version, little).file([("thumb", np.zeros((2, 2), "u2"), "u2"),
                                                      ("SI", cube, "f4", cals, 300000.0)]))
    thumb, si = read_dm_header(str(path)).images
    assert [(pytest.approx(s), u, o) for s, u, o in si.calibrations] == cals
    assert si.calibration(2) == (pytest.approx(0.023), "nm") and si.calibration(0)[1] == "mrad"
    assert si.voltage_V == 300000.0
    assert thumb.calibrations == () and thumb.calibration(0) is None and thumb.voltage_V is None


def test_dm_uncalibrated_dimension_is_none():
    from pyquant4d.callbacks.io.dm_header import DMImage
    im = DMImage("x", 0, "f4", 2, (2, 2, 2, 2), 16, calibrations=((1.0, "", 0.0),) * 4)
    assert im.calibration(2) is None and im.calibration(7) is None


def test_dm_header_rejects_other_files(tmp_path):
    p = tmp_path / "x.dm4"
    p.write_bytes(struct.pack(">I", 7) + b"\x00" * 64)
    with pytest.raises(ValueError, match="not a DM3/DM4"):
        read_dm_header(str(p))


# ---------------------------------------------------------------------- raw
NFX, NFY, NPX, NPY = 5, 4, 6, 8


@pytest.fixture()
def cube():
    return np.random.default_rng(1).integers(0, 1000, (NFY, NFX, NPY, NPX)).astype(np.uint16)


def _write(path, cube, order="<", header=0, footer=0, offset=0):
    with open(path, "wb") as fh:
        fh.write(b"\xab" * offset)
        for frame in cube.reshape(-1, NPY * NPX):
            fh.write(b"\x11" * header + frame.astype(order + "u2").tobytes() + b"\x22" * footer)


@pytest.mark.parametrize("order, flag", [("<", "l"), (">", "b")])
def test_open_frames_with_header_footer_and_offset(tmp_path, cube, order, flag):
    p = str(tmp_path / "x.raw")
    _write(p, cube, order, header=3, footer=5, offset=17)
    frames = open_frames(p, 17, NFX * NFY, NPX * NPY, "u2", 3, 5, flag)
    assert frames.shape == (NFX * NFY, NPX * NPY)
    np.testing.assert_array_equal(np.asarray(frames).reshape(cube.shape), cube)
    assert frame_record_dtype("u2", 4, 3, 5, flag).itemsize == 16


def test_read_frames_full_converts_to_native_float(tmp_path, cube):
    p = str(tmp_path / "x.raw")
    _write(p, cube, ">")
    out = read_frames(open_frames(p, 0, NFX * NFY, NPX * NPY, "u2", byte_order="b"), (NFX, NFY), (NPX, NPY))
    assert out.dtype == np.float32 and out.dtype.isnative
    np.testing.assert_array_equal(out.reshape(cube.shape), cube)


def test_read_frames_crop_bin_sample(tmp_path, cube):
    p = str(tmp_path / "x.raw")
    _write(p, cube, header=2)
    frames, pixels = Region((1, 1), (2, 2), 2), Region((1, 2), (2, 3), 2)
    progress = []
    out = read_frames(open_frames(p, 0, NFX * NFY, NPX * NPY, "u2", header=2), (NFX, NFY), (NPX, NPY),
                      frames, pixels, progress.append)
    ref = cube[1:4:2, 1:4:2, 2:8, 1:5].astype(np.float64).reshape(2, 2, 3, 2, 2, 2).sum(axis=(3, 5))
    np.testing.assert_allclose(out.reshape(ref.shape), ref)
    assert progress and progress[-1] == pytest.approx(1.0)


def test_read_frames_rejects_regions_outside_the_file(tmp_path, cube):
    p = str(tmp_path / "x.raw")
    _write(p, cube)
    with pytest.raises(ValueError):
        read_frames(open_frames(p, 0, NFX * NFY, NPX * NPY, "u2"), (NFX, NFY), (NPX, NPY),
                    Region((3, 0), (2, 1), 2))


def test_float_type():
    assert float_type_for("u2") == np.float32 and float_type_for("f4") == np.float32
    assert float_type_for("u8") == np.float64 and float_type_for("f8") == np.float64


# -------------------------------------------------------------------- EMPAD
from pyquant4d.callbacks.io.empad import detect_empad, scan_from_name  # noqa: E402

_V1, _V2 = 128 * 128 * 4 + 1024, 128 * 128 * 4


@pytest.mark.parametrize("name, size, expected", [
    ("scan_x64_y32.raw", 64 * 32 * _V1, (1, 1024, (64, 32))),                      # v1, EMPAD naming
    ("scan_x64_y32.raw", 64 * 32 * _V2, (2, 0, (64, 32))),                         # v2, same name
    ("a_128x128x16x8.raw", 16 * 8 * _V1, (1, 1024, (16, 8))),                      # v1, AxBxCxD naming
    ("a_128x128x16x8.raw", 16 * 8 * _V2, (2, 0, (16, 8))),                         # v2
    ("noname.raw", 32 * 32 * _V1, (1, 1024, (32, 32))),                            # square scan from size
    ("noname.raw", 32 * 32 * _V2, (2, 0, (32, 32))),
    ("noname.raw", 24 * 12 * _V2, (2, 0, (16, 18))),                               # 288 frames: squarest factors
])
def test_detect_empad(tmp_path, name, size, expected):
    p = tmp_path / name
    p.write_bytes(b"")
    layout = detect_empad(str(p), file_size=size)
    assert (layout.version, layout.footer, layout.scan) == expected


def test_detect_empad_rejects_other_sizes(tmp_path):
    p = tmp_path / "x.raw"
    p.write_bytes(b"")
    assert detect_empad(str(p), file_size=_V2 + 7) is None


def test_scan_from_name():
    assert scan_from_name("/d/EMPAD_Ga2O3_128x128x96x64.raw") == (96, 64)
    assert scan_from_name("scan_x256_y128.raw") == (256, 128)
    assert scan_from_name("scan.raw") is None


def test_empad_v1_and_v2_read_the_same_frames(tmp_path):
    """The footer of v1 must be skipped: both layouts give identical data."""
    frames = np.random.default_rng(2).normal(size=(4, 128 * 128)).astype("<f4")
    v1, v2 = tmp_path / "a_x2_y2.raw", tmp_path / "b_x2_y2.raw"
    with open(v1, "wb") as fh:
        for f in frames:
            fh.write(f.tobytes() + np.full(256, 9e9, "<f4").tobytes())
    frames.tofile(v2)
    out = []
    for p in (v1, v2):
        lay = detect_empad(str(p))
        out.append(read_frames(open_frames(str(p), 0, lay.n_frames, 128 * 128, "f4", 0, lay.footer, "l"), lay.scan, (128, 128)))
    np.testing.assert_array_equal(out[0], frames)
    np.testing.assert_array_equal(out[1], frames)


# --------------------------------------------------------------- mask files
from PIL import Image  # noqa: E402

from pyquant4d.callbacks.io.mask_file import load_mask_image  # noqa: E402


def test_mask_png_scaled_and_kept_as_weights(tmp_path):
    a = np.zeros((3, 5), np.uint8)
    a[1, 2], a[0, 0] = 200, 50
    p = str(tmp_path / "m.png")
    Image.fromarray(a).save(p)
    m, notes = load_mask_image(p, (3, 5))
    np.testing.assert_allclose(m, a / 200.0)
    assert any("scaled" in n for n in notes)


def test_mask_transposed_only_when_shapes_differ(tmp_path):
    a = np.arange(15, dtype=np.uint8).reshape(5, 3)
    p = str(tmp_path / "t.png")
    Image.fromarray(a).save(p)
    m, notes = load_mask_image(p, (3, 5))
    np.testing.assert_allclose(m, a.T / a.max())
    assert any("transposed" in n for n in notes)
    sq = np.triu(np.ones((4, 4), np.uint8))           # square: must never be transposed
    p2 = str(tmp_path / "s.png")
    Image.fromarray(sq).save(p2)
    m2, notes2 = load_mask_image(p2, (4, 4))
    np.testing.assert_array_equal(m2, sq)
    assert notes2 == []


def test_mask_float_tiff_and_npy_keep_values(tmp_path):
    a = np.array([[0.0, 0.5], [np.nan, 2.0]], np.float32)
    p = str(tmp_path / "f.tif")
    Image.fromarray(a, mode="F").save(p)
    m, notes = load_mask_image(p, (2, 2))
    np.testing.assert_allclose(m, [[0, 0.25], [0, 1]])
    assert any("NaN" in n for n in notes)
    q = str(tmp_path / "f.npy")
    np.save(q, np.eye(2))
    np.testing.assert_array_equal(load_mask_image(q, (2, 2))[0], np.eye(2))


@pytest.mark.parametrize("name, shape", [("x.png", (4, 4)), ("x.txt", (3, 5))])
def test_mask_refused(tmp_path, name, shape):
    p = str(tmp_path / name)
    if name.endswith(".png"):
        Image.fromarray(np.zeros((3, 5), np.uint8)).save(p)
    else:
        open(p, "w").close()
    with pytest.raises(ValueError):
        load_mask_image(p, shape)


# ---------------------------------------------------------------------------
# HDF5 through h5py (chunked / compressed datasets have no data offset)
# ---------------------------------------------------------------------------
class TestH5Frames:
    NY, NX, PY, PX = 3, 5, 6, 7

    @pytest.fixture()
    def cube(self):
        return np.arange(self.NY * self.NX * self.PY * self.PX, dtype=np.float32).reshape(
            self.NY, self.NX, self.PY, self.PX)

    def _ds(self, tmp_path, data, **kw):
        h5py = pytest.importorskip("h5py")
        f = h5py.File(tmp_path / "d.h5", "w")
        f.create_dataset("data", data=data, **kw)
        f.close()
        return h5py.File(tmp_path / "d.h5", "r")["data"]

    def test_dims4(self):
        from pyquant4d.callbacks.io.hdf5 import dims4
        assert dims4((2, 3, 4, 5)) == (2, 3, 4, 5)
        assert dims4((12, 4, 5)) == (1, 12, 4, 5)
        assert dims4((4, 5)) == (1, 1, 4, 5)
        with pytest.raises(ValueError):
            dims4((5,))

    @pytest.mark.parametrize("kw", [{}, {"chunks": (1, 2, 6, 7), "compression": "gzip"}])
    def test_4d_indexing(self, tmp_path, cube, kw):
        from pyquant4d.callbacks.io.hdf5 import H5Frames
        frames = H5Frames(self._ds(tmp_path, cube, **kw))
        flat = cube.reshape(self.NY * self.NX, -1)
        assert frames.shape == flat.shape and frames.dtype == np.float32
        assert np.array_equal(frames[7], flat[7])
        assert np.array_equal(frames[2:9:3], flat[2:9:3])
        assert np.array_equal(frames[np.array([5, 7, 9])], flat[[5, 7, 9]])      # one scan row
        assert np.array_equal(frames[np.array([3, 4, 6, 12])], flat[[3, 4, 6, 12]])  # across rows
        frames.close()

    def test_3d_stack(self, tmp_path, cube):
        from pyquant4d.callbacks.io.hdf5 import H5Frames
        stack = cube.reshape(-1, self.PY, self.PX)
        frames = H5Frames(self._ds(tmp_path, stack, chunks=(4, 6, 7), compression="gzip"))
        assert frames.shape == (stack.shape[0], self.PY * self.PX)
        assert np.array_equal(frames[np.array([1, 2, 11])], stack[[1, 2, 11]].reshape(3, -1))

    def test_read_frames_crop_bin_sample(self, tmp_path, cube):
        """The same cropping/binning/sampling as the offset reader."""
        from pyquant4d.callbacks.io.export import Region
        from pyquant4d.callbacks.io.hdf5 import H5Frames
        from pyquant4d.callbacks.io.raw import read_frames
        frames = H5Frames(self._ds(tmp_path, cube, chunks=True, compression="gzip"))
        got = read_frames(frames, (self.NX, self.NY), (self.PX, self.PY),
                          Region((1, 0), (2, 2), 2), Region((1, 2), (3, 2), 2))
        sub = cube[0:3:2, 1:4:2, 2:6, 1:7]
        expected = sub.reshape(2, 2, 2, 2, 3, 2).sum(axis=(3, 5))
        assert np.allclose(got, expected.reshape(4, -1))
