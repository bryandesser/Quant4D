"""
InteractiveRectangle — a draggable, resizable, rotatable rectangle annotation.

Used as MATLAB's rotatable ``images.roi.Rectangle``:

* drag inside               → move
* drag a corner             → resize, the opposite corner stays put (in the rectangle's own frame);
                              hold Shift to keep the aspect ratio
* drag just outside a corner → rotate about the centre; the cursor shows a curved double arrow there

Signals
-------
updateRect : emitted on every change while dragging, and once more on release
rightClick : emitted on right mouse button press

Public attributes
-----------------
center   : np.ndarray (2,)  — (cx, cy) in data coordinates
size     : np.ndarray (2,)  — (width, height) along the rectangle's own axes, always positive
rotation : float            — degrees from the data +x axis towards +y
patch    : matplotlib.patches.Polygon — the outline
handles  : PathCollection   — the four corner handles
"""
from __future__ import annotations

from typing import Any

import numpy as np
from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.backend_tools import Cursors
from matplotlib.patches import Polygon as MplPolygon
from PyQt5 import QtCore as qtc

from annotationsClasses._geometry import (corner_action, rotation_matrix, set_rotate_cursor, shift_held, to_local,
                                          turn)

_UNIT_CORNERS = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]], float) / 2.0   # in units of (w, h)


