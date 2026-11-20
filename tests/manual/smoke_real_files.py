"""Import real 4D-STEM files through the Import window and check what arrives.

Usage (from the repo root, after ``pip install -e .``)::

    python tests/manual/smoke_real_files.py "Diffraction SI.dm4" triangleNP_512x512x64x64.mrc

For each file the script selects the matching file type, checks the geometry
read from the header, previews three probe positions, then imports a reduced
version (scan sampled by 2, diffraction binned by 4 for large files) and
compares it with the same reduction computed straight from the file.  It then
runs every detector mode on the imported data.

Files are not part of the repository (see .gitignore).
"""
import os
import sys
import time
import traceback

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import numpy as np  # noqa: E402
from PyQt5.QtWidgets import QApplication, QMessageBox  # noqa: E402

qapp = QApplication(sys.argv)
QMessageBox.exec_ = lambda self: QMessageBox.Ok
QMessageBox.exec = lambda self: QMessageBox.Ok
errors = []
sys.excepthook = lambda t, v, tb: errors.append("".join(traceback.format_exception(t, v, tb)[-3:]))

from quant4d.callbacks.guiClass import MainWindow  # noqa: E402
from quant4d.callbacks.import_io import importSelectFile  # noqa: E402
from quant4d.callbacks.io.raw import open_frames  # noqa: E402
import quant4d.callbacks.utils as _utils  # noqa: E402

_utils.notifDLG = lambda *a, **k: ''

BUTTONS = {".dm3": "DM34Button", ".dm4": "DM34Button", ".mrc": "MRCButton", ".h5": "HDF5Button",
           ".hdf5": "HDF5Button", ".mib": "MedipixButton", ".raw": "EMPADButton"}   # .raw files are taken to be EMPAD
NAMES = ("DNPxX", "DNPxY", "DNFrX", "DNFrY", "DataOffset", "FrHead", "FrFoot")


def step(name, fn):
    n = len(errors)
    t = time.time()
    try:
        out = fn()
    except Exception:
        errors.append(traceback.format_exc(limit=-3))
        out = None
    qapp.processEvents()
    print(("FAIL " if len(errors) > n else "ok   ") + f"{name}  ({time.time() - t:.1f} s)")
    for e in errors[n:]:
        print("     " + e.strip().replace("\n", "\n     "))
    return out


def select(w, path):
    iw = w.ImportWindow
    w.ShowImportWdw.trigger()
    iw.ImpFilePath.setText(path)
    iw.ImpFilePath.editingFinished.emit()   # as if the path had been typed in; runs importSelectFile as a slot
    getattr(iw, BUTTONS[os.path.splitext(path)[1].lower()]).click()
    qapp.processEvents()
    geo = {n: getattr(iw, n).value() for n in NAMES}
    print(f"     {geo}, {iw.ImpDataType.currentData()}, byte order {iw.ImpByteOrder.currentData()}")
    assert iw.ImpDataType.currentData() not in (None, "unknown"), "data type not recognised"
    return geo


def disk(w, geo):
    iw = w.ImportWindow
    return open_frames(iw.ImpFilePath.text(), geo["DataOffset"], geo["DNFrX"] * geo["DNFrY"],
                       geo["DNPxX"] * geo["DNPxY"], iw.ImpDataType.currentData(),
                       geo["FrHead"], geo["FrFoot"], iw.ImpByteOrder.currentData())


def preview(w, geo):
    on_disk = disk(w, geo)
    for fx, fy in ((0, 0), (geo["DNFrX"] - 1, geo["DNFrY"] - 1), (geo["DNFrX"] // 2, geo["DNFrY"] // 3)):
        w.PvFrX.setValue(fx)
        w.PvFrY.setValue(fy)
        w.PreviewButton.click()
        qapp.processEvents()
        expected = np.asarray(on_disk[fy * geo["DNFrX"] + fx], float).reshape(geo["DNPxY"], geo["DNPxX"])
        assert np.array_equal(w.Fig.Preview.Image, expected), f"preview of ({fx}, {fy}) differs from the file"


def partial_import(w, geo, bin_px, sample_fr):
    iw = w.ImportWindow
    iw.ImpFrPart.setChecked(True)
    iw.ImpFrPart.clicked.emit(True)
    iw.IFrD.setValue(sample_fr)
    iw.ImpPxPart.setChecked(True)
    iw.ImpPxPart.clicked.emit(True)
    iw.IPxD.setValue(bin_px)
    qapp.processEvents()
    fx, fy = iw.INFrX.value(), iw.INFrY.value()
    px, py = iw.INPxX.value(), iw.INPxY.value()
    assert (fx, fy) == ((geo["DNFrX"] - 1) // sample_fr + 1, (geo["DNFrY"] - 1) // sample_fr + 1), (fx, fy)
    assert (px, py) == (geo["DNPxX"] // bin_px, geo["DNPxY"] // bin_px), (px, py)
    iw.ImportDataButton.click()
    deadline = time.time() + 600
    while time.time() < deadline and not (w.Data is not None and w.Data.shape == (fx * fy, px * py)
                                          and w.Fig.Dfrn.Image is not None):
        qapp.processEvents()
        time.sleep(0.05)
    assert w.Data is not None and w.Data.shape == (fx * fy, px * py), \
        f"imported {None if w.Data is None else w.Data.shape}, expected {(fx * fy, px * py)}"

    # compare a few frames with the same reduction done directly on the file
    on_disk = disk(w, geo)
    rng = np.random.default_rng(0)
    for k in rng.choice(fx * fy, size=min(20, fx * fy), replace=False):
        ry, rx = divmod(int(k), fx)
        raw = np.asarray(on_disk[ry * sample_fr * geo["DNFrX"] + rx * sample_fr], np.float64)
        raw = raw.reshape(geo["DNPxY"], geo["DNPxX"])[:py * bin_px, :px * bin_px]
        ref = raw.reshape(py, bin_px, px, bin_px).sum(axis=(1, 3))
        # float32 sums: compare to the frame's scale (EMPAD data have both signs, so some sums are near 0)
        err = np.abs(w.Data[k].reshape(py, px) - ref).max() / max(np.abs(ref).max(), 1e-12)
        assert err < 1e-6, f"imported frame {k} differs by {err:.1e} of its range"
    print(f"     imported {fy} x {fx} scan of {py} x {px} patterns, {w.Data.dtype}, "
          f"{w.Data.nbytes / 1024 ** 2:.0f} MiB; B0 = {w.B0}, TBR = {w.TBR.value():.1f}")


def modes(w):
    for m in ("AlignMod", "AnnMod", "CoMMod", "DPCMod", "VrApMod"):
        w.DetrMode.setCurrentIndex(w.DetrMode.findData(m))
        qapp.processEvents()
        for i in ("Dfrn", "Real") + (("CoMX", "CoMY", "iCoM") if m in ("CoMMod", "DPCMod") else ()):
            im = w.Fig[i].Image
            assert im is not None and np.isfinite(im).all(), f"{m}: Fig.{i}.Image missing or not finite"


def main(paths):
    w = MainWindow()
    for path in paths:
        path = os.path.abspath(path)
        size = os.path.getsize(path)
        print(f"\n== {os.path.basename(path)} ({size / 1024 ** 3:.2f} GiB)")
        geo = step("read header", lambda: select(w, path))
        if geo is None:
            continue
        step("preview three probe positions", lambda: preview(w, geo))
        big = size > 512 * 1024 ** 2
        step(f"partial import (scan every {2}, diffraction binned {4 if big else 1})",
             lambda: partial_import(w, geo, 4 if big else 1, 2))
        step("all detector modes", lambda: modes(w))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
