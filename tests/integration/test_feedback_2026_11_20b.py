"""Bryan's second interactive-testing round of 2026-11-20."""
import os

import numpy as np
import pytest
from matplotlib.backend_bases import MouseEvent
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, import_raw, set_mode, wait_until

COM_ACTIONS = ("actionShow_Phase_Magnitude", "actionShow_Center_of_Mass_X", "actionShow_Integrated_Center_of_Mass_iCoM")


# ---------------------------------------------------------------------- menus and shortcuts
class TestMenus:
    def test_center_of_mass_menu_only_in_com_and_dpc(self, loaded_app, qapp):
        w = loaded_app
        for mode, on in (("AnnMod", False), ("CoMMod", True), ("AlignMod", False), ("DPCMod", True),
                         ("AnnMod", False)):
            set_mode(w, qapp, mode)
            assert w.menuCenter_of_Mass.menuAction().isEnabled() == on, mode
            assert all(getattr(w, a).isEnabled() == on for a in COM_ACTIONS), mode
        assert w.actionShow_Diffraction_Pattern.isEnabled()

    def test_disabled_right_after_import(self, loaded_app):
        assert loaded_app.DetrMode.currentData() != "CoMMod" or loaded_app.menuCenter_of_Mass.isEnabled()

    def test_shortcuts_work_from_any_window(self, app):
        for name in ("actionShow_Diffraction_Pattern", "actionShow_Real_Space_Image", "ShowImportWdw", "ShowSaveWdw"):
            assert getattr(app, name).shortcutContext() == qtc.Qt.ApplicationShortcut, name
        assert app.debugImport.shortcutContext() != qtc.Qt.ApplicationShortcut


