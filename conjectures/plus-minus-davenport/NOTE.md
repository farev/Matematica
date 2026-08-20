# The plus-minus weighted Davenport constant at the smallest open cases: D±(C₅⊕C₁₅) = 6, D±(C₇⊕C₂₁) = 8, D±(C₃⊕C₄₅) = 7

**Session date:** 2026-08-20.
**Status of this note:** research note from a one-day session; computational
results CERTIFIED as described; every literature citation is **(secondary)** —
retrieved as search-engine snippets from a sandbox whose direct web access was
blocked — and none has been verified against the primary PDF. See §9 for the
declared overlap risks. Produced with AI assistance (disclosed per repository
policy).

## Abstract

For a finite abelian group G, the plus-minus weighted Davenport constant
D±(G) is the least ℓ such that every sequence of ℓ elements of G contains a
nonempty subsequence with a {+1, −1}-weighted zero sum. Marchan, Ordaz and
Schmid (Int. J. Number Theory 10 (2014) 1219–1239; arXiv:1308.3316,
(secondary)) determined D±(G) for every abelian group of order ≤ 100 with the
single exception of C₅ ⊕ C₁₅, boxed between 6 and 7, and reported the
rank-two families C₅⊕C₅ₙ and C₇⊕C₇ₙ unknown from n = 3; their C₃⊕C₃ₙ theorem
leaves n = 15 as the first open member of that family.

We decide all three smallest open cases by exhaustive exact computation with
cross-checking independent implementations:

- **D±(C₅ ⊕ C₁₅) = 6** — completing the order ≤ 100 table. The upper-bound
  exhaustion (no dissociated 6-set) takes 136,464 nodes in the primary engine
  and is replicated by a definitional engine with no shared reductions.
- **D±(C₇ ⊕ C₂₁) = 8** — the counting bound ⌊log₂ 147⌋ + 1 is attained, by a
  genuinely mixed 7-element witness (the natural split construction stalls at
  6); there are exactly 2016 maximum dissociated 7-sets up to sign
  normalization.
- **D±(C₃ ⊕ C₄₅) = 7** — the first open case (n = 15) of the C₃⊕C₃ₙ family is
  a *deficit* case: the counting bound 8 is not attained.

The three answers land on both sides of the general bounds, so no uniform
"upper bound is always right in rank two" heuristic survives. We add a proved
fiber-counting obstruction (Lemma F) constraining how a hypothetical
6-set in C₅⊕C₁₅ would have to sit over the C₃-fiber, [family tables and a
census of all abelian groups of small order — see §6–§7], and the E±
corollaries via the Grynkiewicz–Marchan–Ordaz identity E±(G) = |G| + D±(G) − 1
((secondary)).

## 1. Definitions

Let G be a finite abelian group, written additively. A *sequence* over G is a
finite unordered list with repetition allowed. A sequence (g₁, …, g_ℓ) has a
*plus-minus (signed) zero-sum subsequence* if there are a nonempty T ⊆ [ℓ]
and signs ε_i ∈ {+1, −1} with Σ_{i∈T} ε_i g_i = 0.

**D±(G)** is the least ℓ such that *every* sequence of length ℓ over G has a
signed zero-sum subsequence. Equivalently D±(G) − 1 is the maximum length of
a *signed-zero-sum-free* sequence.

A set S ⊆ G is **dissociated** if all 2^|S| subset sums Σ_{g∈A} g (A ⊆ S)
are pairwise distinct. Write **dis(G)** for the maximum size of a dissociated
subset of G. (Equivalent classical formulation: no relation
Σ_{g∈S} ε_g g = 0 with ε ∈ {−1, 0, 1}^S, ε ≠ 0.)

Everything below reduces computation of D± to computation of dis.

## 2. Elementary lemmas (proved here, self-contained)

