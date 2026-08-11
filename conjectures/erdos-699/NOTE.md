# Erdős Problem 699: certified verification to 10⁸ and the complete census of Erdős–Szekeres exceptional triples

**Date.** 2026-08-11.  **Status of the problem.** Open (erdosproblems.com
status "falsifiable", 2025-08-31; Lean formalization 2026-01-04).
**AI disclosure.** This note was produced in an AI-assisted research
session (Claude); every proof below is elementary and self-contained,
and every computational claim ships code and data in this directory.

## Abstract

For 1 ≤ i < j ≤ ⌊n/2⌋, Erdős Problem #699 asks whether some prime
p ≥ i divides gcd(C(n,i), C(n,j)); Erdős–Szekeres [ErSz78] conjectured
further that p > i works outside a finite exceptional set of triples.
We verify the p ≥ i statement for all 4 ≤ n ≤ 10⁸ — ten times the
previously public frontier — with two independent coverage engines, an
independent re-verifier, and OEIS-anchored controls, and we certify that
the complete set of exceptional triples for the p > i strengthening in
this range is the nine known triples

  (10,3,5), (16,2,6), (28,3,14), (28,5,14), (244,3,122),
  (512,2,147), (2048,2,713), (2188,3,1094), (1594324,3,797162),

each carrying an independently re-verified certificate.  The dense range
(10⁷, 10⁸] is searched here for the first time.  We prove the elementary
reduction that makes the computation cheap (only "hard rows" i ≤ n −
prevprime(n) at composite n require work), the structural constraints on
exceptions (i prime, witness p = i, i | C(n,i) ⟺ n mod i² < i), a
Mersenne-prime cleanliness criterion, and the digit mechanisms of the two
known exceptional families (n = 2^k at i = 2, n = 3^m+1 at i = 3 with
j = n/2).

## 1. The problem and prior work

**Problem 699** (Erdős–Szekeres; statement as formalized in
[formal-conjectures]): *is it true that for all n and all
1 ≤ i < j ≤ ⌊n/2⌋ there exists a prime p ≥ i with
p | gcd(C(n,i), C(n,j))?*  The **strengthening**: *there is a finite set
E of triples such that for all (n,i,j) ∉ E with 1 ≤ i < j ≤ ⌊n/2⌋ some
prime p > i divides the gcd.*

Context.  Sylvester–Schur (classical; Lean-verified in
[FC-Bench]) gives a prime p > i dividing C(n,i) alone for i ≤ n/2.  That
gcd(C(n,i), C(n,j)) > 1 always is the Erdős–Szekeres common-divisor
theorem from the same 1978 paper (= Erdős Problem #698, quantitative form
proved by Bergman [Be11]).  #699 asks for the *size* of a common prime
factor.  [ErSz78] already exhibited exceptional behavior for the p > i
strengthening; the erdosproblems.com page records (secondary): failures
at i = 2 for certain powers of 2, some at i = 3, and exactly one known
with i ≥ 4, gcd(C(28,5), C(28,14)) = 2³·3³·5.

