# An attempt on Gilbreath's conjecture

*A research session, July 28, 2026. Code: `explore.py`, `verify.py`, `verify_big.py`,
`experiments.py`, `prefix_experiment.py`, `meanfield.py`.*

## 1. The conjecture

Write the primes in a row and repeatedly take absolute differences of adjacent
entries:

```
p   :   2   3   5   7  11  13  17  19  23  29  31  37 ...
d^1 :   1   2   2   4   2   4   2   4   6   2   6 ...
d^2 :   1   0   2   2   2   2   2   2   4   4 ...
d^3 :   1   2   0   0   0   0   0   2   0 ...
d^4 :   1   2   0   0   0   0   2   2 ...
```

**Conjecture (Proth 1878, Gilbreath 1958).** Every row after the first begins
with 1.

Formally, with `d_0(n) = p_n` and `d_{k+1}(n) = |d_k(n) - d_k(n+1)|`, the claim
is `d_k(1) = 1` for all `k ≥ 1`. Proth published a flawed proof in 1878;
Gilbreath rediscovered the pattern in 1958; it remains open. I chose it because
it sits on a fault line: it *looks* like a theorem about primes, but everything
below suggests it is really a theorem about statistics of prime gaps plus a
lucky seed — and because pieces of it are provable by elementary means today.

## 2. What I can prove

Throughout, a *sequence of Gilbreath type* is any `a_1 = 2 < a_2 < a_3 < ...`
with `a_i` odd for `i ≥ 2` (the primes after 2 qualify). Write row `k`'s first
entry as `L_k` (the *lead*) and its remaining entries as the *tail*.

**Lemma 1 (parity).** For any sequence of Gilbreath type and every `k ≥ 1`:
every tail entry of row `k` is even, and `L_k` is odd.

*Proof.* `|x−y| ≡ x+y (mod 2)`. Row 1 is `(a_2 − 2, a_3 − a_2, ...)`: the first
entry is odd−even = odd, the rest are differences of odd numbers, hence even.
If row `k` is (odd, even, even, ...), then row `k+1` begins `|odd − even|` =
odd and continues with differences of evens. Induct. ∎

So the lead is *forced* to be odd; the conjecture says this forced-odd value is
always the smallest possible, 1. Failure would mean some lead is 3, 5, 7, ...

**Lemma 2 (propagation).** If row `k` is `(1, e_1, ..., e_m)` with every
`e_i ∈ {0, 2}`, then row `k+1` is `(1, e'_1, ..., e'_{m−1})` with every
`e'_i ∈ {0, 2}`. Consequently rows `k, k+1, ..., k+m` all begin with 1.

*Proof.* `|1 − e_1| = 1` since `e_1 ∈ {0,2}`, and `|e_i − e_{i+1}| ∈ {0,2}`
for `e_i, e_{i+1} ∈ {0,2}`. Induct on the shrinking row. ∎

**Corollary 3 (verification criterion).** Since `L_k` depends only on
`p_1, ..., p_{k+1}`, the leads computed from the first `n` primes are the true
leads of the infinite triangle for `k ≤ n−1`. Hence if rows `1..k*` (computed
from the first `n` primes) all begin with 1 and row `k*` has an all-`{0,2}`
tail, then Gilbreath's conjecture holds for rows `1` through `n−1`. ∎

This is Odlyzko's strategy, and it is what makes the computations in §3
rigorous rather than heuristic.

For the dynamics it pays to halve the tail. By Lemma 1, tail entries are even;
write `u_k(j) = (j-th tail entry of row k)/2 ≥ 0`. The tail evolves
autonomously, `u_{k+1}(j) = |u_k(j) − u_k(j+1)|`, and the lead couples to it
only through `u_k(1)`. Call `u_k(j) ≥ 2` (original entry ≥ 4) a **defect**.

**Lemma 4 (reduction to boundary defects).** For a sequence of Gilbreath type,
the Gilbreath property (`L_k = 1` for all `k ≥ 1`) holds if and only if
`u_k(1) ≤ 1` for every `k ≥ 1`, i.e. no defect ever touches the left edge of
the tail.

*Proof.* `L_1 = 1` always (`a_2 = 3`). If `L_k = 1` then
`L_{k+1} = |1 − 2u_k(1)|`, which is 1 iff `u_k(1) ∈ {0,1}` and equals
`2u_k(1) − 1 ≥ 3` iff `u_k(1) ≥ 2`. Induct on the first failure. ∎

