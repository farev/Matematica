# Signed difference sets: bulk closure of the open cells of Gordon's database

*Session 2026-08-09. AI-assisted (Claude); all proofs below are
self-contained and human-checkable; all computations ship code and
certificates in this directory.*

## Abstract

A signed difference set SDS(v,k,λ) in a finite abelian group G of order v
is an element A of the group ring Z[G] with coefficients in {−1,0,+1},
exactly k of them nonzero, satisfying A·A^(−1) = k·e + λ(G−e). Gordon
introduced the notion (Des. Codes Cryptogr. 91 (2023) 2107–2115,
arXiv:2212.10630) with a companion database of 70,543 parameter cells, of
which 67,823 were marked Open in the snapshot fetched 2026-08-09
(sha256 `39bab9fc…ca85`). We prove two nonexistence criteria for SDS —
verbatim transfers of the classical even-order square condition of
symmetric-design theory and of Turyn's self-conjugacy argument — and apply
them to every cell: **45,328 of the 67,823 Open cells are closed**
(23,997 by the first, 21,331 by the second), each with a one-line
checkable certificate. Independently, an exhaustive-search engine,
validated by reproducing the entire decided database at v ≤ 24 (42 cells,
zero discrepancies) and by exact witness-list agreement with a second
implementation, decides the small Open cells the criteria do not reach
(list in §5; every nonexistence double-checked against the criteria with
zero conflicts). Finally, an audit with an independent checker found that
**147 of the 280 witness sets stored in the database fail the defining
equation** (21 of 144 witness-bearing cells); for the one such cell small
enough to re-enumerate completely, SDS(20,11,2) in Z₂₀, we show the
cell's "All" status is nonetheless correct (exactly 40 labeled sets in 2
translation classes) and the stored sets are true sets with elements
swapped between the plus- and minus-parts — an export-stage defect.

## 1. Definitions and notation

Let G be a finite abelian group of order v, written additively, and let
Z[G] be its integral group ring with basis {x^g : g ∈ G} and involution
A ↦ A^(−1) induced by g ↦ −g. A **signed difference set** SDS(v,k,λ) in G
is A = Σ_g A(g)·x^g with A(g) ∈ {−1,0,+1}, #{g : A(g) ≠ 0} = k, and

    A · A^(−1)  =  k·e + λ·(G − e)                                (1)

in Z[G], where e = x^0 and G also denotes Σ_g x^g. Equivalently, for
every d ≠ 0, the signed autocorrelation Σ_g A(g)A(g−d) equals λ. Write
P = {g : A(g) = +1}, M = {g : A(g) = −1}, σ = |P| − |M|. Difference sets
are the case M = ∅; circulant weighing matrices are cyclic G with λ = 0.
This is exactly the convention of Gordon's reference checker `is_sds`
(his `sds_code.py`, shipped in `data/`), against which our independent
checker agrees on all 133 valid stored witnesses.

**Lemma 1 (character identities).** Let A be an SDS(v,k,λ) in G and χ a
character of G. Then

    |χ(A)|² = k − λ   for χ nontrivial,      σ² = k + λ(v−1)      (2)

for the trivial χ. In particular s := √(k+λ(v−1)) ∈ Z≥0 with s ≡ k
(mod 2), |P| = (k+s)/2 and |M| = (k−s)/2 after the global sign flip
A ↦ −A (which preserves (1)) normalizing σ ≥ 0.

*Proof.* Extend χ linearly to Z[G]. Since χ(A^(−1)) = Σ A(g)χ(−g) =
conj(χ(A)) and χ(G) = 0 for nontrivial χ (column orthogonality), applying
χ to (1) gives |χ(A)|² = k − λ; the trivial character gives
σ² = k + λ(v−1). The parity claim: σ ≡ |P| + |M| = k (mod 2). ∎

## 2. Two nonexistence criteria

**Theorem 1 (even order; the classical even-v square condition).** If v
is even and k − λ is not a perfect square, then no SDS(v,k,λ) exists in
any abelian group of order v.

*Proof.* An abelian group of even order has a subgroup of index 2, hence
a character χ of order 2, whose values are ±1. Then χ(A) ∈ Z and (2)
gives k − λ = χ(A)². ∎

