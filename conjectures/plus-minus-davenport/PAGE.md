# PAGE.md — handoff for the plus-minus-davenport page (new page)

No page exists for this conjecture yet; this is a new build at
`fabianarevalo.com/plus-minus-davenport`.

## 1. Headline claim

**CERTIFIED** — The last unknown plus–minus weighted Davenport constant
among all abelian groups of order ≤ 100 is decided: `D±(C₅ ⊕ C₁₅) = 6`,
the lower end of the `{6, 7}` bracket left open by Marchan–Ordaz–Schmid
in 2014 (openness (secondary), see caveats).

## 2. Contributions

1. **CERTIFIED** `D±(C₅ ⊕ C₁₅) = 6` — no ±zero-sum-free 6-set exists in
   the 75-element group; exactly **85,155** extremal 5-sets, censused by
   four independent methods (C census DFS, 792,672 nodes / 0.098 s; raw
   multiset DFS, 46.7M nodes, exact `2^k` count relation; clean-room
   Python engine, digit-for-digit; decomposition case-audit), each
   extremal set re-verified free and non-extendable from the definition.
2. **CERTIFIED** `D±(C₇ ⊕ C₂₁) = 8` — the `n = 3` cell of the second
   family flagged unknown in 2013, no published value found; same
   four-path battery (raw run 17.2G nodes / 45 min).
3. **CERTIFIED** (inverse theorem) — the maximal ±free sequence of
   `C₇ ⊕ C₂₁` is **unique up to automorphisms and signs**: exactly
   `2016 = |GL(2,7)|` extremal 7-sets in a single Aut-orbit, every
   element with nonzero `C₃`-part. For `C₅ ⊕ C₁₅`: 193 orbits
   (167×480 + 17×240 + 7×120 + 60 + 15).
4. **CERTIFIED** — complete `D±` table for all **312** abelian groups of
   order ≤ 162 (data: `table_002_100.csv`, `table_101_150.csv`,
   `table_151_162.csv`): the 184 groups ≤ 100 match every
   snippet-recoverable published value/bound with zero exceptions; 15
   gap cells past 100 are new.
5. **CERTIFIED** (Theorem 12) — `D±(C₃² ⊕ C₁₅) = 7` (order 135) and
   `D±(C₃³ ⊕ C₆) = 7` (order 162) lie **strictly between** the
   Marchan–Ordaz–Schmid bounds `{6, 8}`: the constant is not always at
   an endpoint of the general bounds. Battery: second-encoding census,
   raw runs (5.66G / 7.48G nodes) with exact `2^k` relations, verified
   witnesses; Python census for the 135 middle cell.
6. **CERTIFIED** — `D±(C₃ ⊕ C₄₅) = 7` (order 135): first lower-bound
   cell of the `C₃ ⊕ C₃ₙ` family after ten consecutive upper-bound gap
   cells (n = 2..11); carries the ⚠ caveat below.
7. **PROVED** (elementary, in-house) — sign-class model; `L(C_p^r) = r`
   for `p ∈ {2,3}`; product superadditivity; binary pigeonhole upper
   bound `D± ≤ ⌊log₂|G|⌋ + 1`; exact cyclic value; the `F₅² ⊕ Z₃`
   reduction lemma; saturation of maximal free sets; case (4,2) of the
   headline nonexistence. These prove every bounds-coincide cell of the
   table without any computation.

## 3. Figure specs

- **F1 — the landscape.** Scatter `|G|` (x, 2..162) vs `D±(G)` (y), one
  point per group (312 points), with the binary upper bound
  `⌊log₂ x⌋ + 1` as a step curve; color points by attribution
  (bounds-coincide / upper / lower / **middle**), starring the two
  middle cells (135, 162) and `C₅⊕C₁₅`. Data: the three `table_*.csv`
  (columns `order`, `invariant`, `DPM`; bounds recomputable as
  `sum(floor(log2 d_i)) + 1` and `floor(log2 order) + 1`), attribution
  in `analysis_2_162.txt`. Reader sentence: *"Every abelian group up to
  order 162 sits on one of the two classical bounds — except two, at
  orders 135 and 162, which sit strictly between them."*
- **F2 — the unique extremal configuration.** For `C₇ ⊕ C₂₁ ≅ F₇² ⊕ Z₃`:
  a 7×7 grid (the `F₇²` parts) marking the seven elements of the unique
  orbit's representative, each cell labeled by its `Z₃`-part; caption
  notes all seven have nonzero `Z₃`-part and the orbit count 2016 =
  |GL(2,7)|. Data: `classify_7_21.txt` (representative, orbit size),
  `enum_7_21_size7.txt`. Reader sentence: *"Up to the group's symmetries
  and sign flips, there is exactly one way to build the longest
  ±zero-sum-free sequence over C₇⊕C₂₁."*
- **F3 — a family with a dent.** Line/step plot of `D±(C₃ ⊕ C₃ₙ)` for
  `n = 2..18` against both bounds, showing the value riding the upper
  bound at every gap cell until it drops to the lower bound at `n = 15`
  (order 135). Data: family rows in `analysis_2_162.txt` (or filter the
  CSVs on invariant `3+3n`). Reader sentence: *"The family follows the
  upper bound for a decade of cases, then dips at n = 15."*

## 4. Caveats the page must carry

- **Every literature citation is (secondary).** The session's sandbox
  could not fetch any primary source (arXiv/HAL/publisher all
  egress-blocked); all statements about Marchan–Ordaz–Schmid (IJNT
  2014), Adhikari–Rath (2006), the 2017 survey, the Perez-Lavin thesis
  (2021), and Merito–Ordaz–Schmid (arXiv:2506.14279) come from
  search-result snippets dated 2026-08-22. NOTE §1/§7 lists them.
- **Openness of the two headline cells** rests on: the 2014 bracket
  sentence (near-verbatim via two independent queries), its 2021 thesis
  restatement, and 27 fruitless resolution-searches (11 aimed directly).
  A resolution could exist in the unreadable full texts. The page should
  say "as far as we could check" and link the NOTE's search log.
- ⚠ **Do not present `D±(C₃⊕C₄₅) = 7` as contradicting MOS** — a
  search-engine paraphrase of their family theorem says "matches the
  upper bound for n ≥ 2", but paraphrases drop hypotheses; the paper
  must be read first (NOTE §5, §8). Present it as "our value, in tension
  with a paraphrase, pending the primary source".
- The two 1800 s-timeout cells (`C₂⁵⊕C₄`, `C₂⁵⊕C₅`) carry lemma-proved
  values (bounds coincide) but no census counts.
- Beyond-162 spot cells (`C₇⊕C₂₈`, `C₁₄²`, `C₅⊕C₃₅`) have a lighter
  verification tier: single census + verified witness (no second
  encoding / raw run). `C₅⊕C₃₅` is additionally lemma-forced.
- The middle-value claim is "the only two such groups **of order ≤ 162**"
  — no claim past 162.
- AI assistance (Claude) per repository policy; disclosed in NOTE.

## 5. Existing page

None — new page.
