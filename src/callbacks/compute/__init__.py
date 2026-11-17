"""Pure computation for pyQuant4D.

Nothing in this package touches Qt, matplotlib or the application object:
every function takes NumPy arrays (and plain numbers) and returns NumPy
arrays, so each can be tested without constructing the GUI.

Conventions (see :mod:`callbacks.layout`)
-----------------------------------------
* ``data`` is the flat ``(frame, pixel)`` dataset, ``frame = ry*NFrX + rx`` and
  ``pixel = py*NPxX + px``.
* Diffraction-space images and masks are ``(NPxY, NPxX)``; their ``ravel()``
  lines up with the pixel axis of ``data``.
* Points such as the beam centre are ``(x, y)`` in 0-based pixel coordinates.
* ``device`` is a CUDA device (``"cuda:0"``, an index, or ``None`` for CPU).
  Results always come back as NumPy arrays.
"""
from callbacks.compute.backend import project, resolve_device
from callbacks.compute.annular import (
    annular_mask, masked_sum, radial_index, ring_integrals, ring_matrix,
)
from callbacks.compute.com import (
    center_of_mass, divergence, integrate_field, magnitude_phase, rotate_field,
    weighted_mean_position,
)
from callbacks.compute.dpc import sector_centroid_radius, segment_weights, segmented_dpc
from callbacks.compute.masks import (
    circle_mask, circles_mask, ellipse_mask, polygon_mask, rectangle_mask,
)
from callbacks.compute.roi import roi_pattern

__all__ = [
    "project", "resolve_device",
    "annular_mask", "masked_sum", "radial_index", "ring_integrals", "ring_matrix",
    "center_of_mass", "divergence", "integrate_field", "magnitude_phase", "rotate_field",
    "weighted_mean_position",
    "sector_centroid_radius", "segment_weights", "segmented_dpc",
    "circle_mask", "circles_mask", "ellipse_mask", "polygon_mask", "rectangle_mask",
    "roi_pattern",
]
