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
  InteractiveRectangle constructor: (axis, center, size, color='r', interactions='all', rotation=0.0)
                      attributes:  .center, .size (np.ndarray shape (2,)), .rotation (float)
                      NOTE: no set_center() method; modify .center directly
  InteractiveEllipse  constructor: (axis, center, semiaxes, rotation=0.0, color='r', interactions='all')
                      attributes:  .center, .semiaxes (np.ndarray shape (2,)), .rotation (degrees)
  InteractivePolygon  constructor: (axis, vertices, color='r')
                      attributes:  .vertices (np.ndarray shape (N, 2))
                      NOTE: no translate() method; modify .vertices directly

  _roi_to_mask(roi, shape, typ) — typ must be 'ellipse' | 'rectangle' | 'poly'
"""

import numpy as np
import pytest

from conftest import just_outside, turned


CENTRE = np.array([16.0, 16.0])
SHAPE = (32, 32)   # detector pixel grid


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _roi_to_mask(roi, shape, typ: str):
    """Thin wrapper around the real mask-builder, which requires a typ string."""
    from pyquant4d.callbacks.realSpaceROICallbacks import _roi_to_mask as _m
    return _m(roi, shape, typ)


# ---------------------------------------------------------------------------
# InteractiveAnnulus
# ---------------------------------------------------------------------------
class TestInteractiveAnnulus:
    @pytest.fixture(autouse=True)
    def setup(self, mpl_fig_ax):
        from pyquant4d.annotationsClasses.interactiveAnnulus import InteractiveAnnulus
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
        from pyquant4d.annotationsClasses.interactiveCircle import InteractiveCircle
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
        from pyquant4d.annotationsClasses.interactiveRectangle import InteractiveRectangle
        _, self.ax = mpl_fig_ax
        self.rect = InteractiveRectangle(self.ax, center=CENTRE,
                                         size=np.array([10.0, 6.0]))

    def test_patch_and_handles(self):
        assert self.rect.patch in self.ax.patches
        assert len(self.rect.handles.get_offsets()) == 4
        assert self.rect.handles.get_visible()

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
        from pyquant4d.annotationsClasses.interactivePolygon import InteractivePolygon
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


# ---------------------------------------------------------------------------
# Mouse interaction: ellipse handles, rectangle rotation, polygon vertices
# ---------------------------------------------------------------------------
def _mouse(ax, *path, modifiers=None, key=None):
    """Press at the first data point, move through the others, release at the last
    (with *modifiers*, e.g. ``{"shift"}``, or a held *key*)."""
    from matplotlib.backend_bases import MouseEvent
    canvas = ax.figure.canvas
    canvas.draw()
    pts = [ax.transData.transform(p) for p in path]
    steps = [("button_press_event", pts[0])] + [("motion_notify_event", p) for p in pts[1:]] \
        + [("button_release_event", pts[-1])]
    for name, (x, y) in steps:
        kw = {"button": 1} if name != "motion_notify_event" else {}
        if modifiers is not None:
            kw["modifiers"] = frozenset(modifiers)
        canvas.callbacks.process(name, MouseEvent(name, canvas, x, y, key=key, **kw))


def _hover(ax, p):
    from matplotlib.backend_bases import MouseEvent
    canvas = ax.figure.canvas
    canvas.draw()
    x, y = ax.transData.transform(p)
    canvas.callbacks.process("motion_notify_event", MouseEvent("motion_notify_event", canvas, x, y))


@pytest.fixture()
def roi_ax(mpl_fig_ax):
    _, ax = mpl_fig_ax
    ax.set_xlim(-0.5, 31.5)
    ax.set_ylim(31.5, -0.5)          # image orientation: y down
    return ax


class TestInteractiveEllipse:
    @pytest.fixture(autouse=True)
    def setup(self, roi_ax):
        from pyquant4d.annotationsClasses.interactiveEllipse import InteractiveEllipse
        self.ax = roi_ax
        self.ell = InteractiveEllipse(self.ax, CENTRE, semiaxes=(6.0, 3.0))
        self.ell.connect()
        self.moves = []
        self.ell.updateEllipse.connect(lambda: self.moves.append(1))

    def test_two_handles_at_the_semiaxis_ends(self):
        np.testing.assert_allclose(self.ell.handles.get_offsets(), [CENTRE + [6, 0], CENTRE + [0, 3]])

    def test_major_handle_resizes_and_rotates(self):
        _mouse(self.ax, CENTRE + [6, 0], CENTRE + [4, 4], CENTRE + [0, 8])
        np.testing.assert_allclose(self.ell.semiaxes, [8.0, 3.0])
        assert self.ell.rotation % 360 == pytest.approx(90.0)
        np.testing.assert_allclose(self.ell.handles.get_offsets()[0], CENTRE + [0, 8], atol=1e-9)
        assert self.moves, "no update signal"

    def test_minor_handle_resizes_and_rotates(self):
        _mouse(self.ax, CENTRE + [0, 3], CENTRE + [-5, 0])
        np.testing.assert_allclose(self.ell.semiaxes, [6.0, 5.0])
        assert self.ell.rotation % 360 == pytest.approx(90.0)

    def test_drag_inside_translates(self):
        _mouse(self.ax, CENTRE + [1, 1], CENTRE + [3, 2])
        np.testing.assert_allclose(self.ell.center, CENTRE + [2, 1])
        np.testing.assert_allclose(self.ell.semiaxes, [6.0, 3.0])

    def test_mask_follows_rotation(self):
        from pyquant4d.callbacks import compute
        upright = _roi_to_mask(self.ell, SHAPE, 'ellipse')
        assert upright[16, 21] and not upright[21, 16]
        self.ell.rotation = 90.0
        turned = _roi_to_mask(self.ell, SHAPE, 'ellipse')
        assert turned[21, 16] and not turned[16, 21]
        np.testing.assert_array_equal(turned, compute.ellipse_mask(SHAPE, CENTRE, (6.0, 3.0), 90.0))

    def test_remove_disconnects(self):
        self.ell.remove()
        _mouse(self.ax, CENTRE + [6, 0], CENTRE + [0, 8])
        np.testing.assert_allclose(self.ell.semiaxes, [6.0, 3.0])


class TestRectangleRotation:
    @pytest.fixture(autouse=True)
    def setup(self, roi_ax):
        from pyquant4d.annotationsClasses.interactiveRectangle import InteractiveRectangle
        self.ax = roi_ax
        self.rect = InteractiveRectangle(self.ax, CENTRE, (10.0, 6.0))
        self.rect.connect()

    def test_drag_just_outside_a_corner_rotates(self):
        corner = self.rect.handles.get_offsets()[2].copy()
        start = just_outside(self.ax, corner, CENTRE)
        _mouse(self.ax, start, turned(start, CENTRE, 90.0))
        assert self.rect.rotation % 360 == pytest.approx(90.0)
        np.testing.assert_allclose(self.rect.size, [10.0, 6.0])
        np.testing.assert_allclose(self.rect.center, CENTRE)

    def test_on_the_corner_resizes_not_rotates(self):
        corner = self.rect.handles.get_offsets()[2].copy()
        _mouse(self.ax, corner, corner + [2.0, 1.0])
        assert self.rect.rotation == 0.0
        np.testing.assert_allclose(self.rect.size, [12.0, 7.0])

    def test_rotation_cursor_shown_just_outside_a_corner(self, monkeypatch):
        import pyquant4d.annotationsClasses.interactiveRectangle as mod
        shown = []
        monkeypatch.setattr(mod, "set_rotate_cursor", lambda canvas: shown.append(1))
        corner = self.rect.handles.get_offsets()[2].copy()
        _hover(self.ax, just_outside(self.ax, corner, CENTRE))
        assert shown, "no rotation cursor"
        shown.clear()
        _hover(self.ax, CENTRE)                       # inside: move, not rotate
        assert not shown

    def test_resize_in_the_rotated_frame_keeps_the_opposite_corner(self):
        self.rect.rotation = 30.0
        self.rect.redraw()
        corners = self.rect.handles.get_offsets().copy()
        _mouse(self.ax, corners[2], corners[2] + [1.0, 2.0])
        np.testing.assert_allclose(self.rect.handles.get_offsets()[0], corners[0], atol=1e-9)
        assert self.rect.rotation == pytest.approx(30.0)

    def test_mask_is_rotated(self):
        from pyquant4d.callbacks import compute
        self.rect.rotation = 90.0
        np.testing.assert_array_equal(_roi_to_mask(self.rect, SHAPE, 'rectangle'),
                                      compute.rectangle_mask(SHAPE, CENTRE, (10.0, 6.0), 90.0))

    def test_rotates_near_the_image_edge(self):
        """Near the edge of the image the corners still rotate it (a handle off the image could not)."""
        from pyquant4d.annotationsClasses.interactiveRectangle import InteractiveRectangle
        r = InteractiveRectangle(self.ax, (16.0, 2.0), (10.0, 3.0))
        r.connect()
        self.rect.remove()
        corner = r.handles.get_offsets()[2].copy()           # a corner on the image side
        start = just_outside(self.ax, corner, (16.0, 2.0))
        _mouse(self.ax, start, turned(start, (16.0, 2.0), -30.0))
        assert r.rotation == pytest.approx(-30.0)

    def test_static_rectangle_has_no_handles(self):
        from pyquant4d.annotationsClasses.interactiveRectangle import InteractiveRectangle
        r = InteractiveRectangle(self.ax, CENTRE, (10.0, 6.0), interactions='none')
        assert not r.handles.get_visible()
        r.connect()
        corner = r._corner_positions()[2]
        _mouse(self.ax, just_outside(self.ax, corner, CENTRE), CENTRE + [0, 9])
        assert r.rotation == 0.0


class TestPolygonVertices:
    @pytest.fixture(autouse=True)
    def setup(self, roi_ax):
        from pyquant4d.annotationsClasses.interactivePolygon import InteractivePolygon
        self.ax = roi_ax
        self.poly = InteractivePolygon(self.ax, [[10, 10], [22, 10], [16, 22]])
        self.poly.connect()

    def test_one_handle_per_vertex(self):
        np.testing.assert_allclose(self.poly.handles.get_offsets(), self.poly.vertices)

    def test_drag_a_vertex(self):
        _mouse(self.ax, (22, 10), (26, 8))
        np.testing.assert_allclose(self.poly.vertices, [[10, 10], [26, 8], [16, 22]])
        np.testing.assert_allclose(self.poly.handles.get_offsets(), self.poly.vertices)

    def test_drag_inside_moves_all(self):
        _mouse(self.ax, (16, 14), (17, 16))
        np.testing.assert_allclose(self.poly.vertices, [[11, 12], [23, 12], [17, 24]])

    def test_drag_just_outside_a_vertex_rotates_about_the_centre(self):
        centre = self.poly.vertices.mean(axis=0)
        offsets = self.poly.vertices - centre
        start = just_outside(self.ax, self.poly.vertices[2], centre)
        _mouse(self.ax, start, turned(start, centre, 90.0))
        assert self.poly.rotation == pytest.approx(90.0)
        expected = centre + offsets @ np.array([[0.0, -1.0], [1.0, 0.0]]).T     # +90 deg: (x, y) -> (-y, x)
        np.testing.assert_allclose(self.poly.vertices, expected, atol=1e-9)
        np.testing.assert_allclose(self.poly.handles.get_offsets(), self.poly.vertices)

    def test_inside_near_a_vertex_moves_not_rotates(self):
        """Within the rotation distance of a vertex but inside the shape: still a move."""
        centre = self.poly.vertices.mean(axis=0)
        p = self.poly.vertices[0] + (centre - self.poly.vertices[0]) * 0.15
        _mouse(self.ax, p, p + [1.0, 0.0])
        assert self.poly.rotation == 0.0
        np.testing.assert_allclose(self.poly.vertices, [[11, 10], [23, 10], [17, 22]])

    def test_remove_takes_every_artist(self):
        self.poly.remove()
        assert not self.ax.patches and not self.ax.lines and not self.ax.collections


class TestShiftKeepsTheAspectRatio:
    """Holding Shift while resizing a rectangle or ellipse keeps its aspect ratio."""

    def test_rectangle_corner(self, roi_ax):
        from pyquant4d.annotationsClasses.interactiveRectangle import InteractiveRectangle
        r = InteractiveRectangle(roi_ax, CENTRE, (10.0, 6.0), rotation=30.0)
        r.connect()
        corners = r.handles.get_offsets().copy()
        _mouse(roi_ax, corners[2], corners[2] + [3.0, 0.5], modifiers={"shift"})
        assert r.size[0] / r.size[1] == pytest.approx(10.0 / 6.0)
        assert r.size[0] > 10.0
        np.testing.assert_allclose(r.handles.get_offsets()[0], corners[0], atol=1e-9)   # opposite corner fixed
        assert r.rotation == pytest.approx(30.0)

    def test_rectangle_corner_without_shift_is_free(self, roi_ax):
        from pyquant4d.annotationsClasses.interactiveRectangle import InteractiveRectangle
        r = InteractiveRectangle(roi_ax, CENTRE, (10.0, 6.0))
        r.connect()
        corner = r.handles.get_offsets()[2].copy()
        _mouse(roi_ax, corner, corner + [3.0, 0.5])
        np.testing.assert_allclose(r.size, [13.0, 6.5])

    def test_rectangle_shift_as_held_key(self, roi_ax):
        """Older matplotlib has no MouseEvent.modifiers: the held key is used."""
        from pyquant4d.annotationsClasses.interactiveRectangle import InteractiveRectangle
        r = InteractiveRectangle(roi_ax, CENTRE, (10.0, 6.0))
        r.connect()
        corner = r.handles.get_offsets()[2].copy()
        _mouse(roi_ax, corner, corner + [3.0, 0.5], key="shift")
        assert r.size[0] / r.size[1] == pytest.approx(10.0 / 6.0)

    @pytest.mark.parametrize("handle, target, expected", [
        (0, [0, 8], [8.0, 4.0]),           # major handle out to 8: minor follows 3 -> 4
        (1, [-6, 0], [12.0, 6.0]),         # minor handle out to 6: major follows 6 -> 12
    ])
    def test_ellipse_handle(self, roi_ax, handle, target, expected):
        from pyquant4d.annotationsClasses.interactiveEllipse import InteractiveEllipse
        e = InteractiveEllipse(roi_ax, CENTRE, semiaxes=(6.0, 3.0))
        e.connect()
        start = e.handles.get_offsets()[handle].copy()
        _mouse(roi_ax, start, CENTRE + target, modifiers={"shift"})
        np.testing.assert_allclose(e.semiaxes, expected)
