# Session narrative — 2026-07-30

## Why this conjecture

The brief for today was a conjecture that a single explicit object could
kill. The Erdős–Gyárfás conjecture — every graph with minimum degree ≥ 3
contains a cycle whose length is a power of 2 — fits exactly: a counterexample
is one concrete graph, and checking it is pure integer computation (enumerate
cycle lengths). The known computational frontier is small (Markström's
exhaustive search, cubic graphs up to 29 vertices, early 2000s-era hardware),
so a container with 4 cores has a real shot at standing on the frontier rather
than far behind it.

The pivotal observation that shaped the whole session: **a cubic graph on
n ≤ 31 vertices with no 4-, 8-, or 16-cycle is automatically a full
counterexample** — a 32-cycle needs 32 vertices. So "hunt for {4,8,16}-free
cubic graphs at n = 26, 28, 30" is not a warm-up exercise; it is the hunt
itself, on ground just past the exhaustive frontier.

## Tooling (built from scratch — the sandbox blocks all the usual sources)

The proxy blocks House of Graphs, Meringer's genreg page, and the nauty
homepage; the only generator obtainable was Debian's `nauty` package
(`nauty-geng` 2.8.8). Everything else is written in this directory:

- `cyclecheck.c` — exact existence test for cycles of length exactly
  L ∈ {4,8,16,32,64,128} per input graph (graph6, n ≤ 128). Min-vertex DFS
  with BFS-distance pruning. No floating point.
- `crosscheck.py` — independent validation of cyclecheck against
  networkx `simple_cycles` on 71 graphs (named + random cubic + random
  dense). All agree, including Petersen/Heawood/Pappus/McGee spectra.
- `hunt.c` — simulated annealing over connected cubic graphs (2-edge-swap
  moves, connectivity preserved, exact cycle counts as energy). Two-phase:
  cheap C≤8 energy first ({4,8}-free manifold), then full weighted
  C4/C8/C16 energy. Also a girth mode (energy = number of cycles shorter
  than a bound) for synthesizing high-girth seeds.
- `run_exhaustive.sh` / `run_hunt.sh` — drivers with res/mod parallelism.

### Validation discipline

- geng cubic counts for n = 4..18 match OEIS A002851 exactly
  (1, 2, 5, 19, 85, 509, 4060, 41301).
- geng res/mod splitting cross-checked: n=20 C4-free cubic = 36101 both
  unsplit and as 0/2 + 1/2 (9062 + 27039).
- cyclecheck vs networkx: 71/71 agreement (`crosscheck.py`).

### Mistakes made and caught

- First version of the sweep driver aggregated stale per-part logs from an
  earlier run with a different mod value, inflating one count (56547 vs the
  true 36101). Caught by an unsplit control run; fixed by clearing part
  logs at start. Lesson: sum only what this run wrote.
- Overwrote `run_exhaustive.sh` while the n=24 sweep was executing it
  (bash may re-read a running script file). Killed and restarted the sweep
  under the new script rather than trusting an undefined state.
- First crosscheck attempt used `networkx.simple_cycles` with the full
  length bound on dense random graphs — combinatorial explosion, hung.
  Restricted dense instances to n ≤ 12 and clipped the bound to the largest
  power of 2 that matters.

## Exhaustive sweeps (as they complete)

Class: connected cubic, C4-free (`geng -c -d3 -D3 -f`) — every
counterexample is C4-free, and cyclecheck re-verifies C4 absence on every
graph geng emits.

| n | C4-free cubic graphs | {4,8}-free | time |
|---|---|---|---|
| 14 | 36 | 0 | 0 s |
| 16 | 269 | 0 | 0 s |
| 18 | 2 761 | 0 | 4 s |
| 20 | 36 101 | 0 | 24 s (4 cores) |
| 22 | 553 227 | 0 | 444 s (4 cores) |
| 24 | (running) | | |

## Named-graph spectra

`named_spectra.py` builds famous cubic graphs (networkx builtins, LCF
codes, generalized Petersen family) — each construction self-certified by
computing order, regularity, and girth before use — and runs cyclecheck.
Every one of the 24 graphs, up to the Foster graph (n=90, girth 10) and
GP(48,7) (n=96), contains a power-of-2 cycle. Table in
`data/named_spectra.tsv`.

## The recalibration (mid-session)

The literature recon (six parallel agents; primary sources mostly
egress-blocked, so everything paper-level is secondary-sourced and marked)
came back and moved every goalpost:

- Erdős and Gyárfás believed the answer NEGATIVE — hunting a counterexample
  is the direction the posers expected to win.
- Markström (2004) had already exhausted cubic graphs through order 28, and
  an unpublished continuation reports {4,8,16}-avoidance impossible for
  cubic n ≤ 52. My planned "hunt at n=26..30" was dead before it started —
  the live window for a minimal cubic counterexample is **54 ≤ n ≤ 62**,
  where the obstruction set is exactly {4,8,16,32}.
- The general min-degree-3 bound stood at 17 vertices (Royle–Markström,
  secondary-sourced, apparently unpublished). geng timings said n = 17 and
  18 were within reach — that became the session's certified prize.