**Prior computation** (must-cite; found by today's literature pass): an
uncertified Rust scan [CL26] verified the p ≥ i statement for
4 ≤ n ≤ 10⁷ and for the thin families n = 2^k (k ≤ 27) and n = 3^m+1
(m ≤ 17), reporting exactly the nine triples above as the strong-version
failures ("near misses") in its range.  It is a single implementation,
posts no certificates, and stores no per-row witnesses; its committed
scan log is pinned here as `data/prior_art_scan.jsonl` (sha256
`e2f7b858d02c5f7dac4b55383efa99393139aa8b1bc0ff1a2f8c23e30d488af3`).

**This session's contribution.** (1) The first *dense* search of
(10⁷, 10⁸] — 10× range extension.  (2) A certification layer the prior
art lacks: dual independent engines cross-checked row-by-row, a
full-pair reference on small n, an independent Legendre-valuation
re-verifier for every exception, OEIS-anchored controls, and per-triple
certificates.  (3) The reduction and structure lemmas of §2 with proofs,
and the family mechanisms of §4.  (4) The observation table of §5.

Everything attributed to [ErSz78] itself is (secondary): the 1978 paper
(Austral. Math. Soc. Gaz. 5, 97–99) is not readable from this sandbox;
attribution follows Bergman's abstract and the erdosproblems.com page.

## 2. Reduction lemmas

Throughout, p is prime, n ≥ 4, and v_p denotes p-adic valuation.  We use
Kummer's theorem in the following form.

**Criterion K.** p | C(n,k) ⟺ there is t ≥ 1 with
(k mod p^t) > (n mod p^t).

*Proof.* By Kummer, v_p(C(n,k)) is the number of carries when adding k
and n−k in base p, and a carry out of the lowest t digits occurs iff
(k mod p^t) + ((n−k) mod p^t) ≥ p^t.  The left side is ≡ n (mod p^t) and
lies in [0, 2p^t−2], so it equals (n mod p^t) or (n mod p^t) + p^t, the
latter iff (k mod p^t) > (n mod p^t): indeed if (k mod p^t) ≤ (n mod p^t)
then (n−k) mod p^t = (n mod p^t) − (k mod p^t) and the sum is n mod p^t
< p^t; otherwise (n−k) mod p^t = (n mod p^t) − (k mod p^t) + p^t.  ∎

**Lemma 1 (large primes).** If n/2 < p ≤ n and 0 ≤ k ≤ n/2, then
p | C(n,k) ⟺ k > n − p.

*Proof.* n < 2p gives n mod p = n − p; k ≤ n/2 < p gives k mod p = k; so
the t = 1 condition reads k > n − p.  For t ≥ 2, p² > n²/4 ≥ n (n ≥ 4),
so k mod p^t = k ≤ n/2 < n = n mod p^t contributes nothing.  ∎

**Lemma 2 (row reduction).** Let n be composite, q the largest prime
< n, g := n − q.  Then for every pair with g < i < j ≤ ⌊n/2⌋, the prime
q divides both C(n,i) and C(n,j) and satisfies q > j > i.  Hence both
versions of the problem hold at every such pair, and only the "hard
rows" 2 ≤ i ≤ g (paired with all j) remain to be checked (i = 1 is
Lemma 4).

*Proof.* Bertrand's postulate provides a prime in (n/2, n) for composite
n ≥ 4 [take m = ⌈n/2⌉ ≥ 2, a prime p with m < p < 2m; p ≤ n, and p = n
is excluded as n is composite; p > ⌈n/2⌉ ≥ n/2].  Hence q > n/2 ≥
⌊n/2⌋ ≥ j.  By Lemma 1, q | C(n,k) for k ∈ {i, j} ⟺ k > n − q = g.  ∎

**Lemma 3 (prime rows).** If n is prime then n | C(n,k) for all
1 ≤ k ≤ n−1, and p = n > ⌊n/2⌋ ≥ j witnesses every pair at this n, both
versions.

*Proof.* Criterion K at t = 1: k mod n = k > 0 = n mod n.  ∎

**Lemma 4 (i = 1).** For 2 ≤ j ≤ ⌊n/2⌋ let n' = n / gcd(n,j).  Then
n' > 1, n' | C(n,j), and every prime factor p of n' divides
gcd(C(n,1), C(n,j)) with p > 1.  So row i = 1 satisfies both versions.

*Proof.* From j·C(n,j) = n·C(n−1,j−1), n divides j·C(n,j).  With
d = gcd(n,j), n = dn', j = dj', gcd(n',j') = 1: n' | j'·C(n,j), hence
n' | C(n,j).  Since j < n, d < n, so n' ≥ 2.  And C(n,1) = n = dn'.  ∎

**Lemma 5 (hard-row candidates).** Let n be composite, 2 ≤ i ≤ g, and
p > i prime.  Then p | C(n,i) ⟺ p | n(n−1)⋯(n−i+1), and every such p
satisfies p ≤ n/2.

*Proof.* v_p(C(n,i)) = v_p(∏_{r<i}(n−r)) − v_p(i!) and v_p(i!) = 0 for
p > i, giving the equivalence.  Each factor n−r (0 ≤ r < i ≤ g) lies in
(q, n], an interval whose interior contains no primes and whose endpoint
n is composite; so n−r is composite, and a prime factor p of a composite
m satisfies m/p ≥ 2, i.e. p ≤ m/2 ≤ n/2.  ∎

**Lemma 6 (exception structure).** If (n,i,j) satisfies the weak version
but not the strong one, then i is prime and p = i is the *only* prime
p ≥ i dividing gcd(C(n,i), C(n,j)).  Moreover, for i prime,
i | C(n,i) ⟺ n mod i² < i.

