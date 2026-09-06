# Multicolour triangle Ramsey numbers with bounded chromatic number: Sawin's F(j,k)

**Status of this note:** research note, 2026-09-06 (one session). Every claim
carries a label — PROVED / CERTIFIED / NUMERICAL — following the conventions of
this repository. Citations marked (secondary) were not checked against the
primary source.

## Abstract

For integers j ≥ 2 and k ≥ 1 let F(j,k) be the largest n such that the edges of
K_n can be partitioned into k graphs, each triangle-free and vertex
j-colourable (Sawin, MathOverflow 513849, August 2026). Sawin proved
F(2,k) = 2^k, noted the trivial bound F(j,k) ≤ j^k and F(j,k+1) ≤ j·F(j,k), and
asked whether lim_k F(j,k)/j^k = 0 for some j; Wiesner conjectured
F(j,k) ≥ Σ_{i≤j} S(k+1,i). We prove F(3,k) ≥ max_t C(k,t)·2^{k−t} ≥ 3^k/(k+1)
by an explicit construction, so that lim F(3,k)^{1/k} = 3 (the best previously
recorded rate for three-colourable classes is 2^{3/2}, from the OpenAI
palette recursion as expounded by Morris), and more generally that
F(j,k) ≥ j^k/(2k+2)^{d_j} for a constant d_j — unconditionally for j ≤ 4, and
for every j given the saturated-map lemma of the OpenAI chapter. We compute
the first exact values: F(3,3) = 14 and F(4,3) = 16, with F(3,4) = 41
PENDING_F34, and certify F(3,5) ≥ 122, F(4,4) ≥ 44. Wiesner's formula is exact
at (3,3) (and at (3,4) PENDING_F34), a strict lower bound at (4,3), and its
j = 3 value (3^k+1)/2 is realised for k ≤ 5 by the set of ternary words with
an even number of 2's. Whether that set works for every k, which would give
lim F(3,k)/3^k ≥ 1/2, is left open; an LYM argument shows that no palette
construction with an antichain of palettes can exceed max_t C(k,t)2^{k−t}.

## 1. Definitions and the type formulation

**Definition.** F(j,k) is the largest n for which there is a map
κ : E(K_n) → [k] such that for every colour c the graph G_c = κ^{−1}(c) is
triangle-free and admits a proper vertex colouring with j colours. (We call the
proper colouring of G_c its *labelling* ℓ_c : V → [j].)

**Lemma 1.1 (type formulation; PROVED).** F(j,k) equals the largest size of a
set S ⊆ [j]^k for which there is a map col : (S choose 2) → [k] with
col(x,y) ∈ D(x,y) := {c : x_c ≠ y_c} and no triangle x,y,z ∈ S with
col(x,y) = col(x,z) = col(y,z).

*Proof.* Given κ and labellings ℓ_c, send a vertex v to its type
τ(v) = (ℓ_1(v),…,ℓ_k(v)) ∈ [j]^k. If τ(u) = τ(v) for u ≠ v then the edge uv has
some colour c and ℓ_c(u) = ℓ_c(v), contradicting properness; so τ is
injective, and col(τ(u),τ(v)) := κ(uv) lies in D(τ(u),τ(v)) for the same
reason. Monochromatic triangles correspond. Conversely, given S and col, the
colour classes are triangle-free and the c-th coordinate is a proper
j-colouring of G_c since every edge of colour c differs at coordinate c. ∎

All searches below use the type formulation: the vertices are distinct points
of the cube [j]^k, an edge may only receive a coordinate in which its
endpoints differ, and no colour class contains a triangle.

## 2. Elementary bounds

**Lemma 2.1 (PROVED).**
(a) F(j,1) = 2 and F(j,k+1) ≤ j·F(j,k) [Sawin]; hence F(j,k) ≤ F(j,d)·j^{k−d}
for d ≤ k, and in particular F(j,k) ≤ 2·j^{k−1}.
(b) Equivalently: three points of S on an axis-parallel line of [j]^k
pairwise differ only in that coordinate, so all three edges are forced to the
same colour; every line meets S in at most two points.
(c) F(j,k) ≤ r_3(k) − 1, where r_3(k) is the k-colour Ramsey number of the
triangle, and F(j,k) is non-decreasing in j.
(d) F(j,k+l) ≥ F(j,k)·F(j,l).

