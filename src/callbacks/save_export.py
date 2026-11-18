"""Save window: saving images and exporting the dataset.

Every widget of the Save window is connected to :func:`saveExportCallbacks`,
which dispatches on the sender.  The file writing itself lives in
:mod:`callbacks.io.export`.

Export regions use 0-based ``(x, y)`` start points, like the rest of the UI.
"""
from __future__ import annotations

import os

import numpy as np
from PyQt5 import QtWidgets as qtw

from callbacks.io import export as ex
from callbacks.signals import signals_blocked

__all__ = ["saveExportCallbacks", "connectSaveWindow", "resetExportRanges",
           "saveImages", "exportDataset", "imageFilename", "exportRegions", "exportPath"]

_ANNULAR_MODES = ("AnnMod", "CoMMod", "DPCMod")


# ---------------------------------------------------------------------------
# Wiring
# ---------------------------------------------------------------------------
def connectSaveWindow(self):
    """Connect every widget of the Save window; called once from ``slotsSignals``."""
    sw = self.SaveWindow
    cb = lambda *_: saveExportCallbacks(self)    # noqa: E731
    sw.SaveExport.clicked.connect(cb)
    sw.SaveDirButton.clicked.connect(cb)
    sw.SaveCloseButton.clicked.connect(cb)
    sw.SaveTabGroup.currentChanged.connect(cb)
    sw.SaveImgPNG.clicked.connect(cb)
    sw.SaveImgPNGAnnot.clicked.connect(cb)
    for w in (sw.SaveImgPrefix, sw.SaveDir, sw.ExpFilename):
        w.textChanged.connect(cb)
    for w in (sw.ExpFormat, sw.ExpByteOrder):
        w.currentIndexChanged.connect(cb)
    sw.ExpDimSuff.clicked.connect(cb)
    sw.ExpPxPart.clicked.connect(cb)
    sw.ExpFrPart.clicked.connect(cb)
    for name in ("EPxX1", "EPxY1", "ENPxX", "ENPxY", "EPxD", "EFrX1", "EFrY1", "ENFrX", "ENFrY", "EFrD"):
        getattr(sw, name).valueChanged.connect(cb)

    # export formats (the .ui file lists them without data)
    with signals_blocked(sw.ExpFormat):
        sw.ExpFormat.clear()
        sw.ExpFormat.addItem("HDF5 (*.h5)", "h5")
        sw.ExpFormat.addItem("Raw binary (*.raw)", "raw")
    sw.EPxD.setEnabled(True)     # binning is supported
    _updateSaveButton(self)


def saveExportCallbacks(self):
    """Dispatcher for every widget of the Save window."""
    sw = self.SaveWindow
    sender = self.sender()

    if sender is sw.SaveCloseButton:
        sw.hide()
        return
    if sender is sw.SaveDirButton:
        start = sw.SaveDir.text() if os.path.isdir(sw.SaveDir.text()) else os.getcwd()
        chosen = qtw.QFileDialog.getExistingDirectory(sw, "Select Save Directory", start)
        if chosen:
            sw.SaveDir.setText(chosen)
        return
    if sender is sw.SaveExport:
        if sw.SaveTabGroup.currentWidget() is sw.ExportTab:
            exportDataset(self)
        else:
            saveImages(self)
        return

    _updateSaveButton(self)
    if self.D is not None and self.Data is not None:
        _clampExportRanges(self)
        _updateExportNotes(self)


def _updateSaveButton(self):
    sw = self.SaveWindow
    exporting = sw.SaveTabGroup.currentWidget() is sw.ExportTab
    sw.SaveExport.setText("Export Dataset" if exporting else "Save Images")
    sw.SaveImgPNGAnnot.setEnabled(sw.SaveImgPNG.isChecked())
    sw.SaveImgAnnotDPI.setEnabled(sw.SaveImgPNG.isChecked() and sw.SaveImgPNGAnnot.isChecked())


def _tell(self, icon, msg, title):
    from callbacks.utils import notifDLG
    notifDLG(self, self.SaveWindow, icon, msg, title)


# ---------------------------------------------------------------------------
# Save images
# ---------------------------------------------------------------------------
def _number(value: float) -> str:
    """Compact number for a filename: 12.5 -> '12.5', 40.0 -> '40'."""
    return f"{float(value):g}"


def imageFilename(self, id: str, ext: str) -> str:
    """``<prefix><id>[_ri<inner><unit>][_ro<outer><unit>].<ext>``.

    The annular detector angles are added when their boxes are ticked and the
    detector mode uses the annular detector; they are given in the units shown
    next to the radius fields (mrad or px).
    """
    sw = self.SaveWindow
    name = sw.SaveImgPrefix.text() + id
    if self.DetrMode.currentData() in _ANNULAR_MODES:
        unit = self.SettingsWindow.DCUnit.currentData() or ""
        if sw.SavePrfxRi.isChecked():
            name += f"_ri{_number(self.AnnRi_NF.value())}{unit}"
        if sw.SavePrfxRo.isChecked():
            name += f"_ro{_number(self.AnnRo_NF.value())}{unit}"
    return f"{name}.{ext}"


