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
    iw.ImpFilePath.editingFinished.emit()   # as if the path had been typed in; runs importSelectFile as a slot
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


def _wait_for_import(w, shape):
    deadline = time.time() + 20
    while time.time() < deadline and not (w.Data is not None and w.Data.shape == shape
                                          and w.Fig.Dfrn.Image is not None and w.Fig.Dfrn.Image.any()):
        qapp.processEvents()
        time.sleep(0.02)
    assert w.Data is not None and w.Data.shape == shape, \
        f"import gave {None if w.Data is None else w.Data.shape}, expected {shape}"


def _save_images(w, folder):
    """Save every image as TIFF, plain PNG and annotated PNG, with detector angles in the names."""
    from PIL import Image
    sw = w.SaveWindow
    sw.SaveDir.setText(folder)
    sw.SaveImgPrefix.setText("smoke_")
    sw.SaveImgList.selectAll()
    ids = [it.text() for it in sw.SaveImgList.selectedItems()]
    assert "Real" in ids and "Dfrn" in ids, f"image list is {ids}"
    sw.SavePrfxRi.setChecked(True)
    sw.SavePrfxRo.setChecked(True)
    sw.SaveTabGroup.setCurrentWidget(sw.SaveImgTab)
    assert sw.SaveExport.text() == "Save Images"
    for tif, png, annot in ((True, False, False), (False, True, False), (False, True, True)):
        sub = os.path.join(folder, f"t{int(tif)}p{int(png)}a{int(annot)}")
        os.mkdir(sub)
        sw.SaveDir.setText(sub)
        sw.SaveImgTIF.setChecked(tif)
        sw.SaveImgPNG.setChecked(png)
        sw.SaveImgPNGAnnot.setChecked(annot)
        sw.SaveExport.click()
        qapp.processEvents()
        files = sorted(os.listdir(sub))
        assert files, "nothing was saved"
        real = [f for f in files if f.startswith("smoke_Real_") or f.startswith("smoke_Real.")]
        assert len(real) == 1, f"expected one Real image in {files}"
        assert "_ri" in real[0] and "_ro" in real[0], f"detector angles missing from {real[0]}"
        im = np.array(Image.open(os.path.join(sub, real[0])))
        if tif:
            assert im.dtype == np.float32 and np.allclose(im, w.Fig.Real.Image), "TIFF is not the raw Real image"
        elif not annot:
            assert im.shape == (NFY, NFX, 3), f"plain PNG has shape {im.shape}, expected one pixel per probe position"
        else:
            assert im.shape[0] > NFY and im.shape[2] in (3, 4), f"annotated PNG has shape {im.shape}"
    sw.SaveDir.setText(folder)


