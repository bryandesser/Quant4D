"""Import-window support for Gatan DigitalMicrograph DM3/DM4 files.

The file's tag tree is read by :func:`callbacks.io.dm_header.read_dm_header`;
this module only transfers what it finds to the Import window.
"""
import numpy as np

from callbacks.io.dm_header import read_dm_header
from callbacks.signals import signals_blocked

__all__ = ["prepDM"]


def prepDM(self):
    """Fill the Import window from the header of the DM3/DM4 file in the path field.

    Lists every image in the file (selecting the largest unless the user picked
    one), and sets its dimensions, data offset, data type and byte order.

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
    if self.sender() is not iw.ImpSubImg or iw.ImpSubImg.count() != len(info.images):
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
    return ("Dim: X = {}, Y = {}, Z = {}, W = {}\nDM{}, {}\nData type: {}\n"
            "Selected image's offset is {} bytes.").format(*dims[:4], info.version, order, dtype, image.offset)
