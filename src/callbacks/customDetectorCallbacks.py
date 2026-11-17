"""Custom detector mode (CustMod), ported from MATLAB Quant4D's
``custom_detector_callbacks``.

The user builds a detector from any number of masks, listed in the main
table ``CDT`` (ID, Type, Label, Enable, Show, weight μ):

* **Circle** – an aperture, optionally mirrored through the beam centre.
* **Grid** / **GridNoCenter** – a lattice of apertures spanned by two
  draggable basis apertures (GridNoCenter drops the transmitted beam and
  every second site).
* **Bandpass** – a ring between two radii.
* **Wedge** – a sector from the beam centre between two draggable handles,
  mirrored by default.
* **Polygon** – drawn by the user.
* **File** – a mask image loaded from disk.
* **Math** – a formula over the other masks (Settings window, Math tab).

The selected mask's geometry is shown and editable in the details table
``CDDTable`` in the current coordinate system (Cartesian/polar, absolute or
relative to the beam, pixels or mrad).  Masks are combined by the
inter-mask mode (Color Mix, Union, Intersection, Additive, Current-only);
the combined mask is shown in the DfrnMask window and the real-space image
is that mask applied to every diffraction pattern.

The mask shapes themselves are computed in :mod:`callbacks.compute.custom`
and :mod:`callbacks.compute.mask_math`.
"""
from __future__ import annotations

from typing import Any

import numpy as np
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.widgets import PolygonSelector
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw

from annotationsClasses.interactiveCircle import InteractiveCircle
from annotationsClasses.interactivePoint import InteractivePoint
from annotationsClasses.interactivePolygon import InteractivePolygon
from callbacks import compute
from callbacks.compute import custom as cm
from callbacks.compute.mask_math import MaskMathError, evaluate_mask_formula
from callbacks.layout import dfrn_shape, real_shape
from callbacks.signals import signals_blocked

__all__ = ["CustomMask", "customDetectorCallbacks", "connectCustomDetector", "resetCustomDetectors"]

_TYPES = ("Circle", "Grid", "GridNoCenter", "Bandpass", "Wedge", "Polygon", "File", "Math")
_COLS = ("ID", "Type", "Label", "✓", "👁", "μ")
_ENABLE, _SHOW, _WEIGHT, _LABEL = 3, 4, 5, 2


class CustomMask:
    """One custom detector mask: its settings, geometry, annotations and current mask."""

    def __init__(self, id, typ, color):
        self.id, self.type, self.label = id, typ, id
        self.enabled, self.shown, self.weight = True, True, 1.0
        self.color = tuple(float(c) for c in color)
        self.mirrored = typ == "Wedge"
        self.inverted = False
        self.intra = "Union"
        self.p1: Any = None             # (x, y) handles
        self.p2: Any = None
        self.r1: Any = None             # radii, pixels
        self.r2: Any = None
        self.vertices: Any = None       # polygon, (n, 2)
        self.file_mask: Any = None      # File type, (NPxY, NPxX)
        self.formula = "1"              # Math type
        self.mask: Any = None           # current (inverted, unweighted) mask
        self.handles: list = []         # interactive annotations
        self.artists: list = []         # passive matplotlib artists

    def points(self):
        """Geometry rows for the details table: list of ((x, y), r or None)."""
        if self.type == "Circle":
            return [(self.p1, self.r1)]
        if self.type in ("Grid", "GridNoCenter"):
            return [(self.p1, self.r1), (self.p2, self.r1)]
        if self.type == "Bandpass":
            return [(self.p1, self.r1), (self.p1, self.r2)]
        if self.type == "Wedge":
            return [(self.p1, None), (self.p2, None)]
        if self.type == "Polygon":
            return [(v, None) for v in self.vertices]
        return []