def _export(w, folder, fmt, partial, byte_order="l"):
    """Export through the Save window and return (path, expected 4-D array)."""
    sw = w.SaveWindow
    sw.SaveDir.setText(folder)
    sw.SaveTabGroup.setCurrentWidget(sw.ExportTab)
    assert sw.SaveExport.text() == "Export Dataset"
    sw.ExpFormat.setCurrentIndex(sw.ExpFormat.findData(fmt))
    sw.ExpByteOrder.setCurrentIndex(sw.ExpByteOrder.findData(byte_order))
    sw.ExpFilename.setText(f"smoke_{fmt}")
    sw.ExpDimSuff.setChecked(fmt == "raw")
    cube = np.asarray(w.Data).reshape(NFY, NFX, NPY, NPX)
    if partial:
        sw.ExpFrPart.setChecked(True)
        sw.ExpFrPart.clicked.emit(True)
        sw.EFrD.setValue(2)
        sw.EFrX1.setValue(1)
        sw.EFrY1.setValue(0)
        sw.ENFrX.setValue(99)                # clamped to what fits
        sw.ENFrY.setValue(99)
        assert (sw.ENFrX.value(), sw.ENFrY.value()) == ((NFX - 2) // 2 + 1, (NFY - 1) // 2 + 1)
        sw.ExpPxPart.setChecked(True)
        sw.ExpPxPart.clicked.emit(True)
        sw.EPxD.setValue(2)
        sw.EPxX1.setValue(3)
        sw.EPxY1.setValue(1)
        sw.ENPxX.setValue(99)
        sw.ENPxY.setValue(99)
        cx, cy = sw.ENPxX.value(), sw.ENPxY.value()
        assert (cx, cy) == ((NPX - 3) // 2, (NPY - 1) // 2)
        fx, fy = sw.ENFrX.value(), sw.ENFrY.value()
        sub = cube[0:(fy - 1) * 2 + 1:2, 1:1 + (fx - 1) * 2 + 1:2, 1:1 + cy * 2, 3:3 + cx * 2]
        expected = sub.reshape(fy, fx, cy, 2, cx, 2).sum(axis=(3, 5))
    else:
        sw.ExpFrPart.setChecked(False)
        sw.ExpPxPart.setChecked(False)
        sw.ExpPxPart.clicked.emit(False)
        expected = cube.copy()
    notes = sw.ExpNotes.toPlainText()
    assert f"{expected.shape}" in notes, f"export summary does not show {expected.shape}:\n{notes}"
    sw.SaveExport.click()
    qapp.processEvents()
    path = notes.splitlines()[0].replace("File: ", "")
    assert os.path.isfile(path), f"{path} was not written"
    return path, expected


def _check_export_hdf5(w, folder):
    import h5py
    path, expected = _export(w, folder, "h5", partial=False)
    with h5py.File(path) as f:
        assert np.array_equal(f["data"][()], expected), "HDF5 data differs"
        meta = dict(f["metadata"].attrs)
    assert np.allclose(meta["beam_center_xy"], w.B0), meta
    return path, expected


def _check_export_raw_partial(w, folder):
    path, expected = _export(w, folder, "raw", partial=True, byte_order="b")
    ny, nx, py, px = expected.shape
    assert path.endswith(f"_{px}x{py}x{nx}x{ny}.raw"), path
    got = np.fromfile(path, dtype=">f4").reshape(expected.shape)
    assert np.allclose(got, expected, rtol=1e-6), "raw data differs"
    return path, expected


def _reimport(w, path, expected, hdf5, byte_order="l"):
    """Open an exported file through the Import window, letting it detect the geometry."""
    iw = w.ImportWindow
    w.ShowImportWdw.trigger()
    iw.ImpFilePath.setText(path)
    iw.ImpFilePath.editingFinished.emit()   # as if the path had been typed in; runs importSelectFile as a slot
    (iw.HDF5Button if hdf5 else iw.CustomButton).click()
    qapp.processEvents()
    ny, nx, py, px = expected.shape
    got_dims = tuple(getattr(iw, n).value() for n in ("DNPxX", "DNPxY", "DNFrX", "DNFrY"))
    assert got_dims == (px, py, nx, ny), f"importer read dimensions {got_dims} from {os.path.basename(path)}"
    iw.ImpDataType.setCurrentIndex(iw.ImpDataType.findData("f4"))
    if not hdf5:
        iw.ImpByteOrder.setCurrentIndex(iw.ImpByteOrder.findData(byte_order))
    qapp.processEvents()
    iw.ImportDataButton.click()
    _wait_for_import(w, (ny * nx, py * px))
    assert np.allclose(np.asarray(w.Data).reshape(expected.shape), expected, rtol=1e-6), "re-imported data differs"


def _import_variants(w, data):
    """Re-open the synthetic file lazily (memory-mapped), then as a cropped, binned, sampled part."""
    _import_from_file(w, data)                  # sets up the Import window for this file
    iw = w.ImportWindow
    path = iw.ImpFilePath.text()
    cube = data.reshape(NFY, NFX, NPY, NPX)

    # lazy: float32 in native order, no partial import -> the "Virtual Mapping" option is offered
    w.ShowImportWdw.trigger()
    iw.ImpFrPart.setChecked(False)
    iw.ImpPxPart.setChecked(False)
    iw.ImpPxPart.clicked.emit(False)
    qapp.processEvents()
    assert iw.ImpMemType.isEnabled(), "virtual mapping should be available for this file"
    iw.ImpMemType.setCurrentIndex(1)
    iw.ImportDataButton.click()
    _wait_for_import(w, data.shape)
    assert isinstance(w.Data, np.memmap) or isinstance(getattr(w.Data, "base", None), np.memmap), type(w.Data)
    assert np.array_equal(np.asarray(w.Data), data)
    for m in ("AnnMod", "CoMMod", "VrApMod"):
        _set_mode(w, m)

    # partial: start (x, y) = (1, 1), every 2nd probe position; diffraction from (2, 3), binned 2
    w.ShowImportWdw.trigger()
    iw.ImpMemType.setCurrentIndex(0)
    iw.ImpFrPart.setChecked(True)
    iw.ImpFrPart.clicked.emit(True)
    iw.IFrD.setValue(2)
    iw.IFrX1.setValue(1)
    iw.IFrY1.setValue(1)
    iw.ImpPxPart.setChecked(True)
    iw.ImpPxPart.clicked.emit(True)
    assert not iw.ImpMemType.isEnabled(), "virtual mapping cannot crop or bin"
    iw.IPxD.setValue(2)
    iw.IPxX1.setValue(2)
    iw.IPxY1.setValue(3)
    qapp.processEvents()
    fx, fy, px, py = iw.INFrX.value(), iw.INFrY.value(), iw.INPxX.value(), iw.INPxY.value()
    assert (fx, fy, px, py) == ((NFX - 2) // 2 + 1, (NFY - 2) // 2 + 1, (NPX - 2) // 2, (NPY - 3) // 2), (fx, fy, px, py)
    expected = cube[1:1 + (fy - 1) * 2 + 1:2, 1:1 + (fx - 1) * 2 + 1:2, 3:3 + 2 * py, 2:2 + 2 * px]
    expected = expected.reshape(fy, fx, py, 2, px, 2).sum(axis=(3, 5))
    iw.ImportDataButton.click()
    _wait_for_import(w, (fy * fx, py * px))
    assert np.allclose(w.Data.reshape(expected.shape), expected, rtol=1e-6), "partial import differs"
    for m in ("AlignMod", "AnnMod", "CoMMod", "DPCMod", "VrApMod"):
        w.DetrMode.setCurrentIndex(w.DetrMode.findData(m))
        qapp.processEvents()
        assert w.Fig.Dfrn.Image.shape == (py, px) and w.Fig.Real.Image.shape == (fy, fx), m
    w.ShowImportWdw.trigger()
    for box in (iw.ImpFrPart, iw.ImpPxPart):
        box.setChecked(False)
        box.clicked.emit(False)
    _import_from_file(w, data)                  # back to the full dataset


def _check_polygon_roi(w):
    """Draw a polygon ROI by feeding vertices to the selector, as mouse clicks would."""
    import callbacks.realSpaceROICallbacks as rs
    from callbacks import compute
    real_name = w.G.Img[w.G.Img.id == "Real"].name.item()
    old = rs.notifDLG
    rs.notifDLG = lambda *a, **k: real_name        # "which image do you want to draw on?"
    try:
        w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("poly"))
        qapp.processEvents()
    finally:
        rs.notifDLG = old
    assert w.A._tmp_selector is not None, "no polygon selector was started"
    verts = [(0.2, 0.1), (4.6, 0.4), (1.0, 2.8)]
    w.A._tmp_selector.onselect(verts)
    qapp.processEvents()
    assert w.A._tmp_selector is None and w.A.RealROI, "polygon was not created"
    mask = compute.polygon_mask((NFY, NFX), verts)
    assert 0 < mask.sum() < NFX * NFY
    assert np.array_equal(w.Fig.RealMask.Image.astype(bool), mask), "real-space mask is not the polygon"
    expected = w.Data[mask.ravel()].mean(axis=0).reshape(NPY, NPX)
    assert np.allclose(w.Fig.Dfrn.Image, expected, rtol=1e-5), "pattern is not the polygon average"
    w.RealROIInvert.click()
    qapp.processEvents()
    expected = w.Data[~mask.ravel()].mean(axis=0).reshape(NPY, NPX)
    assert np.allclose(w.Fig.Dfrn.Image, expected, rtol=1e-5), "inverted polygon is wrong"
    w.RealROIInvert.click()
    qapp.processEvents()


def _check_file_roi(w):
    """Load a weighted real-space ROI from an image file (stored transposed, to test that path)."""
    from PIL import Image
    from PyQt5 import QtWidgets as qtw
    weights = np.zeros((NFY, NFX))
    weights[1, 1:4] = 255
    weights[2, 2] = 51                          # 0.2 after scaling
    path = os.path.join(tempfile.mkdtemp(), "roi.png")
    Image.fromarray(weights.T.astype(np.uint8)).save(path)
    old = qtw.QFileDialog.getOpenFileName
    qtw.QFileDialog.getOpenFileName = staticmethod(lambda *a, **k: (path, ""))
    try:
        w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("file"))
        qapp.processEvents()
    finally:
        qtw.QFileDialog.getOpenFileName = old
    assert w.RealROIShape.currentData() == "file", "file ROI was rejected"
    wn = weights / 255
    assert np.allclose(w.Fig.RealMask.Image, wn), "real-space mask is not the file"
    expected = (wn.ravel() @ np.asarray(w.Data, float)) / wn.sum()
    assert np.allclose(w.Fig.Dfrn.Image, expected.reshape(NPY, NPX), rtol=1e-5), "pattern is not the weighted average"

    # a file of the wrong size is refused and the ROI falls back to the whole scan
    bad = os.path.join(tempfile.mkdtemp(), "bad.png")
    Image.fromarray(np.zeros((NFY + 1, NFX), np.uint8)).save(bad)
    w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("full"))
    qtw.QFileDialog.getOpenFileName = staticmethod(lambda *a, **k: (bad, ""))
    try:
        w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("file"))
        qapp.processEvents()
    finally:
        qtw.QFileDialog.getOpenFileName = old
    assert w.RealROIShape.currentData() == "full", "mis-sized mask file should be refused"


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


