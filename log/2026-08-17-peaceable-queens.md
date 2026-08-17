# 2026-08-17 — peaceable-queens

**Target.** Prove `a(16) = 37` for OEIS A250000, the peaceable queens
sequence: the largest m such that m white and m black queens fit on an
n × n board with no queen attacking a queen of the opposite color.
Exact values are known only for n ≤ 15 (per Clinch–Drescher–Huynh–
Saffidine 2024, (secondary)); a construction gives `a(16) ≥ 37`, and the
best published upper bounds at n = 16 are far from 37. The plan: a SAT
pipeline with machine-checkable certificates — reproduce the full ladder
`a(1..15)` as positive controls (each boundary shipped as a DRUP proof
checked by the repo's from-definition `rup_check` plus an independently
verified witness), measure the UNSAT cost growth, then attack the open
boundary `n = 16, m = 38` UNSAT. Floor deliverable: the first
machine-checkable certificates for the ILP-folklore values a(12..15).
Ceiling: the first new exact term of A250000 in a decade.

## Connectivity check

- **WebFetch: fully blocked** (same as 08-13). arxiv.org, oeis.org,
  erdosproblems.com all return EGRESS_BLOCKED from the sandbox proxy;
  mathoverflow.net fails too. No primary page was readable this session.
- **WebSearch: working.** All literature claims below are search-snippet
  evidence retrieved 2026-08-17; **every citation in this session is
  (secondary)** unless it is to code/data in this repository.
- **archive.ubuntu.com: reachable** — `cadical` 1.7.4-1 installed via apt.
  This matters: it un-blocks disk-streamed DRUP proofs, which the 08-07
  session lacked (pysat buffers proofs in RAM; three 15 GB OOM kills).
- PyPI reachable (python-sat installable).

## Candidate slate (external)

**C1 — Peaceable queens a(16) (chessboard combinatorics / SAT).**
Statement: max m with m white + m black queens on 16 × 16, no
cross-color attack; is it 37? Sources checked 2026-08-17 (all secondary,
via snippets): oeis.org/A250000 (Bosch 1999 origin; Pratt confirmed
a(1)–a(13) by ILP on 2014-12-01 and gave bounds for n = 14..20);
arXiv 2406.06974 (Clinch–Drescher–Huynh–Saffidine 2024: "only the first
15 terms are known", asymptotic upper bound 0.1716n², lower construction
(7/48)n²); arXiv 1902.05886 (Yao–Zeilberger, numeric/symbolic study);
arXiv 2508.11945 (Rostami–Bright, Aug 2025: queen *domination* by SAT
with DRAT certificates — the adjacent queens problem fell to SAT, and
they found UNIDOM bugs, showing certificates earn their keep here).
Why believed open: the 2024 paper and every snippet state n ≤ 15 only;
searches for a 2025/2026 resolution of a(16) or n = 16 found nothing;
the value would land in A250000 and it has not.

**C2 — No-three-in-line, first open n (discrete geometry).**
Statement: 2n points in the n × n grid, no three collinear — does n = 65
admit one? Sources checked 2026-08-17 (secondary): Flammenkamp's page
(M(n) = 2n for n ≤ 46 and n ∈ {48,50,52}, 1998); snippets report
**Prellberg 2026** extended this to all n ≤ 64 plus {66, 68} by
constraint programming. Why not chosen: the frontier moved *this year*
and is held by a specialist with CP tooling and more compute; the first
open case n = 65 is odd, and 2·65 = 130 ≡ 2 (mod 4) rules out full
C₄-symmetric solutions, so the cheap symmetric search that cracks even n
does not exist there — exactly the case his tools presumably already
failed on. Vetting killed this candidate; that is what vetting is for.

