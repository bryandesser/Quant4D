"""Results of a pyQuant4D session, for Python and notebooks (py4DSTEM conventions).

``pyquant4d.show(datacube)`` returns the main window; these functions are its
methods ``calibration``, ``apply_calibration``, ``image``, ``images`` and ``mask``:

>>> win = pyquant4d.show(dc)            # align, choose detectors... in the UI
>>> win.apply_calibration(dc)           # beam centre, detector scale, semi-angle, scan step
>>> adf = win.image("Real")             # the real-space image as shown, (Rx, Ry)
>>> det = win.mask()                    # the current detector, (Qx, Qy)

Arrays come back in py4DSTEM's index order: pyQuant4D's real-space images are
(ry, rx) = py4DSTEM's (Rx, Ry), its patterns (py, px) = (Qx, Qy), so no
transposes are needed.  Coordinates are swapped where they appear: py4DSTEM's
``qx0`` is pyQuant4D's beam **y**.
"""
from __future__ import annotations

from typing import Optional

import numpy as np

__all__ = ["calibration", "apply_calibration", "image", "images", "mask"]

_R_UNITS = {"A": "A", "nm": "nm", "pm": "pm", "um": "um", "mm": "mm", "pixels": "pixels"}


def _need_data(self) -> None:
    if getattr(self, "Data", None) is None or getattr(self, "D", None) is None:
        raise RuntimeError("no dataset is loaded in pyQuant4D")


def calibration(self) -> dict:
    """The calibration of the loaded dataset, in py4DSTEM's names and (row, column) order.

    Keys: ``qx0_mean``, ``qy0_mean`` (beam centre, detector pixels),
    ``probe_semiangle`` (transmitted disk radius, pixels, as py4DSTEM's
    ``get_probe_size`` stores it), ``convergence_semiangle_mrad``,
    ``Q_pixel_size`` / ``Q_pixel_units`` (mrad per detector pixel),
    ``R_pixel_size`` / ``R_pixel_units`` (scan step; 1 pixel if not set),
    ``accelerating_voltage_kV``, ``aligned`` (False until the beam has been set
    in Alignment mode or by the file), and ``shape`` (the dataset's
    (Rx, Ry, Qx, Qy), which pixel coordinates refer to).
    """
    _need_data(self)
    d = self.D
    bx, by = (float(v) for v in np.asarray(self.B0, float))
    units = str(d.ScanUnits or "pixels")
    calibrated_r = units != "pixels"
    return {
        "qx0_mean": by,                                   # py4DSTEM Qx = rows = pyQuant4D y
        "qy0_mean": bx,
        "probe_semiangle": float(self.TBR.value()),
        "convergence_semiangle_mrad": float(self.Alpha.value()),
        "Q_pixel_size": float(self.mradPx.value()),
        "Q_pixel_units": "mrad",
        "R_pixel_size": float(d.ScanStep) if calibrated_r else 1.0,
        "R_pixel_units": _R_UNITS.get(units, units) if calibrated_r else "pixels",
        "accelerating_voltage_kV": float(d.kV) if d.kV else None,
        "aligned": bool(self.P.TransBeamInit),
        "shape": (int(d.NFrY), int(d.NFrX), int(d.NPxY), int(d.NPxX)),
    }


def apply_calibration(self, datacube, *, scan_step: bool = True) -> dict:
    """Write :func:`calibration` into ``datacube.calibration`` (a py4DSTEM DataCube) and return it.

    Sets the detector scale (mrad), the convergence semi-angle, the disk radius
    (``probe_semiangle``, pixels) and the origin.  Origin maps the DataCube
    already has (e.g. a fitted descan) keep their shape and are shifted so
    their mean is the new centre; without maps, constant ones are written.
    The scan step is written too if it is set in pyQuant4D (``scan_step=False``
    leaves the DataCube's).  The DataCube must have the loaded dataset's shape
    (pixel coordinates refer to it).
    """
    cal = calibration(self)
    shape = tuple(np.shape(getattr(datacube, "data", datacube)))
    if shape != cal["shape"]:
        raise ValueError(f"the DataCube's shape {shape} is not the dataset's in pyQuant4D {cal['shape']} "
                         "(cropped or binned on import?): its pixel coordinates would not match")
    if not cal["aligned"]:
        import warnings
        warnings.warn("the transmitted beam has not been aligned in pyQuant4D yet", stacklevel=2)
    c = datacube.calibration
    c.set_Q_pixel_size(cal["Q_pixel_size"])
    c.set_Q_pixel_units("mrad")
    c.set_probe_semiangle(cal["probe_semiangle"])
    c.set_convergence_semiangle_mrad(cal["convergence_semiangle_mrad"])
    rshape = shape[:2]
    for key, centre in (("qx0", cal["qx0_mean"]), ("qy0", cal["qy0_mean"])):
        try:
            old = getattr(c, f"get_{key}")()
        except Exception:                   # py4DSTEM raises for parameters never set
            old = None
        old = None if old is None else np.asarray(old, float)
        if old is not None and old.shape == rshape and np.isfinite(old).all():
            new = old - old.mean() + centre             # keep the measured descan, move its mean
        else:
            new = np.full(rshape, centre)
        getattr(c, f"set_{key}")(new)                   # also sets {key}_mean and {key}_shift
    if scan_step and cal["R_pixel_units"] != "pixels":
        c.set_R_pixel_size(cal["R_pixel_size"])
        c.set_R_pixel_units(cal["R_pixel_units"])
    return cal


def images(self) -> dict:
    """The images computed so far: ``{id: name}`` (ids for :func:`image`)."""
    return {id: name for id, name in zip(self.G.ImgID, self.G.ImgName)
            if self.Fig[id] is not None and getattr(self.Fig[id], "Image", None) is not None}


def _id(self, key: str) -> str:
    if key in self.G.ImgID:
        return key
    by_name = {str(n).lower(): i for i, n in zip(self.G.ImgID, self.G.ImgName)}
    if str(key).lower() in by_name:
        return by_name[str(key).lower()]
    raise KeyError(f"no image {key!r}; images: {', '.join(self.G.ImgID)}")


def image(self, key: str = "Real") -> np.ndarray:
    """A copy of an image as computed (before display brightness/contrast), by id or window name,
    e.g. ``"Real"``, ``"Dfrn"``, ``"iCoM"``, ``"CoMX"``.  Real-space images are (Rx, Ry),
    diffraction images (Qx, Qy)."""
    _need_data(self)
    id = _id(self, key)
    img = getattr(self.Fig[id], "Image", None)
    if img is None:
        raise ValueError(f"{id} has not been computed (show it, or switch to a mode that makes it)")
    return np.array(img, copy=True)


def mask(self, key: Optional[str] = None) -> np.ndarray:
    """A copy of a detector or ROI mask.

    ``None`` (or ``"detector"``): the detector of the current mode, as on the
    diffraction-mask window, (Qx, Qy); ``"roi"``: the real-space ROI, (Rx, Ry);
    otherwise a custom detector's ID (e.g. ``"A"``), inverted if set so but not
    weighted.
    """
    _need_data(self)
    if key is None or str(key).lower() == "detector":
        out = self.Fig.DfrnMask.Image
    elif str(key).lower() == "roi":
        out = self.Fig.RealMask.Image
    else:
        custom = getattr(self.A, "Custom", {}) or {}
        if key not in custom:
            raise KeyError(f"no custom detector {key!r}; custom detectors: {', '.join(custom) or 'none'}")
        out = custom[key].mask
    if out is None:
        raise ValueError(f"mask {key or 'detector'!r} has not been computed yet")
    return np.array(out, copy=True)
