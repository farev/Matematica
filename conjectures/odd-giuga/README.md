# Odd Giuga numbers (Giuga 1950 / Borwein–Borwein–Borwein–Girgensohn 1996)

A **Giuga number** is a composite `n` with `p | (n/p − 1)` for every prime
`p | n` (equivalently: squarefree with `Σ_{p|n} 1/p − 1/n ∈ ℕ`); a
**primary pseudoperfect number** (PPN) is an `n > 1` with
`1/n + Σ_{p|n} 1/p = 1`. All known members of both families are even;
whether odd ones exist is open, and any counterexample to Giuga's 1950
primality conjecture is an odd Giuga number. The recorded bound — an odd
Giuga number has **at least 14 prime factors** — dates to 1996 (secondary:
BBBG, Amer. Math. Monthly 103), was computed in Maple, and its companion
code was never published. The bottleneck is exact CPU work, so it looked
like a fault line a certified 4-core branch-and-bound could move.

**Status:** active
**Sessions:** 2026-08-23
**Write-up page:** none yet

## Results (labels per repo convention)

| # | Result | Label |
|---|---|---|
| 1 | Every odd Giuga number has at least **FINAL_G** prime factors (recorded bound: 14, secondary) — exhaustion of `Σ 1/p_i − 1/n = 1` over sets of `m ≤ MG` distinct odd primes, all empty, + parity (Lemma 5) | **CERTIFIED** (runs) + **PROVED** (lemmas) |
| 2 | Every odd primary pseudoperfect number — equivalently every all-prime (possibly improper) Znám solution in odd primes — has at least **FINAL_P** prime factors; first explicit odd bound beyond the `≤ 8` consequence of Butske–Jaje–Mayernik's census (secondary) | **CERTIFIED** + **PROVED** |
| 3 | Positive controls: the engine reproduces, from scratch, exactly the published censuses — all 10 Giuga numbers with ≤ 8 prime factors and all 8 PPNs with ≤ 8 prime factors (OEIS A007850 / A054377, secondary) — the first reproduction with open code and committed run records | **CERTIFIED** |
| 4 | Lemma layer: classification of both families as the two signs of `Σ 1/p_i + ε/n = 1`; **an odd solution has an even number of prime factors** (possibly folklore); only the integer class `T = 1` exists below 1412 odd factors; engine-soundness lemmas (windows, closure, one-sided primality, wheel filter) | **PROVED** |
| 5 | The classical constants reproduced exactly by independent computation: `≥ 9` factors for an odd Giuga number, `≥ 59` factors for `sum − prod ≥ 2` | **PROVED** (exact sums) |

`FINAL_G`, `FINAL_P`, `MG` filled at close of session from `results/`.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `search.py` | exact BnB over prime sets solving `Σ 1/p_i + ε/n = 1`; gmpy2 integers, C kernel (`kernel.c`) for the two-primes-left scan, per-unit resume, JSONL run records | controls: seconds; odd m=12: 1.5 min; odd m=14: hours | the exhaustions |
| `kernel.c` | u128 scan of the closure window: keeps `q` with `(Dq−P) \| P²+εD`; wheel filter over primes ≤ 61 | — | — |
| `engine2.py` | clean-room cross-check: stdlib Fractions + sympy, independently derived (looser) windows, no kernel, no divisor route | odd m ≤ 11: 2 s; even m ≤ 6: instant | independent agreement |
| `verify_solution.py` | from-definition verifier of every solution in a results file (Fraction identity + per-prime divisibility + primality) | instant | control-list verification |
| `lemmas.py` | exact rational constants for the NOTE lemmas (1412, 59, 26, 9, and the `S_odd(m) < 2 − 3^{−m}` sweep) | ~2 min | lemma constants |

## Reproduction

```bash
cd conjectures/odd-giuga
gcc -O2 -shared -fPIC -o kernel.so kernel.c
python3 search.py --eps -1 --parity all --m 1 --mmax 8 --jobs 4 --out results/control_giuga.jsonl
python3 search.py --eps  1 --parity all --m 1 --mmax 8 --jobs 4 --out results/control_ppn.jsonl
python3 search.py --eps -1 --parity odd --m 1 --mmax 14 --jobs 4 --split-depth 7 \
    --resume results/resume_odd_giuga.jsonl --out results/odd_giuga.jsonl
python3 search.py --eps  1 --parity odd --m 1 --mmax 14 --jobs 4 --split-depth 7 \
    --resume results/resume_odd_ppn.jsonl --out results/odd_ppn.jsonl
python3 verify_solution.py results/control_giuga.jsonl results/control_ppn.jsonl
python3 engine2.py -1 odd 3 11   # independent engine, overlapping range
python3 lemmas.py
```

Environment: 4 cores / 15 GB (cloud sandbox), Python 3.11.15, gmpy2 2.3.1,
sympy 1.14.0, numpy 2.4.6, gcc -O2. Wall times in the run records.

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `results/control_giuga.jsonl`, `results/control_ppn.jsonl` | `search.py` | control run records: solutions (= the published lists), node counts, closure statistics, engine hashes, complete flags |
| `results/odd_giuga.jsonl`, `results/odd_ppn.jsonl` | `search.py` | frontier run records: the exhaustions behind results 1–2 |
| `results/resume_*.jsonl` | `search.py` | per-unit completion ledger of the long runs (the certificate that every subtree of the split was exhausted, with per-unit statistics) |
| `results/e2_*.jsonl` | `engine2.py` | independent-engine records on the overlap range |

## Known defects and open threads

- The engine's primality is GMP probable-prime (trial division +
  Miller–Rabin). This is one-sided in the safe direction everywhere except
  divisor-route factorizations, where factors ≥ 2^64 would rest on
  BPSW+MR; the runs report any such factor (`bpsw_factors`) and the
  frontier runs report none. See NOTE Lemma 12.
- `m = 16` (the next even rung) is ~2 orders of magnitude beyond `m = 14`;
  needs a cluster or a genuinely better bound at `t ≥ 3`.
- The literature comparison (BBBG 1996, BMS 2013) is (secondary)
  throughout: the sandbox has no access to the papers; only the recorded
  bounds are compared against, and this session's bounds stand on their
  own certificates.

## Prior work

- G. Giuga (1950): the primality conjecture. BBBG, "Giuga's conjecture on
  primality", Amer. Math. Monthly 103 (1996): counterexamples are
  Giuga+Carmichael, > 13800 digits; recorded source of the odd-Giuga
  ≥ 14 and the `sum − prod ≥ 2` ⇒ ≥ 59 bounds (secondary).
- Borwein–Maitland–Skerritt (Integers 2013): conjecture counterexample has
  ≥ 4771 prime factors, > 10^19907 (secondary); companion code repository
  is an empty placeholder (checked 2026-08-23).
- Butske–Jaje–Mayernik (Math. Comp. 2000): complete census of
  `1/N + Σ 1/p = 1` (PPN/Znám) for ≤ 8 prime factors (secondary).
- Wang (arXiv:2605.21518, Apr 2026): first 9-factor PPN; Alekseyev
  (Aug 2026): no further A054377 term below 10^24 (secondary; the two new
  PPNs were re-verified exactly in this session's environment).
- OEIS A007850 (Giuga), A054377 (PPN), A075441 (Znám solution counts)
  (secondary — OEIS unreachable from this sandbox; values from search
  snippets, then reproduced independently by the engine).
