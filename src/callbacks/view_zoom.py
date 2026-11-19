"""Zoom and view linking for the image windows.

* Left-drag on an image (not on an annotation, no toolbar mode active): pan.
* Mouse wheel: zoom in/out about the cursor.  Keys: ``+``/``=`` zoom in, ``-`` zoom out (about the
  centre of the view), ``Home`` (also ``h``/``r``, matplotlib's) back to the whole image.
* Zooming never goes beyond the whole image: zooming or panning out further (also with the
  toolbar) is clamped to the image, so no black margin appears and a real-space ROI cannot be
  placed off the scan.
* All the images of one space (the diffraction pattern and its mask; the real-space image, its mask
  and the CoM/DPC images) show the same view: zooming one zooms them all.
* The toolbar's Home goes back to the whole image of the current dataset (its view history was
  started before the dataset was loaded, so Home used to restore placeholder limits).
"""
from __future__ import annotations

from typing import Any

import matplotlib as mpl
import numpy as np

__all__ = ["connectZoom", "PAN_THRESHOLD_PX", "ensureLinked", "zoomView", "resetView", "imageExtent", "linkedFigures", "resetNavigation"]

ZOOM_STEP = 1.25            # per wheel notch or key press
PAN_THRESHOLD_PX = 4        # a press moves this far before it pans (a click or double-click doesn't)
_EXCLUDED = ("Preview", "ColorWheel")       # not linked to the other images of their space
# matplotlib's default keys that make no sense on an image window (log axes, grid, closing it)
_IGNORED_KEYMAPS = ("keymap.xscale", "keymap.yscale", "keymap.grid", "keymap.grid_minor",
                    "keymap.quit", "keymap.quit_all")


def imageExtent(self, id) -> Any:
    """``((x0, x1), (y0, y1))`` of the image shown in window *id* (x0 < x1, y0 < y1), or None."""
    image = self.ImageAx[id] if id in self.ImageAx else None
    if image is None:
        return None
    left, right, bottom, top = image.get_extent()
    return (min(left, right), max(left, right)), (min(bottom, top), max(bottom, top))


def linkedFigures(self, id) -> list:
    """The other windows showing the same space at the same size as *id*."""
    fig = self.Fig[id]
    ext = imageExtent(self, id)
    if id in _EXCLUDED or ext is None:
        return []
    out = []
    for other in self.G.ImgID:
        o = self.Fig[other]
        if other == id or other in _EXCLUDED or o is None or o.space != fig.space:
            continue
        if imageExtent(self, other) == ext:
            out.append(o)
    return out


def _clamp(lim, full):
    """Limits *lim* (in either order) kept within *full* = (lo, hi): no wider, and shifted inside."""
    lo, hi = sorted(lim)
    flo, fhi = full
    width = min(hi - lo, fhi - flo)
    centre = min(max((lo + hi) / 2, flo + width / 2), fhi - width / 2)
    new = (centre - width / 2, centre + width / 2)
    return new if lim[0] <= lim[1] else new[::-1]


def _onLimitsChanged(self, id) -> None:
    """A window's view changed (wheel, keys, toolbar zoom/pan/home): clamp it to the image and show
    the same view in the linked windows."""
    if getattr(self, "_syncingView", False):
        return
    ext = imageExtent(self, id)
    if ext is None:
        return
    self._syncingView = True
    try:
        ax = self.Fig[id].ax
        xlim, ylim = _clamp(ax.get_xlim(), ext[0]), _clamp(ax.get_ylim(), ext[1])
        if not (np.allclose(xlim, ax.get_xlim()) and np.allclose(ylim, ax.get_ylim())):
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
        for other in linkedFigures(self, id):
            if not (np.allclose(other.ax.get_xlim(), xlim) and np.allclose(other.ax.get_ylim(), ylim)):
                other.ax.set_xlim(xlim)
                other.ax.set_ylim(ylim)
                other.canvas.draw_idle()
    finally:
        self._syncingView = False


def zoomView(self, id, factor, centre=None) -> None:
    """Zoom window *id* by *factor* (< 1 zooms in) about *centre* (data x, y; default: the view's centre)."""
    ax = self.Fig[id].ax
    xlim, ylim = np.asarray(ax.get_xlim(), float), np.asarray(ax.get_ylim(), float)
    if centre is None:
        centre = (xlim.mean(), ylim.mean())
    cx, cy = centre
    ax.set_xlim(cx + (xlim - cx) * factor)      # the point under the cursor stays put
    ax.set_ylim(cy + (ylim - cy) * factor)
    self.Fig[id].canvas.draw_idle()


def resetView(self, id) -> None:
    """Show the whole image in window *id* (and its linked windows)."""
    ext = imageExtent(self, id)
    if ext is None:
        return
    ax = self.Fig[id].ax
    (x0, x1), (y0, y1) = ext
    ax.set_xlim((x0, x1) if ax.get_xlim()[0] <= ax.get_xlim()[1] else (x1, x0))
    ax.set_ylim((y0, y1) if ax.get_ylim()[0] <= ax.get_ylim()[1] else (y1, y0))
    self.Fig[id].canvas.draw_idle()


def resetNavigation(ax) -> None:
    """Start the toolbar's view history at the current (whole-image) view, so Home returns there."""
    toolbar = getattr(ax.figure.canvas, "toolbar", None)
    if toolbar is not None and hasattr(toolbar, "update") and hasattr(toolbar, "push_current"):
        toolbar.update()
        toolbar.push_current()


