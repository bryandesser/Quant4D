import matplotlib.backend_bases
import os
import sys
import traceback
import re
import gc
import psutil
import importlib
import h5py
import matplotlib
import time
from PIL import Image
import numpy as np
try:
    import torch
except ImportError:
    # torch is an optional dependency (install with: pip install pyquant4d[gpu])
    # Provide a null-object stub so all torch.cuda.* call sites work without
    # modification and simply report zero GPUs available.
    class _TorchStub:                                        # noqa: E302
        class cuda:
            @staticmethod
            def is_available(): return False
            @staticmethod
            def device_count(): return 0

            @staticmethod
            def get_device_properties(i):
                raise RuntimeError("torch not installed; install pyquant4d[gpu]")

            @staticmethod
            def get_device_name(i):
                raise RuntimeError("torch not installed; install pyquant4d[gpu]")

        @staticmethod
        def device(x): return x
    torch = _TorchStub()  # type: ignore[assignment]
from multiprocessing.pool import ThreadPool
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *
# annotationsClasses re-exports and virtualApertureCallbacks are loaded lazily
# (see __getattr__ at the bottom of this file) to avoid sys.path ordering
# issues during the editable-install import-test phase of CI.


def gatherImportOptions(self, preview):
    """Delegate to callbacks.import_io.gatherImportOptions."""
    from callbacks.import_io import gatherImportOptions as _impl  # noqa: E402
    return _impl(self, preview)


def importCallbacks(self):
    """Delegate to the full implementation in importCallbacks.py."""
    from callbacks.importCallbacks import importCallbacks as _impl  # noqa: E402
    _impl(self)


def previewCallbacks(self):
    """Delegate to the full implementation in previewCallbacks.py."""
    from callbacks.previewCallbacks import previewCallbacks as _impl  # noqa: E402
    _impl(self)


def notifDLG(self, parent, icon="", msg="", ttl="", opt=[]):
    """Delegate to callbacks.utils.notifDLG."""
    from callbacks.utils import notifDLG as _impl  # noqa: E402
    return _impl(self, parent, icon, msg, ttl, opt)


def checkNaN(self, image, preview=False):
    """Delegate to callbacks.utils.checkNaN."""
    from callbacks.utils import checkNaN as _impl  # noqa: E402
    return _impl(self, image, preview)


def importSelectFile(self):
    """Delegate to callbacks.import_io.importSelectFile."""
    from callbacks.import_io import importSelectFile as _impl  # noqa: E402
    _impl(self)


def importFileType(self):
    """Delegate to callbacks.import_io.importFileType."""
    from callbacks.import_io import importFileType as _impl  # noqa: E402
    return _impl(self)


def importBoxInput(self):
    """Delegate to callbacks.import_io.importBoxInput."""
    from callbacks.import_io import importBoxInput as _impl  # noqa: E402
    return _impl(self)


def saveCallbacks(self):
    """Delegate to callbacks.data_ops.saveCallbacks."""
    from callbacks.data_ops import saveCallbacks as _impl  # noqa: E402
    _impl(self)


def exportCallbacks(self):
    """Delegate to callbacks.data_ops.exportCallbacks."""
    from callbacks.data_ops import exportCallbacks as _impl  # noqa: E402
    _impl(self)


def axeDirCallbacks(self):
    """Delegate to callbacks.data_ops.axeDirCallbacks."""
    from callbacks.data_ops import axeDirCallbacks as _impl  # noqa: E402
    _impl(self)


def realSpaceROICallbacks(self):
    """Delegate to the full implementation in realSpaceROICallbacks.py."""
    from callbacks.realSpaceROICallbacks import realSpaceROICallbacks as _impl  # noqa: E402
    _impl(self)


def clearDetectors(self):
    """Delegate to callbacks.detector.clearDetectors."""
    from callbacks.detector import clearDetectors as _impl  # noqa: E402
    _impl(self)


def detectorModeCallbacks(self):
    """Delegate to callbacks.detector.detectorModeCallbacks."""
    from callbacks.detector import detectorModeCallbacks as _impl  # noqa: E402
    _impl(self)


def datasetOptCallbacks(self):
    """Delegate to the full implementation in datasetOptCallbacks.py."""
    from callbacks.datasetOptCallbacks import datasetOptCallbacks as _impl  # noqa: E402
    _impl(self)


def getImportInfo(self):
    """Delegate to callbacks.import_io.getImportInfo."""
    from callbacks.import_io import getImportInfo as _impl  # noqa: E402
    return _impl(self)


def transBeamCallbacks(self):
    """Delegate to callbacks.alignment.transBeamCallbacks."""
    from callbacks.alignment import transBeamCallbacks as _impl  # noqa: E402
    _impl(self)


def moveTransBeam(self):
    """Delegate to callbacks.alignment.moveTransBeam."""
    from callbacks.alignment import moveTransBeam as _impl  # noqa: E402
    _impl(self)


