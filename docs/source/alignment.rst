.. _alignment:

Alignment
---------
Automatic transmitted beam fitting
**********************************
When a 4D-STEM dataset is first imported, `Quant4D` will attempt to find the
transmitted beam using the mean diffraction pattern from all probe positions. 
This is done using a
`circular Hough transform <https://mathworks.com/help/images/ref/imfindcircles.html>`_,
giving preference to the strongest circular feature nearest the center of the
diffraction pattern. If this routine fails outright or incorrectly fits the
transmitted beam, the user can manually fit the transmitted beam using either an
interactive circular annotation on the diffraction pattern, slider bars, or
numerical inputs (x, y, radius). All of these UI elements are linked and update
automatically.

Additionally, a routine is provided for aligning the transmitted beam to the
intersection of two lines. The user can press the **X** button in the
**Transmitted Beam Position Alignment** panel of the **Main Window**. The
circular annotation will then be linked to the intersection of two line
annotations, which can be interactively moved by the user to correspond, for 
example, to Kikuchi lines or a row of  diffraction spots.

*Tip:* to better see details in the diffraction pattern, use the
brightness/contrast/gamma controls in the **Display** tab of the **Settings**
window.  

Diffraction scale
*****************
`Quant4D` can be calibrated in diffraction space by fitting the transmitted beam
and reporting a known probe convergence angle in mrad, or by simply reporting a
known scale in mrad/pixels, which is then propagated through the rest of the GUI
for all detectors and masks generated. 

.. video:: ../_static/alignment.mp4
    :width: 100%
    :autoplay:
    :loop:
    :controlslist: nodownload,noremoteplayback