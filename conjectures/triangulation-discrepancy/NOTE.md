# The refined discrepancy bound for plane triangulations in the open residue class n ≡ 5 (mod 6)

*Research note, session of 2026-09-04. AI-assisted (Claude); see the repository README.*

## Abstract

A red–blue vertex colouring of a plane triangulation T is *polychromatic* if every face sees
both colours; disc(T) is the least ||R| − |B|| over such colourings. Basti and Cremaschi
(arXiv:2608.21585, 21 Aug 2026) prove disc(T) ≤ n − 2⌈n/3⌉ for all n (the Asayama–Matsumoto
conjecture, via the balanced four-colour theorem of Kawarabayashi–Yoneda–Yoneda) and the
sharper disc(T) ≤ U(n) := n − 2⌈(n+2)/3⌉ for n ≥ 6, n ≢ 5 (mod 6); they state that the
residue class n ≡ 5 (mod 6) — where U(6m+5) = 2m−1 against the universal 2m+1 — "remains
open", and verify U(11) = 1 by exhaustive computation. We prove a structure theorem for a
hypothetical counterexample (Theorem 2): it must carry a proper 4-colouring with class
sizes (3m+2, m+1, m+1, m+1) whose big class V₁ is *fully mixed* (every link shows all
three colour pairs), contains at least 2m+3 vertices of degree 3 and between 3 and m−1
vertices of degree ≥ 5 (none of degree 4), and such that every other vertex lies on a face
avoiding V₁. When the big class has at most two vertices of degree ≥ 5 the bound is
**proved** (Theorem 3, by a single recolouring plus an Euler-formula count); since a
counterexample on 6m+5 vertices has at most m−1 such vertices, **the refined bound holds
for n = 11, 17 and 23**, the first three orders of the open class, and any counterexample
has n ≥ 29. Independently of the proof, the structure theorem turns those orders into
finite checks that brute force cannot reach, and we ran them: all 129,664,753
triangulations on 17 vertices (full census; disc ≤ 3 = U(17), exactly 2,652 attain it) and
all triangulations on 23 vertices (≈ 6·10¹⁰, unreachable directly) via an enumeration of
the 109 million 2-connected plane graphs that can serve as T − V₁ — **CERTIFIED**, §5. We
also extend the authors' exact discrepancy table from n ≤ 12 to n ≤ 17.

## 0. Setting and notation

T is a plane triangulation on n = 6m+5 vertices, m ≥ 1. A proper 4-colouring has classes
V₁, …, V₄. Throughout, "the bound" means disc(T) ≤ 2m−1, equivalently: a polychromatic
colouring exists whose smaller class has ≥ 2m+3 vertices (n − (2m+3) = 4m+2, and the
parity of ||R|−|B|| is that of n).

For v ∈ V₁ the *link* C_v is the cycle of neighbours of v in rotation order. A colour pair
{i,j} *occurs on* C_v if some edge of C_v has ends coloured i and j. Faces of T are
triangles; a face is *V₁-free* if it contains no vertex of V₁.

[BC] = Basti–Cremaschi, arXiv:2608.21585 (read in full). [KYY] = Kawarabayashi, Yoneda,
Yoneda, *The balanced four-color theorem*, arXiv:2607.13025, Corollary 17 (checked in
the HTML version on 2026-09-04): for k ≥ 4, every planar graph with n ≥ 3 vertices admits
a k-colouring in which each colour is used on at most ⌈(n−2)/(k−2)⌉ vertices; for k = 4
and n = 6m+5 this is 3m+2, i.e. fewer than n/2, and the bound is attained by K_{1,1,n−2}.

## 1. The class vector

**Lemma 1.** Let c be a proper 4-colouring of T with class sizes a ≥ b ≥ c ≥ d and
a ≤ 3m+2. Then the bound holds unless (a, b, c, d) = (3m+2, m+1, m+1, m+1).

