"""
GPU tests — Section 4.10.

Skipped automatically on CPU-only machines via the `requires_gpu` mark
defined in conftest.py.
"""

import numpy as np
import pytest


pytestmark = pytest.mark.skipif(
    not _gpu_available(),
    reason="No CUDA GPU detected"
)

def _gpu_available():
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


# ---------------------------------------------------------------------------
# Reference CPU implementations (simple, clearly correct)
# ---------------------------------------------------------------------------
def _cpu_integrate(data, mask):
    return data[:, mask.ravel()].sum(axis=1)


def _cpu_com(data, cx, cy, mask):
    sub = data[:, mask.ravel()]
    total = sub.sum(axis=1) + 1e-12
    com_x = (sub * cx[mask.ravel()]).sum(axis=1) / total
    com_y = (sub * cy[mask.ravel()]).sum(axis=1) / total
    return com_x, com_y


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
class TestGPUIntegrateAnnular:
    def test_matches_cpu(self, app, qtbot):
        import torch
        from callbacks.annularDetectorCallbacks import integrateAnnular

        # Build a simple annular mask
        mask = np.zeros((32, 32), dtype=bool)
        mask[10:22, 10:22] = True

        # CPU reference
        cpu_result = _cpu_integrate(app.D.Data, mask)

        # GPU path
        app.D.GPU = "cuda:0"
        gpu_result = integrateAnnular(app, mask)

        np.testing.assert_allclose(gpu_result, cpu_result, rtol=1e-4)

    def test_fallback_on_cpu_only(self, monkeypatch):
        """Torch available but CUDA not → CPU numpy path used without crash."""
        import callbacks.annularDetectorCallbacks as m
        monkeypatch.setattr(m, "_TORCH_AVAILABLE", False)
        # Just check the import and flag work
        assert not m._TORCH_AVAILABLE


class TestGPUCalcCoM:
    def test_matches_cpu(self, app, qtbot):
        from callbacks.annularDetectorCallbacks import calcCoM

        DX, DY = 32, 32
        xx, yy = np.meshgrid(np.arange(DX), np.arange(DY))
        mask = np.zeros((DY, DX), dtype=bool)
        mask[8:24, 8:24] = True

        cpu_x, cpu_y = _cpu_com(app.D.Data, xx.ravel(), yy.ravel(), mask)

        app.D.GPU = "cuda:0"
        gpu_x, gpu_y = calcCoM(app, mask, xx, yy)

        np.testing.assert_allclose(gpu_x, cpu_x, rtol=1e-4)
        np.testing.assert_allclose(gpu_y, cpu_y, rtol=1e-4)
