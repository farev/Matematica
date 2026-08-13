# PAGE.md — handoff for the distinct-subset-sums page (new page)

*Written per the CLAUDE.md cloud-session contract. This is a NEW conjecture
directory; no page exists yet. Numbers marked ⟨…⟩ are finalized in the
session-close commit — trust the committed data files over prose if they
ever disagree.*

## 1. Headline claim

**CERTIFIED.** The tenth value of the Erdős distinct-subset-sums function
satisfies `⟨B⟩ < f(10) ≤ 309`: an exhaustive, cross-verified search proves
no 10-element set with all subset sums distinct has largest element `≤ ⟨B⟩`
(previous published floor: 220), while the Conway–Guy set attains 309.

## 2. Contributions

1. **CERTIFIED** — `f(10) > ⟨B⟩` (final value in `data/n10_sweep.csv`;
   every row is an independently certified `f(10) > m` statement; the
   engine's per-depth node counts are recorded per row).
2. **CERTIFIED** — full re-derivation of the known ladder
   `f(1..9) = 1, 2, 4, 7, 13, 24, 44, 84, 161` from scratch (no OEIS value
   assumed), with ALL optimal sets enumerated at each level — counts:
   ⟨per-level counts from data/optimal_sets.txt⟩; agreement with A276661
   at every level.
3. **CERTIFIED** — no witness below 309 lies near the Conway–Guy
   structure: all 19,125,539 ten-element sets whose deficiency profile is
   within L1-distance 8 of Conway–Guy's, over every maximum `m ≤ 308`,
   fail DSS.
4. **PROVED (classical method)** — exact finite second-moment floors:
   `f(10) ≥ 192`, `f(11) ≥ 362` (the latter is the standing analytic floor
   for the next open value; `f(11) ≤ 594` from Conway–Guy).
5. **NUMERICAL** — the search-tree growth law ~×1.203 per unit of maximum
   (measured 230 → 250), pricing the full `a(10)` decision at CPU-months;
   and a documented negative: simulated annealing fails its own positive
   control on this landscape (cannot rediscover the Conway–Guy set at cap
   309), so heuristic witness searches carry no evidence here.

## 3. Figure specs

1. **The ladder and the gap.** Data: `data/ladder_sweep.csv` (f-values),
   Conway–Guy values 1,2,4,7,13,24,44,84,161,309 (computed in
   `validate_set.py`). Log-scale `f(n)` vs `n` with the certified window
   `(⟨B⟩, 309]` drawn at `n = 10` as an interval, prior floor 220 marked.
   Reader's sentence: "Every value up to n = 9 is settled; at n = 10 the
   answer is now pinned between ⟨B⟩ and 309."
2. **Cost of certainty.** Data: `data/n10_sweep.csv` columns (m, nodes,
   seconds). Log-scale nodes (and seconds) vs m with the ×1.203/step fit
   drawn over the fitted range only. Reader's sentence: "Each +1 on the
   maximum multiplies the exhaustive search by about 1.2 — the remaining
   range to 309 is a wall, not a walk."
3. **Where the witness cannot be.** Data: `cg_neighborhood.py` output
   summary (19,125,539 checks, K = 8, all m ≤ 308). A schematic of
   deficiency space: Conway–Guy profile at center, L1-ball of radius 8
   shaded "empty", the exhaustive strip `m ≤ ⟨B⟩` shaded "empty", the
   rest open. Reader's sentence: "If a better-than-Conway–Guy set exists,
   it is neither small nor a tweak of Conway–Guy."

## 4. Caveats the page must carry

- Every literature citation of this session is **(secondary)**: the cloud
  sandbox could not fetch ANY primary page (arxiv, OEIS, erdosproblems,
  EJC all egress-blocked); sources were verified only through web-search
  snippet quotes dated 2026-08-13. In particular: the attribution of
  `a(9)` to J. P. Grossman, the recorded floor `a(10) > 220`, and the
  claim that only nine values were previously known all rest on snippet
  quotes of OEIS A276661 and arXiv 2502.19182.
- `f(10)` is NOT decided. The certified statement is the window
  `(⟨B⟩, 309]`, nothing stronger.
- The ×1.203 growth rate is a NUMERICAL fit over m ∈ [230, 250] only.
- The optimal-set multiplicity counts (contribution 2) are *possibly
  known* — Lunnon 1988 could not be read; treat as data, not novelty.
- Tight-mode pruning (the production engine mode) changes the search tree
  relative to the three node-count-identical exact engines; its soundness
  is proved in NOTE §3, and its statuses/solutions were verified identical
  on the full test battery, but its node counts are not independently
  replicated by construction.

## 5. Existing page

None — this is a new conjecture directory and a new page.