*Proof.* Every face uses three distinct colours, so merging two classes into red and the
other two into blue is polychromatic; it suffices to find two classes whose sizes sum to
some s ∈ [2m+3, 4m+2]. Put r = a + d, s = b + c = n − r. As in [BC, proof of Thm 2.2],
r ≥ b, c gives n ≤ 3r, and d ≤ (n − a)/3 gives r ≤ (n + 2a)/3 < 2n/3; so
r, s ≥ ⌈n/3⌉ = 2m+2. If r, s ≥ 2m+3 we are done. If r = 2m+2 then b + c = 4m+3 with
b, c ≤ a ≤ r, forcing (a, b, c, d) = (2m+2, 2m+2, 2m+1, 0): T is properly 3-coloured by
V₁, V₂, V₃; colour V₂ red, V₃ blue, one vertex of V₁ red and the rest of V₁ blue — every
face has one vertex of each class, so it is bichromatic — with classes 2m+3 and 4m+2.
If s = 2m+2 then r = 4m+3, d = r − a ≥ m+1, and b ≥ c ≥ d give s ≥ 2m+2 with equality
only for b = c = d = m+1, a = 3m+2. ∎

By [KYY], T has a proper 4-colouring with all classes ≤ ⌊(n−1)/2⌋ = 3m+2. Hence:

**Corollary.** If disc(T) ≥ 2m+1 then T has a proper 4-colouring with class sizes
(3m+2, m+1, m+1, m+1).

**Standing assumption for §2–§4.** c is such a colouring, V₁ its big class (an independent
set of 3m+2 vertices), W = V₂ ∪ V₃ ∪ V₄ (three independent sets of m+1 vertices).

## 2. Two flips

**Lemma 2 (a free vertex of V₁).** If some v ∈ V₁ has a link on which some colour pair
{i, j} ⊆ {2, 3, 4} does not occur, the bound holds.

*Proof.* Let k be the third colour. Colour V_k red, V_i ∪ V_j blue, v blue, V₁ − v red.
A V₁-free face has colours {2,3,4}, so it contains a red vertex (in V_k) and a blue one.
A face {u, x, y} with u ∈ V₁ − v has u red; x, y are adjacent W-vertices, not both in the
independent set V_k, so one of them is blue. A face {v, x, y}: v is blue; x, y are
consecutive on C_v; they are not both red (V_k is independent) and not both blue (two
adjacent vertices of V_i ∪ V_j would realise the pair {i, j} on C_v). Sizes: red
(m+1) + (3m+1) = 4m+2, blue (2m+2) + 1 = 2m+3. ∎

Call c *fully mixed* if every link C_v, v ∈ V₁, shows all three pairs {2,3}, {2,4}, {3,4}.
A properly 3-coloured 4-cycle shows only two pairs (its colour sequence is a,b,a,b or
a,b,a,c), so in a fully mixed colouring every v ∈ V₁ has degree 3 or degree ≥ 5. Let
D = {v ∈ V₁ : deg v = 3} and H = V₁ − D.

**Lemma 3 (a free vertex of W).** If some w ∈ W lies on no V₁-free face, the bound holds.

*Proof.* Say w ∈ V_k and {i, j} are the other two colours of W. Colour V_k − w red,
V_i ∪ V_j ∪ {w} blue, V₁ red. A V₁-free face has one vertex in each of V_i, V_j, V_k, and
its V_k-vertex is not w, so it is bichromatic. A face {u, x, y} with u ∈ V₁ has u red and
x, y adjacent in W, not both in V_k − w, so one is blue. Sizes: red m + (3m+2) = 4m+2,
blue (2m+2) + 1 = 2m+3. ∎

## 3. Counting consequences

**Lemma 4.** Suppose neither Lemma 2 nor Lemma 3 applies. Let f₀ be the number of V₁-free
faces. Then

    Σ_{v∈V₁} (deg v − 3) ≤ 2m − 1,   m+1 ≤ f₀ ≤ 3m,   |H| ≤ m − 1,   |D| ≥ 2m + 3,

and every v ∈ V₁ has deg v ≤ 2m+2, every v ∈ H has 5 ≤ deg v.

