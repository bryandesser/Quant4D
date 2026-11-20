"""
Integration tests — Section 4.4 (display controls) and 4.5 (histogram box).

The display controls live in the Settings window and act on the image chosen in
``DispImage``.  Each test drives a control and checks what ``plotImage`` put
on the axes.
"""
import numpy as np
import pytest

from conftest import set_mode


@pytest.fixture()
def real(loaded_app, qapp):
    """Select the Real image in the display controls, with default settings."""
    set_mode(loaded_app, qapp, "AnnMod")
    loaded_app.AnnRi.setValue((0, 6))
    sw = loaded_app.SettingsWindow
    sw.DispImage.setCurrentIndex(sw.DispImage.findData("Real"))
    sw.DispBrightnessReset.click()
    sw.DispContrastReset.click()
    sw.DispGammaReset.click()
    if sw.DispCMapInvert.isChecked():
        sw.DispCMapInvert.click()
    sw.DispCMap.setCurrentIndex(sw.DispCMap.findText("gray"))
    qapp.processEvents()
    return loaded_app


def _shown(app, id="Real"):
    return np.ma.getdata(app.ImageAx[id].get_array()).astype(float)


class TestBrightnessContrastGamma:
    def test_defaults_span_full_range(self, real):
        shown = _shown(real)
        assert shown.min() == pytest.approx(0) and shown.max() == pytest.approx(1)

    def test_brightness(self, real, qapp):
        before = _shown(real)
        real.SettingsWindow.DispBrightness.setValue(70)
        qapp.processEvents()
        assert real.Fig.Real.brightness == 70
        assert _shown(real).mean() > before.mean(), "brighter should raise the displayed values"

    def test_contrast(self, real, qapp):
        before = _shown(real)
        real.SettingsWindow.DispContrast.setValue(75)
        qapp.processEvents()
        assert real.Fig.Real.contrast == 75
        after = _shown(real)
        assert after.std() > before.std(), "more contrast should spread the displayed values"
        assert (after == 0).sum() + (after == 1).sum() > (before == 0).sum() + (before == 1).sum()

    def test_gamma(self, real, qapp):
        before = _shown(real)
        real.SettingsWindow.DispGamma.setValue(2.0)
        qapp.processEvents()
        assert np.allclose(_shown(real), before ** 2, atol=1e-6)

    def test_resets(self, real, qapp):
        sw = real.SettingsWindow
        sw.DispBrightness.setValue(80)
        sw.DispContrast.setValue(20)
        sw.DispGamma.setValue(3.0)
        for b in (sw.DispBrightnessReset, sw.DispContrastReset, sw.DispGammaReset):
            b.click()
        qapp.processEvents()
        assert (sw.DispBrightness.value(), sw.DispContrast.value()) == (50, 50)
        assert sw.DispGamma.value() == pytest.approx(1.0)
        f = real.Fig.Real
        assert (f.brightness, f.contrast, f.gamma) == (50, 50, 1)

    def test_settings_are_per_image(self, real, qapp):
        sw = real.SettingsWindow
        sw.DispBrightness.setValue(65)
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Dfrn"))
        qapp.processEvents()
        assert real.Fig.Dfrn.brightness == 50 and sw.DispBrightness.value() == 50
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Real"))
        qapp.processEvents()
        assert sw.DispBrightness.value() == 65


class TestColormap:
    def test_colormap_applies(self, real, qapp):
        sw = real.SettingsWindow
        sw.DispCMap.setCurrentIndex(sw.DispCMap.findText("inferno"))
        qapp.processEvents()
        assert real.ImageAx.Real.get_cmap().name == "inferno"

    def test_invert(self, real, qapp):
        real.SettingsWindow.DispCMapInvert.click()
        qapp.processEvents()
        assert real.ImageAx.Real.get_cmap().name == "gray_r"
        real.SettingsWindow.DispCMapInvert.click()
        qapp.processEvents()
        assert real.ImageAx.Real.get_cmap().name == "gray"


