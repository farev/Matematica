# Session writeup — 2026-08-09 (signed difference sets)

The unedited narrative, including what failed. Companion to NOTE.md
(results) and README.md (tables).

## Morning: survey under a blocked sky

Same egress posture as every session this week: arxiv.org, oeis.org,
erdosproblems.com, mathoverflow.net all EGRESS_BLOCKED; WebSearch and
raw.githubusercontent.com are the working channels. Four scout subagents
went out in parallel (fresh-arXiv quantity hunter; Erdős-database
computational shelves; flagged-papers reader + scoop guard; non-Ramsey
diversifier) while the certified-SAT toolchain was rebuilt and validated
(glucose_static streaming DRUP to disk, toy proof "s VERIFIED" — none of
it ended up needed today, but it stands for tomorrow).

The scouts came back with a slate spanning three subfields (log §2) and
three pieces of intelligence acted on immediately: Tranquilli
(arXiv:2608.02675, one week old) supersedes this repository's
bipartite-cubic Erdős–Gyárfás shelf — recorded in that conjecture's
README the same hour; Carr's structural constraints make our stalled
n = 19 sweep cheaper someday; Muney's Gilbreath-extension holes paper is
flagged in the gilbreath README. Scoop guard came back clean on both of
the repo's newest results.

The diversifier scout found the day's problem: Gordon's signed
difference set database — 67,823 Open cells, primary data on GitHub,
author-maintained, two papers in the whole literature, and the smallest
Open cell decidable in under a second (the scout did it during vetting).
Selected over Erdős #699 (pre-committed pivot, never fired) chiefly on
novelty position: the openness of every target is recorded per cell in
the primary artifact itself.

## The control battery bites the database

First order of business, before any search: an independent checker
(`sdslib.py`, dict-convolution over the group, no Sage, no shared code)
run against every witness stored in the database. Expected outcome: 280
green ticks and a pinned definition. Actual outcome: 133 green, **147
stored sets failing the defining equation**, all 147 concentrated in 21
cyclic cells.

An afternoon-long detour threatened — is my convention wrong? Three
hypotheses were tested and killed in order: (i) sums-instead-of-
differences convention (fails worse); (ii) negated storage of M or of P
(fails); (iii) any group-symmetry re-encoding — impossible in principle,
because translation, automorphisms, inversion and global sign flip all
preserve the multiset of off-peak correlations, and the failing sets
have non-constant profiles. Meanwhile the passing 133 include every
Paley cell, every He–Chen–Ge cell and 23 of Gordon's own orbit-exhaust
cells — same comment classes as some failing cells. Conclusion:
corruption in a subset of stored witness lists, not a convention
mismatch. One separate quirk: SDS(18,13,4,[3,6])'s witness is stored in
undeclared Z₃×Z₃×Z₂ coordinates and verifies once decoded — worth a
line in any upstream report.

Forensics on the smallest affected cell, SDS(20,11,2,[20]) ("All", 4
stored sets, all invalid): the complete enumeration (no reduction,
5.4M nodes, 1.3 s) finds exactly 40 labeled sets in 2 translation
classes, and the nearest true set to stored set 0 differs by exactly one
P↔M transposition (9 and 11 swapped). His exhaust was right; whatever
exported the JSON scrambled signs. The cell's status stands; the stored
coordinates don't. That distinction — status correct, witnesses corrupt —
is the audit's most useful sentence for upstream.

## The engine, and the bug the controls caught

`sds_search.c`: DFS over A: G → {−1,0,+1} with |P|, |M| forced by the
trivial character, incremental correlations, interval pruning by open
pairs, translation reduction 0 ∈ P. Version 1 had a pruning bug:
pairs adjacent to decided-zero elements were removed from the open-pair
counts twice (once when the zero was decided, once when the partner
was), deflating the intervals and producing a **false NONEXIST on
SDS(11,6,1,[11])** — a known "All" cell. The known-cells battery caught
it in the first minute.

The lesson is worth its own paragraph: for a session whose headline
claims are nonexistence-by-exhaust, the dangerous failure mode is a
prune that silently discards a live branch, and *only EXIST-side
controls can catch it* — a battery of No-cells would have validated the
broken engine happily. The fixed engine reproduces the entire decided
database at v ≤ 24 — 42 cells, every No a NONEXIST, every Yes/All an
EXIST with independently verified witnesses — and matches an
independent pure-Python exhaust witness-for-witness on 8 cells
(including two that were Open until that moment: SDS(18,15,2,[3,6]) and
SDS(20,17,8,[2,10]), both empty, each decided by two implementations
that share nothing but the definition).

