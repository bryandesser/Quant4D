API Reference
=============

.. note::
   Quant4D is a GUI application.  The modules listed here are not intended
   as a public library API — they may change between releases.  This page is
   provided for developers who want to understand the internal structure.

Computation
-----------

Pure functions that take and return NumPy arrays and never touch the GUI.
All detector images are computed here.

.. automodule:: quant4d.callbacks.compute
   :no-members:

.. automodule:: quant4d.callbacks.compute.backend
   :members:

.. automodule:: quant4d.callbacks.compute.annular
   :members:

.. automodule:: quant4d.callbacks.compute.com
   :members:

.. automodule:: quant4d.callbacks.compute.dpc
   :members:

.. automodule:: quant4d.callbacks.compute.masks
   :members:

.. automodule:: quant4d.callbacks.compute.roi
   :members:

.. automodule:: quant4d.callbacks.compute.custom
   :members:

.. automodule:: quant4d.callbacks.compute.mask_math
   :members:

Reading files
-------------

.. automodule:: quant4d.callbacks.io.raw
   :members:

.. automodule:: quant4d.callbacks.io.dm_header
   :members:

.. automodule:: quant4d.callbacks.io.empad
   :members:

.. automodule:: quant4d.callbacks.io.hdf5
   :members:

Saving and exporting
--------------------

.. automodule:: quant4d.callbacks.io.export
   :members:

.. automodule:: quant4d.callbacks.io.emd
   :members:

.. automodule:: quant4d.callbacks.save_export
   :members:

Array layout and coordinates
----------------------------

.. automodule:: quant4d.callbacks.layout
   :members:

Signal blocking
---------------

.. automodule:: quant4d.callbacks.signals
   :members:

quant4d.callbacks.appClass
----------------------------

.. automodule:: quant4d.callbacks.appClass
   :members:
   :undoc-members:
   :show-inheritance:

quant4d.callbacks.guiClass
----------------------------

.. automodule:: quant4d.callbacks.guiClass
   :members:
   :undoc-members:
   :show-inheritance:

quant4d.callbacks.allFunctions
--------------------------------

.. warning::
   **Deprecated.** ``quant4d.callbacks.allFunctions`` only re-exports names that now live in other
   modules (each access warns and names the new module).  Import from those
   modules instead; this module will be removed in Quant4D 2.0.

.. automodule:: quant4d.callbacks.allFunctions
   :no-members:
   :no-undoc-members:
   :no-special-members:

.. autodata:: quant4d.callbacks.allFunctions.MOVED
   :no-value:

quant4d.callbacks.annularDetectorCallbacks
--------------------------------------------

.. automodule:: quant4d.callbacks.annularDetectorCallbacks
   :members:
   :undoc-members:
   :show-inheritance:

quant4d.callbacks.axis_direction
----------------------------------

.. automodule:: quant4d.callbacks.axis_direction
   :members:

quant4d.callbacks.view_zoom
-----------------------------

.. automodule:: quant4d.callbacks.view_zoom
   :members:

quant4d.callbacks.variables
-----------------------------

.. automodule:: quant4d.callbacks.variables
   :members:

quant4d.callbacks.menus
-------------------------

.. automodule:: quant4d.callbacks.menus
   :members:

quant4d.callbacks.customDetectorCallbacks
-------------------------------------------

.. automodule:: quant4d.callbacks.customDetectorCallbacks
   :members:
   :show-inheritance:

quant4d.callbacks.displayCallbacks
------------------------------------

.. automodule:: quant4d.callbacks.displayCallbacks
   :members:
   :undoc-members:
   :show-inheritance:

quant4d.callbacks.importCallbacks
-----------------------------------

.. automodule:: quant4d.callbacks.importCallbacks
   :members:
   :undoc-members:
   :show-inheritance:

quant4d.callbacks.file_drop
-----------------------------

.. automodule:: quant4d.callbacks.file_drop
   :members:

quant4d.callbacks.scan_step
-----------------------------

.. automodule:: quant4d.callbacks.scan_step
   :members:

quant4d.callbacks.scale_bar
-----------------------------

.. automodule:: quant4d.callbacks.scale_bar
   :members:

quant4d.callbacks.py4dstem_bridge
-----------------------------------

.. automodule:: quant4d.callbacks.py4dstem_bridge
   :members:

quant4d
---------

.. automodule:: quant4d
   :members: show

quant4d.callbacks.realSpaceROICallbacks
-----------------------------------------

.. automodule:: quant4d.callbacks.realSpaceROICallbacks
   :members:
   :undoc-members:
   :show-inheritance:

annotationsClasses
------------------

.. automodule:: quant4d.annotationsClasses.interactiveAnnulus
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: quant4d.annotationsClasses.interactiveCircle
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: quant4d.annotationsClasses.interactiveEllipse
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: quant4d.annotationsClasses.interactiveRectangle
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: quant4d.annotationsClasses.interactivePolygon
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: quant4d.annotationsClasses.interactivePoint
   :members:
   :undoc-members:
   :show-inheritance:
