# The two-point Chowla conjecture at scale: a certified correlation census to 10^12, exact 2-adic descent, and the measured width of the parity barrier

*Research note, Matematica project. 2026-07-29. AI-assisted (Claude, Anthropic);
all claims labelled PROVED / CERTIFIED / NUMERICAL per project discipline.*

## Abstract

Let λ be the Liouville function and S_h(x) = Σ_{n≤x} λ(n)λ(n+h). Chowla's
conjecture asserts S_h(x) = o(x) for every h ≥ 1; it is open for every h,
and is the paradigmatic instance of the parity barrier. We report: (1)
elementary but organizing exact identities: a 2-adic descent
S_h(x) = U_h(x) + S_{h/2}(⌊x/2⌋) (h even, U_h the odd-n restriction), which
exhibits the pair-correlation field as an exact fixed point of a
renormalization map with the odd-restricted correlations as innovations,
and a Walsh–Hadamard duality between the sign-pattern census and multipoint
correlations (PROVED); (2) a certified integer census of S_h (h ≤ 32),
U_h, three triple and one quadruple correlation, the 256-cell sign-pattern
census, and harmonic pair sums ℓ_h(x) = Σ_{n≤x} λ(n)λ(n+h)/n, on a grid of
spacing 2·10^7 to x = 10^12 (fine grid of 5·10^5 to 10^9), every row
passing exact integer certificates, with published anchors reproduced
exactly: L(10^k) per OEIS A090410 for k = 9, 10, 11, 12; Tanaka's Pólya
island (first L > 0 at 906,150,257; max 829 at 906,316,571); BFM's 252
zeros and 133 sign changes of L below 10^9 (CERTIFIED); (3) every ±1 sign
pattern of length ≤ 27 occurs, with completion points N_k tracking the
uniform coupon-collector law across 27 doublings (mean measured/model
ratio 1.008 for k = 10..30, scatter matching the model's own Gumbel
width); the sequence N_k is new to the OEIS (CERTIFIED by exhibition); (4) verdicts on
six predictions registered before the data existed: 14 scored clauses,
10 hit, 4 missed, all reported (NUMERICAL), including the parameter-free
cross-scale increment correlation 1/√2 = 0.7071 forced by descent plus
innovation independence, measured at +0.7085 ± 0.0046 across 10^12
(+0.688 ± 0.017 at the pre-registered 10^11 scale); (5) at x = 10^12 the
measured |S_1|/x is 1.6·10^-7 while the strongest proven bound at almost
all scales (Pilatte 2025, Remark 2.8) is numerically ≥ 0.9, a gap of
six to seven orders of magnitude (a factor ≈ 5·10^6), quantifying the
parity barrier at real scales; and (6) an audit of arXiv:2211.09736,
whose claimed unconditional two-point equidistribution rests on
transferring logarithmic-average control to natural averages, an
implication refuted by f(n) = n^{iα}; and (7) a second instrument set,
pre-registered separately (PREDICTIONS2/VERDICTS2): a certified 4-point
census to 10^11 (certificates: exact quad descent, Walsh duality, census
totality, and bit-identity of shared columns with the 10^12 run), giving
the first data at an order where even logarithmically averaged Chowla is
open: all twelve measured quadruple correlations are square-root-sized
(RMS 0.78 at 10^11), the quad descent echo is +0.721 ± 0.013, and the
full covariance web of the descent structure (sixteen echo channels
pooling to +0.7069 ± 0.0026, all fifteen same-block off-diagonals and
sixteen innovation-orthogonality channels vanishing, odd core
square-root-sized) matches the fair-coin renormalization model in every
measured entry. The conjecture survives, its open core isolated in the
odd-restricted correlations U_h.

## 1. The conjecture and its status

λ(n) = (−1)^Ω(n), completely multiplicative, λ(p) = −1 at every prime.

**Conjecture (Chowla, two-point case).** For every h ≥ 1,
S_h(x) := Σ_{n≤x} λ(n)λ(n+h) = o(x).

Status of the art (every statement below checked against the cited paper's
own text, not summaries):

- Matomäki–Radziwiłł–Tao (2015): Chowla holds *on average* over shifts;
  all length-3 sign patterns occur with positive density.
- Tao (2016): logarithmically averaged two-point Chowla:
  Σ_{n≤x} λ(n)λ(n+1)/n = o(log x), by the entropy decrement argument.
