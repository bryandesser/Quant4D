"""Menu-bar actions and help icons that have no counterpart in MATLAB Quant4D's uifigure.

The PyQt main window has a menu bar (File / Settings / Window / Help); these are
the entries that are not simply "show a window":

* File → Swap Dataset…  — import another dataset keeping the current settings
  (opens the Import window with *Keep parameters* ticked).
* File → Auto Save Images… — save the selected images straight away with the
  Save window's current settings (MATLAB's ``AutoSaveImage`` button).
* File → Quit — close pyQuant4D (asks first, like the window's close button).
* Settings → Miscellaneous / Brightness and Contrast, Custom Aperture Maths —
  open the Settings window on that tab (maths: in Custom detector mode).
* Help → Quant4D Help (F1) — the online manual; Help → About.
"""
from __future__ import annotations

import os

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw

__all__ = ["connectMenus", "MANUAL_URL", "REPO_URL", "version"]

MANUAL_URL = "https://pyquant4d.readthedocs.io"
REPO_URL = "https://github.com/bryandesser/pyQuant4D"

MATH_HELP = ("• MATLAB syntax and functions are used (evaluated safely, not by MATLAB or eval).\n"
             "• Masks are referred to by their IDs (A, B, …, AA, …).\n"
             "• The X/Y dimensions of the images correspond to the 1st/2nd dimensions "
             "(rows/columns) of the arrays, as in MATLAB Quant4D.\n"
             "• Functions: abs sqrt exp log log2 log10 sin cos tan round floor ceil fix sign mod rem "
             "max min sum mean any all rot90 fliplr flipud circshift transpose double single logical "
             "not and or xor zeros ones numel size isnan isinf; constants pi eps Inf NaN true false.")
POLICY_HELP = ("Calculation policy\n"
               "• Active: recalculate images on every change, including while dragging.\n"
               "• Reduced: recalculate when a change is finished (on releasing a slider or annotation).\n"
               "• Passive: recalculate only with Update Images or when changing the detector mode.")


def version() -> str:
    try:
        from importlib.metadata import version as _v
        return _v("pyquant4d")
    except Exception:          # running from a source checkout without installing
        return "development version"


def connectMenus(self) -> None:
    """Connect the menu actions and set the help icons' tooltips; called once from ``slotsSignals``."""
    sw = self.SettingsWindow
    self.actionSwap_Dataset.triggered.connect(lambda *_: swapDataset(self))
    self.AutoSaveImg.triggered.connect(lambda *_: autoSaveImages(self))
    self.actionQuit.triggered.connect(lambda *_: self.close())
    self.actionMiscellaneous.triggered.connect(lambda *_: openSettingsTab(self, sw.MiscTab))
    self.actionBrightness_and_Contrast.triggered.connect(lambda *_: openSettingsTab(self, sw.DisplayTab))
    self.actionCustom_Aperture_Maths.setCheckable(False)      # opens the tab; nothing to toggle
    self.actionCustom_Aperture_Maths.triggered.connect(lambda *_: openMaths(self))
    self.actionQuant4D_Manual.triggered.connect(lambda *_: qtg.QDesktopServices.openUrl(qtc.QUrl(MANUAL_URL)))
    self.actionAbout_Quant4D.triggered.connect(lambda *_: about(self))

    # icons beside controls: information only (MATLAB shows these as tooltips)
    sw.MathHelpIcon.setToolTip(MATH_HELP)
    sw.MathHelpIcon.clicked.connect(lambda *_: qtw.QToolTip.showText(qtg.QCursor.pos(), MATH_HELP, sw.MathHelpIcon))
    sw.LiveUpdateImageIcon.setToolTip(POLICY_HELP)
    sw.LiveUpdateImageIcon.clicked.connect(
        lambda *_: qtw.QToolTip.showText(qtg.QCursor.pos(), POLICY_HELP, sw.LiveUpdateImageIcon))
    sw.RotDfrnIcon.setToolTip("Rotate the diffraction-space view (clockwise)")
    sw.RotRealIcon.setToolTip("Rotate the real-space view (clockwise)")


def openSettingsTab(self, tab) -> None:
    sw = self.SettingsWindow
    sw.show()
    sw.raise_()
    sw.activateWindow()
    sw.SettingsTabGroup.setCurrentWidget(tab)


def showPreviewDisplayControls(self) -> None:
    """Import preview: brightness/contrast/gamma of the preview on show, the Import window kept on top
    and active (MATLAB opened the display settings with the importer)."""
    openSettingsTab(self, self.SettingsWindow.DisplayTab)
    iw = self.ImportWindow
    iw.show()
    iw.raise_()
    iw.activateWindow()


def openMaths(self) -> None:
    """The maths tab belongs to the Custom detector mode: switch to it if a dataset is loaded."""
    if self.Data is not None and self.DetrMode.currentData() != "CustMod":
        self.DetrMode.setCurrentIndex(self.DetrMode.findData("CustMod"))
    if self.DetrMode.currentData() == "CustMod":
        openSettingsTab(self, self.SettingsWindow.MathTab)


def swapDataset(self) -> None:
    """Import another dataset, keeping the current detector and display settings."""
    self.ImportWindow.ImpKeepP.setChecked(True)
    self.ShowImportWdw.trigger()


def autoSaveImages(self):
    """Save the selected images now with the Save window's settings (creating the folder);
    without a folder, open the Save window instead."""
    from callbacks.save_export import saveImages
    from callbacks.utils import notifDLG
    sw = self.SaveWindow
    folder = sw.SaveDir.text().strip()
    if not folder:
        notifDLG(self, self, "warn", "Choose a folder in the Save window first.", "Directory Missing")
        sw.show()
        sw.SaveTabGroup.setCurrentWidget(sw.SaveImgTab)
        return None
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError as exc:
        notifDLG(self, self, "warn", f"Failed to create the directory:\n{exc}", "Directory Error")
        return None
    return saveImages(self)


def about(self) -> None:
    qtw.QMessageBox.about(
        self, "About pyQuant4D",
        f"<b>pyQuant4D</b> {version()}<br>"
        "Quantitative 4D-STEM data visualisation and analysis.<br><br>"
        "Python port of Quant4D (MATLAB) by Bryan Esser, Monash Imaging Physics.<br>"
        "Licensed under the GNU General Public License v3.0.<br><br>"
        f'<a href="{MANUAL_URL}">Manual</a> · <a href="{REPO_URL}">Source code</a>')
