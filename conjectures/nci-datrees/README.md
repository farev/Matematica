# Minimal counterexample to the Non-Cancelling-Intersections conjecture (Amarilli–Monet–Suciu 2024; refuted Wilhelm 2026)

The NCI conjecture said every finite lattice admits a *winning dot-algebra
tree*: an expression building P∖{⊤} from the down-sets of nonzero-Möbius
elements by disjoint unions and guarded differences. Wilhelm refuted it on
2026-08-27 (arXiv:2608.27416), non-constructively, with smallest certified
counterexample ≈ 1.00011·10¹⁵ elements, and asked (§9, OP 1): *what is the
smallest lattice with no winning da-tree?* The left-linear variant
(arXiv:2608.19414, 2026-08-19) asks the same. It looked tractable for a
session because a day-old question has no recorded bounds, every lattice
with ≤ 15 elements is reachable by streaming posets from `nauty-genposetg`,
and winnability per lattice is an exact bounded bitmask closure.

**Status:** active
**Sessions:** 2026-08-28

## Results

| Claim | Label | Where |
|---|---|---|
| Every lattice with ≤ 15 elements admits a winning **left-linear** da-tree; hence the minimal counterexample (general, [3] §9 OP1) and the minimal left-linear counterexample ([2] §9 OP1) both have **≥ 16 elements**, and no lattice with ≤ 15 elements separates left-linear from general trees | CERTIFIED | NOTE §4 Thm A; `data/census_summary.tsv` |
| Any counterexample *set family* to the original conjecture has > 15 distinct subfamily intersections (modulo the equivalences proved in [1] §4–5, checked at statement level) | CERTIFIED (modulo cited equivalences) | NOTE §4 Cor B |
| Closure/BFS characterizations of (left-linear) winnability; poset⇄lattice enumeration bijection; duality robustness | PROVED | NOTE §3 |
| Unique-coatom lattices at size n are exactly A006966(n−1) many, all winning | PROVED (two lines) + observed exactly | NOTE §6 |

Every generation count matches OEIS A000112 (posets) and every filter count
matches A006966 (lattices) at all sizes 3…15 — these anchors are part of the
certificate.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `lattscan.c` | streams digraph6 posets, filters lattices, decides left-linear then (if needed) general winnability, prints any SEPARATING / NONWINNING lattice immediately | n≤13: ~80 s; n=14: 5.2 min (8 parts, 4 cores); n=15: 133 min / 8.2 CPU-h (16 parts) | `RESULT … winning=… llwinning=…` |
| `run_census.sh N [PARTS] [CONC]` | full census at size N: generation, scan, aggregation, OEIS count check, summary row | as above | `data/census_summary.tsv` row |
| `reference.py` | independent Python implementation (parser, filter, µ, both deciders); OEIS-anchored self-test `python3 reference.py 9` | k≤9: seconds; k=11: ~1 h | dual-implementation agreement |
| `verify_witness.py '<digraph6>'` | independent lattice rebuild + winning-tree extraction + mechanical Definition-3.1 check | ms per lattice | verified explicit trees |

```bash
cd conjectures/nci-datrees && gcc -O3 -o lattscan lattscan.c && ./run_census.sh 12 1 1
```

Requires Debian `nauty` (for `nauty-genposetg`), gcc, Python 3.

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/census_summary.tsv` | `run_census.sh` | per-size totals: posets, lattices, winning, LL-winning, separating, non-winning, max BFS states, OEIS checks |
| `data/parts_n*/part_*.log` | `run_census.sh` | raw per-part engine output (the aggregation inputs) |
| `data/fig31.d6` | hand-encoded from [3] Fig. 3.1 | the paper's example lattice; control input |
| `data/crosscheck_*.txt` | session | dual-implementation agreement records |

## Known defects and open threads

- Corollary B leans on [1]'s isomorphism-invariance and canonical-realization
  results, checked at statement level only (their proofs not re-verified
  here).
- Sharpest next step: a canonical-construction-path *lattice* generator
  (poset yield at n = 15 is 0.45%) to reach n = 16–18; and the minimal
  separating lattice, which the engine reports automatically if in range.

## Prior work

[1] arXiv:2401.16210 (conjecture; brute-force verification for ground sets
≤ 5 points in the strong left-linear+polarity version — incomparable to our
lattice-size bound, see NOTE §7). [2] arXiv:2608.19414 (left-linear
refutation; explicit upper bound 10^(10^2215); OP: size bounds).
[3] arXiv:2608.27416 (full refutation; ≈ 1.00011·10¹⁵; OP: smallest
lattice). All three read in full 2026-08-28. This directory's bound is, to
our knowledge as of today, the first lower bound recorded for either open
problem; the arXiv full-text search "non-cancelling" returns only these
three papers.
