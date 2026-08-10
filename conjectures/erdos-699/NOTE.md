# Common prime factors of binomial coefficients: the exceptional set of Erdős problem #699

**Session date.** 2026-08-10. AI-assisted (Claude); disclosed per repository
policy. All claims carry the repository's PROVED / CERTIFIED / NUMERICAL
labels.

## Abstract

Erdős problem #699 asks whether for every 1 ≤ i < j ≤ n/2 some prime
p ≥ i divides gcd(C(n,i), C(n,j)); Erdős–Szekeres conjectured further
that p > i works outside a *finite* exceptional set of triples [ErSz78]
(secondary). We give a complete, reproducible verification apparatus for
the problem and run it to 10⁹: the base conjecture holds for all
n ≤ 10⁹, and the strict-form (p > i) failures below 10⁹ are exactly
nine triples, each saved by p = i (§3). We prove a structural
characterization of the two families these failures form: for
n = 3^m + 1 the triple (n, 3, n/2) fails strictly **iff** an explicit
digit-domination condition holds at every prime p > 3 of 3^{2m} − 1
(Lemma 4), and for n = 2^k the level-2 failures are the nonempty
CRT-digit intersections of the primes of 2^k − 1 (§5). The
characterizations decide the families at exponents far beyond any sweep
(k, m ≤ 120 subject to factorization completeness; prime-power scan to
m ≤ 1400) and produce **four new exceptional triples** — at
n = 2⁴¹, 2⁶⁷, 2¹⁰¹, 2¹³⁷, the largest with 42-digit n — apparently the
first exhibited beyond the classical list, each certified with
deterministic primality (§6). The data support a bipartite heuristic
conclusion (§7): the
i = 3 family should be **finite** (twin prime-power events of density
~ 1/m²), while the i = 2 family should be **infinite** (driven by
Mersenne semiprimes at positive density per exponent) — so the
Erdős–Szekeres strengthening is heuristically **false as stated**, even
though every known and predicted failure is saved by p = i and the base
problem #699 is untouched. The p = i rescue is itself structural: at
composite i the two forms coincide, so the base conjecture is refutable
exactly through composite-i strict failures, of which the sweep found
none.

## 1. The problem

For integers 1 ≤ i < j ≤ n/2, [ErSz78] proved gcd(C(n,i), C(n,j)) > 1
(the neighbouring problem #698, quantitatively strengthened by Bergman
[Be11] (secondary)) and asked (problem #699, statement fixed by the Lean
formalization in `google-deepmind/formal-conjectures`, fetched
2026-08-10):

> **#699 (base form).** Is it true that for every 1 ≤ i < j ≤ n/2 there
> is a prime p ≥ i with p | gcd(C(n,i), C(n,j))?
>
> **Strengthening (`erdos_szekeres_strengthening`).** There is a finite
> set E of triples such that for all (n,i,j) ∉ E with 1 ≤ i < j ≤ n/2,
> some prime p > i divides gcd(C(n,i), C(n,j)).

Call (n,i,j) a **strict failure** if no prime p > i divides both
coefficients; a strict failure is an **exception** (EXC) if p = i saves
the base form (i prime, i | C(n,i), i | C(n,j)) and a **counterexample**
(CEX) to #699 otherwise. Since for composite i "p ≥ i" and "p > i"
coincide on primes, **the base conjecture can fail only through a strict
failure at composite i** (or prime i with the p = i test failing) —
Observation 1. The classical Sylvester–Schur theorem (each single
C(n,i), i ≤ n/2, has a prime factor > i; formal proof exists in
`AllenGrahamHart/FormalConjectures-Bench`) makes the *common*-prime
requirement the entire content.

Status: open per `teorth/erdosproblems` (`falsifiable`, 2025-08-31) and
the Lean mirror (both statements `research open`, 2026-01-04). Prior
computation: one unpublished forum sweep (secondary; no code, author, or
certificate recoverable) reporting the base form verified to n = 10⁷,
plus families 2^k (k ≤ 27) and 3^m + 1 (m ≤ 17), with strict failures at
i = 3, n = 3^m + 1, j = n/2 for m ∈ {2,3,5,7,13} and the lone i ≥ 4
triple (28,5,14).

## 2. Reductions

Everything below n-specific rests on five elementary facts. Fix n and
write g(n) = n − prevprime(n) (g(n) = 0 iff n prime).

