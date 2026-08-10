# Erdős #699 — common prime factors of binomial coefficients

**Problem** ([erdosproblems.com/699](https://www.erdosproblems.com/699);
Erdős–Szekeres 1978): for 1 ≤ i < j ≤ n/2, is there always a prime
p ≥ i dividing gcd(C(n,i), C(n,j))? The **strengthening** conjectures
p > i works outside a *finite* set of exceptional triples. Status: open
(both maintained mirrors, 2026-08-10). A triple with no witness p > i
is a *strict failure*; it is an *exception* if p = i saves the base
form, a *counterexample* to #699 otherwise.

**Status here: active.** Session 1 (2026-08-10).

## Results

| # | Claim | Label |
|---|---|---|
| 1 | Base form holds and the strict failures for **all n ≤ 10⁹** are exactly the 9 triples of the census table below — none with composite i, so **no counterexample to #699 below 10⁹** | **CERTIFIED** |
| 2 | **Four new exceptional triples** beyond every previously reported one: (2^k, 2, j_k) for k = **41, 67, 101, 137**, with j₄₁ = 285920731515, j₆₇ = 23206563898901803639, j₁₀₁ = 137177249633792241973877360183, j₁₃₇ = 16141961986503368055107762054812561012816 — at n up to ≈ 1.7·10⁴¹; each verified by an independent checker with **deterministic** primality (Sorenson–Webster bound), and each the *unique* strict failure at its (n, i) | **CERTIFIED** |
| 3 | Level i = 1 never fails; only levels 2 ≤ i ≤ n − prevprime(n) can fail; witness pool = primes of the gap window (NOTE R1–R5, L1) | **PROVED** |
| 4 | Exact characterization of the i = 3 family: for n = 3^m+1, (n, 3, n/2) fails strictly **iff** every prime p > 3 of 3^{2m}−1 satisfies the cofactor digit-domination condition (NOTE Lemma 4); both odd parts prime powers ⟹ failure, for odd m (Corollary 5) | **PROVED** |
| 5 | The i = 3 family is exactly m ∈ {2, 3, 5, 7, 13} for every decided m ≤ 120 (all but m = 89, 119, blocked by two uncracked 40+-digit cofactors), and **no member beyond m = 13 exists via the prime-power criterion up to m = 1400** (n ≈ 10⁶⁶⁸) | **CERTIFIED** (BPSW-grade primality for large auxiliaries) |
| 6 | The i = 2 family (n = 2^k) is exactly k ∈ {4, 9, 11, 41, 67, 101, 137} among all decided k: **every k ≤ 120**, plus k ∈ {131, 137, 139, 167, 197, 199, 241} via self-verified factorizations; level 3 at n = 2^k is clean for every decided k (that channel would produce counterexamples when k ≢ 0,1 mod 6) | **CERTIFIED** (BPSW-grade above the SW bound) |
| 7 | Heuristic: the i = 3 family should be finite (twin repunit-prime events, density ~ m⁻²) but the i = 2 family should be **infinite** (digit-alignment at Mersenne-semiprime exponents fires at observed rate 7/21 ≈ ⅓) — so the Erdős–Szekeres strengthening is **probably false as stated**, while the base form is untouched (every 2^k failure is saved by p = 2, NOTE Lemma 6) | **NUMERICAL** |

**Census of all strict failures, n ≤ 10⁹** (all EXC, saved by p = i):
(10, 3, 5), (16, 2, 6), (28, 3, 14), (28, 5, 14), (244, 3, 122),
(512, 2, 147), (2048, 2, 713), (2188, 3, 1094), (1594324, 3, 797162).
The prior frontier was an unpublished forum sweep to 10⁷ (secondary; no
code or certificate); (2048, 2, 713) and everything in rows 2, 4–6 are
new to this session.

## Scripts

| script | what it does | cost |
|---|---|---|
| `proto699.py` | semantics prototype + dual-path cross-check (Kummer vs big-int gcd) | 2 s |
| `brute699.c` | exhaustive all-pairs validator, per-prime bitsets | n ≤ 3000: ~4 min·4 cores |
| `scan699.c` | production sweep: windowed factorization, gap cut R3, prime-power CRT filter R5, exact slow path | [4, 10⁹): ~35 min·4 cores |
| `audit699.c` | independent third-path auditor (trial division, full j-scans, recorded seeds) | ~10 min·4 cores |
| `families.py` | exact level-2/3 decisions for n = 2^k, 3^m+1 from complete factorizations (cyclotomic split + Brent rho); built-in Lemma-4 cross-check | k, m ≤ 120: ~25 min |
| `repunit_hunt.py` | prime-power criterion scan over m ≤ 1400 | ~4 min |
| `bigk_hunt.py` | big-k decisions from self-verified recalled factorizations | seconds |
| `verify_exceptions.py` | independent verifier + completeness re-enumeration for all 13 exceptional triples; deterministic MR < 3.317·10²⁴ | seconds |

## Reproduction

```bash
cd conjectures/erdos-699
python3 verify_exceptions.py               # certify all 13 exceptional triples
gcc -O2 -march=native -o scan699 scan699.c && ./scan699 4 3001 out.csv
gcc -O2 -march=native -o brute699 brute699.c && ./brute699 4 3000 m.csv > x.txt
diff <(tail -n+2 out.csv | sort) <(awk '{print "EXC,"$2","$3","$4","$3}' x.txt | sort)  # censuses agree
python3 families.py pow3 18                # reproduces the m-family anchors
python3 repunit_hunt.py 1400
```

Environment: 4 cores, 15 GB RAM, gcc 13.3.0, Python 3.11.15, gmpy2,
sympy (cyclotomic polynomials only). All critical-path arithmetic is
exact integer; no floating point anywhere; the only randomness is the
auditor's recorded LCG seeds.

## Known defects / scope notes

- m = 89, 119 of the 3^m+1 family are UNDECIDED (40- and 44-digit
  composite cofactors beyond in-sandbox rho); k beyond 120 decided only
  at the listed self-verified exponents.
- Large-factor primality above 3.317·10²⁴ (result rows 5–6 only) is
  BPSW+50MR probable-prime grade; every prime in the 13 exceptional
  triples themselves is below the Sorenson–Webster bound and hence
  deterministic.
- The structured-family checks at exponents beyond the sweep decide
  levels i ∈ {2, 3} (the levels the factorizations reach); higher
  levels at those specific n are unswept — no failure of any kind has
  ever been seen at i ≥ 4 except (28, 5, 14).
- [ErSz78] itself is unreadable from this sandbox; all statements about
  its contents are (secondary).