class TestMaskOpacity:
    def test_unmasked_area_fades(self, real, qapp):
        real.SettingsWindow.DispMaskOpa.setValue(80)
        qapp.processEvents()
        alpha = np.asarray(real.ImageAx.Real.get_alpha(), float)
        mask = np.asarray(real.Fig.RealMask.Image, bool)
        assert np.allclose(alpha[mask], 1) and (mask.all() or np.allclose(alpha[~mask], 0.2))


class TestWindowVisibility:
    def test_hide_and_show_all(self, loaded_app, qapp):
        loaded_app.actionHide_All_Windows.trigger()
        qapp.processEvents()
        assert not loaded_app.Fig.Dfrn.isVisible() and not loaded_app.Fig.Real.isVisible()
        loaded_app.actionShow_All_Windows.trigger()
        qapp.processEvents()
        assert all(loaded_app.Fig[i].isVisible() for i in loaded_app.Fig)


class TestHistogram:
    def test_histogram_drawn_for_selected_image(self, real, qapp):
        real.SettingsWindow.DispBrightness.setValue(55)
        qapp.processEvents()
        ax = real.SettingsWindow.HistAxes.axes
        assert ax.patches or ax.lines or ax.collections, "no histogram drawn"
        assert real.A.histGamma is not None

    def test_histbox_follows_brightness(self, real, qapp):
        """Brightness shifts the display window down: both limits move by the same amount."""
        real.SettingsWindow.DispBrightness.setValue(40)
        qapp.processEvents()
        box = real.A.histBox
        lo_a, hi_a = box._lo, box._hi
        real.SettingsWindow.DispBrightness.setValue(60)
        qapp.processEvents()
        assert real.A.histBox is box, "histogram box was recreated instead of moved"
        im = real.Fig.Real.Image
        shift = 0.2 * (np.nanmax(im) - np.nanmin(im))
        assert box._lo == pytest.approx(lo_a - shift) and box._hi == pytest.approx(hi_a - shift)

    def test_dragging_histbox_sets_sliders(self, real, qapp):
        """Moving the box (as a drag would) feeds brightness/contrast back to the sliders."""
        from pyquant4d.callbacks.histBoxWidget import histbox_to_sliders
        im = real.Fig.Real.Image
        lo, hi = np.nanmin(im), np.nanmax(im)
        lo2, hi2 = lo + 0.1 * (hi - lo), hi - 0.3 * (hi - lo)
        real.A.histBox._on_change(lo2, hi2)
        qapp.processEvents()
        b, c = histbox_to_sliders(lo2, hi2, lo, hi)
        assert real.Fig.Real.brightness == round(b) and real.Fig.Real.contrast == round(c)

    def test_histbox_acts_on_current_image(self, real, qapp):
        """The box is shared; after switching images a drag must change the new image only."""
        sw = real.SettingsWindow
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Dfrn"))
        qapp.processEvents()
        im = real.Fig.Dfrn.Image
        lo, hi = float(np.nanmin(im)), float(np.nanmax(im))
        real.A.histBox._on_change(lo, lo + 0.5 * (hi - lo))
        qapp.processEvents()
        assert real.Fig.Dfrn.contrast != 50 and (real.Fig.Real.brightness, real.Fig.Real.contrast) == (50, 50)
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Dfrn"))
        sw.DispBrightnessReset.click()
        sw.DispContrastReset.click()
        qapp.processEvents()


