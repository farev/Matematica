# Ordinary lines of 15 points: a SAT attack on the smallest open case of the Dirac–Motzkin conjecture

*Research note, 2026-09-05. Produced with substantial AI assistance (Claude); every proof
below was checked by hand, every computation ships code and a machine-readable ledger of
solver verdicts with checked proofs.*

## Abstract

For a set P of n points in the real projective plane, not all on a line, let t₂(P) be the
number of *ordinary lines* (lines containing exactly two points of P) and t₂(n) the minimum
over all such P. The Dirac–Motzkin conjecture asserts t₂(n) ≥ n/2 for n ≥ 14; Green and Tao
(2013) proved it for all n ≥ n₀ with n₀ unspecified and "of double exponential type", and
exact values are recorded only for n ≤ 14 and n = 16, 18, 22 (OEIS A003034). We attack the
smallest open case, n = 15, where 7 ≤ t₂(15) ≤ 9 was all that was known. Melchior's
inequality and pair counting show that a 15-point set with exactly 7 ordinary lines must
have exactly two 5-point lines and twenty-six 3-point lines and nothing else (Cor. 5.3). We
encode "rank-3 chirotope on 15 elements, collinear triples allowed, at most 7 two-element
lines" as a SAT instance whose axioms are only necessary conditions satisfied by every real
configuration and every rank-3 oriented matroid, and refute it with DRAT proofs checked by
drat-trim in the case where the two 5-point lines are **disjoint** (261 sub-cubes, all
UNSAT, Theorem 6.1), and in the star-free sub-case where they **meet** (411 arrays, all
UNSAT, Theorem 6.2). Parity arguments dispose of 83 of the remaining 130 sub-cases of the
meeting case. **The meeting case with 1 ≤ s ≤ 5 ordinary lines among the 16 cross pairs
(45 sub-cases after two more were closed, about 151 000 arrays) is not finished**, so t₂(15) ≥ 8 is *not* established
here; what is established is that any 15-point configuration with 7 ordinary lines, real
or pseudo, has its two 5-point lines meeting and has between 1 and 5 ordinary lines among
the pairs joining them. Everything is reproducible from the scripts in this directory.

## 1. Statement and background

Let P ⊂ RP² be a finite set of n points, not all collinear. A line spanned by P is *ordinary*
if it contains exactly two points of P; write t_k(P) for the number of lines containing
exactly k points of P and t₂(n) = min_P t₂(P). The Sylvester–Gallai theorem is t₂(n) ≥ 1;
Melchior's argument gives t₂(n) ≥ 3; Kelly–Moser (1958) proved t₂(n) ≥ 3n/7 and Csima–Sawyer
(1993) t₂(n) ≥ 6n/13 for n > 7 [both statements quoted from Green–Tao, arXiv:1208.4714,
Introduction; the original papers are behind paywalls and were not read — (secondary)].
Green and Tao proved:

> **Theorem (Green–Tao 2013, Thm 1.2 and 2.2 of arXiv:1208.4714).** There is n₀ such that
> for n ≥ n₀ every set of n points in RP², not all on a line, spans at least f(n) ordinary
> lines, where f(2m) = m, f(4m+1) = 3m, f(4m−1) = 3m−3; equality holds only for the
> Böröczky examples.

They add (loc. cit., p. 3): "Kelly and Moser observe that a triangle together with the
midpoints of its sides and its centroid has n = 7 and just 3 ordinary lines. Crowe and
McKee provide a more complicated configuration with n = 13 and 6 ordinary lines. It is
possible that Theorem 1.2 remains true for all n with the exception of these two examples
(or equivalently, one could take n₀ as low as 14)."

