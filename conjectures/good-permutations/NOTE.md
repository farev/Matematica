# Good permutations of {1, …, n} and Mersenne numbers

*Research note, session of 2026-09-07. AI-assisted (Claude); every proof
below was checked by hand, every computation ships code and a run record.*

## Abstract

Call a permutation a_1, …, a_n of {1, …, n} **good** if no proper consecutive
block of length at least 2 has an integer average, i.e. no block sum is
divisible by the block length. Weiss (MathOverflow 514690, 27 Aug 2026) found
good permutations for odd n = 3, 7, 31 only (odd n ≤ 41), gave the family
1, p−1, p, p−3, p−2, …, 2, 3 for Mersenne primes p, and asked whether good
permutations exist for odd n if and only if n is a Mersenne prime. Bîsceanu
(same thread) proved that odd n admits a good permutation only if
n = 2^m − 1. We (i) re-derive that structure theorem in the sharper form
needed for computation — every good permutation of a Mersenne number is a
"triangular" bijection: a_t mod 2^k depends only on t mod 2^k, bijectively
and with 0 ↦ 0, for every k < m; (ii) show that under this structure every
block of even length is automatically fine, so goodness is a condition on
odd block lengths alone; (iii) prove that Weiss's family is good **exactly
when p is prime** (its prefix of odd length L sums to −p mod L; nothing else
ever fails); and (iv) report exhaustive computations: the good permutations
of [n] for every n ≤ 31 and for n = 63 — see §5 for the labelled results.

## 1. Definitions and the symmetry group

For a sequence a_1..a_n write P_t = a_1 + ⋯ + a_t (P_0 = 0). The block
a_{s+1}, …, a_{s+L} (0 ≤ s, s + L ≤ n, 2 ≤ L ≤ n − 1) is *proper*; it is
*bad* if L | P_{s+L} − P_s. A permutation is good if it has no bad block.

The maps ρ: a_t ↦ a_{n+1−t} (reversal) and κ: a_t ↦ n + 1 − a_t (complement)
preserve goodness (a block of length L has its sum S replaced by S or by
L(n+1) − S, and L | L(n+1) − S iff L | S). They generate a Klein four-group
acting on good permutations; the action is free for n ≥ 3 (ρ fixes no
permutation with a_1 ≠ a_n; κ fixes none since n+1−a ≠ a for n even… for
odd n, κ fixes a permutation only if a_t = (n+1)/2 for all t, impossible;
ρκ fixes a_t = n+1−a_{n+1−t}, which forces the middle term a_{(n+1)/2} =
(n+1)/2 and is possible in principle — see §5 for what actually occurs).
So for odd n ≥ 3 the number of good permutations is a multiple of 2, and
a multiple of 4 whenever no good permutation is ρκ-symmetric.

## 2. The structure theorem

**Lemma 1 (power-of-two blocks; Bîsceanu–te4).** Let a be a good
permutation of [n] and 2^k < n. Then every block of 2^k consecutive terms has
sum ≡ 2^{k−1} (mod 2^k), and a_{t+2^k} ≡ a_t (mod 2^k) whenever
t + 2^k ≤ n.

*Proof.* Induction on k. For k = 1 a block of two terms has odd sum since
its average is not an integer. If every 2^k-block has sum ≡ 2^{k−1}
(mod 2^k) and 2^{k+1} < n, a 2^{k+1}-block is the union of two 2^k-blocks,
so its sum is ≡ 0 (mod 2^k); it is not ≡ 0 (mod 2^{k+1}) because the block
is proper and good, hence it is ≡ 2^k (mod 2^{k+1}). For the congruence,
subtract the sums of the blocks starting at t and at t + 1: they share
2^k − 1 terms, so a_{t+2^k} − a_t ≡ 0 (mod 2^k). ∎

**Lemma 2 (triangular structure).** Let n = 2^m − 1 and let a be good.
For every 1 ≤ k ≤ m − 1 there is a bijection σ_k: Z/2^k → Z/2^k with
σ_k(0) = 0 such that a_t ≡ σ_k(t mod 2^k) (mod 2^k) for every t. In
particular a_{2^{m−1}} = 2^{m−1}, and for every t < 2^{m−1} the pair
{a_t, a_{t+2^{m−1}}} is {j, j + 2^{m−1}} for some 1 ≤ j < 2^{m−1}.