*Proof.* Immediate for the first part.  For the criterion, apply K with
k = i: at t = 1, i mod i = 0 exceeds nothing; for t ≥ 2 the condition is
n mod i^t < i, and if it holds for some t ≥ 2 then n mod i² =
(n mod i^t) mod i² = n mod i^t < i, so it holds at t = 2.  ∎

**Lemma 7 (n − 1 prime ⟹ clean row-set).** If n is composite and n−1
prime, then g = 1: there are no hard rows, so no exceptional triple has
this n.  In particular n = 2^k with 2^k − 1 a Mersenne prime carries no
exception — consistent with the observed i = 2 exceptional exponents
k ∈ {4, 9, 11} (2^k−1 = 15, 511, 2047 all composite) and the absence of
k ∈ {2,3,5,7,13,17,19} (Mersenne exponents ≤ 2²⁶ range).  ∎

Lemmas 1–6 are elementary and surely classical in substance — Lemma 1/5
style reasoning is implicit in how [ErSz78] located their examples — but
we could not verify the 1978 paper's contents directly; the write-ups
above are independent.  The computation of §3 relies only on K and on
Lemmas 1–6, each of which is exercised by the control battery.

## 3. The computation

**Algorithm.** Sieve smallest prime factors to N.  For each composite n
(Lemma 3 skips primes) with q, g as above: rows i ∈ [2, min(g, ⌊n/2⌋−1)]
(Lemmas 2, 4).  Per row, the candidate primes are read off the
factorizations of n, n−1, …, n−i+1 (Lemma 5); the sweep subtracts each
candidate's divisibility pattern S_p = {j : p | C(n,j)} (built from
Criterion K layer-by-layer in t) from the uncovered set (i, ⌊n/2⌋],
stopping when empty.  A j left uncovered by all candidates p > i is an
exception candidate; it is then tested against p = i by Lemma 6 (both
i | C(n,i) and i | C(n,j)).  If that also fails, the pair is a weak
counterexample — the falsifying event; none occurred.

**Engines.** Two independent per-row coverage engines: `bitset`
(word-parallel bit array over j) and `interval` (sorted interval-list
subtraction with transactional per-prime semantics and a per-element
filter for small primes; falls back to bitset on pathological rows).
`--engine=both` runs both on every row and reports any disagreement
(`ENGDIFF`) — zero across all dual-engine ranges.

**Tripwire.** Sylvester–Schur guarantees every hard row a nonempty
candidate list; the sweep asserts this (`SSVIOL`) — zero firings.  This
control catches candidate-collection bugs in the dangerous direction
(false NONEXIST of candidates → false exceptions / missed coverage).

**Controls.** (i) A full-pair pure-Python reference (no reduction, both
versions, big-int bitmasks) agrees with a bigint gcd + trial-division
path on [4, 150] and with the C sweep's census on [4, 3000].
(ii) `--engine=both` on all of [4, 10⁶] and on spot slices at 5·10⁷ and
10⁸.  (iii) OEIS anchors reproduced exactly from mirror-pinned `.seq`
files: A129488 (smallest odd prime dividing C(2n,n), 105 terms), A263922
(max exponent in C(2n,n), 87 terms), A030979 (C(2k,k) coprime to 3·5·7,
13 terms ≤ 25000, no extras).  (iv) Record prime gaps: per-chunk maximal
g values against A005250/A002386.  (v) Planted positive control: the
prior art's (1594324, 3, 797162) was never given to this code; the sweep
found it independently.  (vi) Every exception re-verified by
`verify_exceptions.py` — Legendre digit-sum valuations over *all* primes
≤ n, no reduction, no shared code — with a selftest that accepts the 8
small real exceptions and rejects 3 fabricated near-triples.
(vii) Sampled hard rows re-verified by `verify_row.py` (trial-division
factoring, big-int tiling masks, deterministic LCG sampling).

**Scale.** See `data/summary.csv` for per-chunk row counts, exception
counts, maximal gaps and runtimes (4 cores; exact integer arithmetic
throughout; no randomness in the production path).

## 4. The census and the family mechanisms

**Census (CERTIFIED).** On 4 ≤ n ≤ 10⁸ the exceptional triples for the
p > i strengthening are exactly:

| n | i | j | gcd structure | family |
|---|---|---|---|---|
| 10 | 3 | 5 | 2²·3 | n = 3²+1, j = n/2 |
| 16 | 2 | 6 | 2³ | n = 2⁴ |
| 28 | 3 | 14 | 2²·3² | n = 3³+1, j = n/2 |
| 28 | 5 | 14 | 2³·3³·5 | sporadic (i ≥ 4; known to [ErSz78]) |
| 244 | 3 | 122 | 2²·3⁴ | n = 3⁵+1, j = n/2 |
| 512 | 2 | 147 | 2⁴ | n = 2⁹ |
| 2048 | 2 | 713 | 2⁵ | n = 2¹¹ |
| 2188 | 3 | 1094 | 2²·3⁸ | n = 3⁷+1, j = n/2 |
| 1594324 | 3 | 797162 | 2²·3¹⁴ | n = 3¹³+1, j = n/2 |

(gcd structures from the per-triple certificates in `certs/`, each
re-derived independently; for n ≤ 3000 additionally by bigint gcd.)

**Proposition 8 (the n = 3^m+1 family, i = 3, j = n/2).** Let m ≥ 2,
n = 3^m+1, j = (3^m+1)/2.  Then:
(a) the weak witness p = 3 always works at (n,3,j): n ≡ 1 (mod 9) gives
3 | C(n,3) by Lemma 6, and j ≡ 2 > 1 ≡ n (mod 3) gives 3 | C(n,j) by K;
(b) every candidate prime p > 3 (Lemma 5) divides
n(n−1)(n−2) = (3^m+1)·3^m·(3^m−1), hence divides 3^{2m}−1;
(c) for such p the lowest base-p digits never carry: p | 3^m−1 ⟹
j ≡ 1, n ≡ 2 (mod p); p | 3^m+1 ⟹ j ≡ 0, n ≡ 0 (mod p).
So whether (n,3,n/2) is exceptional is decided entirely by the higher
base-p digits of j against n, a per-m finite check that the sweep
certifies: exceptional exactly at m ∈ {2, 3, 5, 7, 13} in the range
covered (m ≤ 16 dense, i.e. n ≤ 10⁸).

*Proof.* (a) 9 | 3^m for m ≥ 2 so n mod 9 = 1 < 3; and 2j = 3^m+1 ≡ 1
(mod 3) gives j ≡ 2 (mod 3) since 2·2 ≡ 1.  (b) Lemma 5 and p ∤ 3.
(c) 2j = 3^m+1; if p | 3^m−1 then 2j ≡ 2, and p odd gives j ≡ 1; the
n-digit is n = (3^m−1) + 2 ≡ 2; since 1 ≤ 2, no t = 1 carry.  If
p | 3^m+1 then 2j ≡ 0 so j ≡ 0 ≤ 0 ≡ n.  ∎

**Proposition 9 (the n = 2^k family, i = 2).** Let n = 2^k, k ≥ 4.
(a) The weak witness p = 2 works at (n,2,j) for every 2 < j ≤ n/2:
n ≡ 0 (mod 4) gives 2 | C(n,2) (Lemma 6), and 0 < j < n gives
2 | C(n,j) (K at the lowest set bit of j).
(b) The candidates are exactly the odd prime factors of the Mersenne
number 2^k−1; each satisfies n ≡ 1 (mod p), so an exceptional j must
have j mod p ∈ {0, 1} for every such p, with the higher digits again a
finite per-k check.  If 2^k−1 is a Mersenne prime, Lemma 7 already
precludes any exception at n.  Certified: exceptional exactly at
k ∈ {4, 9, 11} in the dense range (k ≤ 26).

*Proof.* (a) as in Lemma 6/K.  (b) Lemma 5 with n(n−1) = 2^k(2^k−1);
n = (2^k−1) + 1 ≡ 1 (mod p); a t = 1 carry needs j mod p > 1.  ∎

**The sporadic (28, 5, 14).** Candidates p > 5 dividing 28·27·26·25·24:
{7, 13}.  Base 7: 28 = (4,0)₇, 14 = (2,0)₇ — fits, no carry.  Base 13:
28 = (2,2)₁₃, 14 = (1,1)₁₃ — fits.  Weak witness p = 5:
28 mod 25 = 3 < 5 (Lemma 6) and 14 mod 5 = 4 > 3 = 28 mod 5 (K).  So
gcd(C(28,5), C(28,14)) = 2³·3³·5 has no prime > 5, as [ErSz78] found.  ∎

## 5. Observations and heuristics (not proved)

