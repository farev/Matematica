# Lattice points of the parking-function polytope: an exact enumeration

**Session date.** 2026-08-29. AI-assisted (Claude); see repository README
for the disclosure policy. All computations exact integer/rational
arithmetic; scripts and cross-checks in this directory.

## Abstract

Let P_n ⊂ R^n be the convex hull of the parking functions of length n and
a(n) = #(P_n ∩ Z^n) its number of lattice points (OEIS A333331; entry by
Stanley, 2020). Amanbayeva and Wang (2022) computed a(n) only as a sum of
Postnikov-type evaluations over coordinate-sum slices, and asked for an
Ehrhart polynomial; the OEIS entry carries two standing conjectures
(Howroyd, Jan 2024: an explicit e.g.f.; Wiseman, Mar 2024: a graph-count
equivalence), and Selig (Electron. J. Combin., 2024) asked for an exact
enumeration of the equivalent object StoRec_n, the recurrent states of the
stochastic sandpile on a complete graph. We prove all of it at once:

> **Theorem A.** a(n) equals the number u(n) of loop-graphs on [n] with n
> edges in which every connected component contains exactly one cycle
> (loops count as cycles of length 1; parallel edges are not allowed).
> Consequently Σ a(n)x^n/n! = exp(T + Σ_{k≥3} T^k/2k)
> = exp(−½log(1−T) + T/2 − T²/4), where T = T(x) is the tree function —
> Howroyd's conjectured e.g.f. — and Wiseman's choosability conjecture
> holds. Equivalently |StoRec_n| = u(n), answering Selig's enumeration
> question, with the asymptotics a(n) ~ C·n^{n−1/4},
> C = e^{1/4}√(2π) / (2^{1/4}Γ(1/4)) = 0.7464918…, answering its second
> half.

> **Theorem B.** The Ehrhart polynomial of P_n is
> i(P_n, t) = Σ_M t^{s(M)} (t(t+1)/2)^{d(M)}, the sum over the sparse
> multiforests M of Theorem A's proof (multigraphs on [n], pair
> multiplicities ≤ 2, every component a tree or unicyclic), where s(M),
> d(M) count single and doubled pairs. In generating-function form
> Σ_{n≥0} i(P_n, t) x^n/n! = (1−τ)^{−1/2} exp( (2−t)τ/(2t) − τ²/(4t) )
> with τ = T(tx). This answers Amanbayeva–Wang's question 6(b); the
> general sum-form is a specialization of Liu–Thawinrak (Dec 2025),
> Corollary 7.6 — the combinatorial identification of the index set and
> the closed form are new (see §7 for the precise credit).

Everything below carries the repository's claim labels. Theorems A and B
and all lemmas are **PROVED** (two external published theorems do real
work: Stanley's facet description of P_n, as established in
Amanbayeva–Wang, and Postnikov's lattice-point formula, Theorem 11.3 of
*Permutohedra, associahedra, and beyond*). The term table a(1..40) is
**CERTIFIED** (exact DP, independently cross-checked at every overlap).

## 1. Setup

A **parking function** of length n is a vector c ∈ {1,…,n}^n whose
non-decreasing rearrangement b satisfies b_i ≤ i. PF_n is the set of
parking functions, |PF_n| = (n+1)^{n−1}, and P_n = conv(PF_n) ⊂ R^n.
Stanley (reported and used in [AW22, §1]; the polytope was posed as AMM
Problem 12191) determined the facet description

  P_n = { x ∈ R^n : x_i ≥ 1 for all i;
          Σ_{i∈I} x_i ≤ σ(|I|) for every nonempty I ⊆ [n] },
  σ(k) := (n−k+1) + (n−k+2) + ⋯ + n = kn − k(k−1)/2.        (1)

Amanbayeva–Wang [AW22, Thm 5.2] give a(n) = #(P_n ∩ Z^n) as a double sum
(over coordinate-sum slices, each a permutohedron evaluated by a
Postnikov formula); it is not a closed form, the entry A333331 held eight
terms, and the values from a(9) on had never been computed independently
of the conjectured e.g.f.

A **loop-graph** on [n] is a graph with vertex set [n], loops allowed,
parallel edges not allowed (a simple graph plus at most one loop per
vertex). Let

  U_n = { loop-graphs on [n] with n edges, every component unicyclic },
  u(n) = |U_n|,