**Lemma 5 (defect descent).** If `u_{k+1}(j) ≥ 2` then `u_k(j) ≥ 2` or
`u_k(j+1) ≥ 2`. Defects are never created spontaneously: every defect heads an
ancestral chain of defects going back to row 1, whose position moves left by at
most one per row.

*Proof.* If `u_k(j), u_k(j+1) ≤ 1` then `|u_k(j) − u_k(j+1)| ≤ 1`. ∎

**Corollary 6 (finite, local cause of failure).** If the conjecture first fails
at row `K+1`, then `u_K(1) ≥ 2`, and by Lemma 5 there is an unbroken chain of
defects from some row-1 defect at position `m ≤ K` down to the edge — that is,
a prime gap `≥ 4` among the first `K+2` primes whose "descendants" survive `K−1`
difference steps while drifting `m−1` steps left. The conjecture is exactly the
statement that **no defect lineage ever reaches the left edge**. ∎

**Lemma 7 (parity rigidity / Sierpiński structure).** `u_{k+1}(j) ≡ u_k(j) +
u_k(j+1) (mod 2)`, so parities evolve *linearly*: `u_k(j) ≡ Σ_i C(k−1, i)
u_1(j+i) (mod 2)`. The parity table of the entire triangle is the XOR–Pascal
(Sierpiński) image of the prime gaps mod 4, hence fully deterministic and
governed by Lucas' theorem at dyadic scales. *(Verified computationally:
predicted vs. actual parities agree exactly on row 24 — see `meanfield.py`.)*

*Proof.* `|x−y| ≡ x+y (mod 2)`; iterate the linear recursion. ∎

**Proposition 8 (a toy universe, solved).** Let `a` be of Gilbreath type with
all gaps `a_{i+1} − a_i ∈ {2, 4}` for `i ≥ 2`. Then the Gilbreath property
holds if and only if `a_3 − a_2 = 2`.

*Proof.* Here `u_1(j) ∈ {1, 2}`, so `u_2(j) = |u_1(j) − u_1(j+1)| ∈ {0, 1}`:
row 2 has no defects, and by Lemma 5 no later row does either; by Lemma 4 the
only possible failure is at `k = 1`: `u_1(1) = (a_3 − a_2)/2`, which is ≤ 1
iff the first true gap is 2. ∎

Proposition 8 is a microcosm of the whole story: **the bulk takes care of
itself; only the left edge can kill you, and only early.**

## 3. Rigorous verification: the first 455 million rows

Using Corollary 3 (`verify.py`, `verify_big.py`; segmented odds-only sieve,
NumPy difference rows, int16):

| primes below | rows verified | k* (first all-{0,2} row) | 0.75·(ln n)² |
|---:|---:|---:|---:|
| 10⁵ | 9,591 | 65 | 63 |
| 10⁶ | 78,497 | 95 | 95 |
| 10⁷ | 664,578 | 135 | 135 |
| 10⁸ | 5,761,454 | 175 | 175 |
| 10⁹ | 50,847,533 | 248 | 233 |
| 10¹⁰ | 455,052,510 | **329** | 298 |

**Gilbreath's conjecture holds for at least the first 455,052,510 rows**
(106 seconds of difference rows after a 32-second sieve). Not a record:
Odlyzko verified it to π(10¹³) ≈ 3.46×10¹¹ rows in 1993, finding that row 635
of that triangle is all 0s and 2s. The point of my computation is the dynamics
below, not the bound.

The last column is an empirical law, **k*(n) ≈ 0.75 (ln n)²** (`n` = number of
primes), fit to the first four data points. Used as a genuine out-of-sample
prediction it gave 298 for the 10¹⁰ run before it finished; the actual value
was 329, so the law drifts low (−6% at 10⁹, −10% at 10¹⁰). Refitting a power
law to all six points gives exponent ≈ 2.1: **k* ≈ 0.63 (ln n)^2.1**, which
retrodicts Odlyzko's 635 at n ≈ 3.46×10¹¹ as ≈ 598 (−6%). The take-away is
robust even if the exact exponent isn't: k* grows *polylogarithmically* in n —
a slightly-super-quadratic power of log — which is why verification is cheap
and why the cooled front's lead over the left edge becomes astronomically safe
almost immediately. A (log n)²-ish scale is natural: the depth at which the
initial density of large gaps balances exponential per-row decay is a product
of two logarithms (gap size × decay horizon).

