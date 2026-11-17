from callbacks.appClass import D
from callbacks.allFunctions import prepareData, unloadData, gatherImportOptions, importData, notifDLG
import os


def importCallbacks(self):
    match self.sender():
        case self.ShowImportWdw:
            self.ImportWindow.show()
            # Enter Import Preview Mode
            if self.DetrMode.currentData() != "PrvwMod":
                self.DetrMode.setCurrentIndex(self.DetrMode.findData("PrvwMod"))

        case self.ImportWindow.ImportCancelButton:  # Hide window when closing
            self.ImportWindow.hide()
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
                    self.ImportWindow.hide()
                    unloadData(self, self.ImportWindow.ImpKeepP.isChecked())
                    self.D = gatherImportOptions(self, False)
                    self.T.prev_D = self.D  # Backup current `self.D`
                    importData(self)
                else:  # Preview
                    self.T.Preview = gatherImportOptions(self, True)

        case self.SettingsWindow.SwapDfrnXY | self.SettingsWindow.SwapRealXY:  # Refresh axes settings etc when dimensions swapped
            prepareData(self)
