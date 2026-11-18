import sys
from dataclasses import dataclass, field, fields
from typing import Any, Optional
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


# ---------------------------------------------------------------------------
# State namespaces
#
# Each namespace is a slotted dataclass: every attribute the app uses is
# declared here with its default, and assigning to a name that is not
# declared raises AttributeError instead of silently creating a new field.
# Add the field here first when a callback needs new state.
# ---------------------------------------------------------------------------
def _unit_pair() -> np.ndarray:
    return np.array([1, 1])


@dataclass(slots=True)
class D:
    """ Parameters of the current imported dataset; should be constants (except for data type conversion) """
    annWidth: float = 0.5           # annuli width for BF/ADF integration
    ByteOrder: str = 'l'
    ByteSize: int = 4
    DataType: str = 'single'
    DNFrX: int = 1                  # dataset (on-disk) dimensions
    DNFrY: int = 1
    DNPxX: int = 1
    DNPxY: int = 1
    EstMem: float = 0
    fileDir: str = ''
    fileExt: str = ''
    fileName: str = ''
    filePath: str = ''
    FrD: int = 1
    FrFoot: int = 0
    FrHead: int = 0
    FrX1: int = 1
    FrY1: int = 1
    GPU: Any = None                 # CUDA device index/name, or None for CPU
    h5ds: Any = field(default_factory=list)   # [] or the HDF5 dataset path
    KeepP: bool = False
    mem: str = 'Physical Memory'
    NFr: np.ndarray = field(default_factory=_unit_pair)   # real-space image shape (NFrY, NFrX)
    NFrS: int = 1
    NFrX: int = 1                   # imported dimensions (after partial import / binning)
    NFrY: int = 1
    NoteFileMeta: str = ''
    NoteImp: str = ''
    NPx: np.ndarray = field(default_factory=_unit_pair)   # (x, y) size vector [NPxX, NPxY]; not an image shape
    NPxS: int = 1
    NPxX: int = 1
    NPxY: int = 1
    Offset: int = 0
    PxD: int = 1
    PxX1: int = 1
    PxY1: int = 1
    subImg: Any = ''
    # Only read by the module-level GPU helpers in annularDetectorCallbacks
    # (and their tests); the app itself keeps the dataset on ``self.Data``.
    Data: Optional[np.ndarray] = None

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


@dataclass(slots=True)
class T:
    """ Temporary global variables, e.g. for progress bar and import etc., should never be cleared """
    FileSize: int = 0
    dm: Any = field(default_factory=list)
    h5: Any = field(default_factory=list)
    fileTail: int = 0
    EstSize: int = 0
    EstMem: float = 0
    Preview: D = field(default_factory=D)
    prev_D: Optional[D] = field(default_factory=D)
    frameJ: int = 0


@dataclass(slots=True)
class C:
    """ Constants for system info that set at app startup """
    ScreenSize: Any = field(default_factory=list)
    MonitorPositions: Any = field(default_factory=list)
    ScreenPxScale: float = 1
    monitorWidth: Any = field(default_factory=list)
    monitorHeight: Any = field(default_factory=list)
    monitorAvailWidth: Any = field(default_factory=list)
    monitorAvailHeight: Any = field(default_factory=list)
    dpi: Any = field(default_factory=list)
    hOffset: Any = field(default_factory=list)
    vOffset: Any = field(default_factory=list)
    toolbarWidth: Any = field(default_factory=list)
    toolbarHeight: Any = field(default_factory=list)
    decorPad: Any = field(default_factory=list)
    titleHeight: Any = field(default_factory=list)
    mplDecor: Any = field(default_factory=list)
    sz: Any = field(default_factory=list)
    shc: Any = field(default_factory=list)
    left: Any = field(default_factory=list)
    lines: Any = field(default_factory=list)
    wb0: Any = field(default_factory=list)
    BgC: Any = field(default_factory=lambda: qtg.QColor.fromRgbF(0.94, 0.94, 0.94, 1))
    WarnC: Any = field(default_factory=lambda: qtg.QColor.fromRgbF(1, 0.65, 0, 1))
    SysEndian: str = 'l'
    EndianTxt: dict = field(default_factory=lambda: {"l": "Little Endian", "b": "Big Endian"})
    MemTot: int = 0
    MemFree: int = 0
    nGPU: int = 1
    GPUmem: list = field(default_factory=list)
    GPUname: list = field(default_factory=list)


@dataclass(slots=True)
class P:
    """ Common parameters, should be cleared when a dataset is unloaded """
    ScanDirInit: int = 0
    CoMRadiusInit: bool = False     # CoM/DPC entered with this dataset (inner radius set to 0 the first time)
    DfCtr: Any = field(default_factory=list)       # (x, y) centre of the diffraction image
    RsCtr: Any = field(default_factory=list)       # (x, y) centre of the real-space image
    VrApXY: Any = field(default_factory=list)      # (x, y) virtual aperture centre
    DfrnAxLim: Any = field(default_factory=list)
    RealAxLim: Any = field(default_factory=list)
    TransBeamInit: int = 0
    RMax: float = 0
    DetrMode: Any = None
    detWidth: float = 0
    PreviewAxLim: Any = field(default_factory=lambda: [0, 1, 0, 1])


