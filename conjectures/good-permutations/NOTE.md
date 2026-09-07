# Good permutations and Mersenne numbers: the first composite case, n = 63

*Research note, 2026-09-05. Produced with substantial AI assistance (Claude, including a
subagent that wrote the code and the first drafts of the proofs); every proof below was
re-checked by hand by the session, every computation ships code and its output.*

## Abstract

Call a permutation a₁, …, aₙ of {1, …, n}, n > 1 odd, *good* if every proper consecutive
block of length ≥ 2 has a non-integer average. A MathOverflow question (514690, P. Weiss,
27 Aug 2026) asks whether good permutations exist exactly when n is a Mersenne prime; the
thread proves that n must be of the form 2^m − 1 and exhibits the permutation
1, p−1, p, p−3, p−2, …, 2, 3 for Mersenne primes p, and the asker's search covers odd
n ≤ 41. We (i) prove that goodness for n = 2^m − 1 is equivalent to a 2-adic isometry
condition plus the odd-length block conditions (Lemma B), which cuts the search space from
n! to 2^{2^m−1−m}; (ii) prove that the asker's construction is good if and only if p is
prime (Proposition C); (iii) settle the first undecided case by an exhaustive search over
the 2^57 candidates for n = 63: **no good permutation of {1, …, 63} exists** (CERTIFIED,
two independent implementations, 1,433,402,570 nodes each); (iv) re-derive the asker's
search lemma-free and extend it to n = 43, with the exact counts 2, 4, 4 of good
permutations for n = 3, 7, 31. Consequently the conjecture holds for every odd n < 255.
The general composite case remains open; we record the structural observations (an
exact criterion for the two block lengths 2^{m−1} ± 1 that kill every near-solution at
n = 63, and a rigidity conjecture) that a proof attempt should start from.

## 1. Statement

**Definition.** For odd n > 1, a permutation a = (a₁, …, aₙ) of {1, …, n} is *good* if for
every block a_s, …, a_{s+L−1} with 2 ≤ L ≤ n − 1 the sum is not divisible by L. (The whole
permutation has average (n+1)/2 ∈ Z and is excluded; blocks of length 2 are included. For
even n the permutation 2, 1, 4, 3, …, n, n−1 is good — asker's comment, verified for
n ≤ 120 — so only odd n is of interest.)

**Question (MO 514690).** Does a good permutation of {1, …, n} exist if and only if n is a
Mersenne prime?

**Known from the thread (read via the Stack Exchange API on 2026-09-05).** Exist for
n = 3, 7, 31 (the construction c(p) = 1, p−1, p, p−3, p−2, …, 2, 3); none for the other odd
n ≤ 41 (asker's computer search, unpublished); n must be 2^m − 1 (answer by S. A. Bîsceanu
building on a comment by te4, score 11). Primality is not addressed in the thread.

## 2. The 2-adic structure

Throughout n = 2^m − 1 and we set a₀ := 0. v₂ is the 2-adic valuation.

**Lemma A (thread; re-checked).** Let a be good. For every k ≥ 1 with 2^k < n: (a) the sum
of any 2^k consecutive terms is an odd multiple of 2^{k−1}; (b) a_{t+2^k} ≡ a_t (mod 2^k)
for 1 ≤ t ≤ n − 2^k. Moreover n = 2^m − 1 for some m.

*Proof.* (a) k = 1: adjacent terms have odd sum. If (a) holds for k and 2^{k+1} < n, a block
of 2^{k+1} terms is the union of two blocks of 2^k terms, each an odd multiple of 2^{k−1}, so
the total is divisible by 2^k and, being a proper block, not by 2^{k+1}. (b) Subtracting the
sums of the blocks starting at t and t+1 gives a_{t+2^k} − a_t as a difference of two odd
multiples of 2^{k−1}, hence divisible by 2^k. Mersenne form: let q be the largest power of 2
below n and s = n − q, 0 < s < q. By (b) a_{i+q} ≡ a_i (mod q) for i ≤ s. The only pairs of
distinct elements of {1..n} congruent mod q are {j, j+q}, j ≤ s, so the s disjoint pairs
{a_i, a_{i+q}} exhaust them, and a_{s+1}, …, a_q is a permutation of s+1, …, q, whose average
(n+1)/2 is an integer; this block is proper, so its length q − s must be 1: n = 2q − 1. ∎

**Lemma B (PROVED).** Let n = 2^m − 1, m ≥ 2, and a a permutation of {1..n} with a₀ = 0. Then
a is good if and only if

 (i) v₂(a_y − a_x) = v₂(y − x) for all 0 ≤ x < y ≤ n — equivalently a_x ≡ a_y (mod 2^k) ⟺
     x ≡ y (mod 2^k) for all k ≤ m — and
 (ii) every proper block of odd length L ≥ 3 has sum not divisible by L.

