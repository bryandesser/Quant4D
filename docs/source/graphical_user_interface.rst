.. _graphical_user_interface:

Graphical user interface
========================
The graphical user interface (GUI) allows for intuitive interactions with the 4D-STEM data. The GUI consists of two main windows and several other windows as needed, as described below. 

Main Window
***********

Settings Window
***************
Import Window
*************
.. image:: ../_static/import_window.png
    :width: 306
    :height: 268
    :align: center

The import window allows the user to import several common file formats (EMPAD ``.raw``, Gatan ``.dm3/.dm4``, Medipix ``.mib``, MRC, HDF5) as well as any file format for which the user knows the file structure.

* ``.raw`` files are assumed to be in the EMPAD file format with 128x128 detector frames separated by a 1024 byte footer.
* ``.dm3/.dm4`` and ``.hdf5`` files are scanned allowing the user to select the correct dataset
* ``.mib`` file metadata are scanned for the relavent parameters. 

Parameters
^^^^^^^^^^
* `Sub-dataset`: Coice of dataset in hierarchical datasets such as ``.hdf5`` and ``.dm3/.dm4`` files.
* `Data offset`: Offset to the start of the 4D-STEM dataset in bytes.
* `Frame header`: Header data size in bytes repeated before *each* image frame. 
* `Frame footer`: Footer data size in bytes repeated after *each* image frame.
* `Data type`: Data type of the 4D-STEM dataset (8-, 16-, 32-, or 64-bit; signed integer, unsigned integer, or floating point)
* `Byte order`: Big or little endian ordering.
* `Pixels (x,y)`: Number of detector pixels in each frame. 
* `Frames (x,y)`: Number of probe positions.

File information
^^^^^^^^^^^^^^^^
* `Size`: Actual file size in GiB.
* `Estimated size`: Estimated dataset size in GiB based on the above parameters. If the two agree, the text will be shown in green; if not, it will show in red. 
* `Dataset Info from Metadata`: Information automatically detected from the file metadata.

Preview Window
**************
Image Windows
*************
Export Window
*************