class TestHoverReadout:
    """The toolbar shows the raw image value under the cursor, not the display-scaled one."""

    @pytest.mark.parametrize("id", ["Real", "Dfrn"])
    def test_value_at_far_corner(self, real, qapp, id):
        from matplotlib.backend_bases import MouseEvent
        from pyquant4d.callbacks.guiClass import NavigationToolbar
        fig = real.Fig[id]
        fig.canvas.draw()
        im = fig.Image
        ny, nx = im.shape                       # non-square: a swapped x/y clip shows here
        x_px, y_px = fig.ax.transData.transform((nx - 1, ny - 1))
        event = MouseEvent("motion_notify_event", fig.canvas, x_px, y_px)
        msg = NavigationToolbar._mouse_event_to_message(event)
        value = fig.ax.get_images()[0].format_cursor_data(im[ny - 1, nx - 1]).rstrip().strip("[]")
        assert msg.endswith(value), f"hover shows {msg!r}, expected the value {value}"
        assert msg.startswith(f"x={nx - 1}, y={ny - 1}"), msg           # pixel indices, compact


class TestOnScreen:
    """What is actually drawn, not just the data handed to the image: the diffraction window used
    to skip its redraw, so brightness/contrast/gamma/colour map never showed there."""

    @staticmethod
    def _pixels(app, qapp, id):
        qapp.processEvents()
        return np.asarray(app.Fig[id].canvas.buffer_rgba()).copy()

    @pytest.mark.parametrize("id", ["Dfrn", "Real"])
    @pytest.mark.parametrize("control", ["brightness", "contrast", "gamma", "colormap", "invert"])
    def test_display_controls_change_the_screen(self, real, qapp, id, control):
        sw = real.SettingsWindow
        sw.DispImage.setCurrentIndex(sw.DispImage.findData(id))
        real.Fig[id].canvas.draw()
        before = self._pixels(real, qapp, id)
        change = {"brightness": lambda: sw.DispBrightness.setValue(75),
                  "contrast": lambda: sw.DispContrast.setValue(80),
                  "gamma": lambda: sw.DispGamma.setValue(2.5),
                  "colormap": lambda: sw.DispCMap.setCurrentIndex(sw.DispCMap.findText("inferno")),
                  "invert": lambda: sw.DispCMapInvert.click()}[control]
        try:
            change()
            assert not np.array_equal(self._pixels(real, qapp, id), before), f"{control} did not change the {id} window"
        finally:
            sw.DispBrightnessReset.click()
            sw.DispContrastReset.click()
            sw.DispGammaReset.click()
            sw.DispCMap.setCurrentIndex(sw.DispCMap.findText("gray"))
            if sw.DispCMapInvert.isChecked():
                sw.DispCMapInvert.click()
            qapp.processEvents()

    def test_moving_an_annotation_does_not_paint_an_old_image(self, loaded_app, qapp):
        """Annotations moved from a spinbox used to blit a background saved earlier, painting the
        diffraction pattern as it was then over the current one."""
        from conftest import set_mode
        set_mode(loaded_app, qapp, "AlignMod")
        sw = loaded_app.SettingsWindow
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Dfrn"))
        sw.DispBrightness.setValue(80)
        qapp.processEvents()
        loaded_app.TBR.setValue(loaded_app.TBR.value() + 0.5)      # redraws the beam circle
        shown = self._pixels(loaded_app, qapp, "Dfrn")
        loaded_app.Fig.Dfrn.canvas.draw()
        try:
            assert np.array_equal(shown, self._pixels(loaded_app, qapp, "Dfrn")), "stale background painted"
        finally:
            sw.DispBrightnessReset.click()
            loaded_app.TBR.setValue(loaded_app.TBR.value() - 0.5)
            set_mode(loaded_app, qapp, "AnnMod")


