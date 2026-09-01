# Chromatic number of PG(7,2) — is χ₂(8) = 5 or 6?

**Statement.** χ_q(n) is the minimum number of colors for the points of the
projective space PG(n−1,q) such that no line is monochromatic. For q = 2
this is: partition F₂ⁿ ∖ {0} into color classes containing no triple
{x, y, x⊕y} — i.e. into *sum-free sets*. Bishnoi–Cames van Batenburg–Ravi
(arXiv:2512.01760, v3 2026-05-24) determine χ₂(n) = 2,3,3,4,5,5 for
n = 2..7 and pose as **Problem 1**: *determine whether χ₂(8) = 5 or 6*.
χ₂(8) = 5 would give the multicolor Ramsey bound R(3;5) ≥ 257 (known:
162 ≤ R(3;5) ≤ 307, as cited in their §6.1).

**Status.** Open; χ₂(8) ∈ {5, 6}. This session (2026-09-01): every proper
5-coloring of PG(7,2), if one exists, has severely restricted symmetry.

| result | label | where |
|---|---|---|
| No proper k-coloring of any PG(n−1,2) is invariant under a collineation of order 3, 7, 31, or 127 (Mersenne-prime orders: an irreducible invariant subspace is a single orbit and contains lines) | PROVED | NOTE Lemma B |
| Every class of a 5-coloring of PG(7,2) meets every hyperplane; every hyperplane restriction is a 5-coloring of PG(6,2) using all 5 colors; no class fits in an affine hyperplane | PROVED | NOTE Lemma A |
| No 5-coloring of PG(7,2) is invariant under any order-17 element (all order-17 subgroups are conjugate; contracted instance UNSAT) | CERTIFIED (DRUP verified) | `certs/ord17.{cnf,drup}` |
| No 5-coloring of PG(7,2) is invariant under the Frobenius x ↦ x² of F₂₅₆ | CERTIFIED (DRUP verified) | `certs/frob.{cnf,drup}` |
| Order-5 elements (two conjugacy classes [C,C], [C,I]) — the only odd prime order left by Lemma B; **UNSAT would make every witness's automorphism group a 2-group** | RUNNING at session close — see `data/ord5_status.md` | `gen_order5.py` |
| PG(6,2) *does* admit an order-5-invariant 5-coloring, class sizes [21,21,25,27,33]; the invariant family is large (≥ 10⁵ raw cell-colorings) | CERTIFIED (witness re-verified from definition) | `data/witness_n7_ord5.txt` |
| No 5-coloring of PG(7,2) invariant under any of 24 block-diagonal Singer/twisted/swap subgroups (20 DEAD: an orbit contains a line; order-5-related cases are the pending ones above) nor under multiplicative subgroups of orders 3, 15, 17, 51, 85, 255 (DEAD: e.g. F₄*-cosets are lines) | CERTIFIED (DEAD cells exact; UNSAT cells solver-decided, order-17/Frobenius DRUP-verified) | `ansatz.py`, `matrix_ansatz.py` |
| 1,000 randomized χ₂(7) witnesses: 1,000 distinct fingerprints, none extends over a hyperplane to a χ₂(8) witness; the order-5-symmetric witness does not extend either | NUMERICAL (each non-extension is a solver-decided UNSAT; sampling is solver-biased) | `sample_extend.py`, `data/sample1000_summary.txt` |
| Extension bottleneck is packing, not capacity: per-class Hoffman bounds (exact integer spectra) sum to ≈ 265–274 vs 128 needed | NUMERICAL | `alpha_fourier.py` |
| Published table χ₂(2..7) = 2,3,3,4,5,5 reproduced end-to-end (SAT witnesses re-verified; small UNSATs solver-decided; (6,4)/(7,4) from R(3;4) ≤ 62 as in the paper) | control | `satdec.py` |
| Local search: min-conflicts stalls at 1 mono line even at n = 7; breakout weighting cracks n = 7 in ~5×10³ flips but n = 8 yields nothing in ≈ 5×10⁹ flips (estimated; counters lost at retirement) | NUMERICAL | `mincon.c` |

