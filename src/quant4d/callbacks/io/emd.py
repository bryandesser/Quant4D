"""py4DSTEM-compatible EMD 1.0 files, written and read with h5py alone.

py4DSTEM saves through the ``emdfile`` package.  The layout used for a
``DataCube`` is small and fixed, so Quant4D writes it directly: the dataset
is streamed block by block (partial, sampled and binned exports work exactly
as for the plain HDF5 export, at any dataset size), it is stored contiguously
(so Quant4D can import the file again by offset) and py4DSTEM does not have
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
    /<root>/metadatabundle/quant4d     python_class=Metadata (session record)

Axis names
----------
py4DSTEM uses matrix order: its first axis ``Rx``/``Qx`` is the *row*.
Quant4D's x is the column (the fast scan axis).  The array needs no
transposition, but every coordinate pair swaps: py4DSTEM's ``qx0`` is
Quant4D's beam **y**, ``qy0`` its beam **x**.
"""
from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field, replace
from typing import Any, Mapping, Optional

import numpy as np

from .export import (Region, _iter_blocks, _with_byteorder, exported_dtype,
                                 exported_shape)

__all__ = ["EmdCalibration", "EmdImage", "EmdInfo", "write_emd", "is_emd", "read_emd_info",
           "usable_calibration", "calibration_for_region", "describe_emd",
           "electron_wavelength_A", "mrad_per_inverse_angstrom", "is_inverse_angstrom", "mrad_per_unit"]

ROOT = "quant4d_root"
DATACUBE = "datacube"


@dataclass
class EmdCalibration:
    """Calibration of the *exported* dataset, in Quant4D's (x, y) convention.

    Attributes
    ----------
    beam_xy : (x, y) or None
        Transmitted-beam centre in exported detector pixels.  A single global
        centre: written as py4DSTEM's mean origin and as constant origin maps
        over the scan.  #descan: per-position centres would replace the
        constant maps once Quant4D measures them.
    q_pixel_size, q_units : detector pixel size, e.g. (0.25, "mrad").
    r_pixel_size, r_units : scan step, e.g. (1.0, "pixels").
    probe_semiangle_mrad : convergence semi-angle in mrad (py4DSTEM's
        ``convergence_semiangle_mrad``), or None.
    probe_radius_px : radius of the transmitted disk in detector pixels
        (py4DSTEM's ``probe_semiangle``, as ``get_probe_size`` measures it), or None.
    """
    beam_xy: Optional[tuple[float, float]] = None
    q_pixel_size: float = 1.0
    q_units: str = "pixels"
    r_pixel_size: float = 1.0
    r_units: str = "pixels"
    probe_semiangle_mrad: Optional[float] = None
    probe_radius_px: Optional[float] = None


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
    mask: bool = False          # a mask: binned raw (summed) or normalised to 0..1, see write_emd


@dataclass
class EmdInfo:
    """What :func:`read_emd_info` finds in an EMD file."""
    dataset: str                                # HDF5 path of the 4-D data
    shape: tuple[int, int, int, int]            # (ry, rx, py, px)
    dtype: np.dtype
    calibration: EmdCalibration
    images: list[str] = field(default_factory=list)   # HDF5 paths of child arrays
    authoring_program: str = ""
    origin_spread_px: float = 0.0               # how far the origin maps vary over the scan (#descan)
    accelerating_voltage_kV: Optional[float] = None   # from Quant4D's session record, if present


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
              byte_order: str = "l", normalize_masks: bool = False) -> tuple[int, int, int, int]:
    """Write the selection as a py4DSTEM DataCube in an EMD 1.0 file.

    Arguments as for :func:`callbacks.io.export.write_hdf5`; *calibration*
    must already describe the exported (cropped/binned) pixels.  Binned
    diffraction images are summed like the data; with *normalize_masks*, those
    marked ``mask`` are divided by the bin area instead (the fraction of each
    binned pixel inside the mask, 0 to 1).  Returns the shape written,
    ``(NFrY, NFrX, NPxY, NPxX)``.
    """
    import h5py

    frames.check(scan, binned=False)
    pixels.check(detector, binned=True)
    cal = calibration or EmdCalibration()
    shape = exported_shape(frames, pixels)
    dtype = _with_byteorder(exported_dtype(data.dtype, pixels), byte_order)

    tmp = path + ".part"
    with h5py.File(tmp, "w") as f:
        f.attrs.update({"UUID": str(uuid.uuid4()), "authoring_program": "Quant4D",
                        "authoring_user": "", "emd_group_type": "file",
                        "version_major": 1, "version_minor": 0})
        root = f.create_group(ROOT)
        root.attrs.update({"emd_group_type": "root", "python_class": "Root"})

        # the 4-D dataset, streamed; contiguous so Quant4D can re-import it by offset
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
                if img.mask and normalize_masks:
                    arr = arr / np.float32(pixels.step ** 2)
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
            _put(cg, "qx0_mean", by, "number")          # py4DSTEM Qx = rows = Quant4D y
            _put(cg, "qy0_mean", bx, "number")
            # #descan: constant maps until per-position centres are measured
            _put(cg, "qx0", np.full(rshape, by), "array")
            _put(cg, "qy0", np.full(rshape, bx), "array")
            _put(cg, "qx0_shift", np.zeros(rshape), "array")
            _put(cg, "qy0_shift", np.zeros(rshape), "array")
        # py4DSTEM: probe_semiangle is the disk radius in pixels, the angle is convergence_semiangle_mrad
        if cal.probe_semiangle_mrad is not None:
            _put(cg, "convergence_semiangle_mrad", float(cal.probe_semiangle_mrad), "number")
        radius = cal.probe_radius_px
        if radius is None and cal.probe_semiangle_mrad and cal.q_units == "mrad" and cal.q_pixel_size > 0:
            radius = cal.probe_semiangle_mrad / cal.q_pixel_size
        if radius is not None:
            _put(cg, "probe_semiangle", float(radius), "number")

        # Quant4D's own record of the session
        if metadata:
            mg = mb.create_group("quant4d")
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


def _is_datacube(g: Any) -> bool:
    """An EMD DataCube group: tagged so, with a 4-D ``data`` dataset (h5py nodes typed loosely)."""
    import h5py
    if not isinstance(g, h5py.Group) or _str(g.attrs.get("python_class", "")) != "DataCube":
        return False
    data = g.get("data")
    return isinstance(data, h5py.Dataset) and data.ndim == 4


def _value(group: Any, key: str, default=None) -> Any:
    """``group[key][()]`` if there is one, else *default*."""
    return group[key][()] if key in group else default


def read_emd_info(path: str) -> Optional[EmdInfo]:
    """The first DataCube of an EMD file and its calibration, or None if there is none.

    Coordinates are returned in Quant4D's (x, y) order.
    """
    import h5py

    with h5py.File(path, "r") as f:
        if f.attrs.get("emd_group_type") != "file":
            return None
        for root_name, root in f.items():
            if not isinstance(root, h5py.Group):
                continue
            cube: Any = next((g for g in root.values() if _is_datacube(g)), None)
            if cube is None:
                continue
            cal = EmdCalibration()
            spread = 0.0
            cg: Any = root.get("metadatabundle/calibration")
            if isinstance(cg, h5py.Group):
                def get(key, default=None) -> Any:
                    return _value(cg, key, default)
                cal.q_pixel_size = float(get("Q_pixel_size", 1.0))
                cal.q_units = _str(get("Q_pixel_units", b"pixels"))
                cal.r_pixel_size = float(get("R_pixel_size", 1.0))
                cal.r_units = _str(get("R_pixel_units", b"pixels"))
                qx0, qy0 = get("qx0_mean"), get("qy0_mean")
                if "qx0" in cg and "qy0" in cg:
                    maps = np.asarray(get("qx0"), float), np.asarray(get("qy0"), float)
                    if all(m.size and np.isfinite(m).any() for m in maps):
                        spread = max(float(np.nanmax(m) - np.nanmin(m)) for m in maps)
                        if qx0 is None:                    # maps but no means
                            qx0, qy0 = float(np.nanmean(maps[0])), float(np.nanmean(maps[1]))
                if qx0 is not None and qy0 is not None:
                    cal.beam_xy = (float(qy0), float(qx0))   # back to (x, y)
                semi, radius = get("convergence_semiangle_mrad"), get("probe_semiangle")
                cal.probe_semiangle_mrad = None if semi is None else float(semi)
                cal.probe_radius_px = None if radius is None else float(radius)   # pixels in py4DSTEM
            images = [str(g.name) for g in cube.values() if isinstance(g, h5py.Group)
                      and g.attrs.get("emd_group_type") == "array"]
            data = cube["data"]
            s = data.shape
            return EmdInfo(dataset=str(data.name), shape=(s[0], s[1], s[2], s[3]), dtype=data.dtype,
                           calibration=cal, images=images,
                           authoring_program=_str(f.attrs.get("authoring_program", "")),
                           origin_spread_px=spread, accelerating_voltage_kV=_session_kV(root))
    return None


