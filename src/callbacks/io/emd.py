"""py4DSTEM-compatible EMD 1.0 files, written and read with h5py alone.

py4DSTEM saves through the ``emdfile`` package.  The layout used for a
``DataCube`` is small and fixed, so pyQuant4D writes it directly: the dataset
is streamed block by block (partial, sampled and binned exports work exactly
as for the plain HDF5 export, at any dataset size), it is stored contiguously
(so pyQuant4D can import the file again by offset) and py4DSTEM does not have
to be installed.  ``tests/unit/test_emd.py`` reads every file back with
``py4DSTEM.read`` whenever py4DSTEM is installed, which pins the layout.

Layout (``emdfile`` 0.0.x / EMD 1.0, as written by py4DSTEM 0.14)::

    /                            emd_group_type=file, version 1.0
    /<root>                      emd_group_type=root
    /<root>/datacube             emd_group_type=array, python_class=DataCube
        data                     (ry, rx, py, px); py4DSTEM calls the axes (Rx, Ry, Qx, Qy)
        dim0 .. dim3             two-point calibration vectors, attrs name/units
        <image>                  child arrays (VirtualImage, RealSlice, DiffractionSlice)
    /<root>/metadatabundle/calibration   python_class=Calibration
    /<root>/metadatabundle/pyquant4d     python_class=Metadata (session record)

Axis names
----------
py4DSTEM uses matrix order: its first axis ``Rx``/``Qx`` is the *row*.
pyQuant4D's x is the column (the fast scan axis).  The array needs no
transposition, but every coordinate pair swaps: py4DSTEM's ``qx0`` is
pyQuant4D's beam **y**, ``qy0`` its beam **x**.
"""
from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from typing import Mapping, Optional

import numpy as np

from callbacks.io.export import (Region, _iter_blocks, _with_byteorder, exported_dtype,
                                 exported_shape)

__all__ = ["EmdCalibration", "EmdImage", "EmdInfo", "write_emd", "is_emd", "read_emd_info"]

ROOT = "pyquant4d_root"
DATACUBE = "datacube"


@dataclass
class EmdCalibration:
    """Calibration of the *exported* dataset, in pyQuant4D's (x, y) convention.

    Attributes
    ----------
    beam_xy : (x, y) or None
        Transmitted-beam centre in exported detector pixels.  A single global
        centre: written as py4DSTEM's mean origin and as constant origin maps
        over the scan.  #descan: per-position centres would replace the
        constant maps once pyQuant4D measures them.
    q_pixel_size, q_units : detector pixel size, e.g. (0.25, "mrad").
    r_pixel_size, r_units : scan step, e.g. (1.0, "pixels").
    probe_semiangle_mrad : convergence semi-angle, or None.
    """
    beam_xy: Optional[tuple[float, float]] = None
    q_pixel_size: float = 1.0
    q_units: str = "pixels"
    r_pixel_size: float = 1.0
    r_units: str = "pixels"
    probe_semiangle_mrad: Optional[float] = None


@dataclass
class EmdImage:
    """A derived image stored as a child of the DataCube.

    ``space`` is ``"real"`` (shape (NFrY, NFrX) of the loaded scan) or
    ``"dfrn"`` (shape (NPxY, NPxX) of the loaded pattern); the writer crops,
    samples or bins it like the dataset.
    """
    data: np.ndarray
    space: str = "real"
    python_class: str = ""      # default: VirtualImage (real) / DiffractionSlice (dfrn)


@dataclass
class EmdInfo:
    """What :func:`read_emd_info` finds in an EMD file."""
    dataset: str                                # HDF5 path of the 4-D data
    shape: tuple[int, int, int, int]            # (ry, rx, py, px)
    dtype: np.dtype
    calibration: EmdCalibration
    images: list[str] = field(default_factory=list)   # HDF5 paths of child arrays
    authoring_program: str = ""


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------
def _put(group, key: str, value, kind: str) -> None:
    """One calibration/metadata item, tagged the way emdfile tags it."""
    ds = group.create_dataset(key, data=value)
    ds.attrs["type"] = kind


def _put_any(group, key: str, value) -> None:
    if value is None:
        return
    if isinstance(value, (bool, np.bool_)):
        _put(group, key, bool(value), "bool")
    elif isinstance(value, str):
        _put(group, key, value, "string")
    elif np.ndim(value) == 0:
        _put(group, key, float(value), "number")
    else:
        _put(group, key, np.asarray(value), "array")


