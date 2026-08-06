# satcert — certified-UNSAT toolkit (SAT results with checkable proofs)

Built 2026-08-05 while scoping a Rado-number candidate that was ultimately
not selected; kept because it closes a recorded defect class (2026-08-03:
SAT UNSAT verdicts with no checked proof) for any future SAT-shaped session.

| file | what it is |
|---|---|
| `rup_check.c` | forward DRUP (reverse-unit-propagation) proof checker, written from the definition, no code shared with any solver. `gcc -O2 -o rup_check rup_check.c`; usage `rup_check <cnf> <drup>`; exit 0 + "s VERIFIED" iff the proof derives the empty clause with every step RUP. Honors `d` deletion lines (unit deletions ignored — sound). |
| `check_coloring.c` | independent verifier for Rado/Schur lower-bound witnesses: enumerates ALL solution tuples of a linear equation over {1..n} by nested loops (deliberately not the encoder's method) and checks no monochromatic one. Reads header `n k m const mode`, coefficients, colors from stdin. |
| `rado.py` | encoder + driver for k-color Rado numbers of `sum a_i x_i + c = 0` (conventions: all / not_all_equal / distinct solutions). `rado_fast()` = exponential climb + bisection with Cadical, then boundary-only certification: SAT witness at R−1 (export to `check_coloring`), Glucose42 DRUP proof at R checked by `rup_check`. Requires python-sat; compile the two C tools alongside. |

## Validation record (2026-08-05, 4 cores)

- `rup_check`: verifies a genuine Glucose42 proof of PHP(6,5) UNSAT
  (260 proof lines); **rejects** an injected non-RUP clause ("FAIL line 1")
  and a truncated proof. Witness checker rejects a monochromatic coloring.
- Calibration battery (0.09 s, every UNSAT step proof-checked):
  R₂(x+y=z)=5, R₃(x+y=z)=14, R₂(x+y=2z, not-all-equal)=9 (=W(2;3)),
  R₃(x−y=z)=14.
- End-to-end at the next tier: **R₄(x+y=z) = 45** (classical; Schur number
  44 + 1) — witness at 44 verified independently (85184 tuples enumerated,
  946 solutions, none monochromatic), UNSAT at 45 with DRUP proof
  RUP-VERIFIED. 28.5 min wall, dominated by the proof-logged Glucose solve.

Caveat: Glucose42's DRUP output is pure RUP in these runs; a solver with
inprocessing (e.g. CaDiCaL) may emit RAT steps `rup_check` would reject —
use Glucose for the proof-logged boundary run, as `rado.py` does.
