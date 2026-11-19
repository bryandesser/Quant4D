"""Window show/hide/toggle callbacks."""
import os
import sys
import traceback
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *
from callbacks.signals import signals_blocked  # noqa: E402
from contextlib import contextmanager  # noqa: E402


def placeBesideMain(self, window) -> None:
    """Put *window* to the right of the main window, tops aligned (on the left if it would leave
    the screen).  New windows otherwise open centred on the screen, under whatever is there."""
    main = self.frameGeometry()
    pad = int(self.C.decorPad or 0) * 2
    geo = window.frameGeometry()
    x = main.right() + 1 + pad
    screen = self.screen().availableGeometry() if self.screen() is not None else None
    if screen is not None and x + geo.width() > screen.right():
        x = max(screen.left(), main.left() - geo.width() - pad)
    window.move(x, main.top())


def placeImageWindows(self) -> None:
    """First layout of the image windows, beside the Settings window and at the top of its screen:
    the diffraction-space windows stacked in one column, the real-space windows in the next (at
    their default size; on a screen too narrow for both columns the real-space one overlaps the
    diffraction one rather than leave the screen).  Done once (on the first import); after that the
    windows stay where the user puts them."""
    if getattr(self, "_imageWindowsPlaced", False):
        return
    self._imageWindowsPlaced = True
    sw = self.SettingsWindow
    screen = sw.screen() or self.screen()
    if screen is None:
        return
    avail = screen.availableGeometry()
    pad = int(self.C.decorPad or 0)
    title = int(self.C.titleHeight or 0)
    frame_w = self.Fig.Dfrn.width() + 2 * pad
    x0 = sw.frameGeometry().right() + 1
    if x0 + frame_w > avail.right() + 1:          # Settings at the right edge: start from the left
        x0 = avail.left()
    x_real = max(x0, min(x0 + frame_w, avail.right() + 1 - frame_w))
    for id in self.G.ImgID:
        fig = self.Fig[id]
        if fig.space not in ("Dfrn", "Real") or getattr(fig, "group", None) is not None:
            continue
        x = x_real if fig.space == "Real" else x0
        # the client area, inside the frame: title bar at the top of the screen
        fig.setGeometry(qtc.QRect(int(x + pad), int(avail.top() + title), fig.width(), fig.height()))


@contextmanager
def busyIndicator(self):
    """Show the progress bar at the bottom of the main window as "busy" for the duration, then hide it."""
    self.progressBar.setTextVisible(False)
    self.progressBar.setMaximum(0)
    self.progressBarPanel.setVisible(True)
    self.progressBarPanel.setEnabled(True)
    try:
        yield
    finally:
        hideProgressBar(self)


def hideProgressBar(self) -> None:
    """The work is done: no progress bar left on the main window."""
    self.progressBar.setMaximum(1)
    self.progressBar.setValue(1)
    self.progressBarPanel.setVisible(False)


def toggleWindows(self):
    print(self.sender())
    match self.sender():
        case self.Fig.Dfrn:
            print(999)


def showAllWindows(self):
    for ii in self.Fig:
        self.Fig[ii].show()
    self.actionShow_All_Windows.setChecked(True)
    self.actionHide_All_Windows.setChecked(False)
    self.activateWindow()


def hideAllWindows(self):
    for ii in self.Fig:
        self.Fig[ii].hide()
    self.actionShow_All_Windows.setChecked(False)
    self.actionHide_All_Windows.setChecked(True)
    self.activateWindow()


def unHideOpenWindows(self):
    # figure out which windows should be re-shown after a hideAll event
    for action in self.menuDiffraction.actions() + self.menuReal_Space.actions() + self.menuCenter_of_Mass.actions():
        if not action.isSeparator() and action.isChecked():
            action.trigger()
            action.trigger()


def on_ShowImportWdw_triggered(self):
    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    self.ShowImportWdw.setChecked(not self.ImportWindow.isVisible())
    self.ImportWindow.show(self.ShowImportWdw.isChecked())

    if self.ShowImportWdw.isChecked():
        hideAllWindows(self)
        self.ImportWindow.activateWindow()
    else:
        unHideOpenWindows(self)


def showImageContent(self, id) -> None:
    """A window that was hidden is not redrawn (only visible images are): draw it now that it is
    shown.  CoM/DPC images not computed yet are computed first."""
    from callbacks.plotting import plotImage  # noqa: E402
    fig = self.Fig[id]
    if fig.Image is None and fig.type == "CoM" and id != "ColorWheel" \
            and self.DetrMode.currentData() in ("CoMMod", "DPCMod") and self.Data is not None:
        self.Prev.CoM_P = None              # whatever was computed before, it is not there now
        self.UpdateImages.trigger()         # computes every CoM/DPC image and draws the visible ones
        return
    if fig.Image is not None or id == "ColorWheel":
        plotImage(self, id)