def _custom_sum(w):
    """Real image must be the combined custom mask applied to every pattern."""
    mask = np.asarray(w.Fig.DfrnMask.Image, float)
    expected = (np.asarray(w.Data, float) @ mask.ravel()).reshape(NFY, NFX)
    assert np.allclose(w.Fig.Real.Image, expected, rtol=1e-5), "custom image is not the mask applied to the data"


def _cd_select(w, mid):
    row = list(w.A.Custom).index(mid)
    w.CDT.selectRow(row)
    qapp.processEvents()


def _check_custom_masks(w):
    from callbacks.compute import custom as cm
    _set_mode(w, "CustMod")
    assert w.CDInterMask.currentText() == "Color Mix" and w.CDRotStep.currentData() == 90
    b0 = np.asarray(w.B0, float)
    for btn, typ in ((w.CDNewCircle, "Circle"), (w.CDNewGrid, "Grid"), (w.CDNewGridNoCenter, "GridNoCenter"),
                     (w.CDNewBandpass, "Bandpass"), (w.CDNewWedge, "Wedge")):
        n = len(w.A.Custom)
        btn.click()
        qapp.processEvents()
        assert len(w.A.Custom) == n + 1, f"no {typ} mask was created"
        cmask = list(w.A.Custom.values())[-1]
        assert cmask.type == typ and cmask.mask is not None and cmask.mask.shape == (NPY, NPX)
        assert w.CDT.rowCount() == n + 1 and w.CDT.item(n, 0).text() == cmask.id
        assert w.CDDTable.rowCount() == len(cmask.points()), f"details table rows wrong for {typ}"
    assert list(w.A.Custom) == ["A", "B", "C", "D", "E"]
    a = w.A.Custom["A"]
    assert np.allclose(a.p1, b0) and a.r1 == w.TBR.value(), "circle should start on the transmitted beam"
    assert np.array_equal(a.mask, cm.circle_detector((NPY, NPX), b0, w.TBR.value(), b0))
    assert w.A.Custom["E"].mirrored, "wedges are mirrored by default"
    # Color Mix: RGB images shown, 2-D images kept
    assert w.Fig.DfrnMask.ColorMix.shape == (NPY, NPX, 3) and w.Fig.Real.ColorMix.shape == (NFY, NFX, 3)
    assert w.ImageAx.Real.get_array().shape == (NFY, NFX, 3), "Color Mix composite is not displayed"
    _check_images(w, ["Real", "DfrnMask"])
    _custom_sum(w)


