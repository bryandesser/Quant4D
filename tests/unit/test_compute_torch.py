"""
The torch code path of callbacks.compute.backend.

Runs wherever torch is installed.  Without a GPU it uses torch's CPU device,
which exercises exactly the same code (resident dataset, fallbacks to NumPy);
with CUDA available every test is repeated on the GPU.
"""
import gc

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from callbacks import compute                    # noqa: E402
from callbacks.compute import backend            # noqa: E402

NFY, NFX, NPY, NPX = 6, 7, 16, 20
CENTER = (9.3, 6.6)
DEVICES = ["cpu"] + (["cuda:0"] if torch.cuda.is_available() else [])


@pytest.fixture(params=DEVICES)
def device(request):
    compute.release_device_data()
    yield request.param
    compute.release_device_data()


@pytest.fixture()
def data():
    return np.random.default_rng(3).random((NFY * NFX, NPY * NPX), dtype=np.float32)


@pytest.fixture()
def weights():
    return np.random.default_rng(4).random((NPY * NPX, 3)).astype(np.float32)


def _one_frame_per_chunk(monkeypatch):
    monkeypatch.setattr(backend, "CHUNK_BYTES", 1)


def _no_room_on_device(monkeypatch):
    monkeypatch.setattr(backend, "_free_bytes", lambda dev: 0)


# ------------------------------------------------------------------ resident
def test_first_call_uploads_and_later_calls_reuse(data, weights, device):
    assert compute.device_data_info() is None
    np.testing.assert_allclose(compute.project(data, weights, device), data @ weights, rtol=1e-4)
    info = compute.device_data_info()
    assert info["shape"] == data.shape and info["bytes"] == data.size * 4
    assert info["device"].startswith(device.split(":")[0])

    held = backend._resident.tensor
    compute.project(data, weights[:, 0], device)
    assert backend._resident.tensor is held, "the dataset was uploaded again"


def test_upload_in_many_chunks_is_exact(data, weights, device, monkeypatch):
    _one_frame_per_chunk(monkeypatch)
    compute.project(data, weights, device)
    np.testing.assert_array_equal(backend._resident.tensor.cpu().numpy(), data)


def test_new_dataset_replaces_the_resident_one(data, weights, device):
    compute.project(data, weights, device)
    other = data[::-1].copy()
    np.testing.assert_allclose(compute.project(other, weights, device), other @ weights, rtol=1e-4)
    np.testing.assert_array_equal(backend._resident.tensor.cpu().numpy(), other)


def test_in_place_edit_needs_release(data, weights, device):
    compute.project(data, weights, device)
    data *= 2.0
    stale = compute.project(data, weights, device)
    assert not np.allclose(stale, data @ weights, rtol=1e-3), "expected the stale copy to be used"
    compute.release_device_data()
    assert compute.device_data_info() is None
    np.testing.assert_allclose(compute.project(data, weights, device), data @ weights, rtol=1e-4)


def test_release_is_safe_when_nothing_is_held():
    compute.release_device_data()
    compute.release_device_data()
    assert compute.device_data_info() is None


def test_dead_array_is_not_mistaken_for_a_new_one(weights, device):
    a = np.ones((NFY * NFX, NPY * NPX), np.float32)
    compute.project(a, weights, device)
    del a
    gc.collect()
    b = np.full((NFY * NFX, NPY * NPX), 3.0, np.float32)      # may reuse the same id()
    np.testing.assert_allclose(compute.project(b, weights, device), b @ weights, rtol=1e-4)


# ------------------------------------------------- does not fit on the device
def test_dataset_too_big_for_the_device_uses_numpy(data, weights, device, monkeypatch):
    _no_room_on_device(monkeypatch)
    uploads = []
    monkeypatch.setattr(torch, "empty", lambda *a, **k: uploads.append(a) or (_ for _ in ()).throw(AssertionError("upload attempted")))
    np.testing.assert_allclose(compute.project(data, weights, device), data @ weights, rtol=1e-5)
    np.testing.assert_allclose(compute.project(data, weights[:, 1], device), data @ weights[:, 1], rtol=1e-5)
    assert not uploads and compute.device_data_info() is None


def test_integer_data_resident_and_not(device, weights, monkeypatch):
    ints = np.random.default_rng(5).integers(0, 4000, (NFY * NFX, NPY * NPX)).astype(np.uint16)
    expected = ints.astype(np.float64) @ weights
    np.testing.assert_allclose(compute.project(ints, weights, device), expected, rtol=1e-4)
    assert compute.device_data_info() is not None
    compute.release_device_data()
    _no_room_on_device(monkeypatch)
    _one_frame_per_chunk(monkeypatch)
    np.testing.assert_allclose(compute.project(ints, weights, device), expected, rtol=1e-4)
    assert compute.device_data_info() is None


