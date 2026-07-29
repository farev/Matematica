# Gilbreath's conjecture — research sessions

**Public-facing note: [NOTE.md](NOTE.md)** — the presentable results:
exact c₄–c₆ with certificates, Theorem 2 (c_n ≥ 2·exp(−Σ_{k<n} c_k),
sharpening Chase–Hunter–Tao Prop. 2.1), the submask law, and the audits.
Also as a shareable page: `note_artifact.html`.

**Session narrative: [WRITEUP.md](WRITEUP.md)** — proofs, verification
results, dynamics, the Chase–Hunter–Tao engagement, and an honest account
of what is new, what is rediscovered, and what failed.

## Part I — the conjecture itself

| file | what it does | headline result |
|---|---|---|
| `explore.py` | small-scale triangle, first counterexamples | intuition |
| `verify.py` | rigorous verification via the propagation lemma | conjecture holds for 50.8M rows (primes < 10⁹), k\* = 248 |
| `verify_big.py` | segmented sieve to 10¹⁰ | **conjecture holds for the first 455,052,510 rows**, k\* = 329 |
| `experiments.py` | k\*(x) growth, defect decay, shuffled/i.i.d. gap models | defects decay ×0.936/row; shuffled gaps fail instantly |
| `prefix_experiment.py` | how much authentic prime prefix is needed | seed threshold ≈ 16–32 gaps |
| `meanfield.py` | branching statistics, parity-rigidity check | mean-field branching is exactly critical; Sierpiński period-4 modulation |

## Part II — the Chase–Hunter–Tao program (arXiv 2607.08712, July 2026)

| file | what it does | headline result |
|---|---|---|
| `block_audit.py` | audits CHT Theorem 1.6 hypotheses on real primes | dangerous blocks are 10¹¹ and 10²⁵ below thresholds (primes < 10⁹) |
| `ck_exact.py` | exact rational c_i by sign-chamber cone decomposition | **c₄ = 778959731701/1447295850000, c₅ = 0.55325784... (31-digit fraction), both certified**; chamber count = 2^{i(i+1)/2} (proved) |
| `ck6_parallel.py` | parallel c₆ over 2,097,152 chambers | c₆ ≈ 0.448389, **uncertified** (partition deficit 1.7×10⁻⁷, see below) |
| `ck_montecarlo.py` | tiered MC of c_i to i = 1023 (`ck_montecarlo.csv`) | **digit-sum law**: c_i ≈ i⁻¹·ρ^s(i), ρ ≈ 1.22; S_n ≈ 10.84·n^{1/5} |
| `ck_analysis.py` | fits/regressions on the MC data | pure c_i ~ 1/i rejected (R² < 0); +ν₂(i) covariate → R² 0.68 |

### Status notes

- **c₆ is certified** as of the second session pass: `ck_exact_certified.py`
  (double-Delaunay cross-check + exact pulling-triangulation fallback via
  integer rank tests) achieves ∑Z = 1 exactly; result in
  `c6_certified.txt` (0.448388672133…). The earlier `c6_uncertified.txt`
  (kept for the record) was wrong by 1.25×10⁻⁷.
- **Theorem 2** (two-channel bound, NOTE.md §5): proof verified
  numerically step-by-step at n = 6 on 4×10⁶ samples.
- float32 MC audited against an independent float64 run: agreement within
  2.5σ at five checkpoints (bias ≲ 1–2%; structural effects 20–370%).
- Deep MC to i = 4095 (`ck_mc_deep.py` / `ck_mc_deep.csv`) provides the
  out-of-sample test of the submask law; `final_validation.py` runs it.

Everything runs with Python 3 + NumPy (+ SciPy for `ck_exact.py`).
The 10¹⁰ verification needs ~3 GB RAM and ~2.5 min; c₆ took 11 min on 11
cores; the full MC took ~14 min.
