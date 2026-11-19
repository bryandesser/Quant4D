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


# ---------------------------------------------------------------------------
# Using a file's calibration (import)
# ---------------------------------------------------------------------------
def test_usable_calibration_keeps_mrad_drops_other_units():
    from callbacks.io.emd import usable_calibration
    mrad = usable_calibration(EmdCalibration(beam_xy=BEAM_XY, q_pixel_size=0.5, q_units="mrad"))
    assert (mrad.q_pixel_size, mrad.q_units, mrad.beam_xy) == (0.5, "mrad", BEAM_XY)
    inv_a = usable_calibration(EmdCalibration(beam_xy=BEAM_XY, q_pixel_size=0.01, q_units="A^-1",
                                              probe_semiangle_mrad=20.0))
    assert (inv_a.q_pixel_size, inv_a.q_units, inv_a.probe_semiangle_mrad) == (1.0, "pixels", 20.0)
    assert usable_calibration(EmdCalibration()) is None                        # nothing to use
    assert usable_calibration(EmdCalibration(q_units="A^-1", q_pixel_size=0.01, probe_semiangle_mrad=0)) is None


def test_calibration_for_region_crops_and_bins():
    from callbacks.io.emd import calibration_for_region
    cal = EmdCalibration(beam_xy=(10.0, 7.0), q_pixel_size=0.5, q_units="mrad", probe_semiangle_mrad=20.0)
    assert calibration_for_region(cal, (0, 0), 1) == cal
    out = calibration_for_region(cal, (2, 1), 2)
    assert out.beam_xy == pytest.approx(((10 - 2 + 0.5) / 2 - 0.5, (7 - 1 + 0.5) / 2 - 0.5))
    assert out.q_pixel_size == 1.0 and out.probe_semiangle_mrad == 20.0
    # binning a 2x2 block whose centre is the beam keeps the beam at that block's centre
    assert calibration_for_region(EmdCalibration(beam_xy=(4.5, 4.5)), (0, 0), 2).beam_xy == (2.0, 2.0)


def test_describe_emd(tmp_path):
    from callbacks.io.emd import EmdInfo, describe_emd
    cal = EmdCalibration(beam_xy=BEAM_XY, q_pixel_size=0.5, q_units="mrad", probe_semiangle_mrad=21.4)
    path, _ = _write(tmp_path, calibration=cal, images={"ADF": EmdImage(np.ones((NFY, NFX)))})
    text = describe_emd(read_emd_info(path))
    assert "Beam centre (x, y) = (2.00, 4.00)" in text and "0.5 mrad/px" in text
    assert "21.4 mrad" in text and "Images: ADF" in text and "applied" in text
    assert "moves" not in text                                                  # constant origin maps
    other = describe_emd(EmdInfo("/d", (1, 1, 1, 1), np.dtype("f4"),
                                 EmdCalibration(q_pixel_size=0.01, q_units="A^-1"), origin_spread_px=1.5))
    assert "not used" in other and "applied" not in other


@needs_py4dstem
def test_reads_a_file_py4dstem_wrote(tmp_path):
    """Our reader on py4DSTEM's own output: origin swapped back to (x, y), varying origin reported."""
    _, full = _dataset()
    dc = py4DSTEM.DataCube(full)
    dc.calibration.set_Q_pixel_size(0.25)
    dc.calibration.set_Q_pixel_units("mrad")
    dc.calibration.set_probe_semiangle(18.0)
    qx0 = np.full((NFY, NFX), 4.0)
    qx0[0, 0] = 4.5                                     # the origin moves (descan)
    dc.calibration.set_origin((qx0, np.full((NFY, NFX), 2.0)))
    path = str(tmp_path / "p4d.h5")
    py4DSTEM.save(path, dc, mode="o")
    info = read_emd_info(path)
    assert info is not None and info.shape == (NFY, NFX, NPY, NPX)
    assert info.calibration.beam_xy == pytest.approx((2.0, float(qx0.mean())))   # (x, y) = (qy0, qx0)
    assert info.calibration.q_pixel_size == 0.25 and info.calibration.q_units == "mrad"
    assert info.calibration.probe_semiangle_mrad == pytest.approx(18.0)
    assert info.origin_spread_px == pytest.approx(0.5)


def test_swapping_detector_xy_swaps_the_file_beam():
    """Settings > Misc 'swap diffraction X/Y' re-aligns from the file calibration: its beam must swap too."""
    from callbacks.appClass import D
    d = D(Calib=EmdCalibration(beam_xy=(1.0, 2.0), q_pixel_size=0.5, q_units="mrad"))
    d.swapDiff()
    assert d.Calib.beam_xy == (2.0, 1.0) and d.Calib.q_pixel_size == 0.5
    D().swapDiff()                                     # no calibration: nothing to swap
