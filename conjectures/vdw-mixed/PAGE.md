# PAGE.md — handoff for the vdw-mixed page (new page)

New conjecture directory; no page exists yet. Target URL:
`fabianarevalo.com/vdw-mixed`, linked from the math index and from this
directory's README header once live.

## 1. Headline claim

**CERTIFIED** — `w(2;5,8) > 295`: the first recorded bound on the smallest
open cell of the row of the mixed van der Waerden table that Ahmed's
`w(2;5,7) = 260` has capped since 2013, by an exactly-74-periodic
2-coloring of `[1,295]` with no red 5-term and no blue 8-term arithmetic
progression, verified by two independent from-definition checkers.

## 2. Contributions

1. **CERTIFIED** — `w(2;5,8) > 295` (witness
   `data/witness_5_8_n295_perdef_p74k0.txt`, exactly 74-periodic, verified
   by independent Python and C enumerators; found by a complete SAT search
   over periodic-with-≤8-defects colorings which returned a 0-defect
   solution in 0.2 s).
2. **CERTIFIED** — first proof-carrying derivations of seven cells of the
   mixed table: `w(2;3,5)=22`, `w(2;3,6)=32`, `w(2;4,4)=35`, `w(2;4,5)=55`,
   `w(2;4,6)=73`, `w(2;4,7)=109`, `w(2;5,5)=178`. Every UNSAT leg ships a
   DRUP proof checked by a from-definition RUP checker (largest: 18,434,058
   lines / 1.14 GB for `w(2;4,7)=109`, checked in ~50 CPU-min); every
   witness passes two independent verifiers. The published values
   (1978–2013) predate certificate practice; these are their first
   machine-checkable proofs. (`w(2;5,6)=206`: legs still running at
   session close — see README status table for the live state.)
3. **CERTIFIED / structural** — extremal witnesses are near-periodic with
   a defect count that grows along the ladder: exactly 22-periodic at
   `(4,5)@54`; 44-periodic with **one** defect at `(5,5)@177`; no periodic
   witness with `p ∈ [30,49]` at `(5,6)@205` (complete per-period result);
   exactly-74-periodic at `(5,8)@295` but with different blocks governing
   different `n` (the `n=290` block dies at 292). This structure is what
   makes lower-bound legs computable: complete `(p, k)`-restricted searches
   in `2^p · C(n,≤k)` instead of `2^n`.
4. Infrastructure a future session resumes: validated cube-and-conquer
   driver (three controls, zero check failures, append-only campaign CSVs)
   and the measured UNSAT-cost curve (18 s at `(5,5)@178` vs > 2 h at
   `(5,6)@206` in the proof-logged solver) pricing the `w(2;5,7)`/`w(2;5,8)`
   decisions as multi-session cube-and-conquer campaigns.

## 3. Figure specs

- **F1 — the witness.** Render `data/witness_5_8_n295_perdef_p74k0.txt` as
  a 74×4 color grid (rows = periods, cells = colors), with the 74-block
  called out. Reader sentence: "A single 74-cell pattern, tiled four times,
  colors 1 through 295 with no red 5-term and no blue 8-term progression —
  so w(2;5,8) is bigger than 295."
- **F2 — the certified table.** The 7-row table from NOTE §2 (cell, value,
  proof lines, verdict). Reader sentence: "Every value has a checkable
  proof, and the proofs get astronomically longer as the numbers grow."
- **F3 — defect structure along the ladder.** Simple diagram: (4,5) → 0
  defects, (5,5) → 1 defect, (5,6) → no small-period witness at all,
  (5,8)@295 → 0 defects at a larger period. Data in NOTE §4. Reader
  sentence: "The extremal colorings are almost, but not quite, periodic —
  and how un-periodic they must be grows with the problem."

## 4. Caveats the page must carry

- **Every citation is (secondary)**: the sandbox's egress proxy blocked all
  primary sources (arXiv, OEIS, erdosproblems, journal pages, authors'
  pages — full list in `log/2026-08-16-vdw-mixed.md`). Published values
  quoted (178, 206, 260, etc.) were cross-checked only against search
  snippets retrieved 2026-08-16 — though the seven re-derived cells are now
  independently established by this session's own certificates.
- **Openness of `w(2;5,8)`** rests on: Ahmed's 2013 paper being the row's
  last movement in every reachable snippet, and the exact-value community's
  visible pivot to asymptotics and to Ramsey-number certificates. Residual
  risk: an unreadable BOINC lower-bounds project (boincsynergy.ca) could
  conceivably have unpublished bounds; stated in the log.
- `w(2;5,6)=206` is **not yet** among the certified cells if its in-flight
  legs did not land by publication time — check the README status table.
- The `>295` bound is a lower bound only; the row heuristic (+28, +54
  differences) puts the true value plausibly in the low-to-mid 300s.
- Proofs above ~10 MB are not in git: `certs/MANIFEST.csv` carries sha256 +
  checker verdict; regeneration commands are in the README (Zenodo deposit
  pending a session with upload access).

## 5. Existing page

None — this is a new page and a new top-level README row (already added
this session).
