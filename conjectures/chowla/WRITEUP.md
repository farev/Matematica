# Session writeup, 2026-07-29: Chowla's conjecture (two-point Liouville correlations)

The lab notebook. Chronological, failures included, nothing edited to look
smarter in hindsight. The presentable artifact is NOTE.md.

## Why this target

Chowla's conjecture (S_h(x) = Σ_{n≤x} λ(n)λ(n+h) = o(x)) is the cleanest
statement of the parity barrier: the obstruction that blocks twin primes
and every sieve-based attack on prime patterns. Tao's 2016 logarithmic
two-point theorem, Helfgott–Radziwiłł 2021, and Pilatte 2023/2025 form an
active, current literature with explicit walls. Maximal win: prove
unaveraged two-point Chowla (nobody has; we did not). Realistic win: exact
structural lemmas + a certified census far beyond anything published +
audited claims + measured theory-truth gap. The realistic win happened.

## Phase 1: exploration before literature (by design)

- Wrote exact integer segmented sieve (`liouville.py`), validated against
  trial division on [1, 2·10^5] and windows at 10^9, 3·10^10, 10^12, 2^40,
  plus segmentation invariance. First try passed; L(10^6) = −530 agreed
  with the published value.
- Looked at S_h(10^7) for h ≤ 12: all O(√x). Shuffled control:
  indistinguishable magnitudes. 9 of 12 shifts negative → flagged a
  possible sign bias (later resolved as arcsine-law persistence, NOT bias;
  a false discovery avoided by the Run A grid analysis: pooled negativity
  0.443, per-h occupation extreme in both directions).
- Near-miss counterexample: completely multiplicative f = χ₃-extension
  fails Chowla with S_1/x → −1/3, S_3/x → +5/9 (measured to 7 digits;
  later PROVED as NOTE Prop 4). Lesson: complete multiplicativity permits
  maximal correlation; Chowla is about non-pretentiousness. This is the
  known structural obstruction, rediscovered from data before reading the
  literature; recorded as validation.

## Phase 2: the identities

The 2-adic descent (NOTE Lemma 1) came from asking what λ(2m) = −λ(m)
does to pair sums: S_h(x) = U_h(x) + S_{h/2}(⌊x/2⌋) for even h. Its
consequences organized everything:

- Certificate C1: three independently computed integer columns per row
  must satisfy the identity exactly.
- The odd-restricted U_h are computable as *contiguous* dot products on
  the odd subsequence (odd n, even h keeps n and n+h both odd); this
  later fixed the performance disaster (below).
- The renormalization reading: pair-correlation field = exact fixed point,
  odd-restricted correlations = innovations → parameter-free 1/√2
  cross-scale correlation prediction under innovation independence.

Walsh duality census ↔ correlations (Lemma 3) gave certificate C2.

## Phase 3: compute, including the failure

- Run A (fine): x ≤ 10^9, grid 5·10^5, coverage of all sign patterns
  k ≤ 24. Completed cleanly (~13 min). All certificates pass; L(10^9) =
  −25216 = A090410. N_24 = 293,427,643 vs coupon-collector 2.89·10^8.
- **Failure: Run B first launch.** Strided odd-index operations + int16
  temporaries made the 10^12 census a ~7 h job (ETA from log). Killed it
  at x ≈ 5·10^9. Rewrite: all correlations as float64 BLAS dots (±1
  entries, every intermediate an integer < 2^53 ⟹ every IEEE add exact, so
  certified integers via float hardware), odd-subsequence contiguity for
  U_h, harmonic columns added in the same pass. New kernel: bit-identical
  to the old on all 100 test rows; 1.0 s/segment single-core at any
  height. Relaunched.
- **Second failure (partial): contention.** With 10 workers + memory
  bandwidth, wall pace is ~0.55 s/segment, not 0.1: full 10^12 ≈ 8 h,
  not 85 min. Decision: let it stream (the CSV is valid at any prefix;
  certificates are per-row) and cap at whatever it reaches when analysis
  finalizes; state the exact cap. The 10^12 target remains reachable by
  just letting it finish overnight.
- Run harm1e9: harmonic ℓ_h baselines at 10^9 (for prediction P6).
  Cross-validated: integer columns identical to Run A's (different kernel
  paths).
- signchange.py: zeros/sign changes of L below 10^9 = 252/133, exactly
  BFM's published counts. S_1 path: 23,770 sign changes below 10^9.
- coverage_ext.py: k = 25, 26, 27 first-coverage (out-of-sample test of
  P5), running.

## Phase 4/5: literature (primary sources, read from the PDFs)

- Pilatte 2310.19357v2 (pp. 1–11 read): main theorem (log x)^{1−c},
  inexplicit c, "best possible with current techniques"; Remark 2.8
  (almost-all-scales unaveraged (log X)^{−c/2}); Remark 3.5 (the method's
  eigenvalue obstruction: integers with many prime factors; the cap is
  structural). Unaveraged Chowla open for all k ≥ 2, stated flatly.
- BFM Math. Comp. 2008 (read in full): L to 2·10^14 (2.5 CPU-years then);
  Turán T(n) first negative at 7.22·10^13; the island values we
  reproduced; their integrity checks were per-interval harmonic identities,
  the same philosophy as our C1–C3.