def _check_custom_modes(w):
    from callbacks.compute import custom as cm
    masks = [c.mask for c in w.A.Custom.values()]
    for mode in cm.INTER_MODES:
        w.CDInterMask.setCurrentIndex(w.CDInterMask.findText(mode))
        qapp.processEvents()
        _custom_sum(w)
        if mode == "Additive":
            assert np.allclose(w.Fig.DfrnMask.Image, sum(masks)), "additive is not the sum"
        if mode == "Current-only":
            sel = w.CDT.item(w.CDT.currentRow(), 0).text()
            assert np.allclose(w.Fig.DfrnMask.Image, w.A.Custom[sel].mask)
    w.CDInterMask.setCurrentIndex(w.CDInterMask.findText("Union"))
    qapp.processEvents()
    assert w.ImageAx.Real.get_array().ndim == 2, "RGB still shown outside Color Mix"
    # disabling and weighting via the table
    from PyQt5 import QtCore as qtc
    w.CDT.item(1, 3).setCheckState(qtc.Qt.Unchecked)
    qapp.processEvents()
    assert not w.A.Custom["B"].enabled
    w.CDT.item(0, 5).setText("2")
    qapp.processEvents()
    assert w.A.Custom["A"].weight == 2
    w.CDInterMask.setCurrentIndex(w.CDInterMask.findText("Additive"))
    qapp.processEvents()
    expected = sum(c.mask * c.weight for c in w.A.Custom.values() if c.enabled)
    assert np.allclose(w.Fig.DfrnMask.Image, expected), "weights/enable not honoured"
    _custom_sum(w)


