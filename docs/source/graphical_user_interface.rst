.. _graphical_user_interface:

Graphical User Interface
========================

pyQuant4D presents four main windows that work together to let you load,
explore, and analyse 4D-STEM data.

Main window
-----------

The main window contains the primary controls:

- **Detector Mode** selector — switch between analysis modes
  (:ref:`alignment`, :ref:`annular_round`, :ref:`dpc_com`,
  :ref:`virtual_apertures`, etc.)
- **Brightness / Contrast / Gamma** sliders for the active image
- **Real-space frame** spinboxes (FrameX / FrameY) for point-ROI selection
- **Import**, **Settings**, and **Save/Export** toolbar buttons

Import window
-------------

Opened via the Import button.  Lets you:

- Browse for a dataset file (DM4, DM3, raw binary, HDF5, MRC, Medipix), or
  drop one onto any pyQuant4D window (see below)
- Set real-space and diffraction-pattern dimensions
- Choose a partial frame or pixel sub-range
- Estimate memory requirements before loading
- Enable GPU loading when a compatible device is present

**Drag and drop.**  Drop a dataset file on any pyQuant4D window (main,
Import, Settings, Save/Export or an image window) to open it in the Import
window, exactly as if it had been picked with **Select**: the file type is
chosen from the extension and the dimensions are read from the file.  Nothing
is loaded until you press **Import Data**.  ``.h5``, ``.hdf5`` and ``.emd``
open as HDF5, so a py4DSTEM file selects its 4-D ``DataCube``.  If several
files are dropped, only the first is opened (the import notes say so).
Folders are not accepted, and drops are ignored while an import is running.

Settings window
---------------

Contains tabs for display, windows, and miscellaneous options:

- **Display** — image selection (and lock), colour map, histogram, brightness,
  contrast, gamma and mask opacity
- **Windows** — buttons to show each image window and the vector-field overlay;
  the iCoM/dCoM bandpass filter; window size and orientation (axis directions,
  reversal, rotation, size) for diffraction and real space
- **Misc** — calculation policy, detector coordinate options, byte-order and
  X/Y swaps of the dataset
- **Info** — dataset information; **Show all variables** adds a **Variables**
  tab listing the dataset parameters and settings
- **Math** — formula for custom-detector Math masks (Custom Detectors mode)

Save / Export window
--------------------

See :ref:`export` for full details.

Image windows
-------------

Each analysis mode opens a set of image windows (diffraction pattern,
real-space image, CoM channels, etc.), each with a matplotlib toolbar for pan,
zoom and restore-view.

- **Pan**: drag the image (anywhere that is not an annotation) when zoomed in.
- **Zoom**: the mouse wheel zooms about the cursor; ``+`` and ``-`` zoom about
  the centre of the view; ``Home`` (or the toolbar's Home) shows the whole image
  again.  Views never extend past the image.
- **One view per space**: zooming or panning one diffraction-space image applies
  the same view to the other (pattern and mask); likewise for all real-space
  images (image, mask, CoM/DPC images).
- **Histogram**: double-click the histogram in Settings → Display to reset the
  brightness, contrast and gamma of the selected image.

.. note::
   Full screenshot walkthroughs will be added in a future documentation update.