*Proof.* By Lemma 1, a_t mod 2^k depends only on the class of t mod 2^k
(walk from t in steps of 2^k; 2^k < n). Since 2^k | n + 1, the values
1..n contain exactly u := (n+1)/2^k members of each nonzero residue class
mod 2^k and u − 1 members of the class 0, and the positions 1..n contain
exactly u members of each nonzero class mod 2^k and u − 1 of class 0. Every
position class carries a single residue class of values, and all u (resp.
u − 1) values of a residue class must be placed, so distinct position
classes carry distinct residues (two classes on one residue would need
≥ 2u − 1 > u values), i.e. σ_k is a bijection; and the class 0 of
positions, having only u − 1 members, cannot host a nonzero residue class
(u values), so σ_k(0) = 0. For k = m − 1: a_{2^{m−1}} ≡ 0 (mod 2^{m−1})
and the only value in range is 2^{m−1} itself; the pairs statement is the
case k = m − 1 of "positions t, t + 2^{m−1} carry the same residue", the
only two values with that residue being j and j + 2^{m−1}. ∎

Consequently a good permutation of 2^m − 1 is determined by
2^m − m − 1 bits: writing bit_k for the k-th binary digit,
bit_k(a_t) = b_k(t mod 2^k) ⊕ bit_k(t) for a family of functions
b_k: Z/2^k → {0,1} with b_k(0) = 0 (k = 1, …, m − 1; the case k = 0 is
forced: odd positions carry odd values). The search space for n = 63 is
therefore 2^57, for n = 255 it is 2^247.

**Corollary (Bîsceanu).** If n is odd and admits a good permutation then
n = 2^m − 1. *Proof sketch, as in the thread:* let q be the largest power
of 2 below n and n = q + s. By Lemma 1, a_{i+q} ≡ a_i (mod q) for i ≤ s;
the only pairs of distinct elements of [n] congruent mod q are {j, j+q},
j ≤ s, so the middle segment a_{s+1}, …, a_q is {s+1, …, q} in some order,
a block of length q − s whose average is (n+1)/2, an integer. It is proper
if q − s ≥ 2. Hence q − s = 1 and n = 2q − 1. ∎

**Lemma 3 (even lengths are automatic).** Let n = 2^m − 1 and let a be any
permutation satisfying the conclusion of Lemma 2 (for all k ≤ m − 1). Then
no proper block of even length has an integer average.

*Proof.* Let L = 2^j d with j ≥ 1, d odd, L ≤ n − 1 < 2^m, so j ≤ m − 1.
A block of L consecutive positions meets every class mod 2^j exactly d
times, and the residues σ_j(c) over all classes c form a complete residue
system mod 2^j, so the block sum is ≡ d · (0 + 1 + ⋯ + (2^j − 1)) =
d · 2^{j−1}(2^j − 1) ≡ 2^{j−1} (mod 2^j) (d and 2^j − 1 odd). It is not
divisible by 2^j, hence not by L. ∎

So, for n = 2^m − 1: **a is good iff a has the triangular structure of
Lemma 2 and no proper block of odd length ≥ 3 has sum divisible by its
length.** This is what the search engine enforces (`goodperm.c`, mode 1)
and it is what makes the tree small.

## 3. Weiss's family

For odd p ≥ 3 let W(p) be the permutation 1, p−1, p, p−3, p−2, …, 2, 3:
a_1 = 1 and, for t ≥ 2, a_t = p + 1 − t + 2·[t odd].

**Theorem 4.** W(p) is good if and only if p is prime (p ≥ 3). More
precisely, for p = 2^m − 1 the only bad blocks of W(p) are the prefixes of
odd length L ≥ 3 with L | p; for general odd p the same holds together with
the even-length prefix condition below.

*Proof.* (a) Blocks avoiding position 1. Let the block occupy positions
s..e with s ≥ 2, L = e − s + 1, and let O be the number of odd positions in
[s, e]. Then Σ a_t = L(p+1) − Σ t + 2O = L(p+1) − L(s+e)/2 + 2O. If L is
even then s + e is odd and O = L/2, so Σ a_t = L(p+1) − (L/2)(s+e) + L ≡
(L/2)·(odd) ≢ 0 (mod L). If L is odd then s + e is even, so L | L(s+e)/2,
and O = (L ± 1)/2, so Σ a_t ≡ 2O = L ± 1 ≢ 0 (mod L). No such block is
bad, for every odd p.

