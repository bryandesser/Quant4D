"""py4DSTEM-only entry points (callbacks.py4dstem_bridge, pyquant4d.show).

The menu item is hidden without py4DSTEM; arrays load without it.  Tests that
read or build py4DSTEM objects are skipped when py4DSTEM is not installed.
"""
import numpy as np
import pytest

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, wait_until

try:
    import py4DSTEM
except ImportError:          # optional dependency
    py4DSTEM = None
needs_py4dstem = pytest.mark.skipif(py4DSTEM is None, reason="py4DSTEM not installed")


def _cube(synthetic_data):
    return synthetic_data.reshape(SCAN_Y, SCAN_X, DET_Y, DET_X)


def _loaded(win, qapp):
    assert wait_until(qapp, lambda: win.Data is not None and win.Fig.Dfrn.Image is not None)
    qapp.processEvents()
    return win


def _py4dstem_cube(synthetic_data):
    dc = py4DSTEM.DataCube(_cube(synthetic_data).copy())
    c = dc.calibration
    c.set_Q_pixel_size(0.5)
    c.set_Q_pixel_units("mrad")
    c.set_R_pixel_size(2.5)
    c.set_R_pixel_units("A")
    c.set_probe_semiangle(8.0)                       # the disk radius, pixels (get_probe_size)
    c.set_convergence_semiangle_mrad(4.0)
    c.set_origin((np.full((SCAN_Y, SCAN_X), 7.0), np.full((SCAN_Y, SCAN_X), 10.0)))   # (qx0, qy0) = (row, col)
    return dc


class TestMenu:
    def test_visible_with_py4dstem_only(self, app, monkeypatch):
        import importlib.util
        from callbacks.py4dstem_bridge import connectPy4DSTEM
        assert app.actionOpen_with_py4DSTEM.isVisible() == (py4DSTEM is not None)
        assert app.actionOpen_with_py4DSTEM.isEnabled()                 # available before any import
        monkeypatch.setattr(importlib.util, "find_spec", lambda name, *a, **k: None)
        connectPy4DSTEM(app)
        assert not app.actionOpen_with_py4DSTEM.isVisible()

    def test_in_the_file_menu(self, app):
        assert app.actionOpen_with_py4DSTEM in app.menuFile.actions()


class TestLoadArray:
    def test_array_loads_like_an_import(self, app, qapp, synthetic_data):
        from callbacks.py4dstem_bridge import loadDataCube
        loadDataCube(app, _cube(synthetic_data), name="from_array")
        _loaded(app, qapp)
        assert app.Data.shape == (SCAN_X * SCAN_Y, DET_X * DET_Y)
        assert np.allclose(app.Data, synthetic_data)
        assert (app.D.NFrX, app.D.NFrY, app.D.NPxX, app.D.NPxY) == (SCAN_X, SCAN_Y, DET_X, DET_Y)
        assert app.DetrMode.currentData() == "AlignMod" and app.D.Calib is None
        assert app.windowTitle() == "from_array"

    def test_big_endian_and_odd_types(self, app, qapp, synthetic_data):
        from callbacks.py4dstem_bridge import loadDataCube
        loadDataCube(app, _cube(synthetic_data).astype(">f8"))
        _loaded(app, qapp)
        assert app.Data.dtype.isnative and np.allclose(app.Data, synthetic_data)
        loadDataCube(app, _cube(synthetic_data).astype(np.float16))
        _loaded(app, qapp)
        assert app.Data.dtype == np.float32

    def test_not_4d(self, app, synthetic_data):
        from callbacks.py4dstem_bridge import loadDataCube
        with pytest.raises(ValueError):
            loadDataCube(app, synthetic_data)


@needs_py4dstem
class TestPy4DSTEM:
    def test_calibration_swapped_to_xy(self, synthetic_data):
        from callbacks.py4dstem_bridge import calibrationFromPy4DSTEM
        cal = calibrationFromPy4DSTEM(_py4dstem_cube(synthetic_data))
        assert cal.beam_xy == (10.0, 7.0)
        assert (cal.q_pixel_size, cal.q_units, cal.probe_semiangle_mrad) == (0.5, "mrad", 4.0)
        assert cal.probe_radius_px == 8.0
        assert (cal.r_pixel_size, cal.r_units) == (2.5, "A")

    def test_uncalibrated_cube(self, synthetic_data):
        from callbacks.py4dstem_bridge import calibrationFromPy4DSTEM
        cal = calibrationFromPy4DSTEM(py4DSTEM.DataCube(_cube(synthetic_data).copy()))
        assert cal.beam_xy is None and cal.probe_semiangle_mrad is None

    def test_datacube_sets_the_beam(self, app, qapp, synthetic_data):
        from callbacks.py4dstem_bridge import loadDataCube
        loadDataCube(app, _py4dstem_cube(synthetic_data))
        _loaded(app, qapp)
        assert (app.TBX.value(), app.TBY.value()) == pytest.approx((10.0, 7.0))
        assert app.Alpha.value() == pytest.approx(4.0) and app.mradPx.value() == pytest.approx(0.5)
        assert (app.D.ScanStep, app.D.ScanUnits) == (2.5, "A")

    def test_open_with_reader(self, app, qapp, tmp_path, synthetic_data):
        from callbacks.py4dstem_bridge import openWithPy4DSTEM
        path = str(tmp_path / "saved_by_py4dstem.h5")
        py4DSTEM.save(path, _py4dstem_cube(synthetic_data), mode="o")
        assert openWithPy4DSTEM(app, path)
        _loaded(app, qapp)
        assert np.allclose(app.Data, synthetic_data)
        assert (app.TBX.value(), app.TBY.value()) == pytest.approx((10.0, 7.0))
        assert app.D.filePath == path and app.SaveWindow.SaveImgPrefix.text() == "saved_by_py4dstem_"

    def test_unreadable_file(self, app, tmp_path):
        from callbacks.py4dstem_bridge import openWithPy4DSTEM
        bad = tmp_path / "bad.h5"
        bad.write_bytes(b"not hdf5")
        assert not openWithPy4DSTEM(app, str(bad))
        assert app.Data is None

    def test_find_datacube_in_lists_and_trees(self, synthetic_data):
        from callbacks.py4dstem_bridge import findDataCube
        dc = _py4dstem_cube(synthetic_data)
        assert findDataCube(dc) is dc and findDataCube([None, dc]) is dc
        assert findDataCube(None) is None and findDataCube([1, "x"]) is None


def test_show_returns_the_window_without_blocking(qapp, synthetic_data):
    import pyquant4d
    win = pyquant4d.show(_cube(synthetic_data), name="notebook", block=False)
    try:
        _loaded(win, qapp)
        assert win.embedded and win.windowTitle() == "notebook"
        assert np.allclose(win.Data, synthetic_data)
    finally:
        win.close()                       # embedded: closes its windows, does not end the session
        qapp.processEvents()
    assert not win.isVisible() and not win.SettingsWindow.isVisible()
