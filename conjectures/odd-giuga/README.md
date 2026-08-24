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
| 1 | **Every odd Giuga number has at least 14 prime factors** — exhaustion of `Σ 1/pᵢ − 1/n = 1` over all sets of `m ≤ 12` distinct odd primes (empty; `m = 13` excluded by the parity lemma), equalling the recorded bound (secondary) with, to our knowledge, the first open, certified, reproducible derivation | **CERTIFIED** runs + **PROVED** lemmas |
| 2 | **Every odd primary pseudoperfect number — equivalently every all-prime (improper-allowed) Znám solution in odd primes — has at least 14 prime factors**; the strongest recorded statement located is the ≥ 9 consequence of Butske–Jaje–Mayernik's census (secondary), so this appears to be a new bound | **CERTIFIED** + **PROVED** |
| 3 | Control censuses reproduced from scratch, exactly: **all 12 published Giuga numbers have ≤ 8 prime factors and are the complete census there** (m=8: 3 solutions, 831,968 nodes, 512 s) and **the 8 published PPNs are the complete census for ≤ 8 factors** (m=8: 1 solution, 510 s) — the first reproduction of BBBG 1996 / BJM 2000 with open code and committed certificates; independent from-definition verifier passes 21/21 and 8/8 solution sets | **CERTIFIED** |
| 4 | Lemma layer: both families are the two signs of `Σ 1/pᵢ + ε/n = 1` below 1412 odd factors; **odd solutions have an even number of prime factors** (possibly folklore); engine-soundness lemmas (windows, `(Dq−P)(Dr−P) = P²+εD` closure with `gcd(u,D)=1`, one-sided primality, wheel filter) | **PROVED** |
| 5 | Classical constants reproduced by exact computation: ≥ 9 factors for odd members (both signs), ≥ 59 factors for `sum − prod ≥ 2`; the parity-refined floor is ≥ 10 | **PROVED** (exact sums) |
| 6 | The `m = 13` wall quantified: the odd `m = 13` tree contains `t = 3` nodes of deficit `~10⁻⁹` whose closure cost is `~10¹⁵` kernel candidates (observed live node recorded in NOTE §3.1) vs `2.8×10¹⁰` for all of `m ≤ 12` — direct exhaustion is ~5 orders past a 4-core session, which also bears on what the 1996 "14" can have been | analysis (NOTE §3.1) |
| 7 | **9-factor Giuga census attempted; the same wall, measured on the even side** — the run reached the near-fill region and its live workers were profiled at prefixes `(2, 3, 7, 43, 1811, ≈654371, ≈1.8×10⁹)` with two-primes-left windows of width `~10¹²`, each t = 3 near-fill node fanning into `~10⁸` p₇-candidates and each candidate demanding a ~43-digit factorization: the 9-factor stratum is `~10⁵×` beyond the complete m = 8 census. Conclusion: BBBG (1996) and BJM (2000) stopped at 8 factors at a *structural* horizon of the branch-and-close method, not a hardware one — consistent with BJM's own remark about the 9-factor step, and with the 2026 PPN-side finds coming from constructive methods | analysis (NOTE §3.1) |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `search.py` | exact BnB over prime sets solving `Σ 1/pᵢ + ε/n = 1`; gmpy2 integers, C kernel (`kernel.c`) for two-primes-left scans, FLINT divisor route, per-unit resume, JSONL records | odd m=12: 117 s; even m=8 census: 512 s | the exhaustions and censuses |
| `kernel.c` | u128 scan of the closure window: keeps `q` with `(Dq−P) \| P²+εD`; wheel filter over primes ≤ 61; valid for `P + 2D + 2 < 2⁶⁴` | — | — |
| `engine2.py` | clean-room cross-check: stdlib Fractions + sympy, independently derived looser windows, no kernel, no divisor route | odd m ≤ 11: 2 s | independent agreement everywhere it reaches |
| `verify_solution.py` | from-definition verifier of every solution in a results file (Fraction identity + per-prime divisibility + primality) | instant | 29/29 across control files |
| `lemmas.py` | exact rational constants for the NOTE lemmas (1412, 59, 26, 9, and the `S_odd(m) < 2 − 3⁻ᵐ` sweep) | ~2 min | lemma constants |
| `run_official.sh` | the frozen-engine official run set, resumable, appending to `results/` | hours end-to-end | — |

## Reproduction

