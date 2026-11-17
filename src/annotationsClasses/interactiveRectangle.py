"""
InteractiveRectangle — a draggable, resizable, rotatable rectangle annotation.

* drag inside      → move
* drag a corner    → resize, the opposite corner stays put (in the rectangle's own frame)
* drag the handle on the stalk beyond one side → rotate about the centre

Signals
-------
updateRect : emitted on every change while dragging, and once more on release
rightClick : emitted on right mouse button press

Public attributes
-----------------
center    : np.ndarray (2,)  — (cx, cy) in data coordinates
size      : np.ndarray (2,)  — (width, height) along the rectangle's own axes, always positive
rotation  : float            — degrees from the data +x axis towards +y
patch     : matplotlib.patches.Polygon — the outline
handles   : PathCollection   — the four corner handles
rotHandle : PathCollection   — the rotation handle;  rotStalk : Line2D joining it to the side
"""
from __future__ import annotations

from typing import Any

import numpy as np
from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.backend_tools import Cursors
from matplotlib.patches import Polygon as MplPolygon
from PyQt5 import QtCore as qtc

from annotationsClasses._geometry import HANDLE_PICK_PX, nearest_handle, rotation_matrix, to_local

_UNIT_CORNERS = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]], float) / 2.0   # in units of (w, h)


class InteractiveRectangle(qtc.QObject):
    """
    Parameters
    ----------
    axis         : matplotlib.axes.Axes
    center, size : (x, y) and (width, height) in data units
    rotation     : degrees (default 0, axis-aligned)
    color        : matplotlib colour spec
    interactions : ``'all'`` (move, resize, rotate) | ``'translate'`` | ``'resize'`` (resize, rotate) | ``'none'``
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
        stalk = np.array([self._side_midpoint(), self._rot_handle_position()])
        self.rotStalk, = axis.plot(stalk[:, 0], stalk[:, 1], color=color, linewidth=1, animated=False)
        r = self._rot_handle_position()
        self.rotHandle = axis.scatter([r[0]], [r[1]], color=[color], s=40, marker='o', zorder=5,
                                      facecolors='none', linewidths=1.5, animated=False)
        if interactions in ('none', 'translate'):
            for a in (self.handles, self.rotStalk, self.rotHandle):
                a.set_visible(False)
        self.background = None      # taken when a drag starts
        self.canvas.draw_idle()

    # ------------------------------------------------------------------ geometry
    def _corner_positions(self) -> np.ndarray:
        """(4, 2) corners, in the order (-w,-h), (+w,-h), (+w,+h), (-w,+h) of the rectangle's own frame."""
        return self.center + (_UNIT_CORNERS * self.size) @ rotation_matrix(self.rotation).T

    def _stalk_length(self) -> float:
        """A fixed fraction of the visible axes, so the rotation handle stays reachable at any size."""
        return 0.08 * max(float(np.ptp(self.axis.get_xlim())), float(np.ptp(self.axis.get_ylim())))

    def _side_midpoint(self) -> np.ndarray:
        return self.center + rotation_matrix(self.rotation) @ np.array([0.0, -self.size[1] / 2.0])

    def _rot_handle_position(self) -> np.ndarray:
        return self.center + rotation_matrix(self.rotation) @ np.array(
            [0.0, -(self.size[1] / 2.0 + self._stalk_length())])

    def _inside(self, x, y) -> bool:
        lx, ly = to_local((x, y), self.center, self.rotation)[0]
        return abs(lx) <= self.size[0] / 2.0 and abs(ly) <= self.size[1] / 2.0

    def _hit(self, event) -> str | None:
        """The part of the rectangle under the mouse: 'rotate', 'resize_<i>', 'translate' or None."""
        if self.interactions in ('all', 'resize') and self.handles.get_visible():
            _, d = nearest_handle(self.axis, [self._rot_handle_position()], event)
            if d <= HANDLE_PICK_PX:
                return 'rotate'
            i, d = nearest_handle(self.axis, self._corner_positions(), event)
            if d <= HANDLE_PICK_PX:
                return f'resize_{i}'
        if self.interactions in ('all', 'translate') and event.xdata is not None and event.ydata is not None \
                and self._inside(event.xdata, event.ydata):
            return 'translate'
        return None

    def _update_artists(self):
        c = self._corner_positions()
        self.patch.set_xy(c)
        self.handles.set_offsets(c)
        stalk = np.array([self._side_midpoint(), self._rot_handle_position()])
        self.rotStalk.set_data(stalk[:, 0], stalk[:, 1])
        self.rotHandle.set_offsets(stalk[1:])

    def _artists(self):
        return [self.patch] + [a for a in (self.rotStalk, self.handles, self.rotHandle) if a.get_visible()]

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
        for a in (self.patch, self.handles, self.rotStalk, self.rotHandle):
            a.remove()

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
        self.canvas.set_cursor(Cursors.MOVE if self._transform == 'translate' else Cursors.HAND)
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
            if event.xdata is None or event.ydata is None:
                return
            hit = self._hit(event)
            self.canvas.set_cursor(Cursors.POINTER if hit is None else
                                   Cursors.MOVE if hit == 'translate' else Cursors.HAND)
            return
        if self._press is None or event.xdata is None or event.ydata is None:
            return
        center0, size0, rotation0, x0, y0 = self._press
        p = np.array([event.xdata, event.ydata])
        if self._transform == 'translate':
            self.center = center0 + p - np.array([x0, y0])
        elif self._transform == 'rotate':
            v = p - center0
            # the handle lies along the rectangle's own -y axis
            self.rotation = float(np.degrees(np.arctan2(v[1], v[0]))) + 90.0
        elif self._transform is not None and self._transform.startswith('resize_'):
            i = int(self._transform[-1])
            R = rotation_matrix(rotation0)
            corners0 = center0 + (_UNIT_CORNERS * size0) @ R.T
            fixed = corners0[(i + 2) % 4]                 # the opposite corner stays put
            new = corners0[i] + p - np.array([x0, y0])
            span = R.T @ (new - fixed)                    # diagonal in the rectangle's own frame
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
        for a in (self.patch, self.handles, self.rotStalk, self.rotHandle):
            a.set_animated(False)
        self.canvas.draw()
        self.updateRect.emit()      # final update after the drag (Reduced calculation policy)
