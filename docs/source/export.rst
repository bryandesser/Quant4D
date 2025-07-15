.. _export:

.. |save_icon| image:: ../../src/icons/save.png
    :height: 2ex

.. |image_toolbar| image:: ../_static/image_toolbar.png
    :height: 2ex

===========
Save/Export
===========
Quant4D allows the user to save and export data in various formats. The Save/
Export dialog can be accessed by clicking the |save_icon| icon in the main UI,
pressing ctrl+s at any point, or selecting "Export -> Save as" on the toolbar
in any image window, |image_toolbar|. 

Save Images
***********
In the **Save Images** tab, the user may set a `Filename Prefix` that will be
prepended to all saved images. Additionally, tick boxes are provided to include
the inner and/or outer annular detector angles in the filename. A list of
available images is shown where the user can select one or more images.

*Tip:* To select specific images, hold down the control key (ctrl) while
clicking the desired images. To select a range of images, hold shift and click
the first and last image in the range. 

Data formats
============
After selecting the desired images, the user can choose the format in which the
images are saved. By default, both options are selected, but the user can
select one or both independently.

Raw data
--------
When the **Raw data** option is selected, data are saved as TIFF files at the
resolution of the original 4D-STEM dataset with raw intensity values directly
from the data as processed in the UI. This format is most useful for direct 
quantitative analysis of the data, as it preserves the original pixel density
and counts scale.

Annotated display quality data
------------------------------
When the **As-displayed** option is selected, data are saved as PNG files at
the desired resolution set by the user in the **DPI** field. Additionally, the
user can choose to include any annotations such as detectors, ROIs, axis
labels, etc. This format is most useful for presentation, publication, and
later reference as it provides a clear visualization of detectors and ROIs used
to generate the images, and can be saved at artificially higher resolution than
the original data.

Export Dataset
**************

Bin/crop
========
test