**Known exact values.** OEIS A003034 (revision #27, 30 May 2026) lists t₂(n) for n = 3..14
as 3, 3, 4, 3, 3, 4, 6, 5, 6, 6, 6, 7 and quotes the Pach–Sharir table continuing
"?, 8, ?, 9, ?, ?, ?, 11" for n = 15..22.

**The case n = 15.** Csima–Sawyer gives t₂(15) ≥ ⌈90/13⌉ = 7 (Kelly–Moser also gives
⌈45/7⌉ = 7). Green–Tao's Proposition 2.1(iii) (X₄ₘ minus a point at infinity, m = 4) is a
15-point set with 3·4 − 3 = 9 ordinary lines. Hence 7 ≤ t₂(15) ≤ 9, and the sharp-threshold
formula predicts f(15) = 9 if n₀ ≤ 15. No smaller upper bound and no better lower bound
appear in the literature we could reach (A003034; Green–Tao; arXiv API sweeps for
"ordinary lines" 2020–2026; Lenchner–Sengupta arXiv:2608.24656).

## 2. Two elementary consequences of the literature (for the record)

**Proposition 2.1 (folklore, PROVED from published theorems).** t₂(20) = 10 and t₂(24) = 12.

*Proof.* Csima–Sawyer: t₂(n) ≥ 6n/13, so t₂(20) ≥ ⌈120/13⌉ = 10 and t₂(24) ≥ ⌈144/13⌉ = 12.
Green–Tao Prop. 2.1(i): X₂ₘ has 2m points and exactly m ordinary lines, so t₂(20) ≤ 10 and
t₂(24) ≤ 12. ∎

The same two theorems give t₂(16) = 8, t₂(18) = 9, t₂(22) = 11 (the values the Pach–Sharir
table does list), so the "?" recorded at n = 20 in A003034's comment is a transcription
gap, not an open case. n = 26 is the first even case they leave open (⌈156/13⌉ = 12 < 13).
Both facts rest on the Csima–Sawyer statement as quoted by Green–Tao (secondary).

## 3. The combinatorial abstraction

Fix homogeneous coordinates p₁, …, pₙ ∈ R³ ∖ {0} for the points and define
χ(i, j, k) = sign det(p_i, p_j, p_k) ∈ {−1, 0, +1}. Then:

* **(B1) alternating:** χ(σ(i), σ(j), σ(k)) = sign(σ) χ(i, j, k) for every permutation σ,
  and χ(i, j, k) = 0 whenever two indices coincide.
* **(S) simple:** for every pair i ≠ j some k has χ(i, j, k) ≠ 0 (the points are distinct
  and not all collinear).
* **(GP) three-term Grassmann–Plücker relations:** for all a, b, c, d, e,
  det(a,b,c)·det(a,d,e) − det(a,b,d)·det(a,c,e) + det(a,b,e)·det(a,c,d) = 0
  (a polynomial identity, checked on 2000 random integer 5-tuples in
  `chiro_sat.py::numeric_gp_selfcheck`). Consequently the three numbers
  χ(a,b,c)χ(a,d,e), −χ(a,b,d)χ(a,c,e), χ(a,b,e)χ(a,c,d) are either all zero or contain both
  a +1 and a −1: three reals summing to zero cannot all be nonzero of one sign, and if two
  vanish so does the third.

Collinearity is the zero set: i, j, k are collinear iff χ(i,j,k) = 0, and the line through
i and j is {i, j} ∪ {k : χ(i,j,k) = 0}. Ordinary lines are the pairs {i, j} with
χ(i, j, k) ≠ 0 for every k.

**Lemma 3.1 (soundness).** If some set of n points, not all collinear, spans at most m
ordinary lines, then the CNF Φ(n, m) described in §4 is satisfiable. The same holds for
every simple rank-3 oriented matroid on n elements with at most m two-element rank-2 flats,
hence (by the topological representation theorem) for every arrangement of n pseudolines
with at most m ordinary crossing points — (secondary): Björner–Las Vergnas–Sturmfels–White–
Ziegler, *Oriented Matroids*, the chirotope axioms of §3.5–3.6 and Thm 5.2.1, not re-read.

*Proof.* Assign Z_{ijk} = [χ(i,j,k) = 0], P_{ijk} = [χ(i,j,k) = +1] for i < j < k; every clause
of Φ(n, m) is one of (B1), (S), (GP), the definition of the auxiliary variables, or the
cardinality constraint, all of which hold for χ by the above. For oriented matroids, (GP)
is the three-term Grassmann–Plücker condition that every chirotope satisfies. ∎

The contrapositive is what we use: **Φ(n, m) unsatisfiable ⟹ t₂(n) > m**, for lines and for
pseudolines alike. Nothing in the argument needs the converse (that every model of Φ is a
chirotope), so no completeness theorem for the axiom system is invoked; a satisfying model
would only be a *candidate* pseudo-configuration, to be checked by `verify_chirotope.py`
(general axiom (B2)) and then for realizability.

## 4. The encoding Φ(n, m)

Variables Z_t, P_t for each of the C(n,3) triples t = {i<j<k}; χ(a,b,c) for an arbitrary
ordering is read off by sorting and multiplying P by the permutation sign. Clauses:

* (S) for each pair i<j: ⋁_k ¬Z_{ijk}.
* (T) transitivity, redundant but useful: within every 4-set, if two of its four triples are
  collinear then so are the other two (12 ternary clauses per 4-set). This is implied by (GP)
  but shortens propagation.
* (GP) for each 5-set and each apex a in it: six auxiliary variables pos_i, neg_i (i = 1,2,3)
  defined by 8 clauses each to be exactly "term i is +1" / "term i is −1", and the six
  clauses pos_i → ⋁_{j≠i} neg_j, neg_i → ⋁_{j≠i} pos_j, which say precisely "all zero or both
  signs present".
* (O) for each pair: O_{ij} ∨ ⋁_k Z_{ijk}, so an ordinary pair forces O_{ij}; then
  Σ O_{ij} ≤ m by a sequential counter (Sinz). Only the direction "ordinary ⟹ counted" is
  encoded; an over-counted O only strengthens the constraint, so unsatisfiability remains
  sound. Where a sub-case imposes t₂ = 7 exactly (§5), O_{ij} is first made exact by the
  clauses O_{ij} → ¬Z_{ijk}.
* (L) cube clauses, §5: prescribed lines of size ≥ 4 forced collinear and closed, all other
  lines forced to have at most 3 points.

Sizes at n = 15: 455 triples, 15 015 GP relations, 91 791 variables and about 655 500
clauses per cube (`ordlines_sat.py`).

## 5. The case split

**Lemma 5.1 (pair counting).** Σ_{k≥2} C(k,2) t_k(P) = C(n,2). *Proof.* Every pair of points
lies on exactly one spanned line. ∎

**Lemma 5.2 (Melchior 1940).** t₂(P) ≥ 3 + Σ_{k≥4} (k − 3) t_k(P) for every finite
non-collinear P ⊂ RP², n = |P| ≥ 3.

*Proof (classical; written out because the case split depends on it).* Dualise: the points
of P become an arrangement A of n distinct lines in RP², not all through one point, and a
line of P containing exactly k points becomes a vertex of A at which exactly k lines meet.
A induces a cell decomposition of RP² whose vertices are the intersection points
(V = Σ_k t_k), whose edges are the open segments into which the vertices cut the lines
(a line carrying v vertices is a circle cut into v arcs, so E = Σ_lines v_ℓ = Σ_k k·t_k,
each vertex of multiplicity k being counted on k lines), and whose faces are open discs
(this uses that not all lines are concurrent). Euler's formula for RP² gives V − E + F = 1.
Every face has at least three sides: two projective lines meet in exactly one point, so a
face with two sides would have to be bounded by two lines meeting twice, and a face with
one side is impossible; each edge borders two faces, so 3F ≤ 2E. Hence
1 = V − E + F ≤ V − E/3 = Σ_k (1 − k/3) t_k, i.e. 3 ≤ Σ_k (3 − k) t_k = t₂ − Σ_{k≥4}(k−3)t_k. ∎

(Green–Tao, eq. (3.5), record the equality version N₂ = 3 + Σ(k−3)N_k + Σ(s−3)M_s in the
same dual setting.) For pseudoline arrangements the same Euler argument applies because a
pseudoline arrangement is by definition a cell decomposition of RP² by simple closed curves
pairwise crossing exactly once (Bokowski–Pokora, arXiv:1607.05864, abstract: "Melchior's
inequality also holds for arrangements of pseudolines" — (secondary): abstract read, proof
not).

**Corollary 5.3 (line-type distributions at n = 15).** If P has 15 points and t₂(P) ≤ 8,
then (t_k)_{k≥3} is one of the 14 vectors computed by `distributions.py` from Lemmas 5.1–5.2
alone. In particular:

* t₂ = 7 forces t₅ = 2, t₃ = 26 and no other line of size ≥ 4;
* t₂ = 8 allows six shapes: {5}, {5,4}, {5,4,4}, {5,4,4,4}, {6,5}, {8} (multisets of sizes
  ≥ 4), with t₃ = 29, 27, 25, 23, 24, 23 respectively;
* t₂ ≤ 6 allows eight shapes (all excluded by Kelly–Moser and Csima–Sawyer; not machine-
  checked here).

*Proof.* Enumerate (t_k)_{k≥4} with Σ(k−3)t_k ≤ t₂ − 3 and solve Lemma 5.1 for t₃, keeping
integer solutions. E.g. for t₂ = 7: 105 − 7 = 98 ≡ 2 (mod 3) while C(k,2) ≡ 0 (mod 3) for
k ≡ 0, 1 (mod 3) and ≡ 1 for k = 5, 8, …; the budget 4 leaves only t₅ = 2. ∎

**Lemma 5.4 (cubes).** Two placements of the lines of size ≥ 4 that are isomorphic as
partial linear spaces (each pair of lines meeting in at most one point) give
equisatisfiable cube instances; hence it suffices to run one representative per
isomorphism class. `cubes.py` canonicalises a placement by the multiset of point-incidence
vectors minimised over permutations of the lines, which is a complete invariant for
labelled-line/unlabelled-point structures. This yields 2 cubes at t₂ = 7 — the two 5-point
lines are disjoint (**cube B**, L₁ = {0..4}, L₂ = {5..9}) or meet in a point q (**cube A**,
L₁ = {0,1,2,3,4}, L₂ = {4,5,6,7,8}) — and 41 cubes at t₂ = 8.

**Lemma 5.5 (sub-cubes for the two-5-line cubes).** Let L₁, L₂ be the two 5-point lines of a
t₂ = 7 configuration, R = L₁∖L₂, C = L₂∖L₁, F the remaining points (|F| = 5 in cube B, 6 in
cube A). For a ∈ R, b ∈ C the line ab contains no third point of L₁ ∪ L₂ and at most one
point of F, so
φ(a, b) := the point of F on line ab, or ∗ if ab is ordinary,
is a well-defined array in which every f ∈ F occurs at most once per row and per column
(two occurrences in a row would put f, a, b, b′ on one line, forcing a ∈ L₂). The number s
of ∗ entries is at most t₂ = 7. The relabellings fixing L₁ and L₂ setwise act on φ by row
permutations, column permutations and permutations of F; hence every configuration is
isomorphic to one whose ∗-pattern is the chosen representative of its class under row ×
column permutations (`star_classes`: 260 classes for the 5×5 array of cube B, 131 for the
4×4 array of cube A), and whose F-labels are in order of first occurrence in row-major
reading (value precedence). For the ∗-free disjoint case φ is a Latin square of order 5,
and we may take one of the two isotopy-class representatives (`latin_square_classes`
recomputes the classical count 2). Therefore, if the instances for every ∗-class (with
value-precedence clauses) and for the two Latin squares are unsatisfiable, so is the whole
cube. Each sub-cube adds only unit clauses and precedence clauses, all consequences of the
labelling convention, so soundness (Lemma 3.1) is untouched. ∎

**Lemma 5.6 (type vectors).** Keep the notation of Lemma 5.5, let M = |R||C| − s be the
number of mixed 3-lines (a, b, f). Every other 3-line has one of the types RFF (a, f, f′),
CFF (b, f, f′), FFF (f, f′, f″), and — in cube A, with q = L₁ ∩ L₂ — qFF (q, f, f′). Writing
A₃, B₃, C₃, Q₃ for their numbers and counting each kind of pair once:

*cube B (|F| = 5):* 26 = M + A₃ + B₃ + C₃, ord_RF = 25 − M − 2A₃, ord_CF = 25 − M − 2B₃,
ord_FF = 10 − A₃ − B₃ − 3C₃, and t₂ = s + ord_RF + ord_CF + ord_FF;

*cube A (|F| = 6):* 26 = M + A₃ + B₃ + Q₃ + C₃, ord_RF = 24 − M − 2A₃, ord_CF = 24 − M − 2B₃,
ord_FF = 15 − A₃ − B₃ − Q₃ − 3C₃, ord_qF = 6 − 2Q₃, and t₂ = s + ord_qF + ord_RF + ord_CF + ord_FF.

In both cases t₂ = 7 is then an identity (it reduces to 105 − 20 − 3·26 = 7), and all
"ord" quantities must be non-negative integers. Consequences (`typecubes.type_vectors`):

* cube B: s = 7 is impossible — A₃ + B₃ + C₃ = 8 forces ord_RF = 7 − 2A₃ and
  ord_CF = 7 − 2B₃ to be odd, hence ≥ 1 each, while they must sum with ord_FF ≥ 0 to
  t₂ − s = 0. So 130 of the 260 ∗-classes are void by arithmetic (they were nevertheless
  run, §6).
* cube A: s ≥ 6 is impossible (s = 6 forces Q₃ = 3 and ord_RF = ord_CF = 0, hence
  A₃ = B₃ = 7 and C₃ = −1; s = 7 forces 2A₃ = 15). So 83 of the 131 ∗-classes are void.
* every point lies on an even number of ordinary lines: for a point p, Σ over the lines
  through p of (|line| − 1) = 14, 3-lines contribute 2 and 5-lines 4.

Since every configuration in a cube has exactly one type vector, imposing the counts as
exact cardinality constraints (with O_{ij} made exact) is a sound refinement; it was
implemented (`typecubes.py`) and found not to speed up cube A (§7). ∎

**Lemma 5.7 (fillings).** Within a ∗-class, the fillings of the non-∗ cells by free points
(each at most once per row and column) up to Aut(S) × relabelling of F are enumerated by
`fillcubes.fillings` with canonical form "minimum over Aut(S) of the row-major word
relabelled by first occurrence". Every configuration in the ∗-class is isomorphic to one
whose array is a listed representative, so "all fillings UNSAT" implies "∗-class UNSAT". ∎

*Positive control (implementation check).* `poscontrol.py` constructs an explicit rational
configuration with two disjoint 5-point lines (t₂ = 43, t₃ = 14), relabels it into the
canonical form of Lemma 5.5, and solves the resulting sub-cube with m = 43: SAT in 0.3 s,
the model passes `verify_chirotope.py`, and the configuration's own chirotope violates none
of the 23 460 primary-variable clauses of that sub-cube. The n = 9 positive-control model of
§8 likewise passes the general chirotope axiom (B2) over all 9⁶ tuple pairs.

## 6. Results

All solver runs: Kissat 4.0.4 with `--no-binary` DRAT logging, proofs checked by drat-trim
(backward mode), on the 4-core / 15 GB session machine; solve and verification times are
single-core seconds summed over the jobs of each run; every proof was deleted after
verification (the ledgers record proof sizes and the SHA-256 of each CNF, which
`subcubes.py` / `fillcubes.py` regenerate deterministically).

**Theorem 6.1 (CERTIFIED).** No set of 15 points in RP², not all collinear, spans exactly
7 ordinary lines with its two 5-point lines disjoint. The same holds for rank-3 oriented
matroids (pseudoline arrangements) with the citations of Lemma 3.1 and Lemma 5.2.

*Certificate.* Cube B, all 261 sub-cubes of Lemma 5.5 (2 Latin squares + 259 ∗-classes with
s ≥ 1), every one UNSAT with a drat-trim-verified DRAT proof (`certs/ledger_B_m7.jsonl`):

| s (∗ entries) | sub-cubes | solve s | max solve s | verify s | proofs GB |
|---|---|---|---|---|---|
| 0 (Latin squares) | 2 | 3 | 2 | 4 | 0.06 |
| 1 | 1 | 63 | 63 | 24 | 0.11 |
| 2 | 3 | 118 | 72 | 56 | 0.23 |
| 3 | 6 | 169 | 156 | 155 | 0.33 |
| 4 | 16 | 888 | 540 | 837 | 1.04 |
| 5 | 34 | 882 | 245 | 858 | 1.36 |
| 6 | 69 | 140 | 4 | 234 | 1.43 |
| 7 (void by Lemma 5.6) | 130 | 209 | 4 | 312 | 1.71 |
| **total** | **261** | **2 472** | 540 | **2 480** | **6.3** |

Wall time about 55 minutes on two cores. Every sub-cube instance has 91 791 primary and
auxiliary variables before the precedence clauses and 655 5xx clauses. ∎

**Theorem 6.2 (CERTIFIED).** No set of 15 points (nor rank-3 oriented matroid) spans exactly
7 ordinary lines with its two 5-point lines meeting in a point q and *no* ordinary line
among the 16 pairs (a, b), a ∈ L₁∖{q}, b ∈ L₂∖{q}.

*Certificate.* Cube A, ∗-class 0 (s = 0), all 411 fillings of Lemma 5.7 (|Aut(S)| = 576), every
one UNSAT with a verified proof (`certs/ledger_A_m7_class0_fill.jsonl`): solve 1 212 s in
total (median 1.9 s, maximum 14.5 s), verification 1 384 s, proofs 13.1 GB in total (largest
59 MB); 45 minutes on one core. ∎

**Proposition 6.3 (PROVED + CERTIFIED).** In cube A the number s of ordinary lines among the
16 cross pairs satisfies 1 ≤ s ≤ 5: s = 0 by Theorem 6.2, s ≥ 6 by Lemma 5.6. The 83
∗-classes with s ≥ 6 were also run as sub-cubes as a machine check of the parity argument:
all 83 UNSAT with verified proofs, 134 s solving (maximum 4.0 s), 258 s checking, 1.45 GB of
proofs (`certs/ledger_A_void.jsonl`). ∎

**What remains open (the meeting case, 1 ≤ s ≤ 5).** 47 ∗-classes before the two closures
below, with 70 to 16 631 fillings each (3 268 for the single s = 1 class), 151 449 fillings
in total (`fillcubes.py … --count`).
Sub-cubes of this case do not finish: the s = 1 sub-cube ran 20 min on Kissat and 10 min on
CaDiCaL without a verdict, the s = 2 class 15 min; with the type-vector refinement the
first instance of the s = 1 class took 14 s but the second ran 10 min without verdict;
fixing the four cells of one free point leaves a 300 s timeout. Fully fixed arrays are
refuted quickly (median 0.04–0.3 s in an incremental CaDiCaL session, but with a heavy
tail up to 20 s concentrated on arrays whose six free points carry 3, 3, 3, 2, 2, 2 mixed
lines), which puts the whole case at roughly 25 CPU-hours by the measurements of §7 —
outside this session's budget. The two smallest open classes (indices 11 and 22 in
`star_classes(4,4,7)`, |Aut(S)| = 144, 70 fillings each) were closed in fill mode: 140
arrays, all UNSAT with verified proofs (`certs/ledger_A_m7_class11_fill.jsonl`,
`…class22_fill.jsonl`; 212 s solving, 358 s checking). That leaves **45 open ∗-classes with
151 309 fillings**.

