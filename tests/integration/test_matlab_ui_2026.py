"""The MATLAB UI changes ported in November 2026: Annular Integration Step, Settings > Windows (show
image windows + vector field, iCoM/dCoM bandpass filter, window size and orientation per space),
slimmer Misc, Info's "Show all variables" and the Variables tab, the mirror-angle controls following
the mirror button, CoM before DPC, and the grid-without-transmitted-beam icon."""
import numpy as np
import pytest

from conftest import set_mode


# ------------------------------------------------------------------ layout
class TestLayout:
    def test_settings_tabs(self, app):
        tabs = app.SettingsWindow.SettingsTabGroup
        names = [tabs.widget(i).objectName() for i in range(tabs.count())]
        assert names == ["DisplayTab", "WindowsTab", "MiscTab", "InfoTab", "MathTab", "VariablesTab"]

    def test_windows_tab(self, app):
        from PyQt5 import QtWidgets as qtw
        sw = app.SettingsWindow
        box = sw.ShowImageWindowsBox
        for name in ("ShowDfrnWdw", "ShowRealWdw", "ShowiCoMWdw", "ShowColorWheelWdw_2",
                     "DispVecField", "DispVecColor", "DispVecFieldLabel"):
            assert box.isAncestorOf(getattr(sw, name)), name
        assert sw.BandpassFilterBox.isAncestorOf(sw.BandpassFilter)
        tw = sw.WindowResizeTabGroup
        assert [tw.tabText(i) for i in range(tw.count())] == ["Diffraction", "Real-space"]
        for space, page in (("Dfrn", sw.DfrnWindowTab), ("Real", sw.RealWindowTab)):
            for name in (f"Show{space}Axes", f"RvsX{space}", f"RvsY{space}", f"Rot{space}", f"WdwW{space}",
                         f"WdwH{space}", f"WdwSet{space}", f"WdwSetAll{space}"):
                assert page.isAncestorOf(getattr(sw, name)), name
        assert isinstance(sw.BandpassFilterLow, qtw.QDoubleSpinBox) and sw.BandpassFilterLow.suffix() == ""

    def test_misc_and_info(self, app):
        sw = app.SettingsWindow
        for name in ("CalcPolicy", "DCSys", "DCPos", "SwapByteOrder", "SwapDfrnXY", "SwapRealXY"):
            assert sw.MiscTab.isAncestorOf(getattr(sw, name)), name
        # both calibrations live in Settings > Windows (Bryan, 2026-11-20)
        for name in ("ShowDfrnWdw", "WdwWDfrn", "RotDfrn", "DfScale", "RsStep", "RsUnits"):
            assert not sw.MiscTab.isAncestorOf(getattr(sw, name)), name
        assert sw.InfoTab.isAncestorOf(sw.ShowVariables) and sw.InfoTab.isAncestorOf(sw.DataInfo)

    def test_main_window(self, app):
        assert not hasattr(app, "DispVecField") and not hasattr(app, "ShowColorWheelWdw")
        assert app.AlignmentTab.isAncestorOf(app.AlignmentHelpIcon)
        assert "Convergence Angle" in app.AlignmentHelpIcon.toolTip()
        modes = [app.DetrMode.itemData(i) for i in range(app.DetrMode.count())]
        assert modes.index("CoMMod") < modes.index("DPCMod")

    def test_grid_without_beam_button(self, app):
        from PyQt5 import QtWidgets as qtw
        buttons = app.findChildren(qtw.QToolButton, "CDNewGridNoCenter")
        assert len(buttons) == 1, "the button is in the .ui now; it must not also be added by code"
        assert not buttons[0].icon().isNull() and buttons[0].text() != "×"


# ------------------------------------------------------------------ annular integration step
class TestAnnularStep:
    def test_default_and_placement(self, loaded_app, qapp):
        w = loaded_app
        set_mode(w, qapp, "AlignMod")
        assert w.AlignmentTab.isAncestorOf(w.AnnStepPanel) and w.AnnStepPanel.isVisibleTo(w.AlignmentTab)
        assert w.D.annWidth == pytest.approx(max(1.0, w.P.RMax / 250))
        assert w.AnnStep.value() == pytest.approx(w.D.annWidth * w.mradPx.value(), abs=1e-3)
        for mode in ("AnnMod", "CoMMod", "DPCMod"):
            set_mode(w, qapp, mode)
            assert w.AnnularDetectorTab.isAncestorOf(w.AnnStepPanel), mode
        set_mode(w, qapp, "AlignMod")
        assert w.AlignmentTab.isAncestorOf(w.AnnStepPanel)
        set_mode(w, qapp, "AnnMod")

    def test_coarser_step_reintegrates_and_keeps_the_detector_size(self, loaded_app, qapp):
        from pyquant4d.callbacks import compute
        w = loaded_app
        set_mode(w, qapp, "AnnMod")
        step0 = w.AnnStep.value()
        w.AnnRi.setValue((2, 8))
        qapp.processEvents()
        px0 = np.array(w.AnnRi.value()) * w.D.annWidth
        rings0 = w.adfImages.shape[2]
        try:
            w.AnnStep.setValue(2 * step0)
            qapp.processEvents()
            assert w.D.annWidth == pytest.approx(2 * step0 / w.mradPx.value())
            assert w.adfImages.shape[2] < rings0, "annular images not integrated again"
            np.testing.assert_allclose(np.array(w.AnnRi.value()) * w.D.annWidth, px0, atol=w.D.annWidth)
            ri, ro = w.AnnRi.value()
            mask = compute.annular_mask(w.A.k, ri, ro)
            expected = (np.asarray(w.Data, float) @ mask.ravel().astype(float)).reshape(w.Fig.Real.Image.shape)
            np.testing.assert_allclose(w.Fig.Real.Image, expected, rtol=1e-4)
            np.testing.assert_allclose(np.ravel(w.A.adf.radius), np.array([ri, ro]) * w.D.annWidth)
            assert w.AnnRo_NF.singleStep() == pytest.approx(w.D.annWidth * w.DfPxR)
        finally:
            w.AnnStep.setValue(step0)
            qapp.processEvents()