**Theorem 2 (self-conjugacy; Turyn's argument).** Let m > 2 divide
exp(G), and let p be a prime with p ∤ m such that p^j ≡ −1 (mod m) for
some j ≥ 1. If v_p(k−λ) is odd, then no SDS(v,k,λ) exists in G.

*Proof.* Take χ of order exactly m (it exists because m | exp(G)) and
α = χ(A) ∈ Z[ζ_m], so αᾱ = n := k−λ by (2). The Galois group of
Q(ζ_m)/Q is (Z/m)^×, and the decomposition group of any prime ideal P
above p is ⟨p mod m⟩, which by hypothesis contains −1, i.e. complex
conjugation; hence P̄ = P. Since p ∤ m, p is unramified, so
v_P(n) = v_p(n) is odd, while v_P(αᾱ) = v_P(α) + v_P(ᾱ) =
v_P(α) + v_{P̄}(α) = 2·v_P(α) is even — a contradiction. ∎

*(The hypothesis p ∤ m is essential: for p | m, ramification defeats the
argument, and Gauss sums realize |α|² = p in Z[ζ_p].)*

**Remarks on novelty.** Both arguments are classical: Theorem 1 is the
signed analogue of the standard "v even ⇒ k−λ square" condition for
symmetric designs / abelian difference sets, and Theorem 2 is Turyn's
self-conjugacy test, standard in difference-set and weighing-matrix
nonexistence. Their transfer to SDS is immediate from Lemma 1 (the
{−1,0,+1} coefficients play no role beyond χ(A) lying in Z[ζ_m]).
Gordon's paper (arXiv:2212.10630) is egress-blocked from this sandbox and
unread — it may well state one or both transfers, and we mark the
*criteria* as possible rediscoveries accordingly (secondary). What is
demonstrably new is their systematic application to the database: cells
as small as SDS(18,15,2,[3,6]) (k−λ = 13, v even) were Open in the
2026-08-09 snapshot, so the artifact had not absorbed even Theorem 1.
Lemma 1's trivial-character part reproduces, as a special case at λ = 0,
the classical fact that the weight of a circulant weighing matrix is a
perfect square — a literature anchor for the machinery.

## 3. Bulk application to the database

`theory.py` applies an admissibility test T0 (s ∈ Z, s ≡ k mod 2,
s ≤ k, k ≤ v — all following from Lemma 1) and Theorems 1 (T1) and 2
(T2) to each of the 70,543 cells. Results on the 2026-08-09 snapshot:

| shelf | count |
|---|---|
| Open cells closed by T1 | 23,997 |
| Open cells closed by T2 (and not T1) | 21,331 |
| **Open cells closed, total** | **45,328 of 67,823** |
| Yes/All cells violating any criterion | **0** (146 cells checked) |
| exhaust decisions conflicting with criteria | **0** |
| Gordon's exhaust-No cells retro-covered by the criteria | 984 of 2,574 |

Each closure is recorded in `data/theory_closures.csv` as
(cell, criterion, m, p, v_p(k−λ)) — a certificate checkable by hand or
by rerunning `theory.py` (1.1 s). The zero-violation rows are the
soundness controls: the criteria never contradict a cell known to
contain an SDS (every such cell's witnesses were verified
independently first, §6), and never contradict an exhaust decision.

## 4. The exhaustive-search engine

`sds_search.c` performs a depth-first search over assignments
A: G → {−1,0,+1} in a fixed element order, with |P| and |M| forced by
Lemma 1, exact incremental correlation sums, and an interval prune
(each unresolved pair can move a correlation by at most 1). One
reduction is applied in production mode:

**Lemma 2 (translation reduction).** For p ∈ P, the translate
A'(g) = A(g+p) is an SDS with the same parameters and 0 ∈ P'. Hence
restricting the search to A(0) = +1 preserves existence and
nonexistence. (|P| ≥ 1 holds in every admissible cell since s ≤ k.) ∎

Validation (all before any new claim; `check_engine.py`, `sweep.py`):

- **Full concordance at v ≤ 24**: the engine reproduces the status of
  all 42 decided cells — every No is NONEXIST, every Yes/All is EXIST
  with witnesses re-verified by the independent checker. Zero
  discrepancies.
- **Exact dual-implementation agreement**: on 8 cells (including two
  then-Open ones) an independent pure-Python exhaust returns literally
  identical witness lists.
- **Mutual control with §2**: every criterion-closed cell that was also
  exhausted came back NONEXIST (17 cells at first freeze; final count in
  `data/results.csv`).
- A v1 pruning bug (double-removal of pairs adjacent to decided zeros)
  was caught by the EXIST side of this battery — see WRITEUP; the fix
  and the re-validation are part of the session record.

## 5. New decisions of Open cells

Authoritative table: `data/values.csv` (generated by `make_values.py`
from `data/results.csv`; every row carries engine+source sha256 and
wall time; certificates in `certs/`). Every EXIST row ships an explicit
witness verified by the independent checker; every NONEXIST row is an
exhaust with node counts, plus — where the criteria also apply — an
independent proof. Final counts in README; the mathematical content:

**New signed difference sets (existence cells).** Eight previously-Open
cells contain SDS; representative witnesses (full lists in `certs/`,
elements as coordinates in the invariant-factor groups):

- SDS(25,12,1) in Z₅×Z₅ — a λ = 1 signed difference set:
  P = {00,01,02,10,11,12,23,30,43}, M = {03,22,24} (digits = coordinates).
- SDS(27,10,1) in Z₃×Z₉: P = {(0,0),(0,1),(0,2),(0,3),(0,6),(1,1),
  (1,8),(2,5)}, M = {(0,4),(1,7)}; also exists in Z₃³.
- SDS(27,14,5) in both non-cyclic groups of order 27.
- SDS(27,17,8) in Z₃³ (it was known in Z₃×Z₉; today's exhaust shows it
  does **not** exist in Z₂₇ — completing the parameter across all three
  groups of order 27).
- SDS(32,28,12) in Z₄×Z₈ and in Z₂×Z₄×Z₄ — and in **no other** abelian
  group of order 32 (all five remaining groups exhausted empty).

**Group structure decides existence.** Two exhibits from today's table:

Order 27 (columns: Z₂₇ / Z₃×Z₉ / Z₃³; "No" = Gordon, else today):

| (v,k,λ) | Z₂₇ | Z₃×Z₉ | Z₃³ |
|---|---|---|---|
| (27,10,1) | No | **exists** | **exists** |
| (27,12,2) | No | empty | empty |
| (27,14,5) | No | **exists** | **exists** |
| (27,17,4) | No | empty | empty |
| (27,17,8) | **empty** | Yes (known) | **exists** |
| (27,22,3), (27,22,9), (27,23,1), (27,23,13), (27,25,16) | No/empty | empty | empty |

At order 27 the cyclic group carries nothing anywhere on the shelf,
while both non-cyclic groups carry SDS at three parameter triples —
in this range cyclicity is an obstruction, not an aid.

Order 32, parameter (32,28,12) across all seven abelian groups:

| G | [32] | [2,16] | [4,8] | [2,2,8] | [2,4,4] | [2,2,2,4] | [2,2,2,2,2] |
|---|---|---|---|---|---|---|---|
| SDS? | empty | empty | **exists** | empty | **exists** | empty | empty |

The two existing groups are exactly the ones containing a Z₄×Z₄
subgroup. With seven data points this is an observation, not a theorem
(NUMERICAL-grade pattern; recorded as open question 5 in §7).

## 6. The witness audit

`check_db.py` runs the independent checker over every stored witness:
**133 of 280 verify; 147 fail**, concentrated in 21 of the 144
witness-bearing cells (all cyclic; the other 123 cells — all Paley, all
He–Chen–Ge, all "Paley and zero", 23 orbit-exhaust cells — verify
perfectly, which pins the convention). No symmetry of definition (1)
(translation, group automorphism, inversion, global sign flip — all of
which preserve the multiset of off-peak correlations) can repair a set
whose correlation profile is non-constant, so these are invalid as
stored, not differently-encoded. One quirk is separate: the witness of
SDS(18,13,4,[3,6]) is stored in undeclared Z₃×Z₃×Z₂ coordinates and
verifies once decoded (`check_db.py` reports it).

Forensics on the smallest affected cell, SDS(20,11,2,[20]) (status
"All", 4 stored sets, all invalid): complete enumeration
(`--all`, no reduction; 5,426,081 nodes, 1.3 s) finds **exactly 40
labeled SDS**, forming 2 translation classes. The stored sets are true
sets with elements exchanged between P and M — stored set 0 is a true
set with 9 and 11 swapped (symmetric difference 4); sets 1 and 3 are two
swaps away. The cell's status is therefore **correct**, and the defect
is an export-stage corruption of the witness lists.

The mechanism generalizes: `repair.py` searches the ≤2-swap
neighborhood of every invalid stored set and **repairs 22 of the 147,
each re-verified independently** (`data/repaired_witnesses.csv`) —
recovering at least one valid witness for **12 of the 21 affected
cells**: every stored set of SDS(20,11,2,[20]) and SDS(35,21,10,[35]),
all four of SDS(247,127,63,[247]), both of SDS(499,250,123,[499]), and
single sets of SDS(61,49,36), SDS(167,84,40), SDS(191,96,46),
SDS(199,100,48), SDS(347,174,85), SDS(379,190,93), SDS(443,222,109),
SDS(491,246,121). The Yes/All statuses of those 12 cells are thereby
confirmed constructively. The remaining **9 cells** — SDS(51,19,3),
SDS(78,53,28), SDS(104,29,4), SDS(111,66,17), SDS(181,136,11),
SDS(182,38,2), SDS(182,101,20), SDS(200,151,102), SDS(277,208,17) —
hold only sets more than two swaps from any valid SDS; their statuses
rest on Gordon's exhaust claims alone (deeper repair — support-changing
moves — is an open thread). The 21 affected
cells are listed in `data/witness_audit.csv`; the second-smallest,
SDS(35,21,10,[35]), is re-exhausted in this session if time permits
(see README). This audit is reportable upstream (the repository's README
invites problem reports to dmgordo@gmail.com).

