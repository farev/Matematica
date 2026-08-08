# Session writeup — 2026-08-08 (reciprocal Rado numbers)

The narrative, including what failed. Companion to NOTE.md (results) and
the daily log (selection).

## Why this problem

Two scout subagents mapped the arithmetic-Ramsey exact-value frontier and
four non-SAT directions; the July 2026 Gaiser–Ramezanpour paper stood out
for leaving a named exactness question (is f₂(p^m) = 3k²+1 for odd prime
powers?) at sizes a 4-core sandbox decides in seconds, one month after
publication, with no incumbent certification effort. The checkerboard
no-three-in-line table (Prellberg, May 2026) was the runner-up, declined
for scoop risk (the author is the most active computational player in
that space) and weaker definitional controls. Full slate in the log.

## Semantics under a blocked PDF

Neither paper's PDF was reachable; the definition came from abstract
snippets repeated verbatim across searches. The risk of attacking a
subtly different quantity was retired by theorem-anchored controls
computed before any new claim: f₂(6) = 108 = 3·6² reproduced their
3·2^m theorem exactly (boundary SAT/UNSAT at 107/108), and SAT witnesses
exist at 3k² for k = 3, 5, 7, exactly as their odd-prime-power lower
bound requires. A definition differing anywhere in [1, 3k²] would have
had to conspire to pass all of these.

## What happened, in order

1. Enumerator (exact-rational Egyptian DFS) written twice — Python
   reference and C (`enum.c`) — cross-checked against each other, against
   a Fraction-arithmetic brute force on a (k,n) grid, and against OEIS
   A002966 (147 representations of 1 by five unit fractions, etc.).
2. f₂(2) = 60, f₂(3) = 40 fell in under a second each; f₂(3) already
   refutes sharpness at the smallest odd prime power (40 = 3k²+13, not
   28). Then the k = 6 control, then f₂(4) = 48 (= 3k² exactly — the
   2^m family, covered by neither of their theorems, attains 3k² here
   while k = 2 sits at 60, five times 3k²), then f₂(5) = 80 (= 3k²+5;
   sharpness refuted again, and the surplus is not monotone in k).
3. Three colors: f₃(2) = 3276 (their bound: 32) and f₃(3) = 585 (their
   bound: 189). The k = 2 three-color instance is decided by Cadical in
   ~2 s at n = 5178 — the SAT instances stay trivial far beyond where
   the numbers live; enumeration is the entire cost of this family.
4. The k = 8 wall: full enumeration is hopeless (a 1/16 stripe of the
   n = 200 enumeration did not finish in 90 s; the y = 1 branch alone is
   an Egyptian-fraction census in the tens of millions). Pivot: CEGAR.
   Any subset of solution-clauses that is UNSAT proves the upper bound
   (dropping constraints only helps colorings), and a SAT model is
   believed only after the pristine independent checker accepts it;
   violations become clauses. Seeds: diagonal solutions {y, ky} and all
   solutions with ≤ 3 distinct x-values (weighted DFS over partitions).
   Controls: CEGAR reproduces f₂(4), f₂(5), f₂(6) from ground truth —
   and the seed clauses alone carry every one of those UNSAT proofs,
   at 2–4k clauses against the full encoding's 30k+.
5. Endgame: f₂(7) = 150 (CEGAR; the boundary pair re-derived and its CNF
   sha256 reproduced identically across two runs; witness passed by both
   checkers) and f₂(8) = 192 — Conjecture B's prediction, stated in the
   log before the run, confirmed with a pure three-interval extremal
   witness at 191. f₄(2) > 60000 (verified witness); the n = 150000
   4-color instance was abandoned undecided after ~80 CaDiCaL-minutes.
   k = 9 did not finish its first decide (the complete class check at
   n = 243 is the hardest checker instance yet); k = 10–12 and f₃(4)
   were never launched. The recorded k = 9 prediction (245–246) stays
   untested.

## What failed / mistakes made

- Two `pkill -f` invocations matched their own shell's command line and
  killed the compound command issuing them (exit 144/143). Cost: ~3
  minutes and two garbled control runs, re-run clean. Lesson recorded:
  `pkill -x` on the exact binary name.
