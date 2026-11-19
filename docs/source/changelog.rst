Changelog
=========

Unreleased
----------

- Export to py4DSTEM: a "py4DSTEM EMD (*.h5)" export format that
  ``py4DSTEM.read`` opens as a ``DataCube``, with the beam centre, detector
  pixel size (mrad) and convergence angle as its calibration and the images
  selected on the Save Images tab embedded.  Written with h5py alone.
- Drag and drop: drop a dataset file on any window to open it in the Import
  window; ``.hdf5`` and ``.emd`` files are now recognised as HDF5.
- Import from py4DSTEM: an EMD file's DataCube calibration (beam centre,
  mrad/px, convergence angle) sets the transmitted beam after import, allowing
  for partial import and binning; the import notes describe it.
- Accelerating voltage field in the Import window; a py4DSTEM calibration in
  Å⁻¹ is converted to mrad with the relativistic electron wavelength.
- Real-space calibration: **Scan Step** of the file in the Import window
  (filled in from calibrated py4DSTEM/pyQuant4D files) and of the loaded data
  in Settings > Misc (editable after import); scaled by import and export
  sampling, listed in the Info tab and written on export.
- Info tab: the real-space size was shown as Y⨯X under an X⨯Y label.
- Scan step read from DM3/DM4 calibrations (with the microscope voltage) and
  MRC cells (z spacing).
- Scale bars on the real-space and diffraction windows (scan step / mrad, or
  pixels when uncalibrated), with Show scale bar toggles in Settings > Windows.
- Binned diffraction masks in the py4DSTEM export: raw sums by default, or
  normalised to 0..1.
- File > Open with py4DSTEM Reader... (when py4DSTEM is installed) and
  ``pyquant4d.show(datacube)`` from Python; ``pip install pyquant4d[py4dstem]``.
- The diffraction scale (mrad/px) shows 4 decimals.
- A path typed into the Import window starts the HDF5 dataset list again for a
  new file; the dataset picked is kept otherwise (also across file-type changes).

0.2.0 (2026)
------------

Structural cleanup, full feature parity with the 2026 MATLAB release, and
many fixes from interactive testing.

Data and layout

- Canonical ``(ry, rx, py, px)`` data layout; fixes transposed pixel grids in
  CoM, DPC, annular integration and virtual apertures.
- Slotted dataclass application state; 0-based UI coordinates.
- Pure ``compute`` sub-package; ``allFunctions.py`` kept only as a deprecated
  alias table.

Import, export and saving

- Offset-based reader with partial, binned and sampled import and lazy
  loading; DM3/DM4 header reader; EMPAD v1/v2 detection.
- Compressed, chunked and fewer-than-4-D HDF5 files read via h5py.
- Byte-order swap and diffraction/real X-Y swap options, also for lazy data.
- Image saving and dataset export (HDF5/raw, partial, binned).

GPU

- Dataset kept resident on the GPU with chunked upload and out-of-memory
  recovery; falls back to the CPU when the dataset does not fit.
- GPUs detected at startup are now usable from the Import window.
- Faster max/std patterns, on the GPU when resident.

Detector modes

- Custom detector mode ported from ``Quant4D.mlapp`` (all mask types, mask
  maths without ``eval``, Color Mix, duplicate and invert masks).
- DPC weighted by segment centroid with the scan direction applied.
- AutoCurl scan-direction estimate (**Auto** button).
- Annular Integration Step (mrad) for ring width.
- iCoM/dCoM Fourier bandpass filter.
- Virtual-aperture position/radius fields, rotation, mirror and reset;
  calculation policy (active/reduced/passive).
- Diffraction Pattern dropdown (sum/mean/max/std/sqrt/ln/log10).
- Double-click a disk to pick the transmitted beam.

Display and interaction

- Wheel/key zoom and drag-to-pan, with one linked view per space.
- Image orientation (reverse X/Y, rotate view, axis and scan-direction
  arrows) and per-space window size from Settings.
- Rotatable rectangle and true ellipse ROIs, editable polygon vertices,
  Shift to keep the aspect ratio while resizing.
- Double-click the histogram to reset its range.
- Settings window reorganised to match MATLAB: new Windows tab (show
  windows, vector field, bandpass filter, window size/orientation), slimmer
  Misc tab, Info tab with **Show all variables** and a Variables tab.
- Window menu shows and hides image windows.

Development

- Integration test suite against a loaded dataset (650 tests).
- pyright (basic) in CI; GPU CI job for the torch tests.

0.1.0 (2026)
------------

Initial Python release.

- Ported all GUI and analysis functions from the original MATLAB Quant4D
  application.
- PyQt5 GUI with matplotlib-embedded image windows.
- Annular integration, CoM/DPC, iCoM, dCoM, and segmented-DPC modes.
- Real-space ROI selection and masking.
- Save images as 32-bit float TIFF or annotated PNG.
- Export datasets as HDF5 (gzip-compressed) or raw binary.
- Optional GPU acceleration via PyTorch.
- pip-installable package (``pip install pyquant4d``).
- GitHub Actions CI for lint and import tests on Linux and Windows.
- ReadTheDocs documentation.
