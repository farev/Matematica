# Ordinary lines of 15 points (Sylvester's problem, OEIS A003034; Dirac–Motzkin conjecture)

For n points in the real plane, not all on a line, t₂(n) is the least possible number of
*ordinary lines* — lines through exactly two of the points. Melchior (1940) gave t₂ ≥ 3,
Kelly–Moser (1958) 3n/7, Csima–Sawyer (1993) 6n/13; Green and Tao (2013) proved the
Dirac–Motzkin conjecture t₂(n) ≥ n/2 for all n ≥ n₀ with n₀ unspecified ("double
exponential type"), remarking that n₀ = 14 may be the truth since only n = 7 and n = 13
are known to break the bound. Exact values are recorded for n ≤ 14 and for n = 16, 18, 22
(A003034); at n = 15 only 7 ≤ t₂(15) ≤ 9 was known. This session attacks n = 15 — the
smallest open case — by SAT over rank-3 chirotopes with collinearities, split along the
line-type distribution that Melchior's inequality forces. It looked tractable because
the forced distribution for seven ordinary lines is a single rigid shape (two 5-point
lines, twenty-six 3-point lines). Half of it was.

**Write-up page:** *(pending — see PAGE.md; the result is partial and the page must say so)*

**Status:** active — the meeting case of cube A (45 sub-cases) is open
**Sessions:** 2026-09-05

## Results

| Claim | Label | Where |
|---|---|---|
| **Theorem 6.1.** No 15-point set in RP² (and no rank-3 oriented matroid / pseudoline arrangement) spans exactly 7 ordinary lines with its two 5-point lines *disjoint*: all 261 sub-cubes of the disjoint case are UNSAT with drat-trim-verified DRAT proofs (2 472 s solving, 2 480 s checking, 6.3 GB of proofs, 55 min wall on 2 cores). | CERTIFIED | NOTE §6, `certs/ledger_B_m7.jsonl` |
| **Theorem 6.2.** Nor with the two 5-point lines *meeting* and no ordinary line among the 16 pairs joining them: all 411 arrays of that sub-case UNSAT, verified (1 212 s solving, 45 min on 1 core). | CERTIFIED | NOTE §6, `certs/ledger_A_m7_class0_fill.jsonl` |
| **Corollary 5.3.** A 15-point set with t₂ ≤ 7 has t₂ = 7, exactly two 5-point lines, twenty-six 3-point lines and no other line of size ≥ 4 (Melchior + pair counting; the sub-7 shapes are those excluded by Kelly–Moser/Csima–Sawyer). | PROVED | NOTE §5 |
| **Lemma 5.6.** In the disjoint case at most 6 of the 25 cross pairs are ordinary; in the meeting case between 1 (Thm 6.2) and 5 of the 16; every point lies on an even number of ordinary lines. | PROVED | NOTE §5 |
| **Proposition 6.3.** The 83 meeting-case sub-classes with ≥ 6 ordinary cross pairs are void by parity and were machine-checked (83 UNSAT, verified); the two smallest open classes (70 arrays each) were closed in fill mode (140 UNSAT, verified). | PROVED + CERTIFIED | NOTE §6, `certs/ledger_A_void.jsonl`, `certs/ledger_A_m7_class{11,22}_fill.jsonl` |
| **Corollary 6.4.** The Dirac–Motzkin bound t₂(15) ≥ 8 is equivalent to the unsatisfiability of the 45 remaining ∗-classes of the meeting case (151 309 arrays). **Not established.** | reduction, PROVED | NOTE §6 |
| Soundness of the whole pipeline needs only the alternating/simple/three-term Grassmann–Plücker conditions, which every real configuration and every oriented matroid satisfies (no completeness theorem is used); positive controls: an explicit rational two-5-line configuration is SAT in its own sub-cube, models pass an independent full-axiom check. | PROVED | NOTE §3–5, `poscontrol.py`, `verify_chirotope.py` |
| Calibration: the method reproduces t₂(9..12) on the refutation side (n = 10, 11 by counting alone; n = 9 in 25 ms; n = 12 in 18.5 s) and finds the known configurations on the SAT side. | CERTIFIED | `certs/calibration_n9_12.log` |
| t₂(20) = 10 and t₂(24) = 12 follow from Csima–Sawyer + Böröczky; the "?" at n = 20 in the A003034 comment is a gap in the quoted table, not an open case. | PROVED (from literature, secondary) | NOTE §2 |
| The remaining 45 sub-cases resist every split tried (sub-cubes, type vectors, parity, one-symbol fixing, both solvers; incremental fill mode measured at 0.6–0.9 s per array, i.e. ~25 CPU-hours). | NUMERICAL (cost measurements) | NOTE §7 |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `ordlines_sat.py` | encoder: rank-3 chirotope axioms (alternation, simplicity, transitivity, three-term Grassmann–Plücker sign relations), ordinary-pair indicators, cardinality ≤ m, optional prescribed lines of size ≥ 4; DIMACS export; model decoder | `python3 ordlines_sat.py 15 7 --big 0,1,2,3,4 --big 5,6,7,8,9 --out x.cnf`: 1 s | 91 791 variables, 655 533 clauses per n = 15 cube |
| `distributions.py` | line-type distributions (t_k) compatible with pair counting and Melchior's inequality | `python3 distributions.py 15 8`: instant | t₂ = 7 forces {t₅ = 2, t₃ = 26}; t₂ = 8 admits six shapes |
| `cubes.py` | non-isomorphic placements of the lines of size ≥ 4 (partial linear spaces; canonical form = multiset of point-incidence vectors minimised over line permutations) | `python3 cubes.py 15 7`: instant; `15 8`: 1 min | 2 cubes at t₂ = 7, 41 at t₂ = 8 |
| `subcubes.py` | the two t₂ = 7 cubes split by the ∗-pattern of the free-point array (up to row/column permutations) with value precedence, plus the two Latin squares of order 5 for the ∗-free disjoint case; runs Kissat with DRAT logging and drat-trim on every sub-cube; JSONL ledger | `python3 subcubes.py B 7 --jobs 2`: 55 min | 261/261 UNSAT verified (Theorem 6.1) |
| `fillcubes.py` | "fill mode": all fillings of one ∗-class up to Aut(S) × relabelling, each run as its own instance | `python3 fillcubes.py A 7 0`: 45 min (411 fillings); `--count` to size a class | 411/411 UNSAT verified (Theorem 6.2) |
| `typecubes.py` | type-vector refinement (Lemma 5.6): exact counts of RFF/CFF/FFF/qFF lines, exact ordinary sub-counts, per-point parity | `--dry` lists 184 (B) / 149 (A) instances | void classes; not faster on cube A |
| `certify.py` | whole-cube driver (calibration ladder and the t₂ = 8 cubes) | varies | `certs/calibration_n9_12.log` |
| `verify_chirotope.py` | independent check of any satisfying assignment: simplicity, linear space, general chirotope axiom (B2) over all n⁶ tuple pairs, 3-term relations, line-type distribution — no code shared with the encoder | 1 s at n = 9 | used on every SAT model |
| `poscontrol.py` | positive control: explicit rational two-5-line configuration → its canonical sub-cube must be SAT | 5 s | SAT in 0.3 s, 0 violated clauses |
| `lexcubes.py` | alternative symmetry breaking (double-lex + value precedence, soundness proved in NOTE §7); slower; kept as a record | not used for results | — |
| `chiro_sat.py` | first prototype and the numeric self-check of the Grassmann–Plücker identity | `python3 chiro_sat.py`: seconds | reproduces t₂(5..8) = 4, 3, 3, 4 |

Run from inside this directory; `kissat` and `drat-trim` must be on `PATH`
(or set `KISSAT`, `DRATTRIM`); Python 3.11 with `python-sat`.

```bash
cd conjectures/ordinary-lines
python3 distributions.py 15 7 && python3 cubes.py 15 7
python3 subcubes.py B 7 --jobs 2          # Theorem 6.1: 261 sub-cubes, ~55 min on 2 cores
python3 fillcubes.py A 7 0 --jobs 1       # Theorem 6.2: 411 fillings, ~45 min
python3 fillcubes.py A 7 1 --count        # sizes the first open class: 3268 fillings
python3 poscontrol.py                      # positive control
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `certs/ledger_B_m7.jsonl` | `subcubes.py B 7` | one line per sub-cube of cube B: ∗-pattern, Latin square if any, SHA-256 of the regenerable CNF, Kissat verdict and time, proof size, drat-trim verdict and time |
| `certs/ledger_A_m7_class0_fill.jsonl` | `fillcubes.py A 7 0` | the same for the 411 fillings of cube A's ∗-free class |
| `certs/ledger_A_void.jsonl` | `subcubes.py A 7 --only 48..130` | the 83 ∗-classes of cube A that Lemma 5.6 shows void, run anyway (83 UNSAT, verified) |
| `certs/ledger_A_m7_class11_fill.jsonl`, `…class22_fill.jsonl` | `fillcubes.py A 7 11`, `… 22` | the two 70-array classes of the meeting case (140 UNSAT, verified) |
| `certs/calibration_n9_12.log` | `calib2.py` (scratch driver over `certify`-style cubes) | refutation and positive controls for n = 9..12 |

Proof files (6.3 GB for cube B, 13.1 GB for cube A class 0) were checked and deleted; they
are regenerated deterministically by the scripts. No random seeds are involved.

## Known defects and open threads

- **The meeting case (cube A, 1 ≤ s ≤ 5, 45 ∗-classes, 151 309 arrays) is open**, so t₂(15) ≥ 8 is not
  proved here. Measured cost about 25 CPU-hours in incremental fill mode; a better split is
  wanted (NOTE §9.1).
- The claim for pseudolines rests on two cited theorems not re-read today (Melchior for
  pseudolines; the topological representation theorem) — both marked (secondary).
- The sub-7 shapes of Corollary 5.3 were not machine-checked; they are excluded by
  Kelly–Moser (secondary). The n = 13 and n = 14 refutation controls did not finish in the
  session (single-5-line cubes).
- Kissat's DRAT output was checked by drat-trim only; the repository's own `rup_check` was
  not used (Kissat emits RAT steps).

## Prior work

* E. Melchior, Über Vielseite der projektiven Ebene, Deutsche Math. 5 (1940) — t₂ ≥ 3 and the
  inequality used for the case split (secondary; via Green–Tao §3).
* L. M. Kelly, W. O. J. Moser, Canad. J. Math. 10 (1958) 210–219 — t₂ ≥ 3n/7 (secondary).
* J. Csima, E. T. Sawyer, Discrete Comput. Geom. 9 (1993) 187–202 — t₂ ≥ 6n/13, n > 7
  (secondary; via Green–Tao and A003034).
* D. W. Crowe, T. A. McKee, Math. Mag. 41 (1968) — the 13-point configuration with 6 ordinary
  lines and small-n values (secondary).
* B. Green, T. Tao, On sets defining few ordinary lines, Discrete Comput. Geom. 50 (2013),
  arXiv:1208.4714 — Dirac–Motzkin for n ≥ n₀, Böröczky examples, sharp threshold f(n) (read).
* OEIS A003034 (Sylvester's problem), revision #27, 30 May 2026 — the table with "?" at n = 15.
* J. Bokowski, P. Pokora, Period. Math. Hungar. 77 (2018), arXiv:1607.05864 — Melchior for
  pseudolines; classification of 12-pseudoline arrangements with 19 triple points (abstract read).
* M. Scheucher and co-authors — SAT over (uniform) chirotopes with DRAT certificates in
  combinatorial geometry (arXiv:2105.08406 and later); the encoding style used here.
