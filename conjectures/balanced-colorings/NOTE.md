# Balanced colourings of complete graphs and the Erdős–Gyárfás bound at r²+1

**Session 2026-08-27.** AI-assisted (Claude); see repository disclosure.
Every literature statement below is **(secondary)** — reconstructed from
search snippets and two mirrored databases under a blocked network — except
where marked as proved or computed here.

## §0. Problem and conventions

An edge r-colouring of K_N is **balanced** if every set of r+1 vertices
spans all r colours (equivalently: no (r+1)-clique misses a colour).
Erdős Problem #617 (Erdős–Gyárfás, Discrete Math. 200 (1999) 79–86
(secondary)): *for r ≥ 3, K_{r²+1} admits no balanced r-colouring.*
Known (secondary, problem page + Lean formalization): true for r = 3, 4
(ErGy); false for r = 2 (see §3.3); balanced r-colourings of K_{r²} exist
for some r and fail for infinitely many r.

Write T(r) for the largest N such that K_N admits a balanced r-colouring
(monotone: restricting a balanced colouring of K_N to any N−1 vertices
leaves it balanced, since every (r+1)-subset of the restriction is one of
K_N). The conjecture says T(r) ≤ r² for r ≥ 3.

For a colouring and a colour c, let G_c be the graph of c-edges and
H_c = K_N − G_c its complement. Balanced ⟺ every H_c is K_{r+1}-free.

## §1. Turán floor

**Lemma 1.** In a balanced r-colouring of K_N, every colour class G_c has
at least C(N,2) − ex(N; K_{r+1}) edges.

*Proof.* H_c is K_{r+1}-free, so |H_c| ≤ ex(N; K_{r+1}); |G_c| = C(N,2) −
|H_c|. ∎

For N = 26, r = 5: ex(26; K_6) = e(T_5(26)) = 270 (parts 6,5,5,5,5), so
each of the five classes has ≥ 55 of the 325 edges — total slack 50.

## §2. Codes ⇒ balanced colourings; the Singleton bound at r²

**Definition.** A colouring is **partition-structured** if every H_c is
r-partite, i.e. for every colour c the vertex set splits into ≤ r parts
each of which is a c-monochromatic clique (an H_c-independent set is
exactly a set all of whose internal edges have colour c).

**Lemma 2 (codes give balanced colourings).** Let C ⊆ A^r be a set of N
words over an alphabet A with |A| = r, with pairwise Hamming distance
≥ r−1 (equivalently: any two words agree in at most one coordinate). Then
K_N has a balanced, partition-structured r-colouring.

*Proof.* Identify the vertices with the words. For coordinate c, let Q_c
be the partition of the vertices by their c-th letter (≤ r parts). Two
words agree in ≤ 1 coordinate, so each pair of vertices is co-partitioned
in at most one Q_c; colour such a pair by that c, and colour never
co-partitioned pairs arbitrarily. Balanced: for any r+1 vertices and any
coordinate c, the r+1 words take ≤ r values at c, so two agree at c
(pigeonhole); that pair is co-partitioned in Q_c, hence coloured c.
Partition-structured: each part of Q_c is a c-clique by construction, so
H_c is r-partite via Q_c. ∎

**Lemma 3 (partition-structured colourings are codes).** If K_N has a
balanced r-colouring in which every H_c is r-partite, then there is a set
of N words in {1..r}^r with pairwise Hamming distance ≥ r−1.

*Proof.* Fix for each c a partition Q_c of the vertices into ≤ r
c-monochromatic cliques. Map each vertex to the word of its part indices
(q_1(v), …, q_r(v)). If two vertices agreed in two coordinates c ≠ c′,
their edge would lie inside a part of Q_c and a part of Q_{c′}, so it
would be coloured both c and c′ — impossible. Distinct vertices agree in
≤ 1 coordinate, so the words are distinct with distance ≥ r−1. ∎

**Theorem 4 (Singleton bound for the structured sector).** For every
r ≥ 2: (a) K_{r²+1} admits **no** partition-structured balanced
r-colouring. (b) If r is a prime power, K_{r²} admits one, so T(r) ≥ r²;
explicitly, AG(2,r) — colour each edge by the parallel class of the line
through its endpoints and merge two of the r+1 classes — is such a
colouring (equivalently, delete one coordinate of the extended
Reed–Solomon [r+1, 2, r]_r code).

