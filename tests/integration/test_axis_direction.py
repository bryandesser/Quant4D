"""
Integration tests — image orientation controls in the Settings window
(reverse X/Y, rotate view, axis-direction arrows), ported from MATLAB's
axis_direction_callbacks.
"""
import numpy as np
import pytest

from quant4d.callbacks.axis_direction import screen_directions
from conftest import set_mode


@pytest.fixture()
def oriented(loaded_app, qapp):
    """Default orientation before and after each test."""
    def reset():
        sw = loaded_app.SettingsWindow
        for space in ("Dfrn", "Real"):
            if getattr(sw, f"RvsX{space}").isChecked():
                getattr(sw, f"RvsX{space}").click()
            if not getattr(sw, f"RvsY{space}").isChecked():
                getattr(sw, f"RvsY{space}").click()
            getattr(sw, f"Rot{space}").setCurrentIndex(0)
            if not getattr(sw, f"Show{space}Axes").isChecked():
                getattr(sw, f"Show{space}Axes").click()
        qapp.processEvents()
    reset()
    yield loaded_app
    reset()


def _dirs(app, id):
    fig = app.Fig[id]
    fig.canvas.draw()
    return screen_directions(fig.ax, [(1, 0), (0, 1)])


def test_defaults_match_matlab(oriented):
    sw = oriented.SettingsWindow
    for space in ("Dfrn", "Real"):
        rot = getattr(sw, f"Rot{space}")
        assert [rot.itemData(i) for i in range(rot.count())] == [0, 90, 180, -90]
        assert not getattr(sw, f"RvsX{space}").isChecked() and getattr(sw, f"RvsY{space}").isChecked()
        assert getattr(sw, f"Show{space}Axes").isChecked()
    assert np.allclose(_dirs(oriented, "Dfrn"), [(1, 0), (0, -1)])      # x right, y down


def test_reverse_x_applies_to_one_space(oriented, qapp):
    oriented.SettingsWindow.RvsXDfrn.click()
    qapp.processEvents()
    for id in ("Dfrn", "DfrnMask", "Preview"):
        assert np.allclose(_dirs(oriented, id)[0], (-1, 0)), id
    for id in ("Real", "RealMask", "ColorWheel"):
        assert np.allclose(_dirs(oriented, id)[0], (1, 0)), id


def test_reverse_y_off_puts_y_up(oriented, qapp):
    set_mode(oriented, qapp, "CoMMod")                 # draws the colour wheel
    oriented.SettingsWindow.RvsYReal.click()
    qapp.processEvents()
    assert np.allclose(_dirs(oriented, "Real")[1], (0, 1))
    assert np.allclose(_dirs(oriented, "ColorWheel")[1], (0, 1)), "colour wheel follows the real-space view"
    set_mode(oriented, qapp, "AnnMod")


def test_rotate_view(oriented, qapp):
    sw = oriented.SettingsWindow
    sw.RotDfrn.setCurrentIndex(sw.RotDfrn.findData(90))
    qapp.processEvents()
    assert np.allclose(_dirs(oriented, "Dfrn"), [(0, -1), (-1, 0)]), "90° turns the image clockwise"
    ax = oriented.Fig.Dfrn.ax
    p0, px, py = ax.transData.transform([(0, 0), (1, 0), (0, 1)])
    assert np.isclose(np.linalg.norm(px - p0), np.linalg.norm(py - p0), rtol=1e-3), "pixels must stay square"


def test_arrows(oriented, qapp):
    fig = oriented.Fig.Real
    labels = sorted(a.get_text() for a in fig.axisArrows if hasattr(a, "get_text") and a.get_text())
    assert labels == ["rx", "ry"]
    assert sorted(a.get_text() for a in oriented.Fig.Dfrn.axisArrows if a.get_text())[:2] == ["kx", "ky"]
    oriented.SettingsWindow.ShowRealAxes.click()
    qapp.processEvents()
    assert fig.axisArrows == [] and all(oriented.Fig[i].axisArrows for i in ("Dfrn", "DfrnMask"))


