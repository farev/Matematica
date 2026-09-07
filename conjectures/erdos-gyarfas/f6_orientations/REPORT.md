# f(6) probe: orientation SAT instances for Garcia's AGL(1,p) base graphs

Bounded computational probe, 2026-09-07, 11:54-12:40 UTC, one sandbox
(Intel Xeon 2.80 GHz, 4 cores visible, at most 2 used concurrently for the
heavy runs, 15 GB RAM; Python 3.11.15, numpy 2.4.6, python-sat 1.9.dev15,
gcc 13.3). Everything lives in this directory; the repository was not touched.

Setup taken as given from the task statement (Garcia, arXiv:2609.04686,
Lemma 3.2 / Section 5): the expansion of a cubic girth-14 base graph B by the
gadget H15 with an orientation (choice of the u-edge at every vertex) is
{4,8,16,32,64}-free iff every 14-cycle of B has at least 5 vertices whose
u-edge is OFF the cycle, every 15-cycle at least 3, every 16-cycle at least 1.
I did not re-derive that lemma and could not consult the paper from the
sandbox; every statement below is conditional on that reduction.

Conventions. AGL(1,p) elements are pairs (a,b) for x -> ax+b, composed as
functions, (a,b)(c,d) = (ac, ad+b). Cay(G,S) has x ~ xs for s in S, so left
multiplication is a graph automorphism. Labels: 0 = t-edge, 1 = g-edge
(x -> xg), 2 = g^{-1}-edge. The involutions of AGL(1,p) are exactly the p
elements (-1,b), so t = (p-1, b).

## 1. Connection sets of girth 14 (CERTIFIED for the ranges stated)

`scan.py p` enumerates every set {t, g, g^{-1}} with t an involution and g
neither the identity nor an involution (counted once modulo g <-> g^{-1}),
tests generation (connectivity) and computes the girth by BFS from the
identity (exact for vertex-transitive graphs: the shortest cycle through the
root is the girth). Girth 14 of one representative per class was re-checked
by BFS from every root, and again by the exact cycle enumeration of
Section 2 (zero cycles of length 3..13).

| p | candidate sets | non-generating | girth 10 | girth 12 | girth 14 | classes under conjugation |
|---|---|---|---|---|---|---|
| 29 | 11,339 | 6,467 | 812 | 2,436 | **1,624** | 2 (each of size 812) |
| 31 | 13,919 | 6,479 | 1,860 | 1,860 | **3,720** | 4 (each of size 930) |

No generating set has girth below 10 or above 14 (scan: 11.3 s and 16.9 s).
Girth-14 sets exist for p = 29, as the paper states. Class representatives
(t = (-1,0), g = (a,1); conjugation preserves the multiplier a and inversion
sends a to a^{-1}, so the classes are {a, a^{-1}}):

| p | g | ord(g) | class = multipliers | N14 | N15 | N16 |
|---|---|---|---|---|---|---|
| 29 | (3,1)  | 28 | {3, 10}  | 2,030 | 0  | 5,278 |
| 29 | (8,1)  | 28 | {8, 11}  |   812 | 0  | 6,902 |
| 31 | (7,1)  | 15 | {7, 9}   | 1,395 | 62 | 5,580 |
| 31 | (10,1) | 15 | {10, 28} | 2,790 | 62 | 3,255 |
| 31 | (11,1) | 30 | {11, 17} | 2,325 | 0  | 3,720 |
| 31 | (22,1) | 30 | {22, 24} | 2,790 | 0  | 3,720 |

Conjugate sets give isomorphic Cayley graphs (conjugation by h composed with
left multiplication by h^{-1} is an isomorphism), so each class is one graph
up to isomorphism, and the six representatives are pairwise
**non-isomorphic** because their (N14, N15, N16) triples differ. Calling the
conjugacy classes "automorphism classes" would use Aut(AGL(1,p)) = Inn
(AGL(1,p) is complete) - from memory, not re-verified, and nothing depends on
it: the enumeration is over all 11,339 / 13,919 sets.

I cannot tell which of the two (p = 29) or four (p = 31) graphs Garcia
used; "searching all generating pairs" is consistent with any of them.
Files: `scan_p{29,31}_all.csv` (every set with its girth),
`girth14_p{29,31}.csv` (class representatives), and for each representative
`p{p}_t{a}_{b}_g{a}_{b}.edges` (edge list), `.g6` (graph6), `.graph`
(adjacency lists, input format of the enumerator).

## 2. Cycle counts (CERTIFIED)

