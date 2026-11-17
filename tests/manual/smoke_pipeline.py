"""Headless end-to-end smoke run.

Writes a synthetic dataset to disk, imports it through the real Import
window, then cycles every detector
mode and real-space ROI shape, printing ok/FAIL per step.  Exit code is 1 if
any step failed.

Not collected by pytest.  Run from the repo root after ``pip install -e .``:

    python tests/manual/smoke_pipeline.py

Set SMOKE_DUMP=<file.npz> to save every image after every step; comparing the
dumps from two versions of the code shows exactly which outputs a change moved.
"""
import os
import sys
import tempfile
import time
import traceback

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import numpy as np  # noqa: E402
from PyQt5.QtWidgets import QApplication, QMessageBox  # noqa: E402

qapp = QApplication(sys.argv)
# never block on a modal dialog
QMessageBox.exec_ = lambda self: QMessageBox.Ok
QMessageBox.exec = lambda self: QMessageBox.Ok

errors = []


def _hook(t, v, tb):
    errors.append("".join(traceback.format_exception(t, v, tb)[-3:]))


sys.excepthook = _hook

from callbacks.guiClass import MainWindow  # noqa: E402
from callbacks.appClass import D  # noqa: E402
from callbacks.import_io import importSelectFile  # noqa: E402
from callbacks.window_manager import showAllWindows, hideAllWindows  # noqa: E402
import callbacks.utils as _utils  # noqa: E402

_utils.notifDLG = lambda *a, **k: ''

NFX, NFY, NPX, NPY = 6, 4, 24, 16      # deliberately non-square


snapshots = {}
_window = []


def _step(name, fn):
    n = len(errors)
    try:
        fn()
    except Exception:
        errors.append(traceback.format_exc(limit=-3))
    qapp.processEvents()
    # keep every image after every step so two runs can be compared (SMOKE_DUMP)
    for w in _window:
        for i in w.Fig:
            im = getattr(w.Fig[i], "Image", None)
            if im is not None:
                snapshots[f"{len(snapshots):04d}|{name}|{i}"] = np.array(im, dtype=float)
    print(("FAIL " if len(errors) > n else "ok   ") + name)
    for e in errors[n:]:
        print("     " + e.strip().replace("\n", "\n     "))


def _dataset():
    """A disc that drifts with probe position, so CoM has a known gradient."""
    yy, xx = np.mgrid[0:NPY, 0:NPX]
    data = np.zeros((NFY * NFX, NPY * NPX), np.float32)
    for ry in range(NFY):
        for rx in range(NFX):
            data[ry * NFX + rx] = (np.hypot(xx - (14 + 0.3 * rx), yy - (6 + 0.3 * ry)) < 4).ravel()
    return data


def _import_from_file(w, data):
    """Drive the real Import window: pick a file, set its geometry, press Import."""
    path = os.path.join(tempfile.mkdtemp(), f"smoke_x{NFX}_y{NFY}.raw")
    data.astype("<f4").tofile(path)
    iw = w.ImportWindow
    w.ShowImportWdw.trigger()
    iw.ImpFilePath.setText(path)
    importSelectFile(w)
    iw.CustomButton.click()             # plain binary, geometry entered by hand
    qapp.processEvents()
    iw.ImpDataType.setCurrentIndex(iw.ImpDataType.findData("f4"))
    iw.DataOffset.setValue(0)
    iw.FrHead.setValue(0)
    iw.FrFoot.setValue(0)
    for name, val in (("DNPxX", NPX), ("DNPxY", NPY), ("DNFrX", NFX), ("DNFrY", NFY)):
        getattr(iw, name).setValue(val)
    qapp.processEvents()
    iw.ImportDataButton.click()
    deadline = time.time() + 20
    while time.time() < deadline and not (w.Data is not None and w.Fig.Dfrn.Image is not None and w.Fig.Dfrn.Image.any()):
        qapp.processEvents()
        time.sleep(0.02)
    assert w.Data is not None, "import thread never delivered data"
    assert w.Data.shape == data.shape, f"imported shape {w.Data.shape}, expected {data.shape}"
    assert np.array_equal(np.asarray(w.Data), data), "imported data differs from file contents"


def _check_images(w, ids):
    for i in ids:
        im = w.Fig[i].Image
        space = (NFY, NFX) if i in w.G.RealID else (NPY, NPX)
        assert im is not None, f"Fig.{i}.Image is None"
        assert im.shape == space, f"Fig.{i}.Image has shape {im.shape}, expected {space}"
        assert np.isfinite(im).all(), f"Fig.{i}.Image contains NaN/Inf"


def _set_mode(w, mode):
    w.DetrMode.setCurrentIndex(w.DetrMode.findData(mode))
    qapp.processEvents()
    assert w.DetrMode.currentData() == mode
    _check_images(w, ["Dfrn", "Real"])


def _check_zero_based_defaults(w):
    assert np.allclose(w.P.DfCtr, [(NPX - 1) / 2, (NPY - 1) / 2]), f"DfCtr = {w.P.DfCtr}"
    assert np.allclose(w.P.RsCtr, [(NFX - 1) / 2, (NFY - 1) / 2]), f"RsCtr = {w.P.RsCtr}"
    assert w.TBX.maximum() == NPX - 1 and w.TBY.maximum() == NPY - 1
    w.TBX.setValue(0)
    w.TBY.setValue(0)
    qapp.processEvents()
    assert np.allclose(w.B0, [0, 0]), f"beam centre cannot reach pixel (0, 0): B0 = {w.B0}"


def _check_auto_align(w):
    assert w.A.tb is not None, "no transmitted-beam annotation was drawn"
    err = np.abs(np.asarray(w.B0, float) - [14.75, 6.45]).max()
    assert err < 1.0 and abs(w.TBR.value() - 4) < 1.5, f"B0 = {w.B0}, TBR = {w.TBR.value():.2f}"


def _check_annular(w):
    """The BF/ADF image must equal the plain masked sum over the selected rings."""
    for ri, ro in ((0, int(w.AnnRi.maximum())), (0, 6), (4, 12)):
        w.AnnRi.setValue((ri, ro))
        qapp.processEvents()
        ri, ro = w.AnnRi.value()
        _check_images(w, ["Real", "DfrnMask"])
        yy, xx = np.mgrid[0:NPY, 0:NPX]
        ring = np.int32(np.hypot(xx - w.B0[0], yy - w.B0[1]) / w.D.annWidth)
        mask = (ring >= ri) & (ring <= ro)
        expected = w.Data[:, mask.ravel()].sum(axis=1).reshape(NFY, NFX)
        assert np.allclose(w.Fig.Real.Image, expected, rtol=1e-5), f"annular image wrong for rings {ri}-{ro}"
        assert np.array_equal(w.Fig.DfrnMask.Image.astype(bool), mask), f"displayed mask wrong for rings {ri}-{ro}"


def _check_com(w):
    """The disc drifts +0.3 px in x per rx step and +0.3 px in y per ry step."""
    _check_images(w, ["CoMX", "CoMY", "CoMMag", "CoMPh", "iCoM", "dCoM"])
    gx = np.diff(w.Fig.CoMX.Image, axis=1).mean()
    gy = np.diff(w.Fig.CoMY.Image, axis=0).mean()
    cross_x = np.abs(np.diff(w.Fig.CoMX.Image, axis=0)).mean()
    cross_y = np.abs(np.diff(w.Fig.CoMY.Image, axis=1)).mean()
    print(f"     dCoMX/drx = {gx:.3f}, dCoMY/dry = {gy:.3f} (expected ~0.3); cross terms {cross_x:.3f}, {cross_y:.3f}")
    assert abs(gx - 0.3) < 0.1 and abs(gy - 0.3) < 0.1, "CoM does not follow the disc"
    assert cross_x < 0.1 and cross_y < 0.1, "CoM X/Y are mixed"


def _changes(w, ids, action):
    """Run *action* and require every image in *ids* to change."""
    before = {i: np.array(w.Fig[i].Image, dtype=float) for i in ids}
    action()
    qapp.processEvents()
    same = [i for i in ids if np.array_equal(before[i], np.asarray(w.Fig[i].Image, dtype=float))]
    assert not same, f"no effect on {same}"


def _check_scan_direction(w):
    assert w.ScanDirUnlock.isEnabled(), "scan-direction unlock button is not clickable in CoM mode"
    assert not w.ScanDirYFlip.isEnabled(), "Y flip should be locked until unlocked"
    w.ScanDirUnlock.click()
    qapp.processEvents()
    assert w.ScanDirUnlock.isChecked() and w.ScanDirYFlip.isEnabled() and w.ScanDir.isEnabled()
    x0, y0 = w.Fig.CoMX.Image.copy(), w.Fig.CoMY.Image.copy()
    _changes(w, ["CoMX", "CoMY"], lambda: w.ScanDir.setValue(90))
    # rotating the scan direction by 90 degrees maps (x, y) -> (-y, x)
    assert np.allclose(w.Fig.CoMX.Image, -y0, atol=1e-5) and np.allclose(w.Fig.CoMY.Image, x0, atol=1e-5)
    w.ScanDir.setValue(0)
    _changes(w, ["CoMY"], lambda: w.ScanDirYFlip.click())
    assert np.allclose(w.Fig.CoMY.Image, -y0, atol=1e-5) and np.allclose(w.Fig.CoMX.Image, x0, atol=1e-5)
    w.ScanDirYFlip.click()
    qapp.processEvents()
    assert np.allclose(w.Fig.CoMY.Image, y0, atol=1e-5)


