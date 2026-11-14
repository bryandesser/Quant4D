"""EMPAD file-format reader."""
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


def prepEMPAD(self):
    # filename from import dialog
    filename = self.D.fileName

    # standar dataset header/footer sizes (in bytes)
    header = 0
    footer = 1024

    # standard detector shape
    nopix = 128
    nopiy = 128

    # default EMPAD datatype is float32
    bitsize = 4

    # real space scan shape is saved in the empad footer data
    framesx, framesy = np.fromfile(filename, count=2, dtype="float32", offset=header +
                                   (nopix * nopiy + 142) * bitsize).astype(int)

    # check to make sure scan shape makes sense
    if self.T.FileSize != ((header + nopix * nopiy * bitsize + footer) * int(framesx * framesy)):
        # check to see if filename has 'fooAxBxCxDbar' structure, where:  A =
        # NPxX, B = NPxY, C = NFrX, D = NFrY, and are numbers
        if re.findall(r"\d+x\d+x\d+x\d+", filename):
            s = re.findall(r"\d+x\d+x\d+x\d+", filename)
            nopix, nopiy, framesx, framesy = [int(i) for i in re.split("x", s[0])]
        elif re.findall(r"_x\d+_y\d+", filename):
            s = re.findall(r"\d+", filename)
            framesx, framesy = [int(i) for i in s]
        else:
            framesx, framesy = 1, 1

    self.ImportWindow.DNPxX.setValue(nopix)
    self.ImportWindow.DNPxY.setValue(nopiy)
    self.ImportWindow.DNFrX.setValue(framesx)
    self.ImportWindow.DNFrY.setValue(framesy)
    self.ImportWindow.ImpByteOrder.setCurrentIndex(0)
    self.ImportWindow.FrHead.setValue(header)
    self.ImportWindow.FrFoot.setValue(footer)
