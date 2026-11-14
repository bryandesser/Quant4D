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
    
    def remove(self):
        'allow the points to be removed from plots'
        self.point.remove()

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        if InteractivePoint.lock is not None: return
        
        # check that mouse press contains one of the InteractivePoints
        contains, attrd = self.point.contains(event)

        if not contains: return
        # if the point is contained, save point index (i.e. adfInner or adfOuter)
        self.idx = attrd["ind"][0]

        # save info to the self.press 
        self.press = (self.point.get_offsets()[attrd["ind"][0]]), event.xdata, event.ydata

        InteractivePoint.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.point.figure.canvas
        axes = self.point.axes
        self.point.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)

        # update cursor
        canvas.set_cursor(Cursors.HAND)

        # now redraw just the rectangle
        axes.draw_artist(self.point)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        # monitor mouse location, if hovering over a Draggable point,
        # change the cursor to HAND, if not, return to standard pointer
        contains, _ = self.point.contains(event)#,radius=self.radius)
        if contains:
            self.point.figure.canvas.set_cursor(Cursors.HAND)
        else:
            self.point.figure.canvas.set_cursor(Cursors.POINTER)

        if InteractivePoint.lock is not self:
            return
        if event.inaxes != self.point.axes: return

        self.point.center, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        centers = self.point.get_offsets()
        centers[self.idx] = np.array([self.point.center[0]+dx, self.point.center[1]+dy])

        self.point.set_offsets(centers)

        canvas = self.point.figure.canvas
        axes = self.point.axes

        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.point)

        # notify listeners (e.g. associated circle/annulus or ROI callback)
        self.positionChanged.emit()

    def on_release(self, event):
        'on release we reset the press data'
        if InteractivePoint.lock is not self:
            return

        self.press = None
        InteractivePoint.lock = None

        # update cursor
        self.point.figure.canvas.set_cursor(Cursors.POINTER)

        # turn off the rect animation property and reset the background
        self.point.set_animated(False)
        self.background = None

        # redraw the full figure
        self.point.figure.canvas.draw()       
    
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