def _check_scan_rotation(w):
    """Scan rotation and Y flip must act on the DPC field exactly as on CoM."""
    if not w.ScanDirUnlock.isChecked():     # entering a mode re-locks the scan direction
        w.ScanDirUnlock.click()
        qapp.processEvents()
    assert w.ScanDirUnlock.isChecked() and w.ScanDir.isEnabled() and w.ScanDirYFlip.isEnabled()
    x0, y0 = w.Fig.CoMX.Image.copy(), w.Fig.CoMY.Image.copy()
    _changes(w, ["CoMX", "CoMY"], lambda: w.ScanDir.setValue(90))
    assert np.allclose(w.Fig.CoMX.Image, -y0, atol=1e-5) and np.allclose(w.Fig.CoMY.Image, x0, atol=1e-5)
    w.ScanDir.setValue(0)
    _changes(w, ["CoMY"], lambda: w.ScanDirYFlip.click())
    assert np.allclose(w.Fig.CoMY.Image, -y0, atol=1e-5) and np.allclose(w.Fig.CoMX.Image, x0, atol=1e-5)
    w.ScanDirYFlip.click()
    qapp.processEvents()
    assert np.allclose(w.Fig.CoMX.Image, x0, atol=1e-5) and np.allclose(w.Fig.CoMY.Image, y0, atol=1e-5)


def _check_dpc_tracks_com(w):
    """A finely divided detector must see the same drift of the disc as CoM does."""
    w.NSeg.setValue(int(w.NSeg.maximum()))
    w.NRung.setValue(int(w.NRung.maximum()))
    qapp.processEvents()
    gx = np.diff(w.Fig.CoMX.Image, axis=1).mean()
    gy = np.diff(w.Fig.CoMY.Image, axis=0).mean()
    print(f"     {w.NSeg.value()} segments x {w.NRung.value()} rungs: dDPCX/drx = {gx:.3f}, dDPCY/dry = {gy:.3f} (CoM gives ~0.3)")
    assert gx > 0.15 and gy > 0.15, "DPC does not follow the disc in the right direction"


def _move_aperture(w, dx, dy):
    w.P.VrApXY = np.array([w.B0[0] + dx, w.B0[1] + dy])
    w.UpdateImages.trigger()


def _check_virtual_sum(w):
    mask = w.Fig.DfrnMask.Image.astype(bool)
    expected = w.Data[:, mask.ravel()].sum(axis=1).reshape(NFY, NFX)
    assert np.allclose(w.Fig.Real.Image, expected), "virtual image is not the masked sum"


def _check_virtual_aperture(w):
    _check_images(w, ["Real", "DfrnMask"])
    _check_virtual_sum(w)
    mask = w.Fig.DfrnMask.Image.astype(bool)
    yy, xx = np.nonzero(mask)
    centre = np.array([xx.mean(), yy.mean()])
    assert np.abs(centre - np.asarray(w.P.VrApXY, float)).max() < 1.0, \
        f"aperture mask centred at {centre}, annotation at {w.P.VrApXY}"


def _check_point_roi(w):
    w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("point"))
    for fx, fy in ((4, 2), (0, 0), (NFX - 1, NFY - 1)):      # 0-based, including both corners
        w.FrameX.setValue(fx)
        w.FrameY.setValue(fy)
        qapp.processEvents()
        assert (w.FrameX.value(), w.FrameY.value()) == (fx, fy), "spinbox range rejects a valid 0-based frame"
        expected = w.Data[fy * NFX + fx].reshape(NPY, NPX)
        assert np.allclose(w.Fig.Dfrn.Image, expected), f"point ROI at ({fx}, {fy}) shows a different probe position"
        marker = np.asarray(w.A.RealROI["Real"].position, float).ravel()
        assert np.allclose(marker, [fx, fy]), f"marker drawn at {marker}, spinboxes say ({fx}, {fy})"
    assert w.FrameX.maximum() == NFX - 1 and w.FrameY.maximum() == NFY - 1


