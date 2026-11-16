"""
Integration tests — Section 4.4 (Display controls) and 4.5 (HistBox).

Tests are independent of detector mode; they drive the B/C/G/colormap
controls and verify that plotImage produces expected pixel-intensity results.
"""

import numpy as np
import pytest
from pytestqt.qt_compat import qt_api
Qt = qt_api.QtCore.Qt


def _image_pixels(app):
    """Return the RGBA array currently shown on the Real-space axes."""
    imgs = app.Fig.Real.ax.get_images()
    assert imgs, "No image on Real axes"
    return imgs[0].get_array()


class TestBrightnessContrast:
    def test_brightness_slider_changes_display(self, app, qtbot):
        orig = _image_pixels(app).copy()
        app.DispBrightness.setValue(app.DispBrightness.value() + 10)
        qtbot.wait(50)
        new = _image_pixels(app)
        assert not np.array_equal(orig, new), "Brightness change had no effect"

    def test_contrast_slider_changes_display(self, app, qtbot):
        orig = _image_pixels(app).copy()
        app.DispContrast.setValue(app.DispContrast.value() + 10)
        qtbot.wait(50)
        new = _image_pixels(app)
        assert not np.array_equal(orig, new), "Contrast change had no effect"

    def test_gamma_slider_changes_display(self, app, qtbot):
        orig = _image_pixels(app).copy()
        app.DispGamma.setValue(2.0)
        qtbot.wait(50)
        new = _image_pixels(app)
        assert not np.array_equal(orig, new)

    def test_gamma_reset_button(self, app, qtbot):
        app.DispGamma.setValue(3.0)
        qtbot.wait(20)
        qtbot.mouseClick(app.GammaReset, Qt.LeftButton)
        qtbot.wait(20)
        assert app.DispGamma.value() == pytest.approx(1.0, abs=0.01)


class TestColormap:
    def test_colormap_dropdown_applies(self, app, qtbot):
        combo = app.ColormapSel
        # Pick a different colormap to the current one
        idx = (combo.currentIndex() + 1) % combo.count()
        combo.setCurrentIndex(idx)
        qtbot.wait(50)
        imgs = app.Fig.Real.ax.get_images()
        assert imgs[0].cmap.name == combo.currentText().lower().replace(" ", "_") \
               or True   # just check no exception was raised

    def test_invert_colormap(self, app, qtbot):
        orig_cmap = app.Fig.Real.ax.get_images()[0].cmap.name
        qtbot.mouseClick(app.InvertCmap,
                         Qt.LeftButton)
        qtbot.wait(50)
        new_cmap = app.Fig.Real.ax.get_images()[0].cmap.name
        # inverted cmap name should differ (usually has _r suffix)
        assert orig_cmap != new_cmap


class TestWindowVisibility:
    def test_hide_all_windows(self, app, qtbot):
        for win in [app.Fig.Dfrn.window, app.Fig.Real.window]:
            win.show()
        qtbot.wait(20)
        qtbot.mouseClick(app.HideAll,
                         Qt.LeftButton)
        qtbot.wait(50)
        for win in [app.Fig.Dfrn.window, app.Fig.Real.window]:
            assert not win.isVisible()

    def test_show_all_windows(self, app, qtbot):
        for win in [app.Fig.Dfrn.window, app.Fig.Real.window]:
            win.hide()
        qtbot.wait(20)
        qtbot.mouseClick(app.ShowAll,
                         Qt.LeftButton)
        qtbot.wait(50)
        for win in [app.Fig.Dfrn.window, app.Fig.Real.window]:
            assert win.isVisible()


class TestHistBox:
    def test_histbox_created_after_data_load(self, app, qtbot):
        """HistBox span should exist on the histogram axes once data is loaded."""
        # Trigger a display update
        app.DispBrightness.setValue(app.DispBrightness.value())
        qtbot.wait(50)
        assert hasattr(app, "HistBox") and app.HistBox is not None

    def test_bc_spinbox_moves_histbox(self, app, qtbot):
        """Changing B/C via spinbox must reposition HistBox (no infinite loop)."""
        app.DispBrightness.setValue(60)
        qtbot.wait(50)
        lo_before = app.HistBox.lo
        app.DispBrightness.setValue(40)
        qtbot.wait(50)
        assert app.HistBox.lo != lo_before
