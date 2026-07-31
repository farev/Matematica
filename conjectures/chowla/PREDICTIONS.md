# Out-of-sample predictions — committed before the data existed

Written 2026-07-29 11:10 PDT.

Data available at time of writing and used to fit: **Run A only**
(`data/fineA_grid.csv`, x ≤ 10^9, grid 5·10^5) plus published literature
(BFM 2008; OEIS A090410) and closed-form null models. Run B
(`census_run.py 1e12 2e7 10`) was at segment ~400/50000 (x ≈ 8·10^9) per its
log; **no Run B rows have been read**. The coverage-extension run for P5 had
not been launched when this file was written.

Every prediction names its generating model. Verification happens in
VERDICTS.md when the runs land.

## P1 — scaling of pair correlations (model: random ±1 walk, α = 1/2)

RMS over h ∈ [1,32] of S_h(x)/√x:

- x = 10^10: 0.90 ± 0.35
- x = 10^11: 0.90 ± 0.35
- x = 10^12 (or final flushed x of Run B): 0.90 ± 0.40

Sub-prediction: log-log fit of RMS_h S_h vs x over [10^8, x_max] gives
exponent α ∈ [0.47, 0.53] (Run A's local α̂ = 0.55 on [10^7,10^9] is
predicted to be a transient of the single path, not a real drift).

## P2 — cross-scale increment correlation (model: Lemma 1 descent + odd-part
independence; parameter-free value 1/√2 = 0.7071)

Pooled over h ∈ {1,2,3,4,6,8}, disjoint blocks of Δ = 20 grid units
(4·10^8), pairs (ΔS_h at [y, y+Δ), ΔS_2h at [2y, 2y+2Δ)) for y from 2·10^9
to x_max/2: pooled correlation ∈ **[0.68, 0.73]**, per-h values within
±0.05 of 0.7071.

## P3 — census extreme (model: 256 near-independent Gaussian cells, Gumbel)

At final x of Run B: max over 256 patterns of |count − x/256| / sqrt(x·(1/256)(255/256))
∈ **[2.7, 4.3]** (center 3.5).

## P4 — external anchors (model: none; published computations must be
reproduced exactly or the pipeline is wrong)

- L(x) matches OEIS A090410 at every power of 10 on the grid:
  L(10^10) = −116026, L(10^11) = −342224, L(10^12) = −522626.
- L(x) < 0 at every grid row with x ≥ 1.2·10^9 (BFM: no positive values in
  [10^9, 2·10^14]).
- Turán column hL(x) = Σ λ(n)/n > 0 at every grid row (BFM: first negative
  at n ≈ 7.22·10^13 > 10^12), and hL(10^12) ∈ [5·10^-8, 6·10^-7]
  (BFM Table 1 local minima nearby: T(1.34·10^12) ≈ 1.65·10^-7).

## P5 — pattern-coverage completion (model: uniform coupon collector,
M = 2^k coupons, N ≈ M(ln M + γ), 2σ Gumbel band ≈ ±2·(π/√6)M)

- N_25 = (6.0 ± 0.9)·10^8
- N_26 = (1.25 ± 0.17)·10^9
- N_27 = (2.6 ± 0.34)·10^9

(Run A observed N_24 = 293,427,643 vs model 2.89·10^8 — ratio 1.014 — which
is what motivates trusting the model out of sample.)

## P6 — harmonic pair sums (model: increments λ(n)λ(n+h)/n behave as
independent ±1/n; Var of tail past a = 1/a)

For every h ∈ [1, 32]: ℓ_h(10^12) = ℓ_h(10^9) ± 2·10^-4 (a ±6σ band;
σ = 3.2·10^-5). Baseline ℓ_h(10^9) values to be filled from the dedicated
1e9 harmonic run (in flight at time of writing; its prefix duplicates
Run B's range and involves no data beyond 10^9):

Baselines from `data/harm1e9_grid.csv` (appended 11:14 PDT, still before any
Run B harmonic column beyond 10^9 was read). ℓ_h(10^9) for h = 1..32:

```
-0.842490 -1.356346 +0.623358 -1.546202 +2.096571 -0.492160 -2.312847
+0.360562 +1.455376 +0.233711 -0.326367 -1.178250 -0.296923 +0.215497
+1.832514 -0.405187 -0.685095 -0.380966 -2.086503 +1.254825 +0.762311
-1.652508 -0.043798 +1.290266 +2.182868 -0.561114 -0.736176 -1.167398
+0.190820 +0.111433 -1.817985 +0.424765
```

Their empirical spread (sample sd 1.21) matches the model sd
sqrt(Σ 1/n²) = sqrt(π²/6) ≈ 1.28: the constants are frozen by small n.
The prediction above is therefore a *no-late-drift* test: any systematic
correlation emerging between 10^9 and 10^12 would break the ±2·10^-4 band.

Also: hL(10^9) = +1.899·10^-5 > 0, consistent with BFM.
