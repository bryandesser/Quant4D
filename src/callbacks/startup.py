"""App startup, slot/signal wiring, window enable, layout helpers."""
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
from multiprocessing.pool import ThreadPool
# Deferred cross-module imports (safe: startup is itself only loaded lazily)
from callbacks.plotting import displayCallbacks  # noqa: E402
from callbacks.detector import detectorModeCallbacks  # noqa: E402
from callbacks.annularDetectorCallbacks import annularDetectorCallbacks  # noqa: E402


def unlockScanDir(self):
    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    if self.ScanDirUnlock.isChecked():
        self.ScanDirUnlock.setIcon(self.unlock)
    else:
        self.ScanDirUnlock.setIcon(self.lock)


def debugImport(self):
    self.fname = 'C:/Users/bess0001/Documents/dataStorage/research/code/testData/scan_x128_y128.raw'
    if os.path.exists(self.fname):
        self.ImportWindow.ImpFilePath.setText(self.fname)
        self.ShowImportWdw.trigger()
        for widget in self.ImportWindow.children():
            widget.setEnabled(True)
        importSelectFile(self)
        self.ImportWindow.ImportDataButton.click()


def slotsSignals(self):
    # debug
    self.enableAllUIs.triggered.connect(lambda: enableWindows(self, True))
    self.debugImport.triggered.connect(lambda: debugImport(self))
    self.breakpoint.triggered.connect(lambda: breakpoint(self))

    # resize window callabcks
    self.SettingsWindow.WdwSetDfrn.clicked.connect(lambda: resizeWindowCallbacks(self))
    self.SettingsWindow.WdwSetAllDfrn.clicked.connect(lambda: resizeWindowCallbacks(self))
    self.SettingsWindow.WdwSetReal.clicked.connect(lambda: resizeWindowCallbacks(self))
    self.SettingsWindow.WdwSetAllReal.clicked.connect(lambda: resizeWindowCallbacks(self))

    # change lock/unlock icon when clicked
    self.ScanDirUnlock.clicked.connect(lambda: unlockScanDir(self))

    # Import window slots/signals
    self.ShowImportWdw.triggered.connect(lambda: importCallbacks(self))
    self.ImportWindow.ImportCancelButton.clicked.connect(lambda: importCallbacks(self))
    self.ImportWindow.xEvent.connect(lambda: self.ShowImportWdw.setChecked(False)
                                     )  # ImportWindow.ImportCancelButton.click())
    self.ImportWindow.ImpFileSelect.clicked.connect(lambda: importSelectFile(self))
    self.ImportWindow.ImportDataButton.clicked.connect(lambda: importCallbacks(self))
    self.ImportWindow.ImpKeepP.clicked.connect(lambda: importBoxInput(self))
    self.ImportWindow.ImpGPU.currentIndexChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.ImpFrPart.clicked.connect(lambda: importBoxInput(self))
    self.ImportWindow.ImpPxPart.clicked.connect(lambda: importBoxInput(self))
    self.ImportWindow.IFrD.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.IFrY1.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.INFrX.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.IFrX1.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.INFrY.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.IPxD.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.INPxY.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.IPxY1.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.INPxX.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.IPxX1.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.DNFrY.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.DNFrX.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.DNPxY.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.DNPxX.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.ImpByteOrder.currentIndexChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.ImpDataType.currentIndexChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.DataOffset.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.FrFoot.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.FrHead.valueChanged.connect(lambda: importBoxInput(self))
    self.ImportWindow.ImpSubImg.currentIndexChanged.connect(lambda: importFileType(self))

    # save window slots/signals
    self.SaveWindow.SaveImgSelectAll.clicked.connect(
        lambda isChecked: self.SaveWindow.SaveImgList.selectAll() if isChecked else self.SaveWindow.SaveImgList.clearSelection())

    # menu action slots/signals
    self.actionShow_Diffraction_Pattern.triggered.connect(
        lambda: self.Fig.Dfrn.show(
            self.actionShow_Diffraction_Pattern.isChecked()))
    self.actionShow_Diffraction_Mask.triggered.connect(
        lambda: self.Fig.DfrnMask.show(
            self.actionShow_Diffraction_Mask.isChecked()))
    self.actionShow_Real_Space_Image.triggered.connect(
        lambda: self.Fig.Real.show(
            self.actionShow_Real_Space_Image.isChecked()))
    self.actionShow_Real_Space_Mask.triggered.connect(
        lambda: self.Fig.RealMask.show(
            self.actionShow_Real_Space_Mask.isChecked()))
    self.actionShow_Center_of_Mass_Magnitude_CoM.triggered.connect(
        lambda: self.Fig.CoMMag.show(self.actionShow_Center_of_Mass_Magnitude_CoM.isChecked()))
    self.actionShow_Center_of_Mass_X.triggered.connect(
        lambda: self.Fig.CoMX.show(
            self.actionShow_Center_of_Mass_X.isChecked()))
    self.actionShow_Center_of_Mass_Y.triggered.connect(
        lambda: self.Fig.CoMY.show(
            self.actionShow_Center_of_Mass_Y.isChecked()))
    self.actionShow_Colorwheel.triggered.connect(
        lambda: self.Fig.ColorWheel.show(
            self.actionShow_Colorwheel.isChecked()))
    self.actionShow_Differential_Center_of_Mass_dCoM.triggered.connect(
        lambda: self.Fig.dCoM.show(self.actionShow_Differential_Center_of_Mass_dCoM.isChecked()))
    self.actionShow_Integrated_Center_of_Mass_iCoM.triggered.connect(
        lambda: self.Fig.iCoM.show(self.actionShow_Integrated_Center_of_Mass_iCoM.isChecked()))
    self.actionShow_Phase_Magnitude.triggered.connect(
        lambda: self.Fig.CoMPhMag.show(
            self.actionShow_Phase_Magnitude.isChecked()))
    self.actionShow_Phase_Vector_Image.triggered.connect(
        lambda: self.Fig.CoMPh.show(
            self.actionShow_Phase_Vector_Image.isChecked()))
    self.actionShow_All_Windows.triggered.connect(lambda: showAllWindows(self))
    self.actionHide_All_Windows.triggered.connect(lambda: hideAllWindows(self))
    self.ShowSettingsWdw.triggered.connect(lambda: self.SettingsWindow.show())
    self.ShowSettingsWdw.triggered.connect(lambda: self.SettingsWindow.activateWindow())
    self.ShowSaveWdw.triggered.connect(lambda: self.SaveWindow.show())
    self.ShowSaveWdw.triggered.connect(lambda: self.SaveWindow.activateWindow())

    self.DetrMode.currentIndexChanged.connect(lambda: detectorModeCallbacks(self))

    # dataset options (i.e. swap Rxy, swap Kxy, and swap endianness)
    self.SettingsWindow.SwapDfrnXY.clicked.connect(lambda: datasetOptCallbacks(self))
    self.SettingsWindow.SwapRealXY.clicked.connect(lambda: datasetOptCallbacks(self))
    self.SettingsWindow.SwapByteOrder.clicked.connect(lambda: datasetOptCallbacks(self))

    # show window buttons
    self.SettingsWindow.ShowDfrnWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowRealMaskWdw_2.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowColorWheelWdw_2.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowDfrnMaskWdw_2.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowCoMMagWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowCoMPhWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowCoMPhMagWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowRealWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowCoMXWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowCoMYWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowdCoMWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowiCoMWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowImageWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.SettingsWindow.ShowMaskWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.ShowRealMaskWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.ShowDfrnMaskWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.ShowColorWheelWdw.clicked.connect(lambda: showWindowCallbacks(self))

    # transmitted beam controls
    self.TBX.valueChanged.connect(lambda: moveTransBeam(self))
    self.TBY.valueChanged.connect(lambda: moveTransBeam(self))
    self.TBR.valueChanged.connect(lambda: moveTransBeam(self))
    self.Alpha.valueChanged.connect(lambda: moveTransBeam(self))
    self.mradPx.valueChanged.connect(lambda: moveTransBeam(self))
    self.TBX_NF.valueChanged.connect(lambda: moveTransBeam(self))
    self.TBY_NF.valueChanged.connect(lambda: moveTransBeam(self))
    self.TBR_NF.valueChanged.connect(lambda: moveTransBeam(self))
    self.TBAutoAlign.clicked.connect(lambda: transBeamCallbacks(self))
    self.TBCrossAlign.clicked.connect(lambda: transBeamCallbacks(self))

    # Math formula (CustMod)
    self.SettingsWindow.MathEval.clicked.connect(lambda: mathCallbacks(self))

    # preview tab on main UI
    self.PvBL.clicked.connect(lambda: previewCallbacks(self))
    self.PvBC.clicked.connect(lambda: previewCallbacks(self))
    self.PvBR.clicked.connect(lambda: previewCallbacks(self))
    self.PvCL.clicked.connect(lambda: previewCallbacks(self))
    self.PvCC.clicked.connect(lambda: previewCallbacks(self))
    self.PvCR.clicked.connect(lambda: previewCallbacks(self))
    self.PvTL.clicked.connect(lambda: previewCallbacks(self))
    self.PvTC.clicked.connect(lambda: previewCallbacks(self))
    self.PvTR.clicked.connect(lambda: previewCallbacks(self))
    self.PreviewButton.clicked.connect(lambda: previewCallbacks(self))
    self.PvFrX.valueChanged.connect(lambda: previewCallbacks(self))
    self.PvFrY.valueChanged.connect(lambda: previewCallbacks(self))

    # displayCallbacks
    self.UpdateImages.triggered.connect(lambda: updateImagesCallbacks(self))
    self.DispVecColor.triggered.connect(lambda: displayCallbacks(self))
    self.DispVecField.currentIndexChanged.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.DispCMap.currentIndexChanged.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.DispCMapInvert.clicked.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.DispImage.currentIndexChanged.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.DispLock.clicked.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.DispBrightness.valueChanged.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.DispContrast.valueChanged.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.DispGamma.setSingleStep(0.1 / 3)  # scroll step = 3 single steps
    self.SettingsWindow.DispGamma.setValue(1)
    self.SettingsWindow.DispGamma.valueChanged.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.DispGammaReset.triggered.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.DispContrastReset.triggered.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.DispBrightnessReset.triggered.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.DispMaskOpa.valueChanged.connect(lambda: displayCallbacks(self))
    self.SettingsWindow.HistLog.clicked.connect(lambda: displayCallbacks(self))

    # reset values, should not be necessary once connected to displayCallbacks #TODO
    self.SettingsWindow.DispBrightnessReset.clicked.connect(lambda: self.SettingsWindow.DispBrightness.setValue(50))
    self.SettingsWindow.DispContrastReset.clicked.connect(lambda: self.SettingsWindow.DispContrast.setValue(50))
    self.SettingsWindow.DispGammaReset.clicked.connect(lambda: self.SettingsWindow.DispGamma.setValue(1))

    # detector slider/numerical field connections
    self.AnnRi.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.AnnRi_NF.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.AnnRo_NF.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.NSeg.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.DetRot_NF.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.DetRot.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.ScanDirUnlock.clicked.connect(lambda: annularDetectorCallbacks(self))
    self.ScanDirYFlip.clicked.connect(lambda: annularDetectorCallbacks(self))
    self.ScanDir_NF.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.ScanDir.valueChanged.connect(lambda: annularDetectorCallbacks(self))

    # virtual aperture connections
    self.VrApR.valueChanged.connect(lambda: virtualApertureCallbacks(self))
    self.VrApSymm.currentIndexChanged.connect(lambda: virtualApertureCallbacks(self))
    self.VrApInvert.clicked.connect(lambda: virtualApertureCallbacks(self))
    self.VrApMirror.clicked.connect(lambda: virtualApertureCallbacks(self))
    self.VrApMirrRot.valueChanged.connect(lambda: virtualApertureCallbacks(self))
    self.VrApMirrRot_NF.valueChanged.connect(lambda: virtualApertureCallbacks(self))

    # Settings window, units choices
    self.SettingsWindow.DCSys.currentIndexChanged.connect(lambda: detrCoordCallbacks(self))
    self.SettingsWindow.DCPos.currentIndexChanged.connect(lambda: detrCoordCallbacks(self))
    self.SettingsWindow.DCUnit.currentIndexChanged.connect(lambda: detrCoordCallbacks(self))
    self.RealROIShape.currentIndexChanged.connect(lambda: realSpaceROICallbacks(self))