## The theory turn

Writing the soundness argument for the |P|/|M| split (trivial
character) made the rest of the character story impossible to ignore:
every nontrivial χ has |χ(A)|² = k−λ. Two classical consequences
transfer verbatim (NOTE §2): v even forces k−λ to be a perfect square
(order-2 character), and Turyn's self-conjugacy argument kills odd
p-valuations of k−λ for p self-conjugate modulo any m | exp(G), p ∤ m.
The canary: SDS(18,15,2,[3,6]) — decided empty by both engines an hour
earlier — has k−λ = 13 and even order. A one-line theorem proves what
the morning's exhaust computed, and the cell was *Open in the
database*, so the artifact had never absorbed even the order-2 test.

`theory.py` swept all 70,543 cells: **45,328 of the 67,823 Open cells
close** (23,997 by T1, 21,331 by T2), with zero violations among the
146 Yes/All cells (the criteria never contradict a cell that verifiably
contains an SDS) and zero conflicts with exhaust decisions — theory and
engine validating each other. As a byproduct the criteria retro-cover
984 of Gordon's 2,574 exhaust-No cells; the remaining 1,590 of his No
cells are "hard" nonexistence, invisible to these characters — as are
the small cells our exhausts decide.

Honesty note, prominently: both criteria are classical machinery, and
Gordon's unread paper may state either transfer. The 45,328 per-cell
closures are new to the database regardless — that is checkable from
the snapshot in `data/` — and every criterion fires with parameters a
referee can verify by hand.

## Sweeps

The concordance sweep (v ≤ 24, all statuses) doubled as production:
six previously-Open cells decided, all empty. Batch 2 (Open, v 25–32,
naive cost ≤ 6·10⁹, ~35 min on 4 cores) was the harvest: 36 decisions
including the first eight EXIST cells — the moment the day turned from
"closing empty cells" to "finding signed difference sets nobody has
published". Batch 3 (v 33–50) added 16 more, including the
(36,11,2) 3-Sylow split and both order-49 and order-50 cells; its
slowest member, SDS(50,49,24,[50]), took 31 minutes. Total: 58
decisions, 10 EXIST, wall times 30 ms to 31 min per cell.

The (32,20,4) family — the smallest cells surviving both criteria and
all exhausts — got a measured verdict rather than an attempt: a
node-limit probe clocked 3.2·10⁶ nodes/s against a ~5.5·10¹¹-node
tree, i.e. ≈ 48 core-hours per group × 7 groups. Recorded as the open
frontier (an automorphism-canonical search would collapse it — the
elementary-abelian member has |GL(5,2)| ≈ 10⁷ worth of unused
symmetry). The audit re-exhaust of SDS(35,21,10,[35]) was still
churning at close (its existence question had already been settled by
the swap-repair recoveries) and was killed after ~60 minutes wall; the
engine emits no progress lines, so the cert file records the kill and
the wall time, not a node count — the complete-count question there
stays open, honestly.

## What failed

- Engine v1's unsound prune (above) — caught by design, fixed, engine
  re-validated from scratch.
- The witness-control battery "failed" in the productive sense: it was
  meant to be a formality and instead became a deliverable (the audit).
- `check_db.py`'s first run crashed on the undeclared-coordinates
  quirk instead of reporting it — the checker returned an exception
  where a verdict belonged; fixed to fail soft.
- Committed the compiled search binary once, against repo convention —
  caught by the stop-hook, untracked, gitignored.
- The (32,19,2) and (25,16,2)-class cells burned background CPU before
  the criteria landed and marked them closed; harmless (the exhausts
  agree with the theorems — mutual control), but a criteria-first
  pipeline would have ordered the day better. Next SDS session: run
  `theory.py` before `sweep.py`.

## Where this leaves the problem

The database's Open shelf drops from 67,823 to 22,495 minus the day's
exhaust decisions, and the surviving small cells are now genuinely
interesting: they pass every classical character test and (v ≤ 32)
contain no SDS by exhaust — each one is a small sporadic-existence
question with no cheap answer in either direction. The (32,20,4)
family across all seven abelian groups of order 32 is the natural next
compute target; the theory question worth a future session is which
*stronger* classical tests (multiplier theorems, field descent) survive
the signed setting, given that ramified primes (Gauss sums) genuinely
escape self-conjugacy here.

Upstream: everything in this directory — the audit, the closures, the
decisions, the witnesses — is formatted to be reportable to Gordon
(his README requests problem reports; the fix list is
`data/witness_audit.csv`, the closures `data/theory_closures.csv`, the
decisions `data/values.csv` with `certs/`).
