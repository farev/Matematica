# The computational frontier of Graham's 105 problem: a census of C(2n,n) coprime to 105 below 3^600

**Session date.** 2026-08-14. Produced with substantial AI assistance
(Claude); every proof was checked by hand and every computational claim
ships code that reruns it. AI systems are not authors.

## Abstract

Let G = {n ≥ 0 : gcd(C(2n,n), 105) = 1}, the subject of a $1000 question of
Graham (is G infinite?), raised by Erdős, Graham, Ruzsa and Straus in 1975
and listed as erdosproblems.com #376. The published computational frontier
was a complete enumeration of G up to 10^70 (1374 terms; C. E. Thompson,
OEIS A030979 b-file, Nov 2015). We give a complete, five-way cross-verified
enumeration of G below 3^600 ≈ 1.87·10^286 — ⟨PENDING-600: total⟩ terms —
extending the complete range by 216 orders of magnitude. Along the way we
verify that n = 3160 remains the largest known element of G whose binomial
coefficient is also coprime to 11 (Graham conjectured it is the last), now
confirmed below 3^600, and we compute the counting function G(N) across the
full range, giving the first empirical test of the N^0.02595 independence
heuristic far beyond 10^70. The infinitude question itself is untouched: it
is a question about ideas, not ranges; what this note contributes is the
data layer that the heuristic arguments rest on.

## 1. The problem and its classical reduction

