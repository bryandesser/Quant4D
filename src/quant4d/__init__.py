"""Quant4D from Python: ``quant4d.show(datacube)``.

>>> import py4DSTEM, quant4d
>>> datacube = py4DSTEM.read("scan.h5")
>>> win = quant4d.show(datacube)          # opens Quant4D with the data loaded

In a notebook, run ``%gui qt`` first: ``show`` then returns at once and the
window stays live.  Read the results back from the window afterwards:

>>> win.apply_calibration(datacube)        # beam centre, scale, semi-angle, scan step
>>> adf = win.image("Real")                # (Rx, Ry), as shown in Quant4D
>>> detector = win.mask()                  # the current detector, (Qx, Qy)
  In a plain script, ``show`` runs the Qt event loop until
Quant4D is closed (pass ``block=False`` to return the window instead).
"""
from __future__ import annotations

__all__ = ["show", "__version__"]

try:
    from importlib.metadata import version as _version
    __version__ = _version("quant4d")
except Exception:              # running from a source checkout without installing
    __version__ = "development version"


def _event_loop_running() -> bool:
    """True when an event loop already serves Qt (IPython ``%gui qt``)."""
    try:
        from IPython import get_ipython
    except ImportError:
        return False
    ip = get_ipython()
    return bool(ip is not None and getattr(ip, "active_eventloop", None))


def show(data, calibration=None, *, name: str = "py4DSTEM DataCube", kV: float | None = None,
         block: bool | None = None, copy: bool = True):
    """Open Quant4D with *data* loaded and return its main window.

    Parameters
    ----------
    data : py4DSTEM.DataCube or array of shape (ry, rx, py, px)
        A DataCube brings its calibration (beam centre, detector scale,
        convergence angle, scan step); py4DSTEM's (Rx, Ry, Qx, Qy) axes are
        Quant4D's (ry, rx, py, px), so the array is used as it is.
    calibration : callbacks.io.emd.EmdCalibration, optional
        Overrides the DataCube's calibration (Quant4D's (x, y) order).
    name : str
        Window title and file-name prefix for saving.
    kV : float, optional
        Accelerating voltage, to convert a calibration in Å⁻¹ to mrad.
    block : bool, optional
        Run the Qt event loop until the window is closed.  Default: only when
        no event loop is running already (a script, not ``%gui qt``).
    copy : bool
        Work on a copy (default), so the DataCube is never changed.  ``False``
        shares its array (no extra memory for a large dataset); the dataset
        options that change data in place (Set NaNs to 0, Swap Byte Order)
        then make a copy first.

    Returns
    -------
    The main window.  Read results back with its methods (py4DSTEM's
    conventions): ``calibration()``, ``apply_calibration(datacube)``,
    ``image(id)``, ``images()`` and ``mask(id)``.
    """
    import os
    import sys

    os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
    from PyQt5 import QtWidgets as qtw

    app = qtw.QApplication.instance() or qtw.QApplication(sys.argv[:1] or ["quant4d"])
    from .callbacks.guiClass import MainWindow
    from .callbacks.py4dstem_bridge import loadDataCube

    win = MainWindow()
    win.embedded = True            # closing it closes Quant4D's windows, not the Python session
    win.show()
    loadDataCube(win, data, name=name, calibration=calibration, kV=kV, copy=copy)
    if block is None:
        block = not _event_loop_running()
    if block:
        app.exec_()
    return win
