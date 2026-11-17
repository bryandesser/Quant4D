"""
Integration tests — Section 4.3 (detector modes).

Each test drives the real widgets of a window that has imported the synthetic
dataset (``loaded_app``) and checks the annotation drawn on the diffraction
pattern and the images computed from the data against direct NumPy references.
"""
import numpy as np
import pytest
from matplotlib.lines import Line2D

from annotationsClasses.interactiveAnnulus import InteractiveAnnulus
from annotationsClasses.interactiveCircle import InteractiveCircle
from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, set_mode


def _cube(app):
    return np.asarray(app.Data, float).reshape(SCAN_Y * SCAN_X, DET_Y, DET_X)


def _disc_mask(center, r):
    yy, xx = np.mgrid[0:DET_Y, 0:DET_X]
    return np.hypot(xx - center[0], yy - center[1]) <= r


class TestAlignMode:
    def test_circle_on_beam(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "AlignMod")
        tb = loaded_app.A.tb
        assert isinstance(tb, InteractiveCircle)
        assert np.allclose(tb.center, loaded_app.B0)
        assert tb.radius[-1] == pytest.approx(loaded_app.TBR.value())

    def test_spinboxes_move_circle(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "AlignMod")
        x0 = loaded_app.TBX.value()
        loaded_app.TBX.setValue(x0 + 1.5)
        loaded_app.TBR.setValue(3.0)
        qapp.processEvents()
        assert loaded_app.B0[0] == pytest.approx(x0 + 1.5)
        assert loaded_app.A.tb.center[0] == pytest.approx(x0 + 1.5)
        assert loaded_app.A.tb.radius[-1] == pytest.approx(3.0)
        loaded_app.TBX.setValue(x0)
        qapp.processEvents()

    def test_auto_align_finds_disc(self, loaded_app, qapp):
        """The disc centre averaged over the scan is ~ (0.58*DET_X + 0.75, 0.4*DET_Y + 0.45)."""
        set_mode(loaded_app, qapp, "AlignMod")
        expected = np.array([0.58 * DET_X + 0.3 * (SCAN_X - 1) / 2, 0.4 * DET_Y + 0.3 * (SCAN_Y - 1) / 2])
        assert np.abs(np.asarray(loaded_app.B0) - expected).max() < 1.0, loaded_app.B0


class TestAnnularMode:
    def test_annulus_matches_controls(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "AnnMod")
        loaded_app.AnnRi.setValue((1, 6))
        qapp.processEvents()
        adf = loaded_app.A.adf
        assert isinstance(adf, InteractiveAnnulus)
        ri, ro = (v * loaded_app.D.annWidth for v in loaded_app.AnnRi.value())
        assert np.allclose(sorted(adf.radius), [ri, ro])
        assert np.allclose(adf.center, loaded_app.B0)

    def test_image_is_annular_sum(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "AnnMod")
        mask = np.asarray(loaded_app.Fig.DfrnMask.Image, bool)
        expected = np.asarray(loaded_app.Data, float)[:, mask.ravel()].sum(axis=1).reshape(SCAN_Y, SCAN_X)
        assert mask.any() and not mask.all()
        assert np.allclose(loaded_app.Fig.Real.Image, expected, rtol=1e-5)

    def test_radius_change_recomputes(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "AnnMod")
        loaded_app.AnnRi.setValue((0, 3))
        qapp.processEvents()
        small = loaded_app.Fig.Real.Image.copy()
        loaded_app.AnnRi.setValue((0, 8))
        qapp.processEvents()
        assert loaded_app.Fig.Real.Image.sum() > small.sum()
        assert sorted(loaded_app.A.adf.radius)[1] == pytest.approx(8 * loaded_app.D.annWidth)


class TestCoMMode:
    def test_com_images(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "CoMMod")
        for i in ("CoMX", "CoMY", "CoMMag", "CoMPh"):
            im = loaded_app.Fig[i].Image
            assert im is not None and im.shape == (SCAN_Y, SCAN_X) and np.isfinite(im).all(), i

    def test_com_follows_disc(self, loaded_app, qapp):
        """The disc moves 0.3 px per probe step in x and y; with an unrotated scan, so does the CoM."""
        set_mode(loaded_app, qapp, "CoMMod")
        cx, cy = loaded_app.Fig.CoMX.Image, loaded_app.Fig.CoMY.Image
        assert np.diff(cx, axis=1).mean() == pytest.approx(0.3, abs=0.06)
        assert np.diff(cy, axis=0).mean() == pytest.approx(0.3, abs=0.06)

    def test_no_vector_field_outside_com(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "AnnMod")
        quivers = [c for c in loaded_app.Fig.Real.ax.get_children() if type(c).__name__ == "Quiver"]
        assert not quivers


class TestDPCMode:
    def test_segment_lines(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "DPCMod")
        lines = loaded_app.A.SegDetrL
        assert lines and all(isinstance(ln, Line2D) for ln in lines)
        assert len(lines) == loaded_app.NSeg.value()

    def test_nseg_change_redraws(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "DPCMod")
        n = loaded_app.NSeg.value()
        new = n + 2 if n + 2 <= loaded_app.NSeg.maximum() else n - 2
        loaded_app.NSeg.setValue(new)
        qapp.processEvents()
        assert len(loaded_app.A.SegDetrL) == new

    def test_rotation_turns_segments(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "DPCMod")
        before = [ln.get_xydata().copy() for ln in loaded_app.A.SegDetrL]
        loaded_app.DetRot.setValue(loaded_app.DetRot.value() + 15)
        qapp.processEvents()
        after = [ln.get_xydata() for ln in loaded_app.A.SegDetrL]
        assert not all(np.allclose(a, b) for a, b in zip(before, after))


class TestVirtualApertureMode:
    def test_aperture_and_image(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "VrApMod")
        loaded_app.VrApR.setValue(3)
        qapp.processEvents()
        ap = loaded_app.A.VrAp
        assert isinstance(ap, InteractiveCircle)
        mask = _disc_mask(ap.center, ap.radius[-1])
        assert np.array_equal(np.asarray(loaded_app.Fig.DfrnMask.Image, bool), mask)
        expected = _cube(loaded_app)[:, mask].sum(axis=1).reshape(SCAN_Y, SCAN_X)
        assert np.allclose(loaded_app.Fig.Real.Image, expected, rtol=1e-5)


class TestCustomMode:
    def test_circle_detector(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "CustMod")
        loaded_app.CDNewCircle.click()
        qapp.processEvents()
        cmask = list(loaded_app.A.Custom.values())[-1]
        assert isinstance(cmask.handles[0], InteractiveCircle)
        mask = np.asarray(loaded_app.Fig.DfrnMask.Image, float)
        expected = np.asarray(loaded_app.Data, float) @ mask.ravel()
        assert np.allclose(loaded_app.Fig.Real.Image, expected.reshape(SCAN_Y, SCAN_X), rtol=1e-5)

    def test_annotations_follow_mode(self, loaded_app, qapp):
        set_mode(loaded_app, qapp, "CustMod")
        if not loaded_app.A.Custom:
            loaded_app.CDNewCircle.click()
            qapp.processEvents()
        set_mode(loaded_app, qapp, "AnnMod")
        assert all(not c.handles for c in loaded_app.A.Custom.values())
        set_mode(loaded_app, qapp, "CustMod")
        assert all(c.handles for c in loaded_app.A.Custom.values() if c.type == "Circle")
        set_mode(loaded_app, qapp, "AnnMod")
