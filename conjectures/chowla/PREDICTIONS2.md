# Pre-registered predictions, round 2 (4-point census, covariance web, coverage 28-30)

Written 2026-07-29, evening, immediately after the 10^12 two-point census
was certified. At the time of writing: no 4-point correlation has ever
been computed by us beyond the single recorded quadruple Q_{0123}; no
coverage scan beyond k = 27 exists; the covariance-matrix analysis of the
existing grid has not been run. Models are named per prediction; verdicts
go to VERDICTS2.md regardless of outcome.

## Instruments

- Run Q ("quad census"): 12 quadruple correlations
  Q_{0,a,b,c}(x) = Σ_{n≤x} λ(n)λ(n+a)λ(n+b)λ(n+c) for the six bases
  (1,2,3), (1,2,4), (1,3,5), (2,3,4), (1,2,5), (1,4,5) and their doubles
  (2,4,6), (2,4,8), (2,6,10), (4,6,8), (2,4,10), (2,8,10), plus the six
  odd-restricted V columns for the doubles, plus the 256-cell census, on
  the 2·10^7 grid to x = 10^11. Certificates: C1Q (quad descent, exact),
  C2Q (Walsh duality vs census for the 7 quadruples inside window ≤ 7),
  C3 (census totality), and cross-run census identity against the
  certified mainB12 grid at every row.
- Run K: coverage scan for k = 28, 29, 30 to 3·10^10 (single worker).
- Analysis W: block-increment covariance matrix of {S_h} on the certified
  10^12 grid.

## P7, size of 4-point correlations (model: fair coin; context: even-order
logarithmic Chowla is OPEN, so theory does not even give o(log x) control
of the averaged version of these)

- At x = 10^11: RMS over the 12 quadruples of Q/√x ∈ [0.55, 1.35];
  max over the 12 of |Q|/√x < 3.5.
- No drift: RMS_quads Q/√x at 10^10 also ∈ [0.55, 1.35].

## P8a, quad descent echo (model: Lemma 1 applied to 4 factors, λ(d)^4 = 1,
plus innovation independence; parameter-free 1/√2)

- corr(ΔQ_double at (2y, 2Δ), ΔQ_base at (y, Δ)), Δ = 20 grid units,
  pooled over the 6 base/double pairs: ∈ [0.66, 0.75].

## P8b, covariance web on the two-point grid (model: descent web + fair
coin; all same-block couplings vanish)

- Same-block increment correlations corr(ΔS_h, ΔS_h') at Δ = 20 grid
  units on the 10^12 grid, over all 15 pairs from h, h' ∈ {1,2,3,4,6,8},
  h ≠ h': every pair ∈ [−0.06, +0.06]; pooled mean ∈ [−0.015, +0.015].
  (Each such correlation is secretly a 4-point correlation test: the
  n = m diagonal contributes ΔS_{|h−h'|}-type terms and the rest is
  genuine 4-point cancellation.)

## P9, coverage completion (model: uniform coupon collector,
N ≈ 2^k (k ln 2 + γ), 2σ Gumbel bands)

- N_28 = (5.37 ± 0.69)·10^9
- N_29 = (11.10 ± 1.38)·10^9
- N_30 = (22.95 ± 2.76)·10^9  (contingent: scan reaches 3·10^10)

Coverage caveat, registered in advance: the scan is single-worker (the
observed corruption events have all been in 10-worker runs), occurrence
at the reported indices will be certified by independent recomputation of
the completing segments, and the minimality side carries the hardware
caveat unless the scan is repeated.
