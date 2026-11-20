"""
DPC segments, scan-direction arrows and virtual-aperture copies follow what they belong to.

* The DPC segment lines span the annulus: they follow its radii (slider or ring drag).
* The scan-direction labels were added anew on every change and piled up on the pattern.
* Artists that move with a dragged annotation (DPC segments with the rotation handle or the
  annulus, the virtual aperture's symmetry copies) are drawn with it while it is dragged; left in
  the background taken at the press, they lagged until the drag ended.
* "Auto" sets the scan direction from the curl of the deflection field (MATLAB's AutoCurl).
"""
import numpy as np
import pytest
from matplotlib.backend_bases import MouseEvent

from conftest import set_mode


def _press_move(fig, start, end):
    """Press at *start* and move to *end* (data coordinates), without releasing."""
    canvas = fig.canvas
    canvas.draw()
    p0, p1 = fig.ax.transData.transform(start), fig.ax.transData.transform(end)
    canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, *p0))
    canvas.callbacks.process("button_press_event", MouseEvent("button_press_event", canvas, *p0, button=1))
    canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, *p1))
    return p1


def _release(fig, p1):
    canvas = fig.canvas
    canvas.callbacks.process("button_release_event", MouseEvent("button_release_event", canvas, *p1, button=1))


@pytest.fixture()
def dpc(loaded_app, qapp):
    set_mode(loaded_app, qapp, "DPCMod")
    loaded_app.AnnRi.setValue((1, 5))
    qapp.processEvents()
    yield loaded_app
    set_mode(loaded_app, qapp, "AnnMod")


def _spoke_radii(app):
    b0 = np.asarray(app.B0, float)
    x, y = app.A.SegDetrL0.get_data()
    return np.hypot(np.asarray(x) - b0[0], np.asarray(y) - b0[1])


class TestSegmentsFollowTheAnnulus:
    def test_slider(self, dpc, qapp):
        w = dpc.D.annWidth
        dpc.AnnRi.setValue((2, 6))
        qapp.processEvents()
        np.testing.assert_allclose(_spoke_radii(dpc), [2 * w, 6 * w], atol=1e-9)
        for line in dpc.A.SegDetrL:
            x, y = line.get_data()
            np.testing.assert_allclose(np.hypot(np.asarray(x) - dpc.B0[0], np.asarray(y) - dpc.B0[1]),
                                       [2 * w, 6 * w], atol=1e-9)

    def test_ring_drag(self, dpc, qapp):
        w = dpc.D.annWidth
        dpc.A.adf.radius = np.array([1.0, 4.0]) * w
        dpc.A.adf.updateCircle.emit()
        qapp.processEvents()
        np.testing.assert_allclose(_spoke_radii(dpc), [1 * w, 4 * w], atol=1e-9)

    def test_segments_drawn_with_the_dragged_ring(self, dpc, qapp, monkeypatch):
        fig = dpc.Fig.Dfrn
        outer = dpc.A.adf.point.get_offsets()[-1].copy()
        drawn = []
        saved = fig.ax.draw_artist
        monkeypatch.setattr(fig.ax, "draw_artist", lambda a: (drawn.append(a), saved(a))[1])
        p1 = _press_move(fig, outer, outer + [1.5 * dpc.D.annWidth, 0])
        try:
            assert dpc.A.adf.dragging
            assert dpc.A.SegDetrL0.get_animated(), "segments left in the drag's background"
            assert dpc.A.SegDetrL0 in drawn, "segments not drawn with the ring while dragged"
        finally:
            _release(fig, p1)
            qapp.processEvents()
        assert not dpc.A.SegDetrL0.get_animated()

    def test_segments_drawn_with_the_rotation_handle(self, dpc, qapp, monkeypatch):
        fig = dpc.Fig.Dfrn
        handle = dpc.A.SegDetrP0
        tip = handle.point.get_offsets()[0].copy()
        b0 = np.asarray(dpc.B0, float)
        drawn = []
        saved = fig.ax.draw_artist
        monkeypatch.setattr(fig.ax, "draw_artist", lambda a: (drawn.append(a), saved(a))[1])
        target = b0 + np.array([[0, -1], [1, 0]]) @ (tip - b0)         # a quarter turn
        p1 = _press_move(fig, tip, target)
        try:
            assert handle.dragging and dpc.A.SegDetrP0 is handle, "the dragged handle was replaced"
            assert dpc.A.SegDetrL0 in drawn
            x, y = dpc.A.SegDetrL0.get_data()
            angle = np.degrees(np.arctan2(y[1] - b0[1], x[1] - b0[0])) % 360
            assert angle == pytest.approx(dpc.DetRot.value() % 360, abs=1.0)
        finally:
            _release(fig, p1)
            qapp.processEvents()