*Proof.* (⇒) (ii) is part of goodness. For (i) fix 1 ≤ k ≤ m − 1 (so 2^k < n). By Lemma A(b),
a_t mod 2^k is a function ρ_k(t mod 2^k) of t mod 2^k for 1 ≤ t ≤ n. Among the positions
1..n the residue class r (mod 2^k) has 2^{m−k} elements if r ≠ 0 and 2^{m−k} − 1 if r = 0;
the same holds for the values 1..n. Since a is a bijection, #{t : a_t ≡ s} = #{v : v ≡ s}
for every s. If ρ_k(r) = ρ_k(r′) = s with r ≠ r′ then #{t : a_t ≡ s} ≥ 2^{m−k} − 1 + 2^{m−k}
> 2^{m−k}, impossible; so ρ_k is a bijection of Z/2^k. If ρ_k(0) = s ≠ 0 then
#{t : a_t ≡ s} = 2^{m−k} − 1 ≠ 2^{m−k}, impossible; so ρ_k(0) = 0. Hence for x, y ∈ [1, n]:
a_x ≡ a_y (mod 2^k) ⟺ x ≡ y (mod 2^k), and a_x ≡ 0 = a₀ ⟺ x ≡ 0 (mod 2^k). For k = m both
congruences are equalities since all quantities lie in [0, 2^m). This is (i).
(⇐) Let a block have even length L = 2^j u with u odd, 1 ≤ j ≤ m − 1 (L ≤ n − 1 = 2^m − 2).
By (i) any 2^j consecutive positions are pairwise incongruent mod 2^j, so their values form
a complete residue system mod 2^j; the block is u such systems, so its sum is
≡ u·2^{j−1}(2^j − 1) ≡ 2^{j−1} (mod 2^j), not divisible by 2^j, hence not by L. Odd lengths
are (ii). ∎

*Remark.* The maps satisfying (i) are exactly the automorphisms of the complete binary tree
of depth m on the leaves Z/2^m (branching on successive bits) that fix the leaf 0; there are
2^{2^m−1−m} of them (m = 3: 16; m = 4: 2^{11}; m = 5: 2^{26}; m = 6: 2^{57}). In particular
v₂(a_t) = v₂(t), and a_{2^{m−1}} = 2^{m−1}.

**Lemma B′ (PROVED; candidate generation).** Let a₀ = 0, a₁, …, a_{t−1} satisfy (i) among
themselves, t ≥ 1, K = ⌊log₂ t⌋, t′ = t − 2^K. An integer v satisfies v₂(v − a_x) = v₂(t − x)
for all 0 ≤ x < t if and only if v ≡ a_{t′} + 2^K (mod 2^{K+1}). In [0, 2^m) there are exactly
2^{m−1−K} such v, all nonzero.

*Proof.* (⇒) x = t′: v₂(t − t′) = K forces v ≡ a_{t′} (mod 2^K) and v ≢ a_{t′} (mod 2^{K+1}).
(⇐) Let x < t, x ≠ t′. If x < 2^K: v₂(t − x) = v₂(2^K + (t′ − x)) = v₂(t′ − x) =: j < K, and
v − a_x = (v − a_{t′}) + (a_{t′} − a_x) has terms of valuation K and j, so valuation j. If
2^K ≤ x < t, write x = x′ + 2^K with 0 ≤ x′ < t′; v₂(t − x) = v₂(t′ − x′) =: j < K, and
v − a_x = (v − a_{t′}) + (a_{t′} − a_{x′}) + (a_{x′} − a_x) has terms of valuation K, j, K (the
last by (i): v₂(x′ − x) = K), so valuation j. Counting: v is determined mod 2^{K+1}, leaving
bits K+1, …, m−1 free; v ≡ 0 would need v₂(a_{t′}) = K, but v₂(a_{t′}) = v₂(t′) < K or t′ = 0. ∎

Consequently a depth-first search that, at position t, tries exactly the 2^{m−1−K} values of
Lemma B′ (and prunes with (ii) on every odd block ending at t) visits every map satisfying
(i); the sum over t of (m − 1 − ⌊log₂ t⌋) is 2^m − 1 − m, matching the Remark. This is what
`tree.c` does; every leaf is re-verified against all block lengths 2..n−1 before being
counted, so the solution counts do not depend on the reasoning about even blocks.

## 3. The construction

