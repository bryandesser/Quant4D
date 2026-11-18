"""Zoom and linked views, window menu, window-size fields, byte-order swap prompt, histogram reset,
picking the transmitted beam."""
import numpy as np
import pytest
from matplotlib.backend_bases import KeyEvent, MouseEvent

from conftest import set_mode


def _scroll(fig, xy, step):
    x, y = fig.ax.transData.transform(xy)
    fig.canvas.callbacks.process("scroll_event", MouseEvent("scroll_event", fig.canvas, x, y, step=step))


def _key(fig, key):
    fig.on_key_press(KeyEvent("key_press_event", fig.canvas, key))


def _full(app, id):
    ny, nx = app.Fig[id].Image.shape[:2]
    return (-0.5, nx - 0.5), (-0.5, ny - 0.5)


@pytest.fixture()
def ann(loaded_app, qapp):
    set_mode(loaded_app, qapp, "AnnMod")
    for id in ("Dfrn", "Real"):
        _key(loaded_app.Fig[id], "home")
    yield loaded_app
    for id in ("Dfrn", "Real"):
        _key(loaded_app.Fig[id], "home")


class TestZoom:
    def test_wheel_zooms_about_the_cursor(self, ann):
        fig = ann.Fig.Dfrn
        point = (5.0, 4.0)
        before = np.diff(fig.ax.get_xlim())[0]
        _scroll(fig, point, +1)
        assert np.diff(fig.ax.get_xlim())[0] == pytest.approx(before / 1.25)
        x0, x1 = fig.ax.get_xlim()
        assert (point[0] - x0) / (x1 - x0) == pytest.approx((point[0] + 0.5) / before)   # cursor kept in place

    def test_keys(self, ann):
        fig = ann.Fig.Dfrn
        full = _full(ann, "Dfrn")
        _key(fig, "+")
        _key(fig, "+")
        assert np.ptp(fig.ax.get_xlim()) == pytest.approx(np.ptp(full[0]) / 1.25 ** 2)
        _key(fig, "-")
        assert np.ptp(fig.ax.get_xlim()) == pytest.approx(np.ptp(full[0]) / 1.25)
        _key(fig, "home")
        assert sorted(fig.ax.get_xlim()) == pytest.approx(full[0])
        assert sorted(fig.ax.get_ylim()) == pytest.approx(full[1])

    def test_never_beyond_the_image(self, ann):
        fig = ann.Fig.Real
        full = _full(ann, "Real")
        for _ in range(5):
            _scroll(fig, (1.0, 1.0), -1)          # zoom out
        assert sorted(fig.ax.get_xlim()) == pytest.approx(full[0])
        fig.ax.set_xlim(2.0, 12.0)               # e.g. a toolbar zoom/pan past the edge
        assert sorted(fig.ax.get_xlim()) == pytest.approx(full[0])
        fig.ax.set_xlim(3.0, 7.0)                # a narrower view pushed past the edge: shifted back in
        assert fig.ax.get_xlim()[1] <= full[0][1] + 1e-9

    def test_toolbar_home_is_the_whole_image(self, ann):
        fig = ann.Fig.Real
        full = _full(ann, "Real")
        fig.ax.set_xlim(1.0, 3.0)
        fig.toolbar.home()
        assert sorted(fig.ax.get_xlim()) == pytest.approx(full[0])
        assert sorted(fig.ax.get_ylim()) == pytest.approx(full[1])

    @pytest.mark.parametrize("src, others", [("Dfrn", ["DfrnMask"]), ("Real", ["RealMask"]),
                                             ("RealMask", ["Real"])])
    def test_one_view_per_space(self, ann, src, others):
        fig = ann.Fig[src]
        _scroll(fig, (2.0, 2.0), +1)
        _scroll(fig, (2.0, 2.0), +1)
        for o in others:
            assert ann.Fig[o].ax.get_xlim() == pytest.approx(fig.ax.get_xlim()), o
            assert ann.Fig[o].ax.get_ylim() == pytest.approx(fig.ax.get_ylim()), o

    def test_log_scale_key_ignored(self, ann):
        fig = ann.Fig.Dfrn
        _key(fig, "l")
        _key(fig, "k")
        assert fig.ax.get_yscale() == "linear" and fig.ax.get_xscale() == "linear"


class TestWindowMenu:
    def test_show_after_hide_all(self, loaded_app, qapp):
        w = loaded_app
        w.actionHide_All_Windows.trigger()
        qapp.processEvents()
        assert not w.Fig.Dfrn.isVisible()
        assert not w.actionShow_Diffraction_Pattern.isChecked()
        w.actionShow_Diffraction_Pattern.trigger()        # raised a TypeError
        qapp.processEvents()
        assert w.Fig.Dfrn.isVisible() and w.actionShow_Diffraction_Pattern.isChecked()
        w.actionShow_Diffraction_Pattern.trigger()
        qapp.processEvents()
        assert not w.Fig.Dfrn.isVisible()
        w.actionShow_All_Windows.trigger()
        qapp.processEvents()


