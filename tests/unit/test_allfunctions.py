"""callbacks.allFunctions is a deprecated alias table (removal in 2.0)."""
import importlib
import pathlib
import warnings

import pytest

import callbacks.allFunctions as af

SRC = pathlib.Path(__file__).resolve().parents[2] / "src"


@pytest.mark.parametrize("name", sorted(af.MOVED))
def test_alias_resolves_with_warning(name):
    with pytest.warns(DeprecationWarning, match=af.MOVED[name]):
        obj = getattr(af, name)
    assert obj is getattr(importlib.import_module(af.MOVED[name]), name)


def test_from_import_still_works():
    with pytest.warns(DeprecationWarning):
        from callbacks.allFunctions import plotImage
    from callbacks.plotting import plotImage as real
    assert plotImage is real


def test_appclass_names_served():
    with pytest.warns(DeprecationWarning, match="callbacks.appClass"):
        D = af.D
    from callbacks.appClass import D as real
    assert D is real


def test_unknown_name():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        with pytest.raises(AttributeError):
            af.no_such_function
        with pytest.raises(AttributeError):
            af._private


def test_nothing_in_the_package_imports_it():
    """Internal code imports from the real modules; the alias table is only for outside users."""
    users = [str(p.relative_to(SRC)) for p in SRC.rglob("*.py")
             if p.name != "allFunctions.py" and "allFunctions" in p.read_text(encoding="utf-8")]
    assert not users, f"import from the real modules instead: {users}"
