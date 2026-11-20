"""Math, save and export operation callbacks."""
import os
import re
import sys
import traceback
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from . import appClass
from .appClass import *
import matplotlib


def mathCallbacks(self):
    """Math → Evaluate: re-evaluate the selected custom Math mask.

    The formula is MATLAB syntax over the other custom mask IDs (``A``, ``B``, ...) and is
    evaluated by :func:`callbacks.compute.mask_math.evaluate_mask_formula` (no ``eval``).
    """
    from .customDetectorCallbacks import customDetectorCallbacks  # noqa: E402
    customDetectorCallbacks(self, source=self.SettingsWindow.MathEval)


def saveCallbacks(self):
    """Save the images selected in the Save window (see callbacks.save_export)."""
    from .save_export import saveImages  # noqa: E402
    return saveImages(self)


def exportCallbacks(self):
    """Export the dataset as set up in the Save window (see callbacks.save_export)."""
    from .save_export import exportDataset  # noqa: E402
    return exportDataset(self)


def axeDirCallbacks(self):
    pass  # TODO


def saveVect(self):
    """Save the two components of the CoM/DPC vector field as CoMX and CoMY float32 TIFFs."""
    import os
    from .io.export import save_tiff  # noqa: E402
    from .save_export import imageFilename  # noqa: E402
    written = []
    for id in ("CoMX", "CoMY"):
        if self.Fig[id] is not None and self.Fig[id].Image is not None:
            path = os.path.join(self.SaveWindow.SaveDir.text(), imageFilename(self, id, "tif"))
            save_tiff(path, self.Fig[id].Image)
            written.append(path)
    return written
