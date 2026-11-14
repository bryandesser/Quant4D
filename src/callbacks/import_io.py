"""Import UI callbacks and file I/O helpers."""
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
# Deferred cross-module imports (safe: import_io is itself only loaded lazily)
from callbacks.utils import notifDLG, checkNaN  # noqa: E402
from callbacks.startup import enableWindows  # noqa: E402
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


def gatherImportOptions(self, preview):
    """Gather import options from the Import window UI fields.

    Parameters
    ----------
    self : app instance
    preview : bool
        True when called for preview (skips GPU device selection).

    Returns
    -------
    D
        Data-container populated from the Import window UI.
    """
    from callbacks.appClass import D  # noqa: E402

    d = D()  # initialize

    d.filePath = self.ImportWindow.ImpFilePath.text()
    [d.fileDir, d.fileName] = os.path.split(d.filePath)
    d.fileDir = d.fileDir + os.sep
    d.subImg = self.ImportWindow.ImpSubImg.currentText()

    # BYTES offset of: 1) the dataset from the beginning of file,
    #                  2) before and 3) after each frame
    d.Offset = self.ImportWindow.DataOffset.value()
    d.FrHead = self.ImportWindow.FrHead.value()
    d.FrFoot = self.ImportWindow.FrFoot.value()

    # Endianness ('b' big / 'l' little), Data type, Byte size
    d.ByteOrder = self.ImportWindow.ImpByteOrder.currentData()
    d.DataType = self.ImportWindow.ImpDataType.currentData()
    d.ByteSize = self.ByteSize[d.DataType]

    # Physical or virtual memory loading
    d.mem = self.ImportWindow.ImpMemType.currentText()

    # Select GPU if acceleration enabled AND not in Import Preview Mode
    d.GPU = self.ImportWindow.ImpGPU.currentData()
    if not preview and d.GPU is not None:
        torch.device(0 if torch.cuda.is_available() else "cpu")

    # Pixel/frame dimensions and binning/sampling distance
    d.DNPxX = self.ImportWindow.DNPxX.value()
    d.DNPxY = self.ImportWindow.DNPxY.value()
    d.PxD = self.ImportWindow.IPxD.value()
    d.DNFrX = self.ImportWindow.DNFrX.value()
    d.DNFrY = self.ImportWindow.DNFrY.value()
    d.FrD = self.ImportWindow.IFrD.value()

    # Starting points and number of pixels/frames after binning/sampling
    d.PxX1 = self.ImportWindow.IPxX1.value()
    d.PxY1 = self.ImportWindow.IPxY1.value()
    d.NPxX = self.ImportWindow.INPxX.value()
    d.NPxY = self.ImportWindow.INPxY.value()
    d.FrX1 = self.ImportWindow.IFrX1.value()
    d.FrY1 = self.ImportWindow.IFrY1.value()
    d.NFrX = self.ImportWindow.INFrX.value()
    d.NFrY = self.ImportWindow.INFrY.value()

    # Frequently used dimension parameters
    d.NPx = np.array([d.NPxX, d.NPxY])
    d.NPxS = d.NPxX * d.NPxY
    d.NFr = np.array([d.NFrY, d.NFrX])
    d.NFrS = d.NFrX * d.NFrY

    # Estimated memory usage for current dataset
    d.EstMem = self.T.EstMem

    # Keep-previous option
    d.KeepP = self.ImportWindow.ImpKeepP.isChecked()

    # Notes at import
    d.NoteFileMeta = self.ImportWindow.ImpFileMetaNotes.toPlainText()
    d.NoteImp = self.ImportWindow.ImpNotes.toPlainText()

    # HDF5 dataset path within the file
    d.h5ds = []
    if self.ImportWindow.HDF5Button.isChecked() and ("Physical Memory" in d.mem):
        d.h5ds = d.subImg

    return d


def importSelectFile(self):
    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    # if the user pushes the "Select" button in the Import window, open file dialog, filter for known filetypes
    if self.sender() is self.ImportWindow.ImpFileSelect:
        fDialog = qtw.QFileDialog(self)
        fDialog.setWindowTitle("Select 4DSTEM Dataset")
        fDialog.setNameFilter("(*.raw *.mib *.mrc *.dm3 *.dm4 *.npy *.h5 *.hdf5);;(*.*)")
        fDialog.setDirectory(qtc.QDir.currentPath())
        fileName = None
        if fDialog.exec_() == qtw.QDialog.Accepted:
            fileName, = fDialog.selectedFiles()
        else:  # user selected cancel
            self.ImportWindow.activateWindow()
            self.ImportWindow.ImportDataButton.setDefault(False)
            self.ImportWindow.ImportDataButton.setAutoDefault(False)
            self.ImportWindow.ImpFileSelect.setFocus(True)
            self.ImportWindow.ImpFileSelect.setAutoDefault(True)
            self.ImportWindow.ImpFileSelect.setDefault(True)
            return

        # reflect user selection in path field box
        if fileName is not None:
            self.fname = fileName
            self.ImportWindow.ImpFilePath.setText(self.fname)
            # enable rest of wigets in window
            for widget in self.ImportWindow.children():
                widget.setEnabled(True)
        else:
            # keep wigets disabled
            for widget in self.ImportWindow.children():
                widget.setEnabled(False)

        # switch to directory containing dataset for future saving
        os.chdir(qtc.QDir.currentPath())

        # ensure ImportWindow remains on top
        self.ImportWindow.activateWindow()

        # set default button to "Import Data"
        self.ImportWindow.ImportDataButton.setDefault(True)
        self.ImportWindow.ImportDataButton.setAutoDefault(True)
        self.ImportWindow.ImportDataButton.setFocus(True)
        self.ImportWindow.ImpFileSelect.setAutoDefault(False)
        self.ImportWindow.ImpFileSelect.setDefault(False)

    # get file directory, name, extension, and size. display in filesize field
    if os.path.isfile(self.ImportWindow.ImpFilePath.text()):
        self.fileDir = os.path.dirname(self.ImportWindow.ImpFilePath.text())
        self.fileName = os.path.basename(self.ImportWindow.ImpFilePath.text())
        _, self.fileExt = os.path.splitext(self.ImportWindow.ImpFilePath.text())
        os.chdir(self.fileDir)
        self.T.FileSize = os.path.getsize(self.fileName)
        self.ImportWindow.ImpActualFilesize.setText(
            "{} bytes, {:.2f} GiB".format(
                self.T.FileSize, self.T.FileSize / 1024**3))

        # activate Import Preview
        self.DfrnDetrTabGroup.setVisible(True)
        self.DfrnDetrTabGroup.setCurrentIndex(0)

        # activate preset buttons if file extension matches a known filetype, else custom
        match self.fileExt.casefold():
            case ".raw":
                self.ImportWindow.EMPADButton.setChecked(True)
            case ".mib":
                self.ImportWindow.MedipixButton.setChecked(True)
            case ".mrc":
                self.ImportWindow.MRCButton.setChecked(True)
            case ".dm3" | ".dm4":
                self.ImportWindow.DM34Button.setChecked(True)
            case ".h5":
                self.ImportWindow.HDF5Button.setChecked(True)
            case other:
                self.ImportWindow.CustomButton.setChecked(True)

    # if filename is incorrect/does not exist...
    else:
        self.ImportWindow.ImpActualFilesize.clear()
        self.DfrnDetrTabGroup.setVisible(False)
        self.PreviewTab.setVisible(False)
        self.PreviewTab.setEnabled(False)

    importFileType(self)


