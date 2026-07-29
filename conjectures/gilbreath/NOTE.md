# The fine structure of the Chase–Hunter–Tao constants:
# exact values c₄–c₆ and a two-parameter submask law

*Research note, July 28, 2026. Companion code and data in this directory;
full session narrative in WRITEUP.md.*

## Abstract

For the continuous model of Gilbreath's conjecture introduced by Chase,
Hunter and Tao (arXiv 2607.08712, July 2026) — iterated absolute
differences of i.i.d. Exp(1) initial data — we compute the expected
depth-i entry c_i exactly for i = 4, 5, 6, extending the exact values
c₀…c₃ of CHT, with computer-verified exactness certificates in ℚ. We
prove that the sign arrangement of the model has the maximal number
2^{i(i+1)/2} of chambers ("all sign histories occur"). A tiered Monte
Carlo to depth i = 4095, anchored on the exact values, reveals that the
sequence c_i is governed by the binary expansion of i through a
two-parameter **submask law**

    c_i  ≈  C · i^{−α} · Σ_{m ⊆ i} q^m ,        (⋆)

where the sum runs over binary submasks m of i (equivalently
Σ_{m⊆i} q^m = Π_{j: bit_j(i)=1} (1+q^{2^j})), with α ≈ 0.81, q ≈ 0.67.
The law explains the Lucas-theorem oscillation observed by CHT, fits with
R² ≈ 0.98 where a pure power law fails entirely (R² < 0), and implies
that the tentative conjecture c_i ≍ 1/i of CHT (their Remark 1.5) is
untenable in the computationally accessible range: partial sums grow like
S_n ≈ 10.8·n^{1/5}, not like log n, and the local decay exponent
oscillates log-periodically between ≈ 0.63 (i = 2^k − 1) and ≈ 0.93
(i = 2^k). On the rigorous side we prove a two-channel sharpening of
CHT's key inequality: c_n ≥ 2·exp(−Σ_{k<n} c_k) for n ≥ 2, whence
Σ_{i≤n} c_i ≥ log(2n − 2 + e²), improving their Theorem 1.4. Fitted
below depth 1024, the law predicts the next two octaves out of sample
with R² = 0.90, and the partial-sum formula extrapolates to 0.4%.

## 1. Setting

CHT define the Gilbreath array a_{(i,j)} by a_{(0,j)} = a_j (i.i.d.
Exp(1)) and a_{(i+1,j)} = |a_{(i,j)} − a_{(i,j+1)}|; by stationarity in j,
c_i := E a_{(i,j)} depends only on i. They compute c₀ = c₁ = 1,
c₂ = 7/9, c₃ = 227/288, note the non-monotonicity and its likely relation
to Lucas' theorem, prove Σ_{i≤n} c_i ≥ log(n+e) and the key inequality
c_n ≥ exp(−Σ_{i<n} c_i) (their Prop. 2.1), state that they cannot prove
boundedness of (c_i), and tentatively conjecture c_i ≍ 1/i (Remark 1.5,
supported by a 10⁶-sample Monte Carlo to i = 20).

## 2. Exact values

**Method.** Fix the sign of every intermediate difference: each of the
2^{i(i+1)/2} sign patterns defines a polyhedral cone in R^{i+1}_{≥0} on
which the depth-i entry is a linear functional ℓ. Over a simplicial cone
with integer rays w_k, s_k := ⟨1, w_k⟩,

  ∫ e^{−⟨1,x⟩} dx = |det W| Π_k s_k^{−1},
  ∫ ℓ(x) e^{−⟨1,x⟩} dx = |det W| (Π_k s_k^{−1}) Σ_k ℓ(w_k)/s_k .