**Lemma L1 (equivalence).** A sequence over G is signed-zero-sum-free iff all
its 2^ℓ subset sums (over subsets of *positions*) are pairwise distinct.
Consequently a maximal signed-zero-sum-free sequence has distinct entries,
and **D±(G) = dis(G) + 1**.

*Proof.* If Σ_{i∈T} ε_i g_i = 0 with T ≠ ∅, put A = {i ∈ T : ε_i = +1},
B = {i ∈ T : ε_i = −1}. Then σ_A = σ_B and A ≠ B (they are disjoint, not both
empty). Conversely if σ_A = σ_B with A ≠ B, then
0 = σ_{A∖B} − σ_{B∖A} is a signed zero-sum on the nonempty index set
(A∖B) ∪ (B∖A). For the consequence: a repeated entry g at positions i ≠ j
gives the signed zero-sum g − g = 0, so maximal signed-zero-sum-free
sequences are sets; the entry 0 is itself a signed zero-sum; and a set is
signed-zero-sum-free iff dissociated by the equivalence just proved. ∎

**Lemma L2 (counting bound).** dis(G) ≤ ⌊log₂ |G|⌋.
*Proof.* The 2^|S| subset sums are distinct elements of G. ∎
(With L1 this is the upper bound D±(G) ≤ ⌊log₂|G|⌋ + 1 of MOS
(secondary).)

**Lemma L3 (split and ladder bounds).**
(a) If G = A ⊕ B then dis(G) ≥ dis(A) + dis(B).
(b) dis(C_n) ≥ ⌊log₂ n⌋, attained by {1, 2, 4, …, 2^{⌊log₂ n⌋ − 1}}; with L2,
dis(C_n) = ⌊log₂ n⌋ and D±(C_n) = ⌊log₂ n⌋ + 1 (the cyclic theorem of
Adhikari et al. / MOS, (secondary); re-proved here).
(c) More generally, for invariant factors G ≅ C_{n₁} ⊕ ⋯ ⊕ C_{n_r}:
dis(G) ≥ Σ ⌊log₂ n_i⌋ (the MOS lower bound, (secondary)).

*Proof.* (a) Take S_A dissociated in A × {0}, S_B in {0} × B. A signed
zero-sum of S_A ∪ S_B projects to a signed zero-sum of the corresponding
subsequences in each factor separately; both must be empty. (b) A
{−1,0,1}-combination of distinct powers 2^0, …, 2^{k−1}, not all
coefficients 0, is a nonzero integer (look at the least power with nonzero
coefficient modulo the next power) of absolute value ≤ 2^k − 1 ≤ n − 1,
hence nonzero mod n. Here k = ⌊log₂ n⌋ gives 2^k ≤ n. (c) Apply (a)
and (b) factor by factor. ∎

**Lemma L4 (elementary 2- and 3-groups).** dis(C₂^r) = dis(C₃^r) = r.
*Proof.* For p ∈ {2, 3} the coefficient set {−1, 0, 1} maps onto 𝔽_p, so a
subset of 𝔽_p^r is dissociated iff it is linearly independent (for p = 2 note
+1 ≡ −1, and "all subset sums distinct" ⟺ "no nonempty subset sums to 0" ⟺
independent). Maximum size r, attained by a basis. ∎
(dis(C₃^r) = r is D±(elementary 3-group) = r + 1, MOS Theorem 5.1,
(secondary), re-proved.)

**Lemma L5 (sign normalization).** If S is dissociated and S′ is obtained by
replacing any subset of its elements g by −g, then |S′| = |S| and S′ is
dissociated. No dissociated set contains 0, or both g and −g for g ≠ −g.
Hence every dissociated set maps, injectively on elements, to a dissociated
set of representatives (one fixed choice from each pair {g, −g}), and: (i)
searching subsets of representatives finds dis(G); (ii) in a group of odd
order, the number of dissociated k-sets equals 2^k times the number of
representative-form ones.
*Proof.* Signed combinations of S′ are signed combinations of S with some
signs flipped; the exclusions are the signed zero-sums g − g′ (g′ = g),
g + (−g), and 0 alone. For (ii): in odd order no element equals its negative,
so each representative-form set lifts to exactly 2^k dissociated sets. ∎

