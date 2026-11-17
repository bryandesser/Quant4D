"""
Integration tests — controls that were never connected before the widget audit:
virtual-aperture position/radius fields and Reset, the calculation policy,
menu actions and help icons.
"""
import numpy as np
import pytest
from PyQt5 import QtWidgets as qtw

from conftest import set_mode


@pytest.fixture()
def vrap(loaded_app, qapp):
    sw = loaded_app.SettingsWindow
    sw.DCSys.setCurrentIndex(sw.DCSys.findText("Cartesian"))
    sw.DCPos.setCurrentIndex(sw.DCPos.findText("Relative"))
    sw.DCUnit.setCurrentIndex(sw.DCUnit.findData("mrad"))
    set_mode(loaded_app, qapp, "VrApMod")
    loaded_app.VrApReset.click()
    qapp.processEvents()
    yield loaded_app
    set_mode(loaded_app, qapp, "AnnMod")


def _mask_centre(app):
    yy, xx = np.nonzero(np.asarray(app.Fig.DfrnMask.Image, bool))
    return np.array([xx.mean(), yy.mean()])


class TestVirtualApertureFields:
    def test_reset(self, vrap, qapp):
        vrap.P.VrApXY = np.asarray(vrap.B0, float) + [4, 2]
        vrap.VrApR.setValue(1.5)
        vrap.VrApReset.click()
        qapp.processEvents()
        assert np.allclose(vrap.P.VrApXY, vrap.B0) and vrap.VrApR.value() == pytest.approx(vrap.TBR.value())
        assert vrap.VrApX_NF.value() == pytest.approx(0, abs=1e-6) and vrap.VrApY_NF.value() == pytest.approx(0, abs=1e-6)

    def test_typed_cartesian_position_in_mrad(self, vrap, qapp):
        s = float(vrap.DfPxR)
        assert s != 1, "test needs mrad units"
        vrap.VrApR.setValue(2)
        vrap.VrApX_NF.setValue(4 * s)            # 4 px right of the beam, in mrad
        vrap.VrApY_NF.setValue(-2 * s)           # 2 px up
        qapp.processEvents()
        expected = np.asarray(vrap.B0, float) + [4, -2]
        assert np.allclose(vrap.P.VrApXY, expected, atol=1e-2)
        assert np.abs(_mask_centre(vrap) - expected).max() < 1, "image not recomputed at the typed position"
        assert vrap.VrApX.value() == pytest.approx(4 * s, rel=1e-3), "slider not kept in step"

    def test_polar(self, vrap, qapp):
        sw = vrap.SettingsWindow
        sw.DCSys.setCurrentIndex(sw.DCSys.findText("Polar"))
        qapp.processEvents()
        assert (vrap.VrApXLabel.text(), vrap.VrApYLabel.text()) == ("Distance", "Rotation")
        s = float(vrap.DfPxR)
        vrap.VrApX_NF.setValue(3 * s)
        vrap.VrApY_NF.setValue(90)               # +y: downwards on screen
        qapp.processEvents()
        assert np.allclose(vrap.P.VrApXY, np.asarray(vrap.B0, float) + [0, 3], atol=1e-2)

    def test_radius_field_in_mrad(self, vrap, qapp):
        """The .ui used to copy the raw pixel radius into the mrad field and back (shrinking it)."""
        s = float(vrap.DfPxR)
        vrap.VrApR.setValue(2)
        qapp.processEvents()
        assert vrap.VrApR.value() == pytest.approx(2) and vrap.VrApR_NF.value() == pytest.approx(2 * s, rel=1e-3)
        vrap.VrApR_NF.setValue(3 * s)
        qapp.processEvents()
        assert vrap.VrApR.value() == pytest.approx(3, rel=1e-3)
        assert vrap.A.VrAp.radius[-1] == pytest.approx(3, rel=1e-3)

    def test_dragging_updates_fields(self, vrap, qapp):
        vrap.A.VrAp.center = np.asarray(vrap.B0, float) + [5, 0]
        vrap.A.VrAp.updateCircle.emit()
        qapp.processEvents()
        assert vrap.VrApX_NF.value() == pytest.approx(5 * float(vrap.DfPxR), rel=1e-3)


