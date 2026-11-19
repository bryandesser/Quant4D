"""Bryan's interactive-testing round of 2026-11-20: calibrations in Settings > Windows, the
diffraction Pattern dropdown and cursor readout in the status bar, the histogram handles, the
mask-opacity reset button, the rotation icons removed."""
import numpy as np
import pytest
from matplotlib.backend_bases import MouseEvent
from PyQt5 import QtCore as qtc

from conftest import set_mode


@pytest.fixture()
def annular(loaded_app, qapp):
    set_mode(loaded_app, qapp, "AnnMod")
    sw = loaded_app.SettingsWindow
    saved = (loaded_app.mradPx.value(), sw.DCUnit.currentIndex())
    yield loaded_app
    loaded_app.mradPx.setValue(saved[0])
    sw.DCUnit.setCurrentIndex(saved[1])
    qapp.processEvents()


class TestCalibrationsInWindowsTab:
    def test_layout(self, app):
        sw = app.SettingsWindow
        for name in ("DfScale", "DfScaleUnits", "ScaleBarDfrn"):
            assert sw.DfrnWindowTab.isAncestorOf(getattr(sw, name)), name
        for name in ("RsStep", "RsUnits", "ScaleBarReal"):
            assert sw.RealWindowTab.isAncestorOf(getattr(sw, name)), name
        # detector coordinate options back in Misc (Bryan, 2026-11-20: the two tabs look alike)
        for name in ("DCSys", "DCPos", "DCUnit"):
            assert sw.MiscTab.isAncestorOf(getattr(sw, name)), name
        assert not sw.MiscTab.isAncestorOf(sw.RsStep)

    def test_rotation_icons_gone(self, app):
        sw = app.SettingsWindow
        assert not hasattr(sw, "RotDfrnIcon") and not hasattr(sw, "RotRealIcon")
        assert sw.DfrnWindowTab.isAncestorOf(sw.RotDfrn) and sw.RealWindowTab.isAncestorOf(sw.RotReal)

    def test_diffraction_scale_follows_the_main_window(self, annular, qapp):
        w = annular
        w.mradPx.setValue(0.75)
        qapp.processEvents()
        assert w.SettingsWindow.DfScale.value() == pytest.approx(0.75)

    def test_editing_the_scale_recalculates(self, annular, qapp):
        w, sw = annular, annular.SettingsWindow
        sw.DCUnit.setCurrentIndex(sw.DCUnit.findData("mrad"))
        r = w.TBR.value()
        ring_mrad = w.AnnRo_NF.value()
        old = w.mradPx.value()
        sw.DfScale.setValue(2 * old)
        qapp.processEvents()
        assert w.mradPx.value() == pytest.approx(2 * old, abs=1e-4)
        assert w.Alpha.value() == pytest.approx(2 * old * r, abs=0.01)      # angle follows the scale
        assert w.AnnRo_NF.value() == pytest.approx(2 * ring_mrad, rel=0.01)  # detector shown in mrad
        w.Fig.Dfrn.canvas.draw()
        assert w.Fig.Dfrn.scaleBar.label.endswith(" mrad")


class TestStatusBar:
    def test_pattern_dropdown_in_the_status_bar(self, loaded_app):
        fig = loaded_app.Fig.Dfrn
        combo = loaded_app.DfrnCombine
        assert fig.statusBar().isAncestorOf(combo) and not fig.toolbar.isAncestorOf(combo)
        assert not fig.toolbar.coordinates                  # no coordinate label to widen the toolbar

    @pytest.mark.parametrize("id", ["Dfrn", "Real"])
    def test_readout_goes_to_the_status_bar(self, loaded_app, qapp, id):
        fig = loaded_app.Fig[id]
        fig.toolbar.set_message("x=3, y=4\n1.5")
        assert fig.statusBar().currentMessage() == "x=3, y=4  1.5"


class TestHistogramHandles:
    @pytest.fixture()
    def hist(self, loaded_app, qapp):
        w = loaded_app
        set_mode(w, qapp, "AnnMod")
        sw = w.SettingsWindow
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Real"))
        sw.DispBrightnessReset.click()
        sw.DispContrastReset.click()
        qapp.processEvents()
        sw.HistAxes.draw()
        return w, sw.HistAxes, w.A.histBox

    def test_default_window_inside_the_axes(self, hist):
        w, canvas, box = hist
        lo_x, hi_x = canvas.axes.get_xlim()
        assert lo_x < box._lo and box._hi < hi_x                       # edges can be grabbed
        im = w.Fig.Real.Image
        pad = 0.05 * (np.nanmax(im) - np.nanmin(im))
        assert lo_x == pytest.approx(np.nanmin(im) - pad, rel=1e-3, abs=1e-6)

    def test_round_handles_on_both_edges(self, hist):
        _, canvas, box = hist
        assert box._handle_lo.get_xdata()[0] == box._lo and box._handle_hi.get_xdata()[0] == box._hi
        assert box._handle_lo.get_marker() == "o"

    def test_cursor_shows_what_a_drag_does(self, hist, qapp):
        _, canvas, box = hist
        ax = canvas.axes

        def hover(x):
            px, py = ax.transData.transform((x, np.mean(ax.get_ylim())))
            canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, px, py))
            qapp.processEvents()
            return canvas.cursor().shape()

        assert hover(box._lo) == qtc.Qt.SizeHorCursor
        assert hover(box._hi) == qtc.Qt.SizeHorCursor
        assert hover(box._lo + 0.25 * (box._hi - box._lo)) == qtc.Qt.SizeAllCursor
        assert hover(ax.get_xlim()[0] + 1e-9) == qtc.Qt.ArrowCursor       # in the margin: nothing to drag

    def test_handles_follow_a_drag(self, hist, qapp):
        _, canvas, box = hist
        ax = canvas.axes
        y = np.mean(ax.get_ylim())
        x0, _ = ax.transData.transform((box._lo, y))
        span = box._hi - box._lo
        x1, _ = ax.transData.transform((box._lo + 0.25 * span, y))
        _, py = ax.transData.transform((box._lo, y))
        for kind, x, kw in (("button_press_event", x0, {"button": 1}), ("motion_notify_event", x1, {}),
                            ("button_release_event", x1, {"button": 1})):
            canvas.callbacks.process(kind, MouseEvent(kind, canvas, x, py, **kw))
        qapp.processEvents()
        assert box._handle_lo.get_xdata()[0] == pytest.approx(box._lo)


class TestMaskOpacityReset:
    def test_resets_to_zero_without_opening_the_mask(self, loaded_app, qapp):
        w = loaded_app
        sw = w.SettingsWindow
        set_mode(w, qapp, "AnnMod")
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Dfrn"))
        w.Fig.DfrnMask.hide()
        sw.DispMaskOpa.setValue(40)
        qapp.processEvents()
        assert w.Fig.Dfrn.maskOpa == 40
        sw.DispMaskOpaReset.click()
        qapp.processEvents()
        assert (sw.DispMaskOpa.value(), sw.DispMaskOpa_NF.value(), w.Fig.Dfrn.maskOpa) == (0, 0, 0)
        assert not w.Fig.DfrnMask.isVisible()
        assert "0 %" in sw.DispMaskOpaReset.toolTip()


def test_drop_diagnostics(monkeypatch, capsys):
    import callbacks.file_drop as fd
    assert fd.runningElevated() is False or fd.sys.platform == "win32"
    monkeypatch.setattr(fd, "_DEBUG", True)
    fd._debug("hello")
    assert "[pyQuant4D drop] hello" in capsys.readouterr().err
