# Verdicts, round 2 (registered in PREDICTIONS2.md)

Scored as results land; every clause reported. Analyses on the certified
mainB12 grid; new runs carry their own certificates.

## P8b: covariance web on the two-point grid. SCORED

Same-block increment correlations, Δ = 20 grid units, 2499 disjoint
blocks, all 15 pairs from h, h' ∈ {1,2,3,4,6,8}:

- Registered: every pair ∈ [−0.06, +0.06] → measured min −0.0207,
  max +0.0253. **HIT (15 of 15 inside, with room).**
- Registered: pooled mean ∈ [−0.015, +0.015] → measured **+0.0025**. HIT.

Unregistered companion measurements (reported for completeness, not
scored): the echo family over all sixteen channels h = 1..16 pools to
**+0.7069 ± 0.0026** against the parameter-free 1/√2 = 0.7071; the
innovation-orthogonality channels pool to **−0.0066 ± 0.0061** against
the model's 0; the odd-core RMS_h U_h(x)/√(x/2) sits in [0.92, 1.20]
across 10^9..10^12. The full covariance structure of the descent web
(diagonal echo, vanishing off-diagonals, square-root-sized innovations)
matches the fair-coin renormalization model in every measured entry.
A final companion entry: the innovations are independent across scales
too, corr(ΔU_2h(2y), ΔU_h(y)) pooling to −0.011 ± 0.010 over six
channels against the model's 0.

## P7: size of 4-point correlations. SCORED

Quad run to 10^11 completed in 3696 s; ALL certificates pass (C1Q at
15,000 points, C2Q at all rows, C3, and the cross-run identity: census
and Lx columns bit-identical to mainB12 on all 5000 shared rows). No
corruption events in this run.

- RMS over the 12 quadruples of Q/√x: registered [0.55, 1.35] →
  measured **0.725 at 10^10, 0.778 at 10^11**. HIT (both clauses).
- max |Q|/√x: registered < 3.5 → measured **1.498 / 1.394**. HIT.

First measurement of these sums at any scale that we are aware of;
even-order averaged Chowla being open, no theorem controls them beyond
the trivial bound. All twelve are square-root-sized.

## P8a: quad descent echo. SCORED

- Pooled over the 6 base/double pairs, Δ = 20 grid units: registered
  [0.66, 0.75] → measured **+0.7206 ± 0.0128** (122 blocks per pair).
  HIT; consistent with the parameter-free 1/√2 = 0.7071 (+1.1σ).
  The 2-adic renormalization structure extends to 4-point correlations
  exactly as the four-factor Lemma 1 requires.

## P9: coverage 28, 29, 30. PARTIALLY SCORED (k=30 in flight)

- N_28: registered (5.37 ± 0.69)·10^9 → measured **5,542,425,842**
  (model ratio 1.033). HIT. Completing pattern (code 18557987) confirmed
  at n = 5,542,425,842 by independent recomputation.
- N_29: registered (11.10 ± 1.38)·10^9 → measured **11,647,289,153**
  (ratio 1.049). HIT. Completing pattern (code 261683248) confirmed by
  independent recomputation.
- N_30: registered (22.95 ± 2.76)·10^9 → measured **22,249,147,014**
  (ratio 0.970). HIT. Completing pattern (code 1068405371) confirmed at
  n = 22,249,147,014 by independent recomputation. Scan wall time 5891 s.

## Round-2 ledger

**10 registered clauses, 10 hits, 0 misses** (P7 three clauses; P8a; P8b
two clauses; P9 three clauses, each completion independently
reconfirmed). Combined with round 1: 24 scored clauses, 20 hits,
4 misses, all reported.
