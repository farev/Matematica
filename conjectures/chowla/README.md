# chowla: two-point correlations of the Liouville function

**Statement.** Chowla's conjecture (two-point case): for every h ≥ 1,
S_h(x) = Σ_{n≤x} λ(n)λ(n+h) = o(x). Open for every h; the model instance
of the parity barrier. Write-up: <https://fabianarevalo.com/chowla>.

**Status.** Open (of course).

**Session 2 (2026-08-01) — clean-room audit and coverage extension.** The
sandbox had gcc and no network, no NumPy and no way to install it, so none of
the scripts below could run there; the coverage pipeline was rewritten from
scratch in C (`lambda_coverage.c`) with a stdlib-only Python verifier. All
thirty previously certified coverage values (N_k and last-completing pattern
code, k = 1..30) **reproduce exactly** from the independent implementation, as
do L(10^j), j = 1..8 (CERTIFIED). Coverage then extended: every ±1 sign
pattern of length ≤ 33 occurs in λ: N_31 = 43,901,697,682,
N_32 = 99,494,377,311, N_33 = 196,202,853,829 (CERTIFIED by exhibition; each
completing window re-verified by pure-Python trial division, along with 10, 12
and 12 further endgame windows). New instrument: the *first-occurrence
spectrum* scores all 2^k patterns against Conway's exact waiting time A(w)
rather than reporting only the maximum; at k = 24 λ's mean R = 1.000123 against 32 i.i.d. fair-coin
controls at 0.999953 ± 0.000319, i.e. **+0.53 control-σ**, with the
popcount slope accounted for by λ's own one-point bias (residual −0.56σ)
(NUMERICAL). See NOTE §11, WRITEUP session 2.

**Session 1 (2026-07-29).** Exact descent/duality lemmas
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

Session-2 tooling — C and Python-stdlib only, no NumPy, runs on a bare machine:

| script | what it produces |
|---|---|
| `lambda_coverage.c` | exact segmented λ sieve + first-occurrence census; `--prng` control stream, `--firstocc` full spectrum, `--lcheck` L(10^j) |
| `verify_coverage.py` | independent trial-division verifier: `small` (N_k from scratch), `window`, `check`, `endgame` |
| `firstocc_stats.c` | Conway-normalised statistics R(w) of a first-occurrence spectrum |
| `firstocc_analysis.py` | λ vs the control ensemble: mean R, popcount slope, overlap classes |
| `coverage_model.py` | coupon-collector comparison for N_k, with the self-overlap correction bounded |

Reproduce (from this directory):

```bash
python3 test_liouville.py
python3 census_run.py 1e9 5e5 1 data/fineA --coverage 24
python3 certify.py data/fineA_grid.csv
python3 analyze.py data/fineA_grid.csv
```

Main run (6.5 h on an M3 Pro; grid valid at any prefix):
`python3 census_run.py 1e12 2e7 10 data/mainB12`.

Session-2 reproduction (needs only gcc and Python 3, no NumPy):

```bash
cc -O2 -fopenmp -march=native -o lambda_coverage lambda_coverage.c
cc -O2 -o firstocc_stats firstocc_stats.c -lm

python3 verify_coverage.py small 200000              # N_k, k<=14, trial division
./lambda_coverage 2.4e10 25,26,27,28,29,30 /tmp/v --threads 4 --report 2e9
                                                     # 8 min, reproduces k=25..30
./lambda_coverage 2.4e11 31,32,33 /tmp/m --threads 4 --endgame 256
                                                     # the long run; see below
python3 verify_coverage.py window 33 196202853829 3712643644
python3 verify_coverage.py endgame data/endgame_3133.txt 12
python3 coverage_model.py
```

Long-run cost, this session's machine (4 cores, 15 GB, no other load): the
k = 31,32,33 run reached N_31 at 1718 s, N_32 at 3774 s and N_33 at 7387 s
(total 7387 s wall: sieve 1701 s, bitmap probes 5677 s); steady state is about
390 s per 10^10 values of n. Peak RSS ≈ 2.5 GB (bitmaps 256 MB + 512 MB + 1 GB).

Data: `data/*_grid.csv` (certified integer columns + float64 harmonic
columns; committed as .gz, all < 7 MB), `data/*_coverage*.csv`,
`data/*_meta.json` (runtimes/machine). Session 2: `data/coverage_3133.csv`
(N_31..N_33), `data/endgame_3133.txt` (the last 256 completions per k, each an
independently checkable exhibition), `data/coverage_3133.log`,
`data/repro_k25_30.csv`, `data/firstocc_k24_*`. `data/fineA_firstocc.npz` (exact
first-occurrence index of every sign pattern, k ≤ 24; 135 MB) exceeds the
repo's ~10 MB limit → destined for Zenodo, kept locally meanwhile. Documents: NOTE.md (paper-shaped), WRITEUP.md (lab
notebook), PREDICTIONS.md / VERDICTS.md (out-of-sample protocol).

**Known defects.** *Reproducibility:* every script from session 1 imports
NumPy, and on a clean machine without it (as here) none of the certified
results can be rerun at all. Only the coverage results now have a
dependency-free path; the census, quad and covariance-web results do not.
*Coverage minimality:* N_k is CERTIFIED by exhibition — the completing window
is exhibited and independently re-verified — but "no earlier occurrence" has no
compact witness and rests on the exhaustive scan, exactly as in session 1.
The `--endgame` certificate log is line-buffered only as of this session; runs
made before that lose the endgame lines still in the stdio buffer if killed.
Harmonic columns are float64 with a rigorous < 10^-8
rounding bound, not exact rationals. Columns S_h for odd h ≥ 9 carry no
independent per-row certificate above 10^11 (below, the two-run overlap
certifies every column). `data/*_grid_raw.csv` preserve the pre-repair
files from the disclosed corruption incidents. This machine's RAM threw
~1.5 single-page corruption events per hour under sustained 10-worker
load (all caught and repaired); run a hardware memory diagnostic before
further multi-hour runs.
