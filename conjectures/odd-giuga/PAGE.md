# PAGE.md — handoff for the odd-giuga write-up page

New page (no existing page for this conjecture). Flat path:
`fabianarevalo.com/odd-giuga`.

## 1. Headline claim

**Every odd Giuga number, and every odd primary pseudoperfect number, has
at least 14 prime factors** — CERTIFIED (exhaustive exact computation
through 12 factors) + PROVED (a parity lemma excludes 13, and proved
reductions make the computation cover both families).

## 2. Contributions

1. **Odd Giuga bound, ≥ 14 prime factors** — CERTIFIED + PROVED. Equals
   the recorded bound (secondary: attributed to Borwein–Borwein–Borwein–
   Girgensohn 1996, computed in Maple, code never published; the
   companion repository of the 2013 successor paper has been an empty
   "Coming Soon" since 2014). To our knowledge the first open,
   reproducible, certificate-carrying derivation.
2. **Odd primary pseudoperfect / all-prime odd Znám bound, ≥ 14 prime
   factors** — CERTIFIED + PROVED, and apparently **new**: the strongest
   recorded statement located is ≥ 9, the trivial consequence of
   Butske–Jaje–Mayernik's 2000 census (secondary).
3. **Both defining equations exhausted for every m ≤ 12** (empty):
   `Σ 1/pᵢ − 1/n = 1` and `Σ 1/pᵢ + 1/n = 1` over sets of m distinct odd
   primes — 242,828 nodes and 28,131,218,255 closure candidates at
   m = 12 per sign, 117 s each on 4 cores. PROVED lemmas: odd solutions
   have an even number of prime factors (excludes m = 13); below 1412
   odd factors these equations capture exactly the Giuga numbers / PPNs.
4. **Both published even censuses reproduced from scratch, exactly** —
   CERTIFIED: the 12 known Giuga numbers are the complete census to 8
   factors (the three 8-factor ones found in 512 s), and the 8 known
   PPNs likewise (510 s); a deliberately independent from-definition
   verifier passes 29/29 solution sets; a clean-room second engine
   agrees on both censuses to m = 6 and on odd emptiness to m = 11.
5. **The m = 13 wall, quantified** — the reason "≥ 16" was not reached:
   the odd m = 13 tree contains three-primes-left nodes of deficit
   ~10⁻⁹ whose closures cost ~10¹⁵⁻¹⁶ kernel candidates in total,
   against 2.8×10¹⁰ for all of m ≤ 12 (a live monster node with prefix
   3·5·7·11·13·17·19·23·967·101429·679364479 and a single window of
   width 3.3×10¹³ is preserved in NOTE §3.1). This also argues the
   recorded 1996 "14" cannot have been a plain odd-tree exhaustion —
   discussed carefully, with both readings, in NOTE §3.1.
6. **The 9-factor census attempt closed the story instead of a table**:
   the even m = 9 stratum hits the identical near-fill wall (live worker
   profile: prefixes 2·3·7·43·1811·≈654371·≈1.8×10⁹, two-primes-left
   windows of width ~10¹², ~10⁸-prime fanouts), putting it ~10⁵× beyond
   the complete m = 8 census. Together with contribution 5 this says the
   1996/2000 census horizon at 8 factors was *structural* — the
   branch-and-close method itself runs out exactly there, on both the
   odd frontier and the even census — which is the page's closing
   argument, not a loose end.

## 3. Figure specs

- **Figure 1 — the rungs and the wall.** Log-scale bar chart of total
  closure-candidate counts per rung m = 10, 11, 12 from
  `results/odd_giuga_official.jsonl` (`t2_width_sum`: 1,974 · 1,016,502 ·
  28,131,218,255), with a hatched estimated bar ~10¹⁵⁻¹⁶ at m = 13 (NOTE
  §3.1). Reader's sentence: "each rung costs about a thousand times the
  one before, and the 13th is off the chart — that is why the bound
  stops at 14."
- **Figure 2 — where the two families stand.** Two horizontal frontier
  bars (Giuga / PPN): factor counts 1..14+, shaded "empty, certified"
  through 12, hatched at 13 ("excluded by parity"), open beyond 14, with
  the previous records marked (14 secondary / 9). Data: results 1–2
  tables in `README.md`. Reader's sentence: "below 14 prime factors
  there is nothing odd in either family — and for pseudoperfect numbers
  that is five factors further than anyone had shown."

No other figures; contribution 6 is prose (its numbers live in Figure 1's
m = 13 bar and NOTE §3.1).

## 4. Caveats the page must carry

- Every literature statement is (secondary): this sandbox could not open
  arxiv.org, oeis.org, Wikipedia, MathWorld or any paper; records and
  openness claims were triangulated from search-result snippets. In
  particular: the attribution of the odd "14" to BBBG 1996, the BJM 2000
  census, the OEIS A007850/A054377 term lists (independently re-derived
  here), the BMS 2013 record (≥ 4771 factors for conjecture
  counterexamples), and the 2026 activity on the even PPN side
  (Wang arXiv:2605.21518; Alekseyev's 10²⁴ exhaustion).
- The bounds hold for the stated families; counterexamples to Giuga's
  primality conjecture satisfy strictly stronger conditions and their
  dedicated record (≥ 4771 factors, secondary) is far beyond ours.
- Engine primality is GMP probable-prime — one-sided in the safe
  direction; the only completeness-relevant use (divisor-route factor
  verification) reported zero factors ≥ 2⁶⁴ across all official runs
  (`bpsw_factors`), keeping everything inside the verified BPSW range
  (secondary: Feitsma–Galway).
- The m ≥ 10 odd trees coincide node-for-node between the two equation
  signs (ε shifts every bound by less than an integer there); the m ≤ 9
  trees differ and the censuses distinguish the signs decisively.
- "First open certified derivation" (contribution 1) is a claim about
  availability of code and certificates, not priority of the constant.

## 5. Existing page

None — this is a new conjecture directory and a new page.
