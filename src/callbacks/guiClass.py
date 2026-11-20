import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import sys
import os as _os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import uic


import matplotlib
matplotlib.use('Qt5Agg')


# Locate the gui/ directory relative to this file so the package works both
# when run from the repo root and when installed via pip.
_GUI_DIR = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "gui")

# Convert .ui Files from QT Designer to python
# Main window
MW_Ui, MW_Base = uic.loadUiType(_os.path.join(_GUI_DIR, "Quant4D_FigForm.ui"))
# Import window
IW_Ui, IW_Base = uic.loadUiType(_os.path.join(_GUI_DIR, "ImportDataForm.ui"))
# Settings window
SW_Ui, SW_Base = uic.loadUiType(_os.path.join(_GUI_DIR, "SettingsPanelForm.ui"))
# Save/Export window
EW_Ui, EW_Base = uic.loadUiType(_os.path.join(_GUI_DIR, "SavePanelForm.ui"))


class MainWindow(MW_Base, MW_Ui):
    pointPickerRadius = qtc.pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # startup function
        from callbacks.startup import startupFcn  # noqa: E402  (startup imports this module)
        startupFcn(self)

        # place gui and show
        self.move(self.C.hOffset, self.C.vOffset)
        self.show()

        # connect screenChange slot/signal
        # self.windowHandle().screenChanged.connect(lambda: self.C.__setattr__("dpi",self.screen().physicalDotsPerInch()))
        # self.windowHandle().screenChanged.connect(lambda: self.pointPickerRadius.emit(self.screen().physicalDotsPerInch()))

    embedded = False      # opened by pyquant4d.show(): closing must not end the Python session

    # Results for Python / notebooks, in py4DSTEM's conventions (callbacks.results)
    def calibration(self) -> dict:
        """The loaded dataset's calibration in py4DSTEM's names: see :func:`callbacks.results.calibration`."""
        from callbacks.results import calibration
        return calibration(self)

    def apply_calibration(self, datacube, *, scan_step: bool = True) -> dict:
        """Write the calibration into a py4DSTEM DataCube: see :func:`callbacks.results.apply_calibration`."""
        from callbacks.results import apply_calibration
        return apply_calibration(self, datacube, scan_step=scan_step)

    def image(self, key: str = "Real"):
        """A copy of an image, (Rx, Ry) or (Qx, Qy): see :func:`callbacks.results.image`."""
        from callbacks.results import image
        return image(self, key)

    def images(self) -> dict:
        """The images computed so far, ``{id: name}``."""
        from callbacks.results import images
        return images(self)

    def mask(self, key=None):
        """A copy of the current detector, the ROI or a custom detector: see :func:`callbacks.results.mask`."""
        from callbacks.results import mask
        return mask(self, key)

    def closeEvent(self, event):
        if self.embedded:
            for w in [self.ImportWindow, self.SettingsWindow, self.SaveWindow, *self.Fig.values()]:
                if isinstance(w, qtw.QWidget):
                    w.close()
            event.accept()
            return
        # In headless / CI mode (QT_QPA_PLATFORM=offscreen) do not show a
        # QMessageBox: on Windows it triggers a fatal access violation at the
        # C++ level before Python can handle it.  Also avoid sys.exit() which
        # would kill the whole test-runner process.
        if _os.environ.get('QT_QPA_PLATFORM', '') == 'offscreen':
            event.accept()
            qtw.QApplication.quit()
            return

        reply = qtw.QMessageBox.question(self, 'Window Close', 'Are you sure you want to quit?',
                                         qtw.QMessageBox.No | qtw.QMessageBox.Yes, qtw.QMessageBox.No)

        if reply == qtw.QMessageBox.Yes:
            event.accept()
            # close all windows and quit application
            sys.exit()
        else:
            event.ignore()

    def receiveThreadData(self, data):
        self.Data = data

    def receiveWorkerData(self, adfImages):
        self.adfImages = adfImages