```bash
cd conjectures/odd-giuga
python3 -m pip install gmpy2 sympy numpy python-flint
gcc -O2 -shared -fPIC -o kernel.so kernel.c
./run_official.sh          # or the individual commands inside it
python3 verify_solution.py results/control_giuga_official.jsonl results/control_ppn_official.jsonl
python3 engine2.py -1 odd 3 11    # independent engine, overlap range
python3 lemmas.py
```

Environment: 4 cores / 15 GB (cloud sandbox), Python 3.11.15, gmpy2 2.3.1,
sympy 1.14.0, numpy 2.4.6, python-flint 0.9.0, gcc -O2. Wall times, node
counts and engine hashes are in every run record. Engine changes during
the session were each gated by a fixed battery (the ≤ 7-factor censuses
on both signs and the odd `m = 12` fingerprint — 240,534 closures, summed
window width 28,131,218,255 — reproduced identically by five independent
traversals across engine versions).

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `results/odd_giuga_official.jsonl`, `results/odd_ppn_official.jsonl` | `search.py` | the Theorem A/B exhaustion records, `m = 1..12`, complete flags, closure statistics, engine hashes |
| `results/control_giuga_official.jsonl`, `results/control_ppn_official.jsonl` | `search.py` | the census records with the published solutions found (12 and 8 numbers) |
| `results/resume_odd_*.jsonl` | `search.py` | per-unit exhaustion ledgers of the odd ladders |
| `results/e2_odd_giuga.jsonl`, `results/e2_odd_ppn.jsonl` | `engine2.py` | independent-engine emptiness records, odd `m ≤ 11` |
| `results/official_driver.log` | `run_official.sh` | the full driver transcript with phase timestamps |

Fat per-unit ledgers of the control/census runs (hundreds of MB) are
regenerable and excluded from git per the repository's ~10 MB policy;
the official run records above are the committed certificates.

Provenance note: a driver launched twice by accident, so the odd ladders
(and part of the Giuga control) appear **twice** in the official files —
two complete passes under two engine builds. All closure invariants
(`t2_closures`, `t2_width_sum`, `t2_width_max`, solutions, complete
flags) agree pair-for-pair; only `nodes` differs at odd m = 8, 9 because
serial runs count the frontier-side nodes that parallel runs leave to
the splitter. Kept as an (unplanned) additional cross-validation.

## Known defects and open threads

- Primality inside the engine is GMP probable-prime: one-sided in the
  safe direction everywhere except inside divisor-route factorizations,
  where factors are re-verified and any factor ≥ 2⁶⁴ would be disclosed
  per run (`bpsw_factors`); every official run reports none. NOTE
  Lemma 12.
- `m = 13` odd (and `m = 14`, the rung that would beat the recorded
  bound) are ~5 and ~7 orders of magnitude beyond a 4-core session by
  the measured tree shape; NOTE §4 lists what could change that.
- All literature comparisons are (secondary): the sandbox has no access
  to the papers, only to search-snippet excerpts; the bounds here stand
  on this session's own certificates.
- The odd `m ≥ 10` trees for the two signs coincide node-for-node
  (`ε` shifts every window bound by less than the integer floor there);
  they differ at `m ≤ 9`, and the controls distinguish the signs
  decisively. Observed, explained in NOTE, and harmless — but worth
  knowing before comparing fingerprints.

## Prior work

- G. Giuga (1950): the primality conjecture. Borwein–Borwein–Borwein–
  Girgensohn, "Giuga's conjecture on primality", Amer. Math. Monthly 103
  (1996): counterexamples are Giuga+Carmichael with > 13800 digits;
  recorded source of the odd ≥ 14 and the `sum − prod ≥ 2` ⇒ ≥ 59
  bounds (secondary), and of the even `m ≤ 8` Giuga census reproduced
  here.
- Borwein–Maitland–Skerritt (Integers 2013): conjecture counterexamples
  have ≥ 4771 prime factors, > 10^19907 (secondary); companion code
  repository confirmed to be an empty placeholder (2026-08-23).
- Butske–Jaje–Mayernik (Math. Comp. 2000): complete census of
  `1/N + Σ 1/p = 1` for ≤ 8 prime factors (secondary), reproduced here.
- Wang (arXiv:2605.21518, Apr 2026): first 9-factor PPN; Alekseyev
  (Aug 2026): no further A054377 term below 10^24 (secondary; both new
  PPNs were re-verified exactly during the survey). The PPN `m = 9`
  stratum is deliberately left to those authors; the Giuga `m = 9`
  stratum (result 7) is untouched territory.
- OEIS A007850 (Giuga), A054377 (PPN), A075441 (Znám counts) —
  (secondary; unreachable from this sandbox, values triangulated from
  search snippets and then reproduced independently by the engine).
