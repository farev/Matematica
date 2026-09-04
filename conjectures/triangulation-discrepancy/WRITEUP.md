# Session narrative — triangulation-discrepancy

## 2026-09-04 (session 1)

**How it was chosen.** The day's main target (the antidiagonal traffic anomaly,
`conjectures/antidiagonal-anomaly/`) was settled within the first hour, and the internal
secondary target (peaceable queens a(18)) needed only cores, not attention. The arXiv scout
had flagged Basti–Cremaschi's two-week-old note as a clean open statement with a computable
smallest case: their refined bound disc(T) ≤ n − 2⌈(n+2)/3⌉ is proved for n ≢ 5 (mod 6),
stated open for n ≡ 5 (mod 6), and checked only at n = 11. The scout's plan was a census
at n = 17 (129.7 million triangulations, "1–2 h on 4 cores"). Reading the five-page paper
showed something better: their proof fails in the open residue class at exactly one
class-size vector of the balanced 4-colouring, (3m+2, m+1, m+1, m+1), and that
configuration is rigid enough to attack directly.

**Tooling first.** plantri 5.5 was compiled and its triangulation counts checked against
OEIS A000109. A C checker (`disc.c`) computes disc(T) exactly by backtracking over
red/blue assignments with monochromatic-face pruning and a cardinality target; it
reproduced the paper's Table 2 for every order 4 ≤ n ≤ 12 on the first run (including the
2 + 16 discrepancy-2 graphs), and an independent Python brute force over all 2^{n−1}
masks — the paper's own method — agreed for n ≤ 11. At ~4 μs per graph the n = 17 census
turned out to cost 15 minutes on one core, not hours; it ran in the background in four
`res/mod` parts while the mathematics went on.

**The reduction.** The paper's argument for n = 3q+2 handles r = a+d = q+1 (3-colourable
case) and, for q even, derives a contradiction from s = b+c = q+1. For q odd the same
computation leaves exactly the vector (3m+2, m+1, m+1, m+1) — the big class as large as
the balanced four-colour theorem allows, the other three equal — and there every 2+2
merge gives discrepancy 2m+1, one step too many. Two observations broke the rigidity:

1. *A free vertex of V₁.* If some vertex v of the big class has a link missing one colour
   pair, colour that pair's classes blue, the third class red, V₁ red except v blue: the
   faces at v are safe precisely because the missing pair never sits on an edge of v's
   link. This gives 4m+2 / 2m+3. So a counterexample is "fully mixed", which already
   excludes degree 4 in V₁ (a 3-coloured 4-cycle has only two pairs).
2. *A free vertex of W.* If some vertex w outside V₁ lies on no face disjoint from V₁,
   move w alone to the other side of the 1+2 split of W. This forces every W-vertex onto
   a V₁-free face, which bounds the total degree excess of V₁ by 2m−1: at least 2m+3 of
   the 3m+2 big-class vertices have degree 3, at most m−1 have degree ≥ 5.

The "single flip" then does the rest when all big-class vertices have degree 3: recolour
one vertex u of V₂ red; the degree-3 neighbours of u are forced blue, the other degree-3
vertices forced red, and the count works out iff 2 ≤ occ(u) ≤ 2m+1, where occ(u) counts
the degree-3 neighbours of u. Averaging gives occ(u) ≥ 3 for some u; the upper bound
needed a separate argument (Lemma 6): a vertex with 2m+2 degree-3 neighbours has a link
that alternates between them and the vertices of the other two classes, so it lies on no
V₁-free face — contradicting observation 2. That closes the H = ∅ case (Theorem 3).

**Where the proof stalls.** With vertices of degree ≥ 5 in the big class, the single flip
can be "blocked": a high-degree vertex whose link has u next to an S-vertex (forcing it
blue) and an F–B edge elsewhere (forcing it red). Several hours went into this: a
formulation with an arbitrary flipped set X ⊆ V₂ (the "closed sets" under the blocking
relation form a lattice; whole Kempe components are closed and always fail by exactly
one, as they must, since they are just recolourings; proper sub-closed sets are what is
needed), Kempe-chain facts (every (i,j)-component within W is balanced, each (1,i)-graph
has a unique component with a surplus of colour 1), and the observation that every
V₂-vertex with ≥ 2 degree-3 neighbours must sit on a high-degree link next to a
V₄-vertex — and symmetrically. None of it produced the missing inequality, and the
honest statement is Theorem 2: a precise list of properties a counterexample must have.

