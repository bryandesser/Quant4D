"""Notebook round trip: pyquant4d.show(copy=...) and the results methods of the window
(callbacks.results), in py4DSTEM's conventions."""
import numpy as np
import pytest

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, set_mode, wait_until

try:
    import py4DSTEM
except ImportError:          # optional dependency
    py4DSTEM = None
needs_py4dstem = pytest.mark.skipif(py4DSTEM is None, reason="py4DSTEM not installed")


def _cube(synthetic_data):
    return synthetic_data.reshape(SCAN_Y, SCAN_X, DET_Y, DET_X).astype(np.float32).copy()


def _load(app, qapp, data, **kw):
    from pyquant4d.callbacks.py4dstem_bridge import loadDataCube
    loadDataCube(app, data, **kw)
    assert wait_until(qapp, lambda: app.Data is not None and app.Fig.Dfrn.Image is not None)
    qapp.processEvents()


# ---------------------------------------------------------------------- copy or share
class TestCopy:
    def test_copy_by_default(self, app, qapp, synthetic_data):
        arr = _cube(synthetic_data)
        _load(app, qapp, arr)
        assert not np.shares_memory(app.Data, arr) and not app._sharedData

    def test_shared_then_copied_before_changing(self, app, qapp, synthetic_data):
        from pyquant4d.callbacks.datasetOptCallbacks import swapByteOrder
        arr = _cube(synthetic_data)
        before = arr.copy()
        _load(app, qapp, arr, copy=False)
        assert np.shares_memory(app.Data, arr) and app._sharedData
        assert swapByteOrder(app, update=False)
        assert not np.shares_memory(app.Data, arr) and not app._sharedData
        np.testing.assert_array_equal(arr, before)                   # the caller's array untouched
        assert not np.array_equal(app.Data, before.reshape(app.Data.shape))

    def test_nan_zeroing_copies_first(self, app, qapp, synthetic_data):
        from pyquant4d.callbacks.py4dstem_bridge import ownData
        arr = _cube(synthetic_data)
        arr[0, 0, 0, 0] = np.nan
        _load(app, qapp, arr, copy=False)
        ownData(app)                         # what Set NaNs to 0 does before writing
        app.Data[np.ma.masked_invalid(app.Data).mask] = 0
        assert np.isnan(arr[0, 0, 0, 0])

    def test_unload_resets(self, app, qapp, synthetic_data):
        from pyquant4d.callbacks.import_io import unloadData
        _load(app, qapp, _cube(synthetic_data), copy=False)
        unloadData(app)
        assert not app._sharedData

    def test_show_passes_copy(self, qapp, synthetic_data):
        import pyquant4d
        arr = _cube(synthetic_data)
        win = pyquant4d.show(arr, block=False, copy=False)
        try:
            assert wait_until(qapp, lambda: win.Data is not None)
            assert np.shares_memory(win.Data, arr)
        finally:
            win.close()
            qapp.processEvents()


# ---------------------------------------------------------------------- results
@pytest.fixture()
def aligned(app, qapp, synthetic_data):
    _load(app, qapp, _cube(synthetic_data))
    for box, v in ((app.TBX, 13.0), (app.TBY, 9.0)):
        box.setValue(v)
    app.TBR.setValue(4.0)
    app.Alpha.setValue(10.0)
    qapp.processEvents()
    set_mode(app, qapp, "AnnMod")           # leaving Alignment marks the beam as set
    return app


