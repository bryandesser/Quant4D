"""
The Import window's GPU list.  Startup used to fill it with the detected GPUs and then
clear it again, so a GPU could never be chosen in the app.  A fake CUDA module stands in
for real hardware here; tests/integration/test_gpu.py checks a real card end to end.
"""
import types

import pytest

GB = 1024 ** 3


@pytest.fixture()
def fake_cuda(monkeypatch):
    import callbacks.import_io as import_io
    import callbacks.startup as startup
    cuda = types.SimpleNamespace(
        device_count=lambda: 2, is_available=lambda: True,
        get_device_properties=lambda i: types.SimpleNamespace(total_memory=(4, 8)[i] * GB),
        get_device_name=lambda i: ("Small GPU", "Big GPU")[i],
        mem_get_info=lambda i=0: (7 * GB, 8 * GB))
    fake = types.SimpleNamespace(cuda=cuda, device=lambda x: x)
    monkeypatch.setattr(startup, "torch", fake)
    monkeypatch.setattr(import_io, "torch", fake)
    return cuda


def _items(app):
    combo = app.ImportWindow.ImpGPU
    return [(combo.itemText(i), combo.itemData(i)) for i in range(combo.count())]


def test_detected_gpus_are_listed_and_largest_selected(fake_cuda, app):
    assert _items(app) == [("Small GPU", 0), ("Big GPU", 1), ("GPU off", None)]
    assert app.ImportWindow.ImpGPU.currentData() == 1
    assert type(app.ImportWindow.ImpGPU.currentData()) is int


def test_memory_note_never_switches_the_gpu_off(fake_cuda, app, qapp, sample_raw_file):
    from conftest import DET_X, DET_Y, SCAN_X, SCAN_Y
    iw = app.ImportWindow
    app.ShowImportWdw.trigger()
    iw.ImpFilePath.setText(str(sample_raw_file))
    iw.ImpFilePath.editingFinished.emit()
    iw.CustomButton.click()
    iw.ImpDataType.setCurrentIndex(iw.ImpDataType.findData("f4"))
    for name, val in (("DNPxX", DET_X), ("DNPxY", DET_Y), ("DNFrX", SCAN_X), ("DNFrY", SCAN_Y)):
        getattr(iw, name).setValue(val)
    qapp.processEvents()
    assert "kept on the GPU" in iw.ImpNotes.toPlainText()
    fake_cuda.mem_get_info = lambda i=0: (1024, 8 * GB)            # card nearly full
    iw.DNFrY.setValue(SCAN_Y - 1)
    qapp.processEvents()
    assert "run on the CPU" in iw.ImpNotes.toPlainText()
    assert iw.ImpGPU.currentData() == 1, "the GPU choice must stay; the compute code falls back by itself"


def test_no_gpu(monkeypatch, app):
    """Without CUDA the list says so and means 'CPU' (it used to carry device 0)."""
    import callbacks.startup as startup
    if startup.torch.cuda.device_count():
        pytest.skip("a GPU is present")
    assert _items(app) == [("No GPU found.", None)]
