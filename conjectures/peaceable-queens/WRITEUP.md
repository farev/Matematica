# Session narrative — 2026-08-17

The target was picked from a three-candidate external slate (see
`log/2026-08-17-peaceable-queens.md` for the slate and scoring): decide
a(16) of OEIS A250000, with a certified re-derivation of the known
ladder as the floor deliverable.

## Act 1: the SAT plan, and how it died

The plan looked clean: the repo already had a validated DRUP checker
(`tools/satcert`), apt had cadical, and a direct CNF encoding of the
problem is small (2n² cell variables, pairwise line-exclusion clauses,
sequential-counter cardinality). The encoder's first version had a
genuine soundness bug — no same-cell exclusion, so the solver stacked
both colors on one 5-queens solution and "achieved" m = 5 at n = 5.
The independently written witness checker was what caught it. Fixed,
the pipeline reproduced a(3)..a(8) with DRUP-verified proofs at each
boundary.

Then the wall: UNSAT time grew ~12–20× per rung (n = 7: 2 s, n = 8:
46 s). Extrapolation put n = 13 at CPU-months and n = 16 at geological
time. Two structural fixes were tried:

1. **Line-labeling encoding** (94 core variables at n = 16 instead of
   512): barely helped (1.7 s vs 2.0 s at n = 7). CDCL still has to
   *count*, and resolution is weak at counting.
2. **Counting cuts** (product bound and diagonal-capacity bounds as
   CNF over unary counters, each cut a proved lemma): no help at the
   near-optimal m where it matters (38 s at n = 8, m = 10), and — the
   diagnostic experiment — even far-from-optimal instances stayed hard:
   n = 16, m = 64, where a one-line counting argument (RW·CW ≥ 64 and
   (16−RW)(16−CW) ≥ 64 forces RW = CW = 8) collapses the space, took
   cadical past a 240 s timeout. The solver re-proves the
   diagonal-span overlap argument separately for every row/column
   subset pair; learned clauses do not generalize across subsets.

That killed pure SAT for n = 16 at any m — mid-session checkpoint,
invoked with data.

## Act 2: the branch-and-bound that the reformulation wanted

The line-labeling view (NOTE Lemma 1) is not just a smaller encoding;
it is a search space a bespoke exact solver can walk directly: choose
white rows, white columns, then DFS over the two diagonal families with
three cheap exact bounds (product, cell, family-sum — NOTE Lemmas 3–5).
A ~200-line Python reference got a(8)'s boundary from 46 s (SAT) to
2.3 s; the C port took it to 0.02 s with node-for-node identical
counts. The ladder then fell in sequence — a(13)'s refutation (the last
ILP-confirmed value) in 99 s / 478M nodes, a(14) and a(15) (values
reported known, provenance unclear) in minutes on 4 cores.

The one real bug of Act 2 was caught, again, by the independent
checker: the first witness extractor read the live-cell sets *after*
the DFS had unwound (kills are undone on backtrack), so the "witness"
at n = 11 was the full candidate grids — 90 attacking pairs. The
verdicts were unaffected (they had been separately validated against
the SAT engine on 40 instances), but it is exactly the class of bug
that turns a true theorem into a false artifact, and it is why the
checker shares no code with the search. Fixed by snapshotting at the
SAT leaf; every witness re-verified.

## Act 3: n = 16

The plan at 16 was a bracket walk-down — every completed UNSAT at army
size m is a permanent bound a(16) ≤ m − 1, resumable across sessions —
with the m = 38 decision as the stretch goal. Three things made the
stretch goal land the same afternoon:

1. The witness at 37 came almost free: the plain engine found a 37+37
   placement in 29 s (177M nodes), with the classic four-triangle
   structure, and the checker passed it. So the lower half of
   a(16) = 37 was in hand before lunch, independent of Ainley.
2. The full-group canonicalization (SYM16: D4 × color swap acting on
   the row/column sets, Lemma 6′) bought the predicted ~8×: validated
   16/16 against the plain engine on the whole ladder, then a(15)'s
   refutation went from an 8.5-minute-and-counting plain run to 156 s.
3. Chunking the outer loop (16 stride pieces, each a file) made the
   big runs killable, parallel, and auditable. m = 42 fell in 174 s
   (607M nodes): a(16) ≤ 41, already four better than the recorded 64.
   Then m = 38: 462 s, 5.03B nodes, sixteen UNSAT chunks. Combined
   with the witness: **a(16) = 37**.

The m = 38 growth curve behaved: 1.48B nodes at the n = 15 boundary,
5.03B at n = 16 (×3.4) — consistent with the ×3–5 per rung the ladder
showed, and nowhere near the ×20 wall that killed the SAT route. The
sub-optimum hardening feared after n = 15 (its boundary sits below the
continuum optimum 7n²/48) did not bite at 16, whose boundary sits just
above it.