## 4. The dynamics: a branching process sitting on a knife's edge

Everything below is for the primes < 10⁸ (5.76M gaps) unless stated.

**Cooling front.** Let `f(k)` = length of the maximal all-{0,2} prefix of row
`k`'s tail. Lemma 2 localizes: the front can retreat by at most 1 per row, and
empirically it *explodes* — `f(k)` for k = 1, 13, 34, 55, 89, 144:
2, 97, 865, 4204, 31535, 733577 — roughly geometric growth ×1.1–1.2 per row.
The conjecture is equivalent to `f(k) ≥ 1` for all k (Lemma 4), and the front
races away from the edge so fast that nothing deep in the triangle ever
threatens it again.

**Defect decay.** The defect count decays exponentially, ~×0.936 per row
(measured over rows 20–140), reaching zero at k* = 175. Superposed on the decay
is a clean **period-4 oscillation** with per-row factors cycling roughly
(0.75, 1.6, 0.4, 1.5) — product ≈ 0.70 per 4 rows. The clock is Lemma 7's
Sierpiński structure: binomial parities `C(k, i) mod 2` reorganize at dyadic
rows, alternately splitting defects (a lone defect between two 0s has *two*
surviving children) and annihilating them.

**Criticality — why this conjecture is hard.** In deep rows the tail is
half 0s, half 2s (measured: P(0) = P(2) = 0.5000 at k ≥ 100, as parity
equidistribution predicts). A defect `u = 2` at position j has potential
children at j−1 and j, and a child survives essentially iff its gating
neighbour is 0. Under a mean-field (independence) assumption the expected
offspring is `2 × P(neighbour = 0) ≈ 2 × 1/2 = 1`: **the naive branching
process is exactly critical.** A critical branching population decays only
polynomially, and first-moment arguments cannot decide survival at all. The
observed decay (×0.936/row, i.e. effective offspring 0.936) lives entirely in
the *correlations*: measured mean offspring in even rows is 0.38–0.51,
compensated by expansion in odd rows — the Sierpiński clock plus
defect–defect interactions (adjacent defects annihilate: |2−2| = 0) push the
process just below criticality. Any proof must capture a correlation effect
that mean-field reasoning is structurally blind to. That, in one sentence, is
the wall I hit.

## 5. What the conjecture is *really* about: a seed plus statistics

Row k's lead depends only on the first k+1 primes, so shuffling all gaps after
position M can only affect rows ≥ M. Experiment (`prefix_experiment.py`): keep
the first M prime gaps, randomly permute the remaining ~5.7 million, and test
the full triangle. Five trials per M:

| M kept | trials passing | failure rows |
|---:|:--|:--|
| 0–8 | 0/5 each | fails at row ≈ M+1, immediately |
| 16 | 4/5 | one failure at row 36 |
| 32–256 | 5/5 | k* ≈ 164–205, same as true primes (175) |

Two conclusions. First, the conjecture is **not** about the multiset of gaps:
almost any rearrangement of the true prime gaps fails instantly if the first
few gaps are wrong. Second, given ~32 authentic initial gaps as a seed, the
property survived *every* tested rearrangement of the other 5.7 million gaps —
and an i.i.d. geometric gap model behaves identically. So empirically:

> **Gilbreath = (a benign seed of ~30 small early prime gaps) + (subcritical
> defect dynamics driven by gap statistics alone).**

The primes' role is oddly minimal: they must start 2, 3, 5, 7, 11, 13, ... (the
seed), and thereafter only their gap *statistics* matter. This sharpens, and
quantifies, Odlyzko's 1993 heuristic. The fragility is real: sequences as tame
as 2, 3, 7, 9, 11, 13, ... (gaps 1, 4, 2, 2, ...) violate the property at row 2
(Proposition 8).

## 6. Position relative to the literature

I did the computations and proofs above first and searched the literature
afterwards; here is where they land.