def _dims(group, specs) -> None:
    for i, (name, units, step) in enumerate(specs):
        ds = group.create_dataset(f"dim{i}", data=np.array([0.0, float(step)]))
        ds.attrs["name"] = name
        ds.attrs["units"] = units


def _array_group(parent, name: str, python_class: str, data: np.ndarray, units: str, dims) -> None:
    g = parent.create_group(name)
    g.attrs["emd_group_type"] = "array"
    g.attrs["python_class"] = python_class
    ds = g.create_dataset("data", data=data)
    ds.attrs["units"] = units
    _dims(g, dims)


def _real_part(image: np.ndarray, frames: Region) -> np.ndarray:
    """The sampled scan region of a real-space image (NFrY, NFrX)."""
    (x0, y0), (cx, cy), s = frames.start, frames.count, frames.step
    return np.ascontiguousarray(image[y0:y0 + cy * s:s, x0:x0 + cx * s:s][:cy, :cx], dtype=np.float32)


def _dfrn_part(image: np.ndarray, pixels: Region) -> np.ndarray:
    """The binned detector region of a diffraction image (NPxY, NPxX), summed like the data."""
    (x0, y0), (cx, cy), b = pixels.start, pixels.count, pixels.step
    part = np.asarray(image, dtype=np.float64)[y0:y0 + cy * b, x0:x0 + cx * b]
    return part.reshape(cy, b, cx, b).sum(axis=(1, 3)).astype(np.float32)


def write_emd(path: str, data: np.ndarray, scan, detector, frames: Region, pixels: Region,
              calibration: Optional[EmdCalibration] = None,
              images: Optional[Mapping[str, EmdImage]] = None,
              metadata: Optional[Mapping[str, object]] = None,
              byte_order: str = "l") -> tuple[int, int, int, int]:
    """Write the selection as a py4DSTEM DataCube in an EMD 1.0 file.

    Arguments as for :func:`callbacks.io.export.write_hdf5`; *calibration*
    must already describe the exported (cropped/binned) pixels.  Returns the
    shape written, ``(NFrY, NFrX, NPxY, NPxX)``.
    """
    import h5py

    frames.check(scan, binned=False)
    pixels.check(detector, binned=True)
    cal = calibration or EmdCalibration()
    shape = exported_shape(frames, pixels)
    dtype = _with_byteorder(exported_dtype(data.dtype, pixels), byte_order)

    tmp = path + ".part"
    with h5py.File(tmp, "w") as f:
        f.attrs.update({"UUID": str(uuid.uuid4()), "authoring_program": "pyQuant4D",
                        "authoring_user": "", "emd_group_type": "file",
                        "version_major": 1, "version_minor": 0})
        root = f.create_group(ROOT)
        root.attrs.update({"emd_group_type": "root", "python_class": "Root"})

        # the 4-D dataset, streamed; contiguous so pyQuant4D can re-import it by offset
        dc = root.create_group(DATACUBE)
        dc.attrs.update({"emd_group_type": "array", "python_class": "DataCube"})
        dset = dc.create_dataset("data", shape=shape, dtype=dtype)
        dset.attrs["units"] = "pixel intensity"
        for row, col, block in _iter_blocks(data, scan, detector, frames, pixels):
            dset[row, col:col + block.shape[0]] = block
        _dims(dc, [("Rx", cal.r_units, cal.r_pixel_size), ("Ry", cal.r_units, cal.r_pixel_size),
                   ("Qx", cal.q_units, cal.q_pixel_size), ("Qy", cal.q_units, cal.q_pixel_size)])

        # derived images as children of the DataCube
        for name, img in (images or {}).items():
            if img.space == "dfrn":
                arr, cls = _dfrn_part(img.data, pixels), img.python_class or "DiffractionSlice"
                dims = [("Qx", cal.q_units, cal.q_pixel_size), ("Qy", cal.q_units, cal.q_pixel_size)]
            else:
                arr, cls = _real_part(img.data, frames), img.python_class or "VirtualImage"
                dims = [("Rx", cal.r_units, cal.r_pixel_size), ("Ry", cal.r_units, cal.r_pixel_size)]
            _array_group(dc, name, cls, arr, "intensity", dims)

        # calibration, in py4DSTEM's names and (row, column) order
        mb = root.create_group("metadatabundle")
        mb.attrs["emd_group_type"] = "metadatabundle"
        cg = mb.create_group("calibration")
        cg.attrs.update({"emd_group_type": "metadata", "python_class": "Calibration"})
        _put(cg, "Q_pixel_size", float(cal.q_pixel_size), "number")
        _put(cg, "Q_pixel_units", cal.q_units, "string")
        _put(cg, "R_pixel_size", float(cal.r_pixel_size), "number")
        _put(cg, "R_pixel_units", cal.r_units, "string")
        _put(cg, "QR_flip", False, "bool")
        _put(cg, "_root_treepath", "", "string")
        tp = cg.create_group("_target_paths")
        tp.attrs.update({"length": 1, "type": "list_of_strings"})
        tp.create_dataset("0", data=f"/{DATACUBE}")
        if cal.beam_xy is not None:
            bx, by = (float(v) for v in cal.beam_xy)
            rshape = shape[:2]
            _put(cg, "qx0_mean", by, "number")          # py4DSTEM Qx = rows = pyQuant4D y
            _put(cg, "qy0_mean", bx, "number")
            # #descan: constant maps until per-position centres are measured
            _put(cg, "qx0", np.full(rshape, by), "array")
            _put(cg, "qy0", np.full(rshape, bx), "array")
            _put(cg, "qx0_shift", np.zeros(rshape), "array")
            _put(cg, "qy0_shift", np.zeros(rshape), "array")
        if cal.probe_semiangle_mrad is not None:
            _put(cg, "probe_semiangle", float(cal.probe_semiangle_mrad), "number")

        # pyQuant4D's own record of the session
        if metadata:
            mg = mb.create_group("pyquant4d")
            mg.attrs.update({"emd_group_type": "metadata", "python_class": "Metadata"})
            for key, value in metadata.items():
                _put_any(mg, key, value)
    os.replace(tmp, path)
    return shape


