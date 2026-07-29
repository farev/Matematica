# 2026-07-28 — Gilbreath's conjecture

**Target.** Gilbreath's conjecture (Proth 1878, Gilbreath 1958): every row of
the iterated absolute-difference triangle of the primes begins with 1. Chosen
because it sits on a fault line — it looks like a statement about primes, but
appears to be a statement about prime-gap statistics plus a lucky seed, and
parts of it are reachable by elementary means. Mid-session the target shifted
to the continuous model of Chase, Hunter and Tao (arXiv:2607.08712, July 2026),
where the open questions are sharper and actually movable.

**Result.**

- PROVED — `c_n ≥ 2·exp(−Σ_{k<n} c_k)` for `n ≥ 2`. A factor-2 sharpening of
  Chase–Hunter–Tao Proposition 2.1, obtained by pushing their mechanism through
  both ends of the triangle (reversal symmetry plus the identity
  `|A−B| = (A−B)⁺ + (B−A)⁺`). Gives `Σ_{i≤n} c_i ≥ log(2n − 2 + e²)`, an
  additive `log 2` improvement on their Theorem 1.4. Every step checked
  numerically at `n = 6` on 4×10⁶ samples.
- PROVED — the sign arrangement realises all `2^{i(i+1)/2}` chambers; the
  continuous model has no combinatorial obstruction, so the cooling is
  irreducibly statistical.
- CERTIFIED — exact rational `c₄`, `c₅`, `c₆` with partition-of-unity
  certificates in ℚ, extending the `c₀…c₃` of Chase–Hunter–Tao. `c₆` is a
  153-digit over 154-digit fraction. Certified chamber counts 2, 8, 64, 1024,
  32768, 2097152.
- CERTIFIED — Gilbreath holds for the first 455,052,510 rows (primes < 10¹⁰),
  `k* = 329`, via Odlyzko's propagation criterion.
- CERTIFIED — audit of Chase–Hunter–Tao Theorem 1.6 hypotheses against real
  primes: both dangerous block structures sit 11 and 25 orders of magnitude
  below their thresholds up to 10⁹, and grow at coin-flip rates.
- NUMERICAL — submask law `c_i ≈ C·i^{−α}·Σ_{m ⊆ i} q^m` with `α ≈ 0.798`,
  `q ≈ 0.685`, `C ≈ 1.14`. `R² = 0.980` on `i ∈ [64, 1023]`. Fitted on that
  range alone it predicts `i ∈ [1024, 4095]` out-of-sample at `R² = 0.90`,
  median relative error 13%. A pure power law fails outright (R² < 0). Implies
  the tentative `c_i ≍ 1/i` of their Remark 1.5 is untenable in the accessible
  range: partial sums grow like `n^{1/5}`, not `log n`.

**What failed.**

- The first `c₆` run (`ck6_parallel.py`) lost sliver simplices in degenerate
  Delaunay cross-sections — partition deficit `∑Z = 99316783/99316800 ≠ 1`.
  The value was right to within Monte Carlo error but could not be certified.
  Fixed later in the session; `c6_uncertified.txt` is kept as the record.
- Independently rediscovered Chase–Hunter–Tao's own lower-bound inequality
  before noticing it was theirs. Recorded as a rediscovery, not a result — and
  it paid off, since the same mechanism pushed harder gave the factor-2
  sharpening above.
- Pure `c_i ~ 1/i` regression: rejected, R² < 0. Adding a `ν₂(i)` covariate got
  to R² 0.68, still not the right structure. The binary-expansion framing came
  only after looking at the residuals by digit sum.
- Shuffled and i.i.d. gap models fail the Gilbreath property immediately, which
  kills any explanation resting on gap statistics alone. The authentic prime
  prefix matters: seed threshold ≈ 16–32 gaps.

**Next.**

- Universality: does the submask law survive uniform initial data instead of
  exponential? If yes it is a property of the iteration, not the distribution.
- Push the Monte Carlo a decade further (`i ~ 10⁴`) to test whether the
  `ρ`-ladder and `n^{1/5}` partial-sum growth persist. Needs ~10× compute or
  variance reduction.
- Identify `ρ` and `α` in closed form. `q ≈ 0.685` and `α ≈ 0.80` are measured,
  not derived, and nothing yet explains either.
- Formalize Lemmas 1–5 (parity, propagation, defect descent) in Lean 4. They
  are elementary and would give the core an unimpeachable machine-checked base.
- Submit the `c_i` numerator/denominator sequences to OEIS
  (`oeis_draft.txt` is written).
- Verify arXiv:2607.08712 resolves as cited before any of this goes public.
