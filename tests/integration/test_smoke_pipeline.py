"""
End-to-end smoke test: real file import -> every detector mode -> every ROI
shape -> display settings -> re-import, with numerical checks on the CoM and
virtual-aperture images.

The scenario lives in tests/manual/smoke_pipeline.py so it can also be run by
hand; it needs its own QApplication and exception hook, so it runs in a
subprocess here.
"""
import os
import pathlib
import subprocess
import sys

import pytest

_SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "manual" / "smoke_pipeline.py"


@pytest.mark.slow
def test_smoke_pipeline_is_clean():
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen", PYTHONPATH=os.pathsep.join(p for p in sys.path if p))
    run = subprocess.run([sys.executable, str(_SCRIPT)], env=env, capture_output=True, text=True, timeout=300)
    steps = [line for line in run.stdout.splitlines() if line.startswith(("ok ", "FAIL "))]
    failed = [line for line in steps if line.startswith("FAIL ")]
    assert steps, f"smoke script produced no steps:\n{run.stdout}\n{run.stderr}"
    assert run.returncode == 0 and not failed, f"{len(failed)} step(s) failed:\n{run.stdout}\n{run.stderr[-2000:]}"
