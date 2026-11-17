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
        from callbacks.histBoxWidget import histbox_to_sliders
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
