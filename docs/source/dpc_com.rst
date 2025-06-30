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
changes. In addition to the rotation angle, the handedness of the scan
direction can be swapped by enabling or disabling the |swap_y| icon, which
inverts the y-axis scan direction.

.. |lock| image:: ../../src/icons/lock.png
    :height: 2ex

.. |swap_y| image:: ../../src/icons/axis-y.png
    :height: 2ex

Images
******
Many images are calculated in DPC/CoM modes; however, most are not immediately
made visible to the user to avoid opening too many windows at once. The user
can show any/all of the following images by clicking the corresponding icon in
the **Show Image Windows** panel of  **Windows** tab in the **Settings** UI.
When the user is enters DPC or CoM mode, this tab is automatically activated.
The name of the images will automatically update to reflect the current mode
(i.e. CoMx or DPCx, etc.).

.. |diffraction| image:: ../_static/diffraction.png
    :height: 2ex
.. |diffraction_mask| image:: ../_static/diffraction_mask.png
    :height: 2ex
.. |bfdf| image:: ../_static/bfdf.png
    :height: 2ex
.. |bfdf_mask| image:: ../_static/bfdf_mask.png
    :height: 2ex
.. |CoMX| image:: ../_static/CoMX.png
    :height: 2ex
.. |CoMY| image:: ../_static/CoMY.png
    :height: 2ex
.. |CoM_magnitude| image:: ../_static/CoM_magnitude.png
    :height: 2ex
.. |CoM_phase| image:: ../_static/CoM_phase.png
    :height: 2ex
.. |colorwheel| image:: ../_static/colorwheel.png
    :height: 2ex
.. |CoM_phase_mag| image:: ../_static/CoM_phase_mag.png
    :height: 2ex
.. |dCoM| image:: ../_static/dCoM.png
    :height: 2ex
.. |iCoM| image:: ../_static/iCoM.png
    :height: 2ex

* |diffraction| - Main diffraction space image.
* |diffraction_mask| - Diffraction space mask used to generate images.
* |bfdf| - Main real space image.
* |bfdf_mask| - Real space mask (i.e. if an ROI is used)
* |CoMX| - CoM/DPC image in the x-direction.
* |CoMY| - CoM/DPC image in the y-direction.
* |CoM_magnitude| - CoM/DPC magnitude image.
* |CoM_phase| - CoM/DPC phase image.
* |colorwheel| - Color wheel legend for phase images.
* |CoM_phase_mag| - CoM/DPC phase image with opacity based on the magnitude image
* |dCoM| - Differential CoM/DPC image.
* |iCoM| - Integrated CoM/DPC image. 

Vector overlays
***************
.. |colorpicker| image:: ../../src/icons/colorPicker.png
    :height: 2ex

DPC and CoM imaging generates a vector field, which can be selectively overlaid
on any/all real space images. The user should first select the desired image by
either clicking the relevant button above, clicking within the image window
(i.e. *not* the title bar), or selecting the image from the **Image** dropdown
on the Display tab in the **Settings** UI. After the desired image is selected,
the user can click the **Vector Sampling** dropdown in the **Windows** tab of
the **Settings** UI. Vectors can be displayed at each pixel (1:1), or
subsampled by a factor of 2, 4, 8, or 16. This is especially helpful when the
vector field is highly oversampled compared to its rate of change.
Additionally, the user can change the color of the vector overlay independently
on each image using the |colorpicker| icon next to the vector sampling dropdown.

iDPC/iCoM
*********
Integrated DPC/CoM images are generated automatically using the detector chosen
by the user. Integration of the DPC/CoM signal retrieves the phase of the
specimen transmission function. The maths are thoroughly described by `Lazić *et
al.*`_.

dDPC/dCoM
*********
Differentiated DPC/CoM images are generated automatically using the detector
chose by the user. Differentiation of the DPC/CoM signal retrieves the charge
density distribution of the specimen transmission. `Lazić *et al.*`_

Filtering
*********
Because the integration step can amplify noise at low spatial frequencies,
while differentiation can suffer from noise at high spatial frequencies, a
bandpass filter is made available to the user in the **Windows** tab of the
**Settings** UI. The user can independently change the low and high frequency
cutoff values (in pixels) to apply a bandpass, lowpass, or highpass filter. The
filter is only applied to the iCoM/iDPC and dCoM/dDPC images.


.. _Lazić *et al.*: Ivan Lazić, Eric G. T. Bosch, and Sorin Lazar. "Phase contrast STEM for
  thin samples: Integrated differential phase contrast." Ultramicroscopy 160
  (2016): 265-280. https://doi.org/10.1016/j.ultramic.2015.10.011