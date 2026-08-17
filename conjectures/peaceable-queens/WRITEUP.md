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

[Filled in as runs complete — witness search at m = 37 and the UNSAT
walk-down. Every completed UNSAT at m is a permanent certified bound
a(16) ≤ m − 1; the recorded bound to beat was Pratt's 64.]

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
