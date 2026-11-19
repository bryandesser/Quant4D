"""A minimal DM3/DM4 writer for tests: follows the published tag layout, both versions and byte orders."""
import struct

import numpy as np

# DM image DataType codes and tag encodings used by the writer
_DM_TYPE = {"u2": 10, "f4": 2, "u4": 11, "i2": 1}
_ENC = {"u2": 4, "f4": 6, "u4": 5, "i2": 2}


class _DMWriter:
    def __init__(self, version, little):
        self.v4, self.o = version == 4, "<" if little else ">"
        self.version, self.little = version, little

    def L(self, n):                                   # big-endian length field
        return struct.pack(">Q" if self.v4 else ">I", n)

    def tag(self, kind, label, body):
        label = label.encode()
        head = struct.pack(">BH", kind, len(label)) + label
        return head + (struct.pack(">Q", len(body)) if self.v4 else b"") + body

    def group(self, entries):
        return b"\x00\x01" + self.L(len(entries)) + b"".join(entries)

    def long(self, label, v):
        return self.tag(21, label, b"%%%%" + self.L(1) + self.L(3) + struct.pack(self.o + "i", v))

    def string(self, label, text):                     # ushort array holding UTF-16 text
        raw = text.encode("utf-16-le" if self.o == "<" else "utf-16-be")
        return self.tag(21, label, b"%%%%" + self.L(3) + self.L(20) + self.L(4) + self.L(len(raw) // 2) + raw)

    def struct_tag(self, label):                       # a 2-field struct, to exercise struct parsing
        info = [15, 0, 2, 0, 6, 0, 6]
        return self.tag(21, label, b"%%%%" + self.L(len(info)) + b"".join(self.L(i) for i in info)
                        + struct.pack(self.o + "ff", 1.5, 2.5))

    def array(self, label, arr, code):
        info = [20, _ENC[code], arr.size]
        head = b"%%%%" + self.L(len(info)) + b"".join(self.L(i) for i in info)
        return self.tag(21, label, head + arr.astype(np.dtype(code).newbyteorder(self.o)).tobytes())

    def real(self, label, v):                          # a float (DM 'float', encoding 6)
        return self.tag(21, label, b"%%%%" + self.L(1) + self.L(6) + struct.pack(self.o + "f", v))

    def double(self, label, v):                        # encoding 7
        return self.tag(21, label, b"%%%%" + self.L(1) + self.L(7) + struct.pack(self.o + "d", v))

    def calibrations(self, cals):
        """``ImageData/Calibrations/Dimension/<i>`` groups of (scale, units, origin)."""
        dims = [self.tag(20, "", self.group([self.real("Origin", o), self.real("Scale", s), self.string("Units", u)]))
                for s, u, o in cals]
        return self.tag(20, "Calibrations", self.group([self.tag(20, "Dimension", self.group(dims))]))

    def image(self, name, arr, code, cals=None, voltage=None):
        dims = arr.shape[::-1]                         # DM lists the fastest dimension first
        data = self.group([self.long("DataType", _DM_TYPE[code]), self.array("Data", arr.ravel(), code),
                           self.tag(20, "Dimensions", self.group([self.long("", d) for d in dims])),
                           self.calibrations(cals) if cals else self.struct_tag("Calibrations")])
        entries = [self.string("Name", name), self.tag(20, "ImageData", data)]
        if voltage is not None:
            entries.append(self.tag(20, "ImageTags", self.group([
                self.tag(20, "Microscope Info", self.group([self.double("Voltage", voltage)]))])))
        return self.tag(20, "", self.group(entries))

    def file(self, images):
        root = self.group([self.struct_tag("Something"),
                           self.tag(20, "ImageList", self.group([self.image(*im) for im in images]))])
        head = struct.pack(">I", self.version) + self.L(len(root)) + struct.pack(">I", 1 if self.little else 0)
        return head + root + b"\x00" * 8