def _check_custom_edit(w):
    _cd_select(w, "A")
    a = w.A.Custom["A"]
    b0 = np.asarray(w.B0, float)
    # move the circle 3 px right through the details table (absolute pixel Cartesian)
    w.SettingsWindow.DCUnit.setCurrentIndex(w.SettingsWindow.DCUnit.findData("px"))
    w.SettingsWindow.DCPos.setCurrentIndex(w.SettingsWindow.DCPos.findText("Absolute"))
    qapp.processEvents()
    assert w.CDDTable.horizontalHeaderItem(0).text().startswith("X")
    w.CDDTable.setCurrentCell(0, 0)
    w.CDDTable.item(0, 0).setText(str(b0[0] + 3))
    qapp.processEvents()
    assert np.allclose(a.p1, b0 + [3, 0]), f"table edit gave p1 = {a.p1}"
    # rotate 90° clockwise on screen (y down): +x -> +y
    w.CDRotCW.click()
    qapp.processEvents()
    assert np.allclose(a.p1, b0 + [0, 3]), f"rotation gave p1 = {a.p1}"
    w.CDFlipHorz.click()
    qapp.processEvents()
    assert np.allclose(a.p1, b0 + [0, -3])
    w.CDTranspose.click()
    qapp.processEvents()
    assert np.allclose(a.p1, b0 + [-3, 0])
    w.CDFlipVert.click()
    qapp.processEvents()
    assert np.allclose(a.p1, b0 + [3, 0])
    before = a.mask.copy()
    w.CDMirror.click()
    qapp.processEvents()
    assert a.mirrored and a.mask.sum() > before.sum(), "mirror added nothing"
    mirrored = a.mask.copy()
    w.CDInvert.click()
    qapp.processEvents()
    assert a.inverted and np.array_equal(a.mask, mirrored.max() - mirrored), "invert is not max - mask"
    w.CDInvert.click()
    w.CDMirror.click()
    qapp.processEvents()
    assert np.array_equal(a.mask, before), "mirror/invert off did not restore the mask"
    # polar, relative: radius column follows
    w.SettingsWindow.DCSys.setCurrentIndex(w.SettingsWindow.DCSys.findText("Polar"))
    qapp.processEvents()
    assert w.CDDTable.horizontalHeaderItem(0).text().startswith("ρ")
    assert abs(float(w.CDDTable.item(0, 0).text()) - 3) < 1e-3, "polar ρ wrong"
    w.SettingsWindow.DCSys.setCurrentIndex(w.SettingsWindow.DCSys.findText("Cartesian"))
    qapp.processEvents()
    _custom_sum(w)