def setPreviewTabs(self, preview: bool) -> None:
    """Import Preview shows only the tabs that apply to a preview: no Misc, Info or Math settings
    and no dataset export.  (Math is shown again only in Custom Detectors mode.)"""
    sw, tabs = self.SettingsWindow, self.SettingsWindow.SettingsTabGroup
    for tab in (sw.MiscTab, sw.InfoTab):
        tabs.setTabVisible(tabs.indexOf(tab), not preview)
    if preview:
        tabs.setTabVisible(tabs.indexOf(sw.MathTab), False)
        tabs.setTabVisible(tabs.indexOf(sw.VariablesTab), False)
    else:
        tabs.setTabVisible(tabs.indexOf(sw.VariablesTab), sw.ShowVariables.isChecked())
    self.SaveWindow.SaveTabGroup.setTabVisible(self.SaveWindow.SaveTabGroup.indexOf(self.SaveWindow.ExportTab),
                                               not preview)


def setWindowShown(self, id, shown: bool) -> None:
    """Show (and draw) or hide one image window, e.g. from the Window menu."""
    fig = self.Fig[id]
    if shown:
        fig.show()
        fig.activateWindow()
        showImageContent(self, id)
    else:
        fig.hide()


def showWindowCallbacks(self):
    id = self.SettingsWindow.DispImage.currentData()
    match self.sender():
        case self.SettingsWindow.ShowImageWdw:  # Show selected image
            self.Fig[id].show()
            self.Fig[id].activateWindow()
            showImageContent(self, id)
        case other:  # All other `self.Show***Wdw` buttons
            id = self.sender().accessibleName()
            if id in self.G.ImgID:
                self.Fig[id].show()
                self.Fig[id].activateWindow()
                showImageContent(self, id)
                # If `id` is one of the available images, select it
                if (not self.SettingsWindow.DispLock.isChecked()) and (self.SettingsWindow.DispImage.currentData()
                                                                       != id) and (self.SettingsWindow.DispImage.findData(id) != -1):
                    self.SettingsWindow.DispImage.setCurrentIndex(self.SettingsWindow.DispImage.findData(id))

# Function to import mask for given (diffraction/real) space


def resizeWindowCallbacks(self):
    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    # set the space: `Dfrn` or `Real`; get updated height and width, add mpl decor size
    if self.sender() in [
            self.SettingsWindow.WdwWDfrn,
            self.SettingsWindow.WdwHDfrn,
            self.SettingsWindow.WdwSetDfrn,
            self.SettingsWindow.WdwSetAllDfrn]:
        space = "Dfrn"
        width = self.SettingsWindow.WdwWDfrn.value() + self.C.mplDecor.width()
        height = self.SettingsWindow.WdwHDfrn.value() + self.C.mplDecor.height()
    else:
        space = "Real"
        width = self.SettingsWindow.WdwWReal.value() + self.C.mplDecor.width()
        height = self.SettingsWindow.WdwHReal.value() + self.C.mplDecor.height()

    match self.sender():
        case self.SettingsWindow.WdwSetDfrn | self.SettingsWindow.WdwSetReal:  # Set size for just one image window
            id = self.SettingsWindow.DispImage.currentData()  # Default image window to resize

            # If the selected image is not of that space, then resize that space's primary image window instead
            if self.Fig[id].space != space:
                id = space

            # temporarily block slots/signals to avoid recursion
            with signals_blocked(self.Fig[id]):
                # set the height and wdith
                self.Fig[id].resize(width, height)

        case self.SettingsWindow.WdwSetAllDfrn | self.SettingsWindow.WdwSetAllReal:  # Set all image windows of the given space to the same size
            for fig in self.G.ImgFig:
                if fig.space == space:
                    with signals_blocked(fig):
                        fig.resize(width, height)


def enableWindows(self, sw=True):
    """ Function to enable/disable windows/UI; disable is only for notification/progress bar/busy background etc """
    assert isinstance(sw, bool)

    prvw = self.DetrMode.currentData() == "PrvwMod"  # Preview mode or not
    # Detector Mode UI, keep disabled in Import Preview Mode unless a dataset is loaded
    self.DetrMode.setEnabled(sw and not prvw)  # (sw and (not prvw or self.D is not None))

    # Real-space ROI controls, keep disabled in Import Preview Mode
    self.RealSpacePanel.setEnabled(sw and not prvw)

    # Other UIs can be enabled in Import Preview Mode
    self.toolBar.setEnabled(sw)
    self.DfrnDetrTabGroup.setEnabled(sw)
    self.SettingsWindow.setEnabled(sw)
    self.SaveWindow.setEnabled(sw)
    self.ImportWindow.setEnabled(sw)

    # Also reset all windows' mouse pointer when enabling UIs
    if sw:
        [ii.setCursor(qtc.Qt.CursorShape.ArrowCursor) for ii in self.G.AllFig]
