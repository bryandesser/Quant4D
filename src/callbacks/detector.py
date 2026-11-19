"""Detector mode and coordinate callbacks."""
import os
import sys
import traceback
import numpy as np
import re
from callbacks.menus import showPreviewDisplayControls
from callbacks.window_manager import setPreviewTabs
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *
from callbacks.layout import dfrn_grids, dfrn_shape, real_shape
from annotationsClasses.interactiveCircle import InteractiveCircle
from annotationsClasses.interactiveAnnulus import InteractiveAnnulus
from annotationsClasses.interactivePoint import InteractivePoint
from callbacks.signals import signals_blocked  # noqa: E402


def clearDetectors(self):

    detectorList = [
        "adf",
        "tb",
        "VrAp",         # virtual aperture, its mirror handle and mirror line
        "VrApMirP",
        "VrApMirL"]

    # Try removing annotations and then setting to None so that they can be replotted later
    for ii in detectorList:
        if getattr(self.A, ii) is not None:
            try:
                getattr(self.A, ii).remove()
            except BaseException:
                pass
            finally:
                setattr(self.A, ii, None)

    # DPC segments and the scan-direction arrows: redrawn by the modes that use them
    from callbacks.annularDetectorCallbacks import removeScanDir, removeSegDetr  # noqa: E402
    removeSegDetr(self)
    removeScanDir(self)

    # Virtual aperture's symmetry/mirror copies (plain lines, tagged when drawn)
    for ln in list(self.Fig.Dfrn.ax.lines):
        if getattr(ln, '_vrAp_clone', False):
            ln.remove()

    # Custom detectors: remove their annotations; they are redrawn on returning to CustMod
    from callbacks.customDetectorCallbacks import _removeArtists  # noqa: E402
    for cmask in self.A.Custom.values():
        _removeArtists(cmask)
    # Scan direction alignment
    # delete(findobj(self.ImageAx.Dfrn,'Tag','ScanDirAnnot')) #TODO


def detectorModeCallbacks(self):
    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    from callbacks.alignment import moveTransBeam, transBeamCallbacks  # noqa: E402
    from callbacks.annularDetectorCallbacks import annularDetectorCallbacks  # noqa: E402
    from callbacks.plotting import plotImage  # noqa: E402
    from callbacks.previewCallbacks import previewCallbacks  # noqa: E402
    from callbacks.window_manager import enableWindows  # noqa: E402
    from callbacks.virtualApertureCallbacks import virtualApertureCallbacks  # noqa: E402
    if self.blockAllSignals:
        return

    dmod = self.DetrMode.currentData()

    enableWindows(self, False)  # Disable all on change windows
    clearDetectors(self)  # Clear ROIs on Diffraction

    # Clear Real-space images if not switching to alignment or preview
    if dmod not in ["AlignMod", "PrvwMod"]:
        for ii in self.G.RealID:
            if "Mask" not in ii:
                # self.Fig[ii].ax.cla()
                self.Fig[ii].canvas.draw_idle()

    # Enable/Disable CoM/DPC related buttons/images (and the Window menu's Center of Mass items)
    for btn in self.G.CoM_btns:
        btn.setEnabled(dmod in ["CoMMod", "DPCMod"])
    syncCoMActions(self)

    # a locked display selection survives the mode change (if the image is still listed)
    locked_id = self.SettingsWindow.DispImage.currentData() if self.SettingsWindow.DispLock.isChecked() else None

    # block singals whilst updating DispImage QComboBox
    with signals_blocked(self.SettingsWindow.DispImage):
        if dmod in ["CoMMod", "DPCMod"]:
            # add all images to dropdown list in the Settings Window and
            # Subsitute "CoM"/"DPC" in image names and window titles
            imageNames = [re.sub('DPC|CoM', dmod[:3], ii) for ii in self.G.ImgName]

            self.SettingsWindow.DispImage.clear()
            for itemText, itemID in zip(imageNames, self.G.ImgID):
                self.SettingsWindow.DispImage.addItem(itemText, itemID)  # drop down items
                self.Fig[itemID].setWindowTitle(itemText)  # window title

            # Subsitute "CoM"/"DPC" in button text
            for btn in self.G.CoM_btns:
                re.sub('DPC|CoM', dmod[:3], btn.text())

        else:
            self.SettingsWindow.DispImage.clear()
            for itemText, itemID, itemType in zip(self.G.ImgName, self.G.ImgID, self.G.ImgType):
                if "CoM" not in itemType:
                    self.SettingsWindow.DispImage.addItem(itemText, itemID)  # drop down items
                else:
                    self.Fig[itemID].hide()  # Image windows

        # Show primary diffraction/real-space image when mode changes unless in Preview mode
        if dmod != "PrvwMod":
            self.Fig.Dfrn.show()
            self.Fig.Real.show()
        else:
            self.Fig.Dfrn.hide()
            self.Fig.Real.hide()

        # Special case for Import Preview Mode
        if dmod == "PrvwMod":
            # Keep only "Preview" image
            self.SettingsWindow.DispImage.clear()
            self.SettingsWindow.DispImage.addItem("Preview", "Preview")

            # Hide other UIs
            setPreviewTabs(self, True)

            self.Fig.Preview.show()
            showPreviewDisplayControls(self)    # brightness/contrast/gamma pop up with the importer
        else:
            self.P.DetrMode = self.DetrMode.currentData()  # Note current mode
            # Remove "Preview" image from drop down
            self.SettingsWindow.DispImage.removeItem(self.SettingsWindow.DispImage.findData("Preview"))
            self.Fig.Preview.hide()

            # Show all UIs
            setPreviewTabs(self, False)

    # Define images in the saving list
    with signals_blocked(self.SaveWindow.SaveImgList):
        self.SaveWindow.SaveImgList.clear()
        self.SaveWindow.SaveImgList.addItems([self.SettingsWindow.DispImage.itemData(ii)
                                             for ii in range(self.SettingsWindow.DispImage.count())])
    self.SaveWindow.SaveImgPrefix.textChanged.emit(self.SaveWindow.SaveImgPrefix.text())  # Update Image saving prefix
    from callbacks.axis_direction import axisDirectionCallbacks  # noqa: E402
    axisDirectionCallbacks(self)  # orientation and direction arrows (scan arrows depend on the mode)

    # Set detector size when transmitted beam is aligned the first time
    if not (self.P.TransBeamInit) and (dmod != "AlignMod"):
        with signals_blocked(self.AnnRi):
            # radii in rings of D.annWidth pixels: the beam's edge to a third of the way out
            w = float(self.D.annWidth) if self.D is not None else 1.0
            self.AnnRi.setValue((int(round(self.TBR.value() / w)), int(round((self.TBR.value() + self.P.RMax) / 3 / w))))
        self.VrApR.setValue(self.TBR.value())
        self.P.VrApXY = self.B0
        self.P.TransBeamInit = 1

    if locked_id is not None and self.SettingsWindow.DispImage.findData(locked_id) != -1:
        with signals_blocked(self.SettingsWindow.DispImage):
            self.SettingsWindow.DispImage.setCurrentIndex(self.SettingsWindow.DispImage.findData(locked_id))

    from callbacks.plotting import updateVecFieldUI  # noqa: E402
    updateVecFieldUI(self)          # vector fields only in CoM/DPC modes

    # hide custom mask maths tab
    self.SettingsWindow.SettingsTabGroup.setTabVisible(
        self.SettingsWindow.SettingsTabGroup.indexOf(
            self.SettingsWindow.MathTab), False)

    from callbacks.annularDetectorCallbacks import placeAnnStep  # noqa: E402
    placeAnnStep(self, dmod)        # Annular Integration Step: Alignment tab, or the annular tab

    match dmod:
        case "PrvwMod":
            self.DfrnDetrTabGroup.setCurrentIndex(0)
            previewCallbacks(self)
        case "AlignMod":
            # The full dataset: pattern (combined as the Pattern dropdown says, default mean), the real-space
            # image of an all-ones detector, and all-ones masks (MATLAB's alignment view).  Drawn through
            # plotImage — a bare imshow here skipped the histogram/statistics and the display settings,
            # and stacked a new image on the axes every time Align mode was entered.
            from callbacks.realSpaceROICallbacks import diffractionPattern  # noqa: E402
            from callbacks.plotting import plotImage  # noqa: E402
            self.Fig.Dfrn.Image = diffractionPattern(self, np.ones(self.Data.shape[0]))
            self.Fig.Real.Image = self.Data.sum(axis=1).reshape(real_shape(self.D))
            self.Fig.DfrnMask.Image = np.ones(dfrn_shape(self.D))
            self.Fig.RealMask.Image = np.ones(real_shape(self.D))
            for id, limits in (("DfrnMask", self.P.DfrnAxLim), ("RealMask", self.P.RealAxLim),
                               ("Dfrn", self.P.DfrnAxLim), ("Real", self.P.RealAxLim)):
                plotImage(self, id)
                self.Fig[id].fig.set_facecolor('black')
                self.Fig[id].ax.axis(limits)
            self.Fig.Dfrn.show()
            self.Fig.Real.show()

            # Create transmitted beam annotation, allow for disk as large as the entire diffraction pattern
            if self.A.tb is None:
                self.A.tb = InteractiveCircle(
                    center=self.B0,
                    radius=self.TBR.value(),
                    axis=self.Fig.Dfrn.ax,
                    color="r",
                    interactions="all")
                self.A.tb.connect()
                self.A.tb.updateCircle.connect(lambda: moveTransBeam(self))
                self.Fig.Dfrn.canvas.flush_events()

            self.DfrnDetrTabGroup.setCurrentIndex(1)
            transBeamCallbacks(self)

        case "AnnMod":
            self.DfrnDetrTabGroup.setCurrentIndex(2)
            self.dpcControls.setVisible(False)
            self.comControls.setVisible(False)
            annularDetectorCallbacks(self)  # TODO
        case "CoMMod" | "DPCMod":
            self.DfrnDetrTabGroup.setCurrentIndex(2)
            self.dpcControls.setVisible("DPC" in dmod)
            self.comControls.setVisible(True)
            annularDetectorCallbacks(self)  # first visit per dataset: also AutoCurl
            plotImage(self, 'ColorWheel')  # Plot ColorWheel #TODO
            # the phase/magnitude image and iCoM/dCoM always come up (even if hidden earlier); the
            # others are a click away on Settings > Windows, which is brought forward
            from callbacks.window_manager import showImageContent  # noqa: E402
            for id in COM_WINDOWS:
                self.Fig[id].show()
                showImageContent(self, id)
            self.Fig.CoMPhMag.activateWindow()
            self.SettingsWindow.SettingsTabGroup.setCurrentWidget(self.SettingsWindow.WindowsTab)
        case "VrApMod":  # 'Virtual Aperture'
            self.DfrnDetrTabGroup.setCurrentIndex(3)
            virtualApertureCallbacks(self)
        case "CustMod":
            self.DfrnDetrTabGroup.setCurrentIndex(4)
            self.SettingsWindow.SettingsTabGroup.setTabVisible(
                self.SettingsWindow.SettingsTabGroup.indexOf(
                    self.SettingsWindow.MathTab), True)
            customDetectorCallbacks(self, source=self.DetrMode)
            self.Fig.DfrnMask.activateWindow()

    enableWindows(self, True)


