# Symmetry obstructions for 5-colorings of PG(7,2)

*Research note, 2026-09-01 session. AI-assisted (Claude); all proofs
checked by hand, all computational claims ship reproducible code and,
where stated, machine-checkable certificates.*

## Abstract

Bishnoi, Cames van Batenburg and Ravi (arXiv:2512.01760) determine the
chromatic number χ₂(n) of PG(n−1,2) — the least number of colors on the
nonzero vectors of F₂ⁿ with no monochromatic line {x, y, x⊕y},
equivalently the least number of sum-free sets partitioning F₂ⁿ∖{0} —
for all n ≤ 7, and ask (their Problem 1) whether χ₂(8) is 5 or 6. A
positive 5 would give the multicolor Ramsey bound R(3;5) ≥ 257. We do
not decide χ₂(8), but we constrain any witness severely. (1) A proper
5-coloring of PG(7,2) cannot be invariant under any collineation of
order 3, 7, 31 or 127: for prime p = 2^d − 1 the element has an
irreducible invariant d-space whose 2^d − 1 = p nonzero points form a
single orbit containing lines (Lemma B — valid for every n, k and every
Mersenne prime order). (2) The only other odd prime orders available in
GL(8,2) are 5 and 17; we set up exact orbit-contracted SAT instances
for every conjugacy class of such subgroups (one class for 17, two for
5) and certify: no order-17-invariant witness (UNSAT, 131-line DRUP
proof, independently checked), and no Frobenius-invariant witness. The
order-5 instances are harder; both fell after color-symmetry breaking
(a two-line WLOG lemma): no order-5-invariant witness of either class,
with both proofs independently machine-verified. Hence — modulo only
that hand lemma — **every proper 5-coloring of PG(7,2) has a 2-group
stabilizer**. (3) In contrast,
PG(6,2) admits an order-5-invariant proper 5-coloring (explicit witness,
verified). (4) Every witness restricts, on each of the 255 hyperplanes,
to a proper 5-coloring of PG(6,2) using all five colors (Lemma A);
across 1,000 sampled 5-colorings of PG(6,2) — all structurally distinct
— not one extends back over a hyperplane split, and per-class spectral
capacity exceeds the requirement by a factor ≈ 2, locating the
obstruction at the packing level. The evidence is consistent with
χ₂(8) = 6.

## 1. Problem and background

Throughout, points of PG(n−1,2) are the nonzero vectors of F₂ⁿ and the
line through distinct points x, y is {x, y, x⊕y}; PG(7,2) has 255
points and 10,795 = (2⁸−1)(2⁸−2)/6 lines (count cross-checked against
OEIS A006095). A color class avoids monochromatic lines iff it is
sum-free. From [BCvBR]: χ₂(n) = 2, 3, 3, 4, 5, 5 for n = 2..7,
χ₂(n) ≤ ⌊2n/3⌋ + 1 always, and χ₂(8) ∈ {5, 6} with "determine whether
χ₂(8) = 5" posed as Problem 1. Their §6.1 records the connection
χ₂(n) ≤ k ⟹ R(3;k) > 2ⁿ and the known range 162 ≤ R(3;5) ≤ 307
(their citations; not independently re-verified here — (secondary)).
We verified the quoted statements against the arXiv v3 text directly.
The paper contains no computational work on n = 8.

The full collineation group of PG(7,2) is GL(8,2) (q = 2: no field
automorphisms, projectivities = linear maps), of order
2²⁸ · 3⁵ · 5² · 7² · 17 · 31 · 127
(= ∏ᵢ₌₀⁷ (2⁸ − 2ⁱ); factorization recomputed for this note). The
*stabilizer* of a coloring χ is {φ ∈ GL(8,2) : χ∘φ = χ up to nothing —
i.e. every class is φ-invariant as a set}. We say χ is φ-invariant when
each color class is a union of ⟨φ⟩-orbits.

## 2. Lemma A (hyperplane restriction)

**Lemma A.** Let χ be a proper 5-coloring of PG(7,2) and H ≤ F₂⁸ any
hyperplane (dim 7). Then every color class meets H∖{0}, and χ
restricted to H∖{0} is a proper 5-coloring of PG(6,2) using all five
colors. Consequently no color class is contained in the affine part
F₂⁸ ∖ H.

*Proof.* Restrictions of sum-free sets are sum-free, so χ|_{H∖0} is a
proper coloring of PG(6,2) with at most 5 colors. If some class missed
H∖{0}, at most 4 classes would cover H∖{0}, giving a proper 4-coloring
of PG(6,2) — contradicting χ₂(7) = 5 [BCvBR]. A class contained in
F₂⁸ ∖ H is exactly a class missing H∖{0}. ∎

(The same argument gives the general statement: in a proper k-coloring
of PG(n−1,2) with k < χ₂(n−1) + 1, every class meets every hyperplane.)
Two consequences worth recording: the natural ansatz "one class = a
maximum sum-free set" is impossible (maximum sum-free sets in F₂⁸ are
affine hyperplanes of size 128); and any witness yields 255 proper
5-colorings of PG(6,2), one per hyperplane — the basis of the extension
experiments of §6.

## 3. Lemma B (Mersenne obstruction)

**Lemma B.** Let p = 2^d − 1 be prime with d ≥ 2, and let φ ∈ GL(n,2)
have order p (any n ≥ d). Then *no* proper coloring of PG(n−1,2), with
any number of colors, is φ-invariant.

*Proof.* Over F₂, x^p − 1 = (x − 1) f₁ ⋯ f_m with each fᵢ irreducible
of degree exactly d = ord_p(2) (standard: the irreducible factors of
the p-th cyclotomic polynomial over F₂ have degree ord_p(2), and
ord_p(2) = d when p = 2^d − 1). Since φ ≠ I and φ^p = I, some fᵢ
divides the minimal polynomial of φ, so V := ker fᵢ(φ) ≠ 0 contains a
φ-invariant subspace V₀ of dimension d on which the minimal polynomial
of φ|_{V₀} is fᵢ. As fᵢ ≠ x − 1, φ|_{V₀} has no nonzero fixed vector,
so every ⟨φ⟩-orbit on V₀∖{0} has size p. But |V₀∖{0}| = 2^d − 1 = p:
V₀∖{0} is a *single orbit*. A φ-invariant coloring is constant on
orbits, so V₀∖{0} is monochromatic; since d ≥ 2, V₀ contains a 2-dim
subspace W, and W∖{0} is a line — monochromatic. ∎

**Corollary.** In GL(8,2) the odd primes dividing the group order are
3, 5, 7, 17, 31, 127. Of these, 3 = 2²−1, 7 = 2³−1, 31 = 2⁵−1,
127 = 2⁷−1 are Mersenne, so by Lemma B (and Cauchy's theorem applied to
any subgroup of odd order divisible by them) an invariant proper
coloring of PG(7,2) can only tolerate odd symmetry of order divisible
by 5 or 17 alone. ∎

## 4. The certified exclusions

**Orbit contraction.** For G ≤ GL(8,2) with point-orbits O₁,…,O_m, the
G-invariant proper k-colorings correspond bijectively to maps
c : {O₁,…,O_m} → [k] such that no line is monochromatic under the
induced point coloring. For a line ℓ with orbit multiset (a) all in one
orbit: no c works (the instance is *dead*, certificate: the line and
the orbit); (b) two orbits {A,A,B}: constraint c(A) ≠ c(B); (c) three
orbits: not-all-equal. We encode cells × colors with exactly-one
clauses and solve exactly. A satisfying assignment is lifted to the 255
points and re-verified from the definition; unsatisfiability is
certified by a DRUP proof checked with `tools/satcert/rup_check`
(an independent from-the-definition checker; it accepts pure RUP + 
deletion steps only).

**Order 17.** ord₁₇(2) = 8, so order-17 elements act with one
irreducible 8-dim block; 17 divides |GL(8,2)| to the first power, so
all order-17 subgroups are Sylow and conjugate; conjugating a subgroup
transports invariant colorings, so one representative decides all. We
take multiplication by an order-17 element of F₂₅₆* (15 orbit cells of
size 17). Result: **UNSAT**; Glucose42 DRUP proof, 131 lines,
`rup_check`: `s VERIFIED` (`certs/ord17.{cnf,drup}`).

**Frobenius.** The field Frobenius x ↦ x² of F₂₅₆ (order 8, a
2-element — not needed for the odd-order theorem but a natural
symmetry) has 35 orbit cells. Result: **UNSAT**; 5,227-line DRUP,
verified (`certs/frob.{cnf,drup}`).