`cycles.c` enumerates every simple cycle of length <= L by rooted DFS with
BFS-distance pruning inside the subgraph on vertices >= root, reporting each
cycle exactly once. Validation (`validate_cycles.py`): identical cycle sets to
an independent unpruned brute-force enumerator on Petersen, Heawood and three
random cubic graphs; Petersen gives 12, 10, 0, 15, 20, 0 cycles of lengths
5..10 and Heawood 28 six-cycles and 24 Hamiltonian cycles, matching the
literature. All cycles of length <= 16 of an 812/930-vertex graph take about
0.1 s. Counts are in the table above; the cycles themselves are in
`p*_*.cycles` (one line per cycle: length then vertices).

The number of 14-cycles through the t-edge (c_t) and through either g-edge
(c_g) is the same at every vertex (the two edge orbits are edge-transitive),
and 14 N14 = n (c_t/2 + c_g) holds in every case:

| instance | c_t | c_g | sum_v c_min(v) = n c_g | 9 N14 | Lemma 5.2 condition |
|---|---|---|---|---|---|
| p29 g=(3,1)  | 26 | 22 | 17,864 | 18,270 | holds (slack 406) |
| p29 g=(8,1)  | 10 |  9 |  7,308 |  7,308 | holds with **equality** |
| p31 g=(7,1)  | 18 | 12 | 11,160 | 12,555 | holds (slack 1,395) |
| p31 g=(10,1) | 32 | 26 | 24,180 | 25,110 | holds (slack 930) |
| p31 g=(11,1) | 26 | 22 | 20,460 | 20,925 | holds (slack 465) |
| p31 g=(22,1) | 30 | 27 | 25,110 | 25,110 | holds with **equality** |

Number k_t of t-edges on the 14-cycles: p29 (3,1): 812 cycles with k_t = 4
and 1,218 with 6; p29 (8,1): 406 / 406; p31 (7,1): all 1,395 have 6;
p31 (10,1): 930 / 1,860; p31 (11,1): 930 / 1,395; p31 (22,1): 1,395 / 1,395.
No 14-cycle has fewer than 4 t-edges. For ord(g) = 15 the 62 fifteen-cycles
are exactly the cosets of <g> (checked: all their edges are g-edges and they
cover all 930 vertices).

## 3. Sharper counting consequences (PROVED, given the certified counts)

Let n_t be the number of vertices whose u-edge is the t-edge. Summing a(C)
over the 14-cycles, n_t c_t + (n - n_t) c_g = sum_C a(C) <= 9 N14, hence
n_t <= (9 N14 - n c_g)/(c_t - c_g). For ord(g) = 15 every <g>-coset is a
15-cycle whose off-cycle edges are all t-edges, so it needs >= 3 vertices
with u = t; the 62 cosets partition V, hence n_t >= 186.

| instance | n_t upper bound | n_t lower bound | consequence |
|---|---|---|---|
| p29 (3,1)  | 101 | 0   | open |
| p29 (8,1)  | **0** | 0 | every vertex must pick a g/g^{-1}-edge and every 14-cycle must have a(C) = 9 exactly |
| p31 (7,1)  | 232 | 186 | open, narrow window |
| p31 (10,1) | 155 | **186** | **no admissible orientation exists** |
| p31 (11,1) | 116 | 0   | open |
| p31 (22,1) | **0** | 0 | as for p29 (8,1) |

So Cay(AGL(1,31), {(30,0), (10,1), (28,1)}) is closed by counting alone: the
15-cycle constraints need n_t >= 186 while the 14-cycle constraints allow
n_t <= 155.

## 4. Invariant orientations (CERTIFIED: checked against every enumerated cycle)

Constant orientations (`orient.py`, `check_orientation`, which recounts a(C)
from the neighbour table, independently of any SAT encoding):

| instance | u = t everywhere | u = g everywhere (u = g^{-1} gives the same a(C) on every cycle) |
|---|---|---|
| p29 (3,1)  | 1,624 cycles violated (14-cycles up to a=12, 16-cycles a=16) | 812 violated (14-cycles with a=10) |
| p29 (8,1)  | 812 violated | 406 violated (a=10) |
| p31 (7,1)  | 1,395 violated | **only the 62 pure-g 15-cycles** (a=15) |
| p31 (10,1) | 1,860 violated | 992 violated (930 14-cycles with a=10, 62 15-cycles) |
| p31 (11,1) | 1,395 violated | 930 violated (a=10) |
| p31 (22,1) | 1,395 violated | 1,395 violated (a=10) |

None is admissible. (With u = t, a(C) = 2 k_t; with u = g or g^{-1},
a(C) = number of g-edges on C = |C| - k_t, and every instance has 14-cycles
with k_t = 4, giving a = 10 > 9.)

Orientations invariant under a subgroup K acting by left multiplication
(label constant on K-orbits), encoded with one 3-valued variable per orbit
(`build_cnf` in `orient.py`; sequential-counter cardinality encoding, repeated
literals aliased so every cardinality constraint has distinct inputs) and
solved with CaDiCaL 1.9.5 (`orient_*.log`):

