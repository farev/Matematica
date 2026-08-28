# PAGE.md — handoff for the site build (new page: fabianarevalo.com/nci-datrees)

**FINALIZATION GUARD:** the n = 15 census leg is [PENDING — see
data/census_summary.tsv; if its row 15 is absent, replace every "15" below
by "14", every "16" by "15", and "171,432,955" by "19,199,437"]. Do not
build the page while this guard paragraph is present.

## 1. Headline claim (one sentence)

**CERTIFIED** — Every one of the 171,432,955 lattices with at most 15
elements admits a winning left-linear dot-algebra tree, so the minimal
counterexample to the Non-Cancelling-Intersections conjecture — refuted
the day before this session, non-constructively, at ≈ 1.00011·10¹⁵
elements — has at least 16 elements; this is the first lower bound
recorded for either of the two open problems posed in the refutation
papers.

## 2. Contributions

1. **CERTIFIED.** Exhaustive census: all lattices with 3 ≤ n ≤ 15 elements
   (171,432,955 lattices, streamed as 34,978,238,589 posets on ≤ 13
   points), every one decided *left-linear winnable*; zero non-winning,
   zero left-linear/general separations. Generation counts equal OEIS
   A000112(n−2) and lattice counts equal A006966(n) at every size — the
   anchors are part of the certificate.
2. **CERTIFIED (consequence).** The minimal lattice with no winning
   da-tree (arXiv:2608.27416, §9 OP 1) has ≥ 16 elements; upper bound from
   that paper ≈ 1.00011·10¹⁵ (p = 100003). The minimal lattice with no
   winning *left-linear* da-tree (arXiv:2608.19414, §9 OP 1) has ≥ 16
   elements; that paper's own certified upper bound was 10^(10^2215),
   since improved to the same ≈ 10¹⁵ by the full refutation.
3. **CERTIFIED (consequence).** No lattice with ≤ 15 elements separates
   left-linear from general da-trees — the separation the two refutations
   jointly imply exists happens strictly above 15 elements — and the
   engine prints an explicit separating witness the moment one enters
   range.
4. **CERTIFIED modulo cited equivalences.** Any counterexample *set
   family* to the original Amarilli–Monet–Suciu conjecture has more than
   15 distinct subfamily intersections (via their §4 isomorphism-invariance
   + canonical realization, checked at statement level).
5. **PROVED (small).** Closure/BFS characterizations of the two
   winnability notions; the poset⇄lattice enumeration bijection; duality
   robustness of the census; unique-coatom lattices at size n are
   A006966(n−1) many and trivially winning (observed exactly at every
   size).

## 3. Figure specs

- **Fig. A — the gap.** A log-scale number line from 1 to 10¹⁶ with a
  solid green band over [1, 15] ("every lattice here is winnable —
  checked, all 171,432,955 of them"), a red marker at ≈ 1.00011·10¹⁵
  ("smallest counterexample the refutation certifies"), and open space
  between. Data: the two endpoints, provenance in NOTE §1/§4.
  Reader's sentence: *"Below 16 elements it's certified impossible to find
  a counterexample; the one known to exist lives near 10¹⁵; the fourteen
  orders of magnitude between are open."*
- **Fig. B — what a winning tree is.** The 9-element lattice from the
  refutation paper's own Figure 3.1 (Hasse diagram, data:
  `data/fig31.d6`) beside the session's machine-verified tree
  ((S_a − S_d) + S_g) + ((S_c − S_e) + (S_b − S_f)), with the four leaf
  down-sets shaded. Reader's sentence: *"A winning tree assembles
  everything-but-the-top out of down-sets of nonzero-Möbius elements,
  using only disjoint unions and subtractions of subsets."*
- **Fig. C — the census ladder.** Bar chart, log y: lattices per size n =
  3…15 (1, 2, 5, 15, 53, 222, 1078, 5994, 37622, 262776, 2018305,
  16873364, 152233518), each bar fully green. Data:
  `data/census_summary.tsv`. Reader's sentence: *"The population grows
  ninefold per added element and stays 100% winnable through 15."*
  (Drop this figure if the page wants only two — A and B carry the story.)

## 4. Caveats the page must carry

- The refutation and its companion are **days old and unrefereed**
  (arXiv:2608.27416 posted 2026-08-27; 2608.19414 posted 2026-08-19; both
  disclose AI assistance). The original conjecture paper arXiv:2401.16210
  is also a preprint. This page's bound answers their open problems *as
  posed there*.
- "First lower bound" is qualified: to our knowledge as of 2026-08-28,
  based on reading all three papers in full and an arXiv full-text search
  for "non-cancelling" returning only those three; the conjecture's
  authors' own 2024 verification (ground sets ≤ 5 points, strong
  left-linear+polarity version) bounds by *point count*, which neither
  subsumes nor is subsumed by this census's *lattice size* bound (NOTE
  §7 states the incomparability precisely).
- Corollary 4 (set-family form) chains through [1]'s equivalence results
  **checked at statement level only**; their proofs were not re-verified
  here.
- The census claims nothing beyond n = 15. The upper bound ≈ 1.00011·10¹⁵
  is the smallest instance *their theorem certifies*, not the smallest
  counterexample.
- Heitzig–Reinhold / Jipsen–Lawless as the literature's route to
  enumerating lattices to n ≈ 19–20 is cited (secondary) — mentioned only
  as future-work context, no result of theirs is used.
- OEIS A000112/A006966 b-file values are used as anchors (fetched
  2026-08-28); A000112 is exact through n = 16 there, A006966 through
  n = 19.

## 5. Existing page

None — this is a new conjecture directory and a new page. After
publishing, add the page link to this conjecture's row in the top-level
README (the row itself was added by this session, without the link).
