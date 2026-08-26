# PAGE.md — handoff for the site build (new page)

Proposed path: `fabianarevalo.com/strong-truncations` (flat path per
site convention). No existing page: build fresh.

## 1. Headline claim

Kardoš's 2025 question "is every diamond-free claw-free cubic graph
strongly 6-edge-colorable?" has a negative answer: a proved local
obstruction (**PROVED**, the Balloon Lemma) produces an 18-vertex
counterexample G₁₈ with strong chromatic index 7 (**CERTIFIED**:
DRUP-checked UNSAT at six colors plus a verified 7-coloring), unique at
its order, with counterexamples at every admissible order above —
while the census says the *intended* reading (truncations of simple
cubic graphs) survives everywhere it was tested.

## 2. Contributions

1. **PROVED — Balloon Lemma.** If a cubic multigraph H contains a
   *balloon* (a doubled edge whose two endpoints share their third
   neighbour — the expanded form of a loop), the truncation T(H) has no
   strong 6-edge-coloring. Ten-line palette argument in a dart
   reformulation (also PROVED) of strong 6-colorings of truncations;
   machine cross-check: the balloon piece admits 0 of 60 conceivable
   boundary states.
2. **CERTIFIED — G₁₈.** The truncation of the 6-vertex quotient with
   doubled edges 1‖3 (tied at 5) and 2‖4 (tied at 0): an 18-vertex
   connected claw-free diamond-free cubic simple graph, graph6
   `Q??CA?_cAOA_DC@`PO@OOOW?`_?`, with χ′ₛ = 7 — UNSAT at 6 colors with
   a 4200-line DRUP proof verified by an independent from-the-definition
   checker, verified 7-coloring, and two independent enumeration
   pipelines (all 41,301 cubic graphs on 18 vertices filtered by
   definition vs. quotient generation + truncation) converging on the
   same graph. It is the **unique smallest** such graph; the classical
   exception, the prism, has χ′ₛ = 9.
3. **PROVED + CERTIFIED — infinite family.** Chain quotients (two
   balloons joined through k dumbbells) give counterexamples on
   18 + 6k vertices for every k ≥ 0 (χ′ₛ ≥ 7 proved for all k; = 7
   certified for k ≤ 8) — and diamond-free claw-free cubic graphs exist
   only at orders 4 and multiples of 6, so every admissible order ≥ 18
   carries a counterexample. All previously published graphs attaining
   Lin–Lin's tight bound 7 contain diamonds (secondary): diamonds are
   not needed.
4. **CERTIFIED — census with an exact empirical law.** All 36,093
   truncations of connected cubic loopless multigraphs of order ≤ 16
   decided by two independent engines with per-instance
   definition-checked certificates: 29,787 have χ′ₛ = 6 (verified
   witness + conflict 6-clique each), 6,305 have χ′ₛ = 7 (independent
   UNSAT at 6 + verified 7-coloring each; counts by order 1, 4, 19,
   102, 682, 5497), one (the prism) has χ′ₛ = 9. **χ′ₛ = 7 occurs
   exactly on the quotients containing a balloon** — zero exceptions
   either way. Conjecture: this is the complete characterization.
5. **CERTIFIED — the intended reading survives.** Every truncation of a
   connected **simple** cubic graph on ≤ 20 vertices — 556,471 graphs,
   truncations up to 60 vertices — is strongly 6-edge-colorable
   (509,950 order-20 witnesses re-verified from the definition in
   session; 539 engine-capped instances SAT-resolved). First
   systematic verification beyond Han–Cui's truncated prisms
   (secondary).

## 3. Figure specs

* **F1 — the counterexample.** Draw G₁₈ from its graph6 string
  `Q??CA?_cAOA_DC@`PO@OOOW?`_?` (also `certs/G18_7col.txt` carries the
  edge list), ideally with the six triangles shaded and the two
  balloon pieces visually grouped, colored by the verified 7-coloring
  in the same file. Reader's sentence: "This 18-vertex graph is the
  smallest diamond-free claw-free cubic graph that cannot be strongly
  edge-colored with six colors."
* **F2 — the balloon mechanism.** Schematic of a balloon (doubled edge
  u‖v, both third edges into w, stem s) with the forced palette
  structure from NOTE §2 Step 2–3 annotated ({p,q} forced on the
  doubled pair, nowhere to live at w). Reader's sentence: "A doubled
  edge forces two colors, and a shared neighbour gives those two colors
  nowhere to go."
* **F3 — census bars.** Per quotient order 6–16, stacked counts of
  χ′ₛ = 6 vs χ′ₛ = 7 truncations (data: the order table in NOTE §4 /
  `data/census*.txt`: totals 6, 20, 91, 509, 3608, 31856 with 1, 4, 19,
  102, 682, 5497 sevens). Reader's sentence: "By order 16 about one in
  six truncations needs seven colors — and every single one contains a
  balloon."

## 4. Caveats the page must carry

* Every literature citation is **(secondary)**: the sandbox could not
  reach arXiv/OEIS/erdosproblems/MathOverflow; Kardoš's problem
  statement, Lin–Lin's theorem and tight examples, and Han–Cui's result
  were reconstructed from search snippets on 2026-08-26. The primary
  sources must be read before this page claims novelty outright; the
  page should say the result is "new as far as a snippet-level search
  can tell".
* The two phrasings of Problem 4.1 differ: the counterexamples are
  truncations of cubic **multigraphs** (the diamond-free claw-free
  class per the structure lemma); the "χ′ₛ(T(G)) for cubic G" phrasing
  with G *simple* excludes them, and the census supports that reading
  (all simple quotients ≤ 20 colorable). The page must not blur this.
* χ′ₛ = 7 (rather than ≥ 7) for the infinite family beyond k = 8 uses
  Lin–Lin's upper bound (secondary); every census instance's = 7 is
  certified independently of it.
* The characterization "7 ⟺ balloon" is a conjecture: balloon ⇒ 7 is
  proved; balloon-free ⇒ 6 is open, verified computationally for all
  317,246 balloon-free quotients of order ≤ 18 (order 18 by the lighter
  protocol: engine-decided with verified witnesses plus SAT-resolved
  caps; balloon side by the lemma with a 500-sample check).
* "Unique smallest" is relative to the prism exception (χ′ₛ = 9),
  which is classical (secondary).
