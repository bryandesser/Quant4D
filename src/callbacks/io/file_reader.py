"""Top-level file reading and data preparation."""
import os
import sys
import traceback
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *
import re
import gc
import psutil
import importlib
import h5py
import time
import matplotlib
from PIL import Image
try:
    import torch
except ImportError:
    class _TorchStub:                                        # noqa: E302
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

# Deferred cross-module imports (safe: file_reader is itself only loaded lazily)
from callbacks.threading_workers import importThread  # noqa: E402
from callbacks.utils import notifDLG, checkNaN  # noqa: E402
from callbacks.startup import enableWindows  # noqa: E402


def readFile(self):
    self.ImportWindow.hide()
    self.ShowImportWdw.setChecked(False)

    # initialize progressBar
    self.progressBar.setTextVisible(False)
    self.progressBar.setMaximum(0)

    # while not importDialog.wasCanceled():
    filename = self.D.filePath

    # dataset offset
    dataOffset = self.D.Offset

    # dataset header/foot sizes (in bytes)
    header = self.D.FrHead
    footer = self.D.FrFoot

    # detector shape
    nopix = self.D.NPxX
    nopiy = self.D.NPxY

    # real space scan shape
    framesx = self.D.NFrX
    framesy = self.D.NFrY
    dataType = [("header", "{}uint8".format(header)), ("data", "{}{}".format(
        nopix * nopiy, self.D.DataType)), ("footer", "{}uint8".format(footer))]

    # show progressbar to let user know things are happening
    self.progressBarPanel.setVisible(True)
    self.progressBarPanel.setEnabled(True)

    # Read in the file on a separate thread, if dtype is int, default to memmap and convert to float
    if self.ImportWindow.ImpMemType.currentIndex() == 0:  # physical memory
        self.workerThread = qtc.QThread()
        self.worker = importThread(filename, dataType, self.D.DataType, nopix * nopiy, framesx * framesy, dataOffset)
        self.worker.moveToThread(self.workerThread)
        self.workerThread.started.connect(self.worker.run)
        self.worker.result.connect(self.receiveThreadData)
        self.worker.finished.connect(lambda: finishImport(self))
        self.workerThread.start()

    else:  # lazy loading
        self.Data = np.memmap(filename, dataType, 'r')["data"]


