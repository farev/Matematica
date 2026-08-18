# Session writeup — 2026-08-15 (Grimm's conjecture, session 1)

The session narrative, including what failed. The polished statements are in
[NOTE.md](NOTE.md); the labelled claims in [README.md](README.md).

## How Grimm was chosen

The scheduled mandate: survey outside the repository, pick three external
candidates, and only work an internal thread if it clearly beats all three.
Network reality shaped everything: every literature site (arxiv, oeis,
erdosproblems, mathoverflow) was egress-blocked; only search-snippet access
worked. Three research agents vetted candidates in parallel (number theory /
combinatorics on words / additive combinatorics + Ramsey), a fourth swept
the repo's own threads.

The slate that survived vetting: Grimm's conjecture (verification record
untouched since 2006, corner inactive, compute fully deterministic);
URT(22) = 21/20 (clean next case of Currie–Mol, but the construction family
lives in an unreadable paper); Ruzsa numbers past m = 100 (extends a June
2026 paper, but an active group owns the tooling and the adjacent novelty
check needs an unreadable Math. Comp. paper). Rejected with evidence:
peaceable queens a(16) (eight years open under MIP/SAT fire), queens
domination γ(Q₂₆), w(2;3,20) (~196 CPU-years reported for the previous
case), balanced-sequence RTB(13), abelian ART(11).

The internal runner-up was generalized-schur's (4,4,u) ladder — unblocked
by the 08-08 disk-streaming Glucose. It lost on predictability: its one
decisive instance had already eaten 15 GB of proof RAM once, while Grimm's
compute is a sieve whose cost was measured in-session before committing.
Ties go to the new problem anyway. The (4,4,10)/(3,3,12) boundary CNFs were
generated and cross-validated during the survey phase and are parked for a
future session (nothing solved today).

A cautionary find during vetting: a search-engine AI summary asserted
"S(3;4,4,10) = 109 was computed in a 2026 paper" — with wrong supporting
arithmetic, and almost certainly echoing this repository's own public page,
which *predicts* 109. When your own conjecture page can come back at you
through a search summary wearing a "computed in the literature" costume,
snippet evidence deserves systematic distrust. Everything cited today is
marked (secondary).

## What was built

`grimm_sweep.c`: 4-thread segmented sieve; alongside primality, a
cache-blocked sieve over odd prime powers ≤ 600 accumulates every integer's
odd smooth part, so "no prime factor above the gap length" is decided
exactly (fast path k < 600, trial-division slow path to 2000, dynamic
aborts beyond — never triggered). Criticals are matched to primes ≤ k by
augmenting paths; exact Hall margins by subset enumeration (s ≤ 20 always
in practice; max seen was 10).

**Bug caught before it could bite.** The first draft consulted the
smooth-part array of the *current* segment while closing gaps — but a gap
can span a segment boundary, where those entries belong to the next segment
(the array is recycled). Caught in code review before any run; the fix
(buffer candidates as the walk streams them, decide criticality only when
the closing prime fixes k) is also structurally simpler. Lesson repeated
from earlier sessions: segment-boundary state is where sieve bugs live.

## Controls (all green before production)

- Unit tests: matcher accepts a matchable instance with distinct
  assignments, rejects a constructed Hall violator (3 members over {2,3})
  with margin −1; factorizer handles big-cofactor refusal and powers of 2.
- Exhaustive cross-checks against an independent sympy implementation
  (different algorithm: factor *every* member of *every* gap): [2, 3×10⁵]
  — 25,919 gaps, 3,620 criticals, 0 errors; [10⁹, 10⁹+10⁵] — 0 errors;
  [10¹¹, 10¹¹+3×10⁴] — 0 errors.
- π anchors exact: π(10⁸) = 5,761,455; π(10⁹) = 50,847,534; π(10¹⁰) =
  455,052,511 (c1+c2 additivity). Maximal-gap anchors reproduced: 86 after
  155921; 220 after 47326693; 282 after 436273009; 354 after 4302407359
  (anchor values from memory, (secondary), but four-for-four agreement).