- Odlyzko, *Iterated absolute values of differences of consecutive primes*,
  Math. Comp. 61 (1993): verification to π(10¹³) rows via the same criterion
  (his row-635 certificate), plus the original statistical heuristic. My §3–§5
  are an independent, smaller-scale replication with new measurements (the
  (ln n)² law, the period-4 Sierpiński modulation, the seed-size threshold).
- Chase, *A random analogue of Gilbreath's conjecture*, Math. Annalen (2023,
  arXiv 2005.00530): the Gilbreath property holds a.s. for random sequences
  with slowly growing, sufficiently random gaps — the first rigorous version of
  "it's only statistics".
- Chase–Hunter–Tao, *Gilbreath's conjecture: a Cramér random model and a
  deterministic analysis* (arXiv 2607.08712, **July 2026** — seventeen days
  before this session): proves the a.s. Gilbreath property for the full
  Cramér random model (gap ranges up to o(n)), and a deterministic *inverse
  theorem*: failure to cool requires either enormous constant-parity blocks or
  persistent two-valued `{0, d}` blocks. Their "2-separated set" obstruction
  is the rigorous face of the same phenomenon my Lemma 5 + criticality
  analysis probes empirically: generic configurations cool, and only rigid,
  measure-zero structures can survive.

So the random-model half of the story is now theorems (not mine). The primes
case stays open because nothing known about primes rules out those rigid
obstructions — that would need gap-equidistribution input (Cramér-type
conjectures, or at least strong Hardy–Littlewood-with-uniformity information)
far beyond current unconditional technology.

## 7. Where my attempt stands

What I proved: Lemmas 1–7 and Proposition 8 — elementary but they organize the
problem completely: the conjecture is exactly "no defect lineage reaches the
left edge" (Cor. 6), parities are rigid (Lemma 7), and bounded-gap toy
universes are fully solvable (Prop. 8).

What I verified: the conjecture for the first 455 million rows (Cor. 3 makes
this rigorous), the (ln n)² law for k*, the seed threshold M ≈ 16–32, the
exact criticality of the mean-field branching picture, and the period-4
correlation mechanism that supplies the subcritical margin.

What I could not do — and what I believe a proof needs: an unconditional
handle on correlations of prime gaps mod 4 along Sierpiński-patterned index
sets, strong enough to show the defect branching process on the *actual* prime
gaps stays below its critical point uniformly in depth. First moments are
exactly critical; the theorem lives in the second-order structure. Even the
new Chase–Hunter–Tao inverse theorem, which reduces failure to two rigid
scenarios, still needs prime-gap inputs at Cramér strength to close the loop.

**Conclusion.** Gilbreath's conjecture survives this attempt intact — as it
has survived everyone's since 1878. I leave with proofs of the structural
lemmas, a rigorous half-billion-row certificate, two clean empirical laws, a
sharpened statement of *why* it is true, and an honest identification of the
missing ingredient: the conjecture is a statement about second-order
correlations of prime gaps, sitting one epsilon below a critical branching
threshold — and number theory does not yet own that epsilon.

---

# Part II. Engaging the Chase–Hunter–Tao program

*Continuation of the session: working directly from the CHT preprint
(arXiv 2607.08712, July 9, 2026), read in full. Code: `block_audit.py`,
`ck_montecarlo.py`, `ck_exact.py`, `ck6_parallel.py`.*

CHT's Theorem 1.6 reduces Gilbreath (for row N−1, assuming Cramér-strength
gap bounds) to two hypotheses about the normalized-gap array: **(ii)** it
contains no all-zero block of length ~ log¹⁰N, and **(iii)** it contains no
{0,d}-valued block (d ≥ 2) of depth i and length ≫ 8^M·i with
M ≥ 10 log log N. Their continuous model (i.i.d. Exp(1) initial data) has
expected depth-i entries c_i, computed by them for i ≤ 3, with even
boundedness of (c_i) open. This part contributes on all three fronts.

## 8. First empirical audit of the CHT hypotheses on the primes

`block_audit.py` scans the *entire* normalized-gap array (every depth) for
the two dangerous structures. For primes < 10⁹ (N = 50,847,532 columns,
248 depths):

| CHT hypothesis | worst offender found | danger threshold | margin |
|---|---|---|---|
| (ii) zero-blocks | length **31** (depth 158) | log¹⁰N ≈ 3.1×10¹² | **10¹¹·⁰** |
| (iii) {0,d}-blocks | length 30, d=2 (depth 55); worst length/depth = 11 | 8^M ≈ 9.4×10²⁵ | **10²⁴·⁹** |

