# PAGE.md — handoff for the site page `fabianarevalo.com/kobon-triangles`

New page (no page exists for this conjecture).

## 1. Headline claim (one sentence, with label)

**CERTIFIED (independent machine-checked confirmation of a 2008 theorem, found to be prior
work mid-session):** no simple arrangement of 18 pseudolines has 94 bounded triangular
faces, so the simple-pseudoline Kobon value for 18 lines is 93 — Bartholdi–Blanc–Loisel's
"93–94" table entry, which Blanc's polynomial bound had already closed in 2008 — decided
here by 561 dihedral-orbit SAT cubes with drat-trim-verified proofs; plus a **flagged
audit**: the upper bounds quoted on OEIS A006066 and Wikipedia for even `n` are theorems
about arrangements in general position, while the recorded optima at `n = 8, 12, 14` use
triple points, so on the cited literature `54 ≤ K(14) ≤ 55` and `93 ≤ K(18) ≤ 95`.

## 2. Contributions (numbered, labelled, with the numbers)

1. **CERTIFIED.** `a^s_3(18) = 93` for simple Euclidean pseudoline arrangements: all
   561 cubes UNSAT, 561 of 561 DRAT proofs verified by `drat-trim`
   (5.0 core-hours solving, 8.2 verifying; SHA-256 of every proof in
   `data/cubes_T2.csv`). Upper bound: rediscovery of Blanc 2008 (Geombinatorics 2011),
   Theorem 1 / Theorem 3; lower bound: Bader's 93-triangle straight-line arrangement
   (OEIS A006066).
2. **PROVED.** The equality-case structure at `n = 18` (NOTE §4): a 94-triangle simple
   arrangement would have exactly 12 perfect lines and 6 lines with one unused segment,
   each unused segment joining two extreme crossings of perfect lines; and the order-`4n`
   dihedral symmetry of the signotope model (NOTE §5), validated exhaustively for `n ≤ 7`.
3. **CERTIFIED (controls).** The encodings reproduce OEIS A006245 (8, 62, 908, 24698
   arrangements for `n = 4..7`) and every value of BBL Theorem 1.4 for `n ≤ 16`, including
   the non-trivial UNSATs at `(8,15)`, `(10,26)`, `(11,33)` (0.7 s; Savchuk's table encoding:
   1.67 s) and `(12,38)`.
4. **Audit (flagged, not settled).** OEIS A006066's upper-bound column uses
   `⌊n(n − 7/3)/3⌋` (BBL, simple arrangements) for even `n`, and calls `a(14) = 54` exact on
   that basis although the `a(14) = 54` arrangements have triple points; the only bound
   stated for general configurations (Clément–Bader draft, Table I) is 55 at `n = 14` and
   95 at `n = 18`.
5. **NUMERICAL / search.** A triple-point search model (collapse vertex-disjoint triangular
   faces of a simple arrangement; quadrilaterals with one collapsed neighbour become
   triangles) reproduces `K(8) = 15` in 13 s and finds `n = 8, t = 16` UNSAT in 196 s
   (within the model); its `n = 12, t = 38` positive control timed out at 40 min, and the
   searches at `n = 12` (39), `n = 14` (55), `n = 18` (94) were stopped unresolved after
   35–40 min. No construction is claimed.

## 3. Figure specs

* **Figure 1 — what a cube is.** Data: `data/cubes_T2.csv` (cube index, imperfect-line
  set, orbit size, solve time). Show the 18-cycle of line labels with one 6-subset
  highlighted, and a histogram of solve times (fast early cubes vs. the spread-out sets).
  Sentence: "The 18,564 ways to choose which six lines are imperfect fall into 561
  symmetry classes, each refuted separately in seconds to minutes."
* **Figure 2 — why triple points matter.** Data: the decoded `n = 8` model in
  `data/c3_n8_t15.model.txt` (a simple 8-line arrangement with 14 triangles, two collapsed
  triangles, four promoted quadrilaterals). Draw the wiring diagram before and after the
  collapse. Sentence: "Merging a small triangle into a triple point can turn its
  neighbouring quadrilaterals into triangles, which is how 15 beats the general-position
  maximum of 14."
* **Figure 3 — the two bound columns.** Data: NOTE §9 table (Tamura, Clément–Bader
  general, BBL/Blanc simple, best known) for `n = 8..20`. Sentence: "For even n the
  bound everyone quotes is a theorem about general position; the records that reach it
  are not in general position."

## 4. Caveats the page must carry

* The certified result is for *simple* arrangements (pseudolines or lines in general
  position) and was already a theorem (Blanc 2008/2011); the page must say
  "independent confirmation", never "new".
* The cube certificate depends on BBL's association lemma (published; re-proved in NOTE
  §4 and checked computationally on all even-`n` cases available) and on the
  Felsner–Weil signotope bijection (published). The plain lemma-free instance was not
  finished.
* Secondary/unread: Zarzuelo Urdiales 2026 (even lower bounds); Clément–Bader is an
  unpublished 2007 draft (read from the OEIS-cached copy).
* Stretchability is irrelevant to the negative result but essential to any positive
  triple-point construction; none is claimed.

## 5. Existing page

None.
