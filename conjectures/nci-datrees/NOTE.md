# The minimal counterexample to the Non-Cancelling-Intersections conjecture has more than 15 elements

*Research note, Matematica log, 2026-08-28. AI-assisted (Claude); see the
repository's disclosure policy. All claims carry the repository's
PROVED / CERTIFIED / NUMERICAL labels.*

**Abstract.** The Non-Cancelling-Intersections (NCI) conjecture of Amarilli,
Monet and Suciu [1] states, in its lattice formulation, that every finite
lattice admits a *winning dot-algebra tree*: a tree expression built from the
principal down-sets of the elements of nonzero Möbius value, using disjoint
union and guarded set difference, whose value is the whole lattice minus its
top. Wilhelm refuted the conjecture nine days ago for left-linear trees [2]
and yesterday in full [3]; both refutations are probabilistic, produce no
explicit counterexample, and pose as their first open problem a lower bound
on the size of the smallest counterexample. The smallest counterexample
size certified by [3] is p³+2p² + 2 for a prime p ≥ 10⁵, about 1.0001·10¹⁵.
We give the first lower bound: **every lattice with at most 15 elements
admits a winning dot-algebra tree** — in fact a winning *left-linear* one
(CERTIFIED: exhaustive computation over all 171,432,955 lattices with 3 to
15 elements, streamed from `nauty-genposetg` with generation counts matching
OEIS A000112 and A006966 at every size, dual independent implementations,
and machine-verified explicit trees for controls). Hence the minimal
counterexample of [3] has at least 16 elements, the minimal *left-linear*
counterexample of [2] has at least 16 elements, and — via the equivalences
proved in [1, §4–5] and restated in [3, Remark 3.4] — any counterexample
*set family* to the original conjecture has an intersection lattice with at
least 16 elements. As a further consequence, at most 15 elements no lattice
separates left-linear from general dot-algebra trees; the separation proved
to exist by [2]+[3] happens strictly above this range.

## 1. Background

Amarilli, Monet and Suciu [1] conjectured (NCI conjecture, their Conjecture
3.4, formulation I): *for every intersection lattice L, the union 1̂ can be
expressed from the intersections with nonzero Möbius value using disjoint
union and subset complement* — and proved that every finite lattice is
isomorphic to an intersection lattice ([1], Remark 2.3), so the conjecture
is equivalently about all finite lattices. Their motivation comes from
database provenance (safe query plans); the conjecture also generalizes the
classical fact that inclusion–exclusion identities can sometimes be realized
"without cancellation".

Wilhelm's two August 2026 papers refute the conjecture:

- [2] (arXiv:2608.19414, 2026-08-19) shows that a winning **left-linear**
  da-tree (every right child a leaf — equivalently, a *toggle sequence*)
  does not always exist. The proof is a first-moment argument through an
  arithmetic Nullstellensatz; its own §8 computes the explicit upper bound
  10^(10^2215) on the size of some counterexample it produces, and its §9
  Open Problem 1 asks for "constructing an explicit counterexample, or
  establishing a lower bound on the size of any counterexample". It states
  plainly: "Determining the size of the smallest lattice on which the
  toggle game cannot be won remains open."
- [3] (arXiv:2608.27416, 2026-08-27) removes the left-linear restriction:
  for every prime p ≥ 10⁵ there is a marking m of the affine plane F_p² such
  that the lattice P_{p,m}, of size p³ + 2p² + 2, admits no winning da-tree
  at all (Theorem 8.1). With p = 100003 this certifies a counterexample of
  size ≈ 1.00011·10¹⁵ — for both the general and the left-linear question.
  Its §9 Open Problem 1: "What is the smallest lattice on which no winning
  da-tree exists?"

No lower bound on either minimal counterexample was recorded anywhere before
today, beyond what is implied by [1]'s own verification (see §7).

## 2. Definitions

We use [3, Definition 3.1] verbatim. Let P be a finite lattice with top ⊤.
The Möbius function here is µ(⊤) = 1 and µ(v) = −Σ_{u>v} µ(u) (this is
µ(v,⊤) in standard notation). For v ≠ ⊤ let S_v := ↓v ⊆ P∖{⊤} be the
principal down-set. A **da-tree** is a finite rooted binary tree whose
leaves are labelled ∅ or by vertices v ≠ ⊤ with µ(v) ≠ 0, and whose internal
nodes are labelled + or −. States: X_∅ = ∅, X_v = S_v; a +-node requires its
children's states disjoint and takes their union; a −-node requires its
right child's state contained in its left child's and takes the difference.
The tree is **winning** if the root state is P∖{⊤}, and **left-linear** if
every right child of an internal node is a leaf.