# ---------------------------------------------------------------------------
# Wiring
# ---------------------------------------------------------------------------
def connectCustomDetector(self):
    """Set up the Custom Detector tab and connect its widgets; called once from ``slotsSignals``."""
    cb = lambda *_: customDetectorCallbacks(self)    # noqa: E731

    # "Grid without centre" was added to the MATLAB app after the .ui file was made
    if not hasattr(self, "CDNewGridNoCenter"):
        btn = qtw.QToolButton(self.CDNewGrid.parent())
        btn.setObjectName("CDNewGridNoCenter")
        btn.setIcon(self.CDNewGrid.icon())
        btn.setIconSize(self.CDNewGrid.iconSize())
        btn.setText("×")
        btn.setToolButtonStyle(qtc.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btn.setToolTip("New grid of apertures without the transmitted beam (every 2nd lattice site)")
        layout = self.CDNewGrid.parent().layout()
        layout.insertWidget(layout.indexOf(self.CDNewGrid) + 1, btn) if isinstance(layout, qtw.QBoxLayout) \
            else self.CDNewMaskHGrid.insertWidget(self.CDNewMaskHGrid.indexOf(self.CDNewGrid) + 1, btn)
        self.CDNewGridNoCenter = btn
    tips = {"CDNewCircle": "New circular aperture", "CDNewGrid": "New grid of apertures",
            "CDNewBandpass": "New band-pass (ring)", "CDNewWedge": "New wedge", "CDNewPolygon": "Draw a polygon mask",
            "CDNewFromFile": "Mask from an image file", "CDNewMath": "Mask from a formula over other masks",
            "CDDelMask": "Delete the selected mask", "CDMirror": "Mirror through the beam centre",
            "CDInvert": "Invert the mask", "CDColor": "Mask colour", "CDRotCCW": "Rotate anticlockwise",
            "CDRotCW": "Rotate clockwise", "CDFlipHorz": "Flip across the horizontal axis (y → -y)",
            "CDFlipVert": "Flip across the vertical axis (x → -x)", "CDTranspose": "Transpose (swap x and y)"}
    for name, tip in tips.items():
        getattr(self, name).setToolTip(tip)

    for name in ("CDNewCircle", "CDNewGrid", "CDNewGridNoCenter", "CDNewBandpass", "CDNewWedge", "CDNewPolygon",
                 "CDNewFromFile", "CDNewMath", "CDDelMask", "CDColor", "CDRotCCW", "CDRotCW", "CDFlipHorz",
                 "CDFlipVert", "CDTranspose"):
        getattr(self, name).clicked.connect(cb)
    for name in ("CDMirror", "CDInvert"):
        getattr(self, name).setCheckable(True)
        getattr(self, name).clicked.connect(cb)
    self.CDIntraMask.currentIndexChanged.connect(cb)
    self.CDInterMask.currentIndexChanged.connect(cb)
    self.SettingsWindow.MathEval.clicked.connect(cb)

    with signals_blocked(self.CDInterMask, self.CDRotStep):
        self.CDInterMask.clear()
        self.CDInterMask.addItems(list(cm.INTER_MODES))
        self.CDInterMask.setCurrentIndex(0)            # Color Mix, as in MATLAB
        self.CDRotStep.clear()
        for step in (180, 90, 60, 45, 30, 22.5, 10, 5, 2, 1, 0.5, 0.25):
            self.CDRotStep.addItem(f"{step:g}°", step)
        self.CDRotStep.setCurrentIndex(1)              # 90°

    t = self.CDT
    t.setColumnCount(len(_COLS))
    t.setHorizontalHeaderLabels(list(_COLS))
    t.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
    t.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
    t.verticalHeader().setVisible(False)
    t.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
    t.horizontalHeader().setSectionResizeMode(_LABEL, qtw.QHeaderView.Stretch)
    t.setRowCount(0)
    t.itemSelectionChanged.connect(cb)
    t.itemChanged.connect(cb)

    d = self.CDDTable
    d.setColumnCount(3)
    d.verticalHeader().setVisible(False)
    d.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
    d.setRowCount(0)
    d.itemChanged.connect(cb)
    _updateDetailsUI(self)


def resetCustomDetectors(self):
    """Remove every custom mask (dataset unloaded)."""
    for cmask in list(getattr(self.A, "Custom", {}).values()):
        _removeArtists(cmask)
    self.A.Custom = {}
    with signals_blocked(self.CDT, self.CDDTable):
        self.CDT.setRowCount(0)
        self.CDDTable.setRowCount(0)


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------
def customDetectorCallbacks(self, source=None):
    """Dispatcher for every widget of the Custom Detector tab (and Math → Evaluate)."""
    if self.blockAllSignals or self.D is None or self.Data is None:
        return
    if self.DetrMode.currentData() != "CustMod":
        return
    sender = source if source is not None else self.sender()
    sel = _selected(self)
    new = {self.CDNewCircle: "Circle", self.CDNewGrid: "Grid", self.CDNewGridNoCenter: "GridNoCenter",
           self.CDNewBandpass: "Bandpass", self.CDNewWedge: "Wedge", self.CDNewPolygon: "Polygon",
           self.CDNewFromFile: "File", self.CDNewMath: "Math"}

    if sender is self.DetrMode or sender is self.UpdateImages:
        _setDiffractionMaskCmap(self)
        for cmask in self.A.Custom.values():         # beam centre may have moved since
            _computeMask(self, cmask)
            _draw(self, cmask)
        _updateDetailsUI(self)
        _plotCustom(self)
    elif sender in new:
        _newMask(self, new[sender])
    elif sender is self.SettingsWindow.DCSys:      # via detrCoordCallbacks: system/unit/reference changed
        _updateDetailsUI(self)
    elif sender is self.CDT:
        _syncFromMainTable(self)
        _updateDetailsUI(self)
        _plotCustom(self)
    elif sender is self.CDInterMask:
        _plotCustom(self)
    elif sel is None:
        return
    elif sender is self.CDDelMask:
        _deleteMask(self, sel)
    elif sender in (self.CDMirror, self.CDInvert, self.CDIntraMask):
        sel.mirrored = self.CDMirror.isChecked()
        sel.inverted = self.CDInvert.isChecked()
        sel.intra = self.CDIntraMask.currentText()
        _update(self, sel)
    elif sender is self.CDColor:
        c = qtw.QColorDialog.getColor(qtg.QColor.fromRgbF(*sel.color), self, f"Colour of mask {sel.id}")
        if c.isValid():
            sel.color = (c.redF(), c.greenF(), c.blueF())
            _draw(self, sel)
            _fillMainTable(self)
            _updateDetailsUI(self)
            if self.CDInterMask.currentText() == "Color Mix":
                _plotCustom(self)
    elif sender in (self.CDFlipHorz, self.CDFlipVert, self.CDTranspose, self.CDRotCW, self.CDRotCCW):
        _transform(self, sel, sender)
    elif sender is self.CDDTable:
        _syncFromDetailsTable(self, sel)
    elif sender is self.SettingsWindow.MathEval:
        if sel.type == "Math":
            sel.formula = self.SettingsWindow.MathFormula.toPlainText().strip() or "1"
            _update(self, sel)


# ---------------------------------------------------------------------------
# Creating and deleting masks
# ---------------------------------------------------------------------------
def _nextId(self) -> str:
    """A, B, ..., Z, AA, AB, ... after the last mask's ID."""
    if not self.A.Custom:
        return "A"
    last = list(self.A.Custom)[-1]
    n = 0
    for ch in last:
        n = n * 26 + (ord(ch) - 64)
    n += 1
    out = ""
    while n:
        n, r = divmod(n - 1, 26)
        out = chr(65 + r) + out
    return out


def _newMask(self, typ):
    if len(self.A.Custom) and list(self.A.Custom)[-1] == "ZZ":
        _tell(self, "warn", "Mask ID can not go beyond 'ZZ'!", "Maximum Custom Detectors Reached")
        return
    rng = np.random.default_rng()
    cmask = CustomMask(_nextId(self), typ, rng.random(3))
    b0 = np.asarray(self.B0, float)
    r0 = float(self.TBR.value())
    ny, nx = dfrn_shape(self.D)

    if typ == "Circle":                      # identical to the transmitted beam
        cmask.p1, cmask.r1 = b0.copy(), r0
    elif typ in ("Grid", "GridNoCenter"):    # basis apertures a quarter of the pattern away
        cmask.p1, cmask.p2, cmask.r1 = b0 + [nx / 4, 0], b0 + [0, ny / 4], r0
    elif typ == "Bandpass":
        cmask.p1, cmask.r1, cmask.r2 = b0.copy(), r0, nx / 4 + r0 / 2
    elif typ == "Wedge":
        el = min(nx, ny) / 3
        cmask.p1, cmask.p2 = np.array([el, el]), np.array([el, 2 * el])
    elif typ == "File":
        from callbacks.import_io import importMask
        mask = importMask(self, "Dfrn")
        if mask is None:
            return
        cmask.file_mask = mask
    elif typ == "Math":
        self.SettingsWindow.MathFormula.setPlainText("1")
        self.SettingsWindow.show()
        self.SettingsWindow.SettingsTabGroup.setCurrentWidget(self.SettingsWindow.MathTab)
    elif typ == "Polygon":
        _drawPolygon(self, cmask)            # finishes asynchronously
        return
    _addMask(self, cmask)


def _addMask(self, cmask):
    self.A.Custom[cmask.id] = cmask
    _computeMask(self, cmask)
    _draw(self, cmask)
    _fillMainTable(self, select=cmask.id)
    _updateDetailsUI(self)
    _plotCustom(self)


def _drawPolygon(self, cmask):
    """Let the user click the polygon on the diffraction pattern; Esc cancels."""
    ax = self.Fig.Dfrn.ax
    self.Fig.Dfrn.show()
    self.Fig.Dfrn.activateWindow()
    _tell(self, "help", "Click the vertices of the polygon on the diffraction pattern; "
                        "click the first vertex again to close it.  Press Esc to cancel.", "Draw Polygon Mask")

    def done(vertices):
        sel = getattr(self, "_cdSelector", None)
        if sel is not None:
            sel.disconnect_events()
            sel.set_visible(False)
        self._cdSelector = None
        ax.figure.canvas.mpl_disconnect(esc_cid[0])
        ax.figure.canvas.draw_idle()
        if vertices is None or len(vertices) < 3:
            return
        cmask.vertices = np.asarray(vertices, float)
        _addMask(self, cmask)

    def on_key(event):
        if event.key == "escape":
            done(None)

    esc_cid = [ax.figure.canvas.mpl_connect("key_press_event", on_key)]
    # matplotlib's stub types onselect as (x, y); PolygonSelector actually passes the vertex list
    self._cdSelector = PolygonSelector(ax, done, props=dict(color=cmask.color, linewidth=1.5))  # pyright: ignore[reportArgumentType]


def _deleteMask(self, cmask):
    _removeArtists(cmask)
    ids = list(self.A.Custom)
    row = ids.index(cmask.id)
    del self.A.Custom[cmask.id]
    remaining = list(self.A.Custom)
    _fillMainTable(self, select=remaining[min(row, len(remaining) - 1)] if remaining else None)
    _updateDetailsUI(self)
    _plotCustom(self)


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------
def _selected(self):
    rows = self.CDT.selectionModel().selectedRows() if self.CDT.selectionModel() else []
    if not rows:
        return None
    item = self.CDT.item(rows[0].row(), 0)
    return self.A.Custom.get(item.text()) if item is not None else None


def _fontColor(color):
    """Black or white text, whichever reads better on *color*."""
    lum = np.dot(np.square(color), [0.299, 0.587, 0.114])
    return qtg.QColor("white") if lum < 0.25 else qtg.QColor("black")


def _fillMainTable(self, select=None):
    t = self.CDT
    sel = _selected(self)
    current = select if select is not None else (sel.id if sel is not None else None)
    with signals_blocked(t):
        t.setRowCount(len(self.A.Custom))
        for row, cmask in enumerate(self.A.Custom.values()):
            fixed = qtc.Qt.ItemFlags(qtc.Qt.ItemFlag.ItemIsSelectable) | qtc.Qt.ItemFlag.ItemIsEnabled
            for col, text in ((0, cmask.id), (1, cmask.type)):
                item = qtw.QTableWidgetItem(text)
                item.setFlags(fixed)
                t.setItem(row, col, item)
            label = qtw.QTableWidgetItem(cmask.label)
            label.setBackground(qtg.QColor.fromRgbF(*cmask.color))
            label.setForeground(_fontColor(cmask.color))
            t.setItem(row, _LABEL, label)
            for col, state in ((_ENABLE, cmask.enabled), (_SHOW, cmask.shown)):
                item = qtw.QTableWidgetItem()
                item.setFlags(qtc.Qt.ItemFlags(fixed | qtc.Qt.ItemFlag.ItemIsUserCheckable))
                item.setCheckState(qtc.Qt.CheckState.Checked if state else qtc.Qt.CheckState.Unchecked)
                t.setItem(row, col, item)
            t.setItem(row, _WEIGHT, qtw.QTableWidgetItem(f"{cmask.weight:g}"))
            if cmask.id == current:
                t.selectRow(row)
        if current is None:
            t.clearSelection()


def _syncFromMainTable(self):
    """Read Label/Enable/Show/weight edits back into the masks."""
    t = self.CDT
    for row, cmask in enumerate(self.A.Custom.values()):
        if t.item(row, _LABEL) is None:
            continue
        cmask.label = t.item(row, _LABEL).text()
        cmask.enabled = t.item(row, _ENABLE).checkState() == qtc.Qt.CheckState.Checked
        cmask.shown = t.item(row, _SHOW).checkState() == qtc.Qt.CheckState.Checked
        try:
            cmask.weight = float(t.item(row, _WEIGHT).text())
        except ValueError:
            pass
        _setVisible(self, cmask)
    _fillMainTable(self)


def _units(self):
    return " " + (self.SettingsWindow.DCUnit.currentData() or "px")


def _polar(self):
    return self.SettingsWindow.DCSys.currentText() == "Polar"


def _toTable(self, p):
    """Pixel (x, y) -> table coordinates (relative/absolute, px/mrad, Cartesian/polar)."""
    q = (np.asarray(p, float) - np.asarray(self.RB0, float)) * self.DfPxR
    if _polar(self):
        return np.array([np.hypot(*q), np.degrees(np.arctan2(q[1], q[0])) % 360.0])
    return q


def _fromTable(self, a, b):
    q = np.array([a * np.cos(np.radians(b)), a * np.sin(np.radians(b))]) if _polar(self) else np.array([a, b])
    return q / self.DfPxR + np.asarray(self.RB0, float)


def _fillDetailsTable(self, cmask):
    d = self.CDDTable
    unit = _units(self)
    labels = ["ρ" + unit, "θ °", "R" + unit] if _polar(self) else ["X" + unit, "Y" + unit, "R" + unit]
    rows = cmask.points() if cmask is not None else []
    with signals_blocked(d):
        d.setHorizontalHeaderLabels(labels)
        d.setRowCount(len(rows))
        for row, (p, r) in enumerate(rows):
            a, b = _toTable(self, p)
            values = (a, b, None if r is None else r * self.DfPxR)
            for col, v in enumerate(values):
                item = qtw.QTableWidgetItem("" if v is None else f"{v:.4g}")
                if v is None:
                    item.setFlags(qtc.Qt.ItemFlag.ItemIsEnabled)
                d.setItem(row, col, item)


def _syncFromDetailsTable(self, cmask):
    """Apply an edit of the details table to the selected mask's geometry."""
    d = self.CDDTable
    rows = []
    for row in range(d.rowCount()):
        vals = []
        for col in range(3):
            item = d.item(row, col)
            try:
                vals.append(float(item.text()) if item is not None and item.text() else None)
            except ValueError:
                vals.append(None)
        rows.append(vals)
    if any(r[0] is None or r[1] is None for r in rows):
        _fillDetailsTable(self, cmask)          # reject the edit
        return
    pts = [_fromTable(self, r[0], r[1]) for r in rows]
    radii = [None if r[2] is None else r[2] / self.DfPxR for r in rows]
    edited = d.currentRow()

    if cmask.type == "Circle":
        cmask.p1, cmask.r1 = pts[0], radii[0]
    elif cmask.type in ("Grid", "GridNoCenter"):
        cmask.p1, cmask.p2 = pts[0], pts[1]
        cmask.r1 = radii[1] if edited == 1 else radii[0]
    elif cmask.type == "Bandpass":
        cmask.p1 = pts[1] if edited == 1 else pts[0]
        cmask.r1, cmask.r2 = radii[0], radii[1]
    elif cmask.type == "Wedge":
        cmask.p1, cmask.p2 = pts[0], pts[1]
    elif cmask.type == "Polygon":
        cmask.vertices = np.array(pts)
    _update(self, cmask)


def _updateDetailsUI(self):
    """Enable and fill the details panel for the selected mask."""
    sel = _selected(self)
    widgets = (self.CDMirror, self.CDInvert, self.CDColor, self.CDIntraMask, self.CDRotCW, self.CDRotCCW,
               self.CDRotStep, self.CDFlipHorz, self.CDFlipVert, self.CDTranspose, self.CDDTable, self.CDDelMask)
    for w in widgets:
        w.setEnabled(sel is not None)
    _fillDetailsTable(self, sel)
    if sel is None:
        return
    with signals_blocked(self.CDMirror, self.CDInvert, self.CDIntraMask, self.CDRotStep):
        self.CDMirror.setChecked(sel.mirrored)
        self.CDInvert.setChecked(sel.inverted)
        self.CDIntraMask.setCurrentIndex(max(0, self.CDIntraMask.findText(sel.intra)))
        self.CDMirror.setEnabled(sel.type in ("Circle", "Wedge"))
        self.CDIntraMask.setEnabled(sel.type in ("Grid", "GridNoCenter") or (sel.type == "Circle" and sel.mirrored))
        square = self.D.NPxX == self.D.NPxY
        if sel.type == "File":
            self.CDTranspose.setEnabled(square)
            self.CDRotStep.setCurrentIndex(self.CDRotStep.findData(90 if square else 180))
            self.CDRotStep.setEnabled(False)
        elif sel.type == "Math":
            for w in (self.CDRotCW, self.CDRotCCW, self.CDRotStep, self.CDFlipHorz, self.CDFlipVert, self.CDTranspose):
                w.setEnabled(False)
    if sel.type == "Math":
        self.SettingsWindow.MathFormula.setPlainText(sel.formula)
    pal = self.CDDTable.palette()
    pal.setColor(qtg.QPalette.Base, qtg.QColor.fromRgbF(*sel.color))
    pal.setColor(qtg.QPalette.Text, _fontColor(sel.color))
    self.CDDTable.setPalette(pal)


# ---------------------------------------------------------------------------
# Geometry changes
# ---------------------------------------------------------------------------
def _transform(self, cmask, sender):
    """Flip, transpose or rotate the selected mask about the beam centre."""
    b0 = np.asarray(self.B0, float)
    if sender in (self.CDRotCW, self.CDRotCCW):
        from callbacks.axis_direction import clockwise_angle  # noqa: E402
        step = float(self.CDRotStep.currentData())
        angle = clockwise_angle(self, step, sender is self.CDRotCW)     # clockwise as displayed
    if cmask.type == "File":
        m = cmask.file_mask
        if sender is self.CDFlipVert:
            m = np.fliplr(m)
        elif sender is self.CDFlipHorz:
            m = np.flipud(m)
        elif sender is self.CDTranspose:
            m = m.T
        else:
            if m.shape[0] != m.shape[1] and step % 180:
                return
            m = np.rot90(m, -int(round(angle / 90)))      # rot90 is anticlockwise on screen for positive k
        cmask.file_mask = np.ascontiguousarray(m)
        _update(self, cmask)
        return

    from callbacks.axis_direction import rotate_about  # noqa: E402

    def apply(p):
        q = np.asarray(p, float) - b0
        if sender is self.CDFlipVert:
            q = q * [-1, 1]
        elif sender is self.CDFlipHorz:
            q = q * [1, -1]
        elif sender is self.CDTranspose:
            q = q[..., ::-1]
        else:
            return rotate_about(q + b0, b0, angle)
        return q + b0

    for attr in ("p1", "p2", "vertices"):
        if getattr(cmask, attr) is not None:
            setattr(cmask, attr, apply(getattr(cmask, attr)))
    _update(self, cmask)


def _update(self, cmask):
    """The mask's settings or geometry changed: recompute, redraw, refresh tables and images."""
    _computeMask(self, cmask)
    _draw(self, cmask)
    _fillDetailsTable(self, cmask)
    _plotCustom(self)


def _onHandleMoved(self, cmask, handle_index):
    """An annotation was dragged: read its geometry back."""
    h = cmask.handles[handle_index]
    if cmask.type == "Circle":
        cmask.p1, cmask.r1 = np.array(h.center, float), float(h.radius[-1])
    elif cmask.type in ("Grid", "GridNoCenter"):
        p = np.array(h.center, float)
        if handle_index == 0:
            cmask.p1 = p
        else:
            cmask.p2 = p
        cmask.r1 = float(h.radius[-1])
    elif cmask.type == "Bandpass":
        cmask.p1 = np.array(h.center, float)
        cmask.r1, cmask.r2 = float(h.radius[0]), float(h.radius[-1])
    elif cmask.type == "Wedge":
        p = np.asarray(h.position, float).ravel()
        if handle_index == 0:
            cmask.p1 = p
        else:
            cmask.p2 = p
    elif cmask.type == "Polygon":
        cmask.vertices = np.asarray(h.vertices, float)
    if _selected(self) is not cmask:
        _fillMainTable(self, select=cmask.id)
        _updateDetailsUI(self)
    _computeMask(self, cmask)
    _drawPassive(self, cmask)
    _fillDetailsTable(self, cmask)
    _plotCustom(self)


# ---------------------------------------------------------------------------
# Masks
# ---------------------------------------------------------------------------
def _computeMask(self, cmask):
    shape = dfrn_shape(self.D)
    b0 = np.asarray(self.B0, float)
    t = cmask.type
    if t == "Circle":
        mask = cm.circle_detector(shape, cmask.p1, cmask.r1, b0, cmask.mirrored, cmask.intra)
    elif t in ("Grid", "GridNoCenter"):
        pts = cm.grid_points(shape, b0, cmask.p1, cmask.p2, cmask.r1, no_center=(t == "GridNoCenter"))
        mask = cm.grid_detector(shape, pts, cmask.r1, cmask.intra)
    elif t == "Bandpass":
        mask = cm.bandpass_detector(shape, cmask.p1, cmask.r1, cmask.r2)
    elif t == "Wedge":
        mask = cm.wedge_detector(shape, b0, cmask.p1, cmask.p2, cmask.mirrored)
    elif t == "Polygon":
        mask = cm.polygon_detector(shape, cmask.vertices)
    elif t == "File":
        mask = cmask.file_mask
    else:                                                 # Math
        others = {k: v.mask for k, v in self.A.Custom.items() if k != cmask.id and v.mask is not None}
        if cmask.id in _idsIn(cmask.formula):
            _tell(self, "warn", f"The formula refers to the mask itself ({cmask.id}).", "Evaluation Failed")
            return
        try:
            mask = evaluate_mask_formula(cmask.formula, others, shape)
        except MaskMathError as exc:
            _tell(self, "warn", f"Calculation failed!\n{exc}", "Evaluation Failed")
            return
    mask = np.asarray(mask, float)
    cmask.mask = cm.invert_mask(mask) if cmask.inverted else mask


def _idsIn(formula):
    from callbacks.compute.mask_math import mask_ids
    return mask_ids(formula)


def _plotCustom(self):
    """Combine the enabled masks and update the DfrnMask and Real images."""
    shape = dfrn_shape(self.D)
    active = [c for c in self.A.Custom.values() if c.enabled and c.weight != 0 and c.mask is not None]
    mode = self.CDInterMask.currentText()
    sel = _selected(self)
    if active:
        combined = cm.combine_masks([c.mask for c in active], [c.weight for c in active], mode,
                                    ids=[c.id for c in active], current=sel.id if sel else None, shape=shape)
    else:
        combined = np.zeros(shape)
    self.Fig.DfrnMask.Image = combined
    self.Fig.Real.Image = np.asarray(compute.project(self.Data, combined.ravel(), self.D.GPU), float).reshape(real_shape(self.D))

    if mode == "Color Mix" and active:
        rgb_mask, rgb_real = cm.color_mix(self.Data, [c.mask for c in active], [c.weight for c in active],
                                          [c.color for c in active], self.D.GPU)
        top = rgb_mask.max()
        self.Fig.DfrnMask.ColorMix = rgb_mask / top if top > 0 else rgb_mask
        self.Fig.Real.ColorMix = rgb_real.reshape(*real_shape(self.D), 3)
    else:
        self.Fig.DfrnMask.ColorMix = None
        self.Fig.Real.ColorMix = None

    from callbacks.plotting import plotAllPatterns
    plotAllPatterns(self)


def _setDiffractionMaskCmap(self):
    for id in ("DfrnMask", "Real"):
        if not hasattr(self.Fig[id], "ColorMix"):
            self.Fig[id].ColorMix = None


# ---------------------------------------------------------------------------
# Annotations
# ---------------------------------------------------------------------------
def _removeArtists(cmask):
    for obj in cmask.handles + cmask.artists:
        try:
            obj.remove()
        except (ValueError, AttributeError, NotImplementedError):
            pass
    cmask.handles, cmask.artists = [], []


def _setVisible(self, cmask):
    visible = cmask.enabled and cmask.shown
    for h in cmask.handles:
        for art in (getattr(h, "circ", None) or []) + [getattr(h, a, None) for a in ("point", "patch")]:
            if art is not None:
                art.set_visible(visible)
        if isinstance(h, InteractivePoint):
            h.point.set_visible(visible)
    for art in cmask.artists:
        art.set_visible(visible)
    self.Fig.Dfrn.canvas.draw_idle()


def _draw(self, cmask):
    """(Re)create the interactive annotations of a mask, then its passive outline."""
    _removeArtists(cmask)
    ax = self.Fig.Dfrn.ax
    color = cmask.color
    hs = []
    if cmask.type == "Circle":
        hs.append(InteractiveCircle(ax, center=cmask.p1, radius=cmask.r1, color=color, interactions="all"))
    elif cmask.type in ("Grid", "GridNoCenter"):
        hs.append(InteractiveCircle(ax, center=cmask.p1, radius=cmask.r1, color=color, interactions="all"))
        hs.append(InteractiveCircle(ax, center=cmask.p2, radius=cmask.r1, color=color, interactions="all"))
    elif cmask.type == "Bandpass":
        hs.append(InteractiveCircle(ax, center=cmask.p1, radius=[cmask.r1, cmask.r2], color=color, interactions="all"))
    elif cmask.type == "Wedge":
        for p in (cmask.p1, cmask.p2):
            hs.append(InteractivePoint(ax.scatter([p[0]], [p[1]], color=[color], s=60, zorder=8)))
    elif cmask.type == "Polygon":
        hs.append(InteractivePolygon(ax, vertices=cmask.vertices, color=color))
    for k, h in enumerate(hs):
        # the annotation classes start animated (blitting); they animate themselves while dragged,
        # so leave them as ordinary artists in between, otherwise full redraws would drop them
        for art in (getattr(h, "circ", None) or []) + [getattr(h, a, None) for a in ("point", "patch")]:
            if art is not None:
                art.set_animated(False)
        h.connect()
        signal = getattr(h, "updateCircle", None) or getattr(h, "updatePoly", None) or h.positionChanged
        signal.connect(lambda *_, _c=cmask, _k=k: _onHandleMoved(self, _c, _k))
    cmask.handles = hs
    _drawPassive(self, cmask)


def _drawPassive(self, cmask):
    """Non-interactive parts: mirrored copy, grid circles, wedge sector, mask outline."""
    for art in cmask.artists:
        try:
            art.remove()
        except (ValueError, AttributeError, NotImplementedError):
            pass
    cmask.artists = []
    ax = self.Fig.Dfrn.ax
    b0 = np.asarray(self.B0, float)
    ny, nx = dfrn_shape(self.D)
    t = np.linspace(0, 2 * np.pi, 73)
    color = cmask.color

    def ring(c, r, **kw):
        line, = ax.plot(c[0] + r * np.cos(t), c[1] + r * np.sin(t), color=color, linewidth=1, **kw)
        cmask.artists.append(line)

    if cmask.type == "Circle" and cmask.mirrored:
        ring(2 * b0 - cmask.p1, cmask.r1, linestyle="--")
    elif cmask.type in ("Grid", "GridNoCenter"):
        pts = cm.grid_points((ny, nx), b0, cmask.p1, cmask.p2, cmask.r1, no_center=(cmask.type == "GridNoCenter"))
        xs = (pts[:, 0:1] + cmask.r1 * np.cos(t)[None, :]).T
        ys = (pts[:, 1:2] + cmask.r1 * np.sin(t)[None, :]).T
        if xs.size:
            cmask.artists.extend(ax.plot(xs, ys, color=color, linewidth=0.8))
    elif cmask.type == "Wedge":
        far = 2 * max(nx, ny)
        d = np.array([cmask.p1, cmask.p2]) - b0
        a = np.sort(np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 360)
        if a[1] - a[0] > 180:
            a = np.array([a[1], a[0] + 360])
        for off in ((0, 180) if cmask.mirrored else (0,)):
            th = np.radians(np.linspace(a[0] + off, a[1] + off, 30))
            poly = np.vstack([b0, b0 + far * np.column_stack([np.cos(th), np.sin(th)])])
            cmask.artists.append(ax.add_patch(MplPolygon(poly, closed=True, facecolor=color, edgecolor=color,
                                                         alpha=0.25, linewidth=1)))
    if cmask.type in ("File", "Math", "Polygon", "Bandpass", "Wedge") and cmask.mask is not None \
            and cmask.mask.max() > cmask.mask.min():
        cs = ax.contour(np.arange(nx), np.arange(ny), (cmask.mask > 0).astype(float), levels=[0.5],
                        colors=[color], linewidths=0.8, linestyles=":")
        cmask.artists.append(cs)
    for art in cmask.artists:
        art.set_visible(cmask.enabled and cmask.shown)
    ax.set_xlim(-0.5, nx - 0.5)
    ax.set_ylim(ny - 0.5, -0.5)
    self.Fig.Dfrn.canvas.draw_idle()


def _tell(self, icon, msg, title):
    from callbacks.utils import notifDLG
    notifDLG(self, self, icon, msg, title)
