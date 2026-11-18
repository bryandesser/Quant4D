.. _alignment:

Beam Alignment
==============

Before running any quantitative analysis, the direct beam centre should be
aligned to the centre of the diffraction pattern.

Alignment mode
--------------

Select **Alignment** from the Detector Mode dropdown.  pyQuant4D displays the
probe-averaged convergent-beam electron diffraction (PACBED) pattern — the
incoherent sum of all diffraction frames.

An interactive circle annotation appears on the diffraction-pattern window.
Drag the circle to position it over the direct beam, and use the radius handle
to match the bright-field disc.

The beam-centre coordinates (TBX, TBY) and beam radius (TBR) are synchronised
with the spinboxes in the main window and can also be entered manually.

**Auto** finds the transmitted beam with a circular Hough transform.  If it
chooses the wrong disk, **double-click the right disk** on the diffraction
pattern: the beam is refitted to the detected circle nearest the click (or, if
no circle is detected there, centred on the click with the current radius).

.. note::
   Full alignment walkthrough with screenshots will be added in a future
   documentation update.