## 3. Reductions (PROVED)

**Lemma 1 (closure form of winnability).** For a finite lattice P, the set
of states of roots of da-trees for P is exactly the closure C(P) of
{∅} ∪ {S_v : v ≠ ⊤, µ(v) ≠ 0} under the two partial operations
(A,B) ↦ A ∪ B when A ∩ B = ∅ and (A,B) ↦ A ∖ B when B ⊆ A. In particular P
is winning iff P∖{⊤} ∈ C(P).

*Proof.* Any state buildable by a da-tree is in the closure, by induction on
the tree. Conversely each closure element is witnessed by a tree: leaves are
trees; if A, B have trees T_A, T_B and the guard holds, a fresh node +/− with
children T_A, T_B (subtrees may be duplicated freely — trees, not DAGs,
impose no sharing constraints) witnesses A ∪ B or A ∖ B. ∎

**Lemma 2 (left-linear winnability).** P admits a winning left-linear
da-tree iff P∖{⊤} is reachable from {∅} ∪ {S_v : µ(v) ≠ 0} under the
operations A ↦ A ∪ S (disjoint) and A ↦ A ∖ S (S ⊆ A) with S ranging over
{∅} ∪ {S_v : µ(v) ≠ 0} only.

*Proof.* In a left-linear tree the left spine carries the intermediate
states and every combination step has a leaf as its right operand. ∎

**Lemma 3 (enumeration).** For n ≥ 3, unlabeled lattices with n elements
correspond bijectively to unlabeled posets Q on n−2 points such that in
Q ∪ {⊥,⊤} every pair of incomparable points of Q with a common upper bound
in Q has a least one. (Then all joins exist, and a finite bounded poset with
all joins is a lattice.)

*Proof.* A lattice's interior P∖{⊥,⊤} determines it; conversely the bounded
extension of Q is a lattice iff every pair has a join, which for pairs
involving ⊥, ⊤ or comparable pairs is automatic, and meets then exist by the
standard semilattice argument (finite, bounded, join-complete). ∎

**Remark (duality robustness).** The census consumes `nauty-genposetg`
output as Hasse diagrams with edges read upward. If the generator's edge
convention were the opposite, every computation would run on the dual
lattice; since duality is a bijection on unlabeled lattices, the census as a
whole — a universally quantified statement over all lattices of each size —
would be unchanged. (The convention was additionally confirmed empirically:
with edges read downward the lattice filter would not reproduce A006966,
and it does, at thirteen consecutive sizes.)

## 4. The census (CERTIFIED)

**Theorem A.** Every lattice with at most 15 elements admits a winning
left-linear da-tree. Consequently:

1. the minimal lattice with no winning da-tree ([3], §9 OP 1) has **at
   least 16 elements** (upper bound from [3]: ≈ 1.00011·10¹⁵);
2. the minimal lattice with no winning *left-linear* da-tree ([2], §9 OP 1)
   has **at least 16 elements** (same upper bound, via [3]);
3. no lattice with at most 15 elements separates left-linear from general
   da-trees, so the separation implied by [2] happens strictly above 15
   elements.

Label: CERTIFIED — exhaustive, exact integer/bitmask arithmetic, no
floating point, deterministic, reproducible by `./run_census.sh n`; the
verification layer is described below. Scope: 171,432,955 lattices
(3 ≤ n ≤ 15); nothing is claimed beyond n = 15.

| n | posets on n−2 (A000112 ✓) | lattices (A006966 ✓) | winning | left-linear winning |
|---|---|---|---|---|
| 3 | 1 | 1 | 1 | 1 |
| 4 | 2 | 2 | 2 | 2 |
| 5 | 5 | 5 | 5 | 5 |
| 6 | 16 | 15 | 15 | 15 |
| 7 | 63 | 53 | 53 | 53 |
| 8 | 318 | 222 | 222 | 222 |
| 9 | 2,045 | 1,078 | 1,078 | 1,078 |
| 10 | 16,999 | 5,994 | 5,994 | 5,994 |
| 11 | 183,231 | 37,622 | 37,622 | 37,622 |
| 12 | 2,567,284 | 262,776 | 262,776 | 262,776 |
| 13 | 46,749,427 | 2,018,305 | 2,018,305 | 2,018,305 |
| 14 | 1,104,891,746 | 16,873,364 | 16,873,364 | 16,873,364 |
| 15 | 33,823,827,452 | 152,233,518 | 152,233,518 | 152,233,518 |