class TestResults:
    def test_calibration_in_py4dstem_order(self, aligned):
        cal = aligned.calibration()
        assert (cal["qx0_mean"], cal["qy0_mean"]) == pytest.approx((9.0, 13.0))   # (row, column) = (y, x)
        assert cal["probe_semiangle"] == pytest.approx(4.0)                        # pixels, as py4DSTEM
        assert cal["convergence_semiangle_mrad"] == pytest.approx(10.0)
        assert cal["Q_pixel_size"] == pytest.approx(2.5, abs=0.01) and cal["Q_pixel_units"] == "mrad"
        assert (cal["R_pixel_size"], cal["R_pixel_units"]) == (1.0, "pixels")
        assert cal["aligned"] and cal["shape"] == (SCAN_Y, SCAN_X, DET_Y, DET_X)

    def test_scan_step_reported(self, aligned):
        aligned.D.ScanStep, aligned.D.ScanUnits = 0.5, "nm"
        cal = aligned.calibration()
        assert (cal["R_pixel_size"], cal["R_pixel_units"]) == (0.5, "nm")

    def test_images_and_masks(self, aligned, qapp):
        assert "Real" in aligned.images() and "Dfrn" in aligned.images()
        real = aligned.image("Real")
        assert real.shape == (SCAN_Y, SCAN_X)                        # (Rx, Ry)
        np.testing.assert_array_equal(real, aligned.Fig.Real.Image)
        real[:] = -1                                                 # a copy: pyQuant4D's is untouched
        assert not np.array_equal(real, aligned.Fig.Real.Image)
        assert aligned.image("real-space").shape == real.shape       # by window name too
        assert aligned.image("Dfrn").shape == (DET_Y, DET_X)        # (Qx, Qy)
        det = aligned.mask()
        assert det.shape == (DET_Y, DET_X) and np.array_equal(det, aligned.Fig.DfrnMask.Image)
        # the real-space image is the data weighted by that detector
        expected = (aligned.Data @ det.ravel()).reshape(SCAN_Y, SCAN_X)
        np.testing.assert_allclose(aligned.image("Real"), expected, rtol=1e-4)
        assert aligned.mask("roi").shape == (SCAN_Y, SCAN_X)

    def test_errors_name_what_exists(self, aligned):
        with pytest.raises(KeyError, match="Real"):
            aligned.image("nope")
        with pytest.raises(KeyError, match="custom detectors"):
            aligned.mask("Z")

    def test_custom_detector_mask(self, aligned, qapp):
        set_mode(aligned, qapp, "CustMod")
        aligned.CDNewCircle.click()
        qapp.processEvents()
        cmask = list(aligned.A.Custom.values())[-1]
        np.testing.assert_array_equal(aligned.mask(cmask.id), cmask.mask)
        aligned.CDDelMask.click()
        set_mode(aligned, qapp, "AnnMod")

    def test_nothing_loaded(self, app):
        with pytest.raises(RuntimeError, match="no dataset"):
            app.calibration()


@needs_py4dstem
class TestApplyCalibration:
    def test_round_trip(self, aligned, synthetic_data):
        dc = py4DSTEM.DataCube(_cube(synthetic_data))
        aligned.D.ScanStep, aligned.D.ScanUnits = 2.0, "A"
        aligned.apply_calibration(dc)
        c = dc.calibration
        assert c.get_origin_mean() == pytest.approx((9.0, 13.0))
        assert np.asarray(c.get_qx0()).shape == (SCAN_Y, SCAN_X)
        assert c.get_probe_semiangle() == pytest.approx(4.0)
        assert c.get_convergence_semiangle_mrad() == pytest.approx(10.0)
        assert c.get_Q_pixel_size() == pytest.approx(2.5, abs=0.01) and c.get_Q_pixel_units() == "mrad"
        assert (c.get_R_pixel_size(), c.get_R_pixel_units()) == (2.0, "A")
        # and back: the bridge reads it as pyQuant4D wrote it
        from pyquant4d.callbacks.py4dstem_bridge import calibrationFromPy4DSTEM
        cal = calibrationFromPy4DSTEM(dc)
        assert cal.beam_xy == pytest.approx((13.0, 9.0)) and cal.probe_radius_px == pytest.approx(4.0)

    def test_descan_maps_keep_their_shape(self, aligned, synthetic_data):
        dc = py4DSTEM.DataCube(_cube(synthetic_data))
        qx0 = 5.0 + np.arange(SCAN_Y * SCAN_X, dtype=float).reshape(SCAN_Y, SCAN_X) * 0.01
        dc.calibration.set_origin((qx0, np.full((SCAN_Y, SCAN_X), 3.0)))
        aligned.apply_calibration(dc, scan_step=False)
        new = np.asarray(dc.calibration.get_qx0())
        assert new.mean() == pytest.approx(9.0)
        np.testing.assert_allclose(new - new.mean(), qx0 - qx0.mean())
        assert dc.calibration.get_R_pixel_units() != "A"

    def test_shape_must_match(self, aligned, synthetic_data):
        small = py4DSTEM.DataCube(_cube(synthetic_data)[:, :, ::2, ::2].copy())
        with pytest.raises(ValueError, match="shape"):
            aligned.apply_calibration(small)

    def test_warns_before_alignment(self, app, qapp, synthetic_data):
        _load(app, qapp, _cube(synthetic_data))
        app.P.TransBeamInit = 0
        with pytest.warns(UserWarning, match="aligned"):
            app.apply_calibration(py4DSTEM.DataCube(_cube(synthetic_data)))
