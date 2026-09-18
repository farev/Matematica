# Leech's tree-labelling problem (Leech 1975; OEIS A007187; Guy UPINT §C10)

For a tree on n vertices with positive integer edge weights, count the path
sums between pairs of vertices. Leech asked for the largest k = a(n) such that
some tree realises every integer 1, 2, …, k. This is the covering relative of
the perfect *Leech tree* problem (all C(n,2) sums distinct and equal to
1..C(n,2)), whose nonexistence results run through Taylor 1977 and Ghodsi
2026; the covering values were known only for n ≤ 10 (1, 3, 6, 9, 15, 20, 26,
34, 41), with "a(11) ≥ 48, a(12) ≥ 55" unattributed in OEIS. The fault line:
a covering tree wastes only C(n,2) − k pairs, so the forced-least-missing-weight
recursion of the Leech-tree literature applies with a budget attached.

Page: [PENDING: fabianarevalo.com/leech-tree-labelling] · Write-up pipeline: `PAGE.md`.

**Status:** active
**Sessions:** 2026-09-18

## Results

| Claim | Label | Where |
|---|---|---|
| a(2..10) = 1, 3, 6, 9, 15, 20, 26, 34, 41 re-derived from scratch: witnesses checked by `code/check_cover.py`, refutations of k = a(n)+1 exhaustive (node counts in NOTE §3) | CERTIFIED (positive control, matches OEIS) | NOTE §3, `witnesses/` |
| **a(11) = 49** (OEIS had a(11) ≥ 48): witness tree (0,1,1) (2,3,1) (0,4,2) (5,6,4) (3,6,5) (5,7,7) (6,8,8) (5,9,11) (2,10,22) (0,3,24) checked by `check_cover.py`; no tree on 11 vertices covers 1..50, exhaustive search of 1 400 728 816 nodes on four workers (≈ 5 min), plus the ladder k = 55..51 | CERTIFIED (single-engine refutation, see defects) | NOTE §4, `witnesses/n11_k49.txt`, `runs/run7_n11_k50_w*.txt` |
| Lemmas 1–6 (weight window, monotone excess, budgeted parity, edge load, budgeted block bounds after Ghodsi Thm 4.1, symmetry) | PROVED | NOTE §2 |
| **a(12) ≥ 57** (OEIS had ≥ 55): witness (0,1,1) (0,2,1) (1,3,1) (2,4,4) (5,6,6) (7,8,8) (2,7,9) (5,9,14) (7,5,15) (6,10,16) (5,11,29), checked; upper bound [PENDING] | CERTIFIED | NOTE §5, `witnesses/n12_k57.txt` |
| **Distinct-sum variant** (maximum Leech index of Varghese–Lakshmanan–Arumugam over trees of order n): **1, 3, 6, 9, 15, 20, 25, 30, 37, 45, 47** for n = 2..12, witnesses checked with `--distinct`, every larger k refuted; not in OEIS | CERTIFIED (two engines for n ≤ 11 [PENDING: 12]; brute force for n ≤ 7) | NOTE §6, `witnesses/distinct_*`, `runs/run8_*` |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `code/cover_search.c` | exhaustive budgeted search: `./cover_search n k [split_depth worker nworkers]`; prints `WITNESS` or `RESULT … found=0` with node counts | n = 10: seconds; n = 11, k = 50: ~2 G nodes; see `runs/` | the a(n) ladder and the n = 11 refutations |
| `code/check_cover.py` | independent witness checker (no shared code): `python3 check_cover.py n k "(u,v,w) …"` | instant | `OK`/`FAIL` |
| `code/satcover.py`, `code/trees.py` | independent SAT engine, one CNF per tree shape (CaDiCaL via python-sat); optional DRUP proofs | n = 8: 2 min; n = 9: 1–3 min per shape | replication of a(7), a(8) (all shapes) and 17 of the 47 shapes at n = 9, k = 35 (all UNSAT; stopped for CPU) |
| `code/plain_search.c` | minimal second engine (weight window, budget, repeat pruning only; no block bounds, parity or canonical forms): `./plain_search n k [-d]` | n = 11 distinct: seconds; n = 10, k = 42: [PENDING] | independent re-derivation of the ladders |
| `code/brute_small.c` (+ `code/shapes.h`) | brute force over every tree shape and every weight vector within the edge-weight bound, both modes, n ≤ 7 | 3 min | a(2..7) = 1, 3, 6, 9, 15, 20 in both modes |
| `code/proto_search.py` | the 40-line Python prototype of the recursion (first cross-check, n ≤ 9) | 5 min | a(2..9) |

Run from inside this directory:

```bash
cd conjectures/leech-tree-labelling
gcc -O2 -march=native -o cover_search code/cover_search.c
for n in 5 6 7 8 9 10; do ./cover_search $n $((n*(n-1)/2 - 3)); done   # examples
./cover_search 11 51 5 0 2 & ./cover_search 11 51 5 1 2 & wait          # two workers
./cover_search 11 46 -d                                                  # distinct-sum variant
python3 code/check_cover.py 11 48 "$(cat witnesses/n11_k48.txt)"
python3 code/satcover.py 8 27       # all 23 shapes UNSAT
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `witnesses/nN_kK.txt` | `cover_search` (checked by `check_cover.py`) | a weighted tree on N vertices covering 1..K |
| `runs/run7_n11_k*.txt` | `cover_search` | verbatim `RESULT` lines: n, k, budget, worker/split, node counts, seconds |

## Known defects and open threads

- The n = 11 refutations are single-engine (one C program; two variants of it
  agree to the node, the SAT engine replicates only n ≤ 9). An independently
  written second engine at n = 11 is the first thing to add.
- a(12) is open: 57 ≤ a(12) ≤ [PENDING]. Refuting k = 58 (excess budget 8) is projected at ~10¹¹ nodes.
- The distinct-sum value at n = 12 (47) is single-engine until the minimal engine's run finishes [PENDING].
- Leech 1975 and Guy §C10 unread (paywalled/unavailable): cited (secondary).

## Prior work

- J. Leech, *Another tree labelling problem*, Amer. Math. Monthly 82 (1975):
  the problem and a(2..10) (secondary, via OEIS A007187).
- H. Taylor (1977): Leech-tree orders are m² or m² + 2 (secondary, via Ghodsi).
- Székely–Wang–Zhang 2005, Calhoun–Ferland–Lister–Polhill 2007,
  Varghese–Lakshmanan–Arumugam 2020: nonexistence of Leech trees at orders
  9, 11, 16 and structural results (secondary, via Ghodsi).
- M. Ghodsi, arXiv:2609.20492 (17 Sep 2026): no Leech tree of order 18; the
  whole-block exact-cover condition (Theorem 4.1) that Lemma 5 here budgets.
  Read in full.
- Nothing found on the covering problem beyond n = 10.
