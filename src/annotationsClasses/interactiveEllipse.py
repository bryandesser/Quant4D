"""
InteractiveEllipse — a draggable, resizable, rotatable ellipse annotation.

Two handles sit at the ends of the semi-axes.  Dragging either sets that semi-axis'
length and turns the ellipse so the axis points at the cursor (the other axis
follows, staying perpendicular); dragging inside the ellipse moves it.

Signals
-------
updateEllipse : emitted on every change while dragging, and once more on release
rightClick    : emitted on right mouse button press

Public attributes
-----------------
center   : np.ndarray (2,)  — (cx, cy) in data coordinates
semiaxes : np.ndarray (2,)  — (a, b); *a* lies along the ellipse's own x axis
rotation : float            — degrees from the data +x axis towards +y
patch    : matplotlib.patches.Ellipse
handles  : PathCollection   — the two semi-axis handles
"""
from __future__ import annotations

from typing import Any

import numpy as np
from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.backend_tools import Cursors
from matplotlib.patches import Ellipse
from PyQt5 import QtCore as qtc

from annotationsClasses._geometry import HANDLE_PICK_PX, nearest_handle, rotation_matrix, to_local

_MIN_SEMIAXIS = 0.5     # data units (pixels); keeps the ellipse grabbable


class InteractiveEllipse(qtc.QObject):
    updateEllipse = qtc.pyqtSignal()
    rightClick = qtc.pyqtSignal(MouseEvent)

    lock: 'InteractiveEllipse | None' = None    # only one ellipse is dragged at a time

    def __init__(self, axis, center, semiaxes, rotation: float = 0.0, color: Any = 'r', interactions='all'):
        super().__init__()
        self.axis = axis
        self.canvas = axis.figure.canvas
        self.center = np.asarray(center, float).copy()
        self.semiaxes = np.maximum(np.abs(np.broadcast_to(np.asarray(semiaxes, float), (2,))), _MIN_SEMIAXIS)
        self.rotation = float(rotation)
        self.color = color
        self.interactions = interactions
        self._press = None          # (center0, semiaxes0, rotation0, x0, y0) while dragging
        self._transform = None      # 'translate' | 'axis_0' | 'axis_1'

        self.patch = axis.add_patch(Ellipse(
            tuple(self.center), 2 * self.semiaxes[0], 2 * self.semiaxes[1], angle=self.rotation,
            fill=False, edgecolor=color, linewidth=1.5, animated=False))
        hp = self._handle_positions()
        self.handles = axis.scatter(hp[:, 0], hp[:, 1], color=[color], s=40, zorder=5, animated=False)
        if interactions in ('none', 'translate'):
            self.handles.set_visible(False)
        self.background = None      # taken when a drag starts
        self.canvas.draw_idle()

    # ------------------------------------------------------------------ geometry
    def _handle_positions(self) -> np.ndarray:
        """Ends of the two semi-axes: (a, 0) and (0, b) in the ellipse's own frame."""
        R = rotation_matrix(self.rotation)
        return self.center + (np.diag(self.semiaxes) @ R.T)

    def _inside(self, x, y) -> bool:
        lx, ly = to_local((x, y), self.center, self.rotation)[0]
        a, b = self.semiaxes
        return (lx / a) ** 2 + (ly / b) ** 2 <= 1.0

    def _hit_handle(self, event) -> int:
        if not self.handles.get_visible() or self.interactions not in ('all', 'resize'):
            return -1
        i, d = nearest_handle(self.axis, self._handle_positions(), event)
        return i if d <= HANDLE_PICK_PX else -1

    def _update_artists(self):
        self.patch.set_center(tuple(self.center))
        self.patch.set_width(2 * self.semiaxes[0])
        self.patch.set_height(2 * self.semiaxes[1])
        self.patch.set_angle(self.rotation)
        self.handles.set_offsets(self._handle_positions())

    # ------------------------------------------------------------------ public API
    def connect(self):
        self._cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self._cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self._cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def disconnect(self):
        """Stop listening to the mouse (a removed annotation must not react any more)."""
        for name in ('_cidpress', '_cidrelease', '_cidmotion'):
            cid = getattr(self, name, None)
            if cid is not None:
                self.canvas.mpl_disconnect(cid)
            setattr(self, name, None)
        if InteractiveEllipse.lock is self:
            InteractiveEllipse.lock = None

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
        self.axis.draw_artist(self.patch)
        if self.handles.get_visible():
            self.axis.draw_artist(self.handles)
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
        if (self.interactions == 'none' or event.inaxes != self.axis or InteractiveEllipse.lock is not None
                or event.xdata is None or event.ydata is None):
            return
        h = self._hit_handle(event)
        if h >= 0:
            self._transform = f'axis_{h}'
            self.canvas.set_cursor(Cursors.HAND)
        elif self.interactions in ('all', 'translate') and self._inside(event.xdata, event.ydata):
            self._transform = 'translate'
            self.canvas.set_cursor(Cursors.MOVE)
        else:
            return
        self._press = (self.center.copy(), self.semiaxes.copy(), self.rotation, event.xdata, event.ydata)
        InteractiveEllipse.lock = self
        self.patch.set_animated(True)
        self.handles.set_animated(self.handles.get_visible())
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.axis.bbox)
        self.restoreBackground()

    def on_motion(self, event):
        if event.inaxes != self.axis:
            return
        if InteractiveEllipse.lock is not self:                     # hover feedback
            if event.xdata is None or event.ydata is None:
                return
            if self._hit_handle(event) >= 0:
                self.canvas.set_cursor(Cursors.HAND)
            elif self.interactions in ('all', 'translate') and self._inside(event.xdata, event.ydata):
                self.canvas.set_cursor(Cursors.MOVE)
            else:
                self.canvas.set_cursor(Cursors.POINTER)
            return
        if self._press is None or event.xdata is None or event.ydata is None:
            return
        center0, semiaxes0, rotation0, x0, y0 = self._press
        p = np.array([event.xdata, event.ydata])
        if self._transform == 'translate':
            self.center = center0 + p - np.array([x0, y0])
        else:
            k = int(str(self._transform)[-1])
            v = p - center0
            self.semiaxes = semiaxes0.copy()
            self.semiaxes[k] = max(float(np.hypot(*v)), _MIN_SEMIAXIS)
            # handle k points along the ellipse's own x (k=0) or y (k=1) axis
            self.rotation = float(np.degrees(np.arctan2(v[1], v[0]))) - 90.0 * k
        self._update_artists()
        self.restoreBackground()
        self.updateEllipse.emit()

    def on_release(self, event):
        if InteractiveEllipse.lock is not self:
            return
        self._press = None
        self._transform = None
        InteractiveEllipse.lock = None
        self.patch.set_animated(False)
        self.handles.set_animated(False)
        self.canvas.draw()
        self.updateEllipse.emit()   # final update after the drag (Reduced calculation policy)
