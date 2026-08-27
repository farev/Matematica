# Balanced colourings of complete graphs: the Erdős–Gyárfás problem at K₂₆

**Session 2026-08-27.** AI-assisted (Claude); see repository disclosure.
Every literature statement below is **(secondary)** — reconstructed from
search snippets and mirrored databases under a blocked network — except
what is proved or computed here.

## §0. Problem and conventions

An edge r-colouring of K_N is **balanced** if every set of r+1 vertices
spans all r colours (no (r+1)-clique misses a colour). Erdős Problem #617
(Erdős–Gyárfás, *Split and balanced colorings of complete graphs*,
Discrete Math. 200 (1999) 79–86 (secondary)): *for r ≥ 3, K_{r²+1} admits
no balanced r-colouring.* Known (secondary; problem page + Lean
formalization, both checked 2026-08-27): proved for r = 3, 4 (ErGy); false
for r = 2; balanced r-colourings of K_{r²} exist for some r and fail for
infinitely many r. **r = 5 — is K₂₆ balanced-5-colourable? — is the first
open case**, and this session's target.

T(r) := the largest N with a balanced r-colouring of K_N. Monotone:
restricting a balanced colouring to N−1 vertices leaves it balanced (every
(r+1)-subset of the restriction is an (r+1)-subset of K_N). The conjecture
says T(r) ≤ r² for r ≥ 3; T(2) = 5 (K₅ = C₅ ⊕ C₅ works, R(3,3) = 6 kills
K₆ — both machine-exhausted here as controls).

For a colouring, G_c = the graph of c-edges, H_c = its complement in K_N.
Balanced ⟺ α(G_c) ≤ r for every c ⟺ every H_c is K_{r+1}-free.

## §1. Two elementary counting facts

**Lemma 1 (Turán floor).** In a balanced r-colouring of K_N,
|G_c| ≥ C(N,2) − ex(N; K_{r+1}) for every colour c.
*Proof.* H_c is K_{r+1}-free. ∎
At N = 26, r = 5: ex(26; K₆) = e(T₅(26)) = 270, so every |G_c| ≥ 55.

**Fact A (no monochromatic K_{r+1}, and its chromatic consequence).**
In a balanced r-colouring (r ≥ 2), every monochromatic clique has ≤ r
vertices: an all-c (r+1)-set would miss the other r−1 colours. Hence the
independence number of every H_c is ≤ r, and at N = r²+1,
χ(H_c) ≥ N/α(H_c) ≥ (r²+1)/r > r, i.e. **every H_c has chromatic number
≥ r+1** while being K_{r+1}-free.

**Corollary A1 (structured sector is empty).** At N = r²+1, no colour
class complement H_c is r-partite. In particular, for every r ≥ 2 there is
no balanced r-colouring of K_{r²+1} in which some H_c is r-partite — an
r-partition of V into H_c-independent parts would be a partition into ≤ r
monochromatic-c cliques of size ≤ r each, covering ≤ r² < r²+1 vertices. ∎

Fact A also explains r = 2: the K₅ witness has H_c = C₅ with
χ(C₅) = 3 = r+1 — the conjecture at r ≥ 3 asserts that this odd-cycle
escape has no higher-r analogue.

## §2. Codes give balanced colourings; the construction at r²

**Lemma 2 (codes ⇒ balanced colourings).** Let C be a set of N words of
length r over an r-letter alphabet with pairwise Hamming distance ≥ r−1
(equivalently, any two words agree in ≤ 1 coordinate). Then K_N has a
balanced r-colouring: identify vertices with words; for coordinate c let
Q_c partition the vertices by their c-th letter (≤ r parts); each pair of
vertices is co-partitioned in at most one Q_c — colour it by that
coordinate, and colour never-co-partitioned pairs arbitrarily. Any r+1
vertices take ≤ r values at coordinate c, so two agree (pigeonhole) and
that edge has colour c: all colours appear. ∎

**Theorem 3 (T(r) ≥ r² for prime powers).** For a prime power r, the
evaluation code {(ax+b)_{x∈F_r} : a,b ∈ F_r} ([r,2,r−1]_r Reed–Solomon)
has r² words with pairwise agreement ≤ 1 (distinct affine polynomials
agree at ≤ 1 point), so K_{r²} has a balanced r-colouring. Equivalently:
colour each edge of K on the point set of AG(2,r) by the parallel class
of the line through its endpoints and merge two of the r+1 classes —
every (r+1)-set contains two points on a common line of *every* parallel
class (r+1 points, r lines). Machine-verified here from the definition
for r = 3, 4, 5 over all 126 / 4,368 / 177,100 (r+1)-subsets
(`construction.py`; the K₂₅ witness is committed). ∎