def importFileType(self):
    def guessFramesFromSize():
        """ Make an initial guess at the file dimensions (assume ~square field of view: NFrX≈NFrY) """
        if self.ImportWindow.DNPxX.value() > 1 and self.ImportWindow.DNPxY.value() > 1:
            bitSize = self.ByteSize[self.ImportWindow.ImpDataType.currentData()]

            # factoring in dataoffset/tail/header/footer lengths, get total number of frames (xy)
            z = (self.T.FileSize - self.ImportWindow.DataOffset.value() - self.T.fileTail) / (self.ImportWindow.DNPxX.value()
                                                                                              * self.ImportWindow.DNPxY.value() * bitSize + self.ImportWindow.FrHead.value() + self.ImportWindow.FrFoot.value())

            # assume dataset is as close to square as possible, factorize xy to (x,y)
            guessFramesFromDimZ(int(z))

    def guessFramesFromDimZ(z):
        """ Guess number of frames (x,y) from 3D dataset by finding the two largest integer factors that go into z without remainder """
        x = round(np.sqrt(z))
        while z % x > 0:
            x -= 1

        self.ImportWindow.DNFrX.setValue(x)
        self.ImportWindow.DNFrY.setValue(z // x)

    def getDimFromName(filename):
        """
        Guess dataset size from fileName in the following style (only the first match):
            fileName = 'fooAxBxCxDbar', where A,B,C,D are integers:
                            A = NPxX
                            B = NPxY
                            C = NFrX
                            D = NFrY
        """

        try:
            # standard EMPAD naming scheme
            s = re.search(r'_x(\d+)_y(\d+).raw', filename)
            DNFrX, DNFrY = [int(ii) for ii in s.groups()]
            DNPxX = DNPxY = int(128)

        except BaseException:
            try:
                # above described naming scheme
                t = re.search(r'(\d+)x(\d+)x(\d+)x(\d+)', filename)
                DNPxX, DNPxY, DNFrX, DNFrY = [int(ii) for ii in t.groups()]
            except BaseException:
                # failure, quit now
                return

        finally:
            # if the above passed, set the import window UI values
            self.ImportWindow.DNPxX.setValue(DNPxX)
            self.ImportWindow.DNPxY.setValue(DNPxY)
            self.ImportWindow.DNFrX.setValue(DNFrX)
            self.ImportWindow.DNFrY.setValue(DNFrY)

    def returnKeys(obj):
        datasetKeys = []

        def allkeys(obj):
            keys = (obj.name,)
            if isinstance(obj, h5py.Group):
                for key, value in obj.items():
                    if isinstance(value, h5py.Group):
                        keys = keys + allkeys(value)
                    else:
                        keys = keys + (value.name,)
                        datasetKeys.append(value.name)
            return keys
        allkeys(obj)
        return datasetKeys

    # block slots/signals whilst updating UI values
    self.blockAllSignals = True

    # Default values/properties
    notes = None
    err = 0  # TODO
    self.T.dm = []
    self.T.h5 = []
    self.T.fileTail = 0
    self.ImportWindow.DataOffset.setValue(0)
    self.ImportWindow.FrHead.setValue(0)
    self.ImportWindow.FrFoot.setValue(0)
    self.ImportWindow.DNPxX.setValue(1)
    self.ImportWindow.DNPxY.setValue(1)
    self.ImportWindow.DNFrX.setValue(1)
    self.ImportWindow.DNFrY.setValue(1)

    # Medipix data are saved as a .mib file of varying bit-depth as unsigned integers of the next highest class
    #   (i.e. 12-bit is saved as a 16-bit unsigned integer) with big-endian ordering.
    # EMPAD data are saved as a .raw file with 32-bit depth with little endian ordering.
    # Fiji/ImageJ tend to save their files with big-endian ordering, though this is also system- and user-dependent.
    # H5 and other binary/raw data types are allowed, but user-dependent.

    # available data types and their plain text names
    dataType = ['unknown', 'i1', 'u1', 'i2', 'u2', 'f4', 'i4', 'u4', 'f8', 'i8', 'u8']
    dataTypeText = [
        'Select Data Type...',
        '8-bit Signed',
        '8-bit Unsigned',
        '16-bit Signed',
        '16-bit Unsigned',
        '32-bit Real',
        '32-bit Signed',
        '32-bit Unsigned',
        '64-bit Real',
        '64-bit Signed',
        '64-bit Unsigned']

    # add to combobox
    self.ImportWindow.ImpDataType.clear()
    for dtt, dt in zip(dataTypeText, dataType):
        self.ImportWindow.ImpDataType.addItem(dtt, dt)

    # default to "Select Data Type..." prompt
    self.ImportWindow.ImpDataType.setCurrentIndex(0)

    # start with h5 directory combobox cleared and disabled
    if self.sender() == self.ImportWindow.ImpFileSelect:
        self.ImportWindow.ImpSubImg.clear()
        self.ImportWindow.ImpSubImg.setEnabled(False)

    # default to "little endian"
    self.ImportWindow.ImpByteOrder.setCurrentIndex(0)

    # unblock slots/signals
    self.blockAllSignals = False

    if os.path.isfile(self.ImportWindow.ImpFilePath.text()):
        if self.ImportWindow.EMPADButton.isChecked():
            self.ImportWindow.FrFoot.setValue(1024)
            self.ImportWindow.DNPxX.setValue(128)
            self.ImportWindow.DNPxY.setValue(128)
            self.ImportWindow.ImpDataType.setCurrentIndex(self.ImportWindow.ImpDataType.findData('f4'))

            notes = 'Pixels:\t128x128\n32-bit Real\n** EMPAD data have 1024-byte frame footers'
            guessFramesFromSize()
            getDimFromName(self.ImportWindow.ImpFilePath.text())

        elif self.ImportWindow.MedipixButton.isChecked():
            # available data types and their plain text names - Medipix edition
            dataType = ['unknown', 'u1', 'u2', 'u4']
            dataTypeText = [
                'Select Data Type...',
                '1 or 6-bit Padded Unsigned',
                '12-bit Padded Unsigned',
                '24-bit Padded Unsigned']

            # add to combobox
            self.ImportWindow.ImpDataType.blockSignals(True)
            self.ImportWindow.ImpDataType.clear()
            for dtt, dt in zip(dataTypeText, dataType):
                self.ImportWindow.ImpDataType.addItem(dtt, dt)
            self.ImportWindow.ImpDataType.blockSignals(True)

            # check .mib file header
            fmeta = np.fromfile(self.ImportWindow.ImpFilePath.text(), dtype=np.uint8, count=128)
            fmeta = re.split(",", ''.join(chr(i) for i in fmeta))

            if (len(fmeta) >= 7) and (fmeta[6][0].casefold() in ("u", "r")):
                # Re-read with known header size
                fmeta = np.fromfile(self.ImportWindow.ImpFilePath.text(), dtype=np.uint8, count=int(fmeta[2]))
                fmeta = re.split(",", ''.join(chr(i) for i in fmeta))
                datatype = fmeta[6].casefold()
                bitsize = int(fmeta[-2])
                if datatype.startswith('u'):
                    match bitsize:
                        case 1 | 6:
                            self.ImportWindow.ImpDataType.setCurrentIndex(1)
                        case 12:
                            self.ImportWindow.ImpDataType.setCurrentIndex(2)
                        case 24:
                            self.ImportWindow.ImpDataType.setCurrentIndex(3)

                self.ImportWindow.FrHead.setValue(int(fmeta[2]))
                self.ImportWindow.ImpByteOrder.setCurrentIndex(1)  # 'b'
                self.ImportWindow.DNPxX.setValue(int(fmeta[4]))
                self.ImportWindow.DNPxY.setValue(int(fmeta[5]))
                notes = 'Dim: X = ' + str(int(fmeta[4])) + ', Y = ' + str(int(fmeta[5])) + '\nData type: ' + fmeta[6] + \
                    '\nPixel depth: ' + str(bitsize) + ' bit\n' 'Frame header: ' + str(int(fmeta[2])) + ' bytes\nBig endian'
                guessFramesFromSize()
                getDimFromName(self.ImportWindow.ImpFilePath.text())
            else:
                notes = 'Unrecognizable as a Medipix/.mib file.'
                err = -1

        elif self.ImportWindow.MRCButton.isChecked():
            # Read in MRC header - first 1024 bytes
            map = np.fromfile(self.ImportWindow.ImpFilePath.text(), count=212, dtype=np.uint8)
            map = ''.join(chr(let) for let in map[-4:])

            if map == "MAP ":
                # Bytes for Endianness
                e = np.fromfile(self.ImportWindow.ImpFilePath.text(), count=2, dtype=np.uint8, offset=212)
                if e[0] == 68 and e[1] in [65, 68]:
                    self.ImportWindow.ImpByteOrder.setCurrentIndex(0)  # 'l'
                    bo = 'Little Endian'
                elif e[0] == 17 and e[1] == 17:
                    self.ImportWindow.ImpByteOrder.setCurrentIndex(1)  # 'b'
                    bo = 'Big Endian'
                else:
                    bo = 'Unknown Endianness'

                # X, Y and Z: data is structured as 3D
                dim = np.fromfile(self.ImportWindow.ImpFilePath.text(), count=3, dtype=np.uint32)
                self.ImportWindow.DNPxX.setValue(dim[0])
                self.ImportWindow.DNPxY.setValue(dim[1])
                self.ImportWindow.DNFrX.setValue(dim[2])

                guessFramesFromDimZ(dim[2])
                getDimFromName(self.ImportWindow.ImpFilePath.text())

                dataType = np.fromfile(self.ImportWindow.ImpFilePath.text(), count=1, dtype=np.uint32, offset=12)
                match dataType:
                    case 0:
                        self.ImportWindow.ImpDataType.setCurrentIndex(self.ImportWindow.ImpDataType.findData('i1'))
                        tnote = '8-bit Signed Integer'
                    case 1:
                        self.ImportWindow.ImpDataType.setCurrentIndex(self.ImportWindow.ImpDataType.findData('i2'))
                        tnote = '16-bit Signed Integer'
                    case 2:
                        self.ImportWindow.ImpDataType.setCurrentIndex(self.ImportWindow.ImpDataType.findData('f4'))
                        tnote = '32-bit Real Float'
                    case 3:
                        tnote = '16-bit Complex Signed Integer, unsupported'
                    case 4:
                        tnote = '32-bit Complex Float, unsupported'
                    case 6:
                        self.ImportWindow.ImpDataType.setCurrentIndex(self.ImportWindow.ImpDataType.findData('u2'))
                        tnote = '16-bit Unsigned Integer'
                    case other:
                        tnote = 'Uknown data type'

                self.ImportWindow.DataOffset.setValue(1024)
                notes = 'Dim: X = ' + str(dim[0]) + ', Y = ' + str(dim[1]) + ', Z = ' + str(dim[2]) + \
                    '\n' + tnote + ', ' + bo + '\n** MRC files have a 1024-byte data offset'
            else:
                notes = 'Unrecognizable as MRC.\n\n"MAP " word missed.'
                err = -1
                return
        elif self.ImportWindow.DM34Button.isChecked():
            prepDM(self)
        elif self.ImportWindow.HDF5Button.isChecked():
            try:
                self.T.h5 = h5py.File(self.ImportWindow.ImpFilePath.text())
                keys = returnKeys(self.T.h5)
            except BaseException:
                notes = 'Read HDF5 file error'
                err = -1

            if err != -1:
                # enable subimage dropdown
                self.ImportWindow.ImpSubImg.setEnabled(True)

                # Select sub-image with the 1st largest dimension; unless manually selected
                if self.sender() is not self.ImportWindow.ImpSubImg:
                    # List all images' names in `self.ImportWindow.ImpSubImg`
                    self.ImportWindow.ImpSubImg.blockSignals(True)
                    pdim = [self.T.h5[key].size for key in keys]
                    self.ImportWindow.ImpSubImg.clear()
                    self.ImportWindow.ImpSubImg.addItems(keys)
                    self.ImportWindow.ImpSubImg.blockSignals(False)
                    self.ImportWindow.ImpSubImg.setCurrentIndex(np.argmax(pdim))

                # Info of selected sub-image
                h5i = self.T.h5[keys[self.ImportWindow.ImpSubImg.currentIndex()]]

                # Read dimensions,
                dims = h5i.shape
                if len(dims) < 4:
                    np.append(dims, np.ones(4 - len(dims), dtype=int))
                self.ImportWindow.DNPxX.setValue(dims[3])
                self.ImportWindow.DNPxY.setValue(dims[2])
                self.ImportWindow.DNFrX.setValue(dims[1])
                self.ImportWindow.DNFrY.setValue(dims[0])

                # Find offset, file tail, data type, byte-order of dataset
                offset = int(h5i.id.get_offset())
                if offset == -1:
                    self.ImportWindow.DataOffset.setValue(0)
                    noteoffs = 'This dataset is not "contiguous", thus data offset is unknown.'
                else:
                    self.ImportWindow.DataOffset.setValue(offset)
                    noteoffs = "Selected dataset's offset is {} bytes.".format(offset)

                self.T.fileTail = self.T.FileSize - self.ImportWindow.DataOffset.value() - h5i.size

                # set datatype; strip < or > if included as these represent big/little endian
                self.ImportWindow.ImpDataType.setCurrentIndex(
                    self.ImportWindow.ImpDataType.findData(re.sub('<|>', "", h5i.dtype.str)))

                if ">" in h5i.dtype.str:
                    self.ImportWindow.ImpByteOrder.setCurrentIndex(1)
                    bo = 'Big Endian'
                else:
                    self.ImportWindow.ImpByteOrder.setCurrentIndex(0)
                    bo = 'Little Endian'

                notes = "Dim: X = {:d}, Y = {:d}, Z = {:d}, W = {:d}\n{:s}, {:s}\n{:s}".format(
                    *dims, bo, str(h5i.dtype), noteoffs)
                if dims[3] == 1:
                    guessFramesFromDimZ(dims[2])
        else:
            getDimFromName(self.ImportWindow.ImpFilePath.text())
            self.ImportWindow.ImpDataType.setCurrentIndex(self.ImportWindow.ImpDataType.findData("f4"))  # 32-bit float
            notes = "Custom import"
    else:
        notes = "File path is invalid"
        err = -1

    self.ImportWindow.ImpFileMetaNotes.setText(notes)
    if self.ImportWindow.ImpDataType.currentIndex() == 0 and err != -1:
        _ = notifDLG(
            self,
            self.ImportWindow,
            "warn",
            "The data type indicated in the file's metadata is not supported/recognized.",
            "Invalid Data Type!")

    # Reset import range selections
    rangeImportExport(self, self.ImportWindow.DNPxX)
    rangeImportExport(self, self.ImportWindow.DNFrX)

    # generate placeholder images #TODO #DELETE?
    # self.Fig.Preview.Image = np.zeros(self.D.NPx)
    # self.Fig.Dfrn.Image = np.zeros(self.D.NPx)
    # self.Fig.Dfrn.Real = np.zeros(self.D.NFr)

    importBoxInput(self)


def importBoxInput(self):

    def checkMem(nPx, nFr, byte_size):
        # Display estimated size in green if matches actual size, brown if smaller, red if larger
        if self.T.EstSize == self.T.FileSize:
            self.ImportWindow.ImpEstFilesize.setStyleSheet("color: rgb(0, 128, 0);")
        elif self.T.EstSize < self.T.FileSize:
            self.ImportWindow.ImpEstFilesize.setStyleSheet("color: rgb(128, 128, 0);")
        else:
            self.ImportWindow.ImpEstFilesize.setStyleSheet("color: rgb(255, 0, 0);")

        # keep the same font after changing color
        self.ImportWindow.ImpEstFilesize.setFont(self.ImportWindow.ImpActualFilesize.font())

        # Estimate the amount of memory needed to hold the largest arrays in memory
        # Estimate of the distance to the far corner of the diffraciton pattern
        # est_mem = np.prod([nPx,nFr]) \                                        # self.Data
        #         + nFr.prod()*(2*np.floor(np.linalg.norm(nPx/2))+1) \          # self.adfImages
        #         + 10*nFr.prod() + 2*nPx.prod()  \                             # self.Fig[id].Image
        #         + 10*nPx.prod()                                               # self.Mask
        est_mem = np.prod([nPx, nFr]) \
            + nFr.prod() * (2 * np.floor(np.linalg.norm(nPx / 2)) + 1) \
            + 10 * nFr.prod() + 2 * nPx.prod() \
            + 10 * nPx.prod()
        self.T.EstMem = est_mem * byte_size

        notes = "Estimated memory usage: {:.3f} GiB.".format(self.T.EstMem / (1024**3))

        # warn if the dataset will not fit in memory
        if self.T.EstMem > self.C.MemTot:
            msg = "WARNING: Size of dataset is larger than the system memory!"
            _ = notifDLG(self, self.ImportWindow, "warn", msg, "Size Exceeds System Memory!")
            notes += "\n" + msg

        notes += "\nSystem byte order: " + self.C.EndianTxt[self.C.SysEndian] + "."

        return notes

    def checkGPUMEM(nPx, nFr):
        igpu = self.ImportWindow.ImpGPU.currentData()
        if igpu is None:
            gpu_note = 'GPU disabled.'
        else:
            tgpu = f"GPU {igpu:.0f}. " + self.C.GPU(igpu).name + f" {self.C.GPU(igpu).mem / 1024**3:.2f} GiB"
            try:
                device = torch.device(igpu if torch.cuda.is_available() else "cpu")
                amem = torch.cuda.get_device_properties(igpu).total_memory
                # If GPU is already in use, taking the current data size into account
                if self.D.GPU == self.ImportWindow.ImpGPU.value():
                    try:
                        amem = amem + self.D.EstMem
                    except BaseException:
                        pass

                amem_t = '{:.3f} GiB'.format(amem / 1024**3)
                wt = None
                # TODO - this seems really arbitrary
                if self.T.EstMem > amem - 128 * 1024**2:  # Has 128 MiB extra?
                    gpu_note = tgpu + \
                        " has NOT enough free memory (" + amem_t + "). 128 MiB EXTRA free memory is also required."
                    wt = 'GPU Not Enough Free Memory!'
                    self.ImportWindow.ImpGPU.setCurrentIndex(self.ImportWindow.ImpGPU.findData(None))

                elif self.T.EstMem > (amem - 512 * 1024**2):  # Has 512 MiB extra?
                    gpu_note = tgpu + " has LIMITED free memory (" + amem_t + ") and may cause errors."
                    wt = 'GPU Limited Free Memory!'

                else:
                    gpu_note = tgpu + " has enough free memory (" + amem_t + ") for the selected dataset."

                # Notify warnings if any
                if wt:
                    _ = notifDLG(self, self.ImportWindow, "warn", gpu_note, wt)
            except BaseException:
                gpu_note = "Failed to select " + tgpu + "!"
                _ = notifDLG(self, self.ImportWindow, "warn", gpu_note, "Error Selecting GPU")
                self.ImportWindow.ImpGPU.setCurrentIndex(self.ImportWindow.ImpGPU.findData(None))

        return gpu_note

    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    self.ImportWindow.ImpEstFilesize.clear()       # clear estimated file size
    notes = None                                   # initialize notes in case file is not on path
    dfrn_src = real_src = self.sender()            # capture UI component that triggered this callback

    if os.path.isfile(self.ImportWindow.ImpFilePath.text()):

        # Update Diffraction and Real-space import ranges; use default source if
        # self.sender() is not a range UI component
        if (not hasattr(self.sender(), 'accessibleDescription')) or (
                "Dfrn" not in self.sender().accessibleDescription()):
            dfrn_src = self.ImportWindow.IPxD
        if (not hasattr(self.sender(), 'accessibleDescription')) or (
                "Real" not in self.sender().accessibleDescription()):
            real_src = self.ImportWindow.IFrD

        dnote, _, _, nPx, _ = rangeImportExport(self, dfrn_src)
        rnote, _, _, nFr, _ = rangeImportExport(self, real_src)

        notes = dnote + rnote

        # Enable/Disable Range UIs
        self.ImportWindow.ImpPxPart.setEnabled(True)
        self.ImportWindow.ImpFrPart.setEnabled(True)

        # Current dataset dimensions
        irng = [nPx, nFr]

        # Allow for virtual memory mapping in some situations
        if self.ImportWindow.FrHead.value() == 0 and self.ImportWindow.FrFoot.value() == 0 and (
                not self.ImportWindow.HDF5Button.isChecked() or self.ImportWindow.DataOffset.value() > 0) and (
                self.ImportWindow.ImpByteOrder.currentData() == self.C.SysEndian) and (
                'int' not in self.ImportWindow.ImpDataType.currentData()) and [
                    self.ImportWindow.DNPxX.value(),
                    self.ImportWindow.DNPxY.value(),
                    self.ImportWindow.DNFrX.value(),
                self.ImportWindow.DNFrY.value()] == irng:
            self.ImportWindow.ImpMemType.setEnabled(True)
        else:
            self.ImportWindow.ImpMemType.setEnabled(False)
            self.ImportWindow.ImpMemType.setCurrentIndex(0)  # Physical Memory

        # Calculate dataset size and memory usage
        if self.ImportWindow.ImpDataType.currentData() != "unknown":
            byte_size = self.ByteSize[self.ImportWindow.ImpDataType.currentData()]
            self.T.EstSize = self.ImportWindow.DataOffset.value() + self.T.fileTail \
                + (self.ImportWindow.FrHead.value() + self.ImportWindow.DNPxX.value() * self.ImportWindow.DNPxY.value() * byte_size + self.ImportWindow.FrFoot.value()) \
                * self.ImportWindow.DNFrX.value() * self.ImportWindow.DNFrY.value()
            self.ImportWindow.ImpEstFilesize.setText(
                "{} bytes, {:.2f} GiB".format(
                    self.T.EstSize, self.T.EstSize / 1024**3))

            if np.issubdtype(self.ImportWindow.ImpDataType.currentData(), np.integer):
                if byte_size > 4:
                    f = 'f8'
                else:
                    f = 'f4'
                byte_size = self.ByteSize[f]
                notes += "\nDataset will be converted into " + str(byte_size * 8) + "-bit Real."

            notes += "\nImport by " + self.ImportWindow.ImpMemType.currentText() + "\n" + checkMem(nPx, nFr, byte_size) + "\n\n"
            notes += checkGPUMEM(nPx, nFr)

        # Allow to swap dataset/keep parameters if the dimensions are identical and self.D is not None
        # self.ImportWindow.ImpKeepP.Enable = ~isempty(self.D) and isequal(irng,
        # [self.D.NPxX self.D.NPxY self.D.NFrX self.D.NFrY])
        self.ImportWindow.ImpKeepP.setEnabled(
            (self.D is not None) and (
                irng == [
                    self.D.NPxX,
                    self.D.NPxY,
                    self.D.NFrX,
                    self.D.NFrY]))
        if self.ImportWindow.ImpKeepP.isEnabled() == False:
            self.ImportWindow.ImpKeepP.setChecked(False)
        if self.ImportWindow.ImpKeepP.isChecked():
            notes += "\n\nSwapping dataset - keeping current setups/alignments etc."

    # update notes in the text field
    self.ImportWindow.ImpNotes.setText(notes)


def getImportInfo(self):
    """ Function to update current data info """
    d = self.D
    d0 = self.T.prev_D
    notes = "File: " + d.filePath
    if d.subImg != '':
        notes += "\nSub-dataset: " + d.subImg

    notes += "\n\n# Current Data Info #" +\
        "\nByte Order: " + self.C.EndianTxt[d.ByteOrder] + "\nData Type: " + np.dtype(d.DataType).name + "\nByte Size: " + str(d.ByteSize) + " bytes" +\
        "\n{:s} (X\u2A2FY): {:d}\u2A2F{:d}".format("Diffraction", *d.NPx) +\
        "\n{:s} (X\u2A2FY): {:d}\u2A2F{:d}".format("Real-space", *d.NFr) +\
        "\n\n# Data Structure in File #" +\
        "\nData Offset: " + str(d0.Offset) + " bytes\nFrame Header: " + str(d0.FrHead) + " bytes\nFrame Footer: " + str(d0.FrFoot) + " bytes" +\
        "\nByte Order: " + self.C.EndianTxt[d0.ByteOrder] + "\nData Type: " + np.dtype(d0.DataType).name + "\nByte Size: " + str(d0.ByteSize) + " bytes" +\
        "\n\n# File Meta Info Notes #\n" + d0.NoteFileMeta + '\n' +\
        "\n\n# Import Option Notes #\n" + d0.NoteImp + '\n'

    return notes


def rangeImportExport(self, src):
    # spinner upper/lower limits must be different, so now set lower limit `0` but force minimum to `1`
    if hasattr(src, 'value'):
        val = np.maximum(src.value(), 0)

    # Round positions from ROIs
    # if hasattr(evt,'CurrentPosition'):
    #    pos = round(evt.CurrentPosition)

    # `sp`/`U`: space/unit, "Dfrn"/"Px" for diffraction/pixel OR "Real"/"Fr" for real-space/frame
    if "Dfrn" in src.accessibleDescription():
        sp = "Dfrn"
        U = "Px"
    else:
        sp = "Real"
        U = "Fr"

    # `io_mode`: "I" or "E" for Import/Export
    if "Import" in src.accessibleDescription():
        io_mode = "I"
        dnp = np.asarray([self.ImportWindow.findChild(qtw.QSpinBox, "DN" +
                                                      U +
                                                      "X").value(), self.ImportWindow.findChild(qtw.QSpinBox, "DN" +
                                                                                                U +
                                                                                                "Y").value()]).astype(int)  # Raw dataset dimensions, e.g. self.ImportWindow.DNPxX.value()
    else:  # Export
        io_mode = "E"
        dnp = np.asarray(getattr(self.D, "N" + U)).astype(int)  # Loaded dataset dimensions

    # Get values from UI
    # Binning/Sampling (self.ImportWindow.IPxD, self.ImportWindow.EPxD, self.ImportWindow.IFrD or self.ImportWindow.EFrD)
    binDist = np.asarray(self.ImportWindow.findChild(qtw.QSpinBox, io_mode + U + "D").value())

    if src.accessibleDescription() == "Export Dfrn ROI":  # From Export Diffraction ROIs
        initPoint = pos[0:1]
        numPoints = np.max(np.floor((pos[2:3] + 1) / binDist), 1)
    elif src.accessibleDescription() == "Export Real ROI":  # From Export Real-space ROIs
        initPoint = pos[0:1]
        numPoints = np.floor(pos[2:3] / binDist) + 1
    else:  # From other sources
        initPoint = np.asarray([self.ImportWindow.findChild(qtw.QSpinBox,
                                                            io_mode + U + "X1").value(),
                                self.ImportWindow.findChild(qtw.QSpinBox,
                                io_mode + U + "Y1").value()])  # self.IPxX1, self.EFrX1 etc, Point-1 X & Y UIs
        numPoints = np.asarray([self.ImportWindow.findChild(qtw.QSpinBox,
                                                            io_mode + "N" + U + "X").value(),
                                self.ImportWindow.findChild(qtw.QSpinBox,
                                io_mode + "N" + U + "Y").value()])  # self.INPxX, self.ENFrX etc, N-Points X & Y UIs

    # Replace value with current event value
    if src == getattr(self.ImportWindow, io_mode + U + "D"):
        binDist = val  # Binning/Sampling UI
    elif src == getattr(self.ImportWindow, io_mode + U + "X1"):
        initPoint[0] = val  # Point-1 X UI
    elif src == getattr(self.ImportWindow, io_mode + U + "Y1"):
        initPoint[1] = val  # Point-1 Y UI
    elif src == getattr(self.ImportWindow, io_mode + "N" + U + "X"):
        numPoints[0] = val  # N-Points X UI
    elif src == getattr(self.ImportWindow, io_mode + "N" + U + "Y"):
        numPoints[1] = val  # N-Points Y UI
    elif src in [getattr(self.ImportWindow, "DN" + U + "X"), getattr(self.ImportWindow, "DN" + U + "Y"), getattr(self.ImportWindow, "Imp" + U + "Part"), getattr(self.SaveWindow, "Exp" + U + "Part")]:
        # Reset range options if dataset raw dimension changes OR partial selection enables/disables
        getattr(self.ImportWindow, io_mode + U + "D").setMaximum(min(dnp))  # Update binning/sampling UI limits
        if io_mode == "I" and U == "Fr":  # Update preview frame limits
            self.blockAllSignals = True
            self.PvFrX.setRange(1, dnp[0])
            self.PvFrX.setValue(dnp[0])
            self.PvFrY.setRange(1, dnp[1])
            self.PvFrY.setValue(dnp[1])
            self.blockAllSignals = False
        binDist = 1
        initPoint = np.asarray([1, 1])
        numPoints = dnp

    # In general, N-Points are determined by Point-1 and Binning/Sampling, unless N-Points are the source
    # s = [self.ImportWindow.findChild(qtw.QSpinBox,io_mode+"N"+U+"X"), self.ImportWindow.findChild(qtw.QSpinBox,io_mode+"N"+U+"Y")] != src # Whether N-Points X or Y are not the source
    # s = np.asarray([x in src for x in [self.ImportWindow.findChild(qtw.QSpinBox,io_mode+"N"+U+"X"), self.ImportWindow.findChild(qtw.QSpinBox,io_mode+"N"+U+"Y")]])
    if src == getattr(self.ImportWindow, io_mode + "N" + U + "X"):
        s = np.asarray([1])
    elif src == getattr(self.ImportWindow, io_mode + "N" + U + "Y"):
        s = np.asarray([0])
    else:
        s = np.asarray([0, 1])

    if U == "Px":
        numPoints[s] = np.maximum(
            1,
            np.minimum(
                numPoints[s],
                np.floor(
                    (dnp[s] -
                     initPoint[s] +
                     1) /
                    binDist)))  # Determine N-Points X/Y if not source
        # numPoints[s] = np.maximum(np.asarray([1,1]), np.minimum(numPoints[s],
        # np.floor((dnp[s]-initPoint[s]+1)/binDist)))  # Determine N-Points X/Y if
        # not source
        initPoint = np.minimum(initPoint, dnp - numPoints * binDist + 1)
        endPoint = initPoint + numPoints * binDist - 1  # Endpoints of Pixel ranges
        l1 = dnp - binDist + 1
        ln = np.floor(dnp / binDist).astype(int)  # Upper limits of Pixel Point-1 X & Y and N-Points X & Y
        pos = [initPoint, numPoints * binDist - 1]  # Positions for Export ROI
        txt = "Diffraction Range (in pixels [px])"
        u = " px"
        txtb = "binning to "
    else:  # "Fr"
        # Frame sampling has slightly different logics to pixel binning
        numPoints[s] = np.minimum(numPoints[s], np.floor((dnp[s] - initPoint[s]) / binDist) + 1)
        initPoint = np.minimum(initPoint, dnp - (numPoints - 1) * binDist)
        endPoint = initPoint + (numPoints - 1) * binDist  # Endpoints of Frame ranges
        l1 = dnp
        ln = np.floor((dnp - 1) / binDist).astype(int) + 1  # Upper limits of Frame Point-1 X & Y and N-Points X & Y
        pos = [initPoint, (numPoints - 1) * binDist]  # Positions for Export ROI
        txt = "Real-space Range (in frames [fr])"
        u = " fr"
        txtb = "sampling "

    # Set Point-1 X & Y, N-Points X & Y and Binning/Sampling UIs
    getattr(self.ImportWindow, io_mode + U + "X1").setRange(0, l1[0])
    getattr(self.ImportWindow, io_mode + U + "Y1").setRange(0, l1[1])
    getattr(self.ImportWindow, io_mode + "N" + U + "X").setRange(0, ln[0])
    getattr(self.ImportWindow, io_mode + "N" + U + "Y").setRange(0, ln[1])
    getattr(self.ImportWindow, io_mode + U + "D").setRange(0, min(dnp))

    getattr(self.ImportWindow, io_mode + U + "X1").setValue(initPoint[0])
    getattr(self.ImportWindow, io_mode + U + "Y1").setValue(initPoint[1])
    getattr(self.ImportWindow, io_mode + "N" + U + "X").setValue(numPoints[0])
    getattr(self.ImportWindow, io_mode + "N" + U + "Y").setValue(numPoints[1])
    getattr(self.ImportWindow, io_mode + U + "D").setValue(binDist)

    # Try to update Export ROIs
    # if O == "E":
    #    set(findobj(self.G.(sp+"Ax"),'Tag',"Export "+sp+" ROI"), 'Position', pos) #TODO

    # Range notes
    tp = [x1 + u for x1 in [str(ints) for ints in numPoints]]

    if binDist > 1:
        tp = [x6 + u for x6 in [x4 + x5 for x4,
                                x5 in list(zip([x3 + " from " for x3 in [txtb + x2 for x2 in tp]],
                                               [str(ints) for ints in endPoint - initPoint + 1]))]]

    # If not from 1st to last
    s = np.maximum(initPoint > 1, endPoint < dnp)
    for i in np.arange(len(s)):
        if s[i]:
            tp[i] = str(numPoints[i]) + u + ", " + str(initPoint[i] - 1) + "/" + \
                str(dnp[i] - endPoint[i]) + u + " offset from start/end"
    notes = "{}:\n\tX = {}-{} ({})\n\tY = {}-{} ({})\n".format(txt, *
                                                               [items for sublist in zip(initPoint, endPoint, tp) for items in sublist])

    return notes, binDist, initPoint, numPoints, endPoint

# Function to unload data and clean all images


def unloadData(self, keep_p=False):
    importlib.reload(appClass)
    from callbacks.appClass import A, P, Mask, D, Prev

    """ Function to unload data and clean all images """
    enableWindows(self, False)  # Disable windows for the data unload process
    self.setWindowTitle('Quant4D')
    # Whether to swap dataset only, without changing any existing parameters
    if not keep_p:
        # clear all axes
        for id in self.Fig:
            fig = self.Fig[id]
            fig.Image = None
            fig.ax.cla()
            fig.canvas.draw_idle()
            self.ImageAx[id] = None
        self.SettingsWindow.HistAxes.axes.cla()
        self.SettingsWindow.HistAxes.figure.canvas.draw_idle()

        # clear annotations (lines and draggable points)
        for ii in dir(self.A):
            if type(
                getattr(
                    self.A,
                    ii)) in (
                InteractivePoint,
                InteractiveCircle,
                    matplotlib.lines.Line2D):  # ,InteractiveBox #TODO
                setattr(self.A, ii, None)

        setattr(self, 'P', P())
        setattr(self, 'A', A())
        setattr(self, 'Mask', Mask())
        # self.ImgD = [] #TODO
        self.CDT.clearContents()  # custom aperture table

    # Remove all data from GPU if in use #TODO
    # try:
    #    if self.D.GPU > 0:
    #        reset(parallel.gpu.GPUDevice.getDevice(self.D.GPU))
    #        gpuDevice([])
    # except:
    #    pass

    # Clear data, parameters and Axes
    self.Data = None
    self.Memfile = None
    # setattr(self,'D',D()) #TODO #DELTE
    setattr(self, "D", None)
    setattr(self, 'Prev', Prev())


def importData(self):
    assert (os.path.isfile(self.ImportWindow.ImpFilePath.text())), "File does not exist at the specified location"

    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    if os.path.isfile(self.ImportWindow.ImpFilePath.text()):
        # Set save/export filenames etc.
        self.setWindowTitle(self.fileName)
        self.SaveWindow.SaveDir.setText(self.fileDir)
        self.SaveWindow.SaveImgPrefix.setText(self.fileName.replace(self.fileExt, "") + "_")

        # TODO
        # if self.ImportWindow.MedipixButton.isChecked():
        #     readMRC(self)
        # elif self.ImportWindow.EMPADButton.isChecked():
        try:
            readFile(self)
        except BaseException:
            unloadData(self)
            notifDLG(self, self, 'error', 'Error during Import!', 'Error!')
            enableWindows(self, True)

        # Start file reading here
        # if ~isempty(self.D.h5ds) % HDF5 import
        #    data = zeros(npx, npy, nfx, nfy, dtype1); % Pre-allocate array
        #    fid = H5F.open(self.D.filePath);   dset_id = H5D.open(fid, self.D.h5ds);
        #    file_space_id = H5S.create_simple(4, [dnfy dnfx dnpy dnpx], []);
        #    mem_space_id = H5S.create_simple(2, [npy*pd npx*pd], []);
        #    % data = H5D.read(dset_id,'H5ML_DEFAULT','H5S_ALL','H5S_ALL','H5P_DEFAULT'); % Read whole
        #    for ify = 1:nfy
        #      for ifx = 1:nfx
        #        if ~isvalid(self.T.progDLG), err = -1; break; end % Cancel if progress window closed
        #        self.T.frameJ(1) = (ify-1)*nfx + ifx; % Update processed Frame Number for progress update
        #        H5S.select_hyperslab(file_space_id, 'H5S_SELECT_SET', [fy1+(ify-1)*fd, fx1+(ifx-1)*fd, py1, px1]-1, ...
        #          [],[], [1 1 npy*pd npx*pd]); % Read 1 frame at a time; C-like array indices for H5 low-level APIs
        #        frame = H5D.read(dset_id, 'H5ML_DEFAULT', mem_space_id, file_space_id, 'H5P_DEFAULT');
        #        if pd > 1, frame = squeeze(sum(reshape(frame, [pd npx pd npy]), [1 3])); end % Pixel binning
        #        data(:, :, ifx, ify) = frame; % Store frame
        #      end
        #      if err == -1, break; end
        #    end
        #    % Close opened handles
        #    H5S.close(mem_space_id);  H5S.close(file_space_id);  H5D.close(dset_id);  H5F.close(fid);
        #    data = reshape(data, self.D.NPxS, self.D.NFrS); % Make dataset a 2D array
        #    self.Data = data;
        #  elseif self.D.mem == "Physical Memory" % General reading method; read data into physical memory
        # if self.D.mem == "Physical Memory": #General reading method; read data into physical memory
        #  data = zeros(npx, npy, nfx, nfy, dtype1) # Pre-allocate array
        #  dfrSize = hdr+dnpx*dnpy*bsize+ftr # frame size including header/footer
        #  fid = fopen(self.D.filePath,'r')
        #  for ify = 1:nfy:
        #      for ifx = 1:nfx:
        #          if ~isvalid(self.T.progDLG):
        #              err = -1
        #              break # Cancel if progress window closed
        #          self.T.frameJ(1) = (ify-1)*nfx + ifx # Update processed Frame Number for progress update
        #          # Read 1 frame at a time; move cursor to "frame offset" + "pixel Y offset" in file dataset
        #          dfx = fx1+(ifx-1)*fd;  dfy = fy1+(ify-1)*fd; % Frame indices in dataset file
        #          fseek(fid, offs + (dfx-1 + (dfy-1)*dnfx) * dfrSize + hdr + ((px1-1) + (py1-1)*dnpx) * bsize, 'bof')
        #          frame = fread(fid, [dnpx, npy*pd], dtype, 0, order) # Read including "pixel X offset"
        #          if npx*pd ~= dnpx:
        #              frame = frame(px1:px1+npx*pd-1, :) # Crop "pixel X offset" off from array memory
        #          if pd > 1:
        #              frame = squeeze(sum(reshape(frame, [pd npx pd npy]), [1 3])) # Pixel binning
        #          data[:, :, ifx, ify] = frame # Store frame
        #  if err == -1:
        #      break
        #
        #  data = reshape(data,self.D.NPxS,self.D.NFrS) # Make dataset a 2D array
        #  self.Data = data;
        # elseif self.D.mem == "Virtual Mapping" % Virtual memory mapping
        #  % Create a memory mapped file, rather than reading the file directly into memory
        #  if ~strcmp(self.C.SysEndian, order)
        #    error("Dataset's endianness is different to that of the system's!")
        #  end
        #
        #  if hdr == 0 and ftr == 0:
        #      self.Memfile = memmapfile(self.D.filePath,'Offset',offs, 'Format',{dtype1,[self.D.NPxS self.D.NFrS],'data'}, 'Repeat',1)
        #      self.Data = self.Memfile.Data.data
        #  else:
        #      error("Virtual memory with header/footer > 0 not supported yet.")

    else:
        msg = "File: " + self.ImportWindow.ImpFilePath.text() + " is not found!"
        ttl = "File not found!"
        notifDLG(self, self.ImportWindow, 'error', msg, ttl)


def importMask(self, space):
    if space == "Real":
        spaceName = "Real-space"
        imShape = self.D.NFr
    else:  # "Dfrn"
        spaceName = "Diffraction"
        imShape = self.D.NPx

    im = []
    msg = ""

    fDialog = qtw.QFileDialog(self)
    fDialog.setWindowTitle("Select a mask image with shape [{:d},{:d}]".format(*imShape))
    fDialog.setNameFilter("('*.tif;*.tiff;*.png;*.jpg;*.jpeg;*.bmp;*.gif);;(*.*)")
    fDialog.setFileMode(qtw.QFileDialog.ExistingFile)
    fDialog.setDirectory(qtc.QDir.currentPath())
    file = None
    if fDialog.exec_() == qtw.QDialog.Accepted:
        file = fDialog.selectedFiles()

    _, ext = os.path.splitext(file)

    match ext.lower():  # force lowercase
        case '.tif' | '.tiff' | '.png' | '.jpg' | '.jpeg' | '.bmp' | '.gif':

            # directly convert image to grayscale floating point numpy array
            im = np.array(Image.open(file).convert("L")).astype(np.float64)

            # get mask shape
            isize = im.shape

            # if imported dimensions do not matched data dimensions
            if ~all(isize == imShape):
                # check for a transpose
                if all(isize == np.flip(imShape)):
                    im = im.T
                    msg += "Image shape ({:d},{:d}) transposed to fit data's {:s} shape ({:d},{:d}).\n".format(*
                                                                                                               isize, spaceName, *imShape)
                else:  # throw error
                    notifDLG(
                        self,
                        self,
                        'warn',
                        "Image size ({:d},{:d}) does not fit data's {:s} size ({:d},{:d})!".format(
                            *
                            isize,
                            spaceName,
                            *
                            imShape),
                        'Dimension Mismatch')
                    return

        case "":  # Canceled, etc.
            return

        case other:  # unsupported filetype
            _ = notifDLG(self, self, 'warn', "File type '*" + ext + "' currently unsupported!", 'Import Failed')
            return

    # check for invalid data (nan or inf) and replace with zeros
    invalidMask = np.ma.masked_invalid(im).mask
    if invalidMask.any():
        im[invalidMask] = 0
        msg += "NaN/Inf found in image, and set to 0.\n"

    # scale the maximum to 1
    imax = im.max()
    if (imax != 0) and (imax != 1):
        im /= imax
        msg += "The maximum was {:d}; now scaled to 1, by `IMG = IMG/{:d}`.\n".format(imax, imax)

    # notify user of what has been done and return the mask
    if msg != "":
        msg = "Please note:\n" + msg + "\n"

    _ = notifDLG(self, self, 'help', msg + "Please check the " + spaceName + " Mask image.", 'Mask Imported')
    self.Fig[space + "Mask"].activateWindow()

    return im