**Lemma L6 (monotonicity).** If H ≤ G then dis(H) ≤ dis(G); moreover
dis(G) ≥ dis(G/H) (lift a dissociated set of the quotient — distinct sums
mod H are distinct in G). ∎

## 3. The fiber-counting obstruction (new here, proved)

**Lemma F.** Let G = H ⊕ C_q and let S be a dissociated set with a elements
in H ⊕ {0} and b = |S| − a elements whose C_q-coordinates are c₁, …, c_b ≠ 0.
Then for every j ∈ C_q,
2^a · #{ A ⊆ [b] : Σ_{i∈A} c_i = j } ≤ |H|.

*Proof.* Subsets of S with C_q-projection j are pairs (A₀, A) with A₀ any
subset of the fiber part (2^a choices) and A ⊆ [b] with c(A) = j. By L1
their subset sums are pairwise distinct, and they all lie in the coset of
H ⊕ {0} over j, which has |H| elements. ∎

**Corollary F5.** Every dissociated 6-set in C₅ ⊕ C₁₅ ≅ C₅² ⊕ C₃ has at
least 3 elements with nonzero C₃-coordinate.
*Proof.* By L5 normalize all nonzero C₃-coordinates to +1. If b ≤ 2 then
some j ∈ C₃ has #{A ⊆ [b] : |A| ≡ j (mod 3)} ≥ 2^b·… — concretely: b = 0
gives 2⁶ = 64 > 25 at j = 0; b = 1 gives 2⁵ = 32 > 25 at j = 0; b = 2 gives
j = 1 count 2 (the two singletons), 2⁴ · 2 = 32 > 25. All contradict
Lemma F with |H| = 25. ∎

The corollary shows why the deficit at C₅⊕C₁₅ (§5) is not a counting
accident: pure counting is consistent with a 6-set (2⁶ = 64 ≤ 75), the
obstruction to b ≤ 2 is Lemma F, and for b ∈ {3, 4, 5, 6} no counting
argument closes the case — the exhaustive search does (§5). A human proof
for b ≥ 3 is open (§8).

**Corollary F45.** Every dissociated 7-set in C₃ ⊕ C₄₅ (with the C₃-fiber
structure G = C₄₅ ⊕ C₃, |H| = 45) has at least 5 elements with nonzero
C₃-coordinate; and the surviving shapes (a, b) ∈ {(2,5), (1,6), (0,7)} fit
Lemma F with **one element to spare** (fiber loads 44, 44, 43 ≤ 45).
*Proof.* Normalize c_i = +1 (L5). The per-residue subset counts
#{A ⊆ [b] : |A| ≡ j mod 3} for b = 0…7 have maxima 1, 1, 2, 3, 6, 11, 22,
43; Lemma F requires 2^a · max_j ≤ 45 with a = 7 − b, which fails for
b ≤ 4 (loads 128, 64, 64, 48, 48) and holds with loads 44, 44, 43 for
b = 5, 6, 7. ∎
The one-element slack is why n = 15 resisted the MOS-era methods: the
deficit is real (§5.3) but invisible to fiber counting.

**Corollary F87.** Every dissociated 8-set in C₃ ⊕ C₈₇ has at least 7
elements with nonzero C₃-coordinate: with fiber capacity |H| = 87, the
loads 2^{8−b} · max_j #{A ⊆ [b] : |A| ≡ j (mod 3)} for b = 0…8 are
256, 128, 128, 96, 96, 88, 88, 86, 85, exceeding 87 for every b ≤ 6. ∎
(Note the contrast inside one failing block of §6: the b = 5 load 88 fits
under the capacities 90 and 93 of n = 30, 31 — where the machine indeed
found b = 5 witnesses — but not under 87.)

## 4. Computation: three cross-checking implementations

