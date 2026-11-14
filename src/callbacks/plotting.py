"""Image plotting and display callbacks."""
import os
import sys
import traceback
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import callbacks.appClass as appClass
from callbacks.appClass import *
import matplotlib
from callbacks.utils import isDiffToPrev


def displayCallbacks(self):

    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    id = self.SettingsWindow.DispImage.currentData()
    fig = self.Fig[id]
    ax = self.ImageAx[id]

    # Initial contrast will be set as the total range of min:max
    # A change in contrast will expand or contract the width of the range
    # Initial brightness will be also set as the total range of min:max
    # A change in brightness will result in shift of the range up or down
    # Initial gamma is set to 1
    # A change in gamma will result in a powerlaw change in contrast I' = I^gamma
    match self.sender():
        case self.SettingsWindow.HistLog:  # Log-scale option of histogram
            if self.SettingsWindow.HistLog.isChecked():
                self.SettingsWindow.HistAxes.axes.set_yscale('log')
            else:
                self.SettingsWindow.HistAxes.axes.set_yscale('linear')

        case self.SettingsWindow.DispLock:  # Lock "current" image
            # Change dropdown color if locked
            if self.SettingsWindow.DispLock.isChecked():
                backgroundStyle = "background:rgb(255,204,127.5);"  # orange
            else:
                backgroundStyle = ""  # default
            self.SettingsWindow.DispImage.setStyleSheet(backgroundStyle)

        case self.DispVecField:
            fig.vecField = self.DispVecField.currentData()  # Vector field

        case self.DispVecColor:  # Vector field color
            # Vector field color
            c = qtw.QColorDialog.getColor()
            if c.isValid():
                fig.vecColor = c
            else:
                return  # return if canceled

        case self.SettingsWindow.DispCMap:
            fig.cmap = self.SettingsWindow.DispCMap.currentText()  # chosen colormap

        case self.SettingsWindow.DispCMapInvert:
            fig.invert = self.SettingsWindow.DispCMapInvert.isChecked()  # Invert colormap

        case self.SettingsWindow.DispBrightnessReset:
            fig.brightness = 50  # Reset brightness

        case self.SettingsWindow.DispContrastReset:
            fig.contrast = 50  # Reset contrast

        case self.SettingsWindow.DispGammaReset:
            fig.gamma = 1  # Reset gamma

        case self.SettingsWindow.DispBrightness_NF | self.SettingsWindow.DispBrightness:
            fig.brightness = self.sender().value()  # Brightness

        case self.SettingsWindow.DispContrast_NF | self.SettingsWindow.DispContrast:
            fig.contrast = self.sender().value()  # Contrast

        case self.SettingsWindow.DispGamma | self.SettingsWindow.DispGamma_NF:
            fig.gamma = max(self.sender().value(), np.finfo(np.single).eps)  # Gamma

        case self.SettingsWindow.DispMaskOpa | self.SettingsWindow.DispMaskOpa_NF:
            fig.maskOpa = self.sender().value()  # Mask opacity

        case other:  # e.g. self.SettingsWindow.DispImage
            # Update GUIs by values stored in `self.ImageAx.(id).UserData` for the current selected image
            self.Fig[id].show()
            self.Fig[id].activateWindow()  # Bring selected image to front
            self.DispVecField.setCurrentIndex(self.DispVecField.findData(fig.vecField))
            self.SettingsWindow.DispCMap.setCurrentIndex(self.SettingsWindow.DispCMap.findText(fig.cmap))
            self.SettingsWindow.DispCMapInvert.setChecked(fig.invert)
            self.DispVecColor.setStyleSheet("background-color:" + fig.vecColor.name())

            # Enable vector field UIs if: 1) in CoM/DPC mode AND 2) real-space image selected
            enabledState = (self.DetrMode.currentData() in ["CoMMod", "DPCMod"]) and (fig.space == "Real")
            self.DispVecField.setEnabled(enabledState)
            self.DispVecFieldLabel.setEnabled(enabledState)
            self.DispVecColor.setEnabled(enabledState)

            # Disable brightness/contrast/colormap UIs if: (CoM/DPC) "Phase" and "ColorWheel for Phase" images
            enabledState = "Phase" not in fig.name  # enable components if NOT a Phase image
            self.SettingsWindow.DispBrightness.setEnabled(enabledState)
            self.SettingsWindow.DispBrightness_NF.setEnabled(enabledState)
            self.SettingsWindow.DispContrast.setEnabled(enabledState)
            self.SettingsWindow.DispContrast_NF.setEnabled(enabledState)
            self.SettingsWindow.DispGamma.setEnabled(enabledState)
            self.SettingsWindow.DispGamma_NF.setEnabled(enabledState)
            self.SettingsWindow.DispCMap.setEnabled(enabledState)
            self.SettingsWindow.DispCMapInvert.setEnabled(enabledState)

            # Disable mask opacity UIs if: ColorWheel/Mask/Preview images selected
            enabledState = (fig.space != "ColorWheel") and (fig.type not in ["Mask", "Preview"])
            self.SettingsWindow.ShowMaskWdw.setEnabled(enabledState)
            self.SettingsWindow.DispMaskOpa_NF.setEnabled(enabledState)
            self.SettingsWindow.DispMaskOpa.setEnabled(enabledState)

    # block signals during UI update
    self.blockAllSignals = False

    # Update UI
    self.SettingsWindow.DispBrightness_NF.setValue(fig.brightness)
    self.SettingsWindow.DispBrightness.setValue(fig.brightness)
    self.SettingsWindow.DispContrast_NF.setValue(fig.contrast)
    self.SettingsWindow.DispContrast.setValue(fig.contrast)
    self.SettingsWindow.DispGamma_NF.setValue(fig.gamma)
    self.SettingsWindow.DispGamma.setValue(fig.gamma)
    self.SettingsWindow.DispMaskOpa_NF.setValue(fig.maskOpa)
    self.SettingsWindow.DispMaskOpa.setValue(fig.maskOpa)

    # unblock signals
    self.blockAllSignals = False

    # Update image
    plotImage(self, id)  # Re-plot image


