import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import uic
import numpy as np
import pandas as pd

# set out all image name, id, space, and type information
DfrnID = ['Dfrn', 'DfrnMask']
RealID = ['iCoM', 'dCoM', 'CoMY', 'CoMX', 'CoMMag', 'CoMPh', 'CoMPhMag', 'RealMask', 'Real', 'Preview', 'ColorWheel']
ImgID = DfrnID + RealID

diffNames = ['Diffraction', 'Diffraction Mask']
realNames = [
    'iCoM',
    'dCoM',
    'CoM Y',
    'CoM X',
    'CoM Magnitude',
    'CoM Phase',
    'CoM Phase (Magnitude-shaded)',
    'Real-space Mask',
    'Real-space',
    'Preview',
    'Color Wheel for Phase Direction']
ImgName = diffNames + realNames

ImgSpace = [
    'Dfrn',
    'Dfrn',
    'Real',
    'Real',
    'Real',
    'Real',
    'Real',
    'Real',
    'Real',
    'Real',
    'Real',
    'Preview',
    'ColorWheel']

ImgType = ['Primary', 'Mask', 'CoM', 'CoM', 'CoM', 'CoM', 'CoM', 'CoM', 'CoM', 'Mask', 'Primary', 'Preview', 'CoM']


class propDict(dict):
    """allows for dot indexing"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class D:
    """ Parameters of the current imported dataset; should be constants (except for data type conversion) """

    def __init__(self):
        self.annWidth = 0.5  # annuli width for BF/ADF integration
        self.ByteOrder = 'l'
        self.ByteSize = 4
        self.DataType = 'single'
        self.DNFrX = 1
        self.DNFrY = 1
        self.DNPxX = 1
        self.DNPxY = 1
        self.EstMem = 0
        self.fileDir = ''
        self.fileExt = ''
        self.fileName = ''
        self.filePath = ''
        self.FrD = 1
        self.FrFoot = 0
        self.FrHead = 0
        self.FrX1 = 1
        self.FrY1 = 1
        self.GPU = 0
        self.h5ds = []
        self.KeepP = 0
        self.mem = 'Physical Memory'
        self.NFr = np.array([1, 1])
        self.NFrS = 1
        self.NFrX = 1
        self.NFrY = 1
        self.NoteFileMeta = ''
        self.NoteImp = ''
        self.NPx = np.array([1, 1])
        self.NPxS = 1
        self.NPxX = 1
        self.NPxY = 1
        self.Offset = 0
        self.PxD = 1
        self.PxX1 = 1
        self.PxY1 = 1
        self.subImg = {}

    def swapDiff(self):
        # Swap diffraction X/Y dimensions
        self.DNPxX, self.DNPxY = self.DNPxY, self.DNPxX
        self.NPxX, self.NPxY = self.NPxY, self.NPxX
        self.PxX1, self.PxY1 = self.PxY1, self.PxX1
        self.NPx = np.flip(self.NPx)

    def swapReal(self):
        # Swap real X/Y dimensions
        self.DNFrX, self.DNFrY = self.DNFrY, self.DNFrX
        self.NFrX, self.NFrY = self.NFrY, self.NFrX
        self.FrX1, self.FrY1 = self.FrY1, self.FrX1
        self.NFr = np.flip(self.NFr)


class T:
    """ Temporary global variables, e.g. for progress bar and import etc., should never be cleared """

    def __init__(self):
        self.FileSize = 0
        self.dm = []
        self.h5 = []
        self.fileTail = 0
        self.EstSize = 0
        self.EstMem = 0
        self.Preview = D()
        self.prev_D = D()
        self.frameJ = 0


class C:
    """ Constants for system info that set at app startup """

    def __init__(self):
        self.ScreenSize = []
        self.MonitorPositions = []
        self.ScreenPxScale = 1
        self.monitorWidth = []
        self.monitorHeight = []
        self.monitorAvailWidth = []
        self.monitorAvailHeight = []
        self.dpi = []
        self.hOffset = []
        self.vOffset = []
        self.toolbarWidth = []
        self.toolbarHeight = []
        self.decorPad = []
        self.titleHeight = []
        self.mplDecor = []
        self.sz = []
        self.shc = []
        self.lines = []
        self.wb0 = []
        self.BgC = qtg.QColor.fromRgbF(0.94, 0.94, 0.94, 1)
        self.WarnC = qtg.QColor.fromRgbF(1, 0.65, 0, 1)
        self.SysEndian = 'l'
        self.EndianTxt = {"l": "Little Endian", "b": "Big Endian"}
        self.MemTot = 0
        self.MemFree = 0
        self.nGPU = 1
        self.GPUmem = []
        self.GPUname = []


class P:
    """ Common parameters, should be cleared when a dataset is unloaded """

    def __init__(self):
        self.ScanDirInit = 0
        self.DfCtr = []
        self.RsCtr = []
        self.VrApXY = []
        self.DfrnAxLim = []
        self.RealAxLim = []
        self.TransBeamInit = 0
        self.RMax = 0
        self.DetrMode = None
        self.detWidth = 0
        self.PreviewAxLim = [0, 1, 0, 1]


class Prev:
    """ Previous values, should be cleared when a dataset is unloaded """

    def __init__(self):
        self.ims = None
        self.hist = None
        self.B0 = None
        self.AnnR = None
        self.CoM_P = None


class A:
    """ Image annotations on `axes` `uiaxes`, excluding annotations on `figure` `uifigure` """

    def __init__(self):
        # generic circle starting point
        self.circX = np.cos(np.arange(0, 2.01 * np.pi, np.pi / 100))
        self.circY = np.sin(np.arange(0, 2.01 * np.pi, np.pi / 100))

        # bf/adf detector
        self.adf = None

        # transmitted beam
        self.tb = None

        # DPC segments
        self.SegDetrCir = None
        self.SegDetrL = None
        self.SegDetrL0 = None
        self.SegDetrP0 = None

        # scan direction for CoM/DPC
        self.ScanDirXline = None
        self.ScanDirYline = None
        self.ScanDirXcirc = None
        self.ScanDirYcirc = None

        # virtual apertures
        self.VrApMirL = None
        self.VrApMirP = None
        self.VrAp = None

        # ROIs
        self.ROIs = dict()
        self.ROIs["RealROI"] = None
        self.ROIs["CoMPhMagROI"] = None
        self.ROIs["CoMPhROI"] = None
        self.ROIs["CoMMagROI"] = None
        self.ROIs["CoMXROI"] = None
        self.ROIs["CoMYROI"] = None
        self.ROIs["dCoMROI"] = None
        self.ROIs["iCoMROI"] = None

        # vectorField quivers
        self.vectField = dict()
        self.vectField["CoMPhMag"] = None
        self.vectField["Real"] = None
        self.vectField["CoMX"] = None
        self.vectField["CoMY"] = None
        self.vectField["CoMPh"] = None
        self.vectField["dCoM"] = None
        self.vectField["CoMMag"] = None
        self.vectField["iCoM"] = None

        # histogram annotations
        self.histBox = None
        self.histGamma = None

    def removeGroup(self, tag):
        """ allow for groups of annotations to be removed and set to None using a string "tag" """
        for item in vars(self):
            if item.startswith(tag):

                if not isinstance(getattr(self, item), dict):
                    try:
                        getattr(self, item).remove()
                    except BaseException:
                        pass
                    finally:
                        setattr(self, item, None)
                else:
                    for key in getattr(self, item).keys():
                        try:
                            getattr(self, item)[key].remove()
                        except BaseException:
                            pass
                        finally:
                            getattr(self, item)[key] = None


class Mask:
    pass


class G:
    def __init__(self):
        self.ImgID = ImgID          # ID/fieldnames under `self.Fig` `self.ImageAx` `self.ImgD` etc
        self.ImgName = ImgName      # Names/Titles
        self.ImgType = ImgType      # Types ("Primary", "CoM" related, "Mask", "Test")
        self.ImgSpace = ImgSpace    # Spaces ("Real"/"Dfrn")

        self.DfrnID = DfrnID
        self.RealID = RealID

        # DataFrame of above properties (allows for easier logics and slicing)
        data = {"id": self.ImgID, "name": self.ImgName, "space": self.ImgSpace, "type": self.ImgType}
        self.Img = pd.DataFrame(data)

    def getReal(self):
        return [ii for ii in self.Img if self.Img[ii].space == "Real"]

    def getDfrn(self):
        return [ii for ii in self.Img if self.Img[ii].space == "Dfrn"]


ByteSize = {"u1": 1,
            "i1": 1,
            "u2": 2,
            "i2": 2,
            "f4": 4,
            "i4": 4,
            "u4": 4,
            "f8": 8,
            "i8": 8,
            "u8": 8,
            "unknown": 0}


def appStruct(self):
    setattr(self, 'B0', [0, 0])
    setattr(self, 'RB0', [0, 0])
    setattr(self, 'DfPxR', 1)
    setattr(self, 'RsPxR', 1)
    setattr(self, 'path', '')
    setattr(self, 'T', T())
    setattr(self, 'D', None)  # initialize as None, filled with gatherImportOptions
    setattr(self, 'Data', None)
    setattr(self, 'Memfile', None)
    setattr(self, 'C', C())
    setattr(self, 'P', P())
    setattr(self, 'Prev', Prev())
    setattr(self, 'A', A())
    setattr(self, 'Mask', Mask())
    setattr(self, 'G', G())
    setattr(self, 'ByteSize', ByteSize)

    Fig = propDict({})
    ImageAx = propDict({})

    for ii in ImgID:
        Fig[ii] = None
        ImageAx[ii] = None

    setattr(self, 'Fig', Fig)
    setattr(self, 'ImageAx', ImageAx)
    setattr(self, 'blockAllSignals', False)
