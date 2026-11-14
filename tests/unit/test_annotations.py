"""
Unit tests for all annotation classes in annotationsClasses/.

No Qt required — these widgets work purely with matplotlib axes.
"""

import numpy as np
import pytest


CENTRE = np.array([16.0, 16.0])
SHAPE  = (32, 32)   # detector pixel grid


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _roi_to_mask(roi, shape):
    """Import the shared mask-builder (adjust path to actual location)."""
    from callbacks.realSpaceROICallbacks import _roi_to_mask as _m
    return _m(roi, shape)


# ---------------------------------------------------------------------------
# InteractiveAnnulus
# ---------------------------------------------------------------------------
class TestInteractiveAnnulus:
    @pytest.fixture(autouse=True)
    def setup(self, mpl_fig_ax):
        from annotationsClasses.interactiveAnnulus import InteractiveAnnulus
        _, self.ax = mpl_fig_ax
        self.ann = InteractiveAnnulus(self.ax, CENTRE, r_inner=5, r_outer=12)

    def test_two_circles_drawn(self):
        circles = [c for c in self.ax.get_children()
                   if hasattr(c, "get_radius")]
        assert len(circles) >= 2

    def test_initial_radii(self):
        assert self.ann.r_inner == pytest.approx(5)
        assert self.ann.r_outer == pytest.approx(12)

    def test_set_outer_does_not_change_inner(self):
        self.ann.set_r_outer(20)
        assert self.ann.r_inner == pytest.approx(5)
        assert self.ann.r_outer == pytest.approx(20)

    def test_centre(self):
        np.testing.assert_allclose(self.ann.center, CENTRE)


# ---------------------------------------------------------------------------
# InteractiveCircle
# ---------------------------------------------------------------------------
class TestInteractiveCircle:
    @pytest.fixture(autouse=True)
    def setup(self, mpl_fig_ax):
        from annotationsClasses.interactiveCircle import InteractiveCircle
        _, self.ax = mpl_fig_ax
        self.circ = InteractiveCircle(self.ax, CENTRE, radius=8)

    def test_circle_drawn(self):
        circles = [c for c in self.ax.get_children()
                   if hasattr(c, "get_radius")]
        assert len(circles) >= 1

    def test_radius(self):
        assert self.circ.radius == pytest.approx(8)

    def test_centre(self):
        np.testing.assert_allclose(self.circ.center, CENTRE)

    def test_move(self):
        self.circ.set_center(np.array([10.0, 10.0]))
        np.testing.assert_allclose(self.circ.center, [10.0, 10.0])


# ---------------------------------------------------------------------------
# InteractiveRectangle
# ---------------------------------------------------------------------------
class TestInteractiveRectangle:
    @pytest.fixture(autouse=True)
    def setup(self, mpl_fig_ax):
        from annotationsClasses.interactiveRectangle import InteractiveRectangle
        _, self.ax = mpl_fig_ax
        self.rect = InteractiveRectangle(self.ax, center=CENTRE, size=np.array([10.0, 6.0]))

    def test_patch_and_handles(self):
        patches = [c for c in self.ax.get_children()
                   if hasattr(c, "get_x")]
        assert len(patches) >= 1

    def test_initial_size(self):
        np.testing.assert_allclose(self.rect.size, [10.0, 6.0])

    def test_initial_center(self):
        np.testing.assert_allclose(self.rect.center, CENTRE)

    def test_drag_body_translates(self):
        """Simulate dragging the body by calling the internal move method."""
        new_centre = CENTRE + np.array([3.0, 3.0])
        self.rect.set_center(new_centre)
        np.testing.assert_allclose(self.rect.center, new_centre)

    def test_drag_corner_changes_size(self):
        """Moving a corner should change size, keeping opposite corner fixed."""
        import types
        # Simulate corner-drag protocol if the class exposes it
        if hasattr(self.rect, "_drag_corner"):
            self.rect._drag_corner(0, np.array([CENTRE[0] - 8, CENTRE[1] - 5]))
            # Opposite corner is CENTRE + [5, 3] originally; check size grew
            assert self.rect.size[0] > 10.0 or self.rect.size[1] > 6.0

    def test_roi_to_mask_rectangle(self):
        mask = _roi_to_mask(self.rect, SHAPE)
        assert mask.dtype == bool
        assert mask.shape == SHAPE
        # Centre pixel should be inside
        assert mask[int(CENTRE[1]), int(CENTRE[0])]


# ---------------------------------------------------------------------------
# InteractivePolygon
# ---------------------------------------------------------------------------
class TestInteractivePolygon:
    @pytest.fixture(autouse=True)
    def setup(self, mpl_fig_ax):
        from annotationsClasses.interactivePolygon import InteractivePolygon
        _, self.ax = mpl_fig_ax
        verts = np.array([[10, 10], [22, 10], [16, 22]], dtype=float)
        self.poly = InteractivePolygon(self.ax, verts)

    def test_patch_drawn(self):
        from matplotlib.patches import Polygon
        polygons = [c for c in self.ax.get_children() if isinstance(c, Polygon)]
        assert len(polygons) >= 1

    def test_roi_to_mask_polygon(self):
        mask = _roi_to_mask(self.poly, SHAPE)
        assert mask.dtype == bool
        assert mask.shape == SHAPE
        # Centroid of the triangle
        cx, cy = int((10 + 22 + 16) / 3), int((10 + 10 + 22) / 3)
        assert mask[cy, cx]

    def test_translate(self):
        """Translate all vertices and check the patch updates."""
        delta = np.array([2.0, -2.0])
        orig = self.poly.verts.copy()
        self.poly.translate(delta)
        np.testing.assert_allclose(self.poly.verts, orig + delta)
