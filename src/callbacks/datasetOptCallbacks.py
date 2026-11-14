from callbacks.allFunctions import notifDLG, checkNaN, getImportInfo
from callbacks.importCallbacks import importCallbacks
import numpy as np


def datasetOptCallbacks(self):
    match self.sender():
        case self.SettingsWindow.SwapByteOrder:  # Swap byte-order
            # msg = "Swapping byte order ..." #TODO
            # self.T.progDLG = progDLG(self, sprintf("\n#s\n",msg), "Byte Order Swap") #TODO
            self.progressBar.setMaximum(0)
            try:
                self.Data.byteswap(inplace=True)
            except BaseException:
                notifDLG(
                    self,
                    'error',
                    "It seems the system does not have enough memory for this process! Maybe try to increase system's virtual memory.",
                    "Out of Memory")
                return

            self.D.ByteOrder = ['b', 'l'][self.D.ByteOrder == 'b']  # swap `l`<->`b` at `self.D.ByteOrder`
            self.SettingsWindow.DataInfo.setPlainText(getImportInfo(self))
            self.UpdateImages.tirgger()
            # delete(self.T.progDLG) #TODO
            self.progressBar.setValue(1)
            self.progressBar.setMaximum(1)
            sel = notifDLG(self, 'quest', "Is the current byte-order correct?",
                           'Byte Order Swap', ["Yes", "No. Revert"])

            # Run the process again if selected "No ....."
            if sel.startswith("No"):
                self.SettingsWindow.SwapByteOrder.click()  # datasetOptCallbacks(self,struct('Source',self.SwapByteOrder,'EventName',"")) #TODO?

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
            sel = checkNaN(self, image=self.Image.Preview.get_array(), preview=True)
            if sel == 'Set NaNs to 0':
                self.Data[np.ma.masked_invalid(self.Data).mask] = 0

        case other:
            self.DataInfo.Value = getImportInfo()
            # Check data NaN/Inf, ask whether to sway byte-order
            sel = checkNaN(self, image=self.Image.Dfrn.get_array(), preview=False)
            if sel == 'Set NaNs to 0':
                self.Data[np.ma.masked_invalid(self.Data).mask] = 0


def getImportInfo(self):
    """ Function to update current data info """
    d = self.D
    d0 = self.T.prev_D
    notes = "File: " + d.filePath
    if d.subImg != '':
        notes = notes + "\nSub-dataset: " + d.subImg

    notes += "\n\n# Current Data Info #" +\
        "\nByte Order: " + self.C.EndianTxt[d.ByteOrder] + "\nData Type: " + np.dtype(d.DataType).name + "\nByte Size: " + str(d.ByteSize) + " bytes" +\
        "\n{:s} (X\u2A2FY): {:d}\u2A2F{:d}".format("Diffraction", *d.NPx) +\
        "\n{:s} (X\u2A2FY): {:d}\u2A2F{:d}".format("Real-space", *d.NFr) +\
        "\n\n# Data Structure in File #" +\
        "\nData Offset: " + str(d0.Offset) + " bytes\nFrame Header: " + str(d0.FrHead) + " bytes\nFrame Footer: " + str(d0.FrFoot) + " bytes" +\
        "\nByte Order: " + self.C.EndianTxt[d0.ByteOrder] + "\nData Type: " + np.dtype(d0.DataType).name + "\nByte Size: " + str(d0.ByteSize) + " bytes" +\
        "\n\n# File Meta Info Notes #\n" + d0.NoteFileMeta + '\n' +\
        "\n\n# Import Option Notes #\n" + d0.NoteImp + '\n'

    return notes