**R1 (Kummer/Lucas).** p | C(n,k) iff some base-p digit of k exceeds the
corresponding digit of n ("k is not p-dominated by n").

**R2 (witness window).** For p > i: p | C(n,i) iff n mod p < i. Hence
the level-i witness pool is T_i = {p prime > i : n mod p < i} ∪ {i if i
prime, n mod i² < i}, and every p ∈ T_i with p > i divides exactly one
of n, n−1, …, n−(i−1) — T_i is read off the factorizations of an
i-window below n.
*Proof.* For p > i, i is a single base-p digit, so by R1 p | C(n,i) iff
i > n mod p. For p = i: i = (1,0) base p, so p | C(n,i) iff the p-digit
of n at position 1 is 0, i.e. n mod p² < p. If p | n−r and p | n−r′ with
r, r′ < i < p then p | r−r′ forces r = r′. ∎

**R3 (gap bound).** If i > g(n) then (i,j) has the witness
p = prevprime(n): indeed p > n/2 ≥ j > i by Bertrand, and
n mod p = g(n) < i < j, so p divides both coefficients by R2. **Only
levels 2 ≤ i ≤ g(n) can host strict failures** (levels i = 1 by L1
below; n prime has g = 0 and no failures at all).

**L1 (level 1 never fails).** For every n and 1 < j ≤ n/2 some prime
p | n divides C(n,j).
*Proof.* If p^e ∥ n then the e lowest base-p digits of n are 0, so a j
that is p-dominated by n must have its e lowest digits 0, i.e.
p^e | j. If j were dominated for every p | n then n | j, impossible for
0 < j ≤ n/2. So some p | n has j not dominated, i.e. p | C(n,j) by R1;
and p ≥ 1 = i trivially. ∎
(For i = 1 the strict form p > 1 is the same statement since every
prime exceeds 1.)

**R5 (candidate confinement).** Let p^e ∥ n−r with r = n mod p < i ≤ p.
Every strict-failure j at level i satisfies j ≡ b (mod p^e) for some
0 ≤ b ≤ r, and the base-p digits of ⌊j/p^e⌋ are dominated by those of
(n−r)/p^e.
*Proof.* p ∈ T_i by R2, so j must be p-dominated by n. In base p,
n = ((n−r)/p^e digits, 0×(e−1), r): positions 1..e−1 carry digit 0
(p^e | n − r and r < p), position 0 carries r. Domination forces j's
digits there to be 0 and ≤ r respectively. ∎

R5 applied to the two largest available prime powers confines all
candidate j to ≤ (r₁+1)(r₂+1) ≤ i² CRT classes modulo their product —
the engine of the sweep (§8) and of the family analysis (§4–5).

## 3. The census to 10⁹ (CERTIFIED)

**Theorem 2 (CERTIFIED).** For every 4 ≤ n ≤ N₀ = 10⁹ and
1 ≤ i < j ≤ n/2:
some prime p ≥ i divides gcd(C(n,i), C(n,j)) — the base form of #699
holds — and the strict failures (no p > i) are exactly the nine triples

| n | i | j | structure | saved by |
|---|---|---|---|---|
| 10 | 3 | 5 | 3² + 1, j = n/2 | p = 3 |
| 16 | 2 | 6 | 2⁴ | p = 2 |
| 28 | 3 | 14 | 3³ + 1, j = n/2 | p = 3 |
| 28 | 5 | 14 | — (the only i ≥ 4 failure known) | p = 5 |
| 244 | 3 | 122 | 3⁵ + 1, j = n/2 | p = 3 |
| 512 | 2 | 147 | 2⁹ | p = 2 |
| 2048 | 2 | 713 | 2¹¹ | p = 2 |
| 2188 | 3 | 1094 | 3⁷ + 1, j = n/2 | p = 3 |
| 1594324 | 3 | 797162 | 3¹³ + 1, j = n/2 | p = 3 |

In particular there is **no counterexample to #699 below 10⁹**, and no
strict failure with composite i.

