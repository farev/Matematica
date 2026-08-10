# Session writeup — 2026-08-10 — Erdős #699

The narrative, including everything that went wrong. Results and proofs
live in NOTE.md; labelled tables in README.md.

## Morning: selection

Three scout subagents ran in parallel: one pinned #699's statement and
status from the two maintained mirrors (`teorth/erdosproblems` YAML,
`formal-conjectures` Lean) and found the single prior verification — an
anonymous, unpublished forum sweep to 10⁷ with family checks to
~1.3·10⁸; one swept 5,140 fresh arXiv abstracts (June–Aug 2026) through
a validated RSS mirror and reported the "small open case + certificate"
seam crowded by at least five other AI research operations — with #699
untouched; one cloned the full OEIS corpus into the sandbox (a new
primary channel for this project) and surfaced an octal-game candidate
with measured feasibility but a blocked record table (Flammenkamp), the
same publication-boundary failure mode that has burned this log twice.
Selection went to #699 on novelty position and citation target; the
slate and scoring are in the daily log.

Before selection was final, a 40-line Python prototype had already
reproduced the entire known exception structure below n = 300 in 1.5 s
— including (244, 3, 122), which sits far beyond where hand-checking
would have gone — and cross-validated a big-int gcd path against the
Kummer digit path. That prototype's exception list matching the
forum-reported family structure (fetched independently by the scout)
was the moment the problem stopped looking risky: two unrelated sources
agreeing on a nontrivial invariant (the m-list {2,3,5}, the lone
(28,5,14)) means both the semantics and the sources are solid.

## The engines, and three bugs worth remembering

`brute699.c` (all pairs, per-prime bitsets) swept n ≤ 3000 and
immediately paid for itself twice. First, it found (2048, 2, 713) — an
i = 2 exception *not* in the forum's list (their power-of-2 family
checks apparently reported n = 16 and 512 only below their bound; the
2¹¹ member was sitting in the open). Second, its fourth worker crashed
with a glibc heap-corruption abort: the primes array was allocated with
capacity N/10 + 100, and π(2000) = 303 exceeds 300. A one-line
allocation bug, caught only because it happened to smash the heap
loudly; the three workers that survived were silently within bounds.
Every buffer in every later engine got an explicit capacity assert.

`scan699.c` went through three versions:

- **v1** worked (byte-identical census with the brute force on
  [4, 3000]) but benchmarked slow (39 s per 10⁶ at n ≈ 10⁸), with 11%
  of n escalating to the slow path and two HEAVY give-ups — genuine
  completeness holes — at prime-power-rich n like 10⁸ = 2⁸·5⁸.
- Working the give-ups produced the session's nicest small theorem
  (NOTE L1): level i = 1 can *never* fail, because p^e ∥ n forces
  p^e | j on any dominated j, and all prime powers of n together force
  n | j. The entire level-1 machinery was deleted.
- **v2** switched the CRT moduli to full prime powers (R5) and promptly
  *lost half the census*: the segment sieve now marked each small prime
  at its own position, divided it out of itself, and the primality flag
  `rem == m` failed — every prime ≤ √B was flagged composite, so
  prevprime tracking skipped every n below 59. Caught in seconds
  because re-validation against the brute census is mandatory after any
  engine change: 4 exceptions instead of 8 is unmissable. The
  primality test became "exactly one prime factor, with multiplicity
  one, equal to m".
- Re-reading the filter's necessity proof before trusting v2 exposed a
  subtler hole: the fast filter killed candidate j using *all* odd
  primes of n(n−1), but a level-i failure only implies domination for
  primes > i — a small prime like 3 could veto a candidate that a
  level-5 check must see. No test had caught this (the eight known
  exceptions all escalate for other reasons); it was found only by
  proof-reading the invariant. The filter now uses primes > g(n) only,
  which are in T_i for every relevant level. The lesson from 08-09
  stands: in exhaustive searches the dangerous bugs are the ones that
  produce false NONEXIST, and only proofs or positive controls catch
  them.
- **v3** validated (census match) and benchmarked at 4.3/6.6/9.7 s per
  10⁶ at n ≈ 10⁷/10⁸/10⁹ single-core. The [4, 10⁹) production sweep ran
  as four range chunks on four cores.

The independent auditor `audit699.c` (trial-division factoring, full
j-scans, recorded LCG seeds 699–702) then rediscovered all nine census
triples as positive controls and found nothing at 45 random (n, i)
samples — a third algorithm agreeing with the other two.

## The family theory

The forum's m-list {2,3,5,7,13} for the 3^m+1 family looked like
Mersenne exponents until m = 17 broke the pattern; working the digit
conditions by hand produced Lemma 4 (the cofactor-domination
characterization) and its corollary: both odd parts prime powers ⟹
exception, for odd m. The first scan implementation of the corollary
listed m = 4 as a hit — but n = 82 is *not* exceptional, and tracing
the discrepancy exposed the corollary's even-m caveat (v₂(3⁴−1) = 4
makes the cofactor 16 multi-digit base 5, and 8 = (1,3)₅ is not
dominated). The fixed condition discriminates the data perfectly,
explains *why* 82 escapes, and survived an independent cross-check
built into `families.py`: Lemma 4 evaluated per-prime agrees with the
general level-3 checker at every decided m (the script aborts on any
mismatch; it never fired).

The scan to m = 1400 found no new prime-power hits: under the
sufficient criterion the family is empty from 14 to 1400 — up to
n ≈ 10⁶⁶⁸. The deep run decided every m ≤ 120 except 89 and 119
(uncracked 40+-digit cofactors): failures exactly at {2,3,5,7,13}.

The 2^k family flipped the story. All three known members have 2^k−1
semiprime, and the counting heuristic (|D_P|·|D_Q|/2^{k−1} ≈ 2 per
semiprime exponent) says the alignment event has constant-order
probability per Mersenne-semiprime k — of which infinitely many are
expected. So the two families should have opposite fates: i = 3 finite
(twin repunit-prime events, density 1/m²), i = 2 infinite. The
Erdős–Szekeres *strengthening* is heuristically false as stated, while
the base problem is protected by Lemma 6 (every 2^k level-2 failure is
saved by p = 2). ⟨POW2-DEEP: outcome of the k ≤ 120 run — filled at
close⟩

## Operational failures worth logging

- The first launch of the two deep family runs lost the pow2 lane to a
  shell-precedence mistake (`cd X && (A) & (B) &` runs B in the
  original directory); it died instantly on a missing script path and
  the error surfaced only at the wait. Relaunched with absolute paths.
- Ten processes shared four cores for half an hour (sweep + families +
  audit); nothing broke, but the sweep's wall time roughly doubled
  during the overlap. The 08-07 rule ("heavies sequential") was
  violated knowingly and the cost was paid in wall-clock, not
  correctness.

⟨CLOSE: final timings, the 4·10⁹ extension decision, and end-of-session
state — filled at close⟩
