.. _export:

Saving and Exporting
====================

Open the **Save / Export** panel from the toolbar.

Launching the application
-------------------------

After installation, launch pyQuant4D from the command line::

    quant4d

or run directly from the repository root::

    python Quant4D_app.py

Save images
-----------

Select one or more images from the list, choose a directory and filename
prefix, then save as:

- **TIFF** — 32-bit float, lossless
- **PNG** — 8-bit, with optional annotations (scale bar, colourbar)

Export dataset
--------------

Export the 4-D dataset (everything, or a part of it) from the **Export** tab.
**Part of the scan** takes a start point, a number of positions and a
sampling step; **part of the pattern** a start point, a number of pixels and
a binning factor.  Coordinates are 0-based ``(x, y)``.  The notes box shows
the file name, the shape ``(NFrY, NFrX, NPxY, NPxX)``, the data type and the
size before anything is written.  Integer data are widened when binning, so
binned sums cannot overflow.

Formats:

- **HDF5** (``.h5``) — the dataset ``/data``, stored contiguously and
  uncompressed (so pyQuant4D can import it again quickly), with the session
  (source file, export region, beam centre, ``mrad``/px, convergence angle)
  as attributes of ``/metadata``.
- **Raw binary** (``.raw``) — headerless, little- or big-endian, frame after
  frame.  Tick **dimension suffix** to add ``_<NPxX>x<NPxY>x<NFrX>x<NFrY>``
  to the name, which the importer reads back.
- **py4DSTEM EMD** (``.h5``) — an EMD 1.0 file that ``py4DSTEM.read`` opens
  as a ``DataCube`` (py4DSTEM does not need to be installed to write it).

py4DSTEM export
^^^^^^^^^^^^^^^

Once the transmitted beam has been set, the file carries a py4DSTEM
calibration of the *exported* pixels:

- detector pixel size ``Q_pixel_size`` in mrad: ``mrad/px`` × binning;
- the beam centre as py4DSTEM's origin (``qx0_mean``/``qy0_mean`` and
  constant ``qx0``/``qy0`` maps over the scan), shifted and scaled for the
  exported region;
- the convergence semi-angle as ``probe_semiangle``;
- scan step ``R_pixel_size``: the loaded data's scan step (Settings > Misc >
  Real-space Calibration) × the export sampling, in its units; uncalibrated,
  in positions of the source scan.  Cropping changes neither scale.

Before the beam is set, the detector is left uncalibrated (pixels).

The images selected on the **Save Images** tab are stored with the dataset:
real-space images as ``VirtualImage`` and diffraction images as
``DiffractionSlice``, cropped, sampled or binned like the dataset (binned
diffraction images are summed).  Images not computed yet are skipped; the
notes box lists what will be embedded.

Binned diffraction **masks** are summed like the data by default (raw: a
binned pixel holds 0 to *b*² for binning *b*, consistent with the summed
intensities).  Tick **Normalise binned masks (0 to 1)** in the partial
pattern group to divide by the bin area instead, giving the fraction of each
binned pixel inside the mask.  Real-space masks are sampled, not binned, and
stay as they are.  In py4DSTEM::

    import py4DSTEM
    datacube = py4DSTEM.read("export.h5")
    datacube.calibration.get_origin_mean()   # (row, column) = pyQuant4D (y, x)
    datacube.tree("Real")                    # an embedded image

.. note::

   py4DSTEM names its axes in matrix order: ``(Rx, Ry, Qx, Qy)`` is
   pyQuant4D's ``(ry, rx, py, px)``.  The array is the same, but every
   coordinate pair swaps: py4DSTEM's ``qx0`` is pyQuant4D's beam **y**.

The pyQuant4D session record is stored alongside, in the metadata bundle
``pyquant4d`` (it includes the scan step and the accelerating voltage, also
written to the plain HDF5 export's ``/metadata``).  A progress indicator is
shown during export.
