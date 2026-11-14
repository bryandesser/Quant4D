from callbacks.allFunctions import enableWindows, plotImage, datasetOptCallbacks, notifDLG
from callbacks.importCallbacks import importCallbacks
import numpy as np
import h5py


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
                    frY = np.ceil(self.PvFrY.maximum() / 2)
                case self.PvTC | self.PvTL | self.PvTR:
                    frY = 1

            match self.sender():
                # Pv*L = Left; Pv*C = Horizontal Center; Pv*R = Right
                case self.PvBR | self.PvCR | self.PvTR:
                    frX = self.PvFrX.maximum()
                case self.PvBC | self.PvCC | self.PvTC:
                    frX = np.ceil(self.PvFrX.maximum() / 2)
                case self.PvBL | self.PvCL | self.PvTL:
                    frX = 1

            self.blockAllSignals = True
            self.PvFrX.setValue(int(frX))
            self.PvFrY.setValue(int(frY))
            self.blockAllSignals = False
            self.PreviewButton.click()  # Preview

        case self.PreviewButton | self.UpdateImages | self.PvFrX | self.PvFrY:
            # Get parameters
            importCallbacks(self)
            d = self.D
            ifx = self.PvFrX.value() - 1  # indices displayed in GUI start at 1; python indices start at 0 -->
            ify = self.PvFrY.value() - 1  # subtract 1 to get to the beginning of the frame of interest

            if d != []:
                dnpx = d.DNPxX
                dnpy = d.DNPxY
                dnfx = d.DNFrX
                dnfy = d.DNFrY
                self.P.PreviewAxLim = np.array([0, dnpx, dnpy, 0]) - 0.5
                self.Fig.Preview.ax.set_xlim(self.P.PreviewAxLim[0:2])
                self.Fig.Preview.ax.set_ylim(self.P.PreviewAxLim[2:])
                try:
                    if not d.h5ds == []:  # Preview HDF5
                        f = h5py.File(d.filePath)
                        if d.h5ds in f:
                            frame = f["datacube"][ify, ifx, :, :]
                        else:
                            return
                    else:  # Preview others
                        skipBytes = d.Offset + (d.FrHead + dnpx * dnpy * d.ByteSize +
                                                d.FrFoot) * (dnfx * ify + ifx) + d.FrHead
                        frame = np.fromfile(
                            file=d.filePath,
                            offset=skipBytes,
                            count=1,
                            dtype=str(
                                dnpx *
                                dnpy) +
                            d.DataType).reshape(
                            dnpx,
                            dnpy)

                    self.Fig.Preview.Image = frame
                    plotImage(self, "Preview")  # Plot image
                    datasetOptCallbacks(self)  # Check NaN
                except BaseException:
                    notifDLG(
                        self,
                        'error',
                        "Errors occurred during preview! Maybe reached end-of-file.",
                        'Error during Preview!')