class TestCalculationPolicy:
    @pytest.fixture()
    def ann(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "AnnMod")
        loaded_app.AnnRi.setValue((0, 4))
        qapp.processEvents()
        yield loaded_app
        sw = loaded_app.SettingsWindow
        sw.CalcPolicy.setCurrentIndex(sw.CalcPolicy.findData(2))
        loaded_app.AnnRi.setValue((0, 4))
        qapp.processEvents()

    def _policy(self, app, qapp, value):
        sw = app.SettingsWindow
        sw.CalcPolicy.setCurrentIndex(sw.CalcPolicy.findData(value))
        qapp.processEvents()

    def test_passive_waits_for_update_images(self, ann, qapp):
        self._policy(ann, qapp, 0)
        before = ann.Fig.Real.Image.copy()
        ann.AnnRi.setValue((0, 8))
        qapp.processEvents()
        assert np.array_equal(ann.Fig.Real.Image, before), "passive policy recalculated"
        ann.UpdateImages.trigger()
        qapp.processEvents()
        assert not np.array_equal(ann.Fig.Real.Image, before)

    def test_reduced_waits_for_slider_release(self, ann, qapp):
        self._policy(ann, qapp, 1)
        before = ann.Fig.Real.Image.copy()
        ann.AnnRi.setSliderDown(True)            # the user is dragging
        ann.AnnRi.setValue((0, 8))
        qapp.processEvents()
        assert np.array_equal(ann.Fig.Real.Image, before), "reduced policy recalculated mid-drag"
        ann.AnnRi.setSliderDown(False)
        ann.AnnRi.sliderReleased.emit()
        qapp.processEvents()
        assert not np.array_equal(ann.Fig.Real.Image, before), "no update after the release"

    def test_reduced_updates_typed_values(self, ann, qapp):
        self._policy(ann, qapp, 1)
        before = ann.Fig.Real.Image.copy()
        ann.AnnRi.setValue((0, 8))               # not a drag
        qapp.processEvents()
        assert not np.array_equal(ann.Fig.Real.Image, before)

    def test_annotation_release_signals_once_more(self, ann, qapp):
        from annotationsClasses.interactiveCircle import InteractiveCircle
        circle = ann.A.adf
        assert isinstance(circle, InteractiveCircle) and not circle.dragging
        hits = []
        circle.updateCircle.connect(lambda: hits.append(circle.dragging))
        from matplotlib.backend_bases import MouseEvent
        InteractiveCircle.lock = circle
        circle.press = ([c._xy for c in circle.circ], circle.point.get_offsets(), (0, 0))
        circle.on_release(MouseEvent("button_release_event", circle.canvas, 0, 0))
        assert hits == [False], "release must emit a final, non-dragging update"


class TestMenus:
    def test_settings_shortcuts(self, loaded_app, qapp):
        sw = loaded_app.SettingsWindow
        loaded_app.actionMiscellaneous.trigger()
        assert sw.isVisible() and sw.SettingsTabGroup.currentWidget() is sw.MiscTab
        loaded_app.actionBrightness_and_Contrast.trigger()
        assert sw.SettingsTabGroup.currentWidget() is sw.DisplayTab
        loaded_app.actionCustom_Aperture_Maths.trigger()
        qapp.processEvents()
        assert loaded_app.DetrMode.currentData() == "CustMod" and sw.SettingsTabGroup.currentWidget() is sw.MathTab
        set_mode(loaded_app, qapp, "AnnMod")

    def test_swap_dataset_keeps_parameters(self, loaded_app, qapp):
        loaded_app.ImportWindow.ImpKeepP.setChecked(False)
        loaded_app.actionSwap_Dataset.trigger()
        qapp.processEvents()
        assert loaded_app.ImportWindow.isVisible() and loaded_app.ImportWindow.ImpKeepP.isChecked()
        loaded_app.ImportWindow.ImportCancelButton.click()
        loaded_app.ImportWindow.ImpKeepP.setChecked(False)
        qapp.processEvents()

    def test_auto_save(self, loaded_app, qapp, tmp_path):
        sw = loaded_app.SaveWindow
        sw.SaveDir.setText(str(tmp_path / "new"))
        sw.SaveImgPrefix.setText("auto_")
        sw.SaveImgTIF.setChecked(True)
        sw.SaveImgPNG.setChecked(False)
        for i in range(sw.SaveImgList.count()):
            sw.SaveImgList.item(i).setSelected(sw.SaveImgList.item(i).text() == "Real")
        loaded_app.AutoSaveImg.trigger()
        qapp.processEvents()
        assert [p.name for p in (tmp_path / "new").iterdir()][0].startswith("auto_Real"), "folder created, image saved"

    def test_about_and_help(self, loaded_app, monkeypatch):
        from PyQt5 import QtGui as qtg
        shown, opened = [], []
        monkeypatch.setattr(qtw.QMessageBox, "about", staticmethod(lambda parent, title, text: shown.append(text)))
        monkeypatch.setattr(qtg.QDesktopServices, "openUrl", staticmethod(lambda url: opened.append(url.toString())))
        loaded_app.actionAbout_Quant4D.trigger()
        loaded_app.actionQuant4D_Manual.trigger()
        assert "GNU General Public License" in shown[0] and opened == ["https://pyquant4d.readthedocs.io"]

    def test_always_available_before_import(self, app):
        assert all(a.isEnabled() for a in (app.actionQuit, app.actionAbout_Quant4D, app.actionQuant4D_Manual))
        assert not app.actionSwap_Dataset.isEnabled()

    def test_help_icons(self, loaded_app):
        sw = loaded_app.SettingsWindow
        assert "MATLAB syntax" in sw.MathHelpIcon.toolTip() and "Reduced" in sw.LiveUpdateImageIcon.toolTip()


def test_no_unit_unaware_ui_links():
    """Designer links copy raw values; they must only join widgets that share a unit."""
    import pathlib
    import re
    ui = (pathlib.Path(__file__).resolve().parents[2] / "src/gui/Quant4D_FigForm.ui").read_text(encoding="utf-8")
    pairs = {frozenset(re.findall(r"<(?:sender|receiver)>([^<]*)<", c)) for c in re.findall(r"<connection>(.*?)</connection>", ui, re.S)}
    for w in ("VrApR", "VrApX", "VrApY"):
        assert frozenset((w, w + "_NF")) not in pairs, f"{w} (px) is linked raw to {w}_NF (display unit)"