## 7. Open questions

1. The surviving small cells: after criteria + exhausts, the smallest
   still-Open cells (see README table) — do sporadic SDS live there?
   The (32,20,4) family across all seven abelian groups of order 32 is
   the natural next target (naive cost 5.5·10¹¹ per group; needs either
   patience or automorphism-orbit canonicalization).
2. Equivalence conventions: Gordon's "All" cells list orbit
   representatives under an equivalence we did not need to pin for
   existence questions; pinning it (translations × Aut(G) × inversion ×
   sign flip?) matters before contributing complete enumerations
   upstream.
3. Do stronger classical tests (Mann-type, multiplier theorems,
   field-descent) transfer as cleanly and close more of the 22,495
   surviving Open cells? The 2-adic behavior at ramified primes (the
   Gauss-sum escape hatch in Theorem 2) is where signed sets genuinely
   differ from difference sets.
4. Existence side: He–Chen–Ge's PDS constructions populate ten cells;
   today's exhausts found sporadic SDS at eight more (§5). Is there a
   uniform construction behind the (27,10,1)/(27,14,5)/(27,17,8)
   non-cyclic family?
5. Does (32,28,12) existing exactly in the two order-32 groups
   containing Z₄×Z₄ generalize — i.e., is there a transfer/projection
   argument through a Z₄×Z₄ quotient or subgroup that explains both the
   existence and the five nonexistences?

## References

(All secondary unless noted: the papers are egress-blocked from this
sandbox; the database and code are primary, fetched 2026-08-09.)

- D. M. Gordon, *Signed difference sets*, Des. Codes Cryptogr. 91 (2023)
  2107–2115; arXiv:2212.10630. (secondary)
- Companion repository `dmgordo/signed-difference-sets` (primary:
  `sds.json` sha256 `39bab9fce78d5c4353c22ba482ff5c3bb8b8b9931edc5ca0fc60062dfe80ca85`,
  `sds_code.py`, README; fetched 2026-08-09, snapshot in `data/`).
- Z. He, X. Chen, G. Ge, *New constructions of signed difference sets*,
  arXiv:2306.05631 (2023). (secondary)
- R. J. Turyn, *Character sums and difference sets*, Pacific J. Math. 15
  (1965) 319–346 — the self-conjugacy argument of Theorem 2. (secondary)
- Classical even-v square condition for symmetric designs (Schützenberger;
  Bruck–Ryser–Chowla circle): any standard design-theory text. (secondary)
