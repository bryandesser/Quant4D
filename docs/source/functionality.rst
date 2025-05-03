.. _functionality:

Functionality
=============

`Quant4D` has many useful features to allow you to quickly and intuitively interactive with 4D-STEM data. Because it is built using MATLAB, it can be installed on any platform that can run MATLAB, including Windows, Mac, and Linux. The code is also GPU-accelerated when a GPU is present with enough virtual memory to hold the entire 4D-STEM dataset plus some overhead for additional data. 

Features
--------

Import
******
File formats
^^^^^^^^^^^^
The **Import Window** automatically attempts to determine the file type by the file extension, with preset routines for several common file formats (EMPAD, Gatan, Medipix, MRC, HDF5). Any file format can be opened if file structure is known. The import parameters required are the offset to the start of the data

Bin/crop
^^^^^^^^
Subsample
^^^^^^^^^
Memorymap
^^^^^^^^^

Calibration
***********
Automatic transmitted beam fitting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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