def _check_custom_polygon_file_math(w):
    from PIL import Image
    from PyQt5 import QtWidgets as qtw
    from callbacks import compute
    w.CDNewPolygon.click()
    qapp.processEvents()
    verts = [(2.0, 2.0), (10.0, 3.0), (5.0, 12.0)]
    w._cdSelector.onselect(verts)
    qapp.processEvents()
    poly = list(w.A.Custom.values())[-1]
    assert poly.type == "Polygon" and np.array_equal(poly.mask, compute.polygon_mask((NPY, NPX), verts))

    img = np.zeros((NPY, NPX), np.uint8)
    img[3:8, 5:15] = 255
    path = os.path.join(tempfile.mkdtemp(), "mask.png")
    Image.fromarray(img).save(path)
    old = qtw.QFileDialog.getOpenFileName
    qtw.QFileDialog.getOpenFileName = staticmethod(lambda *a, **k: (path, ""))
    try:
        w.CDNewFromFile.click()
        qapp.processEvents()
    finally:
        qtw.QFileDialog.getOpenFileName = old
    fm = list(w.A.Custom.values())[-1]
    assert fm.type == "File" and np.allclose(fm.mask, img / 255), "file mask wrong"
    w.CDRotCW.click()          # non-square: rotation step is 180 and fixed
    qapp.processEvents()
    assert w.CDRotStep.currentData() == 180 and np.allclose(fm.mask, np.rot90(img / 255, 2))

    w.CDNewMath.click()
    qapp.processEvents()
    mm = list(w.A.Custom.values())[-1]
    assert mm.type == "Math" and np.allclose(mm.mask, 1)
    w.SettingsWindow.MathFormula.setPlainText(f"{poly.id} & ~{fm.id}")
    w.SettingsWindow.MathEval.click()
    qapp.processEvents()
    assert np.array_equal(mm.mask.astype(bool), poly.mask.astype(bool) & ~fm.mask.astype(bool)), "math mask wrong"
    w.SettingsWindow.MathFormula.setPlainText(f"{mm.id} + 1")       # self-reference is refused
    w.SettingsWindow.MathEval.click()
    qapp.processEvents()
    assert mm.formula.endswith("+ 1")
    _custom_sum(w)


def _check_custom_delete_and_modes(w):
    n = len(w.A.Custom)
    _cd_select(w, "B")
    w.CDDelMask.click()
    qapp.processEvents()
    assert "B" not in w.A.Custom and w.CDT.rowCount() == n - 1
    _custom_sum(w)
    _set_mode(w, "AnnMod")
    assert all(not c.handles for c in w.A.Custom.values()), "custom annotations left on other modes"
    _set_mode(w, "CustMod")
    assert all(c.handles or c.type in ("File", "Math") for c in w.A.Custom.values()), "annotations not redrawn"
    _custom_sum(w)
    _set_mode(w, "AnnMod")


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

    _step("custom: circle, grids, bandpass, wedge", lambda: _check_custom_masks(w))
    _step("custom: inter-mask modes, enable, weight", lambda: _check_custom_modes(w))
    _step("custom: details table, rotate, flip, mirror, invert, polar", lambda: _check_custom_edit(w))
    _step("custom: polygon, file, math", lambda: _check_custom_polygon_file_math(w))
    _step("custom: delete, leave and return to mode", lambda: _check_custom_delete_and_modes(w))
    _step("ROI point", lambda: _check_point_roi(w))
    for shape in ["rectangle", "ellipse", "full"]:
        _step("ROI " + shape, lambda s=shape: (w.RealROIShape.setCurrentIndex(w.RealROIShape.findData(s)),
                                               _check_images(w, ["Dfrn", "RealMask"])))
    _step("ROI invert", lambda: (w.RealROIInvert.setChecked(True), w.RealROIInvert.setChecked(False)))
    _step("ROI polygon (drawn) and invert", lambda: _check_polygon_roi(w))
    _step("ROI from file (weighted, transposed) and a refused file", lambda: _check_file_roi(w))
    _step("ROI back to full", lambda: w.RealROIShape.setCurrentIndex(w.RealROIShape.findData("full")))

    sw = w.SettingsWindow
    for i in [sw.DispImage.itemData(k) for k in range(sw.DispImage.count())]:
        _step("display settings on " + str(i), lambda i=i: _display(w, i))
    _step("update images", lambda: w.UpdateImages.trigger())
    _step("hide all image windows", lambda: hideAllWindows(w))
    _step("re-import same file", lambda: _import_from_file(w, data))
    _step("lazy import, then partial import (crop, bin, sample)", lambda: _import_variants(w, data))

    out = tempfile.mkdtemp()
    _step("mode AnnMod for saving", lambda: _set_mode(w, "AnnMod"))
    _step("save images (TIFF, PNG, annotated PNG)", lambda: _save_images(w, out))
    exported = {}
    _step("export HDF5, whole dataset", lambda: exported.update(h5=_check_export_hdf5(w, out)))
    _step("export raw, big endian, partial + binned + sampled", lambda: exported.update(raw=_check_export_raw_partial(w, out)))
    _step("re-import exported big-endian raw (geometry from file name)", lambda: _reimport(w, *exported["raw"], hdf5=False, byte_order="b"))
    _step("re-import exported HDF5", lambda: _reimport(w, *exported["h5"], hdf5=True))
    _step("modes after re-import", lambda: [_set_mode(w, m) for m in ("AlignMod", "AnnMod", "CoMMod", "VrApMod")])
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