*Method and certificate.* Exact integer arithmetic throughout (Lucas
digit tests; no floating point). Three independent implementations:
(a) a Python prototype (Kummer path vs big-int gcd path, agreement on
n ≤ 120); (b) a C brute force over all pairs with per-prime bitsets,
n ≤ 3000; (c) the production engine `scan699.c` (windowed segmented
factorization, R3 gap cut, R5 prime-power CRT filter with exact
per-level slow path). (b) and (c) produce **byte-identical censuses on
[4, 3000]**; (c) ran [4, 10⁹) in four disjoint chunks plus a separate endpoint
check at n = 10⁹ (121,612,945 n escalated to the exact slow path,
16.65·10⁹ candidate j walked and tested, zero fallbacks, zero hard
errors, all workers exit 0); a fourth implementation, `audit699.c`
(trial-division factoring, full j-scans, LCG seeds 699–702 recorded),
re-derived the strict-failure sets at 48 random (n,i) plus all nine
census pairs as positive controls. Worker ranges, stats, runtimes:
`data/census_1e9.log`. Scope note: "verified for n ≤ 10⁹" is a
CERTIFIED statement about that range, not evidence beyond it.

## 4. The i = 3 family: exact characterization (PROVED)

Throughout this section n = 3^m + 1, m ≥ 2, j = n/2 (n ≡ 2 or 4 mod 8,
so j is an integer; j ≤ n/2 with equality — admissible since
i = 3 < j).

**Lemma 3 (saved by 3).** 3 | C(n,3) and 3 | C(n, n/2) for every m ≥ 2.
*Proof.* Base 3: n = (1, 0, …, 0, 1) (digits at positions m and 0).
i = 3 = (1,0): position-1 digit 1 > 0 = n's. j = n/2: since
(3^m−1)/2 = (1,1,…,1) base 3 (m ones), j = (3^m−1)/2 + 1 has base-3
digits (1, 1, …, 1, 2): position-0 digit 2 > 1 = n's. By R1 both are
divisible. ∎ So a strict failure here is always an exception, never a
counterexample.

**Lemma 4 (characterization).** (n, 3, n/2) is a strict failure iff for
every prime p > 3 dividing 3^{2m} − 1, writing p^e ∥ 3^m − ε (ε = ±1
the side p divides) and c_p = (3^m − ε)/p^e (an even integer), the
base-p digits of c_p/2 are dominated by those of c_p.

*Proof.* By R2 the level-3 witness pool T₃ consists of primes p > 3
with n mod p ∈ {0,1,2}, i.e. p | n, p | n−1 or p | n−2. Here
n−1 = 3^m contributes nothing (> 3), so T₃ = {p > 3 : p | 3^m+1 or
p | 3^m−1}, and these are exactly the primes p > 3 of
3^{2m}−1 = (3^m−1)(3^m+1); no prime > 2 divides both sides
(gcd = 2). The triple is a strict failure iff j is p-dominated by n for
every p ∈ T₃.

Side ε = −1 (p | n − 2, n mod p = 2): n = c p^e + 2 with c = c_p, so
n's base-p digits are (digits of c, 0×(e−1), 2), and
j = n/2 = (c/2)p^e + 1 has digits (digits of c/2, 0×(e−1), 1). Since
1 ≤ 2 and 0 ≤ 0, domination holds iff digits(c/2) ≼ digits(c).

Side ε = +1 (p | n, n mod p = 0): n = c p^e, digits
(digits of c, 0×e); j = (c/2) p^e, digits (digits of c/2, 0×e);
domination iff digits(c/2) ≼ digits(c). ∎

**Corollary 5 (prime-power criterion).** If the odd parts of 3^m − 1
and 3^m + 1 are prime powers q^a, s^b (q, s > 3 or the part is 1), then
the only cofactors are c = 2^{v} with v = v₂(3^m ∓ 1), and the
condition of Lemma 4 at q, s reads: the base-q (resp. base-s) digits of
2^{v−1} are dominated by those of 2^v — automatic whenever 2^v < p. For
odd m, v₂(3^m−1) = 1 and v₂(3^m+1) = 2, so **odd parts both prime
powers ⟹ strict failure**. For even m the digit condition must be
checked (it fails e.g. at m = 4: 2⁴ ∥ 3⁴−1, and 8 = (1,3)₅ is not
dominated by 16 = (3,1)₅ — which is exactly why n = 82 is not
exceptional although both odd parts are prime).

**Verified instances (CERTIFIED).** The exact level-3 checker
(`families.py`, greedy prime-power CRT + full domination tests, all
candidates enumerated) decides every m with complete factorizations of
3^m ∓ 1 (cyclotomic split; deterministic Brent rho): for m ≤ 18 it
reproduces the sweep exactly — failures at m ∈ {2,3,5,7,13} only,
always at j = n/2 alone, never at level 2 (the prime power 3^m ∥ n−1
dominates: candidates ≡ {0,1} mod 3^m, none in range — a one-line
lemma). Lemma 4, evaluated independently per m, agrees with the checker
at every decided m (built-in cross-check). Deep run to m ≤ 120: see
`data/fam_pow3.csv` and §6.

