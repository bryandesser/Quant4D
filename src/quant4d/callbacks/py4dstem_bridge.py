"""py4DSTEM interoperability that needs py4DSTEM installed.

Two ways in, both through :func:`loadDataCube`:

* **File > Open with py4DSTEM Reader...** (shown only when py4DSTEM can be
  imported) reads a file with ``py4DSTEM.read``: legacy py4DSTEM files
  (0.12 and earlier) and anything else py4DSTEM reads.  EMD 1.0 files open
  through the Import window without py4DSTEM.
* :func:`quant4d.show` takes a ``py4DSTEM.DataCube`` (or a 4-D array) from
  a Python session or notebook.

The DataCube's calibration is used as for an imported EMD file: beam centre,
detector scale (mrad, or Å⁻¹ converted at the accelerating voltage),
convergence angle and scan step.
"""
from __future__ import annotations

import importlib.util
import os
from typing import Any, Optional

import numpy as np

from .io.emd import EmdCalibration

__all__ = ["ownData", "py4dstem_available", "calibrationFromPy4DSTEM", "findDataCube", "loadDataCube",
           "openWithPy4DSTEM", "connectPy4DSTEM"]


def ownData(self) -> None:
    """Before changing the dataset in place: copy it if it is the caller's array
    (``quant4d.show(..., copy=False)``), so their DataCube is left as it was."""
    if getattr(self, "_sharedData", False) and self.Data is not None:
        self.Data = np.array(self.Data, copy=True)
        self._sharedData = False


def py4dstem_available() -> bool:
    """True if py4DSTEM can be imported (without importing it: it is slow to load)."""
    return importlib.util.find_spec("py4DSTEM") is not None


def _get(getter):
    try:
        return getter()
    except Exception:          # py4DSTEM getters raise for parameters never set
        return None


def calibrationFromPy4DSTEM(datacube) -> Optional[EmdCalibration]:
    """The calibration of a py4DSTEM DataCube in Quant4D's (x, y) order, or None if it has none."""
    c = getattr(datacube, "calibration", None)
    if c is None:
        return None
    cal = EmdCalibration()
    q, qu = _get(c.get_Q_pixel_size), _get(c.get_Q_pixel_units)
    r, ru = _get(c.get_R_pixel_size), _get(c.get_R_pixel_units)
    if q and qu:
        cal.q_pixel_size, cal.q_units = float(q), str(qu)
    if r and ru:
        cal.r_pixel_size, cal.r_units = float(r), str(ru)
    origin = _get(c.get_origin_mean)
    if origin is not None and len(origin) == 2 and None not in origin and np.all(np.isfinite(origin)):
        qx0, qy0 = (float(v) for v in origin)
        cal.beam_xy = (qy0, qx0)                 # py4DSTEM Qx = rows = Quant4D y
    # py4DSTEM's probe_semiangle is the disk radius in pixels (get_probe_size); the angle is
    # convergence_semiangle_mrad
    semi, radius = _get(c.get_convergence_semiangle_mrad), _get(c.get_probe_semiangle)
    if semi:
        cal.probe_semiangle_mrad = float(semi)
    if radius:
        cal.probe_radius_px = float(radius)
    return cal


def findDataCube(obj):
    """The first DataCube in what ``py4DSTEM.read`` returned (a DataCube, a tree root or a list)."""
    if obj is None:
        return None
    if type(obj).__name__ == "DataCube":
        return obj
    if isinstance(obj, (list, tuple)):
        for item in obj:
            found = findDataCube(item)
            if found is not None:
                return found
        return None
    branch = getattr(obj, "_branch", None)            # an emdfile tree node: search its children
    values: Any = getattr(branch, "values", None)
    children: list = list(values()) if values is not None else []
    for child in children:
        found = findDataCube(child)
        if found is not None:
            return found
    return None