# ------------------------------------------------------------ out of memory
def test_out_of_memory_on_upload_falls_back_to_numpy(data, weights, device, monkeypatch):
    real_empty = torch.empty
    attempts = []

    def no_room(*args, **kwargs):
        attempts.append(1)
        raise RuntimeError("CUDA out of memory. Tried to allocate ...")

    monkeypatch.setattr(torch, "empty", no_room)
    np.testing.assert_allclose(compute.project(data, weights, device), data @ weights, rtol=1e-5)
    assert compute.device_data_info() is None
    # remembered as too big: no second upload attempt for the same dataset
    np.testing.assert_allclose(compute.project(data, weights, device), data @ weights, rtol=1e-5)
    assert len(attempts) == 1
    # a different dataset is tried afresh
    monkeypatch.setattr(torch, "empty", real_empty)
    other = data.copy()
    compute.project(other, weights, device)
    assert compute.device_data_info() is not None


def test_out_of_memory_during_the_product_falls_back_to_numpy(data, weights, device, monkeypatch):
    compute.project(data, weights, device)
    assert compute.device_data_info() is not None

    def oom(*args, **kwargs):
        raise RuntimeError("CUDA out of memory.")

    monkeypatch.setattr(backend, "_project_torch", oom)
    np.testing.assert_allclose(compute.project(data, weights, device), data @ weights, rtol=1e-5)
    assert compute.device_data_info() is None, "the resident copy should have been released"


def test_other_runtime_errors_are_not_swallowed(data, weights, device, monkeypatch):
    def broken(*args, **kwargs):
        raise RuntimeError("shape mismatch")

    monkeypatch.setattr(backend, "_project_torch", broken)
    with pytest.raises(RuntimeError, match="shape mismatch"):
        compute.project(data, weights, device)


# ------------------------------------------------- every detector, on device
@pytest.mark.parametrize("fits", [True, False])
def test_detectors_match_numpy(data, device, fits, monkeypatch):
    if not fits:
        _no_room_on_device(monkeypatch)
    k = compute.radial_index((NPY, NPX), CENTER, 0.5)
    mask = compute.annular_mask(k, 2, 14)

    np.testing.assert_allclose(compute.ring_integrals(data, k, device), compute.ring_integrals(data, k), rtol=1e-4, atol=1e-5)
    np.testing.assert_allclose(compute.masked_sum(data, mask, device), compute.masked_sum(data, mask), rtol=1e-4)

    got, ref = compute.center_of_mass(data, mask, CENTER, device), compute.center_of_mass(data, mask, CENTER)
    np.testing.assert_allclose(got[0], ref[0], rtol=1e-3, atol=1e-4)
    np.testing.assert_allclose(got[1], ref[1], rtol=1e-3, atol=1e-4)

    w = compute.segment_weights(mask, CENTER, 1.0, 7.0, 6, 2, 25.0)
    got, ref = compute.segmented_dpc(data, w, device), compute.segmented_dpc(data, w)
    np.testing.assert_allclose(got[0], ref[0], rtol=1e-3, atol=1e-4)
    np.testing.assert_allclose(got[1], ref[1], rtol=1e-3, atol=1e-4)

    roi = np.zeros((NFY, NFX))
    roi[1:5, 0:6] = 1                               # large selection -> matrix-product path
    np.testing.assert_allclose(compute.roi_pattern(data, roi, device), compute.roi_pattern(data, roi), rtol=1e-4)
    weighted = np.linspace(0.1, 1.0, NFY * NFX)
    np.testing.assert_allclose(compute.roi_pattern(data, weighted, device), compute.roi_pattern(data, weighted), rtol=1e-4)
    assert (compute.device_data_info() is not None) == fits


def test_cuda_request_without_cuda_uses_numpy(data, weights, monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    assert compute.resolve_device("cuda:0") is None
    np.testing.assert_allclose(compute.project(data, weights, "cuda:0"), data @ weights, rtol=1e-5)


def test_upload_non_native_byte_order(device):
    """A byte-swapped memory map (lazy data after Swap Byte Order) uploads and projects correctly."""
    from callbacks import compute
    rng = np.random.default_rng(5)
    data = rng.random((6, 20), dtype=np.float32)
    swapped = data.byteswap().view(data.dtype.newbyteorder())     # same values, other byte order
    assert not swapped.dtype.isnative
    weights = rng.random(20).astype(np.float32)
    compute.release_device_data()
    assert np.allclose(compute.project(swapped, weights, device), data @ weights, rtol=1e-5)
    compute.release_device_data()