A second full exhaustion of m = 38 on the plain engine (different
canonical form, different outer-loop code path) was launched as
belt-and-braces; it is pure redundancy on top of an engine that was
already two-implementation-validated, SAT-cross-validated, and
DRUP-anchored, but a first determination deserves it.

## Accounting of failures

- Same-cell exclusion missing in encoder v1 (caught by checker).
- Cell-pairwise SAT encoding: growth-rate dead end (measured, documented).
- Line SAT encoding: same wall (measured).
- Counting cuts in CNF: sound, validated, useless here (measured; the
  m = 64 experiment is the clean demonstration).
- Witness extraction after unwinding (caught by checker; verdicts
  unaffected).
- The first `check_peaceable.c` had 16 MB of stack arrays and
  segfaulted before reading input (caught by its own negative control).

## Session 2 (2026-09-03): a(17), as a secondary target

The day's mandate went to an external problem (the Bit Deletion game,
`conjectures/bit-deletion/`, solved by lunchtime); the internal-thread
audit had named a(17) the one internal thread breakable on 4 cores in an
afternoon, so it was launched on the freed cores rather than left for a
third session. No new code: the SYM16 engine and the chunked driver from
session 1, rebuilt from source.

1. **Lower bound first, from the literature, then from the definition.**
   OEIS A250000 still ends at a(15) (fetched today; a(16) = 37 from session
   1 is not yet in the entry). Kamenetsky's link file of best known
   placements gives a 42 + 42 board for n = 17 (attributed to Ainley
   1977); `check_peaceable` accepts it — 42 white, 42 black, zero attacking
   pairs. That is a(17) ≥ 42, CERTIFIED, whatever the provenance.
2. **The refutation.** `run_chunked.py 17 43 16 4 ./bnb_sym`: sixteen
   chunks, four at a time, every one UNSAT; 21,454,699,264 nodes in 1712 s
   wall (28.5 min). Chunk sizes ranged from 7.2·10⁷ nodes (68 s) to
   2.56·10⁹ (588 s); the chunk files are the run record. Node growth over
   the n = 16 boundary: ×4.26 — the ladder's ×3–5 per rung held, and the
   "sub-optimum hardening" that session 1 feared did not bite.
3. **So a(17) = 42**, Ainley's value, and the second consecutive open case
   of A250000 decided here.

What was *not* done, and why it matters: session 1 backed a(16) with a
second full exhaustion on the plain engine (different canonical form,
45·10⁹ nodes, an hour). At n = 17 that replication is ≈ 9× the SYM16
count — 4–5 h — and the session did not have it. The verdict therefore
stands on one engine plus its validation record, and the README says so.
A capped attempt to have the engines find a 42-witness of their own (as
they did at n = 16 in seconds) was launched alongside the write-up; its
outcome is recorded in the log entry.

## Session 3 (2026-09-04): a(18), again as a secondary target

The day's mandate went to two external problems (the antidiagonal traffic
anomaly and the triangulation-discrepancy residue class, both in their own
directories); neither needed the cores, and the internal audit had again
named the next rung of this ladder as the one internal thread breakable in
an afternoon. Same engines, rebuilt from source and re-calibrated (chunk 0
of the n = 15 refutation reproduced its recorded 27,106,454 nodes to the
node), same chunked driver, launched at 11:54 UTC.

1. **Lower bound from the literature, checked from the definition.** The
   A250000 link file's n = 18 board (Kamenetsky 2019, "Ainley 1977") has 47
   white and 48 black queens; `check_peaceable` finds no attacking pair, so
   a(18) ≥ 47 is CERTIFIED before the refutation starts. No engine search
   for a witness was run this time.
2. **The refutation.** `run_chunked.py 18 48 16 4 ./bnb_sym`: sixteen chunks,
   every one UNSAT, NODES_TOTAL nodes, ENGINE_S s of engine time. The wall
   time, WALL_S s, is not the engine's fault: for roughly two of the four
   hours the four workers shared the machine with the day's other
   computations (a 15-minute census, then an enumeration that turned out to
   cost seven core-hours instead of the twenty minutes estimated, and three
   background processes left behind by scouting agents). Once those were
   paused or killed the workers ran at full speed. Chunk sizes ranged from
   MINCHUNK to MAXCHUNK nodes (MAXCHUNK_S s); node growth over n = 17 was
   ×GROWTH, above the ×4 projected from the previous rung.
3. **So a(18) = 47**, Ainley's value, and the third consecutive open case of
   A250000 decided here (16, 17, 18 all inside this repository's three
   sessions on the problem).

What was *not* done: the plain-engine replication (≈ 9× the nodes,
≈ HOURS_PLAIN h) — the same single-engine caveat as n = 17 — and any engine
witness search. The lesson of the day is operational: never run a
"20-minute" enumeration next to a multi-hour exhaustion without measuring
the enumeration first.