**Remark (converse and Singleton).** If every H_c is r-partite, fixing a
partition of V into ≤ r c-cliques per colour and mapping each vertex to
its r-tuple of part indices gives N words with pairwise agreement ≤ 1 (an
edge co-partitioned twice would need two colours), so partition-structured
balanced colourings of K_N are exactly the code colourings of Lemma 2, and
the Singleton bound caps them at N ≤ r² — a second proof of Corollary A1,
and at N = r² the equivalence "structured witness ⟺ OA(r², r, r, 2) ⟺
r−2 MOLS(r)" connects the K_{r²} cases of the ErGy problem to the MOLS
existence problem (all (secondary) as regards what ErGy knew; for r = 6,
Tarry's theorem denies even 2 MOLS(6), consistent with their remark that
K_{r²} fails for infinitely many r).

## §3. What a K₂₆ witness must look like

By Fact A and Lemma 1, in any balanced 5-colouring of K₂₆ every colour
class G_c has ≥ 55 of the 325 edges, ω(G_c) ≤ 5, α(G_c) ≤ 5, and every
complement H_c is a K₆-free graph with χ(H_c) ≥ 6 and 220–270 edges. Such
graphs exist in isolation (C₅ ∨ K₃ is K₆-free with χ = 6 on 8 vertices),
so no per-class argument closes the problem; the content is the joint
edge-partition. Each G_c (and each H_c) is a Ramsey-type graph: no K₆ and
no I₆.

## §4. The extremal programme: E*(N, s) and the counting barrier

Define **E*(N, s)** = maximum edges of a graph on N vertices with no K_s
and no independent set of size s. **Notation/novelty flag:** this is
E(s, s, N) in the standard notation of Radziszowski's *Small Ramsey
Numbers* survey (DS1; latest revision 2026-04-24 (secondary)), where
minimal/maximal Ramsey-graph edge counts e(s,t,n)/E(s,t,n) are studied
quantities; whether E(4,4,10), E(5,5,17) or E(6,6,26) are already
tabulated there could not be checked from this sandbox (every mirror of
DS1 is egress-blocked) — treat the values below as possibly known until
DS1 is read. In a balanced r-colouring of K_{r²+1}
(s = r+1, N = r²+1), every H_c is such a graph, so
C(N,2) = Σ_c |G_c| ≥ r·(C(N,2) − E*(N, r+1)), i.e.

    existence at K_{r²+1}  ⇒  E*(r²+1, r+1) ≥ (r−1)/r · C(r²+1, 2).

Thresholds: r=3: E*(10,4) ≥ 30; r=4: E*(17,5) ≥ 102; r=5: E*(26,6) ≥ 260.

Computed here (SAT, witnesses re-verified from the definition by
independent code; UNSAT by CaDiCaL):

| quantity | value | status |
|---|---|---|
| E*(5,3) | = 5 (C₅; classical) | anchor: at r = 2 the threshold 5 is met with equality and realized by the unique witness (both classes C₅) |
| E*(10,4) | **= 31** | CERTIFIED (SAT witness at 31; UNSAT at 32 in 4.6 s) |
| E*(17,5) | ≥ 104 | CERTIFIED lower bound (≤ 108 = ex(17;K₅) trivially) |
| E*(26,6) | ≥ **265** | CERTIFIED lower bound (≤ 269: a 270-edge K₆-free graph is T₅(26), whose 6-part is an I₆) |
| max circulant on Z₂₆, no K₆/I₆ | 221 edges (S = {1,2,3,4,6,7,8,9,13}) | CERTIFIED (exhaustive over all 2¹³ connection sets) |

So the **counting barrier is sharp but never decides**: the per-class
bound misses the proved r = 3 case by exactly one edge (31 vs 30),
misses r = 4 (≥ 104 vs 102), and at r = 5 clears the threshold by ≥ 5
(265 vs 260). Two once-hoped kills died the same day, in order:

**Proposition 4 (rigidity — refuted as stated).** *If* E*(26,6) were
exactly 260, every colour class of a K₂₆ witness would have exactly 65
edges with every complement extremal (Σ|G_c| = 325 = 5·(325−260) forces
equality throughout). The machine refuted the premise within the hour:
E*(26,6) ≥ 261, then ≥ 265 (witnesses committed, definition-verified).
What survives: |G_c| ∈ [325 − E*(26,6), 105] for every class, i.e.
classes of 56–60 edges minimum once E* is pinned — still far above the
naive Turán floor 55, by the α-constraint that disqualifies the Turán
graph itself. The r = 2 anchor shows the rigidity scenario is not
vacuous: there it holds and produces the counterexample.

