# Verdicts on the pre-registered predictions

Written 2026-07-29 after the main run was capped at x = 10^11 (5000 grid
rows; run wall time to cap 2752 s on 10 workers) and the coverage extension
completed. Predictions were registered in PREDICTIONS.md at 11:10–11:14 PDT,
when only x ≤ 10^9 data existed. Targets registered for the 10^12 horizon
that the cap did not reach are scored UNTESTED, not rescoped.

## P1: scaling (model: fair-coin walk)

- RMS_h S_h/√x at 10^10: predicted 0.90 ± 0.35 → measured **1.155**. HIT
  (near the top of the band).
- At 10^11 (= final flushed x clause): predicted 0.90 ± 0.40 → measured
  **0.794**. HIT.
- At 10^12: UNTESTED (cap).
- Sub-prediction α ∈ [0.47, 0.53] on [10^8, x_max]: measured **α = 0.436**.
  **MISS.** The fluctuation level stayed square-root-sized while the local
  log-log slope of one path over three decades drifted low, consistent
  with arcsine-scale wander of a single trajectory, but the registered
  band was wrong about it. Recorded as a miss.

## P2: cross-scale echo (model: Lemma 1 + independent innovations, 1/√2)

- Pooled over h ∈ {1,2,3,4,6,8}, Δ = 20 grid units: predicted [0.68, 0.73]
  → measured **+0.6884 ± 0.0174** (122 disjoint blocks per pair). HIT.
- Per-h within ±0.05 of 0.7071: 4 of 6 inside; h=1 (+0.637) and h=2→4
  (+0.760) fall just outside. **Sub-clause: MISS on 2 of 6.**

## P3: census extreme (model: 256 Gaussian cells, Gumbel)

- Predicted max|z| ∈ [2.7, 4.3] at cap → measured **4.21** (cell 163). HIT.

## P4: external anchors (no model: published values must be reproduced)

- L(10^10) = −116026: **exact**. L(10^11) = −342224: **exact**. HIT.
- L(10^12): UNTESTED (cap).
- L(x) < 0 at every grid row ≥ 1.2·10^9: **holds at all rows**. HIT.
- hL(x) > 0 at every grid row: **holds**; hL(10^11) = +8.43·10^-7, in the
  regime of BFM's neighbouring local minima (≈ 6·10^-7 at 9.8·10^10). HIT.
- hL(10^12) band: UNTESTED (cap).

## P5: coverage completion (model: uniform coupon collector, 2σ bands)

- N_25: predicted (6.0 ± 0.9)·10^8 → measured **722,808,938** (ratio to
  model 1.203). **MISS**, outside the band. As a Gumbel tail event its
  probability is ≈ 2.6%; with 27 lengths tested one such event is
  unremarkable, and:
- N_26: predicted (1.25 ± 0.17)·10^9 → measured **1,312,765,349**
  (ratio 1.052). HIT.
- N_27: predicted (2.6 ± 0.34)·10^9 → measured **2,794,709,788**
  (ratio 1.079). HIT.
- Verdict on the follow-up question the miss raised: no systematic drift:
  k = 26, 27 return to the model. The k = 25 excursion reads as tail
  fluctuation, not structure.

## P6: harmonic freeze (model: independent ±1/n tail, σ = 3.2·10^-5)

- Registered band was for 10^12: UNTESTED (cap).
- Same model at 10^11 (tail variance from 10^9 essentially identical):
  band ±2·10^-4 → measured max_h |ℓ_h(10^11) − ℓ_h(10^9)| = **9.61·10^-5**.
  HIT, and sharply: the expected maximum of 32 half-normal drifts is
  σ√(2 ln 64) ≈ 9.2·10^-5, against 9.6·10^-5 observed.

## Ledger

10 scored clauses: 7 hits, 3 misses (α sub-fit; 2-of-6 per-h corridor;
N_25), 4 untested (10^12 horizon). Misses reported exactly as registered.

## Incident disclosure (affects no verdict)