Rays are computed by exact integer double description; triangulations are
found with two independent floating Delaunay projections used for
*combinatorics only* and cross-checked exactly against each other, with
an exact fallback ("pulling" triangulation via integer rank tests on the
cone's H-representation) whenever they disagree; all arithmetic in ℚ.
**Certificate:** the exponential measures of all chambers must sum to
exactly 1 in ℚ; this identity holds exactly in every reported run, and
the pipeline reproduces c₁, c₂, c₃.

**Proposition 1 (all sign histories occur).** Every one of the
2^{i(i+1)/2} sign patterns is realized on a full-dimensional cone.
*Proof.* Build the array bottom-up: set the bottom entry to 1; given row
t+1 > 0 and desired signs, define A^t_1 = T_t and A^t_{j+1} = A^t_j −
s^{t+1}_j A^{t+1}_j; taking T_t large makes row t positive, and all
constraints hold strictly. ∎ (Chamber counts 2, 8, 64, 1024, 32768,
2097152 confirmed computationally for i ≤ 6.) Consequently the continuous
model admits no combinatorial obstruction: whatever forces cooling is
statistical, not local-combinatorial.

**Results.**

| i | c_i | status |
|---|---|---|
| 2 | 7/9 = 0.7778 | CHT |
| 3 | 227/288 = 0.78819 | CHT |
| 4 | **778959731701/1447295850000 = 0.53821735…** | new, certified |
| 5 | **14008668886481596262550223816901/25320304994525128311856832700000 = 0.55325830…** | new, certified |
| 6 | **0.448388672133… (exact 153-digit/154-digit fraction, `c6_certified.txt`)** | new, certified |

c₆ required 2,097,152 chambers; 685,625 of them were routed through the
exact-fallback triangulation after the two Delaunay projections
disagreed, and the partition identity then held exactly (a first run
without the fallback machinery missed 1.7×10⁻⁷ of the measure and gave a
value wrong by 1.25×10⁻⁷ — caught by the certificate, not by the Monte
Carlo, which sat 0.8σ away in both cases; exactness auditing matters).
The denominators factor over small primes (≤ 17 for c₄, ≤ 47 for c₅,
≤ 331 for c₆ — inherited from ray sums); the numerators contain large
prime factors, so no closed form is apparent. None of these values or
their parts appear in the OEIS. Note c₆ < c₄ < c₅: the dyadic
non-monotonicity pattern deepens.

## 3. Monte Carlo to depth 4095

Tiered sampling (40M samples to depth 63, decreasing to 150k at 4095),
merged by minimal standard error; float32 difference arithmetic. Because
|diff| dynamics is chaotic, float32 and float64 trajectories decorrelate,
so precision was audited statistically: an independent 400k-sample
float64 run agreed with the float32 estimates at i = 255, 256, 511, 512,
1023 within 2.5σ (deviations +2.5, −2.1, +1.4, −0.2, +0.0σ, alternating
sign) — any arithmetic bias is ≲ 1–2%, versus the 20–370% structural
effects reported below. All exact anchors (c₀…c₆) reproduced within
1.2σ.

## 4. The submask law

Weighted regression of log(i·c_i) on the individual binary digits of i
(i ∈ [64, 1023]) gives R² = 0.953 with a *cascade* of per-bit factors:

| bit j | 0 | 1 | 2 | 3 | 4 | ≥5 |
|---|---|---|---|---|---|---|
| factor | 1.696 | 1.461 | 1.214 | 1.071 | 1.024 | ≈ 1 |

These are matched, within noise, by the one-parameter family
f_j = 1 + q^{2^j} at q ≈ 0.68 — which is exactly the statement that a
binary submask m of i contributes weight q^m:
Σ_{m⊆i} q^m = Π_{j∈i} (1+q^{2^j}). Fitting (⋆) directly:

- **q = 0.685, α = 0.798, C = 1.14, R² = 0.980** on i ∈ [64, 1023] —
  outperforming the 10-parameter free-bit model (0.953);
- adding one interaction term (× 1.019 per adjacent pair of set bits)
  raises R² to 0.982; the largest remaining residuals sit on indices with
  long runs of ones (i = 1023, 895, 959, …), i.e. cooperative
  channel effects beyond pairwise;
- cross-validation: parameters fitted on [64, 511] predict [512, 1023]
  with out-of-sample R² = 0.93 (mean |relative error| 9.8%);
- **out-of-sample test on [1024, 4095]:** fitted on [64, 1023] only
  (q = 0.670, α = 0.811), the law predicts all 3072 new values with
  R² = 0.90 (median |rel. error| 13%). The digit-sum ladder remains
  cleanly geometric at the new scale (11 rungs, ratio ≈ 1.20 per bit;
  mean i·c_i from 4.4 at s = 2 to 24.8 at s = 11), and adjacent indices
  now differ by ×6.8 (c₂₀₄₇ vs c₂₀₄₈). The one systematic deviation is
  itself informative: constant q under-predicts the extremes (all-ones
  indices measured 1.34–1.42× above the law, powers of two 0.73–0.83×
  below), i.e. the oscillation amplitude keeps *growing* with scale —
  the truth is more digit-structured than (⋆), not less;
- **tail-dependence (not universality):** with Uniform[0,1] initial data
  the oscillation nearly vanishes — c₁₂₇ ≈ c₁₂₈ within 1.5% (they differ
  by ×3.1 for exponential data) — and the decay is a cleaner power law
  with α ≈ 0.92. The Lucas channels are *activated by the unbounded tail*
  of the initial distribution: exponential data keeps supplying large
  values at every scale, bounded data starves the channels. Since the
  Cramér model for prime gaps is geometric (exponential-type tail), the
  exponential model — where the submask law is strong — is precisely the
  Gilbreath-relevant one.

## 5. Consequences for the decay of c_i

1. **c_i ≍ 1/i is untenable in the accessible range.** A pure power law
   has R² < 0 (worse than the mean); adjacent indices differ by up to
   ×4.7 (c₅₁₁ vs c₅₁₂); the local exponent oscillates between ≈ 0.63
   (all-ones i) and ≈ 0.93 (powers of two).
2. **Partial sums grow like a power.** S_n = Σ_{i≤n} c_i fits
   10.84·n^{1/5} − 11.43 to three decimals at n = 63, 127, 255, 511,
   1023 — against log(n+e) ≤ 6.94 there. Fitted on n ≤ 1023, the same
   formula then *predicted* S₂₀₄₇ = 38.37 and S₄₀₉₅ = 45.78; the deep
   run measured 38.33 and 45.60 — 0.1–0.4% accuracy two octaves out of
   sample. (Consistent with (⋆): typical s(i) ≈ ½log₂ i gives mean
   i·c_i growing like a small power of i, and 1 − α ≈ 0.2.)
3. CHT's Theorem 1.4 (Σ ≥ log) is respected with room to spare; their
   key inequality c_n ≥ e^{−S_{n−1}} is the m = 0 term of the channel
   picture below.

## 6. Interpretation: Lucas channels with lateral attenuation

A large initial value M at offset m propagates through |diff| dynamics as
an exact Pascal-mod-2 (Sierpiński) pattern and reaches the apex iff
C(i, m) is odd, i.e. iff m ⊆ i (Lucas). The submask sum in (⋆) is then a
sum over *open channels*, with the fitted weight q^m ≈ 0.67^m measuring
the attenuation of a channel at lateral offset m. CHT's own lower-bound
mechanism (Prop. 2.1: a_{(n,1)} ≥ a₁ − Σ_k a_{(k,2)}) is precisely the
m = 0 channel. The tail-dependence experiment above confirms the
mechanism: cut off the tail and the channels die.

The two *outer* channels (m = 0 and m = n, both always open since
C(n,0) = C(n,n) = 1) can be made rigorous simultaneously, and this yields
a strict improvement of CHT's key inequality:

**Theorem 2 (two-channel lower bound).** For every n ≥ 2,

  c_n ≥ E[e^{−(S_L^− + B)}] + E[e^{−(S_R^− + A)}] ≥ 2 exp(−Σ_{k=0}^{n−1} c_k),

where A = a_{(n−1,1)}, B = a_{(n−1,2)}, S_L^− = Σ_{k=0}^{n−2} a_{(k,2)},
S_R^− = Σ_{k=0}^{n−2} a_{(k,n−k)}. Consequently (via CHT's induction)
Σ_{i≤n} c_i ≥ log(2n − 2 + e²), improving their Theorem 1.4 by an
asymptotic additive log 2.

*Proof.* The apex satisfies a_{(n,1)} = |A − B|, and |A − B| =
(A−B)⁺ + (B−A)⁺. CHT's telescoping at depth n−1 gives A ≥ a₁ − S_L^−,
and its mirror image (the triangle is invariant under reversing the
initial sequence) gives B ≥ a_{n+1} − S_R^−. The key measurability facts:
S_L^− and S_R^− involve only a₂,…,a_n; B involves only a₂,…,a_{n+1};
A involves only a₁,…,a_n. Hence W := S_L^− + B is independent of a₁,
and (A−B)⁺ ≥ (a₁ − W)⁺ with E[(a₁ − W)⁺ | W] = e^{−W}, so
E(A−B)⁺ ≥ E e^{−W}; by Jensen and E S_L^− = c₀+…+c_{n−2},
E B = c_{n−1}, this is ≥ exp(−Σ_{k<n} c_k). The mirrored argument bounds
E(B−A)⁺ the same way. Summing gives the theorem; the partial-sum
corollary follows from exp(Σ_{i≤n}) ≥ exp(Σ_{i<n})(1 + c_n) ≥
exp(Σ_{i<n}) + 2 and exp(c₀+c₁) = e². ∎

Every inequality in the proof was additionally verified numerically at
n = 6 on 4×10⁶ samples (the two telescopes hold pointwise on every
sample; E S_L^− matched c₀+…+c₄ to 4 digits). The theorem is elementary
— CHT's own techniques plus reversal symmetry — but it is a strict
sharpening of their Proposition 2.1, and the first bound that uses two
Lucas channels at once. Making any *middle* channel (0 < m < n, m ⊆ n)
rigorous would be a first step toward proving any part of (⋆) itself;
the natural conjecture, supported by (⋆), is that all open channels
contribute: c_n ≳ (Σ_{m⊆n} q^m)·exp(−Σ_{k<n} c_k) for some q > 0.

## 7. Open questions

1. Prove any strict digit-dependence of c_i (e.g. c_{2^k+1} > c_{2^k}
   for large k) — nothing of this kind is currently known rigorously.
2. Extend Theorem 2 to middle channels or improve its constant — e.g.
   does c_n ≥ (2+κ)e^{−Σc} hold for odd n (channel m = 1 open)? Is
   q universal across initial distributions with exponential-type tails?
   Is α + θ = 1 exact (θ the partial-sum exponent)?
3. Does (⋆) persist as i → ∞, or is it a transient of the accessible
   range? (CHT's Theorem 1.4 requires only S_n ≳ log n.)
4. Exact c₇ (2^28 chambers) — needs either symmetry reductions or a
   smarter integration scheme.
5. The discrete Cramér-model analogue and the route back to the primes.

## 8. Reproducibility

`ck_exact.py`, `ck_exact_certified.py` (exact pipeline + certificates),
`ck6_certified.py`, `ck_montecarlo.py`, `ck_mc_deep.py` (data:
`ck_montecarlo.csv`, `ck_mc_deep.csv`), analysis scripts in this
directory. All computations are Python 3 + NumPy/SciPy, exact arithmetic
via `fractions.Fraction`; total compute for this note ≈ 3 CPU-hours.
