# PAGE.md — handoff for the Chowla write-up page (session 2026-08-01)

A page already exists at <https://fabianarevalo.com/chowla>. **This is an
update, not a rebuild.** See §5 for exactly what changed.

## 1. Headline claim

**CERTIFIED** — every one of the 8,589,934,592 possible ±1 sign patterns of
length 33 occurs in the Liouville function below 2·10^11, the last one
appearing at n = 196,202,853,829; and the length-24 window statistics of λ are
indistinguishable from a fair coin at a resolution of 3·10⁻⁴, measured against
32 control streams.

## 2. Contributions

1. **CERTIFIED.** Coverage extended past the previous record of k = 30:
   N_31 = 43,901,697,682 (last pattern code 1,784,492,180),
   N_32 = 99,494,377,311 (code 2,930,773,200) and
   N_33 = 196,202,853,829 (code 3,712,643,644). N_k is the smallest window
   *start* index by which every one of the 2^k patterns of length k has
   occurred. Certified by exhibition: all three completing windows were
   re-verified by pure-Python trial division, independent of the sieve, along
   with 10, 12 and 12 further endgame windows. One run: 4 cores, 7387 s,
   peak RSS 2.5 GB.
2. **CERTIFIED.** A clean-room reproduction of every previously published
   coverage value. A C implementation sharing no code with the original NumPy
   pipeline reproduces all thirty values of N_k *and* all thirty
   last-completing pattern codes for k = 1..30, plus L(10^j) for j = 1..8
   (0, −2, −14, −94, −288, −530, −842, −3884). A third implementation, pure
   Python trial division, independently confirms k = 1..14.
3. **NUMERICAL.** A new instrument, the *first-occurrence spectrum*. Instead of
   reporting only the maximum N_k, record the first occurrence of all 2^k
   patterns and score each against Conway's exact fair-coin waiting time
   A(w) = Σ_j δ_j(w)·2^j (δ_j = 1 iff w's length-j prefix equals its length-j
   suffix). The statistic R(w) = (start + k − 1)/A(w) has model mean exactly 1,
   with **no fitted parameter and one prediction per pattern**. At k = 24 over
   all 16,777,216 patterns: λ gives mean R = 1.000123 against 32 i.i.d.
   fair-coin controls at 0.999953 ± 0.000319 — **+0.53 control-σ**, rank 23 of
   33. The controls' own mean is −0.8 SE from the exact value 1, so the
   statistic is unbiased.
4. **NUMERICAL.** Resolved by popcount (how many of the 24 entries are −1),
   λ's slope of mean R is −2.64·10⁻⁴ per unit popcount against a control band
   of −1.10·10⁻⁴ ± 3.53·10⁻⁴ (−0.44σ). Across the 32 controls that slope
   correlates at r = +0.80 with the stream's own realised one-point bias
   L(10⁷)/10⁷, so λ's value is exactly what its known negative bias predicts;
   the residual is −0.56σ. Nothing anomalous survives.
5. **NUMERICAL.** Read as a Gumbel variate rather than a ratio, every coverage
   record from k = 16 to 33 sits within 2.9 standard deviations of the
   coupon-collector law, mean z = +0.4. Along the way the unseen-pattern count
   tracked the model 2^k·e^{−x/2^k} to three significant figures: at x = 10^11
   the k = 33 tracker had 75,925 patterns left against a predicted 75,600.
   The self-overlap correction that a careful reader would worry about
   (constant words wait twice as long) is
   bounded below 0.3% at k = 32 and 33 — see `coverage_model.py`.

## 3. Figures

**Fig 1 — coverage against the coupon-collector law.**
Data: `data/fineA_coverage.csv`, `data/coverage_ext.csv`,
`data/coverage_2830.csv`, `data/coverage_3133.csv` (columns k, N_k; k runs to
33), curve from `coverage_model.py` (m·H_m with m = 2^k). Log y-axis, k on x.
*Sentence:* "The number of Liouville values you must read before every ±1
pattern of length k has appeared follows the pure coupon-collector law, with no
drift, through thirty-three doublings."

