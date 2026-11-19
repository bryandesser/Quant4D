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
from callbacks.window_manager import enableWindows  # noqa: E402
from callbacks.layout import dfrn_grids, dfrn_shape, real_shape  # noqa: E402
from callbacks.io.export import Region  # noqa: E402
from callbacks.io.raw import open_frames  # noqa: E402
from callbacks.signals import all_signals_blocked  # noqa: E402


def readFile(self):
    self.ImportWindow.hide()
    self.ShowImportWdw.setChecked(False)

    # initialize progressBar
    self.progressBar.setTextVisible(False)
    self.progressBar.setMaximum(0)

    # while not importDialog.wasCanceled():
    filename = self.D.filePath

    d = self.D
    # what is on disk, and which part of it to read (0-based starts)
    scan, detector = (d.DNFrX, d.DNFrY), (d.DNPxX, d.DNPxY)
    frames = Region((d.FrX1, d.FrY1), (d.NFrX, d.NFrY), d.FrD)
    pixels = Region((d.PxX1, d.PxY1), (d.NPxX, d.NPxY), d.PxD)
    if d.h5ds:      # HDF5 into memory: read through h5py (chunked/compressed datasets have no data offset)
        from callbacks.io.hdf5 import H5Frames
        on_disk = H5Frames(h5py.File(filename, "r")[d.h5ds])
        if on_disk.shape != (scan[0] * scan[1], detector[0] * detector[1]):
            on_disk.close()
            importFailed(self, f"The dataset {d.h5ds} holds {on_disk.shape[0]} frames of {on_disk.shape[1]} pixels, "
                               f"not {scan[0]} x {scan[1]} frames of {detector[0]} x {detector[1]} pixels.")
            return
    else:
        on_disk = open_frames(filename, d.Offset, scan[0] * scan[1], detector[0] * detector[1],
                              d.DataType, d.FrHead, d.FrFoot, d.ByteOrder)

    # show progressbar to let user know things are happening
    self.progressBarPanel.setVisible(True)
    self.progressBarPanel.setEnabled(True)

    if self.ImportWindow.ImpMemType.currentIndex() == 0:  # physical memory, read on a worker thread
        _stopImportThread(self)
        self.workerThread = qtc.QThread()
        self.worker = importThread(on_disk, scan, detector, frames, pixels)
        self.worker.moveToThread(self.workerThread)
        self.workerThread.started.connect(self.worker.run)
        self.worker.result.connect(self.receiveThreadData)
        self.worker.failed.connect(lambda msg: importFailed(self, msg))
        self.worker.finished.connect(lambda: finishImport(self))
        self.workerThread.start()

    else:  # lazy loading: the whole dataset, mapped (only offered for float data without partial import)
        self.Data = on_disk
        self.workerThread = None
        finishImport(self)


def _stopImportThread(self):
    """Stop the import thread and wait for it.

    Waiting matters: the next import replaces ``self.workerThread``, and Qt
    aborts the program if a QThread object is destroyed while still running.
    """
    thread = getattr(self, "workerThread", None)
    if thread is not None:
        thread.quit()
        thread.wait()


def importFailed(self, msg):
    """The worker could not read the file: report it and leave no dataset loaded."""
    from callbacks.utils import notifDLG
    from callbacks.import_io import unloadData
    from callbacks.window_manager import hideProgressBar
    _stopImportThread(self)
    hideProgressBar(self)
    unloadData(self)
    notifDLG(self, self, "error", f"Error during import:\n{msg}", "Import Failed")