def saveImages(self):
    """Save the images selected in the list, in the formats ticked."""
    from callbacks.plotting import plotImage

    sw = self.SaveWindow
    folder = sw.SaveDir.text()
    ids = [item.text() for item in sw.SaveImgList.selectedItems()]
    as_tif, as_png, annotated = sw.SaveImgTIF.isChecked(), sw.SaveImgPNG.isChecked(), sw.SaveImgPNGAnnot.isChecked()

    if not os.path.isdir(folder):
        return _tell(self, "warn", f"The save directory does not exist:\n{folder}", "Invalid Directory")
    if not ids:
        return _tell(self, "warn", "Select at least one image in the list.", "Nothing Selected")
    if not (as_tif or as_png):
        return _tell(self, "warn", "Tick at least one format (TIFF or PNG).", "No Format Selected")

    written, skipped = [], []
    for id in ids:
        fig = self.Fig[id]
        if fig is None or fig.Image is None:
            skipped.append(id)
            continue
        if as_tif:
            path = os.path.join(folder, imageFilename(self, id, "tif"))
            ex.save_tiff(path, fig.Image)
            written.append(path)
        if as_png:
            plotImage(self, id)          # make sure the drawn image is current, even if its window is hidden
            path = os.path.join(folder, imageFilename(self, id, "png"))
            if annotated:
                fig.fig.savefig(path, dpi=sw.SaveImgAnnotDPI.value(), facecolor=fig.fig.get_facecolor())
            else:
                ex.save_png(path, ex.rgb_as_displayed(self.ImageAx[id]))
            written.append(path)

    msg = f"Saved {len(written)} file(s) to {folder}:\n" + "\n".join(os.path.basename(p) for p in written)
    if skipped:
        msg += "\n\nNot computed yet, so not saved: " + ", ".join(skipped)
    _tell(self, "none", msg, "Images Saved")
    return written


# ---------------------------------------------------------------------------
# Export dataset
# ---------------------------------------------------------------------------
_PX = ("EPxX1", "EPxY1", "ENPxX", "ENPxY", "EPxD")
_FR = ("EFrX1", "EFrY1", "ENFrX", "ENFrY", "EFrD")


def resetExportRanges(self):
    """Set the export regions to the whole of a newly loaded dataset."""
    sw = self.SaveWindow
    widgets = [getattr(sw, n) for n in _PX + _FR]
    with signals_blocked(*widgets, sw.ExpPxPart, sw.ExpFrPart):
        sw.ExpPxPart.setChecked(False)
        sw.ExpFrPart.setChecked(False)
        for names, (nx, ny) in ((_PX, (self.D.NPxX, self.D.NPxY)), (_FR, (self.D.NFrX, self.D.NFrY))):
            x1, y1, cx, cy, step = (getattr(sw, n) for n in names)
            x1.setRange(0, nx - 1)
            y1.setRange(0, ny - 1)
            cx.setRange(1, nx)
            cy.setRange(1, ny)
            step.setRange(1, max(1, min(nx, ny)))
            x1.setValue(0)
            y1.setValue(0)
            cx.setValue(nx)
            cy.setValue(ny)
            step.setValue(1)
    _updateExportNotes(self)


def _clampExportRanges(self):
    """Keep each region inside the dataset after any of its fields changes.

    The start and step take priority; the count shrinks to fit.
    """
    sw = self.SaveWindow
    for names, (nx, ny), binned in ((_PX, (self.D.NPxX, self.D.NPxY), True),
                                    (_FR, (self.D.NFrX, self.D.NFrY), False)):
        x1, y1, cx, cy, step = (getattr(sw, n) for n in names)
        with signals_blocked(x1, y1, cx, cy, step):
            b = step.value()
            for start, count, n in ((x1, cx, nx), (y1, cy, ny)):
                most = (n - start.value()) // b if binned else (n - 1 - start.value()) // b + 1
                if most < 1:            # start too far for this step: pull the start back
                    start.setValue(n - b if binned else n - 1)
                    most = 1
                count.setMaximum(max(1, most))
                count.setValue(min(count.value(), most))


def exportRegions(self) -> tuple[ex.Region, ex.Region]:
    """``(frames, pixels)`` to export, from the partial-export fields (or everything)."""
    sw = self.SaveWindow

    def read(names, part, size):
        if not part.isChecked():
            return ex.full_region(size)
        x1, y1, cx, cy, step = (getattr(sw, n).value() for n in names)
        return ex.Region((x1, y1), (cx, cy), step)

    frames = read(_FR, sw.ExpFrPart, (self.D.NFrX, self.D.NFrY))
    pixels = read(_PX, sw.ExpPxPart, (self.D.NPxX, self.D.NPxY))
    return frames, pixels


def exportPath(self, frames: ex.Region, pixels: ex.Region) -> str:
    """Full path of the export file, from the directory, file name, format and suffix options."""
    sw = self.SaveWindow
    fmt = sw.ExpFormat.currentData() or "h5"
    stem = sw.ExpFilename.text().strip()
    if not stem:
        stem = (sw.SaveImgPrefix.text().rstrip("_") or "export") + "_export"
    stem = os.path.splitext(stem)[0] if os.path.splitext(stem)[1].lower() in (".h5", ".hdf5", ".raw") else stem
    if sw.ExpDimSuff.isChecked():
        stem += ex.dims_suffix(frames, pixels)
    return os.path.join(sw.SaveDir.text(), f"{stem}.{fmt}")


