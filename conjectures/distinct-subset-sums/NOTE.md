# Certified progress on the tenth value of the Erdős distinct-subset-sums function

*Session 2026-08-13. Written with AI assistance (Claude); all proofs
checked line-by-line in-session, all computations reproducible from this
directory. Sources marked (secondary) were verified only through search-index
snippets — the sandbox had no access to any primary page (see the session
log's connectivity section).*

## Abstract

Let `f(n)` be the least possible largest element of a set of `n` positive
integers all of whose `2^n` subset sums are distinct (OEIS A276661). Exact
values were previously known for `n ≤ 9`; for `n = 10` the Conway–Guy
construction gives `f(10) ≤ 309`, conjectured sharp, and OEIS recorded
`f(10) > 220`. We (i) re-derive `f(1..9) = 1, 2, 4, 7, 13, 24, 44, 84, 161`
from scratch with three mutually node-count-verifying implementations,
enumerating *all* optimal sets at each level; (ii) push the certified
frontier to **`f(10) > 262`** — 102 exhausted maxima `m = 161..262`,
166,893,497,453 search-tree nodes in 2.87 h of 4-thread wall time — by
exhaustive branch-and-bound over each possible maximum `m`; (iii) rule
out every witness below 309 whose deficiency profile lies within
L1-distance 8 of the Conway–Guy profile (19,125,539 sets); (iv) record the
empirical growth law of the search tree (~×1.20 per unit of `m` in the
probed range), which prices the full `a(10)` decision at CPU-months on
commodity cores and makes the multi-`m` deficiency-vector engine sketched
in §6 the natural next step.

## 1. The problem

A set `S = {a_1 < ... < a_n}` of positive integers has **distinct subset
sums** (DSS) if `A ↦ Σ_{i∈A} a_i` is injective on subsets. Erdős (1931;
problem #1 of the Erdős problems database, $500) asked whether
`max S ≥ c·2^n` for an absolute `c > 0`. The powers of two give
`f(n) ≤ 2^{n-1}`; Conway–Guy (1967) constructed better sets, and Bohman
(1996) proved every set in their sequence is DSS, with the best asymptotic
upper bound `f(n) ≤ 0.22002·2^n`. In the other direction the second-moment
method of Erdős–Moser gives `f(n) ≥ c'·2^n/√n`, with the record constant
`√(2/π)` (Elkies–Gleason, unpublished; re-proved by Dubroff–Fox–Xu 2021 and
Steinerberger 2023). All statements in this paragraph are (secondary).

Known exact values (A276661): `f(1..9) = 1, 2, 4, 7, 13, 24, 44, 84, 161`,
due to Lunnon (1988, exhaustive for `n ≤ 8`) and J. P. Grossman (`n = 9`;
his optimal set is the 9-element Conway–Guy set). (secondary)

Everything below is self-contained: no claim depends on any of the
secondary facts except where explicitly noted.

## 2. Certified results

**Theorem 1 (ladder, CERTIFIED).** For `n = 2..9`, exhaustive search over
every possible maximum `m` proves
`f(n) = 2, 4, 7, 13, 24, 44, 84, 161` respectively, and the complete lists
of optimal sets (those with largest element `f(n)`) are as recorded in
`data/optimal_sets.txt`; in particular the counts of optimal sets for
`n = 2..9` are as in that file. This re-derives the known ladder without
assuming it (the OEIS values enter only as *assertions to be matched*, and
as search-pruning floors for *later* levels, in increasing order of `n` —
see the bootstrap note in §3).

**Theorem 2 (frontier, CERTIFIED).** No 10-element DSS set has largest
element `≤ 262`. Hence `f(10) > 262`. Combined with the validated
Conway–Guy witness (Theorem 3(i)), `262 < f(10) ≤ 309`.
*Every row of `data/n10_sweep.csv` with status NONE is an independent
statement of this form for its own `m`; the theorem is the union of the
contiguous cleared prefix.*

**Theorem 3 (witness side, CERTIFIED).**
(i) The Conway–Guy 10-set `{148, 225, 265, 285, 296, 302, 305, 307, 308,
309}` is DSS (verified by brute enumeration of all 1024 sums), so
`f(10) ≤ 309`.
(ii) Writing a 10-set with maximum `m` as `{m − d_9, ..., m − d_1, m}` with
deficiencies `0 < d_1 < ... < d_9 < m`, there is **no** DSS set with
`m ≤ 308` whose deficiency vector `d` satisfies
`Σ_i |d_i − u_i| ≤ 8`, where `u = (1, 2, 4, 7, 13, 24, 44, 84, 161)` is the
Conway–Guy deficiency profile. (19,125,539 candidate sets checked exactly.)

**Lemma 4 (second-moment floor, PROVED — classical method).** Every
`n`-element DSS set satisfies `Σ a_i² ≥ (4^n − 1)/3`. Consequently
`f(10) ≥ 192` and `f(11) ≥ 362`.

*Proof.* For `ε ∈ {−1, +1}^n` uniform let `X = Σ ε_i a_i`. The map
`A ↦ ε(A)` (signs +1 on `A`) is a bijection from subsets to sign vectors,
and `X(A) = 2·S_A − Σa_i`, so DSS forces the `2^n` values of `X` to be
distinct; they are also all congruent to `Σ a_i (mod 2)`, and the value
multiset is symmetric under negation, so `E[X] = 0` and
`E[X²] = Σ a_i²` (independence). Write each value as `2y + c` with `c` the
common parity bit: the `y`-values are `N = 2^n` distinct integers, and
`E[X²] = Var(X) = 4·Var(y-multiset)`. Among `N` distinct integers the
variance is minimized by `N` consecutive integers (exchange argument: if
the sorted values have a gap `> 1`, shrinking the gap moves the two blocks
closer to the common mean and strictly decreases the sum of squared
deviations), and `Var({0,...,N−1}) = (N²−1)/12`. Hence
`Σ a_i² ≥ 4(N²−1)/12 = (4^n−1)/3`. For `n = 10`: the ten elements are
distinct, so `Σ a_i² ≤ Σ_{j=0}^{9} (m−j)² = 10m² − 90m + 285`, and
`10m² − 90m + 285 ≥ 349,525` forces `m ≥ 192` (the root is ≈ 191.44).
For `n = 11`: `11m² − 110m + 385 ≥ (4^{11}−1)/3 = 1,398,101` forces
`m ≥ 362` (root ≈ 361.5). ∎

The bound `f(10) ≥ 192` is strictly weaker than Theorem 2 and is stated
because the engine uses it as a prune (P3) and because its `n = 11`
instance is the current analytic floor for the next open value
(`f(11) ≤ 594` from Conway–Guy).

## 3. The search and why it is exhaustive

Fix `n` and the exact maximum `m`. The engine constructs candidate sets in
strictly decreasing order `a_n = m > a_{n-1} > ... > a_1 ≥ 1`, maintaining
for the chosen suffix `T` the bitset of its achievable subset sums (engine
v2) or, equivalently, the set `D(T)` of pairwise differences of achievable
sums (engine v3). A run at `(n, m)` reports FOUND with all solutions, or
NONE with per-depth node counts; sweeping `m` upward from `f(n−1)`, the
first FOUND is `f(n)`.

**Completeness of the incremental collision test (P4).** Adding a new
smallest element `a` to suffix `T` preserves DSS iff no achievable sum of
`T` plus `a` equals another achievable sum, i.e. iff
`sums(T) ∩ (sums(T) + a) = ∅`, i.e. iff `a ∉ D(T)`. Any collision in a
final set is detected at the moment its largest-index differing element is
added, so a leaf is reported iff the full set is DSS. (Induction on the
suffix; both engine representations implement the same test.)

**Difference-set update (engine v3).** If `S' = S ∪ (S + a)` then
`D(S') = D(S) ∪ (D(S)+a) ∪ (D(S)−a)|_{>0} ∪ (a−D(S))|_{>0} ∪ {a}` —
the four cases are: both sums in `S`; both in `S+a`; cross pairs, whose
differences are `|a + d|` or `|a − d|` for `d ∈ D(S) ∪ {0}`. The engine
maintains `D` and its bit-reversal `R` in a fixed frame so the reversed
term is two machine shifts; bits shifted beyond the frame cannot occur as
differences (the frame bounds the largest achievable sum).

**Prunes (all exact, integer-only):**
- **P1 (position floors).** In a DSS set, the bottom `r` elements form an
  `r`-element DSS set whose maximum is the `r`-th smallest element; hence
  the next element to be chosen (largest remaining) is `≥ f(r)`.
  *Bootstrap honesty:* the level-`n` run consults `f(r)` only for
  `r ≤ n − 1`, and `ladder.py` establishes those in increasing order of
  `n` before any level uses them; a mismatch at any level aborts the run.
- **P2 (sum).** `2^n` distinct nonnegative subset sums live in
  `[0, Σ a_i]`, so `Σ a_i ≥ 2^n − 1`; at a node, the maximum achievable
  remaining sum bounds the check.
- **P3 (second moment).** Lemma 4; at a node, the maximum achievable
  remaining `Σ a²` bounds the check.
- **Tight caps (v3 `--tight`).** Since `D` only grows down the tree, any
  future element lies in `V = [1, c−1] \ D(T)` (`c` = current minimum).
  The `r` remaining elements are `r` distinct members of `V`, so `|V| ≥ r`
  and the sums/squares of the `r` largest members of `V` below the current
  candidate cap the achievable remainders in P2/P3. `V` is *not* truncated
  at `f(r)`: only the largest remaining element must clear `f(r)`.
  All these conditions are monotone along the descending candidate
  iteration, so failures terminate the loop; none can cut a completable
  branch (each is a necessary condition on any completion).

**Determinism.** A NONE run traverses the entire pruned tree; its per-depth
node counts are traversal-order-independent, hence comparable across
implementations and thread schedules. FOUND runs in exists-mode stop
early; the ladder therefore re-runs each hit in `--enum` mode (full
traversal), which restores comparability and yields all optimal sets.

## 4. Verification architecture

Four implementations of the identical tree (v2 `dss_search.c`; its
pre-optimization snapshot `dss_search_basic.c`; v3 `dss_search3.c` in
default mode; `dss_reference.py` in Python with bigint bitsets), plus a
zero-cleverness brute validator (`validate_set.py`) with positive controls
(all known optimal sets `n = 4..9`, the Conway–Guy 10-set, the Conway–Guy
recurrence itself) and negative controls.

Equality checks performed (all PASS):
- v2 ≡ basic: 42 full-traversal cases (`n = 4..8` sweeps + enum runs) —
  identical statuses, node counts, solution lists.
- v2 ≡ v3-default: same 42 cases, plus `n = 9, m ∈ {150, 155}`
  (429,697,049 and 769,328,147 nodes, identical per-depth profiles).
- v2 ≡ Python reference: exhaustive for every `m` in every sweep `n ≤ 7`,
  plus enum runs (identical node counts and solution lists).
- v3-tight vs v2: statuses and solution sets identical on all 42 cases
  (node counts differ by design — tight mode prunes more).
- Every solution reported by any engine is re-validated by brute
  enumeration, and each `f(n)` is compared against A276661.
- Positive filter control: Grossman's optimal 9-set is *found* by the
  `n = 9, m = 161` enum run.

Hardware and cost: 4 cores (shared cloud sandbox), 15 GB RAM, gcc 13.3,
`-O3 -march=native -fopenmp`. Certified costs: the full ladder
(`n = 2..9`, every sweep plus enum reruns, with the Python cross-checks)
took 2,991 s wall on 4 threads with engine v2; `n=10` probes: `m=230`:
1.1×10⁸ nodes / 16 s; `m=250`: 4.5×10⁹ nodes / 566 s (both 4 threads,
tight mode). No floating point exists anywhere in any engine's critical
path (`time` fields excepted); all arithmetic is 64-bit integer with
magnitudes bounded by `3·(nm)² < 2^63`.

## 5. Numerical observations (not certified)

- **Tree growth.** Between `m = 230` and `m = 250` the tight-mode tree
  grows ×40.4, i.e. ×1.203 per unit of `m`; over the final certified
  stretch `m = 250..262` the measured rate eased to ×1.138 per unit
  (21.2×10⁹ nodes at `m = 262` alone). Even at the gentler rate the
  remaining range to 308 costs ~10²·⁶ ≈ 400× the `m = 262` instance —
  CPU-months on this box. This prices the full `a(10)` decision and
  motivates §6.
- **Optimal-set multiplicities** (CERTIFIED by the enum runs; listed in
  `data/optimal_sets.txt`): for `n = 2..9` the numbers of optimal sets are
  `1, 2, 1, 2, 1, 1, 3, 1`. In particular the optimal set is UNIQUE at
  `n = 9` and equals Grossman's (= the 9-element Conway–Guy set), while
  `n = 8` has three optimal sets, two of them not of Conway–Guy shape
  (`{20,40,71,77,80,82,83,84}`, `{39,59,70,77,78,79,81,84}`). Whether
  these multiplicities were previously published is unknown to this
  session (Lunnon's paper was unreachable) — *possibly known* for
  `n ≤ 8`; the `n = 9` uniqueness may be new (Grossman's value is an OEIS
  credit line, not a paper).
- **Annealing fails its positive control.** Simulated annealing over
  10-sets (uniform + local ±δ moves, exact collision-count energy) stalls
  at energy 3–5 and cannot rediscover any DSS set even with the cap at
  309, where the Conway–Guy witness exists. Near-optimal DSS sets appear
  to be isolated points of the move graph. Consequently no heuristic
  evidence about `f(10) < 309` can be extracted this way, and none is
  claimed.

## 6. Open threads

1. **Finish `a(10)`.** Resume `sweep10.py` in future sessions; every
   completed `m` is a permanent certified row. Projected completion needs
   either ~10³ core-hours or the engine below.
2. **Multi-`m` deficiency engine (sketch).** Parametrize sets as
   `{m − d_i}` and search over deficiency vectors `d`. Collisions between
   equal-cardinality subsets impose conditions on `d` alone — independent
   of `m` — while a collision between subsets of cardinalities differing
   by `k ≥ 1` excludes exactly the single value `m = (Δ_D)/k` for the
   corresponding deficiency difference. One tree over `d` with per-node
   alive-`m` intervals (clipped by the P2/P3 inequalities, which are
   monotone in `m`) plus finite exclusion lists would replace ~150 per-`m`
   trees; the k-graded difference structure needs `n` bitsets per node.
   Projected ~5–10×; unimplemented.
3. **`f(11) ∈ [362, 594]`** (Lemma 4 + Conway–Guy): once `a(10)` closes,
   the same machinery applies with `f(10)` as the new P1 floor.
4. **Multiplicity question.** The optimal set is unique at
   `n = 4, 6, 7, 9` but not at `n = 3, 5, 8` (counts 2, 2, 3). Is there
   structure in which `n` admit non-Conway–Guy optima (as `n = 5, 8` do)?
   What is the multiplicity at `n = 10` once `a(10)` closes?

## Disclosure

Run with substantial AI assistance (Claude, this repository's standing
setup). AI is not an author. Every labelled claim was machine-verified
in-session as described in §4; the session log records the failed
approaches (`log/2026-08-13-distinct-subset-sums.md`).