**Proposition C (PROVED).** Let p = 2^m − 1 ≥ 3 and c(p) = (1, p−1, p, p−3, p−2, …, 2, 3),
i.e. c₁ = 1, c_{2j} = p + 1 − 2j, c_{2j+1} = p + 2 − 2j for 1 ≤ j ≤ (p−1)/2. For a proper block
B = [s, s+L−1] with sum S: if s ≥ 2 then L ∤ S; if s = 1 and L is even then L ∤ S; if s = 1 and
L is odd then S ≡ −p (mod L), so L | S ⟺ L | p. Hence c(p) is good if and only if p is prime.

*Proof.* Put N = p + 1 = 2^m. Consecutive pairs (2j, 2j+1) have c_{2j} + c_{2j+1} = 2N − 4j + 1.
*s = 2j even, L = 2r:* S = Σ_{i=j}^{j+r−1}(2N − 4i + 1) = r(2N + 3 − 4j − 2r); the second
factor is odd, so 2r ∤ S. *s = 2j even, L = 2r+1:* S = r(2N + 3 − 4j − 2r) + (N − 2j − 2r);
modulo L, 2r ≡ −1 gives 2S ≡ −(2N + 4 − 4j) + (2N − 4j + 2) = −2, so S ≡ −1. *s = 2j+1 ≥ 3,
L = 2r:* with A = 2N − 4j − 2r, S = r(A + 1) with A + 1 odd, so 2r ∤ S. *s = 2j+1 ≥ 3,
L = 2r+1:* S = r(A + 1) + (N − 2j − 2r + 1) and 2S ≡ −(A + 1) + 2N − 4j + 4 = 2r + 3 ≡ 2
(mod L), so S ≡ 1. *s = 1, L = 2r:* S = 1 + Σ_{i=1}^{r−1}(2N − 4i + 1) + (N − 2r) ≡ r − N
(mod 2r); 2r | S would give N = r(2k+1), impossible for N = 2^m and r < N. *s = 1, L = 2r+1:*
S = 1 + Σ_{i=1}^{r}(2N − 4i + 1) = 1 + r(2N − 2r − 1), and 2S ≡ 2 − 2N (mod L), so
S ≡ 1 − N = −p (mod L). If p is composite it has an odd divisor L with 3 ≤ L ≤ p/3 ≤ p − 2 and
the block [1, L] has integer average; if p is prime no proper block does. ∎

Numerically confirmed by `check.py --construction p` for p = 3, 7, 15, …, 2047: good exactly
for the primes 3, 7, 31, 127; for composite p the first offending block is always [1, L] with
L the least prime factor of p (`data/batch1.txt`).

## 4. Computations

All runs single-threaded, exact integer arithmetic, < 100 MB RAM, on the session machine
(4 cores, 15 GB, gcc -O2).