class TestDisplayKeepsOtherArtists:
    def test_axis_labels_survive_display_changes(self, real, qapp):
        """Updating the histogram note used to remove every text from the image axes."""
        sw = real.SettingsWindow
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Dfrn"))
        qapp.processEvents()
        labels = lambda: sorted(t.get_text() for t in real.Fig.Dfrn.ax.texts if t.get_text())   # noqa: E731
        before = labels()
        assert "kx" in before and "ky" in before
        sw.DispGamma.setValue(1.7)
        sw.DispBrightness.setValue(60)
        qapp.processEvents()
        assert labels() == before

    def test_histogram_box_survives_switching_images(self, real, qapp):
        """Clearing the histogram for another image removed the box's artists but kept the box."""
        sw = real.SettingsWindow
        for id in ("Dfrn", "Real", "Dfrn"):
            sw.DispImage.setCurrentIndex(sw.DispImage.findData(id))
            qapp.processEvents()
            box = real.A.histBox
            assert box is not None and box._rect.axes is sw.HistAxes.axes, f"histogram box missing for {id}"
        assert real.A.hist is not None and real.A.histNote.axes is sw.HistAxes.axes

    def test_mask_opacity(self, loaded_app, qapp):
        from conftest import set_mode
        set_mode(loaded_app, qapp, "AnnMod")
        loaded_app.AnnRi.setValue((2, 6))            # a ring: there is something outside the mask
        sw = loaded_app.SettingsWindow
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Dfrn"))
        qapp.processEvents()
        assert not np.asarray(loaded_app.Fig.DfrnMask.Image, bool).all()
        fig = loaded_app.Fig.Dfrn
        fig.canvas.draw()
        before = np.asarray(fig.canvas.buffer_rgba()).copy()
        sw.DispMaskOpa.setValue(70)
        qapp.processEvents()
        fig.canvas.draw()
        try:
            assert not np.array_equal(np.asarray(fig.canvas.buffer_rgba()), before), "outside the annulus not dimmed"
            assert "Align mode" in sw.DispMaskOpa.toolTip()
        finally:
            sw.DispMaskOpa.setValue(0)
            qapp.processEvents()


class TestHistogramFollowsTheImage:
    """With the selection locked on the diffraction pattern, a new pattern with the same minimum
    and maximum (another probe position) left the old histogram on screen: the histogram canvas
    was only repainted when the display limits changed."""

    def test_new_image_same_range_repaints_and_keeps_the_box(self, loaded_app, qapp, monkeypatch):
        from pyquant4d.callbacks.plotting import plotImage
        w = loaded_app
        set_mode(w, qapp, "AnnMod")
        sw = w.SettingsWindow
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Dfrn"))
        qapp.processEvents()
        saved = w.Fig.Dfrn.Image
        rng = np.random.default_rng(0)
        a = rng.random(saved.shape)
        a.flat[0], a.flat[1] = 0.0, 1.0
        b = rng.random(saved.shape) ** 4             # a very different distribution, same min and max
        b.flat[0], b.flat[1] = 0.0, 1.0
        canvas = sw.HistAxes.figure.canvas
        draws = []
        monkeypatch.setattr(canvas, "draw_idle", lambda *_a, **_k: draws.append(1))
        try:
            w.Fig.Dfrn.Image = a
            plotImage(w, "Dfrn")
            draws.clear()
            w.Fig.Dfrn.Image = b
            plotImage(w, "Dfrn")
            assert draws, "histogram not repainted for a new image with the same range"
            counts, _ = np.histogram(b, bins=128)
            np.testing.assert_array_equal(w.A.hist.get_data().values, counts)
            assert w.A.histBox is not None and w.A.histGamma is not None and w.A.histNote is not None, \
                "the histogram box, gamma curve or note went missing"
        finally:
            w.Fig.Dfrn.Image = saved
            plotImage(w, "Dfrn")

    def test_locked_on_diffraction_follows_a_point_roi(self, loaded_app, qapp):
        w = loaded_app
        set_mode(w, qapp, "AnnMod")
        sw = w.SettingsWindow
        w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("point"))
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Dfrn"))
        sw.DispLock.click()
        try:
            for fx in (1, 4):
                w.FrameX.setValue(fx)
                qapp.processEvents()
                counts, _ = np.histogram(np.ma.masked_invalid(w.Fig.Dfrn.Image).compressed(), bins=128)
                np.testing.assert_array_equal(w.A.hist.get_data().values, counts)
        finally:
            sw.DispLock.click()
            w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("full"))
            qapp.processEvents()
