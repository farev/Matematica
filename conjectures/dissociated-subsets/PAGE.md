# PAGE.md — handoff for the site page `fabianarevalo.com/dissociated-subsets`

New page (no page exists for this conjecture). Check the README's status line for the
`k = 5` runs before building: it may add one line to contribution 3.

## 1. Headline claim

**CERTIFIED** — Erdős Problem #963: every 7 distinct positive reals contain a subset of
4 with all subset sums distinct (and 6 need not), which through a one-line reduction
settles Erdős's question "is `f(n) ≥ ⌊log₂ n⌋`?" for every `n ≤ 31` and gives `f(n)`
exactly for `n ≤ 27` — the first exact values of this 1965 function.

## 2. Contributions

1. **PROVED.** `f(n) = g(⌈(n−1)/2⌉)`, where `g(m)` is the same minimum over sets of `m`
   distinct positive reals (sign flips and zero never help a dissociated subset). Hence
   Erdős's inequality holds for all `n` iff every `2^{k−1}` distinct positive reals
   contain a dissociated `k`-subset, for every `k`. Nobody on the problem page had used
   this; it turns the page's `f(13) ≤ 4` into `f(13) = 3`.
2. **CERTIFIED.** `m₄ = 7`: every 7 distinct positive reals contain a dissociated
   4-subset; `{1,2,3,4,5,6}`, `{1,2,3,5,7,8}` and one-parameter families through them
   have none. Four independent exact engines (case trees of 290, 1099, 111, 62 nodes)
   agree; three of the trees are JSON certificates verified by an independent checker
   (`data/checker_log.txt`).
3. **PROVED (given 2).** `f(n) = 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, …, 4` for
   `n = 1, …, 27`; `f(n) ≥ ⌊log₂ n⌋` for all `n ≤ 31`; equality for `n ≤ 13` and
   `16 ≤ n ≤ 27`, strict at `n = 14, 15`. For `k = 5`: `14 ≤ m₅ ≤ 41`, with sets of every
   size `m ≤ 13` having no dissociated 5-subset (CERTIFIED witnesses).
4. **CERTIFIED.** `A₂₄ = {1,…,21,24,25,27}` has no dissociated 6-subset (all 134 596
   six-subsets checked by two programs): `m₆ ≥ 25`, one more than the interval bound.
5. **PROVED.** The signed-sum lemma: every element of a set with no dissociated
   `k`-subset is `±t₁ ± … ± t_{k−1}` (some signs zero) for any dissociated
   `(k−1)`-subset — the structure that makes the `k = 5` searches four-dimensional.

## 3. Figures

1. **Data:** `data/witnesses.txt` (the 6-element sets) and NOTE §4. *Sentence:* "Six
   numbers can be arranged so that every four of them satisfy a coincidence like
   1 + 2 = 3 or 3 + 6 = 4 + 5; seven never can."
2. **Data:** the table in NOTE Cor. 4.2 (`f(n)` vs `⌊log₂ n⌋`, `n ≤ 31`). *Sentence:*
   "Erdős's guess `⌊log₂ n⌋` is exactly right up to 27 except at 14 and 15, where the
   truth is one larger."
3. **Data:** `certs/D_k4_m7.json` rendered as a tree (62 nodes; split on the four
   smallest elements, six relation branches plus the dissociated branch).
   *Sentence:* "The whole proof is this case tree, and a separate program checks every
   node."
4. **Data:** the thresholds `m_k = 1, 2, 4, 7`, `14 ≤ m₅ ≤ 41`, `25 ≤ m₆ ≤ 122` against
   the Conway–Guy values `F(k) = 1, 2, 4, 7, 13, 24` and `2^{k−1}` (NOTE §7).
   *Sentence:* "So far the threshold tracks the distinct-subset-sums numbers, well below
   the powers of two Erdős asked about."

## 4. Caveats the page must carry

- The `k = 4` theorem is CERTIFIED (machine case analysis with checked certificates),
  not PROVED by a written argument.
- `F(7..9)` are cited from OEIS A276661 (Lunnon, Grossman; secondary); the original
  Erdős and Vaughan sources ([Er65], [Va99]) were not consulted.
- The problem page's status: OPEN, but Bloom wrote in January 2026 that KoishiChan's
  asymptotic argument "looks good" — the asymptotic `(1−o(1)) log₂ n` is settled in
  that sense; what this session settles is the exact inequality in a range and the exact
  values.
- The annealing hedge's failure to find 14-sets with `d ≤ 4` or 25-sets with `d ≤ 5`
  is heuristic (NUMERICAL).
- `k = 5` exhaustive status: see the README (single engine, if completed).

## 5. Existing page

None.