All arithmetic is exact (integer indices, bitmasks); no floating point
appears anywhere in any critical path. Deterministic, no seeds.

- **`dis_search.c`** (primary engine): DFS over element indices in
  increasing order, one representative per pair {g, −g} (sound by L5),
  state = bitmask over G of all achievable *nonzero signed* subset sums,
  pruned the moment 0 becomes achievable. Modes: `max` (find dis(G) and a
  witness), `all T` (count every representative-form dissociated T-set;
  exhaustive), `decide T` (existence with early exit), `-r LO HI` (root
  sharding for parallel runs; shards over a partition of the root range
  compose exactly).
- **`verify_defn.c`** (independent engine): DFS over *all* N elements (no
  representative reduction, no signed sums), state = bitmask of *subset
  sums*, extension test "mask ∩ (mask + g) = ∅" — the definition itself,
  plus definitional monotonicity. Agrees with the primary engine only
  through Lemmas L1/L5, so agreement is a real check.
- **`dis_reference.py`** (clean-room Python): an independent third
  implementation of the signed-sum DFS, plus `check` — a witness checker
  that enumerates all 2^k subset sums literally from the definition.

**Controls** (`data/controls.txt`, all pass, `control_failures=0`):
the cyclic formula dis(C_n) = ⌊log₂ n⌋ for n = 2…40; 2-groups attaining
⌊log₂|G|⌋ at eleven groups up to C₂⊕C₄⊕C₈ (MOS: 2-groups attain the upper
bound, (secondary)); elementary 3-groups dis = r for r ≤ 4; the MOS values
D±(C₃²⊕C₉) = 6, D±(C₅⊕C₅) = 5, D±(C₅⊕C₁₀) = 6, D±(C₇⊕C₇) = 6,
D±(C₇⊕C₁₄) = 7, and the C₂⊕C₂ₙ family at n = 3, 5, 6, 7 ((secondary)
values; every one reproduced). Cross-implementation identity at the
headline group: 85,155 representative-form dissociated 5-sets × 2⁵ =
2,724,960 = the definitional engine's raw count of dissociated 5-subsets
(L5(ii)), bit for bit.

## 5. The three decided cases

### 5.1 D±(C₅ ⊕ C₁₅) = 6 (CERTIFIED)

The last open value at order ≤ 100 (MOS box {6, 7}, (secondary)).
dis(C₅⊕C₁₅) = 5.

*Lower bound.* S = {(0,1), (0,2), (0,4), (1,0), (2,0)} ⊂ C₅⊕C₁₅ is
dissociated (this is the split construction L3; checked from the definition
by `dis_reference.py check` — 32 subset sums, milliseconds).

*Upper bound.* No dissociated 6-set exists:
- primary engine, exhaustive count at T = 6: **count = 0**, 136,464 nodes;
- definitional engine, all C(75,6) prefixes with pruning: **0 dissociated
  6-subsets**, 3,505,201 nodes, 42,579,925 extension tests;
- clean-room Python engine: dis = 5 independently.

Certificate: `data/c5c15_certificate.txt`. Total wall time under 3 s
(§10), so anyone can re-run all three exhaustions from source.

### 5.2 D±(C₇ ⊕ C₂₁) = 8 (CERTIFIED)

MOS box {7, 8}, "unknown already for n = 3" (secondary). dis(C₇⊕C₂₁) = 7 =
⌊log₂ 147⌋: the counting bound is attained.

*Lower bound.* Witness (found by the primary engine, verified from the
definition):
S = {(0,1), (0,2), (1,1), (1,5), (2,1), (2,10), (3,19)} ⊂ C₇ ⊕ C₂₁.
Note the split bound L3(c) gives only 2 + 4 = 6; every maximum dissociated
set here genuinely mixes the two coordinates.

*Upper bound.* L2: 2⁸ = 256 > 147. (No search needed.)

*Structure.* Exhaustive count: exactly **2016** representative-form
dissociated 7-sets (16,386,057 nodes). Certificate:
`data/c7c21_certificate.txt`.