*Proof.* T has 2n − 4 = 12m+6 faces; V₁ is independent, so each face contains at most
one vertex of V₁, and v ∈ V₁ lies on exactly deg v faces. Hence f₀ = 12m+6 − Σ deg v.
By Lemma 3 every one of the 3m+3 vertices of W lies on a V₁-free face, and such a face
has three W-vertices, so 3f₀ ≥ 3m+3, i.e. Σ deg v ≤ 11m+5, which is the first
inequality since Σ 3 = 9m+6; f₀ ≤ 3m because every degree is ≥ 3. By Lemma 2's
consequence, vertices of H have degree ≥ 5, so 2|H| ≤ 2m−1. ∎

**Lemma 5 (the graph T − V₁).** G := T − V₁ is a 2-connected plane graph on 3m+3 vertices,
properly 3-coloured by V₂, V₃, V₄, whose faces are: for each v ∈ V₁ the open disc bounded
by C_v (an *occupied* face, of length deg v ≥ 3), and the f₀ V₁-free faces of T (*empty*
triangles). Conversely T is recovered from G by inserting one vertex into each occupied
face, joined to the whole boundary.

*Proof.* The disc bounded by the cycle C_v contains v and the edges vx, x ∈ C_v, and
nothing else (they triangulate it), so it is a face of G with boundary C_v; every other
face of G contains no vertex of V₁, is bounded by edges of G, and is a union of faces of
T none of which meets V₁; since consecutive such faces are separated by edges of G, it is
a single triangle. All faces are bounded by cycles, so G is 2-connected. ∎

So a counterexample is determined by: a 2-connected plane graph G on 3m+3 vertices, an
equitable proper 3-colouring of G, and the choice of which triangular faces are empty
(non-triangular faces are occupied), subject to: 3m+2 occupied faces, no face of length
4 or > 2m+2, at most m−1 non-triangular faces with total excess Σ(len − 3) ≤ 2m−1,
every vertex on an empty triangle, and every occupied boundary fully mixed. This is the
enumeration of §5.

## 4. The single flip

For u ∈ W let occ(u) be the number of D-vertices adjacent to u.

**Lemma 6 (no dominant vertex).** If neither Lemma 2 nor Lemma 3 applies, then
occ(u) ≤ 2m+1 for every u ∈ W.

*Proof.* Let u ∈ F, with S, B the other two classes of W, and suppose occ(u) ≥ 2m+2.
A D-neighbour d of u has link {u, s, b} with s ∈ S, b ∈ B, so on the link L_u of u the
vertex d is flanked by s and b. Each S-vertex of L_u flanks at most two vertices of L_u,
and L_u contains at most |S| = m+1 S-vertices, so occ(u) ≤ 2m+2, with equality only if
all m+1 vertices of S lie on L_u, each flanked by two D-neighbours of u; likewise for B.
Then L_u alternates D-vertices and W-vertices, no two W-vertices are consecutive on L_u,
so every face at u contains a vertex of D ⊆ V₁: u lies on no V₁-free face, contradicting
the assumption that Lemma 3 does not apply. ∎

**Lemma 7 (single flip).** Let F be one of V₂, V₃, V₄, let S be another and B the third,
and let u ∈ F. For v ∈ H say that *u blocks v* if u ∈ C_v, u is C_v-adjacent to a vertex of
S, and C_v has an edge with one end in F − u and the other in B. Let
q(u) = #{v ∈ H : u ∈ C_v and u is C_v-adjacent to a vertex of S} and
p(u) = #{v ∈ H : every edge of C_v with ends in F and B is incident to u}. If u blocks
no vertex of H and

    occ(u) + p(u) ≥ 2   and   occ(u) + q(u) ≤ 2m + 1,

then the bound holds.