def prepareData(self):
    # self.T.progDLG = progDLG(self, 'Preparing data ...', "Data Preparation"); #TODO

    # block slots/signals whilst initializing UI components
    self.blockAllSignals = True

    # move to alignment mode
    self.DetrMode.setCurrentIndex(self.DetrMode.findData("AlignMod"))

    # Detector controls
    self.P.ScanDirInit = 0              # Reset alignments
    self.NSeg.setValue(4)               # DPC defaults: 4 segments for DPC
    self.NRung.setValue(1)  # 1 rung for DPC
    self.DetRot.setValue(0)  # 0 detector rotation
    self.DetRot_NF.setValue(0)          #
    self.ScanDir.setValue(0)  # 0 scan rotation
    self.ScanDir_NF.setValue(0)         #

    self.VrApSymm.setCurrentIndex(0)    # default to one virtual aperture
    self.VrApInvert.setChecked(False)   # without inversion
    self.VrApMirror.setChecked(False)   # without mirror symmetry
    self.VrApMirrRot.setValue(0)        # initialize mirror symmetry to 0 degrees
    self.VrApMirrRot_NF.setValue(0)     #

    # Alignments
    self.P.DfCtr = self.D.NPx / 2 + .5      # Exact center of the Diffraction image
    self.P.RsCtr = self.D.NFr / 2 + .5      # Exact center of the Real-space image
    self.Alpha.setValue(12)             # initialize alpha to 12 mrad
    self.P.VrApXY = self.P.DfCtr        # initialize virtual aperture to diffraction center

    # Axes limits, restrict to avoid rounding to pixels outside the image. Origin upper left as in raster scanning
    self.P.DfrnAxLim = np.array([0, self.D.NPxX, self.D.NPxY, 0]) - 0.5
    self.P.RealAxLim = np.array([0, self.D.NFrX, self.D.NFrY, 0]) - 0.5

    # initialize diffraction space axis limits for all diffraction space images
    for id in self.G.DfrnID:
        self.Fig[id].ax.set_xbound(self.P.DfrnAxLim[0:2])
        self.Fig[id].ax.set_ybound(self.P.DfrnAxLim[2:4])
        self.Fig[id].canvas.draw_idle()

    # initialize real space axis limits for all real space images
    for id in self.G.RealID:
        self.Fig[id].ax.set_xbound(self.P.RealAxLim[0:2])
        self.Fig[id].ax.set_ybound(self.P.RealAxLim[2:4])
        self.Fig[id].canvas.draw_idle()

    # Transmitted Beam controls
    if self.sender() is not self.SettingsWindow.SwapRealXY:  # Keep transmitted beam alignment if swapping Real-space X/Y
        self.P.TransBeamInit = 0
        # set transmitted beam ranges and values for sliders and number fields
        self.TBR.setRange(0, max(self.D.NPx))
        self.TBX.setRange(0, self.D.NPxX)
        self.TBY.setRange(0, self.D.NPxY)
        self.TBR.setValue(min(self.D.NPx) / 10)
        self.TBX.setValue(self.P.DfCtr[0])
        self.TBY.setValue(self.P.DfCtr[1])
        self.TBX_NF.setRange(0, self.D.NPxX)
        self.TBY_NF.setRange(0, self.D.NPxY)
        self.TBX_NF.setValue(self.P.DfCtr[0])
        self.TBY_NF.setValue(self.P.DfCtr[1])
        transBeamCallbacks(self)  # Update Transmitted Beam dependant variables

    # Real-space ROI controls
    self.FrameX.setRange(0, self.D.NFrX)
    self.FrameY.setRange(0, self.D.NFrY)
    self.FrameX.setValue(round(self.P.RsCtr[0]))
    self.FrameY.setValue(round(self.P.RsCtr[1]))
    self.RealROIInvert.setChecked(False)  # do not invert the real space ROI picker on initialization
    self.RealROIShape.setCurrentIndex(self.RealROIShape.findData("full"))  # display PACBED from the entire dataset

    # Export controls #TODO
    self.SaveWindow.ExpPxPart.setChecked(False)
    self.SaveWindow.ExpFrPart.setChecked(False)

    # initiate image display parameters for all ImageWindows
    for id in self.G.ImgID:
        self.Fig[id].brightness = 50
        self.Fig[id].contrast = 50
        self.Fig[id].gamma = 1
        self.Fig[id].maskOpa = 0
        self.Fig[id].vecField = 0

    # unblock slots/signals
    self.blockAllSignals = False

    self.UpdateImages.trigger()  # Update all images
    # delete(self.T.progDLG);  # Close progress bar and Enable panel objects #TODO

    # initialize SettingsWindow and move next to main UI window
    self.SettingsWindow.SettingsTabGroup.setCurrentWidget(self.SettingsWindow.DisplayTab)
    pos = self.SettingsWindow.geometry()
    pos.moveLeft(self.geometry().getRect()[0] + self.geometry().getRect()[2] + self.C.decorPad * 2)
    pos.moveTop(self.geometry().getRect()[1])
    self.SettingsWindow.setGeometry(pos)
    self.SettingsWindow.show()

    self.DetrMode.setCurrentIndex(self.DetrMode.findData("AlignMod"))
    detectorModeCallbacks(self)

    # flashBackground(self, [self.DfrnCalibGrid self.TransBeamAlignGrid])


def finishImport(self):
    # push annular integration to a worker threadpool #TODO
    # print("finishImport(self) on thread {}".format(int(qtc.QThread.currentThreadId())))
    # print("worker established: {}".format(datetime.now()))
    # worker = Worker(integrateAnnular,self)
    # worker.signals.result.connect(self.receiveWorkerData)
    # worker.signals.finished.connect(lambda: reinitializeUI(self))
    # print("threadpool established: {}".format(datetime.now()))
    # self.threadpool = qtc.QThreadPool()
    # print("threadpool started: {}".format(datetime.now()))
    # self.threadpool.start(worker)

    # quit the import thread
    self.workerThread.quit()

    # generate placeholder images
    self.Fig.Preview.Image = np.zeros(self.D.NPx)
    self.Fig.Dfrn.Image = np.zeros(self.D.NPx)
    self.Fig.Dfrn.ImageMask = np.zeros(self.D.NPx)
    self.Fig.Dfrn.Real = np.zeros(self.D.NFr)
    self.Fig.Dfrn.RealMask = np.zeros(self.D.NFr)

    prepareData(self)
    reinitializeUI(self)
