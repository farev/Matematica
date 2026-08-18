# vdw-mixed — certificates for mixed van der Waerden numbers, and the w(2;5,8) frontier

**Problem.** The mixed two-color van der Waerden number `w(2;s,t)` is the
least `n` such that every 2-coloring of `{1,…,n}` contains a monochromatic
`s`-term arithmetic progression in color 0 or a monochromatic `t`-term AP in
color 1. Exact values are known only for a small table (Landman–Robertson;
Ahmed's computations 2009–2013 (secondary)); the row `w(2;5,t)` ends at
`w(2;5,7) = 260` (Ahmed 2013, J. Integer Seq. 16, art. 13.4.4 (secondary)),
and **`w(2;5,8)` is open** as far as every source reachable this session
shows. None of the published exact values ship machine-checkable proofs —
they predate DRUP/DRAT certificate practice.

**This directory** re-derives the table with certificates (witness at `w−1`
independently verified + DRUP-checked UNSAT at `w`, which by restriction
monotonicity pins the value), and opens a certified campaign on `w(2;5,8)`.

**Write-up page:** [fabianarevalo.com/vdw-mixed](https://fabianarevalo.com/vdw-mixed)

## Status (2026-08-16, session 1 — in progress)

| cell | published (secondary) | this repo | certificate |
|---|---|---|---|
| w(2;3,5) | 22 | **22 CERTIFIED** | witness + RUP-verified UNSAT |
| w(2;3,6) | 32 | **32 CERTIFIED** | witness + RUP-verified UNSAT |
| w(2;4,4) | 35 | **35 CERTIFIED** | witness + RUP-verified UNSAT |
| w(2;4,5) | 55 | **55 CERTIFIED** | witness + RUP-verified UNSAT |
| w(2;4,6) | 73 | **73 CERTIFIED** | witness + RUP-verified UNSAT (also closed by the validated cube-and-conquer driver, 64/64 leaves) |
| w(2;5,5) | 178 | **178 CERTIFIED** | witness + RUP-verified UNSAT (1.56M-line proof) |
| w(2;4,7) | 109 | **109 CERTIFIED** | witness + RUP-verified UNSAT (18.4M-line proof; sha256 + verdict in MANIFEST, file re-derivable) |
| w(2;5,6) | 206 | both legs in flight | pending |
| w(2;5,7) | 260 | planned (stretch) | pending |
| w(2;5,8) | — (open) | **> 295 CERTIFIED** (exactly-74-periodic witness at n=295, both verifiers; escalation running) | witness committed |

## Scripts

| file | what it does |
|---|---|
| `vdw_cnf.py` | CNF encoder + AP-count self-check + brute-force ground truth for tiny cells + independent witness verifier (`coloring_is_good`) |
| `solve_cell.py` | per-cell driver: cadical fast path, Glucose42+DRUP cert path, boundary certification (`cert s t w`), warm-start phases |
| `cnc.py` | resumable cube-and-conquer UNSAT campaigns: adaptive splitting, per-leaf DRUP checked at production, append-only CSV state |
| `periodic_sat.py` | complete per-period search for exactly-periodic witnesses (projection onto block variables) |
| `periodic_defect_sat.py` | complete search for `p`-periodic witnesses with ≤ k defects (XOR + sequential counter) |
| `periodic_search.py` | incomplete periodic-block tabu (numpy full-string cost); kept for seed generation |
| `witness_search.py` | free-bit tabu with violated-AP moves; kept honest: failed its positive controls, see WRITEUP |
| `manifest.py` | append a certificate row (sha256, size, verdict) to `certs/MANIFEST.csv` |

Certificates: small DRUP proofs are committed in `certs/`; proofs above the
repo's ~10 MB rule are excluded by `certs/.gitignore`, recorded in
`certs/MANIFEST.csv` with sha256 + checker verdict, and re-derivable by
`solve_cell.py`. The checker is `tools/satcert/rup_check` (compile with
`gcc -O2`; from-definition forward RUP, no solver code shared).

## Reproduction

```bash
cd conjectures/vdw-mixed
pip install python-sat numpy
gcc -O2 -o ../../tools/satcert/rup_check ../../tools/satcert/rup_check.c
python3 vdw_cnf.py                      # encoder self-checks + brute controls
python3 solve_cell.py cert 4 6 73       # example: full boundary certification
python3 cnc.py 4 6 73 6 20000 4        # example: cube-and-conquer campaign
```

## Known defects / caveats

- Every literature citation this session is **(secondary)** — the egress
  proxy blocked all primary sources (see the session log for the list); the
  openness of w(2;5,8) rests on absence from every reachable snippet plus
  the 2013 frontier, and an unreadable BOINC lower-bounds project is noted
  as residual risk.
- w(2;4,9)'s published status could not be pinned down at all; treated as
  unknown, not attacked.
