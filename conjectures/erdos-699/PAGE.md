# PAGE.md — handoff for the local publish pass (new page: fabianarevalo.com/erdos-699)

New conjecture directory; no page exists yet.  Built by the 2026-08-11
session.  Delete this file once the page is live.

## 1. Headline claim (one sentence)

**CERTIFIED** — Erdős Problem #699 (for every 1 ≤ i < j ≤ ⌊n/2⌋ some
prime p ≥ i divides gcd(C(n,i), C(n,j))) holds for all 4 ≤ n ≤ 10⁸, and
on that whole range the Erdős–Szekeres "p > i" strengthening fails at
exactly nine triples — the nine already known — each now carrying an
independently re-verified certificate.

## 2. Contributions

1. **CERTIFIED.** Weak version verified for all 4 ≤ n ≤ 10⁸: 94,609,120
   composite n, 1,363,743,928 hard rows examined, zero weak
   counterexamples.  This is 10× the previously public frontier (an
   uncertified Rust scan to 10⁷, Jan 2026, posted on the problem's
   forum), and the first dense search of (10⁷, 10⁸].  Engine time 5,972 s
   on 4 cores (~1.7 core-hours) vs the prior art's 121 CPU-hours at 10⁷
   — the reduction lemmas are doing the work.
2. **CERTIFIED.** The complete census of p > i exceptional triples on
   [4, 10⁸]: exactly (10,3,5), (16,2,6), (28,3,14), (28,5,14),
   (244,3,122), (512,2,147), (2048,2,713), (2188,3,1094),
   (1594324,3,797162).  No tenth triple exists below 10⁸.  Per-triple
   certificates in `certs/` (weak witness p = i, complete candidate
   list, per-prime no-carry digit tables, gcd factorization),
   re-derived by an independent Legendre-valuation verifier, and for
   n ≤ 3000 by a third bigint-gcd path.
3. **PROVED** (elementary; the substance of L1/L5 surely implicit in
   ErSz78, marked as such).  Reduction: only rows 2 ≤ i ≤
   n − prevprime(n) at composite n need checking (largest-prime witness
   + Bertrand); prime n and i = 1 rows are always clean; hard-row
   candidates are exactly the primes > i dividing n(n−1)⋯(n−i+1), all
   ≤ n/2; every exceptional triple has i prime with unique witness
   p = i and i | C(n,i) ⟺ n mod i² < i; if n−1 is prime, n carries no
   exception — so n = 2^k is exception-free whenever 2^k−1 is a
   Mersenne prime (explains exceptional exponents {4,9,11} vs Mersenne
   {2,3,5,7,13,17,19}).
4. **PROVED mechanism + CERTIFIED decisions.** The two families: for
   n = 3^m+1, i = 3, j = n/2, the weak witness p = 3 always works and
   every candidate prime divides 3^{2m}−1 with forced no-carry lowest
   digits — exceptional exactly at m ∈ {2,3,5,7,13} (dense range covers
   m ≤ 16).  For n = 2^k, i = 2, candidates are the odd prime factors
   of 2^k−1 — exceptional exactly at k ∈ {4,9,11} (dense range covers
   k ≤ 26).
5. **Observations (labelled as such).** Every i = 3 exception has
   j = n/2 exactly; every exceptional n has the Kummer-degenerate shape
   p^a + p^b; no exception has i ≥ 7; finiteness heuristic (NUMERICAL)
   for both families.

## 3. Figure specs

- **Fig 1 — the census.**  Data: `data/exceptions.csv` (nine rows:
  n, i, j, gcd factorization, family).  Log-scale n axis, one marker per
  triple, colored by family (i = 2 powers of two; i = 3 values 3^m+1;
  the sporadic (28,5,14)), with the verified range [4, 10⁸] drawn as a
  bar so the empty stretch from 1.6×10⁶ to 10⁸ is visible.  Reader
  sentence: "All nine exceptions sit in two structured families plus one
  sporadic point at n = 28, and the searched range beyond the last one
  is sixty times longer than everything before it."
- **Fig 2 — why the computation is cheap.**  Data: `data/summary.csv`
  (per-chunk composites, hard rows, engine seconds).  Bar or annotated
  table contrasting ~2.5·10¹⁵ naive pairs with 1.36·10⁹ hard rows and
  5,972 engine-seconds.  Reader sentence: "One classical lemma about the
  largest prime below n eliminates 99.99995% of the work before any bit
  is set."
- **Fig 3 — what an exception looks like.**  Data:
  `certs/EXC_512_2_147.txt` (digit tables).  Typeset the base-7 and
  base-73 digit comparisons of j = 147 against n = 512 (147 = 300₇ fits
  under 512 = 1331₇; 147 = (2,1)₇₃ fits under 512 = (7,1)₇₃), plus
  2 | both.  Reader sentence: "An exception is a simultaneous
  digit-domination coincidence in every candidate base at once — here
  both 7 and 73 fail to carry, so nothing bigger than 2 divides both
  binomials."

## 4. Caveats the page must carry

- **Prior art, prominently**: the Jan-2026 uncertified Rust scan
  (`conglu1997/erdos_699_rust`, posted on the erdosproblems.com forum
  thread) verified the weak version to 10⁷ dense plus the thin families
  2^k ≤ 2²⁷ and 3^m+1 ≤ 3¹⁷+1 and already listed all nine triples.
  This session's news is the certification layer, the 10× dense
  extension, the per-triple certificates, and the lemma/mechanism
  write-up — not the discovery of the triples.
- **(secondary)** citations the page must mark: [ErSz78] itself
  (Austral. Math. Soc. Gaz. 5 (1978) 97–99 — unreachable from the
  session sandbox; attribution via Bergman's abstract and
  erdosproblems.com snippets); Bergman 2011 (abstract only); the
  erdosproblems.com page/forum content (search snippets); Guy UPINT B31.
- **Engine coverage, stated exactly**: dual-engine row-level
  cross-checking on [4, 10⁶] and spot slices [49 999 000, 50 001 000],
  [99 998 000, 10⁸]; elsewhere single interval engine (with per-row
  bitset fallback) plus the independent-verifier sampling layer.  No
  per-row positive witnesses are stored (would be ~10⁹ lines);
  exhaustive-negative certification is by reproducibility + layered
  controls, the repository's standing convention.
- **No OEIS submission was made**: the exceptional sequences are absent
  from OEIS (`oeis: N/A` in the database record; direct search), but
  OEIS forbids AI-generated submissions — submitting is a human
  decision left open.
- The strengthening's finiteness and the j = n/2 rigidity remain open;
  the finiteness argument on the page is a heuristic and must be
  labelled NUMERICAL.

## 5. Existing page

None — this is a new page.  Index row for the top-level README is in
place; add the `page ↗` link there once live.
