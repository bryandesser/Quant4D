"""callbacks.scale_bar: round lengths, units, and a bar that follows zoom and view rotation."""
import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from callbacks.scale_bar import ScaleBar, nice_length  # noqa: E402


@pytest.mark.parametrize("target, units, expected", [
    (12, "nm", (10, "nm", 10)),
    (0.37, "nm", (200, "pm", 0.2)),
    (2500, "nm", (2, "µm", 2000)),
    (0.37, "A", (20, "pm", 0.2)),
    (37, "A", (2, "nm", 20)),
    (7, "px", (5, "px", 5)),
    (7, "pixels", (5, "px", 5)),
    (3.3, "mrad", (2, "mrad", 2)),
    (1.0, "mrad", (1, "mrad", 1)),
])
def test_nice_length(target, units, expected):
    shown, unit, length = nice_length(target, units)
    assert shown == pytest.approx(expected[0]) and unit == expected[1]
    assert length == pytest.approx(expected[2])
    assert length <= target * (1 + 1e-9)


@pytest.mark.parametrize("bad", [0, -1, float("nan"), float("inf")])
def test_nice_length_refuses(bad):
    with pytest.raises(ValueError):
        nice_length(bad, "nm")


@pytest.fixture()
def axes():
    fig = plt.figure(figsize=(5, 5), dpi=100)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.imshow(np.zeros((100, 100)))
    yield fig, ax
    plt.close(fig)


def _draw(fig, bar):
    fig.canvas.draw()
    return bar.label, bar.length_px


def test_bar_length_and_label(axes):
    fig, ax = axes                                   # 100 px image over 500 display px: 5 display px / px
    bar = ScaleBar(lambda: (0.1, "nm"))
    ax.add_artist(bar)
    label, length = _draw(fig, bar)                  # target a fifth: 100 display px = 2 nm
    assert label == "2 nm" and length == pytest.approx(100)


def test_bar_follows_zoom(axes):
    fig, ax = axes
    bar = ScaleBar(lambda: (0.1, "nm"))
    ax.add_artist(bar)
    ax.set_xlim(-0.5, 49.5)
    ax.set_ylim(49.5, -0.5)                          # 2x zoom: 10 display px per image pixel
    assert _draw(fig, bar) == ("1 nm", pytest.approx(100))


def test_bar_same_in_rotated_and_flipped_views(axes):
    from callbacks.axis_direction import set_view
    fig, ax = axes
    bar = ScaleBar(lambda: (0.1, "nm"))
    ax.add_artist(bar)
    before = _draw(fig, bar)
    set_view(ax, reverse_x=True, reverse_y=True, rotation=90)
    assert _draw(fig, bar) == before


def test_bar_scales_with_dpi(axes, tmp_path):
    fig, ax = axes
    bar = ScaleBar(lambda: (0.1, "nm"))
    ax.add_artist(bar)
    fig.savefig(tmp_path / "x.png", dpi=200)          # twice the pixels: same label, twice the length
    assert bar.label == "2 nm" and bar.length_px == pytest.approx(200)


@pytest.mark.parametrize("scale", [None, (0, "nm"), (-1, "nm")])
def test_nothing_drawn_without_a_scale(axes, scale):
    fig, ax = axes
    bar = ScaleBar(lambda: scale)
    ax.add_artist(bar)
    assert _draw(fig, bar) == ("", 0.0)


def test_hidden(axes):
    fig, ax = axes
    bar = ScaleBar(lambda: (1, "px"))
    ax.add_artist(bar)
    bar.set_visible(False)
    assert _draw(fig, bar) == ("", 0.0)
