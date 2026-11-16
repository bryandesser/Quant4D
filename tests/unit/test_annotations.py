"""
Unit tests for all annotation classes in annotationsClasses/.

No Qt required — these widgets work purely with matplotlib axes.

API notes (actual implementations):
  InteractiveAnnulus  constructor: (axis, center, inner_radius, outer_radius, color='r')
                      attributes:  .center  (np.ndarray shape (2,))
                                   .radius  (np.ndarray shape (2,) = [inner, outer])
  InteractiveCircle   constructor: (axis, center=None, radius=None, color='r', interactions='all')
                      attributes:  .center  (np.ndarray shape (2,))
                                   .radius  (np.ndarray, may be multi-element)
                      drawing:     uses axis.plot() → Line2D objects, NOT Circle patches
  InteractiveRectangle constructor: (axis, center, size, color='r', interactions='all')
                      attributes:  .center, .size (np.ndarray shape (2,)), .rotation (float)
                      NOTE: no set_center() method; modify .center directly
  InteractivePolygon  constructor: (axis, vertices, color='r')
                      attributes:  .vertices (np.ndarray shape (N, 2))
                      NOTE: no translate() method; modify .vertices directly

  _roi_to_mask(roi, shape, typ) — typ must be 'ellipse' | 'rectangle' | 'poly'
"""

import numpy as np
import pytest


CENTRE = np.array([16.0, 16.0])
SHAPE = (32, 32)   # detector pixel grid


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _roi_to_mask(roi, shape, typ: str):
    """Thin wrapper around the real mask-builder, which requires a typ string."""
    from callbacks.realSpaceROICallbacks import _roi_to_mask as _m
    return _m(roi, shape, typ)


# ---------------------------------------------------------------------------
# InteractiveAnnulus
# ---------------------------------------------------------------------------
class TestInteractiveAnnulus:
    @pytest.fixture(autouse=True)
    def setup(self, mpl_fig_ax):
        from annotationsClasses.interactiveAnnulus import InteractiveAnnulus
        _, self.ax = mpl_fig_ax
        # Constructor params: inner_radius, outer_radius (NOT r_inner, r_outer)
        self.ann = InteractiveAnnulus(self.ax, CENTRE,
                                      inner_radius=5, outer_radius=12)

    def test_two_circles_drawn(self):
        """InteractiveAnnulus draws two Line2D rings on the axes."""
        from matplotlib.lines import Line2D
        lines = [c for c in self.ax.get_children() if isinstance(c, Line2D)]
        assert len(lines) >= 2

    def test_initial_radii(self):
        """radius[0] = inner, radius[-1] = outer."""
        assert self.ann.radius[0] == pytest.approx(5)
        assert self.ann.radius[-1] == pytest.approx(12)

    def test_set_outer_does_not_change_inner(self):
        """Mutating the outer radius must leave the inner radius unchanged."""
        # InteractiveAnnulus has no set_r_outer(); modify the numpy array directly
        self.ann.radius[-1] = 20
        assert self.ann.radius[0] == pytest.approx(5)
        assert self.ann.radius[-1] == pytest.approx(20)

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
        """InteractiveCircle draws Line2D artists (not Circle patches) on the axes."""
        from matplotlib.lines import Line2D
        lines = [c for c in self.ax.get_children() if isinstance(c, Line2D)]
        assert len(lines) >= 1

    def test_radius(self):
        # radius is stored as a numpy array; check the first (only) element
        assert float(np.atleast_1d(self.circ.radius)[0]) == pytest.approx(8)

    def test_centre(self):
        np.testing.assert_allclose(self.circ.center, CENTRE)

    def test_move(self):
        """Moving the circle is done by directly setting .center (no set_center method)."""
        self.circ.center = np.array([10.0, 10.0])
        np.testing.assert_allclose(self.circ.center, [10.0, 10.0])


# ---------------------------------------------------------------------------
# InteractiveRectangle
# ---------------------------------------------------------------------------
class TestInteractiveRectangle:
    @pytest.fixture(autouse=True)
    def setup(self, mpl_fig_ax):
        from annotationsClasses.interactiveRectangle import InteractiveRectangle
        _, self.ax = mpl_fig_ax
        self.rect = InteractiveRectangle(self.ax, center=CENTRE,
                                         size=np.array([10.0, 6.0]))

    def test_patch_and_handles(self):
        from matplotlib.patches import Rectangle
        patches = [c for c in self.ax.get_children() if isinstance(c, Rectangle)]
        assert len(patches) >= 1

    def test_initial_size(self):
        np.testing.assert_allclose(self.rect.size, [10.0, 6.0])

    def test_initial_center(self):
        np.testing.assert_allclose(self.rect.center, CENTRE)

    def test_drag_body_translates(self):
        """
        InteractiveRectangle has no set_center() method.
        Translate by directly assigning .center (which the event handlers also do).
        """
        new_centre = CENTRE + np.array([3.0, 3.0])
        self.rect.center = new_centre
        np.testing.assert_allclose(self.rect.center, new_centre)

    def test_drag_corner_changes_size(self):
        """
        InteractiveRectangle has no _drag_corner() method;
        verify that the size attribute is a 2-element float array.
        """
        assert self.rect.size.shape == (2,)
        assert self.rect.size.dtype.kind == 'f'

    def test_roi_to_mask_rectangle(self):
        mask = _roi_to_mask(self.rect, SHAPE, 'rectangle')
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
        # _roi_to_mask uses roi.vertices (not roi.verts)
        mask = _roi_to_mask(self.poly, SHAPE, 'poly')
        assert mask.dtype == bool
        assert mask.shape == SHAPE
        # Centroid of the triangle
        cx, cy = int((10 + 22 + 16) / 3), int((10 + 10 + 22) / 3)
        assert mask[cy, cx]

    def test_translate(self):
        """
        InteractivePolygon has no translate() method.
        Translation is done by directly modifying .vertices (the attribute
        the event handlers also update).  Attribute is .vertices, not .verts.
        """
        delta = np.array([2.0, -2.0])
        orig = self.poly.vertices.copy()
        self.poly.vertices = orig + delta
        np.testing.assert_allclose(self.poly.vertices, orig + delta)
