# The plus–minus weighted Davenport constant: D±(C₅⊕C₁₅) = 6, and the landscape between the concatenation and pigeonhole bounds

**Session date:** 2026-08-24. Produced with substantial AI assistance (Claude);
every proof below is elementary and written to be checked by hand; every
computational claim ships code and certificates in this directory.

**Source caveat.** This session ran in a sandbox with all primary literature
unreachable (arxiv.org, oeis.org, journal sites, HAL: egress-blocked;
verified 2026-08-24). Every citation below is **(secondary)**, reconstructed
from search-result snippets, and every statement about what is "known" or
"open" is exactly as strong as those snippets. The two published anchor
values used as controls (the cyclic formula and D±(C₃⊕C₃⊕C₉) = 6) are
reproduced independently by the code here, which is the only sense in which
they are verified. See §9 for the full list of literature statements that
must be re-checked against primary sources on a network-enabled day.

## Abstract

For a finite abelian group G, the plus–minus weighted Davenport constant
D±(G) is the least ℓ such that every sequence of ℓ elements of G has a
nonempty subsequence with a ±1-weighted zero sum. Marchan, Ordaz and Schmid
(IJNT 2014, (secondary)) determined D± for every abelian group of order at
most 100 **except one**: C₅⊕C₁₅, where their bounds give 6 or 7. We decide
that cell: **D±(C₅⊕C₁₅) = 6** — the concatenation lower bound is the truth
and the pigeonhole bound is not attained. The decision is CERTIFIED by four
independent implementations (two of which agree on exact search-tree node
counts, 139 052), and large parts of the nonexistence proof are upgraded to
PROVED by a stratified hand argument. We then recompute, from scratch, d± for
all 184 abelian group types of order ≤ 100 and extend the table beyond 100
(all types through order 135, plus targeted cells to order 243), obtaining
what appear to be the first values past the published range, including
D±(C₇⊕C₂₁) = 8 (pigeonhole-tight) and the first cell strictly between both
elementary bounds (C₃⊕C₃⊕C₁₅, order 135). The landscape suggests a clean
structural conjecture: **either d±(G) = ⌊log₂|G|⌋, or d± splits over a proper
direct-sum decomposition** — verified at every group computed today. An
interim family conjecture the session formulated at midday (C₃⊕C₃ₙ always
pigeonhole-tight) was refuted by its own sweep an hour later at C₃⊕C₄₅
(order 135); the refutation is reported in full (§8).

## 1. The problem

Notation: sequences over G are finite multisets; for S = (g₁,…,g_k) a
**±-weighted zero-sum subsequence** is a nonempty subsequence together with
signs εᵢ ∈ {+1,−1} whose signed sum is 0 in G. S is **±-zero-sum-free
(±-zsf)** if it has none. Define

  d±(G) = max{ |S| : S a ±-zsf sequence over G },   D±(G) = d±(G) + 1.

Status per the search snippets of 2026-08-24 (all (secondary)):

* D±(C_n) = ⌊log₂ n⌋ + 1 (Adhikari, Balasubramanian, Pappalardi, Rath et al.).
* Marchan–Ordaz–Schmid, *Remarks on the plus-minus weighted Davenport
  constant*, Int. J. Number Theory (2014) (arXiv:1308.3316): exact values for
  all |G| ≤ 100 except C₅⊕C₁₅, where 6 ≤ D± ≤ 7; general bounds; for the
  families C₅⊕C₅ₙ and C₇⊕C₇ₙ the value is described as unknown already at
  n = 3.
* The area is active through 2026 (Merito–Ordaz–Schmid on arithmetic of
  monoids of ±-weighted zero-sum sequences, arXiv:2506.14279; sets of
  lengths, arXiv:2404.17258; universal zero-sum invariants, arXiv:2607.02132).
* A 2021 University of Kentucky PhD thesis (D. Perez-Lavin, advisor D. Leep,
  *The Plus-Minus Davenport Constant of Finite Abelian Groups*) studies
  groups whose order is a product of two prime powers "looking more closely
  at primes 2 and 3" (abstract snippet). **We could not read it.** If it, or
  any other unread source, already determines D±(C₅⊕C₁₅), Theorem 1 below is
  an independent confirmation, not a first determination. This is the main
  novelty risk of this note and we flag it prominently rather than bury it.

## 2. Reductions

