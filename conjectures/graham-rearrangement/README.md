# Graham's rearrangement conjecture (Erdős #475)

**Statement.** For a prime p, every subset A ⊆ F_p ∖ {0} has an ordering
whose partial sums are pairwise distinct mod p.
[erdosproblems.com/475](https://www.erdosproblems.com/475) · status there:
DECIDABLE (proved for all sufficiently large p by four ineffective results;
open prime by prime below that).

**Status here.** Session 1 (2026-08-30), claims labelled:

- **CERTIFIED** — holds for *every* subset of F_p ∖ {0}, every size, for
  **every prime p ≤ 37**: 1,954,471,973 dilation orbits decided
  (= 70,066,181,009 subsets), a witness ordering for every orbit, zero
  failures; orbit counts match an independent Burnside computation exactly
  on all 173 (p,t) cells. Previous published record: uncertified random
  search through cyclic order 25 (ADMS 2016). Smallest undecided prime is
  now **41**.
- **CERTIFIED** — the zero-sum size-(p−3) layer (sets Z_p ∖ {0,x,−x};
  one dilation orbit per prime; unreachable by the HOS19 construction and
  inconsistently treated in print — see NOTE §5) holds for every prime
  **7 ≤ p ≤ 61**.
- **PROVED** (elementary lemmas): dilation-invariance of admissibility;
  single-orbit structure of the zero-sum p−3 layer.

Full statements, quotes from the primary sources, and open questions:
[NOTE.md](NOTE.md). Session narrative including all failed approaches:
[WRITEUP.md](WRITEUP.md).

## Scripts

| script | what it does | cost |
|---|---|---|
| `verify_grc.c` | orbit-level exhaustive verifier. `verify_grc p tmin tmax nthreads seed [witfile] [wsample]` sweeps all sizes; `-s a1,a2,…` decides one set (`-z` forbids 0-sums — negative control; `-l` returns the lex-min witness by complete DFS) | p=29: 13 s · p=31: 58 s · p=37: ~2.5 h (4 threads) |
| `burnside.py` | independent exact orbit counts per (p,t) | instant |
| `summarize.py` | per-prime summary table; re-asserts Burnside on every cell | instant |
| `check_witnesses.py` | clean-room verifier: `selftest`, `hard <files>` (re-check every committed witness + canonicality), `sample p tmin tmax N seed` (independent re-decision of random orbits) | selftest instant; samples minutes |

## Reproduction

```bash
cd conjectures/graham-rearrangement
gcc -O3 -march=native -o verify_grc verify_grc.c -lpthread
./verify_grc 29 2 28 4 12345 /tmp/wit_p29.txt 1000   # 13 s, compare data/results_p29.txt
python3 summarize.py                                  # Burnside check, all cells
python3 check_witnesses.py selftest
python3 check_witnesses.py hard data/witness_sample_p29.txt
python3 check_witnesses.py sample 29 13 26 60 777
```

All engine decisions are deterministic given the seed (12345 for every
committed run; sampler seed 777). Witness files log every 1000th orbit
(100000th at p = 37) plus every set that needed tier ≥ 3.

## Data

| file | contents |
|---|---|
| `data/results_p*.txt` | per-layer counts, hardness tiers, max DFS nodes, wall times |
| `data/witness_sample_p*.txt` | ~47k sampled witness orderings (independently re-verified) |
| `data/grayzone_witnesses.txt` | zero-sum p−3 witnesses, 7 ≤ p ≤ 61 |
| `data/lexmin_pminus3.txt` | lexicographically minimal witnesses for the same layer, p ≤ 31 |

## Known defects

- Sets that are logged both by sampling (rank ≡ 0 mod wsample) and as
  tier-3 hard appear twice in the witness files (harmless; the verifier
  handles duplicates).
- `check_witnesses.py sample` is pure Python and slow on dense layers;
  keep N modest.
