"""Smoke tests for the Erdős–Gyárfás pipeline (conjectures/erdos-gyarfas).

Self-contained: compiles cyclecheck.c with gcc and checks the power-of-2
cycle spectra of graphs whose spectra are known. No nauty, no networkx.
"""

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EG = REPO / "conjectures" / "erdos-gyarfas"

# graph6, expected spectrum (as printed by cyclecheck -p, "-" = none)
KNOWN = [
    ("C~", "4"),                    # K4
    ("IheA@GUAo", "8"),             # Petersen: no C4, has C8
    ("MhEGHC@AI?_PC@_G_", "8"),     # Heawood: girth 6, has C8
    # one of the four Markström graphs (order 24, no C4/C8, has C16),
    # found by hunt.c during the 2026-07-30 session and matched against
    # the census re-derived that day
    ("WO?GB?A_AAoA@g??E??_@?@??@?O?Q@????MB??O?AgAOG?", "16"),
]


def test_cyclecheck_known_spectra(tmp_path):
    binary = tmp_path / "cyclecheck"
    subprocess.run(
        ["gcc", "-O2", "-o", str(binary), str(EG / "cyclecheck.c")],
        check=True, capture_output=True, timeout=120,
    )
    inp = "".join(g6 + "\n" for g6, _ in KNOWN)
    out = subprocess.run(
        [str(binary), "-p"], input=inp, capture_output=True, text=True,
        check=True, timeout=120,
    ).stdout.strip().split("\n")
    assert len(out) == len(KNOWN)
    for (g6, expect), line in zip(KNOWN, out):
        got_g6, got_spec = line.split("\t")
        assert got_g6 == g6
        assert got_spec == expect, f"{g6}: expected {expect}, got {got_spec}"


def test_markstrom_candidate_committed():
    """The {4,8}-free order-24 graph is committed and matches the test vector."""
    g6 = (EG / "data" / "markstrom_candidate_n24.g6").read_text().strip()
    assert g6 == KNOWN[3][0]