def plotImage(self, id):
    """Generic function for plotting an image on a given axis with brightness/contrast/gamma values"""

    # Special case for plotting the color wheel - can get unloaded
    if id == "ColorWheel":
        plotColorWheel(self)
        return

    # get image figure and axes
    fig = self.Fig[id]  # ImageWindow
    ax = fig.ax         # AxesSubplot
    im = np.ma.masked_invalid(self.Fig[id].Image)  # numpy masked array

    # clear old image(s)
    # [ii.remove() for ii in self.Fig[id].ax.get_images()]

    # return if image not yet plotted
    if im is None:
        if id == self.SettingsWindow.DispImage.currentData():
            self.SettingsWindow.ImStatsNotes.setPlainText(fig.name)
        return

    # get image min and max values and resultant range, ignore NaN and +/- Inf
    minVal = im.min()
    maxVal = im.max()
    intensityRange = maxVal - minVal

    # Brightness between -0.5 and 0.5; Contrast between -Inf and 0.5
    brightness = (fig.brightness - 50) / 100
    contrast = np.log2(np.max((np.finfo('single').eps, fig.contrast / 50))) / 2  # Avoid log2(0)

    # Display limits from brightness/contrast; have the same magnitude to the raw image `im`
    limitLow = minVal - (brightness - contrast) * intensityRange
    limitHigh = maxVal - (brightness + contrast) * intensityRange
    limitRange = limitHigh - limitLow

    # Normalize image, and apply display thresholds; `im` is always between 0 and 1
    if (limitHigh == limitLow) and (limitHigh <= 1 or limitHigh >= 0):
        # If display limits are both 1 or 0, then no rescale (e.g. `im` is all 1 or 0)
        pass

    elif (limitHigh > limitLow) or ((limitHigh == limitLow) and ((limitHigh > 1) or (limitHigh < 0))):
        # Typical case for upper limit > lower limit; apply limits and rescale [0,1]
        im = (im.clip(limitLow, limitHigh) - limitLow) / limitRange

    else:
        # Display limits are too close/identical, im becomes binary
        # If limits are NaN, then make them 0.5
        immi = (limitHigh + limitLow) / 2
        if np.isnan(immi):
            immi = 0.5
        limitHigh = limitLow = immi
        im = np.double(im > immi)

    # display image with gamma and brightness contrast applied
    if self.ImageAx[id] is None:
        self.ImageAx[id] = ax.imshow(im**fig.gamma)
    else:
        self.ImageAx[id].set_data(im**fig.gamma)
    self.ImageAx[id].set_clim(0, 1)

    # Plot mask opacity on non-mask/non-preview image; maskOpa is in percent (i.e. 50 => 50%)
    if fig.type not in ["Mask", "Preview"]:
        mask = self.Fig[fig.space + "Mask"].Image  # should be a logical mask
        self.ImageAx[id].set_alpha((1 - fig.maskOpa / 100) * (1 - mask.astype(bool)) + mask.astype(bool))

    # Shade CoM/DPC Phase with Magnitude
    if id == "CoMPhMag":
        CoMMagNorm = self.Fig.Dfrn.CoMMag
        CoMMagNorm -= np.nanmin(CoMMagNorm)
        CoMMagNorm /= np.nanmax(CoMMagNorm)
        self.ImageAx.CoMPhMag.set_alpha(self.ImageAx.CoMPhMag.get_alpha() * CoMMagNorm)

    plotVectorField(self, id)  # Plot vector field, if selected #TODO

    # Only update statistics if not in changing Event AND it is the "selected" image
    if (id == self.SettingsWindow.DispImage.currentData()):  # and isStaticEvt(evt): #TODO
        # don't update stats while things are changing, only when finished to increase responsiveness
        updateDispImgStats(self, id, minVal, maxVal, limitLow, limitHigh, limitRange)

    # set colormap
    self.ImageAx[id].set_cmap(fig.cmap + ["", "_r"][fig.invert])  # append "_r" if inverted

    # update plot
    if id != "Dfrn":
        fig.canvas.draw_idle()
    fig.canvas.flush_events()