For primes < 10⁸ the corresponding worst cases are 29 and margin 10²³·⁷.
Two structural observations. First, the worst zero-block grew from 29 to 31
as the array grew 10× — exactly the logarithmic growth a coin-flip model
predicts (log₂ of array area ≈ 30 and 33): **the primes show no excess
tendency whatsoever toward the dangerous structures.** Second, the worst
length/depth ratio for {0,d}-blocks is attained at depth 1 and equals 11 —
five orders of magnitude below even a *hypothetical* threshold of 10⁶, let
alone 8^M. If the CHT criterion is ever to be closed unconditionally, these
are the two quantities that must be bounded; this audit documents that the
truth has room to spare by ~11 and ~25 orders of magnitude respectively.

## 9. The sign-chamber theorem for the continuous model

Computing the c_i exactly (§10) required decomposing the positive orthant by
the sign pattern of every intermediate difference. A byproduct is a clean
statement with a two-line proof, which I have not seen stated:

**Proposition 9 (all sign histories occur).** For every i ≥ 1, each of the
2^{i(i+1)/2} sign patterns σ = (s^t_j) of the intermediate differences
δ^t_j is realized on a full-dimensional cone of initial data in R^{i+1}_{≥0};
so the "Gilbreath sign arrangement" has exactly 2^{i(i+1)/2} chambers.

*Proof.* Build the array bottom-up. Set the bottom entry to 1. Given row
t+1 with positive entries and the desired signs s^{t+1}, define row t by
A^t_1 = T_t and A^t_{j+1} = A^t_j − s^{t+1}_j A^{t+1}_j; then
A^t_j − A^t_{j+1} has exactly the prescribed sign and absolute value, and
taking T_t large makes every entry of row t strictly positive. The top row
is the initial data. All constraints hold strictly, so a neighborhood of
this point lies in the same chamber. ∎

