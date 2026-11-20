from .import_io import getImportInfo
from .utils import checkNaN, notifDLG
from .importCallbacks import importCallbacks
import numpy as np
from . import compute  # noqa: E402


def datasetOptCallbacks(self):
    match self.sender():
        case self.SettingsWindow.SwapByteOrder:  # Swap byte-order, then ask whether it is right
            # Only the diffraction pattern is updated while the user decides: the other windows
            # would show stale images, so they are hidden until the answer.
            hidden = [id for id in self.G.ImgID if id != "Dfrn" and self.Fig[id].isVisible()]
            for id in hidden:
                self.Fig[id].hide()
            keep = False
            try:
                if not swapByteOrder(self, update=False):
                    return
                _showPatternOnly(self)
                sel = notifDLG(self, self, 'quest', "Is the current byte-order correct?",
                               'Byte Order Swap', ["Yes", "No. Revert"])
                keep = not str(sel or "").startswith("No")     # None when the dialog is dismissed
                if not keep:
                    swapByteOrder(self, update=False)          # back to the data the other images show
                    _showPatternOnly(self)
            finally:
                for id in hidden:
                    self.Fig[id].show()
            if keep:
                self.UpdateImages.trigger()                    # every image from the swapped data

        case self.SettingsWindow.SwapDfrnXY | self.SettingsWindow.SwapRealXY:
            # Diffraction or real-space
            if self.sender() == self.SettingsWindow.SwapDfrnXY:
                # Swap diffraction X/Y dimensions
                self.D.DNPxX, self.D.DNPxY = self.D.DNPxY, self.D.DNPxX
                self.D.NPxX, self.D.NPxY = self.D.NPxY, self.D.NPxX
                self.D.PxX1, self.D.PxY1 = self.D.PxY1, self.D.PxX1
                self.D.NPx = np.flip(self.D.NPx)

            else:
                # Delete all Real-space ROIs;
                for ii in self.A.ROIs:
                    try:
                        self.A.ROIs[ii].remove()
                    except BaseException:
                        pass
                    finally:
                        self.A.ROIs[ii] = None
                self.P.TransBeamInit = 1

                # Swap real X/Y dimensions
                self.D.DNFrX, self.D.DNFrY = self.D.DNFrY, self.D.DNFrX
                self.D.NFrX, self.D.NFrY = self.D.NFrY, self.D.NFrX
                self.D.FrX1, self.D.FrY1 = self.D.FrY1, self.D.FrX1
                self.D.NFr = np.flip(self.D.NFr)

            # Re-prepare the imported data
            importCallbacks(self)

            self.SettingsWindow.DataInfo.setPlainText(getImportInfo(self))

        case self.PreviewButton:
            # Check data NaN/Inf, without asking to sway byte-order
            sel = checkNaN(self, image=self.ImageAx.Preview.get_array(), preview=True)
            if sel == 'Set NaNs to 0':
                from .py4dstem_bridge import ownData  # noqa: E402
                ownData(self)                   # never write into a notebook's DataCube
                self.Data[np.ma.masked_invalid(self.Data).mask] = 0
                compute.release_device_data()   # the GPU copy is now stale

        case other:
            self.SettingsWindow.DataInfo.setPlainText(getImportInfo(self))
            # Check data NaN/Inf, ask whether to sway byte-order
            sel = checkNaN(self, image=self.ImageAx.Dfrn.get_array(), preview=False)
            if sel == 'Set NaNs to 0':
                from .py4dstem_bridge import ownData  # noqa: E402
                ownData(self)                   # never write into a notebook's DataCube
                self.Data[np.ma.masked_invalid(self.Data).mask] = 0
                compute.release_device_data()   # the GPU copy is now stale


def _showPatternOnly(self) -> None:
    """Recompute and show just the diffraction pattern (of the current real-space region)."""
    from .plotting import plotImage  # noqa: E402
    from .realSpaceROICallbacks import diffractionPattern  # noqa: E402
    weights = self.Fig.RealMask.Image
    if weights is None:
        weights = np.ones(self.Data.shape[0])
    self.Fig.Dfrn.Image = diffractionPattern(self, np.asarray(weights, float).ravel())
    self.Fig.Dfrn.show()
    plotImage(self, "Dfrn")


def swapByteOrder(self, update: bool = True) -> bool:
    """Reinterpret the dataset with the other byte order and (if *update*) update the images.

    In-memory data is byte-swapped in place (it stays in the native byte order the compute and
    GPU paths need); a lazily loaded dataset is a read-only memory map, so it is viewed with the
    swapped dtype instead (no copy, nothing written to the file).  Returns False on failure.
    """
    from .window_manager import busyIndicator  # noqa: E402
    try:
        with busyIndicator(self):
            if isinstance(self.Data, np.memmap) or not self.Data.flags.writeable:
                self.Data = self.Data.view(self.Data.dtype.newbyteorder())
            else:
                from .py4dstem_bridge import ownData  # noqa: E402
                ownData(self)                   # never write into a notebook's DataCube
                self.Data.byteswap(inplace=True)
    except MemoryError:
        notifDLG(self, self, 'error',
                 "It seems the system does not have enough memory for this process! "
                 "Maybe try to increase system's virtual memory.", "Out of Memory")
        return False
    compute.release_device_data()   # the GPU copy is now stale
    self.D.ByteOrder = ['b', 'l'][self.D.ByteOrder == 'b']  # swap `l`<->`b`
    self.SettingsWindow.DataInfo.setPlainText(getImportInfo(self))
    if update:
        self.UpdateImages.trigger()
    return True
