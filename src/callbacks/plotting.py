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
from callbacks.signals import all_signals_blocked, signals_blocked  # noqa: E402


def displayCallbacks(self, source=None):
    """Display controls (Settings → Display) for the selected image.

    *source* is the widget that changed; by default ``self.sender()``.  Callers that are not
    Qt slots (the histogram box, run from a matplotlib mouse event) must pass it — or ``"refresh"``
    — because ``self.sender()`` outside a signal can return a deleted object and crash.
    """
    # bypass execution if signals are actively being blocked (i.e. for programmatically updating UI values)
    if self.blockAllSignals:
        return

    id = self.SettingsWindow.DispImage.currentData()
    if id is None:  # nothing selected (e.g. while the list is being repopulated)
        return
    fig = self.Fig[id]
    ax = self.ImageAx[id]

    # Initial contrast will be set as the total range of min:max
    # A change in contrast will expand or contract the width of the range
    # Initial brightness will be also set as the total range of min:max
    # A change in brightness will result in shift of the range up or down
    # Initial gamma is set to 1
    # A change in gamma will result in a powerlaw change in contrast I' = I^gamma
    if source is None:
        source = self.sender()
    match source:
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

        case self.SettingsWindow.DispVecField:
            fig.vecField = self.SettingsWindow.DispVecField.currentData()  # Vector field

        case self.SettingsWindow.DispVecColor:  # Vector field color
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
            fig.brightness = source.value()  # Brightness

        case self.SettingsWindow.DispContrast_NF | self.SettingsWindow.DispContrast:
            fig.contrast = source.value()  # Contrast

        case self.SettingsWindow.DispGamma | self.SettingsWindow.DispGamma_NF:
            fig.gamma = max(source.value(), np.finfo(np.single).eps)  # Gamma

        case self.SettingsWindow.DispMaskOpa | self.SettingsWindow.DispMaskOpa_NF:
            fig.maskOpa = source.value()  # Mask opacity

        case other:  # e.g. self.SettingsWindow.DispImage
            # Update GUIs by values stored in `self.ImageAx.(id).UserData` for the current selected image
            self.Fig[id].show()
            self.Fig[id].activateWindow()  # Bring selected image to front
            self.SettingsWindow.DispVecField.setCurrentIndex(self.SettingsWindow.DispVecField.findData(fig.vecField))
            self.SettingsWindow.DispCMap.setCurrentIndex(self.SettingsWindow.DispCMap.findText(fig.cmap))
            self.SettingsWindow.DispCMapInvert.setChecked(fig.invert)
            self.SettingsWindow.DispVecColor.setStyleSheet("background-color:" + fig.vecColor.name())

            # Enable vector field UIs if: 1) in CoM/DPC mode AND 2) real-space image selected
            updateVecFieldUI(self)

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
            self.SettingsWindow.DispMaskOpaReset.setEnabled(enabledState)
            self.SettingsWindow.DispMaskOpa_NF.setEnabled(enabledState)
            self.SettingsWindow.DispMaskOpa.setEnabled(enabledState)

    # block signals during UI update
    with all_signals_blocked(self):
        # Update UI
        self.SettingsWindow.DispBrightness_NF.setValue(fig.brightness)
        self.SettingsWindow.DispBrightness.setValue(fig.brightness)
        self.SettingsWindow.DispContrast_NF.setValue(fig.contrast)
        self.SettingsWindow.DispContrast.setValue(fig.contrast)
        self.SettingsWindow.DispGamma_NF.setValue(fig.gamma)
        self.SettingsWindow.DispGamma.setValue(fig.gamma)
        self.SettingsWindow.DispMaskOpa_NF.setValue(fig.maskOpa)
        self.SettingsWindow.DispMaskOpa.setValue(fig.maskOpa)

    # Update image
    plotImage(self, id)  # Re-plot image


def resetDisplay(self) -> None:
    """Brightness, contrast and gamma of the selected image back to their defaults."""
    id = self.SettingsWindow.DispImage.currentData()
    if id is None:
        return
    fig = self.Fig[id]
    fig.brightness, fig.contrast, fig.gamma = 50, 50, 1
    displayCallbacks(self, source="refresh")        # the controls follow the image, which is redrawn