### 5.3 D±(C₃ ⊕ C₄₅) = 7 (CERTIFIED)

The first open case, n = 15, of the MOS C₃⊕C₃ₙ theorem — their
fractional-part condition first fails there ((secondary)). dis(C₃⊕C₄₅) = 6:
a **deficit** case, like C₅⊕C₁₅ and unlike C₇⊕C₂₁.

*Lower bound.* The split construction: {(0,1), (0,2), (0,4), (0,8), (0,16),
(1,0)} — a ⌊log₂ 45⌋ = 5 ladder plus one independent C₃ element
(witness emitted by the engine and definitionally checked;
`data/c3c45_certificate.txt`).

*Upper bound.* No dissociated 7-set: primary engine `decide T = 7` ran to
exhaustion with **exists = NO**, 8,202,091 nodes; the definitional engine
confirms 0 dissociated 7-subsets. (Counting alone would allow 7:
2⁷ = 128 ≤ 135.)

### 5.4 E± corollaries (conditional on a (secondary) identity)

Grynkiewicz–Marchan–Ordaz (Ramanujan J. 28 (2012), (secondary)) prove
E_A(G) = |G| + D_A(G) − 1 for all finite abelian G and nonempty A ⊆ ℤ.
Taking A = {±1}: **E±(C₅⊕C₁₅) = 80, E±(C₇⊕C₂₁) = 154, E±(C₃⊕C₄₅) = 141.**
These inherit the (secondary) status of the identity, not of our D± values.

## 6. The C₃ ⊕ C₃ₙ family: an attainment theorem and the machine table

**Theorem T1 (attainment; proved here, and presumably the mechanism of MOS
Theorem 4.4 — see the remark).** Let n ≥ 2 and K = ⌊log₂ 9n⌋ − 3. If
2^K ≤ n, then dis(C₃ ⊕ C₃ₙ) = ⌊log₂ 9n⌋, i.e. D±(C₃ ⊕ C₃ₙ) = ⌊log₂ 9n⌋ + 1
(the counting bound).