class TestScanDirectionLabels:
    def test_labels_do_not_pile_up(self, loaded_app, qapp):
        w = loaded_app
        set_mode(w, qapp, "CoMMod")
        try:
            w.ScanDirUnlock.click()
            qapp.processEvents()
            n = len(w.Fig.Dfrn.ax.texts)
            for angle in (10.0, 50.0, 120.0, 300.0):
                w.ScanDir_NF.setValue(angle)
                qapp.processEvents()
            assert len(w.Fig.Dfrn.ax.texts) == n, "a new pair of labels on every change"
            labels = [t for t in w.Fig.Dfrn.ax.texts if t in (w.A.ScanDirXtext, w.A.ScanDirYtext)]
            assert len(labels) == 2
        finally:
            if w.ScanDirUnlock.isChecked():
                w.ScanDirUnlock.click()
            set_mode(w, qapp, "AnnMod")
        assert w.A.ScanDirXtext is None and w.A.ScanDirXline is None


class TestVirtualApertureCopies:
    def test_copies_follow_the_dragged_aperture(self, loaded_app, qapp, monkeypatch):
        w = loaded_app
        set_mode(w, qapp, "VrApMod")
        w.VrApSymm.setCurrentIndex(w.VrApSymm.findData(4) if w.VrApSymm.findData(4) != -1 else w.VrApSymm.count() - 1)
        qapp.processEvents()
        fig = w.Fig.Dfrn
        start = np.asarray(w.A.VrAp.center, float)
        drawn = []
        saved = fig.ax.draw_artist
        monkeypatch.setattr(fig.ax, "draw_artist", lambda a: (drawn.append(a), saved(a))[1])
        p1 = _press_move(fig, start, start + [2.0, 1.0])
        try:
            clones = [ln for ln in fig.ax.lines if getattr(ln, "_vrAp_clone", False)]
            assert clones and w.A.VrAp.dragging
            assert any(c in drawn for c in clones), "symmetry copies not drawn with the dragged aperture"
            b0 = np.asarray(w.B0, float)
            centre = np.array([np.mean(clones[0].get_xdata()), np.mean(clones[0].get_ydata())])
            moved = np.asarray(w.P.VrApXY, float)
            assert np.hypot(*(centre - b0)) == pytest.approx(np.hypot(*(moved - b0)), abs=0.1)
        finally:
            _release(fig, p1)
            qapp.processEvents()
            w.VrApSymm.setCurrentIndex(0)
            set_mode(w, qapp, "AnnMod")


class TestAutoCurl:
    def test_sets_the_direction_and_closes_the_alignment(self, loaded_app, qapp, monkeypatch):
        from callbacks import compute
        w = loaded_app
        set_mode(w, qapp, "CoMMod")
        try:
            assert w.AutoCurl.isEnabled()
            w.ScanDirUnlock.click()
            qapp.processEvents()
            monkeypatch.setattr(compute, "scan_rotation_by_curl", lambda fx, fy, prefer_deg=0, **kw: (123.4, True, 0.0))
            w.AutoCurl.click()
            qapp.processEvents()
            assert w.ScanDir_NF.value() == pytest.approx(123.4)
            assert w.ScanDir.value() == pytest.approx(123.4)
            assert w.ScanDirYFlip.isChecked()
            assert not w.ScanDirUnlock.isChecked(), "alignment left open"
            assert w.P.ScanDirInit
            assert w.A.ScanDirXline is None
            # the images now use the new direction
            mask = compute.annular_mask(w.A.k, *w.AnnRi.value())
            cx, cy = compute.center_of_mass(np.asarray(w.Data), mask, w.B0)
            ex, ey = compute.rotate_field(cx, -cy, 123.4)
            np.testing.assert_allclose(w.Fig.CoMX.Image.ravel(), ex, rtol=1e-4, atol=1e-6)
            np.testing.assert_allclose(w.Fig.CoMY.Image.ravel(), ey, rtol=1e-4, atol=1e-6)
        finally:
            w.ScanDirYFlip.setChecked(False)
            set_mode(w, qapp, "AnnMod")

    @pytest.mark.parametrize("mode", ["CoMMod", "DPCMod"])
    def test_runs_on_real_data(self, loaded_app, qapp, mode):
        w = loaded_app
        set_mode(w, qapp, mode)
        try:
            w.AutoCurl.click()
            qapp.processEvents()
            assert 0 <= w.ScanDir_NF.value() < 360
        finally:
            w.ScanDirYFlip.setChecked(False)
            set_mode(w, qapp, "AnnMod")

    def test_disabled_outside_com_and_dpc(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "AnnMod")
        assert not loaded_app.AutoCurl.isEnabled()