def loadDataCube(self, data, name: str = "py4DSTEM DataCube", calibration: Optional[EmdCalibration] = None,
                 kV: Optional[float] = None, source_path: str = "", copy: bool = True) -> None:
    """Load an in-memory 4-D dataset ``(ry, rx, py, px)`` as if it had been imported.

    *data* is a ``py4DSTEM.DataCube`` (its calibration is used unless
    *calibration* is given) or an array.  *kV* converts an Å⁻¹ calibration
    (default: the Import window's accelerating voltage).

    *copy*: Quant4D works on its own copy (the caller's array is never
    changed).  ``copy=False`` uses the array itself when it can (no extra
    memory); the two options that change the dataset in place (Set NaNs to 0,
    Swap Byte Order) then copy it first (:func:`ownData`).
    """
    from .appClass import D
    from .import_io import unloadData
    from .io.emd import usable_calibration
    from .io.file_reader import finishImport

    if calibration is None and hasattr(data, "calibration"):
        calibration = calibrationFromPy4DSTEM(data)
    arr = np.asarray(getattr(data, "data", data))
    if arr.ndim != 4:
        raise ValueError(f"a 4-D dataset (ry, rx, py, px) is needed, not shape {arr.shape}")
    if not arr.dtype.isnative:
        arr = arr.astype(arr.dtype.newbyteorder("="))
    code = arr.dtype.str.lstrip("<>|=")
    if code not in self.ByteSize:              # e.g. float16, bool, complex: compute in float32
        arr, code = arr.astype(np.float32), "f4"
    ny, nx, py, px = arr.shape

    self.ImportWindow.hide()
    self.ShowImportWdw.setChecked(False)
    unloadData(self)

    d = D()
    d.filePath = source_path or name
    folder, d.fileName = os.path.split(d.filePath)
    d.fileDir = (folder or os.getcwd()) + os.sep
    d.fileExt = os.path.splitext(d.fileName)[1]
    d.DataType, d.ByteSize = code, self.ByteSize[code]
    d.DNPxX = d.NPxX = px
    d.DNPxY = d.NPxY = py
    d.DNFrX = d.NFrX = nx
    d.DNFrY = d.NFrY = ny
    d.PxX1 = d.PxY1 = d.FrX1 = d.FrY1 = 0
    d.NPx, d.NPxS = np.array([px, py]), px * py
    d.NFr, d.NFrS = np.array([ny, nx]), nx * ny
    d.mem = "Physical Memory"
    d.GPU = self.ImportWindow.ImpGPU.currentData()
    d.kV = float(kV if kV else self.ImportWindow.ImpAccVolt.value())
    if calibration is not None:
        d.Calib = usable_calibration(calibration, d.kV)
        from .scan_step import unitCode
        d.ScanUnits = unitCode(calibration.r_units)
        d.ScanStep = d.ScanStepFile = float(calibration.r_pixel_size) if d.ScanUnits != "pixels" else 1.0
    d.NoteImp = f"Loaded through py4DSTEM: {d.filePath}"
    self.D = d
    self.T.prev_D = d

    # names first: the Save window reacts to them, and must not see the data before the
    # export ranges are set (prepareData)
    stem = os.path.splitext(d.fileName)[0] or "py4DSTEM"
    self.setWindowTitle(d.fileName or name)
    self.SaveWindow.SaveDir.setText(d.fileDir.rstrip(os.sep) or os.getcwd())
    self.SaveWindow.SaveImgPrefix.setText(stem + "_")

    flat = arr.reshape(ny * nx, py * px)
    self.Data = np.array(flat, order="C", copy=True) if copy else np.ascontiguousarray(flat)
    self._sharedData = (not copy) and np.shares_memory(self.Data, arr)
    self.workerThread = None
    finishImport(self)


def openWithPy4DSTEM(self, path: Optional[str] = None) -> bool:
    """Ask for a file (unless *path*), read it with ``py4DSTEM.read`` and load its first DataCube.

    Returns True if a dataset was loaded.
    """
    from PyQt5 import QtWidgets as qtw
    from .utils import notifDLG

    if not self.ImportWindow.isEnabled():     # an import is running
        return False
    if path is None:
        path, _ = qtw.QFileDialog.getOpenFileName(self, "Open with py4DSTEM Reader", os.getcwd(),
                                                  "py4DSTEM / HDF5 (*.h5 *.hdf5 *.emd *.py4dstem);;All files (*)")
        if not path:
            return False
    try:
        import py4DSTEM
        from .window_manager import busyIndicator
        with busyIndicator(self):
            result = py4DSTEM.read(path)
    except Exception as exc:                  # py4DSTEM raises many kinds of errors for unreadable files
        notifDLG(self, self, "error", f"py4DSTEM could not read\n{path}\n\n{type(exc).__name__}: {exc}",
                 "py4DSTEM Reader")
        return False
    cube = findDataCube(result)
    if cube is None:
        notifDLG(self, self, "warn", f"No 4-D DataCube found in\n{path}", "py4DSTEM Reader")
        return False
    loadDataCube(self, cube, source_path=path, copy=False)
    self._sharedData = False          # read here: nobody else holds that array
    return True


def connectPy4DSTEM(self) -> None:
    """Show File > Open with py4DSTEM Reader... only when py4DSTEM is installed; called from ``slotsSignals``."""
    action = self.actionOpen_with_py4DSTEM
    action.setVisible(py4dstem_available())
    action.triggered.connect(lambda *_: openWithPy4DSTEM(self))
