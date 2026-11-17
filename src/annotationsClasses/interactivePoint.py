from matplotlib.backend_tools import Cursors
from PyQt5 import QtCore as qtc
import numpy as np


class InteractivePoint(qtc.QObject):
    """
    Wraps an existing matplotlib scatter artist to make it draggable.

    Parameters
    ----------
    point : matplotlib PathCollection (scatter artist)
        The artist to make interactive.  The artist must already be added
        to an axes before constructing InteractivePoint.

    Signal
    ------
    positionChanged
        Emitted whenever the point moves (on_motion).  Replaces the
        previously mis-named ``redrawCircle`` signal.
    """
    positionChanged = qtc.pyqtSignal()

    lock = None  # only one can be animated at a time

    def __init__(self, point):
        super().__init__()
        self.point = point
        self.press = None
        self.idx = 0
        self.background = None
        self.radius = 1

    def disconnect(self):
        """Stop listening to the mouse.  A removed annotation that kept its handlers went on reacting
        to every hover/click on the canvas (drawing artists no longer in a figure, emitting moves)."""
        canvas = getattr(self, "_canvas", None)
        for name in ('cidpress', 'cidrelease', 'cidmotion'):
            cid = getattr(self, name, None)
            if cid is not None and canvas is not None:
                canvas.mpl_disconnect(cid)
            setattr(self, name, None)
        self._stopDrawHandler()
        if InteractivePoint.lock is self:
            InteractivePoint.lock = None

    def _stopDrawHandler(self):
        handler = getattr(self, "_ciddraw", None)
        if handler is not None:
            canvas, cid = handler
            canvas.mpl_disconnect(cid)
        self._ciddraw = None

    def remove(self):
        'remove the point from the plot and stop listening to the mouse'
        self.disconnect()
        self.point.remove()

    def connect(self):
        'connect to all the events we need'
        self._canvas = self.point.figure.canvas      # kept: point.figure is None once removed
        self.cidpress = self._canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self._canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self._canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes:
            return
        if InteractivePoint.lock is not None:
            return

        # check that mouse press contains one of the InteractivePoints
        contains, attrd = self.point.contains(event)

        if not contains:
            return
        # if the point is contained, save point index (i.e. adfInner or adfOuter)
        self.idx = attrd["ind"][0]

        # save info to the self.press
        self.press = (self.point.get_offsets()[attrd["ind"][0]]), event.xdata, event.ydata

        InteractivePoint.lock = self

        # Blit while dragging: draw everything but the point, keep that as the background.  Any full
        # redraw during the drag (e.g. one the move itself triggers) would leave the animated point
        # out, so a draw_event handler takes the new background and paints the point back on.
        canvas = self.point.figure.canvas
        self.point.set_animated(True)
        self._ciddraw = (canvas, canvas.mpl_connect('draw_event', self._on_draw))
        canvas.draw()                   # → _on_draw: background + point

        # update cursor
        canvas.set_cursor(Cursors.HAND)
        canvas.blit(self.point.axes.bbox)

    def _on_draw(self, event):
        """A full redraw while dragging: new background, and the point painted back on top."""
        if self.press is None or self.point.axes is None:
            return
        canvas = self.point.figure.canvas
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)
        self.point.axes.draw_artist(self.point)

    def on_motion(self, event):
        # monitor mouse location, if hovering over a Draggable point,
        # change the cursor to HAND, if not, return to standard pointer
        contains, _ = self.point.contains(event)  # ,radius=self.radius)
        if contains:
            self.point.figure.canvas.set_cursor(Cursors.HAND)
        else:
            self.point.figure.canvas.set_cursor(Cursors.POINTER)

        if InteractivePoint.lock is not self:
            return
        if event.inaxes != self.point.axes:
            return

        if self.press is None:
            return
        self.point.center, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        centers = self.point.get_offsets()
        centers[self.idx] = np.array([self.point.center[0] + dx, self.point.center[1] + dy])

        self.point.set_offsets(centers)

        canvas = self.point.figure.canvas
        axes = self.point.axes

        # restore the background region, draw the point and put it on screen
        if self.background is not None:
            canvas.restore_region(self.background)
        axes.draw_artist(self.point)
        canvas.blit(axes.bbox)

        # notify listeners (e.g. associated circle/annulus or ROI callback)
        self.positionChanged.emit()

    def on_release(self, event):
        'on release we reset the press data'
        if InteractivePoint.lock is not self:
            return

        self.press = None
        InteractivePoint.lock = None
        self._stopDrawHandler()

        # update cursor
        self.point.figure.canvas.set_cursor(Cursors.POINTER)

        # turn off the rect animation property and reset the background
        self.point.set_animated(False)
        self.background = None

        # redraw the full figure
        self.point.figure.canvas.draw()

        # the drag is over: a final update (the Reduced calculation policy waits for this one)
        self.positionChanged.emit()

    @property
    def dragging(self) -> bool:
        """True while the user is dragging this point."""
        return self.press is not None

    def setPointPickerRadius(self, radius):
        self.radius = radius / 2
        self.point.set_sizes(2 * [self.radius / 2])

    # ------------------------------------------------------------------
    # Convenience API for standalone ROI use
    # ------------------------------------------------------------------

    @property
    def position(self):
        """Current (x, y) position as a 1-D NumPy array."""
        return np.asarray(self.point.get_offsets()[self.idx])

    @position.setter
    def position(self, xy):
        """Move the point to *xy* = (x, y) without triggering a signal."""
        offsets = self.point.get_offsets().copy()
        offsets[self.idx] = xy
        self.point.set_offsets(offsets)

    def redraw(self):
        """Refresh the artist after an external position change."""
        self.point.figure.canvas.draw_idle()