def connectHistogramReset(self) -> None:
    """Double-click the histogram to reset brightness, contrast and gamma; called once from slotsSignals."""
    canvas = self.SettingsWindow.HistAxes.figure.canvas
    canvas.mpl_connect("button_press_event", lambda e: resetDisplay(self) if e.dblclick else None)
    canvas.setToolTip("Drag the box to set the display range; double-click to reset brightness, contrast and gamma")


def plotImage(self, id):
    """Generic function for plotting an image on a given axis with brightness/contrast/gamma values"""

    # Special case for plotting the color wheel - can get unloaded
    if id == "ColorWheel":
        plotColorWheel(self)
        return

    # get image figure and axes
    fig = self.Fig[id]  # ImageWindow
    ax = fig.ax         # AxesSubplot

    # nothing computed yet (this check came after masked_invalid(None), which raised)
    if fig.Image is None:
        if id == self.SettingsWindow.DispImage.currentData():
            self.SettingsWindow.ImStatsNotes.setPlainText(fig.name)
        return
    im = np.ma.masked_invalid(fig.Image)  # numpy masked array

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
    disp = im**fig.gamma
    # Custom detector "Color Mix": show the RGB composite instead (Image keeps the union/real image for saving)
    colorMix = getattr(fig, "ColorMix", None)
    if colorMix is not None and self.DetrMode.currentData() == "CustMod":
        disp = np.clip(colorMix, 0, 1) ** fig.gamma
    if self.ImageAx[id] is None:
        self.ImageAx[id] = ax.imshow(disp)
        fitAxesToImage(ax, disp.shape)
        from callbacks.view_zoom import ensureLinked  # noqa: E402
        ensureLinked(self, id)      # zoom clamping and one view per space (cla() drops the callbacks)
    else:
        same_shape = np.shape(self.ImageAx[id].get_array())[:2] == disp.shape[:2]
        self.ImageAx[id].set_data(disp)
        if not same_shape:
            ny, nx = disp.shape[:2]
            self.ImageAx[id].set_extent((-0.5, nx - 0.5, ny - 0.5, -0.5))
            fitAxesToImage(ax, disp.shape)
    self.ImageAx[id].set_clim(0, 1)
    from callbacks.scale_bar import ensureScaleBar  # noqa: E402
    ensureScaleBar(self, id)        # bottom-right scale bar (re-added after ax.cla())

    # Plot mask opacity on non-mask/non-preview image; maskOpa is in percent (i.e. 50 => 50%)
    if fig.type not in ["Mask", "Preview"]:
        mask = self.Fig[fig.space + "Mask"].Image  # should be a logical mask
        self.ImageAx[id].set_alpha((1 - fig.maskOpa / 100) * (1 - mask.astype(bool)) + mask.astype(bool))

    # Shade CoM/DPC Phase with Magnitude
    if id == "CoMPhMag":
        # work on a copy so the stored CoM magnitude image is not rescaled in place
        CoMMagNorm = self.Fig.CoMMag.Image - np.nanmin(self.Fig.CoMMag.Image)
        CoMMagNorm = CoMMagNorm / max(np.nanmax(CoMMagNorm), np.finfo(np.float32).eps)
        self.ImageAx.CoMPhMag.set_alpha(self.ImageAx.CoMPhMag.get_alpha() * CoMMagNorm)

    plotVectorField(self, id)  # Plot vector field, if selected #TODO

    # Only update statistics if not in changing Event AND it is the "selected" image
    if (id == self.SettingsWindow.DispImage.currentData()):  # and isStaticEvt(evt): #TODO
        # don't update stats while things are changing, only when finished to increase responsiveness
        updateDispImgStats(self, id, minVal, maxVal, limitLow, limitHigh, limitRange)

    # set colormap
    self.ImageAx[id].set_cmap(fig.cmap + ["", "_r"][fig.invert])  # append "_r" if inverted

    # update plot (the diffraction window used to be skipped here, so brightness, contrast, gamma and
    # colour-map changes never showed on it; the annotations no longer paint stale backgrounds over it)
    fig.canvas.draw_idle()       # not flushed: rapid changes (a slider drag) coalesce into one redraw