## §5. Exclusion results at K₂₆ (all this session)

**Lemma 5 (the affine family does not extend).** Colour K₂₅ on the points
of AG(2,5) by five of its six parallel classes, the 50 pairs of the sixth
class free (every choice is balanced — the pigeonhole uses only the five
kept classes). No choice of the 50 free colours and of 25 edge colours at
a new vertex makes K₂₆ balanced: the SAT instance (375 vars, 16,450
clauses; only 6-sets through the new vertex constrain) is UNSAT, with a
DRUP proof checked by the repository's independent verifier
(`certs/extend_code_unsat.drup`, 1,160 lines). The same pipeline at q = 2
(K₄ family → K₅) finds the 2 known C₅-type extensions — positive control. ∎

**Lemma 6 (profile arithmetic for invariant colourings).** In a
group-invariant balanced 5-colouring of K₂₆ by a regular action, each
colour class is a union of Cayley edge-classes; with a rotation classes
(26 edges) and b involution classes (13 edges) per colour, Lemma 1 forces
2a + b ≥ 5 per colour, and Σ_c (2a_c + b_c) = 25 forces **equality: every
colour class has exactly 65 edges**. For Z₂₆ (twelve full difference
classes + one half class) the equation 2a+b = 5 with b ∈ {0,1} per colour
and Σb = 1 is unsolvable — **no Z₂₆-circulant witness** — and for D₁₃
(6 rotation classes + 13 reflection matchings) the admissible profiles
are (a,b) ∈ {(2,1),(1,3),(0,5)}. ∎

**Theorem 7 (no dihedral witness).** No D₁₃-invariant balanced
5-colouring of K₂₆ exists: of the 195 + 1,716 + 1,287 = 3,198 candidate
colour classes admitted by Lemma 6, **not one** has independence number
≤ 5 (exhaustive computation, `dihedral.py`, with positive and negative
controls on the α-checker). A fortiori no exact cover exists. ∎

**Remark.** Any 2-transitive symmetry is impossible trivially (a
2-transitive group has one orbital, so the colouring would be
monochromatic). Contrast with r = 2, where the unique witness at
T(2) = 5 *is* a circulant (C₅): the vertex-regular escape that produces
the r = 2 counterexample provably has no analogue at r = 5.

## §6. Computational hardness of the direct question (observation)

The natural CNF for "K_N has a balanced r-colouring" (exactly-one colour
per edge + one coverage clause per ((r+1)-set, colour)) is already
practically unsolvable for CDCL at K₁₀, r = 3: 135 variables, 810
clauses, yet CaDiCaL 1.9.5, Glucose 4.2 and kissat 4.0.4 all exceed
minutes–hours unaided, and a cutting-planes PB solver (RoundingSat,
without LP) exceeds 120 s on the equivalent OPB model. The refutations
are pigeonhole-like counting arguments, exponentially hard for
resolution. With BreakID 3 symmetry-breaking predicates (S_N × S_r), the
same K₁₀ instance is UNSAT in 3.1 s — reproducing the Erdős–Gyárfás
r = 3 theorem by machine (certification caveat: the SBPs are trusted, not
DRUP-derived from the base formula). The K₁₇ (r = 4) and K₂₆ (r = 5)
instances, symmetry-broken and strengthened with Lemma-1 cardinality
totalizers, are running as of this note's writing; see WRITEUP for
outcomes. This hardness profile is evidence that #617's open cases have
not fallen to casual computation, and that certified progress requires
either verified symmetry breaking (VeriPB-style) or the structural
reductions of §§4–5.

## §7. Open threads after this session

1. Decide E*(26,6) = 260? (UNSAT at 261 ⇒ Proposition 4's rigidity ⇒
   attack via the extremal catalogue.)
2. The K₂₆ decision itself (SAT runs; then cube-and-conquer on the
   symmetry-broken + cardinality-strengthened formula).
3. Read [ErGy99] and Füredi–Ramamurthi (JGT 2002) from an unblocked
   machine: what exactly they prove about K_{r²}/K_{r²+1}, whether the
   code correspondence appears, and whether E*-type bounds are their
   method for r = 3, 4. Every (secondary) mark above must be resolved
   before any preprint.
4. If E*(26,6) > 260: quantify the slack and redo the rigidity analysis
   with classes in [325−E*, 105].