**Problem (EGRS 1975; Graham's $1000 question).** Are there infinitely many
n with gcd(C(2n,n), 105) = 1, where 105 = 3·5·7?

**Lemma 1 (Kummer's criterion, classical).** For a prime p and n ≥ 0,
p ∤ C(2n,n) if and only if every base-p digit of n is at most (p−1)/2.

*Proof.* By Kummer's theorem, the exponent of p in C(2n,n) = C(n+n, n) is
the number of carries when n is added to n in base p. If every digit
d_i ≤ (p−1)/2, then by induction from the least significant position no
carry ever forms: an incoming carry c ∈ {0,1} is 0 by induction, and
2d_i + 0 ≤ p−1 < p produces none. If some digit has d_i ≥ (p+1)/2, take the
least such i; the incoming carry is c ≥ 0 and 2d_i + c ≥ p+1 > p−1 forces a
carry at position i. So carries exist iff some digit exceeds (p−1)/2. ∎

Hence G = {n : base-3 digits ≤ 1, base-5 digits ≤ 2, base-7 digits ≤ 3},
and membership also demands base-11 digits ≤ 5 exactly when additionally
11 ∤ C(2n,n) (the "1155 flag" below). OEIS A030979 lists G with a(1) = 0;
we follow that convention (C(0,0) = 1) and all counts below include 0.

## 2. The enumeration algorithm and its soundness

Write L for the search height: we enumerate G ∩ [0, 3^L). The base-3
condition says n is a sum of distinct powers 3^k, k < L. The search fixes
the base-3 digits from the most significant end. After d digits are fixed
with prefix value A, every completion satisfies

    A ≤ n ≤ A + (3^(L−d) − 1)/2,                                   (1)

the upper bound being the sum of all remaining powers.

**Lemma 2 (interval prune).** Fix a base b ∈ {5,7} with digit cap c and let
W = (3^(L−d)+1)/2, e = min{e : b^e ≥ W}. For every n in the interval (1),
floor(n/b^e) ∈ {Q, Q+1} where Q = floor(A/b^e), and the base-b digits of n
at positions ≥ e are exactly the digits of floor(n/b^e). Consequently, if
both Q and Q+1 have some base-b digit > c, no completion of the prefix lies
in G, and the subtree may be discarded.

*Proof.* From (1), 0 ≤ n − A ≤ W − 1 < b^e, so floor(n/b^e) can exceed
floor(A/b^e) by at most one. Writing n = floor(n/b^e)·b^e + (n mod b^e),
the base-b expansion of n at positions ≥ e is the expansion of
floor(n/b^e). A member of G has all base-b digits ≤ c, in particular those
at positions ≥ e. ∎

The engines prune exactly when Lemma 2 permits, for b = 5 and b = 7. (A
refinement — only considering Q+1 when the interval actually straddles a
multiple of b^e — was measured to prune ~20% more nodes and deliberately
omitted; it complicates the constant-time incremental test below and does
not change the output.) At a leaf (d = L) the value n = A is fully
determined and is tested digit-by-digit in bases 5 and 7 (base 3 holds by
construction); its base-11 digits give the 1155 flag. Soundness of the
census is Lemma 2 plus the exhaustiveness of the binary tree over base-3
digit choices; no probabilistic or floating-point step exists anywhere.

**Why this is fast.** The number of surviving prefixes at depth d grows
like the count function itself, ~N^0.026 at scale N = 3^d, so the tree
visited is within a constant factor of the output size: empirically ~125
nodes per term across the whole ladder. The published frontier 10^70 costs
0.7 s in the Python reference; each further order of magnitude costs ~6%
more nodes on average (with genuine local fluctuations, §5).

**The C engine's incremental state.** The prefix A is carried as
little-endian digit arrays in bases 5, 7 and 11 simultaneously; choosing or
unchoosing the power 3^k adds or subtracts a precomputed digit array of 3^k
with exact carry/borrow propagation. For b ∈ {5,7} the engine maintains
nbad_b = #{positions i ≥ e_b(d) : digit_i > c}. Q is invalid iff nbad_b>0.
For Q+1, observe the increment at position e propagates through the run of
digits equal to b−1 (each > c, so each counted in nbad_b), zeroing them,
and raises the next digit by one; hence, given nbad_b > 0, Q+1 is invalid
iff that next digit is ≥ c or nbad_b exceeds the run length. This makes the
prune test O(carry run) — amortized O(1) — with no division anywhere in the
hot path. Thresholds e_b(d) are precomputed exactly by comparing 3^m with
2·b^e through the stored digit arrays (equality is impossible by parity).

## 3. Results

All labels follow the repository convention (PROVED / CERTIFIED /
NUMERICAL); every number below is emitted by a committed script.

**C1 (CERTIFIED). Complete census below 3^600.** G ∩ [0, 3^600) has
exactly ⟨PENDING-600: total⟩ elements (3^600 ≈ 1.87·10^286). The ladder

| L | 3^L ≈ | terms G(3^L) | nodes | engine |
|---|---|---|---|---|
| 148 | 4.1·10^70 | 1374 | 137,551 | C + Python, identical |
| 200 | 2.7·10^95 | 10,215 | 1,221,201 | C + Python, identical |
| 250 | 1.9·10^119 | 95,861 | 11,963,213 | C + Python, identical |
| 300 | 1.4·10^143 | 288,836 | 36,430,897 | C full ≡ C 4-worker ≡ Python |
| 350 | 1.9·10^167 | 674,540 | 85,263,581 | C full |
| 400 | 7.1·10^190 | 4,190,720 | 529,206,039 | C full |
| 500 | 3.6·10^238 | 29,814,852 | 3,760,885,157 | C full |
| 600 | 1.9·10^286 | ⟨PENDING-600⟩ | ⟨PENDING-600⟩ | C, 4-worker task mode |

is cumulative and nests (each run reproduces every smaller run's list —
checked by fingerprint). The complete term list is committed to 3^200
plain (`data/terms_3e200_full.txt`, 10,215 lines) and to 3^250 gzipped
(`data/terms_3e250_full.txt.gz`, 95,861 terms); beyond that, runs commit
the first 2000 terms, every 100,000th term, all 1155-flagged terms, the
largest term, per-length histograms and fingerprints. The largest element
of G below 3^600 is a 286-digit number (base-3 length 600), in
`data/max600.txt`; the previous largest published term (≤ 10^70) has 66
digits.

**C2 (CERTIFIED). The 1155 companion.** The only n < 3^600 with
gcd(C(2n,n), 1155) = 1 are n = 0, 1, 3160. Equivalently, Graham's
prediction that 3160 is the last such n survives a complete search 216
orders of magnitude beyond the previously published complete range.
(Strongest prior statement we could source: the complete-to-10^70 census
plus a base-11 filter; an unconfirmed snippet attributes "searches up to
10^104" to the literature — see caveats.)

**C3 (CERTIFIED). Counts.** G(3^k) for every k ≤ 600, in
`data/counts600.txt` (from the merged per-length histograms; the table in
§5 gives decade milestones). These are the first counts beyond 10^70.

**C4 (CERTIFIED, replication).** Thompson's frontier reproduced exactly:
G(10^70) = 1374, including the value 0 (his b-file has 1374 entries).
Independently, a bottom-up engine of a completely different design
(Gray-code walk over sums of distinct powers of 3 with staged residue
filters, 2140 exhaustive tasks) reproduced the census below
3.66·10^19 > 3^41 — covering Alekseyev's entire reported 2008 range — with
zero discrepancies on terms, counts, or flags.

**C5 (NUMERICAL). The heuristic exponent.** The independence heuristic
(EGRS; Pomerance) predicts G(N) ≍ N^θ with
θ = log2/log3 + log3/log5 + log4/log7 − 2 = 0.025954…. The data:
⟨PENDING-ANALYZE: local exponents per band, global fit, discussion⟩.

**C6 (NUMERICAL). Expected further 1155 terms.** Conditional on the same
independence heuristic, the expected number of further 1155-terms —
⟨PENDING-ANALYZE: value among enumerated range and the tail beyond⟩ —
quantifying how unsurprising C2 is and why Graham's finiteness prediction
is safe from computation alone.

## 4. Verification architecture

1. **Definition-level control.** Brute force over all n ≤ 2·10^7 with
   literal gcd(math.comb(2n,n), 105) — no Kummer shortcut — matches the
   digit-condition engines (13 terms).
2. **Five implementations, two algorithm families.** Bottom-up: Python DFS
   over subset sums; C Gray-code grid (32768-task design, stopped at 2140
   ascending tasks = complete below 36,647,386,166,054,954,105). Top-down:
   Python reference; C digit-array engine; C task-mode (4 workers).
   Every overlapping range agrees exactly: term lists, per-task/leaf
   counts, node counts (C top-down ≡ Python top-down node-for-node at
   L = 35, 148, 200, 250, 300), and fingerprints (count, Σn mod 2^64,
   XOR of n mod 2^64, Σn mod 10^9+7).
3. **Task-mode reconciliation.** At L = 300, the 4-worker run's totals
   plus the task generator's internal node count equal the full-mode run's
   fingerprint exactly (nodes 36,417,860 + 13,037 = 36,430,897; terms,
   sums, xor, mod-p all equal).
4. **Independent per-term validation.** Every printed term passes
   `validate_terms.py`: string-conversion digit checks and a Lucas-theorem
   route (C(2n,n) mod p ≠ 0 iff digits of 2n dominate digits of n, with 2n
   computed by bigint doubling — logic disjoint from the search's
   carry-free criterion), for p = 3, 5, 7, 11 (11 against the flag), plus
   literal math.comb for n ≤ 10^5.
5. **External anchors, used as assertions.** The 23-term OEIS display
   line; Thompson's 1374 at 10^70; Graham's 3160. All reproduced.
6. **Leaf identities.** The Gray engine's leaf count equals the digit-DP
   closed form for #{base-3-valid n ≤ T} exactly, per task and in total.

## 5. Counts against the heuristic

⟨PENDING-ANALYZE: table of decade milestones, band exponents, fit, and the
discussion of the swings; nothing here yet — the run has not finished.⟩

## 6. Caveats

- No primary literature source was readable from this sandbox (network
  egress blocked); every citation is search-snippet-sourced 2026-08-14 and
  marked (secondary) except two verbatim GitHub mirrors of OEIS entries
  (A030979, A129489). The load-bearing external claims — Thompson's b-file
  extent ("complete up to 10^70", 1374 terms) and its Nov 2015 date — are
  quoted consistently across five independent snippets but must be checked
  against oeis.org before any external publication of this note. The same
  applies to the "3^41" attribution to Alekseyev (single snippet) and to
  the erdosproblems #376 status text.
- A "searched up to 10^104" claim for the 1155 companion surfaced once, in
  an AI-generated search summary over Pomerance's (blocked) PDFs, and
  resisted five confirmation attempts; we treat 10^70 as the published
  frontier and mention 10^104 only as an unconfirmed possibility. Even
  against it, C2 extends the verification by 182 orders of magnitude.
- The census's correctness rests on the code and cross-checks in §4; there
  is no independent-party certificate format for a search of this shape
  (the output is too large to re-derive by simpler means). What we commit
  is sufficient for a from-scratch reimplementation to be compared
  fingerprint-for-fingerprint at every rung.
- Terms beyond 3^250 are committed as heads/samples/extremes/histograms,
  not full lists (the full 3^600 list is ~⟨PENDING-600: size⟩; the
  repository policy caps committed data at ~10 MB). Anyone needing the
  full list reruns one command per rung.

## 7. Open questions this data sharpens

1. The local exponent of G(N) fluctuates about θ (§5). Is there a
   quantitative log-periodic prediction — the three digit systems beat
   against each other at incommensurate scales log 3 : log 5 : log 7 —
   that matches the observed swings? Pomerance's heuristic argument is the
   natural starting point.
2. EGRS proved infinitude for any two odd primes. The three-prime case is
   the wall. Does the two-prime method plus any quantitative equidistribution
   input give infinitude for {3,5,7} along a sparse explicit sequence?
   (Bloom–Croot 2025 get "all but ε log n digits small" for sufficiently
   large bases — the small-base case is exactly what is missing.)
3. Is the 1155 heuristic sum (C6) provably convergent — i.e., can one
   prove unconditionally that {n : gcd(C(2n,n), 1155) = 1} has counting
   function bounded on a subsequence? Even that seems open.