- Determinism: 1-thread and 4-thread runs of [2, 10⁸] byte-identical as
  row sets; identical histograms and prime counts.
- Sampled deep verification of finished chunks: c1 and c2 light-passed on
  all 1,485,867 rows and heavy-passed (primality, gap maximality, full
  refactorization, completeness) on 300 sampled gaps each, 0 errors.

## The runs

Recorded in `data/c*.summary.txt` (wall clock, per-thread seconds, 4 threads
on a 4-core/15 GB sandbox):

- c1 [2, 10⁹): 8.9 s. 409,845 criticals in 383,963 gaps; max s = 10 (the
  72-gap after 31397: ten criticals, matched with {2,3,5,7,13,17,19,41,43,
  67}, margin 1).
- c2 [10⁹, 10¹⁰): 44.7 s. 1,076,022 criticals; min margin 0; the 354-gap
  at 4302407359 reproduced.
- c3 [10¹⁰, 10¹¹): 335.7 s. 3,807,285 criticals in 3,761,362 gaps; max
  s = 5; the 464-gap at 42652618343 reproduced; prime count = π(10¹¹) −
  π(10¹⁰) exactly.
- c4 [10¹¹, 10¹²): 2736.2 s. 13,281,870 criticals in 13,206,090 gaps; max
  s = 4; min margin 0; the largest gap below 10¹² (k = 539 after
  738832927927) reproduced, and it contains a critical member; prime count
  = π(10¹²) − π(10¹¹) exactly.

Post-run: seams verified across all four chunks; light verification pass
over all 18,575,022 rows and heavy sympy re-derivation of 250–300 sampled
gaps per chunk — zero errors anywhere; mining and tight-gap classification
(below).

## The tight gaps

All 133 margin-0 gaps below 10¹² are prime-power tight — the minimum is
achieved by a singleton prime power in every single one; no gap anywhere in
range is tight (or negative) through genuine interaction of several
criticals. The ten largest tight gaps are tight at 31⁸, 3²⁵, 97⁶, 5¹⁷,
7¹⁴, 2³⁹, 29⁸, 19⁹, 11¹¹, 3²⁴. Two pre-data predictions made from the
mechanism (before c4 finished): that 3²⁵ = 847,288,609,443 would be tight,
and that the last tight gap below 10¹² would be 31⁸ if its local gap
reached k ≥ 31 — both confirmed (31⁸ sits in a k = 109 gap). The rate of
tight gaps per decade (9–18) is roughly constant, as the prime-power
mechanism predicts.

## What failed / what surprised

- `mine_stats.py` first crashed on a name-shadowing bug (`dec` as both
  function and dict) that my own post-chain surfaced; fixed and rerun —
  the kind of bug the census pipeline can afford, since it only mines
  already-verified data.
- An LLM-typical hallucination was caught in review: a draft NOTE line
  invented a factorization (with a stray CJK character) for the max-L
  member 614,487,453,811; the real factorization (7·11·139·263·419·521)
  was computed and substituted. Every specific number in the final NOTE
  either comes from a data file or was recomputed explicitly.
- Criticals turned out ~30× more numerous than the back-of-envelope
  Dickman estimate made during selection (10⁵ predicted; 1.5M already below
  10¹⁰). The error: the estimate integrated only mid-length gaps and
  ignored that every prime power of a tiny base is critical wherever it
  lands, plus the full weight of ordinary-length gaps at low heights.
  Harmless for feasibility, fatal for the "commit the whole census"
  plan — hence the mined artifacts + hash manifest.

## AI assistance

This session was run by an AI assistant (Claude) end to end — survey,
selection, code, runs, verification, and prose — under the repository's
claim discipline. Every computational claim ships code and is
double-implemented or anchor-checked as described above.
