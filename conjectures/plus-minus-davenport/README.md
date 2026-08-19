# Plus-minus weighted Davenport constants (Marchan–Ordaz–Schmid, 2014)

For a finite abelian group `G`, `D±(G)` is the least `ℓ` such that every
sequence of `ℓ` elements of `G` has a nonempty subsequence summing to zero
after some choice of `±1` signs; equivalently `D±(G) − 1` is the maximum
size of a *dissociated* subset of `G` (all `2^k` subset sums distinct).
Marchan–Ordaz–Schmid (Int. J. Number Theory 2014, (secondary)) determined
`D±` for every group of order ≤ 100 **except one**: `C5⊕C15`, left as
"either 6 or 7". It looked tractable because the bottleneck is a bounded
exhaustive search nobody appeared to have run — the risk was rediscovery,
not compute, so the session budget went into openness-vetting and
six-way verification redundancy.

**Status:** active
**Sessions:** 2026-08-19
**Write-up page:** pending (see `PAGE.md`)

## Results

| Claim | Label | Where |
|---|---|---|
| `D±(C5⊕C15) = 6` — the last unknown value of order ≤ 100 decided: lower bound by explicit proved construction; upper bound by six independent exhaustive computations across three distinct methods (DFS census ×2 impls ×2 reductions, combination enumeration ×2 universes, F₅² class-injectivity reduction) | lower **PROVED**, upper **CERTIFIED** | NOTE §3 Thm 1, `certs/` |
| `D±(C7⊕C21) = 8` — first case of the next open family (`n = 3` for `C7⊕C7n`); upper bound from the distinct-subset-sums cap, lower from a verified explicit 7-set; **caveat**: possible overlap with the 2021 Perez-Lavin thesis (100–200 range, coverage unverifiable from this sandbox) | upper **PROVED**, lower **CERTIFIED** | NOTE §3 Thm 2 |
| Certified table of `dim±`/`D±` for 343 groups (rank ≤ 4, incl. all rank-2 of order ≤ 256): every value at floor ≤ dim± ≤ cap; rank-2 values always at an endpoint (only `C3⊕C3`, `C5⊕C15` stuck at floor); first strictly-intermediate value at rank 3 (`C3⊕C3⊕C15`); appending `C₂` can raise `dim±` by 2 | **CERTIFIED** | `data/table.csv`, NOTE §4 |
| Window bounds floor/cap (subset-sum cap for **all** `G`, not just odd order), forced families (all 2-groups; `C2⊕C2n`; …), cyclic values, `dim±(G⊕C₂) ≥ dim±(G)+1` | **PROVED** (partly folklore, flagged) | NOTE §2 |
| Lemma R: dissociativity in `C_p⊕C_3p` ⟺ class-injective subset sums in `F_p²`; explains why no counting argument decides `C5⊕C15` (class sizes 22/21/21 ≤ 25) | **PROVED** | NOTE §6 |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `dpm_search.c` (E1) | exhaustive DFS, sign-red + reduction-free modes, per-size census | ms–minutes/cell | every table value |
| `dpm_python.py` (E2) | independent Python DFS, exact node-count match required | ~50× E1 | cross-check log |
| `dpm_brute.py` (E3) | from-definition brute, tiny groups + selftest battery | seconds | controls |
| `enum_check.c` (E4) | combinations + `3^l` checks, no DFS | 0.4 s / 186 s | the size-6 double zero at 75 |
| `reduction_check.py` (E5) | Lemma R class-injectivity over `F_p²` | 25 min | seven-way infeasibility at 75 |
| `verify_witness.py` | from-definition witness checker + selftest | instant | witness verdicts |
| `witness_hunt.c` | randomized dissociated-set hunter (one-sided) | varies | controls; `C23⊕C23` attempt |
| `run_sweep.sh` + `cells.txt` | 339-cell sweep driver (resumable) | ~2 h wall / 3 workers | `data/sweep/` |
| `make_table.py` | consolidates sweep → table with exact floors/caps | seconds | `data/table.csv` |
| `cross_check.py` | E1-vs-E2 node-count comparison, all cells ≤ 100 | ~20 min | `data/cross_check.log` |

Reproduction (from inside this directory):

```bash
gcc -O2 -o dpm_search dpm_search.c && gcc -O2 -o enum_check enum_check.c
./dpm_search 5 15 --count-by-size     # Theorem 1 in 20 ms
./dpm_search 7 21                     # Theorem 2 in ~2 s
python3 verify_witness.py --selftest && python3 dpm_brute.py --selftest
./run_sweep.sh && python3 make_table.py && python3 cross_check.py
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/table.csv` | `make_table.py` | the master table (one row per isomorphism type) |
| `data/sweep/*.txt` | `run_sweep.sh` | raw per-cell outputs (value, node count, witness) |
| `data/cross_check.log` | `cross_check.py` | E1-vs-E2 exact node agreement, all cells ≤ 100 |
| `certs/e1_c5c15_*.txt`, `certs/e1_c7c21_*.txt` | E1 | headline censuses, both reductions, with per-size counts |
| `certs/e4_c5c15_l6_full.txt` | E4 | 0 dissociated 6-sets in 185,250,786 combinations |
| `certs/e5_c5c15_size6.txt` | E5 | all seven `(a,b)` splits infeasible |
| `certs/hunt_*.txt` | `witness_hunt` | seeded hunter transcripts (incl. negative results, which prove nothing) |

## Known defects and open threads

- **Every literature claim is (secondary)** — no primary source was readable
  from this sandbox (egress blocked; snippets only). Before any external
  use: read arXiv:1308.3316, the Perez-Lavin thesis (esp. its 100–200
  coverage — it may already contain `C7⊕C21`), and the Adhikari survey.
- Two open mathematical threads lead the list: a human proof of the `F₅²`
  infeasibility behind Theorem 1 (Lemma R makes it finite and structured),
  and the rank-2 endpoint dichotomy (Question 2 in NOTE §8).
- `C23⊕C23` (window {8,9}; motivated by an unverified "23, 46, 47" snippet)
  is undecided: the hunter has not found a 9-set; exhaustion needs
  ≈ 10¹¹–10¹² nodes.
- The sweep's deepest cells (`7⁷`-order 343 band) may carry TIMEOUT
  markers rather than values; the table lists them explicitly.

## Prior work

Marchan–Ordaz–Schmid, IJNT 10(5) 2014 1219–1239 (arXiv:1308.3316) —
the problem source (secondary). Perez-Lavin, PhD thesis, U. Kentucky 2021
(secondary). Adhikari, survey chapter, Springer PROMS 221, 2017
(secondary, unread). B±(G) monoid line: arXiv:2404.17258, 2506.14279,
Merito–Ordaz–Schmid 2025 (secondary). Dissociated sets: standard
harmonic-analysis notion; Lev, *On the size of dissociated bases* (EJC,
(secondary)). Full sourcing and the vetting trail: NOTE §7, WRITEUP, and
the daily log.
