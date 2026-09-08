# PAGE.md — handoff for the site page `fabianarevalo.com/equitable-total-colorings`

New page (no page exists for this conjecture).

## 1. Headline claim

**CERTIFIED** — Question 7.1 of arXiv:2609.05259 (Adauto, de Figueiredo, Sasaki,
Schneider, 4 Sep 2026) has a negative answer: the smallest Type 1 cubic graphs with no
equitable 4-total colouring have order 16, not 20 — there are exactly 16 of them at
order 16 and 7 at order 18, with checked proofs.

## 2. Contributions

1. **CERTIFIED.** Among the 45 982 connected cubic graphs of order ≤ 18, exactly 23 are
   Type 1 (4-total-colourable) with `χ''_e = 5` (no 4-total colouring has colour classes
   of sizes differing by ≤ 1): 16 of order 16, 7 of order 18 (three bipartite); every
   Type 1 cubic graph of order ≤ 14 has an equitable 4-total colouring. Every "no
   equitable colouring" verdict has a DRUP proof checked by the repository's own checker
   (46 proofs, with and without symmetry breaking), every witness was verified
   independently, and a SAT-free enumerator agrees on all 23.
2. **CERTIFIED.** The Type 1 / Type 2 census of connected cubic graphs of order ≤ 18:
   Type 2 counts 1, 1, 1, 10, 25, 48, 227, 2103 (all Type 2 verdicts DRUP-certified).
3. **CERTIFIED.** Every 4-total colouring of each order-16 counterexample has colour
   class sizes (11,10,10,9) — between 16 and 240 colourings per graph, all enumerated —
   matching the paper's Theorem 5.3.
4. **Partial (certified per graph).** At order 20, 3 of 10 generator classes
   (161 130 graphs) hold 20 more such graphs, all with sizes (14,12,12,12) like the
   paper's `R`.

## 3. Figures

1. **Data:** `data/cx_n16.g6` (16 graph6 strings). *Sentence:* "These are the sixteen
   smallest cubic graphs that can be totally 4-coloured but never evenly."
   (Draw a few; the two with a bridge are the natural ones to show.)
2. **Data:** the per-order table in NOTE §3 (`data/summary_n*.json`). *Sentence:*
   "Up to 14 vertices every 4-colourable cubic graph can be coloured evenly; at 16 and
   18 a handful cannot."
3. **Data:** `data/brute_cx16_all.txt` (colouring counts and configurations).
   *Sentence:* "Every one of the 16-vertex exceptions has all its 4-colourings of shape
   11-10-10-9: one colour class is always one element too big."

## 4. Caveats the page must carry

- Priority is unchecked: Adauto's 2022 M.Sc. dissertation and Stemock's work were not
  accessible; the paper says the orders ≤ 18 had not been checked.
- `R` was reconstructed from Figure 1 of the paper; its isomorphism with the graph of
  Dantas et al. (DAM 2016, secondary) is not verified — only its stated properties.
- Connected graphs only (the paper's own reduction, quoted in NOTE §1).
- Order 20 is a partial census (31.6 %); Type 2 verdicts there carry no proofs.
- Type 2 counts were not compared with the literature.
- SAT witnesses were verified but not stored (regenerable in 7 minutes).

## 5. Existing page

None.