(b) Prefixes. For the prefix of length L ≥ 2, with O' = ⌊(L−1)/2⌋ odd
positions in [2, L],
Σ_{t≤L} a_t = 1 + (L−1)(p+1) − (L(L+1)/2 − 1) + 2O'.
If L is odd: L | L(L+1)/2 and 2O' = L − 1, so the sum is
≡ −(p+1) + 2 + (L − 1) ≡ −p (mod L): the prefix is bad iff L | p.
If L is even, write L = 2^j o with o odd: L(L+1)/2 ≡ L/2 (mod L) and
2O' = L − 2, so the sum is ≡ −(p+1) − L/2 (mod L); modulo 2^j this is
−(p+1) − 2^{j−1}o ≡ −(p+1) + 2^{j−1} (mod 2^j), which is nonzero whenever
2^j | p + 1 — always true for p = 2^m − 1 since j ≤ m − 1 — so no even
prefix of W(2^m − 1) is bad. (For general odd p an even prefix is bad iff
L | p + 1 + L/2.)

(c) Hence for p = 2^m − 1, W(p) is good iff no odd L with 3 ≤ L ≤ p − 1
divides p, i.e. iff p is prime. For general odd prime p the odd prefixes
are fine and an even prefix of length L = 2^j o is bad iff L | p+1+L/2;
this can happen (e.g. p = 5: L = 2, sum 1 + 4 = 5? no — 5 is odd; L = 4:
1+4+5+2 = 12, divisible by 4: W(5) = 1,4,5,2,3 is bad), which is why the
family is only claimed for Mersenne primes. ∎

The computational check (`check_good`, `construction p`) agrees: W(p) is
good for p = 7, 31, 127, 8191, 131071, 524287 and bad for p = 15, 63, 255,
511, 1023, 2047, 4095, in every case first failing at the prefix whose
length is the least prime factor of p (§5).

## 4. What remains: composite Mersenne numbers

By the Corollary and Theorem 4, Weiss's question is exactly: *does some
composite 2^m − 1 admit a good permutation?* The smallest cases are
63 = 3²·7, 255 = 3·5·17, 511 = 7·73, 1023 = 3·11·31, 2047 = 23·89 (the
first with prime exponent). For n = 15 the answer is no (Weiss; reproduced
here in both engine modes). §5 reports n = 63.

The relaxation probe at n = 15 (`goodperm_subset`) shows the obstruction is
not a plain divisor argument: with the triangular structure imposed, the
odd block lengths {3, 7, 11} — two of which do not divide 15 — already
exclude every candidate, and the minimal excluding sets are {3,5,7},
{3,5,9}, {3,7,11}, {3,9,11}; length 3 belongs to all of them. Any proof of
nonexistence for composite Mersenne numbers must therefore use the
interaction between the binary structure and short odd blocks, not just
divisibility of n.

## 4a. The resonant lengths 2^k − 1

The relaxation ladders (README rows 6, 8; `results/n63_prefix_lengths.txt`,
`results/n31_prefix_lengths.txt`) single out the block lengths 2^k − 1.
At n = 63, imposing all odd lengths 3, 5, …, 29 leaves 260 candidates
(with a_1 < 32) and adding L = 31 = q − 1 leaves none; at n = 31 the ladder
reaches the true count exactly when L = 15 = q − 1 enters, and at n = 15
every minimal excluding set contains 3 and one of 7 = q − 1, 9, 11.

There is a reason these lengths are special. A block of 2^k − 1 consecutive
positions misses exactly one class c mod 2^k, and 2^k ≡ 1 (mod 2^k − 1), so
writing each value as a_t = (a_t mod 2^k) + 2^k h_t (h_t = the higher bits)
gives, modulo 2^k − 1,

  Σ_block a_t ≡ Σ_{r ≠ σ_k(c)} r + Σ_block h_t ≡ −σ_k(c) + Σ_block h_t,

because Σ_{r=0}^{2^k−1} r = 2^{k−1}(2^k − 1) ≡ 0. For k = m − 1 the higher
part h_t is the single top bit ε_t ∈ {0,1}, with ε_{t+q} = 1 − ε_t and
ε_q = 1. So the length-(q−1) conditions read, for 1 ≤ s ≤ q − 1 (block
s+1 … s+q−1, which straddles position q),

  E_0 + s − ε_s − 2 F_{s−1} ≢ a_s (mod q − 1)   with F_{s−1} = Σ_{t<s} ε_t,
  E_0 = F_{q−1},

and for s = 0, q: E_0 ∉ {0, q − 1}. These tie the prefix counts of the top
bits to the residues a_s mod q — a global linear-arithmetic constraint on
the top bits, unlike the short odd lengths, which are local. A proof of
nonexistence for composite Mersenne numbers would have to use exactly this
interaction; today's session only identified it.

## 4b. What the short lengths force (observations, n = 63)

Classifying the residue patterns σ_k (positions 1..2^k mod 2^k) of the
relaxation survivors at n = 63 with a_1 < 32 (`results/n63_survivors_*.txt`):

