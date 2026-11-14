"""Detector mode and coordinate callbacks."""
import os
import sys
import traceback
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *
from annotationsClasses.interactiveCircle import InteractiveCircle
from annotationsClasses.interactiveAnnulus import InteractiveAnnulus
from annotationsClasses.interactivePoint import InteractivePoint


def clearDetectors(self):

    detectorList = [
        "adf",
        "tb"]

    # Try removing annotations and then setting to None so that they can be replotted later
    for ii in detectorList:
        if getattr(self.A, ii) is not None:
            try:
                getattr(self.A, ii).remove()
            except BaseException:
                pass
            finally:
                setattr(self.A, ii, None)

    # Custom detectors
    # Hide Custom ROIs only
    # set(findobj(self.ImageAx.Dfrn.Children,'-regexp','Tag',"Custom "),'Visible',0) #TODO
    # Scan direction alignment
    # delete(findobj(self.ImageAx.Dfrn,'Tag','ScanDirAnnot')) #TODO


def detectorModeCallbacks(self):
    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    dmod = self.DetrMode.currentData()

    enableWindows(self, False)  # Disable all on change windows
    clearDetectors(self)  # Clear ROIs on Diffraction

    # Clear Real-space images if not switching to alignment or preview
    if dmod not in ["AlignMod", "PrvwMod"]:
        for ii in self.G.RealID:
            if "Mask" not in ii:
                # self.Fig[ii].ax.cla()
                self.Fig[ii].canvas.draw_idle()

    # Enable/Disable CoM/DPC related buttons/images
    for btn in self.G.CoM_btns:
        btn.setEnabled(dmod in ["CoMMod", "DPCMod"])

    # block singals whilst updating DispImage QComboBox
    self.SettingsWindow.DispImage.blockSignals(True)

    if dmod in ["CoMMod", "DPCMod"]:
        # add all images to dropdown list in the Settings Window and
        # Subsitute "CoM"/"DPC" in image names and window titles
        imageNames = [re.sub('DPC|CoM', dmod[:3], ii) for ii in self.G.ImgName]

        self.SettingsWindow.DispImage.clear()
        for itemText, itemID in zip(imageNames, self.G.ImgID):
            self.SettingsWindow.DispImage.addItem(itemText, itemID)  # drop down items
            self.Fig[itemID].setWindowTitle(itemText)  # window title

        # Subsitute "CoM"/"DPC" in button text
        for btn in self.G.CoM_btns:
            re.sub('DPC|CoM', dmod[:3], btn.text())

    else:
        self.SettingsWindow.DispImage.clear()
        for itemText, itemID, itemType in zip(self.G.ImgName, self.G.ImgID, self.G.ImgType):
            if "CoM" not in itemType:
                self.SettingsWindow.DispImage.addItem(itemText, itemID)  # drop down items
            else:
                self.Fig[itemID].hide()  # Image windows

    # Show primary diffraction/real-space image when mode changes unless in Preview mode
    if dmod != "PrvwMod":
        self.Fig.Dfrn.show()
        self.Fig.Real.show()
    else:
        self.Fig.Dfrn.hide()
        self.Fig.Real.hide()

    # Special case for Import Preview Mode
    if dmod == "PrvwMod":
        # Keep only "Preview" image
        self.SettingsWindow.DispImage.clear()
        self.SettingsWindow.DispImage.addItem("Preview", "Preview")

        # Hide other UIs
        self.SettingsWindow.SettingsTabGroup.setTabVisible(
            self.SettingsWindow.SettingsTabGroup.indexOf(
                self.SettingsWindow.MiscTab), False)
        self.SettingsWindow.SettingsTabGroup.setTabVisible(
            self.SettingsWindow.SettingsTabGroup.indexOf(
                self.SettingsWindow.InfoTab), False)
        self.SaveWindow.SaveTabGroup.setTabVisible(
            self.SaveWindow.SaveTabGroup.indexOf(
                self.SaveWindow.ExportTab), False)

        self.Fig.Preview.show()
        self.ImportWindow.show()
        self.SettingsWindow.show()
    else:
        self.P.DetrMode = self.DetrMode.currentData()  # Note current mode
        # Remove "Preview" image from drop down
        self.SettingsWindow.DispImage.removeItem(self.SettingsWindow.DispImage.findData("Preview"))
        self.Fig.Preview.hide()

        # Show all UIs
        self.SettingsWindow.SettingsTabGroup.setTabVisible(
            self.SettingsWindow.SettingsTabGroup.indexOf(
                self.SettingsWindow.MiscTab), True)
        self.SettingsWindow.SettingsTabGroup.setTabVisible(
            self.SettingsWindow.SettingsTabGroup.indexOf(
                self.SettingsWindow.InfoTab), True)
        self.SaveWindow.SaveTabGroup.setTabVisible(
            self.SaveWindow.SaveTabGroup.indexOf(
                self.SaveWindow.ExportTab), True)

    # unblock singals after updating DispImage QComboBox
    self.SettingsWindow.DispImage.blockSignals(False)

    # Define images in the saving list
    self.SaveWindow.SaveImgList.blockSignals(True)
    self.SaveWindow.SaveImgList.clear()
    self.SaveWindow.SaveImgList.addItems([self.SettingsWindow.DispImage.itemData(ii)
                                         for ii in range(self.SettingsWindow.DispImage.count())])
    self.SaveWindow.SaveImgList.blockSignals(False)
    self.SaveWindow.SaveImgPrefix.textChanged.emit(self.SaveWindow.SaveImgPrefix.text())  # Update Image saving prefix
    self.SettingsWindow.ShowDfrnAxes.clicked.emit()  # Update diffraction axis annotations

    # Set detector size when transmitted beam is aligned the first time
    if not (self.P.TransBeamInit) and (dmod != "AlignMod"):
        self.AnnRi.blockSignals(True)
        self.AnnRi.setValue((self.TBR.value(), (self.TBR.value() + self.P.RMax) / 3))
        self.AnnRi.blockSignals(False)
        self.VrApR.setValue(self.TBR.value())
        self.P.VrApXY = self.B0
        self.P.TransBeamInit = 1

    # hide custom mask maths tab
    self.SettingsWindow.SettingsTabGroup.setTabVisible(
        self.SettingsWindow.SettingsTabGroup.indexOf(
            self.SettingsWindow.MathTab), False)

    match dmod:
        case "PrvwMod":
            self.DfrnDetrTabGroup.setCurrentIndex(0)
            previewCallbacks(self)
        case "AlignMod":
            # display the full dataset pacbed
            self.Fig.Dfrn.Image = self.Data.sum(axis=0).reshape(self.D.NPx)
            self.ImageAx.Dfrn = self.Fig.Dfrn.ax.imshow(self.Fig.Dfrn.Image, cmap=self.Fig.Dfrn.cmap)
            self.ImageAx.Dfrn.figure.set_facecolor('black')
            self.Fig.Dfrn.show()
            self.Fig.Dfrn.ax.axis(self.P.DfrnAxLim)
            self.Fig.Dfrn.canvas.draw_idle()

            # initialize real space image with sum over all diffraction space
            self.Fig.Real.Image = self.Data.sum(axis=1).reshape(self.D.NFrY, self.D.NFrX)
            self.ImageAx.Real = self.Fig.Real.ax.imshow(self.Fig.Real.Image, cmap=self.Fig.Real.cmap)
            self.ImageAx.Real.figure.set_facecolor('black')
            self.Fig.Real.show()
            self.Fig.Real.ax.axis(self.P.RealAxLim)
            self.Fig.Real.canvas.draw_idle()

            # initial masking for diffraction space should be all ones
            self.Fig.DfrnMask.Image = np.ones(self.D.NPx)
            self.ImageAx.DfrnMask = self.Fig.DfrnMask.ax.imshow(self.Fig.DfrnMask.Image, cmap=self.Fig.DfrnMask.cmap)
            self.ImageAx.DfrnMask.figure.set_facecolor('black')
            self.Fig.DfrnMask.ax.axis(self.P.DfrnAxLim)
            self.Fig.DfrnMask.canvas.draw_idle()

            # initial masking for real space should be all ones
            self.Fig.RealMask.Image = np.ones(self.D.NFr)
            self.ImageAx.RealMask = self.Fig.RealMask.ax.imshow(self.Fig.RealMask.Image, cmap=self.Fig.RealMask.cmap)
            self.ImageAx.RealMask.figure.set_facecolor('black')
            self.Fig.RealMask.ax.axis(self.P.RealAxLim)
            self.Fig.RealMask.canvas.draw_idle()

            # Create transmitted beam annotation, allow for disk as large as the entire diffraction pattern
            if self.A.tb is None:
                self.A.tb = InteractiveCircle(
                    center=self.B0,
                    radius=self.TBR.value(),
                    axis=self.Fig.Dfrn.ax,
                    color="r",
                    interactions="all")
                self.A.tb.connect()
                self.A.tb.updateCircle.connect(lambda: moveTransBeam(self))
                self.Fig.Dfrn.canvas.flush_events()

            self.DfrnDetrTabGroup.setCurrentIndex(1)
            transBeamCallbacks(self)

        case "AnnMod":
            self.DfrnDetrTabGroup.setCurrentIndex(2)
            self.dpcControls.setVisible(False)
            self.comControls.setVisible(False)
            annularDetectorCallbacks(self)  # TODO
        case "CoMMod" | "DPCMod":
            self.DfrnDetrTabGroup.setCurrentIndex(2)
            self.dpcControls.setVisible("DPC" in dmod)
            self.comControls.setVisible(True)
            annularDetectorCallbacks(self)  # TODO
            plotImage(self, 'ColorWheel')  # Plot ColorWheel #TODO
            self.Fig.CoMPhMag.activateWindow()
            self.Fig.ColorWheel.activateWindow()
            if not self.P.ScanDirInit:
                pass  # flashBackground(self, self.ScanDirGrid) # Flashing to align scan direction #TODO
        case "VrApMod":  # 'Virtual Aperture'
            self.DfrnDetrTabGroup.setCurrentIndex(3)
            virtualApertureCallbacks(self)
        case "CustMod":
            self.DfrnDetrTabGroup.setCurrentIndex(4)
            self.SettingsWindow.SettingsTabGroup.setTabVisible(
                self.SettingsWindow.SettingsTabGroup.indexOf(
                    self.SettingsWindow.MathTab), True)
            # customDetectorCallbacks(self) #TODO
            self.Fig.DfrnMask.activateWindow()

    enableWindows(self, True)


