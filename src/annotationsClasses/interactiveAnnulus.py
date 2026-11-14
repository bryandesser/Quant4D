"""
InteractiveAnnulus — a resizable two-ring (annular) detector overlay.

Thin subclass of InteractiveCircle with:
  • two concentric circles (inner ring, outer ring)
  • resize-only interactions (centre is locked to the beam centre)

The parent class already supports multiple radii and the 'resize' interaction
mode, so the only job here is to provide a clean constructor interface and
document the semantics clearly.

Signals (inherited)
-------------------
updateCircle : emitted whenever the user drags either ring handle
rightClick   : emitted on right-click events

Attributes (inherited, most useful ones)
-----------------------------------------
center : np.ndarray shape (2,)  — beam-centre in data units (read-only in
                                   this mode; use parent.center to read)
radius : np.ndarray shape (2,)  — [inner_radius, outer_radius] in data units
"""

from annotationsClasses.interactiveCircle import InteractiveCircle


class InteractiveAnnulus(InteractiveCircle):
    """
    Annular (ring) detector annotation with two concentric, resizable circles
    and a fixed centre.

    Parameters
    ----------
    axis          : matplotlib.axes.Axes
    center        : array-like, shape (2,)   — (x, y) in data units
    inner_radius  : float — inner ring radius in data units
    outer_radius  : float — outer ring radius in data units
    color         : matplotlib colour spec (default ``'r'``)
    """

    def __init__(self, axis, center, inner_radius, outer_radius, color='r'):
        super().__init__(
            axis,
            center=center,
            radius=[inner_radius, outer_radius],
            color=color,
            interactions='resize',      # centre is fixed to beam position
        )