- The first control battery ran the full k = 5 enumeration at n = 1810
  (55+ s, timeout) to check a y = 1-only count; the lean rewrite checks
  the OEIS value directly. Cost: ~4 minutes.
- **The k = 7 near-miss, the session's most important failure.** The
  completion check on the backgrounded k = 7 striped enumeration was
  `cat logfile && echo DONE` — which succeeds on a logfile that exists
  but is still empty. The enumeration was still running; the bracketing
  probe loaded the stripe files mid-flight (409,446 of an eventual
  568,105 lines, plus torn-line artifacts) and reported SAT up to
  n = 167 against the incomplete constraint set. "f₂(7) ≥ 168 = 3k²+21"
  went into the draft README and was pushed. The error surfaced only
  because CEGAR — whose UNSAT verdicts are sound by construction (every
  clause is an exactly-verified solution) — reported UNSAT at n = 151,
  contradicting it; a subset of true constraints can never be UNSAT
  where the full set is SAT. Chasing the contradiction (Python re-
  enumeration at n ≤ 60 vs the stripe files: two junk tuples) exposed
  the mid-flight read. The struck claim is corrected in the README; the
  lesson — a SAT verdict is *nothing* without a verified witness, and
  "done" checks must test completion markers, not file existence — is
  exactly why the claim discipline exists. The cap-168 stripe data was
  discarded rather than repaired.
- The full k = 7 enumeration at cap 224, launched before the k = 8 probe
  exposed the enumeration wall, was killed ~35 minutes in once CEGAR
  made it obsolete (two pkill mishaps along the way, below).
- **Concurrent lanes sharing file paths, twice.** (i) Orphaned checker
  subprocesses from killed CEGAR lanes kept running and wrote/read the
  same per-(tag,n) witness paths as their replacements — a live lane
  could in principle have verified a stale coloring. Fixed with
  per-process unique filenames. (ii) Two `--certify-at=150` runs for
  k = 7 overlapped; the older binary-deleting version removed the CNF
  the newer retaining version had just written. Re-run cleanly; the
  second run's CNF sha256 matched the first — the CEGAR run is
  reproducible — and the final artifact set was re-verified from disk.
  Standing rule now: one lane per (r,k) tag, ever; kill commands and
  run commands never share a shell line.
- `verify_witness.py` and `check_class.c` each shipped with a garbled
  block from an editing pass (caught by inspection/compile before any
  use).
- The oracle escalation initially fell back to the slow Python weighted
  search (minutes per round at k = 7-8) — the C weighted enumerator and
  the staged `--dmax` C checker replaced it; k = 8's first full check
  dropped from 20+ Python-minutes to ~15 contended C-minutes, and
  mid-loop rounds to seconds.
- A README claim that f₁(2) = 6 was wrong (1/2 + 1/2 = 1/1 gives
  f₁(2) = 2); caught and fixed within minutes. The searched fingerprint
  "6, 60, 3276" was therefore also slightly wrong; "60, 3276" matches
  nothing indexed either.
- The headline value count was wrong twice ("nine" when it was eight,
  "ten" when it was nine) — fixed against the generated table, which is
  now the only source for that number.
- Stale-module races, twice: lanes launched before a cegar.py patch kept
  executing the old code (the k = 8 lane's certify deleted its CNF under
  the pre-retention rule; an earlier concurrent pair did the same to
  k = 7). Both certificates were regenerated by fresh `--certify-at`
  runs. The pkill self-match happened a fourth time closing the f₄ lane.
  The general lesson, now standing: after editing lane code, kill and
  relaunch every lane, and never put a kill and anything else on one
  shell line.

## Judgment calls a referee should know about

- The Gaiser–Ramezanpour computational table is in a PDF this sandbox
  cannot read. Values here at small k plausibly reproduce entries of
  that table; nothing here assumes otherwise, and the write-up marks
  every such value as a possible rediscovery. The certificates, the
  k ≥ 7 values, and the three/four-color values at this scale are
  claimed as new with the appropriate hedges.
- CEGAR's UNSAT CNFs are subsets of the true constraint set; the .sols
  provenance files list every clause's solution tuple so an auditor can
  re-verify each in exact arithmetic without trusting the generator.
