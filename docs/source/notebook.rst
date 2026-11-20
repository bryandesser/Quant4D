.. _notebook:

From Python and notebooks (py4DSTEM)
====================================

pyQuant4D can sit in the middle of a py4DSTEM notebook: process in py4DSTEM,
open the data in pyQuant4D to align the beam and try detectors interactively,
then carry the results back into the notebook and continue there.

Requirements
------------

``pip install pyquant4d[py4dstem]`` (py4DSTEM 0.14 or later), and Jupyter
running on the same computer (pyQuant4D opens desktop windows).

The round trip
--------------

.. code-block:: python

    %gui qt                                   # once, before pyquant4d.show
    import py4DSTEM, pyquant4d

    dc = py4DSTEM.read("scan.h5")
    # ... py4DSTEM processing ...

    win = pyquant4d.show(dc)                  # returns at once; the windows stay open

Now work in pyQuant4D: align the transmitted beam, set the scan step, try
annular, CoM/DPC or custom detectors.  The notebook stays usable meanwhile.
When you are done, back in the notebook:

.. code-block:: python

    cal = win.apply_calibration(dc)           # beam centre, detector scale, semi-angle, scan step
    adf = win.image("Real")                   # the real-space image, (Rx, Ry)
    detector = win.mask()                     # the detector that made it, (Qx, Qy)
    icom = win.image("iCoM")                  # any image computed so far: win.images()

    # continue in py4DSTEM with the calibrated DataCube
    py4DSTEM.show(adf)

You can call these at any time while pyQuant4D is open (they read its current
state), and as often as you like.  Closing pyQuant4D closes its windows only;
the notebook session carries on, but read the results before closing.

What comes back
---------------

``win.calibration()``
    A dictionary in py4DSTEM's names: ``qx0_mean``, ``qy0_mean`` (the beam
    centre in detector pixels), ``probe_semiangle`` (the transmitted disk's
    radius in pixels, as py4DSTEM's ``get_probe_size`` stores it),
    ``convergence_semiangle_mrad``, ``Q_pixel_size`` and ``Q_pixel_units``
    (mrad per detector pixel), ``R_pixel_size`` and ``R_pixel_units`` (the
    scan step; 1 pixel if not set), ``accelerating_voltage_kV``, ``aligned``
    (False until the beam has been set) and ``shape``.

``win.apply_calibration(dc, scan_step=True)``
    Writes that calibration into ``dc.calibration`` and returns it.  Origin
    maps the DataCube already has (for example a fitted descan) keep their
    shape and are shifted so that their mean is the new centre; without maps,
    constant ones are written.  The DataCube must have the shape of the data
    in pyQuant4D.  Warns if the beam has not been aligned yet.

``win.image(id)``, ``win.images()``
    A copy of an image as computed (before display brightness, contrast and
    gamma), by id (``"Real"``, ``"Dfrn"``, ``"iCoM"``, ``"dCoM"``,
    ``"CoMX"``, ...) or window name.  ``images()`` lists those computed so far.

``win.mask(id=None)``
    A copy of the current mode's detector (as on the diffraction-mask window),
    ``"roi"`` for the real-space ROI, or a custom detector's ID (``"A"``).

Orientation
-----------

No transposes are needed: pyQuant4D's real-space images are indexed (ry, rx)
and its patterns (py, px), which are py4DSTEM's (Rx, Ry) and (Qx, Qy).  Where
coordinates appear as numbers they are swapped: py4DSTEM's ``qx0`` (a row) is
pyQuant4D's beam **y**, shown in the main window as TBY.

Memory: copy or share
---------------------

By default ``show`` gives pyQuant4D its own copy of the data, so nothing it
does can change ``dc``.  For a dataset too large to hold twice, pass
``copy=False``: pyQuant4D then works on the DataCube's own array.  The two
dataset options that change data in place, **Set NaNs to 0** and **Swap Byte
Order**, make a copy first even then, so ``dc`` is never changed.

Without a notebook
------------------

In a plain script ``pyquant4d.show(dc)`` runs until pyQuant4D is closed (pass
``block=False`` to get the window back at once and run the Qt event loop
yourself).  The results are also available through a file: export
"py4DSTEM EMD (\*.h5)" from the Save window and ``py4DSTEM.read`` it (see
:ref:`export`).

API
---

.. automodule:: callbacks.results
   :members:
