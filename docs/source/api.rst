API Reference
=============

.. note::
   pyQuant4D is a GUI application.  The modules listed here are not intended
   as a public library API — they may change between releases.  This page is
   provided for developers who want to understand the internal structure.

Computation
-----------

Pure functions that take and return NumPy arrays and never touch the GUI.
All detector images are computed here.

.. automodule:: pyquant4d.callbacks.compute
   :no-members:

.. automodule:: pyquant4d.callbacks.compute.backend
   :members:

.. automodule:: pyquant4d.callbacks.compute.annular
   :members:

.. automodule:: pyquant4d.callbacks.compute.com
   :members:

.. automodule:: pyquant4d.callbacks.compute.dpc
   :members:

.. automodule:: pyquant4d.callbacks.compute.masks
   :members:

.. automodule:: pyquant4d.callbacks.compute.roi
   :members:

.. automodule:: pyquant4d.callbacks.compute.custom
   :members:

.. automodule:: pyquant4d.callbacks.compute.mask_math
   :members:

Reading files
-------------

.. automodule:: pyquant4d.callbacks.io.raw
   :members:

.. automodule:: pyquant4d.callbacks.io.dm_header
   :members:

.. automodule:: pyquant4d.callbacks.io.empad
   :members:

.. automodule:: pyquant4d.callbacks.io.hdf5
   :members:

Saving and exporting
--------------------

.. automodule:: pyquant4d.callbacks.io.export
   :members:

.. automodule:: pyquant4d.callbacks.io.emd
   :members:

.. automodule:: pyquant4d.callbacks.save_export
   :members:

Array layout and coordinates
----------------------------

.. automodule:: pyquant4d.callbacks.layout
   :members:

Signal blocking
---------------

.. automodule:: pyquant4d.callbacks.signals
   :members:

pyquant4d.callbacks.appClass
----------------------------

.. automodule:: pyquant4d.callbacks.appClass
   :members:
   :undoc-members:
   :show-inheritance:

pyquant4d.callbacks.guiClass
----------------------------

.. automodule:: pyquant4d.callbacks.guiClass
   :members:
   :undoc-members:
   :show-inheritance:

pyquant4d.callbacks.allFunctions
--------------------------------

.. warning::
   **Deprecated.** ``pyquant4d.callbacks.allFunctions`` only re-exports names that now live in other
   modules (each access warns and names the new module).  Import from those
   modules instead; this module will be removed in pyQuant4D 2.0.

.. automodule:: pyquant4d.callbacks.allFunctions
   :no-members:
   :no-undoc-members:
   :no-special-members:

.. autodata:: pyquant4d.callbacks.allFunctions.MOVED
   :no-value:

pyquant4d.callbacks.annularDetectorCallbacks
--------------------------------------------

.. automodule:: pyquant4d.callbacks.annularDetectorCallbacks
   :members:
   :undoc-members:
   :show-inheritance:

pyquant4d.callbacks.axis_direction
----------------------------------

.. automodule:: pyquant4d.callbacks.axis_direction
   :members:

pyquant4d.callbacks.view_zoom
-----------------------------

.. automodule:: pyquant4d.callbacks.view_zoom
   :members:

pyquant4d.callbacks.variables
-----------------------------

.. automodule:: pyquant4d.callbacks.variables
   :members:

pyquant4d.callbacks.menus
-------------------------

.. automodule:: pyquant4d.callbacks.menus
   :members:

pyquant4d.callbacks.customDetectorCallbacks
-------------------------------------------

.. automodule:: pyquant4d.callbacks.customDetectorCallbacks
   :members:
   :show-inheritance:

pyquant4d.callbacks.displayCallbacks
------------------------------------

.. automodule:: pyquant4d.callbacks.displayCallbacks
   :members:
   :undoc-members:
   :show-inheritance:

pyquant4d.callbacks.importCallbacks
-----------------------------------

.. automodule:: pyquant4d.callbacks.importCallbacks
   :members:
   :undoc-members:
   :show-inheritance:

pyquant4d.callbacks.file_drop
-----------------------------

.. automodule:: pyquant4d.callbacks.file_drop
   :members:

pyquant4d.callbacks.scan_step
-----------------------------

.. automodule:: pyquant4d.callbacks.scan_step
   :members:

pyquant4d.callbacks.scale_bar
-----------------------------

.. automodule:: pyquant4d.callbacks.scale_bar
   :members:

pyquant4d.callbacks.py4dstem_bridge
-----------------------------------

.. automodule:: pyquant4d.callbacks.py4dstem_bridge
   :members:

pyquant4d
---------

.. automodule:: pyquant4d
   :members: show

pyquant4d.callbacks.realSpaceROICallbacks
-----------------------------------------

.. automodule:: pyquant4d.callbacks.realSpaceROICallbacks
   :members:
   :undoc-members:
   :show-inheritance:

annotationsClasses
------------------

.. automodule:: pyquant4d.annotationsClasses.interactiveAnnulus
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: pyquant4d.annotationsClasses.interactiveCircle
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: pyquant4d.annotationsClasses.interactiveEllipse
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: pyquant4d.annotationsClasses.interactiveRectangle
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: pyquant4d.annotationsClasses.interactivePolygon
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: pyquant4d.annotationsClasses.interactivePoint
   :members:
   :undoc-members:
   :show-inheritance:
