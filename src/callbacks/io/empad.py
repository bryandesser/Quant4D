"""EMPAD file layout detection.

EMPAD data are 128 x 128 float32 frames, little endian.  Two layouts exist:

* **v1**: each frame is followed by a 1024-byte footer (two 128-float rows of
  metadata), so a frame record is 66,560 bytes.
* **v2**: frames are stored back to back with no footer (65,536 bytes each).

The version is not recorded in the file, so it is worked out from the file
size, using the scan size in the file name (``..._x<NFrX>_y<NFrY>.raw`` or
``..._<NPxX>x<NPxY>x<NFrX>x<NFrY>...``) when there is one.
"""
from __future__ import annotations

import math
import os
import re
from dataclasses import dataclass
from typing import Optional

__all__ = ["EMPAD_PIXELS", "EMPAD_FOOTER_V1", "EmpadLayout", "detect_empad", "scan_from_name"]

EMPAD_PIXELS = 128
EMPAD_FOOTER_V1 = 1024
_FRAME_BYTES = EMPAD_PIXELS * EMPAD_PIXELS * 4


@dataclass(frozen=True)
class EmpadLayout:
    version: int                 # 1 (with footer) or 2 (without)
    footer: int                  # bytes after each frame
    scan: Optional[tuple]        # (NFrX, NFrY) if known
    n_frames: int


def scan_from_name(path: str) -> Optional[tuple]:
    """``(NFrX, NFrY)`` from an EMPAD-style file name, or ``None``."""
    name = os.path.basename(path)
    m = re.search(r"_x(\d+)_y(\d+)", name)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"(\d+)x(\d+)x(\d+)x(\d+)", name)
    if m:
        return int(m.group(3)), int(m.group(4))
    return None


def _squarest(n: int) -> tuple:
    """Factor *n* into ``(x, y)`` with ``x <= y`` as close to square as possible."""
    x = int(math.isqrt(n))
    while x > 1 and n % x:
        x -= 1
    return (x, n // x) if x else (1, n)


def detect_empad(path: str, file_size: Optional[int] = None) -> Optional[EmpadLayout]:
    """Work out whether *path* is an EMPAD v1 or v2 file, and its scan size.

    Returns ``None`` if the file size fits neither layout.
    """
    size = os.path.getsize(path) if file_size is None else file_size
    named = scan_from_name(path)
    fits = []
    for version, footer in ((1, EMPAD_FOOTER_V1), (2, 0)):
        record = _FRAME_BYTES + footer
        if size % record == 0 and size >= record:
            fits.append((version, footer, size // record))
    if not fits:
        return None

    if named is not None:
        for version, footer, n in fits:
            if n == named[0] * named[1]:
                return EmpadLayout(version, footer, named, n)

    # No usable name: prefer the layout whose frame count is a square scan,
    # then v1 (the format that needs the footer to be skipped).
    def score(fit):
        n = fit[2]
        return (math.isqrt(n) ** 2 == n, fit[0] == 1)

    version, footer, n = max(fits, key=score)
    return EmpadLayout(version, footer, _squarest(n), n)