def updateDispImgStats(self, id, minVal, maxVal, limitLow, limitHigh, limitRange):
    """Function to update image's statistics"""
    fig = self.Fig[id]
    ax = fig.ax
    im = np.ma.masked_invalid(fig.Image)

    # Update histogram skip if image unchanged
    if isDiffToPrev(self, 'im', im):
        if im.mask.any():
            nanwarn = "Contains NaN/Inf"
        else:
            nanwarn = ""
        self.SettingsWindow.ImStatsNotes.setPlainText(
            "min:{:< 14.7g}\tavg:{:< 14.7g}\nmax:{:< 14.7g}\tstd:{:< 14.7g}\nsum:{:< 14.7g}\t{:s}".format(
                minVal, np.nanmean(im), maxVal, np.nanstd(im), np.nansum(im), nanwarn))

        # try to clear the histogram
        try:
            self.SettingsWindow.HistAxes.axes.cla()
            self.A.hist = None
        except BaseException:
            pass

        # Generate an intensity histogram for the selected image
        binCounts, binEdges, self.A.hist = self.SettingsWindow.HistAxes.axes.hist(
            im.ravel(), bins=128, ec='k', linewidth=0.5)

        # Set histogram limits
        self.SettingsWindow.HistAxes.axes.set_xlim(binEdges.min(), binEdges.max())
        self.SettingsWindow.HistAxes.axes.set_ylim(
            0.5, (1.1 * binCounts).max().clip(1))  # Make sure upper limit is at least 1

        # set vertical scale
        if self.SettingsWindow.HistLog.isChecked():
            self.SettingsWindow.HistAxes.axes.set_yscale('log')
        else:
            self.SettingsWindow.HistAxes.axes.set_yscale('linear')

    # Update histogram annotations skip if values unchanged
    if isDiffToPrev(
        self,
        'hist',
        (ax,
         minVal,
         maxVal,
         limitLow,
         limitHigh,
         limitRange,
         fig.gamma,
         self.SettingsWindow.HistLog.isChecked())):
        # Create histogram ROI on first call; afterwards just reposition it
        if self.A.histBox is None:
            from callbacks.histBoxWidget import HistBox, histbox_to_sliders
            hist_ax = self.SettingsWindow.HistAxes.axes

            def _on_histbox_change(lo, hi):
                """Convert dragged limits back to brightness/contrast sliders."""
                b_new, c_new = histbox_to_sliders(lo, hi, minVal, maxVal)
                # Block the other spinbox while updating to avoid re-entry
                for w in [self.SettingsWindow.DispBrightness,
                          self.SettingsWindow.DispContrast,
                          self.SettingsWindow.DispBrightness_NF,
                          self.SettingsWindow.DispContrast_NF]:
                    w.blockSignals(True)
                self.SettingsWindow.DispBrightness.setValue(int(round(b_new)))
                self.SettingsWindow.DispBrightness_NF.setValue(b_new)
                self.SettingsWindow.DispContrast.setValue(int(round(c_new)))
                self.SettingsWindow.DispContrast_NF.setValue(c_new)
                for w in [self.SettingsWindow.DispBrightness,
                          self.SettingsWindow.DispContrast,
                          self.SettingsWindow.DispBrightness_NF,
                          self.SettingsWindow.DispContrast_NF]:
                    w.blockSignals(False)
                # Trigger a display refresh
                fig.brightness = int(round(b_new))
                fig.contrast = int(round(c_new))
                displayCallbacks(self)

            self.A.histBox = HistBox(hist_ax, limitLow, limitHigh,
                                     on_change=_on_histbox_change)

        # Reposition ROI if the caller is NOT the histBox itself (avoid loop)
        elif self.sender() is not self.A.histBox:
            self.A.histBox.update_position(limitLow, limitHigh)

        # Update other annotations
        # remove gamma curve
        try:
            self.A.histGamma.remove()
            self.A.histGamma = None
        except BaseException:
            pass
        # remove any text(s)
        if len(ax.texts):
            for ii in ax.texts:
                ii.remove()
        self.A.histNote = None

        # Gamma line
        x = np.linspace(limitLow, limitHigh, 128)  # histogram is on x_lim = [0,1]
        self.A.histGamma, = self.SettingsWindow.HistAxes.axes.plot(x, ((x - limitLow) / (limitHigh - limitLow))**fig.gamma * np.diff(
            self.SettingsWindow.HistAxes.axes.get_ylim()) + self.SettingsWindow.HistAxes.axes.get_ylim()[0], color='k')

        # Print display limits on the histogram
        textstr = "High:{:< 9.2e}\nLow:{:< 9.2e}".format(limitHigh, limitLow)

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        self.A.histNote = self.SettingsWindow.HistAxes.axes.text(
            0.05,
            0.95,
            textstr,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=props)  # , font="Courier")

        # update histogram canvas
        self.SettingsWindow.HistAxes.figure.canvas.draw_idle()