def _onScroll(self, id, event) -> None:
    if event.inaxes is not self.Fig[id].ax or event.xdata is None:
        return
    zoomView(self, id, 1 / ZOOM_STEP if event.step > 0 else ZOOM_STEP, (event.xdata, event.ydata))


def handleKey(self, id, event) -> bool:
    """Zoom keys; returns True if *event* was one of them (or a key ignored on image windows)."""
    key = event.key or ""
    if key in ("+", "="):
        zoomView(self, id, 1 / ZOOM_STEP)
        return True
    if key in ("-", "_"):
        zoomView(self, id, ZOOM_STEP)
        return True
    if key in mpl.rcParams["keymap.home"]:
        resetView(self, id)
        return True
    return any(key in mpl.rcParams[k] for k in _IGNORED_KEYMAPS)


def _annotationBusy(self) -> bool:
    """An annotation is being dragged, or a click tool (polygon drawing) is active.  (The cross-align
    lines only take presses on themselves: their lock says when one is dragged.)"""
    from annotationsClasses.interactiveCircle import InteractiveCircle
    from annotationsClasses.interactiveEllipse import InteractiveEllipse
    from annotationsClasses.interactiveLine import InteractiveLine
    from annotationsClasses.interactivePoint import InteractivePoint
    from annotationsClasses.interactivePolygon import InteractivePolygon
    from annotationsClasses.interactiveRectangle import InteractiveRectangle
    if any(cls.lock is not None for cls in (InteractiveCircle, InteractiveEllipse, InteractiveLine, InteractivePoint,
                                            InteractivePolygon, InteractiveRectangle)):
        return True
    return any(getattr(obj, name, None) is not None
               for obj, name in ((self.A, "_tmp_selector"), (self, "_cdSelector")))


def _onPanPress(self, id, event) -> None:
    fig = self.Fig[id]
    toolbar = getattr(fig.canvas, "toolbar", None)
    if (event.button != 1 or event.inaxes is not fig.ax or event.xdata is None or event.dblclick
            or (toolbar is not None and getattr(toolbar, "mode", "")) or imageExtent(self, id) is None):
        self._pan = None
        return
    ax = fig.ax
    self._pan = {"id": id, "xy": (event.x, event.y), "inv": ax.transData.inverted().frozen(),
                 "xlim": ax.get_xlim(), "ylim": ax.get_ylim(), "active": False}


def _onPanMove(self, id, event) -> None:
    pan = getattr(self, "_pan", None)
    if pan is None or pan["id"] != id or event.x is None:
        return
    if not pan["active"]:
        if np.hypot(event.x - pan["xy"][0], event.y - pan["xy"][1]) < PAN_THRESHOLD_PX:
            return
        if _annotationBusy(self):           # the press picked an annotation: that is a drag, not a pan
            self._pan = None
            return
        pan["active"] = True
        from matplotlib.backend_tools import Cursors
        self.Fig[id].canvas.set_cursor(Cursors.MOVE)
    # the data point under the press follows the mouse (inverse transform frozen at the press)
    d0 = np.asarray(pan["inv"].transform(pan["xy"]))
    d1 = np.asarray(pan["inv"].transform((event.x, event.y)))
    shift = d0 - d1
    ax = self.Fig[id].ax
    ax.set_xlim(np.asarray(pan["xlim"]) + shift[0])
    ax.set_ylim(np.asarray(pan["ylim"]) + shift[1])
    self.Fig[id].canvas.draw_idle()


def _onPanRelease(self, id, event) -> None:
    pan = getattr(self, "_pan", None)
    self._pan = None
    if pan is not None and pan["active"]:
        from matplotlib.backend_tools import Cursors
        self.Fig[id].canvas.set_cursor(Cursors.POINTER)
        toolbar = getattr(self.Fig[id].canvas, "toolbar", None)
        if toolbar is not None and hasattr(toolbar, "push_current"):
            toolbar.push_current()          # the toolbar's back/forward know this view


def connectZoom(self) -> None:
    """Connect wheel zoom, zoom keys and view linking for every image window; called once from slotsSignals."""
    for id in self.G.ImgID:
        fig = self.Fig[id]
        if fig is None:
            continue
        fig.canvas.mpl_connect("scroll_event", lambda e, _id=id: _onScroll(self, _id, e))
        fig.canvas.mpl_connect("button_press_event", lambda e, _id=id: _onPanPress(self, _id, e))
        fig.canvas.mpl_connect("motion_notify_event", lambda e, _id=id: _onPanMove(self, _id, e))
        fig.canvas.mpl_connect("button_release_event", lambda e, _id=id: _onPanRelease(self, _id, e))
        fig.zoomKeys = lambda e, _id=id: handleKey(self, _id, e)
        ensureLinked(self, id)


def ensureLinked(self, id) -> None:
    """Watch window *id*'s view limits (clamping and linking).  ``Axes.cla()`` replaces the axes'
    callback registry, so this is checked again whenever the image is drawn."""
    ax = self.Fig[id].ax
    if getattr(ax, "_q4dWatched", None) is ax.callbacks:
        return
    ax.callbacks.connect("xlim_changed", lambda _ax, _id=id: _onLimitsChanged(self, _id))
    ax.callbacks.connect("ylim_changed", lambda _ax, _id=id: _onLimitsChanged(self, _id))
    ax._q4dWatched = ax.callbacks
