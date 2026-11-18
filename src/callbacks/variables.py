"""Settings > Info > "Show all variables": a Variables tab with the dataset and app parameters.

MATLAB Quant4D's Variables tab lists (almost) the whole app struct.  Here it lists the parameters
that describe the dataset and the current analysis — the dataset (``D``), parameters (``P``), the
transmitted beam, detector coordinates and calibration — refreshed whenever the tab is shown.
Arrays are summarised (shape, dtype, range) unless they are small.
"""
from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any

import numpy as np
from PyQt5 import QtWidgets as qtw

__all__ = ["connectVariables", "refreshVariables", "describe", "variableGroups"]

_SMALL = 8          # arrays up to this many elements are shown in full


def describe(value: Any) -> str:
    """A short, readable value for the Value column."""
    if isinstance(value, np.ndarray):
        if value.size <= _SMALL:
            return np.array2string(value, precision=4, separator=", ")
        text = f"array {value.shape} {value.dtype}"
        if value.size and np.issubdtype(value.dtype, np.number):
            finite = value[np.isfinite(value)] if np.issubdtype(value.dtype, np.floating) else value
            if finite.size:
                text += f", {float(finite.min()):.4g} .. {float(finite.max()):.4g}"
        return text
    if isinstance(value, float):
        return f"{value:.6g}"
    if isinstance(value, (list, tuple)) and len(value) > _SMALL:
        return f"{type(value).__name__} of {len(value)}"
    text = repr(value)
    return text if len(text) <= 120 else text[:117] + "..."


def _members(obj) -> list[tuple[str, Any]]:
    if is_dataclass(obj):
        return [(f.name, getattr(obj, f.name, None)) for f in fields(obj)]
    return sorted(((k, v) for k, v in vars(obj).items() if not k.startswith("_")), key=lambda kv: kv[0])


def variableGroups(self) -> list[tuple[str, list[tuple[str, Any]]]]:
    """``[(group, [(name, value), ...]), ...]`` shown in the Variables tab."""
    groups = []
    if getattr(self, "D", None) is not None:
        groups.append(("Dataset (D)", _members(self.D)))
    if getattr(self, "P", None) is not None:
        groups.append(("Parameters (P)", _members(self.P)))
    data = getattr(self, "Data", None)
    groups.append(("Data", [("array", data)] if data is not None else [("array", None)]))
    groups.append(("Transmitted beam", [("centre B0 (x, y) px", np.asarray(getattr(self, "B0", [np.nan] * 2), float)),
                                        ("radius px", self.TBR.value()), ("mrad per px", self.mradPx.value()),
                                        ("convergence angle mrad", self.Alpha.value())]))
    sw = self.SettingsWindow
    groups.append(("Detector coordinates", [("system", sw.DCSys.currentText()), ("position", sw.DCPos.currentText()),
                                            ("unit", sw.DCUnit.currentText()),
                                            ("annular integration step mrad", self.AnnStep.value())]))
    groups.append(("Mode", [("detector mode", self.DetrMode.currentText()),
                            ("calculation policy", sw.CalcPolicy.currentText())]))
    return groups


def refreshVariables(self) -> None:
    """Fill the Variables tree again from the current state."""
    tree = self.SettingsWindow.VariablesTree
    tree.clear()
    for group, members in variableGroups(self):
        top = qtw.QTreeWidgetItem([group, ""])
        for name, value in members:
            top.addChild(qtw.QTreeWidgetItem([name, describe(value)]))
        tree.addTopLevelItem(top)
        top.setExpanded(True)
    tree.resizeColumnToContents(0)


def _toggle(self) -> None:
    sw = self.SettingsWindow
    tabs = sw.SettingsTabGroup
    shown = sw.ShowVariables.isChecked()
    tabs.setTabVisible(tabs.indexOf(sw.VariablesTab), shown)
    if shown:
        refreshVariables(self)
        tabs.setCurrentWidget(sw.VariablesTab)


def connectVariables(self) -> None:
    """Called once from slotsSignals: the button shows/hides the tab; the tab refreshes when shown."""
    sw = self.SettingsWindow
    tabs = sw.SettingsTabGroup
    tabs.setTabVisible(tabs.indexOf(sw.VariablesTab), False)
    sw.ShowVariables.toggled.connect(lambda *_: _toggle(self))
    tabs.currentChanged.connect(lambda i: refreshVariables(self) if tabs.widget(i) is sw.VariablesTab else None)
