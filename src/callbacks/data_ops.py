"""Math, save and export operation callbacks."""
import os
import re
import sys
import traceback
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *
import matplotlib


def mathCallbacks(self):
    """
    Evaluate the formula in MathFormula (CustMod).

    Supported variables (case-sensitive):
        A   – current Real image (self.Fig.Real.Image)
        B   – current DfrnMask image (self.Fig.DfrnMask.Image)
        C   – diffraction preview (self.Fig.Dfrn.Image if set)
        D   – CoM magnitude (self.Fig.CoMX / CoMY combined, if available)

    Supported Python / numpy operators:
        +  -  *  /  **  @  &  |  ~  .T  np.xxx(...)

    MATLAB shorthands translated before evaluation:
        .^  →  **      element-wise power
        .*  →  *       element-wise multiply (arrays multiply element-wise in numpy anyway)
        .'  →  .T      element-wise transpose
        end →  -1      (simple end-of-array alias)
        ^   →  **      (scalar power fall-through)

    The result is stored in self.Fig.Real.Image and plotted.
    """
    formula = self.SettingsWindow.MathFormula.toPlainText().strip()
    if not formula:
        return

    # ── Translate MATLAB shorthands → Python/numpy ───────────────────────
    formula = formula.replace('.^', '**')   # element-wise power
    formula = formula.replace('.*', '*')    # element-wise multiply
    formula = formula.replace(".'", '.T')   # transpose
    formula = formula.replace('end', '-1')  # end-of-array index
    # bare ^ that wasn't already converted (scalar context)
    formula = re.sub(r'(?<!\*)\^', '**', formula)

    # ── Build evaluation namespace ────────────────────────────────────────
    def _safe_img(img):
        return np.ma.masked_invalid(img).astype(np.float64) if img is not None else None

    ns = {
        'np': np,
        'A': _safe_img(self.Fig.Real.Image),
        'B': _safe_img(self.Fig.DfrnMask.Image),
        'C': _safe_img(getattr(self.Fig.Dfrn, 'Image', None)),
        'D': _safe_img(getattr(self.Fig, 'CoMMag', None)),
        'abs': np.abs,
        'sum': np.nansum,
        'mean': np.nanmean,
        'max': np.nanmax,
        'min': np.nanmin,
        'sqrt': np.sqrt,
        'log': np.log,
        'log2': np.log2,
        'exp': np.exp,
        'fft': np.fft.fft2,
        'ifft': np.fft.ifft2,
    }

    # ── Evaluate ─────────────────────────────────────────────────────────
    try:
        result = eval(formula, {"__builtins__": {}}, ns)  # restrict builtins
        result = np.array(result, dtype=np.float64)
    except Exception as exc:
        qtw.QMessageBox.warning(
            self, "Math formula error",
            f"Could not evaluate formula:\n{formula}\n\nError: {exc}"
        )
        return

    # ── Store and display ─────────────────────────────────────────────────
    self.Fig.Real.Image = result
    from callbacks.plotting import plotImage  # noqa: E402  (deferred to avoid circular import)
    plotImage(self, 'Real')


def saveCallbacks(self):
    """Save the images selected in the Save window (see callbacks.save_export)."""
    from callbacks.save_export import saveImages  # noqa: E402
    return saveImages(self)


def exportCallbacks(self):
    """Export the dataset as set up in the Save window (see callbacks.save_export)."""
    from callbacks.save_export import exportDataset  # noqa: E402
    return exportDataset(self)


def axeDirCallbacks(self):
    pass  # TODO


def saveVect(self):
    """Save the two components of the CoM/DPC vector field as CoMX and CoMY float32 TIFFs."""
    import os
    from callbacks.io.export import save_tiff  # noqa: E402
    from callbacks.save_export import imageFilename  # noqa: E402
    written = []
    for id in ("CoMX", "CoMY"):
        if self.Fig[id] is not None and self.Fig[id].Image is not None:
            path = os.path.join(self.SaveWindow.SaveDir.text(), imageFilename(self, id, "tif"))
            save_tiff(path, self.Fig[id].Image)
            written.append(path)
    return written
