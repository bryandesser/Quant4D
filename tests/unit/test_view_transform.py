"""Orientation transform of image axes (callbacks.axis_direction), no Qt."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

from callbacks.axis_direction import install_view_transform, mirrored, rotate_about, screen_directions, set_view  # noqa: E402

NY, NX = 16, 24


@pytest.fixture()
def ax():
    fig, ax = plt.subplots(figsize=(4, 4))
    install_view_transform(ax)
    ax.imshow(np.zeros((NY, NX)))
    fig.canvas.draw()
    yield ax
    plt.close(fig)


# screen directions (pixels, y up) of data +x and +y for each setting
CASES = [
    ((False, True, 0), (1, 0), (0, -1)),       # default: x right, y down
    ((True, True, 0), (-1, 0), (0, -1)),       # reverse x
    ((False, False, 0), (1, 0), (0, 1)),       # y up
    ((False, True, 180), (-1, 0), (0, 1)),
    ((False, True, 90), (0, -1), (-1, 0)),     # clockwise: +x (right) turns to point down
    ((False, True, -90), (0, 1), (1, 0)),
    ((True, True, 90), (0, 1), (-1, 0)),       # flip x first, then rotate
]


@pytest.mark.parametrize("setting, dx, dy", CASES)
def test_directions(ax, setting, dx, dy):
    set_view(ax, *setting)
    ax.figure.canvas.draw()
    d = screen_directions(ax, [(1, 0), (0, 1)])
    assert np.allclose(d, [dx, dy], atol=1e-9)


@pytest.mark.parametrize("rot", [0, 90, 180, -90])
def test_picking_round_trip(ax, rot):
    """Mouse events map back to the same data point whatever the orientation."""
    set_view(ax, True, False, rot)
    ax.figure.canvas.draw()
    p = np.array([20.0, 12.0])
    assert np.allclose(ax.transData.inverted().transform(ax.transData.transform(p)), p)


def test_rotated_box_has_equal_scale(ax):
    set_view(ax, False, True, 90)
    ax.figure.canvas.draw()
    p0, px, py = ax.transData.transform([(0, 0), (1, 0), (0, 1)])
    assert np.isclose(np.linalg.norm(px - p0), np.linalg.norm(py - p0), rtol=1e-3), "non-square pixels"
    assert ax.bbox.height > ax.bbox.width, "a 24 x 16 image rotated by 90° is taller than wide"
    ax.set_xlim(2, 10)                                    # zooming keeps the scale equal
    ax.figure.canvas.draw()
    p0, px, py = ax.transData.transform([(0, 0), (1, 0), (0, 1)])
    assert np.isclose(np.linalg.norm(px - p0), np.linalg.norm(py - p0), rtol=1e-3)


def test_survives_cla(ax):
    set_view(ax, True, True, 0)
    ax.cla()
    install_view_transform(ax)
    set_view(ax, True, True, 0)
    ax.imshow(np.zeros((NY, NX)))
    ax.figure.canvas.draw()
    assert np.allclose(screen_directions(ax, [(1, 0)]), [(-1, 0)])


def test_bad_rotation(ax):
    with pytest.raises(ValueError):
        set_view(ax, False, True, 45)


def test_mirrored_and_rotate_about():
    assert not mirrored(False, True) and mirrored(True, True) and mirrored(False, False) and not mirrored(True, False)
    # +90 in pixel coordinates (y down) takes +x to +y, i.e. clockwise on screen
    assert np.allclose(rotate_about([[13.0, 10.0]], [10.0, 10.0], 90), [[10.0, 13.0]])
