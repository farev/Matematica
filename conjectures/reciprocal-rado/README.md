# Reciprocal Rado numbers (sharpness of the Gaiser–Ramezanpour bounds)

The reciprocal Rado number `f_r(k)` is the least `n` such that every
`r`-coloring of `{1,…,n}` has a monochromatic solution of

```
1/x₁ + 1/x₂ + ⋯ + 1/x_k  =  1/x_{k+1}
```

with the `x_i` not necessarily distinct (all positive terms force
`x_{k+1} < x_i` for every `i`). Introduced by Gaiser (Discrete Math. 347
(2024) 114156, arXiv:2306.04029, `f₂(k) = O(k³)`); Gaiser–Ramezanpour
(arXiv:2607.04373, July 2026) prove `f₂(3·2^m) = 3k²` for `m ≥ 1`, prove
`f₂(p^m) ≥ 3k² + 1` for odd prime powers **with no matching upper bound**,
prove `f_r(2) ≥ 4^r/2` and `f_r(k) ≥ (2^r−1)k^r`, and report computational
values in a table this sandbox could not read (all four literature sites
egress-blocked; every citation here is from abstract-level snippets and is
**(secondary)** except where a theorem was reproduced computationally).

The fault line for a session: the SAT instances are tiny even where the
numbers are four digits, nobody in this family ships certificates, and the
sharpness question at odd prime powers was open as of the July paper.

**Status:** active
**Sessions:** [2026-08-08](../../log/2026-08-08-reciprocal-rado.md)

## Results (2026-08-08 session)

Every value carries a DRUP proof of UNSAT at `f` checked by
`tools/satcert/rup_check` and a witness coloring at `f−1` verified by two
independent checkers (`verify_witness.py` and `check_class.c`);
certificates in `certs/`, append-only run log in `data/results.csv`,
authoritative table in `data/values.csv` (built by `make_table.py`).

| Claim | Label | Where |
|---|---|---|
| `f₂(2)=60, f₂(3)=40, f₂(4)=48, f₂(5)=80, f₂(6)=108, f₂(7)=150, f₂(8)=192` | CERTIFIED | `certs/`, `data/values.csv` |
| Sharpness of the odd-prime-power bound `f₂(p^m) ≥ 3k²+1` **fails at every computed case, with shrinking excess**: Δ = f₂(k)−3k² = **13, 5, 3** at k = 3, 5, 7 (an earlier "f₂(7) ≥ 168" here was **struck** — mid-flight enumeration read, see WRITEUP; the certified value is 150) | CERTIFIED | `certs/` |
| `f₃(2)=3276`, `f₃(3)=585` — first multi-color values of the family; the `4^r/2` and `(2^r−1)k^r` bounds are off by 102× and 3× | CERTIFIED | `certs/` |
| `f₄(2) > 60000` (4-coloring of [1,60000], independently verified); n=150000 instance undecided at close | CERTIFIED (bound) | `certs/f4_2_n60000.witness` |
| **Conjecture B**: `f₂(k)=3k²` for all even `k ≥ 4` (even-k half-diagonal mechanism, NOTE §4) — **f₂(8)=192=3k² was predicted before the run and confirmed**; the `k=2^m` family splits: 4 and 8 attain `3k²`, k=2 sits at `5·3k²` | CERTIFIED + conjecture | `certs/`, NOTE |
| Extremal structure: odd-k two-colorings are an interval core `{1,2} ∪ [3,3k−1]-swaps ∪ [3k, …]` plus sparse high corrections; the `f₃(2)` extremal satisfies `χ(z) ≠ χ(2z)` at **all** 1637 applicable pairs | CERTIFIED (by inspection of verified witnesses) | NOTE §6 |

## Scripts

| file | what it does | cost |
|---|---|---|
| `enum.c` | full solution enumerator (exact 64/128-bit rational DFS), `--stripe=s/S` | fast to k=6; wall at k=8 |
| `enumw.c` | weighted enumerator: all solutions with ≤ dmax distinct values (partitions × orderings); CEGAR's seed/pool source | seconds |
| `enum2.c` | independent k=2 enumerator via the divisor parametrization `d₁d₂=z²` (SPF sieve); `n=10⁶` in <1 s | seconds |
| `recip.py` | reference Python enumerator + encoder + certified single-instance driver | small cases |
| `sweep.py` | full-enumeration driver: enumerate once, bracket with Cadical, certify boundary pair, append `data/results.csv` | per value: seconds–minutes |
| `cegar.py` | large-k driver: verified-clause subsets grown by counterexamples (UNSAT sound by construction; SAT gated by the full checker); `--certify-at=F` re-certifies a known boundary | per value: minutes |
| `check_class.c` | independent C witness checker, 128-bit exact; `--all` batch mode, `--dmax=D` staged partial mode (partial results are labelled PARTIAL, never "OK") | seconds–minutes |
| `verify_witness.py` | independent Python witness checker (the original gate; cross-validates `check_class`) | fast to k≈6 |
| `make_table.py` | aggregates `data/results.csv` (append-only run log) into `data/values.csv` (authoritative table); aborts on any value conflict | instant |

Reproduce (from inside this directory; build tools first):

```bash
gcc -O2 -o enum enum.c && gcc -O2 -o enum2 enum2.c
gcc -O2 -o ../../tools/satcert/rup_check ../../tools/satcert/rup_check.c
python3 sweep.py 5 2 120 --start=75     # f2(5) = 80, certified
python3 sweep.py 3 3 900 --start=189    # f3(3) = 585, certified
```

`GLUCOSE_BIN` must point at a standalone Glucose 4.2.1 (`-certified`
streams DRUP to disk); built here from the python-sat sdist's bundled
pristine source (see the session log for provenance).

## Controls

- Enumerator vs OEIS A002966 (partitions of 1 into k unit fractions):
  1, 3, 14, 147 reproduced at k=2..5.
- C DFS ≡ Python DFS ≡ brute force on a (k,n) grid; C DFS ≡ divisor
  method at n = 60, 500, 3276 for k=2.
- Gaiser–Ramezanpour theorem anchors reproduced: `f₂(6) = 108 = 3·6²`
  exactly (their `3·2^m` theorem, m=1), SAT witnesses found at `3k²` for
  k = 3, 5, 7 as their odd-prime-power bound requires.
- Every UNSAT is DRUP-checked; every witness re-verified independently.

## Known defects and open threads

- The Gaiser–Ramezanpour computational table (in the blocked PDF) could
  not be compared against; small-`k` values here may reproduce entries of
  that table. All certificates are new regardless (they report none).
- No OEIS sequence for `f_r(k)` was findable by search (absence-of-
  evidence, (secondary)); `60, 3276` (the `f_r(2)` column; the trivial
  `f₁(2) = 2` via `1/2+1/2 = 1/1`) matches nothing indexed. Candidate
  OEIS submission after the paper PDF becomes readable.