class InteractiveRectangle(qtc.QObject):
    """
    Parameters
    ----------
    axis         : matplotlib.axes.Axes
    center, size : (x, y) and (width, height) in data units
    rotation     : degrees (default 0, axis-aligned)
    color        : matplotlib colour spec
    interactions : str
        ``'all'`` (move, resize, rotate), ``'translate'``, ``'resize'`` (resize and rotate) or ``'none'``
    """

    updateRect = qtc.pyqtSignal()
    rightClick = qtc.pyqtSignal(MouseEvent)

    lock: 'InteractiveRectangle | None' = None    # only one rectangle is dragged at a time

    def __init__(self, axis, center, size, color: Any = 'r', interactions='all', rotation: float = 0.0):
        super().__init__()
        self.center = np.asarray(center, float).copy()
        self.size = np.abs(np.asarray(size, float)).copy()
        self.rotation = float(rotation)
        self.color = color
        self.interactions = interactions
        self.axis = axis
        self.canvas = axis.figure.canvas
        self._press = None          # (center0, size0, rotation0, x0, y0) while dragging
        self._transform = None      # 'translate' | 'resize_<corner>' | 'rotate'

        self.patch = axis.add_patch(MplPolygon(
            self._corner_positions(), closed=True, linewidth=1.5, edgecolor=color, facecolor='none',
            animated=False))
        c = self._corner_positions()
        self.handles = axis.scatter(c[:, 0], c[:, 1], color=[color], s=40, zorder=5, animated=False)
        if interactions in ('none', 'translate'):
            self.handles.set_visible(False)
        self.background = None      # taken when a drag starts
        self.canvas.draw_idle()

    # ------------------------------------------------------------------ geometry
    def _corner_positions(self) -> np.ndarray:
        """(4, 2) corners, in the order (-w,-h), (+w,-h), (+w,+h), (-w,+h) of the rectangle's own frame."""
        return self.center + (_UNIT_CORNERS * self.size) @ rotation_matrix(self.rotation).T

    def _inside(self, x, y) -> bool:
        lx, ly = to_local((x, y), self.center, self.rotation)[0]
        return abs(lx) <= self.size[0] / 2.0 and abs(ly) <= self.size[1] / 2.0

    def _hit(self, event) -> str | None:
        """The action under the mouse: 'resize_<i>', 'rotate', 'translate' or None."""
        inside = event.xdata is not None and event.ydata is not None and self._inside(event.xdata, event.ydata)
        if self.interactions in ('all', 'resize') and self.handles.get_visible():
            what, i = corner_action(self.axis, self._corner_positions(), event, inside)
            if what == 'corner':
                return f'resize_{i}'
            if what == 'rotate':
                return 'rotate'
        if self.interactions in ('all', 'translate') and inside:
            return 'translate'
        return None

    def _set_cursor(self, hit):
        if hit == 'rotate':
            set_rotate_cursor(self.canvas)
        else:
            self.canvas.set_cursor(Cursors.POINTER if hit is None else
                                   Cursors.MOVE if hit == 'translate' else Cursors.HAND)

    def _update_artists(self):
        c = self._corner_positions()
        self.patch.set_xy(c)
        self.handles.set_offsets(c)

    def _artists(self):
        return [self.patch] + ([self.handles] if self.handles.get_visible() else [])

    # ------------------------------------------------------------------ public API
    def connect(self):
        self._cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self._cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self._cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def disconnect(self):
        """Stop listening to the mouse (a removed annotation must not react any more)."""
        for name in ('_cidpress', '_cidrelease', '_cidmotion'):
            cid = getattr(self, name, None)
            if cid is not None and self.canvas is not None:
                self.canvas.mpl_disconnect(cid)
            setattr(self, name, None)
        if InteractiveRectangle.lock is self:
            InteractiveRectangle.lock = None

    def remove(self):
        self.disconnect()
        self.patch.remove()
        self.handles.remove()

    def redraw(self):
        self._update_artists()
        self.restoreBackground()

    def restoreBackground(self):
        if not self.dragging:       # outside a drag a saved background is stale: plain redraw
            self.canvas.draw_idle()
            return
        self.canvas.restore_region(self.background)
        for a in self._artists():
            self.axis.draw_artist(a)
        self.canvas.blit(self.axis.bbox)

    def updateBackground(self):
        self.canvas.draw_idle()

    @property
    def dragging(self) -> bool:
        return self._press is not None

    # ------------------------------------------------------------------ events
    def on_press(self, event):
        if event.button == MouseButton.RIGHT:
            self.rightClick.emit(event)
            return
        if (self.interactions == 'none' or event.inaxes != self.axis or InteractiveRectangle.lock is not None
                or event.xdata is None or event.ydata is None):
            return
        self._transform = self._hit(event)
        if self._transform is None:
            return
        self._set_cursor(self._transform)
        self._press = (self.center.copy(), self.size.copy(), self.rotation, event.xdata, event.ydata)
        InteractiveRectangle.lock = self
        for a in self._artists():
            a.set_animated(True)
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.axis.bbox)
        self.restoreBackground()

    def on_motion(self, event):
        if event.inaxes != self.axis:
            return
        if InteractiveRectangle.lock is not self:                   # hover feedback
            if event.xdata is None or event.ydata is None or InteractiveRectangle.lock is not None \
                    or self.interactions == 'none':
                return
            self._set_cursor(self._hit(event))
            return
        if self._press is None or event.xdata is None or event.ydata is None:
            return
        center0, size0, rotation0, x0, y0 = self._press
        p = np.array([event.xdata, event.ydata])
        if self._transform == 'translate':
            self.center = center0 + p - np.array([x0, y0])
        elif self._transform == 'rotate':
            self.rotation = rotation0 + turn(center0, (x0, y0), p)
        elif self._transform is not None and self._transform.startswith('resize_'):
            i = int(self._transform[-1])
            R = rotation_matrix(rotation0)
            corners0 = center0 + (_UNIT_CORNERS * size0) @ R.T
            fixed = corners0[(i + 2) % 4]                 # the opposite corner stays put
            new = corners0[i] + p - np.array([x0, y0])
            span = R.T @ (new - fixed)                    # diagonal in the rectangle's own frame
            if shift_held(event) and size0.min() > 0:
                # Shift: keep the aspect ratio, scaled to the larger of the two stretches
                scale = max(abs(span[0]) / size0[0], abs(span[1]) / size0[1])
                span = np.where(span < 0, -1.0, 1.0) * size0 * scale
                new = fixed + R @ span
            if abs(span[0]) > 1e-6 and abs(span[1]) > 1e-6:
                self.size = np.abs(span)
                self.center = (new + fixed) / 2.0
        self._update_artists()
        self.restoreBackground()
        self.updateRect.emit()

    def on_release(self, event):
        if InteractiveRectangle.lock is not self:
            return
        self._press = None
        self._transform = None
        InteractiveRectangle.lock = None
        self.patch.set_animated(False)
        self.handles.set_animated(False)
        self.canvas.draw()
        self.updateRect.emit()      # final update after the drag (Reduced calculation policy)
