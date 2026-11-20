"""
Every global name a callback module uses must exist in that module at runtime.

flake8's F821 cannot see through the ``from callbacks.appClass import *`` star
imports, so a function that calls a helper living in another module passes
lint and then raises NameError the first time it runs.  This test imports each
module and checks every global name its code refers to.
"""
import builtins
import importlib
import pathlib
import symtable

import pytest

_SRC = pathlib.Path(__file__).resolve().parents[2] / "src"
_SKIP = {"pyquant4d.callbacks.moveHist"}          # deliberately raises ImportError (deprecated stub)
_MODULES = sorted(
    ".".join(p.relative_to(_SRC).with_suffix("").parts)
    for pkg in ("callbacks", "annotationsClasses")
    for p in (_SRC / "pyquant4d" / pkg).rglob("*.py")
    if p.name != "__init__.py"
)
assert _MODULES, "no modules found: has the package moved?"


def _global_refs(table, out):
    for sym in table.get_symbols():
        if sym.is_referenced() and (sym.is_global() or table.get_type() == "module"):
            out.add(sym.get_name())
    for child in table.get_children():
        _global_refs(child, out)


@pytest.mark.parametrize("modname", [m for m in _MODULES if m not in _SKIP])
def test_no_undefined_globals(qapp, modname):
    mod = importlib.import_module(modname)
    path = pathlib.Path(mod.__file__)
    top = symtable.symtable(path.read_text(encoding="utf-8"), str(path), "exec")

    used = set()
    _global_refs(top, used)
    # names bound somewhere at module level (e.g. under ``if __name__ == "__main__"``
    # or in a guarded optional import) count as defined
    bound = {s.get_name() for s in top.get_symbols() if s.is_assigned() or s.is_imported()}

    missing = sorted(
        n for n in used
        if n not in bound and not hasattr(mod, n) and not hasattr(builtins, n)
    )
    assert not missing, f"{modname} uses undefined global name(s): {missing}"
