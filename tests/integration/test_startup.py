"""
Integration tests — Section 4.1 (Startup) and packaging smoke tests.

All tests use the function-scoped `app` fixture so each test gets a clean
window, even though it costs a bit more time.
"""

import pytest


class TestStartup:
    def test_app_launches_no_errors(self, app):
        """MainWindow constructs without raising."""
        assert app is not None

    def test_four_windows_created(self, app):
        """MainWindow, ImportWindow, SettingsWindow, SaveWindow all exist."""
        assert hasattr(app, "ImportWindow")
        assert hasattr(app, "SettingsWindow")
        assert hasattr(app, "SaveWindow")

    def test_figure_windows_created(self, app):
        """Fig.Dfrn, Fig.Real etc. exist on app.Fig."""
        for attr in ("Dfrn", "Real"):
            assert hasattr(app.Fig, attr), f"Fig.{attr} missing"

    def test_detector_mode_default(self, app):
        """Detector mode dropdown should default to Import Preview (PrvwMod)."""
        # Widget is DetrMode (QComboBox); data value is "PrvwMod", display text is "Import Preview"
        assert app.DetrMode.currentText() == "Import Preview"

    def test_memory_detection(self, app):
        """getMem() should have stored a positive integer in app.C.MemTot."""
        # Total system memory is stored on app.C (the C constants struct), not app.D
        assert app.C.MemTot > 0

    def test_gpu_ui_populated(self, app):
        """
        If a GPU is present ImpGPU has >1 item; on CPU-only systems it has
        exactly 1 item (the 'None' / 'CPU' placeholder).
        """
        count = app.ImportWindow.ImpGPU.count()
        assert count >= 1


class TestImports:
    """Smoke-test that all public modules import without error."""

    @pytest.mark.parametrize("module", [
        "pyquant4d.callbacks.appClass",
        "pyquant4d.callbacks.allFunctions",
        "pyquant4d.callbacks.histBoxWidget",
        "pyquant4d.callbacks.annularDetectorCallbacks",
        "pyquant4d.callbacks.virtualApertureCallbacks",
        "pyquant4d.callbacks.realSpaceROICallbacks",
        "pyquant4d.callbacks.displayCallbacks",
        "pyquant4d.annotationsClasses.interactiveCircle",
        "pyquant4d.annotationsClasses.interactivePoint",
        "pyquant4d.annotationsClasses.interactiveAnnulus",
        "pyquant4d.annotationsClasses.interactiveRectangle",
        "pyquant4d.annotationsClasses.interactivePolygon",
    ])
    def test_import(self, module):
        import importlib
        importlib.import_module(module)