- Tao–Teräväinen: logarithmic Chowla for all odd orders; even ≥ 4 open.
- Helfgott–Radziwiłł (2021): Σ_{n≤x} λ(n)λ(n+1)/n ≪ (log x)/(log log x)^{1/2}.
- Pilatte (2023; v2 Dec 2025): Σ_{n≤x} λ(n)λ(n+1)/n ≪ (log x)^{1−c},
  c > 0 inexplicit; "it appears that saving a fixed power of the logarithm
  is the best that is achievable with current techniques" (§1.1). His
  Remark 2.8 gives the strongest unaveraged statement known:
  |S_1(x)|/x ≪ (log X)^{−c/2} for x ≤ X outside an exceptional set of
  logarithmic density O((log X)^{−c/2}).
- The unaveraged conjecture is open for all orders k ≥ 2 (Pilatte, §1.1).

## 2. Exact structure (PROVED)

**Lemma 1 (dilation descent).** Let d ≥ 1, h = d·h′. Then
Σ_{n≤x, d|n} λ(n)λ(n+h) = S_{h′}(⌊x/d⌋). In particular, for even h, with
U_h(x) := Σ_{n≤x, n odd} λ(n)λ(n+h):

  S_h(x) = U_h(x) + S_{h/2}(⌊x/2⌋).

*Proof.* For n = dm ≤ x, complete multiplicativity gives
λ(dm)λ(dm+dh′) = λ(d)²λ(m)λ(m+h′) = λ(m)λ(m+h′); the map n ↦ m is a
bijection {n ≤ x : d|n} → {m ≤ ⌊x/d⌋}. ∎

**Proposition 2 (2-adic reduction).** Write h = 2^a h₀, h₀ odd. Then

  S_h(x) = Σ_{j=0}^{a−1} U_{h/2^j}(⌊x/2^j⌋) + S_{h₀}(⌊x/2^a⌋),

and if |U_g(y)| ≤ δy for all even g and all y then |S_h(x)| ≤ 2δx + x/2^a.
Consequently the two-point conjecture is equivalent to: S_h = o(x) for odd
h, and U_h = o(x) for even h; the odd-restricted correlations are the
irreducible content, and shifts of high 2-adic valuation are automatically
small up to innovation terms.

*Proof.* Iterate Lemma 1; bound the final term trivially; sum the
geometric series. ∎