**Scan to m = 1400 (CERTIFIED for the criterion, BPSW-grade
primality).** No m in (13, 1400] has both odd parts prime powers
(`repunit_hunt.py`: trial division to 10⁵, then BPSW with 40 extra MR
rounds, perfect powers to exponent 11). So no member of this family
beyond m = 13 can arise through Corollary 5 up to n = 3^1400 + 1
≈ 10^668; a member would need a *composite* side satisfying Lemma 4 at
every one of its primes (see the heuristics, §7).

## 5. The i = 2 family: n = 2^k (PROVED structure, CERTIFIED decisions)

**Lemma 6.** Every strict failure at level 2 with n = 2^k is an
exception (saved by p = 2): v₂(C(2^k, 2)) = k − 1 ≥ 1, and base-2
domination of j by 2^k = (1, 0×k) forces j ∈ {0, 2^k}, so
2 | C(2^k, j) for all 1 ≤ j ≤ 2^{k−1}.

**Structure.** T₂ = odd primes of 2^k − 1, each with residue r = 1, so
by R5 the strict failures at (2^k, 2, ·) are exactly the
j ∈ [3, 2^{k−1}] with j ≡ 0, 1 (mod p^e) and upper base-p digits
dominated by those of (2^k−1)/p^e, simultaneously for every
p^e ∥ 2^k − 1. This is decidable per k from the factorization of
2^k − 1 (`families.py pow2`): below 10⁹ the failures are k = 4 (j = 6),
k = 9 (j = 147), k = 11 (j = 713) — reproduced independently by the
sweep — and 2^k − 1 is a semiprime P·Q in all three cases
(15 = 3·5, 511 = 7·73, 2047 = 23·89).

**Level 3 at n = 2^k — a counterexample channel.** T₃ = primes > 3 of
(2^k−1) [r = 1] and 2^{k−1}−1 [r = 2]; the saving witness p = 3
requires n mod 9 < 3, i.e. k ≡ 0, 1 (mod 6). A level-3 strict failure
at any 2^k with k ≡ 2,3,4,5 (mod 6) would be a **counterexample to
#699**. None exists for k ≤ 120 (decided cases; `data/fam_pow2.csv`).

**Observation 7 (odd n need small primes).** In any strict failure with
n odd, some prime factor of n is ≤ i: otherwise L1's argument applies
to the full odd n (every p | n has p > i, so p ∈ T_i, and domination
for all of them forces n | j). Consistently, all known failures have n
even.

## 6. Deep family decisions: four new exceptional triples (CERTIFIED)

**Theorem 8 (CERTIFIED).** The following are strict failures of the
Erdős–Szekeres strengthening, each an exception (saved by p = 2), each
the unique strict failure at its (n, i = 2), and each verified by an
independent checker (`verify_exceptions.py`, output in
`certs/verify_output.txt`) with every primality proof deterministic
(all primes < 3.317·10²⁴, the Sorenson–Webster 13-base bound):

| k | n = 2^k | j | 2^k − 1 |
|---|---|---|---|
| 41 | ≈ 2.199·10¹² | 285 920 731 515 | 13367 · 164511353 |
| 67 | ≈ 1.476·10²⁰ | 23 206 563 898 901 803 639 | 193707721 · 761838257287 (Cole 1903) |
| 101 | ≈ 2.535·10³⁰ | 137 177 249 633 792 241 973 877 360 183 | 7432339208719 · 341117531003194129 |
| 137 | ≈ 1.743·10⁴¹ | 16 141 961 986 503 368 055 107 762 054 812 561 012 816 | 32032215596496435569 · 5439042183600204290159 |

To our knowledge these are the first exceptional triples exhibited
beyond the classical list (the problem page cites failures at i = 2
for "particular powers of 2", i = 3 examples, and (28,5,14); the
unpublished forum sweep reached n ≈ 1.3·10⁸ < 2⁴¹). They are far
beyond any sweep's reach; they were found by the structural reduction
(R5 confinement over the factorization of 2^k − 1), not by search over
n.