*Proof.* Upper bound: L2. Lower bound: write G = C₃ ⊕ C_{3n} and take
S = { (0, 2^i) : 0 ≤ i < K } ∪ { (1, x), (1, y), (1, z) },
|S| = K + 3 = ⌊log₂ 9n⌋, with x, y, z ∈ Z_{3n} to be chosen. Let
W = [−(2^K − 1), 2^K − 1] mod 3n, the set of signed sums of the ladder
(including 0). A signed combination of S sums to zero only if its
C₃-coordinate vanishes; writing t for the number of (1, ·) elements used,
the net C₃-coefficient is (#plus) − (#minus) with t = #plus + #minus ≤ 3,
which is ≡ 0 (mod 3) only for: t = 0 (pure ladder), t = 2 with opposite
signs, and t = 3 with equal signs. So S is dissociated iff
(i) the ladder is (true since 2^K − 1 < 3n);
(ii) x − y, y − z, x − z ∉ W (mod 3n);
(iii) x + y + z ∉ W (mod 3n).
Take x = 0, y = 2^K, z = 2·2^K. The three circular distances are
2^K, 2^K, and min(2^{K+1}, 3n − 2^{K+1}); all are ≥ 2^K exactly because
3n ≥ 3·2^K, i.e. 2^K ≤ n — this is the hypothesis — giving (ii), since W
contains only residues of circular distance ≤ 2^K − 1 from 0. For (iii),
replace (x, y, z) by (x + t, y + t, z + t): (ii) is unchanged and the sum
sweeps the coset (x+y+z) + 3·Z_{3n}, which has n elements, of which at most
⌈(2^{K+1} − 1)/3⌉ ≤ (2n + 1)/3 < n lie in W (using 2^{K+1} ≤ 2n from the
hypothesis, and n ≥ 2); choose t to land outside. ∎

**Remark (which n are covered, and the MOS condition).** 2^K ≤ n fails
exactly when ⌊log₂ 9n⌋ = ⌊log₂ n⌋ + 4, i.e. when {log₂ n} ≥ 1 − {log₂ 9}
≈ 0.830: the failing set is n ∈ {15} ∪ {29, 30, 31} ∪ {57, …, 63} ∪
{114, …, 127} ∪ … . Translating by {log₂ 3n} = {log₂ n + log₂ 3}, the
covered set is exactly "{log₂ 3n} < 1 − {log₂ 3} or {log₂ 3n} ≥ {log₂ 3}" —
verbatim the condition under which MOS Theorem 4.4 is quoted to determine
the family ((secondary), snippet). So T1 as stated should be read as a
**rediscovery** of their attainment regime, re-proved here self-contained
because the primary paper was unreadable from this sandbox; the session's
new content in this family is what happens when the condition *fails*:

- **n = 15 is a genuine deficit** (§5.3): dis(C₃⊕C₄₅) = 6 = the split
  bound, not 7. The first failing n is the first counterexample to
  upper-bound attainment in the family.
- **n = 30 and n = 31 attain** (CERTIFIED): witnesses with *five*
  spread points (b = 5) — e.g. at n = 31:
  (0,1),(0,2),(0,4),(1,3),(1,11),(1,44),(1,71),(1,87) — found in 594k and
  727k nodes respectively; definitionally re-verified. So T1's b = 3
  construction is not the family's only attainment mechanism, and
  "T1-condition fails ⟹ deficit" is false.
- **n = 29 is different, provably**: Lemma F at ℓ = 8 over the C₈₇ fiber
  (capacity 87) gives loads 2^{8−b}·max_j #{A ⊆ [b] : |A| ≡ j mod 3}
  = 256, 128, 128, 96, 96, **88, 88**, 86, 85 for b = 0…8, so **every
  shape with b ≤ 6 is impossible — including the b = 5 shape that saves
  n = 30 (capacity 90 ≥ 88) and n = 31 (93 ≥ 88)**. Only (a, b) = (1, 7)
  and (0, 8) survive counting at n = 29 (Corollary F87). [Machine decision
  for n = 29 in flight at this writing — final outcome in the log and
  `data/c3_n29.txt`.]

**Machine table, C₃ ⊕ C₃ₙ** (from `data/family_le200.txt` and §5.3; every
value CERTIFIED by the primary engine; ✓ = attains ⌊log₂ 9n⌋, ✗ = deficit):

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dis | 2✗ | 4✓ | 4✓ | 5✓ | 5✓ | 5✓ | 5✓ | 6✓ | 6✓ | 6✓ | 6✓ | 6✓ | 6✓ | 6✓ | **6✗** | 7✓ | 7✓ | 7✓ | 7✓ | 7✓ | [n21] |

With T1 covering every n outside the failing blocks, the family
D±(C₃⊕C₃ₙ) is now determined for **all n ≤ 56 except any member of
{29} left unresolved today** (n ≤ 21 by machine, 22–28 by T1, 29–31 by
machine, 32–56 by T1); the first fully open case beyond that is **n = 57**
(the next failing block, 57 ≤ n ≤ 63, order ≥ 513 — beyond today's box).

(n = 1 is C₃², dis 2 < 3, a deficit — covered by L4, outside T1, whose
n ≥ 2 hypothesis is used in step (iii).)

[C₅ ⊕ C₅ₙ AND C₇ ⊕ C₇ₙ TABLES — TO FILL FROM SWEEPS IN FLIGHT.]

## 7. Census and the dichotomy

`data/census.csv` holds dis(G) and D±(G) for **all 184 abelian groups of
order ≤ 100**, computed from scratch in this session (total ≈ 4 CPU-minutes;
the heaviest single group was C₂⁵⊕C₃ at 69 s). Cross-checks: every value
agrees with the controls of §4, and the exceptional set matches the MOS
exception list ((secondary)) — with the previously open C₅⊕C₁₅ now filled
in.

**The deficit groups at order ≤ 100 are exactly five:**

| G | \|G\| | dis | ⌊log₂\|G\|⌋ | D± |
|---|---|---|---|---|
| C₃² | 9 | 2 | 3 | 3 |
| C₃³ | 27 | 3 | 4 | 4 |
| C₅⊕C₁₅ | 75 | 5 | 6 | **6** (new) |
| C₃²⊕C₉ | 81 | 5 | 6 | 6 |
| C₃⁴ | 81 | 4 | 6 | 5 |

(The MOS snippet lists "C₃², C₃³, C₃²⊕C₉, C₅⊕C₁₅" as exceptions; C₃⁴ is
also one, forced by their own elementary-3-group theorem D± = r + 1, so we
read the snippet's list as illustrative, not exhaustive.)

**Conjecture D′ (dichotomy, new here as far as today's searches show).**
For every finite abelian G with invariant factors d₁ | d₂ | ⋯ | d_r, write
L(G) = Σᵢ ⌊log₂ dᵢ⌋ (the MOS lower bound, L3c). Then
dis(G) = ⌊log₂ |G|⌋ or dis(G) = L(G):
**the MOS lower and upper bounds are never both strict.**

*Evidence.* All 184 groups of order ≤ 100 plus every value computed today
beyond 100 (C₃⊕C₄₅, C₇⊕C₂₁, C₃⊕C₉₀, C₃⊕C₉₃, C₅⊕C₆₀, C₇⊕C₄₂, C₇⊕C₄₉,
C₇⊕C₅₆, C₁₁², C₁₃², C₁₄₇, C₃⊕C₃ₙ for 16 ≤ n ≤ 20): zero exceptions, and
zero values strictly between the bounds (scripts in §10). The five census
deficit groups and C₃⊕C₄₅ all sit exactly at L(G).
Status: **NUMERICAL/conjectural** — verified in computed range only.

*Remarks.* (1) A Sylow-split variant ("dis(G) ∈ {Σ_p dis(G_p), counting}")
also fits the census, but the two phrasings part company at groups like
C₃⊕C₈₇, where L = 7 exceeds the Sylow split dis(C₃²) + dis(C₂₉) = 6: if
C₃⊕C₈₇ turns out to be a deficit case (run in flight at writeup time), the
Sylow variant is refuted while D′ survives — see §6/log for the outcome.
(2) The strongest generally-valid split bound is recursive
(max over decompositions G = A ⊕ B of dis(A) + dis(B), e.g.
dis(C₇⊕C₁₄) ≥ dis(C₇²) + dis(C₂) = 6 > 5 = L); D′ deliberately uses the
non-recursive L, and every group where the recursive bound beats L has, so
far, attained the counting bound outright.

Within p-groups the deficit question reduces to: which p-groups miss the
counting bound? In range, *only* 3-groups do (all 2-groups attain — MOS,
(secondary), and every 2-group in the census confirms; C₅², C₇², C₁₁²,
C₁₃² attain by search; C₅³ and C₅⊕C₂₅ attain already by L2 + L3), and
among 3-groups of rank ≤ 2 only C₃²
misses (C₃⊕C₉, C₃⊕C₂₇, C₉⊕C₉, C₈₁ … attain), while every 3-group of rank
≥ 3 in range misses.

## 8. Open questions from this session

1. Prove dis(C₅⊕C₁₅) ≤ 5 by hand. Lemma F reduces to b ∈ {3,4,5,6} nonzero
   C₃-coordinates (shapes (a,b) = (3,3), (2,4), (1,5), (0,6), with fiber
   loads 24, 24, 22, 22 against capacity 25 — all survive counting). The
   extreme shape (0,6) reduces to a clean finite-geometry question: six
   distinct points v₁…v₆ ∈ 𝔽₅² with total F = Σv_i such that (i) all 20
   triple-sums σ_T avoid {0, F}, are pairwise distinct, and satisfy
   2σ_T ≠ F (equivalently: {0, F} ∪ {σ_T} is a 22-point subset of the
   25-point plane, closed under the fixed-point-free involution
   v ↦ F − v); (ii) the 15 pair-sums are pairwise distinct; (iii)
   F ≠ 2v_e + v_f for all ordered pairs. The machine says no such
   configuration exists; a human reason — a 22-in-25 packing obstruction —
   is the missing lemma. The b = 4 case is equivalent to: no dissociated
   4-set F ⊂ 𝔽₅² admits a pair {v₅, v₆} with v₅ − v₆ outside the signed
   span Σ±(F) ∪ {0}. A conceptual reason is missing in both.
2. Characterize the groups with dis(G) < ⌊log₂|G|⌋ ("deficit groups").
   Known at ≤ 100 (MOS (secondary) + this session): C₃², C₃³, C₃⁴-adjacent
   families, C₃²⊕C₉, C₅⊕C₁₅; new at 135: C₃⊕C₄₅. [Update with census.]
3. The next open family members. [Update with sweeps: which n in C₅⊕C₅ₙ,
   C₇⊕C₇ₙ, C₃⊕C₃ₙ remain undecided beyond this session's range.]

## 9. Declared risks and prior-work statement

- **Perez-Lavin, PhD thesis, U. Kentucky 2021** ("The Plus-Minus Davenport
  Constant of Finite Abelian Groups"): scope includes groups whose order is
  a product of two prime powers; 75 = 3·5² qualifies. Its search snippets
  still describe C₅⊕C₁₅ as the sub-100 unknown, but **the PDF was not
  readable from this sandbox and must be checked before any novelty claim
  is published**. If it (or anything else) already decided these values,
  this note's computations become independent confirmations and this
  paragraph must be rewritten to say so.
- **Adhikari, "Plus-Minus Weighted Zero-Sum Constants: A Survey"** (Springer
  2017, ALLADI60 proceedings): paywalled, unread; could contain partial
  progress on these cases.
- Every citation in this note is (secondary): MOS 2014 (arXiv:1308.3316),
  Adhikari et al. 2009 (arXiv:0909.2388), GMO 2012 (arXiv:0903.2810), MOS
  exceptions list, and the openness statements were all reconstructed from
  search snippets on 2026-08-20 and must be verified against the papers
  before submission of any kind.
- The dissociated-set vocabulary connects this to harmonic analysis
  (Rudin; quasi-independent sets). A search under that vocabulary found no
  computation of rank-two exact values ((secondary), 57-query sweep), but
  the communities are large.

## 10. Reproducibility

Machine: 4-core sandbox (Intel, 2.1–3 GHz class), 15 GB RAM, gcc 12/13
(-O2 -march=native), Python 3.11.15. All runs single-thread unless a shard
range `-r` is shown. Deterministic; no randomness anywhere.

```
gcc -O2 -march=native -o dis_search dis_search.c
gcc -O2 -march=native -o verify_defn verify_defn.c

./dis_search max 5 15          # dis=5, 139,052 nodes, < 0.1 s
./dis_search all 5 15 6        # count=0, 136,464 nodes
./verify_defn 5 15 6           # 0 dissociated 6-subsets, 3,505,201 nodes, ~2.3 s
./dis_search max 7 21          # dis=7, 16,528,742 nodes, ~73 s
./dis_search all 7 21 7        # count=2016
./dis_search decide 3 45 7     # exists=NO, 8,202,091 nodes
python3 dis_reference.py max 5 15
python3 dis_reference.py check 5 15 "(0,1),(0,2),(0,4),(1,0),(2,0)"
python3 census.py 100 > data/census.csv
python3 make_tables.py        # parses data/, re-verifies EVERY witness
python3 check_dichotomy.py    # Conjecture D': zero violations expected
```

Certificates and run logs: `data/`.