def plotVectorField(self, id):
    """ Function to plot a vector field image over top of the DPC or CoM images (either magnitude, angle, or combination) """
    fig = self.Fig[id]
    # try: #TODO
    #    self.A.vecField.remove()
    #    self.A.vecField = None
    # except:
    #    pass

    # vector field sampling (0,1:1,1:2,1:4,1:8,1:16)
    vec = fig.vecField

    # if vector field sampling == 0, or not currently in CoM or DPC modes, return
    if (not vec) or (self.DetrMode.currentData() not in ["CoMMod", "DPCMod"]):
        return

    # Plot vector arrows over the selected image
    x, y = np.meshgrid(np.arange(0, self.D.NFrX, vec), np.arange(0, self.D.NFrY, vec))
    u = self.Fig.Dfrn.CoMX[0::vec, 0::vec]
    v = self.Fig.Dfrn.CoMY[0::vec, 0::vec]
    self.A.vecField[id] = fig.ax.quiver(x, y, u, v, color=fig.vecColor, units='xy')
    fig.canvas.draw_idle()


def plotAllPatterns(self):
    # always update primary and mask images
    ids = [iID for iType, iID in zip(self.G.ImgType, self.G.ImgID) if iType in ["Primary", "Mask"]]
    # update CoM/DPC images if in the correct mode
    if self.DetrMode.currentData() in ["CoMMod", "DPCMod"]:
        ids += [iID for iType, iID in zip(self.G.ImgType, self.G.ImgID) if (iID != "ColorWheel") and (iType == 'CoM')]

    # Update images if visible OR not in changing event; include CoMs if in the modes
    for id in ids:
        if self.Fig[id].isVisible():  # or isStaticEvt(evt): #TODO?
            print(id, self.Fig[id].fig.stale)
            plotImage(self, id)