**Complete family decisions.**
- *i = 2, n = 2^k*: decided for **every** k ≤ 120 (complete
  factorizations via cyclotomic split + Brent rho) and for
  k ∈ {131, 137, 139, 167, 197, 199, 241} (recalled factorizations,
  verified in-script by exact product + primality — a wrong
  recollection can only yield UNDECIDED, never a wrong decision; three
  recollections did fail verification and were discarded). Failures:
  exactly k ∈ {4, 9, 11, 41, 67, 101, 137}.
- *i = 3 at n = 2^k*: clean at every decided k — relevant because a
  level-3 failure at k ≢ 0, 1 (mod 6) would have been a
  **counterexample to #699** (the p = 3 rescue needs n mod 9 < 3).
- *i = 3, n = 3^m + 1*: decided for every m ≤ 120 except m = 89, 119
  (uncracked 40- and 44-digit cofactors). Failures: exactly
  m ∈ {2, 3, 5, 7, 13}, always j = n/2 alone; level 2 clean at every
  m (the prime power 3^m ∥ n−1 confines candidates to j ∈ {0, 1}).
  The prime-power criterion (Corollary 5) is empty for
  13 < m ≤ 1400.
- Primality grade: every prime below 3.317·10²⁴ deterministic. **No
  FAIL row depends on a probable prime** — all primes in all 13
  exceptional triples are below the bound. The handful of larger
  cofactors occur only in NONE-rows (k = 131, 139, 167, 197, 199, 241
  and large-m pow3 rows) and are BPSW+50MR, flagged per-row in the
  data files; a BPSW failure there could only hide a *further*
  exception, never invalidate an exhibited one.

## 7. Heuristics: the exceptional set is (probably) infinite (NUMERICAL)

Two families, two different verdicts.

**i = 3 family: finite.** By Corollary 5 (and the near-necessity of
prime-power sides once cofactor digits must align at every prime),
membership at odd m essentially requires (3^m−1)/2 and (3^m+1)/4 both
prime. Repunit-prime heuristics give each event density ~ c/m;
independence gives ~ c′/m², and Σ 1/m² converges: **finitely many
members expected beyond 13** (expected count over m ∈ (13, ∞) of order
10⁻¹ by the standard constants). The m ≤ 1400 scan (§4) found none.

**i = 2 family: infinite.** For k with 2^k − 1 = P·Q semiprime
(P < Q), the candidate set has expected size
|D_P ∩ [0,2^{k−1}]| · |D_Q ∩ [0,2^{k−1}]| / 2^{k−1} ≈ (2Q · 2P)/2^k
≈ 2 — order one per semiprime exponent, Poisson-ish in the digit
alignment. The session's decided data (§6): among the **22** exponents
whose 2^k − 1 has exactly two prime-power factors, the alignment event
fired at **7** — k ∈ {4, 9, 11, 41, 67, 101, 137} — and missed at 15
(6, 23, 37, 49, 59, 83, 97, 103, 109, 131, 139, 167, 197, 199, 241):
observed rate ≈ 1/3, consistent with the constant-order heuristic
(`data/semiprime_record.csv`, every factorization verified in-script).
At Mersenne-*prime* exponents the witness pool is the singleton
{2^k − 1} and the dominated set is {0, 1}: the family is provably
empty there, so exceptions require composite 2^k − 1 — the heuristic
rides on composite Mersennes of two-prime-power shape, whose count
grows without bound under standard models. Mersenne semiprimes are expected infinite (a positive
fraction of prime exponents heuristically), so **infinitely many
exceptional triples (2^k, 2, j) are expected**. If so, the
Erdős–Szekeres strengthening — a *finite* exceptional set — is
**false as stated**, while the base form #699 is unaffected (Lemma 6:
every such failure is saved by p = 2).

These are heuristics over verified structure: the family memberships
themselves are exact computations; only the density arguments are
NUMERICAL.

## 8. Methodology

