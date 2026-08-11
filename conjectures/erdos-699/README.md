# Erdős Problem 699 — common prime factors of binomial coefficients

**Problem** (Erdős–Szekeres 1978; erdosproblems.com/699, open, status
"falsifiable"): for every 1 ≤ i < j ≤ ⌊n/2⌋, is there a prime **p ≥ i**
with p | gcd(C(n,i), C(n,j))?  **Strengthening**: outside a finite
exceptional set of triples (n,i,j), one can take **p > i**.  Statement
pinned from the Lean formalization (google-deepmind/formal-conjectures,
fetched 2026-08-11).  Sylvester–Schur is the single-coefficient analogue;
the i = 1 face and gcd > 1 are the proved Erdős–Szekeres common-divisor
theorem (#698, Bergman 2011).

**Prior art** (cited, pinned): uncertified Rust scan
`conglu1997/erdos_699_rust` (2026-01-03, on the problem's forum): weak
version to 10⁷ dense + families 2^k ≤ 2²⁷, 3^m+1 ≤ 3¹⁷+1; nine
strong-version failures recorded (`data/prior_art_scan.jsonl`, sha256
`e2f7b858…`).  This session extends the dense range 10× and adds the
certification layer, census certificates, and lemmas.

**Status:** active
**Sessions:** [2026-08-11](../../log/2026-08-11-erdos-699.md)
**Write-up page:** fabianarevalo.com/erdos-699 (pending first publish)

## Results (2026-08-11 session)

| Claim | Label | Where |
|---|---|---|
| Weak version (p ≥ i) holds for all 4 ≤ n ≤ 10⁸ — no counterexample; 10× the prior public bound, first dense search of (10⁷, 10⁸] | CERTIFIED | `data/summary.csv`, chunk outputs, controls below |
| The complete census of strong-version (p > i) exceptional triples on 4 ≤ n ≤ 10⁸ is exactly the nine known triples — none new; each with an independently re-verified certificate | CERTIFIED | `data/exceptions.csv`, `certs/EXC_*.txt` |
| Reduction scaffolding: hard rows i ≤ n − prevprime(n) (composite n), prime n and i = 1 trivial, candidates = primes > i in the falling window, all ≤ n/2; exceptions have i prime, unique witness p = i, i \| C(n,i) ⟺ n mod i² < i; n−1 prime ⟹ no exceptions at n (Mersenne-prime corollary for n = 2^k) | PROVED (elementary; L1/L5 surely implicit in ErSz78 — marked) | NOTE §2 |
| Family mechanisms: n = 3^m+1 (i = 3, j = n/2) — weak witness p = 3 always works, candidates divide 3^{2m}−1, lowest digits never carry; n = 2^k (i = 2) — candidates are the odd factors of 2^k−1; exceptional m ∈ {2,3,5,7,13}, k ∈ {4,9,11} in range | PROVED mechanism + CERTIFIED per-case decisions | NOTE §4 |
| j = n/2 rigidity (all i = 3 exceptions), p^a + p^b shape of every exceptional n, finiteness heuristics | Observation / NUMERICAL | NOTE §5 |

## The nine exceptional triples (4 ≤ n ≤ 10⁸)

(10,3,5), (16,2,6), (28,3,14), (28,5,14), (244,3,122), (512,2,147),
(2048,2,713), (2188,3,1094), (1594324,3,797162) — gcd factorizations in
`data/exceptions.csv`.  The last was found by the prior art and
rediscovered here unprompted (planted positive control).

## Scripts

| file | what it does | cost |
|---|---|---|
| `sweep.c` | production verifier; engines `bitset` / `interval` / `both` (row-level cross-check); SSVIOL + ENGDIFF tripwires | [4,10⁶] both: 52 s; [4,10⁸] on 4 cores: see `data/summary.csv` |
| `proto.py` | full-pair Python reference (no reduction) + bigint gcd third path | n ≤ 3000: ~15 s |
| `verify_exceptions.py` | independent per-triple re-verifier (Legendre valuations, all primes ≤ n); `--selftest` | seconds |
| `verify_row.py` | independent hard-row re-verifier (trial division + big-int masks); deterministic `--sample` | seconds/row |
| `oeis_controls.py` | A129488 / A263922 / A030979 anchors from pinned mirror `.seq` files | 5 s |
| `check_summaries.py` | chunk tiling, weakfail scan, record-prime-gap control (A005250/A002386), writes `data/summary.csv` | instant |
| `make_certs.py` | per-triple certificates + `data/exceptions.csv` | seconds |
| `compare_prior.py` | formal diff vs `data/prior_art_scan.jsonl` | instant |

## Reproduce

```bash
cd conjectures/erdos-699
gcc -O2 -march=native -o sweep sweep.c
python3 proto.py 3000 --census                 # reference census, ~15 s
./sweep 4 1000000 --engine=both                # dual-engine base range, ~1 min
python3 oeis_controls.py                       # OEIS anchors
python3 verify_exceptions.py --selftest
# full production run (4 cores, 3.2 core-hours engine time, ~75 min wall):
./sweep 4        1000000  --engine=both     > data/chunk_A.txt
./sweep 1000001  40000000 --engine=interval > data/chunk_B1.txt &
./sweep 40000001 65000000 --engine=interval > data/chunk_B2.txt &
./sweep 65000001 85000000 --engine=interval > data/chunk_B3.txt &
./sweep 85000001 100000000 --engine=interval > data/chunk_B4.txt &
wait
cat data/chunk_A.txt data/chunk_B*.txt > data/merged.txt
python3 check_summaries.py 100000000 data/chunk_A.txt data/chunk_B1.txt data/chunk_B2.txt data/chunk_B3.txt data/chunk_B4.txt
python3 make_certs.py data/merged.txt
grep ^EXC data/merged.txt | awk '{print $2, $3, $4}' > /tmp/exc.txt
python3 verify_exceptions.py /tmp/exc.txt
python3 compare_prior.py data/merged.txt
```

## Controls (all green on the production run)

- Dual engines row-by-row on [4, 10⁶] + spot slices at 5·10⁷ and 10⁸
  (`ENGDIFF` = 0), full-pair Python reference census equality on
  [4, 3000], bigint gcd third path on [4, 150].
- OEIS anchors: A129488 (105 terms), A263922 (87), A030979 (13, no
  extras) — machinery-level ground truth.
- Record-prime-gap control: max hard-row gap per chunk vs
  A005250/A002386.
- Sylvester–Schur nonempty-candidates assert on every hard row
  (`SSVIOL` = 0).
- Planted positive control: prior art's (1594324, 3, 797162) found
  independently.
- Every exception re-verified by the independent Legendre path
  (+ bigint gcd for n ≤ 3000); sampled rows re-verified by
  `verify_row.py` (LCG seed 20260811).

## Known defects / limitations

- The dense ranges (10⁶, 10⁸] outside the spot slices are single-engine
  (interval, with per-row bitset fallback); the dual-engine guarantee is
  stated precisely in NOTE §3 and the label does not overclaim.
- [ErSz78] itself was unreachable; everything attributed to it is
  (secondary).  The 1978 paper may contain small-range checks that would
  predate the prior art's 10⁷ — the priority statement here is about
  *public machine-checkable* artifacts.
- No per-row positive witnesses are stored (they would be ~10⁹ lines);
  negatives are certified by reproducibility + the layered controls, per
  this repository's standing convention for exhaustive negatives.