*Proof.* Colour S ∪ {u} red and (F − u) ∪ B blue. For v ∈ V₁: an edge of C_v with both
ends red has both ends in S ∪ {u}, hence is an edge us (S is independent); an edge with
both ends blue has one end in F − u and the other in B (F and B are independent). Say v is
*forced blue* if C_v has a red–red edge and *forced red* if it has a blue–blue edge. A
vertex forced both ways lies in H (for d ∈ D, C_d = {f, s, b} has a red–red edge only if
f = u and then its only F–B edge is incident to u) and is blocked by u; by hypothesis
there is none. Give every forced vertex its forced colour and choose the colours of the
free vertices so that exactly k vertices of V₁ are blue, for a k to be fixed. Then every
face {v, x, y}, v ∈ V₁, is bichromatic (x, y consecutive on C_v cannot be monochromatic in
v's colour), and every V₁-free face {s, f, b} has s red and b blue. The number of forced-blue
vertices is occ(u) + q(u) (the D-neighbours of u, whose links contain the edge us, and the
q(u) vertices of H); the number of forced-red vertices is (|D| − occ(u)) + (|H| − p(u)).
So k can be any integer in [occ(u) + q(u), occ(u) + p(u)], using |D| + |H| = 3m+2. The
classes have sizes blue = (2m+1) + k and red = (m+2) + (3m+2 − k), both ≥ 2m+3 exactly
when 2 ≤ k ≤ 2m+1; the hypotheses provide such a k. ∎

**Lemma 8 (an outside vertex with two degree-3 neighbours).** Suppose neither Lemma 2
nor Lemma 3 applies and 1 ≤ h := |H| ≤ 2. Let N = ⋃_{v∈H} V(C_v) ⊆ W be the set of
W-vertices lying on the link of a high-degree vertex. Then some u ∈ W − N has occ(u) ≥ 2.

*Proof.* Suppose instead that every u ∈ W − N has occ(u) ≤ 1.

(1) *Inner D-vertices.* For each class F, the vertices of F − N have occ ≤ 1, so distinct
D-vertices whose F-neighbour lies outside N have distinct such neighbours: at most |F − N|
of them. Hence at most |W − N| = 3m+3−|N| vertices of D have a neighbour outside N, and at
least |D| − (3m+3−|N|) = |N| − h − 1 have all three neighbours in N. Call them *inner*;
each occupies a triangular face of G whose three vertices lie in N, and distinct inner
vertices occupy distinct faces. Let τ_D ≥ |N| − h − 1 be the number of these faces.

(2) *The plane graph G″ = G[N].* Its faces are of three kinds: the h faces bounded by the
links C_v (each contains only its vertex v of T); the faces containing no vertex of W − N
and not of the first kind — such a face contains no vertex or edge of G (an edge of G with
both ends in N is in G″, one with an end outside N would put that end inside the face), so
it is a face of G, i.e. a triangle: τ_D of them are the inner D-faces and ε_N of them are
empty triangles with all vertices in N; and ρ ≥ 0 faces containing at least one vertex of
W − N, with total boundary-walk length Λ ≥ 3ρ. Let c ≥ 1 be the number of components of
G″ and σ = Σ_{v∈H} deg v = Σ_v |C_v| ≥ |N|. Euler's formula and the count of edge sides
give

    h + τ_D + ε_N + ρ = E(G″) − |N| + 1 + c,    2E(G″) = σ + 3τ_D + 3ε_N + Λ,

whence τ_D + ε_N = 2h + 2ρ + 2|N| − 2 − 2c − σ − Λ.

(3) *Covering.* By Lemma 3 every vertex of N lies on an empty triangle of T. Such a
triangle either has all three vertices in N — one of the ε_N faces, covering at most three
vertices of N — or contains a vertex of W − N, in which case it lies inside a face of the
third kind and its vertices of N lie on that face's boundary walk. Hence |N| ≤ 3ε_N + Λ.

(4) *Conclusion.* From (2) and (3),
τ_D ≤ 2h + 2ρ + 2|N| − 2 − 2c − σ − Λ − (|N| − Λ)/3 ≤ 2h − 4 − σ + (5/3)|N|,
using Λ ≥ 3ρ and c ≥ 1. With (1) this gives σ ≤ 3h − 3 + (2/3)|N|. For h = 1, N = V(C_v)
and σ = |N|, so |N| ≤ (2/3)|N|, absurd. For h = 2, σ ≥ |N| and σ ≥ 5·2 = 10 (Lemma 4):
if |N| ≥ 10 then σ ≥ |N| > 3 + (2/3)|N|; if |N| ≤ 9 then σ ≥ 10 > 3 + 6 ≥ 3 + (2/3)|N|.
Either way the inequality fails. ∎

**Theorem 3 (at most two high-degree vertices in the big class).** If T has a proper
4-colouring with class sizes (3m+2, m+1, m+1, m+1) in which at most two vertices of the
big class have degree ≥ 5, then disc(T) ≤ 2m−1. In particular, since a counterexample
has at most m−1 such vertices (Lemma 4), **the refined bound holds for every
triangulation on n = 11, 17 and 23 vertices**, the first three orders of the open class.

*Proof.* If Lemma 2 or Lemma 3 applies we are done; otherwise every vertex of V₁ has
degree 3 or ≥ 5 and h ≤ 2, and Lemma 6 gives occ(u) ≤ 2m+1 for every u ∈ W. If h = 0,
Σ_{u∈V₂} occ(u) = |D| = 3m+2 > 2(m+1) shows that some u ∈ V₂ has occ(u) ≥ 3; with H = ∅
the hypotheses of Lemma 7 (any S) reduce to 2 ≤ occ(u) ≤ 2m+1. If h ∈ {1, 2}, Lemma 8
provides u ∈ W − N with occ(u) ≥ 2; as u lies on no link of a vertex of H it blocks none
of them and p(u) = q(u) = 0, so Lemma 7 applies with any S. For n ∈ {11, 17, 23} we have
m ≤ 3, so any counterexample would have h ≤ m − 1 ≤ 2, contradicting the first
statement together with the Corollary of Lemma 1. ∎

For h = 0 the statement reads: every triangulation obtained from an Eulerian
triangulation on 3m+3 vertices with colour classes of size m+1 by inserting a degree-3
vertex into 3m+2 of its faces satisfies the refined bound (there G = T − V₁ has
3(3m+3) − 6 edges, i.e. is a triangulation, and is 3-colourable, hence Eulerian).

**Theorem 2 (structure of a counterexample).** If n = 6m+5 and disc(T) ≥ 2m+1, then
m ≥ 4 and T has a proper 4-colouring with class sizes (3m+2, m+1, m+1, m+1) such that,
with V₁ the big class: (i) every link C_v, v ∈ V₁, shows all three colour pairs, so
deg v ∈ {3} ∪ [5, 2m+2]; (ii) Σ_{v∈V₁}(deg v − 3) ≤ 2m−1, so at least 2m+3 vertices of V₁
have degree 3 and at most m−1 have degree ≥ 5; (iii) at least three vertices of V₁ have
degree ≥ 5; (iv) every vertex of W = V(T) − V₁ lies on a face disjoint from V₁, and there
are between m+1 and 3m such faces; (v) every u ∈ W is adjacent to at most 2m+1 degree-3
vertices of V₁; (vi) for every choice of classes (F, S) and every u ∈ F the hypotheses of
Lemma 7 fail — in particular every u ∈ W with occ(u) ≥ 2 lies on the link of some vertex
of degree ≥ 5.

*Proof.* Corollary of Lemma 1 for the colouring; (i) Lemma 2; (ii) Lemma 4; (iii)
Theorem 3, and then m − 1 ≥ 3; (iv) Lemmas 3 and 4; (v) Lemma 6; (vi) Lemma 7 (a vertex
u with occ(u) ≥ 2 on no high-degree link would satisfy it with p = q = 0). ∎

## 5. Exact computations

All computations use plantri 5.5 (Brinkmann–McKay) for generation and the C programs of
this directory; every decision is exact (backtracking over colourings with monochromatic-
face pruning), no floating point anywhere. Positive controls: `disc` reproduces [BC,
Table 2] for 4 ≤ n ≤ 12 exactly (in particular the 2 and 16 triangulations of discrepancy
2 at n = 10, 12 and all 1,249 of discrepancy 1 at n = 11), and agrees with an independent
brute-force Python implementation of [BC]'s method (all 2^{n−1} masks) for n ≤ 11; the
generated counts equal OEIS A000109 at every order.

**Theorem 4 (census to n = 17).** The exact distribution of disc(T) over all
triangulations with 13 ≤ n ≤ 17 is

| n | triangulations (A000109) | disc 0 | disc 1 | disc 2 | disc 3 | disc 4 | U(n) |
|---|---|---|---|---|---|---|---|
| 13 | 49,566 | – | 49,562 | – | 4 | – | 3 |
| 14 | 339,722 | 339,300 | – | 422 | – | – | 2 |
| 15 | 2,406,841 | – | 2,406,752 | – | 89 | – | 3 |
| 16 | 17,490,241 | 17,481,631 | – | 8,596 | – | 14 | 4 |
| 17 | 129,664,753 | – | 129,662,101 | – | 2,652 | – | 3 |

In particular **every triangulation on 17 vertices satisfies disc(T) ≤ 3 = U(17)** (the
second order of the open residue class), and the refined bound is attained at every
order 13 ≤ n ≤ 17. CERTIFIED (15 min for n = 17 on one core, the four residue-class parts
of plantri's `res/mod` splitting, 258 + 247 + 193 + 208 s; the 2,652 extremal triangulations are stored as
certificates in `data/n17_disc3.txt`, the 4 + 89 + 14 extremal ones of orders 13, 15, 16
in `data/n13_disc3.txt`, `data/n15_disc3.txt`, `data/n16_disc4.txt`).

**Theorem 5 (n = 23 through the structure theorem).** Every triangulation on 23 vertices
satisfies disc(T) ≤ 5 = U(23). CERTIFIED: of the 109,507,132 two-connected plane graphs
on 12 vertices with 25–30 edges and faces of length ≤ 8, 1,848,652 pass the face filter
(7,595 with no non-triangular face, 307,423 with one, 1,533,634 with two); they admit
11,678 equitable proper 3-colourings (up to renaming colours); these give 998,162
choices of empty triangles covering every vertex, of which 948,057 have every occupied
boundary fully mixed; every one of the resulting 23-vertex triangulations has
disc(T) = 1 — none is a counterexample, and none even reaches discrepancy 3. Run time
277 s on one core (shared). Summary in `results_struct_m3.txt`.

Method: by Theorem 2 (i), (ii), (iv) and Lemma 5, a counterexample on 23 vertices arises
from a 2-connected plane graph G on 12 vertices with e(G) = 63 − Σ_{v∈V₁} deg v ∈ [25, 30]
edges, faces of length 3 or 5–8, at most two non-triangular faces with total excess ≤ 5,
an equitable proper 3-colouring, and a set of empty triangular faces (all other faces
occupied, 11 occupied in all) covering every vertex, with every occupied boundary fully
mixed. `struct_enum` reads all 2-connected plane graphs on 12 vertices with 25–30 edges
and faces of length ≤ 8 from plantri (`-p -c2 -e25:30 -f8`; 109,507,132 graphs, all
embeddings), applies these filters, enumerates the colourings and empty-face sets, builds
T, and computes disc(T) exactly. Controls: at m = 1 the same program finds the octahedral
family (32 candidate configurations, all of discrepancy 1) and at m = 2 it finds 2,051
fully-mixed candidates, all of discrepancy 1, consistent with Theorem 4.

**A second parametrisation, and n = 29.** By Lemma 5 a counterexample T with h
high-degree big-class vertices H and D = V₁ − H yields the triangulation T′ = T − D on
3m+3+h vertices, in which H is an independent set of vertices of degree in [5, 2m+2] with
Σ(deg − 3) ≤ 2m−1, G = T′ − H, and the faces of G are the h links of H together with the
faces of T′ not incident to H (the D-triangles and the empty triangles). `hstruct.c`
enumerates candidates from plantri's triangulations on 3m+3+h vertices in this way (all
independent h-sets with the degree constraints, then colourings and empty sets as before).
Cross-check at m = 3: by h = 0, 1, 2 it finds 488,648 / 412,239 / 101,434 fully mixed
configurations (the two parametrisations count configurations with different
multiplicities, so the totals 1,002,321 and 948,057 need not agree), all of discrepancy 1,
all admitting a single flip, all with a vertex off the high-degree links having two
degree-3 neighbours — the situation of Lemma 8, as the proof predicts. At n = 29 (m = 4)
Theorem 3 leaves only h = 3, i.e. T′ a triangulation on 18 vertices (A000109(18) =
977,526,957) with three pairwise non-adjacent vertices of degrees (5,5,5) or (5,5,6);
the run is reported in §5b.