**Lemma R.** Let S be a ±-zsf sequence over G. Then:
(a) 0 does not occur in S;
(b) no element occurs twice;
(c) no pair {g, −g} occurs;
(d) replacing any element by its negative preserves ±-zsf-ness;
(e) consequently, ±-zsf sequences are exactly the subsets of a fixed set of
representatives of the sign classes {g, −g}, g ∈ G∖{0}, with some elements
possibly replaced by their negatives; d±(G) is the maximum size of a ±-zsf
**subset of class representatives**.

*Proof.* (a) the subsequence (0) with weight +1. (b) (g,g) with weights
(+1,−1). (c) (g,−g) with weights (+1,+1). (d) signs absorb the change:
a signed zero-sum of the modified sequence yields one of the original by
flipping that ε. (e) follows from (a)–(d). ∎

For |G| = N odd there are (N−1)/2 sign classes. All searches below run over
subsets of class representatives; Lemma R(e) makes this exhaustive.

**Reachable sets.** For a set T write R(T) = { Σ_{t∈T'} ε_t t : ∅ ≠ T' ⊆ T,
ε ∈ {±1}^{T'} }. Then R(T ∪ {g}) = R(T) ∪ (R(T)+g) ∪ (R(T)−g) ∪ {g, −g},
R is monotone under extension, T is ±-zsf iff 0 ∉ R(T), and
**T ∪ {g} is ±-zsf iff T is ±-zsf and g ∉ R(T) ∪ {0}** (using −R(T) = R(T)).
This recursion is the engine's invariant and also drives the proofs below.

## 3. Elementary bounds (all proofs in-house)

**Lemma P (pigeonhole; known, (secondary)).** d±(G) ≤ ⌊log₂ |G|⌋.

*Proof.* If |S| = k and 2^k > |G|, two of the 2^k {0,1}-subset sums coincide;
subtracting them gives a signed zero-sum on the (nonempty) symmetric
difference. ∎

**Lemma Cy (cyclic; known, (secondary)).** d±(C_n) = ⌊log₂ n⌋.

*Proof.* Upper: Lemma P. Lower: take S = (1, 2, 4, …, 2^(k−1)), k = ⌊log₂ n⌋.
A signed sum of distinct powers of two is nonzero in ℤ (the lowest chosen
power survives modulo higher ones) and has absolute value ≤ 2^k − 1 < n,
hence is nonzero mod n. ∎

**Lemma C (concatenation/quotient).** For any subgroup H ≤ G,
d±(G) ≥ d±(G/H) + d±(H). In particular, for a direct sum,
d±(A ⊕ B) ≥ d±(A) + d±(B), and iterating over the invariant factors
G ≅ C_{d₁} ⊕ ⋯ ⊕ C_{d_r}: d±(G) ≥ Σᵢ ⌊log₂ dᵢ⌋.

*Proof.* Let T̄ be ±-zsf over G/H, lift each element arbitrarily to G, and
let U be ±-zsf over H. In a signed zero-sum of the concatenation, projecting
to G/H kills the U-part, so the T-part is a signed zero-sum of T̄, hence
empty; then the U-part is a signed zero-sum of U, hence empty. The
invariant-factor form follows with Lemma Cy (among all splittings into cyclic
groups, invariant factors maximize Σ⌊log₂⌋ because ⌊log₂ a⌋ + ⌊log₂ b⌋ ≤
⌊log₂ ab⌋). ∎

**Lemma S (saturation).** A ±-zsf set T of maximum size d±(G) has
R(T) = G ∖ {0}; more generally T is non-extendable iff R(T) ∪ {0} = G.

*Proof.* Immediate from "T ∪ {g} ±-zsf iff g ∉ R(T) ∪ {0}" (§2). ∎

**Lemma E3 (exponent 3 = rank).** If G has exponent 3 (G ≅ C₃^r), a set is
±-zsf iff it is linearly independent over 𝔽₃; hence d±(C₃^r) = r.

*Proof.* Over 𝔽₃ the possible coefficients {−1, 0, +1} are all of 𝔽₃, so a
signed zero-sum of a subset is precisely a nontrivial linear dependence. ∎

Lemmas P and C give, for every G, the bracket
Σᵢ⌊log₂ dᵢ⌋ ≤ d±(G) ≤ ⌊log₂|G|⌋. For C₅⊕C₁₅ this is 5 ≤ d± ≤ 6, i.e.
6 ≤ D± ≤ 7, reproducing the Marchan–Ordaz–Schmid bracket in-house.

## 4. Theorem 1

**Theorem 1.** D±(C₅⊕C₁₅) = 6. Equivalently, d±(C₅⊕C₁₅) = 5: the largest
±-zero-sum-free sequence over C₅⊕C₁₅ has five elements.

**Labels.** The lower bound (d± ≥ 5) is **PROVED** (Lemma C + Lemma Cy;
explicit witness {(0,1), (0,2), (0,4), (1,0), (2,0)} verified by
`verify_witness.py`, all 3⁵−1 = 242 signed sums nonzero). The upper bound
(no ±-zsf 6-set) is **CERTIFIED** by four independent computations (§6);
of the stratified argument below, strata (4,2) and (3,3) and the
parallel-kernel half of stratum (2,4) are **PROVED**. The remaining parts
rest on exhaustive computation; the theorem as a whole therefore carries the
label CERTIFIED.

### 4.1 Stratified nonexistence argument

Write G = C₅⊕C₅⊕C₃ (CRT on the C₁₅ factor), H = the 5-torsion subgroup
≅ C₅⊕C₅, π : G → C₃. Let S be a hypothetical ±-zsf 6-set. By Lemma R(d)
normalize every element outside H to π = +1; the outside σ-parts (components
in C₅⊕C₅ ≅ 𝔽₅²) are then pairwise distinct, and T = S ∩ H is ±-zsf in H.
Since π of a signed combination is (Σε)·1, the binding constraints are the
combinations with Σε ≡ 0 (mod 3). With t₀ = |T|, Lemma P inside H
(d±(𝔽₅²) ≤ 4) gives t₀ ≤ 4, so (t₀, t₁) ∈ {(4,2), (3,3), (2,4), (1,5), (0,6)}.

**Stratum (4,2) — PROVED empty.** Here T is a maximum ±-zsf set in H
(d±(C₅⊕C₅) = 4 is forced: Lemmas P and C meet at 4). By Lemma S,
R(T) = H∖{0}. The two outside elements u, v have π(u−v) = 0, so u − v ∈ H,
and u − v must avoid R(T) ∪ {0} = H — impossible. ∎

**Stratum (3,3) — PROVED empty.** The outside elements u, v, w impose:
x−y, x−z, y−z and ±(x+y+z) all lie in A(T) := H ∖ (R(T) ∪ {0}), where
x, y, z are the σ-parts. Since (x−y) + (y−z) = (x−z), the stratum is empty
provided **A(T) contains no triangle a, b, a+b** (A is symmetric, A = −A),
i.e. provided A(T) is sum-free, for every ±-zsf 3-set T ⊂ 𝔽₅². We classify
those 3-sets. No line of 𝔽₅² contributes 3 elements (a line has only two
sign classes). Two cases:

*(ii) two classes on a line plus one point off it:* T = {a, 2a, c}, c ∉ ⟨a⟩.
Signed sums are αa + βc with α ∈ {0,…,±3}, β ∈ {0,±1}, zero only for
α = β = 0; so T is ±-zsf, R(T) = (⟨a⟩∖{0}) ∪ (±c + ⟨a⟩), and
A(T) = (±2c + ⟨a⟩), of size 10. In the quotient 𝔽₅²/⟨a⟩ ≅ 𝔽₅ the set A(T)
maps to {±2}, which is sum-free in 𝔽₅ (±2±2 ∈ {±1, ∓4} ∌ ±2); hence A(T) is
sum-free. There are 6·1·10 = 60 such T.

*(iii) three pairwise non-proportional classes:* after a change of basis
T = {e₁, e₂, c}. The only possible signed relations use all three elements,
so T is ±-zsf iff c ∉ {±e₁ ± e₂}; with c also off both axes this leaves the
six classes c ∈ {(1,2), (1,3), (2,1), (2,2), (2,3), (2,4)}. For each,
|R(T)| = 20 and A(T) has 4 elements; the six allowed sets are

| c | A(T) |
|---|---|
| (1,2) | (2,0), (3,0), (2,4), (3,1) |
| (1,3) | (2,0), (3,0), (2,1), (3,4) |
| (2,1) | (0,2), (0,3), (1,3), (4,2) |
| (2,2) | (0,2), (0,3), (2,0), (3,0) |
| (2,3) | (0,2), (0,3), (2,0), (3,0) |
| (2,4) | (0,2), (0,3), (1,2), (4,3) |

and each is checked sum-free by inspecting the 10 pairwise sums (done in
`verify_strata.py`, and small enough to redo by hand). Change of basis
(GL(2,5) acts on H fixing the stratification) reduces every type-(iii) T to
one of these six. There are 120 such T, and 60 + 120 = 180 matches the
machine census of ±-zsf 3-subsets. Hence no triangle, and the stratum is
empty. ∎

**Stratum (2,4), parallel kernel pair — PROVED empty.** If T = {a, 2a}
(both classes on one line L = ⟨a⟩), then R(T) ∪ {0} = L. All thirteen
balanced combinations of the four outside σ-parts must avoid L, so their
images under the quotient q : 𝔽₅² → 𝔽₅²/L ≅ 𝔽₅ must be nonzero. Write
yᵢ = q(xᵢ). The six differences give: the yᵢ are pairwise distinct, so
{y₁,…,y₄} = 𝔽₅ ∖ {m} for some m. The four triple sums are
(Σy) − yᵢ = −m − yᵢ (since Σ_{𝔽₅∖{m}} = −m), nonzero for all i iff
−m ∉ {y} iff −m = m iff m = 0. So {y} = {1,2,3,4} — and then the balanced
quad (y₁+y₄) − (y₂+y₃) = (1+4) − (2+3) = 0, a contradiction. ∎

**Stratum (2,4) with independent kernel pair, and strata (1,5), (0,6) —
CERTIFIED empty.** For independent T = {e₁, e₂} the forbidden set is the
3×3 box B = {−1,0,1}², and the constraints say: all pairwise differences
avoid the box, all xᵢ avoid the box s − B (s = Σxᵢ), and all six pair-sums
avoid the box 3s + {0,±2}². A machine-checked reduction brings this
sub-stratum to within one page of a hand proof: among all 12 650 four-point
subsets of 𝔽₅², exactly **two** satisfy the difference and triple
constraints — the punctured lines {(t, 2t) : t ≠ 0} and {(t, 3t) : t ≠ 0} —
and each is then killed by the balanced quad x₁+x₄−x₂−x₃ = 0 (on the line
this is 1+4−2−3 = 0 in 𝔽₅, the same arithmetic that ends the parallel
case). What is missing is a hand derivation of that two-survivor
classification. We did not find a short argument for it, nor for
t₁ = 5, 6 — in stratum (1,5) the balanced 2+2− sums alone annihilate all
2 800 difference-and-triple survivors (ablation profile
19 375 → 2 800 → 0, the 4+1− family never needed), and in stratum (0,6)
the profile is 64 260 → 1 680 → 0 with the 4+1− sums finishing it (the
3+3− splits and the full sum are never load-bearing in either stratum), with
no two-survivor collapse to exploit (constraint families as in
`verify_strata.py`:
differences; triple sums; balanced 2+2− sums; 4+1− sums; for t₁ = 6 also
3+3− sums and the full sum). Exhaustive enumeration finds no admissible
configuration in any of them (66, 12, 1 kernel sets respectively; 0
admissible outside configurations); the search spaces are ≤ 10⁶
configurations each and are independently re-verified by the global searches
of §6.

### 4.2 Extremal structure (inverse problem)

The engine enumerated **all** maximum ±-zsf sets: exactly **85 155** ±-zsf
5-subsets of sign-class representatives. By stratum |S ∩ H|:

| \|S∩H\| | 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|
| count | 3 375 | 13 500 | 29 040 | 27 960 | 11 280 |

The 3 375 = 135 × 25 decomposes exactly as (maximum ±-zsf 4-sets of H:
machine census 135) × (any of the 25 outside sign classes) — as it must:
by Lemma S a maximum kernel set saturates H, while a *single* outside element
never participates in a signed zero-sum (π ≠ 0), so every such extension is
±-zsf. The absence of the stratum |S∩H| = 5 re-confirms d±(C₅⊕C₅) = 4.

A byproduct for the neighbor cell C₇⊕C₇ (CERTIFIED): its census of maximum
±-zsf 5-sets has exactly 1 008 members (implementations A and B agree), and
they form a **single GL(2,7)-orbit** (the orbit of
{(0,1), (1,0), (1,2), (1,4), (3,1)} has size 1 008 = |GL(2,7)|/2, checked by
direct orbit enumeration) — a complete inverse theorem for that cell: up to
linear equivalence there is exactly one maximum ±-zero-sum-free
configuration in C₇⊕C₇.

## 5. The full table, |G| ≤ 100

We recomputed d± for all 184 abelian group types of order ≤ 100
independently of the literature (`data/table_le100.csv`,
`data/table_le100_certs.json`). For 167 of them the elementary bracket of §3
is already an equality ("forced": the value is PROVED by Lemmas P/C/Cy); the
17 cells where the bracket is open were decided by exhaustive search
(CERTIFIED):

| G (primary form) | order | bracket [lo,up] | d± | attains |
|---|---|---|---|---|
| C₃⊕C₃ | 9 | [2,3] | 2 | lower |
| C₃⊕C₃⊕C₂ (≅C₃⊕C₆) | 18 | [3,4] | 4 | **upper** |
| C₃³ | 27 | [3,4] | 3 | lower (=Lemma E3) |
| C₃⊕C₃⊕C₂² (≅C₆⊕C₆) | 36 | [4,5] | 5 | **upper** |
| C₄⊕C₃⊕C₃ (≅C₃⊕C₁₂) | 36 | [4,5] | 5 | **upper** |
| C₅⊕C₃⊕C₃ (≅C₃⊕C₁₅) | 45 | [4,5] | 5 | **upper** |
| C₇⊕C₇ | 49 | [4,5] | 5 | **upper** |
| C₃³⊕C₂ (≅C₃⊕C₃⊕C₆) | 54 | [4,5] | 5 | **upper** |
| C₃⊕C₃⊕C₂³ (≅C₂⊕C₆⊕C₆) | 72 | [5,6] | 6 | **upper** |
| C₄⊕C₃⊕C₃⊕C₂ (≅C₆⊕C₁₂) | 72 | [5,6] | 6 | **upper** |
| C₈⊕C₃⊕C₃ (≅C₃⊕C₂₄) | 72 | [5,6] | 6 | **upper** |
| **C₅⊕C₅⊕C₃ (≅C₅⊕C₁₅)** | **75** | **[5,6]** | **5** | **lower** |
| C₃⁴ | 81 | [4,6] | 4 | lower (=Lemma E3) |
| C₉⊕C₃⊕C₃ | 81 | [5,6] | 5 | lower |
| C₂₇⊕C₃ | 81 | [5,6] | 6 | **upper** |
| C₅⊕C₃⊕C₃⊕C₂ (≅C₃⊕C₃₀) | 90 | [5,6] | 6 | **upper** |
| C₇⊕C₇⊕C₂ (≅C₇⊕C₁₄) | 98 | [5,6] | 6 | **upper** |

Observations. (1) Twelve of the seventeen attain the **pigeonhole** bound —
the concatenation bound is *not* the typical truth, which makes the behavior
of C₅⊕C₁₅ (lower) the exception, not the rule; in hindsight the 2014 open
cell was genuinely delicate. (2) The five lower-attained cells are the
exponent-3 groups C₃^r (r = 2, 3, 4; explained exactly by Lemma E3), the
published anchor C₉⊕C₃⊕C₃, and C₅⊕C₁₅. (3) d± separates four of the five
order-81 groups (values 6, 6, 6, 5, 4 for C₈₁, C₂₇⊕C₃, C₉⊕C₉, C₉⊕C₃⊕C₃,
C₃⁴). (4) Every value is consistent with additivity failing: e.g.
d±(C₃⊕C₆) = 4 > 3 = d±(C₃) + d±(C₆).

Cross-checks: the anchor C₉⊕C₃⊕C₃ reproduces the published D± = 6
((secondary)); all cyclic rows match Lemma Cy; all forced rows match their
proved value (the search never disagreed with a proved bound — asserted at
runtime); **all seventeen gap cells were re-run in the independent C engine,
and the search-tree node counts match the Python engine exactly, cell by
cell** (11, 111, 326, …, 899 134 — table in the session transcript;
rerunnable via `dpm_fast`); C₇⊕C₇ additionally carries the full
implementation-B cross-check (0 six-sets; 1 008 five-sets in both A and B).
For the two largest 2-group trees (C₂⁶ and C₃⊕C₂⁵ shapes) the confirmation
search was node-capped, which is recorded in the CSV — their values rest on
the PROVED bracket, not on search.

## 6. Certification of Theorem 1

Four implementations, written to share no method:

| impl | file | method | result |
|---|---|---|---|
| A | `dpm_core.py` | DFS over class subsets, numpy boolean reachable-set | d±=5; 139 052 nodes; census 85 155 |
| B | `bruteforce_check.py` | all C(37,6) = 2 324 784 six-subsets × 364 sign patterns, integer einsum | zero ±-zsf 6-sets; 85 155 five-sets |
| C | `dpm_fast.c` | bitset DFS in C, same tree order as A | d±=5; **139 052 nodes (exact match with A)** |
| D | `verify_strata.py` | stratified direct enumeration (§4.1) | all five strata empty |

The A/C node-count identity is a strong reproducibility check (same tree,
independently coded); B and D do not share even the tree. The witness
certificate is `data/cert_C5xC15.json` and re-verifiable standalone via
`verify_witness.py` (242 signed sums, pure-int).

## 7. Beyond order 100

All group types of orders 101–135 were computed (`data/table_101_135.csv`),
plus targeted larger cells with the C engine. As far as we could determine
from snippets, no values beyond order 100 are in the literature — every cell
below is *possibly new* with that (secondary)-strength caveat. Highlights
(d± values; D± = d±+1):

* **D±(C₇⊕C₂₁) = 8** (order 147; bracket [6,7] for d±, search: 7 =
  pigeonhole; 16 528 742 nodes, 78 s). The C₇⊕C₇ₙ family is
  pigeonhole-tight at n = 1, 2, 3 — answering, for the C₇ family, the n = 3
  case that the 2014 paper's snippet describes as unknown.
* **C₃⊕C₃⊕C₁₅ (order 135): d± = 6, strictly between both elementary bounds**
  (bracket [5,7]) — the first such cell anywhere in our data. It is
  explained by the best *split*: C₃ ⊕ (C₃⊕C₁₅) gives
  d± ≥ 1 + 5 = 6 via Lemma C with the computed d±(C₃⊕C₁₅) = 5.
* **d±(C₃⊕C₄₅) = 6 < 7 = pigeonhole** (order 135; the n = 15 member of the
  C₃⊕C₃ₙ family) — refuting this session's own interim Conjecture B within
  the hour (§8) and joining the short list of lower-attained cells.
* The other order-101–135 gap cells: d±(C₃⊕C₆⊕C₆) = d±(C₃⊕C₃⊕C₁₂) = 6
  (both order 108, both = pigeonhole and split-attained simultaneously).
* Further values in `data/` (see README table): the C₃⊕C₃ₙ family
  (n = 17, 19 searched; n = 21 forced by split), C₅⊕C₃₀, C₁₃⊕C₁₃
  (54.45M-node sharded exhaustion), and the batch of order-189–243 cells
  whose values Lemma C over the computed table already forces
  (C₃⊕C₆₃, C₇⊕C₂₈, C₁₄⊕C₁₄, C₁₅⊕C₁₅, C₃⊕C₃⊕C₂₇ — predictions
  pre-registered in WRITEUP.md before the confirming runs).

## 8. Conjectures from the data

**Conjecture A (split-or-pigeonhole).** For every finite abelian group G,
either d±(G) = ⌊log₂|G|⌋, or there is a proper direct-sum decomposition
G = A ⊕ B with d±(G) = d±(A) + d±(B).

Verified mechanically at all 261 groups computed in this session
(`conjecture_check.py` over the three data tables; also zero violations of
component-removal monotonicity). Equivalently: the "superadditive atoms" —
groups exceeding every split — are exactly the pigeonhole-tight groups. The
noncyclic atoms in the computed range: C₃⊕C₆, C₃⊕C₁₂, C₃⊕C₁₅, C₇⊕C₇,
C₃⊕C₂₄, C₃⊕C₂₇ below order 100 (none in 101–135), then C₇⊕C₂₁, C₅⊕C₃₀,
C₃⊕C₅₁, C₁₃⊕C₁₃, C₃⊕C₅₇ among the beyond-135 cells. Conjecture A would
reduce the computation of d± to identifying which groups are
pigeonhole-tight.

**Conjecture B — REFUTED the same day, by this session's own sweep.** The
midday form, "d±(C₃⊕C₃ₙ) = ⌊log₂ 9n⌋ (pigeonhole) for all n ≥ 2",
formulated from the n ≤ 11 data, is **false at n = 15**:
d±(C₃⊕C₄₅) = 6 < 7 = ⌊log₂135⌋ (double-engine certified, 8 293 370 nodes
in both engines; the maximum witness is exactly the concatenation
{1}∪{1,2}∪{1,2,4} across C₃⊕C₅⊕C₉). The family is tight at every other
computed n — n = 2, 4, 5, 8, 9, 10, 17, 19 by search, n = 3, 6, 7, 11, 12,
13, 14 forced by the elementary bracket, n = 21 forced by the split
C₉ ⊕ C₂₁ = 3+4 meeting the pigeonhole bound — and fails exactly where no
split reaches ⌊log₂ 9n⌋ (at n = 15 every split tops out at 6). The
refutation is kept here deliberately: it is the session's own cautionary
exhibit on curve-fitting small tables, and it converts Conjecture B into
evidence *for* Conjecture A, which predicted the two admissible values at
n = 15 and is consistent with the one realized.

**Conjecture C.** d±(C₇⊕C₇ₙ) = ⌊log₂ 49n⌋ (pigeonhole) for all n ≥ 1.
(n = 1, 2, 3 by search; n = 4 forced by the split C₄⊕(C₇⊕C₇) = 2+5 meeting
the bound; n = 5 forced by the elementary bracket. First open case: n = 6,
C₇⊕C₄₂, order 294. After the fate of Conjecture B, held with appropriate
humility.)

**Question D.** Which groups attain the concatenation bound while the
pigeonhole bound is strictly larger? In our data: the exponent-3 groups
C₃^r (Lemma E3), C₉⊕C₃⊕C₃, C₅⊕C₁₅, and now C₃⊕C₄₅ — while the siblings
C₅⊕C₃₀ (n = 6) and the C₃⊕C₃ₙ tight cases go to the top. No pattern
covering all four families is apparent yet; Conjecture A says the right
question is which groups are pigeonhole-tight.

## 9. Methodology, reproducibility, and what must be re-checked

Hardware: 4-core cloud sandbox, 15 GB RAM, Python 3.11.15, numpy 2.3.x,
gcc 13. All searches deterministic; no randomness, no floats in any decision
path (numpy used only for boolean/integer array ops). Runtimes are recorded
per group in the CSVs; the entire ≤ 100 table costs ≈ 12 core-minutes except
the two node-capped 2-group confirmations (≈ 8 min each, value proved
independently of search). C engine: `gcc -O2 -o dpm_fast dpm_fast.c`.

Controls (all pass; `controls.py`): cyclic law for n = 2–48, 63, 64, 65;
hand-computed d±(C₃⊕C₃) = 2; published D±(C₉⊕C₃⊕C₃) = 6 (secondary);
five forced cells; isomorphism invariance (C₁₅ ≅ C₃⊕C₅; C₅⊕C₁₅ in three
presentations); a negative control (a planted signed zero-sum is detected).

To re-check on a network-enabled day: (1) the Marchan–Ordaz–Schmid paper's
exact table and conventions, in particular that their open cell is C₅⊕C₁₅
and their bracket is {6,7}; (2) whether the Perez-Lavin thesis (2021), the
2017 survey (Adhikari et al.), or any Merito–Ordaz–Schmid-line paper already
decides C₅⊕C₁₅ or any beyond-100 value; (3) the attribution of the cyclic
formula; (4) whether Conjectures A–C appear in the literature (Conjecture A
in particular has a classical flavor; its Davenport-constant analogue is
false in general, which makes its ±-weighted status interesting either way).

## 10. Open questions

1. A hand proof for the three remaining strata of Theorem 1 (the (2,4)
   stratum resisted a clean argument today; the constraint system has 13
   values in an allowed set of ≥ 16 — the obstruction is structural, not
   counting).
2. Conjecture A: prove for rank 2, or find a counterexample (the first
   unforced rank-2 cells beyond today's range: C₂₃⊕C₂₃, C₂₉⊕C₂₉,
   C₅⊕C₅₅, C₅⊕C₆₅, …).
3. The C₅⊕C₅ₙ family: is d± ever pigeonhole-tight for odd n ≥ 3?
4. Push the complete table to order 200 (only a handful of heavy cells
   remain; the C engine with sharding covers them in CPU-hours).
