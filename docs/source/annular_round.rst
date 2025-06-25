.. _annular_round:

.. |radius_link| image:: ../../src/icons/link.png
    :height: 2ex

Annular/Round detectors
-----------------------
The most basic and intuitive detector format, this mode provides the user with a
pair of circular annotations on the diffraction pattern, which are linked to
slider bars and numerical inputs in the main UI. These can be used to form
circular or annular detectors centered on the transmitted beam. The width of the
detector can be fixed by enabling the |radius_link| icon between the two slider
bars. This allows the user to change the inner and outer angles simultaneously.

When the user first switches to this mode from the **Alignment** mode, a
pre-calculation step is performed to improve display speeds upon interaction.
Here we calculate a range of images with a given annular step size, defined by
the **Annular Integration Step** field at the bottom of the panel in the main UI. 
This way, when the user changes the detector range, the images can be directly 
plotted, rather than calculated from the entire dataset. The initial value for 
**Annular Integration Step** is set to one pixel step in diffraction space, or a
maximum of 250 steps. This balances reasonably fine control of detector geometry
and computational efficiency; however, the user can directly change this step
size for finer/coarser control, at which point the pre-calculation is repeated
with the new step size. 

.. image:: ../_static/annular_round.gif
    :scale: 100%
    :align: centered