def _session_kV(root) -> Optional[float]:
    """The accelerating voltage Quant4D recorded with an export, if any."""
    ds = root.get("metadatabundle/quant4d/accelerating_voltage_kV")
    try:
        kv = float(ds[()]) if ds is not None else None
    except (TypeError, ValueError):
        return None
    return kv if kv is not None and kv > 0 else None


# ---------------------------------------------------------------------------
# Scattering angle <-> spatial frequency
# ---------------------------------------------------------------------------
HC_KEV_A = 12.398419843320026          # h c in keV Å
MC2_KEV = 510.99895000                 # electron rest energy in keV
_INVERSE_ANGSTROM = {"a^-1", "å^-1", "a-1", "å-1", "1/a", "1/å", "a^{-1}", "å^{-1}", "angstrom^-1", "inverse angstrom"}


def electron_wavelength_A(kV: float) -> float:
    """Relativistic electron wavelength in Å for an accelerating voltage in kV.

    ``λ = h c / sqrt(E (E + 2 m c²))`` with E the kinetic energy (e.g. 300 kV:
    0.019687 Å; 200 kV: 0.025079 Å).
    """
    e = float(kV)
    if e <= 0:
        raise ValueError(f"the accelerating voltage must be positive, not {kV}")
    return HC_KEV_A / np.sqrt(e * (e + 2 * MC2_KEV))


def mrad_per_inverse_angstrom(kV: float) -> float:
    """Scattering angle per spatial frequency: θ = λ k (small angles, py4DSTEM's
    convention: k in Å⁻¹ without 2π), so 1 Å⁻¹ is ``1000 λ`` mrad."""
    return 1000.0 * electron_wavelength_A(kV)


def is_inverse_angstrom(units: str) -> bool:
    return units.strip().lower().replace(" ", "") in _INVERSE_ANGSTROM


# detector units Quant4D converts to mrad: angles directly, spatial frequencies (no 2π) at a voltage
_ANGLES_MRAD = {"mrad": 1.0, "rad": 1000.0, "urad": 1e-3, "µrad": 1e-3, "μrad": 1e-3}
_PER_ANGSTROM = {"1/nm": 0.1, "nm^-1": 0.1, "nm-1": 0.1, "nm^{-1}": 0.1, "1/pm": 100.0, "pm^-1": 100.0}


def mrad_per_unit(units: str, kV: Optional[float] = None) -> Optional[float]:
    """mrad per detector unit (mrad, rad, µrad; Å⁻¹ or nm⁻¹ at *kV*), or None if it cannot be converted."""
    u = units.strip().lower().replace(" ", "")
    if u in _ANGLES_MRAD:
        return _ANGLES_MRAD[u]
    per_a = 1.0 if u in _INVERSE_ANGSTROM else _PER_ANGSTROM.get(u)
    if per_a is None or not kV or kV <= 0:
        return None
    return per_a * mrad_per_inverse_angstrom(kV)


# ---------------------------------------------------------------------------
# Using a file's calibration in Quant4D
# ---------------------------------------------------------------------------
def _in_mrad(cal: EmdCalibration) -> bool:
    return cal.q_units.strip().lower() == "mrad" and cal.q_pixel_size > 0


