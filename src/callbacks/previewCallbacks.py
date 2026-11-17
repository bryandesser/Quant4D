from callbacks.allFunctions import enableWindows, plotImage, notifDLG
from callbacks.utils import checkNaN
from callbacks.importCallbacks import importCallbacks
import numpy as np
import h5py
from callbacks.signals import all_signals_blocked  # noqa: E402
from callbacks.io.raw import open_frames  # noqa: E402


def previewCallbacks(self):
    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    self.Fig.Preview.show()

    match self.sender():
        case self.DetrMode:  # Entering mode
            self.Fig.Preview.ax.cla()
            self.Fig.Preview.Image = None  # Clear previous preview
            self.ImageAx.Preview = None  # clear AxesImage
            enableWindows(self, True)  # Enable windows

        case self.PvBC | self.PvBL | self.PvBR | self.PvCC | self.PvCL | self.PvCR | self.PvTC | self.PvTL | self.PvTR:  # Location buttons
            # set fractional probe position; naming convetion is horrible #TODO
            match self.sender():
                # PvB* = Bottom; PvC* = Vertical Center; PvT* = Top
                case self.PvBC | self.PvBL | self.PvBR:
                    frY = self.PvFrY.maximum()
                case self.PvCC | self.PvCL | self.PvCR:
                    frY = self.PvFrY.maximum() // 2
                case self.PvTC | self.PvTL | self.PvTR:
                    frY = 0

            match self.sender():
                # Pv*L = Left; Pv*C = Horizontal Center; Pv*R = Right
                case self.PvBR | self.PvCR | self.PvTR:
                    frX = self.PvFrX.maximum()
                case self.PvBC | self.PvCC | self.PvTC:
                    frX = self.PvFrX.maximum() // 2
                case self.PvBL | self.PvCL | self.PvTL:
                    frX = 0

            with all_signals_blocked(self):
                self.PvFrX.setValue(int(frX))
                self.PvFrY.setValue(int(frY))
            self.PreviewButton.click()  # Preview

        case self.PreviewButton | self.UpdateImages | self.PvFrX | self.PvFrY:
            # Import options as currently set in the Import window
            importCallbacks(self)
            d = self.T.Preview
            if d is None or not d.filePath:
                return
            ifx = min(self.PvFrX.value(), d.DNFrX - 1)  # frame indices in the GUI are 0-based
            ify = min(self.PvFrY.value(), d.DNFrY - 1)

            self.P.PreviewAxLim = np.array([0, d.DNPxX, d.DNPxY, 0]) - 0.5
            self.Fig.Preview.ax.set_xlim(self.P.PreviewAxLim[0:2])
            self.Fig.Preview.ax.set_ylim(self.P.PreviewAxLim[2:])
            try:
                if d.h5ds:                          # HDF5: through h5py (any layout, chunked or compressed)
                    from callbacks.io.hdf5 import H5Frames
                    with h5py.File(d.filePath, "r") as f:
                        frame = np.asarray(H5Frames(f[d.h5ds])[ify * d.DNFrX + ifx], dtype=float).reshape(d.DNPxY, d.DNPxX)
                else:                              # any file read by offset
                    frames = open_frames(d.filePath, d.Offset, d.DNFrX * d.DNFrY, d.DNPxX * d.DNPxY,
                                         d.DataType, d.FrHead, d.FrFoot, d.ByteOrder)
                    frame = np.asarray(frames[ify * d.DNFrX + ifx], dtype=float).reshape(d.DNPxY, d.DNPxX)
                    del frames
            except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
                notifDLG(self, self, 'error',
                         f"Errors occurred during preview! Maybe reached end-of-file.\n\n{exc}",
                         'Error during Preview!')
                return

            self.Fig.Preview.Image = frame
            plotImage(self, "Preview")  # Plot image
            checkNaN(self, image=frame, preview=True)  # warn about NaN/Inf, which suggest wrong import settings