_SENDER = object()

COM_WINDOWS = ("CoMPhMag", "iCoM", "dCoM")       # shown on entering CoM/DPC mode


def syncCoMActions(self) -> None:
    """Window > Center of Mass (submenu and its items, shortcuts included) only in CoM/DPC mode."""
    in_com = self.DetrMode.currentData() in ("CoMMod", "DPCMod")
    self.menuCenter_of_Mass.menuAction().setEnabled(in_com)
    for action in self.menuCenter_of_Mass.actions():
        action.setEnabled(in_com)


def detrCoordCallbacks(self, source=_SENDER):
    """Detector coordinate options changed, or the diffraction scale/beam moved (*source* None:
    called from :func:`callbacks.alignment.moveTransBeam`, possibly outside a slot)."""
    src = self.sender() if source is _SENDER else source
    # "Polar" and "Absolute" are mutually exclusive
    match src:
        case self.SettingsWindow.DCSys:
            if self.SettingsWindow.DCSys.currentText() == "Polar":
                self.SettingsWindow.DCPos.setCurrentIndex(self.SettingsWindow.DCPos.findText("Relative"))
        case self.SettingsWindow.DCPos:
            if self.SettingsWindow.DCPos.currentText() == "Absolute":
                self.SettingsWindow.DCSys.setCurrentIndex(self.SettingsWindow.DCSys.findText("Cartesian"))
        case self.SettingsWindow.DCUnit:
            pass

    # Update coordinate conversion related convenient global properties
    self.DfPxR = 1
    self.RB0 = [0, 0]

    if self.SettingsWindow.DCUnit.currentText() == "mrad":
        self.DfPxR = self.mradPx.value()
    if self.SettingsWindow.DCPos.currentText() == "Relative":
        self.RB0 = self.B0

    # Update the current mode's coordinate displays.  Called directly: re-emitting
    # DCSys.currentIndexChanged (as before) re-entered this slot without end.
    match self.DetrMode.currentData():
        case "AnnMod" | "DPCMod" | "CoMMod":
            from callbacks.annularDetectorCallbacks import annularDetectorCallbacks  # noqa: E402
            annularDetectorCallbacks(self, source="units")      # radii shown in the (new) unit and scale
        case "VrApMod":
            from callbacks.virtualApertureCallbacks import syncVrApControls  # noqa: E402
            syncVrApControls(self)
        case "CustMod":
            customDetectorCallbacks(self, source=self.SettingsWindow.DCSys)


def customDetectorCallbacks(self, source=None):
    """Custom detector mode; implemented in :mod:`callbacks.customDetectorCallbacks`."""
    from callbacks.customDetectorCallbacks import customDetectorCallbacks as _custom  # noqa: E402
    _custom(self, source=source if source is not None else self.sender())