## 5b. n = 29

**Theorem 6 (n = 29).** Every triangulation on 29 vertices satisfies disc(T) ≤ 7 = U(29).
CERTIFIED: by Theorem 3 a counterexample would have exactly three big-class vertices of
degree ≥ 5, so T′ = T − D is one of the 977,526,957 triangulations on 18 vertices with
three pairwise non-adjacent vertices of degrees (5,5,5) or (5,5,6) (Lemma 4: Σ(deg − 3) ≤ 7).
`hstruct 4 3` processed all of them in four plantri `res/mod` parts (T′ read: 244,448,771 +
244,311,056 + 244,313,162 + 244,453,968 = 977,526,957): 4,151,483,419 admissible
independent triples, all passing the face filter, 12,828,786 equitable 3-colourings,
62,588,172 choices of empty triangles covering every vertex, 60,070,002 of them with every
link fully mixed — and **every one of the resulting 29-vertex triangulations has
disc(T) = 1**. Moreover every one of them admits a single flip in the sense of Lemma 7
(0 exceptions), although 72,709 of them have no vertex off the three links with two
degree-3 neighbours — so at n = 29 the situation of Lemma 8 does fail, and Lemma 7's
flips (with the blocking analysis) are what carry the day. Wall time per part
4,158 / 8,049 / 7,989 / 7,987 s on a shared machine (the last three were paused for
an hour to give the cores to another run); summaries in `results_struct_m4.txt`.