**Corollary 6.4.** If a set of 15 points in RP² spans only 7 ordinary lines, then its line-type
distribution is t₅ = 2, t₃ = 26, t₂ = 7, its two 5-point lines meet, between one and five of
the sixteen pairs joining them span ordinary lines, and every point lies on an even number
of ordinary lines. The Dirac–Motzkin bound t₂(15) ≥ 8 is equivalent to the unsatisfiability
of the 45 remaining ∗-classes of cube A.

## 7. Method notes and negative results

* *Plain encoding.* Without a case split the refutation side is hopeless already at n = 9
  (CaDiCaL > 6 min, Kissat killed), although the SAT side and n ≤ 8 are instant; the
  Melchior/counting split (one cube with a 5-point line) refutes n = 9, m = 5 in 25 ms.
* *Monolithic n = 15 cubes:* 30 min on Kissat without verdict (both cubes).
* *Double-lex symmetry breaking* (`lexcubes.py`; rows and columns of φ lexicographically
  ordered plus value precedence — sound because sorting rows, sorting columns and canonical
  relabelling each weakly decrease the row-major word, so iterating them from any solution
  reaches a fixpoint satisfying all three) was slower than the ∗-class sub-cubes: no verdict
  in 4 min on the s = 1, 2, 3 instances of cube B that the sub-cubes settle in about a minute.
