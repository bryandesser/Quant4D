"""py4DSTEM-compatible EMD export/read (callbacks.io.emd).

The py4DSTEM round trips pin the hand-written layout to what py4DSTEM
actually reads; they are skipped when py4DSTEM is not installed.
"""
import h5py
import numpy as np
import pytest

from callbacks.io.emd import EmdCalibration, EmdImage, is_emd, read_emd_info, write_emd
from callbacks.io.export import Region, full_region

try:
    import py4DSTEM
except ImportError:          # optional dependency
    py4DSTEM = None
needs_py4dstem = pytest.mark.skipif(py4DSTEM is None, reason="py4DSTEM not installed")

NFX, NFY, NPX, NPY = 5, 4, 8, 6          # scan (x, y) and detector (x, y), all different
BEAM_XY = (2.0, 4.0)                       # column 2, row 4


def _dataset():
    """Flat (frame, pixel) data with a bright pixel at the beam and a frame-dependent level."""
    d = np.zeros((NFY, NFX, NPY, NPX), np.float32)
    d += np.arange(NFY * NFX, dtype=np.float32).reshape(NFY, NFX, 1, 1)
    d[:, :, int(BEAM_XY[1]), int(BEAM_XY[0])] += 1000
    return d.reshape(NFY * NFX, NPY * NPX), d


def _write(tmp_path, frames=None, pixels=None, **kw):
    flat, _ = _dataset()
    path = str(tmp_path / "out.h5")
    shape = write_emd(path, flat, (NFX, NFY), (NPX, NPY),
                      frames or full_region((NFX, NFY)), pixels or full_region((NPX, NPY)), **kw)
    return path, shape


def test_layout_and_data(tmp_path):
    path, shape = _write(tmp_path)
    assert shape == (NFY, NFX, NPY, NPX)
    _, full = _dataset()
    with h5py.File(path) as f:
        assert f.attrs["emd_group_type"] == "file"
        np.testing.assert_array_equal(f["pyquant4d_root/datacube/data"][()], full)
        assert f["pyquant4d_root/datacube/data"].id.get_offset() is not None   # contiguous: re-importable by offset
    assert is_emd(path)


def test_not_emd(tmp_path):
    plain = tmp_path / "plain.h5"
    with h5py.File(plain, "w") as f:
        f["data"] = np.zeros((2, 2, 2, 2))
    assert not is_emd(str(plain))
    assert read_emd_info(str(plain)) is None
    assert not is_emd(str(tmp_path / "missing.h5"))


def test_read_info_swaps_back_to_xy(tmp_path):
    cal = EmdCalibration(beam_xy=BEAM_XY, q_pixel_size=0.5, q_units="mrad", probe_semiangle_mrad=21.4)
    path, _ = _write(tmp_path, calibration=cal,
                     images={"ADF": EmdImage(np.ones((NFY, NFX)))}, metadata={"software": "pyQuant4D"})
    info = read_emd_info(path)
    assert info.shape == (NFY, NFX, NPY, NPX)
    assert info.calibration.beam_xy == BEAM_XY
    assert (info.calibration.q_pixel_size, info.calibration.q_units) == (0.5, "mrad")
    assert info.calibration.probe_semiangle_mrad == pytest.approx(21.4)
    assert info.images == ["/pyquant4d_root/datacube/ADF"]
    assert info.authoring_program == "pyQuant4D"


def test_partial_binned_export_and_images(tmp_path):
    frames = Region((1, 0), (2, 2), 2)             # x = 1, 3; y = 0, 2
    pixels = Region((0, 0), (4, 3), 2)             # 8 x 6 binned by 2
    real = np.arange(NFY * NFX, dtype=float).reshape(NFY, NFX)
    dfrn = np.ones((NPY, NPX))
    path, shape = _write(tmp_path, frames, pixels,
                         images={"Real": EmdImage(real), "Dfrn": EmdImage(dfrn, "dfrn")})
    assert shape == (2, 2, 3, 4)
    with h5py.File(path) as f:
        np.testing.assert_array_equal(f["pyquant4d_root/datacube/Real/data"][()], real[0:4:2, 1:5:2])
        np.testing.assert_array_equal(f["pyquant4d_root/datacube/Dfrn/data"][()], np.full((3, 4), 4.0))


@needs_py4dstem
def test_py4dstem_reads_datacube_and_calibration(tmp_path):
    cal = EmdCalibration(beam_xy=BEAM_XY, q_pixel_size=0.5, q_units="mrad", probe_semiangle_mrad=21.4)
    path, _ = _write(tmp_path, calibration=cal, metadata={"source_file": "x.raw", "scan_sampling": 1})
    dc = py4DSTEM.read(path)
    assert isinstance(dc, py4DSTEM.DataCube)
    assert dc.data.shape == (NFY, NFX, NPY, NPX)
    c = dc.calibration
    assert c.get_Q_pixel_size() == 0.5 and c.get_Q_pixel_units() == "mrad"
    # py4DSTEM's (qx0, qy0) is (row, column) = pyQuant4D (y, x)
    assert c.get_origin_mean() == (BEAM_XY[1], BEAM_XY[0])
    assert c.get_qx0().shape == (NFY, NFX)
    assert c.get_probe_semiangle() == pytest.approx(21.4)


@needs_py4dstem
def test_py4dstem_centred_detector_lands_on_the_beam(tmp_path):
    """A centred bright-field detector in py4DSTEM must see the beam pyQuant4D set."""
    path, _ = _write(tmp_path, calibration=EmdCalibration(beam_xy=BEAM_XY))
    dc = py4DSTEM.read(path)
    bf = dc.get_virtual_image("circle", ((0, 0), 0.5), centered=True, verbose=False, returncalc=True)
    _, full = _dataset()
    np.testing.assert_allclose(bf.data, full[:, :, int(BEAM_XY[1]), int(BEAM_XY[0])])


@needs_py4dstem
def test_py4dstem_reads_child_images(tmp_path):
    adf = np.random.default_rng(0).random((NFY, NFX))
    path, _ = _write(tmp_path, images={"ADF": EmdImage(adf)})
    dc = py4DSTEM.read(path)
    np.testing.assert_allclose(dc.tree("ADF").data, adf.astype(np.float32))