def usable_calibration(cal: EmdCalibration, kV: Optional[float] = None) -> Optional[EmdCalibration]:
    """The parts of *cal* Quant4D can use, or None if there are none.

    Quant4D calibrates the detector in mrad.  Other angles (rad, µrad) are
    rescaled; a pixel size in Å⁻¹ (py4DSTEM's ``A^-1``) or nm⁻¹ (DM's
    ``1/nm``) is converted with the relativistic wavelength at *kV*; without a
    voltage, or in other units (plain pixels), it is dropped.
    """
    semi = cal.probe_semiangle_mrad if cal.probe_semiangle_mrad and cal.probe_semiangle_mrad > 0 else None
    factor = mrad_per_unit(cal.q_units, kV) if cal.q_pixel_size > 0 else None
    if factor is not None:
        q = cal.q_pixel_size * factor
        if semi is None and cal.probe_radius_px and cal.probe_radius_px > 0:
            semi = cal.probe_radius_px * q          # the disk radius at the detector scale
        out = replace(cal, q_pixel_size=q, q_units="mrad", probe_semiangle_mrad=semi)
    else:
        out = replace(cal, q_pixel_size=1.0, q_units="pixels", probe_semiangle_mrad=semi)
    if out.beam_xy is None and out.q_units != "mrad" and semi is None and not out.probe_radius_px:
        return None
    return out


def calibration_for_region(cal: EmdCalibration, start_xy, binning: int) -> EmdCalibration:
    """*cal*, in pixels of the file's detector, for a region starting at
    *start_xy* (0-based (x, y)) and binned by *binning*.

    Pixel i of the region covers file pixels ``start + i*b`` to
    ``start + i*b + b - 1``, so a centre ``c`` becomes ``(c - start + 0.5)/b - 0.5``.
    """
    b = int(binning)
    beam = None
    if cal.beam_xy is not None:
        beam = tuple((float(c) - float(s) + 0.5) / b - 0.5 for c, s in zip(cal.beam_xy, start_xy))
    q = cal.q_pixel_size * b if cal.q_units != "pixels" else cal.q_pixel_size
    radius = None if cal.probe_radius_px is None else cal.probe_radius_px / b
    return replace(cal, beam_xy=beam, q_pixel_size=q, probe_radius_px=radius)


def describe_emd(info: EmdInfo, kV: Optional[float] = None) -> str:
    """Lines for the Import window's file notes about a py4DSTEM DataCube (*kV*: the
    accelerating voltage set in the Import window, for an Å⁻¹ calibration)."""
    cal = info.calibration
    lines = [f"py4DSTEM DataCube{f' (written by {info.authoring_program})' if info.authoring_program else ''}"]
    if cal.beam_xy is not None:
        line = f"Beam centre (x, y) = ({cal.beam_xy[0]:.2f}, {cal.beam_xy[1]:.2f}) px"
        if info.origin_spread_px > 0.01:
            line += f"; the origin moves by up to {info.origin_spread_px:.2f} px over the scan (the mean is used)"
        lines.append(line)
    if _in_mrad(cal):
        lines.append(f"Detector: {cal.q_pixel_size:g} mrad/px")
    elif cal.q_pixel_size > 0 and mrad_per_unit(cal.q_units, kV) is not None:
        factor = mrad_per_unit(cal.q_units, kV)
        assert factor is not None
        at = f" at {kV:g} kV" if cal.q_units.strip().lower().replace(" ", "") not in _ANGLES_MRAD else ""
        lines.append(f"Detector: {cal.q_pixel_size:g} {cal.q_units}/px = "
                     f"{cal.q_pixel_size * factor:.4g} mrad/px{at}")
    elif cal.q_units.strip().lower() != "pixels":
        lines.append(f"Detector: {cal.q_pixel_size:g} {cal.q_units}/px, not used "
                     "(Quant4D calibrates in mrad; set the accelerating voltage to convert Å⁻¹)")
    if cal.r_units.strip().lower() != "pixels":
        lines.append(f"Scan step: {cal.r_pixel_size:g} {cal.r_units}")
    if info.accelerating_voltage_kV:
        lines.append(f"Accelerating voltage: {info.accelerating_voltage_kV:g} kV")
    if cal.probe_semiangle_mrad:
        lines.append(f"Convergence semi-angle: {cal.probe_semiangle_mrad:g} mrad")
    if cal.probe_radius_px:
        lines.append(f"Transmitted disk radius: {cal.probe_radius_px:.2f} px")
    if info.images:
        lines.append("Images: " + ", ".join(p.rsplit("/", 1)[-1] for p in info.images))
    if usable_calibration(cal, kV) is not None:
        lines.append("The calibration is applied to the transmitted beam after import (Alignment mode).")
    return "\n".join(lines)