# ------------------------------------------------------------------ bandpass filter
class TestBandpass:
    def test_reset_to_all_frequencies_on_import(self, loaded_app):
        sw = loaded_app.SettingsWindow
        ny, nx = loaded_app.Fig.Real.Image.shape
        kmax = int(np.ceil(np.hypot(nx // 2, ny // 2)))
        assert (sw.BandpassFilterLow.value(), sw.BandpassFilterHigh.value()) == (0, kmax)
        assert tuple(sw.BandpassFilter.value()) == (0, kmax)

    def test_filters_icom_and_dcom(self, loaded_app, qapp):
        from pyquant4d.callbacks import compute
        w = loaded_app
        sw = w.SettingsWindow
        set_mode(w, qapp, "CoMMod")
        kmax = sw.BandpassFilterHigh.maximum()
        try:
            unfiltered = compute.integrate_field(w.Fig.CoMX.Image, w.Fig.CoMY.Image)
            np.testing.assert_allclose(w.Fig.iCoM.Image, unfiltered)       # all-pass: unchanged
            sw.BandpassFilterHigh.setValue(1)
            qapp.processEvents()
            assert tuple(sw.BandpassFilter.value()) == (0, 1), "slider not following the spin box"
            np.testing.assert_allclose(w.Fig.iCoM.Image, compute.fourier_bandpass(unfiltered, 0, 1))
            np.testing.assert_allclose(w.Fig.dCoM.Image, compute.fourier_bandpass(
                compute.divergence(w.Fig.CoMX.Image, w.Fig.CoMY.Image), 0, 1))
            sw.BandpassFilter.setValue((1, 2))
            qapp.processEvents()
            assert (sw.BandpassFilterLow.value(), sw.BandpassFilterHigh.value()) == (1, 2)
        finally:
            sw.BandpassFilter.setValue((0, kmax))
            qapp.processEvents()
            set_mode(w, qapp, "AnnMod")


# ------------------------------------------------------------------ variables, mirror controls
class TestVariables:
    def test_show_all_variables(self, loaded_app, qapp):
        w = loaded_app
        sw = w.SettingsWindow
        tabs = sw.SettingsTabGroup
        set_mode(w, qapp, "AnnMod")
        assert not tabs.isTabVisible(tabs.indexOf(sw.VariablesTab))
        sw.ShowVariables.click()
        qapp.processEvents()
        try:
            assert tabs.isTabVisible(tabs.indexOf(sw.VariablesTab))
            assert sw.ShowVariables.text() == "Hide variables"
            groups = [sw.VariablesTree.topLevelItem(i).text(0) for i in range(sw.VariablesTree.topLevelItemCount())]
            assert "Dataset (D)" in groups and "Transmitted beam" in groups
            d = sw.VariablesTree.topLevelItem(groups.index("Dataset (D)"))
            rows = {d.child(i).text(0): d.child(i).text(1) for i in range(d.childCount())}
            assert rows["NFrX"] == repr(w.D.NFrX)
        finally:
            sw.ShowVariables.click()
            qapp.processEvents()
        assert not tabs.isTabVisible(tabs.indexOf(sw.VariablesTab))
        assert sw.ShowVariables.text() == "Show all variables"

    def test_describe(self):
        from pyquant4d.callbacks.variables import describe
        assert describe(np.arange(3)) == "[0, 1, 2]"
        assert describe(np.zeros((40, 50), np.float32)).startswith("array (40, 50) float32, 0 .. 0")
        assert describe(0.123456789) == "0.123457"


def test_mirror_angle_follows_the_mirror_button(loaded_app, qapp):
    w = loaded_app
    set_mode(w, qapp, "VrApMod")
    try:
        if w.VrApMirror.isChecked():
            w.VrApMirror.click()
            qapp.processEvents()
        assert not w.VrApMirrRot.isEnabled() and not w.VrApMirrRot_NF.isEnabled()
        w.VrApMirror.click()
        qapp.processEvents()
        assert w.VrApMirrRot.isEnabled() and w.VrApMirrRot_NF.isEnabled()
    finally:
        if w.VrApMirror.isChecked():
            w.VrApMirror.click()
        set_mode(w, qapp, "AnnMod")


def test_mirror_angle_off_at_startup(app):
    assert not app.VrApMirror.isChecked() and not app.VrApMirrRot.isEnabled()