*Proof of (d).* Take an optimal colouring κ_1 of K_m with colours [k] and
labellings ℓ_c, and an optimal colouring κ_2 of K_n with colours
{k+1,…,k+l}. On V × W colour {(v,w),(v',w')} by κ_1(vv') if v ≠ v' and by
κ_2(ww') if v = v'. A colour c ≤ k has class G_c^{(1)}[K̄_n] (each vertex blown
up into an independent set): a triangle in it has three distinct first
coordinates pairwise adjacent in G_c^{(1)}, impossible, and (v,w) ↦ ℓ_c(v) is a
proper j-colouring. A colour c > k has class a disjoint union of copies of
G_c^{(2)}. ∎ This is the classical product argument for r_3 (e.g.
r_{k+l}(3) − 1 ≥ (r_k(3) − 1)(r_l(3) − 1)); the only observation is that it
preserves the chromatic numbers of the colour classes.

**Corollary 2.2 (PROVED).** For each j the limits lim_k F(j,k)^{1/k}
(Fekete, from (d)) and lim_k F(j,k)/j^k (the ratio is non-increasing in k by
(a)) exist, the second being the infimum of the ratios.

## 3. Three-colourable classes: the antichain construction

**Theorem 3.1 (PROVED).** For every k ≥ 1 and 0 ≤ t ≤ k,
F(3,k) ≥ C(k,t)·2^{k−t}. Consequently
F(3,k) ≥ max_t C(k,t)2^{k−t} ≥ 3^k/(k+1), and
F(3,k) ≥ (1+o(1))·(3/(2√π))·3^k/√k; in particular lim_k F(3,k)^{1/k} = 3.

*Construction.* Colours are [k]. For each t-subset P ⊆ [k] (the *palette*
of missing colours) let V_P = {±1}^{[k]∖P}, the set of sign vectors indexed by
the colours outside P. The vertex set is the disjoint union of the V_P, of
size C(k,t)2^{k−t}.
- Inside V_P: colour {u,u'} by the least c ∉ P with u_c ≠ u'_c.
- Between V_P and V_Q, P ≠ Q: let a = min(Q∖P) and b = min(P∖Q) (both
  non-empty because |P| = |Q|). For u ∈ V_P, v ∈ V_Q colour {u,v} by a if
  u_a = v_b and by b otherwise. (u_a is defined because a ∉ P; v_b because
  b ∉ Q.)
- Labelling of colour class c: λ_c(P,u) = u_c if c ∉ P and λ_c(P,u) = 0 if
  c ∈ P; three labels {+1,−1,0}.

*Proof.* Properness: an edge of colour c inside V_P has u_c ≠ u'_c; a cross
edge of colour a between V_P and V_Q has a ∉ P, a ∈ Q, so its labels are
u_a ∈ {±1} and 0; likewise for colour b. Triangle-freeness of colour c: three
vertices of one block cannot pairwise differ at c (two values). Two vertices
u,u' ∈ V_P and one v ∈ V_Q: the edge uu' has a colour outside P, so c ∉ P and
c ≠ b; hence c = a, so u_a = v_b = u'_a, whereas uu' of colour a requires
u_a ≠ u'_a. Two vertices v,v' ∈ V_Q and one u ∈ V_P: now c ∉ Q, so c ≠ a and
c = b; uv and uv' of colour b give u_a ≠ v_b and u_a ≠ v'_b, hence v_b = v'_b
(the labels are binary), whereas vv' of colour b requires v_b ≠ v'_b. Three
vertices in distinct blocks P,Q,R: every cross colour lies in the symmetric
difference of the two palettes, and no c lies in P△Q, Q△R and P△R
simultaneously (c ∈ P△Q and c ∈ P△R force [c∈Q] = [c∈R]). The
asymptotics: C(k,t)2^{k−t}/3^k is the probability that a Binomial(k,1/3)
variable equals t; the k+1 values sum to 1, so the maximum is at least
1/(k+1), and by the local limit theorem it is (1+o(1))/√(2πk·(1/3)(2/3)) =
(1+o(1))·3/(2√(πk)). The rate: 3^k/(k+1) ≤ F(3,k) ≤ 2·3^{k−1}. ∎

The construction was also checked mechanically (`antichain.py` +
`verify_colouring.c`, which enumerates all C(n,3) triples and checks every
label) for (k,t) = (2,1), (3,1), (4,1), (4,2), (5,1), (5,2), (6,2), (6,3),
(7,2), (7,3), (8,3), up to K_1792 with 8 colours. Theorem 3.1 is the case
r = 2, s = 1 of Theorem 4.2 below with 𝒫 the family of all t-subsets (any two
distinct t-subsets satisfy |P∖Q| ≥ 1) and F(2,k−t) = 2^{k−t}.

**Remark 3.2 (an LYM barrier; PROVED).** Call a *palette construction* any
colouring built from blocks V_P = {±1}^{[k]∖P} indexed by a family 𝒫 of
subsets of [k], with cross edges coloured inside P△Q. For the cross rule of
Theorem 3.1 the family must be an antichain (both P∖Q and Q∖P non-empty), and
then Σ_{P∈𝒫} 2^{k−|P|} = Σ_P C(k,|P|)2^{k−|P|}/C(k,|P|) ≤
max_t C(k,t)2^{k−t}·Σ_P 1/C(k,|P|) ≤ max_t C(k,t)2^{k−t} by the LYM
inequality. So Theorem 3.1 is optimal among antichain palette constructions,
and reaching a positive proportion of 3^k requires comparable palettes — which
is exactly what the even-weight sets of §6 have.

**Remark 3.3 (context).** The palette-and-block scheme is the recursion of
OpenAI's *Ten Advances*, Chapter 9 (Proposition 3.1 there: blocks indexed by a
palette family P_j, a copy of the previous colouring on each block, cross
edges coloured inside P△Q using a fixed "two-sided coordinate cover"
f,g : [H]^s → [H]^s of Lemma 2.2 there, and the invariant "χ(Γ_{κ_j}(c)) ≤
j+1"; the chapter says "The saturated-matrix construction is not new; its
application to R(3,…,3) is."). Two observations make the j = 3 case sharp: for
binary labels the cover has dimension s = 1 (f = id, g = −id), so *every*
t-subset can be a palette and the "least d" bookkeeping disappears; and no
Ramsey-type loss is needed. Morris's exposition of the OpenAI bound states, for
three-colourable classes, "Theorem 2.1. For some n = 2^{3k−o(k)}, there exists
a colouring of the edges of K_n with 2k colours such that each colour forms a
triangle-free tripartite graph", i.e. a rate of 2^{3/2} ≈ 2.83 per colour;
Theorem 3.1 raises this to the optimal rate 3.

## 4. General j: rate j for every fixed j

**Definition.** A *saturated pair of dimension s over [r]* is a pair of maps
f,g : [r]^s → [r]^s such that for all x,y ∈ [r]^s there is d ∈ [s] with
x_d = f(y)_d or y_d = g(x)_d. Let s_r be the least such s.

**Lemma 4.1 (PROVED / CERTIFIED).** s_2 = 1 (f = id, g = −id). s_3 = 2: no
pair exists for s = 1 since for each y the r−1 values x ≠ f(y) would all need
g(x) = y, forcing Σ_y|g^{−1}(y)| ≥ r(r−1) > r; a pair for (r,s) = (3,2) was
found by SAT and is verified from the definition in `saturated.py`:

    f: 00→10 01→22 02→01 10→20 11→00 12→02 20→12 21→11 22→21
    g: 00→21 01→00 02→20 10→02 11→11 12→12 20→22 21→10 22→01

For r = 4 no pair of dimension 2 exists (SAT, UNSAT). For every r a saturated
pair exists with s = O(r² log² r): this is Lemma 2.2 of the OpenAI chapter
(with s = m(m+1)+1, m = ⌈2H log H⌉), which the chapter attributes to the
saturated-matrix construction of Alon, Ben-Eliezer, Shangguan and Tamo, JCTB
144 (2020) — cited here (secondary): the chapter was read in the local copy,
the JCTB paper was not.

**Theorem 4.2 (PROVED).** Let r ≥ 2, let (f,g) be a saturated pair of
dimension s over [r], and let 𝒫 be a family of t-subsets of [k] with
|P∖Q| ≥ s for all distinct P,Q ∈ 𝒫. Then F(r+1,k) ≥ |𝒫|·F(r,k−t).

*Proof.* For P ∈ 𝒫 let V_P carry an optimal colouring of K_{F(r,k−t)} with
colour set [k]∖P and proper r-labellings ℓ^P_c (c ∉ P). For P ≠ Q fix
a_1<…<a_s in Q∖P and b_1<…<b_s in P∖Q, and for u ∈ V_P, v ∈ V_Q put
x(u) = (ℓ^P_{a_d}(u))_{d≤s} and y(v) = (ℓ^Q_{b_d}(v))_{d≤s}. Colour uv by a_d
for the least d with x_d(u) = f(y(v))_d if such d exists, and otherwise by b_d
for the least d with y_d(v) = g(x(u))_d, which exists by saturation. Label
colour class c by λ_c(w) = ℓ^{P(w)}_c(w) ∈ [r] if c ∉ P(w) and by r+1 if
c ∈ P(w). Properness: inside blocks by hypothesis; a cross edge of colour
c ∈ P△Q has exactly one endpoint whose palette contains c. Triangles: within
a block, none; u,u' ∈ V_P, v ∈ V_Q with all edges of colour c: uu' has colour
c ∉ P so c ∉ {b_d}, hence c = a_d and ℓ^P_{a_d}(u) = f(y(v))_d =
ℓ^P_{a_d}(u'), contradicting properness of ℓ^P_{a_d} on the edge uu' of colour
a_d; two vertices in V_Q and one in V_P symmetrically with g; three blocks as in
Theorem 3.1 since cross colours lie in the symmetric differences. ∎

**Lemma 4.3 (PROVED).** For k ≥ 1, t ≤ k and s ≥ 1 there is a family of
t-subsets of [k] with pairwise |P∖Q| ≥ s of size at least C(k,t)/(2k)^{s−1}.

*Proof.* Let p be a prime with k < p ≤ 2k (Bertrand). Partition the t-subsets
by the residues (Σ_{i∈T} i^m mod p)_{m=1}^{s−1}; some class has at least
C(k,t)/p^{s−1} members. Two distinct members T,T' with |T∖T'| = m' ≤ s−1 would
have multisets T∖T' and T'∖T of size m' with equal power sums up to exponent
s−1 ≥ m' in F_p; Newton's identities (invertible since m' < p) give equal
elementary symmetric polynomials, so the multisets coincide in F_p and hence,
as the elements of [k] are distinct mod p, T = T'. ∎

**Corollary 4.4 (PROVED for j ≤ 4; PROVED conditional on Lemma 4.1's cited
part for j ≥ 5).** F(j,k) ≥ j^k/(2k+2)^{d_j} with d_2 = 0, d_3 = 1 and
d_{r+1} = d_r + s_r; hence lim_k F(j,k)^{1/k} = j for every j ≥ 2.

*Proof.* Induction on r using Theorem 4.2 with the family of Lemma 4.3:
F(r+1,k) ≥ max_t C(k,t) r^{k−t}/((2k)^{s_r−1}(2k+2)^{d_r}) ≥
(r+1)^k/((k+1)(2k)^{s_r−1}(2k+2)^{d_r}) ≥ (r+1)^k/(2k+2)^{d_r+s_r}. The base
r = 2 is F(2,k) = 2^k and r = 3 is Theorem 3.1. ∎

The induction step r = 3 → 4 was checked mechanically (`blockconstruct.py`
with the saturated pair above, greedy palette families, blocks carrying the
E_3 colouring): K_56 with 6 colours and K_98 with 7 and with 8 colours, every
class triangle-free and properly 4-labelled (`verify_colouring.c`).

Theorem 3.1 and Corollary 4.4 do not decide Sawin's question, which concerns
the constant lim F(j,k)/j^k: the constructions lose a polynomial factor.

## 5. Exact values and certified bounds

**Theorem 5.1 (CERTIFIED unless marked).**

| cell | value | lower bound witness | upper bound |
|---|---|---|---|
| F(j,1) | 2 | one edge | Lemma 2.1(a) — PROVED |
| F(2,2) | 4 | K_4 = C_4 ∪ 2K_2 | C_5 is not bipartite; R(3,3) = 6 — PROVED |
| F(j,2), j ≥ 3 | 5 | K_5 = C_5 ∪ C_5 | R(3,3) = 6 — PROVED |
| F(2,k) | 2^k | Sawin | Sawin — PROVED |
| F(3,3) | **14** | `witness_F3_3_n14.txt`, `col_even0_k3.txt`, circulant `circ_14_3_3.json` | UNSAT at 15: `certs/F33_n15.cnf` + `.drup`, 8,366-line DRUP proof checked by `rup_check` |
| F(3,4) | **41** PENDING_F34 | `witness_F3_4_n41.txt`, `col_even0_k4.txt`, circulant `circ_41_4_3.json` | ≤ 42 by Lemma 2.1(a) from F(3,3) = 14 (PROVED); PENDING_F34_UPPER |
| F(3,5) | ≥ 122 | `col_even0_k5.txt`, circulant `circ_122_5_3.json` | ≤ 3·F(3,4) |
| F(3,6) | PENDING_F36 | | ≤ 3·F(3,5) |
| F(4,3) | **16** | `witness2_F4_3_n16.txt` | r_3(3) = 17 (Greenwood–Gleason 1955, via Radziszowski's dynamic survey — secondary) |
| F(j,3), j ≥ 4 | 16 | same | same |
| F(4,4) | ≥ 44 | circulant `circ_44_4_4.json` | ≤ min(4·16, r_3(4) − 1) = 61, r_3(4) ≤ 62 (Fettes–Kramer–Radziszowski 2004, via the survey — secondary) |

Every witness file is checked from the definition by a program that shares no
code with the searches: `verify_witness.py` (type witnesses: every pair
coloured by a differing coordinate, all C(n,3) triples free of monochromatic
triangles) and `verify_circulant.py` (circulant witnesses: partition of the
difference classes, all triples, and the explicit proper j-colouring of every
class).

F(3,3) = 14 is the first value of F(j,k) beyond F(2,k) and F(j,2), and shows
that the chromatic restriction bites: the two triangle-free 3-colourings of
K_16 have Clebsch colour classes (χ = 4), and even the Clebsch graph minus one
or two vertices is 4-chromatic (checked by SAT), so F(3,3) ≤ 15 follows from
the structure of the K_16 colourings while the true value is 14.

## 6. The even-weight sets and Wiesner's conjecture

Let E_k = {x ∈ {0,1,2}^k : the number of coordinates equal to 2 is even} and
O_k its complement, |E_k| = (3^k+1)/2 = Σ_{i≤3} S(k+1,i), Wiesner's value for
j = 3.

**Proposition 6.1 (CERTIFIED).** E_k admits a valid colouring for
2 ≤ k ≤ 5, and O_k for 2 ≤ k ≤ 4 (files `col_even0_k*.txt`, `col_even1_k*.txt`,
all verified). Hence F(3,k) ≥ (3^k+1)/2 for k ≤ 5. PENDING_F36_E6

**Observations (PROVED).** (i) Every axis-parallel line meets E_k in the two
points with a 0/1 entry (if the fixed coordinates contain an even number of
2's) or in the single point with entry 2 (otherwise); every 2-dimensional
plane meets E_k in 5 or 4 points and every 3-dimensional subcube in 14 or 13.
The SAT-found extremal sets for k = 3, 4 have exactly this profile (layer
sizes 5,5,4 and 14,14,13 in every direction). (ii) E_k = ⊔_{U even}
{0,1}^{[k]∖U} × {2}^U is a palette construction whose palettes are *all* even
subsets — a nested family — with the cross edges between nested palettes
coloured through 0/1 differences; Remark 3.2 shows this nesting is necessary
for density 1/2. (iii) The SAT colourings of E_k are not unique and no simple
local rule reproduces them: the only invariant rule we found valid is
"colour by the first differing coordinate", which works precisely on binary
subcubes; every rule that colours a pair by a function of its coordinate-wise
difference pattern alone fails already for k = 2 (the pairs
{(2,2),(0,0)} and {(2,2),(1,0)} have the same pattern but must receive
different colours in every valid colouring of E_2), and a family of sixty
sign-based inductive rules (`induct.py`) fails by k = 3.

**Symmetry (CERTIFIED).** For k = 3 and k = 5 there are valid colourings of
E_k invariant under the global swap 0 ↔ 1 and under the cyclic shift of
coordinates (which rotates the colours), so all colour classes are isomorphic
(`sym_cyc.py`, `col_sym_k3.txt`); for k = 4 no such colouring exists, because
the points 0000, 1111, 2222 ∈ E_4 form a triangle fixed by the shift, whose
three edges would have to carry every colour.

**Non-uniqueness of extremal sets (CERTIFIED).** All 14-point vertex sets of
[3]^3 admitting a valid colouring were enumerated with blocking clauses:
33,831 sets in 37 orbits under S_3 ≀ S_3 (order 1296); E_3 is the orbit of
size 27. For k = 2 there are 45 five-point sets in 2 orbits (E_2 and the set
{00,01,10,12,21}). So E_k is a natural extremal family, not the extremal
family.

**Conjecture 6.2 (Wiesner's j = 3 case, restated).** E_k admits a valid
colouring for every k; equivalently F(3,k) ≥ (3^k+1)/2 and
lim F(3,k)/3^k ≥ 1/2. Combined with the certified values, F(3,k) = (3^k+1)/2
for k ≤ 4 PENDING_F34; whether the ratio F(3,k)/3^k tends to 1/2 or below is
open. Note F(3,k)/3^k is non-increasing with F(3,4)/81 = 41/81 ≈ 0.506
PENDING_F34.

Wiesner's formula is not exact in general: at (4,3) it gives 15 while
F(4,3) = 16.

## 7. Circulant witnesses

Colouring Z_n by difference classes (colour of {v,w} = colour of ±(v−w))
yields Cayley colourings whose classes are circulant graphs; the class is
triangle-free iff its difference set is sum-free. SAT over the 2^{⌊n/2⌋·k}
assignments with an explicit proper j-colouring of every class found
circulant witnesses for F(3,3) ≥ 14 (Z_14: ±{1,4,7}, ±{2,3}, ±{5,6}),
F(3,4) ≥ 41, F(3,5) ≥ 122 and F(4,4) ≥ 44, each in under 5 s, and proved that
no circulant witness exists for F(4,4) ≥ 45, nor any circulant 4-colouring of
K_46, K_50 or K_51 with triangle-free classes (so Wiesner's predicted
F(4,4) ≥ 51 — which would improve Chung's 1973 bound r_3(4) ≥ 51 — cannot come
from a circulant). The classical quartic-residue 4-colouring of K_41, whose
classes are the cyclotomic graphs, has all four classes 4-chromatic and is
therefore not an F(3,4) witness.

## 8. Open questions

1. Prove Conjecture 6.2 (a valid colouring of E_k for all k), or find a
   construction with lim F(3,k)/3^k > 0 at all.
2. Is F(3,k) = (3^k+1)/2 for all k? The first undecided cell is F(3,5) ∈
   {122, 123} PENDING_F34.
3. Determine F(4,4) ∈ [44, 61]; in particular decide Wiesner's 51.
4. Improve d_j in Corollary 4.4, i.e. the polynomial loss; for j = 3 the loss
   is √k against a conjectured constant 2.

## 9. Reproducibility

All computations are exact. Searches: python-sat 1.9 (CaDiCaL 1.5.3). Certified
UNSAT boundaries: Glucose 4 with DRUP logging, checked by
`tools/satcert/rup_check.c` (this repository's own checker). Witness checks:
`verify_witness.py`, `verify_circulant.py`, `verify_colouring.c`. Hardware:
4 cores, 15 GB. Runtimes are in the README. No random seeds are used anywhere.

## AI assistance

This note was produced with substantial AI assistance (Claude, in the
session logged as `log/2026-09-06-chromatic-ramsey.md`); the literature
search for §3–4 used an AI agent reading the OpenAI chapter, Morris's
exposition, and MathOverflow. Every proof above was written out and checked
by hand in the session; every computational claim ships code and data.
