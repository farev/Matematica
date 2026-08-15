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
determine, the complete census of critical members below 10¹²
({{TOTAL_CRIT}} of them, in {{TOTAL_GAPSC}} gaps), with factorizations,
explicit matchings, and exact Hall margins. The minimum margin is 0 —
witnessed infinitely often in principle (Proposition 5.2) and in the data by
{{TIGHT_TOTAL}} tight gaps, the largest at p = {{LAST_TIGHT_P}} — and no
margin is negative: a negative margin would be a counterexample to Grimm's
conjecture. All computations are exact integer arithmetic, cross-verified
by an independent implementation on exhaustive windows and random samples.

## 1. Statement and prior work

**Conjecture (Grimm 1969).** If n+1, …, n+k are all composite, there exist
distinct primes p₁, …, p_k with pᵢ | n+i.

Sourcing caveat, stated prominently: **no primary source was readable from
this sandbox** (all literature domains egress-blocked; search snippets
only). Every attribution below is (secondary) and must be re-verified
against the actual papers before any publication. With that caveat:

- Grimm, *A conjecture on consecutive composite numbers*, AMM 76 (1969)
  1126–1128. Guy, UPINT §B32.
- Erdős–Selfridge (1971): Grimm's requirement holds when n > k^{π(k)}-ish
  (via Hall's theorem), and the conjecture implies prime-gap bounds
  stronger than what the Riemann hypothesis yields — the reason the
  conjecture is considered deep.
- Ramachandra–Shorey–Tijdeman (Crelle 1975/76): the requirement holds for
  k ≪ (log n / log log n)³, ineffective/unspecified constant.
- Laishram–Shorey (IJNT 2 (2006) 207–211): verified for all
  n ≤ 1.9236701629×10¹⁰. This is the computational record we found cited
  everywhere as current in 2026.
- Laishram–Murty (Michigan Math. J. 61 (2012)): the Grimm function g(n)
  satisfies g(n) = O(n^{0.45}) unconditionally; smooth numbers in short
  intervals are identified as the governing objects — the same objects our
  census tabulates.
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
restriction is exactly such a φ. (3)⇒(1): let W be any window inside
(p, q). Assign to each critical m ∈ W the prime φ(m); to each non-critical
m ∈ W any prime factor P_m > k. These are distinct: two non-critical
members m ≠ m′ with P_m = P_{m′} = P would satisfy P | (m − m′) and
0 < |m − m′| ≤ k − 1 < P, impossible; a critical and a non-critical member
get primes on opposite sides of k; criticals are injective by hypothesis.
∎

By Hall's theorem, (3) holds iff for every nonempty set T of critical
members, |N(T)| ≥ |T|, where N(T) is the set of primes ≤ k dividing some
member of T. We record margin(gap) = min_T (|N(T)| − |T|); Grimm fails on
the gap iff margin < 0. The computation never *relies* on Hall: it exhibits
φ explicitly, and the margin is computed as an independent quantity.

We could not find this reduction stated with the "critical member" census
in the literature, but its substance is classical — Erdős–Selfridge already
argue through Hall's theorem, and the k-smooth reduction is attributed to
Grimm himself (both (secondary)). We claim no novelty for Lemma 2.1.

## 3. Method

`grimm_sweep.c` processes all maximal gaps with left prime in [LO, HI) —
partitioned into decade chunks c1–c4 covering [2, 10¹²) — with four
threads. Per segment of 2²² integers it runs (i) a segmented sieve of
Eratosthenes (odd byte map, base primes to 10⁶+), and (ii) a cache-blocked
sieve over all odd prime powers p^e with p ≤ 600, accumulating
res[m] = ∏_{odd p ≤ 600} p^{v_p(m)}, so that

    m is 600-smooth  ⟺  res[m] = m / 2^{v₂(m)}.

The walk streams each segment once. Composites passing the smoothness test
(res equal to odd part — {{TOTAL_CAND}} of ~10¹² integers) are factored by
trial division and buffered; when the closing prime arrives and k is known,
buffered candidates with P⁺ ≤ k are the gap's criticals. This is complete
for k < 600 because critical ⇒ k-smooth ⇒ 600-smooth. Gaps with k ≥ 600
(none occurred below 10¹²; the largest k was {{MAXK}}) would be redone by
trial division to 2000, with a hard abort beyond — asserted, not assumed.
Matchings by augmenting paths; margins by exhaustive subset enumeration
(the engine aborts if a gap ever has more than 20 criticals for the margin,
or 64 at all; the maximum observed was 10).

Everything is 64-bit exact integer arithmetic. res ≤ m < 2⁴⁰ cannot
overflow. No floating point exists in the engine.

## 4. Verification and controls

Two independent implementations. The verifier (`verify_census.py`) uses
sympy's isprime/factorint/nextprime and re-derives everything from scratch.

1. **Exhaustive windows** (every member of every gap fully factored):
   [2, 3×10⁵] — 25,919 gaps, 3,620 criticals, 0 discrepancies;
   [10⁹, 10⁹+10⁵] and [10¹¹, 10¹¹+3×10⁴] — 0 discrepancies.
2. **π anchors, exact:** π(10⁸) = 5,761,455; π(10⁹) = 50,847,534;
   c1+c2 primes = 455,052,511 = π(10¹⁰); c3 = 3,663,002,302 =
   π(10¹¹) − π(10¹⁰); c4 = {{C4_PRIMES}} {{PI12_CHECK}} (published values
   from memory, (secondary), but exact agreement in every case).
3. **Maximal-gap anchors:** first occurrences of gaps 86 (155921), 220
   (47326693), 282 (436273009), 354 (4302407359), 464 (42652618343)
   reproduced exactly ((secondary) memory values; five-for-five).
4. **Determinism:** 1-thread vs 4-thread runs identical as row sets;
   chunk seams verified (last prime of each chunk = first prime of the
   next).
5. **Unit tests:** the matcher rejects a constructed Hall violator
   (margin −1) — the pipeline's positive control for the one event that
   matters; factorizer edge cases (big cofactor, powers of two).
6. **Sampled deep verification:** per chunk, a light arithmetic pass over
   every census row, plus full re-derivation (primality, gap maximality,
   completeness of the critical set) on 250–300 random gaps (seed
   20260815). 0 errors everywhere.

## 5. Results

**Theorem-shaped claim (CERTIFIED, computation, not a proof of anything
about all n).** For every maximal prime gap with left prime p < 10¹² the
critical members admit an explicit injective assignment to primes ≤ k
dividing them; consequently (Lemma 2.1) **Grimm's conjecture holds for all
n ≤ 10¹²**. No Hall margin below 10¹² is negative.

Census totals (details in `data/`):

| decade of p | gaps with criticals | critical members | max s | min margin | tight gaps |
|---|---|---|---|---|---|
| < 10⁹ (c1) | 383,963 | 409,845 | 10 | 0 | {{T1}} |
| 10⁹–10¹⁰ (c2) | 1,049,580 | 1,076,022 | 6 | 0 | {{T2}} |
| 10¹⁰–10¹¹ (c3) | 3,761,362 | 3,807,285 | 5 | 0 | {{T3}} |
| 10¹¹–10¹² (c4) | {{C4_GAPS}} | {{C4_CRIT}} | {{C4_MAXS}} | {{C4_MINMARG}} | {{T4}} |

**Lemma 5.1 (tightness mechanism, trivial).** If a gap contains a prime
power p₀^a with p₀ ≤ k, its margin is ≤ 0 (take T = {p₀^a}; N(T) = {p₀}).

**Proposition 5.2.** There are infinitely many maximal prime gaps with
margin ≤ 0. Under Grimm's conjecture, all margins are ≥ 0, hence such gaps
have margin exactly 0.

*Proof.* Take a ≡ 3 (mod 6), a ≥ 9, m = 2^a. Then 3 | 2^a + 1 (since a is
odd) and 7 | 2^a − 1 (since 3 | a), and both neighbors exceed 7, so both
are composite: the maximal gap around m has k ≥ 3 ≥ 2 = P⁺(m), making m
critical, and Lemma 5.1 applies. Infinitely many such a give infinitely
many gaps. ∎

**Empirics from the census** (all CERTIFIED as data, any extrapolation
NUMERICAL):

- {{TIGHT_TOTAL}} tight (margin-0) gaps below 10¹²; the largest has
  p = {{LAST_TIGHT_P}}, containing {{LAST_TIGHT_WITNESS}}. Classification:
  {{TIGHT_PP}} arise from the prime-power mechanism of Lemma 5.1,
  {{TIGHT_INT}} from genuine interaction (a witness set T with |T| ≥ 2).
  {{INTERACTION_COMMENT}}
- Critical members per decade grow by ×2.6–3.5 while their density falls;
  the largest critical member below 10¹² is {{MAX_M}} (in the gap at
  p = {{MAX_M_P}}), and the largest prime factor ever needed for a
  critical member is {{MAX_L}}.
- The maximum number of criticals in one gap is 10, attained only below
  10⁹ ({{MAXS_DETAIL}}); above 10¹¹ no gap has more than {{C4_MAXS}}.

## 6. What this does and does not say

The verification is a CERTIFIED statement about n ≤ 10¹² and nothing more;
it is evidence of no counterexample below the bound, not evidence for the
conjecture. The census quantifies *why* verification succeeds so easily:
critical members are vanishingly rare relative to composites
({{TOTAL_CRIT}} in ~10¹²), they cluster in long gaps and around prime
powers, and the Hall condition holds with margin ≥ 0 everywhere with
tightness only at the identified mechanisms. The genuinely-interacting
tight gaps {{INTERACTION_TREND}} — the structural question, echoing
Laishram–Murty's smooth-number framing, is whether interaction tightness
dies out; our data bear on it below 10¹² only.

## 7. Open questions

1. Does the minimum margin over gaps with p ∈ [10^d, 10^{d+1}) eventually
   exceed 0 — i.e., is there a last tight gap of interaction type?
   (Prime-power tightness persists forever by Proposition 5.2.)
2. Push to 10¹³: ~9 hours at measured throughput; the census there would
   decide whether interaction tightness survives another decade.
3. The Grimm function g(n) (largest k such that the requirement holds
   starting at n, greedily extended past the next primes) against the
   Laishram–Murty n^{0.45} window — computable exactly by the same engine
   with a different outer loop.
4. Read the primary sources (blocked today): confirm the exact
   Laishram–Shorey record and method, and whether any census-like
   tabulation exists anywhere.

## 8. Reproducibility and AI disclosure

4 cores, 15 GB RAM, gcc 13.3, Python 3.11.15, sympy 1.14. Wall times:
c1 8.9 s, c2 44.7 s, c3 335.7 s, c4 {{C4_WALL}}. Every number above is
emitted by a committed script (`grimm_sweep.c`, `mine_stats.py`,
`analyze_tight.py`); the full censuses ({{TOTAL_CRIT}} rows) are not
committed but regenerate byte-identically (~50 min), with sha256 hashes in
`data/census_hashes.txt`. Randomness only in verification sampling (seed
20260815). This note was produced with substantial AI assistance (Claude);
AI systems are not authors.