During the main run, certificate C2 caught a single corrupted segment
(rows ≥ 3210; n ∈ [6.420·10^10, 6.422·10^10]): one ~8 KB page of the
window-code array was zeroed at run time, moving 2039 window counts to
pattern 0 while conserving the total (C3 blind, C1 blind, direct
correlation columns unaffected, statistically invisible at 0.1σ of the
cell count). A deterministic recompute of the segment differed from the
recorded values and was itself internally consistent, identifying transient
memory corruption rather than a code defect. The census columns were
repaired from the recompute; the raw file is kept as
`data/mainB_1e11_grid_raw.csv`; all certificates pass on the repaired grid
(C1 at 40,000 (h,x) pairs, C2 and C3 at all 5000 rows). Columns S_h for odd
h ≥ 9 carry no independent per-row certificate (C2 covers h ≤ 7 and the
recorded triples/quadruple; C1 covers all even h); they are validated by
the kernel-level checks only, and are labelled accordingly.

## Addendum, 10^12 completion (2026-07-29 evening)

The full run to 10^12 finished (23,362 s wall on 10 workers) and, after the
repairs described below, passes all certificates (C1 at 400,000 (h, x)
pairs, C2 and C3 at all 50,000 rows). The four clauses scored UNTESTED at
the 10^11 cap now resolve, plus one re-evaluation:

- P1, RMS at 10^12: predicted 0.90 ± 0.40 → measured **0.898**. HIT.
- P3 at the registered "final x of Run B" (now 10^12): max|z| = **2.98**,
  in [2.7, 4.3]. HIT.
- P4, L(10^12): **−522,626, exactly the A090410 value**. HIT.
- P4, hL(10^12) band [5·10^-8, 6·10^-7]: measured **+8.23·10^-7**. **MISS.**
  The band was calibrated from BFM's local *minima*, which sit
  systematically below typical values; a modeling error, recorded as such.
- P6 at its registered horizon: max_h |ℓ_h(10^12) − ℓ_h(10^9)| =
  **9.63·10^-5**, inside ±2·10^-4. HIT.
- α re-evaluated on [10^8, 10^12]: **0.4672**, still marginally outside
  [0.47, 0.53] (original MISS stands; the estimate moved toward 1/2 with
  the added decade, consistent with the single-path-noise reading).

Cross-scale echo at 10^12 scale: pooled **+0.7085 ± 0.0046** (1247 disjoint
block pairs per h) against the parameter-free 1/√2 = 0.7071: within one
standard error.

**Final ledger: 14 scored clauses, 10 hits, 4 misses** (α sub-fit; per-h
corridor 2-of-6; N_25; hL(10^12) band). Misses reported as registered.

## Incident disclosure #2 (10^12 run)

The 6.5-hour run suffered **nine** transient memory-corruption events
(segments 1460, 4388, 29550, 33613, 39754, 41044, 45171, 46233, 46457):
three census-page zeroings of the morning's type, four small hits to the
triple/quadruple entries, and two near-total wipes of a segment's
statistics row (census part conserving totals, hence invisible to C3).
The event at 41044 was detectable only by the descent certificate C1.
Each event was localized by certificate-residual jumps, recomputed
deterministically (recomputes internally consistent; recorded values not),
and patched; raw pre-repair file kept as `data/mainB12_grid_raw.csv`.
Decisive validation of the repaired grid: (a) all certificates pass;
(b) the repaired 10^12 run and the independently repaired morning run are
**bit-identical on all 5000 overlapping rows**, though they were corrupted
at disjoint places; (c) L(10^9..10^12) match A090410 exactly on a column
hit by two separate wipes. Caveat as before: an event confined to the
odd-h ≥ 9 S-columns above 10^11 would evade C1/C2; none of the nine
observed events had that shape. Hardware note: ~1.5 events/hour under
sustained 10-worker memory load on this machine (zero in single-worker
runs); the RAM is not ECC and a hardware memory diagnostic is advisable
before further multi-hour runs.
