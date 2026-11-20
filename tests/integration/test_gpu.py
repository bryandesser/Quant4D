"""
GPU tests — Section 4.10.

Every detector mode is computed through the app with the dataset on the GPU
and again on the CPU (NumPy); the images must agree.  Skipped automatically
on machines without CUDA.  The torch code path itself is unit-tested on any
machine with torch (tests/unit/test_compute_torch.py, device "cpu").
"""
import numpy as np
import pytest

from conftest import set_mode


def _cuda():
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


pytestmark = [pytest.mark.gpu, pytest.mark.skipif(not _cuda(), reason="No CUDA GPU detected")]

MODES = {
    "AnnMod": ["Real"],
    "CoMMod": ["CoMX", "CoMY", "CoMMag", "CoMPh", "iCoM", "dCoM"],
    "DPCMod": ["CoMX", "CoMY", "CoMMag", "CoMPh"],
    "VrApMod": ["Real"],
    "CustMod": ["Real"],
}


def _images(app, qapp, mode):
    set_mode(app, qapp, mode)
    if mode == "CustMod" and not app.A.Custom:
        app.CDNewCircle.click()
        app.CDNewBandpass.click()
    app.UpdateImages.trigger()
    qapp.processEvents()
    return {i: np.array(app.Fig[i].Image, float) for i in MODES[mode]}


def test_dataset_is_resident_on_gpu(loaded_app, qapp):
    from quant4d.callbacks import compute
    loaded_app.D.GPU = 0
    _images(loaded_app, qapp, "AnnMod")
    info = compute.device_data_info()
    assert info is not None and info["device"].startswith("cuda"), info
    assert info["shape"] == tuple(np.asarray(loaded_app.Data).shape)


@pytest.mark.parametrize("mode", list(MODES))
def test_gpu_matches_cpu(loaded_app, qapp, mode):
    from quant4d.callbacks import compute
    loaded_app.D.GPU = 0
    gpu = _images(loaded_app, qapp, mode)
    loaded_app.D.GPU = None
    compute.release_device_data()
    cpu = _images(loaded_app, qapp, mode)
    loaded_app.D.GPU = 0
    for i in gpu:
        assert np.allclose(gpu[i], cpu[i], rtol=1e-4, atol=1e-6 * np.abs(cpu[i]).max()), f"{mode}: {i} differs"
    set_mode(loaded_app, qapp, "AnnMod")


def test_import_window_selects_the_gpu(app, qapp, sample_raw_file):
    """Through the app, not by setting D.GPU: the Import window offers the card, an import uses it."""
    from quant4d.callbacks import compute
    from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y, import_raw
    gpu = app.ImportWindow.ImpGPU.currentData()
    assert gpu is not None, f"no GPU selected; offered: {[app.ImportWindow.ImpGPU.itemText(i) for i in range(app.ImportWindow.ImpGPU.count())]}"
    import_raw(app, qapp, sample_raw_file, SCAN_X, SCAN_Y, DET_X, DET_Y)
    assert app.D.GPU == gpu
    set_mode(app, qapp, "AnnMod")
    app.UpdateImages.trigger()
    qapp.processEvents()
    info = compute.device_data_info()
    assert info is not None and info["device"].startswith("cuda"), info
