"""MRC (2014) header: the unit cell, for the scan step.

A 4D-STEM MRC file is a stack: x and y are the detector, z runs over the
probe positions (``NFrX * NFrY`` frames).  The cell dimensions ``xlen``,
``ylen``, ``zlen`` (words 11-13, Å) over the sampling ``mx``, ``my``, ``mz``
(words 8-10) give the spacing along each axis.  pyQuant4D takes the **z
spacing** as the scan step (one step, the same in x and y); the x/y spacing
describes the detector axes and is reported but not used.  A file without a
z spacing (``zlen = 0``, as most writers leave it) has no scan step.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

__all__ = ["MRCCell", "read_mrc_cell"]


@dataclass
class MRCCell:
    n: tuple            # (nx, ny, nz)
    m: tuple            # sampling (mx, my, mz)
    length_A: tuple     # cell (xlen, ylen, zlen) in Å

    def spacing_A(self, axis: int) -> Optional[float]:
        """Spacing along *axis* (0 = x, 1 = y, 2 = z) in Å, or None if not set."""
        length, m = float(self.length_A[axis]), int(self.m[axis])
        if not np.isfinite(length) or length <= 0 or m <= 0:
            return None
        return length / m

    @property
    def scan_step_A(self) -> Optional[float]:
        return self.spacing_A(2)


def read_mrc_cell(path: str) -> Optional[MRCCell]:
    """The cell of an MRC file, or None if the header is not MRC ("MAP " missing)."""
    head = np.fromfile(path, dtype=np.uint8, count=1024)
    if head.size < 1024 or bytes(head[208:212]) != b"MAP ":
        return None
    stamp = bytes(head[212:214])
    order = ">" if stamp[:1] == b"\x11" else "<"          # 0x44 0x44/0x41: little; 0x11 0x11: big
    words_i = np.frombuffer(head[:40].tobytes(), dtype=order + "i4")
    words_f = np.frombuffer(head[40:52].tobytes(), dtype=order + "f4")
    return MRCCell(n=tuple(int(v) for v in words_i[0:3]), m=tuple(int(v) for v in words_i[7:10]),
                   length_A=tuple(float(v) for v in words_f))