Together with Theorem 3: the refined bound holds for every n ≡ 5 (mod 6) with n ≤ 29,
proved for n ≤ 23 and certified at n = 29; a counterexample needs n ≥ 35 and at least
three high-degree big-class vertices.

## 6. What remains

**The first configuration beyond Theorem 3 exists, and is harmless.** Condition (vi) of
Theorem 2 can hold: if every vertex of W lies on the link of a high-degree vertex, and each
such link is a hexagon coloured periodically 2,3,4,2,3,4, then every vertex of every link
is of mixed type with a second edge of each of its two types elsewhere on the link, so no
single flip in the sense of Lemma 7 survives. The smallest instance has m = 5 (n = 35),
h = 3, three pairwise disjoint hexagonal links covering the 18 vertices of W (this uses the
whole degree budget Σ(deg − 3) = 9 = 2m−1), 14 stellated triangles and 6 empty triangles
partitioning W. Whether such a T exists is a small exact-cover problem on the 216 rainbow
triples of W; `hexpants.py` (pysat/CaDiCaL) finds solutions — after discarding models
whose vertex links are not single paths, the survivors are triangulations of the pair of
pants, hence planar — and computes disc(T) exactly for each. Of the first 1,063 SAT
models, 400 are valid pants triangulations, and **every one of the 400 resulting
35-vertex triangulations has disc(T) = 1**, against the bound U(35) = 9
(`results_hexpants.txt`; the 400 are a sample of the solution set, not all of it). So the
obstruction is an artefact of the flip family: these triangulations admit polychromatic
colourings that no single flip produces, and the proof for h ≥ 3 must use a richer
construction (NUMERICAL as a statement about the configuration in general; CERTIFIED for
the instances computed). The optimal colourings found are not class-based at all: in the
first solution the three hexagons are coloured R,R,R,R,R,B / R,R,R,B,R,B / R,B,R,B,R,B
(12 red among the 18 vertices of W), the high-degree vertices B, B, R and ten of the
fourteen degree-3 vertices blue. A W-colouring with ≤ m blue vertices forming an
independent transversal of the empty triangles would also work (all degree-3 and
high-degree vertices then go blue, giving classes 3m+3−k and 3m+2+k), but here the six
empty triangles partition W, so no transversal has fewer than m+1 vertices.

