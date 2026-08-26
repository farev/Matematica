# Strong 6-edge-colorability of truncated cubic graphs: a local obstruction, the smallest counterexamples, and a certified census

**Date.** 2026-08-26. One session (cloud sandbox, 4 cores).
**AI disclosure.** Research conducted with substantial AI assistance
(Claude); all proofs below are short enough to check by hand, and every
computational claim ships code and certificates.

## Abstract

Kardoš asked (Problem 4.1 of the open problems of the 33rd Workshop on
Cycles and Colourings, arXiv:2511.02892v1, 4 Nov 2025, §4 — quoted from
the original; see §7 for the citation audit): *is every diamond-free
claw-free cubic graph strongly 6-edge-colorable — equivalently, is
χ′ₛ(T(G)) = 6 for every cubic graph G?* We show the two phrasings come
apart, and resolve the first one in the negative. Diamond-free claw-free
cubic graphs are exactly K₄ together with the truncations T(H) of
connected cubic loopless **multigraphs** H (Lemma 0), and a doubled edge
of H whose endpoints share a third neighbour — a **balloon**, the
truncation-side image of a loop — is a complete local obstruction: if H
contains a balloon, T(H) admits no strong 6-edge-coloring (Theorem 3, a
ten-line palette argument in a dart reformulation proved in Lemma 1).
This yields, for every admissible order 18 + 6k, diamond-free claw-free
cubic graphs with strong chromatic index 7; the smallest, G₁₈ = T(H₆),
has 18 vertices and is unique at that order. Every such counterexample
is necessarily **bridged** (Proposition 6: a balloon's stem is a bridge),
so the refutation is confined to the bridged part of the class; the
2-edge-connected reading of the problem — the setting of Oum's structure
theorem, which is where the "well-known fact" behind the question comes
from — is instead *supported* here: all 26,867 bridgeless quotients of
order ≤ 16 other than the triple edge give strongly 6-edge-colorable
truncations. All previously
published examples attaining the tight bound 7 of Lin–Lin contain
diamonds (per Kardoš's own description of them, §7), so diamonds are
not needed for tightness. In the other
direction, a double-verified census of all 36,093 truncations of cubic
multigraphs of order ≤ 16 finds χ′ₛ(T(H)) = 6 **exactly** when H has no
balloon and is not the triple edge (whose truncation is the prism,
χ′ₛ = 9), prompting a complete characterization conjecture — verified
onward through all 287,459 balloon-free quotients of order 18; and the
intended reading of the problem survives strongly: every truncation of a
**simple** connected cubic graph on ≤ 20 vertices (556,471 graphs, T on
up to 60 vertices) is strongly 6-edge-colorable, extending the
truncated-prism family of Han–Cui.

## 0. Definitions

A **strong edge coloring** of a graph G assigns colors to edges so that
every color class is an *induced matching*: two edges of the same color
neither share a vertex nor are joined by an edge of G. χ′ₛ(G) is the
least number of colors. Equivalently, χ′ₛ(G) = χ(C(G)) where the
**conflict graph** C(G) has V(C) = E(G) and X ~ Y iff X, Y share a
vertex or an endpoint of X is adjacent to an endpoint of Y.

The **truncation** T(H) of a connected cubic loopless multigraph H:
replace each vertex u by a triangle on vertices u_e indexed by the edge
instances e at u (triangle edges), and join u_e to v_e for every edge
instance e = uv (link edges). T(H) is a connected cubic simple graph on
3·n(H) vertices; e.g. the triple edge truncates to the triangular prism,
K₄ (as a multigraph quotient of nothing) does not arise.

A **diamond** is K₄ minus an edge; a **claw** is K₁,₃; both as induced
subgraphs. "DFCF" abbreviates connected, cubic, claw-free, diamond-free,
simple.

**Lemma 0 (structure).** The DFCF graphs are exactly K₄ and the
truncations T(H) of connected cubic loopless multigraphs H, and H is
determined by T(H) up to isomorphism. (For 2-edge-connected G this is
the diamond-free case of Oum's Proposition 1, whose proof gives the same
triangle-contraction argument; see §7. The statement here drops
2-edge-connectivity to plain connectivity — which is what the
counterexample needs, since by Proposition 6 it is bridged — and adds
uniqueness of H.)

*Proof.* For cubic G and a vertex u with N(u) = {a,b,c}, let inner(u) be
the number of edges among {a,b,c}. Claw-free ⟺ inner ≥ 1 everywhere.
If inner(u) = 2, the two inner edges (sharing a vertex or not) make
{u,a,b,c} induce K₄ minus an edge — a diamond. So in a DFCF graph
inner(u) ∈ {1,3}; inner(u) = 3 forces the component K₄. Otherwise every
vertex lies in exactly one triangle: a vertex in two triangles would
have inner ≥ 2 (they share an edge through it, or use ≥ 4 neighbours).
Hence the triangles are pairwise vertex-disjoint and partition V;
contracting each gives a connected cubic loopless multigraph H with
G ≅ T(H). Conversely T(H) is DFCF: each T-vertex u_e has neighbours
{u_f, u_g, v_e} with u_f u_g an edge (no claw), and every triangle of
T(H) is a contracted one — a triangle with vertices in two different
contracted triangles would put some vertex in two triangles, giving
inner ≥ 2 (excluded above) — so triangles are disjoint and no diamond
exists. Uniqueness: the triangle partition of T(H) is its unique
triangle decomposition by the same argument. ∎

Two named configurations in a quotient H:

* a **dumbbell**: a doubled edge x‖y whose endpoints' third edges
  ("stems") end at two *distinct* vertices — the expansion of a plain
  edge into a digon;
* a **balloon**: a doubled edge u‖v whose endpoints' third edges uw, vw
  meet at a *common* vertex w — the expansion of a loop at w. The stem
  of the balloon is w's third edge s.

("Balloon" and "dumbbell" are local names for this note.)

## 1. The dart model

Fix a connected cubic loopless multigraph H with n(H) ≥ 2. A **dart** is
an incidence (u, e), u a vertex, e an edge instance at u; each vertex
carries three darts.

**Lemma 1 (dart model).** Strong 6-edge-colorings of T(H) correspond
bijectively to pairs (c, t), where c maps edge instances of H to
{0,…,5}, t maps darts to {0,…,5}, and:

1. **(vertex)** at every vertex u with darts e, f, g the six values
   c(e), c(f), c(g), t_u(e), t_u(f), t_u(g) are pairwise distinct
   (so c is in particular a proper edge coloring of H, parallel
   instances counting as adjacent);
2. **(edge)** for every edge instance e = uv: t_u(x) ≠ t_v(y) for all
   darts x ≠ e at u and y ≠ e at v.

The correspondence: c(e) = color of the link edge of e, and t_u(e) =
color of the triangle edge of u's triangle *opposite* u_e (the one not
containing u_e).

*Proof.* We enumerate the conflict pairs of T(H). Write Δ_u for the
triangle at u. (i) Two edges of Δ_u share a vertex: conflict. (ii) A
triangle edge X ⊂ Δ_u and a link edge of instance g at u: if u_g ∉ X
then X and the link share no vertex, but u_g is adjacent to both ends of
X, so they conflict; if u_g ∈ X they share it: conflict either way. So
every triangle edge at u conflicts with every link at u. (iii) Two link
edges, of instances e = uv and f = xy: if e and f share an H-endpoint,
say u = x, then u_e and u_f are adjacent inside Δ_u, so the links
conflict. If they share none, each endpoint of e's link has as
neighbours only its two triangle mates and the far end of its own link,
none of which is an endpoint of f's link: no conflict. So links
conflict iff their H-edges share a vertex. (iv) Triangle edges X ⊆ Δ_u
and Y ⊆ Δ_v with u ≠ v: the only edges of T(H) between Δ_u and Δ_v are
the links of instances e = uv, joining u_e to v_e; hence X and Y
conflict iff some instance e = uv has u_e ∈ X and v_e ∈ Y — in
particular, never when u, v are non-adjacent. Finally, a triangle edge
X ⊆ Δ_u never conflicts with the link of an instance g = wz not
incident to u: the link's endpoints w_g, z_g have all their neighbours
inside Δ_w, Δ_z and on the link itself, none of them in Δ_u.

Now translate. Constraints inside (i)+(ii)+(iii) at a fixed u say
exactly that the six edges around Δ_u — three triangle edges, three
links — get six distinct colors: this is (vertex), once triangle edges
at u are renamed t_u(·) via the opposite-vertex indexing (the triangle
edge opposite u_e is written t-value of dart e; the three t_u-values
enumerate Δ_u's edges). Constraint family (iv) for the instance e = uv:
the triangle edges at u containing u_e are exactly those opposite the
*other* darts x ≠ e, i.e. with colors t_u(x), x ≠ e; likewise at v; so
(iv) says t_u(x) ≠ t_v(y) for x ≠ e ∋ u, y ≠ e ∋ v — this is (edge).
Every conflict pair of T(H) lies in one of the families above, so the
translation is faithful both ways. ∎

Around every triangle the six incident edges are pairwise conflicting
(a 6-clique in C(T(H))), so **χ′ₛ(T(H)) ≥ 6 always**; deciding strong
6-colorability decides χ′ₛ = 6 versus ≥ 7.

Write P(u) = {c(e) : e ∋ u} (the link palette) and
P̄(u) = {0,…,5} ∖ P(u) = {t_u(e) : e ∋ u}: by (vertex), t_u is a
bijection from u's darts onto P̄(u).

**Lemma 2 (interface).** For an edge instance s = wz, the only
constraints of Lemma 1 joining the two sides of s are: both sides use
the same c(s), and S_w ∩ S_z = ∅, where S_w := {t_w(x) : x ∋ w, x ≠ s}
= P̄(w) ∖ {t_w(s)}. In particular, if s is a bridge with pendant piece P
(w ∈ P), the piece interacts with the rest only through its **boundary
state** (c(s), S_w) — a color and a 2-set not containing it.

*Proof.* By inspection of Lemma 1: (vertex) constraints are local to
one endpoint's side (each mentions c(s), known to both); (edge) for
instances ≠ s is internal to one side; (edge) for s itself reads
t_w(x) ≠ t_z(y) for x ≠ s, y ≠ s, i.e. S_w ∩ S_z = ∅. c(s) ∉ S_w since
S_w ⊆ P̄(w) while c(s) ∈ P(w). ∎

## 2. The balloon obstruction

**Theorem 3 (Balloon Lemma).** If H contains a balloon, then T(H) has
no strong 6-edge-coloring; hence χ′ₛ(T(H)) ≥ 7.

*Proof.* Suppose (c, t) as in Lemma 1 exists. Let the balloon be
u ‖ v (instances e₁, e₂), f = uw, g = vw, and let s be w's third edge.
Put a = c(e₁), b = c(e₂), x = c(f), y = c(g); by (vertex), {a,b,x},
{a,b,y}, {x,y,c(s)} are 3-sets.

*Step 1: x ≠ y.* If x = y then P̄(u) = P̄(v) =: P with |P| = 3. The
(edge) constraint for e₁ says the 2-sets P ∖ {t_u(e₁)} and
P ∖ {t_v(e₁)} are disjoint — impossible inside a 3-set.

*Step 2: the doubled edge freezes everything.* Write
{0,…,5} = {a,b,x,y} ⊔ {p,q}. Then P̄(u) = {y,p,q} and P̄(v) = {x,p,q}.
The (edge) constraint for e₁ makes P̄(u)∖{t_u(e₁)} and P̄(v)∖{t_v(e₁)}
disjoint; since p and q lie in both complements, each must be removed
on at least one side, so {p,q} ⊆ {t_u(e₁), t_v(e₁)} — a set of size at
most two, whence {t_u(e₁), t_v(e₁)} = {p,q}. The same for
e₂ gives {t_u(e₂), t_v(e₂)} = {p,q}. As t_u is injective,
{t_u(e₁), t_u(e₂)} = {p,q}, and therefore t_u(f) = y, the remaining
element of P̄(u); symmetrically t_v(g) = x.

*Step 3: the common neighbour has nowhere to go.* The (edge) constraint
for f = uw gives {t_u(e₁), t_u(e₂)} ∩ {t_w(g), t_w(s)} = ∅, i.e.
{p,q} ∩ {t_w(g), t_w(s)} = ∅; the constraint for g = vw likewise gives
{p,q} ∩ {t_w(f), t_w(s)} = ∅. So no t_w-value equals p or q:
{p,q} ∩ P̄(w) = ∅, i.e. {p,q} ⊆ P(w) = {x, y, c(s)}. But p, q ∉ {x,y}
by construction, so both p and q would have to equal c(s):
contradiction. ∎

An exhaustive machine enumeration of the balloon piece's dart
assignments (`boundary.py`) independently finds **zero** realizable
boundary states, confirming Theorem 3; note the proof never used the
stem's far side, so the balloon piece is infeasible in isolation —
stronger than needed.

**Lemma 4 (Dumbbell Lemma).** Let x ‖ y be a dumbbell with stems s_L at
x and s_R at y. In any (c, t), the colors c(s_L) ≠ c(s_R), and both
boundary pair-sets coincide: S_x = S_y = {p,q} where
{0,…,5} = {c(d₁), c(d₂), c(s_L), c(s_R)} ⊔ {p,q}; moreover every state
pair of this shape is realizable inside the dumbbell. Hence the
dumbbell's transfer relation is exactly
{ ((c₁,S),(c₂,S)) : |S| = 2, c₁ ≠ c₂, {c₁,c₂} ∩ S = ∅ } — 180 labelled
pairs.

*Proof.* Steps 1–2 of Theorem 3 applied verbatim to the doubled pair
give c(s_L) ≠ c(s_R) (else P̄(x) = P̄(y), impossible as in Step 1),
{t_x(d₁), t_x(d₂)} = {p,q} = {t_y(d₁), t_y(d₂)}, t_x(s_L) = c(s_R) and
t_y(s_R) = c(s_L); so S_x = S_y = {p,q}. Conversely, given
(c₁, S), (c₂, S) of the stated shape, color the two parallel instances
with the two elements of {0,…,5} ∖ S ∖ {c₁,c₂} and take the forced t:
all Lemma 1 constraints inside the dumbbell hold by direct check
(machine-verified in `boundary.py`: exactly 180 pairs). ∎

## 3. Consequences

Let H₆ be the 6-vertex quotient with edge multiset
{02, 04, 05, 13², 15, 24², 35}: two balloons (1‖3 tied at 5, 2‖4 tied
at 0) with their stems joined by the bridge 05. Let **G₁₈ = T(H₆)**
(graph6 `Q??CA?_cAOA_DC@`PO@OOOW?`_?`, 18 vertices).

**Theorem 5.**
1. G₁₈ is a connected claw-free diamond-free cubic simple graph with
   χ′ₛ(G₁₈) = 7. Consequently the answer to Problem 4.1 in its
   diamond-free claw-free phrasing is **no**, and among claw-free cubic
   graphs the tight value 7 is attained without diamonds.
2. G₁₈ is the unique smallest such graph: every DFCF graph on < 18
   vertices other than the prism (χ′ₛ = 9) is strongly 6-edge-colorable,
   and G₁₈ is the only exception on exactly 18 vertices.
3. For every k ≥ 0 the chain quotient C_k (two balloons joined through
   k dumbbells) gives a DFCF graph T(C_k) on 18 + 6k vertices with
   χ′ₛ ≥ 7; DFCF graphs exist only on orders 4 and multiples of 6, so
   counterexamples exist at *every* order ≥ 18 admitting any DFCF graph
   beyond order 4. χ′ₛ(T(C_k)) = 7 exactly is certified for k ≤ 8, and
   holds for all k by the bound χ′ₛ ≤ 7 of Lin–Lin (§7; their abstract
   read in the original).

*Proof.* (1) Family membership is Lemma 0 (or the definition-level check
in `verify_census.py`); χ′ₛ ≥ 7 is Theorem 3 (H₆ has a balloon);
χ′ₛ ≤ 7 by explicit verified 7-coloring (`certs/G18_7col.txt`). The
independent certificate: UNSAT at 6 colors of the definition-level CNF,
DRUP proof checked by `tools/satcert/rup_check` (`certs/G18.cnf`,
`certs/G18.drup`). That Lin–Lin's tight examples all contain diamonds is
Kardoš's description of them in the primary text (§7), not read in
Lin–Lin. (2) Census below: all quotients of orders 2–4 and the five
other order-6 quotients are decided 6-colorable with definition-checked
witnesses; K₄ is 6-colorable; DFCF graphs on other orders < 18 do not
exist (Lemma 0 + parity). Uniqueness at 18: of the six order-6
quotients, only H₆ contains a balloon, and the other five carry verified
6-colorings; the geng-side enumeration of all 41,301 cubic graphs on 18
vertices confirms exactly six DFCF graphs with exactly this one
exception. (3) Theorem 3 for the lower bound; certificates for k ≤ 8 in
`data/family_results.txt`; the general upper bound is Lin–Lin's theorem,
which we cite and do not re-prove. ∎

**Proposition 6 (every balloon counterexample has a bridge).** If a
connected cubic loopless multigraph H contains a balloon u ‖ v with
common third neighbour w and stem s at w, then s is a bridge of H, and
the link edge of s is a bridge of T(H). Consequently every graph the
Balloon Lemma rules out is a *bridged* diamond-free claw-free cubic
graph; in particular G₁₈ has exactly one bridge and is not
2-edge-connected.

*Proof.* u and v already have degree 3 inside {u,v,w} (two parallel
instances plus one edge to w), so no further edge meets them, and s
cannot be a loop at w. Hence s is the only edge of H leaving
{u,v,w}, i.e. a bridge, and n(H) ≥ 4. Blowing vertices into triangles
neither creates nor destroys bridges among link edges (triangle edges
lie on triangles), so the link edge of s is a bridge of T(H). ∎

This matters for how Problem 4.1 should be read. Oum's structure
theorem (§7), the source of the "well-known fact" Kardoš quotes, is
stated for **2-edge-connected** claw-free cubic graphs, and much of the
cubic-graph literature carries a bridgeless hypothesis by default. By
Proposition 6 the refutation lives entirely in the bridged part of the
class; the 2-edge-connected case is untouched by it, and the census
below says that case looks true.

## 4. The census

All connected cubic loopless multigraphs H were generated by nauty's
`geng`+`multig` (counts match A002851 and A000421 exactly at every
order used — the generator cross-check), their truncations decided by
two engines sharing no code:

* **Engine A** (`strong6.c`): exhaustive DSATUR backtracking on the
  conflict graph with a greedy-clique color prefix; complete search, so
  its NOT6 verdicts are proofs by exhaustion;
* **Engine B** (`engine_b.py`): definition-level CNF + SAT (CaDiCaL /
  Glucose42), witnesses re-verified from the definition inside the
  engine.

Protocol: every 6-colorable instance ships a witness re-checked from
the definition by a third implementation (`verify_census.py`, which
also re-derives the graph from the raw quotient line, checks
connectivity, cubicity, claw- and diamond-freeness, and locates a
conflict 6-clique, certifying χ′ₛ = 6 exactly); every NOT6 verdict is
confirmed UNSAT by Engine B; every capped Engine-A instance is decided
by Engine B; every NOT6 instance gets a verified 7-coloring
(`chi7_pass.py`), so χ′ₛ = 7 is certified per instance with no reliance
on the literature. Negative controls: a corrupted witness and a
corrupted family line are rejected by the verifier; anchor values
C₅ = 5, C₆ = 3, C₇ = 4, K₃,₃ = 9, Petersen = 5, prism = 9 reproduced
(secondary published values).

| order of H | # quotients | χ′ₛ(T) = 6 | χ′ₛ(T) = 7 | balloon-free among =7 |
|---:|---:|---:|---:|---:|
| 2 | 1 | 0 | 0 (prism: χ′ₛ = 9) | — |
| 4 | 2 | 2 | 0 | |
| 6 | 6 | 5 | 1 | 0 |
| 8 | 20 | 16 | 4 | 0 |
| 10 | 91 | 72 | 19 | 0 |
| 12 | 509 | 407 | 102 | 0 |
| 14 | 3608 | 2926 | 682 | 0 |
| 16 | 31856 | 26359 | 5497 | 0 |

Every χ′ₛ = 7 instance contains a balloon; every balloon instance has
χ′ₛ = 7; the unique balloon-free non-6 quotient is the triple edge. A
cross-check added in the 2026-08-26 publish pass
(`bridge_census.py`) tabulates verdict against 2-edge-connectivity of
the quotient: **all 6,305 quotients with χ′ₛ(T(H)) = 7 are bridged**,
the sole bridgeless failure being the triple edge (prism, χ′ₛ = 9), and
all 26,867 bridgeless quotients of order ≤ 16 other than the triple
edge have χ′ₛ(T(H)) = 6 — as Proposition 6 predicts. So Problem 4.1
restricted to 2-edge-connected graphs is **verified, not refuted**, for
every quotient of order ≤ 16.
Totals: 36,093 quotients of order ≤ 16; 6,305 truncations with
χ′ₛ = 7, every one containing a balloon and carrying a verified
7-coloring; zero balloon-free failures besides the triple edge; zero
balloon-carrying successes.

**Order 18 (appended in-session, lighter protocol).** The 340,416
order-18 quotients split as 287,459 balloon-free + 52,957 balloon.
Every balloon-free one has a strongly 6-edge-colorable truncation:
Engine A decided 286,805 with witnesses re-verified from the
definition, and the 654 instances it capped were decided SAT by Engine
B (witnesses checked in-engine). The balloon side has χ′ₛ ≥ 7 by
Theorem 3 (proved — no computation needed), a 500-instance random
sample was independently confirmed UNSAT at 6 by Engine B (500/500),
and χ′ₛ = 7 exactly then follows from Lin–Lin's bound (§7);
unlike orders ≤ 16, no per-instance 7-colorings were computed here.
Conjecture C's open direction ("balloon-free ⇒ 6") thus stands
verified for all 317,246 balloon-free quotients of order ≤ 18 other
than the triple edge.

**Corollary (bridgeless form).** If Conjecture C holds, every
2-edge-connected diamond-free claw-free cubic graph other than the
prism is strongly 6-edge-colorable: by Proposition 6 a balloon forces a
bridge, so a bridgeless quotient is balloon-free. In other words the
bridgeless reading of Problem 4.1 would be **true**, and the refutation
below is exactly a bridge phenomenon.

**Conjecture C (characterization).** For a connected cubic loopless
multigraph H other than the triple edge:
χ′ₛ(T(H)) = 6 ⟺ H contains no balloon; otherwise χ′ₛ(T(H)) = 7.
(The forward implication "balloon ⇒ 7" is Theorem 3 plus Lin–Lin's
upper bound (§7); open is "balloon-free ⇒ 6".)

## 5. Truncations of simple cubic graphs (the intended reading)

For every connected **simple** cubic graph G on n ≤ 20 vertices —
1 + 2 + 5 + 19 + 85 + 509 + 4060 + 41301 + 510489 = 556,471 graphs —
the truncation T(G) (on up to 60 vertices) is strongly 6-edge-colorable,
with a definition-checked witness per instance (Engine A; the 570
instances Engine A capped were decided SAT by Engine B, witnesses
checked inside the engine). This extends the truncated-prism family of
Han–Cui (secondary: J. Appl. Math. Comput. 69 (2023) 2503–2508) to all
simple quotients of order ≤ 20 and is, to our knowledge, the first
systematic verification of the intended reading of Problem 4.1.

## 5b. Beyond diamond-free: wires, and the claw-free census

The interface calculus extends beyond truncations. In *any* cubic
graph, two edges conflict only when they are within distance one, so
for a bridge s = a·b the two sides interact only through
(c(s), pair of colors of the other two edges at a) and symmetrically at
b, with the junction rule "pairs disjoint" — the general form of
Lemma 2 (same one-paragraph proof). Three two-terminal pieces then act
as "wires" with machine-enumerated transfer relations
(`boundary.py`, `diamond_wire.py`):

| piece | relation between its two boundary states | count |
|---|---|---|
| **diamond** (K₄ − e inserted in an edge) | color preserved, pairs disjoint | 180 |
| **dumbbell** (doubled edge, two stems) | color changed, pair preserved | 180 |
| **balloon** (doubled edge, stems tied) | none — no valid internal state | 0 |

Composing the diamond's relation with the junction rule on both sides
gives exactly { (c,S_a) ~ (c,S_b) : S_a ≠ S_b } — strictly *weaker*
than the bare-edge junction rule S_a ∩ S_b = ∅. Hence inserting a
diamond into a bridge of a cubic graph never destroys strong
6-colorability (it relaxes the constraint), though it is not a
universal joint: equal pairs remain forbidden. (A first hand-derivation
claimed the full relation; the machine check refuted it — the case
S_a = S_b leaves one color where two are needed. Recorded per the
discipline of checking every closed form.)

Census of the whole claw-free class (diamonds allowed): connected
claw-free cubic graphs are rare — by order 4, 6, …, 16 there are
1 (K₄), 1 (prism), 1, 1, 3, 3, 5 of them. Their strong chromatic
indices, decided by the same double-engine protocol: everything is 6
except the prism (9) and: one graph on 10 vertices (χ′ₛ = 7: a diamond
plus two triangles — by this census the **unique smallest claw-free
cubic graph of strong chromatic index 7**, novelty not checked against
Lin–Lin's tight examples, whose list was not read), all three graphs on
14 vertices,
one of the five on 16, five of the eleven on 18, and five of the
fifteen on 20 (χ′ₛ = 7 each, verified 7-colorings; every UNSAT@6
confirmed by engine B). The by-order table of (all, χ′ₛ = 7):
(1,0), (1,–), (1,0), (1,1), (3,0), (3,3), (5,1), (11,5), (15,5) for
orders 4–20, the prism being the one graph counted "–" (χ′ₛ = 9).

## 6. Toward the converse: a sufficient condition

The dart model gives a candidate uniform construction on class-1 simple
quotients: fix a proper 3-edge-coloring φ of H, take colors
{(i, ε) : i ∈ {1,2,3}, ε ∈ {0,1}}, set c(e) = (φ(e), σ(e)) for a sign
σ: E → {0,1}, and t_u(e) = (φ(e), 1−σ(e)). Conditions (vertex) hold
automatically; condition (edge) holds iff for every edge uv and both
colors i ≠ φ(uv), the signs of the i-edges at u and v differ. For each
i this is a proper 2-coloring condition on H ∖ M_i (disjoint even
cycles) compatible with constancy on M_i — a linear system over GF(2).
When all three systems are solvable, T(H) is strongly 6-edge-colorable.
This covers some families directly but not all quotients (the general
converse remains open); we record it as the natural attack line.

## 7. Prior work and openness

**Citation status.** Every citation below was read in the original on
2026-08-26 during the local publish pass, replacing the search-snippet
attributions the (egress-blocked) research session had to rely on.
Where a statement is attributed through Kardoš's write-up rather than
read in the cited paper itself, this is said explicitly.

* **Problem 4.1** — F. Kardoš, §4 of *Open problems of the 33rd
  Workshop on Cycles and Colourings*, ed. A. Onderko, arXiv:2511.02892v1
  [math.CO], 4 Nov 2025 (workshop held Nový Smokovec, Slovakia,
  31 Aug – 5 Sep 2025). **Read in the original.** Verbatim: *“Is it true
  that every diamond-free claw-free cubic graph is strongly
  6-edge-colorable? In other words, is it true that χ′ₛ(T(G)) = 6 for
  every cubic graph G?”*, preceded by *“It is a well-known fact that
  diamond-free claw-free cubic graphs can be obtained from cubic graphs
  by the operation of truncation – replacing each vertex by a
  triangle.”* The two sentences are the two phrasings this note
  separates: the class-level phrasing is refuted here (Theorem 5), while
  the T(G) phrasing with G simple survives §5. The gap is exactly the
  “well-known fact”: by Lemma 0 the class is the truncations of cubic
  loopless **multigraphs** (plus K₄), a strictly larger family than the
  truncations of simple cubic graphs, and G₁₈ lives in the difference.
* **χ′ₛ ≤ 7 for claw-free subcubic ≠ triangular prism, tight** —
  Y. Lin, W. Lin, *The tight bound for the strong chromatic indices of
  claw-free subcubic graphs*, Graphs Combin. **39** (2023), no. 3, 58;
  arXiv:2207.10264. Abstract read in the original: bound 7, prism
  excepted, infinitely many tight examples, linear-time algorithm. That
  *all* their tight examples contain diamonds is Kardoš's
  characterization of them in the primary text above, not a statement
  read in Lin–Lin itself.
* **Truncated prisms are strongly 6-edge-colorable** — Z. Han, Q. Cui,
  *A note on strong edge-coloring of claw-free cubic graphs*, J. Appl.
  Math. Comput. **69** (2023), no. 3, 2503–2508. Attribution and
  bibliographic details from Kardoš's primary text; the paper itself was
  not read.
* **Earlier bound ≤ 8** — J. B. Lv, J. Li, X. Zhang, *On strong
  edge-coloring of claw-free subcubic graphs*, Graphs Combin. **38**
  (2022), no. 3, 63. Attribution from Kardoš's primary text.
* **Openness.** Searched again on 2026-08-26 with full access: no
  published resolution of Problem 4.1 and no diamond-free tight example
  found. Problem 4.1 is open as of that date to the best of a literature
  search; no exhaustive database sweep was performed.
* **Structure (Lemma 0)** — S. Oum, *Perfect matchings in claw-free
  cubic graphs*, Electron. J. Combin. **18** (2011), no. 1, #P62,
  Proposition 1. **Read in the original** (2026-08-26): *“A graph G is
  2-edge-connected claw-free cubic if and only if either (i) G is
  isomorphic to K₄, (ii) G is a ring of diamonds, or (iii) G can be
  built from a 2-edge-connected cubic multigraph H by replacing some
  edges of H with strings of diamonds and replacing each vertex of H
  with a triangle.”* Specialising (iii) to the diamond-free case gives
  Lemma 0 for 2-edge-connected G, and Oum's proof of that case is the
  same triangle-contraction argument used here (*“If G has no diamonds,
  then every vertex of G is in exactly one triangle and therefore V(G)
  can be partitioned into disjoint triangles. By contracting each
  triangle, we obtain a 2-edge-connected cubic multigraph H.”*). Lemma 0
  as stated here is the connected (bridges allowed) version plus
  uniqueness of H; that extension is what the counterexample needs, and
  it is not claimed as new beyond Oum. Oum remarks the proposition also
  follows from Chudnovsky–Seymour's quasi-line structure theorem.
  The packing-coloring literature on DFCF cubic graphs uses the same
  picture (e.g. arXiv:2607.25198, which cites Oum's Proposition 1).
* We found no prior appearance of the balloon obstruction or of any
  χ′ₛ = 7 diamond-free claw-free cubic graph, on the research session's
  snippet-level search and again on the 2026-08-26 full-access re-check.
  This is a literature-search claim, not a proof of novelty.

## 8. Open questions

1. Prove Conjecture C's open half: balloon-free (≠ triple edge) ⇒
   χ′ₛ(T(H)) = 6. The GF(2) construction of §6 and the transfer calculus
   of Lemma 2/Lemma 4 (dumbbells force "same spare pair, different stem
   colors") are the tools; a discharging or induction over the
   dumbbell-core decomposition looks plausible.
2. Kardoš's intended question (simple quotients) in full: §5 verifies it
   to order 20; is there a proof for 3-edge-colorable H (§6), for
   bipartite H, or in general?
3. The counting sequence of χ′ₛ = 7 quotients by order,
   1, 4, 19, 102, 682, … (= balloon-containing cubic multigraphs if
   Conjecture C holds), did not match any OEIS entry findable by search
   from this sandbox; worth submitting once checked against OEIS proper.
4. Among claw-free cubic graphs *with* diamonds, which need 7? The
   engines here decide any instance; a census over the whole claw-free
   class would complete the picture Lin–Lin's theorem frames.