class TestVirtualApertureLook:
    def test_red_with_a_mirror_handle_away_from_the_centre(self, loaded_app, qapp):
        from matplotlib.colors import to_rgba
        w = loaded_app
        rmax = w.P.RMax
        w.P.RMax = 0                                  # as before Annular mode was ever used
        set_mode(w, qapp, "VrApMod")
        try:
            assert to_rgba(w.A.VrAp.circ[0].get_color()) == to_rgba("r")
            if not w.VrApMirror.isChecked():
                w.VrApMirror.click()
                qapp.processEvents()
            handle = w.A.VrApMirP
            assert handle is not None and handle.point.get_visible()
            assert to_rgba(handle.point.get_facecolor()[0]) != to_rgba("r"), "mirror handle lost among the apertures"
            pos = np.asarray(handle.position, float)
            b0 = np.asarray(w.B0, float)
            assert np.hypot(*(pos - b0)) > 2, "mirror handle hidden on the beam centre"
            # dragging it turns the mirror line
            fig = w.Fig.Dfrn
            target = b0 + np.array([[0, -1], [1, 0]]) @ (pos - b0)
            before = w.VrApMirrRot_NF.value()
            p1 = _press_move(fig, pos, target)
            _release(fig, p1)
            qapp.processEvents()
            assert w.VrApMirrRot_NF.value() != pytest.approx(before)
        finally:
            if w.VrApMirror.isChecked():
                w.VrApMirror.click()
            w.P.RMax = rmax
            set_mode(w, qapp, "AnnMod")


class TestVirtualApertureControls:
    @pytest.fixture()
    def polar(self, loaded_app, qapp):
        sw = loaded_app.SettingsWindow
        saved = (sw.DCSys.currentIndex(), sw.DCPos.currentIndex(), sw.DCUnit.currentIndex())
        sw.DCSys.setCurrentIndex(sw.DCSys.findText("Polar"))
        sw.DCPos.setCurrentIndex(sw.DCPos.findText("Relative"))
        sw.DCUnit.setCurrentIndex(sw.DCUnit.findData("px"))
        set_mode(loaded_app, qapp, "VrApMod")
        yield loaded_app
        set_mode(loaded_app, qapp, "AnnMod")
        sw.DCSys.setCurrentIndex(saved[0])
        sw.DCPos.setCurrentIndex(saved[1])
        sw.DCUnit.setCurrentIndex(saved[2])

    def test_distance_range_reaches_the_farthest_corner(self, polar):
        w = polar
        ny, nx = w.Fig.Dfrn.Image.shape
        b0 = np.asarray(w.B0, float)
        corners = np.array([[0, 0], [nx - 1, 0], [0, ny - 1], [nx - 1, ny - 1]], float)
        assert w.VrApX_NF.maximum() == pytest.approx(np.hypot(*(corners - b0).T).max(), abs=0.01)   # 2 decimals

    def test_angle_kept_at_zero_distance(self, polar, qapp):
        w = polar
        w.VrApY_NF.setValue(37.0)
        w.VrApX_NF.setValue(3.0)
        qapp.processEvents()
        w.VrApX_NF.setValue(0.0)
        qapp.processEvents()
        assert w.VrApY_NF.value() == pytest.approx(37.0), "the angle reverted to 0 on the beam centre"
        w.VrApX_NF.setValue(4.0)
        qapp.processEvents()
        d = np.asarray(w.P.VrApXY, float) - np.asarray(w.B0, float)
        assert np.degrees(np.arctan2(d[1], d[0])) == pytest.approx(37.0, abs=0.5)

    def test_invert_shows_in_the_diffraction_mask(self, polar, qapp):
        w = polar
        w.Fig.DfrnMask.show()
        before = np.asarray(w.Fig.DfrnMask.Image, bool).copy()
        w.VrApInvert.click()
        qapp.processEvents()
        try:
            np.testing.assert_array_equal(np.asarray(w.Fig.DfrnMask.Image, bool), ~before)
            shown = np.asarray(w.ImageAx.DfrnMask.get_array())
            assert shown.mean() == pytest.approx((~before).mean(), abs=1e-6), "the mask window was not redrawn"
        finally:
            w.VrApInvert.click()
            qapp.processEvents()


def test_com_starts_with_inner_radius_zero_once(loaded_app, qapp):
    w = loaded_app
    w.P.CoMRadiusInit = False
    set_mode(w, qapp, "AnnMod")
    w.AnnRi.setValue((2, 6))
    qapp.processEvents()
    set_mode(w, qapp, "CoMMod")
    assert w.AnnRi.value() == (0, 6)
    w.AnnRi.setValue((1, 6))
    qapp.processEvents()
    set_mode(w, qapp, "DPCMod")                  # not the first time any more: left alone
    assert w.AnnRi.value() == (1, 6)
    set_mode(w, qapp, "AnnMod")