where *unicyclic* means the component contains exactly one cycle, a loop
counting as a cycle of length 1. (A 2-cycle would need a parallel pair,
which loop-graphs exclude.)

Throughout, T(x) = Σ_{k≥1} k^{k−1} x^k/k! is the exponential generating
function of rooted labeled trees, T = x e^T.

## 2. From the polytope to partial orientations

Write ∂(I) for the number of edges of the complete graph K_n meeting a
vertex subset I, so ∂(I) depends only on k = |I|:

  ∂(k) = C(n,2) − C(n−k,2) = k(n−1) − k(k−1)/2 = σ(k) − k.     (2)

**Lemma 1 (shift).** The map c ↦ e = c − (1,…,1) is a bijection from
P_n ∩ Z^n onto

  E_n := { e ∈ Z_{≥0}^n : Σ_{i∈I} e_i ≤ ∂(|I|) for all I ⊆ [n] }.

*Proof.* Immediate from (1) and (2): Σ_I c_i ≤ σ(|I|) ⟺
Σ_I e_i ≤ σ(|I|) − |I| = ∂(|I|), and x_i ≥ 1 ⟺ e_i ≥ 0. (The k = 1 case
of (1) gives e_i ≤ n−1, which we will not need to impose separately.) ∎

A **partial orientation** of K_n is an assignment, to each edge of K_n,
of one of three states: oriented toward one endpoint, oriented toward the
other, or left blank. Its **in-degree vector** e ∈ Z_{≥0}^n records at
each vertex the number of edges oriented into it.

**Lemma 2 (Hall).** E_n is exactly the set of in-degree vectors of
partial orientations of K_n.

*Proof.* If e is the in-degree vector of a partial orientation, then for
any I the edges oriented into I are distinct edges meeting I, so
Σ_{i∈I} e_i ≤ ∂(I). Conversely, let e ∈ E_n. Build a bipartite graph B:
left vertices are e_i labeled *demand units* at each vertex i, right
vertices are the edges of K_n, and unit (i,t) is adjacent to the edges
containing i. A matching of B saturating the left side assigns to each
demand unit a distinct edge through its vertex; orienting each matched
edge into the vertex of its unit (and leaving other edges blank) realizes
e. Hall's condition holds: a set U of demand units living on the vertex
set I has |N(U)| = ∂(I) ≥ Σ_{i∈I} e_i ≥ |U|. ∎

Equivalently, E_n is the set of integer points of the polymatroid with
rank function ∂, which is the Minkowski sum of triangles
Q_n := Σ_{1≤i<j≤n} conv{0, ê_i, ê_j} (ê_i the standard basis); we will
use this through a lift. Let [n]₀ = {0,1,…,n} and, in R^{[n]₀}, put

  Q̃_n := Σ_{1≤i<j≤n} Δ_{{0,i,j}},   Δ_S := conv{ ê_a : a ∈ S }.

**Lemma 3 (lift).** Projection π: (x_0, x_1, …, x_n) ↦ (x_1, …, x_n)
restricts to a bijection Q̃_n ∩ Z^{n+1} → E_n.

*Proof.* Q̃_n lies in the hyperplane Σ_{a∈[n]₀} x_a = C(n,2) (each of the
C(n,2) triangle summands has coordinate sum 1), so π is injective on it
and x_0 is determined. If z ∈ Q̃_n then for I ⊆ [n]: Σ_{i∈I} z_i ≤
Σ_{i<j} max_{Δ_{{0,i,j}}} Σ_I x = #{edges meeting I} = ∂(I), and z ≥ 0;
hence π(z) ∈ E_n when z is integral. Conversely, given e ∈ E_n, Lemma 2
writes e as a sum, over the C(n,2) triangles, of vertex choices (ê_i if
the edge {i,j} is oriented into i, ê_j if into j, ê_0 if blank); that sum
is a lattice point of Q̃_n projecting to e. ∎

## 3. Draconian sequences and sparse multiforests