- **j = n/2 rigidity.** Every i = 3 exception in the census has j = n/2
  exactly; no i = 3 exception occurs at any other j ≤ 10⁸.  Plausible
  mechanism: candidates p | 3^m∓1 exceeding √n have two base-p digits,
  and the top digit of j = n/2 is roughly half that of n, making the
  no-carry condition maximally easy at j = n/2; a proof is open.
- **Kummer-degenerate n.** Every exceptional n has the shape p^a + p^b
  for the witness prime p (2^k = 2^{k-1}+2^{k-1}; 3^m+1 = 3^m+3⁰;
  28 = 3³+1 for both its triples) — the shape that makes n's base-p
  digits tiny.  Compare Wu's criterion [Wu26] for stride-family gcds,
  where the same 2n = p^i + p^j shape controls odd-prime membership.
- **Finiteness heuristic (NUMERICAL).** For n = 2^k the exceptional j
  must Lucas-fit n in every base p | 2^k−1; modelling digits as uniform,
  the expected count of fitting j ≤ n/2 is ≈ (n/2)·∏_p (density_p) with
  density_p ≈ (2/p)·∏_{t≥2}((n mod p^t)+1)/p^t, which decays rapidly in
  the number of distinct Mersenne factors; the observed thinning
  (k = 4, 9, 11 then nothing through k = 26) is consistent.  Same shape
  for i = 3.  This is a heuristic, not a bound: the strengthening's
  finiteness remains open, and anything touching the factor structure of
  2^k−1 is Mersenne-hard.
- **No exception has i ≥ 7**; the single i = 5 triple is at n = 28.
  Whether i ≥ 7 exceptions exist at all is open; Lemma 6 confines any
  such to prime i with n mod i² < i and every prime in
  (i, n/2] ∩ {divisors of the i-term window} Lucas-fitting at some j.

## 6. Open questions

1. Prove the j = n/2 rigidity for i = 3 exceptions (finite-digit
   argument may suffice for candidates > √n; the small candidates are
   the obstruction).
2. Prove finiteness of the i = 2 family assuming standard conjectures on
   the factor structure of Mersenne numbers — or unconditionally for a
   subfamily (e.g. k with a Mersenne factor p > 2^{k/2}: then p has two
   base-p... digits argument closes the row for j > n − ⌊stuff⌋; the
   sweep data suggests which k are closable this way).
3. Extend the dense range to 10⁹ (segmented SPF sieve; ~2.8 μs/row
   measured here makes it a single-session run at ~4 GB memory).
4. The exceptional sequences {10,16,28,244,512,2048,2188,1594324,…} and
   the triple list are not in OEIS (`oeis: N/A` in the database record;
   direct search today) — a natural submission for a *human* to make
   (OEIS forbids AI-generated submissions).

## References

- [ErSz78] P. Erdős, G. Szekeres, *Some number theoretic problems on
  binomial coefficients*, Austral. Math. Soc. Gaz. 5 (1978) 97–99.
  (secondary — paper unreachable from this sandbox; attribution via
  [Be11] and the erdosproblems.com page.)
- [Be11] G. M. Bergman, *On common divisors of multinomial
  coefficients*, Bull. Aust. Math. Soc. 83 (2011) 138–157;
  arXiv:0806.0607.  (secondary — abstract only.)
- [CL26] `conglu1997/erdos_699_rust`, GitHub, run of 2026-01-03; results
  posted to the erdosproblems.com forum thread for #699.  Scan log
  pinned as `data/prior_art_scan.jsonl` (primary artifact, fetched
  2026-08-11).
- [formal-conjectures] google-deepmind/formal-conjectures,
  `FormalConjectures/ErdosProblems/699.lean` (primary, fetched
  2026-08-11).
- [FC-Bench] AllenGrahamHart/FormalConjectures-Bench, Lean proof of
  Sylvester–Schur at `formalizations/erdos699/` (primary, fetched
  2026-08-11 by scout).
- [Wu26] C. W. Wu, *Computing the greatest common divisor of binomial
  coefficients* C(mn, mk), arXiv:2606.20940 (2026).  (secondary —
  via OEIS A265388 citation lines, primary for the citation itself.)
- [Bloom] T. F. Bloom, Erdős Problem #699,
  https://www.erdosproblems.com/699 (secondary — snippets), and
  teorth/erdosproblems `data/problems.yaml` (primary, fetched
  2026-08-11, sha256 `10ab3644…`).
- OEIS A129488, A263922, A030979, A005250, A002386, A091963 — `.seq`
  files fetched from the oeis/oeisdata mirror 2026-08-11, pinned in
  `data/`.
