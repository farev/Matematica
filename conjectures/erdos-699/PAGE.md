# PAGE.md — handoff for the erdos-699 page (new page)

## 1. Headline claim

Four new exceptional triples for Erdős problem #699 — the first beyond
the classical list, at n = 2⁴¹, 2⁶⁷, 2¹⁰¹ and 2¹³⁷ (a 42-digit n) —
each **CERTIFIED** with deterministic primality, found not by search
but by a **PROVED** structural characterization of the problem's
exceptional families; the same structure gives a certified census
(exactly nine strict failures for all n ≤ 10⁹, none contradicting the
base conjecture) and heuristic evidence that the Erdős–Szekeres
"finitely many exceptions" strengthening is **false as stated**, while
the base problem stands untouched.

## 2. Contributions

1. **CERTIFIED** — complete census of strict failures (no common prime
   p > i) for all n ≤ 10⁹, 1 ≤ i < j ≤ n/2: exactly 9 triples, all
   saved by p = i (so zero counterexamples to #699 below 10⁹; prior
   frontier: an unpublished, uncertified forum sweep to 10⁷). Census:
   (10,3,5), (16,2,6), (28,3,14), (28,5,14), (244,3,122), (512,2,147),
   (2048,2,713), (2188,3,1094), (1594324,3,797162). Three independent
   implementations agree ([4,3000] byte-identical; 57 audited points).
2. **CERTIFIED** — four new exceptional triples (2^k, 2, j_k) at
   k = 41, 67, 101, 137: j₄₁ = 285920731515,
   j₆₇ = 23206563898901803639 (at the Cole semiprime),
   j₁₀₁ = 137177249633792241973877360183,
   j₁₃₇ = 16141961986503368055107762054812561012816. Each verified
   independently, each the unique strict failure at its (n, 2), every
   primality proof deterministic (Sorenson–Webster < 3.317·10²⁴).
3. **PROVED** — the structural calculus: level i = 1 can never fail;
   only levels i ≤ n − prevprime(n) can; witness primes live in the
   gap window's factorizations; and the exact characterization of the
   i = 3 family (n = 3^m+1, j = n/2 fails iff an explicit cofactor
   digit-domination condition holds at every prime p > 3 of 3^{2m}−1),
   with the prime-power corollary that decides membership through
   twin repunit-type primality.
4. **CERTIFIED** — family decisions far beyond any sweep: i = 3 family
   is exactly m ∈ {2,3,5,7,13} for every decided m ≤ 120 (only
   m = 89, 119 undecided — uncracked cofactors) and empty under the
   prime-power criterion to m = 1400 (n ≈ 10⁶⁶⁸); i = 2 family is
   exactly k ∈ {4,9,11,41,67,101,137} over all k ≤ 120 plus seven
   self-verified larger exponents to k = 241.
5. **NUMERICAL** — the bipartite heuristic: the i = 3 family should be
   finite (twin prime-power events, density ~ m⁻²; none found in
   13 < m ≤ 1400), the i = 2 family infinite (digit-alignment fired at
   7 of the 22 decided two-prime-power exponents ≈ ⅓, and composite
   two-prime Mersennes are expected infinite) — so the Erdős–Szekeres
   strengthening is probably false, through the very powers of 2 they
   themselves flagged, while every such failure is saved by p = 2 and
   the base form survives.

## 3. Figure specs

- **Fig 1 — the exceptional set, 1978–today.** Scatter of all 13
  known exceptional triples: x = n on a log axis (10 → 10⁴²), y = i
  (2, 3, 5), point shape by family (2^k / 3^m+1 / the lone (28,5,14)),
  the swept region n ≤ 10⁹ shaded, the four new triples highlighted
  beyond it. Data: `data/exceptions_all.csv`. Reader sentence: "The
  four new exceptions live so far beyond the computable range that no
  sweep could ever have found them — they come from a theorem."
- **Fig 2 — the alignment record at two-prime Mersenne exponents.**
  One row per decided two-prime-power exponent k (22 rows, from
  k = 4 to 241), hit/miss encoding of whether an exception exists.
  Data: `data/semiprime_record.csv`. Reader sentence: "About one in
  three qualifying exponents produces an exception, and qualifying
  exponents never run out — which is exactly why the 'finitely many
  exceptions' conjecture looks wrong."
- **Fig 3 — two families, two fates.** Number line of exponents to
  1400: i = 3 family members {2,3,5,7,13} then provable emptiness of
  the prime-power route to 1400, contrasted with i = 2 hits
  {4,...,137} continuing. Data: `data/fam_pow3.csv` + repunit scan
  (regenerate with `repunit_hunt.py 1400`) + `data/semiprime_record.csv`.
  Reader sentence: "The i = 3 exceptions die out; the i = 2 exceptions
  keep coming."

## 4. Caveats the page must carry

- The original [ErSz78] paper is unread (all mirrors egress-blocked);
  everything about its contents — including which exceptions they knew
  — is (secondary) via the problem page. "First new exceptional
  triples" is qualified accordingly: first beyond everything reported
  on the page, its forum, and the maintained mirrors as of 2026-08-10.
- The prior 10⁷ verification is an unpublished anonymous forum post
  (secondary): our census is the first *reproducible* one, but not the
  first claim of the range below 10⁷.
- "No counterexample below 10⁹" is a CERTIFIED range statement, not
  evidence beyond its range; levels i ≥ 4 at the structured-family n
  beyond the sweep are unswept (only levels 2–3 are decided there).
- Large-factor primality above 3.317·10²⁴ (some NONE rows of the
  family tables only — never the 13 exhibited triples) is BPSW
  probable-prime grade.
- The infinitude/finiteness conclusions in contribution 5 are
  heuristics (labelled NUMERICAL), not theorems; the observed ⅓ rate
  is 7 events over 22 exponents.
- m = 89, 119 of the 3^m family are UNDECIDED (factorization walls).

## 5. Existing page

None — new conjecture, new row. Link this page from the top-level
README row and the conjecture README header once live.