def fitAxesToImage(ax, shape) -> None:
    """Axes limits on the image's pixels, and no autoscaling afterwards: annotations added later
    (contours, quivers, lines) used to rescale the axes, leaving a black margin around the image
    or undoing the user's zoom."""
    ny, nx = shape[:2]
    ax.set_xlim(-0.5, nx - 0.5)
    ax.set_ylim(ny - 0.5, -0.5)
    ax.set_autoscale_on(False)
    from callbacks.view_zoom import resetNavigation  # noqa: E402
    resetNavigation(ax)         # the toolbar's Home goes back to this view


def updateDispImgStats(self, id, minVal, maxVal, limitLow, limitHigh, limitRange):
    """Function to update image's statistics"""
    fig = self.Fig[id]
    ax = fig.ax
    im = np.ma.masked_invalid(fig.Image)

    # Update histogram skip if image unchanged
    image_changed = isDiffToPrev(self, 'im', im)
    if image_changed:
        if im.mask.any():
            nanwarn = "Contains NaN/Inf"
        else:
            nanwarn = ""
        self.SettingsWindow.ImStatsNotes.setPlainText(
            "min:{:< 14.7g}\tavg:{:< 14.7g}\nmax:{:< 14.7g}\tstd:{:< 14.7g}\nsum:{:< 14.7g}\t{:s}".format(
                minVal, np.nanmean(im), maxVal, np.nanstd(im), np.nansum(im), nanwarn))

        # clear the histogram (and its box: cla() removes the box's artists, so it is recreated)
        hax = self.SettingsWindow.HistAxes.axes
        if self.A.histBox is not None:
            try:
                self.A.histBox.remove()
            except (ValueError, AttributeError, NotImplementedError):
                pass
            self.A.histBox = None
        hax.cla()
        self.A.hist = self.A.histGamma = self.A.histNote = None
        self.Prev.hist = None       # cla() took the box, gamma curve and note: redraw them below

        # Intensity histogram of the finite values, drawn as one filled step artist
        # (128 bar patches made every histogram redraw slow, e.g. while dragging gamma)
        values = im.compressed()
        if values.size == 0:
            values = np.zeros(1)
        binCounts, binEdges = np.histogram(values, bins=128)
        self.A.hist = hax.stairs(binCounts, binEdges, fill=True, facecolor="C0", edgecolor="k", linewidth=0.5)

        # Set histogram limits, with a margin so the edges of the default display window (the data
        # range) sit inside the axes, where they can be grabbed
        lo_edge, hi_edge = float(binEdges.min()), float(binEdges.max())
        pad = 0.05 * (hi_edge - lo_edge) if hi_edge > lo_edge else 0.5
        self.SettingsWindow.HistAxes.axes.set_xlim(lo_edge - pad, hi_edge + pad)
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
                # the box is shared by every image: act on the one selected now, with its current range
                # (capturing fig/minVal/maxVal at creation adjusted the wrong image after a switch)
                cur = self.Fig[self.SettingsWindow.DispImage.currentData()]
                img = np.ma.masked_invalid(cur.Image)
                b_new, c_new = histbox_to_sliders(lo, hi, float(img.min()), float(img.max()))
                b_new, c_new = int(round(b_new)), int(round(c_new))   # the spin boxes take ints
                # Block the other spinbox while updating to avoid re-entry
                with signals_blocked(self.SettingsWindow.DispBrightness,
                                     self.SettingsWindow.DispContrast,
                                     self.SettingsWindow.DispBrightness_NF,
                                     self.SettingsWindow.DispContrast_NF):
                    for box, v in ((self.SettingsWindow.DispBrightness, b_new),
                                   (self.SettingsWindow.DispBrightness_NF, b_new),
                                   (self.SettingsWindow.DispContrast, c_new),
                                   (self.SettingsWindow.DispContrast_NF, c_new)):
                        box.setValue(type(box.value())(v))
                # Trigger a display refresh (not a Qt slot: say so rather than rely on self.sender())
                cur.brightness = b_new
                cur.contrast = c_new
                self.A._histDrag = True
                try:
                    displayCallbacks(self, source="refresh")
                finally:
                    self.A._histDrag = False

            def _on_gamma(gamma):
                """The gamma handle was dragged: set gamma as the slider does."""
                sw = self.SettingsWindow
                self.A._histDrag = True
                try:
                    sw.DispGamma_NF.setValue(gamma)        # its slot updates the slider and the image
                finally:
                    self.A._histDrag = False

            self.A.histBox = HistBox(hist_ax, limitLow, limitHigh,
                                     on_change=_on_histbox_change, on_gamma=_on_gamma)
            gmin = max(self.SettingsWindow.DispGamma_NF.minimum(), 1e-3)
            self.A.histBox.gamma_range = (gmin, self.SettingsWindow.DispGamma_NF.maximum())

        # Reposition the box unless it is being dragged (avoid a loop); a flag, because this also
        # runs from matplotlib events, where self.sender() can be a deleted object
        elif not getattr(self.A, "_histDrag", False):
            self.A.histBox.update_position(limitLow, limitHigh)

        # Update other annotations
        # remove gamma curve
        if self.A.histGamma is not None:
            try:
                self.A.histGamma.remove()
            except (ValueError, AttributeError, NotImplementedError):
                pass
            self.A.histGamma = None
        # remove the previous note (only that one: this used to remove every text from the *image*
        # axes, including the kx/ky axis-direction labels)
        if self.A.histNote is not None:
            try:
                self.A.histNote.remove()
            except (ValueError, AttributeError, NotImplementedError):
                pass
        self.A.histNote = None

        # Gamma line
        x = np.linspace(limitLow, limitHigh, 128)  # histogram is on x_lim = [0,1]
        span = limitHigh - limitLow
        ramp = (x - limitLow) / span if span > 0 else np.zeros_like(x)   # a flat image has no ramp
        y0, y1 = self.SettingsWindow.HistAxes.axes.get_ylim()
        self.A.histGamma, = self.SettingsWindow.HistAxes.axes.plot(x, ramp**fig.gamma * (y1 - y0) + y0, color='k')
        self.A.histBox.set_gamma(fig.gamma, y0, y1)        # its handle sits on the curve

        # Print display limits on the histogram
        textstr = "High:{:< 9.2e}\nLow:{:< 9.2e}".format(limitHigh, limitLow)

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        self.A.histNote = self.SettingsWindow.HistAxes.axes.text(
            0.05,
            0.95,
            textstr,
            transform=self.SettingsWindow.HistAxes.axes.transAxes,     # was the image axes' transform
            fontsize=10,
            verticalalignment='top',
            bbox=props)  # , font="Courier")

        image_changed = True

    # Repaint the histogram when anything on it changed.  This used to happen only when the display
    # limits changed, so a new image with the same minimum and maximum (a diffraction pattern at
    # another probe position, say) left the old histogram on screen.
    if image_changed:
        self.SettingsWindow.HistAxes.figure.canvas.draw_idle()


