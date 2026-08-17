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

## Result

(session in progress)

## What failed

(session in progress)

## Next

(session in progress)
