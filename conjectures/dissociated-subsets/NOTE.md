# Dissociated subsets of small sets of reals (Erdős Problem #963)

Research note, session of 2026-09-08. AI-assisted (Claude); every proof below was
re-read by hand before it was labelled, every computation ships its code, and the
case-tree certificates are checked by an independent program.

## Abstract

A set `B` of reals is *dissociated* if its `2^|B|` subset sums are distinct. Erdős
(1965; Erdős Problems #963, Vaughan's list 1.22) defined `f(n)` as the largest `k`
such that every `n`-element set `A ⊂ ℝ` contains a dissociated subset of size `k`,
noted the greedy bound `f(n) ≥ ⌊log₃ n⌋`, and asked whether `f(n) ≥ ⌊log₂ n⌋`.
KoishiChan's argument on the problem page (December 2025) gives
`f(n) ≥ (1−o(1)) log₂ n` asymptotically; the inequality itself, and every exact value
of `f`, were open.

We (i) reduce `f` to sets of distinct positive reals, `f(n) = g(⌈(n−1)/2⌉)` (Lemma 2.1,
PROVED), where `g(m)` is the same minimum over `m` distinct positive reals — so the
question is equivalent to `g(2^{k−1}) ≥ k` for all `k`; (ii) decide the first open
instance by an exact, machine-checked case analysis over the hyperplane arrangement of
±1 relations: **every 7 distinct positive reals contain a dissociated 4-subset, and
6 do not always** (Theorem 4.1, CERTIFIED); hence `f(n)` is known exactly for all
`n ≤ 27`, Erdős's inequality holds for all `n ≤ 31`, and it is *strict* at `n = 14, 15`;
(iii) give the structural lemma behind the searches (every element of a set with no
dissociated `k`-subset is a signed sum of any dissociated `(k−1)`-subset), and (iv)
report the first non-interval records on the upper side: a 24-element set with no
dissociated 6-subset (CERTIFIED), and the state of the `k = 5` threshold `m₅ ∈ {14, …}`
(Section 5).

## 1. Definitions

For a finite `B ⊂ ℝ`, `B` is **dissociated** iff all sums `Σ_{b∈S} b`, `S ⊆ B`, are
distinct; equivalently iff no nonzero `ε ∈ {−1,0,1}^B` has `Σ ε_b b = 0` (take
`ε = 1_S − 1_T` for two subsets with equal sums, and conversely). Write

* `d(A)` for the size of the largest dissociated subset of a finite `A ⊂ ℝ`;
* `f(n) = min { d(A) : A ⊂ ℝ, |A| = n }` (Erdős's function; `f(1) = 0` since `{0}`
  is not dissociated);
* `g(m) = min { d(P) : P ⊂ ℝ_{>0}, |P| = m }` for `m ≥ 1`, `g(0) = 0`;
* `m_k = min { m : g(m) ≥ k }`, the least size that forces a dissociated `k`-subset
  in positive sets.

Both `f` and `g` are non-decreasing (a larger set contains a smaller one). The
problem page states the question as: is `f(n) ≥ ⌊log₂ n⌋`?

## 2. The reduction to positive sets

**Lemma 2.1 (PROVED).** For every `n ≥ 1`, `f(n) = g(⌈(n−1)/2⌉)`.

*Proof.* Let `A ⊂ ℝ`, `|A| = n`, and let `P = {|a| : a ∈ A, a ≠ 0}` be its set of
distinct nonzero absolute values. (a) A dissociated set contains neither `0` (the
empty set and `{0}` have equal sums) nor a pair `{a, −a}`. (b) Dissociation is
invariant under changing the sign of any element: `Σ ε_b b = 0` iff
`Σ (ε_b s_b)(s_b b) = 0`, and `ε ↦ (ε_b s_b)` is a bijection of the nonzero sign
vectors. By (a), a dissociated `B ⊆ A` has `|B|` distinct absolute values, and by (b)
those absolute values form a dissociated subset of `P`; conversely a dissociated
subset of `P` lifts to a dissociated subset of `A` by choosing one preimage of each
absolute value. Hence `d(A) = d(P)`. Since `A` contains at most one zero and at most
two elements of each absolute value, `|P| ≥ ⌈(n−1)/2⌉`, so `d(A) ≥ g(⌈(n−1)/2⌉)`
by monotonicity of `g`. Equality is attained by `A = {0} ∪ P ∪ (−P)` for `n` odd and
`A = P ∪ (−P)` for `n` even, with `|P| = ⌈(n−1)/2⌉` and `P` extremal for `g`. ∎

**Corollary 2.2 (PROVED).** The following are equivalent: (i) `f(n) ≥ ⌊log₂ n⌋` for
all `n ≥ 1`; (ii) `g(m) ≥ ⌊log₂ m⌋ + 1` for all `m ≥ 1`; (iii) `g(2^{k−1}) ≥ k` for
all `k ≥ 1`; (iv) `m_k ≤ 2^{k−1}` for all `k ≥ 1`.

*Proof.* For `n = 2m+1` and `n = 2m` (`m ≥ 1`) Lemma 2.1 gives `f(n) = g(m)`, while
`⌊log₂(2m+1)⌋ = ⌊log₂(2m)⌋ = ⌊log₂ m⌋ + 1`; and `f(1) = 0 = ⌊log₂ 1⌋`. This gives
(i) ⇔ (ii); (ii) ⇔ (iii) by monotonicity of `g` (the values of `⌊log₂ m⌋ + 1` change
exactly at the powers of two), and (iii) ⇔ (iv) by the definition of `m_k`. ∎

So the question has a first open instance for each `k`: `k = 3` asks whether every 4
distinct positive reals contain a dissociated triple, `k = 4` whether every 8 contain a
dissociated 4-subset, `k = 5` whether every 16 contain a dissociated 5-subset.

## 3. Elementary bounds and the structure lemma

**Lemma 3.1 (greedy; PROVED).** `g(m) ≥ k` whenever `m ≥ (3^{k−1}+1)/2`; i.e.
`m_k ≤ (3^{k−1}+1)/2`. In particular `m_3 ≤ 5`, `m_4 ≤ 14`, `m_5 ≤ 41`, `m_6 ≤ 122`.

*Proof.* Induction on `k`; `k = 1` is trivial. If `B ⊆ P` is dissociated with
`|B| = k−1`, then `B ∪ {x}` fails to be dissociated only if `x` is a signed sum
`Σ_{b∈B} ε_b b` (the coefficient of `x` in a relation must be nonzero, and `B` itself
carries no relation). The positive signed sums of `B` number at most `(3^{k−1}−1)/2`
(nonzero signed sums come in pairs `±s`), so if `|P| ≥ (3^{k−1}+1)/2` some `x ∈ P`
extends `B`. ∎ (This is Erdős's `⌊log₃ n⌋` bound in the positive setting.)

**Lemma 3.2 (intervals; PROVED).** `g(m) ≤ d({1,…,m}) = max{ k : F(k) ≤ m }`, where
`F(k)` is the least possible largest element of a `k`-set of positive integers with
distinct subset sums (OEIS A276661: `F(1..9) = 1, 2, 4, 7, 13, 24, 44, 84, 161`,
`262 < F(10) ≤ 309`). Hence `g(m) ≤ 3` for `m ≤ 6`, `≤ 4` for `m ≤ 12`, `≤ 5` for
`m ≤ 23`, `≤ 6` for `m ≤ 43`; i.e. `m_k ≥ F(k)`.

*Proof.* A dissociated subset of `{1,…,m}` is a set of positive integers with distinct
subset sums and largest element `≤ m`. ∎ (The values `F(1..6)` and the row
`d({1..m}) = 1,2,2,3,3,3,4⁶,5¹¹,6` for `m ≤ 24` were re-computed from the definition,
`code/dissoc_search.py` and the session log; `F(7..9)` are cited from A276661,
Lunnon/Grossman, secondary.)

**Lemma 3.3 (signed sums; PROVED).** Let `P ⊂ ℝ_{>0}` have no dissociated `k`-subset
and let `T ⊆ P` be a dissociated `(k−1)`-subset. Then every element of `P` is a signed
sum `Σ_{t∈T} ε_t t`, `ε ∈ {−1,0,1}^T` (the elements of `T` being the unit vectors).

*Proof.* For `x ∈ P ∖ T` the set `T ∪ {x}` carries a relation; its coefficient on `x`
is nonzero since `T` carries none. ∎

Combined with Theorem 4.1 (every 7 positive reals contain a dissociated 4-subset),
Lemma 3.3 says that every set with no dissociated 5-subset and at least 7 elements is
`T ∪ (a choice of signed sums of T)` for a dissociated 4-set `T` — a 4-parameter
family. This is what makes the `k = 5` searches of Section 5 finite in a useful way.

**Lemma 3.4 (relations of a sorted subset; CERTIFIED, trivial to check by hand).**
For `0 < a_1 < a_2 < a_3 < a_4`, a nonzero sign vector `ε` can satisfy
`Σ ε_i a_i = 0` only in these six cases: `a_3 = a_1+a_2`, `a_4 = a_1+a_2`,
`a_4 = a_1+a_3`, `a_4 = a_2+a_3`, `a_4 = a_1+a_2+a_3`, `a_1+a_4 = a_2+a_3`.
For five sorted positive reals there are exactly 26 such patterns (10 of the form
`c = a+b`, 5 of the form `d = a+b+c`, 5 of the form `a+d = b+c`, `e = a+b+c+d`,
`e+a = b+c+d`, `e+b = a+c+d`, `e+c = a+b+d`, `e+d = a+b+c`, `c+d = a+b+e`).
The lists are generated by an exact feasibility test in every engine and re-derived
by the checker.

## 4. The first open instance: `m_4 = 7`

**Theorem 4.1 (CERTIFIED).** (a) Every set of 7 distinct positive reals contains a
dissociated 4-subset. (b) The 6-element sets `{1,2,3,4,5,6}`, `{1,2,3,5,7,8}`,
`{1,2,3,4,6,7}`, `{2,3,5,10,12,15}` (and the one-parameter families through them)
contain none. (c) Every 4 distinct positive reals contain a dissociated triple, and
`{1,2,3}` shows three do not. Hence `m_3 = 4`, `m_4 = 7`.

*Method.* Part (c) has a two-line proof: if no triple of `a_1<a_2<a_3<a_4` is
dissociated then `a_3 = a_1+a_2` and `a_4 = a_1+a_2`, contradicting `a_3 < a_4`.
Part (a) is an exhaustive, exact case analysis. A sorted point `a ∈ ℝ^7` with no
dissociated 4-subset must satisfy, for each of the 35 four-subsets, one of the six
relations of Lemma 3.4. The search keeps a rational linear subspace `S` (the relations
chosen so far, as an integer basis), calls a 4-subset *blocked* on `S` if one of its
relations vanishes identically on `S`, and, while some 4-subset is unblocked, branches
on its six relations (each child is `S ∩ r^⊥`, of dimension one less). A child on which
some `a_i = 0` or `a_i = a_j` is forced is discarded; a child (or a leaf where every
4-subset is blocked) whose subspace does not meet the open cone
`{0 < a_1 < … < a_7}` is discarded with an explicit Gordan certificate
(`λ ≥ 0`, `λ ≠ 0`, `Σ λ_i c_i ∈ span(relations)` for the cone rows `c_i`), found by
Fourier–Motzkin elimination or by a floating LP whose dual is rationalised and verified
exactly. A feasible leaf is a counterexample family and yields an explicit rational
witness. Soundness: every valid point on `S` lies on one of the six relations of the
branching subset, hence in a child.

Three independent engines agree on (a) and (b): engine A (fail-first branching,
Fourier–Motzkin leaves: 290 nodes), engine B (row-echelon state, prefix-first
branching, LP pruning with exact certificates at every node: 1099 nodes), engine C
(fail-first + certified LP pruning + subspace memoisation: 111 nodes), and engine D
(the dissociation case split of Section 5, applied with `k = 4`: 62 nodes). Engines
A, C and D write their case trees as JSON certificates, and `code/checker.py` — no code
shared with the engines, exact rational arithmetic throughout — re-derives the six
relation patterns, verifies that every branching is exhaustive, every forced-equality
pruning is a true linear consequence, every infeasible leaf or pruned child has a valid
Gordan certificate (recomputing one when the file carries none), and every witness is a
sorted positive point of its subspace whose largest dissociated subset really is smaller
than 4. Checker output for the shipped certificates is in `data/checker_log.txt`.

**Corollary 4.2 (PROVED given Theorem 4.1).** `g(m) = 3` for `4 ≤ m ≤ 6`; `g(m) = 4`
for `7 ≤ m ≤ 13` (upper bound: `{1,…,12}` for `m ≤ 12` and BAKKAOUI's set
`{1,…,10,12,13,15}` for `m = 13`, both re-verified here); and therefore

| n | 1 | 2–3 | 4–7 | 8–13 | 14–27 | 28–31 |
|---|---|---|---|---|---|---|
| `f(n)` | 0 | 1 | 2 | 3 | 4 | ≥ 4 |
| `⌊log₂ n⌋` | 0 | 1 | 2 | 3 | 3 (n ≤ 15), 4 | 4 |

so `f(n) ≥ ⌊log₂ n⌋` holds for every `n ≤ 31`, with equality for `n ≤ 13` and
`16 ≤ n ≤ 27`, and strict inequality at `n = 14, 15`. (`f(28..31) = g(14), g(15)`
depend on Section 5.)

## 5. The `k = 5` threshold

By Lemma 3.2 and BAKKAOUI's 13-set, `m_5 ≥ 14`; by Lemma 3.1, `m_5 ≤ 41`; Erdős's
question at `n = 32, 33` is whether `m_5 ≤ 16`.

Three engines were run at `k = 5`. Engine C (sorted-cone case tree, certified LP
pruning) and engine D (the same, with the *dissociation case split*: a 4-subset `Q`
either carries one of its six relations, or is dissociated, in which case every other
coordinate is a signed sum of `Q` and only the 20 patterns involving the new element
are allowed for the 5-subsets `Q ∪ {x}`) both find explicit sets with no dissociated
5-subset for every `m ≤ 12` in seconds to minutes (witnesses in `data/witnesses.txt`,
all re-verified by brute force), e.g. `{1,2,3,5,6,7,8,9,10,12,13,15}` at `m = 12`;
the `m = 8` counterexample certificate of engine D is checker-verified. Engine E
works directly in the 4-parameter family of Lemma 3.3: the state is a set of sign
vectors in `{−1,0,1}^4` together with at most three independent integer cuts of the
parameter `t` (after three cuts `t` is a fixed integer point and everything is checked
numerically); it enumerates configurations in canonical order and prunes only with
exact certificates. Its exhaustive `k = 4` run reproduces `m_4 = 7` and all six-element
families.

*Status at the time of writing (see the README for the final state of the runs):*
SEE_SECTION_5_STATUS

## 6. The `k = 6` side: a 24-element set with no dissociated 6-subset

**Proposition 6.1 (CERTIFIED).** `A₂₄ = {1, 2, …, 21, 24, 25, 27}` has `d(A₂₄) = 5`:
`{1,2,4,8,16}` is dissociated and none of the `C(24,6) = 134 596` six-subsets is.
Hence `g(24) ≤ 5` and `m₆ ≥ 25`, one more than the interval bound `m₆ ≥ F(6) = 24`.

Found by simulated annealing over 24-subsets of `{1,…,40}` (`code/sa/sa.c`, seed 1,
8 s) and verified by two independent exact programs (`code/sa/dval.c`, a DFS over
dissociated subsets, and `code/sa/bruteforce_d.py`, which enumerates all six-subsets).
The same campaign found no 25-element set with `d ≤ 5` (best: 4 dissociated
6-subsets, `A₂₄ ∪ {22}`) and no 14-element set with `d ≤ 4` (best: 7 dissociated
5-subsets, `{1,…,13,15}`) — heuristic evidence only (NUMERICAL).

## 7. Open questions

1. `m₅`: is it 14? (Then `f(n) = 5` for `28 ≤ n ≤ 47` and Erdős's inequality holds for
   all `n ≤ 63`.) A completed exhaustive run of engine E, or of engine D on four cores,
   decides it; see the README for the state of the runs.
2. Is `m_k ≤ 2^{k−1}` for all `k` (Erdős's question in the form of Corollary 2.2)? The
   data `m_k = 1, 2, 4, 7` and `14 ≤ m₅ ≤ 41`, `25 ≤ m₆ ≤ 122` track the Conway–Guy
   thresholds `F(k) = 1, 2, 4, 7, 13, 24` closely (`m_k ≥ F(k)` always); if
   `m_k − F(k)` stays bounded the inequality holds with room to spare, since
   `F(k)/2^{k−1} → 0.44…`. This is an observation, not a conjecture we can support.
3. A human-readable proof of Theorem 4.1(a). Engine D's 62-node tree is the skeleton:
   split on `{a_1,a_2,a_3,a_4}`; in the dissociated branch every other element is a
   signed sum of it and the remaining checks are short; in the six relation branches
   recurse on `{a_1,a_2,a_3,a_5}` or `{a_2,a_3,a_5,a_6}`.
4. Sharper general bounds: Lemma 3.3 applied to *every* dissociated `(k−1)`-subset of
   `P` at once (there are many, since every 7 elements contain one for `k = 5`) should
   improve `m_k ≤ (3^{k−1}+1)/2`; we did not find the argument.

## References (all checked against the live page or entry on 2026-09-08 unless marked)

* T. F. Bloom, *Erdős Problem #963*, https://www.erdosproblems.com/963 (statement,
  status OPEN, greedy remark, comments by KoishiChan, T. Tao, Q. Tang, T. Bloom,
  Adenwalla, Z. Hunter, BAKKAOUI). The original sources are cited there as [Er65] and
  [Va99, 1.22] (secondary; not consulted).
* OEIS A276661 (least largest element of a `k`-set with distinct subset sums) and
  A005318 (Conway–Guy sequence); A201052 for `d({1..n})`.
* This repository, `conjectures/distinct-subset-sums/`, for `F(10) > 262`.
