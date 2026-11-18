"""Window placement, the progress bar, and the display-selection lock."""
import pytest

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, import_raw, set_mode


class TestSettingsBesideMain:
    def test_preview_opens_settings_beside_the_main_window(self, app, qapp, monkeypatch):
        from PyQt5.QtCore import QRect

        class WideScreen:               # the headless screen is too narrow for two windows side by side
            @staticmethod
            def availableGeometry():
                return QRect(0, 0, 3000, 2000)
        monkeypatch.setattr(app, "screen", lambda: WideScreen())
        sw = app.SettingsWindow
        sw.hide()
        sw.move(0, 0)                               # wherever Qt would put it (centred, under the importer)
        app.ShowImportWdw.trigger()
        qapp.processEvents()
        main, s = app.frameGeometry(), sw.frameGeometry()
        assert sw.isVisible()
        assert s.left() > main.right() or s.right() < main.left(), "settings window overlaps the main window"
        assert s.top() == main.top()


class TestProgressBar:
    def test_hidden_after_import(self, app, qapp, sample_raw_file):
        import_raw(app, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
        assert app.Data is not None
        assert not app.progressBarPanel.isVisibleTo(app), "progress bar left on the main window after import"

    def test_hidden_after_a_byte_swap(self, loaded_app, qapp):
        from callbacks.datasetOptCallbacks import swapByteOrder
        seen = []
        bar = loaded_app.progressBarPanel
        saved = bar.setVisible
        bar.setVisible = lambda v: (seen.append(v), saved(v))
        try:
            assert swapByteOrder(loaded_app)
            assert swapByteOrder(loaded_app)        # and back
        finally:
            bar.setVisible = saved
        assert True in seen, "no busy indicator while swapping"
        assert not bar.isVisibleTo(loaded_app)


class TestDisplayLock:
    @pytest.fixture()
    def w(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "AnnMod")
        sw = loaded_app.SettingsWindow
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Real"))
        qapp.processEvents()
        yield loaded_app
        if sw.DispLock.isChecked():
            sw.DispLock.click()
        set_mode(loaded_app, qapp, "AnnMod")

    def test_click_selects_when_unlocked(self, w, qapp):
        w.Fig.Dfrn.activateFigure.emit("Dfrn")       # a click on the diffraction window
        qapp.processEvents()
        assert w.SettingsWindow.DispImage.currentData() == "Dfrn"

    def test_locked_ignores_clicks(self, w, qapp):
        sw = w.SettingsWindow
        sw.DispLock.click()
        assert sw.DispLock.isChecked()
        w.Fig.Dfrn.activateFigure.emit("Dfrn")
        qapp.processEvents()
        assert sw.DispImage.currentData() == "Real"

    def test_locked_survives_mode_changes(self, w, qapp):
        sw = w.SettingsWindow
        sw.DispLock.click()
        for mode in ("AlignMod", "VrApMod", "AnnMod"):
            set_mode(w, qapp, mode)
            assert sw.DispImage.currentData() == "Real", f"lost the locked image entering {mode}"


def test_settings_go_left_when_the_right_is_off_screen(app, qapp, monkeypatch):
    from PyQt5.QtCore import QRect
    from callbacks.window_manager import placeBesideMain

    class Screen:
        @staticmethod
        def availableGeometry():
            return QRect(0, 0, 2000, 1200)
    monkeypatch.setattr(app, "screen", lambda: Screen())
    app.move(1500, 100)
    placeBesideMain(app, app.SettingsWindow)
    assert app.SettingsWindow.frameGeometry().right() < app.frameGeometry().left()


class TestShowWindowButtons:
    @pytest.mark.parametrize("button, id", [("ShowRealMaskWdw", "RealMask"), ("ShowDfrnMaskWdw", "DfrnMask"),
                                            ("ShowColorWheelWdw", "ColorWheel")])
    def test_main_window_buttons_show_their_window(self, loaded_app, qapp, button, id):
        w = loaded_app
        set_mode(w, qapp, "CoMMod")                  # the colour wheel button is for CoM/DPC
        try:
            w.Fig[id].hide()
            assert getattr(w, button).isEnabled()
            getattr(w, button).click()
            qapp.processEvents()
            assert w.Fig[id].isVisible(), f"{button} did not show {id}"
        finally:
            set_mode(w, qapp, "AnnMod")


class TestCoMWindowsWhenShown:
    """CoM/DPC windows shown from Settings > Misc were empty until the detector changed (only
    visible windows are drawn), and showed a black margin around the scan."""

    @pytest.mark.parametrize("id", ["CoMX", "iCoM", "dCoM", "CoMPhMag"])
    def test_drawn_and_fitted_when_shown(self, loaded_app, qapp, id):
        w = loaded_app
        for i in ("CoMX", "CoMY", "iCoM", "dCoM", "CoMMag", "CoMPh", "CoMPhMag"):
            w.Fig[i].hide()
        set_mode(w, qapp, "CoMMod")
        try:
            w.Fig[id].Image = None                   # as if never computed
            w.ImageAx[id] = None
            for art in list(w.Fig[id].ax.images):
                art.remove()
            getattr(w.SettingsWindow, f"Show{id}Wdw").click()
            qapp.processEvents()
            assert w.Fig[id].Image is not None, "not computed when asked for"
            assert w.ImageAx[id] is not None and w.ImageAx[id] in w.Fig[id].ax.images, "not drawn"
            ny, nx = w.Fig[id].Image.shape
            assert w.Fig[id].ax.get_xlim() == pytest.approx((-0.5, nx - 0.5))
            assert sorted(w.Fig[id].ax.get_ylim()) == pytest.approx([-0.5, ny - 0.5])
        finally:
            set_mode(w, qapp, "AnnMod")


class TestVectorField:
    def test_drawn_in_com_mode_with_a_qcolor(self, loaded_app, qapp):
        from matplotlib.quiver import Quiver
        w = loaded_app
        sw = w.SettingsWindow
        set_mode(w, qapp, "CoMMod")
        try:
            sw.DispImage.setCurrentIndex(sw.DispImage.findData("CoMMag"))
            w.Fig.CoMMag.show()
            qapp.processEvents()
            assert w.DispVecField.isEnabled()
            w.DispVecField.setCurrentIndex(1)            # 1:1
            qapp.processEvents()
            quivers = [c for c in w.Fig.CoMMag.ax.collections if isinstance(c, Quiver)]
            assert len(quivers) == 1
            w.DispVecField.setCurrentIndex(2)            # changing it replaces the arrows
            qapp.processEvents()
            assert len([c for c in w.Fig.CoMMag.ax.collections if isinstance(c, Quiver)]) == 1
            w.DispVecField.setCurrentIndex(0)
            qapp.processEvents()
            assert not [c for c in w.Fig.CoMMag.ax.collections if isinstance(c, Quiver)]
        finally:
            w.DispVecField.setCurrentIndex(0)
            set_mode(w, qapp, "AnnMod")

    @pytest.mark.parametrize("mode", ["AlignMod", "AnnMod", "VrApMod", "CustMod"])
    def test_disabled_outside_com_and_dpc(self, loaded_app, qapp, mode):
        w = loaded_app
        sw = w.SettingsWindow
        set_mode(w, qapp, "CoMMod")
        sw.DispImage.setCurrentIndex(sw.DispImage.findData("Real"))
        qapp.processEvents()
        assert w.DispVecField.isEnabled()
        set_mode(w, qapp, mode)
        assert not w.DispVecField.isEnabled()
        set_mode(w, qapp, "AnnMod")


class TestPreviewTabs:
    """Import Preview shows no Math (nor Misc/Info) settings tab and no Export tab; the app starts
    in Preview mode without a mode change, which used to leave them all shown."""

    @staticmethod
    def _visible(app):
        sw, tabs = app.SettingsWindow, app.SettingsWindow.SettingsTabGroup
        names = {"Math": sw.MathTab, "Misc": sw.MiscTab, "Info": sw.InfoTab}
        out = {k: tabs.isTabVisible(tabs.indexOf(t)) for k, t in names.items()}
        out["Export"] = app.SaveWindow.SaveTabGroup.isTabVisible(app.SaveWindow.SaveTabGroup.indexOf(app.SaveWindow.ExportTab))
        return out

    def test_at_startup(self, app):
        assert app.DetrMode.currentData() == "PrvwMod"
        assert self._visible(app) == {"Math": False, "Misc": False, "Info": False, "Export": False}

    def test_back_to_preview_from_custom_detectors(self, loaded_app, qapp):
        w = loaded_app
        set_mode(w, qapp, "CustMod")
        assert self._visible(w)["Math"]
        w.ShowImportWdw.trigger()
        qapp.processEvents()
        try:
            assert self._visible(w) == {"Math": False, "Misc": False, "Info": False, "Export": False}
        finally:
            w.ImportWindow.ImportCancelButton.click()
            qapp.processEvents()
        assert w.DetrMode.currentData() == "CustMod"
        assert self._visible(w) == {"Math": True, "Misc": True, "Info": True, "Export": True}
        set_mode(w, qapp, "AnnMod")
        assert not self._visible(w)["Math"]
