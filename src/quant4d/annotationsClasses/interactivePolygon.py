"""
InteractivePolygon — an editable, draggable, rotatable closed-polygon annotation.

After vertices are obtained from matplotlib's PolygonSelector (which handles
the interactive drawing), this class wraps the result in an editable patch,
used as MATLAB's ``images.roi.Polygon``:

* drag a vertex handle            → move that vertex
* drag just outside a vertex      → rotate about the centre (the mean of the vertices);
                                    the cursor shows a curved double arrow there
* drag inside                     → move the whole polygon

Signals
-------
updatePoly : emitted on every change while dragging, and once more on release
rightClick : emitted on right mouse button press

Public attributes
-----------------
vertices : np.ndarray, shape (N, 2)  — polygon vertices in data coordinates
rotation : float — degrees turned so far (informative; the vertices carry the shape)
patch    : matplotlib.patches.Polygon
handles  : PathCollection — one handle per vertex
"""

from __future__ import annotations

from typing import Any

import numpy as np
from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.backend_tools import Cursors
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.path import Path
from PyQt5 import QtCore as qtc

from ._geometry import corner_action, rotation_matrix, set_rotate_cursor, turn


class InteractivePolygon(qtc.QObject):
    """
    Parameters
    ----------
    axis     : matplotlib.axes.Axes
    vertices : array-like, shape (N, 2)  — (x, y) in data units
    color    : matplotlib colour spec (default ``'r'``)
    """

    updatePoly = qtc.pyqtSignal()
    rightClick = qtc.pyqtSignal(MouseEvent)

    lock: 'InteractivePolygon | None' = None    # only one polygon is dragged at a time

    def __init__(self, axis, vertices, color: Any = 'r'):
        super().__init__()
        self.vertices = np.asarray(vertices, float).copy()
        self.rotation = 0.0
        self.color = color
        self.axis = axis
        self.canvas = axis.figure.canvas
        self._press = None      # (vertices0, rotation0, xpress, ypress) while dragging
        self._transform = None  # 'translate' | 'vertex_<i>' | 'rotate'

        self.patch = axis.add_patch(MplPolygon(
            self.vertices, closed=True, animated=False,
            linewidth=1.5, edgecolor=color, facecolor='none'))
        self.handles = axis.scatter(self.vertices[:, 0], self.vertices[:, 1], color=[color], s=30,
                                    zorder=5, animated=False)
        self.background = None  # taken when a drag starts
        self.companions: Any = None  # callable → artists that move with the polygon (drawn while dragged)
        self.canvas.draw_idle()

    # ------------------------------------------------------------------ geometry
    def _contains_point(self, x: float, y: float) -> bool:
        closed_verts = np.vstack([self.vertices, self.vertices[0]])
        return Path(closed_verts).contains_point((x, y))

    def _hit(self, event) -> str | None:
        """The action under the mouse: 'vertex_<i>', 'rotate', 'translate' or None."""
        inside = (event.xdata is not None and event.ydata is not None
                  and self._contains_point(event.xdata, event.ydata))
        if self.handles.get_visible():
            what, i = corner_action(self.axis, self.vertices, event, inside)
            if what == 'corner':
                return f'vertex_{i}'
            if what == 'rotate':
                return 'rotate'
        return 'translate' if inside else None

    def _set_cursor(self, hit):
        if hit == 'rotate':
            set_rotate_cursor(self.canvas)
        else:
            self.canvas.set_cursor(Cursors.POINTER if hit is None else
                                   Cursors.MOVE if hit == 'translate' else Cursors.HAND)

    def _update_artists(self):
        self.patch.set_xy(self.vertices)
        self.handles.set_offsets(self.vertices)

    def _companionArtists(self):
        try:
            return [a for a in (self.companions() if self.companions is not None else []) if a is not None]
        except (AttributeError, TypeError):
            return []

    def _artists(self):
        own = [self.patch] + ([self.handles] if self.handles.get_visible() else [])
        return [a for a in self._companionArtists() if a.get_visible() and a.axes is self.axis] + own

    # ------------------------------------------------------------------ public API
    def connect(self):
        """Connect matplotlib mouse events."""
        self._cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self._cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self._cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def disconnect(self):
        """Stop listening to the mouse.  A removed annotation that kept its handlers went on reacting
        to every hover/click on the canvas (drawing artists no longer in a figure, emitting moves)."""
        for name in ('_cidpress', '_cidrelease', '_cidmotion'):
            cid = getattr(self, name, None)
            if cid is not None and self.canvas is not None:
                self.canvas.mpl_disconnect(cid)
            setattr(self, name, None)
        if InteractivePolygon.lock is self:
            InteractivePolygon.lock = None

    def remove(self):
        """Remove the artists from the axes and stop listening to the mouse."""
        self.disconnect()
        self.patch.remove()
        self.handles.remove()

    def redraw(self):
        """Sync the artists to the current vertices and repaint."""
        self._update_artists()
        self.restoreBackground()

    def restoreBackground(self):
        # Outside a drag the saved background is stale (the image may have changed since it was
        # taken, e.g. brightness/contrast), so blitting it would paint the old image back: redraw.
        if not self.dragging:
            self.canvas.draw_idle()
            return
        self.canvas.restore_region(self.background)
        for a in self._artists():
            self.axis.draw_artist(a)
        self.canvas.blit(self.axis.bbox)

    def updateBackground(self):
        """Redraw the canvas (kept for compatibility; the background is taken when a drag starts)."""
        self.canvas.draw_idle()

    @property
    def dragging(self) -> bool:
        """True while the user is dragging this polygon."""
        return self._press is not None

    # ------------------------------------------------------------------ events
    def on_press(self, event):
        if event.button == MouseButton.RIGHT:
            self.rightClick.emit(event)
            return
        if (event.inaxes != self.axis or InteractivePolygon.lock is not None
                or event.xdata is None or event.ydata is None or not self.patch.get_visible()):
            return
        self._transform = self._hit(event)
        if self._transform is None:
            return
        self._press = (self.vertices.copy(), self.rotation, event.xdata, event.ydata)
        InteractivePolygon.lock = self
        self._set_cursor(self._transform)
        # the companions (mask outline) are left out of the background too, or their old position
        # would stay painted there until the release
        for a in self._artists() + self._companionArtists():
            a.set_animated(True)
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.axis.bbox)
        self.restoreBackground()

    def on_motion(self, event):
        if event.inaxes != self.axis:
            return
        if InteractivePolygon.lock is not self:                     # hover feedback
            if event.xdata is None or event.ydata is None or InteractivePolygon.lock is not None \
                    or not self.patch.get_visible():
                return
            self._set_cursor(self._hit(event))
            return
        if self._press is None or event.xdata is None or event.ydata is None:
            return
        verts0, rotation0, xpress, ypress = self._press
        now = np.array([event.xdata, event.ydata])
        if self._transform == 'translate':
            self.vertices = verts0 + now - (xpress, ypress)
        elif self._transform == 'rotate':
            c = verts0.mean(axis=0)
            angle = turn(c, (xpress, ypress), now)
            self.vertices = c + (verts0 - c) @ rotation_matrix(angle).T
            self.rotation = rotation0 + angle
        elif self._transform is not None and self._transform.startswith('vertex_'):
            self.vertices = verts0.copy()
            self.vertices[int(self._transform.split('_')[1])] += now - (xpress, ypress)
        self._update_artists()
        self.restoreBackground()
        self.updatePoly.emit()

    def on_release(self, event):
        if InteractivePolygon.lock is not self:
            return
        self._press = None
        self._transform = None
        InteractivePolygon.lock = None
        self.patch.set_animated(False)
        self.handles.set_animated(False)
        for a in self._companionArtists():
            a.set_animated(False)
        self.canvas.draw()
        self.updatePoly.emit()     # final update after the drag (Reduced calculation policy)
