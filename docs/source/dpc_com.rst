.. _dpc_com:

DPC/CoM
-------
Quant4D can generate Differential Phase Contrast (DPC) and Center of Mass (CoM)
images from the 4D-STEM dataset. In CoM mode, the center of mass is calculated 
from within the circular or round mask on the diffraction pattern. In DPC mode,
the circular/annular mask is subdivided into a user-defined number of sectors
both radially and azimuthally (default = 4 quadrants).

Scan rotation estimation
************************
It is critical to estimate the rotation angle between the scan direction in
real space and the diffraction pattern on the detector. The user can explicitly
set this angle in the main UI window, or it can be estimated automatically by
minimizing the curl as a function of the rotation angle. When the user first
enters either DPC or CoM mode, the **Scanning Direction** panel on the main UI
window will be highlighted in orange, indicating that the angle has not yet
been set. The user can enter or estimate the angle by first clicking the |lock|
icon to enable the inputs. If the user clicks the **Auto** button, the curl
minimization routine will run, using the estimated rotation angle and
automatically locking the **Scanning Direction** panel to avoid accidental
changes.

.. |lock| image:: ../../src/icons/lock.png
    :height: 2ex

Images
******


iDPC/iCoM
*********

dDPC/dCoM
*********