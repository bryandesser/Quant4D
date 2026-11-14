"""Shared utility functions: dialogs, NaN checks, diff-to-prev, Qt workers."""
import os
import sys
import traceback
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *


def notifDLG(self, parent, icon="", msg="", ttl="", opt=[]):
    """ Wrapper for notification dialogs; use `sprintf()` before calling this function to process "\n" in `msg` """
    sel = ''

    # predefined Qt icons
    icons = dict()
    icons[""] = qtw.QMessageBox.NoIcon
    icons["help"] = qtw.QMessageBox.Question  # TODO ?
    icons["quest"] = qtw.QMessageBox.Question
    icons["none"] = qtw.QMessageBox.Information
    icons["warn"] = qtw.QMessageBox.Warning
    icons["error"] = qtw.QMessageBox.Critical

    from callbacks.startup import enableWindows  # noqa: E402  (deferred to avoid circular import)
    enableWindows(self, False)  # disable windows

    if icon == 'list':
        sel, ok = qtw.QInputDialog().getItem(parent, ttl, msg, opt, 0, False)  # default option 0, multiselect=False
        if not ok:
            enableWindows(self, True)  # enable windows
            return None

    else:
        dlg = qtw.QMessageBox(parent)  # establish a messagebox
        dlg.setIcon(icons[icon])  # set messagebox icon type
        dlg.setText(msg)  # set the message
        dlg.setWindowTitle(ttl)  # set the title

        match icon:
            case 'quest':
                for ii in opt:
                    dlg.addButton(ii, qtw.QMessageBox.YesRole)

            case '':
                pass

            case 'help' | 'warn' | 'error' | 'none':
                dlg.setStandardButtons(qtw.QMessageBox.Ok)  # only allow for an "Ok" button

        sel = dlg.exec_()  # Block background process until `msgbox()` is gone

    enableWindows(self, True)  # re-enable windows

    # convert from integer return to text
    match icon:
        case 'list':
            pass  # QInputDialog() will return the selected item text
        case 'quest':
            sel = opt[sel]
        case other:
            sel = 'Ok'

    return sel


def checkNaN(self, image, preview=False):
    """ Function to check nan/inf in data/image """

    if np.ma.masked_invalid(image).mask.any():
        ttl = 'NaN/Inf in Data!'
        msg = "There are NaN/Inf values in the data, which may indicate that the data structure is not correctly set " + \
            "(e.g. wrong Data Type, Byte Order, Data Offset, Frame Header/Footer etc).\n\nIf any data are corrupt, NaNs can be set to 0."

        if preview:  # For preview only
            opt = ["Continue", "Set NaNs to 0"]

        elif (self.D.PxD > 1) or (self.D.FrFoot + self.D.FrHead > 0):
            msg += "\n\nRe-importing with corrected configuration is suggested."
            opt = ["Continue", "Set NaNs to 0"]

        else:
            msg += "\n\nDo you want to swap the byte-order?"
            opt = ["Yes, try to swap the byte-order", "No"]
            self.SettingsWindow.activate()
            self.SettingsWindow.SettingsTabGroup.setCurrentWidget(
                self.SettingsWindow.InfoTab)  # Select the Data Info tab

        sel = notifDLG(self, self.ImportWindow, 'quest', msg, ttl, opt)

        # Execute the swap byte order callbacks
        if sel.startswith("Yes"):
            self.SettingsWindow.SwapByteOrder.click()

        return sel  # string of button, will be checked outside function for further action

    else:
        return None


def isDiffToPrev(self, name, val):
    """Function to check whether the named given value is changed compared to the previous value, and store the new value"""
    c = (not hasattr(self.Prev, name)) or (getattr(self.Prev, name) != val)

    # in case an image is being compared to an image, c will be an array of bool, not a single bool
    if isinstance(c, np.ndarray):
        c = c.all()

    if c:
        setattr(self.Prev, name, val)
    return c


class WorkerSignals(qtc.QObject):
    finished = qtc.pyqtSignal()
    error = qtc.pyqtSignal(tuple)
    result = qtc.pyqtSignal(np.ndarray)
    progress = qtc.pyqtSignal(int)


class Worker(qtc.QRunnable):
    def __init__(self, fn, *args):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args[0]
        self.signals = WorkerSignals()

    def run(self):
        # run the function, return results, and signal finished
        try:
            adfImages = self.fn(self.args)
        except BaseException:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(adfImages)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


def breakpoint(self):
    print()