def plotColorWheel(self):
    # Make ColorWheel for DPC/CoM imaging - this color scheme will stay constant for all DPC/CoM images
    # regardless of their individual parameters like scan or detector rotation for consistency
    r = 256
    xgrid, ygrid = np.meshgrid(np.linspace(1 - r, r, int(2 * r)), np.linspace(1 - r, r, int(2 * r)))

    # Get atan from -pi to pi
    a = np.arctan2(ygrid, xgrid)

    # shift the negative values of atan up by 2*pi
    a[a < 0] += 2 * np.pi

    # make circular mask for colorwheel
    mask = (xgrid**2 + ygrid**2) < r**2

    # save masked colorwheel image
    self.Fig.ColorWheel.Image = a
    if self.ImageAx.ColorWheel is None:
        self.ImageAx.ColorWheel = self.Fig.ColorWheel.ax.imshow(
            self.Fig.ColorWheel.Image, alpha=mask.astype(float), cmap='hsv', interpolation="None")
    self.Fig.ColorWheel.maskOpa = 100
    self.Fig.ColorWheel.ax.axis('off')


def toUpdateImage(self):
    """
    Function to determine whether to update images
    Return true if any: 1) `self.SettingsWindow.CalcPolicy.currentData()` is 2 (active update)
                    OR 2) `self.SettingsWindow.CalcPolicy.currentData()` is 1 (reduced) and not when changing
                    OR 3) is a manual update (from update buttons or detector mode change)
    #TODO - currently does not support reduced update functionality
    """
    calc = self.SettingsWindow.CalcPolicy.currentData()
    # upd = (calc == 2) or (calc and isStaticEvt(evt)) or (evt.Source == self.UpdateImages) or (self.sender() == self.DetrMode)
    update = (calc == 2) or (self.sender() in [self.UpdateImages, self.DetrMode])
    return update


def updateImagesCallbacks(self):
    match self.sender():
        case self.SettingsWindow.CalcPolicy:
            # Update once if not passive
            if self.SettingsWindow.CalcPolicy.curentData():
                self.UpdateImages.trigger()

        case self.UpdateImages:  # Calculate and update all images
            # Trigger detector callbacks
            match self.DetrMode.currentData():
                case "PrvwMod":
                    previewCallbacks(self)
                case "AlignMod":
                    transBeamCallbacks(self)
                case 'AnnMod' | 'CoMMod' | 'DPCMod':
                    annularDetectorCallbacks(self)
                case "VrApMod":
                    virtualApertureCallbacks(self)
                case "CustMod":
                    customDetectorCallbacks(self)

            # Trigger real-space ROI callbacks
            if self.DetrMode.currentData() != "PrvwMod":
                realSpaceROICallbacks(self)
