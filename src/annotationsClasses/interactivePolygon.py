"""
InteractivePolygon — a draggable, closed-polygon annotation.

After vertices are obtained from matplotlib's PolygonSelector (which handles
the interactive drawing), this class wraps the result in an editable patch:
drag a vertex handle to move that vertex, drag inside the shape to move it all.

Signals
-------
updatePoly : emitted on every change while dragging, and once more on release
rightClick : emitted on right mouse button press

Public attributes
-----------------
vertices : np.ndarray, shape (N, 2)  — polygon vertices in data coordinates
patch    : matplotlib.patches.Polygon
handles  : matplotlib.collections.PathCollection — one handle per vertex
"""

from __future__ import annotations

from typing import Any

import numpy as np
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.path import Path
from matplotlib.backend_bases import MouseButton
from matplotlib.backend_bases import MouseEvent
from matplotlib.backend_tools import Cursors
from PyQt5 import QtCore as qtc

from annotationsClasses._geometry import HANDLE_PICK_PX, nearest_handle


class InteractivePolygon(qtc.QObject):
    """
    Draggable polygon annotation.

    Parameters
    ----------
    axis     : matplotlib.axes.Axes
    vertices : array-like, shape (N, 2)  — (x, y) in data units
    color    : matplotlib colour spec (default ``'r'``)
    """

    updatePoly = qtc.pyqtSignal()
    rightClick = qtc.pyqtSignal(MouseEvent)

    # Only one InteractivePolygon may be dragged at a time
    lock: 'InteractivePolygon | None' = None

    def __init__(self, axis, vertices, color: Any = 'r'):
        super().__init__()

        self.vertices = np.asarray(vertices, float)
        self.color = color
        self.axis = axis
        self._press = None   # (vertices0, xpress, ypress)
        self._vertex = -1    # index of the vertex being dragged; -1 moves the whole polygon

        # ---- Closed polygon patch ------------------------------------
        self.patch = axis.add_patch(MplPolygon(
            self.vertices,
            closed=True, animated=False,     # animated only while dragged
            linewidth=1.5, edgecolor=color, facecolor='none',
        ))
        self.handles = axis.scatter(self.vertices[:, 0], self.vertices[:, 1], color=[color], s=30,
                                    zorder=5, animated=False)

        # ---- Blitting setup -----------------------------------------
        self.canvas = axis.figure.canvas
        # Ordinary artists, drawn by every redraw; they are animated (blitted) only while dragged.
        self.background = None                  # taken when a drag starts
        self.canvas.draw_idle()

    # ==================================================================
    # Geometry helpers
    # ==================================================================

    def _contains_point(self, x: float, y: float) -> bool:
        """Return True if (x, y) is inside the polygon (using matplotlib Path)."""
        closed_verts = np.vstack([self.vertices, self.vertices[0]])
        return Path(closed_verts).contains_point((x, y))

    def _hit_vertex(self, event) -> int:
        """Index of the vertex handle under the mouse, or -1."""
        if not self.handles.get_visible():
            return -1
        i, d = nearest_handle(self.axis, self.vertices, event)
        return i if d <= HANDLE_PICK_PX else -1

    def _update_artists(self):
        self.patch.set_xy(self.vertices)
        self.handles.set_offsets(self.vertices)

    # ==================================================================
    # Public API  (mirrors InteractiveCircle / InteractiveRectangle)
    # ==================================================================

    def connect(self):
        """Connect matplotlib mouse events."""
        self._cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self._cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self._cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def disconnect(self):
        """Stop listening to the mouse.  A removed annotation that kept its handlers went on reacting
        to every hover/click on the canvas (drawing artists no longer in a figure, emitting moves)."""
        canvas = self.canvas
        for name in ('_cidpress', '_cidrelease', '_cidmotion'):
            cid = getattr(self, name, None)
            if cid is not None and canvas is not None:
                canvas.mpl_disconnect(cid)
            setattr(self, name, None)
        if InteractivePolygon.lock is self:
            InteractivePolygon.lock = None

    def remove(self):
        """Remove polygon patch from the axes and stop listening to the mouse."""
        self.disconnect()
        self.patch.remove()
        self.handles.remove()

    def redraw(self):
        """Sync patch to current vertices and blit."""
        self._update_artists()
        self.restoreBackground()

    def restoreBackground(self):
        """Blit: restore saved background then redraw patch."""
        # Outside a drag the saved background is stale (the image may have changed since it was
        # taken, e.g. brightness/contrast), so blitting it would paint the old image back: redraw.
        if not self.dragging:
            self.canvas.draw_idle()
            return
        self.canvas.restore_region(self.background)
        self.axis.draw_artist(self.patch)
        if self.handles.get_visible():
            self.axis.draw_artist(self.handles)
        self.canvas.blit(self.axis.bbox)

    def updateBackground(self):
        """Redraw the canvas (kept for compatibility; the background is taken when a drag starts)."""
        self.canvas.draw_idle()

    # ==================================================================
    # Event handlers
    # ==================================================================

    def on_press(self, event):
        if event.button == MouseButton.RIGHT:
            self.rightClick.emit(event)
            return
        if event.inaxes != self.axis:
            return
        if InteractivePolygon.lock is not None:
            return
        if event.xdata is None or event.ydata is None:
            return
        self._vertex = self._hit_vertex(event)
        if self._vertex < 0 and not self._contains_point(event.xdata, event.ydata):
            return

        self._press = (self.vertices.copy(), event.xdata, event.ydata)
        InteractivePolygon.lock = self
        self.canvas.set_cursor(Cursors.HAND if self._vertex >= 0 else Cursors.MOVE)

        # Prepare blit background
        self.patch.set_animated(True)
        self.handles.set_animated(True)
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.axis.bbox)
        self.restoreBackground()

    def on_motion(self, event):
        if event.inaxes != self.axis:
            return

        # ---- Hover cursor feedback (no drag) -------------------------
        if InteractivePolygon.lock is not self:
            if event.xdata is not None and event.ydata is not None:
                if self._hit_vertex(event) >= 0:
                    self.canvas.set_cursor(Cursors.HAND)
                elif self._contains_point(event.xdata, event.ydata):
                    self.canvas.set_cursor(Cursors.MOVE)
                else:
                    self.canvas.set_cursor(Cursors.POINTER)
            return

        # ---- Active drag ---------------------------------------------
        if self._press is None or event.xdata is None or event.ydata is None:
            return

        verts0, xpress, ypress = self._press
        shift = np.array([event.xdata - xpress, event.ydata - ypress])

        self.vertices = verts0.copy()
        if self._vertex >= 0:
            self.vertices[self._vertex] += shift
        else:
            self.vertices += shift
        self._update_artists()
        self.restoreBackground()
        self.updatePoly.emit()

    def on_release(self, event):
        if InteractivePolygon.lock is not self:
            return
        self._press = None
        self._vertex = -1
        InteractivePolygon.lock = None

        self.patch.set_animated(False)
        self.handles.set_animated(False)
        self.canvas.draw()
        self.updatePoly.emit()     # final update after the drag (Reduced calculation policy)

    @property
    def dragging(self) -> bool:
        """True while the user is dragging this polygon."""
        return self._press is not None
