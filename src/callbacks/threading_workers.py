"""Qt threading worker classes (WorkerSignals, Worker, importThread)."""
import os
import sys
import traceback
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *


class importThread(qtc.QObject):
    result = qtc.pyqtSignal(np.ndarray)
    finished = qtc.pyqtSignal()

    def __init__(self, filename, dataType, dtype, pixCount, frameCount, dataOffset):
        super().__init__()
        self.filename = filename
        self.dataType = dataType
        self.dType = dtype
        self.pixCount = pixCount
        self.frameCount = frameCount
        self.dataOffset = dataOffset
        self.isInt = np.issubdtype(self.dType, np.integer)
        if self.isInt:
            if np.dtype(self.dType).itemsize > 4:
                self.float = np.float64
            else:
                self.float = np.float32

    def run(self):
        if self.isInt:
            self.DataMemmap = np.memmap(
                self.filename,
                dtype=self.dataType,
                mode="c",
                offset=self.dataOffset,
                shape=(
                    self.frameCount))["data"]
            self.Data = np.zeros(shape=self.DataMemmap.shape, dtype=self.float)
            nThreads = psutil.cpu_count(logical=False)
            with ThreadPool(processes=nThreads) as pool:
                pool.map(self.convertInt2Float, range(self.DataMemmap.shape[0]))
            pool.join()
        else:
            self.Data = np.fromfile(
                self.filename,
                dtype=self.dataType,
                count=self.frameCount,
                offset=self.dataOffset)["data"]
        self.result.emit(self.Data)
        self.finished.emit()

    def convertInt2Float(self, val):
        self.Data[val, :] = self.DataMemmap[val, :].astype(self.float)
