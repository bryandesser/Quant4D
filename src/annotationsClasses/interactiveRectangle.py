"""
InteractiveRectangle — a draggable, resizable axis-aligned rectangle annotation.

Follows the same event-handling pattern as InteractiveCircle so it can be used
as a drop-in ROI widget in realSpaceROICallbacks.

Signals
-------
updateRect : emitted whenever geometry changes (on_motion)
rightClick : emitted on right mouse button press

Public attributes (exposed for _roi_to_mask compatibility)
-----------------------------------------------------------
center   : np.ndarray (2,)  — (cx, cy) in data coordinates
size     : np.ndarray (2,)  — (width, height), always positive
rotation : float — always 0.0  (kept for _roi_to_mask API compatibility)
patch    : matplotlib.patches.Rectangle
handles  : matplotlib.collections.PathCollection  — four corner scatter points
"""

from __future__ import annotations

import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.backend_bases import MouseButton
from matplotlib.backend_bases import MouseEvent
from matplotlib.backend_tools import Cursors
from PyQt5 import QtCore as qtc


class InteractiveRectangle(qtc.QObject):
    """
    Draggable, resizable axis-aligned rectangle annotation.

    Parameters
    ----------
    axis         : matplotlib.axes.Axes
    center       : array-like (2,)   — initial (cx, cy) in data units
    size         : array-like (2,)   — initial (width, height) in data units
    color        : matplotlib colour spec (default ``'r'``)
    interactions : ``'all'``       — translate + resize (default)
                   ``'translate'`` — move only
                   ``'resize'``    — resize only
                   ``'none'``      — no interaction (static display)
    """

    updateRect = qtc.pyqtSignal()
    rightClick  = qtc.pyqtSignal(MouseEvent)

    # Only one InteractiveRectangle may be active at a time
    lock: 'InteractiveRectangle | None' = None

    def __init__(self, axis, center, size, color='r', interactions='all'):
        super().__init__()

        self.center       = np.asarray(center, float)
        self.size         = np.abs(np.asarray(size, float))
        self.rotation     = 0.0          # axis-aligned; kept for API compat
        self.color        = color
        self.interactions = interactions
        self.axis         = axis

        self._press     = None           # (center0, size0, xpress, ypress) on drag start
        self._transform = None           # 'translate' | 'resize_<corner_idx>'

        # ---- Rectangle patch ------------------------------------------
        xy = self.center - self.size / 2.0
        self.patch = axis.add_patch(Rectangle(
            xy, self.size[0], self.size[1],
            linewidth=1.5, edgecolor=color, facecolor='none',
            animated=True,
        ))

        # ---- Corner handles (4 scatter points) ------------------------
        corners = self._corner_positions()
        self.handles = axis.scatter(
            corners[:, 0], corners[:, 1],
            color=color, s=40, zorder=5, animated=True,
        )
        if interactions in ('none', 'translate'):
            self.handles.set_visible(False)

        # ---- Blitting setup -------------------------------------------
        self.canvas = axis.figure.canvas
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(axis.bbox)

    # ==================================================================
    # Geometry helpers
    # ==================================================================

    def _corner_positions(self) -> np.ndarray:
        """Return (4, 2) array of corner (x, y) positions (CCW from BL)."""
        cx, cy = self.center
        hw, hh = self.size / 2.0
        return np.array([
            [cx - hw, cy - hh],   # 0: bottom-left
            [cx + hw, cy - hh],   # 1: bottom-right
            [cx + hw, cy + hh],   # 2: top-right
            [cx - hw, cy + hh],   # 3: top-left
        ])

    def _hit_radius(self) -> float:
        """Generous pick radius for corner handles: 5 % of the larger side."""
        return max(2.0, 0.05 * float(self.size.max()))

    def _nearest_corner(self, x: float, y: float):
        """Return (index, distance) for the nearest corner to (x, y)."""
        corners = self._corner_positions()
        dists   = np.linalg.norm(corners - np.array([x, y]), axis=1)
        idx     = int(np.argmin(dists))
        return idx, float(dists[idx])

    def _inside(self, x: float, y: float) -> bool:
        """Return True if the point (x, y) is inside the rectangle."""
        cx, cy = self.center
        hw, hh = self.size / 2.0
        return (cx - hw <= x <= cx + hw) and (cy - hh <= y <= cy + hh)

    def _update_artists(self):
        """Sync patch and handles to current center / size."""
        xy = self.center - self.size / 2.0
        self.patch.set_xy(xy)
        self.patch.set_width(self.size[0])
        self.patch.set_height(self.size[1])
        self.handles.set_offsets(self._corner_positions())

    # ==================================================================
    # Public API  (mirrors InteractiveCircle / InteractivePoint)
    # ==================================================================

    def connect(self):
        """Connect matplotlib mouse events."""
        self._cidpress   = self.canvas.mpl_connect('button_press_event',   self.on_press)
        self._cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self._cidmotion  = self.canvas.mpl_connect('motion_notify_event',  self.on_motion)

    def remove(self):
        """Remove patch and handle scatter from the axes."""
        self.patch.remove()
        self.handles.remove()

    def redraw(self):
        """Redraw after an external geometry change and blit."""
        self._update_artists()
        self.restoreBackground()

    def restoreBackground(self):
        """Blit: restore saved background then redraw artists."""
        self.canvas.restore_region(self.background)
        self.axis.draw_artist(self.patch)
        if self.handles.get_visible():
            self.axis.draw_artist(self.handles)
        self.canvas.blit(self.axis.bbox)

    def updateBackground(self):
        """Redraw full canvas, capture new background, then blit artists."""
        self.patch.set_animated(True)
        self.handles.set_animated(True)
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.axis.bbox)
        self.axis.draw_artist(self.patch)
        if self.handles.get_visible():
            self.axis.draw_artist(self.handles)
        self.canvas.blit(self.axis.bbox)

    # ==================================================================
    # Event handlers
    # ==================================================================

    def on_press(self, event):
        if event.button == MouseButton.RIGHT:
            self.rightClick.emit(event)
            return
        if self.interactions == 'none':
            return
        if event.inaxes != self.axis:
            return
        if InteractiveRectangle.lock is not None:
            return
        if event.xdata is None or event.ydata is None:
            return

        x, y = event.xdata, event.ydata

        # ---- Prioritise corner handles --------------------------------
        corner_idx, corner_dist = self._nearest_corner(x, y)
        if (self.interactions in ('all', 'resize')
                and self.handles.get_visible()
                and corner_dist <= self._hit_radius()):
            self._transform = f'resize_{corner_idx}'
            self.canvas.set_cursor(Cursors.HAND)

        # ---- Fall back to translate inside the rectangle --------------
        elif self.interactions in ('all', 'translate') and self._inside(x, y):
            self._transform = 'translate'
            self.canvas.set_cursor(Cursors.MOVE)

        else:
            return   # click was outside — ignore

        self._press = (self.center.copy(), self.size.copy(), x, y)
        InteractiveRectangle.lock = self

        # Prepare blit background
        self.patch.set_animated(True)
        self.handles.set_animated(self.handles.get_visible())
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.axis.bbox)
        self.axis.draw_artist(self.patch)
        if self.handles.get_visible():
            self.axis.draw_artist(self.handles)
        self.canvas.blit(self.axis.bbox)

    def on_motion(self, event):
        if event.inaxes != self.axis:
            return

        # ---- Hover cursor feedback (no drag) --------------------------
        if InteractiveRectangle.lock is not self:
            if event.xdata is None or event.ydata is None:
                return
            x, y = event.xdata, event.ydata
            _, cdist = self._nearest_corner(x, y)
            if self.handles.get_visible() and cdist <= self._hit_radius():
                self.canvas.set_cursor(Cursors.HAND)
            elif self._inside(x, y) and self.interactions in ('all', 'translate'):
                self.canvas.set_cursor(Cursors.MOVE)
            else:
                self.canvas.set_cursor(Cursors.POINTER)
            return

        # ---- Active drag ----------------------------------------------
        if self._press is None or event.xdata is None:
            return

        center0, size0, xpress, ypress = self._press
        dx = event.xdata - xpress
        dy = event.ydata - ypress

        if self._transform == 'translate':
            self.center = center0 + np.array([dx, dy])

        elif self._transform is not None and self._transform.startswith('resize_'):
            corner_idx = int(self._transform[-1])
            # Build the four corners from the saved state
            half = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]]) * size0 / 2.0
            corners0    = center0[None, :] + half
            new_corner  = corners0[corner_idx] + np.array([dx, dy])
            opp_idx     = (corner_idx + 2) % 4
            fixed_corner = corners0[opp_idx]
            new_size    = np.abs(new_corner - fixed_corner)
            if new_size[0] > 1e-6 and new_size[1] > 1e-6:
                self.center = (new_corner + fixed_corner) / 2.0
                self.size   = new_size

        self._update_artists()
        self.restoreBackground()
        self.updateRect.emit()

    def on_release(self, event):
        if InteractiveRectangle.lock is not self:
            return
        self._press     = None
        self._transform = None
        InteractiveRectangle.lock = None

        self.patch.set_animated(False)
        self.handles.set_animated(False)
        self.canvas.draw()