| n | program, assumptions | result | nodes | time |
|---|---|---|---|---|
| odd 3 … 43 | `brute.c`: plain backtracking on all permutations, **no lemma** | good permutations only for n = 3 (exactly 2), 7 (exactly 4), 31 (exactly 4); none for every other odd n ≤ 43 | n = 31: 181,519,993; 41: 14,858,098,657; 43: 33,982,657,297 | 2.2 s; 160 s; 358 s |
| 7, 15, 31 | `tree.c` (Lemmas A, B, B′) | 4, 0, 4 — agree with brute force | 60; 1,748; 298,120 | < 0.01 s |
| **63** | `tree.c` | **0 good permutations, search complete** | **1,433,402,570** | **20.0 s** |
| **63** | `brute2.c` mode 2 (independent code: scans all unused values, tests (i) against every earlier position including a₀, checks *all* block lengths) | **0, complete** | 1,433,402,570 (identical, as it must be: both enumerate exactly the maps of Lemma B′) | 200.9 s |
| 31 | `brute2.c` mode 1 (filter uses only the thread's Lemma A) | 4 | 24,620,037 | 1.8 s |

The four good permutations for n = 7 and for n = 31 are the construction c(p) and its images
under reversal and complement a_i ↦ n + 1 − a_i (`data/sols_m3.txt`, `data/sols_m5.txt`);
all pass `lemma_check.py`. Even-length blocks never pruned anything in `tree.c -e` for
m = 2..6, as Lemma B predicts. The counts of good permutations for n = 2..15 are
2, 2, 2, 0, 2, 4, 8, 0, 2, 0, 4, 0, 2, 0 (`data/counts_n2_15.txt`; even n included), a
sequence not in the OEIS as of today.

**Theorem 1 (CERTIFIED).** There is no good permutation of {1, …, 63}.

*Certificate.* Lemmas A, B, B′ (proved above) reduce existence to the 2^57 tree automorphisms
fixing 0; `tree.c` and `brute2.c` (mode 2) exhaust them independently with identical node
counts and find none. Outputs: `data/run63.txt`, `data/b2_63_m2.txt`.

**Corollary 2.** A good permutation of {1, …, n}, n odd, exists for n ∈ {3, 7, 31, 127} and
for no other odd n < 255. *Proof.* Lemma A restricts to n ∈ {3, 7, 15, 31, 63, 127}; 15 is
excluded by `brute.c` (and `tree.c`), 63 by Theorem 1, and 127 admits c(127) by Proposition C. ∎

## 5. The Mersenne ladder beyond 63 (NUMERICAL)

`tree2.c` searches in a "construction-first" order. n = 127 (prime): the construction is the
first leaf visited (and passes `check.py`); with a 300 s cap, 17,205,035,008 nodes, no second
solution in the explored region — the count is **not** exhaustive (2^{120} candidates).
n = 255 = 3·5·17: 900 s cap, 41,182,822,400 nodes, maximal depth 78 of 255, nothing found —
**no information** (2^{247} candidates). The ladder was stopped there.

## 6. Structure of the failure at n = 63 (PROVED criterion, NUMERICAL observations)

Restricting the pruning to a set of odd lengths (`tree.c -L`) shows that there is no small
or divisor-based obstruction: at n = 63 the lengths {3, 5, 7} leave 4228 tree automorphisms,
the odd lengths ≤ 13 leave 680, the divisor lengths {3, 7, 9, 21} leave more than 5248
(`data/exp63.txt`, `data/exp63b.txt`). Each of the 680 survivors of odd lengths ≤ 13 is
killed by the two lengths 31 = q − 1 and 33 = q + 1, where q = 2^{m−1} = 32
(`data/analyze680.txt`; smallest killing length 15, 19, 29, 31 for 16, 16, 128, 520 of them).
For these two lengths there is an exact criterion:

**Lemma E (PROVED).** Let a satisfy (i) with q = 2^{m−1}, and write a_x = ρ(x mod q) + q·h_x with
h_x ∈ {0, 1}, where ρ: Z/q → Z/q is the bijection of Lemma B (ρ(0) = 0). For a block of
positions [t, t+q] (length q+1) let H be the number of x in it with h_x = 1. Then the block has
integer average iff H = ρ(t) + 1. For a block [t, t+q−2] (length q−1) with H defined likewise,
it has integer average iff H ≡ ρ((t−1) mod q) (mod q−1).

*Proof.* The q positions t, …, t+q−1 carry every residue mod q exactly once and t+q repeats
the residue of t, so the sum over [t, t+q] is q(q−1)/2 + ρ(t) + qH. Modulo q+1 we have q ≡ −1,
q(q−1)/2 = (q/2)(q−1) ≡ (−1)(−2)/2 = 1 and qH ≡ −H, so the sum is ≡ 1 + ρ(t) − H; as
0 ≤ H ≤ q+1 and 1 ≤ ρ(t)+1 ≤ q, divisibility by q+1 forces H = ρ(t) + 1. For [t, t+q−2] the
residues cover Z/q except (t−1) mod q, so the sum is q(q−1)/2 − ρ((t−1) mod q) + qH; modulo
q−1, q ≡ 1, q(q−1)/2 = (q−1)(q/2) ≡ 0 and qH ≡ H, giving the criterion. ∎

For the good construction c(31), the length-33 criterion (with q = 16, so length 17) misses
by exactly one at every t.

**Conjecture D (NUMERICAL; rigidity).** For n = 2^m − 1 every good permutation is one of the
four images of c(n) under reversal and complement. True for m = 2, 3, 5 (exhaustive),
consistent with m = 4, 6 (no good permutations, and c(15), c(63) are not good). With
Proposition C it would answer the MO question in the affirmative.

## 7. What was not achieved

No proof of non-existence for composite exponents. Divisor-length arguments (blocks of length
L | n) and local-window arguments are refuted by the data above; the reparametrisation of
Lemma E was not pushed to a contradiction. Whether n = 255 or n = 2047 = 23·89 (composite with
prime exponent) admits a good permutation is open; the structured search space is 2^{247} and
2^{2036} respectively, so a proof, not a search, is needed.

## References

* MathOverflow 514690, "Do only Mersenne primes have 'good' permutations?", P. Weiss,
  2026-08-27, with the answer by S. A. Bîsceanu and the comment by te4 — read via the Stack
  Exchange API on 2026-09-05 (`q.json`, `a.json` in the session scratchpad, not committed).
* No further literature was found (OEIS search for the count sequence and web search, same day).
