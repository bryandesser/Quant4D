"""Digital Micrograph (.dm3/.dm4) file-format reader."""
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


def prepDM(self):
    # create a MATLAB-like structure
    class struct(object):
        def __init__(self) -> None:
            pass

    # Identify DM scalar type for byte reading
    def dmBin(btype, out_type):
        match btype:
            case 2:
                p, b = "i2", 2
            case 3:
                p, b = "i4", 4
            case 4:
                p, b = "u2", 2  # OR Unicode string
            case 5:
                p, b = "u4", 4
            case 6:
                p, b = "f4", 4
            case 7:
                p, b = "f8", 8
            case 8:
                p, b = "i1", 1  # Boolean
            case 9:
                p, b = "i1", 1
            case 10:
                p, b = "u1", 1
            case 11:
                p, b = "i8", 8
            case 12:
                p, b = "u8", 8
            case 15:
                p, b = "TagGroup", None
            case 18:
                p, b = "String", None
            case 20:
                p, b = "Array", None
            case other:
                p, b = "Unknown type", None

        if out_type == 'p':
            prc_bytes = p
        elif out_type == 'b':
            prc_bytes = b

        return prc_bytes

    def dbgDMBin(btype):
        if btype == 8:
            dbt = "int8 (boolean)"
        else:
            dbt = dmBin(btype, 'p')
        return dbt

    # DM Image Data Type

    def dmImageType(iT, oo):
        match iT:
            case 1:
                px, sc, vt, bit = "scalar", "int", 0, 16
            case 2:
                px, sc, vt, bit = "scalar", "float", 0, 32
            case 3:
                px, sc, vt, bit = "complex", "float", 0, 32
            case 5:
                px, sc, vt, bit = "complex", "float", 0, 32
            case 6:
                px, sc, vt, bit = "scalar", "uint", 0, 8
            case 7:
                px, sc, vt, bit = "scalar", "int", 0, 32
            case 8:
                px, sc, vt, bit = "rgba", "uint", 3, 8
            case 9:
                px, sc, vt, bit = "scalar", "int", 0, 8
            case 10:
                px, sc, vt, bit = "scalar", "uint", 0, 16
            case 11:
                px, sc, vt, bit = "scalar", "uint", 0, 32
            case 12:
                px, sc, vt, bit = "scalar", "float", 0, 64
            case 13:
                px, sc, vt, bit = "complex", "float", 0, 64
            case 14:
                px, sc, vt, bit = "scalar", "binary", 0, 8
            case 15:
                px, sc, vt, bit = "rgb", "uint", 0, 8
            case 16:
                px, sc, vt, bit = "rgb", "uint", 1, 8
            case 17:
                px, sc, vt, bit = "rgb", "uint", 0, 16
            case 18:
                px, sc, vt, bit = "rgb", "float", 0, 32
            case 19:
                px, sc, vt, bit = "rgb", "float", 0, 64
            case 20:
                px, sc, vt, bit = "rgba", "uint", 0, 8
            case 21:
                px, sc, vt, bit = "rgba", "uint", 1, 8
            case 22:
                px, sc, vt, bit = "rgba", "uint", 2, 8
            case 23:
                px, sc, vt, bit = "rgba", "uint", 3, 8
            case 24:
                px, sc, vt, bit = "rgba", "uint", 0, 16
            case 25:
                px, sc, vt, bit = "rgba", "float", 0, 32
            case 26:
                px, sc, vt, bit = "rgba", "float", 0, 64
            case 27:
                px, sc, vt, bit = "complex", "float", 0, 32
            case 28:
                px, sc, vt, bit = "complex", "float", 0, 64
            case 29:
                px, sc, vt, bit = "point2", "int", 0, 16
            case 30:
                px, sc, vt, bit = "point2", "int", 1, 16
            case 31:
                px, sc, vt, bit = "point2", "int", 0, 64
            case 32:
                px, sc, vt, bit = "point2", "float", 0, 32
            case 33:
                px, sc, vt, bit = "point2", "float", 0, 64
            case 34:
                px, sc, vt, bit = "rect", "int", 1, 16
            case 35:
                px, sc, vt, bit = "rect", "int", 1, 64
            case 36:
                px, sc, vt, bit = "rect", "float", 1, 32
            case 37:
                px, sc, vt, bit = "rect", "float", 0, 32
            case 38:
                px, sc, vt, bit = "rect", "float", 0, 64
            case 39:
                px, sc, vt, bit = "scalar", "int", 0, 64
            case 40:
                px, sc, vt, bit = "scalar", "uint", 0, 64
            case other:
                px = sc = vt = bit = None

        match oo:
            case 'pixel':
                d = px
            case 'scalar':
                d = sc
            case 'variant':
                d = vt
            case 'bit':
                d = bit
            case other:
                d = px + " " + str(sc) + str(bit)

        return d

    # Pack Image Data Type info
    def imgDataType(dt):
        imgInfo = struct()
        imgInfo.full = dmImageType(dt, 'full')
        imgInfo.pixel = dmImageType(dt, 'pixel')
        imgInfo.scalar = dmImageType(dt, 'scalar')
        imgInfo.variant = dmImageType(dt, 'variant')
        imgInfo.bit = dmImageType(dt, 'bit')
        return imgInfo

    # Read Tag that is not directory
    def readTag(ff, lv, label):
        Tg = struct()

        # tmp = ''.join([chr(let) for let in np.fromfile(ff.file,count=4,offset =
        # int(ff.offset),dtype='u1')]) # "%%%%" for Tag
        ff.offset += 4
        nTagType = np.fromfile(ff.file, count=1, dtype='>' + ff.w, offset=int(ff.offset))[0]
        ff.offset += ff.wSize
        tagType = np.fromfile(ff.file, count=nTagType, dtype='>' + ff.w, offset=int(ff.offset))
        ff.offset += int(nTagType) * ff.wSize

        nA = 1
        nM = 1
        isArray = 0
        isMultiItem = 0

        if tagType[0] == 20:
            isArray = 1
            nA = tagType[-1]

        if tagType[isArray] == 15:
            nM = tagType[2 + isArray]
            isMultiItem = 1

        sTypes = np.zeros(nM)
        sTypes_s = [None] * nM
        sTypes_b = np.zeros(nM)
        for iM in range(nM):
            sTypes[iM] = tagType[isArray + 3 * isMultiItem + (iM + 1) * (1 + isMultiItem) - 1]
            sTypes_s[iM] = dbgDMBin(sTypes[iM])
            sTypes_b[iM] = dmBin(sTypes[iM], 'b')

        if isArray == 1 and (not label.endswith("Name")):
            Tg.offset = int(ff.offset)
            if isMultiItem:
                Tg.dim = [nM, nA]
                Tg.tagType = "array of multiItems"
            else:
                Tg.dim = nA
                Tg.tagType = "array of scalars"

            Tg.dataType = sTypes_s[:]
            aSize = sum(sTypes_b) * nA
            Tg.size = aSize
            ff.offset += aSize

        else:
            # Read data in tag
            aTg = []
            for iA in range(nA):
                aTg.append(struct())

                mTg = []
                for iM in range(nM):
                    mTg.append(
                        np.fromfile(
                            ff.file,
                            count=1,
                            dtype=ff.bo +
                            dmBin(
                                sTypes[iM],
                                'p'),
                            offset=int(
                                ff.offset))[0])
                    ff.offset += int(dmBin(sTypes[iM], 'b'))

                if isMultiItem:
                    aTg[iA] = mTg
                else:
                    aTg[iA] = mTg[0]

            if isArray:
                Tg = aTg
            else:
                Tg = aTg[0]

        return Tg

    # Read Tag directory
    def readTagGp(ff, lv):
        # Tag Group or Tag List
        notList = np.fromfile(ff.file, dtype='u1', offset=int(ff.offset), count=1)[0]  # 0 = Tag List, 1 = Tag Group
        ff.offset += 2
        nChd = np.fromfile(ff.file, dtype='>' + ff.w, offset=int(ff.offset), count=1)[0]
        ff.offset += ff.wSize

        if notList:
            Gp = struct()
        else:
            Gp = []

        for iC in range(nChd):
            tagType = np.fromfile(ff.file, dtype='u1', count=1, offset=int(ff.offset))[0]
            ff.offset += 1
            labelSize = np.fromfile(ff.file, dtype='>u2', count=1, offset=int(ff.offset))[0]
            ff.offset += 2
            label = ""

            if notList:
                label0 = np.fromfile(ff.file, dtype='u1', count=labelSize, offset=int(ff.offset))
                label0 = ''.join([chr(let) for let in label0])
                ff.offset += labelSize

                label = re.sub('[^a-zA-Z_0-9]+', '', label0.replace(' ', '_'))
                if label == "":
                    label = 'LABEL_FORMATTED_'

                # increment labels with the same name
                if hasattr(Gp, label):
                    iL = 1
                    while hasattr(Gp, label + str(iL)):
                        iL += 1
                    label = label + str(iL)

            if ff.v == 4:
                tagSize = np.fromfile(ff.file, count=1, dtype='>' + ff.w, offset=int(ff.offset))[0]
                ff.offset += ff.wSize
                # Skip other Tags
                if lv == 0 and label not in ["ImageList", "ImageSourceList"]:
                    # fast forward and skip to next
                    ff.offset += int(tagSize)
                    continue

            match tagType:
                case 20:
                    chd = readTagGp(ff, lv + 1)
                case 21:
                    chd = readTag(ff, lv + 1, label)

            if notList:
                setattr(Gp, label, chd)
            else:
                Gp.append(chd)

        return Gp

    def dmInfo(file):
        """return DMinfo"""

        ff = struct()
        ff.file = file

        ff.id = open(ff.file, 'rb')

        # Message printing options
        ff.m = 0

        # Setup DM3 & 4 differences
        ff.v = np.fromfile(ff.file, dtype=">u4", count=1)[0]
        match ff.v:
            case 3:
                ff.w = 'u4'
            case 4:
                ff.w = 'u8'
            case other:
                DMinfo = 'Not a DM3/4 file.'
                return
        ff.wSize = np.dtype(ff.w).itemsize

        # Size of the root tag group, i.e. 24/16 bytes for DM4/3 (header + footer) smaller than the file size
        ff.size = np.fromfile(ff.file, dtype='>' + ff.w, count=1, offset=4)[0]
        ff.offset = 4 + ff.wSize

        # Data endianness; probably only little ff.bo for DM4
        endian = np.fromfile(ff.file, dtype='>u4', count=1, offset=int(ff.offset))[0]
        ff.offset += 4
        if endian:
            ff.bo = '<'
        else:
            ff.bo = '>'

        # Read TagGroup
        Tg = readTagGp(ff, 0)

        # Finished file reading
        ff.id.close()

        # Deal with `ImageSourceList`
        nImgs = len(Tg.ImageSourceList)
        R = np.zeros(nImgs, dtype=int)
        for i in range(nImgs):
            R[i] = int(Tg.ImageSourceList[i].ImageRef)

        # Deal with  `ImageList[i]:ImageData:DataType` & `ImageList[i].Name`
        for i in range(nImgs):
            dt = Tg.ImageList[R[i]].ImageData.DataType
            Tg.ImageList[R[i]].ImageData.ImageDataType = imgDataType(dt)
            Tg.ImageList[R[i]].ImageData.Name = "".join([chr(let) for let in Tg.ImageList[R[i]].Name])

        # Setup return
        d = struct()
        if ff.v == 4:
            d.fileSize = ff.size + 24
        else:
            d.fileSize = ff.size + 20

        d.version = ff.v
        d.liEndian = endian

        DMinfo = []
        for i in range(nImgs):
            DMinfo.append(Tg.ImageList[R[i]].ImageData)

        DMinfo.append(d)

        return DMinfo

    # filename from import dialog
    filename = self.D.fileName

    self.T.dm = dmInfo(filename)

    self.ImportWindow.ImpSubImg.setEnabled(True)

    # List all images' names in `self.ImpSubImg`
    # Select sub-image with the largest dimension; unless manually selected
    if self.sender() is not self.ImportWindow.ImpSubImg:
        pdim = np.zeros(len(self.T.dm) - 1)
        self.ImportWindow.ImpSubImg.blockSignals(True)
        for i in range(pdim.size):
            self.ImportWindow.ImpSubImg.addItem(self.T.dm[i].Name)
            pdim[i] = np.array(self.T.dm[i].Dimensions).prod()
        self.ImportWindow.ImpSubImg.blockSignals(False)
        self.ImportWindow.ImpSubImg.setCurrentIndex(pdim.argmax())

    # Info of selected sub-image
    dm = self.T.dm[self.ImportWindow.ImpSubImg.currentIndex()]
    finfo = self.T.dm[-1]

    # Read dimensions
    dims = np.array(dm.Dimensions)

    for i in range(4):
        if i > dims.size:
            dims[i] = 1  # Fill missing dimensions as 1

    self.ImportWindow.DNPxX.setMaximum(np.iinfo(np.int32).max)
    self.ImportWindow.DNPxY.setMaximum(np.iinfo(np.int32).max)
    self.ImportWindow.DNFrX.setMaximum(np.iinfo(np.int32).max)
    self.ImportWindow.DNFrY.setMaximum(np.iinfo(np.int32).max)

    self.ImportWindow.DNPxX.setValue(dims[0])
    self.ImportWindow.DNPxY.setValue(dims[1])
    self.ImportWindow.DNFrX.setValue(dims[2])
    self.ImportWindow.DNFrY.setValue(dims[3])

    # Find offset, file tail, data type, byte-order of dataset
    self.ImportWindow.DataOffset.setMaximum(self.T.FileSize)
    self.ImportWindow.DataOffset.setValue(dm.Data.offset)  # TODO
    try:
        self.ImportWindow.ImpDataType.setCurrentIndex(
            self.ImportWindow.ImpDataType.findData(
                dm.Data.dataType[0]))  # TODO
    except BaseException:
        pass

    self.T.fileTail = int(finfo.fileSize - dm.Data.offset - dm.Data.size)

    if dm.ImageDataType.pixel != "scalar":  # If pixels are not scalars (e.g. complex image)
        self.ImportWindow.ImpDataType.setCurrentIndex(self.ImportWindow.ImpDataType.findData("unknown"))

    # Is it little endian?
    if finfo.liEndian == 1:
        self.ImportWindow.ImpByteOrder.setCurrentIndex(0)
        bo = 'Little Endian'
    else:
        self.ImportWindow.ImpByteOrder.setCurrentIndex(1)
        bo = 'Big Endian'

    notes = "Dim: X = {:d}, Y = {:d}, Z = {:d}, W = {:d}\nDM{:d}, {:s}\nData-type: {:s}\nSelected sub-image's offset is {:d} bytes.".format(
        dims[0], dims[1], dims[2], dims[3], finfo.version, bo, dm.ImageDataType.full, dm.Data.offset)

    # if dims[3] == 1: #TODO
    #    guessFramesFromDimZ(dims[2])

    self.ImportWindow.FrHead.setValue(0)
    self.ImportWindow.FrFoot.setValue(0)
