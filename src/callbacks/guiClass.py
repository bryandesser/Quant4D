import matplotlib.pyplot as plt
from matplotlib import cbook
from callbacks.allFunctions import startupFcn
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
        startupFcn(self)

        # place gui and show
        self.move(self.C.hOffset, self.C.vOffset)
        self.show()

        # connect screenChange slot/signal
        # self.windowHandle().screenChanged.connect(lambda: self.C.__setattr__("dpi",self.screen().physicalDotsPerInch()))
        # self.windowHandle().screenChanged.connect(lambda: self.pointPickerRadius.emit(self.screen().physicalDotsPerInch()))

    def closeEvent(self, event):
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
        self.canvas.setFocusPolicy(qtc.Qt.StrongFocus)
        self.ax.axis('off')
        self.ax.set_facecolor('black')

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

        # only use self.move() for dummy window test, it triggers a moveEvent
        # which draws the decoration so they can be measured
        pos = np.rint(pos).astype(int)  # make sure position is type int
        if id == "":
            self.move(pos[0], pos[1])
            self.show()
        else:
            self.setGeometry(qtc.QRect(pos[0], pos[1], pos[2], pos[3]))

        self.fig.canvas.mpl_connect('button_press_event', lambda id: self.activateFigure.emit(self.id))

        # add custom keyboard shortcuts
        self.shortcut = qtw.QShortcut(qtg.QKeySequence("Ctrl+W"), self)
        self.shortcut.activated.connect(lambda: self.hide())

        # activate native keyboard shortcuts
        self.canvas.mpl_connect('key_press_event', self.on_key_press)

    # change closeEvent behavior to hide rather than close window
    def closeEvent(self, a0: qtg.QCloseEvent) -> None:
        self.hide()
        self.isShown = False
        a0.ignore()
        return super().closeEvent(a0)

    def resizeEvent(self, a0: qtg.QResizeEvent) -> None:
        sizeChange = a0.size() - a0.oldSize()
        self.imageResize.emit(sizeChange, self.space)
        return super().resizeEvent(a0)

    def on_key_press(self, event):
        key_press_handler(event, self.canvas, self.toolbar)

    def mousePressEvent(self, a0: qtg.QMouseEvent) -> None:
        self.activateFigure.emit(self.id)
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
    def __init__(self, canvas, frame, name=None):
        NavigationToolbar2QT.__init__(self, canvas, frame)

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
                    a = cbook._topmost_artist(artists)
                    if a is not event.inaxes.patch:
                        # data = a.get_cursor_data(event) # deleted
                        # get data from the self.Fig[id].Image array rather than
                        # the plotted image, which is scaled. Ensure x,y indices
                        # do not go beyond the length/width of the image array
                        im = event.canvas.parent().parent().Image
                        xmax, ymax = im.shape
                        x = np.clip(round(event.xdata), 0, xmax - 1)
                        y = np.clip(round(event.ydata), 0, ymax - 1)
                        data = im[y, x]

                        # keep data format the matplotlib default
                        if data is not None:
                            data_str = a.format_cursor_data(data).rstrip()
                            if data_str:
                                s = s + '\n' + data_str
                return s
        return ""