*The general target, for a future proof.* Colour W with k blue vertices so that (i) every
empty triangle is bichromatic and (ii) no high-degree link carries both a red–red and a
blue–blue edge; then every degree-3 vertex is forced (blue if its triangle has ≥ 2 red
vertices, red if ≥ 2 blue) and every high-degree vertex is forced or free. Writing a₂ for
the number of degree-3 triangles with ≥ 2 blue vertices and h_R for the number of
high-degree vertices coloured red, the red class has 3m+3−k+a₂+h_R vertices, and the
bound holds exactly when k − m ≤ a₂ + h_R ≤ k + m − 1. Lemma 7 is the case k = 2m+1 of
this (blue = (F − u) ∪ B), and the hexagon example realises k = m+1, a₂ = 4, h_R = 1. A
proof for h ≥ 3 would exhibit a transversal-like blue set with the right number of
"doubly blue" degree-3 triangles; the family of §6 is the natural test bed.

The bound for the whole residue class would follow from a proof that condition (vi) of
Theorem 2 is impossible under (i)–(v) for h ≥ 3 — which the example above shows is false as
stated — or, more realistically, from a colouring construction beyond Lemma 7. Lemma 8's count gives
σ ≤ 3h − 3 + (2/3)|N| for a configuration in which every vertex off the high-degree links
has at most one degree-3 neighbour; for h = 3 this is not yet a contradiction (three
pairwise disjoint links of length 5 or 6 satisfy it), and for large h the set N can be all
of W, so the "outside vertex" route must be replaced by an analysis of the blocking in
Lemma 7 (a vertex of H blocks u when its link has u next to an S-vertex and an F–B edge
elsewhere). Facts established but not needed above, recorded for a future attempt: every
Kempe (i,j)-component with i, j ∈ {2,3,4} of a counterexample's colouring is balanced, and
for each i ∈ {2,3,4} the (1,i)-subgraph has exactly one component with more 1's than i's
(otherwise a Kempe swap produces a colouring to which Lemma 1 applies). The computations
of §5 found, at n = 17 and n = 23, that every configuration satisfying (i), (ii), (iv)
admits a single flip in the sense of Lemma 7 (0 exceptions among 2,051 and 948,057), and
every one of them even has a vertex off all high-degree links with two degree-3
neighbours (the situation of Lemma 8).