- Exoo (2014) constructed the "smallest known" cubic graphs avoiding
  {4,8,16} and {4,8,16,32} (from Petersen and Tutte–Coxeter derivations;
  f(5) ≤ 450) — so hits in the window are compared against constructions of
  unverifiable order, and only a hit at exactly 54 would pin f(4) = 54.

Consequences: the n=24 cubic sweep was reframed from "frontier" to
"pipeline certification" (it must find exactly Markström's 4 graphs); the
n=26..30 hunt was retargeted to 54..62; a planned bipartite push was
deprioritized (would only reproduce the known ≥32 bound).

Also mid-session: the container restarted (killing the first n=24 run), and
the permission classifier denied both the cage-data repo route and further
scratchpad archaeology — the (3,9)-cage screen goes down as an open thread,
not a result.

## Exhaustive results, phase 2 (min-degree-3 — the new bound)

C4-free connected graphs with min degree ≥ 3 (`geng -c -d3 -f`), each
checked for 8-cycles (16-cycle check never reached — no {4,8}-free graph
appeared at all):

| n | scanned | {4,8}-free | time |
|---|---|---|---|
| ≤15 | 98 052 | 0 | seconds |
| 16 | 1 655 659 | 0 | 37 s (4 cores) |
| 17 | 34 758 006 | 0 | 599 s (4 cores) |
| 18 | 834 711 846 | 0 | 12 480 s (3 cores) |

**Theorem C1 final: any Erdős–Gyárfás counterexample has at least 19
vertices.** The n=18 growth factor (×24 over n=17) puts n=19 at roughly
2×10¹⁰ C4-free graphs — a multi-day run at this core count, noted as an
open thread.

Class validated against OEIS A007112 before running (geng -c -d3 counts
2589 / 84 242 / 5 203 110 at n=8/9/10 — exact match).

## The hunt (n = 54..62)

Simulated annealing over connected cubic graphs, energy = weighted exact
counts of C4/C8/C16 (counts cross-checked against networkx enumeration —
the 78 sixteen-cycles of one key graph reproduce exactly). Three
generations of the search:

1. **v1 uniform moves**: chains stall around E=8–14.
2. **v2 focused moves** (70% of swaps pick an edge lying on a currently-bad
   cycle, WalkSAT-style): chains reach E=6 — graphs with C4=0, C16=0 and
   only **three 8-cycles** — at n=56 and n=58 within 2.5M moves.
3. **Polish mode** (deterministic steepest descent over all ~13k 2-swaps,
   proving depth-1 local minimality): applied to the E=6 graph at n=56 with
   manifold-pinning weights (100/50/1), it killed all three 8-cycles at the
   price of 16-cycles, landing on a certified local minimum that is
   **{4,8}-free on 56 vertices with exactly 78 sixteen-cycles**
   (spectrum {16,32}; verified independently).

Structural picture that emerged (consistent across n): the optimizer
converges to triangle-rich graphs — girth 3, 14–16 triangles — exactly the
shape of Markström's extremal order-24 graphs (girth 3, one planar). The
stubborn 8-cycles in the E=6 states are pairwise vertex-disjoint and their
vertices lie almost entirely on triangles. The endgame battle is between
8-cycles and 16-cycles: annihilating the last C8s spawns C16s.

Positive control: at n=24 the same machinery (heavy weights) found a
{4,8}-free cubic graph — necessarily one of Markström's four — with C16
count 228; it passes the survivor filter end-to-end and triple-verifies
(networkx enumeration, SAT UNSAT for C4 and C8, 10 random relabelings).

Basin hopping (anneal → polish → keep-if-better) now runs on the
{4,8}-free manifold minimizing the C16 count; the minimum C16 achieved per
n is this session's quantitative "distance to counterexample".

## The census lands (early morning, day 2)

The n = 24 cubic census sweep finished: 9 467 449 C4-free connected cubic
graphs, exactly **four** {4,8}-free — Markström's census, reproduced
clean-room (his files were never read by this pipeline; only the count "4"
was known from recon). Characterization computed here: all girth 3, C16
counts 330 / 315 / 207 / 228, exactly one planar. Two pleasant closures:

- The graph the annealer had found hours earlier as its n = 24 optimum is
  isomorphic to the planar census graph — the annealer had independently
  rediscovered the **Markström graph** itself.
- The exact minimum C16 count over {4,8}-free cubic graphs on 24 vertices
  is **207** — a certified anchor for the "distance to counterexample"
  curve, against the heuristic ≤ 56 at n = 56.

Basin hopping at n = 56 plateaued at 56 sixteen-cycles after 60 fresh
rounds (the record graph survives every 1M-move perturbation tried). The
parallel descent at n = 58 escaped its 2-C8 local minimum and reached the
manifold at **37 sixteen-cycles** — the session's best object. Both
records committed under `data/`, verified independently (networkx
enumeration + SAT UNSAT for C4/C8 + relabeling stability).

## Where the session ends

Manifold-minimum C16 curve: 207 (n = 24, exact, census) → ≤ 56 (n = 56)
→ ≤ 37 (n = 58). Every graph on that curve is triangle-rich, girth 3.
The next session picks this up with more compute (the curve wants n = 60
and 62, longer hops, and a C32-existence term in the endgame energy), or
attacks the untouched (3,9)-cage screen once the data is reachable.
