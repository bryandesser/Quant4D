.. _functionality:

Functionality
=============

`Quant4D` has many useful features to allow you to quickly and intuitively
interactive with 4D-STEM data. Because it is built using MATLAB, it can be
installed on any platform that can run MATLAB, including Windows, Mac, and
Linux. The code is also GPU-accelerated when a GPU is present with enough
virtual memory to hold the entire 4D-STEM dataset plus some overhead for
additional data. 

Features
--------

.. Import
    ******
    File formats
    ^^^^^^^^^^^^
    The **Import Window** automatically attempts to determine the file type by
    the file extension, with preset routines for several common file formats
    (EMPAD, Gatan, Medipix, MRC, HDF5). Any file format can be opened if file
    structure is known. The import parameters required are the offset to the
    start of the data

    Bin/crop
    ^^^^^^^^
    Subsample
    ^^^^^^^^^
    Memorymap
    ^^^^^^^^^

Calibration
***********
`Quant4D` can be calibrated in diffraction space based on the known probe
convergence angle, which is then propagated through the rest of the GUI for
all detectors and masks generated. 

Automatic transmitted beam fitting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When a 4D-STEM dataset is first imported, `Quant4D` will attempt to find the
transmitted beam using the mean diffraction pattern from all probe positions. 
This is done using a circular Hough transform, giving preference to the
strongest circular feature nearest the center of the diffraction pattern. If
this routine fails outright or incorrectly fits the transmitted beam, the user
can manually fit the transmitted beam using either an interactive circular
annotation on the diffraction pattern, slider bars or numerical inputs (x, y,
radius). All of these methods are linked and update automatically. Additionally,
a routine is provided for aligning to the intersection of Kikuchi lines. The
user can press the **X** button in the **Transmitted Beam Position Alignment**
panel of the **Main Window**. The circular annotation will then be linked to the
intersection of two line annotations, which can be interactively moved by the
user to correspond to Kikuchi lines in the diffraction pattern. *Tip:* to better
see the Kikuchi patterns, change the gamma of the diffraction pattern display in
the **Display** tab of the **Settings** window. 

Diffraction scale
^^^^^^^^^^^^^^^^^

Annular/Round detectors
***********************

Virtual apertures
*****************

DPC/CoM
*******
iDPC/iCoM
^^^^^^^^^
dDPC/dCoM
^^^^^^^^^
Scan rotation estimation
^^^^^^^^^^^^^^^^^^^^^^^^

Custom apertures
****************

Aperture maths
**************

Export
******
Raw data
^^^^^^^^
Annotated display quality data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Bin/crop
^^^^^^^^