def plotVectorField(self, id):
    """Vector field (the CoM/DPC deflection, sampled every *vec* scan pixels) over a real-space image,
    in CoM/DPC modes only.  Replaces the previous arrows of that image."""
    fig = self.Fig[id]
    old = self.A.vectField.get(id)
    if old is not None:
        try:
            old.remove()
        except (ValueError, AttributeError, NotImplementedError):
            pass
        self.A.vectField[id] = None

    vec = int(fig.vecField or 0)        # sampling: 0 (none), 1:1, 1:2, 1:4, ...
    if (not vec) or fig.space != "Real" or (self.DetrMode.currentData() not in ["CoMMod", "DPCMod"]) \
            or self.Fig.CoMX.Image is None or self.Fig.CoMY.Image is None:
        return

    x, y = np.meshgrid(np.arange(0, self.D.NFrX, vec), np.arange(0, self.D.NFrY, vec))
    u = self.Fig.CoMX.Image[0::vec, 0::vec]
    v = self.Fig.CoMY.Image[0::vec, 0::vec]
    colour = fig.vecColor.name() if hasattr(fig.vecColor, "name") else fig.vecColor   # QColor -> '#rrggbb'
    # angles='xy': the arrows point along (u, v) in the image's own coordinates (y down the scan)
    self.A.vectField[id] = fig.ax.quiver(x, y, u, v, color=colour, angles='xy', units='xy', pivot='mid')
    fig.canvas.draw_idle()


