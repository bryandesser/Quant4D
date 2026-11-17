"""Qt threading worker classes (WorkerSignals, Worker, importThread)."""
import os
import sys
import traceback
import numpy as np
from multiprocessing.pool import ThreadPool
import psutil
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *


class importThread(qtc.QObject):
    """Reads (part of) a dataset into memory on a worker thread.

    Emits ``result`` with the ``(frame, pixel)`` float array, or ``failed``
    with a message, and then always ``finished``.
    """
    result = qtc.pyqtSignal(np.ndarray)
    failed = qtc.pyqtSignal(str)
    finished = qtc.pyqtSignal()

    def __init__(self, on_disk, scan, detector, frames, pixels):
        super().__init__()
        self.on_disk = on_disk
        self.scan, self.detector = scan, detector
        self.frames, self.pixels = frames, pixels

    def run(self):
        from callbacks.io.raw import read_frames
        try:
            data = read_frames(self.on_disk, self.scan, self.detector, self.frames, self.pixels)
        except (OSError, ValueError, MemoryError) as exc:
            self.failed.emit(f"{type(exc).__name__}: {exc}")
        else:
            self.result.emit(data)
        finally:
            self.on_disk = None          # close the memory map
            self.finished.emit()
