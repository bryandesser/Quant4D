"""
conftest.py — shared fixtures for the pyQuant4D test suite.

Environment assumptions
-----------------------
* QT_QPA_PLATFORM=offscreen  (set by CI; harmless locally if a display exists)
* matplotlib uses the Agg backend so no display is needed for figure tests
* Heavy-weight fixtures (full app) are session-scoped where safe; lighter
  fixtures (single widget) are function-scoped so state never leaks.
"""

import os
import numpy as np
import pytest

# Force headless matplotlib before any Qt import
import matplotlib
matplotlib.use("Agg")

# ---------------------------------------------------------------------------
# Qt / PyQt5
# ---------------------------------------------------------------------------
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtWidgets import QApplication  # noqa: E402  (must come after env set)


# ---------------------------------------------------------------------------
# GPU helper — defined before any module-level use of _gpu_available()
# ---------------------------------------------------------------------------
def _gpu_available() -> bool:
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


requires_gpu = pytest.mark.skipif(
    not _gpu_available(),
    reason="No CUDA-capable GPU detected"
)


# ---------------------------------------------------------------------------
# Synthetic 4D-STEM dataset
# ---------------------------------------------------------------------------
# Deliberately non-square scan of non-square patterns, so any x/y swap shows up.
SCAN_X, SCAN_Y, DET_X, DET_Y = 6, 4, 24, 16


def make_dataset(nfx=SCAN_X, nfy=SCAN_Y, npx=DET_X, npy=DET_Y, seed=42) -> np.ndarray:
    """A bright disc that drifts with probe position (so CoM has a known gradient) on a noisy floor.

    Returned flat, ``(frame, pixel)`` with frame = ry*nfx + rx and pixel = py*npx + px.
    """
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:npy, 0:npx]
    data = 0.05 * rng.random((nfy * nfx, npy * npx), dtype=np.float32)
    for ry in range(nfy):
        for rx in range(nfx):
            disc = np.hypot(xx - (0.58 * npx + 0.3 * rx), yy - (0.4 * npy + 0.3 * ry)) < 0.25 * npy
            data[ry * nfx + rx] += disc.ravel()
    return data


@pytest.fixture(scope="session")
def synthetic_data() -> np.ndarray:
    return make_dataset()


def wait_until(qapp, condition, timeout=20.0):
    import time
    deadline = time.time() + timeout
    while time.time() < deadline and not condition():
        qapp.processEvents()
        time.sleep(0.01)
    return condition()


def import_raw(win, qapp, path, nfx, nfy, npx, npy, dtype="f4"):
    """Import a headerless binary file through the real Import window, as a user would."""
    iw = win.ImportWindow
    win.ShowImportWdw.trigger()
    iw.ImpFilePath.setText(str(path))
    iw.ImpFilePath.editingFinished.emit()      # as if typed: runs importSelectFile as a slot
    iw.CustomButton.click()
    qapp.processEvents()
    iw.ImpDataType.setCurrentIndex(iw.ImpDataType.findData(dtype))
    for name in ("DataOffset", "FrHead", "FrFoot"):
        getattr(iw, name).setValue(0)
    for name, val in (("DNPxX", npx), ("DNPxY", npy), ("DNFrX", nfx), ("DNFrY", nfy)):
        getattr(iw, name).setValue(val)
    qapp.processEvents()
    iw.ImportDataButton.click()
    ok = wait_until(qapp, lambda: win.Data is not None and win.Data.shape == (nfx * nfy, npx * npy)
                    and win.Fig.Dfrn.Image is not None)
    assert ok, "import did not finish"


@pytest.fixture(scope="session", autouse=True)
def _no_modal_dialogs():
    """Never block on a message box: notifDLG answers '' and QMessageBox.exec returns Ok."""
    from PyQt5.QtWidgets import QMessageBox
    import pyquant4d.callbacks.utils as utils
    saved = (utils.notifDLG, QMessageBox.exec_, QMessageBox.exec)
    utils.notifDLG = lambda *a, **k: ""
    QMessageBox.exec_ = lambda self: QMessageBox.Ok
    QMessageBox.exec = lambda self: QMessageBox.Ok
    yield
    utils.notifDLG, QMessageBox.exec_, QMessageBox.exec = saved


@pytest.fixture(scope="session")
def sample_raw_file(tmp_path_factory, synthetic_data):
    """The synthetic dataset as a headerless little-endian float32 file."""
    p = tmp_path_factory.mktemp("data") / f"sample_x{SCAN_X}_y{SCAN_Y}.raw"
    synthetic_data.astype("<f4").tofile(p)
    return p


@pytest.fixture(scope="session")
def sample_hdf5_file(tmp_path_factory, synthetic_data):
    """The synthetic dataset as HDF5, canonical (ry, rx, py, px) order."""
    h5py = pytest.importorskip("h5py")
    p = tmp_path_factory.mktemp("data") / "sample.h5"
    with h5py.File(p, "w") as f:
        f.create_dataset("data", data=synthetic_data.reshape(SCAN_Y, SCAN_X, DET_Y, DET_X))
    return p


# ---------------------------------------------------------------------------
# App fixtures
# ---------------------------------------------------------------------------
@pytest.fixture()
def app(qtbot):
    """A fresh MainWindow with nothing loaded (startup state)."""
    from pyquant4d.callbacks.guiClass import MainWindow
    win = MainWindow()
    qtbot.addWidget(win)
    win.show()
    return win


@pytest.fixture(scope="module")
def loaded_app(qapp, sample_raw_file):
    """A MainWindow with the synthetic dataset imported through the Import window, all
    image windows shown.  Module-scoped (importing takes ~1 s): tests set the mode and
    controls they rely on rather than assuming what an earlier test left behind."""
    from pyquant4d.callbacks.guiClass import MainWindow
    from pyquant4d.callbacks.window_manager import showAllWindows
    win = MainWindow()
    win.show()
    import_raw(win, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
    showAllWindows(win)
    win.UpdateImages.trigger()
    qapp.processEvents()
    yield win
    win.close()
    qapp.processEvents()


def set_mode(win, qapp, mode):
    win.DetrMode.setCurrentIndex(win.DetrMode.findData(mode))
    qapp.processEvents()
    assert win.DetrMode.currentData() == mode


# ---------------------------------------------------------------------------
# Matplotlib axes fixture (headless, no Qt)
# ---------------------------------------------------------------------------
@pytest.fixture()
def mpl_fig_ax():
    """Return a fresh (fig, ax) pair using the Agg backend."""
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    yield fig, ax
    plt.close(fig)


# ---------------------------------------------------------------------------
# Rotating rectangles/polygons: drag from just outside a corner (MATLAB style)
# ---------------------------------------------------------------------------
def just_outside(ax, corner, centre, px=14.0):
    """A data point *px* screen pixels beyond *corner*, away from *centre*: where the shape rotates."""
    c, k = ax.transData.transform(centre), ax.transData.transform(corner)
    d = (k - c) / np.hypot(*(k - c))
    return ax.transData.inverted().transform(k + px * d)


def turned(p, centre, deg):
    """*p* turned by *deg* about *centre* (data coordinates, +x towards +y)."""
    a = np.radians(deg)
    v = np.asarray(p, float) - np.asarray(centre, float)
    return np.asarray(centre, float) + np.array([np.cos(a) * v[0] - np.sin(a) * v[1],
                                                 np.sin(a) * v[0] + np.cos(a) * v[1]])