def startupFcn(self):
    from callbacks.guiClass import ImageWindow, SettingsWindow, SaveWindow, ImportWindow

    def getGPU(self):
        self.ImportWindow.ImpGPU.clear()
        self.C.nGPU = 0
        self.C.GPUmem = []
        self.C.GPUname = []

        # Check if CUDA capable GPU is available for acceleration
        self.C.nGPU = torch.cuda.device_count()

        # Find GPU devices and turn on/off GPU support;
        # self.ImportWindow.ImgGPU.currentData() = None is always "GPU off"
        if self.C.nGPU == 0:  # no GPU devices
            self.ImportWindow.ImpGPU.addItem('No GPU found.', 0)
        else:  # 1 or more devices found
            maxmem = 0
            for i in np.arange(0, self.C.nGPU):
                self.C.GPUmem.append(torch.cuda.get_device_properties(i).total_memory)
                self.C.GPUname.append(torch.cuda.get_device_name(i))
                self.ImportWindow.ImpGPU.addItem(self.C.GPUname[i], i)
                # Select GPU with max memory
                if self.C.GPUmem[i] > maxmem:
                    maxmem = self.C.GPUmem[i]
                    self.ImportWindow.ImpGPU.setCurrentIndex(i)
            self.ImportWindow.ImpGPU.addItem('GPU off', None)

    # Function to Check usable system memory and make sure the file will fit
    def getMem(self):
        mem = psutil.virtual_memory()
        self.C.MemTot = mem.total
        self.C.MemFree = mem.available

    # Function to get pixels in each monitor
    def checkMonitors(self):
        self.C.ScreenSize = qtw.QDesktopWidget().availableGeometry().getRect()
        for i in range(qtw.QDesktopWidget().screenCount()):
            self.C.MonitorPositions.append(qtw.QDesktopWidget().screenGeometry(i).getRect())

        # monitor size
        self.C.monitorWidth = qtw.QApplication.desktop().screenGeometry().width()
        self.C.monitorHeight = qtw.QApplication.desktop().screenGeometry().height()

        # toolbar size + any horizontal or vertical offsets due to toolbar
        self.C.hOffset, self.C.vOffset, self.C.toolbarWidth, self.C.toolbarHeight = abs(np.array(
            qtw.QApplication.desktop().screenGeometry().getRect()) - np.array(qtw.QApplication.desktop().availableGeometry().getRect()))

        # establish window decoration sizes with temporary image window
        tmp = ImageWindow("", "", "", "", "", [0, 0, 400, 400])
        self.C.decorPad, self.C.titleHeight = [tmp.geometry().x() - tmp.pos().x(), tmp.geometry().y() - tmp.pos().y()]
        if [self.C.decorPad, self.C.titleHeight] == [0, 0]:  # TODO
            self.C.decorPad = 5
            self.C.titleHeight = 25
        self.C.mplDecor = tmp.size() - qtc.QSize(400, 400)
        tmp.close()

        # available monitor space
        self.C.monitorAvailWidth = self.C.monitorWidth - self.C.toolbarWidth
        self.C.monitorAvailHeight = self.C.monitorHeight - self.C.toolbarHeight

        # current monitor dpi
        self.C.dpi = self.screen().physicalDotsPerInch()

        # window positioning
        self.C.sz = int(
            np.floor(
                np.minimum(
                    self.C.monitorAvailWidth -
                    4 *
                    self.C.decorPad -
                    2 *
                    self.C.mplDecor.width(),
                    self.C.monitorAvailHeight -
                    2 *
                    self.C.titleHeight -
                    2 *
                    self.C.decorPad -
                    2 *
                    self.C.mplDecor.height())) /
            2)
        self.C.shc = self.C.monitorAvailWidth / 2
        self.C.left = self.C.monitorAvailWidth - self.C.sz + self.C.hOffset - self.C.mplDecor.width()
        self.C.wb0 = self.C.monitorAvailHeight - self.C.sz + self.C.vOffset

        # Set limits/values for image window resize options
        self.SettingsWindow.WdwWDfrn.setRange(1, self.C.monitorAvailWidth)
        self.SettingsWindow.WdwHDfrn.setRange(1, self.C.monitorAvailHeight)
        self.SettingsWindow.WdwWReal.setRange(1, self.C.monitorAvailWidth)
        self.SettingsWindow.WdwHReal.setRange(1, self.C.monitorAvailHeight)
        self.SettingsWindow.WdwWDfrn.setValue(self.C.sz)
        self.SettingsWindow.WdwHDfrn.setValue(self.C.sz)
        self.SettingsWindow.WdwWReal.setValue(self.C.sz)
        self.SettingsWindow.WdwHReal.setValue(self.C.sz)

    def createImageWindows(self):
        # create figure windows
        self.Fig.Dfrn = ImageWindow("Dfrn",
                                    "Diffraction",
                                    "Dfrn",
                                    "Primary",
                                    "gray",
                                    [self.C.shc - self.C.sz / 2,
                                     self.C.decorPad + self.C.titleHeight + self.C.vOffset,
                                     self.C.sz + self.C.mplDecor.width(),
                                     self.C.sz + self.C.mplDecor.height()])  # Top-center
        self.Fig.DfrnMask = ImageWindow("DfrnMask",
                                        "Diffraction Mask",
                                        "Dfrn",
                                        "Mask",
                                        "gray",
                                        [self.C.shc - self.C.sz / 2,
                                         self.C.sz + 2 * (self.C.decorPad + self.C.titleHeight) + self.C.mplDecor.height() + self.C.vOffset,
                                            self.C.sz + self.C.mplDecor.width(),
                                            self.C.sz + self.C.mplDecor.height()])  # right of Top-center
        self.Fig.iCoM = ImageWindow("iCoM",
                                    "iCoM",
                                    "Real",
                                    "CoM",
                                    "gray",
                                    [self.C.left,
                                     self.C.decorPad + self.C.titleHeight + self.C.vOffset,
                                     self.C.sz + self.C.mplDecor.width(),
                                     self.C.sz + self.C.mplDecor.height()])
        self.Fig.dCoM = ImageWindow("dCoM",
                                    "dCoM",
                                    "Real",
                                    "CoM",
                                    "gray",
                                    [self.C.left,
                                     2 * (self.C.decorPad + self.C.titleHeight) + self.C.vOffset,
                                        self.C.sz + self.C.mplDecor.width(),
                                        self.C.sz + self.C.mplDecor.height()])
        self.Fig.CoMY = ImageWindow("CoMY",
                                    "CoM Y",
                                    "Real",
                                    "CoM",
                                    "gray",
                                    [self.C.left,
                                     3 * (self.C.decorPad + self.C.titleHeight) + self.C.vOffset,
                                        self.C.sz + self.C.mplDecor.width(),
                                        self.C.sz + self.C.mplDecor.height()])
        self.Fig.CoMX = ImageWindow("CoMX",
                                    "CoM X",
                                    "Real",
                                    "CoM",
                                    "gray",
                                    [self.C.left,
                                     4 * (self.C.decorPad + self.C.titleHeight) + self.C.vOffset,
                                        self.C.sz + self.C.mplDecor.width(),
                                        self.C.sz + self.C.mplDecor.height()])
        self.Fig.CoMMag = ImageWindow("CoMMag",
                                      "CoM Magnitude",
                                      "Real",
                                      "CoM",
                                      "gray",
                                      [self.C.left,
                                       5 * (self.C.decorPad + self.C.titleHeight) + self.C.vOffset,
                                          self.C.sz + self.C.mplDecor.width(),
                                          self.C.sz + self.C.mplDecor.height()])
        self.Fig.CoMPh = ImageWindow("CoMPh",
                                     "CoM Phase",
                                     "Real",
                                     "CoM",
                                     "hsv",
                                     [self.C.left,
                                      6 * (self.C.decorPad + self.C.titleHeight) + self.C.vOffset,
                                         self.C.sz + self.C.mplDecor.width(),
                                         self.C.sz + self.C.mplDecor.height()])
        self.Fig.CoMPhMag = ImageWindow("CoMPhMag",
                                        "CoM Phase (Magnitude-shaded)",
                                        "Real",
                                        "CoM",
                                        "hsv",
                                        [self.C.left,
                                         7 * (self.C.decorPad + self.C.titleHeight) + self.C.vOffset,
                                            self.C.sz + self.C.mplDecor.width(),
                                            self.C.sz + self.C.mplDecor.height()])
        self.Fig.RealMask = ImageWindow("RealMask",
                                        "Real-space Mask",
                                        "Real",
                                        "Mask",
                                        "gray",
                                        [self.C.left,
                                         8 * (self.C.decorPad + self.C.titleHeight) + self.C.vOffset,
                                            self.C.sz + self.C.mplDecor.width(),
                                            self.C.sz + self.C.mplDecor.height()])
        self.Fig.Real = ImageWindow("Real",
                                    "Real-space",
                                    "Real",
                                    "Primary",
                                    "gray",
                                    [self.C.left,
                                     9 * (self.C.decorPad + self.C.titleHeight) + self.C.vOffset,
                                        self.C.sz + self.C.mplDecor.width(),
                                        self.C.sz + self.C.mplDecor.height()])
        self.Fig.Preview = ImageWindow("Preview",
                                       "Preview",
                                       "Preview",
                                       "Preview",
                                       "gray",
                                       [self.C.left,
                                        (self.C.ScreenSize[3] - self.C.sz) / 2,
                                           self.C.sz + self.C.mplDecor.width(),
                                           self.C.sz + self.C.mplDecor.height()])
        self.Fig.ColorWheel = ImageWindow(
            id="ColorWheel",
            name="Color Wheel for Phase Direction",
            space="ColorWheel",
            typ="CoM",
            cmap="hsv",
            pos=[
                self.C.shc -
                self.C.sz -
                self.C.mplDecor.width(),
                self.C.sz +
                2 *
                (
                    self.C.decorPad +
                    self.C.titleHeight) +
                self.C.mplDecor.height() +
                self.C.vOffset,
                self.C.sz /
                2 +
                self.C.mplDecor.width(),
                self.C.sz /
                2 +
                self.C.mplDecor.height()])

        # AND their Axes/Figure objects, as well as the gray overlay to disable them
        self.G.ImgAx = [self.Fig[ii].ax for ii in self.Fig]
        self.G.ImgFig = [self.Fig[ii] for ii in self.Fig]

        # connect image resizeEvent signal to slot; updates window size numerical fields in SettingsWindow
        for fig in self.G.ImgFig:
            fig.imageResize.connect(lambda size, space: updateImageWindowSize(self, size, space))
            fig.activateFigure.connect(lambda id: updateDispImg(self, id))

        # Axes objects for all diffraction-sized figures/axes/images
        self.G.DfrnAx = [self.Fig[ii].ax for ii in self.G.DfrnID]

        # Axes objects for all real-space-sized figures/axes/images
        self.G.RealAx = [self.Fig[ii].ax for ii in self.G.RealID]

        # Group all "Show ... Window" buttons related to CoM/DPC
        self.G.CoM_btns = [
            obj for obj in self.SettingsWindow.findChildren(
                qtw.QPushButton) if "CoM" in obj.objectName()]
        self.G.CoM_btns.extend([self.ShowColorWheelWdw, self.SettingsWindow.ShowColorWheelWdw_2])

        # Group all window `figure` `uifigure`
        self.G.AllFig = self.G.ImgFig.copy()
        self.G.AllFig.extend([self, self.SettingsWindow, self.ImportWindow, self.SaveWindow])

    def updateImageWindowSize(self, size, space):
        match space:
            case "Dfrn":
                self.SettingsWindow.WdwHDfrn.setValue(self.SettingsWindow.WdwHDfrn.value() + size.height())
                self.SettingsWindow.WdwWDfrn.setValue(self.SettingsWindow.WdwWDfrn.value() + size.width())
            case "Real":
                self.SettingsWindow.WdwHReal.setValue(self.SettingsWindow.WdwHReal.value() + size.height())
                self.SettingsWindow.WdwWReal.setValue(self.SettingsWindow.WdwWReal.value() + size.width())

    def updateDispImg(self, id):
        self.SettingsWindow.DispImage.setCurrentIndex(self.SettingsWindow.DispImage.findData(id))

    def populateDropdowns(self):
        """ populates GUI dropdowns with itemText and itemData where necessary """

        # import window, byte order
        self.ImportWindow.ImpByteOrder.clear()
        self.ImportWindow.ImpByteOrder.addItem("Little Endian", 'l')
        self.ImportWindow.ImpByteOrder.addItem("Big Endian", 'b')

        # export window, byte order
        self.SaveWindow.ExpByteOrder.clear()
        self.SaveWindow.ExpByteOrder.addItem("Little Endian", 'l')
        self.SaveWindow.ExpByteOrder.addItem("Big Endian", 'b')

        # export window, file format
        self.SaveWindow.ExpFormat.Items = {'HDF5 (*.h5)', 'Raw binary (*.raw)'}
        self.SaveWindow.ExpFormat.ItemsData = {'h5', 'raw'}

        # main UI window, diffraction modes
        diffType = ['PrvwMod', 'AlignMod', 'AnnMod', 'DPCMod', 'CoMMod', 'VrApMod', 'CustMod']
        diffTypeText = [
            'Import Preview',
            'Alignment',
            'Annular/Round',
            'Segmented (DPC)',
            'Center of Mass',
            'Virtual Aperture',
            'Custom Detectors']
        self.DetrMode.clear()
        for dtt, dt in zip(diffTypeText, diffType):
            self.DetrMode.addItem(dtt, dt)

        # main UI window, real-space ROI shapes
        ROIType = ['full', 'point', 'ellipse', 'rectangle', 'poly', 'file']
        ROITypeText = ['Full Image', 'Point', 'Ellipse', 'Rectangle', 'Draw Polygon', 'From File']
        self.RealROIShape.clear()
        for rtt, rt in zip(ROITypeText, ROIType):
            self.RealROIShape.addItem(rtt, rt)

        # main UI window, vecotr overlay sampling options
        vectType = [0, 1, 2, 4, 8, 16]
        vectTypeText = ['None', '1:1', '1:2', '1:4', '1:8', '1:16']
        self.DispVecField.clear()
        for vtt, vt in zip(vectTypeText, vectType):
            self.DispVecField.addItem(vtt, vt)

        # import window, GPU selection
        self.ImportWindow.ImpGPU.clear()
        self.ImportWindow.ImpGPU.addItem('GPU off', None)

        # import window, memory loading selection
        self.ImportWindow.ImpMemType.clear()
        self.ImportWindow.ImpMemType.addItems(['Physical Memory', 'Virtual Mapping'])

        # settings window, colormap options
        self.SettingsWindow.DispCMap.clear()
        self.SettingsWindow.DispCMap.addItems(['gray',
                                               'inferno',
                                               'hsv',
                                               'jet',
                                               'viridis',
                                               'hot',
                                               'cool',
                                               'spring',
                                               'summer',
                                               'autumn',
                                               'winter',
                                               'bone',
                                               'copper',
                                               'pink'])

        # settings window, diffraction space coordinates system
        self.SettingsWindow.DCSys.clear()
        self.SettingsWindow.DCSys.addItems(['Polar', 'Cartesian'])

        # settings window, diffraction space position reference
        self.SettingsWindow.DCPos.clear()
        self.SettingsWindow.DCPos.addItems(['Relative', 'Absolute'])

        # settings window, diffraction space units
        self.SettingsWindow.DCUnit.clear()
        self.SettingsWindow.DCUnit.addItem('mrad', 'mrad')
        self.SettingsWindow.DCUnit.addItem('Pixel', 'px')

        # settings window, real space rotation options
        self.SettingsWindow.RotReal.clear()
        self.SettingsWindow.RotReal.Items = {'0°', '90°', '180°', '-90°'}
        self.SettingsWindow.RotReal.ItemsData = [0, 90, 180, -90]

        # settings window, calculation policy
        self.SettingsWindow.CalcPolicy.clear()
        self.SettingsWindow.CalcPolicy.addItem('Active', 2)
        self.SettingsWindow.CalcPolicy.addItem('Reduced', 1)
        self.SettingsWindow.CalcPolicy.addItem('Passive', 0)

        # main UI window, virtual aperture rotation options
        rotType = [90, 60, 45, 30, 22.5, 10, 5, 2, 1, 0.5, 0.25]
        rotTypeText = ['90°', '60°', '45°', '30°', '22.5°', '10°', '5°', '2°', '1°', '0.5°', '0.25°']
        self.VrApRotStep.clear()
        for rtt, rt in zip(rotTypeText, rotType):
            self.VrApRotStep.addItem(rtt, rt)

        # main UI window, custom aperture rotation options
        rotType = [90, 60, 45, 30, 22.5, 10, 5, 2, 1, 0.5, 0.25]
        rotTypeText = ['90°', '60°', '45°', '30°', '22.5°', '10°', '5°', '2°', '1°', '0.5°', '0.25°']
        self.CDRotStep.clear()
        for rtt, rt in zip(rotTypeText, rotType):
            self.CDRotStep.addItem(rtt, rt)

        # main UI window, virtual aperture symmetry options
        symmType = [1, 2, 3, 4, 6]
        symmTypeText = ['1', '2', '3', '4', '6']
        self.VrApSymm.clear()
        for stt, st in zip(symmTypeText, symmType):
            self.VrApSymm.addItem(stt, st)

        # main UI window, custom intramask interactions
        self.CDIntraMask.clear()
        self.CDIntraMask.addItems(['Union', 'Intersection', 'Additive'])

        # main UI window, custom intermask interactions
        self.CDInterMask.clear()
        self.CDInterMask.addItems(['Union', 'Intersection', 'Additive', 'Current-only'])

    # add class attributes to match those from original Matlab version app.*
    appStruct(self)

    # Generate additional UI windows
    self.ImportWindow = ImportWindow()
    self.SettingsWindow = SettingsWindow()
    self.SaveWindow = SaveWindow()

    # get lock and unlock icons for later user
    self.unlock = qtg.QIcon('./gui/icons/unlock.png')
    self.lock = qtg.QIcon('./gui/icons/lock.png')

    # get current screen size information
    checkMonitors(self)

    # check system endianess
    if sys.byteorder == 'little':
        self.C.SysEndian = 'l'
    else:
        self.C.SysEndian = 'b'

    # get CPU memory information
    getMem(self)

    # get GPU memory information (if available)
    getGPU(self)

    # populate all of the dropdowns
    populateDropdowns(self)

    # create other UI windows and Image figures
    createImageWindows(self)

    # enable custom slot/signal interfaces
    slotsSignals(self)

    # start with a mostly blank UI
    self.RealSpacePanel.setVisible(False)
    self.progressBarPanel.setVisible(False)
    self.DfrnDetrTabGroup.setVisible(False)
    self.DetectorModeGroup.setVisible(False)

    # always keep "Import Preview" hidden from QComboBox
    self.DetrMode.view().setRowHidden(0, True)

    # Import Data is the only option to start
    # turn off ALL actions
    for action in self.findChildren(qtw.QAction):
        if "debug" not in action.iconText():
            action.setEnabled(False)

    # make sure top level menu (File, Settings, Window, Help) is enabled
    for menu in self.menubar.actions():
        menu.setEnabled(True)

    # only allow user to import data
    self.ShowImportWdw.setEnabled(True)

    resetQuant4DCallbacks


