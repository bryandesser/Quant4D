from .appClass import D
from .import_io import gatherImportOptions, importBoxInput, importData, unloadData
from .io.file_reader import prepareData
from .menus import showPreviewDisplayControls
from .utils import notifDLG
import os


def importCallbacks(self):
    match self.sender():
        case self.ShowImportWdw:
            self.ImportWindow.show()
            # Swap Dataset is possible only with a dataset loaded and a file of its size: check now
            # (it was only checked once a file was picked, so the box could stay ticked and disabled)
            iw = self.ImportWindow
            if self.D is None or self.Data is None:
                iw.ImpKeepP.setChecked(False)
                iw.ImpKeepP.setEnabled(False)
            elif os.path.isfile(iw.ImpFilePath.text()):
                importBoxInput(self, None)
            # Enter Import Preview Mode
            if self.DetrMode.currentData() != "PrvwMod":
                self.DetrMode.setCurrentIndex(self.DetrMode.findData("PrvwMod"))
            else:                       # already in it (e.g. at startup): no mode change to show the controls
                showPreviewDisplayControls(self)

        case self.ImportWindow.ImportCancelButton:  # Hide window when closing
            self.ImportWindow.hide()
            self.ImportWindow.ImpKeepP.setChecked(False)      # a cancelled swap is not remembered
            # return to previous detector mode from Import Preview Mode
            if (self.DetrMode.currentData() == "PrvwMod") and (self.P.DetrMode != ""):
                self.DetrMode.setCurrentIndex(self.DetrMode.findData(self.P.DetrMode))

        case self.ImportWindow.ImportDataButton | self.PreviewButton:  # When the "Import Data" or "Preview" button is pressed
            self.T.Preview = D()
            if not os.path.exists(self.ImportWindow.ImpFilePath.text()):
                notifDLG(self, self.ImportWindow, 'warn', 'The entered file path is invalid!', 'Invalid File!')
            elif self.ImportWindow.ImpDataType.currentData() == "unknown":
                notifDLG(self, self.ImportWindow, 'warn', 'Select the correct data type!', 'Select Data Type!')
            else:
                if self.sender() == self.ImportWindow.ImportDataButton:  # Import data
                    in_memory = self.ImportWindow.ImpMemType.currentIndex() == 0
                    if in_memory and (self.T.EstMem or 0) > self.C.MemTot:
                        sel = notifDLG(self, self.ImportWindow, 'quest',
                                       f"The dataset needs about {self.T.EstMem / 1024**3:.1f} GiB, more than this "
                                       f"computer's {self.C.MemTot / 1024**3:.1f} GiB of memory. Consider a partial "
                                       "(cropped, binned or sampled) import.", 'Size Exceeds System Memory!',
                                       ["Import anyway", "Cancel"])
                        if not str(sel or "").startswith("Import"):
                            return
                    self.ImportWindow.hide()
                    unloadData(self, self.ImportWindow.ImpKeepP.isChecked())
                    self.D = gatherImportOptions(self, False)
                    self.T.prev_D = self.D  # Backup current `self.D`
                    importData(self)
                else:  # Preview
                    self.T.Preview = gatherImportOptions(self, True)

        case self.SettingsWindow.SwapDfrnXY | self.SettingsWindow.SwapRealXY:  # Refresh axes settings etc when dimensions swapped
            prepareData(self, keep_beam=self.sender() is self.SettingsWindow.SwapRealXY)
