# PAGE.md — handoff for the local publish pass

New conjecture directory; no page exists yet. Flat path per convention:
`fabianarevalo.com/plus-minus-davenport`.

## 1. Headline claim (one sentence, labelled)

**CERTIFIED** — The last open plus-minus weighted Davenport constant at
order ≤ 100 is decided: `D±(C₅ ⊕ C₁₅) = 6`, the single value
Marchan–Ordaz–Schmid's 2014 paper could not determine ((secondary)), and
with it four more smallest-open family cases: `D±(C₇ ⊕ C₂₁) = 8`,
`D±(C₃ ⊕ C₄₅) = 7`, `D±(C₅ ⊕ C₅₅) = 8`, `D±(C₃ ⊕ C₈₇) = 8`.

## 2. Contributions (numbered, labelled, with the numbers)

1. **CERTIFIED** `D±(C₅⊕C₁₅) = 6` (MOS box {6,7}): no dissociated 6-set in
   C₅⊕C₁₅ — three independent implementations (136,464-node signed-sum
   exhaustion; 3,505,201-node definitional exhaustion with no shared
   reductions; clean-room Python), witness (0,1),(0,2),(0,4),(1,0),(2,0)
   for the lower bound, and the exact cross-check
   85,155 × 2⁵ = 2,724,960 between engines.
2. **CERTIFIED** `D±(C₇⊕C₂₁) = 8`: counting bound attained, only by mixed
   witnesses (split constructions stall at 6); exactly 2016 maximum
   dissociated 7-sets up to sign normalization (16.4M nodes).
3. **CERTIFIED** `D±(C₃⊕C₄₅) = 7`: the first open case (n = 15) of the
   C₃⊕C₃ₙ family is a genuine *deficit* — counting allows 8, the truth is
   the split bound 7; exhaustions of 8.2M nodes (signed engine) and
   361.7M nodes / 6.99B extension tests (definitional engine).
3b. **CERTIFIED** `D±(C₅⊕C₅₅) = 8`: n = 11 of the C₅⊕C₅ₙ family, a *second*
   deficit in that family (so C₅⊕C₁₅ is not the only one) — a complete
   3.49-billion-node exhaustion sharded over four disjoint root ranges.
3c. **CERTIFIED** `D±(C₃⊕C₈₇) = 8`: the n = 29 failing-block case, a deficit
   (2.03-billion-node exhaustion). This is the case that **separates
   Conjecture D′ from its Sylow-split variant** — dis = 7 is the
   invariant-factor bound L, but neither the Sylow split (6) nor the
   counting bound (8), so the Sylow phrasing is refuted and D′ survives;
   the separating group was chosen and the run launched before the outcome
   was known.
4. **CERTIFIED** census: all **184** abelian groups of order ≤ 100 from
   scratch (226 CPU-s); exactly **five** deficit groups: C₃², C₃³, C₃⁴,
   C₃²⊕C₉, C₅⊕C₁₅.
5. **PROVED** Theorem T1: `D±(C₃⊕C₃ₙ) = ⌊log₂ 9n⌋ + 1` whenever
   2^{⌊log₂ 9n⌋ − 3} ≤ n (ladder + 3 spread points + rotation; presumptive
   rediscovery of the MOS Thm 4.4 regime, marked as such). Combined with
   the machine values at the failing blocks (15 and 29 deficit; 30, 31
   attain via five-point witnesses), **the family C₃⊕C₃ₙ is now determined
   for every n ≤ 56** — deficits exactly at n = 1, 15, 29 — and its first
   open case moves from n = 15 to n = 57.
6. **NUMERICAL (Conjecture D′, dichotomy)**: on every computed group —
   184/184 in the census plus every value beyond — dis(G) equals either
   the counting bound ⌊log₂|G|⌋ or exactly the Marchan–Ordaz–Schmid lower
   bound L(G) = Σᵢ⌊log₂ dᵢ⌋ (invariant factors): **their lower and upper
   bounds are never both strict**. Zero strictly-between cases.
7. **PROVED** small theory: the two-line equivalence D± = dis + 1; the
   fiber-counting Lemma F with corollaries (any 6-set in C₅⊕C₁₅ needs ≥ 3
   elements off the C₅²-fiber; any 7-set in C₃⊕C₄₅ needs ≥ 5 off-fiber and
   Lemma F misses by exactly one element — why the case resisted).
8. **CERTIFIED** E± corollaries via the GMO identity ((secondary)):
   E±(C₅⊕C₁₅) = 80, E±(C₇⊕C₂₁) = 154, E±(C₃⊕C₄₅) = 141.

## 3. Figure specs

1. **The census scatter.** Data: `data/census.csv`. x = |G| (2…100),
   y = dis(G), one point per group, the curve ⌊log₂ x⌋ drawn, the five
   deficit groups marked in a second color and labelled. Reader sentence:
   "Almost every abelian group packs a dissociated set of the maximum size
   counting allows — at order ≤ 100 exactly five groups fall short, and
   the one nobody could decide since 2014 (C₅⊕C₁₅) is one of them."
2. **The C₃⊕C₃ₙ family strip.** Data: `data/families.csv` rows 3×3n plus
   NOTE §6 table. x = n (1…56), y = dis; theory-covered n shaded (T1),
   failing-block n outlined, the three deficits n = 1, 15, 29 in red.
   Reader sentence: "A half-page construction settles the whole family for
   every n ≤ 56 except a handful of fractional-part windows — and inside
   those windows sit the three values that genuinely break the pattern."
3. **Witness anatomy at C₇⊕C₂₁.** Data: witness in
   `data/c7c21_certificate.txt`, drawn on the 7×21 torus grid with the
   split construction alongside. Reader sentence: "The split construction
   gives six; nothing built from one coordinate at a time reaches seven —
   the maximum lives only in genuinely two-dimensional configurations."

## 4. Caveats the page must carry

- Every literature citation is **(secondary)** — snippet-derived, primary
  PDFs unreachable from the sandbox. Named prominently: MOS 2014
  (arXiv:1308.3316), the openness statements, the MOS Thm 4.4 condition,
  the GMO E± identity, the cyclic formula's attribution.
- **Perez-Lavin 2021 U. Kentucky thesis**: scope ("orders that are a
  product of two prime powers") brushes 75 = 3·5²; snippets still call
  C₅⊕C₁₅ open, but the thesis must be read before the page claims
  priority. Say "decided here; if the thesis or the paywalled Adhikari
  2017 survey already contains it, this is an independent confirmation".
- Upper bounds at the three headline groups are exhaustive computations
  (CERTIFIED), not proofs; T1 is proved but is a presumptive rediscovery
  of the MOS regime; Conjecture D is data (NUMERICAL), verified only in
  computed range.
- The census's "five deficit groups" statement is exhaustive for order
  ≤ 100 only.

## 5. Existing page

None — new conjecture, new row in the top-level index.