* K = Z_p, translations only (orbits = the p-1 multipliers a; 28 or 30
  orbits, the search asked for): **UNSAT** for all six instances, < 0.1 s each.
* K = Z_p x| H_d for every divisor d of p-1 (coarser, (p-1)/d orbits; d = p-1
  is the three constant orientations): **UNSAT** for all six and all d.
* Both families re-solved with Glucose 4.2 and the totalizer encoding
  (`crosscheck.py`): identical answers.
* K = H_d = <(r^{(p-1)/d}, 0)>, multiplicative subgroups (n/d orbits):
  d = p-1 (29 / 31 orbits): UNSAT for all six (0.5-2.4 s); d = 14, 7 (p = 29;
  58, 116 orbits) and d = 15, 10, 6, 5 (p = 31; 62-186 orbits): undecided in
  the 5 s each was given.

## 5. Full SAT instances

Encoding (`orient.py`, files `*_full.cnf`): 3n variables, exactly-one per
vertex; for every 14/15/16-cycle an at-least-5/3/1 constraint on its
14/15/16 off-cycle literals (pysat `CardEnc.atleast`, `EncType.seqcounter`).

| instance | variables | clauses | cycle constraints |
|---|---|---|---|
| p29 (3,1)  |  93,786 | 183,106 | 7,308 |
| p29 (8,1)  |  38,976 |  79,982 | 7,714 |
| p31 (7,1)  |  67,797 | 133,176 | 7,037 |
| p31 (10,1) | 130,572 | 250,821 | 6,107 (infeasible by Section 3; not run) |
| p31 (11,1) | 107,415 | 207,390 | 6,045 |
| p31 (22,1) | 128,340 | 247,380 | 6,510 |

Strengthened, logically equivalent versions (`strengthen.py`, `*_strong.cnf`)
add the Section 3 bounds: a totalizer "at most n_t^max" over the t-literals
(plus "at least 186" for p31 (7,1)); for the two tight instances unit clauses
forbidding every t-literal and at-most-5 on every 14-cycle (a(C) = 9 forced).

Solver harness (`solve.py`): CaDiCaL runs through a conflict-budget loop
that returns control to Python between chunks (pysat's `interrupt()` from a
timer thread does not preempt the solver - it never fired in a first attempt,
which is why the first sub-instance runs had to be killed and repeated);
Kissat is exposed by pysat only non-incrementally, so it gets a single
`solve()`. Every run is additionally hard-capped by `timeout -s KILL`.