* *Type vectors and parity* (Lemma 5.6): exact counts and per-point XOR constraints made
  the fixed-array refutations propagate faster at the median (0.04 s vs 0.31 s) but not in
  the mean (0.64 s vs 0.87 s), and made the unfixed sub-cubes of cube A no easier.
* *Incremental fill mode* (one CaDiCaL instance per ∗-class, arrays as assumption sets):
  300 random arrays of the s = 1 class of cube A cost 338 s (269 s with parity); the slow
  arrays are exactly those with mixed-line counts (3, 3, 3, 2, 2, 2) (mean 1.64 s, 35 % of
  the sample) while arrays with a free point on four mixed lines take milliseconds.
  Splitting a slow array further by type vector multiplies its cost by 3–5.

## 8. Calibration against known values

The cube method reproduces the refutation side of the known ladder (`certify.py`;
`certs/calibration_n9_12.log`): n = 9, m = 5: one cube, UNSAT in 0.0 s; n = 10, m = 4 and
n = 11, m = 5: no admissible distribution at all, so t₂ ≥ 5 resp. 6 follows from Lemmas
5.1–5.2 alone; n = 12, m = 5: one cube, UNSAT in 18.5 s. Positive controls: n = 9, m = 6 SAT
(in 4 of 6 cubes, 0.1 s), n = 10, m = 5 SAT (0.1 s), n = 11, m = 6 SAT (0.4 s). The n = 13,
m = 5 cube (one 5-point line, t₃ = 21) is a single-line structure with no array to split on; Kissat hit the 3 600 s cap on it with
a 3.9 GB proof and no verdict (`solve_s: 3600.0, result: TIMEOUT` in the scratch ledger),
and the n = 14, m = 6 control (three cubes) was started and stopped at the end of the
session. The refutation side of the calibration therefore stands for n ≤ 12; n = 13, 14
are recorded as unfinished, not as failures — they are exactly the single-5-line structure
that also blocks the t₂ = 8 cube {5} at n = 15 (§9.2).

