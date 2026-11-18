"""Header reader for Gatan DigitalMicrograph DM3 and DM4 files.

Walks the tag tree without loading any image data and reports, for every image
in the file, where its data starts, its element type, byte order and
dimensions.  Pure Python/NumPy; no Qt.

Format summary (both versions)
------------------------------
* File header: version (``>u4``: 3 or 4), root length (``>u4`` in DM3, ``>u8``
  in DM4), byte-order flag (``>u4``: 1 = data little endian, 0 = big endian).
* Tag group: ``sorted`` (u1), ``open`` (u1), number of tags (``>u4`` / ``>u8``).
* Tag: kind (u1: 20 = group, 21 = data), label length (``>u2``), label; in DM4
  also the tag's total size (``>u8``).  A data tag continues with ``%%%%``,
  the number of type descriptors (``>u4`` / ``>u8``), the descriptors (same
  width) and the value.
* Lengths and descriptors are big endian; the values themselves use the
  byte order from the file header.

Image data lives in ``ImageList/<n>/ImageData/Data``; its dimensions are
``ImageData/Dimensions`` (fastest first) and its element type
``ImageData/DataType``.
"""
from __future__ import annotations

import os
import struct
from dataclasses import dataclass, field
from typing import Any, BinaryIO, Optional

import numpy as np

__all__ = ["DMImage", "DMFile", "read_dm_header"]

# tag value encodings -> struct format character and size
_SIMPLE = {
    2: ("h", 2), 3: ("i", 4), 4: ("H", 2), 5: ("I", 4), 6: ("f", 4), 7: ("d", 8),
    8: ("?", 1), 9: ("b", 1), 10: ("B", 1), 11: ("q", 8), 12: ("Q", 8),
}
_STRUCT, _STRING, _ARRAY = 15, 18, 20

# ImageData/DataType -> numpy dtype (without byte order); None = not a plain scalar
IMAGE_DTYPES = {
    1: "i2", 2: "f4", 3: "c8", 6: "u1", 7: "i4", 8: None, 9: "i1", 10: "u2", 11: "u4",
    12: "f8", 13: "c16", 14: "u1", 23: None, 39: "i8", 40: "u8",
}


@dataclass
class DMImage:
    """One image (or 3-D/4-D stack) stored in a DM file."""
    name: str
    offset: int                    # byte offset of the first element
    dtype: Optional[str]           # numpy type code without byte order, e.g. 'f4'; None if unsupported
    data_type_code: int            # ImageData/DataType
    dims: tuple                    # fastest first, as stored in the file
    count: int                     # number of elements

    @property
    def nbytes(self) -> int:
        return self.count * (np.dtype(self.dtype).itemsize if self.dtype else 0)


@dataclass
class DMFile:
    version: int
    little_endian: bool
    file_size: int
    images: list = field(default_factory=list)

    def largest(self) -> Optional[DMImage]:
        return max(self.images, key=lambda im: im.count, default=None)


