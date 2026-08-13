# Erdős distinct subset sums — the tenth value (Erdős 1931; Conway–Guy 1967)

A set of positive integers has *distinct subset sums* (DSS) if all `2^n` of
its subset sums differ. Erdős asked ("perhaps my first serious problem", $500)
whether the largest element of an n-element DSS set must be `≥ c·2^n`. The
data frontier of the problem is the function `f(n)` = least possible largest
element (OEIS A276661): known exactly only for `n ≤ 9` — Lunnon (1988)
exhaustively for `n ≤ 8`, J. P. Grossman for `n = 9`. `f(10)` is open;
the Conway–Guy construction gives `f(10) ≤ 309`, conjectured sharp; before
this session OEIS recorded only `f(10) > 220`. The fault line for a session:
`f(10)` is a pure finite computation, parallelizable, with graceful
certified milestones (`f(10) > m` for every exhausted maximum `m`).

**Status:** active
**Sessions:** 2026-08-13

## Results

| Claim | Label | Where |
|---|---|---|
| Ladder re-derived from scratch: `f(n)` = 1, 2, 4, 7, 13, 24, 44, 84, 161 for `n = 1..9`, agreeing with A276661; all optimal sets enumerated per level | CERTIFIED | `data/ladder_sweep.csv`, `data/optimal_sets.txt` |
| `f(10) > B` (see NOTE for the final frontier `B` of this session; supersedes the recorded 220): no 10-element DSS set has largest element `≤ B` | CERTIFIED | `data/n10_sweep.csv` |
| `f(10) ≤ 309`: the Conway–Guy 10-set `{148,225,265,285,296,302,305,307,308,309}` is DSS (validated by brute enumeration) | CERTIFIED | `validate_set.py` controls |
| No 10-element DSS set with max `≤ 308` exists whose deficiency profile lies within L1-distance 8 of the Conway–Guy profile (19,125,539 sets checked) | CERTIFIED | `cg_neighborhood.py` output, `data/` |
| `f(10) ≥ 192` by the second-moment (Erdős–Moser) bound, exact finite form | PROVED (classical method) | NOTE §3 |
| Simulated annealing cannot even rediscover a DSS 10-set at cap 309 (energy stalls at 3–5): witness-side heuristics uninformative | NUMERICAL (negative) | `anneal_witness.py`, WRITEUP |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `dss_search.c` | branch-and-bound engine, bitset-of-sums state (v2) | `n=9, m=155`: 146 s / 4 threads | RESULT lines with exact node counts |
| `dss_search_basic.c` | v2 before micro-optimization, kept as an independent build of the same tree | slower | identical node counts |
| `dss_search3.c` | difference-set engine (v3): O(1) candidate tests via incremental D and mirror R; `--tight` = exact caps over the true candidate pool | `n=9, m=150`: 30 s / 4 threads | identical statuses; node counts identical in default mode |
| `dss_reference.py` | independent Python reference of the identical tree | n ≤ 7 sweeps in minutes | node counts must match C exactly |
| `validate_set.py` | zero-cleverness brute validator + control suite | instant | `CONTROLS ALL OK` |
| `ladder.py` | re-derives `f(2)..f(9)` from scratch, cross-checks everything | ~1 h / 4 cores | `data/ladder_sweep.csv` |
| `sweep10.py` | the `a(10)` sweep, resumable, per-`m` certified rows | ~40× cost per +20 in `m` | `data/n10_sweep.csv` |
| `cg_neighborhood.py` | exhaustive near-Conway-Guy witness exclusion | K=8: 28 s | zero hits below 309 |
| `anneal_witness.py` | heuristic witness search (failed control; kept as documented negative) | seconds | see WRITEUP |

Build the engines and run everything from inside this directory:

```bash
gcc -O3 -march=native -fopenmp -o dss_search dss_search.c
gcc -O3 -march=native -fopenmp -o dss_search_basic dss_search_basic.c
gcc -O3 -march=native -fopenmp -o dss_search3 dss_search3.c
python3 validate_set.py          # control suite
python3 ladder.py                # f(2)..f(9) re-derivation
python3 sweep10.py               # resumes the a(10) sweep from data/n10_sweep.csv
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/ladder_sweep.csv` | `ladder.py` | per-(n, m) status + exact node counts, n = 2..9 |
| `data/optimal_sets.txt` | `ladder.py` | ALL optimal DSS sets at each `f(n)`, n = 2..9 |
| `data/n10_sweep.csv` | `sweep10.py` | per-m certified NONE rows for n = 10 — each row is `f(10) > m` |
| `data/ladder_run.log` | `ladder.py` | full run transcript |

## Known defects and open threads

- The `a(10)` decision is NOT finished: the sweep's cost grows ~40× per +20
  in `m`; full exhaustion to 308 is months on 4 cores with this engine.
  The certified frontier advances with every resumed session
  (`sweep10.py` is resume-safe; every completed `m` is a permanent result).
- Sharpest algorithmic thread: a multi-`m` engine over deficiency vectors
  `d` (elements `m − d_i`), where equal-cardinality collisions are
  m-independent and unequal-cardinality collisions exclude single values of
  `m` — one shared tree instead of ~150 per-`m` trees (~5–10× projected;
  sketch in NOTE §6).
- Engine node counts at `n = 9` are cross-verified between v2 and v3 at
  `m ∈ {150, 155}` and by the full v2 ladder; the Python reference verifies
  n ≤ 7 exhaustively. No independent check of v3-tight beyond status
  agreement (by design: tight mode changes the tree).
- The annealer's failed positive control means the witness side below 309
  has NO effective heuristic probe here beyond the CG neighborhood slice.

## Prior work

- Erdős's problem: erdosproblems.com/1 *(secondary — all sources in this
  directory were verified only through search-snippet quotes on 2026-08-13;
  the sandbox could not fetch any primary page — see the session log)*.
- Conway–Guy 1967 construction; Bohman 1996 proved all Conway–Guy sets are
  DSS; upper bound `0.22002·2^n` (Bohman). *(secondary)*
- Lunnon 1988: exhaustive `f(n)` for `n ≤ 8`; Grossman: `f(9) = 161`
  (OEIS A276661; his optimal set is the Conway–Guy 9-set). *(secondary)*
- Lower bound `Σ a_i² ≥ (4^n−1)/3` is the Erdős–Moser second-moment method;
  the asymptotic record constant `√(2/π)` is Elkies–Gleason (unpublished),
  matched by Dubroff–Fox–Xu 2021 and Steinerberger 2023 with new proofs.
  *(secondary)*
- Active adjacent line: Costa–Dalai–Della Fiore (DAM 2023), Costa–Della
  Fiore (DAM 2025) on variants; a modular variant paper 2023. *(secondary)*
