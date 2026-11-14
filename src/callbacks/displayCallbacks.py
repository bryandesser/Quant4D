"""
displayCallbacks — backward-compatibility re-export shim.

All implementations have moved to their canonical modules:
  - displayCallbacks, plotImage, updateDispImgStats,
    plotVectorField, plotAllPatterns, plotColorWheel,
    toUpdateImage, updateImagesCallbacks  →  callbacks.plotting
  - isDiffToPrev                          →  callbacks.utils
"""
from callbacks.plotting import (  # noqa: F401
    displayCallbacks,
    plotImage,
    updateDispImgStats,
    plotVectorField,
    plotAllPatterns,
    plotColorWheel,
    toUpdateImage,
    updateImagesCallbacks,
)
from callbacks.utils import isDiffToPrev  # noqa: F401