We now invoke Postnikov's lattice-point formula. For finite ground set
[N] and subsets I_1, …, I_m ⊆ [N], a sequence (a_1,…,a_m) ∈ Z_{≥0}^m is
**G-draconian** [Po09, Def. 9.2] if Σ a_i = N − 1 and for every nonempty
{i_1 < ⋯ < i_k} ⊆ [m],

  |I_{i_1} ∪ ⋯ ∪ I_{i_k}| ≥ a_{i_1} + ⋯ + a_{i_k} + 1.      (3)

**Theorem (Postnikov [Po09, Thm 11.3]).** If I_1 = [N], then for
nonnegative integers y_1, …, y_m the polytope y_1Δ_{I_1} + ⋯ + y_mΔ_{I_m}
has exactly Σ (y_1+1)_{a_1}/a_1! · Π_{i≥2} (y_i)_{a_i}/a_i! lattice
points, the sum over G-draconian sequences, where (y)_a = y(y+1)⋯(y+a−1)
is the raising factorial, (y)_0 = 1.

Apply this on the ground set [n]₀ (so N = n+1) with I_1 = [n]₀, y_1 = 0,
and one summand I_e = {0,i,j} with y_e = 1 for each edge e = {i,j} of
K_n. The polytope is exactly Q̃_n, every factor (1)_a/a! = 1 and
(0+1)_{a_1}/a_1! = 1, so with Lemmas 1–3:

  a(n) = #(Q̃_n ∩ Z^{n+1}) = #{ G-draconian sequences (a_1, (a_e)_e) }. (4)

Define a **sparse multiforest** on [n] to be a multigraph M obtained by
assigning each edge of K_n a multiplicity in {0,1,2} such that every
connected component of M is a tree or unicyclic (a doubled pair is a
2-cycle and so makes its component unicyclic; three or more parallel
edges never occur, see below). Let S_n be their set.

**Lemma 4 (dragon ⟺ sparse multiforest).** The map
(a_1, (a_e)) ↦ M(a) := (multigraph with multiplicity a_e on edge e) is a
bijection from the G-draconian sequences of (4) onto S_n.

*Proof.* First note ∪_{e∈F} I_e = {0} ∪ V(F) for any nonempty set F of
edges, where V(F) ⊆ [n] is the vertex support. So condition (3) for an
index set avoiding 1 reads |V(F)| + 1 ≥ Σ_{e∈F} a_e + 1, i.e.

  every finite sub(multi)graph has at least as many supported vertices
  as edges (counted with multiplicity).                        (5)

For an index set containing 1, |I_1 ∪ ⋯| = n+1 and (3) reads
a_1 + Σ_F a_e ≤ n, which holds automatically since Σ = n. So (3) is
equivalent to (5) plus Σ = n.

(5) holds iff every component C of M(a) satisfies #E(C) ≤ #V(C): "if"
because any F decomposes into components each supported inside a
component of M(a), and sub-multigraphs of graphs with #E ≤ #V per
component again satisfy it componentwise (a connected sub-multigraph of a
tree-or-unicyclic multigraph is a tree or unicyclic); "only if" by taking
F = E(C). Also (5) forces a_e ≤ 2 (apply it to F = {e}, giving
2 ≥ a_e — a triple pair would already violate it on its two vertices).
"#E(C) ≤ #V(C) for every component" is precisely "every component is a
tree or unicyclic".

Finally a_1 = n − Σ_e a_e is determined by M, and it is nonnegative for
every M ∈ S_n: if M has components C_1,…,C_p of which q are trees, then
Σ_e a_e = Σ (#E(C_i)) ≤ Σ #V(C_i) = n, with slack q ≥ 0. Hence
sequences ↔ multigraphs bijectively. ∎

## 4. The dissymmetry count: |S_n| = u(n)

**Lemma 5 (component classes are equinumerous).** For every finite set V
of labels, the number of connected sparse-multiforest structures on V
(trees, edge-doubled trees, and simple unicyclic graphs with cycle
length ≥ 3) equals the number of connected U-structures on V (rooted
trees with a loop at the root, and simple unicyclic graphs with cycle
length ≥ 3).

*Proof.* Let k = |V| ≥ 1. The cycle-length ≥ 3 structures are literally
the same objects on both sides. An edge-doubled tree on V is a tree on V
with a chosen edge (double it; the tree is recovered by forgetting
multiplicity, the edge as the doubled one), so there are (k−1)·k^{k−2} of
them; a loop-rooted tree is a tree with a chosen vertex, k·k^{k−2} of
them; and trees number k^{k−2} (Cayley; conventions k^{k−2} = 1 at
k = 1, and no doubled-edge structures at k = 1). Hence

  #trees + #edge-doubled = k^{k−2} + (k−1)k^{k−2} = k·k^{k−2}
                         = #loop-rooted trees.  ∎

(This is the labeled dissymmetry identity for trees: vertex-rooted =
unrooted + edge-rooted.)

**Proposition 6.** |S_n| = u(n) for all n ≥ 1.

*Proof.* Both S_n and U_n consist of all (multi)graphs on [n] whose every
component lies in a fixed class of connected structures, and by Lemma 5
the two classes have the same number of structures on every label set V.
Fix a bijection φ_V between them for every V ⊆ [n]; replacing each
component C of M ∈ S_n on vertex set V(C) by φ_{V(C)}(C) is a bijection
S_n → U_n. ∎

**Theorem A (first part).** a(n) = u(n). ∎ (By (4), Lemma 4, Prop. 6.)

**Theorem A (e.g.f.).** Σ_{n≥0} u(n) x^n/n! = exp(T + Σ_{k≥3} T^k/2k).

*Proof.* By the exponential formula it suffices to compute the e.g.f. of
connected U-structures. Loop-rooted trees are rooted trees (e.g.f. T).
A connected unicyclic graph with cycle length k ≥ 3 is an undirected
cyclic arrangement of k rooted trees on disjoint label sets: sequences of
k rooted trees have e.g.f. T^k, and the dihedral group of order 2k acts
freely on such sequences (the trees carry disjoint, hence distinct, label
sets, so no nontrivial rotation or reflection fixes a sequence — here
k ≥ 3 matters), giving e.g.f. T^k/(2k). ∎

**Corollary A1 (Howroyd's conjecture).**
Σ u(n)x^n/n! = exp(−½ log(1−T) + T/2 − T²/4).

*Proof.* −½log(1−T) = Σ_{k≥1} T^k/2k, so the exponent equals
T/2 + T²/4 + Σ_{k≥3}T^k/2k + T/2 − T²/4 = T + Σ_{k≥3} T^k/2k. ∎

**Corollary A2 (Wiseman's conjecture).** a(n) equals the number of
loop-graphs on [n] with n edges admitting a system of distinct
representatives (a choice of a different vertex from each edge).

*Proof.* We show a loop-graph H with n edges on [n] is choosable iff
every component is unicyclic. If every component is unicyclic, orient
each component's unique cycle cyclically and hang each off-cycle edge
toward the cycle (orient each edge toward its endpoint nearer the cycle);
every vertex then receives exactly one edge, an SDR. Conversely an SDR is
an injection E(H) → [n] with every edge mapped into itself, so each
component C receives all its edges inside V(C): #E(C) ≤ #V(C). Summing,
Σ#E(C) = n = Σ#V(C) forces #E(C) = #V(C) for all C, i.e. every component
unicyclic. ∎

## 5. The sandpile corollary: Selig's open question

Selig [Se24] studies the stochastic sandpile model (SSM) on the cone
K_n^0 and proves [Se24, Thm 18] that a stable configuration
c ∈ {0,…,n−1}^n is stochastically recurrent (SR) iff
Σ_{i∈A} c_i ≥ C(|A|,2) for every A ⊆ [n], and [Se24, Thm 26] that the SR
states are exactly the lattice points of the convex hull of the
(deterministically) recurrent states — the image of P_n under
x ↦ (n,…,n) − x by the Cori–Rossin correspondence [Se24, Thm 16]. His §6
asks for an explicit enumeration of StoRec_n, and failing that for
asymptotics.

**Corollary A3.** |StoRec_n| = a(n) = u(n), with the e.g.f. of
Corollary A1.

*Proof.* c ↦ e = (n−1,…,n−1) − c maps [Se24, Thm 18]'s set bijectively
onto E_n: Σ_{i∈I} e_i = |I|(n−1) − Σ_{i∈I} c_i ≤ |I|(n−1) − C(|I|,2)
= ∂(|I|), and e ≥ 0 ⟺ c ≤ n−1, e ≤ n−1 ⟺ c ≥ 0. Apply Lemma 1 and
Theorem A. ∎

**Corollary A4 (asymptotics).** a(n) = C·n^{n−1/4}·(1 + o(1)) with
C = e^{1/4}√(2π) / (2^{1/4} Γ(1/4)) = 0.74649181….
Equivalently a(n)/n! ~ (e^{1/4}/(2^{1/4}Γ(1/4)))·e^n n^{−3/4}. In
particular a(n)/|PF_n| ~ (C/e)·n^{3/4}: the hull holds about
0.2746·n^{3/4} times more lattice points than parking functions.

*Proof.* Write F(x) = Σ a(n)x^n/n! = (1−T)^{−1/2} G(T),
G(w) = e^{w/2 − w²/4}. T is ∆-analytic with radius 1/e and singular
expansion 1 − T(x) = √2·√(1−ex)·(1 + O(√(1−ex))) as x → 1/e (classical;
e.g. [FS09, §VI.7] or Corless et al. on Lambert W). Hence
F(x) = e^{1/4} 2^{−1/4} (1−ex)^{−1/4}(1 + O(√(1−ex))), and the transfer
theorem [FS09, Thm VI.3–VI.4] gives
a(n)/n! = e^{1/4}2^{−1/4} e^n n^{−3/4}/Γ(1/4) · (1+o(1)). Multiply by
Stirling. For the last claim, |PF_n| = (n+1)^{n−1} ~ e·n^{n−1}.
(Numerical check: a(n)/(C n^{n−1/4}) = 0.9984, 0.9858, 0.9842, 0.9842 at
n = 10, 20, 30, 40.) ∎

## 6. The Ehrhart polynomial

**Theorem B.** For integers t ≥ 0,

  i(P_n, t) := #(tP_n ∩ Z^n) = Σ_{M ∈ S_n} t^{s(M)} · (t(t+1)/2)^{d(M)},

where s(M) and d(M) are the numbers of single and doubled pairs of M.
Moreover Σ_{n≥0} i(P_n,t) x^n/n! = (1−τ)^{−1/2}·exp((2−t)τ/(2t) −
τ²/(4t)) with τ = T(tx), and for n ≥ 2, i(P_n, t) is a polynomial in t of degree n
with positive coefficients whose leading coefficient recovers
Amanbayeva–Wang's volume (P_1 is a point, i(P_1, t) = 1).

*Proof.* tP_n = t·1 + tQ_n is a lattice translate of tQ_n, and
tQ̃_n = Σ_e tΔ_{{0,i,j}} = P_G(0, t, …, t) in the notation of §3, with
the same projection bijection on lattice points as Lemma 3 (the proof
only used the support-function bound, which scales, and Lemma 2 applied
to Σ_I e_i ≤ t·∂(I), whose Hall argument goes through with t·∂). By
[Po09, Thm 11.3], #(tQ̃_n ∩ Z^{n+1}) = Σ_draconian Π_e (t)_{a_e}/a_e!
with (t)_0/0! = 1, (t)_1/1! = t, (t)_2/2! = t(t+1)/2; Lemma 4 turns the
index set into S_n. For the e.g.f., group S_n by components (exponential
formula) with weights: a tree on k vertices carries t^{k−1}; an
edge-doubled tree t^{k−2}·t(t+1)/2; a unicyclic (≥3) graph t^k. With
τ = T(tx): trees give (τ − τ²/2)/t, edge-doubled trees give
((t+1)/4t)·τ², cycles ≥ 3 give −½log(1−τ) − τ/2 − τ²/4; summing yields
τ/t − τ²/(4t) − τ/2 − ½log(1−τ). Positivity and degree (n ≥ 2): the
coefficient of t^j is positive for 0 ≤ j ≤ n−1 already from the simple
forests with j edges (each contributes exactly t^j), and for j = n from
any spanning M with no tree component (the n-cycle for n ≥ 3, the doubled
edge for n = 2). The leading coefficient is Σ_{M: s+2d=n} (1/2)^{d(M)} =
vol P_n by Ehrhart theory (checked: 1/2 and 4 at n = 2, 3). At t = 1
Theorem B recovers Theorem A since (1·2/2)^{d} = 1. ∎

**Credit.** The route "parking polytope = Minkowski sum of simplices
Δ'_I = conv(0, Δ_I), lift by a cone vertex, apply [Po09, Thm 11.3]" was
carried out in general by Liu–Thawinrak [LT25, Prop. 7.3, Rem. 7.5,
Cor. 7.6] for arbitrary u-parking-function polytopes, giving the Ehrhart
polynomial as a sum over an abstract set of draconian sequences (their
D(PF(u))); with u = (0,1,…,n−1) their Example 7.4 is (a translate of)
our Q_n. We found this mid-session while checking novelty, after deriving
the same route independently; Theorem B's sum-form should be regarded as
the classical-case specialization of their Corollary 7.6. What is new
here is the combinatorial identification of the index set (Lemma 4:
draconian = sparse multiforests), the closed e.g.f., and everything in
Theorem A (which no prior work states or implies: [LT25] never
specializes the draconian set, computes a(n), or touches
A333331/loop-graphs; [AW22] stops at the slice sum; [Se24] poses the
enumeration as open).

**Remark (reciprocity check).** Ehrhart reciprocity predicts
(−1)^n i(P_n,−1) = #interior lattice points. At t = −1 only d(M) = 0
terms survive, giving (−1)^n Σ_{M simple} (−1)^{s(M)}. Verified against
brute-force interior counts: 0, 0, 5, 96 at n = 2,3,4,5 (script
`asymptotics_check.py`).

## 7. Certified computations and cross-checks

Environment: 4-core cloud sandbox, 15 GB RAM, Python 3.11.15, gcc 13.3.0.
All arithmetic exact (Python big integers / fractions; C with int64
counters). Every check below passed; total runtime under two minutes
except where noted.

| # | check | script | result |
|---|---|---|---|
| 1 | facet DP reproduces the 8 published terms of A333331 | `count_lattice_points.py` | 8/8 exact |
| 2 | facet DP vs literal 2^n-inequality enumeration, n ≤ 5 | `controls.py` | equal |
| 3 | positive control: corrupted bound changes counts (n = 3, 4) | `controls.py` | detects |
| 4 | partial-orientation in-degree vectors (3^{C(n,2)} enumeration) vs lattice points, as **sets**, n ≤ 5 | `controls.py` | sets equal |
| 5 | u(n) by edge-subset brute force, n ≤ 7 (Python) and n ≤ 8 (C, 30,260,340 subsets, ~3 min) | `controls.py`, `count_loopgraphs.c` | u(n) = a(n), incl. u(8) = 7 501 422 |
| 6 | S_n (sparse multiforests, 3^{C(n,2)} enumeration) vs a(n), n ≤ 5 | `verify_theorem.py` | equal |
| 7 | per-component identity of Lemma 5, k ≤ 12, exact | `verify_theorem.py` | equal |
| 8 | Ehrhart: dilate-DP vs S_n-formula vs closed e.g.f., n ≤ 5, t ≤ 4 | `verify_theorem.py` | all three agree |
| 9 | exact hull membership (rational phase-1 simplex over PF_n) vs facet description, n = 3, 4 | `verify_theorem.py` | agree pointwise |
| 10 | e.g.f. coefficients vs facet DP, n ≤ 40 | `asymptotics_check.py` | equal |
| 11 | Ehrhart reciprocity vs brute interior counts, n ≤ 5 | `asymptotics_check.py` | equal |
| 12 | asymptotic ratio a(n)/(C n^{n−1/4}) at n = 10..40 | `asymptotics_check.py` | 0.998 → 0.984, consistent |

Terms: `a_values.txt` lists a(1)–a(40) (CERTIFIED; the first independent
computation of any term past a(8)). The DP is O(n^4)-ish states and runs
to n = 40 in seconds; nothing here is compute-bound.

## 8. Prior work

- **Stanley** posed the polytope (AMM Problem 12191) and determined its
  vertices and facets; **Amanbayeva–Wang** [AW22] (Enumer. Comb. Appl. 2
  (2022), #S2R10; arXiv:2104.08454, read in full today) computed the
  f-vector, volume, and the slice-sum lattice-point formula, and asked
  (§6b) for the Ehrhart polynomial. A333331 is Stanley's entry (2020).
- **Postnikov** [Po09] (IMRN 2009; arXiv:math/0507163): draconian
  sequences (Def. 9.2), the lattice-point count for sums of dilated
  simplices (Thm 11.3). His Example 11.4 is the un-coned analogue of our
  Lemma 4: for the permutohedron, draconian sequences biject with forests
  — sparse multiforests are the coned counterpart.
- **Liu–Thawinrak** [LT25] (arXiv:2512.14199, Dec 2025, read in full
  today): Ehrhart polynomials of generalized parking-function polytopes
  in draconian-sum form (Cor. 7.6). See the credit note in §6.
- **Selig** [Se24] (Electron. J. Combin. 31(3) #P3.26; arXiv:2209.07301,
  read in full today): SR states of the stochastic sandpile on complete
  graphs = lattice points of the recurrent-state polytope (Thm 26), the
  subset-sum characterization (Thm 18), and the open enumeration question
  (§6) answered by Corollary A3.
- **Howroyd, Wiseman** (Jan/Mar 2024): the conjectures in A333331 proved
  here (Corollaries A1, A2); Wiseman's cluster includes A368596/A368730
  (non-choosable loop-graphs) and A368951, which our t_U(k) = t_S(k)
  equals (connected loop-graphs with #V = #E — the connected version of
  Theorem A, giving that entry a lattice-point interpretation too).
- Classical ingredients: Cayley's formula; the exponential formula
  [EC2, §5.1]; the labeled dissymmetry identity (Lemma 5) is folklore
  (Otter's idea); tree-function singular expansion and transfer
  [FS09, §VI].

We are not aware of any prior statement or proof of Theorem A, of the
identification in Lemma 4, or of any computation of a(n) for n ≥ 9
(checked today against the live OEIS entry, [AW22], [LT25], [Se24], and
targeted searches; see WRITEUP.md for the search log). Rediscovery
notice: Lemmas 1–3 amount to the polymatroid/Minkowski-sum realization of
P_n, which in hindsight is implicit in [LT25, Ex. 7.4] (and the coning
idea in their Rem. 7.5); we derived them independently from Stanley's
facets but claim no priority on them.

## 9. Open questions

1. **Bijective refinement.** Proposition 6 uses an arbitrary per-label-set
   bijection. Is there a natural bijection StoRec_n → U_n compatible with
   Selig's stochastic burning algorithm — e.g., reading off the unicyclic
   components from the burning record — refining the Cori–Rossin
   tree bijection on the deterministic shell?
2. **h-vector.** [AW22, §6a] also asks for the h-vector of P_n^*; the
   normal-fan description of [LT25] plus the S_n indexing may combine.
3. **Other cones.** Selig–Zhu (WALCOM 2025) study the SSM on complete
   bipartite graphs; the analogous polytope should be a sum of simplices
   Δ_{{0,i,j̄}} over K_{a,b}, and the same draconian machinery should
   identify the lattice-point count with bipartite sparse multiforests.
   Worth a future session.
4. **Interior points.** (−1)^n i(P_n,−1) = Σ_{M simple}(−1)^{s(M)} counts
   interior points; is there a direct sign-reversing involution
   explaining the values 0, 0, 5, 96, …?

## References

[AW22] A. Amanbayeva, D. Wang, *The convex hull of parking functions of
length n*, Enumer. Comb. Appl. 2:2 (2022), #S2R10 (arXiv:2104.08454).
[FS09] P. Flajolet, R. Sedgewick, *Analytic Combinatorics*, CUP 2009.
[LT25] F. Liu, W. Thawinrak, *Parking function polytopes*,
arXiv:2512.14199 (Dec 2025).
[Po09] A. Postnikov, *Permutohedra, associahedra, and beyond*, Int.
Math. Res. Not. 2009, no. 6, 1026–1106 (arXiv:math/0507163).
[Se24] T. Selig, *The stochastic sandpile model on complete graphs*,
Electron. J. Combin. 31(3) (2024), #P3.26 (arXiv:2209.07301).
[EC2] R. Stanley, *Enumerative Combinatorics*, vol. 2, CUP 1999.
OEIS A333331 (R. Stanley, 2020; comments A. Howroyd Jan 2024, G. Wiseman
Mar 2024), A368596, A368730, A368951 — all read live 2026-08-29.