def _updateExportNotes(self):
    sw = self.SaveWindow
    try:
        frames, pixels = exportRegions(self)
        frames.check((self.D.NFrX, self.D.NFrY), binned=False)
        pixels.check((self.D.NPxX, self.D.NPxY), binned=True)
    except ValueError as exc:
        sw.ExpNotes.setPlainText(f"Invalid export region: {exc}")
        return
    shape = ex.exported_shape(frames, pixels)
    dtype = ex.exported_dtype(self.Data.dtype, pixels)
    size = np.prod(shape) * dtype.itemsize

    def describe(r: ex.Region, what: str, unit: str, verb: str) -> str:
        line = f"{what}: {r.count[0]} x {r.count[1]} {unit}, from (x, y) = {r.start}"
        return line + (f", {verb} {r.step}" if r.step > 1 else "")

    lines = [
        f"File: {exportPath(self, frames, pixels)}",
        describe(frames, "Scan", "positions", "every"),
        describe(pixels, "Diffraction", "px", "binned by"),
        f"Shape (NFrY, NFrX, NPxY, NPxX): {shape}",
        f"Data type: {dtype} ({self.C.EndianTxt.get(sw.ExpByteOrder.currentData(), '')})",
        f"Size: {size / 1024 ** 3:.3f} GiB",
    ]
    if dtype != self.Data.dtype:
        lines.append(f"Integer data widened from {self.Data.dtype} so binned sums cannot overflow.")
    sw.ExpNotes.setPlainText("\n".join(lines))


def _metadata(self, frames: ex.Region, pixels: ex.Region) -> dict:
    """What is known about the dataset and the export, stored with HDF5 exports."""
    try:
        from importlib.metadata import version
        pkg_version = version("pyquant4d")
    except Exception:
        pkg_version = "unknown"
    meta = {
        "software": f"pyQuant4D {pkg_version}",
        "source_file": self.D.filePath,
        "source_scan_xy": np.array([self.D.NFrX, self.D.NFrY]),
        "source_detector_xy": np.array([self.D.NPxX, self.D.NPxY]),
        "scan_start_xy": np.array(frames.start),
        "scan_count_xy": np.array(frames.count),
        "scan_sampling": frames.step,
        "detector_start_xy": np.array(pixels.start),
        "detector_count_xy": np.array(pixels.count),
        "detector_binning": pixels.step,
        "import_notes": self.D.NoteImp,
        "file_notes": self.D.NoteFileMeta,
    }
    if getattr(self, "B0", None) is not None and self.P.TransBeamInit:
        b0 = np.asarray(self.B0, dtype=float)
        b = pixels.step
        meta["beam_center_xy_source"] = b0
        # pixel i of the export covers source pixels start + i*b ... start + i*b + b - 1
        meta["beam_center_xy"] = (b0 - np.asarray(pixels.start) + 0.5) / b - 0.5
        meta["beam_radius_px"] = float(self.TBR.value()) / b
        meta["convergence_semiangle_mrad"] = float(self.Alpha.value())
        meta["mrad_per_px"] = float(self.mradPx.value()) * b
    return meta


def exportDataset(self):
    """Write the dataset (or the selected part of it) to HDF5 or raw binary."""
    sw = self.SaveWindow
    if self.D is None or self.Data is None:
        return _tell(self, "warn", "No dataset is loaded.", "Nothing to Export")
    if not os.path.isdir(sw.SaveDir.text()):
        return _tell(self, "warn", f"The save directory does not exist:\n{sw.SaveDir.text()}", "Invalid Directory")
    frames, pixels = exportRegions(self)
    path = exportPath(self, frames, pixels)
    if os.path.exists(path):
        from callbacks.utils import notifDLG
        if notifDLG(self, sw, "quest", f"{path}\nalready exists. Overwrite it?", "File Exists",
                    ["Overwrite", "Cancel"]) != "Overwrite":
            return None

    scan = (self.D.NFrX, self.D.NFrY)
    detector = (self.D.NPxX, self.D.NPxY)
    byte_order = sw.ExpByteOrder.currentData() or "l"
    from callbacks.window_manager import busyIndicator  # noqa: E402
    try:
        with busyIndicator(self):
            if (sw.ExpFormat.currentData() or "h5") == "raw":
                shape = ex.write_raw(path, self.Data, scan, detector, frames, pixels, byte_order)
            else:
                shape = ex.write_hdf5(path, self.Data, scan, detector, frames, pixels, byte_order,
                                      _metadata(self, frames, pixels))
    except (ValueError, OSError) as exc:
        return _tell(self, "error", f"Export failed:\n{exc}", "Export Failed")
    _tell(self, "none", f"Exported {shape} (NFrY, NFrX, NPxY, NPxX) to\n{path}", "Dataset Exported")
    return path
