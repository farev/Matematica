# Grimm's conjecture below 10¹²: certified verification and a census of critical intervals

**Session 1, 2026-08-15.** Research note. AI assistance (Claude) is used
throughout this repository and disclosed in every note; see §8.

## Abstract

Grimm's conjecture (1969) asserts that for every run of consecutive
composite numbers n+1, …, n+k one can choose distinct primes p₁, …, p_k
with pᵢ | n+i. We verify the conjecture for all n ≤ 10¹², extending the
computational record of Laishram–Shorey (2006; n ≤ 1.9236701629×10¹⁰,
(secondary)) by a factor of 52. The verification is organized around the
*critical members* of each maximal prime gap — members with no prime factor
exceeding the gap length k — via the classical reduction: Grimm holds on a
gap iff its critical members admit an injective assignment to primes ≤ k
dividing them. We tabulate, for the first time as far as we could
determine, the complete census of critical members below 10¹² — there are
18,575,022 of them, in 18,400,995 gaps — with factorizations, explicit
matchings, and exact Hall margins. No margin is negative (a negative margin
would be a counterexample to Grimm's conjecture). The minimum margin, 0,
occurs in exactly 133 gaps below 10¹², and every one of them is tight for
the same reason: it contains a prime power p^a with p ≤ k (Lemma 5.1); the
genuinely combinatorial way to be tight — several critical members
competing for a too-small pool of primes — never occurs below 10¹². Such
prime-power tight gaps occur infinitely often (Proposition 5.2); the
largest below 10¹² contains 31⁸. All computations are exact integer
arithmetic, cross-verified by an independent implementation on exhaustive
windows and random samples.

## 1. Statement and prior work

**Conjecture (Grimm 1969).** If n+1, …, n+k are all composite, there exist
distinct primes p₁, …, p_k with pᵢ | n+i.

Sourcing caveat, stated prominently: **no primary source was readable from
this sandbox** (all literature domains egress-blocked; search snippets
only). Every attribution below is (secondary) and must be re-verified
against the actual papers before any publication. With that caveat:

- Grimm, *A conjecture on consecutive composite numbers*, AMM 76 (1969)
  1126–1128. Guy, UPINT §B32.
- Erdős–Selfridge (1971): the requirement holds when the run starts above
  k^{π(k)}-type thresholds (proved via Hall's theorem), and the conjecture
  implies prime-gap bounds stronger than what the Riemann hypothesis
  yields — the reason it is considered deep.
- Ramachandra–Shorey–Tijdeman (Crelle 1975/76): the requirement holds for
  k ≪ (log n / log log n)³, constant unspecified in the sources we could
  see.
- Laishram–Shorey (IJNT 2 (2006) 207–211): verified for all
  n ≤ 1.9236701629×10¹⁰. Cited as the current record in every 2026 source
  we found; two dedicated searches for anything larger found nothing.
- Laishram–Murty (Michigan Math. J. 61 (2012)): the Grimm function g(n) is
  O(n^{0.45}) unconditionally; smooth numbers in short intervals are
  identified as the governing objects — the same objects our census
  tabulates.
- No theorem on record converts the prime-gap tables (verified to 4×10¹⁸)
  into a Grimm verification: with constant 1, the RST bound gives ≈ 1404 at
  the largest gap below 4×10¹⁸ (1476 composites), which is not enough. The
  range (1.9×10¹⁰, 10¹²] handled here is therefore genuinely new territory
  as far as we could determine (absence-of-evidence, (secondary)).

## 2. The reduction

Fix consecutive primes p < q, k = q − p − 1 ≥ 1. Write P⁺(m) for the
largest prime factor.

**Definition.** m ∈ (p, q) is *critical* if P⁺(m) ≤ k.

**Lemma 2.1 (reduction; classical in substance).** The following are
equivalent:

1. every window of consecutive composites contained in (p, q) satisfies
   Grimm's requirement;
2. the full window p+1, …, q−1 satisfies it;
3. there is an injection φ from the critical members of (p, q) into the
   primes ≤ k, with φ(m) | m for every critical m.

*Proof.* (1)⇒(2) is trivial. (2)⇒(3): restrict a system of distinct prime
representatives to the critical members; each representative divides its
member, and every prime factor of a critical member is ≤ k, so the
restriction is such a φ. (3)⇒(1): let W be any window inside (p, q).
Assign to each critical m ∈ W the prime φ(m); to each non-critical m ∈ W
any prime factor P_m > k. These choices are distinct: two non-critical
members m ≠ m′ with P_m = P_{m′} = P would give P | (m − m′) with
0 < |m − m′| ≤ k − 1 < P, impossible; a critical and a non-critical member
receive primes on opposite sides of k; the criticals are injective by
hypothesis. ∎

By Hall's theorem, (3) holds iff |N(T)| ≥ |T| for every nonempty set T of
critical members, where N(T) is the set of primes ≤ k dividing some member
of T. We record margin(gap) = min_T (|N(T)| − |T|); Grimm fails on the gap
iff margin < 0. The computation never *relies* on Hall: it exhibits φ
explicitly, and the margin is computed as an independent quantity.

We could not find this reduction stated together with a census of critical
members in the literature, but its substance is classical — Erdős–Selfridge
already argue through Hall's theorem, and the k-smooth reduction goes back
to Grimm (both (secondary)). We claim no novelty for Lemma 2.1.

## 3. Method

`grimm_sweep.c` processes all maximal gaps with left prime in [LO, HI) —
partitioned into decade chunks c1–c4 covering [2, 10¹²) — with four
threads. Per segment of 2²² integers it runs (i) a segmented sieve of
Eratosthenes (odd byte map, base primes to ~10⁶), and (ii) a cache-blocked
sieve over all odd prime powers p^e with p ≤ 600, accumulating
res[m] = ∏_{odd p ≤ 600} p^{v_p(m)}, so that

    m is 600-smooth  ⟺  res[m] = m / 2^{v₂(m)}.

The walk streams each segment once. Composites passing the smoothness test
(3,108,745,548 of ~10¹² integers) are factored by trial division and
buffered; when the closing prime arrives and k is known, buffered
candidates with P⁺ ≤ k are the gap's criticals. This is complete for
k < 600 because critical ⇒ k-smooth ⇒ 600-smooth. Gaps with k ≥ 600 would
be redone by trial division to 2000, with a hard abort beyond — asserted at
runtime, not assumed; neither path ever triggered, the largest gap below
10¹² having k = 539 (after 738832927927). Matchings are found by
augmenting paths; margins by exhaustive subset enumeration (aborts if a
gap ever exceeded 20 criticals; the maximum observed was 10).

Everything is 64-bit exact integer arithmetic; res ≤ m < 2⁴⁰ cannot
overflow. No floating point exists in the engine.

## 4. Verification and controls

Two independent implementations. The verifier (`verify_census.py`) uses
sympy's isprime/factorint/nextprime and re-derives everything from scratch.

1. **Exhaustive windows** (every member of every gap fully factored):
   [2, 3×10⁵] — 25,919 gaps, 3,620 criticals, 0 discrepancies;
   [10⁹, 10⁹+10⁵] and [10¹¹, 10¹¹+3×10⁴] — 0 discrepancies.
2. **π anchors, exact:** π(10⁸) = 5,761,455; π(10⁹) = 50,847,534;
   c1+c2 = 455,052,511 = π(10¹⁰); c3 = 3,663,002,302 = π(10¹¹) − π(10¹⁰);
   c4 = 33,489,857,205 = π(10¹²) − π(10¹¹); total 37,607,912,018 = π(10¹²)
   (published values from memory, (secondary), but exact agreement in all
   five cases).
3. **Maximal-gap anchors:** first occurrences of gaps 86 (155921), 220
   (47326693), 282 (436273009), 354 (4302407359), 464 (42652618343), and
   the largest below 10¹², 540 (738832927927), reproduced exactly
   ((secondary) memory values; six-for-six).
4. **Determinism and seams:** 1-thread vs 4-thread runs identical as row
   sets; the four chunks agree at their seams (last closing prime of each
   equals the first prime of the next: 1000000007, 10000000019,
   100000000003).
5. **Unit tests:** the matcher rejects a constructed Hall violator
   (margin −1) — the positive control for the one event that matters;
   factorizer edge cases (big cofactor, powers of two).
6. **Sampled deep verification:** per chunk, a light arithmetic pass over
   every census row (18.6M rows), plus full re-derivation (primality, gap
   maximality, completeness of the critical set) on 250–300 random gaps
   per chunk (seed 20260815). 0 errors everywhere.

## 5. Results

**Main claim (CERTIFIED — a statement about the range computed, not
beyond).** For every maximal prime gap with left prime p < 10¹² the
critical members admit an explicit injective assignment to primes ≤ k
dividing them; consequently (Lemma 2.1) **Grimm's conjecture holds for all
n ≤ 10¹²**. No Hall margin below 10¹² is negative.

Census totals (`data/stats_by_decade.csv`; decade d means
10^d ≤ p < 10^{d+1}):

| decade | gaps with criticals | critical members | max s | tight gaps |
|---|---|---|---|---|
| ≤ 8 (i.e. p < 10⁹) | 383,963 | 409,845 | 10 | 83 |
| 9 | 1,049,580 | 1,076,022 | 6 | 15 |
| 10 | 3,761,362 | 3,807,285 | 5 | 17 |
| 11 | 13,206,090 | 13,281,870 | 4 | 18 |
| **total** | **18,400,995** | **18,575,022** | **10** | **133** |

**Lemma 5.1 (tightness mechanism, trivial).** If a gap contains a prime
power p₀^a (a ≥ 2) with p₀ ≤ k, its margin is ≤ 0: take T = {p₀^a}, so
N(T) = {p₀}.

**Proposition 5.2.** There are infinitely many maximal prime gaps with
margin ≤ 0. Under Grimm's conjecture all margins are ≥ 0, so these gaps
have margin exactly 0.

*Proof.* Take a ≡ 3 (mod 6), a ≥ 9, m = 2^a. Then 3 | 2^a + 1 (a odd) and
7 | 2^a − 1 (3 | a), and both neighbors exceed 7, so both are composite:
the maximal gap around m has k ≥ 3 ≥ 2 = P⁺(m), so m is critical and
Lemma 5.1 applies. Distinct large a give distinct gaps. ∎

**Empirics from the census** (CERTIFIED as data; any extrapolation beyond
10¹² is NUMERICAL):

- **Every tight gap below 10¹² is prime-power tight.** All 133 margin-0
  gaps contain a prime power p^a with p ≤ k achieving the minimum as a
  singleton; a genuinely interacting witness set (|T| ≥ 2 criticals
  competing for |T| primes) achieves the minimum in **zero** gaps
  (`analyze_tight.py`). Tight gaps arrive at a roughly constant rate
  (9–18 per decade) exactly as the prime-power mechanism predicts.
- The ten largest tight gaps are tight at, respectively: 31⁸, 3²⁵, 97⁶,
  5¹⁷, 7¹⁴, 2³⁹, 29⁸, 19⁹, 11¹¹, 3²⁴. The largest, at
  p = 852,891,037,337 (k = 109), contains 31⁸ = 852,891,037,441. That 31⁸
  and 97⁶ are critical at all is a small coincidence — each needed its
  local gap to be unusually long (k ≥ 31, resp. ≥ 97), and both were.
- Critical members grow ~×3.5 per decade in count while their density
  falls ~×2.9 per decade; smooth candidates (600-smooth composites) number
  3,108,745,548 below 10¹², of which 18,575,022 (0.6%) are critical for
  their own gap.
- The largest critical member below 10¹² is 10¹² itself
  (= 2¹²·5¹², P⁺ = 5), a member of the 49-composite gap after
  999,999,999,989. The largest prime factor a critical member ever has is
  521 (m = 614,487,453,811 = 7·11·139·263·419·521, six distinct primes all
  at most its gap's k = 533, in the 533-gap after 614,487,453,523).
- The busiest gap below 10¹² is the 72-gap after 31397: ten critical
  members, matched to {2,3,5,7,13,17,19,41,43,67}, margin 1. Above 10¹¹
  no gap has more than 4.

## 6. What this does and does not say

The verification is a CERTIFIED statement about n ≤ 10¹² and nothing more:
evidence that no counterexample lives below the bound, not evidence for
the conjecture. The census quantifies *why* verification succeeds so
easily, in Laishram–Murty's smooth-number terms: critical members are
vanishingly rare (18.6M in a trillion), they concentrate in unusually long
gaps and at prime powers, and Hall's condition holds with slack everywhere
except at the 133 prime-power tight gaps, where the slack is exactly zero
for the trivial reason. The sharp structural fact is negative:
**interaction tightness — the only mechanism by which Grimm's conjecture
could actually fail — never once occurs below 10¹².** Two k-smooth numbers
whose prime supports pack into too few primes would have to sit in the
same short window; that this never happens in range is consistent with
(and quantifies) the heuristic that smooth numbers in short intervals are
too sparse to collide, which is exactly the regime the Laishram–Murty
bound g(n) = O(n^{0.45}) lives in ((secondary); their paper was not
readable today).

## 7. Open questions

1. Does interaction tightness (margin 0 forced by |T| ≥ 2) *ever* occur?
   Below 10¹² the answer is no. A heuristic via Tijdeman-type gaps between
   S-smooth numbers suggests it should die out entirely for large n
   ((secondary), unverified against the actual theorems today) — but small
   heights are not large n, and a first occurrence would be a lovely
   object.
2. Push to 10¹³: ~9 hours at measured throughput (2.8 s per 10⁹ per 4
   cores); decides whether the tight-gap rate stays ~constant and whether
   interaction tightness appears.
3. The Grimm function g(n) against the Laishram–Murty n^{0.45} window —
   computable exactly by the same engine with a different outer loop.
4. Read the primary sources (blocked today): confirm the exact
   Laishram–Shorey record and method; check whether any census-like
   tabulation exists anywhere.

## 8. Reproducibility and AI disclosure

4 cores, 15 GB RAM, gcc 13.3, Python 3.11.15, sympy 1.14. Wall times:
c1 8.9 s, c2 44.7 s, c3 335.7 s, c4 2736.2 s — 52.1 minutes for the full
range. Every number above is emitted by a committed script
(`grimm_sweep.c`, `mine_stats.py`, `analyze_tight.py`); the full censuses
(18,575,022 rows, ~940 MB) are not committed but regenerate
deterministically in ~52 minutes (`run_production.sh`), with sha256 hashes
committed in `data/census_hashes.txt`. Randomness only in verification
sampling (seed 20260815). This note was produced with substantial AI
assistance (Claude); AI systems are not authors.