def virtualApertureCallbacks(self):
    """Delegate to the full implementation in virtualApertureCallbacks.py."""
    from callbacks.virtualApertureCallbacks import virtualApertureCallbacks as _impl  # noqa: E402
    _impl(self)


def autoAlign(self):
    """Delegate to callbacks.alignment.autoAlign."""
    from callbacks.alignment import autoAlign as _impl  # noqa: E402
    return _impl(self)


def crossAlign(self):
    """Delegate to callbacks.alignment.crossAlign."""
    from callbacks.alignment import crossAlign as _impl  # noqa: E402
    _impl(self)


def customDetectorCallbacks(self):
    """Delegate to callbacks.detector.customDetectorCallbacks."""
    from callbacks.detector import customDetectorCallbacks as _impl  # noqa: E402
    _impl(self)


def mathCallbacks(self):
    """Delegate to callbacks.data_ops.mathCallbacks."""
    from callbacks.data_ops import mathCallbacks as _impl  # noqa: E402
    return _impl(self)


def saveVect(self):
    """Delegate to callbacks.data_ops.saveVect."""
    from callbacks.data_ops import saveVect as _impl  # noqa: E402
    _impl(self)


def resizeWindowCallbacks(self):
    """Delegate to callbacks.window_manager.resizeWindowCallbacks."""
    from callbacks.window_manager import resizeWindowCallbacks as _impl  # noqa: E402
    _impl(self)


def updateImagesCallbacks(self):
    """Delegate to callbacks.plotting.updateImagesCallbacks."""
    from callbacks.plotting import updateImagesCallbacks as _impl  # noqa: E402
    _impl(self)


def unlockScanDir(self):
    """Delegate to callbacks.startup.unlockScanDir."""
    from callbacks.startup import unlockScanDir as _impl  # noqa: E402
    _impl(self)


def debugImport(self):
    """Delegate to callbacks.startup.debugImport."""
    from callbacks.startup import debugImport as _impl  # noqa: E402
    _impl(self)


def breakpoint(self):
    """Delegate to callbacks.utils.breakpoint."""
    from callbacks.utils import breakpoint as _impl  # noqa: E402
    _impl(self)


def slotsSignals(self):
    """Delegate to callbacks.startup.slotsSignals."""
    from callbacks.startup import slotsSignals as _impl  # noqa: E402
    _impl(self)


def toggleWindows(self):
    """Delegate to callbacks.window_manager.toggleWindows."""
    from callbacks.window_manager import toggleWindows as _impl  # noqa: E402
    _impl(self)


def showAllWindows(self):
    """Delegate to callbacks.window_manager.showAllWindows."""
    from callbacks.window_manager import showAllWindows as _impl  # noqa: E402
    _impl(self)


def hideAllWindows(self):
    """Delegate to callbacks.window_manager.hideAllWindows."""
    from callbacks.window_manager import hideAllWindows as _impl  # noqa: E402
    _impl(self)


def unHideOpenWindows(self):
    """Delegate to callbacks.window_manager.unHideOpenWindows."""
    from callbacks.window_manager import unHideOpenWindows as _impl  # noqa: E402
    _impl(self)


def on_ShowImportWdw_triggered(self):
    """Delegate to callbacks.window_manager.on_ShowImportWdw_triggered."""
    from callbacks.window_manager import on_ShowImportWdw_triggered as _impl  # noqa: E402
    _impl(self)


def plotColorWheel(self):
    """Delegate to callbacks.plotting.plotColorWheel."""
    from callbacks.plotting import plotColorWheel as _impl  # noqa: E402
    _impl(self)


# WorkerSignals is defined in callbacks.utils; re-exported here for
# backward-compatibility with code that imports from allFunctions.
from callbacks.utils import WorkerSignals  # noqa: F401,E402
# Worker is defined in callbacks.utils; re-exported here for
# backward-compatibility with code that imports from allFunctions.
from callbacks.utils import Worker  # noqa: F401,E402


def detrCoordCallbacks(self):
    """Delegate to callbacks.detector.detrCoordCallbacks."""
    from callbacks.detector import detrCoordCallbacks as _impl  # noqa: E402
    _impl(self)


def annularDetectorCallbacks(self):
    """Delegate to the full implementation in annularDetectorCallbacks.py."""
    from callbacks.annularDetectorCallbacks import annularDetectorCallbacks as _impl  # noqa: E402
    _impl(self)


def plotAllPatterns(self):
    """Delegate to callbacks.plotting.plotAllPatterns."""
    from callbacks.plotting import plotAllPatterns as _impl  # noqa: E402
    _impl(self)


def toUpdateImage(self):
    """Delegate to callbacks.plotting.toUpdateImage."""
    from callbacks.plotting import toUpdateImage as _impl  # noqa: E402
    return _impl(self)


# importThread is defined in callbacks.threading_workers; re-exported here for
# backward-compatibility with code that imports from allFunctions.
from callbacks.threading_workers import importThread  # noqa: F401,E402