**Order 5.** ord₅(2) = 4 and Φ₅ = x⁴+x³+x²+x+1 is irreducible over F₂,
so an order-5 element of GL(8,2) is similar to C ⊕ C or C ⊕ I₄ with
C the companion matrix of Φ₅ — exactly two conjugacy classes, and each
nontrivial power of an element stays in its class (Cᵏ has minimal
polynomial Φ₅ for k = 1..4), so these are also the two conjugacy
classes of order-5 *subgroups*. Realization: F₂⁸ = F₁₆ ⊕ F₁₆ with
ζ₅ ∈ F₁₆* of order 5: [C,C] = (a,b) ↦ (ζ₅a, ζ₅b) (51 cells),
[C,I] = (a,b) ↦ (ζ₅a, b) (63 cells). These are the two instances
`ord5_CC.cnf` (255 vars), `ord5_CI.cnf` (315 vars). They are much
harder than the order-17 cell: Cadical exhausts a 2·10⁶-conflict budget
and unbroken kissat runs went > 2 h without terminating. Both fell after
adding *color-precedence symmetry breaking*, sound by:

**Color-WLOG lemma.** Every proper cell-coloring has a color-permuted
representative in which cell 0 has color 0 and, whenever a cell i has
color γ ≥ 1, some cell j < i has color γ−1. (Relabel colors by order of
first appearance along the cell sequence: first appearances are then
increasing and the used colors are an initial segment.) Hence adding the
corresponding clauses (`*_cbrk.cnf`; 205/253 extra clauses) preserves
satisfiability, and UNSAT of the broken instance gives UNSAT of the
original. ∎

**Results.** `ord5_CC_cbrk.cnf`: **UNSAT** (kissat 4.0.4, ~40 min,
812 MB binary DRAT proof, sha256 3140a05a…; **verified by drat-trim in
2,174 s** — 12.5M lemmas, 5,211 RAT lemmas in core — the proof is too
large to commit, so the repo ships the instance, the hash, and the
regeneration command `kissat ord5_CC_cbrk.cnf proof`).
`ord5_CI_cbrk.cnf`: **UNSAT** twice independently — Glucose42 in 5.5 s
with a 307,292-line *pure DRUP* proof **verified by the repo's own
`rup_check`** (shipped as `certs/ord5_CI_cbrk.drup.gz`), and kissat in
~7 min with a binary DRAT proof (1,221 RAT lemmas) verified by
drat-trim in 6.2 s. The unbroken [C,I] instance also finished:
**UNSAT** directly, with no symmetry breaking (kissat, ~90 min, 6.7 GB
proof — solver verdict only, hash recorded in `data/ord5_status.md`),
independently confirming that leg without the color lemma. The unbroken
[C,C] instance was still running at close; neither is needed for
Theorem 1. So: **no order-5-invariant proper 5-coloring of PG(7,2)
exists, in either conjugacy class** (CERTIFIED modulo the color-WLOG
lemma; the [C,I] leg carries a rup_check-verified DRUP certificate and
the [C,C] leg a drat-trim-verified DRAT proof).

**Theorem 1.** The stabilizer in GL(8,2) of any proper 5-coloring of
PG(7,2) is a 2-group. (Proviso: the order-5 legs rest on the UNSATs of
the color-broken instances, sound by the Color-WLOG lemma above; both
proofs are independently machine-verified — [C,I] by the repo's own
rup_check, [C,C] by drat-trim. Every other leg is a hand proof or a
rup_check-verified DRUP certificate.)

*Proof.* If an odd prime p divides the stabilizer order, Cauchy gives
φ of order p ∈ {3,5,7,17,31,127} (Corollary §3). Mersenne p:
impossible by Lemma B. p = 17: impossible by the certified UNSAT and
Sylow conjugacy. p = 5: φ lies in class [C,C] or [C,I]; conjugation
transports the coloring; the corresponding instance is unsatisfiable. ∎

**Additional certified sweeps** (solver-decided; DRUP kept only for the
two instances above): every cyclic multiplicative subgroup of F₂₅₆* of
order 3, 15, 51, 85, 255 is dead — its cosets contain full lines; the
order-3 case is the pleasant identity that F₄*-cosets {x, ωx, ω²x}
*are* lines, since x + ωx = (1+ω)x = ω²x. The order-17-with-Frobenius
and order-5-with-Frobenius quotients are UNSAT; twenty block-diagonal
Singer/twisted/swap families die because a transitive block action
makes a punctured invariant subspace a single cell (`matrix_ansatz.py`
output). Pure Frobenius powers σ², σ⁴ give weakly contracted instances
(66/135 cells) left undecided — they are 2-elements, outside Theorem 1.

## 5. The n = 7 contrast

The analogue of the order-5 question one level down has the opposite
answer: PG(6,2) admits an order-5-invariant proper 5-coloring. With
F₂⁷ = F₁₆ ⊕ F₂³ and φ = (a,b) ↦ (ζ₅a, b) (the unique order-5 class in
GL(7,2); 31 cells), the contracted instance is satisfiable; the lifted
coloring is proper and φ-invariant, class sizes [21,21,25,27,33]
(`data/witness_n7_ord5.txt`, re-verified from the definition by
`verify_witness.py`). The invariant family is large: ≥ 10⁵ cell-level
solutions before the enumeration cap. Whatever obstructs 5-colorings at
n = 8 — if indeed χ₂(8) = 6 — is not the mere presence of 5-fold
symmetry, and does not propagate down to n = 7.

