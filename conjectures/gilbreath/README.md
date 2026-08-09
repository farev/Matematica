# Gilbreath's conjecture (Proth 1878, Gilbreath 1958)

Write the primes in a row and repeatedly take absolute differences of adjacent
entries:

```
p   :   2   3   5   7  11  13  17  19  23  29  31  37 ...
d^1 :   1   2   2   4   2   4   2   4   6   2   6 ...
d^2 :   1   0   2   2   2   2   2   2   4   4 ...
d^3 :   1   2   0   0   0   0   0   2   0 ...
```

**Conjecture.** Every row after the first begins with 1. Open since 1878.

Chosen because it sits on a fault line: it *looks* like a theorem about primes,
but everything below suggests it is really a theorem about prime-gap statistics
plus a lucky seed — and pieces of it are provable by elementary means today.

**Status:** active
**Sessions:** [2026-07-28](../../log/2026-07-28-gilbreath.md), [2026-07-29](../../log/2026-07-29-gilbreath.md), [2026-07-29 (R3)](../../log/2026-07-29-gilbreath-r3.md)
**Write-up page:** [fabianarevalo.com/gilbreath](https://fabianarevalo.com/gilbreath)

## Results

| Claim | Label | Where |
|---|---|---|
| `c_n ≥ 2·exp(−Σ_{k<n} c_k)` for `n ≥ 2` — factor-2 sharpening of Chase–Hunter–Tao Prop. 2.1, giving `Σ_{i≤n} c_i ≥ log(2n − 2 + e²)` and improving their Thm 1.4 by an additive `log 2` | **PROVED** | [NOTE.md](NOTE.md) §5, Theorem 2 |
| The sign arrangement realises all `2^{i(i+1)/2}` chambers — every sign history occurs, so the model has no combinatorial obstruction | **PROVED** | [NOTE.md](NOTE.md), Prop. 9 |
| Exact rational `c₄`, `c₅`, `c₆` with partition-of-unity certificates in ℚ, extending the `c₀…c₃` of Chase–Hunter–Tao. `c₆` is a 153-digit over 154-digit fraction | **CERTIFIED** | `c6_certified.txt`, [NOTE.md](NOTE.md) §4 |
| Gilbreath holds for the first 455,052,510 rows (primes < 10¹⁰), `k* = 329`, via Odlyzko's propagation criterion | **CERTIFIED** | `verify_big.py` |
| Chase–Hunter–Tao Thm 1.6 hypotheses audited against real primes: both dangerous block structures sit 11 and 25 orders of magnitude below threshold up to 10⁹ | **CERTIFIED** | `block_audit.py` |
| Submask law `c_i ≈ C·i^{−α}·Σ_{m ⊆ i} q^m`, `α ≈ 0.798`, `q ≈ 0.685`, `C ≈ 1.14`. `R² = 0.980` on `i ∈ [64, 1023]`; predicts `i ∈ [1024, 4095]` out-of-sample at `R² = 0.90`, median relative error 13%. Pure power law fails (R² < 0) | **NUMERICAL** | `final_validation.py`, [NOTE.md](NOTE.md) §6 |
| Depth-1 zero-blocks of the CHT array are CPAPs (Lemma M1); prime APs in `(k, x]` have length `≤ 1.25 log x + O(1)` (primorial rigidity, known mechanism), so **CHT hypothesis (ii) at depth 1 holds unconditionally** with margin `log⁹x` | **PROVED** | [MICROSCOPE.md](MICROSCOPE.md) §2–3 |
| Two-valued rigidity (Lemma M6): odd `q \| B−A`, `q ∤ A` caps `{A,B}`-gap runs at `q−2`, so **CHT hypothesis (iii) at depth 0 holds unconditionally for every d with odd part > 1**; bounds attained exactly at `d = 5, 7, 10, 14` on primes < 10⁹. Surviving case `d = 2^s` reduced to a twin-clustering bound with `log x/loglog x` slack (Cor. M9); bounded-gap runs killed absolutely via Montgomery–Vaughan (`{2,6}` ≤ ~27,000 forever); periodic-sign depth-2 structures annihilated (Lemma M11) | **PROVED** | [MICROSCOPE.md](MICROSCOPE.md) §7, `lens_check.py` |
| Dichotomy for depth-2 blocks (Lemma M13): every odd prime factor of the second-difference parameter `w` either caps the block at `q−1` primes or imprisons it in a residue class mod `q`; long escapees have `w = 2^s` with forced gap alternation mod `2^{s+1}`. Verified on 388,068 blocks < 10⁹, zero violations, threshold saturated exactly 922 times. Kernel principle: all surviving enemies are 2-adic or same-class-run-shielded — provably beyond covering and density methods | **PROVED** | [MICROSCOPE.md](MICROSCOPE.md) §8 |
| Theorem R1: Cramér + residual pattern axiom P (strictly narrower than CHT's hypotheses, by the lenses) ⇒ Gilbreath for all but finitely many rows | **PROVED** (reduction) | [REDUCTION.md](REDUCTION.md) §2 |
| Theorem R2: a sequence with all fixed-order Cramér gap statistics (perturbed by `O_k(loglog x)`) whose Gilbreath leads fail infinitely often — so **no fixed-order statistical axiom system implies eventual Gilbreath**; plants verified to derail at exactly row `m−1` | **PROVED** | [REDUCTION.md](REDUCTION.md) §3, `reduction_check.py` |
| Open Problem R3: fixed-order statistics + `o(n)` entries ⇒ eventual Gilbreath? Attacked 2026-07-29: reframed strong/weak, negative route exhausted, affirmative skeleton (S1)–(S3) identified | open | [R3.md](R3.md) |
| Parity-transform package: erosion-path parity = `S·rev(y)`, lead parity = `S·y`, `S² = I`, `SσS = I+σ`, dyadic doubling; corridor systems always solvable with solution space = anchored `2^B`-periodic strings; deep parity rows vanish below depth `2^B` (nilpotency) | **PROVED** | [R3.md](R3.md) §1, `r3_identities.py` |
| The brief's parity-steered corridor self-destructs: forced non-cooling to `{0,2}`, erosion 0.71/row (worse than the 0.56 i.i.d. control), the `V = 3·T_cool`-scale plant dies; but the periodic prefix alone derails leads at density 0.33–0.50 with `O(log x)` entries | **NUMERICAL** (mechanism PROVED) | [R3.md](R3.md) §2, `r3_corridor.py` |
| Bounded-entry failure of Gilbreath: `a_n = 2·geometric` has a.s. infinitely many bad leads (via CHT Thm 1.2 + pairwise-independent lead parities at depths `2^j`), making CHT's "could very well be false" remark precise | **PROVED** | [R3.md](R3.md) §5, Prop. R3.4 |
| Theorem R3.5: for every K, an independent sequence with bounded entries and model-quality window statistics to order K whose leads exceed 1 at positive density, so every finite-order axiom set fails with bounded entries, and CHT Thm 1.3's 2-separated axiom (ii) is necessary, invisibly to all fixed orders | construction + statistics **PROVED**; persistence **NUMERICAL** | [R3.md](R3.md) §5 |
| Lemma R3.6 + Corollary R3.7 (lead-parity rigidity): lead parities vanishing beyond `s₀` force exact `2^⌈log₂ s₀⌉`-periodic top parities; hence all-orders weak statistics force odd leads infinitely often, eliminating the "leads eventually even" failure mode unconditionally | **PROVED** | [R3.md](R3.md) §7, `r3_identities.py` |
| Theorems R3.9 + R3.10 (toward phase confinement): bulk-rooted heat in a generic strip dies below depth `O(ε⁻¹ D₀ log W)` (corollary of CHT Prop. 4.1 applied to interior cones), and `≤2`-valued transport crossing at speed above `v* ≈ 0.773` (root of `H(v) = v`) is exponentially suppressed; the single remaining gap is the slow-crossing renewal lemma (Open Lemma R3.11), whose finite-budget count already predicts the measured `Θ(1)` penetration | **PROVED** (reductions); R3.11 open | [R3.md](R3.md) §7 |
| Cooling race: period-P parity structures survive as `{0,2}` phase iff `P ≲ P*(μ) ≍ μ^{0.84±0.04}`, and `P*` matches the directly measured cooling time within 20% (the race mechanism confirmed); front pinning: a `{0,2}` ocean cannot invade a cooled `{0,1}` strip at any tested entry scale (penetration ≤ 5 columns up to `μ = 4096`, interface value scale 2 independent of `μ`); the residual ballistic channel has range `≈ 2V` with erosion toll 1/2 per row, now PROVED conditionally (Lemma R3.8, pairwise-independent path parities); together these seal every corridor-type route to a negative R3 | **NUMERICAL** (R3.8 conditional PROVED) | [R3.md](R3.md) §3–4, `r3_boundary.py`, `r3_front.py` |
| Microscope calibration: all dangerous micro-patterns in real primes to 10¹⁰ grow like `≤ 1.4·log x` (CPAP 6, alternating-parity runs 32, two-valued runs 10), 12+ orders below the `log¹⁰x` thresholds; alternation outpaces repetition (Lemke Oliver–Soundararajan bias) | **NUMERICAL** | `microscope_bench.py`, [MICROSCOPE.md](MICROSCOPE.md) §5 |

Implication of the last row: the tentative `c_i ≍ 1/i` of Chase–Hunter–Tao
Remark 1.5 is untenable in the computationally accessible range — partial sums
grow like `n^{1/5}`, not `log n`.

**Presentable note: [NOTE.md](NOTE.md)** — the paper-shaped artifact, with
numbered theorems and proofs. Also as a shareable page, `note_artifact.html`.

**Session narrative: [WRITEUP.md](WRITEUP.md)** — including an honest account of
what is new, what is rediscovered, and what failed.

## Scripts

Run from inside this directory — they resolve data files by bare relative name.

### Part I — the conjecture itself

| file | what it does | headline result |
|---|---|---|
| `explore.py` | small-scale triangle, first counterexamples | intuition |
| `verify.py` | rigorous verification via the propagation lemma | conjecture holds for 50.8M rows (primes < 10⁹), k\* = 248 |
| `verify_big.py` | segmented sieve to 10¹⁰ | **conjecture holds for the first 455,052,510 rows**, k\* = 329 |
| `experiments.py` | k\*(x) growth, defect decay, shuffled/i.i.d. gap models | defects decay ×0.936/row; shuffled gaps fail instantly |
| `prefix_experiment.py` | how much authentic prime prefix is needed | seed threshold ≈ 16–32 gaps |
| `meanfield.py` | branching statistics, parity-rigidity check | mean-field branching is exactly critical; Sierpiński period-4 modulation |

### Part III — the R3 session (parity transforms, corridors, fronts)

| file | what it does | headline result |
|---|---|---|
| `r3_common.py` | shared machinery: Sierpinski matrix, conditioned sampling, de Bruijn blocks, traces | — |
| `r3_identities.py` | exact F₂ verification of the transform lemmas | all PASS |
| `r3_corridor.py` | the attack brief's experiment 1, plus the alternating case | corridor self-destructs; periodic prefix alone derails leads |
| `r3_hierarchical.py` | layered growing periods, replication law, stats vs i.i.d. control | replication exact; sealed at first generic band |
| `r3_nested.py` | nested-block two-scale construction | dead beyond depth 66: the cooling race |
| `r3_front.py` | `{0,2}` ocean vs cooled strip front measurement | front pinned, penetration ≤ 2 columns |
| `r3_front2.py` | pinning stress test at `μ` up to 4096 | phase pinned at all `μ`; ballistic channel isolated (range `≈ 2.3μ`, toll 0.52/row) |
| `r3_boundary.py` | (period, entry-scale) viability grid | phase boundary, coarse |
| `r3_boundary_fit.py` | crossings, cooling times, deep persistence | `P* ≍ μ^{0.84±0.04} ≈ T_hot`; density stationary to 49k |

### Part II — the Chase–Hunter–Tao program (arXiv 2607.08712, July 2026)

| file | what it does | headline result |
|---|---|---|
| `block_audit.py` | audits CHT Theorem 1.6 hypotheses on real primes | dangerous blocks are 10¹¹ and 10²⁵ below thresholds (primes < 10⁹) |
| `ck_exact.py` | exact rational c_i by sign-chamber cone decomposition | **c₄ = 778959731701/1447295850000, c₅ = 0.55325784… (31-digit fraction)**; chamber count = 2^{i(i+1)/2} (proved) |
| `ck_exact_certified.py` | exact pipeline with partition-of-unity certificate in ℚ | double-Delaunay cross-check + exact pulling-triangulation fallback; ∑Z = 1 exactly |
| `ck6_parallel.py` | first parallel c₆ attempt over 2,097,152 chambers | c₆ ≈ 0.448389, **uncertified** — partition deficit 1.7×10⁻⁷ (superseded) |
| `ck6_certified.py` | certified c₆ | **c₆ = 0.448388672133…**, exact fraction in `c6_certified.txt` |
| `ck_montecarlo.py` | tiered MC of c_i to i = 1023 | **digit-sum law**: c_i ≈ i⁻¹·ρ^s(i), ρ ≈ 1.22; S_n ≈ 10.84·n^{1/5} |
| `ck_mc_deep.py` | deep MC to i = 4095, merged with the tiered run | `ck_mc_deep.csv` (keeps whichever estimate has smaller SE) |
| `ck_analysis.py` | fits/regressions on the MC data | pure c_i ~ 1/i rejected (R² < 0); +ν₂(i) covariate → R² 0.68 |
| `f64_check.py` | audits the float32 MC against an independent float64 run | agreement within 2.5σ at five checkpoints |
| `final_validation.py` | out-of-sample test of the submask law on i ∈ [1024, 4095] | fitted on [64, 1023] only → R² = 0.90 |

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `c6_certified.txt` | `ck6_certified.py` | exact c₆ as a rational, ∑Z = 1 certificate |
| `c6_uncertified.txt` | `ck6_parallel.py` | superseded value, wrong by 1.25×10⁻⁷ — kept for the record |
| `ck_montecarlo.csv` | `ck_montecarlo.py` | tiered MC estimates to i = 1023, with standard errors |
| `ck_mc_deep.csv` | `ck_mc_deep.py` | deep MC to i = 4095 |
| `f64_check.log` | `f64_check.py` | float32-vs-float64 audit record |
| `oeis_draft.txt` | — | OEIS submission draft for the c_i numerators and denominators |
| `note_artifact.html` | — | shareable rendering of NOTE.md |

## Reproduction

```bash
cd conjectures/gilbreath

python3 verify.py 1e6          # seconds — the fast tier, also run in CI
python3 verify.py 1e9          # 50.8M rows, k* = 248
python3 verify_big.py          # ~2.5 min, ~3 GB RAM — the 10^10 result
python3 ck6_certified.py       # ~11 min on 11 cores — exact c_6
python3 ck_montecarlo.py       # ~14 min — the tiered Monte Carlo
python3 final_validation.py    # out-of-sample test of the submask law
```

Python 3 + NumPy, plus SciPy for `ck_exact.py`.

## Known defects and open threads

- **`ck_analysis.py` reads `c6_exact.txt`, which does not exist.** The certified
  value lives in `c6_certified.txt`. Fix before relying on that script.
- **New adjacent paper (flagged 2026-08-09, unread here):** Muney,
  "Holes in Valid-Extension Sets of Finite Gilbreath Sequences",
  arXiv:2606.23721 (Jun 2026, 36 pp., (secondary)) — the set of integers
  appendable to a finite Gilbreath sequence can have interior holes
  (smallest failure at (2,3,5,9,15)), refuting an interval-shaped
  characterization proposed in earlier literature; gives an exact
  membership criterion and an interval-filling condition described as an
  order-sensitive Brown-completeness analogue. Opens a cheap computational
  surface against this repo's prime machinery (hole statistics of
  prime-prefix extension sets); read the PDF before building on it.
- ~~The arXiv reference 2607.08712 has not been independently verified.~~
  Resolved 2026-07-29 (R3 session): the paper exists as cited (Chase, Hunter,
  Tao, "Gilbreath's conjecture: a Cramér random model and a deterministic
  analysis", 28 pp., math.CO), and Thm 1.3, Lemma 3.10, and Remark 4.5 were
  read verbatim from the PDF and match this repository's records.
- Universality: does the submask law survive uniform initial data instead of
  exponential? If yes, it is a property of the iteration, not the distribution.
- `q ≈ 0.685` and `α ≈ 0.798` are measured, not derived. Nothing yet explains
  either, and a closed form would be the real prize.
- Push the Monte Carlo to `i ~ 10⁴` to test whether the ρ-ladder and the
  `n^{1/5}` partial-sum growth persist. Needs ~10× compute or variance
  reduction.
- Formalize Lemmas 1–5 (parity, propagation, defect descent) in Lean 4. They are
  elementary and would give the core a machine-checked base.
- Submit the c_i numerator/denominator sequences to OEIS — `oeis_draft.txt` is
  written and ready.

## Prior work

Proth published a flawed proof in 1878; Gilbreath rediscovered the pattern in
1958. Odlyzko (1993) supplied the propagation criterion that makes finite
verification rigorous, and it is what `verify.py` implements. Chase, Hunter and
Tao (arXiv:2607.08712, July 2026) introduced the continuous model that Part II
works in, and computed `c₀…c₃`.

The lower-bound inequality of their Proposition 2.1 was independently
rediscovered during this session before it was recognised as theirs. That is
recorded as a rediscovery, not a result — see [WRITEUP.md](WRITEUP.md) §11. The
factor-2 sharpening built on top of it is new.