def detrCoordCallbacks(self):
    # "Polar" and "Absolute" are mutually exclusive
    match self.sender():
        case self.SettingsWindow.DCSys:
            if self.SettingsWindow.DCSys.currentText() == "Polar":
                self.SettingsWindow.DCPos.setCurrentIndex(self.SettingsWindow.DCPos.findText("Relative"))
        case self.SettingsWindow.DCPos:
            if self.SettingsWindow.DCPos.currentText() == "Absolute":
                self.SettingsWindow.DCSys.setCurrentIndex(self.SettingsWindow.DCSys.findText("Cartesian"))
        case self.SettingsWindow.DCUnit:
            pass

    # Update coordinate conversion related convenient global properties
    self.DfPxR = 1
    self.RB0 = [0, 0]

    if self.SettingsWindow.DCUnit.currentText() == "mrad":
        self.DfPxR = self.mradPx.value()
    if self.SettingsWindow.DCPos.currentText() == "Relative":
        self.RB0 = self.B0

    # Update UI
    match self.DetrMode.currentData():
        case "AlignMod":
            pass
        case "AnnMod" | "DPCMod" | "CoMMod":
            self.SettingsWindow.DCSys.currentIndexChanged.emit(self.SettingsWindow.DCSys.currentIndex())
        case "VrApMod":
            self.SettingsWindow.DCSys.currentIndexChanged.emit(self.SettingsWindow.DCSys.currentIndex())
        case "CustMod":
            self.SettingsWindow.DCSys.currentIndexChanged.emit(self.SettingsWindow.DCSys.currentIndex())


def customDetectorCallbacks(self):
    pass