class ImportWindow(IW_Base, IW_Ui):
    xEvent = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def closeEvent(self, a0: qtg.QCloseEvent) -> None:
        self.hide()
        self.xEvent.emit()
        a0.ignore()
        return super().closeEvent(a0)


class SettingsWindow(SW_Base, SW_Ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def closeEvent(self, a0: qtg.QCloseEvent) -> None:
        self.hide()
        a0.ignore()
        return super().closeEvent(a0)


class SaveWindow(EW_Base, EW_Ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def closeEvent(self, a0: qtg.QCloseEvent) -> None:
        self.hide()
        a0.ignore()
        return super().closeEvent(a0)


class ImageWindow(qtw.QMainWindow):
    imageResize = qtc.pyqtSignal((qtc.QSize, str))
    activateFigure = qtc.pyqtSignal(str)

    # callbacks.window_groups.GroupWindow holding this image when its space is grouped into tabs.
    # show/hide/isVisible/activateWindow then ask the group (Python callers only: Qt's own calls,
    # e.g. a tab widget hiding the pages not shown, go to QMainWindow directly).
    group = None

    def show(self):
        if self.group is not None:
            self.group.showMember(self)
        else:
            super().show()

    def hide(self):
        if self.group is not None:
            self.group.hideMember(self)
        else:
            super().hide()

    def isVisible(self) -> bool:
        return self.group.isShown(self) if self.group is not None else super().isVisible()

    def activateWindow(self):
        if self.group is not None:
            self.group.selectMember(self)
        else:
            super().activateWindow()

    def __init__(self, id, name, space, typ, cmap, pos):
        super().__init__
        qtw.QMainWindow.__init__(self)

        self.setObjectName(id)

        self.imageWidget = qtw.QWidget(self)
        self.setCentralWidget(self.imageWidget)
        layout = qtw.QVBoxLayout(self.imageWidget)

        px = 1 / plt.rcParams['figure.dpi']
        self.fig = Figure(figsize=(pos[2] * px, pos[3] * px))
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(bottom=0, right=1, top=1, left=0)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setFocusPolicy(qtc.Qt.FocusPolicy.StrongFocus)
        self.ax.axis('off')
        self.ax.set_facecolor('black')
        from callbacks.axis_direction import install_view_transform  # noqa: E402
        install_view_transform(self.ax)     # flips/rotation of the view (Settings → axis directions)
        self.axisArrows = []                # kx/ky (rx/ry) direction arrows
        self.menuAction = None              # the Window menu's show/hide action for this image
        self.zoomKeys = None                # view_zoom.handleKey for this window (set by connectZoom)

        layout.addWidget(self.canvas)

        # Set defaults for the given window
        self.setWindowTitle(name)

        self.id = id             # window id
        self.space = space       # real or diffraction space?
        self.type = typ          # type of image: Primary (Dfrn and Real), Mask, CoM
        self.cmap = cmap         # colormap
        self.invert = 0          # invert colormap?
        self.maskOpa = 0         # mask opacity
        self.Tag = space + " " + typ  # tag used for finding windows
        self.name = name         # image name
        self.brightness = 50     # brightness value
        self.contrast = 50       # contrast value
        self.gamma = 1           # gamma value
        self.vecField = 0        # vector field display logical
        self.isShown = False     # help with hiding/showing groups of windows
        self.Image = None        # actual image data will be stored here; displayed data is modified by brightness/contrast/gamma

        # set defaul vector color for overlays
        if cmap == "gray":
            self.vecColor = qtg.QColor('red')  # red
        else:
            self.vecColor = qtg.QColor('white')  # white

        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        # the cursor position and intensity go to a status bar under the toolbar, so the toolbar keeps
        # its width (the readout used to push the diffraction "Pattern" dropdown behind ">>")
        self.statusBar().setSizeGripEnabled(False)

        # only use self.move() for dummy window test, it triggers a moveEvent
        # which draws the decoration so they can be measured
        pos = np.rint(pos).astype(int)  # make sure position is type int
        if id == "":
            self.move(pos[0], pos[1])
            self.show()
        else:
            self.setGeometry(qtc.QRect(pos[0], pos[1], pos[2], pos[3]))

        self.fig.canvas.mpl_connect('button_press_event', lambda id: self.activateFigure.emit(self.id))  # pyright: ignore[reportAttributeAccessIssue] (class-level pyqtSignal)

        # add custom keyboard shortcuts
        self.shortcut = qtw.QShortcut(qtg.QKeySequence("Ctrl+W"), self)
        self.shortcut.activated.connect(lambda: self.hide())

        # activate native keyboard shortcuts
        self.canvas.mpl_connect('key_press_event', self.on_key_press)

    def _syncMenuAction(self, shown: bool) -> None:
        """Keep the Window menu's tick for this image in step with the window."""
        action = getattr(self, "menuAction", None)
        if action is not None and action.isChecked() != shown:
            action.blockSignals(True)
            action.setChecked(shown)
            action.blockSignals(False)

    def showEvent(self, a0) -> None:
        if self.group is None:              # grouped: the group keeps the menu ticks (tab switches hide pages)
            self._syncMenuAction(True)
        result = super().showEvent(a0)
        if self._wantImage is not None and self.isWindow():     # sized while hidden: make it exact now
            self.setImageSize(*self._wantImage)
        return result

    def hideEvent(self, a0) -> None:
        if self.group is None:
            self._syncMenuAction(False)
        return super().hideEvent(a0)

    # change closeEvent behavior to hide rather than close window
    def closeEvent(self, a0: qtg.QCloseEvent) -> None:
        self.hide()
        self.isShown = False
        a0.ignore()
        return super().closeEvent(a0)

    _decor = None          # (class default) the last decoration measured on any shown image window
    _wantImage = None      # display size asked for while hidden: applied exactly when shown

    def _layoutNow(self) -> None:
        """Lay the window out at its current size now, so the canvas has its size."""
        for lay in (self.layout(), self.centralWidget().layout() if self.centralWidget() else None):
            if lay is not None:
                lay.activate()

    def _shown(self) -> bool:
        return qtw.QMainWindow.isVisible(self)          # the widget itself (not its tab group)

    def decorSize(self) -> qtc.QSize:
        """Everything in the window around the image canvas (margins, toolbar, status bar): measured
        while the window is shown, otherwise the last measurement (a hidden window is not laid out)."""
        if self._shown():
            self._layoutNow()
            d = self.size() - self.canvas.size()
            self._decor = ImageWindow._decor = d
            return d
        return self._decor or ImageWindow._decor or qtc.QSize(0, 0)

    def imageSize(self) -> qtc.QSize:
        """The display area: the canvas the image is drawn on (for a hidden window, what it will be)."""
        if self._shown():
            self._layoutNow()
            return self.canvas.size()
        return self.size() - self.decorSize()

    def setImageSize(self, width: int, height: int) -> None:
        """Resize the window so its display area (the canvas) is *width* x *height*, the toolbar,
        status bar and margins coming on top.  Checked again after the layout (the toolbar can
        wrap at a new width); a hidden window is checked when it is next shown."""
        self._wantImage = (int(width), int(height))
        if not self._shown():
            d = self.decorSize()
            self.resize(int(width) + d.width(), int(height) + d.height())
            return
        for _ in range(3):
            have = self.imageSize()
            if have.width() == width and have.height() == height:
                break
            self.resize(self.width() + width - have.width(), self.height() + height - have.height())
        self._wantImage = None

    def resizeEvent(self, a0: qtg.QResizeEvent) -> None:
        if not self.isWindow():             # a tab of a grouped space: not a window size
            return super().resizeEvent(a0)
        self.imageResize.emit(a0.size(), self.space)     # the new size (Settings > Windows > window size)  # pyright: ignore[reportAttributeAccessIssue] (class-level pyqtSignal)
        return super().resizeEvent(a0)

    def on_key_press(self, event):
        # zoom keys (+, -, Home) and keys that make no sense on an image are handled first
        zoom_keys = getattr(self, "zoomKeys", None)
        if zoom_keys is not None and zoom_keys(event):
            return
        key_press_handler(event, self.canvas, self.toolbar)

    def mousePressEvent(self, a0: qtg.QMouseEvent) -> None:
        self.activateFigure.emit(self.id)  # pyright: ignore[reportAttributeAccessIssue] (class-level pyqtSignal)
        return super().mousePressEvent(a0)

    # TODO: clicking title bar activates window, but does not trigger a mousePressEvent;
    #      using qtc.QEvent.ActivationChange falls into a recursive spiral as when one window activates
    #      another deactivates, sending two competing signals
    #
    # def changeEvent(self, a0: qtc.QEvent) -> None:
    #     if hasattr(self,'id'):
    #         print(self.id,dict([(getattr(a0,ii),ii) for ii in dir(a0) if ((not ii.startswith("_")) and not (callable(getattr(a0,ii))))])[a0.type()],self.hasFocus())
    #     else:
    #         print(dict([(getattr(a0,ii),ii) for ii in dir(a0) if ((not ii.startswith("_")) and not (callable(getattr(a0,ii))))])[a0.type()],self.hasFocus())

    #     if (a0.type() == qtc.QEvent.ActivationChange) and (not self.isActiveWindow()):
    #         print(self.id,self.isActiveWindow())
    #         self.activateFigure.emit(self.id)
    #     return super().changeEvent(a0)

    # def focusInEvent(self, a0: qtg.QFocusEvent) -> None:
    #     print(999)
    #     return super().focusInEvent(a0)


# subclass NavigationToolbar2QT such that the image intensity displayed
# is NOT effected by brightness/contrast/gamma scaling. Only the
# event-based data picking has been modified:
# data = a.get_cursor_data(event)
class NavigationToolbar(NavigationToolbar2QT):
    """Matplotlib's toolbar without its coordinate label: the readout goes to the window's status bar."""

    def __init__(self, canvas, frame, name=None):
        NavigationToolbar2QT.__init__(self, canvas, frame, coordinates=False)
        self._frame = frame

    def set_message(self, s):
        frame = getattr(self, "_frame", None)          # set after matplotlib's __init__
        bar = frame.statusBar() if isinstance(frame, qtw.QMainWindow) else None
        if bar is not None:
            bar.showMessage("  ".join(part.strip() for part in str(s).splitlines() if part.strip()))

    @staticmethod
    def _mouse_event_to_message(event):
        if event.inaxes and event.inaxes.get_navigate():
            try:
                s = event.inaxes.format_coord(event.xdata, event.ydata)
            except (ValueError, OverflowError):
                pass
            else:
                s = s.rstrip()
                artists = [a for a in event.inaxes._mouseover_set
                           if a.contains(event)[0] and a.get_visible()]
                if artists:
                    a = max(artists, key=lambda art: art.zorder)   # topmost (cbook._topmost_artist is private)
                    if a is not event.inaxes.patch:
                        # data = a.get_cursor_data(event) # deleted
                        # get data from the self.Fig[id].Image array rather than
                        # the plotted image, which is scaled. Ensure x,y indices
                        # do not go beyond the length/width of the image array
                        im = event.canvas.parent().parent().Image
                        ymax, xmax = im.shape          # images are (y, x); was swapped for non-square images
                        x = np.clip(round(event.xdata), 0, xmax - 1)
                        y = np.clip(round(event.ydata), 0, ymax - 1)
                        data = im[y, x]

                        # keep data format the matplotlib default
                        if data is not None:
                            data_str = a.format_cursor_data(data).rstrip()
                            if data_str:
                                # pixel indices and the raw value: short enough to share the status bar
                                # with the diffraction "Pattern" dropdown
                                s = f"x={x}, y={y}\n{data_str.strip('[]')}"
                return s
        return ""
