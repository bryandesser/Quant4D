"""Unit tests for the state namespaces in callbacks.appClass and utils.isDiffToPrev."""
from types import SimpleNamespace

import numpy as np
import pytest

from callbacks.appClass import A, C, D, G, P, Prev, T
from callbacks.utils import isDiffToPrev


@pytest.mark.parametrize("cls", [A, C, D, G, P, Prev, T])
def test_misspelled_attribute_is_rejected(cls):
    obj = cls()
    with pytest.raises(AttributeError):
        obj.NoSuchField = 1


def test_instances_do_not_share_mutable_defaults():
    a1, a2 = A(), A()
    a1.ROIs["RealROI"] = "x"
    a1.vectField["Real"] = "q"
    assert a2.ROIs["RealROI"] is None and a2.vectField["Real"] is None
    assert D().NPx is not D().NPx
    assert T().Preview is not T().Preview


def test_new_instance_resets_to_defaults():
    p = P()
    p.RMax, p.TransBeamInit = 99, 1
    assert (P().RMax, P().TransBeamInit) == (0, 0)


def test_D_swap_keeps_dimensions_consistent():
    d = D()
    d.NPxX, d.NPxY, d.NPx = 12, 8, np.array([12, 8])
    d.NFrX, d.NFrY, d.NFr = 5, 3, np.array([3, 5])
    d.swapDiff()
    d.swapReal()
    assert (d.NPxX, d.NPxY, list(d.NPx)) == (8, 12, [8, 12])
    assert (d.NFrX, d.NFrY, list(d.NFr)) == (3, 5, [5, 3])


def test_A_removeGroup_clears_tagged_annotations():
    removed = []
    a = A()
    a.ScanDirXline = SimpleNamespace(remove=lambda: removed.append("x"))
    a.ScanDirYcirc = SimpleNamespace(remove=lambda: removed.append("y"))
    a.adf = "keep"
    a.removeGroup("ScanDir")
    assert sorted(removed) == ["x", "y"]
    assert a.ScanDirXline is None and a.ScanDirYcirc is None and a.adf == "keep"


def test_G_image_groups():
    g = G()
    assert g.getDfrn() == ["Dfrn", "DfrnMask"]
    assert "Real" in g.getReal() and "Dfrn" not in g.getReal()
    assert len(g.Img) == len(g.ImgID)


class TestIsDiffToPrev:
    @pytest.fixture()
    def app(self):
        return SimpleNamespace(Prev=Prev())

    def test_first_call_is_different_then_same(self, app):
        assert isDiffToPrev(app, "AnnR", [3, 9])
        assert not isDiffToPrev(app, "AnnR", [3, 9])
        assert isDiffToPrev(app, "AnnR", [3, 10])

    def test_beam_centre_moving_along_one_axis_is_a_change(self, app):
        """Regression: the old `.all()` test only fired when X *and* Y both moved."""
        assert isDiffToPrev(app, "B0", np.array([64.0, 64.0]))
        assert isDiffToPrev(app, "B0", np.array([65.0, 64.0]))
        assert not isDiffToPrev(app, "B0", np.array([65.0, 64.0]))

    def test_image_with_one_changed_pixel_is_a_change(self, app):
        im = np.ma.masked_invalid(np.ones((4, 4)))
        assert isDiffToPrev(app, "im", im)
        assert not isDiffToPrev(app, "im", im)
        im[2, 2] = 5.0                      # edited in place
        assert isDiffToPrev(app, "im", im)

    def test_shape_change_is_a_change(self, app):
        isDiffToPrev(app, "im", np.zeros((4, 4)))
        assert isDiffToPrev(app, "im", np.zeros((4, 5)))

    def test_nan_images_compare_equal_to_themselves(self, app):
        im = np.array([[np.nan, 1.0]])
        isDiffToPrev(app, "im", im)
        assert not isDiffToPrev(app, "im", im.copy())

    def test_tuple_of_parameters(self, app):
        ax = object()
        assert isDiffToPrev(app, "hist", (ax, 0.0, 1.0, True))
        assert not isDiffToPrev(app, "hist", (ax, 0.0, 1.0, True))
        assert isDiffToPrev(app, "hist", (ax, 0.0, 2.0, True))

    def test_undeclared_name_raises(self, app):
        with pytest.raises(AttributeError):
            isDiffToPrev(app, "typo", 1)
