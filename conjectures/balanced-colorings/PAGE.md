# PAGE.md — handoff for the site build (new page: fabianarevalo.com/balanced-colorings)

New conjecture directory, new page. Built from the 2026-08-27 session.

## 1. Headline claim

The first computational attack on the open case (r = 5) of the
Erdős–Gyárfás balanced-colouring conjecture: K₂₅ has a certified balanced
5-colouring from the affine plane (CERTIFIED), every colour class of a
hypothetical K₂₆ witness is proved to be a (6,6)-Ramsey graph whose
per-class counting bound comes within one edge of deciding the problem yet
provably never does (PROVED + CERTIFIED), and the two natural witness
routes — extending the affine construction, and vertex-regular symmetry —
are certifiably closed (CERTIFIED). K₂₆ itself remains undecided.

## 2. Contributions

1. **CERTIFIED.** A balanced 5-colouring of K₂₅ (every 6 of the 25
   vertices span all 5 colours), built from AG(2,5) by a three-line
   pigeonhole argument (PROVED for every prime power r: T(r) ≥ r²),
   machine-verified over all 177,100 six-subsets; likewise K₉ (r = 3,
   126 subsets) and K₁₆ (r = 4, 4,368 subsets). So the conjecture's
   bound is tight at r = 5 below: only K₂₆ is in question.
2. **PROVED.** In any balanced r-colouring of K_{r²+1}, every colour
   class has clique number ≤ r and independence number ≤ r — i.e. is an
   (r+1,r+1)-Ramsey graph — and every complement is K_{r+1}-free with
   chromatic number ≥ r+1. Two-line counting; it kills all
   "partition-structured" witnesses and identifies the r = 2
   counterexample (C₅, chromatic number 3 = r+1) as exactly the escape
   the conjecture claims impossible for r ≥ 3.
3. **CERTIFIED.** The counting barrier is sharp: with
   E*(N,s) = max edges of a graph on N vertices with no K_s and no
   independent s-set, existence at K_{r²+1} forces
   E*(r²+1, r+1) ≥ (r−1)/r · C(r²+1, 2). Computed: E*(10,4) = 31
   against threshold 30 (r = 3 — the proved case is missed by ONE
   edge; UNSAT at 32 in 4.6 s), E*(17,5) ≥ 104 against 102 (r = 4),
   E*(26,6) ≥ 265 against 260 (r = 5; witnesses committed and
   definition-verified; exact values open above the thresholds). At
   r = 2 the threshold is met with equality (E*(5,3) = 5 = C₅) and the
   unique witness realizes it — rigidity that provably fails at r ≥ 3.
4. **CERTIFIED (DRUP, checked).** The affine family does not extend: the
   K₂₅ construction leaves exactly 50 pairs free, every choice balanced;
   no choice plus any colouring of a 26th vertex's 25 edges is balanced
   (375-variable SAT instance, UNSAT, 1,160-line DRUP proof verified by
   the repository's independent checker; the q = 2 analogue, where
   extensions do exist, passes as positive control finding exactly the
   2 known C₅-type completions).
5. **PROVED + CERTIFIED.** No vertex-regular witness at K₂₆: an
   invariant colouring's classes must have exactly 65 edges
   (2a + b = 5 profile arithmetic — PROVED), which is unsolvable over
   Z₂₆, and over D₁₃ all 3,198 admissible classes fail the
   independence-number test (exhaustive, with controls). Contrast:
   the r = 2 counterexample IS a circulant.
6. **NUMERICAL (hardness observation).** The direct SAT question is
   pigeonhole-hard: at K₁₀ (r = 3; 135 variables, 810 clauses) CaDiCaL,
   Glucose, kissat and RoundingSat all fail unaided; BreakID symmetry
   breaking cures K₁₀ (UNSAT in 3.1 s — the Erdős–Gyárfás r = 3 theorem
   machine-reproduced) but not K₁₇/K₂₆ within session windows. This
   explains why no computational attack appears in the literature.

## 3. Figure specs

- **Fig 1 — the K₂₅ witness.** Data:
  `data/K25_balanced_5col.txt` (325 lines "u v colour") and, for layout,
  the 25 points as the 5×5 grid of AG(2,5) with the six parallel classes;
  colour = parallel class of the connecting line, two classes merged.
  Sentence a reader should say: "Twenty-five points, five colours, and
  any six points you pick always show all five — because six points must
  contain two on a common line in every direction."
- **Fig 2 — the sharp counting barrier.** Data: thresholds
  (r−1)/r·C(r²+1,2) = 5, 30, 102, 260 for r = 2, 3, 4, 5 vs computed
  E*: 5 (=, tight), 31 (`data/ramsey_10_4_ge31.txt`; = 31 exactly, UNSAT
  at 32), ≥ 104 (`data/ramsey_17_5_ge104.txt`), ≥ 265
  (`data/ramsey_26_6_ge265.txt`), with the Turán ceilings 33, 108, 270
  drawn above. Sentence: "The simplest counting argument would decide
  the problem if the blue bar stayed below the red line — it clears it
  by one edge at r = 3 and by at least five at r = 5, so the conjecture
  lives entirely in how the five colour classes interlock."
- **Fig 3 — no symmetric witness.** Data: `dihedral.py` output — 195 +
  1,716 + 1,287 = 3,198 candidate dihedral colour classes by profile
  (2 rotations + 1 reflection / 1 + 3 / 0 + 5), each 65 edges, 0
  survivors of the independence test. Sentence: "At r = 2 the
  counterexample is a perfectly symmetric pentagon; at r = 5, all 3,198
  symmetric candidates fail — any counterexample to the conjecture at
  K₂₆ would have to be an asymmetric object."

## 4. Caveats the page must carry

- Every literature statement is **(secondary)**: the sandbox could not
  read Erdős–Gyárfás 1999 or Füredi–Ramamurthi 2002. The r = 3, 4
  attributions, the r = 2 remark, and the openness of r = 5 rest on the
  erdosproblems.com page (#617, checked 2026-08-27, "open/falsifiable",
  last updated 2026-04-01), the teorth/erdosproblems problems.yaml
  snapshot (read in full the same day), and DeepMind's
  formal-conjectures Lean statement (tagged research-open, 2026-01-24).
  The construction at r² and the codes⟺structured-colourings
  equivalence may well appear in those papers; the page must not claim
  novelty for them.
- The K₁₀ machine reproduction trusts BreakID's symmetry-breaking
  predicates (satisfiability-preserving by construction, not
  DRUP-derived); the DRUP-certified results are: the code-family
  non-extension (checked by `tools/satcert/rup_check`) and the
  small-instance UNSAT runs listed in the conjecture README.
- E*(17,5) and E*(26,6) are lower-bounded (104, 265), not pinned; the
  page should show them as "≥" bars, not exact values, unless the
  session close updated them (check README before building).
- K₂₆ itself is UNDECIDED. The page's framing must be "first structural
  and computational map of the open case", not "progress toward" either
  verdict.
- The hardness observation (item 6) is NUMERICAL: wall-clock behaviour
  of four solvers on this machine, not a lower-bound theorem.

## 5. Existing page

None — new page, new index row (added to the top-level README this
session).
