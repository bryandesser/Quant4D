"""
InteractivePolygon — a draggable, closed-polygon annotation.

After vertices are obtained from matplotlib's PolygonSelector (which handles
the interactive drawing), this class wraps the result in a draggable patch
so the whole polygon can be translated by click-and-drag inside the shape.

Signals
-------
updatePoly : emitted whenever the polygon is moved (on_motion)
rightClick : emitted on right mouse button press

Public attributes
-----------------
vertices : np.ndarray, shape (N, 2)  — polygon vertices in data coordinates
patch    : matplotlib.patches.Polygon
"""

from __future__ import annotations

import numpy as np
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.path import Path
from matplotlib.backend_bases import MouseButton
from matplotlib.backend_bases import MouseEvent
from matplotlib.backend_tools import Cursors
from PyQt5 import QtCore as qtc


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
    rightClick  = qtc.pyqtSignal(MouseEvent)

    # Only one InteractivePolygon may be dragged at a time
    lock: 'InteractivePolygon | None' = None

    def __init__(self, axis, vertices, color='r'):
        super().__init__()

        self.vertices = np.asarray(vertices, float)
        self.color    = color
        self.axis     = axis
        self._press   = None   # (vertices0, xpress, ypress)

        # ---- Closed polygon patch ------------------------------------
        self.patch = axis.add_patch(MplPolygon(
            self.vertices,
            closed=True, animated=True,
            linewidth=1.5, edgecolor=color, facecolor='none',
        ))

        # ---- Blitting setup -----------------------------------------
        self.canvas = axis.figure.canvas
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(axis.bbox)

    # ==================================================================
    # Geometry helpers
    # ==================================================================

    def _contains_point(self, x: float, y: float) -> bool:
        """Return True if (x, y) is inside the polygon (using matplotlib Path)."""
        closed_verts = np.vstack([self.vertices, self.vertices[0]])
        return Path(closed_verts).contains_point((x, y))

    def _update_artists(self):
        self.patch.set_xy(self.vertices)

    # ==================================================================
    # Public API  (mirrors InteractiveCircle / InteractiveRectangle)
    # ==================================================================

    def connect(self):
        """Connect matplotlib mouse events."""
        self._cidpress   = self.canvas.mpl_connect('button_press_event',   self.on_press)
        self._cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self._cidmotion  = self.canvas.mpl_connect('motion_notify_event',  self.on_motion)

    def remove(self):
        """Remove polygon patch from the axes."""
        self.patch.remove()

    def redraw(self):
        """Sync patch to current vertices and blit."""
        self._update_artists()
        self.restoreBackground()

    def restoreBackground(self):
        """Blit: restore saved background then redraw patch."""
        self.canvas.restore_region(self.background)
        self.axis.draw_artist(self.patch)
        self.canvas.blit(self.axis.bbox)

    def updateBackground(self):
        """Full redraw, capture new background, then blit patch."""
        self.patch.set_animated(True)
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.axis.bbox)
        self.axis.draw_artist(self.patch)
        self.canvas.blit(self.axis.bbox)

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
        if not self._contains_point(event.xdata, event.ydata):
            return

        self._press = (self.vertices.copy(), event.xdata, event.ydata)
        InteractivePolygon.lock = self
        self.canvas.set_cursor(Cursors.MOVE)

        # Prepare blit background
        self.patch.set_animated(True)
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.axis.bbox)
        self.axis.draw_artist(self.patch)
        self.canvas.blit(self.axis.bbox)

    def on_motion(self, event):
        if event.inaxes != self.axis:
            return

        # ---- Hover cursor feedback (no drag) -------------------------
        if InteractivePolygon.lock is not self:
            if event.xdata is not None and event.ydata is not None:
                if self._contains_point(event.xdata, event.ydata):
                    self.canvas.set_cursor(Cursors.MOVE)
                else:
                    self.canvas.set_cursor(Cursors.POINTER)
            return

        # ---- Active drag ---------------------------------------------
        if self._press is None or event.xdata is None:
            return

        verts0, xpress, ypress = self._press
        dx = event.xdata - xpress
        dy = event.ydata - ypress

        self.vertices = verts0 + np.array([dx, dy])
        self._update_artists()
        self.restoreBackground()
        self.updatePoly.emit()

    def on_release(self, event):
        if InteractivePolygon.lock is not self:
            return
        self._press = None
        InteractivePolygon.lock = None

        self.patch.set_animated(False)
        self.canvas.draw()