@dataclass(slots=True)
class Prev:
    """ Previous values (see ``utils.isDiffToPrev``), should be cleared when a dataset is unloaded """
    im: Any = None          # image last used for the statistics/histogram
    hist: Any = None        # histogram annotation parameters
    B0: Any = None          # transmitted-beam centre
    AnnR: Any = None        # annular radii [ri, ro]
    CoM_P: Any = None       # CoM/DPC parameters [ri, ro, sd, syf, dr]
    VrAp: Any = None        # virtual aperture parameters


def _roi_slots() -> dict:
    return {k + "ROI": None for k in ("Real", "CoMPhMag", "CoMPh", "CoMMag", "CoMX", "CoMY", "dCoM", "iCoM")}


def _vect_slots() -> dict:
    return {k: None for k in ("CoMPhMag", "Real", "CoMX", "CoMY", "CoMPh", "dCoM", "CoMMag", "iCoM")}


@dataclass(slots=True)
class A:
    """ Image annotations on `axes` `uiaxes`, excluding annotations on `figure` `uifigure` """
    # generic circle starting point
    circX: np.ndarray = field(default_factory=lambda: np.cos(np.arange(0, 2.01 * np.pi, np.pi / 100)))
    circY: np.ndarray = field(default_factory=lambda: np.sin(np.arange(0, 2.01 * np.pi, np.pi / 100)))

    # bf/adf detector
    adf: Any = None
    k: Optional[np.ndarray] = None      # (NPxY, NPxX) radial bin index about the beam centre

    # transmitted beam
    tb: Any = None

    # DPC segments
    SegDetrCir: Any = None
    SegDetrL: Any = None
    SegDetrL0: Any = None
    SegDetrP0: Any = None

    # scan direction for CoM/DPC
    ScanDirXline: Any = None
    ScanDirYline: Any = None
    ScanDirXcirc: Any = None
    ScanDirYcirc: Any = None
    ScanDirXtext: Any = None
    ScanDirYtext: Any = None

    # virtual apertures
    VrApMirL: Any = None
    VrApMirP: Any = None
    VrAp: Any = None

    # ROIs
    ROIs: dict = field(default_factory=_roi_slots)
    RealROI: dict = field(default_factory=dict)     # live real-space ROI per image id
    _tmp_selector: Any = None                       # in-progress polygon selector

    # custom detectors: mask ID -> customDetectorCallbacks.CustomMask, in table order
    Custom: dict = field(default_factory=dict)

    # vectorField quivers
    vectField: dict = field(default_factory=_vect_slots)

    # histogram annotations
    hist: Any = None
    histNote: Any = None
    histBox: Any = None
    _histDrag: bool = False                         # the histogram box is being dragged
    histGamma: Any = None

    def removeGroup(self, tag):
        """ allow for groups of annotations to be removed and set to None using a string "tag" """
        for item in (f.name for f in fields(self)):
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


@dataclass(slots=True)
class Mask:
    """ Masks loaded from file, cleared when a dataset is unloaded """
    RealROIFile: Any = None     # real-space ROI mask image imported from file


@dataclass(slots=True)
class G:
    """ Image ids/names/groups, and lists of the windows and axes built at startup """
    ImgID: list = field(default_factory=lambda: list(ImgID))        # ID/fieldnames under `self.Fig` `self.ImageAx` etc
    ImgName: list = field(default_factory=lambda: list(ImgName))    # Names/Titles
    ImgType: list = field(default_factory=lambda: list(ImgType))    # Types ("Primary", "CoM" related, "Mask", "Test")
    ImgSpace: list = field(default_factory=lambda: list(ImgSpace))  # Spaces ("Real"/"Dfrn")
    DfrnID: list = field(default_factory=lambda: list(DfrnID))
    RealID: list = field(default_factory=lambda: list(RealID))

    # DataFrame of above properties (allows for easier logics and slicing)
    Img: Any = field(init=False, default=None)

    # filled in by startup.createImageWindows
    ImgAx: list = field(default_factory=list)
    ImgFig: list = field(default_factory=list)
    DfrnAx: list = field(default_factory=list)
    RealAx: list = field(default_factory=list)
    CoM_btns: list = field(default_factory=list)
    AllFig: list = field(default_factory=list)

    def __post_init__(self):
        data = {"id": self.ImgID, "name": self.ImgName, "space": self.ImgSpace, "type": self.ImgType}
        self.Img = pd.DataFrame(data)

    def getReal(self):
        return list(self.Img.id[self.Img.space == "Real"])

    def getDfrn(self):
        return list(self.Img.id[self.Img.space == "Dfrn"])


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