def main():
    w = MainWindow()
    _window.append(w)
    data = _dataset()

    _step("import from file", lambda: _import_from_file(w, data))
    print(f"     after import: B0 = {w.B0}, TBR = {w.TBR.value():.2f} (disc mean centre ~(14.75, 6.45), r = 4)")
    _step("show all image windows", lambda: (showAllWindows(w), w.UpdateImages.trigger()))

    _step("mode AlignMod", lambda: _set_mode(w, "AlignMod"))
    _step("auto-align found the disc", lambda: _check_auto_align(w))
    _step("0-based centres and limits", lambda: _check_zero_based_defaults(w))
    _step("set beam centre/radius", lambda: (w.TBX.setValue(14.75), w.TBY.setValue(6.45), w.TBR.setValue(4.0)))

    _step("mode AnnMod", lambda: _set_mode(w, "AnnMod"))
    _step("annular image equals masked sum", lambda: _check_annular(w))
    _step("annular radii full range", lambda: w.AnnRi.setValue((0, int(w.AnnRi.maximum()))))
    _step("mode CoMMod", lambda: (_set_mode(w, "CoMMod"), _check_com(w)))
    _step("CoM scan direction controls", lambda: _check_scan_direction(w))
    _step("mode DPCMod recomputes", lambda: _changes(w, ["CoMX", "CoMY"], lambda: _set_mode(w, "DPCMod")))
    _step("DPC images", lambda: _check_images(w, ["CoMX", "CoMY", "CoMMag", "CoMPh", "iCoM", "dCoM"]))
    _step("DPC segment count recomputes", lambda: _changes(w, ["CoMX", "CoMY"], lambda: w.NSeg.setValue(6)))
    _step("DPC rung count recomputes", lambda: _changes(w, ["CoMX", "CoMY"], lambda: w.NRung.setValue(3)))
    _step("DPC scan direction", lambda: _check_scan_rotation(w))
    _step("DPC follows the disc", lambda: _check_dpc_tracks_com(w))
    for nseg, nrung, rot in ((8, 2, 30), (4, 3, 45), (6, 1, 200), (4, 1, 0)):
        _step(f"DPC {nseg} segments, {nrung} rungs, rotation {rot}",
              lambda a=nseg, b=nrung, c=rot: (w.NSeg.setValue(a), w.NRung.setValue(b), w.DetRot.setValue(c),
                                              _check_images(w, ["CoMX", "CoMY", "iCoM", "dCoM"])))
    _step("DPC annulus 2-10", lambda: w.AnnRi.setValue((2, 10)))
    _step("mode VrApMod", lambda: (_set_mode(w, "VrApMod"), _check_virtual_aperture(w)))
    _step("virtual aperture radius", lambda: _changes(w, ["Real", "DfrnMask"], lambda: w.VrApR.setValue(2)))
    _step("virtual aperture off-centre", lambda: _changes(w, ["Real", "DfrnMask"], lambda: _move_aperture(w, 5, 1)))
    for k in range(1, w.VrApSymm.count()):
        _step(f"virtual aperture {w.VrApSymm.itemData(k)}-fold symmetry",
              lambda k=k: _changes(w, ["Real", "DfrnMask"], lambda: w.VrApSymm.setCurrentIndex(k)))
    _step("virtual aperture mirror", lambda: _changes(w, ["Real", "DfrnMask"], lambda: (w.VrApMirror.click(), w.VrApMirrRot.setValue(40))))
    _step("virtual aperture invert", lambda: _changes(w, ["Real", "DfrnMask"], lambda: w.VrApInvert.click()))
    _step("virtual aperture mask sum", lambda: _check_virtual_sum(w))
    _step("virtual aperture reset", lambda: (w.VrApInvert.click(), w.VrApMirror.click(), w.VrApSymm.setCurrentIndex(0)))

    _step("ROI point", lambda: _check_point_roi(w))
    for shape in ["rectangle", "ellipse", "full"]:
        _step("ROI " + shape, lambda s=shape: (w.RealROIShape.setCurrentIndex(w.RealROIShape.findData(s)),
                                               _check_images(w, ["Dfrn", "RealMask"])))
    _step("ROI invert", lambda: (w.RealROIInvert.setChecked(True), w.RealROIInvert.setChecked(False)))

    sw = w.SettingsWindow
    for i in [sw.DispImage.itemData(k) for k in range(sw.DispImage.count())]:
        _step("display settings on " + str(i), lambda i=i: _display(w, i))
    _step("update images", lambda: w.UpdateImages.trigger())
    _step("hide all image windows", lambda: hideAllWindows(w))
    _step("re-import same file", lambda: _import_from_file(w, data))
    if os.environ.get("SMOKE_DUMP"):
        np.savez_compressed(os.environ["SMOKE_DUMP"], **snapshots)
    return 1 if errors else 0


def _display(w, i):
    sw = w.SettingsWindow
    sw.DispImage.setCurrentIndex(sw.DispImage.findData(i))
    qapp.processEvents()
    for name in ("HistLog", "DispInvert"):
        box = getattr(sw, name, None)
        if box is not None:
            box.click()
            box.click()
    qapp.processEvents()


if __name__ == "__main__":
    sys.exit(main())
