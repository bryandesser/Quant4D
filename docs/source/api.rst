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

.. automodule:: callbacks.compute
   :no-members:

.. automodule:: callbacks.compute.backend
   :members:

.. automodule:: callbacks.compute.annular
   :members:

.. automodule:: callbacks.compute.com
   :members:

.. automodule:: callbacks.compute.dpc
   :members:

.. automodule:: callbacks.compute.masks
   :members:

.. automodule:: callbacks.compute.roi
   :members:

.. automodule:: callbacks.compute.custom
   :members:

.. automodule:: callbacks.compute.mask_math
   :members:

Reading files
-------------

.. automodule:: callbacks.io.raw
   :members:

.. automodule:: callbacks.io.dm_header
   :members:

.. automodule:: callbacks.io.empad
   :members:

.. automodule:: callbacks.io.hdf5
   :members:

Saving and exporting
--------------------

.. automodule:: callbacks.io.export
   :members:

.. automodule:: callbacks.io.emd
   :members:

.. automodule:: callbacks.save_export
   :members:

Array layout and coordinates
----------------------------

.. automodule:: callbacks.layout
   :members:

Signal blocking
---------------

.. automodule:: callbacks.signals
   :members:

callbacks.appClass
------------------

.. automodule:: callbacks.appClass
   :members:
   :undoc-members:
   :show-inheritance:

callbacks.guiClass
------------------

.. automodule:: callbacks.guiClass
   :members:
   :undoc-members:
   :show-inheritance:

callbacks.allFunctions
----------------------

.. warning::
   **Deprecated.** ``callbacks.allFunctions`` only re-exports names that now live in other
   modules (each access warns and names the new module).  Import from those
   modules instead; this module will be removed in pyQuant4D 2.0.

.. automodule:: callbacks.allFunctions
   :no-members:
   :no-undoc-members:
   :no-special-members:

.. autodata:: callbacks.allFunctions.MOVED
   :no-value:

callbacks.annularDetectorCallbacks
-----------------------------------

.. automodule:: callbacks.annularDetectorCallbacks
   :members:
   :undoc-members:
   :show-inheritance:

callbacks.axis_direction
------------------------

.. automodule:: callbacks.axis_direction
   :members:

callbacks.view_zoom
-------------------

.. automodule:: callbacks.view_zoom
   :members:

callbacks.variables
-------------------

.. automodule:: callbacks.variables
   :members:

callbacks.menus
---------------

.. automodule:: callbacks.menus
   :members:

callbacks.customDetectorCallbacks
---------------------------------

.. automodule:: callbacks.customDetectorCallbacks
   :members:
   :show-inheritance:

callbacks.displayCallbacks
--------------------------

.. automodule:: callbacks.displayCallbacks
   :members:
   :undoc-members:
   :show-inheritance:

callbacks.importCallbacks
--------------------------

.. automodule:: callbacks.importCallbacks
   :members:
   :undoc-members:
   :show-inheritance:

callbacks.realSpaceROICallbacks
--------------------------------

.. automodule:: callbacks.realSpaceROICallbacks
   :members:
   :undoc-members:
   :show-inheritance:

annotationsClasses
------------------

.. automodule:: annotationsClasses.interactiveAnnulus
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: annotationsClasses.interactiveCircle
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: annotationsClasses.interactiveEllipse
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: annotationsClasses.interactiveRectangle
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: annotationsClasses.interactivePolygon
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: annotationsClasses.interactivePoint
   :members:
   :undoc-members:
   :show-inheritance:
