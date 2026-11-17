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