**Fig 2 — each record's deviation from the law.**
Data: the `gumbel_z` column of `python3 coverage_model.py`, k = 16..33.
Bar chart around zero with a ±1 band. (Restrict to k ≥ 16; below that the
asymptotic model is not meaningful and would mislead.)
*Sentence:* "No coverage record is an outlier — the newest ones least of all."

**Fig 3 — λ against the control ensemble.**
Data: `data/firstocc_k24_controls.csv`, the `mean_R` column: 32 control values
as a strip/dot plot, λ marked. Zoom the axis to [0.9990, 1.0010] so the
0.0003-wide spread is visible.
*Sentence:* "On a statistic that reads all sixteen million patterns of length
24 at once, λ lands in the middle of the fair-coin controls, not at the edge."

**Fig 4 — nothing hiding in the sign balance.**
Data: `data/firstocc_k24_popcount.csv` — λ's mean R per popcount class with the
control mean ± sd as a shaded band. Restrict to popcount 4..20 where the
classes are large enough to see anything; say in the caption that the extreme
classes contain one to a few hundred patterns and are pure noise.
*Sentence:* "Patterns with many −1's are no harder or easier for λ to produce
than the coin model says."

Nothing else. In particular there is **no** figure for the endgame logs or the
overlap classes — I could not write a sentence for either that a reader would
be glad to have.

## 4. Caveats the page must carry

- **"Certified" here means exhibited, not proved minimal.** N_k is the start
  index of the completing window; that window is exhibited and independently
  re-verified. The claim that no earlier occurrence exists has no compact
  witness and rests on the exhaustive scan. Same caveat as the previous page.
- **A computation is not a proof.** All of this is consistent with Chowla and
  proves nothing about it. The honest framing is the one the page already uses:
  the parity barrier predicts unlimited numerical pseudorandomness that no
  argument can convert, and this is another few orders of magnitude of it.
- **The instrument's error bars come from controls, not from a formula.** The
  2^k first-occurrence times all come from one stream and are not independent,
  so σ/√(2^k) would be wrong by a large factor. Every ± on this page is the
  dispersion of 32 control streams.
- **The 4.4σ that was not.** The first control ensemble was broken — streams
  seeded by XOR with a small number share their bit multiset, so all 32 "controls"
  had the same density (L(10⁸) = +16362 for every one). Against that fake error
  bar, λ's popcount slope read as a 4.4σ anomaly. With correct seeding the same
  measurement is −0.44σ. If the page has room for one methodological aside,
  this is the one worth telling; if not, it must at least not be omitted from
  the linked note.
- **The regression coefficient in contribution 4 is a calibration, not a
  prediction.** Fitted 0.92 ± 0.12 where the crude first-order theory says 2,
  because the relevant density is a weighted average over the whole range of
  first-occurrence times, not its value at the single reference scale 10⁷.
- **No literature was checkable this session.** The sandbox had no network.
  Every citation on the page is inherited from the previous session's
  primary-source reading; nothing new is cited. In particular the claim that
  the sequence N_k is **new to OEIS is inherited and was not re-checked** —
  it must keep whatever hedge it already carries, and should not be
  strengthened.
- Runtime, for the reproducibility line: 4 cores, 15 GB, ~390 s per 10^10
  values of n; N_31 at 1718 s, N_32 at 3774 s, N_33 at 7387 s; peak RSS
  ≈ 2.5 GB.

## 5. What changed since the existing page

- Coverage headline moves from **k ≤ 30** to **k ≤ 33**; three new rows in
  whatever table carries N_k, and the "every pattern of length ≤ 30" sentence
  needs its number bumped in both prose and figure captions.
- Everything in §2 items 2–5 is new and has no counterpart on the current page.
  Item 3 (the first-occurrence spectrum) is the one that deserves real space:
  it is the first statistic here that reads all 2^k patterns at once rather
  than the maximum, and it is parameter-free.
- Figures 3 and 4 are new. Figures 1 and 2 replace/extend whatever coverage
  figure exists, with the two new points and the Gumbel reading.
- The existing page's framing, tone and the parity-barrier throughline are
  unchanged and should be preserved.
