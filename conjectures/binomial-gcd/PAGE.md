# PAGE.md — handoff for fabianarevalo.com/binomial-gcd

New page (no page exists for this conjecture yet). Link the top-level
README row and this conjecture README's header to it when live.

## 1. Headline claim (one sentence)

**CERTIFIED** — Two new exceptional triples for Erdős problem #699 (pairs
of binomial coefficients in the same row whose gcd is a pure power of 2),
at n = 2⁴¹ and n = 2⁶⁷ — the largest known, the first found since January
2026, and the 2⁶⁷ one *predicted by a density model before it was found*.

## 2. Contributions (numbered, labelled)

1. **CERTIFIED.** (2⁴¹, 2, 285920731515) is a tight triple:
   gcd(C(2⁴¹,2), C(2⁴¹,285920731515)) is a power of 2, so the
   Erdős–Szekeres "p > i" strengthening fails there and only p = i = 2
   works. n ≈ 2.2·10¹², ~200,000× beyond the previous largest known
   (1,594,324). j is unique at (2⁴¹, 2) among 9.07·10⁷ candidates
   (dual-codebase scans). Verified by a standalone checker.
2. **CERTIFIED.** (2⁶⁷, 2, 23206563898901803639), n ≈ 1.5·10²⁰ — found by
   prediction: the exact density model flagged k = 67 (E₆₇ = 1.85, the
   largest undecided value) before enumeration; 2⁶⁷−1 = 193707721 ×
   761838257287 is F. N. Cole's famous 1903 "three years of Sundays"
   factorization. Unique j among 1.94·10⁸ candidates.
3. **PROVED.** Theorem 7: exact criterion for tightness at (2ᵏ, 2) —
   digit domination in every prime base dividing 2ᵏ−1 — and Mersenne
   exclusion: 2ᵏ−1 prime ⟹ no tight triple. Explains the observed family
   exactly: all five members k ∈ {4, 9, 11, 41, 67} have 2ᵏ−1 semiprime
   (OEIS A085724).
4. **PROVED.** Theorem 8: for m = 2 or m odd with (3ᵐ+1)/4 prime and
   (3ᵐ−1)/2 a prime power, (3ᵐ+1, 3, (3ᵐ+1)/2) is tight — the hypotheses
   hold exactly for m ∈ {2, 3, 5, 7, 13}, i.e. every known i=3 member.
5. **CERTIFIED.** Independent confirmation of the January 2026 Rust scan
   (conglu1997/erdos_699_rust): #699 holds for n ≤ 10⁷, with exactly the
   9 known tight pairs — different algorithm (danger-zone reduction:
   exceptional triples need i ≤ n − prevprime(n)), 30 s on 4 cores vs
   ~120 core-hours. Family censuses far beyond any sweep: 2ᵏ complete at
   every danger level for k ≤ 63; i=2 decided at every semiprime exponent
   through k = 109 except k = 101; 3ᵐ+1 complete (i ≥ 2) for m ≤ 40 plus
   m = 41, 43.
6. **NUMERICAL.** A calibrated density model (exact dominated-set counts,
   digit DP): E_k = Θ(1) at exactly the five members, 0.2–0.7 at the
   decided-clean balanced semiprimes (Poisson-consistent misses),
   ≤ 10⁻⁵ elsewhere. Along balanced semiprimes E_k does not decay, so the
   heuristic total **diverges**: the model predicts infinitely many i=2
   exceptions — against the finite-exceptional-set form of the
   strengthening (as formalized in Lean) — while Erdős–Szekeres's main
   p ≥ i conjecture itself stands unthreatened in all data.

## 3. Figure specs

- **F1 (the census).** Data: `data/census_1e7_imin1.csv` + the two new
  triples (NOTE §4 R2 table). Plot all 11 tight triples as points in
  (log n, i)-space, marking the two families (2ᵏ at i=2, 3ᵐ+1 at i=3) and
  the two 2026-08-12 discoveries. Reader's sentence: "Every known
  exception lives on two thin structured families, and the two new ones
  extend the 2ᵏ family eight orders of magnitude deeper."
- **F2 (the model that predicted a theorem-sized needle).** Data:
  `data/density_2k.csv` (columns k, E_heuristic, observed). Scatter E_k
  vs k, log y-axis, members highlighted, Mersenne-prime k at zero,
  near-misses labelled (23, 37, 59, 103, 109), k=101 open. Reader's
  sentence: "The exact digit-coincidence density separates the five hits
  from everything else — and it pointed at k = 67 before the search ran."
- **F3 (why exceptions need prime deserts).** Data: none needed beyond
  NOTE Prop 2/Cor 3. Simple diagram: the interval (n−i, n] and the
  covering prime p > n−i settling every pair. Reader's sentence: "A
  single prime just below n kills every candidate exception at once, so
  exceptions can only live where primes are absent." (Skip if the page
  runs long — F1 and F2 carry the story.)

## 4. Caveats the page must carry

- The Erdős–Szekeres 1978 paper itself was unreachable (all archive
  routes egress-blocked): its statement and its known-exceptions remark
  are **(secondary)**, via erdosproblems.com/699 snippets and the Lean
  formalization (both fetched 2026-08-12). Same for Guy UPINT B31.
- Prior computational work exists and is cited prominently: Cong Lu's
  public scan to 10⁷ (Jan 2026, erdosproblems forum + GitHub repo). This
  session independently confirms it before extending it. The "largest
  known" claims are relative to that census and today's searches.
- The divergence verdict (contribution 6) is a heuristic with an
  untested independence assumption — labelled NUMERICAL, never stated as
  a theorem. The main conjecture (p ≥ i) is NOT challenged by anything
  here.
- Undecided levels are listed explicitly (README defects): (2⁶⁴, i=2,3),
  nine 3ᵐ levels m ∈ {42..48}, (2¹⁰¹, 2) with E = 0.78 (the model's
  strongest open prediction), (2¹³¹, 2), and i ≥ 3 at 2ᵏ for k > 64.
- The deep full sweep past 10⁷ was in flight at session close — the page
  must state whatever bound the log's final update records, not assume
  4·10⁹.
- The uniqueness of j at 2⁶⁷ rests on one C scan plus one Python scan
  written the same day (independent code, same author-session);
  the tightness itself is verified by a third, no-shared-code checker.

## 5. Page status

New page. After it is live: add `· [page ↗](https://fabianarevalo.com/binomial-gcd)`
to the top-level README row and the conjecture README header, then delete
this file.
