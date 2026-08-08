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
`tools/satcert/rup_check` and a witness coloring at `f−1` checked by the
independent `verify_witness.py`; certificates in `certs/`, authoritative
list with runtimes and CNF hashes in `data/results.csv`.

| Claim | Label | Where |
|---|---|---|
| `f₂(2)=60, f₂(3)=40, f₂(4)=48, f₂(5)=80, f₂(6)=108, f₂(7)=…` (session in progress) | CERTIFIED | `certs/`, `data/results.csv` |
| `f₃(2)=3276`, `f₃(3)=585` — first 3-color values at this scale; the `(2^r−1)k^r` and `4^r/2` lower bounds are far from the truth (32 vs 3276, 189 vs 585) | CERTIFIED | `certs/` |
| Sharpness of `f₂(p^m) ≥ 3k²+1` **fails** at odd prime powers computed: `f₂(3)=40=3k²+13`, `f₂(5)=80=3k²+5` (k=7 in progress; an earlier `≥168` claim here was **struck** — it came from reading enumeration output mid-flight, see WRITEUP) | CERTIFIED | `certs/` |
| `f₂(4)=48=3·4²` — the `k=2^m` family (covered by neither of their theorems) attains `3k²` at `k=4`; `k=2` does not (`60 ≠ 12`) | CERTIFIED | `certs/` |

## Scripts

| file | what it does | cost |
|---|---|---|
| `enum.c` | canonical solution enumerator (exact 64/128-bit rational DFS), `--stripe=s/S` for parallel runs | ms–minutes; grows steeply in `k` |
| `enum2.c` | independent k=2 enumerator via the divisor parametrization `x=z+d₁, y=z+d₂, d₁d₂=z²` (SPF sieve); cross-checks `enum.c` and scales to `n=10⁶` in <1 s | seconds |
| `recip.py` | reference Python enumerator + encoder + certified single-instance driver | small cases |
| `sweep.py` | production driver: enumerate once, bracket with Cadical, certify boundary pair (Glucose DRUP → `rup_check`; witness → `verify_witness.py`), append `data/results.csv` | per value: seconds–minutes |
| `verify_witness.py` | independent witness checker (per-class restricted DFS; shares no code with the encoder) | instant |

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
