"""Unit tests for callbacks.signals."""
from types import SimpleNamespace

import pytest
from PyQt5 import QtWidgets as qtw

from pyquant4d.callbacks.signals import all_signals_blocked, signals_blocked


def test_signals_blocked_suppresses_and_restores(qapp):
    a, b = qtw.QSpinBox(), qtw.QSpinBox()
    seen = []
    a.valueChanged.connect(seen.append)
    b.valueChanged.connect(seen.append)

    with signals_blocked(a, b, None):       # None entries are ignored
        a.setValue(3)
        b.setValue(4)
        assert a.signalsBlocked() and b.signalsBlocked()
    assert seen == []
    assert not a.signalsBlocked() and not b.signalsBlocked()

    a.setValue(5)
    assert seen == [5]


def test_signals_blocked_restores_on_exception(qapp):
    w = qtw.QSpinBox()
    with pytest.raises(RuntimeError):
        with signals_blocked(w):
            raise RuntimeError("boom")
    assert not w.signalsBlocked()


def test_signals_blocked_keeps_outer_block(qapp):
    w = qtw.QSpinBox()
    with signals_blocked(w):
        with signals_blocked(w):
            pass
        assert w.signalsBlocked(), "inner block must not unblock the outer one"
    assert not w.signalsBlocked()


def test_all_signals_blocked_restores_on_exception_and_early_return():
    app = SimpleNamespace(blockAllSignals=False)

    def early_return():
        with all_signals_blocked(app):
            assert app.blockAllSignals
            return "done"

    assert early_return() == "done" and app.blockAllSignals is False

    with pytest.raises(ValueError):
        with all_signals_blocked(app):
            raise ValueError
    assert app.blockAllSignals is False


def test_all_signals_blocked_nests():
    app = SimpleNamespace(blockAllSignals=False)
    with all_signals_blocked(app):
        with all_signals_blocked(app):
            pass
        assert app.blockAllSignals is True, "inner block must not unblock the outer one"
    assert app.blockAllSignals is False
