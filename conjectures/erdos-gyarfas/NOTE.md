# Computational lower bounds for counterexamples to the Erdős–Gyárfás conjecture

**Session date.** 2026-07-30.
**AI assistance.** This note was produced with substantial AI assistance
(Claude); all computational claims ship code and data in this directory.

## Abstract

The Erdős–Gyárfás problem (erdosproblems.com #64) asks whether every finite
graph with minimum degree at least 3 contains a cycle of length 2^k for some
k ≥ 2. Erdős and Gyárfás believed the answer to be negative — the modern
"conjecture" is falsifiable by a single finite graph. We re-derive and extend
the computational lower bounds on the order of a counterexample, from scratch
and with independent tooling (nauty's geng, validated against OEIS; a
purpose-built exact cycle-length checker, validated against networkx). Main
new result: **no graph with minimum degree ≥ 3 on at most 18 vertices is a
counterexample** (834 711 846 C4-free candidates scanned at n = 18 alone) —
the previously reported bound was 17 vertices (Royle and Markström,
secondary-sourced). We also reproduce the cubic censuses of Markström
(2004) at order 24, and run simulated-annealing hunts for {4,8,16}-free
cubic graphs in the minimal window 54 ≤ n ≤ 62 where a smallest cubic
counterexample must live; basin-hopping reaches a {4,8}-free cubic graph on
56 vertices with only 56 sixteen-cycles.

## 1. Statement and status

**Problem (Erdős–Gyárfás).** Does every finite graph with minimum degree ≥ 3
contain a cycle of length 2^k, k ≥ 2?

Notes on the statement:

- For simple graphs "cycle of length a power of 2" and "cycle of length 2^k,
  k ≥ 2" coincide (cycles have length ≥ 3).
- Erdős and Gyárfás believed the answer negative, and conjectured more
  strongly that for every r there are graphs of minimum degree ≥ r with no
  power-of-2 cycle. The strong form is **false**: Liu and Montgomery proved
  that sufficiently large minimum degree forces cycles of length 2^k
  (consequence of arXiv:2010.15802). The min-degree-3 question remains open.
- erdosproblems.com lists the problem as #64, status "falsifiable — open, but
  could be disproved with a finite counterexample", with a $1000 prize listed
  (the prize amount conflicts across sources: Wikipedia-derived snippets say
  $100 for a proof / $50 for a counterexample; not resolvable this session).

A counterexample on n vertices must avoid cycles of every length
2^k ∈ [4, n]. In particular a cubic (or any) counterexample on n ≤ 31
vertices needs only to avoid {4, 8, 16}, and one on 33 ≤ n ≤ 63 must avoid
{4, 8, 16, 32}.

## 2. Results

Labels per repository convention: CERTIFIED = exact integer computation,
reproducible, no floating point in the critical path; NUMERICAL = heuristic
search evidence.

### Theorem C1 (CERTIFIED). No counterexample has ≤ 18 vertices.

Every connected graph with minimum degree ≥ 3 on n ≤ 18 vertices contains a
cycle of length 4 or 8. Consequently (components of a min-degree-3 graph
are min-degree-3 graphs) every graph with minimum degree ≥ 3 on at most 18
vertices contains a power-of-2 cycle: any counterexample to Erdős–Gyárfás
has **at least 19 vertices**.

*Method.* A counterexample is C4-free by definition, so it suffices to scan
C4-free connected graphs of minimum degree ≥ 3 (`geng -c -d3 -f`), testing
each for 8- and 16-cycles by exact DFS (`cyclecheck`). Orders and counts of
C4-free min-degree-3 connected graphs scanned:
n=12: 57 · n=13: 503 · n=14: 6 059 · n=15: 91 433 · n=16: 1 655 659 ·
n=17: 34 758 006 · n=18: 834 711 846.
None is {4,8}-free (so the 16-cycle test was never even needed — every one
of these graphs contains an 8-cycle outright, or a 4-cycle is excluded by
construction and re-verified per graph).
Machine: 4-core container; n=18 took 12 480 s wall on 3 cores (48 geng
work parts). Full rows in `data/counts_mindeg3_c4free.tsv`.

*Relation to prior work.* The reported prior bound is "any counterexample
has at least 17 vertices", i.e. none on ≤ 16 (computer searches credited to
G. Royle and K. Markström; known to us only through secondary sources —
Wikipedia-level snippets; the primary computation appears unpublished).
Theorem C1 is independent of that work and supersedes it by two orders.

### Proposition C2 (CERTIFIED). Cubic censuses re-derived, n ≤ 24.