*(Verified computationally: chamber counts 2, 8, 64, 1024, 32768 for
i = 1..5 — all patterns feasible.)* The moral: in the continuous model there
is **no local sign obstruction at all** — every conceivable sign history of
a Gilbreath array actually happens. Whatever mechanism forces cooling, it is
global and statistical, never combinatorial. (Contrast the primes, where
Lemma 7's parity rigidity *does* constrain the integer array mod 2.)

## 10. New exact constants: c₄, c₅ (and c₆)

Method: on each sign chamber the bottom entry is a linear functional; over a
simplicial cone with integer rays w_k and s_k = ⟨1, w_k⟩, the exponential
integrals have closed forms |det W|·∏1/s_k and |det W|·(∏1/s_k)·∑ℓ(w_k)/s_k.
Chambers are enumerated by DFS, rays by exact integer double description,
triangulations use floating Delaunay for combinatorics only with all
arithmetic in ℚ, and the whole computation carries an exact certificate:
the partition identity ∑_σ Z_σ = 1, which held exactly in every run.
The pipeline reproduces CHT's c₂ = 7/9 and c₃ = 227/288, and then gives
two (three) constants beyond the state of the art:

- **c₄ = 778959731701 / 1447295850000 ≈ 0.53821684** — certified (∑Z = 1
  exactly; 1024 chambers).
- **c₅ = 14008668886481596262550223816901 / 25320304994525128311856832700000
  ≈ 0.55325784** — certified (∑Z = 1 exactly; 32,768 chambers).
- **c₆ = 0.448388672133… — now certified** (exact 153-digit-numerator
  fraction in `c6_certified.txt`). The first attempt lost 1.7×10⁻⁷ of
  measure to degenerate dim-6 Delaunay cross-sections and produced a value
  wrong by 1.25×10⁻⁷; the repaired pipeline
  (`ck_exact_certified.py`: two independent Delaunay projections
  cross-checked exactly, with an exact pulling-triangulation fallback via
  integer rank tests — exercised on 685,625 of the 2,097,152 chambers)
  achieves ∑Z = 1 exactly. Notably, the Monte Carlo could never have
  caught the original error (both values sit 0.8σ from it): only the
  algebraic certificate could.

Monte Carlo cross-checks: c₄ MC 0.538110(105) (−1.0σ vs exact), c₅ MC
0.553255(114) (−0.0σ). Denominator structure: the certified denominators
factor over small primes only (largest 17 for c₄, 47 for c₅ — inherited
from the ray coordinate sums), while the numerators contain huge prime
factors (1682418427; 36012002278872998104242220609) — the constants carry
no visible closed form. Neither sequence is in the OEIS. Note c₄ < c₅ <
c₃: the non-monotonicity CHT observed at c₂ < c₃ recurs at the next dyadic
scale — dips at binary digit sum 1, rises at digit sum 2 — a foreshadowing
of §12.

## 11. A pointwise lower bound — independently found, then discovered to
## be CHT's Proposition 2.1 (an honesty note)

Working from the statement of their Theorem 1.4 alone (partial sums
Σ_{k≤n} c_k ≥ log(n+e)), I derived a pointwise inequality: the left column
telescopes, a_{(i,1)} ≥ a_1 − S with S = Σ_{k<i} a_{(k,2)}; S involves only
a_2, a_3, ... and is therefore independent of a_1; Markov plus the Exp(1)
tail of a_1 then give c_i ≥ (1/2)exp(−2 Σ_{k<i} c_k).

On then reading their Section 2, this *is* their key inequality
(Proposition 2.1) — same telescoping, same independence observation — and
their finish is sharper: computing E[max(a_1 − S, 0) | S] = e^{−S} exactly
and applying Jensen gives c_i ≥ exp(−Σ_{k<i} c_k), which is strictly
stronger than my Markov version. So nothing in this section is new, and I
record it only for two reasons: (a) honesty — for half an hour I believed
it was a contribution, and the correction belongs in the record; (b) the
independent rediscovery of the exact mechanism their lower-bound theory
runs on, within an hour of reading the theorem statement, is at least
evidence that the mechanism is canonical. One consequence worth making
explicit (immediate from their Prop 2.1, not stated by them): if
c_k ≤ K/k for all large k, then c_i ≥ c·i^{−K} for every i — a polynomial
upper bound self-enforces a pointwise polynomial lower bound, so the decay
of c_i, whatever it is, cannot be punctuated by anomalous dips.

## 12. The digit-sum law: evidence that c_i ~ 1/i is the wrong conjecture

CHT's Remark 1.5 tentatively conjectures that c_i decays at the maximal
rate 1/i allowed by their Theorem 1.4, while noting they cannot prove even
boundedness. Their evidence was a 10⁶-sample Monte Carlo to i = 20
(Figure 1). I ran a tiered Monte Carlo to **i = 1023** (40M samples for
i ≤ 63, 6M to 255, 0.6M to 1023; `ck_montecarlo.py`, data in
`ck_montecarlo.csv`), anchored on the exact values of §10, with all four
known constants reproduced within 1.2σ. The data says something much more
interesting than 1/i:

**(a) The pure power law is dead in this range.** Weighted fit of
log(i·c_i) against a constant gives R² = −0.53 (worse than useless);
i·c_i is not remotely constant.

**(b) A geometric ladder in the binary digit sum.** Group i ∈ [64, 512]
by s(i) = number of ones in binary. Mean i·c_i climbs geometrically:

| s(i) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| mean i·c_i | 3.36 | 3.85 | 4.55 | 5.47 | 6.67 | 8.23 | 10.28 | 12.96 | 16.54 |

— a factor ρ ≈ 1.22 per additional binary 1. At i = 1023 (ten ones),
i·c_i = 20.7, exactly on the extrapolated ladder. The swing is large and
growing with scale: c₅₁₁/c₅₁₂ ≈ 4.7 between *adjacent* indices.

**(c) Subsequence exponents split.** Model-free log-log fits:
along i = 2^k, c_i ~ i^{−0.93}; along i = 3·2^k, i^{−0.94}; along
i = 2^k − 1 (all ones), **i^{−0.63}**; typical odd i, i^{−0.79}. The
decay exponent oscillates log-periodically with the binary structure of i
— there is no single power law.

**(d) Partial sums grow like a power, not a log.** S_n = Σ_{i≤n} c_i
fits **S_n = 10.84·n^{1/5} − 11.43** to three decimals at every dyadic
checkpoint n = 63, 127, 255, 511, 1023 (S ranges over 13.4 → 31.9 there),
while log(n+e) reaches only 6.9. Under c_i ~ C/i one would have
S_n ~ C log n; the observed growth is a clean power n^{0.2},
consistent with the typical exponent −0.8 from (c).

**(e) Finer fractal structure.** Adding the 2-adic valuation ν₂(i) to the
regression lifts R² from 0.49 to 0.68 (indices divisible by high powers of
2 are systematically low, odd indices high); the remaining residuals still
correlate with the *arrangement* of the binary digits (e.g. i = 2⁹ + 7
sits high, i = 2³·127 sits low), pointing to a genuinely self-similar
multiplicative structure over the binary expansion — a "digital
multifractal", not a power law with noise.

The mechanism is visibly Lucas/Sierpiński: a large initial value at
position m survives to depth i exactly on the odd-binomial pattern
(C(i,m) odd ⇔ m ⊆ i bitwise, giving 2^{s(i)} surviving channels), damped
by interaction with the bulk — the observed base ρ ≈ 1.22 in place of the
naive 2 measures that damping. Honest caveats: the range is i ≤ 1023;
the fitted drift term i^{+0.06..0.12} may be a finite-size transient; an
asymptotic turnover beyond the computationally accessible range cannot be
excluded, and CHT's Theorem 1.4 only *forces* S_n ≳ log n, which a later
flattening could still satisfy. But within the accessible range the
tentative c_i ≍ 1/i of Remark 1.5 is untenable, and the right conjecture
appears to be log-periodic: **c_i ≈ i^{−1} ρ^{s(i)} × (slowly varying)**,
equivalently a decay exponent oscillating between ≈ 0.63 (i = 2^k − 1)
and ≈ 0.94 (i = 2^k), with partial sums S_n ≍ n^{θ}, θ ≈ 0.2.

*Update (later in the session): the deep Monte Carlo to i = 4095
confirmed everything out of sample — the law fitted below 1024 predicts
the next two octaves with R² = 0.90, the partial-sum formula
extrapolates to 0.4%, and adjacent indices reach a ×6.8 ratio. The
refined analysis, the certified c₆, and the new Theorem 2 live in
NOTE.md, which supersedes §10–§12 as the presentable account.*

## 13. Where Part II stands

New in this session, against the 19-day-old state of the art:

1. **First empirical audit of the CHT deterministic criterion on the
   primes** (§8): both dangerous structures are 11 and 25 orders of
   magnitude below their thresholds up to 10⁹, growing at coin-flip rates.
2. **Proposition 9** (§9): all 2^{i(i+1)/2} sign histories occur —
   the continuous model has no combinatorial obstruction; cooling is
   irreducibly statistical.
3. **Two new exact constants** c₄, c₅ with exact certificates, a
   high-confidence c₆, and the certified chamber counts 2, 8, 64, 1024,
   32768, 2097152 (§10). None previously computed or catalogued.
4. **An honest rediscovery** of their key lower-bound inequality (§11) —
   recorded as such, not claimed. Later in the session the rediscovery
   paid off: pushing the same mechanism through *both* ends of the
   triangle (reversal symmetry + the identity |A−B| = (A−B)⁺ + (B−A)⁺)
   proved **c_n ≥ 2·exp(−Σ_{k<n} c_k)** for n ≥ 2 — a factor-2
   sharpening of their Proposition 2.1, hence Σ_{i≤n} c_i ≥
   log(2n − 2 + e²), improving their Theorem 1.4 by an additive log 2.
   Full statement and proof in NOTE.md (Theorem 2); every step verified
   numerically at n = 6 on 4×10⁶ samples.
5. **The digit-sum law** (§12): quantitative evidence that the c_i decay
   is log-periodically modulated by the binary expansion of i, that
   partial sums grow like n^{1/5} in the accessible range, and that the
   natural refinement of their Remark 1.5 is c_i ≈ i^{−1}ρ^{s(i)} with
   ρ ≈ 1.22 — a concrete, falsifiable conjecture their own framework can
   now be pointed at.

What I could not do remains what nobody can do: rule out the two CHT
failure scenarios for the actual primes unconditionally — that still needs
prime-gap equidistribution far beyond current technology. But the model
side has moved: the constants exist now, the sign geometry is understood,
and the c_i question has sharpened from "does it decay like 1/i?" to "why
does the binary expansion of the depth govern the decay, and what is ρ?"
