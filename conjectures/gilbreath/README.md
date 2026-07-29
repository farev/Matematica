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
**Sessions:** [2026-07-28](../../log/2026-07-28-gilbreath.md)
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
- **The arXiv reference 2607.08712 has not been independently verified** to
  resolve as cited. Everything in Part II rests on it. Check before this note
  goes any further than the repository.
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
