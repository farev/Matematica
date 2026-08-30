# PAGE.md — handoff for the public write-up (new page)

New conjecture, new page at `fabianarevalo.com/graham-rearrangement`.

## 1. Headline claim

**CERTIFIED** — Graham's rearrangement conjecture (every subset of
F_p ∖ {0} can be ordered so that its partial sums are pairwise distinct)
holds for **every prime p ≤ 37**, verified exhaustively — 1,954,471,973
dilation orbits, 70,066,181,009 subsets, a witness ordering for every
orbit, zero failures — moving the smallest undecided prime from 29
(where the published record was an uncertified 2016 random search through
order 25) to **41**.

## 2. Contributions

1. **CERTIFIED.** Full closure of primes p = 3 … 37, all sizes
   t = 2 … p−1: 1,954,471,973 orbit representatives decided
   (45,590,075 for p ≤ 31 in 72 s; 1,908,881,898 for p = 37 in ≈ 2.5 h,
   4 threads), covering 70,066,181,009 subsets. Orbit counts match an
   independent Burnside computation exactly on all 173 (p,t) cells.
   p = 29, 31, 37 had never been verified by anyone; the four 2024–26
   asymptotic papers are ineffective at every specific small prime.
2. **CERTIFIED.** The zero-sum size-(p−3) layer — the sets
   Z_p ∖ {0, x, −x}, exactly one dilation orbit per prime, provably
   outside the reach of the Hicks–Ollis–Schmitt construction (their
   removed pairs {d, r+1} require d < r; zero-sum forces d = r) and
   treated inconsistently by the published record — certified for every
   prime **7 ≤ p ≤ 61**, each witness re-verified independently.
3. **PROVED** (elementary but load-bearing): admissibility is a
   dilation-orbit invariant, and the zero-sum p−3 sets form a single
   orbit — this is what turns 70 billion subsets into 2 billion decisions
   and 15 primes of gray zone into 15 witnesses.
4. Negative results worth showing: three natural explicit-construction
   families for the zero-sum p−3 layer are structurally dead (two-block
   and rotated zigzags: 0 valid parameter choices across all 74 primes
   ≤ 397), and a geometric-series route is closed by a clean obstruction —
   {2,…,p−2} *is* the shifted power-run {1 − 2^{i+1}} when 2 is a
   primitive root, but the shift breaks partial-sum injectivity (first
   collision at p = 11), and an unshifted run can never miss the
   antipodal pair {1, −1}.
5. Search anatomy: 64 random shuffles or a swap local search decide
   everything except a thin near-full band. At p = 29 and 31 exactly one
   subset per prime resists — the full set F_p ∖ {0} itself, Graham's
   original 1971 case. At p = 37 the resistant band is t ≥ p−5: 124
   orbits of 1.9 billion, fraction rising from 2% at t = 32 to 100% at
   t ≥ 35, all falling to bounded randomized DFS.

## 3. Figure specs

1. **The frontier map.** Data: `data/frontier.csv` (p, t, prior status,
   today's status; 461 cells for the primes 7 … 61). Grid: x = prime,
   y = size t, cells colored by strongest prior result (refereed proof /
   2026 preprint / uncertified 2016 check / open) with today's certified
   region overlaid. Reader's sentence: "Everything up to p = 37 is now
   settled, plus the zero-sum diagonal out to 61 — the open region starts
   at p = 41."
2. **Cost of a layer.** Data: `data/results_p37.txt` (reps and time per
   t). Log-scale bars of orbits per layer with wall time; annotate the
   peak (t = 18: 252,088,496 orbits). Reader's sentence: "Two billion
   exhaustive decisions fit in an afternoon because dilation symmetry and
   a three-tier search make the average decision ~2 microseconds."
3. **Who resists the search.** Data: `data/results_p29.txt`,
   `data/results_p31.txt`, `data/results_p37.txt` (hard/t3 columns) plus
   the two logged tier-3 witnesses in `data/witness_sample_p29/31.txt`.
   Reader's sentence: "The cheap search fails only in the near-full
   band — and the fraction that resists rises to 100% as the set
   approaches F_p^* itself, the one case Graham proved by hand in 1971."
   (If a third figure is too many, fold this into the page prose.)

## 4. Caveats the page must carry

- The t ≤ 20 proof (Costa–Della Fiore–Fontana–Vena, arXiv:2603.20961) is
  an **unrefereed 2026 preprint**; today's computation is independent of
  it (every size re-decided from scratch) and confirms its range at the
  seven primes 17 … 37.
- Bode–Harborth 2005 (t = p−2) is cited **(secondary)** — paywalled;
  statement as quoted by ADMS16/HOS19.
- The certificate model: decisions are deterministic given the committed
  seed; ~65k sampled witnesses plus every tier-3 set are committed and
  independently re-verified; the remaining witnesses are reproducible
  bit-for-bit but not stored (70 billion orderings would be terabytes).
  The claim's strength is exhaustion + Burnside-exact counts +
  reproducibility, not a per-set witness archive.
- The zero-sum p−3 story is a *documented textual discrepancy* in the
  literature (CDORF22 assert it in one sentence whose printed
  justification is the fixed-k polynomial method, inapplicable at
  k = p−3; Kravitz 2024 still lists the nonzero-sum restriction). The
  page should say the layer's status "was asserted but never given a
  proof or witnesses in print", not that anyone made a false claim.
- erdosproblems.com/475 (as of 2026-08-30) still shows the pre-March
  state (t ≤ 12, no zero-sum caveat at p−3); worth a friendly upstream
  note once the page is live.
- AI assistance per the repository's standing disclosure.

## 5. Existing page

None — new page. Index row for the top-level README is in this session's
commit; link it once the page exists.