class TestWindowSizeFields:
    def test_fields_show_the_image_area(self, loaded_app, qapp):
        w = loaded_app
        sw = w.SettingsWindow
        w.Fig.Dfrn.resize(420, 380)
        qapp.processEvents()
        assert sw.WdwWDfrn.value() == 420 - w.C.mplDecor.width()
        assert sw.WdwHDfrn.value() == 380 - w.C.mplDecor.height()
        w.Fig.DfrnMask.resize(500, 500)                    # another window: no accumulation
        qapp.processEvents()
        assert sw.WdwWDfrn.value() == 500 - w.C.mplDecor.width()


class TestByteOrderPrompt:
    @pytest.mark.parametrize("answer", ["Yes", "No. Revert"])
    def test_other_windows_hidden_while_asking(self, loaded_app, qapp, monkeypatch, answer):
        import callbacks.datasetOptCallbacks as ds
        w = loaded_app
        set_mode(w, qapp, "AnnMod")
        for id in ("Real", "RealMask", "DfrnMask"):
            w.Fig[id].show()
        data_before = np.array(w.Data, copy=True)
        seen = {}

        def ask(*a, **k):
            seen.update({id: w.Fig[id].isVisible() for id in ("Dfrn", "Real", "RealMask", "DfrnMask")})
            return answer
        monkeypatch.setattr(ds, "notifDLG", ask)
        updates = []
        w.UpdateImages.triggered.connect(lambda *_: updates.append(1))
        try:
            w.SettingsWindow.SwapByteOrder.click()
            qapp.processEvents()
        finally:
            w.UpdateImages.triggered.disconnect()
            w.UpdateImages.triggered.connect(lambda: __import__("callbacks.plotting", fromlist=["x"])
                                             .updateImagesCallbacks(w))
        assert seen == {"Dfrn": True, "Real": False, "RealMask": False, "DfrnMask": False}
        for id in ("Real", "RealMask", "DfrnMask"):
            assert w.Fig[id].isVisible(), f"{id} not shown again"
        if answer == "Yes":
            assert updates, "images not recomputed after keeping the swap"
            w.SettingsWindow.SwapByteOrder.click()      # put it back for the other tests
            qapp.processEvents()
        else:
            assert not updates
            np.testing.assert_array_equal(np.asarray(w.Data), data_before)


class TestHistogramDoubleClick:
    def test_resets_brightness_contrast_gamma(self, loaded_app, qapp):
        w = loaded_app
        sw = w.SettingsWindow
        set_mode(w, qapp, "AnnMod")
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Real"))
        sw.DispBrightness.setValue(70)
        sw.DispContrast.setValue(30)
        sw.DispGamma_NF.setValue(2.0)
        qapp.processEvents()
        canvas = sw.HistAxes
        canvas.callbacks.process("button_press_event",
                                 MouseEvent("button_press_event", canvas, 10, 10, button=1, dblclick=True))
        qapp.processEvents()
        fig = w.Fig.Real
        assert (fig.brightness, fig.contrast, fig.gamma) == (50, 50, 1)
        assert (sw.DispBrightness.value(), sw.DispContrast.value(), sw.DispGamma_NF.value()) == (50, 50, 1)


class TestPickTheBeam:
    def _dblclick(self, w, xy):
        fig = w.Fig.Dfrn
        fig.canvas.draw()
        x, y = fig.ax.transData.transform(xy)
        fig.canvas.callbacks.process("button_press_event",
                                     MouseEvent("button_press_event", fig.canvas, x, y, button=1, dblclick=True))
        fig.canvas.callbacks.process("button_release_event",
                                     MouseEvent("button_release_event", fig.canvas, x, y, button=1))

    def test_double_click_picks_the_nearest_detected_disk(self, loaded_app, qapp, monkeypatch):
        import callbacks.alignment as al
        w = loaded_app
        set_mode(w, qapp, "AlignMod")
        before = (w.TBX.value(), w.TBY.value(), w.TBR.value())
        monkeypatch.setattr(al, "_beamCandidates", lambda self, broad=False: (
            np.array([[12.0, 8.0], [5.0, 4.0]]), np.array([3.0, 2.5])))
        try:
            self._dblclick(w, (5.5, 4.5))                  # beside the second disk
            qapp.processEvents()
            assert (w.TBX.value(), w.TBY.value(), w.TBR.value()) == pytest.approx((5.0, 4.0, 2.5))
            np.testing.assert_allclose(w.B0, (5.0, 4.0))
            self._dblclick(w, (19.0, 2.0))                 # nowhere near a disk: centre on the click
            qapp.processEvents()
            assert (w.TBX.value(), w.TBY.value(), w.TBR.value()) == pytest.approx((19.0, 2.0, 2.5))
        finally:
            al._setBeam(w, *before)
            set_mode(w, qapp, "AnnMod")

    def test_only_in_alignment_mode(self, loaded_app, qapp, monkeypatch):
        import callbacks.alignment as al
        w = loaded_app
        set_mode(w, qapp, "AnnMod")
        called = []
        monkeypatch.setattr(al, "autoAlign", lambda *a, **k: called.append(1))
        self._dblclick(w, (5.0, 4.0))
        assert not called
