from callbacks.appClass import D
from callbacks.allFunctions import prepareData, unloadData, gatherImportOptions, importData, notifDLG
import os


def importCallbacks(self):
    match self.sender():
        case self.ShowImportWdw:
            self.ImportWindow.show()
            # Enter Import Preview Mode
            if self.DetrMode.currentData != "PrvwMod":
                self.DetrMode.setCurrentIndex(self.DetrMode.findData("PrvwMod"))

        case self.ImportWindow.ImportCancelButton:  # Hide window when closing
            self.ImportWindow.hide()
            # return to previous detector mode from Import Preview Mode
            if (self.DetrMode.currentData() == "PrvwMod") and (self.P.DetrMode != ""):
                self.DetrMode.setCurrentIndex(self.DetrMode.findData(self.P.DetrMode))

        case self.ImportWindow.ImportDataButton | self.PreviewButton:  # When the "Import Data" or "Preview" button is pressed
            self.T.Preview = D()
            if not os.path.exists(self.ImportWindow.ImpFilePath.text()):
                notifDLG(self, 'warn', 'The entered file path is invalid!', 'Invalid File!')
            elif self.ImpDataType.Value == "unknown":
                notifDLG(self, 'warn', 'Select the correct data type!', 'Select Data Type!')
            else:
                if self.sender() == self.ImportWindow.ImportDataButton:  # Import data
                    self.ImportWindow.hide()
                    unloadData(self, self.ImpKeepP.Value)
                    self.D = gatherImportOptions(self, self.D, False)
                    self.T.prev_D = self.D  # Backup current `self.D`
                    importData(self)
                else:  # Preview
                    self.T.Preview = gatherImportOptions(self, self.T.Preview, True)

        case self.SettingsWindow.SwapDfrnXY | self.SettingsWindow.SwapRealXY:  # Refresh axes settings etc when dimensions swapped
            prepareData(self)
