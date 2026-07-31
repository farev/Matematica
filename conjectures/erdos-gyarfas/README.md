# Erdős–Gyárfás conjecture (Erdős & Gyárfás, ≤1993)

Does every finite graph with minimum degree at least 3 contain a cycle whose
length is a power of 2 (i.e. 2^k, k ≥ 2)? Erdős and Gyárfás themselves
believed the answer is **no** — one explicit graph would settle it. This
session hunts that graph: exhaustive sweeps at small orders (which produced a
new lower bound on any counterexample), plus simulated-annealing hunts in the
window 54 ≤ n ≤ 62 where a minimal cubic counterexample must live.
erdosproblems.com problem #64, status "falsifiable"; prize listed there as
$1000 (other sources: $100/$50 — unresolved).

**Status:** active
**Sessions:** 2026-07-30

## Results

| Claim | Label | Where |
|---|---|---|
| **No counterexample has ≤ 18 vertices** (prior reported bound: 17). Every connected min-degree-3 C4-free graph with n ≤ 18 contains an 8-cycle — 834 711 846 graphs scanned at n = 18 alone. | CERTIFIED | NOTE §2, Thm C1; `data/counts_mindeg3_c4free.tsv` |
| No cubic {4,8}-free graph has n ≤ 22; at n = 24 there are **exactly four** (9.47M C4-free cubic scanned — clean-room reproduction of Markström 2004; girth 3 all, one planar, C16 counts 330/315/207/228) | CERTIFIED | NOTE §2, Prop C2; `data/c48free_cubic_n24.g6` |
| No bipartite cubic {4,8}-free graph has n ≤ 26 (girth ≥ 6 class, 1 201 graphs at n = 26) | CERTIFIED | `data/counts_bipcubic_c4free.tsv` |
| A {4,8}-free cubic graph on 24 vertices (necessarily one of Markström's four), spectrum {16} with 228 sixteen-cycles, triple-verified | CERTIFIED | `data/markstrom_candidate_n24.g6`, `verify_hit.py` |
| {4,8}-free cubic graphs on **56 vertices with 56 sixteen-cycles** and on **58 vertices with 37 sixteen-cycles** (spectra {16,32}), depth-1 local minima; manifold-minimum curve 207 (n=24, exact) → ≤56 → ≤37 | CERTIFIED (the graphs) / NUMERICAL (minimality) | `data/record_c48free_n5*.g6`, `hunts/basinhop.tsv` |
| 24 named cubic graphs (≤ 96 vertices, girth up to 10) all contain power-of-2 cycles | CERTIFIED | `data/named_spectra.tsv` |
| Annealing chains at n = 54..60 all reach C4 = C16 = 0 with only 3–4 disjoint 8-cycles | NUMERICAL | `hunts/results_n*.tsv` |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `cyclecheck.c` | exact per-graph test: which of C4/C8/C16/C32/C64/C128 occur (graph6 in, n ≤ 128) | µs–ms per graph | survivor filters, spectra |
| `crosscheck.py` | validates cyclecheck against networkx on 71 graphs | ~1 min | "all 71 graphs agree" |
| `run_exhaustive.sh <n> <mod> <jobs> [class]` | geng sweep of a C4-free class ({4,8}-free census); classes: cubic, bipcubic, mindeg3 | seconds → hours | `data/c48free_*_n<n>.g6`, count rows |
| `hunt.c` | simulated annealing over connected cubic graphs; energy = weighted exact counts of C4/C8/C16 (or girth mode) | ~1–2k moves/s at n≈54 | `RESULT`/`HIT` lines + best graph |
| `run_hunt.sh <n> <chains> <moves> <jobs> [seed0]` | hunt batch; post-screens best graphs incl. C32 | ~30 min per 2.5M-move chain | `hunts/results_n<n>.tsv` |
| `named_spectra.py` | builds named cubic graphs (self-certified girth), runs cyclecheck | ~1 min | `data/named_spectra.tsv` |

Run from inside this directory, e.g.:

```bash
cd conjectures/erdos-gyarfas
gcc -O3 -march=native -o cyclecheck cyclecheck.c
gcc -O3 -march=native -o hunt hunt.c -lm
./run_exhaustive.sh 18 48 3 mindeg3     # the Theorem C1 workhorse
./run_hunt.sh 54 8 2500000 4            # hunt chains at n=54
```

Requires `nauty` (Debian package; provides `nauty-geng`) and networkx for the
validation scripts.

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/counts_mindeg3_c4free.tsv` | run_exhaustive.sh | per-order counts: C4-free min-deg-3 graphs scanned, {4,8}-free survivors (all zero) — the Thm C1 certificate rows |
| `data/counts_cubic_c4free.tsv` | run_exhaustive.sh | same for connected cubic |
| `data/c48free_cubic_n24.g6` | run_exhaustive.sh | the {4,8}-free cubic graphs at n=24 (graph6) |
| `data/named_spectra.tsv` | named_spectra.py | name, order, girth, power-of-2 cycle spectrum |
| `hunts/results_n*.tsv` | run_hunt.sh | per-chain best energy + exact spectrum of best graph |

The "certificate" for the exhaustive claims is reproducibility plus
validation: generator counts are checked against OEIS (A002851, A007112,
A014372), split-consistency is checked, and the checker is validated against
an independent implementation. There is no compact witness for "we saw every
graph" beyond rerunning.

## Known defects and open threads

- n=19 (min-degree-3) needs ~5×10⁸ C4-free graphs — feasible with patience;
  n=20 wants generation-time C8 pruning (Markström-style modified minibaum).
- The {4,8,16}-free window 54–62 is only touched heuristically here; nobody
  (including us) has exhausted it.
- The 18 (3,9)-cages at n=58 remain unscreened for C16/C32 (data
  unreachable from this sandbox). Two of them lacking both would be a
  counterexample; nobody seems to have published this check.
- Prize amount unresolved ($1000 per erdosproblems.com vs $100/$50 per
  Wikipedia-derived snippets).
- Primary sources (Markström 2004, Exoo 2014, Erdős's problem papers) were
  unfetchable; all such citations are secondary-sourced and marked so.

## Prior work

See NOTE §4 for the full annotated list with per-item verification status.
Headlines: Markström (2004) exhausted cubic graphs through order 28 and
(unpublished) {4,8,16}-avoidance through order 52; Royle–Markström pushed
the general bound to 17 vertices (superseded by Thm C1 here); Heckman–
Krakovski proved the 3-connected cubic planar case; Liu–Montgomery refuted
the strong (large-min-degree) negative belief; Exoo constructed the
smallest known {4,8,16}- and {4,8,16,32}-avoiding cubic graphs (orders not
verifiable this session); Carr (2025–26) constrains minimal counterexamples.
