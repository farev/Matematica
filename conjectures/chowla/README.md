# chowla: two-point correlations of the Liouville function

**Statement.** Chowla's conjecture (two-point case): for every h ≥ 1,
S_h(x) = Σ_{n≤x} λ(n)λ(n+h) = o(x). Open for every h; the model instance
of the parity barrier. Write-up: <https://fabianarevalo.com/chowla>.

**Status.** Open (of course). This session: exact descent/duality lemmas
(PROVED); certified correlation + sign-pattern census on a 2·10^7 grid to
x = 10^12 and fine grid to 10^9, all rows passing exact certificates
C1–C3 (400,000 C1 pairs on the 10^12 grid) and matching every published
anchor: A090410 at 10^9 through 10^12, the Pólya island, BFM's 252 zeros
/ 133 sign changes (CERTIFIED); every sign pattern of length ≤ 27 occurs
(N_27 = 2,794,709,788; sequence N_k new to OEIS; CERTIFIED by exhibition);
pre-registered predictions scored 10 hits / 4 misses on 14 clauses
(VERDICTS.md); cross-scale echo measured +0.7085 ± 0.0046 vs the
parameter-free 1/√2 = 0.7071 (NUMERICAL); measured parity-barrier gap
≈ 5·10^6 at 10^12 vs Pilatte's Remark 2.8 (NOTE §7); audit of
arXiv:2211.09736 locating an invalid average-transfer step (NOTE §8).
The certificates caught and repaired ten transient memory-corruption
events across the two long runs; the independently repaired runs are
bit-identical on their 5000-row overlap (NOTE §3, VERDICTS.md). Round 2
(same day, PREDICTIONS2/VERDICTS2): certified 4-point census to 10^11
(first data at an order where even averaged Chowla is open; all twelve
quadruples square-root-sized), the full covariance web matching the
fair-coin renormalization model in every entry (16-channel echo
+0.7069 ± 0.0026 vs 1/√2), and coverage extended to every pattern of
length ≤ 30 (N_30 = 22,249,147,014); 10 registered clauses, 10 hits.

| script | what it produces |
|---|---|
| `liouville.py` | exact segmented λ sieve (library) |
| `test_liouville.py` | brute-force + segmentation validation |
| `census_run.py X S W P [--coverage K]` | certified census grid CSV (+ coverage) |
| `certify.py P_grid.csv` | exact certificate check C1–C3 |
| `coverage_ext.py X S OUT [--ks a,b,c]` | first-coverage N_k (run to k = 30) |
| `quad_run.py X S W P` / `certify_quad.py` | certified 4-point census + certificates |
| `covariance_web.py` / `quad_analysis.py` | covariance-web and quad scoring |
| `signchange.py X` | zeros / sign changes of L; S_1 path stats |
| `analyze.py P_grid.csv` | scaling, bias, census extremes, 1/√2 test |
| `explore.py` | phase-1 exploration incl. character near-miss |

Reproduce (from this directory):

```bash
python3 test_liouville.py
python3 census_run.py 1e9 5e5 1 data/fineA --coverage 24
python3 certify.py data/fineA_grid.csv
python3 analyze.py data/fineA_grid.csv
```

Main run (6.5 h on an M3 Pro; grid valid at any prefix):
`python3 census_run.py 1e12 2e7 10 data/mainB12`.

Data: `data/*_grid.csv` (certified integer columns + float64 harmonic
columns; committed as .gz, all < 7 MB), `data/*_coverage*.csv`,
`data/*_meta.json` (runtimes/machine). `data/fineA_firstocc.npz` (exact
first-occurrence index of every sign pattern, k ≤ 24; 135 MB) exceeds the
repo's ~10 MB limit → destined for Zenodo, kept locally meanwhile. Documents: NOTE.md (paper-shaped), WRITEUP.md (lab
notebook), PREDICTIONS.md / VERDICTS.md (out-of-sample protocol).

**Known defects.** Harmonic columns are float64 with a rigorous < 10^-8
rounding bound, not exact rationals. Columns S_h for odd h ≥ 9 carry no
independent per-row certificate above 10^11 (below, the two-run overlap
certifies every column). `data/*_grid_raw.csv` preserve the pre-repair
files from the disclosed corruption incidents. This machine's RAM threw
~1.5 single-page corruption events per hour under sustained 10-worker
load (all caught and repaired); run a hardware memory diagnostic before
further multi-hour runs.