## 9. Open questions

1. Finish cube A (45 ∗-classes). Estimated 25 CPU-hours in incremental fill mode; a
   cleverer split is wanted — the slow arrays have no free point on four mixed lines, i.e.
   no perspectivity between L₁ and L₂ defined on all of R, which suggests exploiting the
   projective structure (in the real case, sending q to infinity makes the perspectivities
   affine maps x ↦ αx + β between two 4-point sets, and two free points on four mixed lines
   each must differ by the reflection of R) either as a hand proof of the real case or as
   extra necessary conditions.
2. Then t₂(15) ∈ {8, 9}: the 41 cubes of Corollary 5.3 at t₂ = 8, of which the single-line
   cube {5} (t₃ = 29) and the two-line cubes {5,4}, {6,5} are the ones needing new splits;
   {5,4,4} and {5,4,4,4} (35 cubes) fix three or four lines and may be monolithically easy.
3. Whether any of the abstract instances is *satisfiable*: a model would be a pseudo-
   configuration beating Dirac–Motzkin at n = 15 and would answer the Handbook question on
   whether the minimum number of ordinary points separates lines from pseudolines.
4. Submit the A003034 corrections of §2 (a(20) = 10, a(24) = 12 follow from Csima–Sawyer and
   Böröczky).

## References

