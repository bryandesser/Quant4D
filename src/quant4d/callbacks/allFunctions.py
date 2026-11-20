"""Deprecated: the old catch-all module of the MATLAB port.

Every function that used to live here has a proper home now (see the table
below).  Importing a name from ``quant4d.callbacks.allFunctions`` still works, but
issues a :class:`DeprecationWarning` naming the module to import it from
instead.  The module will be removed in Quant4D 2.0.

Example::

    from quant4d.callbacks.allFunctions import plotImage     # deprecated
    from quant4d.callbacks.plotting import plotImage         # use this

The data classes that were re-exported here with ``from callbacks.appClass
import *`` (``D``, ``P``, ...) are served the same way, from
:mod:`quant4d.callbacks.appClass`.
"""
from __future__ import annotations

import importlib
import warnings
from typing import Any

#: The package these modules live in (``quant4d``), so the table below survives a rename.
_ROOT = __name__.split(".")[0]

#: Old name → module that defines it now (within the package).
MOVED: dict[str, str] = {
    "InteractiveAnnulus": "annotationsClasses.interactiveAnnulus",
    "InteractiveCircle": "annotationsClasses.interactiveCircle",
    "InteractivePoint": "annotationsClasses.interactivePoint",
    "autoAlign": "callbacks.alignment",
    "crossAlign": "callbacks.alignment",
    "moveTransBeam": "callbacks.alignment",
    "transBeamCallbacks": "callbacks.alignment",
    "annularDetectorCallbacks": "callbacks.annularDetectorCallbacks",
    "axeDirCallbacks": "callbacks.data_ops",
    "exportCallbacks": "callbacks.data_ops",
    "mathCallbacks": "callbacks.data_ops",
    "saveCallbacks": "callbacks.data_ops",
    "saveVect": "callbacks.data_ops",
    "datasetOptCallbacks": "callbacks.datasetOptCallbacks",
    "clearDetectors": "callbacks.detector",
    "customDetectorCallbacks": "callbacks.detector",
    "detectorModeCallbacks": "callbacks.detector",
    "detrCoordCallbacks": "callbacks.detector",
    "importCallbacks": "callbacks.importCallbacks",
    "gatherImportOptions": "callbacks.import_io",
    "getImportInfo": "callbacks.import_io",
    "importBoxInput": "callbacks.import_io",
    "importData": "callbacks.import_io",
    "importFileType": "callbacks.import_io",
    "importMask": "callbacks.import_io",
    "importSelectFile": "callbacks.import_io",
    "rangeImportExport": "callbacks.import_io",
    "unloadData": "callbacks.import_io",
    "prepDM": "callbacks.io.dm",
    "finishImport": "callbacks.io.file_reader",
    "prepareData": "callbacks.io.file_reader",
    "readFile": "callbacks.io.file_reader",
    "displayCallbacks": "callbacks.plotting",
    "plotAllPatterns": "callbacks.plotting",
    "plotColorWheel": "callbacks.plotting",
    "plotImage": "callbacks.plotting",
    "plotVectorField": "callbacks.plotting",
    "toUpdateImage": "callbacks.plotting",
    "updateDispImgStats": "callbacks.plotting",
    "updateImagesCallbacks": "callbacks.plotting",
    "previewCallbacks": "callbacks.previewCallbacks",
    "realSpaceROICallbacks": "callbacks.realSpaceROICallbacks",
    "debugImport": "callbacks.startup",
    "enableWindows": "callbacks.startup",
    "getDecorSize": "callbacks.startup",
    "reinitializeUI": "callbacks.startup",
    "resetQuant4DCallbacks": "callbacks.startup",
    "slotsSignals": "callbacks.startup",
    "startupFcn": "callbacks.startup",
    "unlockScanDir": "callbacks.startup",
    "importThread": "callbacks.threading_workers",
    "Worker": "callbacks.utils",
    "WorkerSignals": "callbacks.utils",
    "breakpoint": "callbacks.utils",
    "checkNaN": "callbacks.utils",
    "isDiffToPrev": "callbacks.utils",
    "notifDLG": "callbacks.utils",
    "virtualApertureCallbacks": "callbacks.virtualApertureCallbacks",
    "hideAllWindows": "callbacks.window_manager",
    "on_ShowImportWdw_triggered": "callbacks.window_manager",
    "resizeWindowCallbacks": "callbacks.window_manager",
    "showAllWindows": "callbacks.window_manager",
    "showWindowCallbacks": "callbacks.window_manager",
    "toggleWindows": "callbacks.window_manager",
    "unHideOpenWindows": "callbacks.window_manager",
}

__all__ = sorted(MOVED)


def _new_home(name: str) -> str | None:
    if name in MOVED:
        return MOVED[name]
    if not name.startswith("_") and hasattr(importlib.import_module(f"{_ROOT}.callbacks.appClass"), name):
        return "callbacks.appClass"
    return None


def __getattr__(name: str) -> Any:
    module = _new_home(name)
    if module is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    warnings.warn(f"{_ROOT}.callbacks.allFunctions.{name} is deprecated and will be removed in Quant4D 2.0; "
                  f"import it from {_ROOT}.{module} instead", DeprecationWarning, stacklevel=2)
    return getattr(importlib.import_module(f"{_ROOT}.{module}"), name)


def __dir__() -> list[str]:
    return __all__