- Tao 1509.05422 (downloaded; used for attribution of the log-averaged
  theorem and the dilation mechanism).
- **Audit (NOTE §8): arXiv:2211.09736 (Carella, math.GM)** claims
  natural-density double-pattern equidistribution unconditionally, which would
  be unaveraged two-point Chowla. Read in full. The gap is precise:
  Lemmas 6.1/6.2 transfer log-average smallness to natural-average
  smallness by partial summation; the contradiction step needs a pointwise
  lower bound on the whole range where only a sequence of scales (with
  uncontrolled sign) is available. f(n) = n^{iα} is a bounded explicit
  counterexample to the transfer as stated. Claims unproven; conjecture
  still open. (Empirically the *claim* is on track: the flaw is the
  proof.)

## The corruption incident (the certificates earn their keep)

Certifying the capped 10^11 grid, C2 failed on all census-tied columns
while C1 and C3 passed. Localization: a single segment
(n ∈ [6.420·10^10, 6.422·10^10]); every other of the 5000 rows clean,
cumulative offset +2034 constant afterwards. A deterministic recompute of
that segment disagreed with the recorded values (so: not a code bug) and
was internally C2-consistent. Signature: 2039 window counts moved to
pattern 0 with the total conserved, meaning one zeroed ~8 KB page (2048 int32
codes) during the census build, i.e. transient memory corruption in an
hour-long, ~8 GB, 10-process run. The error is 0.1σ of a cell count:
statistically undetectable. C3 was blind to it (total conserved), C1 was
blind (direct columns unaffected). Only the Walsh duality caught it.
Repaired from the recompute; raw file preserved; disclosed in NOTE §3 and
VERDICTS.md. Lesson recorded: exact identity certificates are not
ceremony: they are the only line of defense against silent single-event
corruption at this scale.

## Honesty ledger

- Rediscoveries recorded as such: pretentious obstruction (Prop 4 context);
  MRT averaged Chowla via L-variance (sketched during planning, not
  claimed); dilation invariance folklore (Lemma 1 remark).
- The ℓ_h "constants" are conditional objects: convergence of the series
  is itself open (strictly between log-Chowla and power-saving Chowla);
  stated as such, values reported as partial sums with a model-based
  stability band.
- Coverage results are certified by exhibition (existence), and the
  *non*-occurrence before N_k is certified by the exhaustive scan; no
  density claim is made for k > 3 (density is proved only for k ≤ 3, MRT).
- Sign-bias "finding" at 10^7 was noise; documented as the false-positive
  it was.
- Predictions were committed with timestamps before target data existed;
  verdicts reported regardless of outcome.

## Obstruction log (where the wall actually is)

- Any elementary manipulation of the descent web (Cauchy–Schwarz over
  levels, telescoping, positivity of census cells) reduces two-point
  Chowla to the odd-restricted U_h, and there the multiplicative
  structure gives no further purchase: U_h is a correlation along a
  non-multiplicative subsequence. This is our precise formulation of where
  parity information dies; recorded as open problem 3 in the NOTE.
- The census positivity constraints (N_ε ≥ 0 for all ε, Lemma 3) imply
  |S_h| ≤ x trivially and nothing better without an input on higher
  correlations; the linear-programming relaxation over census vectors is
  degenerate (the uniform vector is feasible for any S values consistent
  with it; checked by hand for k = 2, 3). Dead end, ~30 min.

## Next session threads

1. Let Run B finish to 10^12; refresh the tables (one command)
2. Coverage k = 28–30 on the 10^12 pass (predictions in PREDICTIONS.md
   style first).
3. The h-aggregated statistics: variance of S_h across h at fixed x vs
   the descent-web covariance model (a full covariance-matrix test, not
   just the 1/√2 diagonal).
4. OEIS submissions (N_k; first-occurrence-of-pattern tables).
5. Write to Mossinghoff (BFM author) with the census + certificates;
   Pilatte with the measured-gap section.

## Continuation, same day: the second instrument set

After the 10^12 census was certified, three new instruments were
registered (PREDICTIONS2.md) and launched:

- **Covariance web (analysis on the certified grid).** All 15 same-block
  cross-shift correlations vanish (max |corr| 0.025, per-pair noise
  0.020, pooled +0.0025): the registered P8b bands hit on both clauses.
  The echo family extended to all sixteen doubling channels pools to
  +0.7069 +- 0.0026 against the parameter-free 0.7071, and the
  innovation-orthogonality channels pool to -0.0066 +- 0.0061 against
  the model's 0. The full covariance structure of the descent web now
  matches the fair-coin renormalization model in every measured entry.
  Each vanishing off-diagonal is implicitly a 4-point cancellation test.
- **Quad census (new run).** Twelve 4-point correlations (six bases,
  six doubles), odd-restricted V columns, census, on the 2·10^7 grid to
  10^11, with certificates C1Q (quad descent, exact), C2Q (Walsh vs
  census), C3, and a cross-run census identity against mainB12.
  Validated by brute force at 10^6 before launch. Context: even-order
  logarithmic Chowla is open; no published data exists for these sums.
- **Coverage 28-30 (new scan).** Single-worker to 3·10^10, coupon bands
  registered in advance; occurrence side to be certified by recomputing
  completing segments.

Results land in VERDICTS2.md as they arrive.