**Engines** (all exact integer arithmetic, no floating point, no
randomness except the auditor's recorded seeds):

1. `proto699.py` — reference semantics; two independent divisibility
   paths (Kummer digit test vs big-int gcd + trial factoring), exact
   agreement for n ≤ 120.
2. `brute699.c` — exhaustive all-pairs sweep with per-prime bitsets;
   the ground-truth census on [4, 3000] (≈ 4 min on 4 cores).
3. `scan699.c` — production engine: segmented windowed factorization
   (primes ≤ √B), incremental prevprime, the R3 gap cut (only
   i ≤ g(n) checked; level 1 skipped by L1), the R4/R5 fast filter
   (top-two prime powers of n(n−1) restricted to p > g(n), ≤ 4 CRT
   classes per n), full per-level slow path on every flagged n with
   candidate confinement by the two largest prime powers of T_i and
   explicit enumeration fallbacks. Any capacity or coverage breach
   aborts the run (no silent give-ups). Rate: 4.3 / 6.6 / 9.7 s per
   10⁶ at n ≈ 10⁷ / 10⁸ / 10⁹ (single core).
4. `audit699.c` — independent auditor: trial-division factoring,
   direct prevprime search, full j-scans at 48 pseudo-random (n, i)
   (LCG seeds 699–702, recorded) plus the nine census (n, i) as
   positive controls. Agreement everywhere; all controls rediscovered.
5. `families.py` — family decisions from complete factorizations
   (cyclotomic split, deterministic Brent rho with fixed c-schedule);
   built-in cross-check of Lemma 4 against the general checker at
   every decided m (abort on mismatch; never fired).
6. `verify_exceptions.py` — independent verification + completeness
   re-enumeration of all 13 exceptional triples; Miller–Rabin with the
   Sorenson–Webster 13-base set, deterministic below 3.317·10²⁴.

**Control battery.** (i) Dual implementation: engines 2 and 3 produce
byte-identical censuses on [4, 3000]. (ii) Third path: engine 4 at 57
sampled/control points. (iii) External anchors: the census reproduces
every failure reported by the prior unpublished sweep in the
overlapping ranges — the i = 3 list {10, 28, 244, 2188, 1594324}, the
i = 2 powers of 2 {16, 512}, and (28, 5, 14), whose gcd
1080 = 2³·3³·5 was also re-verified by direct big-int arithmetic.
(iv) Theory–code agreement: Lemma 4 evaluated symbolically matches the
general enumerator at every decided m (automatic abort otherwise).
(v) Negative-direction discipline: three engine bugs were caught
during validation — a heap overflow (crash), a primality-flag
regression (census shrank against ground truth), and a filter
completeness hole (found by proof re-reading, not by any test) — all
three are documented in WRITEUP.md; the production binary is v3.

**Certificates.** `certs/verify_output.txt` (the 13 triples,
deterministic primality); `data/census_1e9.csv` (the sweep output with
per-worker stats); `data/fam_pow2.csv`, `data/fam_pow3.csv` (per-
exponent decisions with UNDECIDED rows explicit); `data/bigk.txt`
(self-verified large-k decisions); `data/audit_*.txt` (auditor
transcripts). Hardware: 4 cores, 15 GB RAM; gcc 13.3.0 -O2
-march=native; Python 3.11.15 + gmpy2; sympy for cyclotomic
polynomials only.

## 9. Open questions

1. Decide more semiprime exponents k (needs Cunningham-grade
   factorizations of 2^k − 1 beyond this sandbox's reach) — each one
   tests the infinitude heuristic; a single new exceptional k would be
   the first new exceptional triple since [ErSz78]'s era at i = 2.
2. Is (28, 5, 14) truly alone for i ≥ 4? The sweep says yes to 10⁹.
   A structural explanation (28 = 3³+1 sits in *both* families'
   shadow: 27 = 3³, 26 = 2·13) is within reach of the R5 calculus.
3. Prove any unconditional infinitude/finiteness statement for either
   family — the i = 2 case reduces to a statement about digit
   alignment over Mersenne semiprimes.
4. The composite-i channel (Observation 1) is the entire distance
   between the strengthening and the base form; is there a proof that
   strict failures force i prime?

## References

- [ErSz78] P. Erdős, G. Szekeres, *Some number theoretic problems on
  binomial coefficients*, Austral. Math. Soc. Gaz. 5 (1978) 97–99.
  (secondary — unreadable from this sandbox; statement taken from the
  problem page and Lean mirror)
- [Be11] G. M. Bergman, *On common divisors of multinomial
  coefficients*, Bull. Aust. Math. Soc. 83 (2011) 138–157. (secondary)
- erdosproblems.com/699 (statement); `teorth/erdosproblems`
  `data/problems.yaml` (status, fetched 2026-08-10);
  `google-deepmind/formal-conjectures`
  `FormalConjectures/ErdosProblems/699.lean` (formal statements,
  fetched 2026-08-10).
- Unpublished forum verification to 10⁷ (secondary, author unknown):
  erdosproblems.com/forum/thread/699, via search snippets, 2026-08-10.