def prepareData(self, keep_beam=False):
    """Reset the controls for the dataset just loaded (or swapped).

    *keep_beam* keeps the transmitted-beam alignment (swapping real-space X/Y).
    Never reads ``self.sender()``: this also runs outside a slot (``pyquant4d.show``).
    """
    # self.T.progDLG = progDLG(self, 'Preparing data ...', "Data Preparation"); #TODO

    # block slots/signals whilst initializing UI components
    from callbacks.alignment import transBeamCallbacks  # noqa: E402
    from callbacks.detector import detectorModeCallbacks  # noqa: E402
    with all_signals_blocked(self):
        # move to alignment mode
        self.DetrMode.setCurrentIndex(self.DetrMode.findData("AlignMod"))

        # Detector controls
        self.P.ScanDirInit = 0              # Reset alignments
        self.P.CoMRadiusInit = False
        from callbacks.annularDetectorCallbacks import resetBandpass  # noqa: E402
        resetBandpass(self)                 # iCoM/dCoM filter keeps every frequency of this scan
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
        # Exact (x, y) centres in 0-based pixel coordinates: pixel i spans [i - 0.5, i + 0.5]
        self.P.DfCtr = (np.array([self.D.NPxX, self.D.NPxY]) - 1) / 2   # Diffraction image
        self.P.RsCtr = (np.array([self.D.NFrX, self.D.NFrY]) - 1) / 2   # Real-space image
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
        if not keep_beam:  # Keep transmitted beam alignment if swapping Real-space X/Y
            self.P.TransBeamInit = 0
            # set transmitted beam ranges and values for sliders and number fields
            self.TBR.setRange(0, max(self.D.NPx))
            self.TBX.setRange(0, self.D.NPxX - 1)
            self.TBY.setRange(0, self.D.NPxY - 1)
            self.TBR.setValue(min(self.D.NPx) / 10)
            self.TBX.setValue(self.P.DfCtr[0])
            self.TBY.setValue(self.P.DfCtr[1])
            self.TBX_NF.setRange(0, self.D.NPxX - 1)
            self.TBY_NF.setRange(0, self.D.NPxY - 1)
            self.TBX_NF.setValue(self.P.DfCtr[0])
            self.TBY_NF.setValue(self.P.DfCtr[1])
            transBeamCallbacks(self)  # Update Transmitted Beam dependant variables

        # Real-space ROI controls
        self.FrameX.setRange(0, self.D.NFrX - 1)
        self.FrameY.setRange(0, self.D.NFrY - 1)
        self.FrameX.setValue(round(self.P.RsCtr[0]))
        self.FrameY.setValue(round(self.P.RsCtr[1]))
        self.RealROIInvert.setChecked(False)  # do not invert the real space ROI picker on initialization
        self.RealROIShape.setCurrentIndex(self.RealROIShape.findData("full"))  # display PACBED from the entire dataset

        # Export controls: whole dataset
        from callbacks.save_export import resetExportRanges  # noqa: E402
        resetExportRanges(self)

        # initiate image display parameters for all ImageWindows
        for id in self.G.ImgID:
            self.Fig[id].brightness = 50
            self.Fig[id].contrast = 50
            self.Fig[id].gamma = 1
            self.Fig[id].maskOpa = 0
            self.Fig[id].vecField = 0

    self.UpdateImages.trigger()  # Update all images
    # delete(self.T.progDLG);  # Close progress bar and Enable panel objects #TODO

    # initialize SettingsWindow and move next to main UI window
    self.SettingsWindow.SettingsTabGroup.setCurrentWidget(self.SettingsWindow.DisplayTab)
    from callbacks.window_manager import placeBesideMain  # noqa: E402
    placeBesideMain(self, self.SettingsWindow)
    self.SettingsWindow.show()

    # Enter alignment mode.  The mode callbacks dispatch on self.sender(), so
    # emit the combo's own signal rather than calling them directly (the index
    # was already set above while signals were blocked, so setCurrentIndex
    # alone would not fire).
    self.DetrMode.currentIndexChanged.emit(self.DetrMode.currentIndex())

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
    from callbacks.startup import reinitializeUI  # noqa: E402
    _stopImportThread(self)
    if self.Data is None:        # the worker failed; importFailed has reported it
        return

    # generate placeholder images
    self.Fig.Preview.Image = np.zeros(dfrn_shape(self.D))
    self.Fig.Dfrn.Image = np.zeros(dfrn_shape(self.D))
    self.Fig.DfrnMask.Image = np.zeros(dfrn_shape(self.D))
    self.Fig.Real.Image = np.zeros(real_shape(self.D))
    self.Fig.RealMask.Image = np.zeros(real_shape(self.D))

    prepareData(self)
    reinitializeUI(self)