| instance | solver | wall limit | outcome | solve time | conflicts / decisions / propagations |
|---|---|---|---|---|---|
| p29 (8,1) original | cadical195 | 180 s | **TIMEOUT** | 201.4 s | 1,055,014 / 9,484,168 / 506,326,302 |
| p29 (8,1) strengthened (n_t=0, a(C)=9) | cadical195 | 150 s | **UNSAT** | 3.7 s | 2,743 / 4,159 / 2,526,251 |
| p31 (22,1) strengthened (n_t=0, a(C)=9) | cadical195 | 150 s | **UNSAT** | 0.2 s | 227 / 331 / 360,208 |
| p31 (7,1) strengthened (186<=n_t<=232) | cadical195 | 240 s | **TIMEOUT** | 254.9 s | 455,010 / 7,202,526 / 405,850,455 |
| p31 (7,1) strengthened | kissat404 | 300 s | **TIMEOUT** | 300 s | killed at the hard cap (no statistics: pysat's Kissat exposes none, and a killed process writes nothing) |
| p29 (3,1) strengthened (n_t<=101) | cadical195 | 480 s | **TIMEOUT** | 531.2 s | 855,004 / 8,974,185 / 908,581,469 |
| p29 (3,1) original | kissat404 | 1200 s | **TIMEOUT** | 1200 s | killed at the hard cap (no statistics: pysat's Kissat exposes none, and a killed process writes nothing) |
| p31 (11,1) strengthened (n_t<=116) | cadical195 | 300 s | **TIMEOUT** | 324.6 s | 255,006 / 2,828,113 / 299,784,926 |

Timeline: the solver round ran 12:12-12:38 UTC with two solver processes at a
time (one core each). Kissat's first launch (12:12) died immediately because
pysat's Kissat is non-incremental ("incremental solving not supported" under
the conflict-budget loop); it was relaunched at 12:13 with a single `solve()`
under `timeout -s KILL 1200` and was killed at 12:33 without an answer.
The original (unstrengthened) p29 (8,1) instance was still undecided by
CaDiCaL after 180 s and 1.06 M conflicts; with the forced n_t = 0 and
a(C) = 9 added it is UNSAT in 3.7 s, and p31 (22,1) in 0.2 s. Both UNSAT
answers were reproduced from an independent naive re-encoding (812 / 930
Boolean variables, 0.62 M / 2.12 M clauses, no auxiliaries, `tight_check.py`)
by Glucose 4.2 (1.4 s / 4.4 s) and CaDiCaL (2.6 s / 5.0 s).

**Outcome.** No admissible orientation was found for any of the six girth-14
Cayley graphs, and three of the six are now known to admit none:

| p | class (g multiplier) | status of the orientation instance |
|---|---|---|
| 29 | {3, 10}  | **undecided** (CaDiCaL 531 s / 855 k conflicts on the strengthened instance; Kissat 20 min on the original) |
| 29 | {8, 11}  | **UNSAT** (counting forces n_t = 0; then UNSAT in seconds, cross-checked) |
| 31 | {7, 9}   | **undecided** (CaDiCaL 255 s / 455 k conflicts; Kissat 300 s, both on the strengthened instance) |
| 31 | {10, 28} | **infeasible by counting** (n_t >= 186 from the 62 pure-g 15-cycles vs n_t <= 155) |
| 31 | {11, 17} | **undecided** (CaDiCaL 300 s on the strengthened instance) |
| 31 | {22, 24} | **UNSAT** (counting forces n_t = 0; then UNSAT in 0.2 s, cross-checked) |

So the route to f(6) <= 12,180 via AGL(1,29) rests on a single graph,
Cay(AGL(1,29), {(28,0), (3,1), (10,1)}) (multiplier class {3,10}), and the
route to f(6) <= 13,950 via AGL(1,31) on the two graphs with multiplier
classes {7,9} and {11,17}. No model was produced, so nothing was re-verified
with `verify.py` (it is in place: `python3 verify.py 29 28 0 3 1 sat_X.model`
converts a model to a vertex -> chosen-neighbour file and recounts a(C) over
freshly enumerated cycles).

Label for the solver outcomes: the two UNSAT results and the counting
infeasibility are exact (solver answers, cross-checked, but no proof
certificates); the three "undecided" entries are timeouts, i.e. no
information beyond "not easy for CDCL in 5-20 minutes on one core", in line
with the paper's "undecided after several CPU-hours".

**What I would do next with more time.** (i) Symmetry: the instance for the
{3,10} graph has a vertex-transitive symmetry group of order 812 acting on
the 2,436 variables; a solver with symmetry breaking (BreakID + CaDiCaL) or
an orbit-based ILP (n_t <= 101 is a strong global cut; CP-SAT with the
cardinality constraints native) is the natural next step. (ii) Sharper
counting: the tight bound technique of Section 3 generalises to a linear
program over per-vertex choices with the 14- and 16-cycle constraints; an LP
bound below the 15-cycle/16-cycle requirements would settle the undecided
cases without search. (iii) Other base graphs: the ord(g) = 15 cosets are
what kills {10,28}; connection sets with g of order 28/30 avoid pure-g
15-cycles entirely, and cubic graphs of girth 14 exist with far fewer than 812 vertices (the
smallest known has 384, Exoo - from memory, unverified); if Lemma 3.2 does not
need the Cayley structure, those are candidates too, subject to the same
cycle conditions.


## 6. Caveats / what is not verified

* The reduction "admissible orientation iff the 14/15/16-cycle conditions" is
  taken from the task's statement of Garcia's Lemma 3.2 and not re-derived;
  no access to the paper from the sandbox.
* UNSAT answers are solver answers without DRAT proofs. The two tight
  instances were re-encoded independently (naive clause encoding, no
  auxiliary variables, `tight_check.py`) and re-solved with Glucose 4.2 and
  CaDiCaL; the subgroup-invariant families were re-solved with a second
  solver and encoding. The counting infeasibility of p31 (10,1) is a
  three-line argument from certified counts.
* "Non-isomorphic" for the six representatives rests on distinct cycle
  counts (exact); "isomorphic within a class" rests on conjugation being a
  graph isomorphism (exact).
* Nothing here identifies which connection set Garcia's own "undecided after
  several CPU-hours" instances used.

## Files

`agl.py` group + BFS; `scan.py` girth scan; `cycles.c` enumerator (+
`validate_cycles.py`); `orient.py` counts, invariant orientations, subgroup
SAT, full CNF; `crosscheck.py`; `strengthen.py`; `tight_check.py`;
`solve.py`, `run_sat.sh`, `run_sat2.sh` solver drivers; `verify.py`
independent re-verification of an orientation (model -> vertex/neighbour
file -> recount over re-enumerated cycles); logs `*.log`, solver outputs
`sat_*.json`, per-instance `*_summary.json`, `counting_bounds.json`.