# ---------------------------------------------------------------------------
# Reading (no py4DSTEM needed)
# ---------------------------------------------------------------------------
def is_emd(path: str) -> bool:
    """True if *path* is an HDF5 file tagged as an EMD 1.0 file."""
    try:
        import h5py
        with h5py.File(path, "r") as f:
            return f.attrs.get("emd_group_type") == "file"
    except (OSError, ImportError):
        return False


def _str(value) -> str:
    return value.decode() if isinstance(value, bytes) else str(value)


def read_emd_info(path: str) -> Optional[EmdInfo]:
    """The first DataCube of an EMD file and its calibration, or None if there is none.

    Coordinates are returned in pyQuant4D's (x, y) order.
    """
    import h5py

    with h5py.File(path, "r") as f:
        if f.attrs.get("emd_group_type") != "file":
            return None
        for root_name, root in f.items():
            if not isinstance(root, h5py.Group):
                continue
            cube = next((g for g in root.values() if isinstance(g, h5py.Group)
                         and _str(g.attrs.get("python_class", "")) == "DataCube"
                         and isinstance(g.get("data"), h5py.Dataset) and g["data"].ndim == 4), None)
            if cube is None:
                continue
            cal = EmdCalibration()
            cg = root.get("metadatabundle/calibration")
            if isinstance(cg, h5py.Group):
                def get(key, default=None):
                    return cg[key][()] if key in cg else default
                cal.q_pixel_size = float(get("Q_pixel_size", 1.0))
                cal.q_units = _str(get("Q_pixel_units", b"pixels"))
                cal.r_pixel_size = float(get("R_pixel_size", 1.0))
                cal.r_units = _str(get("R_pixel_units", b"pixels"))
                qx0, qy0 = get("qx0_mean"), get("qy0_mean")
                if qx0 is None and "qx0" in cg:            # maps but no means
                    qx0, qy0 = float(np.nanmean(cg["qx0"][()])), float(np.nanmean(cg["qy0"][()]))
                if qx0 is not None and qy0 is not None:
                    cal.beam_xy = (float(qy0), float(qx0))   # back to (x, y)
                semi = get("probe_semiangle")
                cal.probe_semiangle_mrad = None if semi is None else float(semi)
            images = [g.name for g in cube.values() if isinstance(g, h5py.Group)
                      and g.attrs.get("emd_group_type") == "array"]
            data = cube["data"]
            s = data.shape
            return EmdInfo(dataset=data.name, shape=(s[0], s[1], s[2], s[3]), dtype=data.dtype,
                           calibration=cal, images=images,
                           authoring_program=_str(f.attrs.get("authoring_program", "")))
    return None
