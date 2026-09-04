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
three colour pairs), contains at least 2m+3 vertices of degree 3 and between 1 and m−1
vertices of degree ≥ 5 (none of degree 4), and such that every other vertex lies on a face
avoiding V₁. When the big class has no vertex of degree ≥ 5 the bound is **proved**
(Theorem 3). The structure theorem turns the next open orders into finite checks that
brute force cannot reach: all 129,664,753 triangulations on 17 vertices (full census;
disc ≤ 3 = U(17), and exactly 2,652 of them attain it) and all triangulations on 23
vertices (≈ 6·10¹⁰ of them, unreachable directly) via an enumeration of the 109 million
2-connected plane graphs that can serve as T − V₁ — **CERTIFIED**, see §5 for the
outcome. We also extend the authors' exact discrepancy table from n ≤ 12 to n ≤ 17.

## 0. Setting and notation

T is a plane triangulation on n = 6m+5 vertices, m ≥ 1. A proper 4-colouring has classes
V₁, …, V₄. Throughout, "the bound" means disc(T) ≤ 2m−1, equivalently: a polychromatic
colouring exists whose smaller class has ≥ 2m+3 vertices (n − (2m+3) = 4m+2, and the
parity of ||R|−|B|| is that of n).

For v ∈ V₁ the *link* C_v is the cycle of neighbours of v in rotation order. A colour pair
{i,j} *occurs on* C_v if some edge of C_v has ends coloured i and j. Faces of T are
triangles; a face is *V₁-free* if it contains no vertex of V₁.

[BC] = Basti–Cremaschi, arXiv:2608.21585 (read in full). [KYY] = Kawarabayashi, Yoneda,
Yoneda, *The balanced four-color theorem*, arXiv:2607.13025: every planar graph with n ≥ 3
vertices has a proper 4-colouring in which each colour is used on fewer than n/2 vertices
(statement taken from the abstract; [BC] cite it as Corollary 17 — secondary for the
numbering).

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

**Theorem 3 (no high-degree vertex in the big class).** If T has a proper 4-colouring
with class sizes (3m+2, m+1, m+1, m+1) in which every vertex of the big class has degree 3,
then disc(T) ≤ 2m−1.

*Proof.* If Lemma 2 or Lemma 3 applies we are done; otherwise Lemma 6 gives
occ(u) ≤ 2m+1 for all u. Here H = ∅, so for u ∈ V₂ the hypotheses of Lemma 7 read
2 ≤ occ(u) ≤ 2m+1, and Σ_{u∈V₂} occ(u) = |D| = 3m+2 > 2(m+1) shows that some u ∈ V₂
has occ(u) ≥ 3. ∎

Equivalently: every triangulation obtained from an Eulerian triangulation on 3m+3
vertices with colour classes of size m+1 by inserting a degree-3 vertex into 3m+2 of its
faces satisfies the refined bound. (In that situation G = T − V₁ has 3(3m+3) − 6 edges,
i.e. is a triangulation, and is 3-colourable, hence Eulerian.)

**Theorem 2 (structure of a counterexample).** If n = 6m+5 and disc(T) ≥ 2m+1, then T has
a proper 4-colouring with class sizes (3m+2, m+1, m+1, m+1) such that, with V₁ the big
class: (i) every link C_v, v ∈ V₁, shows all three colour pairs, so deg v ∈ {3} ∪ [5, 2m+2];
(ii) Σ_{v∈V₁}(deg v − 3) ≤ 2m−1, so at least 2m+3 vertices of V₁ have degree 3 and at most
m−1 have degree ≥ 5; (iii) at least one vertex of V₁ has degree ≥ 5; (iv) every vertex of
W = V(T) − V₁ lies on a face disjoint from V₁, and there are between m+1 and 3m such
faces; (v) every u ∈ W is adjacent to at most 2m+1 degree-3 vertices of V₁; (vi) for every
choice of classes (F, S) and every u ∈ F the hypotheses of Lemma 7 fail.

*Proof.* Corollary of Lemma 1 for the colouring; (i) Lemma 2; (ii) Lemma 4; (iii)
Theorem 3; (iv) Lemmas 3 and 4; (v) Lemma 6; (vi) Lemma 7. ∎

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
order 13 ≤ n ≤ 17. CERTIFIED (12 min for n = 17 on one core, the four residue-class parts
of plantri's `res/mod` splitting; the 2,652 extremal triangulations are stored as
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

## 6. What remains

The bound for the whole residue class would follow from a proof that condition (vi) of
Theorem 2 is impossible under (i)–(v). Theorem 3 does this when H = ∅; with H ≠ ∅ the
obstruction is a vertex of H "blocking" every candidate u (its link has u next to an
S-vertex and an F–B edge elsewhere). Facts established but not needed above, recorded for
a future attempt: every Kempe (i,j)-component with i, j ∈ {2,3,4} of a counterexample's
colouring is balanced, and for each i ∈ {2,3,4} the (1,i)-subgraph has exactly one
component with more 1's than i's (otherwise a Kempe swap produces a colouring to which
Lemma 1 applies); and for each F and S, every u ∈ F with occ(u) ≥ 2 lies on the link of
some v ∈ H next to an S-vertex (the single flip with X = {u} would otherwise work).

## 7. Reproducibility

- `disc.c` — exact disc(T) for plantri planar_code input; `plantri n | ./disc -q -d 3`
  prints the histogram and dumps every triangulation with disc ≥ 3.
- `brute.py` — independent Python brute force (all 2^{n−1} masks), n ≤ 11.
- `struct_enum.c` — the structural enumeration of §5; `plantri -p -c2 -e25:30 -f8 12 |
  ./struct_enum 3`.
- `census.sh` — the n = 14..17 census driver (n = 17 in four `res/mod` parts).
- Runtimes (one core, shared with other jobs): n ≤ 16 in 2.3 min total; n = 17 in
  4 × ~4.2 min; the n = 23 enumeration in 277 s.

## References

- A. Basti, T. Cremaschi, *The Asayama–Matsumoto conjecture and a refined discrepancy
  bound*, arXiv:2608.21585v1 (21 Aug 2026). Read in full on 2026-09-04.
- K. Kawarabayashi, H. Yoneda, M. Yoneda, *The balanced four-color theorem*,
  arXiv:2607.13025 (14 Jul 2026). Abstract read; the theorem is used as stated there.
- Y. Asayama, N. Matsumoto, *Balanced polychromatic 2-coloring of triangulations*, Graphs
  Combin. 38 (2022) (secondary, via [BC]).
- G. Brinkmann, B. D. McKay, *Fast generation of planar graphs*, MATCH 58 (2007) — plantri.
