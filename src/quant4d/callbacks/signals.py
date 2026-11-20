"""Exception-safe signal blocking.

Two idioms are used throughout the callbacks when the code sets widget values
programmatically and must not react to its own changes:

* per-widget ``QObject.blockSignals`` -> :func:`signals_blocked`
* the app-wide ``blockAllSignals`` flag that every callback checks on entry
  -> :func:`all_signals_blocked`

Both are context managers, so signals are restored even if the body raises or
returns early, and both restore the *previous* state rather than forcing
``False``, so they nest safely.
"""
from contextlib import contextmanager

__all__ = ["signals_blocked", "all_signals_blocked"]


@contextmanager
def signals_blocked(*widgets):
    """Block Qt signals on *widgets* for the duration of the ``with`` block.

    ``None`` entries are ignored.  Each widget is returned to the blocking
    state it had on entry.
    """
    widgets = [w for w in widgets if w is not None]
    previous = [w.blockSignals(True) for w in widgets]   # blockSignals returns the old state
    try:
        yield
    finally:
        for w, was_blocked in zip(widgets, previous):
            w.blockSignals(was_blocked)


@contextmanager
def all_signals_blocked(app):
    """Set ``app.blockAllSignals`` for the duration of the ``with`` block.

    Callbacks return immediately while the flag is set.  The previous value is
    restored on exit, so an inner block does not unblock an outer one.
    """
    previous = getattr(app, "blockAllSignals", False)
    app.blockAllSignals = True
    try:
        yield
    finally:
        app.blockAllSignals = previous