*Proof.* (a) By Lemma 3 such a colouring gives N = r²+1 words of length r
over an r-letter alphabet with pairwise distance d ≥ r−1; the Singleton
bound gives N ≤ r^{r−d+1} ≤ r². (For self-containedness: project the words
onto two fixed coordinates; two words agreeing on both would have distance
≤ r−2, so the projection is injective and N ≤ r².) Contradiction.
(b) The evaluation code {(a·x + b)_{x∈F_r} : a, b ∈ F_r} has r² words and
pairwise agreement ≤ 1 (two distinct affine polynomials over a field agree
at ≤ 1 point); apply Lemma 2. The AG(2,r) merge description is the same
object: vertices = points of F_r², coordinate c = the line of direction c
through the point, for r−1 of the r+1 directions… direct verification of
the merge construction (pigeonhole over the r lines of each direction) is
in `construction.py`, machine-checked for r = 3, 4, 5 over every
(r+1)-subset. ∎

**Machine confirmations (CERTIFIED).** K_9 (r=3), K_16 (r=4), K_25 (r=5)
witnesses from Theorem 4(b) verified from the definition over all 126 /
4368 / 177,100 (r+1)-subsets (`construction.py`); the packing/code SAT
model (`packing_sat.py`) independently finds structured colourings at
N = r² and refutes them at N = r²+1 (see README table for instances and
certificates).

## §3. Consequences for K₂₆ and the shape of the open problem

**3.1.** By Theorem 4(a), any balanced 5-colouring of K₂₆ has a colour c
with χ(H_c) ≥ 6, where H_c is K₆-free with between 220 and 270 edges
(Lemma 1 applied to all five classes). So the r = 5 case of Erdős #617 is
exactly the question of whether a *non-partition-structured* witness
exists: a 5-tuple of K₆-free graphs partitioning E(K₂₆)'s complement
structure with at least one complement of chromatic number ≥ 6.
K₆-free graphs with χ ≥ 6 exist already on 8 vertices (C₅ ∨ K₃), so no
counting shortcut closes this sector; it is decided by the SAT instance.

**3.2.** The general conjecture, in this light, says: *for r ≥ 3 the
Singleton bound survives the removal of the structure hypothesis* — no
balanced r-colouring of K_{r²+1} exists even allowing complements of
chromatic number > r.

**3.3.** The r = 2 failure is exactly an exotic witness: the balanced
2-colouring of K₅ (= C₅ and its complement C₅) has H_c = C₅ with
χ(C₅) = 3 > 2 — not partition-structured; and indeed T(2) = 5 = r²+1
(K₆ has none: R(3,3) = 6, machine-exhausted in `construction.py`). So the
conjecture's content at r ≥ 3 is that the odd-cycle phenomenon that breaks
r = 2 has no higher-r analogue.

**Novelty caveat.** Lemmas 2–3 and Theorem 4 are elementary, and the
construction in 4(b) — or some equivalent of the whole code
correspondence — may well appear in [ErGy99] or in Füredi–Ramamurthi
(J. Graph Theory 2002), neither of which could be read from this sandbox;
their r = 3, 4 proofs must in any case handle the harder unstructured
sector. No claim of novelty is made for §§1–2 until those papers are
read. The computational results (§4) were found in no source reachable
today.

## §4. The r = 5 instance (this session's computation)

Model ↔ balanced colouring, exactly: variables x_{e,c} (e ∈ E(K₂₆),
c ∈ [5]), exactly-one colour per edge, and for each of the 230,230
6-subsets S and each colour c a clause ∨_{e⊆S} x_{e,c}: 1625 variables,
1,155,555 clauses (`encoder.py`; clause count = C(26,2)·(1+C(5,2)) +
C(26,6)·5). Controls: the encoder reproduces T(2) = 5 exactly (SAT at
K₅, UNSAT at K₆ matching the 2^15 exhaustion), finds balanced colourings
at K₉, K₁₆, K₂₅ (each re-verified from the definition by independent
code), accepts the AG(2,5) witness under assumptions, and reproduces the
Erdős–Gyárfás theorems r = 3, 4 as machine certificates (UNSAT at K₁₀,
K₁₇ with DRUP proofs checked by `tools/satcert/rup_check`).

(Results of the K₂₆ decision run: see README/WRITEUP — completed after
this section was drafted.)