## Scripts

| file | what it does | cost |
|---|---|---|
| `lines.py` | line generator {x,y,x⊕y} + from-definition coloring checker; counts cross-checked vs (2ⁿ−1)(2ⁿ−2)/6 = OEIS A006095 | instant |
| `verify_witness.py` | standalone witness verifier (`python3 verify_witness.py data/witness_n7_ord5.txt 7`) | instant |
| `satdec.py` | SAT decision χ₂(n) ≤ k; emits DIMACS with `--dimacs` | n ≤ 7 seconds; (8,5) does not terminate in hours |
| `ansatz.py` | ΓL(1,256)-subgroup invariant sweep: orbit contraction → SAT | seconds per strongly-contracted cell |
| `matrix_ansatz.py` | same for block-diagonal GL(8,2) subgroups (conflict-budgeted) | ~10 min sweep |
| `gen_order5.py` | emits the five certification instances (`ord5_CC/ord5_CI/ord17/frob/n7_ord5.cnf`) | instant |
| `certify.py` | Glucose42 + DRUP + `rup_check` pipeline (`gcc -O2 -o rup_check ../../tools/satcert/rup_check.c`) | ord17/frob < 1 s |
| `sample_extend.py` | randomized-CDCL χ₂(7) witness sampler (needs `kissat` in PATH or `$KISSAT`) + hyperplane extension SAT | ~1.5 s/sample |
| `alpha_fourier.py` | exact Walsh–Hadamard spectra + Hoffman bounds per class | ~10 s/witness |
| `lift_n7_ord5.py` | solves + lifts + verifies the order-5-invariant n=7 witness | seconds |
| `mincon.c` | min-conflicts/breakout local search (`gcc -O3 -o mincon mincon.c; ./mincon 8 5 SEED 1 3600 5`) | as budgeted |
| `audit_contraction.py` | independent rebuild of all four certification instances (cycle-walk orbits, exact linear-algebra class checks) — clause sets must match byte-for-byte | seconds |
| `gen_combined.py` | emits `combined_ord5_ext.cnf`: does any witness restrict on a hyperplane to an order-5-invariant coloring? (UNSAT ⇒ no witness has a symmetric hyperplane shadow) | instant |

Reproduce the certified exclusions (from inside this directory):

```bash
gcc -O2 -o rup_check ../../tools/satcert/rup_check.c
python3 gen_order5.py
python3 certify.py ord17.cnf frob.cnf        # UNSAT + "s VERIFIED" twice
python3 lift_n7_ord5.py                      # order-5-invariant n=7 witness
python3 verify_witness.py data/witness_n7_ord5.txt 7
```

Environment used: 4 cores, 15 GB RAM, Python 3.11, kissat 4.0.4,
python-sat (Cadical195/Glucose42); seeds are in the scripts/outputs.

## Known defects / open ends

- The order-5 UNSAT runs ([C,C] 255 vars, [C,I] 315 vars) had not
  terminated at session close; `data/ord5_status.md` carries the final
  word. Until both land, the 2-group theorem is conditional.
- σ² and σ⁴ (Frobenius powers, 2-elements) and the GL(8,2) involution
  classes are undecided — the sweep certifies odd symmetry only.
- The 1,000-witness extension experiment is solver-biased sampling, not
  uniform; its non-extension UNSATs are solver verdicts (no DRUP logs
  kept). Certifying a subsample is cheap if ever needed.
- kissat proofs for the order-5 instances are DRAT and may contain RAT
  steps `rup_check` rejects; `drat-trim` is the fallback checker
  (documented in NOTE §5).

Write-up page: to be linked from the top-level README once published
(`PAGE.md` is the handoff).