* B. Green, T. Tao, On sets defining few ordinary lines, *Discrete Comput. Geom.* 50 (2013),
  arXiv:1208.4714 — read (PDF text extracted); quotations above are verbatim.
* OEIS A003034, revision #27 (30 May 2026) — read via the OEIS text interface.
* J. Csima, E. T. Sawyer, There exist 6n/13 ordinary points, *Discrete Comput. Geom.* 9
  (1993) 187–202 — (secondary; statement via Green–Tao and A003034).
* L. M. Kelly, W. O. J. Moser, On the number of ordinary lines determined by n points,
  *Canad. J. Math.* 10 (1958) 210–219 — (secondary; first page only via Cambridge Core).
* E. Melchior, Über Vielseite der projektiven Ebene, *Deutsche Math.* 5 (1940) 461–475 —
  (secondary; via Green–Tao §3).
* J. Bokowski, P. Pokora, On the Sylvester–Gallai and the orchard problem for pseudoline
  arrangements, *Period. Math. Hungar.* 77 (2018) 164–174, arXiv:1607.05864 — abstract read.
* A. Björner, M. Las Vergnas, B. Sturmfels, N. White, G. Ziegler, *Oriented Matroids*, 2nd ed.,
  Cambridge 1999 — (secondary; not consulted today).
* A. Biere et al., Kissat 4.0.4; M. Heule, drat-trim; A. Ignatiev et al., PySAT (CaDiCaL 1.5.3
  bindings) — solvers and checker used.
