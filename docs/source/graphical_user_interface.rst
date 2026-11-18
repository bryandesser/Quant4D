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

- Browse for a dataset file (DM4, DM3, raw binary, HDF5, MRC, Medipix)
- Set real-space and diffraction-pattern dimensions
- Choose a partial frame or pixel sub-range
- Estimate memory requirements before loading
- Enable GPU loading when a compatible device is present

Settings window
---------------

Contains tabs for display, layout, and miscellaneous options:

- **Display** — colourmap, invert, lock display to a single image
- **Windows** — show/hide individual image windows; resize controls
- **Variables** — read-only view of key dataset parameters
- **Info** — software version and system information

Save / Export window
--------------------

See :ref:`export` for full details.

Image windows
-------------

Each analysis mode opens a set of image windows (diffraction pattern,
real-space image, CoM channels, etc.), each with a matplotlib toolbar for pan,
zoom and restore-view.

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
