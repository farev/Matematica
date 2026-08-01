"""Smoke tests for the NumPy-free Chowla coverage tooling.

These deliberately use neither NumPy nor the network, because the point of the
tooling is that it runs on a bare machine. The C sieve is compiled here rather
than assumed to be built.

Reference values are the committed first-occurrence numbers N_k (the smallest
window start index by which every one of the 2^k sign patterns of length k has
appeared in the Liouville function), with the last-completing pattern code.
They come from data/fineA_coverage.csv and are independently reproduced below
by two implementations.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
CHOWLA = REPO / "conjectures" / "chowla"

# k: (N_k, last_pattern_code) -- see data/fineA_coverage.csv
REFERENCE = {
    1: (2, 1), 2: (9, 0), 3: (14, 0), 4: (33, 0), 5: (122, 12),
    6: (347, 5), 7: (571, 89), 8: (1141, 44), 9: (2659, 467),
    10: (6277, 907), 11: (15848, 265), 12: (47815, 1907),
}


def test_verify_coverage_small_matches_committed_table():
    """Pure-Python trial division reproduces N_k for k = 1..12."""
    out = subprocess.run(
        [sys.executable, "verify_coverage.py", "small", "60000"],
        cwd=CHOWLA, capture_output=True, text=True, timeout=600,
    )
    assert out.returncode == 0, out.stderr
    got = {}
    for line in out.stdout.splitlines():
        parts = line.strip().split(",")
        if len(parts) == 3 and parts[0].isdigit():
            got[int(parts[0])] = (int(parts[1]), int(parts[2]))
    for k in range(1, 13):
        assert got[k] == REFERENCE[k], f"k={k}: got {got.get(k)}, want {REFERENCE[k]}"


@pytest.mark.skipif(shutil.which("cc") is None, reason="no C compiler")
def test_c_sieve_matches_committed_table(tmp_path):
    """The C sieve agrees with the committed table and with trial division."""
    exe = tmp_path / "lambda_coverage"
    build = subprocess.run(
        ["cc", "-O2", "-fopenmp", "-o", str(exe), "lambda_coverage.c"],
        cwd=CHOWLA, capture_output=True, text=True, timeout=300,
    )
    if build.returncode != 0:            # some toolchains ship without OpenMP
        build = subprocess.run(
            ["cc", "-O2", "-fopenmp=libomp", "-o", str(exe), "lambda_coverage.c"],
            cwd=CHOWLA, capture_output=True, text=True, timeout=300,
        )
    assert build.returncode == 0, build.stderr

    ks = ",".join(str(k) for k in REFERENCE)
    run = subprocess.run(
        [str(exe), "1e6", ks, str(tmp_path / "t"), "--seg", "65536",
         "--threads", "2", "--lcheck"],
        cwd=CHOWLA, capture_output=True, text=True, timeout=600,
    )
    assert run.returncode == 0, run.stderr

    got = {}
    for line in (tmp_path / "t_coverage.csv").read_text().splitlines():
        parts = line.split(",")
        if len(parts) == 3 and parts[0].isdigit():
            got[int(parts[0])] = (int(parts[1]), int(parts[2]))
    assert got == REFERENCE

    # L(x) at powers of ten: the Liouville summatory function
    assert "# L(10) = 0" in run.stderr
    assert "# L(1000) = -14" in run.stderr
    assert "# L(100000) = -288" in run.stderr


@pytest.mark.skipif(shutil.which("cc") is None, reason="no C compiler")
def test_prng_control_streams_are_decorrelated(tmp_path):
    """Different control seeds must not share a bit density.

    Regression test for the defect found on 2026-08-01: seeding as
    sm64(n ^ seed) only permutes n inside a short block, so every seed produced
    a stream with the same bit multiset and the control ensemble had no
    dispersion at all.
    """
    exe = tmp_path / "lambda_coverage"
    build = subprocess.run(
        ["cc", "-O2", "-fopenmp", "-o", str(exe), "lambda_coverage.c"],
        cwd=CHOWLA, capture_output=True, text=True, timeout=300,
    )
    if build.returncode != 0:
        pytest.skip("no OpenMP")

    sums = []
    for seed in (1, 2, 3, 4):
        run = subprocess.run(
            [str(exe), "1e6", "30", str(tmp_path / f"p{seed}"), "--seg", "65536",
             "--threads", "1", "--prng", str(seed), "--lcheck", "--report", "1e9"],
            cwd=CHOWLA, capture_output=True, text=True, timeout=600,
        )
        assert run.returncode == 0, run.stderr
        for line in run.stderr.splitlines():
            if line.startswith("# L(100000) ="):
                sums.append(int(line.split("=")[1]))
    assert len(sums) == 4
    assert len(set(sums)) == 4, f"control streams share a density: {sums}"


def test_coverage_model_runs_and_reads_the_new_terms():
    out = subprocess.run(
        [sys.executable, "coverage_model.py"],
        cwd=CHOWLA, capture_output=True, text=True, timeout=120,
    )
    assert out.returncode == 0, out.stderr
    assert "43901697682" in out.stdout      # N_31
    assert "99494377311" in out.stdout      # N_32
