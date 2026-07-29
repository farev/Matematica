"""Cheap smoke tests — guard against refactors breaking the certified pipeline.

These run the scripts the way they are meant to be run: as subprocesses, from
inside their own conjecture directory, since they resolve data files by bare
relative name. Only the fast tier runs here. The expensive computations (the
10^10 verification, exact c_6) are manual; see each conjecture's README.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GILBREATH = REPO / "conjectures" / "gilbreath"


def run(script, *args, cwd):
    result = subprocess.run(
        [sys.executable, script, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, f"{script} exited {result.returncode}:\n{result.stderr}"
    return result.stdout


def test_gilbreath_verify_small():
    """Gilbreath holds for primes below 10^6, via the propagation criterion."""
    out = run("verify.py", "1e6", cwd=GILBREATH)
    assert "GILBREATH'S CONJECTURE IS FALSE" not in out
    assert "Gilbreath's conjecture holds for the first" in out
    assert "tail of length" in out, "propagation criterion never fired"


def test_gilbreath_explore_runs():
    """The small-scale triangle builder still runs."""
    out = run("explore.py", cwd=GILBREATH)
    assert "d^1" in out


def test_certificate_present():
    """The certified c_6 value is committed and is an exact rational."""
    cert = (GILBREATH / "c6_certified.txt").read_text().strip()
    num, _, den = cert.partition("/")
    assert num.isdigit() and den.isdigit(), "c6 certificate is not a rational"
    assert 0.4483 < int(num) / int(den) < 0.4484, "c6 outside expected range"