def updateVecFieldUI(self) -> None:
    """The vector-field controls only apply to real-space images in CoM/DPC modes."""
    id = self.SettingsWindow.DispImage.currentData()
    fig = self.Fig[id] if id is not None else None
    enabled = (self.DetrMode.currentData() in ["CoMMod", "DPCMod"]) and fig is not None and fig.space == "Real"
    for w in (self.SettingsWindow.DispVecField, self.SettingsWindow.DispVecFieldLabel, self.SettingsWindow.DispVecColor):
        w.setEnabled(enabled)


def plotAllPatterns(self):
    # always update primary and mask images
    ids = [iID for iType, iID in zip(self.G.ImgType, self.G.ImgID) if iType in ["Primary", "Mask"]]
    # update CoM/DPC images if in the correct mode
    if self.DetrMode.currentData() in ["CoMMod", "DPCMod"]:
        ids += [iID for iType, iID in zip(self.G.ImgType, self.G.ImgID) if (iID != "ColorWheel") and (iType == 'CoM')]

    # Update images if visible OR not in changing event; include CoMs if in the modes
    for id in ids:
        if self.Fig[id].isVisible():  # or isStaticEvt(evt): #TODO?
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


def isChanging(self) -> bool:
    """True while the change that called us is still in progress (MATLAB's ValueChanging):
    a slider being dragged, or an annotation being dragged."""
    src = self.sender()
    if isinstance(src, qtw.QAbstractSlider) and src.isSliderDown():
        return True
    return bool(getattr(src, "dragging", False))


def toUpdateImage(self) -> bool:
    """Whether to recompute images now, from the calculation policy (Settings):

    * Active (2): always;
    * Reduced (1): unless the change is still in progress (a slider or an annotation being
      dragged) — the release brings a final update;
    * Passive (0): only for Update Images or a detector-mode change.
    """
    if self.sender() in (self.UpdateImages, self.DetrMode):
        return True
    calc = self.SettingsWindow.CalcPolicy.currentData()
    return calc == 2 or (calc == 1 and not isChanging(self))


def sliderReleased(self) -> None:
    """Reduced policy: a slider drag skipped the updates, so update once it is let go."""
    if self.SettingsWindow.CalcPolicy.currentData() == 1:
        self.UpdateImages.trigger()


def updateImagesCallbacks(self):
    from callbacks.alignment import transBeamCallbacks  # noqa: E402
    from callbacks.annularDetectorCallbacks import annularDetectorCallbacks  # noqa: E402
    from callbacks.detector import customDetectorCallbacks  # noqa: E402
    from callbacks.previewCallbacks import previewCallbacks  # noqa: E402
    from callbacks.realSpaceROICallbacks import realSpaceROICallbacks  # noqa: E402
    from callbacks.virtualApertureCallbacks import virtualApertureCallbacks  # noqa: E402
    match self.sender():
        case self.SettingsWindow.CalcPolicy:
            # Update once if not passive
            if self.SettingsWindow.CalcPolicy.currentData():
                self.UpdateImages.trigger()

        case self.UpdateImages:  # Calculate and update all images
            # Trigger detector callbacks
            match self.DetrMode.currentData():
                case "PrvwMod":
                    previewCallbacks(self)
                case "AlignMod":
                    transBeamCallbacks(self, self.UpdateImages)
                case 'AnnMod' | 'CoMMod' | 'DPCMod':
                    annularDetectorCallbacks(self)
                case "VrApMod":
                    virtualApertureCallbacks(self)
                case "CustMod":
                    customDetectorCallbacks(self)

            # Trigger real-space ROI callbacks
            if self.DetrMode.currentData() != "PrvwMod":
                realSpaceROICallbacks(self)
