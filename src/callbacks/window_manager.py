"""Window show/hide/toggle callbacks."""
import os
import sys
import traceback
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *


def toggleWindows(self):
    print(self.sender())
    match self.sender():
        case self.Fig.Dfrn:
            print(999)


def showAllWindows(self):
    for ii in self.Fig:
        self.Fig[ii].show()
    self.actionShow_All_Windows.setChecked(True)
    self.actionHide_All_Windows.setChecked(False)
    self.activateWindow()


def hideAllWindows(self):
    for ii in self.Fig:
        self.Fig[ii].hide()
    self.actionShow_All_Windows.setChecked(False)
    self.actionHide_All_Windows.setChecked(True)
    self.activateWindow()


def unHideOpenWindows(self):
    # figure out which windows should be re-shown after a hideAll event
    for action in self.menuDiffraction.actions() + self.menuReal_Space.actions() + self.menuCenter_of_Mass.actions():
        if not action.isSeparator() and action.isChecked():
            action.trigger()
            action.trigger()


def on_ShowImportWdw_triggered(self):
    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    self.ShowImportWdw.setChecked(not self.ImportWindow.isVisible())
    self.ImportWindow.show(self.ShowImportWdw.isChecked())

    if self.ShowImportWdw.isChecked():
        hideAllWindows(self)
        self.ImportWindow.activateWindow()
    else:
        unHideOpenWindows(self)


def showWindowCallbacks(self):
    id = self.SettingsWindow.DispImage.currentData()
    match self.sender():
        case self.SettingsWindow.ShowImageWdw:  # Show selected image
            self.Fig[id].show()
            self.Fig[id].activateWindow()
        case self.SettingsWindow.ShowMaskWdw:  # Show diffraction or Real `space` mask for the selected image
            id = self.Fig[id].space + "Mask"
            self.Fig[id].show()
            self.Fig[id].activateWindow()
        case other:  # All other `self.Show***Wdw` buttons
            id = self.sender().accessibleName()
            if id in self.G.ImgID:
                self.Fig[id].show()
                self.Fig[id].activateWindow()
                # If `id` is one of the available images, select it
                if (not self.SettingsWindow.DispLock.isChecked()) and (self.SettingsWindow.DispImage.currentData()
                                                                       != id) and (self.SettingsWindow.DispImage.findData(id) != -1):
                    self.SettingsWindow.DispImage.setCurrentIndex(self.SettingsWindow.DispImage.findData(id))

# Function to import mask for given (diffraction/real) space


def resizeWindowCallbacks(self):
    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    # set the space: `Dfrn` or `Real`; get updated height and width, add mpl decor size
    if self.sender() in [
            self.SettingsWindow.WdwWDfrn,
            self.SettingsWindow.WdwHDfrn,
            self.SettingsWindow.WdwSetDfrn,
            self.SettingsWindow.WdwSetAllDfrn]:
        space = "Dfrn"
        width = self.SettingsWindow.WdwWDfrn.value() + self.C.mplDecor.width()
        height = self.SettingsWindow.WdwHDfrn.value() + self.C.mplDecor.height()
    else:
        space = "Real"
        width = self.SettingsWindow.WdwWReal.value() + self.C.mplDecor.width()
        height = self.SettingsWindow.WdwHReal.value() + self.C.mplDecor.height()

    match self.sender():
        case self.SettingsWindow.WdwSetDfrn | self.SettingsWindow.WdwSetReal:  # Set size for just one image window
            id = self.SettingsWindow.DispImage.currentData()  # Default image window to resize

            # If the selected image is not of that space, then resize that space's primary image window instead
            if self.Fig[id].space != space:
                id = space

            # temporarily block slots/signals to avoid recursion
            self.Fig[id].blockSignals(True)

            # set the height and wdith
            self.Fig[id].resize(width, height)

            # unblock slots/signals
            self.Fig[id].blockSignals(False)

        case self.SettingsWindow.WdwSetAllDfrn | self.SettingsWindow.WdwSetAllReal:  # Set all image windows of the given space to the same size
            for fig in self.G.ImgFig:
                if fig.space == space:
                    fig.blockSignals(True)
                    fig.resize(width, height)
                    fig.blockSignals(False)