def reinitializeUI(self):
    # finalize progressBar
    self.progressBar.setMaximum(100)
    self.progressBar.setValue(100)
    self.progressBar.setTextVisible(False)

    self.progressBar.setEnabled(False)

    # make control panels visible again
    self.RealSpacePanel.setVisible(True)
    self.progressBarPanel.setVisible(True)
    self.DfrnDetrTabGroup.setVisible(True)
    self.DetectorModeGroup.setVisible(True)

    # turn ALL actions back on
    for action in self.findChildren(qtw.QAction):
        action.setEnabled(True)

    # update annular QRangeSlider to match
    self.AnnRi.blockSignals(True)
    self.AnnRi.setValue((self.AnnRi.minimum(), self.AnnRi.maximum()))
    self.AnnRi.blockSignals(False)

    # re-enable windows
    enableWindows(self, True)

    # start alignment mode
    self.DetrMode.setCurrentIndex(self.DetrMode.findData("AlignMod"))


def resetQuant4DCallbacks(self):
    unloadData(self, False)
    self.DetrMode.setCurrentIndex(self.DetrMode.findData("PrvwMod"))


def enableWindows(self, sw=True):
    """ Function to enable/disable windows/UI; disable is only for notification/progress bar/busy background etc """
    assert isinstance(sw, bool)

    prvw = self.DetrMode.currentData() == "PrvwMod"  # Preview mode or not
    # Detector Mode UI, keep disabled in Import Preview Mode unless a dataset is loaded
    self.DetrMode.setEnabled(sw and not prvw)  # (sw and (not prvw or self.D is not None))

    # Real-space ROI controls, keep disabled in Import Preview Mode
    self.RealSpacePanel.setEnabled(sw and not prvw)

    # Other UIs can be enabled in Import Preview Mode
    self.toolBar.setEnabled(sw)
    self.DfrnDetrTabGroup.setEnabled(sw)
    self.SettingsWindow.setEnabled(sw)
    self.SaveWindow.setEnabled(sw)
    self.ImportWindow.setEnabled(sw)

    # Also reset all windows' mouse pointer when enabling UIs
    if sw:
        [ii.setCursor(qtc.Qt.ArrowCursor) for ii in self.G.AllFig]


def getDecorSize(self):
    decorSize = [self.geometry().x() - self.pos().x(), self.geometry().y() - self.pos().y()]
    return decorSize
