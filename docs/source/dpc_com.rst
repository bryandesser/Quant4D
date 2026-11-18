.. _dpc_com:

DPC and Centre-of-Mass
======================

Centre-of-Mass (CoM) and Differential Phase Contrast (DPC) modes compute the
intensity-weighted centroid of each diffraction pattern within the annular mask,
yielding direct access to the projected electric field and charge density.

Output images
-------------

CoM mode produces the following real-space images:

- **CoM X** — horizontal component of the centre-of-mass deflection
- **CoM Y** — vertical component of the centre-of-mass deflection
- **CoM Magnitude** — magnitude of the deflection vector
- **CoM Phase** — angle of the deflection vector
- **iCoM** — integrated CoM (Fourier reconstruction), proportional to the
  projected electrostatic potential
- **dCoM** — divergence of CoM, proportional to the projected charge density

iCoM / dCoM bandpass filter
---------------------------

**Settings → Windows → iCoM / dCoM Bandpass Filter** keeps only the spatial
frequencies between the low and high limits (pixels of the scan's Fourier
transform) in the iCoM and dCoM (iDPC/dDPC) images: a lowpass, highpass or
bandpass filter.  It covers every frequency after an import; changing it updates
the two images at once.

Segmented DPC
-------------

Segmented DPC mode emulates a segmented detector on the annulus: it is divided
into *rungs* (concentric rings) and *segments* (angular wedges, the first at the
detector rotation angle).  Each segment's integrated intensity is placed at the
segment's nominal centre of mass, which gives a coarse-grained centre of mass
and the same output images as CoM mode.  The number of segments and rungs and
the rotation are set in the main window; the dividers are drawn on the
diffraction pattern and follow the annulus when its radii change.  Drag the
handle at the end of the thicker divider to rotate the detector.

Scan direction
--------------

The deflection is measured in the detector's frame, while the images are in the
scan's frame: the scan direction (an angle, and whether the scan's Y direction
is flipped) relates the two.

- **Unlock** (the lock button) shows the scan X and Y arrows on the diffraction
  pattern; drag their handles, or use the angle slider and spin box, and the
  Y-flip button.  Lock again when done.
- **Auto** estimates both automatically, as MATLAB Quant4D's AutoCurl does: a
  deflection field is the gradient of a potential, so it has no curl in the
  scan's frame.  Every angle (refined to 0.01°) is tried with and without the Y
  flip, and the one with the least curl is chosen.  The curl cannot tell an angle
  from the same angle plus 180°; of the two, the one nearer the current
  direction is kept.  Auto also locks the scan direction.

.. note::
   Full mathematical background will be added in a future documentation update.