Every generated-poset count equals OEIS A000112(n−2) and every
lattice-filter count equals OEIS A006966(n) exactly; these anchors validate
the generator invocation and the lattice filter at every size. "Winning"
= "left-linear winning" = the lattice count at every size: no non-winning
lattice and no left-linear/general separation exists in range.

**Corollary B (set-family form).** Every set family F whose intersection
lattice (the intersections of nonempty subfamilies together with the union
1̂, ordered by inclusion — [1, Definition 2.2]) has at most 15 elements
satisfies the original NCI conjecture [1, Conjecture 3.4]; equivalently, a
counterexample family has more than 15 distinct subfamily intersections
(counting 1̂). This follows from Theorem A through the equivalences proved
in [1] (§4: winnability is invariant under intersection-lattice
isomorphism; Remark 2.3: every finite lattice arises) and restated as the
translation in [3, Remark 3.4]; those statements were checked against the
papers today, but their proofs were not re-verified here — the corollary's
label is CERTIFIED *modulo those cited equivalences*.

## 5. Method and verification layer

**Pipeline.** `nauty-genposetg (n−2) t q [m x parts]` streams Hasse
diagrams of all posets on n−2 points in digraph6; `lattscan.c` filters to
lattices (Lemma 3: least-common-upper-bound check over incomparable pairs,
O(1) per pair via the topological order), computes µ by the defining
recursion, forms the leaf masks, and decides left-linear winnability by the
Lemma 2 BFS over bitmask states. A left-linear win implies a win, so the
general Lemma 1 closure (with early detection: a state C wins as soon as
its complement inside the target is already present) runs only on lattices
that fail the left-linear BFS — in range, none did. A lattice failing both
would be printed as a candidate counterexample; a lattice failing
left-linear but winning generally would be printed as an explicit
separation witness. State spaces are ≤ 2^(n−1) ≤ 16,384 bitmasks, so both
decisions are exact and total — no budgets, no sampling, no heuristics in
the decision path.

**Verification layer.**

1. *Count anchors.* Poset and lattice counts match OEIS A000112/A006966 at
   all thirteen sizes (b-files fetched 2026-08-28; A000112 is exact there
   through n = 16, A006966 through n = 19).
2. *Dual implementation.* An independent Python implementation
   (`reference.py`: same specification, separate code) reproduces
   (posets, lattices, winning, left-linear winning) exactly: in full for
   all n ≤ 11 and again in full at n = 12 (262,776 lattices;
   `data/crosscheck_full_n12.txt`), and on generator slices at n = 14
   (1,201,420 posets / 41,149 lattices, `data/crosscheck_slice_n14.txt`)
   and n = 15 (`data/crosscheck_slice_n15.txt`), all four counters
   matching in every case.
3. *Published example.* The lattice of [3, Figure 3.1] (9 elements,
   reconstructed from the paper) gives µ values matching the paper's
   remarks (coatoms −1; doubly-parented level-2 elements +1; µ(⊥) = 0
   there) and is decided WINNING by both implementations;
   `verify_witness.py` extracts the explicit tree
   ((S_a − S_d) + S_g) + ((S_c − S_e) + (S_b − S_f)) and re-verifies it
   against Definition 3.1 mechanically.
4. *Hand controls.* M₃ (µ(⊥) = 2) and N₅ (µ(⊥) = 1) winning with
   hand-checkable trees; an artificial negative control (a 3-chain with the
   middle leaf deleted) is correctly reported non-winning, exercising the
   exhaustion path of the decision procedure.
5. *Witness spot checks.* For the maximum-state-count lattice of every
   census part at n = 14 (8/8) and n = 15 (16/16), `verify_witness.py`
   independently rebuilds the lattice from its digraph6 line
   (boolean-matrix closure, raw-definition lattice test checking both
   joins and meets, recursive µ), finds an explicit winning left-linear
   sequence by its own BFS, and re-verifies that sequence mechanically
   against Definition 3.1 (`data/crosscheck_witness_n1{4,5}.txt`).