**Turning the structure into computation.** The structure theorem is strong enough that
the next open order becomes finite in a practical sense: a counterexample on 23 vertices
must be a 2-connected plane graph on 12 vertices with 25–30 edges and faces of length 3
or 5–8, equitably 3-coloured, with 11 faces stellated and every vertex on an unstellated
triangle. plantri generates those 109.5 million plane graphs in about a minute;
`struct_enum.c` applies the filters, enumerates the equitable colourings and the choices
of empty faces, rebuilds T and computes its discrepancy. The program was validated at
n = 11 (it finds the stellated-octahedron family, 32 configurations, all discrepancy 1,
matching the paper's census) and at n = 17 (2,051 fully-mixed candidates, all
discrepancy 1, consistent with the full census). At n = 23 it ran in 277 seconds:
1.85 million of the 109.5 million graphs pass the face filter, 11,678 of those have an
equitable 3-colouring, 948,057 configurations survive the covering and fully-mixed
conditions, and all of them have discrepancy 1 — not one comes within four of the bound.
So the refined bound holds at n = 23, an order whose 60 billion triangulations no census
could visit, and the structured candidates are in fact the *easiest* triangulations, not
the hardest — which is itself a hint about where a proof should look.

**The count that closed h ≤ 2.** While the n = 23 enumeration ran a second time with a
new statistic (does every candidate admit a Lemma 7 flip? — it does, 0 exceptions at
n = 17 and n = 23), the question became *why*. The answer for one or two high-degree
vertices is a counting argument that had been sitting in plain view: if every vertex off
the high-degree links has at most one degree-3 neighbour, then at least |N| − h − 1
degree-3 vertices have all three neighbours on the links N and occupy triangular faces of
G[N]; Euler's formula on G[N], the fact that every N-vertex must also lie on an *empty*
triangle (Lemma 3 again), and a boundary-length bookkeeping give
σ ≤ 3h − 3 + (2/3)|N| for the total link length σ ≥ max(|N|, 5h) — impossible for
h ≤ 2. So a vertex off the links with two degree-3 neighbours exists, and it is a flip
nobody can block. That upgrades the n = 17 and n = 23 results from CERTIFIED to PROVED
(a counterexample at 6m+5 has at most m−1 high-degree vertices), leaves the computations
as independent confirmations, and moves the frontier to n = 29 with three high-degree
vertices. For h = 3 the same count allows three disjoint links of length 5 or 6, and for
large h the links may cover every vertex, so the general case needs the blocking
analysis proper.

**Probing the wall.** With h ≤ 2 closed, the first configuration the lemmas cannot touch
was written down explicitly: n = 35, three disjoint hexagonal links coloured 2,3,4,2,3,4
covering all 18 other vertices, which kills every single flip. Rather than theorise, a
SAT model (216 rainbow triples, exact-cover-style cardinality constraints, a
planarity-free formulation whose surviving solutions are automatically triangulations of
the pair of pants) produced such triangulations within seconds — and every one of them
has discrepancy 1. So the wall is a property of the flip family, not of the
triangulations: the eventual proof for h ≥ 3 needs a genuinely different colouring
construction, and the hexagon-pants family is the test case to design it on. Meanwhile
the n = 29 case (h = 3, three high-degree vertices) was attacked computationally through
a second parametrisation (`hstruct.c`: triangulations on 18 vertices with three
non-adjacent vertices of degree 5 or 6, from plantri's 1,000,148,231 triangulations),
validated against the first at n = 17 and n = 23.

**Slips and corrections.** The census driver's first version used `/usr/bin/env time`,
absent here, so its first run produced empty logs ("bad header") — caught within a minute
and rerun with shell timing. The chart of which plantri flags select quadrangulations
(`-q`) rather than "quiet" cost one confused minute. A stray invocation of the census
script inside the repository directory created junk log files, deleted before commit.
Two background processes left by a scouting agent (a SAT run and a subset-sum search)
were found competing for the cores and killed.

**Labels.** Theorems 1–3 and Lemmas 1–7 are PROVED (the balanced four-colour theorem is
used as stated in its arXiv abstract). The census (Theorem 4) and the n = 23 enumeration
(Theorem 5) are CERTIFIED: exact integer decisions, reproducible from the committed
programs, with the extremal triangulations committed as certificates. The general
residue-class statement remains open; nothing here is labelled beyond what was done.

**Runtime.** One core throughout, shared with the peaceable-queens run: n ≤ 16 census
2.3 min, n = 17 census 15 min (four parts), n = 23 enumeration 277 s. No seeds, no
floating point.
