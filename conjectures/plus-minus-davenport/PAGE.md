# PAGE.md — handoff for the local publish pass (new page)

No page exists for this conjecture yet; this is a **new** page,
`fabianarevalo.com/plus-minus-davenport`, to be linked from the
top-level README row and the conjecture README header.

## 1. Headline claim

**CERTIFIED** — the two smallest reported-open plus–minus weighted
Davenport constants are decided: `D±(C₅⊕C₁₅) = 6` and
`D±(C₇⊕C₂₁) = 8`; the first misses the counting bound, the second
attains it with an extremal set unique up to symmetry.

## 2. Contributions

1. **CERTIFIED** `D±(C₅⊕C₁₅) = 6` — reportedly the last unresolved
   group of order ≤ 100 ((secondary), see caveat 1): no dissociated
   6-set exists in the order-75 group. Three independent exhaustions:
   two node-count-identical DFS engines (136 463 nodes) and a
   from-scratch enumeration of all C(37,6) = 2 324 784 subsets; plus a
   fourth check — none of the 85 155 maximum 5-sets extends.
2. **CERTIFIED** `D±(C₇⊕C₂₁) = 8` — a dissociated 7-set packs
   2⁷ = 128 subset sums into 147 slots; enumeration of all
   C(73,7) = 1 629 348 612 subsets finds exactly **2016** such sets,
   and they form a **single orbit** of Aut(G) (order 4032, −id acting
   trivially): the extremal packing is unique up to automorphism.
3. **CERTIFIED/PROVED** first census of the maximum dissociated-set
   size (= D± − 1) for **all 493 abelian groups of order ≤ 255**:
   484 attain the counting bound ⌊log₂|G|⌋; the 9 deficient groups are
   catalogued exactly (table in NOTE.md §3). Verified two-engine with
   exact node-count equality on all 184 groups of order ≤ 100.
4. **CERTIFIED** beyond 255: `C₅⊕C₅₅` (order 275) is deficient
   (D± = 8; full exhaustion, 3 487 686 656 nodes, 25.6 min) while
   `C₇²⊕C₉` (order 441) attains (D± = 9; witness after 740 741 480
   nodes). The C₅² family fails its windows, the C₇² family attains
   them — twice each, unexplained.
5. **PROVED** the family `D±(C_p⊕C_{3p})` is `⌊log₂ 3p²⌋ + 1` for
   every prime `p ≤ 17`, with `p = 5` the unique exception (value 6,
   one below the bound); of the 25 primes < 100, 13 are pinned by the
   sandwich argument and 12 are genuine windows, open from `p = 19` up.
6. **Open problem posed** (NOTE §4): characterize the deficient
   groups. The census shows the answer is not a density threshold
   (failure at packing density 0.948, success at 0.871), and two
   groups (`C₃³⊕C₅`, `C₂⊕C₃⁴`) have *neither* classical bound tight.

## 3. Figure specs

- **Fig 1 — attainment map.** Data: `census.csv` (columns order,
  group, lb, cap, lmax). Plot all 493 groups (x = order, y = cap −
  lmax, jittered or stacked per order), highlighting the 9 deficient
  groups by name. Reader sentence: *"Below order 256, all but nine
  abelian groups contain a full binary ladder — and the nine
  exceptions follow no obvious rule."*
- **Fig 2 — rigidity vs abundance.** Data: `orbit_147.out`,
  `orbit_75.out` (orbit counts and sizes). Two panels: order 147 —
  2016 maximum sets, one orbit; order 75 — 85 155 maximum sets, 193
  orbits (size distribution 15–480). Reader sentence: *"When the bound
  is attained the extremal set is unique up to symmetry; when it
  fails, near-maximum sets are everywhere."*
- **Fig 3 — the window primes.** Data: `familydata.csv` (p, t =
  p/2^⌊log₂p⌋, pinned, status). Number line t ∈ [1,2) with the two
  window intervals (2/√3, 4/3) and (2√2/√3, 2) shaded, primes < 100
  plotted at their t, with p = 5 (deficient) and p = 7 (attained)
  marked in contrasting colors. Reader sentence: *"A prime lands in a
  shaded window exactly when arithmetic alone cannot decide its
  constant — and the two windows decided so far went opposite ways."*

## 4. Caveats the page must carry

1. **Openness is secondary-sourced.** The sandbox could not reach any
   primary source (arXiv, HAL, publisher, Wayback all egress-blocked).
   That `D±(C₅⊕C₁₅)` and `D±(C₇⊕C₂₁)` were open rests on two
   independent search snippets of the literature around
   Marchan–Ordaz–Schmid (IJNT 10 (2014) 1219–1239): "all groups up to
   order 100 (except one)" and "unknown already for n = 3". Before the
   page goes live, check the actual paper and the CANT-II survey
   (Springer 978-3-319-68376-8_1); if either value is in print, reframe
   as independent certification + extremal structure.
2. **CERTIFIED ≠ PROVED.** The two headline values and the census
   search cells are exhaustive-search results with reproducible logs
   and witnesses, not human proofs. PROVED applies only to: Lemma E,
   Proposition B (both elementary, not claimed new), Theorem T3 (not
   new), pinned census cells, and Corollary F's assembly.
3. Corollary F claims `p ≤ 17` only; window primes ≥ 19 are open
   (`C₁₉⊕C₅₇`, order 1083, was still under witness search at session
   end — see run_1083.log / the log's Next section for final status).
4. The 2016-set uniqueness statement is at the level of ±-class sets
   (identifying g with −g), with Aut acting through
   GL(2,7) × Aut(C₃).
5. Every number on the page has an emitting script in
   `conjectures/plus-minus-davenport/` (see README table); timings are
   single-threaded on a 4-core sandbox.