def prepEMPAD(self):
    """Delegate to callbacks.io.empad.prepEMPAD."""
    from callbacks.io.empad import prepEMPAD as _impl  # noqa: E402
    _impl(self)


def prepDM(self):
    """Delegate to callbacks.io.dm.prepDM."""
    from callbacks.io.dm import prepDM as _impl  # noqa: E402
    return _impl(self)


def readFile(self):
    """Delegate to callbacks.io.file_reader.readFile."""
    from callbacks.io.file_reader import readFile as _impl  # noqa: E402
    _impl(self)


def prepareData(self):
    """Delegate to callbacks.io.file_reader.prepareData."""
    from callbacks.io.file_reader import prepareData as _impl  # noqa: E402
    _impl(self)


def finishImport(self):
    """Delegate to callbacks.io.file_reader.finishImport."""
    from callbacks.io.file_reader import finishImport as _impl  # noqa: E402
    _impl(self)


def reinitializeUI(self):
    """Delegate to callbacks.startup.reinitializeUI."""
    from callbacks.startup import reinitializeUI as _impl  # noqa: E402
    _impl(self)


def startupFcn(self):
    """Delegate to callbacks.startup.startupFcn."""
    from callbacks.startup import startupFcn as _impl  # noqa: E402
    _impl(self)


def resetQuant4DCallbacks(self):
    """Delegate to callbacks.startup.resetQuant4DCallbacks."""
    from callbacks.startup import resetQuant4DCallbacks as _impl  # noqa: E402
    _impl(self)


def rangeImportExport(self, src):
    """Delegate to callbacks.import_io.rangeImportExport."""
    from callbacks.import_io import rangeImportExport as _impl  # noqa: E402
    return _impl(self, src)


def unloadData(self, keep_p=False):
    """Delegate to callbacks.import_io.unloadData."""
    from callbacks.import_io import unloadData as _impl  # noqa: E402
    _impl(self, keep_p)


def enableWindows(self, sw=True):
    """Delegate to callbacks.startup.enableWindows."""
    from callbacks.startup import enableWindows as _impl  # noqa: E402
    _impl(self, sw)


def importData(self):
    """Delegate to callbacks.import_io.importData."""
    from callbacks.import_io import importData as _impl  # noqa: E402
    _impl(self)


def getDecorSize(self):
    """Delegate to callbacks.startup.getDecorSize."""
    from callbacks.startup import getDecorSize as _impl  # noqa: E402
    return _impl(self)


def displayCallbacks(self):
    """Delegate to callbacks.plotting.displayCallbacks."""
    from callbacks.plotting import displayCallbacks as _impl  # noqa: E402
    return _impl(self)


def plotImage(self, id):
    """Delegate to callbacks.plotting.plotImage."""
    from callbacks.plotting import plotImage as _impl  # noqa: E402
    _impl(self, id)


def updateDispImgStats(self, id, minVal, maxVal, limitLow, limitHigh, limitRange):
    """Delegate to callbacks.plotting.updateDispImgStats."""
    from callbacks.plotting import updateDispImgStats as _impl  # noqa: E402
    _impl(self, id, minVal, maxVal, limitLow, limitHigh, limitRange)


def plotVectorField(self, id):
    """Delegate to callbacks.plotting.plotVectorField."""
    from callbacks.plotting import plotVectorField as _impl  # noqa: E402
    _impl(self, id)


def isDiffToPrev(self, name, val):
    """Delegate to callbacks.utils.isDiffToPrev."""
    from callbacks.utils import isDiffToPrev as _impl  # noqa: E402
    return _impl(self, name, val)


def showWindowCallbacks(self):
    """Delegate to callbacks.window_manager.showWindowCallbacks."""
    from callbacks.window_manager import showWindowCallbacks as _impl  # noqa: E402
    _impl(self)


def importMask(self, space):
    """Delegate to callbacks.import_io.importMask."""
    from callbacks.import_io import importMask as _impl  # noqa: E402
    return _impl(self, space)


# ---------------------------------------------------------------------------
# Lazy re-exports for backward-compatibility
# ---------------------------------------------------------------------------
# Code that does  'from callbacks.allFunctions import InteractiveCircle'
# (or the Annulus / Point variants) still works at runtime, but the import
# of annotationsClasses is deferred until the name is actually requested.
# This avoids sys.path ordering issues during the editable-install CI
# import-test, where the full package graph isn't yet wired up at the moment
# callbacks.allFunctions is first imported.

_LAZY_CLASSES = {
    'InteractiveCircle': 'annotationsClasses.interactiveCircle',
    'InteractiveAnnulus': 'annotationsClasses.interactiveAnnulus',
    'InteractivePoint': 'annotationsClasses.interactivePoint',
}


def __getattr__(name):
    if name in _LAZY_CLASSES:
        import importlib
        mod = importlib.import_module(_LAZY_CLASSES[name])
        obj = getattr(mod, name)
        # Cache on the module so subsequent accesses bypass __getattr__
        globals()[name] = obj
        return obj
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