Among connected cubic graphs: no {4,8}-free graph exists with n ≤ 22
(C4-free counts scanned: 36 / 269 / 2 761 / 36 101 / 553 227 at
n = 14/16/18/20/22), and at n = 24 there are **exactly four** (9 467 449
C4-free cubic graphs scanned) — an independent, clean-room reproduction of
Markström (2004). Their invariants, all computed here: every one has girth
3 and 16-cycles; C16 counts 330, 315, 207, 228; exactly one is planar (the
graph known as the Markström graph — which our annealer had independently
recovered as its n = 24 optimum before the census completed; the census
graph and the annealing graph are isomorphic). Graphs committed in
`data/c48free_cubic_n24.g6`. In particular the minimum number of
16-cycles over all {4,8}-free cubic graphs on 24 vertices is exactly
**207**.

### Data D3 (CERTIFIED per graph). Named cubic graphs all conform.

24 named/constructed cubic graphs (Petersen, Heawood, Möbius–Kantor, Pappus,
Desargues, dodecahedron, McGee, Nauru, Tutte–Coxeter, Dyck, Foster, a
70-vertex girth-10 LCF graph, and generalized Petersen graphs up to
GP(48,7)) each contain a power-of-2 cycle. Constructions are self-certified
(order, 3-regularity, girth recomputed); spectra by exact DFS. Table:
`data/named_spectra.tsv`.

### Hunt H4 (NUMERICAL). Annealing in the minimal cubic window.

Per Markström's unpublished search (secondary-sourced: all cubic graphs with
n ≤ 52 scanned, none avoid {4,8,16}), a minimal cubic counterexample must
have 54 ≤ n ≤ 62, avoiding exactly {4,8,16,32}. We run simulated annealing
over connected cubic graphs (2-edge-swap moves, exact cycle counts as
energy; focused moves biased to edges on bad cycles; deterministic
steepest-descent polish proving depth-1 local minimality; basin hopping).

State of the hunt after this session:

- Chains at n = 54, 56, 58, 60 all reach graphs with C4 = C16 = 0 and only
  **three or four 8-cycles** (pairwise vertex-disjoint, riding on
  triangles).
- On the {4,8}-free manifold, basin hopping at n = 56 drove the exact
  16-cycle count monotonically 78 → 63 → 56, then plateaued for 60 fresh
  rounds. At n = 58 a parallel descent reached **37**. The record graphs
  (`data/record_c48free_n56_c16_56.g6`, `data/record_c48free_n58_c16_37.g6`)
  are connected cubic graphs with no 4-cycle, no 8-cycle, and 56 resp. 37
  sixteen-cycles (spectra {16, 32}; counts independently confirmed by
  networkx enumeration, C4/C8 absence additionally confirmed by SAT
  unsatisfiability).
- Every extremal graph found is triangle-rich (girth 3), matching
  Markström's order-24 extremal graphs.

No {4,8,16}-free cubic graph was found (consistent with their known
scarcity: none exist below 54). The minimum C16 count on the {4,8}-free
manifold falls sharply with order: exactly **207** at n = 24 (full census,
CERTIFIED), at most **56** at n = 56, at most **37** at n = 58 (heuristic
records — these orders are not exhausted, so NUMERICAL). A heuristic
minimum measures search difficulty, not a bound; but the certified n = 24
value anchors the curve, and its steep fall is the most encouraging sign
this session produced that the window [54, 62] (or just beyond) may
actually contain {4,8,16}-free cubic graphs.

### Discussion (heuristic, not a theorem): why triangles

Every extremal graph in sight — Markström's four order-24 graphs, his
order-26 census, and independently our annealing optima at n = 54–62 — has
girth 3 and many triangles, even though nothing in the objective rewards
triangles. A plausible mechanism: expanding a vertex into a triangle (Y→Δ)
sends a cycle of length L through that vertex to length L+1 or L+2
depending on how it enters and leaves the new triangle. Triangle-rich
graphs therefore have "elastic" cycle lengths — the same global circuit
can realize several nearby lengths, and local structure can be tuned to
straddle the powers of 2 rather than land on them. High girth does the
opposite: it rigidifies short cycle lengths (and the smallest girth-9
cubic graphs already have 58 vertices, right in the critical window, with
their cycle spectra out of our control). This is consistent with the
replication repo's observation that "girth is a trap" and suggests the
right search space really is girth-3 gadget structures, vindicating the
annealer's own preference.

## 3. Methods and validation

- `geng` (nauty 2.8.8, Debian) counts validated against OEIS: A002851
  (connected cubic: 1,2,5,19,85,509,4060,41301 at n=4..18 — exact match),
  A007112 (connected min-degree-3: 2589, 84242, 5203110 at n=8,9,10 — exact
  match), A014372 (cubic girth ≥ 5: 1,2,9,49 at n=10..16 — exact match).
  OEIS terms read from the official OEIS git mirror.
- res/mod work-splitting validated: n=20 C4-free cubic count identical
  unsplit vs 2-way vs 4-way split (36 101).
