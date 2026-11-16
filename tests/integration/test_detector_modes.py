"""
Integration tests — Section 4.3 (Detector Mode switching).

Each test switches the detector mode and asserts:
  - the correct annotation appears on the diffraction axes
  - the correct real-space image is computed / displayed
  - no unhandled exceptions are raised
"""

import pytest
from pytestqt.qt_compat import qt_api
Qt = qt_api.QtCore.Qt


MODES = {
    "AlignMod": "InteractiveCircle",
    "AnnMod":   "InteractiveAnnulus",
    "CoMMod":   None,          # no single annotation class
    "DPCMod":   None,
    "VrApMod":  "InteractiveCircle",
}


def _set_mode(app, qtbot, mode_text):
    """Select a detector mode and wait for the UI to settle."""
    combo = app.DetrMode
    idx = combo.findText(mode_text)
    assert idx >= 0, f"Mode {mode_text!r} not found in DetectorMode combo"
    combo.setCurrentIndex(idx)
    # Give Qt a moment to process the signal
    qtbot.wait(100)


@pytest.mark.skip(reason="Requires initialized display pipeline with real data")
class TestAlignMode:
    def test_circle_appears(self, app, qtbot):
        _set_mode(app, qtbot, "AlignMod")
        from annotationsClasses.interactiveCircle import InteractiveCircle
        assert isinstance(app.A.Circle, InteractiveCircle)

    def test_tbox_updates_on_spinbox_change(self, app, qtbot):
        _set_mode(app, qtbot, "AlignMod")
        old_x = app.A.Circle.center[0]
        # Change TBX spinbox
        app.TBX.setValue(app.TBX.value() + 2)
        qtbot.wait(50)
        assert app.A.Circle.center[0] != old_x


@pytest.mark.skip(reason="Requires initialized display pipeline with real data")
class TestAnnularMode:
    def test_annulus_appears(self, app, qtbot):
        _set_mode(app, qtbot, "AnnMod")
        from annotationsClasses.interactiveAnnulus import InteractiveAnnulus
        assert isinstance(app.A.Annulus, InteractiveAnnulus)

    def test_inner_radius_matches_slider(self, app, qtbot):
        _set_mode(app, qtbot, "AnnMod")
        ri = app.AnnRi.value()
        assert app.A.Annulus.r_inner == pytest.approx(ri, rel=0.05)

    def test_outer_radius_matches_slider(self, app, qtbot):
        _set_mode(app, qtbot, "AnnMod")
        ro = app.AnnRo.value()
        assert app.A.Annulus.r_outer == pytest.approx(ro, rel=0.05)

    def test_move_inner_slider_updates_ui(self, app, qtbot):
        _set_mode(app, qtbot, "AnnMod")
        app.AnnRi.setValue(app.AnnRi.value() + 2)
        qtbot.wait(50)
        # Annulus inner radius should track
        assert app.A.Annulus.r_inner == pytest.approx(app.AnnRi.value(), rel=0.05)


@pytest.mark.skip(reason="Requires initialized display pipeline with real data")
class TestCoMMode:
    def test_com_images_computed(self, app, qtbot):
        """After switching to CoMMod, CoM X and Y arrays must be non-None."""
        _set_mode(app, qtbot, "CoMMod")
        assert app.D.CoMX is not None
        assert app.D.CoMY is not None
        assert app.D.CoMX.shape == (8, 8)

    def test_no_vector_field_in_ann_mode(self, app, qtbot):
        """plotVectorField should not draw arrows when not in CoM/DPC mode."""
        _set_mode(app, qtbot, "AnnMod")
        # Quiver artists on Real axes should be absent
        quivers = [c for c in app.Fig.Real.ax.get_children()
                   if type(c).__name__ == "Quiver"]
        assert len(quivers) == 0


@pytest.mark.skip(reason="Requires initialized display pipeline with real data")
class TestDPCMode:
    def test_segments_drawn(self, app, qtbot):
        _set_mode(app, qtbot, "DPCMod")
        # DPC mode draws wedge patches on the diffraction axes
        from matplotlib.patches import Wedge
        wedges = [c for c in app.Fig.Dfrn.ax.get_children()
                  if isinstance(c, Wedge)]
        assert len(wedges) == app.NSeg.value()

    def test_nseg_change_redraws(self, app, qtbot):
        _set_mode(app, qtbot, "DPCMod")
        orig = app.NSeg.value()
        app.NSeg.setValue(orig + 2 if orig + 2 <= app.NSeg.maximum() else orig - 2)
        qtbot.wait(100)
        from matplotlib.patches import Wedge
        wedges = [c for c in app.Fig.Dfrn.ax.get_children()
                  if isinstance(c, Wedge)]
        assert len(wedges) == app.NSeg.value()

    def test_det_rot_rotates_segments(self, app, qtbot):
        _set_mode(app, qtbot, "DPCMod")
        from matplotlib.patches import Wedge
        before = [w.theta1 for w in app.Fig.Dfrn.ax.get_children()
                  if isinstance(w, Wedge)]
        app.DetRot.setValue(app.DetRot.value() + 15)
        qtbot.wait(50)
        after = [w.theta1 for w in app.Fig.Dfrn.ax.get_children()
                 if isinstance(w, Wedge)]
        assert before != after


@pytest.mark.skip(reason="Requires initialized display pipeline with real data")
class TestVirtualApertureMode:
    def test_circle_appears(self, app, qtbot):
        _set_mode(app, qtbot, "VrApMod")
        from annotationsClasses.interactiveCircle import InteractiveCircle
        assert isinstance(app.A.VrAp, InteractiveCircle)