# ---------------------------------------------------------------------- swap dataset
class TestSwapDataset:
    def test_needs_a_dataset(self, app, qapp):
        app.actionSwap_Dataset.trigger()
        qapp.processEvents()
        assert not app.ImportWindow.ImpKeepP.isChecked() and not app.ImportWindow.ImpKeepP.isEnabled()

    def test_tickable_cancellable_and_keeps_settings(self, app, qapp, sample_raw_file):
        w, iw = app, app.ImportWindow
        import_raw(w, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
        set_mode(w, qapp, "AnnMod")
        w.AnnRi.setValue((1, 3))
        w.TBX.setValue(10.0)
        qapp.processEvents()
        w.actionSwap_Dataset.trigger()                   # same file in the path field: same size
        qapp.processEvents()
        assert iw.ImpKeepP.isEnabled() and iw.ImpKeepP.isChecked()
        iw.ImpKeepP.click()                              # can be unticked ...
        assert not iw.ImpKeepP.isChecked()
        iw.ImpKeepP.click()                              # ... and ticked again
        iw.ImportCancelButton.click()                    # cancelled: not remembered
        qapp.processEvents()
        assert not iw.ImpKeepP.isChecked()

        w.actionSwap_Dataset.trigger()
        qapp.processEvents()
        assert iw.ImpKeepP.isChecked()
        iw.ImportDataButton.click()
        assert wait_until(qapp, lambda: w.Data is not None and w.Fig.Dfrn.Image is not None)
        qapp.processEvents()
        assert w.DetrMode.currentData() == "AnnMod"          # the mode it replaced
        assert w.TBX.value() == pytest.approx(10.0)          # alignment kept
        assert tuple(w.AnnRi.value()) == (1, 3)              # detector kept

    def test_other_size_cannot_keep(self, app, qapp, sample_raw_file, tmp_path, synthetic_data):
        w, iw = app, app.ImportWindow
        import_raw(w, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
        other = tmp_path / "other.raw"
        synthetic_data[: (SCAN_X * SCAN_Y) // 2].astype("<f4").tofile(other)
        w.actionSwap_Dataset.trigger()
        iw.ImpFilePath.setText(str(other))
        iw.ImpFilePath.editingFinished.emit()
        iw.CustomButton.click()
        qapp.processEvents()
        iw.ImpDataType.setCurrentIndex(iw.ImpDataType.findData("f4"))
        for name, val in (("DNPxX", DET_X), ("DNPxY", DET_Y), ("DNFrX", SCAN_X // 2), ("DNFrY", SCAN_Y)):
            getattr(iw, name).setValue(val)
        qapp.processEvents()
        assert not iw.ImpKeepP.isEnabled() and not iw.ImpKeepP.isChecked()
        assert "needs the size of the loaded dataset" in iw.ImpNotes.toPlainText()
        iw.ImportCancelButton.click()


# ---------------------------------------------------------------------- tooltips, icons, layout
def test_tooltips(app):
    sw = app.SettingsWindow
    for widget in (app.RealROIInvert, sw.ShowImageWdw, sw.DispLock, sw.DispCMapInvert, sw.DispMaskOpaReset,
                   sw.BandpassUnits, sw.DfScaleUnits):
        assert widget.toolTip(), widget.objectName()


def test_lock_icons_do_not_depend_on_the_current_folder(app, qapp, tmp_path):
    here = os.getcwd()
    try:
        os.chdir(tmp_path)                        # opening a file changes the current folder
        app.ScanDirUnlock.setEnabled(True)
        app.ScanDirUnlock.click()
        qapp.processEvents()
        assert not app.ScanDirUnlock.icon().isNull()
        app.ScanDirUnlock.click()
        assert not app.ScanDirUnlock.icon().isNull()
    finally:
        os.chdir(here)


def test_auto_button_only_in_the_top_row(app):
    grid = app.comControls.layout()
    row, col, rows, cols = grid.getItemPosition(grid.indexOf(app.AutoCurl))
    assert (row, rows) == (0, 1)
    assert grid.getItemPosition(grid.indexOf(app.ScanDir_NF))[0] == 0


def test_settings_minimum_height(app):
    assert app.SettingsWindow.minimumHeight() >= 600


def test_windows_tabs_alike(app):
    sw = app.SettingsWindow
    for a, b in (("DfScaleLabel", "RsStepLabel"), ("DfScale", "RsStep"), ("DfScaleUnits", "RsUnits"),
                 ("ScaleBarDfrn", "ScaleBarReal"), ("RotDfrn", "RotReal")):
        ga, gb = sw.DfrnWindowGrid, sw.RealWindowGrid
        pa = ga.getItemPosition(ga.indexOf(getattr(sw, a)))
        pb = gb.getItemPosition(gb.indexOf(getattr(sw, b)))
        assert pa == pb, (a, b)


# ---------------------------------------------------------------------- CoM / DPC entry
class TestComEntry:
    @pytest.fixture()
    def fresh(self, app, qapp, sample_raw_file):
        import_raw(app, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
        return app

    @pytest.mark.parametrize("mode", ["CoMMod", "DPCMod"])
    def test_first_visit_runs_auto_curl(self, fresh, qapp, monkeypatch, mode):
        from callbacks import compute
        calls = []
        real = compute.scan_rotation_by_curl
        monkeypatch.setattr(compute, "scan_rotation_by_curl", lambda *a, **k: calls.append(1) or real(*a, **k))
        assert not fresh.P.ScanDirInit
        set_mode(fresh, qapp, mode)
        assert calls and fresh.P.ScanDirInit                        # aligned: no orange highlight
        assert fresh.C.WarnC.name() not in fresh.comControls.styleSheet()
        set_mode(fresh, qapp, "AnnMod")
        set_mode(fresh, qapp, mode)
        assert len(calls) == 1                                       # only the first visit

    def test_phase_and_integrated_windows_come_up(self, fresh, qapp):
        set_mode(fresh, qapp, "CoMMod")
        for id in ("CoMPhMag", "iCoM", "dCoM"):
            fresh.Fig[id].hide()
        set_mode(fresh, qapp, "AnnMod")
        set_mode(fresh, qapp, "CoMMod")
        assert all(fresh.Fig[id].isVisible() for id in ("CoMPhMag", "iCoM", "dCoM"))
        assert fresh.SettingsWindow.SettingsTabGroup.currentWidget() is fresh.SettingsWindow.WindowsTab


def test_symmetric_field_keeps_the_flip():
    from callbacks import compute
    y, x = np.mgrid[0:12, 0:16].astype(float)
    for flip in (False, True):                    # a radial field is curl-free with and without the flip
        angle, got, _ = compute.scan_rotation_by_curl(0.3 * x, 0.3 * y, prefer_deg=0, prefer_flip=flip)
        assert got == flip and angle == pytest.approx(0, abs=0.02)


# ---------------------------------------------------------------------- real-space ROI menu
class TestROIMenu:
    @pytest.fixture()
    def ellipse(self, loaded_app, qapp):
        w = loaded_app
        set_mode(w, qapp, "AnnMod")
        w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("ellipse"))
        qapp.processEvents()
        yield w
        w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("full"))
        qapp.processEvents()

    def test_fix_aspect_and_circle(self, ellipse, qapp):
        from callbacks.realSpaceROICallbacks import roiMenu
        w = ellipse
        roi = w.A.RealROI["Real"]
        menu = roiMenu(w, roi)
        aspect, circle = menu.actions()
        assert (aspect.text(), circle.text()) == ("Fix aspect ratio", "Fix circle")
        aspect.setChecked(True)
        assert all(r.keep_aspect for r in w.A.RealROI.values())
        circle.setChecked(True)
        qapp.processEvents()
        for r in w.A.RealROI.values():
            assert r.semiaxes[0] == pytest.approx(r.semiaxes[1])
        # a resize keeps the circle
        roi.keep_aspect = True
        roi.canvas.draw()
        roi.background = roi.canvas.copy_from_bbox(roi.axis.bbox)
        roi._press = (roi.center.copy(), roi.semiaxes.copy(), roi.rotation, 0, 0)
        roi._transform = "axis_0"
        from annotationsClasses.interactiveEllipse import InteractiveEllipse
        InteractiveEllipse.lock = roi
        try:
            x, y = roi.center + np.array([roi.semiaxes[0] * 1.5, 0])
            px, py = roi.axis.transData.transform((x, y))
            roi.on_motion(MouseEvent("motion_notify_event", roi.canvas, px, py))
        finally:
            InteractiveEllipse.lock = None
            roi._press = None
        assert roi.semiaxes[0] == pytest.approx(roi.semiaxes[1], rel=1e-6)
        menu = roiMenu(w, roi)
        assert menu.actions()[1].isChecked() and not menu.actions()[0].isChecked()

    def test_rectangle_square(self, loaded_app, qapp):
        from callbacks.realSpaceROICallbacks import roiMenu
        w = loaded_app
        set_mode(w, qapp, "AnnMod")
        w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("rectangle"))
        qapp.processEvents()
        try:
            roi = w.A.RealROI["Real"]
            menu = roiMenu(w, roi)
            assert menu.actions()[1].text() == "Fix square"
            menu.actions()[1].setChecked(True)
            qapp.processEvents()
            assert roi.size[0] == pytest.approx(roi.size[1]) and roi.keep_aspect
        finally:
            w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("full"))
            qapp.processEvents()


# ---------------------------------------------------------------------- bandpass units
class TestBandpassUnits:
    @pytest.fixture()
    def com(self, loaded_app, qapp):
        w = loaded_app
        sw = w.SettingsWindow
        set_mode(w, qapp, "CoMMod")
        yield w
        sw.BandpassUnits.setCurrentIndex(sw.BandpassUnits.findData("px"))
        sw.RsUnits.setCurrentIndex(sw.RsUnits.findData("pixels"))
        w.SettingsWindow.BandpassFilter.setValue((0, int(sw.BandpassFilter.maximum())))
        qapp.processEvents()
        set_mode(w, qapp, "AnnMod")

    def test_physical_units_need_a_scan_step(self, com):
        sw = com.SettingsWindow
        model = sw.BandpassUnits.model()
        assert not model.item(sw.BandpassUnits.findData("invA")).isEnabled()
        assert not model.item(sw.BandpassUnits.findData("mrad")).isEnabled()
        assert sw.BandpassFilterLow.suffix() == "" and sw.BandpassFilterHigh.suffix() == ""

    def test_values_follow_the_unit_and_edits_convert_back(self, com, qapp):
        from callbacks.annularDetectorCallbacks import bandpassLimits
        from callbacks.io.emd import electron_wavelength_A
        w, sw = com, com.SettingsWindow
        sw.RsUnits.setCurrentIndex(sw.RsUnits.findData("nm"))
        sw.RsStep.setValue(0.5)
        qapp.processEvents()
        sw.BandpassFilter.setValue((1, 2))
        qapp.processEvents()
        lo_px, hi_px = bandpassLimits(w)
        sw.BandpassUnits.setCurrentIndex(sw.BandpassUnits.findData("invA"))
        qapp.processEvents()
        per_a = 1 / (w.D.NFrX * 5.0)                              # 0.5 nm = 5 Å per scan step
        assert sw.BandpassFilterHigh.value() == pytest.approx(hi_px * per_a, abs=1e-4)
        assert bandpassLimits(w) == (lo_px, hi_px)                # changing the unit changes nothing
        sw.BandpassUnits.setCurrentIndex(sw.BandpassUnits.findData("mrad"))
        qapp.processEvents()
        mrad = per_a * 1000 * electron_wavelength_A(w.D.kV)
        assert sw.BandpassFilterHigh.value() == pytest.approx(hi_px * mrad, rel=1e-3)
        sw.BandpassFilterHigh.setValue(1.5 * mrad)
        qapp.processEvents()
        assert bandpassLimits(w)[1] == pytest.approx(1.5, rel=1e-3)
        np.testing.assert_allclose(w.Fig.iCoM.Image, __import__("callbacks").compute.fourier_bandpass(
            __import__("callbacks").compute.integrate_field(w.Fig.CoMX.Image, w.Fig.CoMY.Image), *bandpassLimits(w)))


# ---------------------------------------------------------------------- diffraction scale unit
def test_diffraction_scale_in_inverse_angstrom(loaded_app, qapp):
    from callbacks.io.emd import mrad_per_inverse_angstrom
    w, sw = loaded_app, loaded_app.SettingsWindow
    old = w.mradPx.value()
    try:
        sw.DfScaleUnits.setCurrentIndex(sw.DfScaleUnits.findData("invA"))
        qapp.processEvents()
        k = mrad_per_inverse_angstrom(w.D.kV)
        assert sw.DfScale.value() == pytest.approx(old / k, rel=1e-4)
        sw.DfScale.setValue(2 * old / k)
        qapp.processEvents()
        assert w.mradPx.value() == pytest.approx(2 * old, rel=1e-3)
    finally:
        sw.DfScaleUnits.setCurrentIndex(sw.DfScaleUnits.findData("mrad"))
        w.mradPx.setValue(old)
        qapp.processEvents()


# ---------------------------------------------------------------------- gamma handle
def test_gamma_handle_on_the_curve_and_draggable(loaded_app, qapp):
    w, sw = loaded_app, loaded_app.SettingsWindow
    set_mode(w, qapp, "AnnMod")
    sw.DispImage.setCurrentIndex(sw.DispImage.findData("Real"))
    sw.DispGammaReset.click()
    qapp.processEvents()
    canvas, box = sw.HistAxes, w.A.histBox
    canvas.draw()
    (hx,), (hy,) = box._handle_gamma.get_data()
    y0, y1 = box._gamma_y
    assert hx == pytest.approx((box._lo + box._hi) / 2) and hy == pytest.approx(y0 + 0.5 * (y1 - y0))
    ax = canvas.axes
    px, py = ax.transData.transform((hx, hy))
    canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, px, py))
    assert canvas.cursor().shape() == qtc.Qt.SizeVerCursor
    target = y0 + 0.25 * (y1 - y0)                      # 0.5^gamma = 0.25: gamma 2
    _, ty = ax.transData.transform((hx, target))
    for kind, y, kw in (("button_press_event", py, {"button": 1}), ("motion_notify_event", ty, {}),
                        ("button_release_event", ty, {"button": 1})):
        canvas.callbacks.process(kind, MouseEvent(kind, canvas, px, y, **kw))
    qapp.processEvents()
    try:
        assert sw.DispGamma_NF.value() == pytest.approx(2.0, abs=0.02)
        assert w.Fig.Real.gamma == pytest.approx(2.0, abs=0.02)
    finally:
        sw.DispGammaReset.click()
        qapp.processEvents()
