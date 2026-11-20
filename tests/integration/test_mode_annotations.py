"""
Each detector mode shows (and listens to) only its own annotations.  Changing a shared control
in Align mode (the beam radius also sets the virtual aperture's radius) used to draw the white
virtual-aperture circle in whatever mode was current; it stayed interactive and took over the
real-space image when dragged.
"""
import pytest

from pyquant4d.annotationsClasses.interactiveCircle import InteractiveCircle
from conftest import set_mode

# modes and the annotation attributes (self.A.*) that may be on the diffraction pattern in them
OWN = {
    "AlignMod": {"tb"},
    "AnnMod": {"adf"},
    "CoMMod": {"adf"},
    "DPCMod": {"adf", "SegDetrL0", "SegDetrP0"},
    "VrApMod": {"VrAp", "VrApMirP", "VrApMirL"},
}
ALL = {"tb", "adf", "VrAp", "VrApMirP", "VrApMirL", "SegDetrL0", "SegDetrP0",
       "ScanDirXline", "ScanDirXcirc", "ScanDirXtext"}


def _present(w):
    return {n for n in ALL if getattr(w.A, n, None) is not None}


def _interactive_circles(w):
    """Circles still listening to the mouse on the diffraction pattern (connected handlers)."""
    return [o for o in (getattr(w.A, n, None) for n in ALL)
            if isinstance(o, InteractiveCircle) and getattr(o, "cidpress", None) is not None]


@pytest.mark.parametrize("path", [("AlignMod", "AnnMod"), ("VrApMod", "AnnMod"), ("VrApMod", "AlignMod"),
                                  ("AlignMod", "VrApMod", "CoMMod"), ("DPCMod", "VrApMod"),
                                  ("DPCMod", "CoMMod"), ("DPCMod", "AnnMod")])
def test_only_the_modes_own_annotations(loaded_app, qapp, path):
    w = loaded_app
    for mode in path:
        set_mode(w, qapp, mode)
        if mode == "AlignMod":                  # the beam radius also drives the virtual aperture's radius
            w.TBR.setValue(w.TBR.value() + 1)
            qapp.processEvents()
        if mode == "VrApMod":                   # symmetry and mirror copies of the aperture
            w.VrApSymm.setCurrentIndex(w.VrApSymm.count() - 1)
            if not w.VrApMirror.isChecked():
                w.VrApMirror.click()
            qapp.processEvents()
        clones = [ln for ln in w.Fig.Dfrn.ax.lines if getattr(ln, "_vrAp_clone", False)]
        assert mode == "VrApMod" or not clones, f"{mode}: virtual-aperture copies left on the pattern"
        stray = _present(w) - OWN[mode]
        assert not stray, f"{mode}: annotations of other modes on the pattern: {sorted(stray)}"
    assert len(_interactive_circles(w)) <= 1
    w.VrApSymm.setCurrentIndex(0)
    if w.VrApMirror.isChecked():
        w.VrApMirror.click()
    set_mode(w, qapp, "AnnMod")
