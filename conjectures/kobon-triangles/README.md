# Kobon triangles: simple arrangements of 18 pseudolines (Bartholdi–Blanc–Loisel, 2008)

How many bounded triangular faces can `n` lines (or pseudolines) in general position cut
out of the plane? Bartholdi, Blanc and Loisel proved `⌊n(n − 7/3)/3⌋` is an upper bound
for even `n` and computed the exact simple-pseudoline maximum `a^s_3(n)` for every
`n ≤ 17`; their Theorem 1.4 leaves `n = 18` as the first undecided entry, `93 ≤ a^s_3(18)
≤ 94`, because their 2007 depth-first search could not handle six unused segments. The
fault line: at `n = 18` the bound is an integer, so 94 triangles is the equality case of
their own counting argument, which forces a rigid structure (twelve perfect lines, six
lines with one unused segment each) that a SAT solver can exploit through
cube-and-conquer over dihedral orbits.

Page: *(none yet — see PAGE.md if present)*.

**Status:** active
**Sessions:** 2026-09-02

## Results

| Claim | Label | Where |
|---|---|---|
| **Rediscovery, marked as such.** `a^s_3(18) = 93`: no simple arrangement of 18 pseudolines (hence no 18 lines in general position) has 94 triangular faces — the "93–94" entry of BBL Theorem 1.4 — decided by 561 dihedral-orbit cubes with `drat-trim`-checked DRAT proofs **[numbers pending]**. Found mid-session to be a theorem of Blanc (2008/2011, Theorem 1 + Theorem 3), by a different method. | CERTIFIED (confirmation of known) | NOTE §7, `data/cubes_T2.csv` |
| Audit: OEIS A006066's upper bounds for even `n` (94 at 18, 54 at 14) are simple-arrangement theorems applied to a problem whose records use triple points; the general bound in the cited literature is Clément–Bader's 95 / 55 | flagged (secondary sources checked) | NOTE §9 |
| The signotope model, the segment reformulation, the equality-case structure (T1, T2) at `n = 18`, and the order-`4n` symmetry group (NOTE §§2–5) | PROVED | `NOTE.md` |
| Encodings reproduce every value of BBL Theorem 1.4 for `n ≤ 16` (SAT at the value, decoded and re-counted; UNSAT one above for `n = 8, 10, 11, 12`) and A006245 for `n ≤ 7` | CERTIFIED | `data/ctrl*.log`, `data/lemma_even.log` |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md) for the
session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `kobon_sat.py` | v1 encoding (signotope + triangle count); decoding and independent triangle counters (`analyse`) | seconds | DIMACS; used for counts and checks |
| `kobon_sat2.py` | v2 segment-budget encoding, `--tight` equality-case clauses (n = 18 only), dihedral lex-leader | seconds to build | DIMACS for `n, t` |
| `kobon_sym.py` | the shift/mirror maps; `validate()` checks all `4n` symmetries on every arrangement, `n ≤ 7` | 1 min | orbit histograms |
| `controls.py`, `controls2.py` | positive/negative controls against BBL Thm 1.4 and A006245 | minutes (n ≤ 13), hours (n = 14, 16) | `data/ctrl*.log` |
| `bbl_check.py` | checks the BBL association lemma on decoded arrangements | seconds | `data/lemma_even.log` |
| `cubes.py` | `gen`: 561 `D_18`-orbit cubes of the tight instance; `run K0 K1 kissat proofs [reverse]` | see NOTE §7 | `cubes/run_*.out`, DRAT proofs |
| `verify_cubes.py`, `verify_finished.py` | `drat-trim` verification of every cube proof, with hashes | ~solve time | `cubes/verified.log` |

Run from inside this directory (needs `python-sat`; `kissat`, `cadical` and `drat-trim`
on `PATH` or via the `KISSAT` environment variable):

```bash
cd conjectures/kobon-triangles
python3 controls.py count                 # A006245 counts n = 4..7
python3 controls2.py cases 11@33,12@38    # UNSAT controls
python3 cubes.py gen && python3 cubes.py run 0 561 kissat proofs
python3 verify_finished.py cubes
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/ctrl_3_12.log`, `data/ctrl_13_16.log` | `controls.py` | v1 controls (v1 is weak on UNSAT; kept for the record) |
| `data/ctrl2_unsat.log`, `data/ctrl2_sat.log` | `controls2.py` | v2 controls vs BBL Theorem 1.4 |
| `data/lemma_even.log` | `bbl_check.py` | association lemma: 0 violations on all 908 arrangements at n = 6 and 30,000 at n = 8 |
| **[PENDING: cube index, run logs, verified.log with SHA-256 of every DRAT proof]** | `cubes.py`, `verify_finished.py` | |

## Known defects and open threads

- The result is for *simple* arrangements (pseudolines, hence also straight lines in
  general position). The Kobon number `K(18)` allows concurrent triples and parallels,
  which are known to matter at `n = 14`; deciding `K(18)` needs a model of non-simple
  arrangements (Savchuk's table notation supports them).
- The equality-case clauses (T1, T2) are derived from BBL's published Lemma; the
  derivation is in NOTE §4 and was checked computationally where it applies, but the
  certificate depends on it. A lemma-free certificate (plain cubes) is the first thing a
  follow-up session should finish.
- `n = 20` (`116–117`), `22`, `24`, … are the same shape but not the equality case; the
  general tool for them is the segment encoding plus cubes on the imperfect-line set with
  `|S|` ranging over the counting bounds.

## Prior work

- N. Bartholdi, J. Blanc, S. Loisel, Contemp. Math. 453 (2008), arXiv:0706.0723 —
  the bound, the table, the DFS. Read today.
- S. Felsner, H. Weil, Discrete Appl. Math. 109 (2001) — signotopes ↔ simple
  Euclidean pseudoline arrangements. Read today (damaged text layer).
- P. Savchuk, arXiv:2507.07951 (2025) — SAT table encoding, odd cases, straightening.
  Read today.
- R. Parpalak, D. Utkin, arXiv:2604.22035 (2026); A. Maiorana (OEIS A006066, 2026);
  A. Zarzuelo Urdiales (2026, even lower bounds; (secondary), not read).
- OEIS A006066, A006245, A032765.
