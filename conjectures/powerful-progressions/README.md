# Powerful progressions (van Doorn's consecutive-triples conjecture, 2026)

A powerful number has `p² | n` for every prime `p | n`. Van Doorn
(arXiv:2605.06697, May 2026) conjectured that infinitely many three-term
arithmetic progressions consist of three *consecutive* powerful numbers —
answering a question of Erdős in the negative — with the published evidence
being the complete list of 18 such triples below 10^14. The fault line for a
session: that census is a pure integer sweep whose cost grows like `√X`, so
four cores can push it five orders of magnitude and see whether the
conjecture's evidence base survives, sharpens, or breaks.

**Status:** active
**Sessions:** [2026-08-05](../../log/2026-08-05-powerful-progressions.md)
**Write-up page:** [fabianarevalo.com/powerful-progressions](https://fabianarevalo.com/powerful-progressions)

## Results

| Claim | Label | Where |
|---|---|---|
| Exactly 346 triples of consecutive powerful numbers in AP below 10^19 (152 below 10^18; 18 below 10^14, matching van Doorn) | CERTIFIED | NOTE §3 C1, `data/census_1e19.txt` |
| They form 16 primitive triples up to rational scaling; every chain is integer multiples of a gcd-1 root, e.g. (1728,1764,1800) = 36·(48,49,50) | CERTIFIED | NOTE §3 C2/C5, `data/analysis_1e19.txt` |
| Admissibility criterion for multipliers of a root (mandatory primes + valuation bound) | PROVED | NOTE §2, Lemma 1′ |
| Two squares in a consecutive triple force `d > √x`; hence ≤ 1 square whenever `d ≤ √x` | PROVED | NOTE §2, Lemma 2 |
| 15 of 16 primitives contain exactly one perfect square; P15 (4.15×10^17) contains none | CERTIFIED | NOTE §3 C3 |
| No 4-term AP of consecutive powerful numbers below 10^19 | CERTIFIED | NOTE §3 C4 |
| No chain saturated for long: P8 (272 of 346 triples) first loses multiplier m = 288; smallest failure is 2·(1728,1764,1800) broken by 3481 = 59² | CERTIFIED | NOTE §3 C5 |
| Primitive count 6 → 16 across 10^14 → 10^19 (supports, does not prove, the conjecture) | NUMERICAL | NOTE §5 |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `census.cpp` | monolithic census: enumerate powerful ≤ X as a²b³, sort, scan for AP3/AP4 | 77 s / 5.6 GB at 10^17 | triple list, counts |
| `census_seg.cpp` | segmented census, O(segment) memory, boundary-carry logic | 3m29s at 10^18, 7m52s at 10^19 | same, at any X < 2^64 |
| `analyze.py` | chain decomposition, gcd-1 roots, Lemma-1′ saturation scan, per-decade table | 1.2 s | `data/analysis_1e19.txt` |
| `verify_triples.py` | independent per-triple verifier (different powerfulness algorithm; consecutiveness re-derived per window) | 1m51s | 346/346 PASS |

```bash
cd conjectures/powerful-progressions
g++ -O2 -o census_seg census_seg.cpp && ./census_seg 1e19 2e16 > data/census_1e19.txt
python3 verify_triples.py data/census_1e19.txt
python3 analyze.py data/census_1e19.txt
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/census_1e18.txt` | `census_seg 1e18 2e16` | all 152 triples below 10^18 + totals |
| `data/census_1e19.txt` | `census_seg 1e19 2e16` | all 346 triples below 10^19 + totals |
| `data/analysis_1e18.txt`, `data/analysis_1e19.txt` | `analyze.py` | chains, roots, saturation, decade table |
| `data/verify_1e18.txt`, `data/verify_1e19.txt` | `verify_triples.py` | independent verification transcripts |

## Known defects and open threads

- Counts of powerful numbers were externally confirmed only at 10^10–10^12
  (OEIS A118896 via search summaries) and against van Doorn's 18 at 10^14 —
  all (secondary): **no primary source was readable from this sandbox**.
- Relationship of the 16 primitives to van Doorn's family "A₁": unknown (his
  definition is in the blocked PDF). Do not claim novelty for any specific
  triple beyond "not derivable from the published 18 by scaling" until the
  paper is read.
- Sharpest open thread: prove infinitude for a single chain (needs a density
  argument for consecutiveness along admissible multipliers — Result C5 shows
  it fails infinitely often naively), or find the second squareless primitive.

## Prior work

Van Doorn arXiv:2605.06697 (the conjecture and the 18-triple table); Chan,
INTEGERS 25 #A7 (2025) and JIS 26 (2023) on powerful APs; Erdős–Mollin–Walsh
(three consecutive *integers*, open, erdosproblems #366); OEIS A001694,
A118896, A060355. All (secondary) today — see NOTE §8.
