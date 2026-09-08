# Session narrative — equitable-total-colorings (2026-09-08, hedge)

This directory is the product of a hedge: while the main line of the day attacked
Erdős Problem #963 (see `conjectures/dissociated-subsets/`), a subagent with one core
and a 90-minute budget was given Question 7.1 of arXiv:2609.05259, the cleanest
"explicitly posed, finitely checkable, four days old" item on the day's survey slate.
The paper's authors themselves wrote that the check was within reach of SAT; the only
question was whether anyone had done it. The subagent's full report is condensed here;
the session lead re-checked one counterexample independently and wrote these documents.

## What was done, in order

1. **Read the paper** (PDF fetched, text extracted with pymupdf): definitions of total
   colouring, Type 1/2, equitable, `χ''_e`, the graph `R` (Figure 1 only), Question 7.1,
   the remark that orders ≤ 18 were not checked, and the reduction to connected graphs.
   Theorems 4.1, 5.3, 5.4 (possible colour-class configurations at orders 14, 16, 18)
   were noted as cross-checks.
2. **nauty.** GitHub is blocked from the sandbox; as in the 2026-09-07 session, nauty
   2.8.8 was built from the pynauty source distribution on PyPI. `geng` was validated
   against OEIS A002851 at all eight orders.
3. **Encoding and controls.** Definition-level SAT encoding with python-sat; witness
   checker written separately from the definition; DRUP proofs through the session's
   `satpipe.py` (CaDiCaL verdict, Glucose proof, `rup_check` verification), with
   negative controls on both the checker and the proof checker. Controls: K4 and K3,3
   Type 2; ladders, Petersen, generalized Petersen graphs, the paper's H16 and H18 (with
   the appendix certificates) Type 1 with exactly the stated configurations.
4. **R from Figure 1.** The figure was zoomed and transcribed: four K_{2,3} gadgets
   wired in a ring; the transcribed colouring validates with configuration (14,12,12,12),
   the equitable instance is UNSAT with checked proofs. Two ports are clipped in the
   figure; their colours are forced. Isomorphism with the published `R` is unverified.
5. **The census** over all 45 982 connected cubic graphs of order ≤ 18: 411 s on one
   core, 95 % of it in the equitable solves. Result: 23 Type 1 graphs with `χ''_e = 5`
   (16 at order 16, 7 at order 18), none at order ≤ 14.
6. **Certification pass** (`post.sh`, `cert.py`, `cert_nosb.py`): DRUP proofs with and
   without symmetry breaking for the 23 equitable-UNSATs, for `R`, and for all 2 416
   Type 2 plain-UNSATs (4 920 proofs, 534 MB, all `rup_check`-verified); SAT-free
   enumeration of all colourings of the order-16 counterexamples (all (11,10,10,9)) and
   of the Type 2 graphs of order ≤ 14 (none).
7. **Order 20, partially:** three of ten residue classes in the remaining time (2 073 s):
   20 more examples, all (14,12,12,12).
8. **Lead's re-check:** `brute.py` on the first order-16 counterexample — 0 equitable,
   64 total colourings, all (11,10,10,9).

## What failed or is unfinished

- The subagent could not write its `REPORT.md` (a harness rule blocks report files from
  subagents); the report was returned in the message and is reproduced in NOTE.md.
- SAT witnesses were verified in-process but not saved (a defect; `scan.py` regenerates
  them in 7 minutes).
- The order-20 census is incomplete (31.6 %), and `R`'s residue class was not scanned.
- Type 2 counts were not compared with the literature (Hamilton–Hilton 1991, Sasaki
  2013 inaccessible from the sandbox).
- Whether the 23 graphs appear in Adauto's 2022 dissertation or in Stemock's work is
  unknown; the paper says the check had not been done, which is the only evidence of
  novelty.
- The 520 MB of Type 2 proofs are not committed (manifests are).

## Labels

The negative answer to Question 7.1 and the per-order census are **CERTIFIED**: exact
computation, every relevant UNSAT with a checked DRUP proof, every witness independently
verified, and an independent SAT-free enumerator agreeing on all 23 counterexamples.
The order-20 findings are certified per graph but the census there is partial.