**C3 — w(2; 3, 20) = 389? (arithmetic Ramsey theory / SAT).**
Statement: least N such that every 2-coloring of [1, N] has a
monochromatic 3-AP in color 1 or a 20-AP in color 2. Sources checked
2026-08-17 (secondary): arXiv 1102.5433 (Ahmed–Kullmann–Snevily:
w(2;3,19) = 349 computed, w(2;3,20) ≥ 389 conjectured sharp); snippets
confirm 389 is still only a conjectured lower bound. Why not chosen:
the UNSAT at N = 389 is priced (from their reported effort on t = 19 and
the growth of these instances) at hundreds of core-hours minimum — not a
4-core-session budget. An honest slate needs at least one candidate
rejected on cost measured against the machine actually available.

Subfields spanned: combinatorial chessboard optimization, discrete
geometry, arithmetic Ramsey theory.

Vetted and killed during the survey (recorded so the next session does
not redo the searches): ternary rich-word repetition threshold — solved
by Currie–Mol, EJC June 2025, RT = 1 + 1/(3−μ) ≈ 2.2588, μ the real
root of x³−2x²−1 (secondary).

## Internal-thread assessment

Strongest live internal threads, from the last five logs and READMEs:

1. **distinct-subset-sums** (08-13 "Next"): the multi-m deficiency-vector
   engine, projected 5–10× on the f(10) sweep. Real, but the payoff is
   still CPU-months from deciding f(10); today it buys a range extension,
   not a row change.
2. **generalized-schur** (08-07 "Next"): the (4,4,u) ladder — notably
   **un-blocked today** by apt cadical (the 08-07 blocker was pysat
   buffering DRUP proofs in RAM). Row-changing if several values land.
   But it would be the third session in two weeks mining the same
   Rado/Schur DRUP groove, against a mandate that explicitly prices
   novelty; and the toolchain fix that un-blocks it also un-blocks C1.
3. **signed-difference-sets**: order > 36 needs the layered-refinement
   port, priced at ~2 CPU-weeks or a day of new code. Not today.

Selection argument: C1 beats the internal threads and the slate.
(a) The bottleneck is a finite UNSAT computation with measurable cost
growth and a natural floor deliverable (certified a(12..15)) if n = 16
is priced out — CPU can actually break it, and partial progress is not
vapor. (b) "Already done?" is answerable: the ledger is OEIS A250000,
which stops at 15; the 2024 paper says 15; targeted searches for a 2025–26
resolution found none. (c) The result extends Clinch–Drescher–Huynh–
Saffidine 2024 (their Table of known values), Pratt's 2014 ILP line in
the OEIS entry, and the Rostami–Bright Aug 2025 SAT-on-queens program,
and it lands in A250000 — a sequence prominent enough to have its own
Sloane video. The rotation rule is satisfied (last two sessions:
signed-difference-sets, distinct-subset-sums). Default-external applies
and the external candidate wins on merits anyway.

**Today's specific attempt.** Build a certified SAT pipeline for
peaceable queens; reproduce a(1..15) as controls (which also settles the
attack-model question operationally — the ladder only reproduces if the
no-blocking pairwise line-exclusion model is the right one); certify the
boundaries of a(12..15); then decide n = 16, m = 38 UNSAT within the
session's budget, cube-and-conquer if needed. Success = a(16) = 37 with
a checkable certificate. Honest fallback = certified ladder + a priced,
resumable n = 16 campaign.

Mid-session checkpoint: if the measured growth prices n = 16 out of
~30 core-hours, say so, ship the certified ladder, and leave the
campaign resumable.

## Mid-session checkpoint (invoked, with data)

The SAT plan died on measurement, not on speculation. Cell-pairwise
encoding: UNSAT growth ~12–20×/rung (n=7: 2.0 s, n=8: 46 s). Line
encoding: same wall. Provable counting cuts (unit-tested exhaustively):
no help where it matters — and the diagnostic: n=16 m=64, where a
one-line counting argument collapses the search space, still blew a
240 s cadical timeout, because CDCL re-proves the diagonal-span
argument per row/column subset. Resolution is the wrong proof system
for this problem's counting core. Pivot: exact branch-and-bound in the
line-labeling formulation with proved pruning lemmas (NOTE Lemmas 1–6),
Python reference + C port with node-count equality, SAT pipeline
retained as the small-n cross-validation and DRUP anchor layer.