class _Reader:
    def __init__(self, fh: BinaryIO, version: int, little: bool):
        self.fh, self.v4, self.order = fh, version == 4, "<" if little else ">"

    def big(self, fmt: str):
        size = struct.calcsize(">" + fmt)
        return struct.unpack(">" + fmt, self.fh.read(size))[0]

    def length(self) -> int:
        return self.big("Q" if self.v4 else "I")

    def value(self, fmt: str):
        size = struct.calcsize(self.order + fmt)
        return struct.unpack(self.order + fmt, self.fh.read(size))[0]

    # --------------------------------------------------------------- tags
    def group(self) -> dict:
        self.fh.read(2)                     # sorted, open
        n = self.length()
        out: dict = {}
        unnamed = 0
        for _ in range(n):
            kind = self.big("B")
            label = self.fh.read(self.big("H")).decode("latin-1")
            if self.v4:
                self.length()               # total size of this tag; not needed when walking
            if not label:
                label, unnamed = str(unnamed), unnamed + 1
            if kind == 20:
                out[label] = self.group()
            elif kind == 21:
                out[label] = self.data_tag()
            elif kind == 0:
                break
            else:
                raise ValueError(f"unknown tag kind {kind} at byte {self.fh.tell()}")
        return out

    def data_tag(self) -> Any:
        if self.fh.read(4) != b"%%%%":
            raise ValueError(f"missing %%%% marker at byte {self.fh.tell() - 4}")
        info = [self.length() for _ in range(self.length())]
        return self.typed(info)

    def typed(self, info: list) -> Any:
        enc = info[0]
        if enc in _SIMPLE:
            return self.value(_SIMPLE[enc][0])
        if enc == _STRING:
            return self.fh.read(info[1] * 2).decode("utf-16-le" if self.order == "<" else "utf-16-be", "replace")
        if enc == _STRUCT:
            # [15, name length, n fields, (field name length, field type) * n]
            nfields = info[2]
            types = info[4:3 + 2 * nfields:2]
            return tuple(self.value(_SIMPLE[t][0]) for t in types)
        if enc == _ARRAY:
            elem = info[1]
            if elem == _STRUCT:
                # [20, 15, name length, n fields, (field name length, field type) * n, count]
                nfields = info[3]
                types = info[5:4 + 2 * nfields:2]
                count = info[4 + 2 * nfields]
                size = sum(_SIMPLE[t][1] for t in types) * count
                start = self.fh.tell()
                self.fh.seek(size, os.SEEK_CUR)
                return {"array_of": "struct", "offset": start, "count": count, "bytes": size}
            count = info[2]
            size = _SIMPLE[elem][1] * count
            start = self.fh.tell()
            if elem in (4, 10) and count <= 4096:          # small ushort/octet arrays are usually text
                raw = self.fh.read(size)
                text = raw.decode("utf-16-le" if self.order == "<" else "utf-16-be", "replace") if elem == 4 else None
                return {"array_of": elem, "offset": start, "count": count, "bytes": size, "text": text}
            self.fh.seek(size, os.SEEK_CUR)
            return {"array_of": elem, "offset": start, "count": count, "bytes": size}
        raise ValueError(f"unsupported tag encoding {info}")


def read_dm_header(path: str) -> DMFile:
    """Read the tag tree of a DM3/DM4 file and describe every image in it."""
    with open(path, "rb") as fh:
        version = struct.unpack(">I", fh.read(4))[0]
        if version not in (3, 4):
            raise ValueError(f"{os.path.basename(path)} is not a DM3/DM4 file (version {version})")
        fh.read(8 if version == 4 else 4)               # root length
        little = struct.unpack(">I", fh.read(4))[0] == 1
        root = _Reader(fh, version, little).group()

    images = []
    for key, entry in (root.get("ImageList") or {}).items():
        data = (entry.get("ImageData") or {})
        arr = data.get("Data")
        if not isinstance(arr, dict) or "offset" not in arr:
            continue
        dims = tuple(int(v) for _, v in sorted((data.get("Dimensions") or {}).items(), key=lambda kv: int(kv[0])))
        code = int(data.get("DataType", -1))
        dtype = IMAGE_DTYPES.get(code)
        name = entry.get("Name")
        name = name["text"] if isinstance(name, dict) and name.get("text") else (name if isinstance(name, str) else f"Image {key}")
        count = int(np.prod(dims)) if dims else arr["count"]
        if dtype is not None and arr["bytes"] != count * np.dtype(dtype).itemsize:
            dtype = None                                   # e.g. packed/RGB data: size does not match
        images.append(DMImage(name=name.strip("\x00"), offset=arr["offset"], dtype=dtype,
                              data_type_code=code, dims=dims, count=count))
    return DMFile(version=version, little_endian=little, file_size=os.path.getsize(path), images=images)