- `cyclecheck` (exact DFS, integer-only) validated against independent
  enumeration (networkx `simple_cycles`) on 71 graphs: named graphs with
  known spectra + random cubic + random dense. 71/71 agree
  (`crosscheck.py`).
- Every survivor-producing step re-verifies C4-freeness rather than
  trusting the generator flag.

## 4. Prior work (verification status marked per item)

Primary sources were largely unfetchable from this sandbox (egress proxy
blocks arXiv, Wikipedia, journal sites, and the authors' pages); items
below are labelled by how they were verified. **Anything marked
(secondary) must be re-checked against the primary source before citing in
a preprint.**

- Erdős problem lists: the problem appears in six Erdős papers per
  erdosproblems.com's bibliography, earliest [Er93] Quaestiones Math. 1993,
  p. 343 (verified against three independent scrapes of erdosproblems.com
  #64 and its Lean formalization in google-deepmind/formal-conjectures).
- K. Markström, "Extremal graphs for some problems on cycles in graphs",
  Congr. Numer. 171 (2004): exhaustive cubic search through order 28;
  {4,8}-free cubic censuses 4 / 23 / 251 at n = 24 / 26 / 28; the four
  order-24 graphs have girth 3, one planar (the "Markström graph")
  (secondary: replication repo + search snippets; the order-24/26 censuses
  were independently re-verified computationally during recon, and our own
  n=24 sweep re-derives the order-24 census from scratch).
- Markström's data page (unpublished): all cubic graphs n ≤ 52 searched for
  {4,8,16}-avoidance, none found ⇒ f(4) ≥ 54 (secondary, quoted via a
  replication repo; cited by Exoo as "an unpublished result of Markström").
- G. Exoo, arXiv:1403.5636 (2014): constructions from the Buckyball,
  Petersen, and Tutte–Coxeter graphs; "smallest known cubic graphs with no
  2^m-cycles for m ≤ 4 and m ≤ 5"; f(5) ≤ 450 (secondary, abstract snippet
  only; orders of the constructions unverifiable this session).
- S. E. Shauger, Congr. Numer. 134 (1998): conjecture holds for K_{1,m}-free
  graphs with min degree ≥ m+1 or max degree ≥ 2m−1 (secondary).
- D. Daniel, S. E. Shauger, Congr. Numer. 153 (2001): planar claw-free case
  (secondary).
- C. C. Heckman, R. Krakovski, Electron. J. Combin. 20(2) #P7 (2013): every
  3-connected cubic planar graph has a 2^m-cycle, m ≤ 7 (secondary).
- P. S. Nowbandegani, H. Esfandiari (2011): bipartite counterexample ≥ 32
  vertices (secondary). Same group (arXiv:1109.5398): cubic claw-free
  counterexample ≥ 114 vertices (secondary).
- H. Liu, R. Montgomery (arXiv:2010.15802): large min degree forces
  power-of-2 cycles, refuting the strong Erdős–Gyárfás belief (secondary;
  attribution as stated on erdosproblems.com #64, verified against scrapes).
- M. H. Ghaffari, Z. Mostaghim, Aequat. Math. 92 (2018): Cayley graphs of
  generalized quaternion / dihedral / semidihedral / order-p³ groups
  (secondary). M. Ghasemi, R. Varmazyar, Mat. Vesnik 73 (2021): Cayley
  graphs of order 2p², 4p (secondary).
- A. Carr, arXiv:2508.19302 (2025): diameter-2 min-degree-3 graphs contain a
  4- or 8-cycle. A. Carr, arXiv:2605.22844 (2026): ≥ 4/7 of the vertices of
  a minimal counterexample are cubic; every regular minimal counterexample
  is cubic (secondary).
- Verified-2026-replications (GitHub research logs, not literature):
  oaustegard/experiments (re-census at 24/26, matches Markström
  graph-for-graph) and Joe975/math-lab (cubic n ≤ 20 re-verified). These
  are AI-assisted logs like this one — leads, not authority.

## 5. Open questions after this session

1. Push the general min-degree-3 bound past 18 (n = 19 needs ~5×10⁸ C4-free
   graphs scanned; n = 20 ~10¹⁰ — the latter wants better generation-time
   pruning, e.g. pruning 8-cycles during generation à la Markström's
   modified minibaum).
2. Find any {4,8,16}-free cubic graph with n ≤ 62 (would pin f(4) ∈ [54,62]
   and immediately raise the counterexample question via the C32 screen), or
   push annealing evidence that none exists at 54–62.
3. Obtain and screen the 18 (3,9)-cages (n = 58): girth 9 kills {4,8}; only
   C16 and C32 stand between any of them and a counterexample. (Data was
   unreachable from this sandbox; classifier also denied the repo-mirror
   route.)
4. Resolve the prize question ($1000 vs $100/$50) against Erdős's original
   problem papers.
