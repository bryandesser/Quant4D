"""Time the detector calculations on the CPU and on a GPU.

Run from the repo root after ``pip install -e .``:

    python tests/manual/bench_gpu.py                 # 96x96 scan of 128x128 patterns on cuda:0
    python tests/manual/bench_gpu.py --scan 256 --det 128 --device cuda:0
    python tests/manual/bench_gpu.py --dtype uint16  # integer data, as from a lazily loaded file

"GPU first" includes uploading the dataset; "GPU again" is every later call,
which is what moving a slider costs.  The last column checks the GPU result
against the CPU one.
"""
import argparse
import time

import numpy as np

from pyquant4d.callbacks import compute


def _time(fn, repeats=3):
    best, out = float("inf"), None
    for _ in range(repeats):
        start = time.perf_counter()
        out = fn()
        best = min(best, time.perf_counter() - start)
    return best, out


def _sync(device):
    try:
        import torch
        if torch.cuda.is_available() and str(device).startswith("cuda"):
            torch.cuda.synchronize()
    except ImportError:
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scan", type=int, default=96, help="scan size in frames per side (default 96)")
    ap.add_argument("--det", type=int, default=128, help="detector size in pixels per side (default 128)")
    ap.add_argument("--device", default="cuda:0", help='torch device (default "cuda:0")')
    ap.add_argument("--dtype", default="float32", help="dataset dtype (default float32)")
    args = ap.parse_args()

    n_frames, n_pixels = args.scan ** 2, args.det ** 2
    rng = np.random.default_rng(0)
    data = rng.random((n_frames, n_pixels), dtype=np.float32)
    if args.dtype != "float32":
        data = (data * 4000).astype(args.dtype)
    print(f"dataset: {args.scan}x{args.scan} scan of {args.det}x{args.det} patterns, {args.dtype}, "
          f"{data.nbytes / 1024 ** 3:.2f} GiB")

    dev = compute.resolve_device(args.device)
    if dev is None:
        print(f'device "{args.device}" is not available (torch missing or no CUDA): CPU timings only')
    else:
        print(f"device:  {dev}")

    center = (args.det / 2 - 3.7, args.det / 2 + 2.1)
    k = compute.radial_index((args.det, args.det), center, 0.5)
    mask = compute.annular_mask(k, 10, int(args.det * 0.6))
    seg = compute.segment_weights(mask, center, 5.0, args.det * 0.3, 4, 2, 15.0)
    aperture = compute.circle_mask((args.det, args.det), (center[0] + 12, center[1] - 7), 6)
    roi = np.ones((args.scan, args.scan))

    jobs = [
        ("ring integrals (beam moved)", lambda d: compute.ring_integrals(data, k, d)),
        ("centre of mass", lambda d: np.stack(compute.center_of_mass(data, mask, center, d))),
        ("segmented DPC", lambda d: np.stack(compute.segmented_dpc(data, seg, d))),
        ("virtual aperture", lambda d: compute.masked_sum(data, aperture, d)),
        ("full-ROI pattern", lambda d: compute.roi_pattern(data, roi, d)),
    ]

    print(f"\n{'calculation':30s} {'CPU':>9s} {'GPU first':>10s} {'GPU again':>10s} {'speed-up':>9s} {'max rel diff':>13s}")
    compute.release_device_data()
    first = True
    for name, job in jobs:
        t_cpu, ref = _time(lambda: job(None))
        if dev is None:
            print(f"{name:30s} {t_cpu * 1e3:8.1f}ms")
            continue
        start = time.perf_counter()
        job(args.device)
        _sync(args.device)
        t_first = time.perf_counter() - start

        def again():
            out = job(args.device)
            _sync(args.device)
            return out
        t_again, got = _time(again)
        scale = max(float(np.abs(ref).max()), 1e-12)
        diff = float(np.abs(np.asarray(got, dtype=np.float64) - ref).max()) / scale
        note = " (includes upload)" if first else ""
        first = False
        print(f"{name:30s} {t_cpu * 1e3:8.1f}ms {t_first * 1e3:9.1f}ms {t_again * 1e3:9.1f}ms {t_cpu / t_again:8.1f}x {diff:13.1e}{note}")

    info = compute.device_data_info()
    if dev is not None:
        if info is None:
            print("\nThe dataset did not fit in the device's free memory, so every calculation ran on the CPU "
                  "(the GPU columns are CPU times).")
        else:
            print(f"\nDataset held on {info['device']}: {info['bytes'] / 1024 ** 3:.2f} GiB")
    compute.release_device_data()


if __name__ == "__main__":
    main()