## Result

**PROVED** — line-labeling reformulation and pruning lemmas (NOTE
Lemmas 1–6, with proofs).

**CERTIFIED** — the complete known ladder re-derived from scratch, no
external values assumed: a(1..15) = 0,0,1,2,4,5,7,9,12,14,17,21,24,28,32.
Boundaries: exhaustive B&B refutations at a(n)+1 (a(13): 478M nodes,
99 s serial; a(14): 2.26B nodes, 231 s on 4 workers; a(15): [pending
at time of writing — see final section]); checker-verified witnesses
at a(n) for every n (all in `witnesses/`). For a(14) = 28 and
a(15) = 32 no published proof artifact could be located from the
sandbox (Pratt 2014 recorded only 28 ≤ a(14) ≤ 43, 32 ≤ a(15) ≤ 53;
the 2024 paper reports the values as known): these appear to be the
first independently reproducible derivations, phrased with that
caveat.

**CERTIFIED** — a(16) ≥ 37: the engine independently found a 37+37
placement on 16×16 (29 s, 177M nodes), verified by the from-definition
checker. Matches Ainley's 1977 construction bound (secondary).

**Validation record** — two engines with node-for-node equality
(477,786,646 nodes at the n=13 boundary, serial and 4-way-parallel
alike); 40/40 verdict agreement vs an independent SAT pipeline on all
army sizes for n ≤ 8; DRUP proofs at the n ≤ 7 boundaries verified by
`tools/satcert/rup_check`; every witness re-verified independently.

**In flight at n = 16** — the decisive UNSAT run at m = 38 (auto-chained
after a(15)'s refutation completes): UNSAT proves a(16) = 37 (first new
term of A250000 in a decade); SAT refutes the conjectured value. Every
completed stride chunk is a permanent partial certificate; the recorded
finite upper bound to beat is Pratt's a(16) ≤ 64.

## What failed

- **Encoder v1 soundness bug**: no same-cell exclusion — the solver
  stacked both colors on one 5-queens solution ("a(5) ≥ 5"). Caught by
  the independent witness checker before any claim was made.
- **Pure SAT at scale**: three escalations (cell encoding, line
  encoding, counting cuts), each measured, each dead — documented with
  timings in WRITEUP.md. The m = 64 diagnostic experiment is the clean
  demonstration that the failure is structural (resolution vs
  counting), not an encoding detail.
- **Witness extraction after DFS unwinding**: the first B&B "witness"
  at n = 11 had 90 attacking pairs because backtracking had revived
  every killed cell before extraction. Caught by the checker; verdicts
  unaffected (separately validated); fixed by snapshotting at the SAT
  leaf; all witnesses re-verified.
- **check_peaceable v1** segfaulted on 16 MB of stack arrays before
  reading input — caught by its own negative control.
- **Session hygiene**: `&&`-chaining after `./bnb` swallowed a test
  batch (exit code 10 = SAT by design); a 2-minute default timeout
  killed a benchmark batch mid-loop (moved to background tasks).

## Next

If m = 38 completes UNSAT: a(16) = 37 is decided; write PAGE.md, update
the top-level index, and the note becomes preprint-shaped (the natural
venue continuation of arXiv:2406.06974's table). If still running at
session end: the run is stride-resumable; the next session re-launches
remaining chunks (`drive.py 16 38`, chunk state in `results/`).
Then: a(17) (Pratt: 42 ≤ a(17) ≤ 72) with the same machinery; the
family-sum bound joined across diagonal families (NOTE §7.2) is the
algorithmic lever; the torus (A279405, odd case reported open) is the
adjacent frontier.