*Remark.* The dilation invariance itself is standard (it is the mechanism
of Tao's reduction in [Tao16]); we have not found the renormalization
reading (the correlation field as an exact fixed point with odd-restricted
innovations, and its testable covariance signature, §6) in the
literature.

**Lemma 3 (census–correlation duality).** For a window of length k,
pattern counts N_ε(x) (ε ∈ {±1}^k) and subset correlations
R_S(x) = Σ_{n≤x} Π_{i∈S} λ(n+i) satisfy
N_ε(x) = 2^{−k} Σ_S (Π_{i∈S} ε_i) R_S(x) and
R_S(x) = Σ_ε (Π_{i∈S} ε_i) N_ε(x).

*Proof.* Expand Π_{i<k}(1+ε_i λ(n+i))/2, the indicator of pattern ε at n;
invert by Walsh–Hadamard orthogonality. ∎

**Proposition 4 (a maximal near-miss).** Let f be completely
multiplicative with f(3) = −1 and f(p) = χ(p) for p ≠ 3, χ the quadratic
character mod 3. Then

  Σ_{n≤x} f(n)f(n+1) = −x/3 + O(log x),
  Σ_{n≤x} f(n)f(n+3) = (5/9)x + O(log x).

*Proof.* Exactly one of n, n+1 is divisible by 3. If neither would be
(n ≡ 1 mod 3): f(n)f(n+1) = χ(1)χ(2) = −1; density 1/3, contribution
−x/3 + O(1). If n = 3^a u (a ≥ 1, 3∤u): the product is (−1)^a χ(u)·χ(n+1)
with χ(n+1) = 1, and Σ_{u≤y} χ(u) = O(1) makes each a-level O(1), total
O(log x); symmetrically for 3 | n+1. For h = 3: the class 3∤n contributes
χ(n)² = 1 at density 2/3; the class 3|n reduces by Lemma 1's mechanism
(d = 3) to the h = 1 sum at x/3, giving (2/3) + (1/3)(−1/3) = 5/9. ∎

Measured at 10^7: −0.3333334 and +0.5555556 (7-digit agreement). A
completely multiplicative ±1 function can fail Chowla maximally: the
conjecture is precisely that λ is far from every character-like
("pretentious") function. This is the known structural obstruction
(Frantzikinakis–Host; MRT), rediscovered from the computation before the
literature was read; recorded as validation, not contribution. Note the
failure constants obey the descent recursion s₃ = 2/3 + s₁/3.

## 3. The certified census (CERTIFIED)

Engine: exact segmented sieve for λ: for each n, the parity of its
small-prime-power divisors plus an exact int64 product of its small-prime
part, which detects the single possible prime factor > √x; integer-only
critical path. Correlation sums are computed as float64 BLAS dot products
of ±1 vectors: every intermediate value is an integer < 2^53, so every
IEEE-754 addition is exact and the results are certified integers.
Validation: brute-force trial division (all of [1, 2·10^5]; windows near
10^9, 3·10^10, 10^12, 2^40); an algorithmically independent
smallest-prime-factor sieve agreeing on all 310 columns at 10^6; two
kernel implementations agreeing on all rows ≤ 10^9.

Certificates checked at every grid row of the full main run (x = 10^12,
50,000 rows), the capped first run (10^11, 5000 rows), and the fine run
(10^9, 2000 rows):

- **C1 (Lemma 1):** S_h(2y) = U_h(2y) + S_{h/2}(y), all even h ≤ 32:
  400,000 (h, x) pairs on the 10^12 grid (40,000 and 16,000 on the
  smaller grids), all exact.
- **C2 (Lemma 3):** S_1..S_7, T_{012}, T_{024}, T_{013}, Q_{0123}
  recomputed as signed census sums equal the directly summed columns at
  every row.
- **C3:** the census sums to x exactly at every row.

External anchors (published values reproduced exactly):

| anchor | published | this census |
|---|---|---|
| L(10^9), …, L(10^12) (A090410) | −25216, −116026, −342224, −522626 | equal, exactly |
| first n with L(n) > 0 (Tanaka 1980) | 906,150,257 | 906,150,257 |
| max L below 10^9 | 829 at 906,316,571 | 829 at 906,316,571 |
| zeros / sign changes of L below 10^9 (BFM) | 252 / 133 | 252 / 133 |
| Turán Σλ(k)/k > 0 to 7.22·10^13 (BFM) | positive | positive at every row |

**Incident disclosure.** The certificates caught and localized transient
memory-corruption events in both long runs: one segment in the first
(10^11) run, and nine events in the 6.5-hour 10^12 run, including two
near-total row wipes and one hit detectable only by C1 (full inventory:
VERDICTS.md, incident #2). Every event was repaired from a deterministic
recompute, raw pre-repair files are kept, and the decisive check is
mutual: the two independently corrupted, independently repaired runs are
bit-identical on all 5000 overlapping rows. The morning event, described
next, is representative. Certificate C2 caught one corrupted segment in
the first run (n ∈ [6.420·10^10, 6.422·10^10]): a ~8 KB page of the
window-code array was zeroed at run time (2039 window counts moved to
pattern 0, total conserved, invisible to C3 and to statistics at 0.1σ of
a cell count; direct correlation columns unaffected). A deterministic
recompute differed from the recorded values and was internally consistent,
identifying transient memory corruption, not a code defect; the census
columns were repaired from the recompute and the raw file is kept
(`data/mainB_1e11_grid_raw.csv`). All certificates pass on the repaired
grid. Columns S_h for odd h ≥ 9 carry no independent per-row certificate
(C2 covers h ≤ 7 and the recorded higher tuples; C1 covers all even h) and
rely on kernel-level validation only.

## 4. Results

### 4.1 Size of the correlations (CERTIFIED integers; NUMERICAL reading)

| x | S_1 | S_2 | S_3 | S_4 | S_5 | S_6 | S_7 | S_8 |
|---|---|---|---|---|---|---|---|---|
| 10^9 | −46,682 | 43,790 | 38,866 | 34,016 | 16,032 | 24,660 | 4,132 | −8,508 |
| 10^10 | −71,450 | −118,586 | 18,508 | 153,922 | 83,042 | 1,176 | 132,516 | 137,364 |
| 10^11 | −219,878 | 153,142 | 494,210 | 65,362 | −62,982 | 479,064 | 142,722 | −203,530 |
| 10^12 | −163,274 | 57,386 | −604,438 | 600,878 | −407,794 | 1,672,602 | −996,980 | −299,864 |

In units of √x these are −1.48…+1.67: every measured S_h (h ≤ 32) is
square-root-sized over the whole range; at 10^12,
max_h |S_h|/√x = 2.149 (h = 13) and RMS_h = 0.898. |S_1(10^12)|/10^12 =
1.63·10^-7. The log-log fit of RMS_h S_h on [10^8, 10^12] gives
α = 0.467, against 0.436 on the range ending at 10^11: the estimate moves
toward 1/2 as range is added, as the single-path-noise reading predicts,
though it remains marginally below the band we registered (see §5). The
*level* is square-root-sized throughout. Fits describe this range only.

### 4.2 Sign-pattern coverage (CERTIFIED by exhibition)

Every ±1 pattern of length k ≤ 30 occurs. Completion points, with the
uniform coupon-collector model 2^k(k ln 2 + γ):

| k | N_k | model ratio |
|---|---|---|
| 20 | 16,599,609 | 1.096 |
| 22 | 59,092,365 | 0.890 |
| 24 | 293,427,643 | 1.016 |
| 25 | 722,808,938 | 1.203 |
| 26 | 1,312,765,349 | 1.052 |
| 27 | 2,794,709,788 | 1.079 |
| 28 | 5,542,425,842 | 1.033 |
| 29 | 11,647,289,153 | 1.049 |
| 30 | 22,249,147,014 | 0.970 |

(Full table k = 1…27 in the data; k ≤ 24 from the fine run, 25–27 from a
dedicated pass to 6·10^9, both exhaustive.) Over k = 10..30 the
measured/model ratio has mean 1.008 and sd 0.12, against the model's own
Gumbel width of 0.07–0.17 across these k: the scatter is the model's own
randomness, with no systematic drift. The k = 25 excursion (ratio 1.203)
is a ~2.6% tail event and is not followed by drift. For context:
occurrence of all patterns with positive density is *proved* only for
k ≤ 3 (MRT 2015). The sequence N_k is not in the OEIS (checked
2026-07-29); submission draft in OEIS_DRAFT.md. At 10^12 the 256
window counts deviate from x/256 by at most 2.98σ (cell 43; 4.21σ at the
10^11 cap), consistent with the Gaussian-max expectation ≈ 3.5 ± Gumbel
width.

### 4.3 Harmonic pair sums (NUMERICAL, rounding-bounded)

ℓ_h(x) = Σ_{n≤x} λ(n)λ(n+h)/n is what the modern theorems bound (trivial
bound log 10^12 ≈ 27.6). Measured: ℓ_1(10^12) = −0.842488; the 32 values
ℓ_h(10^12) have sample sd 1.21 vs the model √(π²/6) ≈ 1.28. Between 10^9
and 10^12 the largest drift over h ≤ 32 was 9.63·10^-5, against an
expected max-of-32 of 9.2·10^-5 under the fair-coin tail model
(σ = 3.2·10^-5): the sums are frozen across three decades. Convergence of the series
Σ λ(n)λ(n+h)/n is itself open: strictly stronger than logarithmic
Chowla, strictly weaker than power-saving Chowla (partial summation:
S_h(t) ≪ t/(log t)^{1+ε} suffices). It is proposed as a benchmark
problem in §7. Harmonic columns are float64 with total rounding error < 10^-8; all
other columns are exact.

### 4.4 A known drift, reproduced (NUMERICAL)

Log-weighted mean of L(x)/√x over the fine grid: −0.671, vs the
conjectured density-mean 1/ζ(1/2) ≈ −0.6848 (pole of ζ(2s)/ζ(s) at
s = 1/2): 2% agreement. Illustration only.

## 5. Out-of-sample validation

PREDICTIONS.md was committed (timestamped 11:10–11:14 PDT) using only
x ≤ 10^9 data and closed-form models, before the main run passed 10^10.
Full scoring in VERDICTS.md, including the 10^12-horizon clauses resolved
when the full run landed; final ledger: **14 scored clauses, 10 hits,
4 misses**.

Hits: RMS level at 10^10, 10^11 and 10^12 (0.898 at 10^12 vs registered
0.90 ± 0.40); pooled cross-scale correlation; census extremes; the
L(10^k) anchors through 10^12; N_26, N_27; harmonic freeze at its
registered 10^12 horizon. Misses, reported as registered: the α sub-fit;
the per-h ±0.05 corridor (2 of 6 outside at 10^11 scale); N_25 (+20%, a
~2.6% tail event, followed by two hits); the hL(10^12) band, calibrated
too low from BFM's local minima.

## 6. The cross-scale echo (NUMERICAL)

Lemma 1 forces ΔS_{2h}[2y, 2y+2Δ) = ΔU_{2h}[2y, 2y+2Δ) + ΔS_h[y, y+Δ):
fluctuations of S_h at scale y are replayed exactly inside S_{2h} at
scale 2y. Under innovation independence with fair-coin variance the
correlation of the coupled increments is exactly 1/√2 = 0.7071, with no free
parameter. Measured (Δ = 4·10^8, 122 disjoint block pairs per h, pooled
over h ∈ {1,2,3,4,6,8}):

  corr = +0.7085 ± 0.0046  (1247 blocks per h; per-h: 0.698, 0.713,
  0.719, 0.711, 0.692, 0.719)

At the pre-registered 10^11 scale the measurement was +0.688 ± 0.017;
with ten times the blocks it converged to within one standard error of
the parameter-free value. The identity supplies the coupling; the data
supplies the 1/√2. To our
knowledge the 2-adic self-similarity of the Liouville correlation field
has not been measured before.

## 7. The measured width of the parity barrier

At x = 10^12: |S_1(x)|/x = 1.63·10^-7 (and RMS_h S_h/x = 9.0·10^-7).
The strongest proven statement at individual scales (Pilatte, Remark 2.8)
bounds this by (log X)^{−c/2} off a sparse set, c inexplicit and
structurally small; numerically ≥ 0.905 for any c ≤ 0.06. For the proven
shape to *reach* the measured value at this x would need c ≈ 9.4. The gap
between what is true (now measured) and what is provable is a factor of
about 5·10^6 (six to seven orders of magnitude) at a scale computers
actually reach. That number is the parity barrier, made concrete.

Open problems, in increasing strength, each strictly between the proved
and the conjectured:

1. **Effectivity.** Exhibit any explicit c > 0 in Pilatte's theorem.
2. **Harmonic convergence.** Prove Σ_n λ(n)λ(n+h)/n converges for some h.
3. **Odd core.** Prove U_h(x) = o(x) for a single even h: by
   Proposition 2 the irreducible obstruction at even shifts.

## 8. Audit of arXiv:2211.09736

The preprint (Carella, math.GM, v2 2023) claims unconditionally that all
four double sign patterns of λ have natural density 1/4 (its Theorem 1.1),
equivalent to unaveraged two-point Chowla, listed as open by Pilatte in
Dec 2025. Its route: eq. (3.9) reduces the claim to
Σ_{n≤x} λ(n)λ(n+t) = O(x/(log log x)^{1/2−ε}) (its Theorem 6.4), obtained
from Helfgott–Radziwiłł's *logarithmically averaged* bound via its Lemmas
6.1–6.2, which assert: if Σ_{n≤x} f(n)/n = o(log x) then Σ_{n≤x} f(n) =
o(x). That implication is false for bounded sequences: f(n) = n^{iα}
(α ≠ 0) has Σ f(n)/n = O(1) while |Σ_{n≤x} f(n)|/x → 1/|1+iα| ≠ 0.
Structurally, the contradiction argument in Lemma 6.1 requires its lower
bound pointwise across the whole integration range, where the negation of
the conclusion supplies it only along a sequence of scales with
uncontrolled sign; ∫ B(z)/z² dz can cancel between scales. Theorems 1.1,
1.2, 6.4, 6.6 there are unproven. (Our census shows the claim itself is
empirically on track: the flaw is in the proof, not the belief.)

## 9. Reproducibility

Machine: Apple M3 Pro (6P+6E, 36 GB). Python 3.12, NumPy 2.3.5. No
randomness in any certified path. Runtimes: fine run 231 s; harmonic
baseline 267 s; first main run 2752 s wall to the 10^11 cap; full 10^12
run 23,362 s wall on 10 workers; coverage extension 978 s; brute
validation 24 s. Scripts (run from
`conjectures/chowla/`): `liouville.py`, `test_liouville.py`,
`census_run.py`, `certify.py`, `coverage_ext.py`, `signchange.py`,
`analyze.py`, `finalize.py`, `explore.py`. Data: `data/*_grid.csv`
(fineA to 10^9; mainB_1e11 capped; mainB12 to 10^12; raw pre-repair
files for both),
`data/*_coverage*.csv`, `data/fineA_firstocc.npz`, `data/*_meta.json`.
Every table refreshes from any grid with one `finalize.py` call.

## 10. The second instrument set (same day, pre-registered separately)

**4-point census (CERTIFIED data, NUMERICAL reading).** Twelve quadruple
correlations Q_{0,a,b,c}(x), six bases and their doubles, with
odd-restricted companions and the 8-window census, on the 2·10^7 grid to
10^11 (`quad_run.py`, 3696 s). Lemma 1 holds verbatim for four factors
(λ(d)^4 = 1), giving the exact certificate
Q_{2a,2b,2c}(2y) = V_{2a,2b,2c}(2y) + Q_{a,b,c}(y); together with Walsh
duality, census totality, and a cross-run identity (census and L columns
bit-identical to the 10^12 grid on all 5000 shared rows), every row is
certified. Results: all twelve quadruples are square-root-sized (RMS of
Q/√x: 0.725 at 10^10, 0.778 at 10^11; max 1.50), against registered
bands hit in full; no theorem controls these sums beyond the trivial
bound, the even-order averaged conjecture being open, and we know of no
prior measurement. The quad descent echo pools to +0.721 ± 0.013 over
the six pairs, consistent with the parameter-free 1/√2.

**The covariance web (NUMERICAL, on the certified 10^12 grid).** At
block scale Δ = 4·10^8: the echo family over all sixteen doubling
channels pools to +0.7069 ± 0.0026 against 1/√2 = 0.7071; all fifteen
same-block cross-shift correlations (registered bands) vanish, max
|corr| = 0.025 against per-pair noise 0.020, pooled +0.0025; the sixteen
innovation-orthogonality channels pool to −0.0066 ± 0.0061 against the
model's 0; and the odd-core RMS_h U_h(x)/√(x/2) stays in [0.92, 1.20]
across 10^9 to 10^12. Every measured entry of the covariance structure
forced or forbidden by the descent web matches the fair-coin
renormalization model. Each vanishing same-block off-diagonal is,
through the n = m pairing, an independent 4-point cancellation test.

**Coverage k = 28, 29, 30 (CERTIFIED by exhibition; minimality per the
registered caveat).** N_28 = 5,542,425,842 (model ratio 1.033),
N_29 = 11,647,289,153 (1.049), N_30 = 22,249,147,014 (0.970): all three
inside the registered coupon bands, every completing position confirmed
by independent recomputation. Every ±1 sign pattern of length ≤ 30
occurs in λ; the coverage law tracks the coupon collector through
thirty doublings. Round-2 ledger: 10 registered clauses, 10 hits.

## References

- C. Pilatte, *Improved bounds for the two-point logarithmic Chowla
  conjecture*, arXiv:2310.19357 (v2, Dec 2025). [pp. 1–11 read]
- T. Tao, *The logarithmically averaged Chowla and Elliott conjectures
  for two-point correlations*, Forum Math. Pi 4 (2016), arXiv:1509.05422.
- H. Helfgott, M. Radziwiłł, *Expansion, divisibility and parity* (2021)
  [statement verified via Pilatte §1].
- K. Matomäki, M. Radziwiłł, T. Tao, *Sign patterns of the Liouville and
  Möbius functions* (2015).
- P. Borwein, R. Ferguson, M. Mossinghoff, *Sign changes in sums of the
  Liouville function*, Math. Comp. 77 (2008), 1681–1694. [read in full]
- M. Tanaka, Tokyo J. Math. 3 (1980), 187–189 [via BFM].
- N. A. Carella, arXiv:2211.09736v2 (math.GM). [read in full; §8]
- OEIS A090410, A008836.

---

## 11. Session 2026-08-01: independent audit, and the first-occurrence spectrum

*Addendum. Same labelling discipline; everything below is either CERTIFIED
(exact integer computation, reproducible) or NUMERICAL (statistics on
certified data). Nothing here is a theorem.*

### 11.1 Clean-room reproduction of the coverage census (CERTIFIED)

The sign-pattern coverage numbers of §4 and §10 were recomputed from scratch by
an implementation sharing no code with the original: `lambda_coverage.c`, an
exact segmented Liouville sieve in C, with `verify_coverage.py` (pure Python
standard library, trial division) as a third check at small k.

Method. Ω(n) = #{(p, e) : p^e | n}, so flipping a parity bit on the multiples
of every prime power p^e ≤ x gives Ω(n) mod 2 without divisions or
factorisation. The segment carries a residue rem[i], initialised to n with its
powers of 2 removed and divided by p at each hit; the division is exact and is
performed by multiplication with p^{−1} mod 2^64. Any n left with rem[i] > 1
carries exactly one prime factor > √x (a second would push n past the segment
top) and receives one final flip. The critical path is integer-only.

Result. All thirty previously certified values reproduce **exactly**, N_k and
the last-completing pattern code alike:

| source | k | status |
|---|---|---|
| `data/fineA_coverage.csv` | 1–24 | 24/24 N_k and 24/24 codes exact |
| `data/coverage_ext.csv` | 25–27 | 3/3 exact |
| `data/coverage_2830.csv` | 28–30 | 3/3 exact |

together with L(10^j) for j = 1..8 (0, −2, −14, −94, −288, −530, −842, −3884),
and N_k for k = 1..14 independently from pure-Python trial division. The
reproduction is recorded in `data/repro_k25_30.csv`.

### 11.1b Coverage extended to k = 33 (CERTIFIED by exhibition)

Every one of the 2^33 = 8 589 934 592 sign patterns of length 33 occurs in λ
below 2·10^11:

| k | N_k | last-completing code | N_k / m·H_m | Gumbel z |
|---|---|---|---|---|
| 31 | 43 901 697 682 | 1 784 492 180 | 0.9265 | −1.26 |
| 32 | 99 494 377 311 | 2 930 773 200 | 1.0179 | +0.32 |
| 33 | 196 202 853 829 | 3 712 643 644 | 0.9740 | −0.48 |

Certification is by exhibition, with the same caveat as §10: the completing
window is exhibited, and minimality — that the pattern occurs nowhere earlier —
has no compact witness and rests on the exhaustive scan. Each of the three
completing windows was recomputed by pure-Python trial division
(`verify_coverage.py window`), as were the last 12, 12 and 10 windows to
complete at each k; `data/endgame_3133.txt` ships the last 256 completions per
k, every one of which is an independently checkable exhibition.

The `Gumbel z` column is (N_k/2^k − ln 2^k − γ)/(π/√6), the coupon-collector
reading of N_k; the model gives it mean 0 and sd 1. Over k = 16..33 the mean z
is +0.24 with no significant trend (least-squares slope −0.02 per unit k),
though the values are not independent (the length-k and
length-(k+1) windows share the same stream). Reading N_k as a ratio to m·H_m
instead, as §10 did, understates the fluctuation at large k, since the same
absolute Gumbel spread is divided by a model that grows like k.

One correction a referee should ask about, and its size. Overlapping windows do
not behave like uniform coupon draws: the fair-coin waiting time for a word w
is Conway's A(w) (§11.2), which reaches 2^{k+1}−2 for a constant word, so the
periodic words might be expected to dominate N_k. They do not.
A(w) ≥ (1+ε)2^k forces an overlap at j ≥ k + log₂ε, hence a period
p ≤ −log₂ε, and there are fewer than 2^{p+1} such words; each is an exponential
of mean at most 2^{k+1}, so the chance that any is unseen at the collector
scale is at most 2^{p+1}·exp(−(k ln 2 + γ)/2). For ε = 0.01 that is 2.9·10^−3
at k = 32 and 2.1·10^−3 at k = 33, so the plain coupon collector is the right
model here to well under a percent (`coverage_model.py`).

Cost: one run, 4 cores, 15 GB, 7387 s wall (sieve 1701 s, window/bitmap probes
5677 s), peak RSS ≈ 2.5 GB; N_31 at 1718 s, N_32 at 3774 s. Log:
`data/coverage_3133.log`.

### 11.2 The first-occurrence spectrum and Conway's leading number (NUMERICAL)

The coverage census reports one order statistic, N_k = max_w s(w), where s(w)
is the start index of the first occurrence of pattern w. The full spectrum
{s(w) : w ∈ {±1}^k} carries 2^k data points, and for an i.i.d. fair coin it has
an exact, parameter-free, *per-pattern* prediction. Conway's leading number
(Solov'ev's formula) gives the expected waiting time to the first occurrence of
a word w of length k as

    A(w) = Σ_{j=1}^{k} δ_j(w) · 2^j,     δ_j(w) = 1 iff prefix_j(w) = suffix_j(w),

measured at the position of the last letter. With s(w) the *start* index, the
model prediction is E[s(w) + k − 1] = A(w). Define

    R(w) = (s(w) + k − 1) / A(w),        model: E[R(w)] = 1 for every w.

A(w) spans a factor of two, from 2^k for a word with no self-overlap to
2^{k+1} − 2 for a constant word. That self-overlap clumping dominates the raw
first-occurrence times and is a property of words, not of λ; normalising by
A(w) removes it exactly, which is what makes the residual measurable.

Calibration is by control, not by formula: the 2^k values s(w) come from a
single stream and are not independent, so σ/√(2^k) is the wrong error bar.
`lambda_coverage --prng` runs an i.i.d. fair-coin stream through the identical
window, bitmap and first-occurrence code path, and all error bars below are the
dispersion of 32 such streams.

**Measurement at k = 24** (all 16 777 216 patterns; λ scanned to
N_24 = 293 427 643; `data/firstocc_k24_*`):

| quantity | λ | 32 controls | λ in control-σ |
|---|---|---|---|
| mean R | 1.000123 | 0.999953 ± 0.000319 | +0.53 (rank 23/33) |
| sd of R | 1.000251 | ≈ 1.0004 | — (Exp(1) shape) |
| slope of mean R vs popcount | −2.64·10^−4 | −1.10·10^−4 ± 3.53·10^−4 | −0.44 |

The control ensemble's mean sits −0.8 SE from the exact model value 1, so the
statistic is unbiased. The overlap-class breakdown is flat at 1.000 for λ and
for the controls, confirming the normalisation.

The popcount slope is not free structure. Across the 32 controls it correlates
at r = +0.80 with the stream's own realised one-point bias L(10^7)/10^7; a
density excess must tilt a popcount-resolved waiting time, and to first order
the tilt is −4δ with δ = −L(x)/2x. Regressing λ's slope through that
control-calibrated relation leaves a residual of **−0.56 residual-σ**. (The
fitted coefficient is 0.92 ± 0.12 rather than the first-order 2, as expected:
the relevant density is a weighted average over the whole range of
first-occurrence times, not its value at the single reference scale 10^7. The
regression is used as a calibration, not as a prediction.)

**Reading.** Over the ensemble of all 2^24 sign patterns of length 24, the
first-occurrence spectrum of λ is indistinguishable from an i.i.d. fair coin at
a resolution of about 3·10^−4, once λ's known one-point bias is accounted for.
This is a statement about 24-point behaviour in a range where the two-point
conjecture is open — and it is evidence only. The parity barrier predicts
precisely this: unlimited numerical pseudorandomness, no purchase on a proof.

**Negative result, disclosed.** The first control ensemble was defective and
the control itself is what exposed it. Streams seeded as sm64(n ⊕ seed) share
their bit multiset for small seeds — every seed returned L(10^8) = +16362 to
within 2 — which collapsed the ensemble dispersion and made the λ popcount
slope read as a 4.4σ anomaly. With decorrelated seeding the same slope is
−0.44σ. Recorded because an ensemble of controls that is secretly one control
is the specific way this instrument fails.

### 11.3 Reproducibility defect found in this repository

The sandbox for this session had Python 3.11, gcc, 4 cores, and no network.
It had no NumPy, no SciPy and no networkx, and no way to install them. Every
Python script in this directory imports NumPy, so none of the previously
certified results could be rerun on that machine at all. The C path added here
(`lambda_coverage.c`, `firstocc_stats.c`) and the stdlib-only
`verify_coverage.py` are together a dependency-free route to the coverage
results. The rest of the pipeline — census, quads, covariance web — remains
NumPy-only and is not reproducible on a clean machine without it.
