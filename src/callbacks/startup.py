"""App startup, slot/signal wiring, window enable, layout helpers."""
import os
import sys
import traceback
import psutil
import numpy as np
try:
    import torch
except ImportError:
    class _TorchStub:
        class cuda:
            @staticmethod
            def is_available(): return False

            @staticmethod
            def device_count(): return 0

            @staticmethod
            def get_device_properties(i):
                raise RuntimeError("torch not installed; install pyquant4d[gpu]")

            @staticmethod
            def get_device_name(i):
                raise RuntimeError("torch not installed; install pyquant4d[gpu]")

        @staticmethod
        def device(x): return x
    torch = _TorchStub()  # type: ignore[assignment]
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
from callbacks.plotting import displayCallbacks, sliderReleased, updateImagesCallbacks  # noqa: E402
from callbacks.detector import detectorModeCallbacks, detrCoordCallbacks  # noqa: E402
from callbacks.annularDetectorCallbacks import annularDetectorCallbacks  # noqa: E402
from callbacks.importCallbacks import importCallbacks  # noqa: E402
from callbacks.import_io import importSelectFile, importBoxInput, importFileType, importVoltageChanged  # noqa: E402
from callbacks.window_manager import (  # noqa: E402
    resizeWindowCallbacks, showAllWindows, hideAllWindows, showWindowCallbacks,
)
from callbacks.datasetOptCallbacks import datasetOptCallbacks  # noqa: E402
from callbacks.alignment import moveTransBeam, transBeamCallbacks  # noqa: E402
from callbacks.previewCallbacks import previewCallbacks  # noqa: E402
from callbacks.virtualApertureCallbacks import virtualApertureCallbacks  # noqa: E402
from callbacks.customDetectorCallbacks import connectCustomDetector  # noqa: E402
from callbacks.axis_direction import connectAxisDirection  # noqa: E402
from callbacks.menus import connectMenus  # noqa: E402
from callbacks.realSpaceROICallbacks import connectPatternCombine, realSpaceROICallbacks  # noqa: E402
from callbacks.utils import breakpoint  # noqa: E402,A001
from callbacks.signals import signals_blocked  # noqa: E402
from callbacks.window_manager import enableWindows  # noqa: E402,F401  (moved; re-exported)


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
    self.ImportWindow.ImpFileSelect.clicked.connect(
        lambda: importSelectFile(self, source=self.ImportWindow.ImpFileSelect))
    # a path typed or pasted into the field is read when editing finishes (Enter or focus change)
    self.ImportWindow.ImpFilePath.editingFinished.connect(
        lambda: importSelectFile(self, source=self.ImportWindow.ImpFilePath))
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
    self.ImportWindow.ImpSubImg.currentIndexChanged.connect(
        lambda: importFileType(self, self.ImportWindow.ImpSubImg))
    self.ImportWindow.ImpAccVolt.valueChanged.connect(lambda *_: importVoltageChanged(self))
    # file-type radio buttons: re-read the file's header/geometry for the chosen type
    for button in (self.ImportWindow.EMPADButton, self.ImportWindow.MedipixButton, self.ImportWindow.MRCButton,
                   self.ImportWindow.DM34Button, self.ImportWindow.HDF5Button, self.ImportWindow.CustomButton):
        button.clicked.connect(lambda: importFileType(self))

    # save window slots/signals
    self.SaveWindow.SaveImgSelectAll.clicked.connect(
        lambda isChecked: self.SaveWindow.SaveImgList.selectAll() if isChecked else self.SaveWindow.SaveImgList.clearSelection())
    from callbacks.save_export import connectSaveWindow  # noqa: E402
    connectSaveWindow(self)
    connectCustomDetector(self)   # Custom Detector tab and Math → Evaluate
    from callbacks.scan_step import connectScanStep  # noqa: E402
    connectScanStep(self)         # Scan Step: Import window (file) and Settings > Misc (loaded data)
    from callbacks.py4dstem_bridge import connectPy4DSTEM  # noqa: E402
    connectPy4DSTEM(self)         # File > Open with py4DSTEM Reader... (only with py4DSTEM installed)
    from callbacks.file_drop import installFileDrop  # noqa: E402
    installFileDrop(self)         # drop a dataset file on any window to open it in the Import window
    connectAxisDirection(self)    # Settings: reverse X/Y, rotate view, axis-direction arrows
    connectMenus(self)            # menu-bar actions and help icons
    connectPatternCombine(self)   # diffraction window: how a region's patterns are combined
    from callbacks.view_zoom import connectZoom  # noqa: E402
    connectZoom(self)             # wheel/keys zoom, Home, one view per space
    from callbacks.plotting import connectHistogramReset  # noqa: E402
    connectHistogramReset(self)   # double-click the histogram: default brightness/contrast/gamma
    from callbacks.alignment import connectBeamPick  # noqa: E402
    connectBeamPick(self)         # Alignment mode: double-click a disk to make it the transmitted beam

    # Tooltips also when the window is not the active one (Qt shows them only in the active window,
    # yet hovering highlights buttons in any window, which made the missing tooltip look like a bug)
    for window in [self, self.SettingsWindow, self.ImportWindow, self.SaveWindow] + \
            [self.Fig[id] for id in self.G.ImgID if self.Fig[id] is not None]:
        window.setAttribute(qtc.Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)

    # menu action slots/signals: show/hide an image window (QWidget.show takes no argument: passing
    # the checked state raised a TypeError).  The action's tick follows the window (guiClass).
    from callbacks.window_manager import setWindowShown  # noqa: E402
    for action, id in ((self.actionShow_Diffraction_Pattern, "Dfrn"), (self.actionShow_Diffraction_Mask, "DfrnMask"),
                       (self.actionShow_Real_Space_Image, "Real"), (self.actionShow_Real_Space_Mask, "RealMask"),
                       (self.actionShow_Center_of_Mass_Magnitude_CoM, "CoMMag"),
                       (self.actionShow_Center_of_Mass_X, "CoMX"), (self.actionShow_Center_of_Mass_Y, "CoMY"),
                       (self.actionShow_Colorwheel, "ColorWheel"),
                       (self.actionShow_Differential_Center_of_Mass_dCoM, "dCoM"),
                       (self.actionShow_Integrated_Center_of_Mass_iCoM, "iCoM"),
                       (self.actionShow_Phase_Magnitude, "CoMPhMag"), (self.actionShow_Phase_Vector_Image, "CoMPh")):
        action.setCheckable(True)
        self.Fig[id].menuAction = action
        action.triggered.connect(lambda checked, _id=id: setWindowShown(self, _id, checked))
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
    # the main window's show-window buttons had no accessible name, which names the window to show
    for button, id, tip in ((self.ShowRealMaskWdw, "RealMask", "Show the real-space mask"),
                            (self.ShowDfrnMaskWdw, "DfrnMask", "Show the diffraction mask")):
        button.setAccessibleName(id)
        button.setToolTip(tip)
    self.ShowRealMaskWdw.clicked.connect(lambda: showWindowCallbacks(self))
    self.ShowDfrnMaskWdw.clicked.connect(lambda: showWindowCallbacks(self))

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
    self.SettingsWindow.DispVecColor.clicked.connect(lambda: displayCallbacks(self))   # (triggered needs an action)
    self.SettingsWindow.DispVecField.currentIndexChanged.connect(lambda: displayCallbacks(self))
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
    for w in (self.SettingsWindow.DispMaskOpa, self.SettingsWindow.DispMaskOpa_NF):
        w.setToolTip("Dims the parts of the selected image outside its mask (the detector or real-space ROI). "
                     "No effect where the mask covers everything: Align mode, or the full real-space ROI.")
    self.SettingsWindow.CalcPolicy.currentIndexChanged.connect(lambda *_: updateImagesCallbacks(self))
    for slider in self.findChildren(qtw.QAbstractSlider):            # Reduced policy: update on release
        slider.sliderReleased.connect(lambda: sliderReleased(self))
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
    self.NRung.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.DetRot_NF.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.DetRot.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.ScanDirUnlock.clicked.connect(lambda: annularDetectorCallbacks(self))
    self.ScanDirYFlip.clicked.connect(lambda: annularDetectorCallbacks(self))
    self.ScanDir_NF.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.ScanDir.valueChanged.connect(lambda: annularDetectorCallbacks(self))
    self.AutoCurl.clicked.connect(lambda: annularDetectorCallbacks(self))
    from callbacks.annularDetectorCallbacks import annStepChanged  # noqa: E402
    from callbacks.annularDetectorCallbacks import connectBandpass  # noqa: E402
    connectBandpass(self)                            # Settings > Windows: iCoM/dCoM bandpass filter
    from callbacks.variables import connectVariables  # noqa: E402
    connectVariables(self)                           # Settings > Info: Show all variables
    self.AnnStep.setKeyboardTracking(False)          # a typed value counts once confirmed (Enter, focus out)
    self.AnnStep.valueChanged.connect(lambda *_: annStepChanged(self))

    # virtual aperture connections
    self.VrApR.valueChanged.connect(lambda: virtualApertureCallbacks(self))
    self.VrApSymm.currentIndexChanged.connect(lambda: virtualApertureCallbacks(self))
    # these two are toggles, but the .ui file does not mark them checkable
    self.VrApInvert.setCheckable(True)
    self.VrApMirror.setCheckable(True)
    self.VrApInvert.clicked.connect(lambda: virtualApertureCallbacks(self))
    self.VrApMirror.clicked.connect(lambda: virtualApertureCallbacks(self))
    self.VrApMirrRot.valueChanged.connect(lambda: virtualApertureCallbacks(self))
    self.VrApMirrRot_NF.valueChanged.connect(lambda: virtualApertureCallbacks(self))
    self.VrApRotCW.clicked.connect(lambda: virtualApertureCallbacks(self))
    for w in (self.VrApX, self.VrApY, self.VrApX_NF, self.VrApY_NF, self.VrApR_NF):
        w.valueChanged.connect(lambda *_: virtualApertureCallbacks(self))
    self.VrApReset.clicked.connect(lambda: virtualApertureCallbacks(self))
    self.VrApRotCCW.clicked.connect(lambda: virtualApertureCallbacks(self))

    # Settings window, units choices
    self.SettingsWindow.DCSys.currentIndexChanged.connect(lambda: detrCoordCallbacks(self))
    self.SettingsWindow.DCPos.currentIndexChanged.connect(lambda: detrCoordCallbacks(self))
    self.SettingsWindow.DCUnit.currentIndexChanged.connect(lambda: detrCoordCallbacks(self))
    self.RealROIShape.currentIndexChanged.connect(lambda: realSpaceROICallbacks(self))
    self.FrameX.valueChanged.connect(lambda: realSpaceROICallbacks(self))
    self.FrameY.valueChanged.connect(lambda: realSpaceROICallbacks(self))
    self.RealROIInvert.clicked.connect(lambda: realSpaceROICallbacks(self))


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
        if self.C.nGPU == 0:  # no GPU devices (or no CUDA-enabled torch)
            self.ImportWindow.ImpGPU.addItem('No GPU found.', None)   # None = CPU (it was device 0)
            self.ImportWindow.ImpGPU.setToolTip("No CUDA GPU found. GPU acceleration needs PyTorch with CUDA "
                                                "(pip install pyquant4d[gpu]).")
        else:  # 1 or more devices found
            maxmem = 0
            for i in np.arange(0, self.C.nGPU):
                self.C.GPUmem.append(torch.cuda.get_device_properties(i).total_memory)
                self.C.GPUname.append(torch.cuda.get_device_name(i))
                self.ImportWindow.ImpGPU.addItem(self.C.GPUname[i], int(i))     # plain int for torch.device
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
        desktop = qtw.QApplication.desktop()
        assert desktop is not None, "checkMonitors needs a QApplication"
        self.C.monitorWidth = desktop.screenGeometry().width()
        self.C.monitorHeight = desktop.screenGeometry().height()

        # toolbar size + any horizontal or vertical offsets due to toolbar
        self.C.hOffset, self.C.vOffset, self.C.toolbarWidth, self.C.toolbarHeight = abs(np.array(
            desktop.screenGeometry().getRect()) - np.array(desktop.availableGeometry().getRect()))

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
        self.G.CoM_btns.extend([self.SettingsWindow.ShowColorWheelWdw_2])

        # Group all window `figure` `uifigure`
        self.G.AllFig = self.G.ImgFig.copy()
        self.G.AllFig.extend([self, self.SettingsWindow, self.ImportWindow, self.SaveWindow])

    def updateImageWindowSize(self, size, space):
        """Settings > Misc > window size: the image area of the window just resized, i.e. its size less
        the toolbar/decoration (``mplDecor``, which the Set buttons add back).  This used to add each
        resize's change to the fields, and the first change of a new window is its whole size
        (Qt's old size is -1 x -1), so the fields filled up to about the monitor's size."""
        boxes = {"Dfrn": (self.SettingsWindow.WdwWDfrn, self.SettingsWindow.WdwHDfrn),
                 "Real": (self.SettingsWindow.WdwWReal, self.SettingsWindow.WdwHReal)}.get(space)
        if boxes is None or size.width() <= 0 or size.height() <= 0:
            return
        with signals_blocked(*boxes):
            boxes[0].setValue(max(1, size.width() - self.C.mplDecor.width()))
            boxes[1].setValue(max(1, size.height() - self.C.mplDecor.height()))

    def updateDispImg(self, id):
        """Clicking an image window selects it for the display controls, unless the selection is locked."""
        if self.SettingsWindow.DispLock.isChecked():
            return
        idx = self.SettingsWindow.DispImage.findData(id)
        if idx != -1:
            self.SettingsWindow.DispImage.setCurrentIndex(idx)

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

        # export window, file format: populated in save_export.connectSaveWindow

        # main UI window, diffraction modes
        diffType = ['PrvwMod', 'AlignMod', 'AnnMod', 'CoMMod', 'DPCMod', 'VrApMod', 'CustMod']   # CoM before DPC, as MATLAB
        diffTypeText = [
            'Import Preview',
            'Alignment',
            'Annular/Round',
            'Center of Mass',
            'Segmented (DPC)',
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
        self.SettingsWindow.DispVecField.clear()
        for vtt, vt in zip(vectTypeText, vectType):
            self.SettingsWindow.DispVecField.addItem(vtt, vt)

        # import window, GPU selection: filled by getGPU (clearing it here dropped every detected GPU)

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

        # settings window, view rotation options: callbacks.axis_direction.connectAxisDirection

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

        # custom detector rotation steps and inter-mask modes: customDetectorCallbacks.connectCustomDetector

        # main UI window, virtual aperture symmetry options
        symmType = [1, 2, 3, 4, 6]
        symmTypeText = ['1', '2', '3', '4', '6']
        self.VrApSymm.clear()
        for stt, st in zip(symmTypeText, symmType):
            self.VrApSymm.addItem(stt, st)

        # main UI window, custom intramask interactions
        self.CDIntraMask.clear()
        self.CDIntraMask.addItems(['Union', 'Intersection', 'Additive'])

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
    from callbacks.virtualApertureCallbacks import syncVrApControls  # noqa: E402
    syncVrApControls(self)        # mirror-angle controls off until the mirror is

    # The app starts in Import Preview mode without a mode change, so apply its tab set here
    # (the Math, Misc and Info tabs and the Export tab were all shown until a mode change)
    from callbacks.window_manager import setPreviewTabs  # noqa: E402
    setPreviewTabs(self, True)

    # The app starts in Import Preview mode without a mode change, so the display selector would stay
    # empty (no histogram/statistics for the preview): give it the Preview image, as the mode change does.
    with signals_blocked(self.SettingsWindow.DispImage):
        self.SettingsWindow.DispImage.clear()
        self.SettingsWindow.DispImage.addItem("Preview", "Preview")

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
    for action in (self.actionQuit, self.actionQuant4D_Manual, self.actionAbout_Quant4D, self.actionOpen_with_py4DSTEM):
        action.setEnabled(True)      # always available


def reinitializeUI(self):
    # the import is done: no progress bar left at the bottom of the main window
    from callbacks.window_manager import hideProgressBar  # noqa: E402
    hideProgressBar(self)

    # make control panels visible again
    self.RealSpacePanel.setVisible(True)
    self.DfrnDetrTabGroup.setVisible(True)
    self.DetectorModeGroup.setVisible(True)

    # turn ALL actions back on
    for action in self.findChildren(qtw.QAction):
        action.setEnabled(True)

    # update annular QRangeSlider to match
    with signals_blocked(self.AnnRi):
        self.AnnRi.setValue((self.AnnRi.minimum(), self.AnnRi.maximum()))

    # re-enable windows
    enableWindows(self, True)

    # start alignment mode
    self.DetrMode.setCurrentIndex(self.DetrMode.findData("AlignMod"))


def resetQuant4DCallbacks(self):
    from callbacks.import_io import unloadData  # noqa: E402
    unloadData(self, False)
    self.DetrMode.setCurrentIndex(self.DetrMode.findData("PrvwMod"))


def getDecorSize(self):
    decorSize = [self.geometry().x() - self.pos().x(), self.geometry().y() - self.pos().y()]
    return decorSize
