"""
InteractiveLine — a straight line between two draggable end points (MATLAB's ``images.roi.Line``).

* drag an end point        → move that end (the slope changes)
* drag the line elsewhere  → move the whole line

Signals
-------
updateLine : emitted on every change while dragging, and once more on release

Public attributes
-----------------
ends : np.ndarray, shape (2, 2) — the end points (x, y) in data coordinates
line : matplotlib.lines.Line2D
"""

from __future__ import annotations

from typing import Any

import numpy as np
from matplotlib.backend_bases import MouseButton
from matplotlib.backend_tools import Cursors
from PyQt5 import QtCore as qtc

END_TOL = 9.0       # screen pixels: a press this close to an end point grabs it
LINE_TOL = 6.0      # screen pixels: ... this close to the line grabs the line


class InteractiveLine(qtc.QObject):
    updateLine = qtc.pyqtSignal()

    lock: 'InteractiveLine | None' = None     # only one line is dragged at a time

    def __init__(self, axis, ends, color: Any = 'r'):
        super().__init__()
        self.axis = axis
        self.canvas = axis.figure.canvas
        self.ends = np.asarray(ends, float).reshape(2, 2).copy()
        self.line, = axis.plot(self.ends[:, 0], self.ends[:, 1], color=color, linewidth=1.5,
                               marker='o', markersize=7, markerfacecolor='w', markeredgecolor=color, zorder=9)
        self._press = None          # (ends0, xpress, ypress)
        self._grab = None           # 0 / 1 (an end) or 'line'
        self._cids: list = []
        self.canvas.draw_idle()

    # ------------------------------------------------------------------ geometry
    def _hit(self, event):
        """What a press at *event* grabs: 0 or 1 (an end), 'line', or None."""
        if event.x is None or event.y is None:
            return None
        screen = self.axis.transData.transform(self.ends)
        mouse = np.array([event.x, event.y], float)
        d = np.hypot(*(screen - mouse).T)
        if d.min() <= END_TOL:
            return int(np.argmin(d))
        a, b = screen
        ab = b - a
        t = np.clip(np.dot(mouse - a, ab) / max(np.dot(ab, ab), 1e-12), 0, 1)
        return 'line' if np.hypot(*(a + t * ab - mouse)) <= LINE_TOL else None

    # ------------------------------------------------------------------ public API
    def connect(self):
        self._cids = [self.canvas.mpl_connect('button_press_event', self.on_press),
                      self.canvas.mpl_connect('motion_notify_event', self.on_motion),
                      self.canvas.mpl_connect('button_release_event', self.on_release)]

    def disconnect(self):
        for cid in self._cids:
            self.canvas.mpl_disconnect(cid)
        self._cids = []
        if InteractiveLine.lock is self:
            InteractiveLine.lock = None

    def remove(self):
        self.disconnect()
        try:
            self.line.remove()
        except (ValueError, NotImplementedError):
            pass
        self.canvas.draw_idle()

    @property
    def dragging(self) -> bool:
        return self._press is not None

    # ------------------------------------------------------------------ events
    def on_press(self, event):
        if (event.button != MouseButton.LEFT or event.inaxes is not self.axis or event.xdata is None
                or InteractiveLine.lock is not None or not self.line.get_visible()):
            return
        grab = self._hit(event)
        if grab is None:
            return
        self._grab = grab
        self._press = (self.ends.copy(), event.xdata, event.ydata)
        InteractiveLine.lock = self

    def on_motion(self, event):
        if InteractiveLine.lock is None and event.inaxes is self.axis:     # hover feedback
            grab = self._hit(event)
            if grab is not None:
                self.canvas.set_cursor(Cursors.MOVE if grab == 'line' else Cursors.HAND)
            return
        if InteractiveLine.lock is not self or self._press is None or event.xdata is None:
            return
        ends0, x0, y0 = self._press
        delta = np.array([event.xdata - x0, event.ydata - y0])
        self.ends = ends0 + delta if self._grab == 'line' else ends0.copy()
        if isinstance(self._grab, int):             # an end point
            self.ends[self._grab] += delta
        self.line.set_data(self.ends[:, 0], self.ends[:, 1])
        self.canvas.draw_idle()
        self.updateLine.emit()

    def on_release(self, event):
        if InteractiveLine.lock is not self:
            return
        self._press = None
        self._grab = None
        InteractiveLine.lock = None
        self.updateLine.emit()


def intersection(l1: np.ndarray, l2: np.ndarray):
    """Where the (infinite) lines through the two end-point pairs cross, or None if parallel."""
    (x1, y1), (x2, y2) = l1
    (x3, y3), (x4, y4) = l2
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-12:
        return None
    a, b = x1 * y2 - y1 * x2, x3 * y4 - y3 * x4
    return np.array([(a * (x3 - x4) - (x1 - x2) * b) / den, (a * (y3 - y4) - (y1 - y2) * b) / den])
