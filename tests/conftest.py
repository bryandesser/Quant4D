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
# Minimal synthetic 4D-STEM dataset
# ---------------------------------------------------------------------------
SCAN_X, SCAN_Y, DET_X, DET_Y = 8, 8, 32, 32


@pytest.fixture(scope="session")
def synthetic_data() -> np.ndarray:
    """Return a tiny (8x8 real, 32x32 detector) float32 4D-STEM dataset."""
    rng = np.random.default_rng(42)
    # shape: (SCAN_X * SCAN_Y, DET_X * DET_Y)  — the flat 2D layout used internally
    flat = rng.random((SCAN_X * SCAN_Y, DET_X * DET_Y), dtype=np.float32)
    return flat


# ---------------------------------------------------------------------------
# App-level fixture
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def app_session(tmp_path_factory, synthetic_data):
    """
    Launch pyQuant4D once for the whole test session, pre-loaded with
    synthetic data so detector-mode and display tests run without file I/O.

    Uses session scope because constructing the full Qt application is slow.
    Tests that mutate state heavily should use the function-scoped `app`
    fixture instead (which reloads).
    """
    from Quant4D_app import MainWindow  # adjust import to actual entry point

    win = MainWindow()

    # Inject synthetic data directly so we bypass the file-import pipeline
    win.D.Data = synthetic_data
    win.D.ScanX = SCAN_X
    win.D.ScanY = SCAN_Y
    win.D.DetX = DET_X
    win.D.DetY = DET_Y
    win.D.Loaded = True
    win.D.GPU = None   # CPU-only by default; GPU fixture overrides

    win.show()
    yield win
    win.close()


@pytest.fixture()
def app(qtbot, tmp_path, synthetic_data):
    """
    Function-scoped app fixture — a fresh MainWindow each test.
    Use this whenever the test modifies persistent state (mode changes,
    signal wiring, annotations).
    """
    from Quant4D_app import MainWindow

    win = MainWindow()
    qtbot.addWidget(win)

    win.D.Data = synthetic_data.copy()
    win.D.ScanX = SCAN_X
    win.D.ScanY = SCAN_Y
    win.D.DetX = DET_X
    win.D.DetY = DET_Y
    win.D.Loaded = True
    win.D.GPU = None
    win.show()
    return win


# ---------------------------------------------------------------------------
# Sample file fixtures (created on-the-fly from synthetic data)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def sample_raw_file(tmp_path_factory, synthetic_data):
    """Write a minimal EMPAD-style raw binary file and return its path."""
    p = tmp_path_factory.mktemp("data") / "sample_8x8_32x32.raw"
    # EMPAD: raw float32, no header, row-major
    synthetic_data.astype("<f4").tofile(p)
    return p


@pytest.fixture(scope="session")
def sample_hdf5_file(tmp_path_factory, synthetic_data):
    """Write a minimal HDF5 file containing the synthetic data."""
    h5py = pytest.importorskip("h5py")
    p = tmp_path_factory.mktemp("data") / "sample.h5"
    with h5py.File(p, "w") as f:
        f.create_dataset("data", data=synthetic_data.reshape(SCAN_X, SCAN_Y, DET_X, DET_Y))
    return p


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