| constraints imposed | survivors | σ_2 | σ_3 | σ_4 | σ_5 |
|---|---|---|---|---|---|
| structure + {3,5,7} | 2114 | W(3)-family (= {id, −id}) | id 1579, −id 521, W(7)-family 14 | id 1542, −id 514, other 58 | other |
| structure + {3,5,…,29} | 260 | {id, −id} | id 195, −id 65 | id 195, −id 65 | near-identity with 16-flips |
| + length 31 | 0 | | | | |

Here "id" is r ↦ r, "−id" is r ↦ −r (mod 2^k), and "W(2^k−1)-family" means
the residue pattern of W(2^k−1) or of one of its three images; note W is
self-similar (W(31) mod 16 is W(15), W(63) mod 32 is W(31)). So the short
odd lengths force the low-order structure of any candidate into three
self-similar families — identity-like, negated-identity-like, W-like — and
at n = 63 the W-like branch dies by length 15 (no survivor of {3,…,29} is
W-like mod 8) while the ±identity branches die only at the resonant length
31. This is the shape a proof would take: (a) short lengths force the
family, (b) the resonant length 2^{m−1} − 1 kills the ±identity families
through the top-bit walk of §4a, (c) the W-family fails at a prefix whose
length divides n (Theorem 4 handles W itself; its near relatives need the
argument of (b)). None of (a)–(c) is proved here beyond n = 63.

## 4c. The identity-like families are empty for m ≥ 4 (Theorem 5)

Let n = 2q − 1, q = 2^{m−1}, and call a permutation *identity-like* if
a_t ≡ t (mod q) for every t, *negated-identity-like* if a_t ≡ −t (mod q)
for every t. These are the two families that survive every sub-resonant
relaxation at n = 63 (§4b), and the complement κ maps one onto the other.

**Theorem 5.** For m ≥ 4 no good permutation of [2^m − 1] is identity-like
or negated-identity-like. (For m = 3 the identity-like good permutations
are exactly W(7) = 1 6 7 4 5 2 3 and ρκW(7) = 5 6 3 4 1 2 7.)

*Reduction.* An identity-like permutation has a_q = q and, for 1 ≤ t < q,
a_t = t + q x_t and a_{t+q} = t + q(1 − x_t) for a bit string
x = x_1 … x_{q−1} (Lemma 2 gives the pairing; here the residue map is the
identity). Write O_i = x_1 + ⋯ + x_i (ones among the first i bits) and
O'_j = x_{q−j} + ⋯ + x_{q−1} (ones among the last j bits), O_0 = O'_0 = 0.
By Lemma 3 only odd block lengths L ≥ 3 matter. Three kinds of blocks:

(H) inside [1, q−1]: Σ_{u=t}^{t+L−1} a_u = Lt + L(L−1)/2 + q Σ x_u ≡
q Σ_{window} x (mod L), divisible by L iff the window's bit sum is 0 or L,
i.e. iff the window of x is constant.
(T) inside [q+1, 2q−1]: the same computation with 1 − x_u gives
≡ −q Σ_{window} x: the same condition.
(S) containing position q, say [q−j, q+i] with i, j ≥ 0, i + j = L − 1 even,
(i, j) ≠ (q−1, q−1) (that block is the whole permutation):
Σ = Σ_{u=1}^{j} (q − u + q x_{q−u}) + q + Σ_{u=1}^{i} (u + q(1 − x_u))
  = q (j + 1 + O'_j + i − O_i) + (i − j)(i + j + 1)/2,
and (i − j)(i + j + 1)/2 = ((i − j)/2)·L ≡ 0 (mod L), so Σ ≡ q (L + O'_j − O_i)
(mod L). As gcd(q, L) = 1 and |O'_j − O_i| ≤ max(i, j) < L, the block is bad
iff O_i = O'_j.

Hence an identity-like permutation is good iff
  (I1) x contains neither 000 nor 111, and
  (I2) O_i ≠ O'_j for all i, j ≥ 0 with i + j even, (i, j) ∉ {(0,0), (q−1,q−1)}.
(`idfamily.py` confirms this equivalence by brute force over all 2^{q−1}
strings for q = 4, 8, 16 — 2, 0, 0 good ones — and finds no string
satisfying (I1)+(I2) for q = 32 either.)

*Proof of the theorem.* Let N = q − 1 ≥ 7 (odd) and suppose x satisfies
(I1) and (I2). Put D_i = O_i − O'_i. Then D_0 = D_N = 0, D_i ≠ 0 for
0 < i < N by (I2) with (i, i), and D_{i+1} − D_i = x_{i+1} − x_{N−i} ∈
{−1, 0, 1}, so D has a constant sign on 0 < i < N. Reversing x swaps O and
O', preserves (I1) and (I2) and negates D, so we may assume D_i > 0 for
0 < i < N. Then:
 1. D_1 = x_1 − x_N = 1, so x_1 = 1 and x_N = 0.
 2. (i, j) = (0, 2): O'_2 ≠ 0, so x_{N−1} = 1.
 3. D_2 = (1 + x_2) − (1 + 0) = x_2 > 0, so x_2 = 1; then (I1) forces x_3 = 0.
 4. (i, j) = (1, 3): O_1 = 1 ≠ O'_3 = x_{N−2} + 1, so x_{N−2} = 1.
 5. D_3 = O_3 − O'_3 = (1 + 1 + 0) − (1 + 1 + 0) = 0, contradicting D_3 > 0
    (here 3 < N is used; for N = 3 the argument stops at step 4 and indeed
    x = 110 and its reversal 011 survive, giving ρκW(7) and W(7)).
So no x exists for N ≥ 5, in particular for q ≥ 8. The negated family
follows by κ, which maps a_t ≡ t to a_t ≡ −t (mod q) and preserves
goodness. ∎

Only block lengths 3, 5, 7 around position q and the absence of 111 among
the top bits were used — the same short lengths whose relaxation at n = 63
leaves no identity-like survivor (§4b, σ_5 column). A mechanical check
(`idfamily.py` companion run in WRITEUP) confirms that this constraint
subset alone has no solution for every odd N from 5 to 15 and exactly two
for N = 3.

## 5. Computations (labels per the repository convention)

All exact integer arithmetic; no floating point anywhere; one core of a
4-core sandbox (Intel Xeon 2.8 GHz), gcc 12, -O2 -march=native.

| item | statement | label | record |
|---|---|---|---|
| 5.1 | No good permutation of [63]. Engine A (mode 1): count 0, 1,433,402,570 nodes, 344 s. Engine B: count 0, 1,433,402,570 nodes (identical tree), 128 s. Engine C: count 0, 7,091,512 nodes, 1.65 s | CERTIFIED | `results/n63_*` |
| 5.2 | Counts of good permutations for n = 1..26 (plain engine, no structure used): 1, 2, 2, 2, 0, 2, 4, 8, 0, 2, 0, 4, 0, 2, 0, 4, 0, 2, 0, 4, 0, 2, 0, 4, 0, 2; n = 27, 29: 0 (Corollary); n = 31: 4 (plain engine, 181,519,993 nodes, 4.7 s; structural engines agree) | CERTIFIED | `results/counts_mode0_*`, `results/n31_mode0.txt` |
| 5.3 | The good permutations of [7] and [31] are W(p), ρW, κW, ρκW and nothing else | CERTIFIED | same |
| 5.4 | W(p) good for p = 7, 31, 127, 8191, 131071, 524287; bad for p = 15, 63, 255, 511, 1023, 2047, 4095 with first bad block the prefix of length 3, 3, 3, 7, 3, 23, 3 | CERTIFIED | `results/construction_large.txt`, `construction_test.py` |
| 5.5 | Relaxation data of §4 and §4a (minimal excluding sets at 15; prefix ladders at 31 and 63; Mersenne-length subsets) | CERTIFIED (counts) | `results/n15_*`, `results/n31_*`, `results/n63_*` |
| 5.6 | n = 127: see README (engine C run record `results/n127_mid_run1.txt`) | — | — |
| 5.7 | CP-SAT (OR-Tools 9.15) reproduces the counts at n = 7 (4), 15 (0), 31 (4, enumeration 17 s) but did not decide n = 63 in 25 min of wall time (2 workers; stopped) | negative timing note | `results/n63_cpsat_run1_note.txt` |

Engine ladders (nodes): A/B — 60, 1748, 298,120, 1,433,402,570 at n = 7,
15, 31, 63; C — 20, 416, 26,540, 7,091,512. Growth of C per doubling:
×21, ×64, ×267.

## 6. Open questions

1. Does any composite Mersenne number admit a good permutation? The first
   open case after this session's computation is stated in §5.
2. Is W(p) the only good permutation of a Mersenne prime p up to the
   symmetries ρ, κ? True for p = 7, 31 (exhaustive); n = 127 is beyond the
   plain backtracking engine (see the node-count ladder in the README).
3. For even n the counts are 2, 2, 2, 8, 2, 4, 2, … (n = 2, 4, 6, 8, 10,
   12, 14): is there a structure theorem there too? (Not pursued.)
