# Session narrative — dissociated-subsets (2026-09-08)

## Why this problem

The day's survey (seven scouts; see `log/2026-09-08-dissociated-subsets.md`) put
Erdős Problem #963 third on the Erdős-database scout's list, with the suggestion of a
"window lemma" and a lottery-ticket search for a 16-set with no dissociated 4-subset.
Reading the thread changed the picture: the participants had been computing with
positive integers in short windows, but the problem is stated for `A ⊂ ℝ`, and sign
flips and zero can only hurt a dissociated subset. That gives `f(n) = g(⌈(n−1)/2⌉)`
at once (Lemma 2.1 in the NOTE), turns BAKKAOUI's `f(13) ≤ 4` into `f(13) = 3`, and —
the real point — makes Erdős's `⌊log₂ n⌋` question equivalent to a chain of single
finite statements, one per `k`: do `2^{k−1}` distinct positive reals always contain a
dissociated `k`-subset? For `k = 4` that is a question about 8 (in fact 7) real
numbers and the six ±1 relations a sorted 4-set can carry: an exact case analysis over a
hyperplane arrangement, the kind of computation this repository's tooling is built for.
Selected over the two other slate items (Question 7.1 of arXiv:2609.05259, run as a
hedge and answered — see `conjectures/equitable-total-colorings/`; and MathOverflow
514772, passed over) because it carried both a theorem and a decision.

## The morning: `k = 4`

Engine A (`code/dissoc_search.py`) was written first: sorted coordinates, an integer
basis of the current subspace, six relations per 4-subset, fail-first branching, exact
Fourier–Motzkin at the leaves. Positive controls: `k = 3` gives `g(3) ≤ 2 < 3 ≤ g(4)`
(the hand proof), `k = 4` finds the 5- and 6-element families (`{1,2,3,5,7}`,
`{1,2,3,5,7,8}` and its one-parameter family, `{1,…,6}`). Then `m = 7`: 290 nodes, no
feasible leaf — **every 7 distinct positive reals contain a dissociated 4-subset** —
in under a second, before noon.

Because a single implementation is not evidence, engine B was written from scratch
with different choices everywhere (row-echelon relation matrix, prefix-first branching,
float LP whose verdicts are only accepted after an exact rational certificate — a point
for "feasible", a Gordan vector for "infeasible" — with sympy's exact simplex as the
fallback). It agrees: 1099 nodes, no solution. Engine C combined A's branching with B's
pruning, added memoisation on the canonical row-reduced form of the subspace (the same
subspace is reached by many relation orders), and emits JSON certificates; engine D
(below) gives a fourth agreeing tree. `code/checker.py` — no shared code, exact
arithmetic, recomputes the relation patterns, checks every branching for
exhaustiveness, every pruning for a valid certificate (computing a Gordan vector itself
when a file carries none), and brute-forces every witness — verifies all shipped
certificates (`data/checker_log.txt`). The k = 4 theorem was therefore CERTIFIED by
about 12:45 UTC, with the exact table of `f(n)` for `n ≤ 27` as a corollary.

A hand proof was considered and not written: engine D's 62-node tree (split on the four
smallest elements; in the dissociated branch every other element is a signed sum) is a
proof skeleton, but the one-parameter families of 6-sets make a written case analysis
long, and the time was better spent on `k = 5`.

## The afternoon: `k = 5`

The relation count per sorted 5-subset is 26 (hand count and generator agree). Engine A
without LP pruning stalls at `m = 8` (almost every leaf infeasible); engine B finds
sets with no dissociated 5-subset for `m ≤ 10` but its tree grows ~40× per element;
engine C with memoisation grows ~4.7× per element (627 and 2 954 nodes to the first
family at `m = 10, 11`). Extrapolated, an exhaustive `m = 16` run was days away.

The structural way out is Lemma 3.3: once a 4-subset is dissociated, every other element
is one of its signed sums, and the subspace dimension collapses to 4. Engine D branches
seven ways on a 4-subset (six relations, or "dissociated" — after which only the 20
patterns involving the new element are allowed for the 5-subsets through it). It finds
families at `m = 10, 11, 12` in 0.6 s, 2.3 s and 128 s, and rediscovers BAKKAOUI's
`{1,…,10,12,13,15}` as the first solution at `m = 13` — after 60 590 nodes and
27 minutes, which rules it out for an exhaustive `m = 14` today.

Engine E abandons the sorted-order formulation: it works in the 4-parameter space of a
dissociated 4-set `T`, enumerating sets of sign vectors in `{−1,0,1}^4` in canonical
order, with at most three independent integer cuts of the parameter before everything
becomes integer arithmetic. Two exact reductions keep it small: `T` may be taken inside
the 7 smallest elements (Theorem 4.1), so at most three chosen vectors may be "certainly
below `t_4`" on the whole cone (59 of the 80 vectors are); and cached rational sample
points of the current region settle most positivity and cut-feasibility questions
without an LP. A profile showed the first version spending 95 % of its time in
Fraction-based rank tests — replaced by integer kernel products. Its exhaustive `k = 4`
run reproduces `m_4 = 7` and the six-element families in seconds. Two exhaustive `k = 5`
runs (forward and reversed candidate order) were launched at 13:00 UTC with a 2.5-hour
cap; both reached 12 within five minutes. Their final state is recorded in the README.

In parallel, a one-core annealing hedge (`code/sa/`) searched integer sets directly:
nothing with `d ≤ 4` beyond 13 elements (the best 14-sets keep 7 dissociated 5-subsets),
but a new record on the `k = 6` side, `A₂₄ = {1,…,21,24,25,27}` with `d = 5`, one more
element than the interval bound, verified by two independent exact programs.

## What failed

- **Engine A at `k = 5`**: no feasibility pruning inside the tree; abandoned at `m = 8`.
- **Engine B at `k = 5`**: prefix-first branching explodes (16 553 nodes at `m = 10`);
  used only as a cross-check for `k = 4`.
- **Engine C at `k = 5`**: 4.7× growth per element even with memoisation; the fail-first
  scan (up to 24 candidates × 26 relations of exact linear algebra per node) costs
  20–30 ms per node; changing the scan width barely moves the node count.
- **Engine D at `k = 5`**: correct and certified, but the sorted-order branching over
  20–26 patterns per 5-subset makes `m = 13` a 27-minute search for the *first* family.
- **Engine E, first version**: 7 nodes per minute (Fraction rank tests); second version
  ~150 nodes per minute; the exhaustive enumeration size at `k = 5` is not known in
  advance. Whether it finishes inside the session is recorded in the README.
- **A general theorem**: applying the signed-sum lemma to all dissociated `(k−1)`-subsets
  at once should beat the greedy `m_k ≤ (3^{k−1}+1)/2`; no argument was found.
- **Operations**: three shell commands killed themselves through `pkill`/`pgrep`
  patterns matching their own command line (the same wound the 2026-09-01, 09-05 and
  09-07 logs record); the last one also killed a batch of launches. Use PIDs, bracketed
  patterns, and never launch and kill in the same command.

## Labels, in one place

PROVED: the reduction lemma, the greedy and interval bounds, the signed-sum lemma, the
exact table of `f(n)` for `n ≤ 27` *given* the certified theorem. CERTIFIED: `m_4 = 7`
(four engines, checker-verified trees), the `k = 5` witnesses for `m ≤ 13`, `A₂₄`.
NUMERICAL: the annealing non-findings. Nothing here is claimed for `k = 5` beyond what
the README's status line says.
