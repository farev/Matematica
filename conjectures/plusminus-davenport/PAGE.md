# PAGE.md — handoff for the local page build

New page (no existing page for this conjecture).

## 1. Headline claim

**D±(C₅⊕C₁₅) = 6 — the one plus–minus weighted Davenport constant left
undetermined below order 100 by Marchan–Ordaz–Schmid in 2014 ("6 or 7") is
decided** — CERTIFIED (four independent implementations; the lower bound and
three of the five strata of the nonexistence argument PROVED by hand).

## 2. Contributions

1. **CERTIFIED** — D±(C₅⊕C₁₅) = 6: no ±-zero-sum-free 6-set exists over
   C₅⊕C₁₅; the maximum is 5. Four independent implementations: exhaustive
   DFS (139 052 nodes), full brute force over all 2 324 784 six-element
   class-subsets, a C bitset engine reproducing the DFS node count exactly
   (139 052), and a stratified enumerator finding all five kernel strata
   empty. Census of **all 85 155** maximum ±-zsf 5-sets, stratified
   3 375 / 13 500 / 29 040 / 27 960 / 11 280, with 3 375 = 135 × 25
   explained exactly by the saturation lemma.
2. **PROVED** — the lower bound D± ≥ 6 (concatenation + cyclic lemmas +
   a standalone-verified witness), and strata (4,2), (3,3), and the
   parallel half of (2,4) of the upper bound: a one-line saturation lemma,
   a sum-free classification of allowed sets of ±-zsf 3-sets in 𝔽₅²
   (60 line-type + 120 generic, hand-checkable tables), and an 𝔽₅
   projection argument ending in (1+4)−(2+3) = 0.
3. **CERTIFIED** — independent recomputation of the entire table below
   order 100: all 184 abelian group types; 167 forced by PROVED elementary
   bounds, 17 decided by search; the published anchor D±(C₉⊕C₃⊕C₃) = 6
   reproduced. Landscape: **12 of the 17 bracket-open cells attain the
   pigeonhole bound** — C₅⊕C₁₅'s lower-bound behavior is the exception,
   which is why the 2014 gap was genuinely hard to close by bounds.
4. **CERTIFIED** — apparently the first values past order 100 (novelty
   (secondary)): the complete table for orders 101–135 and targeted cells
   to order 243, including D±(C₇⊕C₂₁) = 8, D±(C₁₃⊕C₁₃) = 8 (54.45M-node
   sharded exhaustion), D±(C₅⊕C₃₀) = 8, D±(C₃⊕C₅₁) = D±(C₃⊕C₅₇) = 8 —
   and the **first cell strictly between the concatenation and pigeonhole
   bounds**: d±(C₃⊕C₃⊕C₁₅) = 6 ∈ (5,7) at order 135.
   Also **d±(C₃⊕C₄₅) = 6 < 7**: the same order 135, and it refuted the
   session's own interim conjecture (see contribution 6) within the hour —
   double-engine certified both times.
5. **PROVED** — the toolkit lemmas: pigeonhole d± ≤ ⌊log₂|G|⌋; cyclic
   d±(C_n) = ⌊log₂n⌋; quotient concatenation d±(G) ≥ d±(G/H)+d±(H);
   saturation (maximal ⇒ reachable set covers G∖{0}); exponent-3 groups:
   ±-zsf = 𝔽₃-linear independence, so d±(C₃^r) = r.
6. **Conjecture A** (new, machine-tested at every computed group, 263
   groups): for every finite abelian G, either d±(G) = ⌊log₂|G|⌋ or some
   proper direct-sum splitting attains d±(G) = d±(A)+d±(B). The noncyclic
   "atoms" below 100 are exactly C₃⊕C₃ₘ (m = 2,4,5,8,9) and C₇⊕C₇.
   An interim **Conjecture B** (C₃⊕C₃ₙ always pigeonhole-tight) was
   **refuted by the session's own sweep** at n = 15 (C₃⊕C₄₅) an hour after
   it was formulated — reported in full as the cautionary exhibit, and
   consistent with Conjecture A, which allowed both values there.
   **Conjecture C** (C₇⊕C₇ₙ tight) stands at n = 1–5, first open case
   n = 6 (order 294).

## 3. Figure specs

* **Fig. 1 — the 17 open cells below 100.** Data:
  `data/table_le100.csv` (rows with status `gap:search-decided`; columns
  lower_d/upper_d/dpm). Dot-and-bracket chart: for each group, the
  [lower, upper] bracket with the computed d± marked. Reader sentence:
  "Where the elementary bounds leave a gap, the answer is nearly always the
  top of the bracket — C₅⊕C₁₅ is one of the few that lands at the bottom."
* **Fig. 2 — the extremal census of C₅⊕C₁₅.** Data:
  `data/cert_C5xC15.json` (`maxsets`, stratify by number of elements with
  C₃-component 0 — counts 3 375/13 500/29 040/27 960/11 280). Bar chart by
  stratum. Reader sentence: "All 85 155 largest ±-zero-sum-free sets, sorted
  by how many of their five elements lie in the 5-torsion kernel — the
  rarest bar is exactly 135 × 25."
* **Fig. 3 — the landscape to order 243.** Data: `data/table_le100.csv`,
  `data/table_101_135.csv`, `data/beyond.csv` (columns order, lower_d,
  upper_d, dpm; noncyclic rows). Scatter of d± vs order with the two bounds
  as guide curves. Reader sentence: "Every computed group sits either on the
  pigeonhole ceiling or at a sum of two smaller groups' values — the
  conjectured law — with the first strictly-in-between point at order 135."

## 4. Caveats the page must carry

* **Every citation is (secondary).** The sandbox could not fetch any primary
  source (arxiv, journals, HAL, theses); all literature statements come from
  search-result snippets dated 2026-08-24. In particular the exact
  conventions and table of Marchan–Ordaz–Schmid (IJNT 2014, arXiv:1308.3316)
  were reconstructed from snippets and anchored by two reproduced published
  values (the cyclic formula; D±(C₉⊕C₃⊕C₃) = 6).
* **Novelty risk, stated plainly:** a 2021 University of Kentucky thesis
  (Perez-Lavin, *The Plus-Minus Davenport Constant of Finite Abelian
  Groups*) could not be read; if it or any unread source already decides
  C₅⊕C₁₅, the headline is an independent confirmation, not a first. Seven
  differently-phrased searches surfaced no statement of the value.
* "First values past order 100" is absence-of-evidence from snippets only.
* Theorem 1 is CERTIFIED, not PROVED: strata (2,4)-independent, (1,5), (0,6)
  rest on exhaustive computation (four implementations).
* Two order-96 2-group rows of the ≤ 100 table have node-capped search
  *confirmations*; their values are PROVED by bounds independent of search
  (recorded in the CSV status column).
* Conjecture A is machine-tested on ~250 groups, nothing more; its
  literature status is unchecked (the analogous statement for the classical
  Davenport constant fails in high rank, which makes the ± version worth a
  referee's poke).

## 5. Existing page

None. New page.