Lemma B, by contrast, bites at every level: PG(6,2) tolerates no
order-3/7/31-invariant coloring either.

## 6. Extension experiments (NUMERICAL)

Fix the split F₂⁸ = H ⊕ ⟨e₈⟩. By Lemma A a witness restricts on H to a
proper 5-coloring W of PG(6,2), and conversely a witness is exactly
W together with a coloring of the 128 "affine" points (v,1) such that
for every h ∈ H∖{0} and every affine pair {(v,1), (v⊕h,1)} the pair
does not receive color W(h) jointly — i.e. color class c on the affine
side must be independent in the Cayley graph Cay(F₂⁷, W⁻¹(c)). Each
candidate W thus yields a 640-variable extension SAT instance.

- Sampling W by randomized CDCL (kissat --sat, varying seeds, composed
  with uniform random GL(7,2) relabelings; every sample re-verified):
  **1,000 samples, 999 pairwise distinct** under a
  class-size-and-line-type fingerprint, and **0 extend** (every
  extension instance UNSAT per Cadical). The order-5-invariant witness
  of §5 does not extend either. Caveats: solver sampling is not
  uniform; the non-extensions are solver verdicts, with a 50-witness
  subsample DRUP-certified end-to-end (`ext_certify.py`, 50/50 verified).
- Capacity is not the obstruction: the Cayley graphs' eigenvalues are
  exact integers (Walsh–Hadamard over ℤ), and the Hoffman ratio bound
  gives per-witness capacity sums Σ_c α-bound ≈ 265–274 against the 128
  needed; randomized greedy alone already packs ≈ 151–170 across
  classes separately. The failure is the simultaneous partition — a
  packing-level rigidity.
- Local-search signature: plain min-conflicts on the full n = 8
  instance plateaus (best 35 monochromatic lines over 73 annealing
  restarts; min-conflicts stalls at 1 even at n = 7 where witnesses
  exist); with breakout clause-weighting, n = 7 witnesses arrive in
  ~5·10³ flips, while n = 8 produced none in ≈ 5×10⁹ weighted flips across two
  independently seeded engines (order-of-magnitude estimate from the
  measured flip rate ≈ 0.2–0.7 M/s; the engines were retired early to
  free cores and their exact counters were not flushed). Consistent with — far from
  proof of — χ₂(8) = 6.

## 7. Controls

The published table is reproduced end-to-end by the same pipeline:
χ₂(n) = 2,3,3,4,5,5 for n = 2..7 — SAT witnesses at (n,k) =
(2,2),(3,3),(4,3),(5,4),(6,5),(7,5) all re-verified from the
definition; UNSAT decisions at (3,2),(4,2),(5,3) solver-decided in
milliseconds. The lower bounds χ₂(6), χ₂(7) > 4 are theory
(R(3;4) ≤ 62 < 2⁶, as in [BCvBR] — their citation, (secondary)); our
(6,4) SAT probe did not terminate in 2 minutes, consistent with the
known hardness of such instances (cf. the balanced-colorings session,
2026-08-27). Line counts match (2ⁿ−1)(2ⁿ−2)/6 for n = 2..8.

## 8. Open questions

1. Finish the order-5 legs (or refute: a SAT model would *be* an
   invariant χ₂(8) = 5 witness and decide Problem 1 positively).
2. Decide the involution classes and σ², σ⁴: "trivial stabilizer only"
   would be the natural endpoint of the symmetry program.
3. Exhaust extensions over the order-5-symmetric n = 7 family (it is
   quotient-enumerable, unlike the full witness space).
4. The full χ₂(8) decision: symmetry-broken UNSAT needs verified
   breaking (VeriPB-style) over GL(8,2); the SAT side is now known to
   need either a non-algebraic construction or a much deeper search.
5. If χ₂(8) = 6: does the Mersenne obstruction plus a quantitative
   packing argument give a human-readable proof?

## Disclosure

Sessions in this repository are run with substantial AI assistance
(Claude). AI systems are not authors. Primary sources read today:
arXiv:2512.01760v3 (abstract page and HTML full text, quoted statements
verified). Secondary (not independently checked): the R(3;4) ≤ 62 and
162 ≤ R(3;5) ≤ 307 bounds as cited therein; the Hoffman bound is used
as textbook material.
