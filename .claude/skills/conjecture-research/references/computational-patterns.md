# Computational patterns for conjecture research

Recipes distilled from real sessions. All Python 3 + NumPy (+ SciPy where
noted); exact work uses `fractions.Fraction` and integer linear algebra.

## Contents
1. Prime generation (fast sieves, segmented)
2. Iterated-map verification with a propagation certificate
3. Tiered Monte Carlo for depth-indexed expectations
4. Run-length / block scanning (auditing block hypotheses)
5. Exact rational integration over polyhedral cones
6. Exact linear algebra kernels
7. Statistical hygiene
8. Background-job orchestration

---

## 1. Prime generation

Odds-only NumPy sieve to ~10⁹ (≈3 s, ≈500 MB):

```python
def primes_up_to(n):
    half = (n - 1) // 2                       # index i <-> odd 2i+1
    sieve = np.ones(half + 1, dtype=bool); sieve[0] = False
    for i in range(1, (int(n**0.5) - 1)//2 + 1):
        if sieve[i]:
            p = 2*i + 1
            sieve[(p*p - 1)//2::p] = False
    return np.concatenate(([2], 2*np.nonzero(sieve)[0][... ] + 1))
```

Beyond ~10⁹, segment: base primes to √limit, then per-segment odds-only
bitmaps; carry the last prime across segments to keep the gap stream
unbroken. Gaps below 10¹⁰ fit int16; store gap/2 in uint8 if memory-bound
(all gaps beyond the first are even).

## 2. Iterated-map verification with a certificate

Pattern for conjectures about iterated maps on sequences (Gilbreath-type):
prove a propagation lemma ("row of form X ⇒ all deeper rows of form X"),
then iterate with NumPy until the criterion fires:

```python
row = np.abs(np.diff(seq)).astype(np.int16)
k = 1
while np.any(row[1:] > 2):          # criterion not yet reached
    assert row[0] == expected_lead   # direct check for shallow rows
    row = np.abs(np.diff(row)); k += 1
# criterion fired at k*: lemma covers all deeper rows -> rigorous claim
```

Report: "conjecture holds for the first N instances, certified by the
criterion at k\* = …". Track the full trajectory (defect counts, front
positions) — the dynamics is where discoveries live, not the bound.

## 3. Tiered Monte Carlo

For E[f(depth i)] across a wide range of i: many samples shallow, few
deep, merged by smallest standard error per index.

```python
TIERS = [(63, 40_000_000, 2_000_000),   # (max depth, samples, batch)
         (255, 6_000_000, 500_000),
         (1023, 600_000, 150_000)]
```

- One batch = array (batch, depth+1); iterate the map along axis 1,
  recording column 0's mean/variance at every depth (all depths for the
  price of the deepest).
- float32 doubles throughput; audit precision statistically (see §7).
- Fix seeds. Save mean AND standard error per index to CSV.
- Anchor against every exactly known value before trusting anything new.

## 4. Run-length / block scanning

Auditing "no long block of zeros / no long two-valued block" hypotheses on
a huge array, per row: get `nz = np.flatnonzero(row)`; zero-runs are
`np.diff(nz) - 1` plus the two edges; for {0,d}-blocks, split `row[nz]`
into constant-value segments (`np.flatnonzero(vals[1:] != vals[:-1])`) —
a segment of value d spans from just after the previous non-d nonzero to
just before the next. O(n) per row, vectorized. Report worst offender vs
the paper's threshold as a margin (orders of magnitude).

## 5. Exact rational integration over polyhedral cones

For expectations of piecewise-linear functionals of i.i.d. Exp(1)
variables (and similar): enumerate sign chambers; on each chamber the
functional is linear on a cone.

- Over a simplicial cone with integer rays w_1..w_d and s_k = ⟨1, w_k⟩:
  ∫ e^{−⟨1,x⟩} = |det W| · Π 1/s_k, and
  ∫ ℓ(x) e^{−⟨1,x⟩} = |det W| · (Π 1/s_k) · Σ_k ℓ(w_k)/s_k.
- Rays by exact integer **double description**: start from the orthant
  (rays = e_j), add constraints one at a time; new rays from adjacent
  (+,−) pairs, w = (h·r₊)r₋ − (h·r₋)r₊, reduced to primitive; adjacency
  test via zero-set bitmasks (no third ray's zero-set contains the pair's
  intersection).
- Triangulation: floating Delaunay of the cross-section for combinatorics
  ONLY — run **two** independent generic projections; accept only if both
  give identical exact (Z, I); otherwise fall back to an exact pulling
  triangulation: facets = constraints whose zero-ray set has exact rank
  d−1; recurse into facets, cone from a fixed ray.
- **Certificate**: Σ over all chambers of the e^{−⟨1,x⟩} integrals must
  equal exactly 1 in ℚ. Compute it always; a failed certificate means a
  wrong exact value even when Monte Carlo agrees (observed: an error of
  1.25×10⁻⁷ invisible at 0.8σ).
- Parallelize by fixing sign-prefixes across a process pool; Fractions
  pickle fine.

## 6. Exact linear algebra kernels

- Integer determinant: Bareiss (fraction-free) — exact, no overflow
  surprises in Python ints.
- Exact rank: fraction-free Gaussian elimination over Fraction.
- Primitive vectors: divide by gcd; dedupe with tuples.

## 7. Statistical hygiene

- **Chaotic maps decorrelate float32 from float64 pathwise.** Same-seed
  pairing does NOT cancel sampling noise after decorrelation, so a paired
  comparison can only bound bias at the level of independent-run σ. Audit
  with a separate float64 run and compare means with σ from both.
- Weight regressions by inverse relative error; prefer model-free
  confirmations (subsequence log-log fits, ratio tables at structured
  indices) alongside any fitted law.
- The escalation ladder: free-parameter fit → parsimonious law (1–2
  params matching the free fit is structure) → cross-validation →
  out-of-sample prediction at NEW scales → mechanism knob-turn.
- Beware covariate collinearity (digit-sum vs log i vs 2-adic valuation);
  quote coefficient values as model-dependent, structure as robust.

## 8. Background-job orchestration

- Launch anything > ~2 min with `run_in_background`; write scripts to
  files (heredoc + `&` does not survive the shell).
- `cd` into the project dir inside the command — background shells reset
  cwd.
- Progress lines with `flush=True`; then `tail` the task output file to
  poll.
- Keep a waiter (`until [ -f result.csv ]; do sleep 10; done`) armed as a
  background task so the result re-invokes you.
- Interleave: while jobs run, do theory, read literature, draft documents
  with explicit `[PENDING]` placeholders, and grep for stale placeholders
  before delivering.