## 7. Reproducibility

- `disc.c` — exact disc(T) for plantri planar_code input; `plantri n | ./disc -q -d 3`
  prints the histogram and dumps every triangulation with disc ≥ 3.
- `brute.py` — independent Python brute force (all 2^{n−1} masks), n ≤ 11.
- `struct_enum.c` — the structural enumeration of §5; `plantri -p -c2 -e25:30 -f8 12 |
  ./struct_enum 3`.
- `census.sh` — the n = 14..17 census driver (n = 17 in four `res/mod` parts).
- `hstruct.c` — the second parametrisation (§5, §5b); `plantri 18 k/4 | ./hstruct 4 3`.
- `hexpants.py` — the SAT construction of §6 (needs `python-sat`); `python3 hexpants.py 400`.
- Runtimes (one core each, shared with other jobs): n ≤ 16 in 2.3 min total; n = 17 in
  4 × ~4 min; the n = 23 enumeration in 277 s (365 s with the flip statistic); `hstruct`
  at m = 3 in 11 s for all h; `hexpants.py 400` in about 3 min.

## References

- A. Basti, T. Cremaschi, *The Asayama–Matsumoto conjecture and a refined discrepancy
  bound*, arXiv:2608.21585v1 (21 Aug 2026). Read in full on 2026-09-04.
- K. Kawarabayashi, H. Yoneda, M. Yoneda, *The balanced four-color theorem*,
  arXiv:2607.13025 (14 Jul 2026). Abstract read; the theorem is used as stated there.
- Y. Asayama, N. Matsumoto, *Balanced polychromatic 2-coloring of triangulations*, Graphs
  Combin. 38 (2022) (secondary, via [BC]).
- G. Brinkmann, B. D. McKay, *Fast generation of planar graphs*, MATCH 58 (2007) — plantri.