**Cost** (4 cores, cloud sandbox, 2026-08-28). n ≤ 13: ~80 s total,
single-pipeline. n = 14: 5 min 13 s wall / 15 min 9 s CPU, 8 generator
parts, 4-way parallel. n = 15: 132 min 55 s wall / 8 h 14 min CPU, 16
parts, 4-way; the generation and parsing of 3.38·10¹⁰ posets dominates
(the 152M lattice decisions are a small fraction of the work — the poset
route's 0.45% lattice yield is the bottleneck). Peak memory per process
< 10 MB. No randomness anywhere (seeds: none).

## 6. Structural observations (data, not theorems)

- **Left-linear suffices everywhere in range.** Not only is every lattice
  with ≤ 15 elements winnable — every one is winnable by the most
  restrictive tree shape in the literature's hierarchy. The separation
  [2]/[3] prove must exist begins above 15 elements. (Their probabilistic
  regime is p ≥ 10⁵; the smallest instance of their construction *family*,
  p = 5, already has 177 elements, far beyond exhaustive state-closure —
  closing the gap [16, 1.00011·10¹⁵] needs either theory or a structured
  search on P_{p,m}, not this census.)
- **Unique-coatom fast path.** Lattices whose top covers a single element
  are winning by the single leaf S_c; their count at size n equals
  A006966(n−1) (delete ⊤ — a bijection onto lattices with n−1 elements),
  observed exactly at every size in the v1 run (e.g. 262,776 of the
  2,018,305 lattices at n = 13).
- **State-space growth.** The worst-case number of BFS states in the
  left-linear decision is exactly 2^(n−1) − 1 at every size 4 ≤ n ≤ 15
  (1023 at n = 11, …, 8191 at n = 14, 16383 at n = 15) — some lattice
  explores all but one subset of the (n−1)-point ground set before its
  decision; the median is single-digit. The census cost is dominated by poset generation, not by
  decisions — which is why a dedicated lattice generator is the right next
  tool (see §8).

## 7. Relation to prior verification

[1] reports (§"Counterexample search", checked verbatim today): brute force
over Sperner families shows the conjecture holds for all intersection
lattices whose ground set 1̂ has **at most 5 points** — in the *strong*
version (left-linear and with prescribed polarity) — with n = 6 already too
large, and random searches finding nothing. Their bound is by *point
count*; ours is by *lattice size*. The two are incomparable: a family on 5
points can have an intersection lattice with up to 2⁵+1 > 15 elements
(e.g. the full Boolean family), which our census does not reach, while a
15-element lattice can require up to 14 points in its canonical family,
far beyond their n ≤ 5. Neither bound subsumes the other; both floors
stand. (Our census does not impose their polarity restriction; theirs does
not decide our n ∈ [6..15] lattices of low point complexity.)

## 8. Open questions

1. Close the gap: the minimal counterexample lies in [16, 1.00011·10¹⁵].
   The bottleneck of this census is poset generation (yield 0.45% at
   n = 15). A canonical-construction-path generator producing lattices
   directly (Heitzig–Reinhold / Jipsen–Lawless style, who enumerated
   A006966 through n = 19–20 (secondary)) would make n = 16–18 reachable
   with the same decision engine.
2. Find the minimal left-linear/general separating lattice — now known to
   have ≥ 16 elements. The engine surfaces any such witness automatically
   (`SEPARATING` lines).
3. Decide winnability of P_{5,m} / P_{7,m} (177 / 443 elements) for
   concrete markings: find-a-win heuristics suffice for "winnable", but
   "non-winnable" at that size is beyond exact closure — the first genuinely
   new idea needed on the lower-bound side.
4. [3, §9 OP 2] asks how many µ = 0 leaves a weakened tree must use; the
   census infrastructure (leaf sets are a parameter) can measure this in
   range with one-line changes.

## References

[1] A. Amarilli, M. Monet, D. Suciu, *The Non-Cancelling Intersections
Conjecture*, arXiv:2401.16210 (2024). (Full text read 2026-08-28.)

[2] H. Wilhelm, *The non-cancelling-intersections conjecture fails for
left-linear trees*, arXiv:2608.19414 (2026-08-19). (Full text read
2026-08-28.)

[3] H. Wilhelm, *Refutation of the Non-Cancelling-Intersections
Conjecture*, arXiv:2608.27416 (2026-08-27). (Full text read 2026-08-28.)

OEIS A000112 (posets), A006966 (lattices): b-files fetched 2026-08-28.
