.. _custom_apertures:

Custom Detectors
================

Custom detector mode builds a detector from any number of masks drawn on the
diffraction pattern.  The masks are combined into one detector, which is shown
in the *Diffraction Mask* window; the real-space image is that detector applied
to the diffraction pattern at every probe position.

Select **Custom Detectors** in the detector mode dropdown of the main window.
The masks are made, listed and edited on the *Custom Detectors* tab.

Mask types
----------

Each button on the tab adds a new mask.  Masks are named ``A``, ``B``, … ``Z``,
``AA``, … up to ``ZZ``, and each gets a random colour.

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Type
     - Description
   * - **Circle**
     - A circular aperture, created on top of the transmitted beam.  Drag inside
       it to move it and drag its handle to change the radius.  **Mirror** adds
       a copy reflected through the beam centre (shown dashed).
   * - **Grid**
     - A lattice of equal apertures.  Two draggable basis apertures set the
       lattice vectors from the beam centre; apertures are placed at every
       lattice site over the pattern.  Dragging a basis aperture's handle sets
       the radius of all of them.
   * - **Grid (×)**
     - The same lattice without the transmitted beam and without every second
       site (only sites where exactly one lattice index is odd), e.g. for
       superlattice reflections.
   * - **Bandpass**
     - A ring between two radii about a centre.  Drag the two handles to set
       the inner and outer radius, or drag inside to move it.
   * - **Wedge**
     - A sector from the beam centre to the edges of the pattern, between the
       directions of two draggable handles (the opening is always below 180°).
       Mirrored by default, which adds the opposite sector.
   * - **Polygon**
     - Click the vertices on the diffraction pattern and click the first vertex
       again to close the polygon (``Esc`` cancels).  Afterwards drag a vertex
       to move it, drag inside to move the polygon, or drag just outside a
       vertex (the cursor becomes a curved double arrow) to rotate it about
       its centre.
   * - **File**
     - A mask image loaded from disk (``.tif``, ``.png``, ``.jpg``, ``.bmp``,
       ``.gif`` or ``.npy``) of the diffraction pattern's size.  Colour images
       are converted to greyscale, grey levels are kept as weights (the maximum
       is scaled to 1), and an image of transposed size is transposed to fit.
   * - **Math**
     - A formula over the other masks, written on the *Math* tab of the
       Settings window (see :ref:`custom_math`).

The mask table
--------------

Every mask has a row in the table, with these columns:

- **ID** — the mask's name, used in formulas.
- **Type** — the mask type.
- **Label** — a free-text label; edit it in place.
- **✓** — include the mask in the detector.
- **👁** — show the mask's outline on the diffraction pattern.
- **μ** — the mask's weight in the detector (``0`` leaves it out).

Selecting a row selects that mask for the controls below the table.

Editing the selected mask
-------------------------

- **Details table** — the mask's points (centres, handles or vertices) and
  radii, editable as numbers.  Coordinates follow the settings on the *Misc*
  tab of the Settings window: polar or Cartesian, relative to the beam centre
  or absolute, in mrad or pixels.
- **Rotate** clockwise or anticlockwise by the chosen step (180° down to
  0.25°) about the beam centre, as displayed.  File masks rotate in steps of
  90° (180° unless the pattern is square) and can only be transposed when the
  pattern is square.
- **Flip** across the horizontal or vertical axis through the beam centre, or
  **transpose** (swap x and y).
- **Mirror** (Circle and Wedge) through the beam centre.
- **Invert** the mask (``max − mask``: swaps inside and outside of a binary
  mask, reverses grey levels).
- **Intra-mask mode** — how the parts of one mask combine (Grid, and a
  mirrored Circle): *Union*, *Intersection* (only where parts overlap) or
  *Additive* (overlaps count more than once).
- **Colour** — change the mask's colour.
- **Delete** the mask.

Rotation, flips and transposes are not available for Math masks; change their
formula instead.

Combining masks
---------------

The **inter-mask mode** sets how the enabled masks form the detector.  Each
mask is first multiplied by its weight μ.

- **Color Mix** (default) — the detector is the union of the masks, and both
  the Diffraction Mask and the real-space image are shown in colour: each
  mask's contribution is drawn in that mask's colour.
- **Union** — pixels in any mask.
- **Intersection** — pixels in every mask.
- **Additive** — the weighted sum of the masks, so overlaps and weights add up
  (e.g. ``A`` with μ = 1 and ``B`` with μ = −1 gives ``A − B``).
- **Current-only** — only the selected mask.

.. _custom_math:

Mask maths
----------

A **Math** mask opens the *Math* tab of the Settings window.  Write a formula
over the other masks' IDs and press **Evaluate**.  The language is the MATLAB
syntax of the original Quant4D, so formulas written for the MATLAB app give
the same mask:

- numbers, ``pi``, ``eps``, ``Inf``, ``NaN``, ``true``, ``false``
- element-wise ``+ - .* ./ .^``, comparisons ``== ~= < <= > >=``, logic
  ``& | ~``
- transpose ``'``, indexing with 1-based ranges and ``end``
  (``A(1:3, :)``), concatenation ``[A(1:3, :); B(4:end, :)]``
- functions such as ``abs``, ``sqrt``, ``exp``, ``log``, ``round``,
  ``max``, ``min``, ``rot90``, ``fliplr``, ``flipud``, ``circshift``,
  ``zeros``, ``ones``

As in MATLAB, the first index runs along x and the second along y.  Examples:

- ``A & (B | C)`` — the union of B and C, intersected with A
- ``(A.^2 + B .* C)'`` — element-wise maths, then transposed
- ``A & ~B`` — A without B

A formula may not refer to its own mask.  If it can't be evaluated, the error
says why and the mask is left unchanged.

GPU
---

With GPU acceleration enabled at import, the real-space images (including the
Color Mix channels) are computed on the GPU.
