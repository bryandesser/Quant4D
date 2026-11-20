"""Import-window support for Gatan DigitalMicrograph DM3/DM4 files.

The file's tag tree is read by :func:`callbacks.io.dm_header.read_dm_header`;
this module only transfers what it finds to the Import window.
"""
import numpy as np

from .dm_header import read_dm_header
from ..signals import signals_blocked

__all__ = ["prepDM"]


def prepDM(self, source=None, adopt=False):
    """Fill the Import window from the header of the DM3/DM4 file in the path field.

    Lists every image in the file (selecting the largest unless the user picked
    one, *source* being the image dropdown), and sets its dimensions, data
    offset, data type and byte order.  With *adopt* (a new file) the scan
    step (calibration of dimensions 3/4) fills the Scan Step field and the
    microscope voltage the Accelerating Voltage field.

    DM stores dimensions fastest first; a 4-D STEM dataset is
    ``(kx, ky, rx, ry)``, i.e. whole diffraction patterns one after another,
    which is the layout pyQuant4D reads.

    Returns
    -------
    str
        Notes for the Import window.
    """
    iw = self.ImportWindow
    path = iw.ImpFilePath.text()
    try:
        info = read_dm_header(path)
    except (OSError, ValueError, KeyError, IndexError) as exc:
        return f"Could not read the DM file header: {exc}"
    self.T.dm = info
    if not info.images:
        return "No images found in this DM file."

    # list the images; pick the largest unless the user chose one
    iw.ImpSubImg.setEnabled(True)
    if source is not iw.ImpSubImg or iw.ImpSubImg.count() != len(info.images):
        with signals_blocked(iw.ImpSubImg):
            iw.ImpSubImg.clear()
            iw.ImpSubImg.addItems([f"{im.name} {'x'.join(map(str, im.dims))}" for im in info.images])
            iw.ImpSubImg.setCurrentIndex(int(np.argmax([im.count for im in info.images])))
    image = info.images[max(0, iw.ImpSubImg.currentIndex())]

    dims = list(image.dims) + [1] * (4 - len(image.dims))
    for name in ("DNPxX", "DNPxY", "DNFrX", "DNFrY"):
        getattr(iw, name).setMaximum(np.iinfo(np.int32).max)
    iw.DNPxX.setValue(dims[0])
    iw.DNPxY.setValue(dims[1])
    iw.DNFrX.setValue(dims[2])
    iw.DNFrY.setValue(int(np.prod(dims[3:])))

    iw.DataOffset.setMaximum(np.iinfo(np.int32).max)
    iw.DataOffset.setValue(image.offset)
    iw.FrHead.setValue(0)
    iw.FrFoot.setValue(0)
    self.T.fileTail = int(info.file_size - image.offset - image.nbytes)

    iw.ImpDataType.setCurrentIndex(max(0, iw.ImpDataType.findData(image.dtype or "unknown")))
    iw.ImpByteOrder.setCurrentIndex(iw.ImpByteOrder.findData("l" if info.little_endian else "b"))

    order = "Little Endian" if info.little_endian else "Big Endian"
    dtype = image.dtype or f"unsupported (DM data type {image.data_type_code})"
    notes = ("Dim: X = {}, Y = {}, Z = {}, W = {}\nDM{}, {}\nData type: {}\n"
             "Selected image's offset is {} bytes.").format(*dims[:4], info.version, order, dtype, image.offset)
    return notes + _calibrationNotes(self, image, adopt)


def _calibrationNotes(self, image, adopt: bool) -> str:
    """Notes on the DM calibration; with *adopt*, fill the Scan Step and voltage fields from it."""
    from ..scan_step import setImportStep  # noqa: E402
    lines = []
    scan = image.calibration(2) if len(image.dims) >= 4 else None
    if scan is not None:
        other = image.calibration(3)
        lines.append(f"Scan step: {scan[0]:.6g} {scan[1]}" + (
            f" (Y: {other[0]:.6g} {other[1]}; X is used)" if other and other != scan else ""))
        if adopt:
            setImportStep(self, scan[0], scan[1])
    if image.voltage_V:
        lines.append(f"Accelerating voltage: {image.voltage_V / 1000:g} kV")
        if adopt:
            with signals_blocked(self.ImportWindow.ImpAccVolt):
                self.ImportWindow.ImpAccVolt.setValue(image.voltage_V / 1000)
    detector = detectorCalibration(image)
    if detector is not None:
        from .emd import mrad_per_unit  # noqa: E402
        scale, units = detector
        other = image.calibration(1)
        line = f"Detector: {scale:.6g} {units}/px"
        if other and (abs(other[0] - scale) > 1e-6 * scale or other[1] != units):
            line += f" (Y: {other[0]:.6g} {other[1]}; X is used)"
        if mrad_per_unit(units, self.ImportWindow.ImpAccVolt.value()) is not None:
            line += ("\nApplied as the diffraction scale after import (Alignment mode); the beam centre "
                     "comes from auto-alignment, not from the DM origin")
            if mrad_per_unit(units) is None:
                line += " (converted to mrad at the Accelerating Voltage)"
        else:
            line += " (not used: pyQuant4D calibrates in mrad)"
        lines.append(line)
    return ("\n\nDM calibration\n" + "\n".join(lines)) if lines else ""


def detectorCalibration(image):
    """``(scale, units)`` of the detector (DM dimension 1, x) of a 3-D or 4-D image, or None."""
    return image.calibration(0) if len(image.dims) >= 3 else None


def dmCalibration(self, image, kV):
    """The DM detector calibration as an EmdCalibration in mrad (no beam centre), or None."""
    from .emd import EmdCalibration, usable_calibration  # noqa: E402
    detector = detectorCalibration(image)
    if detector is None:
        return None
    cal = usable_calibration(EmdCalibration(q_pixel_size=float(detector[0]), q_units=detector[1]), kV)
    return cal if cal is not None and cal.q_units == "mrad" else None
