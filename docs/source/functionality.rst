.. _functionality:

Functionality
=============

`Quant4D` has many useful features to allow you to quickly and intuitively
interactive with 4D-STEM data. Because it is built using MATLAB, it can be
installed on any platform that can run MATLAB, including Windows, Mac, and
Linux. The code is also GPU-accelerated when a GPU is present with enough
virtual memory to hold the entire 4D-STEM dataset plus some overhead for
additional data. 

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

Annular/Round detectors
-----------------------
The most basic and intuitive detector format, this mode provides the user with a
pair of circular annotations on the diffraction pattern, which are linked to
slider bars and numerical inputs in the main UI. These can be used to form
circular or annular detectors centered on the transmitted beam. The width of the
detector can be fixed by enabling the |radius_link| icon between the two slider
bars. This allows the user to change the inner and outer angles simultaneously.

When the user first switches to this mode from the **Alignment** mode, a
pre-calculation step is performed to improve display speeds upon interaction.
Here we calculate a range of images with a given annular step size, defined by
the **Annular Integration Step** field at the bottom of the panel in the main UI. 
This way, when the user changes the detector range, the images can be directly 
plotted, rather than calculated from the entire dataset. The initial value for 
**Annular Integration Step** is set to one pixel step in diffraction space, or a
maximum of 250 steps. This balances reasonably fine control of detector geometry
and computational efficiency; however, the user can directly change this step
size for finer/coarser control, at which point the pre-calculation is repeated
with the new step size. 

Virtual apertures
-----------------
This mode generates one or more round virtual apertures 

DPC/CoM
-------
iDPC/iCoM
*********
dDPC/dCoM
*********
Scan rotation estimation
************************

Custom apertures
----------------

Aperture maths
--------------

Export
------
Raw data
********
Annotated display quality data
******************************
Bin/crop
********


.. |radius_link| image:: ../../src/icons/link.png
    :height: 2ex