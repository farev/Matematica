# Session writeup — 2026-08-11 — Erdős Problem 699

The narrative, including what failed.  Companion to NOTE.md (results) and
README.md (tables/reproduction).  Log entry:
`log/2026-08-11-erdos-699.md`.

## How the problem was chosen

The 08-09 session had pre-committed Erdős #699 as its pivot and never
fired it; today's mandate defaulted to an external problem.  Three scout
subagents ran in parallel while I pinned the statement from the Lean
formalization and prototyped: a deep-vet of #699 (statement, history,
scoop check, OEIS), a fresh-arXiv harvester (which brought back the
three-move subtraction-game census as the strongest alternative and a
sharp warning that AI pipelines are strip-mining Zarankiewicz cells), and
an OEIS-mirror recon (controls + the curling-number diversifier).

The deep-vet changed the session's shape.  My plan A — "first recorded
verification bound for #699" — died at 12:05 UTC when the scout surfaced
`conglu1997/erdos_699_rust`: an uncertified Rust scan to 10⁷ from January
2026, posted on the problem's forum, with exactly nine strong-version
failures logged.  Instead of abandoning the problem, the session
re-targeted to what the prior art is not: a *certified*, dual-engine,
independently re-verified computation, a 10× dense-range extension to
10⁸, per-triple certificates, and the lemma scaffolding written up
properly.  The prior art became an asset: its ninth triple
(1594324, 3, 797162), which my code had never seen, was designated a
planted positive control — my sweep had to find it on its own or the
session would have halted with an engine bug.  (It found it, ~40 s into
the 10⁶–4·10⁷ chunk.)

## What was built

Everything lives in this directory and is exact-integer end to end:

- `proto.py` — full-pair Python reference (no reduction lemmas), plus a
  third path (bigint gcds via `math.comb`, factored by trial division)
  it cross-checks itself against on [4, 150].
- `sweep.c` — the production verifier.  Reduction: primes are trivial
  rows (p = n); composite n reduce to "hard rows" i ≤ n − prevprime(n)
  (largest-prime witness, Bertrand); i = 1 is classical.  Hard-row
  candidates are read off SPF factorizations (primes > i dividing the
  i-term falling window).  Two independent coverage engines — bitset and
  transactional interval-list — run either singly or both-and-compared
  per row (`ENGDIFF` tripwire), with a Sylvester–Schur nonemptiness
  assert (`SSVIOL`) on every row.
- `verify_exceptions.py` — independent re-verifier for exceptional
  triples: Legendre digit-sum valuations over *all* primes ≤ n, no
  reduction, no shared code; selftest with positive and negative
  controls.
- `verify_row.py` — independent hard-row re-verifier (trial-division
  factoring, big-int tiling masks) for deterministic spot samples.
- `oeis_controls.py` — the carry/valuation machinery against pinned
  OEIS mirror data (A129488, A263922, A030979).
- `check_summaries.py` — chunk tiling, weakfail scan, and the
  record-prime-gap control (A005250/A002386).
- `make_certs.py` — per-triple certificates (weak witness, complete
  candidate list with per-prime no-carry digit tables, gcd
  factorization, bigint confirmation where feasible).

## What failed, in order

1. **Interval-engine transactional bug (caught in review, before any
   run).**  The first draft ping-ponged the interval list through two
   scratch buffers *in place*; an overflow abort after an even number of
   layers would have left the caller's list half-subtracted — silently
   wrong coverage, the false-EXC/missed-EXC direction.  Rewritten to
   copy-in/copy-out per prime: overflow now leaves the list untouched
   and defers that prime to the per-element filter.  This is the
   session's standing lesson: set-difference engines must be
   transactional per subtrahend, because partial subtraction is not
   conservative in either direction.
2. **OEIS offset bug in a control (caught by the control itself).**  The
   A129488 check crashed with StopIteration on n = 1: C(2,1) = 2 has no
   odd prime factor at all — the sequence's offset is 2, which I had not
   read from the %O line.  Control-script bug, not engine bug, but it
   would have "passed" silently had the offset shifted values instead of
   crashing.  Offsets are data.
3. **Launcher double-background.**  Worker 1 was started as a background
   compound *containing* `&`, so the wrapper exited immediately, timing
   went to an empty file, and the sweep ran detached.  Adopted via ps;
   harmless here, but a shell habit worth killing: a detached child that
   died would have silently truncated the range, and only the
   chunk-tiling control would have caught it.
4. **Guessed numbers in a draft table (caught by a control).**  While
   the production run was in flight I drafted the NOTE's census table
   with gcd exponents written from memory — 2⁴ at n = 512 where the
   truth is 2⁸, 3⁸ at 2188 where it is 3⁶.  `make_certs.py`'s bigint
   cross-check exposed all four wrong entries the moment it ran.  The
   rule this repository already has — every number in a note has a
   script that emits it — exists precisely because in-flight drafting
   invites this; the table now carries the certificate values and a
   note of the correction.
5. **Quadratic tiling in the row verifier (caught by the clock).**
   `verify_row.py` originally built its big-int divisibility masks with
   an arithmetic-division tiling trick that is linear for small periods
   but quadratic for mid-size ones; at n ≈ 10⁸ a single row would have
   taken hours, and the 12-row production sample sat silent for 15
   minutes before I killed it.  Rewritten with shift-or doubling (still
   pure Python big-ints, still no shared code with the C engines): the
   same 12 rows then verified in 7.7 s.  The rewritten verifier was
   re-validated on all seven exception rows before the sample re-ran.
6. **Not attempted, by decision:** proving finiteness of the i = 2
   exceptional family.  It is equivalent to a Lucas-avoidance statement
   over the factor structures of Mersenne composites 2^k − 1; after an
   hour of digit games it was clear this is Mersenne-hard, and the
   session's value was in the certified census, not in a doomed proof
   attempt.  Recorded as an open question with the heuristic in NOTE §5.

## What the computation showed

See NOTE §3–§5 and README for the numbers.  The short version: the weak
version of #699 holds to 10⁸ with no counterexample; the strengthening's
exceptional set does not grow between 1,594,324 and 10⁸ — the census is
exactly the nine known triples, now each carrying an independent
certificate; the two exceptional families obey clean digit mechanisms
(Propositions 8–9), the Mersenne-prime criterion (Lemma 7) explains
which powers of two can even be candidates, and every exceptional n has
the Kummer-degenerate shape p^a + p^b.  The j = n/2 rigidity at i = 3
and the finiteness of the families remain open — the honest boundary of
the day.

## Accounting

Selection (scouts + prototype + controls) ≈ 35 min wall; engine build +
validation ≈ 25 min; production sweep [4, 10⁸] on 4 cores ≈ see
`data/summary.csv`; verification layer + certificates ≈ 20 min;
documentation the rest.  Hardware: 4 cores, 15 GB RAM, gcc 13.3.0,
Python 3.11.15.  No floating point in any critical path; no randomness
in any production path (the row-sample LCG seed 20260811 is recorded).