def test_arrows_turn_with_view(oriented, qapp):
    """The kx arrow points along +x as displayed."""
    oriented.SettingsWindow.RvsXDfrn.click()
    qapp.processEvents()
    fig = oriented.Fig.Dfrn
    fig.canvas.draw()
    arrow = next(a for a in fig.axisArrows if hasattr(a, "arrow_patch") and a.arrow_patch is not None)
    (x0, y0), (x1, y1) = arrow.xycoords.transform([arrow.xyann, arrow.xy])
    assert x1 < x0 and np.isclose(y1, y0), "kx arrow should point left when X is reversed"


def test_scan_arrows_only_in_com_modes(oriented, qapp):
    def scan_labels():
        return [a.get_text() for a in oriented.Fig.Dfrn.axisArrows if a.get_text() in ("rx", "ry")]
    set_mode(oriented, qapp, "AnnMod")
    assert scan_labels() == []
    set_mode(oriented, qapp, "CoMMod")
    if oriented.ScanDirUnlock.isChecked():
        oriented.ScanDirUnlock.click()
        qapp.processEvents()
    assert sorted(scan_labels()) == ["rx", "ry"]
    oriented.ScanDirUnlock.click()                     # aligning the scan direction: hidden
    qapp.processEvents()
    assert scan_labels() == []
    oriented.ScanDirUnlock.click()
    qapp.processEvents()
    set_mode(oriented, qapp, "AnnMod")


def test_orientation_survives_reimport(oriented, qapp, sample_raw_file):
    from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, import_raw
    oriented.SettingsWindow.RvsXDfrn.click()
    qapp.processEvents()
    import_raw(oriented, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
    assert np.allclose(_dirs(oriented, "Dfrn")[0], (-1, 0)), "unloading cleared the axes and lost the view"
    assert oriented.Fig.Dfrn.axisArrows, "arrows not redrawn after re-import"


class TestRotationButtonsFollowView:
    """Rotate CW/CCW turn things clockwise as displayed; a mirrored view reverses the data angle."""

    def _vrap_angle(self, app, qapp, button):
        b0 = np.asarray(app.B0, float)
        before = np.asarray(app.P.VrApXY, float) - b0
        button.click()
        qapp.processEvents()
        after = np.asarray(app.P.VrApXY, float) - b0
        return np.degrees(np.arctan2(after[1], after[0]) - np.arctan2(before[1], before[0])) % 360

    def test_virtual_aperture(self, oriented, qapp):
        set_mode(oriented, qapp, "VrApMod")
        oriented.P.VrApXY = np.asarray(oriented.B0, float) + [4, 0]
        oriented.VrApRotStep.setCurrentIndex(oriented.VrApRotStep.findData(90))
        assert self._vrap_angle(oriented, qapp, oriented.VrApRotCW) == pytest.approx(90)     # y down: +90 is CW
        assert self._vrap_angle(oriented, qapp, oriented.VrApRotCCW) == pytest.approx(270)
        oriented.SettingsWindow.RvsXDfrn.click()
        qapp.processEvents()
        assert self._vrap_angle(oriented, qapp, oriented.VrApRotCW) == pytest.approx(270), "mirrored view"
        mask = np.asarray(oriented.Fig.DfrnMask.Image, bool)
        yy, xx = np.nonzero(mask)
        assert np.abs(np.array([xx.mean(), yy.mean()]) - oriented.P.VrApXY).max() < 1, "image not recomputed"
        set_mode(oriented, qapp, "AnnMod")

    def test_custom_detector(self, oriented, qapp):
        set_mode(oriented, qapp, "CustMod")
        oriented.CDNewCircle.click()
        qapp.processEvents()
        cmask = list(oriented.A.Custom.values())[-1]
        b0 = np.asarray(oriented.B0, float)
        cmask.p1 = b0 + [3, 0]
        oriented.CDRotStep.setCurrentIndex(oriented.CDRotStep.findData(90))
        oriented.SettingsWindow.RvsYDfrn.click()          # y up: mirrored
        qapp.processEvents()
        oriented.CDRotCW.click()
        qapp.processEvents()
        assert np.allclose(cmask.p1, b0 + [0, -3]), "clockwise as displayed with y up is -90 in pixels"
        oriented.CDDelMask.click()
        set_mode(oriented, qapp, "AnnMod")
