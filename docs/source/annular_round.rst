.. _annular_round:

Annular / Round Detector
========================

Annular integration produces a real-space image by summing the diffraction
intensity within a ring-shaped (annular) mask at each probe position.
Depending on the inner and outer radii chosen, this produces:

- **BF** (Bright-Field) — inner radius = 0, outer radius inside the direct beam
- **ABF** (Annular Bright-Field) — annulus partially overlapping the direct beam
- **ADF** (Annular Dark-Field) — annulus outside the direct beam
- **HAADF** (High-Angle ADF) — large-radius annulus

Detector setup
--------------

Select **Annular / Round** from the Detector Mode dropdown.  An interactive
annular annotation (two concentric draggable rings) appears on the
diffraction-pattern window.

- Drag the **inner ring** to set the inner radius (*Ri*)
- Drag the **outer ring** to set the outer radius (*Ro*)

The ``Ri`` and ``Ro`` values are synchronised with the spinboxes in the main
window.

Annular integration step
------------------------

The ring images behind the annular detector are pre-computed in steps of the
**Annular Integration Step** (mrad), shown on the Alignment tab in Alignment
mode and on the Annular/CoM/DPC tab otherwise.  It defaults to one pixel, but at
most 250 steps out to the farthest corner of the pattern (finer steps cost
computation time and memory).  Changing it integrates the rings again; the
detector keeps its size, and the radius sliders and spin boxes step one ring.

.. note::
   Full walkthrough with screenshots will be added in a future documentation
   update.
