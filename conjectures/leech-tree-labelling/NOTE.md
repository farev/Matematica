# Leech's tree-labelling problem: the eleventh term

*Research note, 2026-09-18. AI-assisted (Claude, Anthropic); all mathematics
below was checked by the author of the session and every computation is
reproducible from the files in this directory.*

## Abstract

For a tree T on n vertices with positive integer edge weights, say T *covers*
[1, k] when every integer 1, 2, …, k is the weighted length of a path between
two vertices. Leech (1975) asked for the largest such k, a(n), and computed
a(2..10) = 1, 3, 6, 9, 15, 20, 26, 34, 41 (OEIS A007187, Guy UPINT §C10); the
entry has carried only "a(11) ≥ 48, a(12) ≥ 55" since. We give a budgeted
form of the forced-least-missing-weight recursion used for perfect Leech
trees, prove the pruning rules it relies on, re-derive a(2..10) from scratch,
and determine **a(11) = 49**: the tree with edges (0,1,1) (2,3,1) (0,4,2) (5,6,4) (3,6,5) (5,7,7) (6,8,8) (5,9,11) (2,10,22) (0,3,24) covers [1, 49], and an exhaustive search over 1.40·10⁹ nodes shows that no tree on 11 vertices covers [1, 50]. So the recorded bound a(11) ≥ 48 was not sharp. Every value carries a checker-verified witness
tree; every refutation is an exhaustive search whose per-run node counts are
recorded, single-engine at n = 11 (see §6).

## 1. Definitions and statement

Let T = (V, E, w) be a tree with n = |V| vertices and w : E → Z_{>0}. For
x ≠ y write d(x, y) for the weight of the unique x–y path, and call the
multiset {d(x, y) : {x, y} ∈ C(V, 2)} the distance spectrum; N = C(n, 2).
T covers [1, k] if every v ∈ [1, k] is in the spectrum. A007187(n) = a(n) is
the largest k for which some T on n vertices covers [1, k]. Trivially
a(n) ≤ N, with equality iff a Leech tree (spectrum exactly [1, N]) exists;
Taylor (1977) showed this needs n = m² or m² + 2, and Leech, Székely–Wang–Zhang
(2005), Calhoun–Ferland–Lister–Polhill (2007) and Ghodsi (2026) excluded
n = 5, 9, 11, 16, 18, leaving n = 2, 3, 4, 6 as the only orders with Leech
trees below 25 (all cited through Ghodsi 2026, arXiv:2609.20492, §1; Leech
1975 and Taylor 1977 are (secondary) here).

**Excess.** If T covers [1, k] then exactly k of its N pairs are "first
realisations" of the values 1..k and the remaining E := N − k pairs are
*excess*: they repeat a value or exceed k. For a subforest F ⊆ T define the
excess of F as (number of pairs inside components of F) − (number of distinct
values in [1, k] they realise).

## 2. The search and its soundness

Fix n, k, and B := N − k. Order the edges of a covering tree T by
nondecreasing weight, e_1, …, e_{n−1} (ties in any order), and let
F_j = {e_1, …, e_j}, a spanning forest. Write D(F_j) for the set of values in
[1, k] realised inside components of F_j and m_j = mex D(F_j) for the least
value of [1, k] not in D(F_j) (m_j = k + 1 if none). The engine
(`code/cover_search.c`) enumerates the sequences F_0 ⊂ F_1 ⊂ … by choosing,
at step j + 1, a weight q, two components and one port vertex in each. The
following lemmas justify its pruning; each is a statement about an arbitrary
covering tree T and its prefix forests, so any tree the search misses would
violate one of them.

**Lemma 1 (weight window).** w(e_{j+1}) ≤ m_j, and w(e_{j+1}) ≥ w(e_j).

*Proof.* The second part is the ordering. For the first, suppose
w(e_{j+1}) > m := m_j ≤ k. Since T covers [1, k], some path P has weight m.
Every edge of P has weight ≤ m < w(e_{j+1}) ≤ w(e_i) for all i ≥ j + 1, so
P ⊆ F_j and m ∈ D(F_j), contradicting the choice of m. ∎

Consequently, if m_j < w(e_j) no completion exists: all remaining edges have
weight ≥ w(e_j) > m_j, so m_j can never be realised.

**Lemma 2 (monotone excess).** The excess of F_j is nondecreasing in j and
equals E = N − k at j = n − 1. Hence a prefix whose excess exceeds B has no
completion. *Proof.* Pairs are only added; a new pair either realises a new
value in [1, k] or is excess. ∎

**Lemma 3 (parity).** Two-colour V by the parity of d(r, ·) from any root r;
two vertices are at odd distance iff they have different colours. If the
colour classes have sizes a and n − a, the number of odd-distance pairs is
a(n − a), and a covering tree must satisfy
⌈k/2⌉ ≤ a(n − a) ≤ ⌈k/2⌉ + B and ⌊k/2⌋ ≤ N − a(n − a) ≤ ⌊k/2⌋ + B.
For a prefix forest each component carries its own two classes (up to a
swap), and the global classes are unions of one class from each component.
*Proof.* Odd values in [1, k] need ⌈k/2⌉ distinct odd-distance pairs, and
every other odd pair is excess; likewise for even. Restriction of the global
colouring to a component is one of its two parity colourings. ∎ (This is
Taylor's argument in budgeted form; at B = 0 it is his order restriction.)

**Lemma 4 (edge load).** If the next edge joins components K_i and K_j with
weight q then q ≤ k + 1 + B − min(|K_i|(n − |K_i|), |K_j|(n − |K_j|)).
*Proof.* In T the edge separates sides S ⊇ K_i and V ∖ S ⊇ K_j, so it lies on
|S|(n − |S|) ≥ min(…) paths (s(n − s) is concave in s), all of weight ≥ q. At
most k − q + 1 values of [1, k] are ≥ q, so at most k − q + 1 + B pairs have
distance ≥ q. ∎

**Lemma 5 (blocks; after Ghodsi 2026, Theorem 4.1).** Let K_i, K_j be two
components of F_j. There are vertices p ∈ K_i, p′ ∈ K_j (the ports) and an
integer L ≥ w(e_j) such that d(x, y) = d(x, p) + L + d(p′, y) for all x ∈ K_i,
y ∈ K_j. *Proof.* The x–y path leaves the subtree K_i at a unique vertex p and
enters K_j at a unique p′ (independent of x, y because T is a tree and
K_i, K_j are connected), and L = d(p, p′). The first edge after p is not in
K_i, hence not in F_j, hence has weight ≥ w(e_j). ∎

Call B_{ij}(p, p′, L) = {d(x, p) + L + d(p′, y)} the block and its excess
ex(B) = |K_i||K_j| − #{distinct values of B in [1, k] not in D(F_j)}. Since
the future pairs are partitioned by the component pairs, the future excess is
at least Σ_{i<j} ex(B_{ij}) for the true blocks, and each true block has
ex ≤ B − (current excess) =: rem. The engine uses: (5a) Σ_{i<j} min_{p,p′,L}
ex(B_{ij}) ≤ rem, with L ranging over [w(e_j), k] and the option "L > k"
(all |K_i||K_j| pairs excess); (5b) every uncovered value lies in some block
with ex ≤ rem (Hall); (5c) when at most 4 components remain and rem ≤ 2, an
exact search over one admissible block per pair, counting overlaps between
chosen blocks as further excess (for chosen blocks A_l the future excess is
exactly Σ_l (ex(A_l) + |A_l ∩ ∪_{l′<l} A_{l′}|)), with look-ahead by the
suffix sums of per-pair minima; the exact search fails open on a step cap or
a candidate cap. Sound because the true blocks are admissible.

**Lemma 6 (symmetry).** If two components of F_j are isomorphic as weighted
trees, the transposition exchanging them is an automorphism of the weighted
forest; hence the search may restrict merges to the first component of each
isomorphism class, and to the first two when both come from one class.
Isomorphism is decided by a canonical string (rooted AHU encoding with edge
weights, rooted at the hop-centre, or the sorted pair of half-encodings for a
bicentral tree), a complete invariant. Singletons are one class, which is the
usual "attach to the lowest unused vertex" rule. ∎

**Completeness.** Given a covering tree T with sorted edges, the search
generates F_0, F_1, … : at each step Lemma 1 admits w(e_{j+1}); the component
pair and ports of e_{j+1} are enumerated (up to Lemma 6, after which the
state is an isomorphic forest, and every test used is an isomorphism
invariant); Lemmas 2–5 are necessary conditions satisfied by every prefix of
T. So if the search reports no tree, none exists.

**Witnesses.** When D(F_j) = [1, k] the remaining components may be joined
by edges of any weight; the engine prints such edges with weight 1000 + i.
`code/check_cover.py` re-derives all path sums from the printed edges with
no shared code and checks 1..k.

## 3. Positive control

The engine reproduces the entire published ladder from scratch (single run,
4-core sandbox, ≤ 15 s total for n ≤ 10):

| n | N | a(n) | witness (u,v,w) | refuted k | nodes at refutation |
|---|---|---|---|---|---|
| 2 | 1 | 1 | (0,1,1) | — | — |
| 3 | 3 | 3 | (0,1,1)(0,2,2) | — | — |
| 4 | 6 | 6 | (0,1,1)(0,2,2)(0,3,4) | — | — |
| 5 | 10 | 9 | (0,1,1)(0,2,1)(1,3,3)(1,4,6) | 10 | 1 (parity) |
| 6 | 15 | 15 | (0,1,1)(0,2,2)(3,4,4)(0,3,5)(3,5,8) | — | — |
| 7 | 21 | 20 | (0,1,1)(0,2,2)(3,4,4)(3,5,4)(0,4,5)(4,6,12) | 21 | 1 (parity) |
| 8 | 28 | 26 | (0,1,1)(0,2,2)(1,3,3)(4,5,5)(4,6,5)(0,5,7)(5,7,15) | 27 | 7 500 |
| 9 | 36 | 34 | (0,1,1)(0,2,2)(0,3,3)(2,4,6)(5,6,7)(2,5,10)(5,7,14)(5,8,18) | 35 | 71 554 |
| 10 | 45 | 41 | (0,1,1)(0,2,1)(1,3,3)(4,5,6)(1,4,7)(5,6,11)(4,7,12)(5,8,17)(5,9,23) | 42 | 14 062 200 |

All nine values agree with A007187. (At n = 8 and n = 10 the parity lemma
alone refutes k = N and k = N − 1.) An independent SAT engine
(`code/satcover.py`: one CNF per unlabelled tree shape, unary weights and
unary path sums, coverage clauses; shapes generated by `code/trees.py` and
counted against A000055) agrees at n = 7, 8 (all shapes) and on the first 17 of the 47 shapes of n = 9, k = 35 (each UNSAT, 1–3 min per shape; stopped to free the cores).

## 4. n = 11: a(11) = 49

**Theorem 1.** a(11) = 49.

*Lower bound (CERTIFIED by `code/check_cover.py`).* The tree with edges
(u, v, w) = (0,1,1) (2,3,1) (0,4,2) (5,6,4) (3,6,5) (5,7,7) (6,8,8) (5,9,11)
(2,10,22) (0,3,24) (`witnesses/n11_k49.txt`; degrees 3,1,2,3,1,3,3,1,1,1,1)
has distance multiset [1..49] ∪ {1, 11, 23, 25, 26, 39}: every value 1..49
occurs, six values twice, none exceeds 49. Three further witnesses, one from
each of the other workers, are in `runs/run7_n11_k49_w*.txt`, all checked.
For the record the engine also finds a covering tree for k = 48 in 1 s
(`witnesses/n11_k48.txt`), so the OEIS bound is reproduced independently.

*Upper bound (CERTIFIED, single engine).* `cover_search 11 50 5 w 4` for
w = 0..3 (split at depth 5, round-robin over prefixes) all report `found=0`:

| k | B | workers | nodes | seconds (per worker) | verdict |
|---|---|---|---|---|---|
| 55 | 0 | 1 | 2 434 374 (engine 2) | 8.7 | no tree (no Leech tree of order 11, as known) |
| 54 | 1 | 1 | 26 512 620 (engine 2) | 76.7 | no tree |
| 53 | 2 | 1 | 27 939 234 | 28.6 | no tree |
| 52 | 3 | 1 | 121 430 938 | 105.6 | no tree |
| 51 | 4 | 2 | 238 530 202 + 254 545 288 | 203.1, 217.8 | no tree |
| 50 | 5 | 4 | 380 848 963 + 323 587 070 + 355 591 248 + 340 701 535 = 1 400 728 816 | 304.4, 259.4, 283.7, 271.1 | **no tree** |
| 49 | 6 | 4 | 85 450 603 (to first witness, w0) | 65.2 | **witness** |
| 48 | 7 | 1 | 1 376 421 (to first witness) | 1.1 | witness |

(Engine 2 = the bitset engine before the exact-cover and candidate-children
changes; its verdicts at k = 55, 54 and its 141 758 526-node refutation of
k = 53 agree with the final engine.) Wall clock on the 4-core sandbox
(Linux, 15 GB): the k = 50 refutation took under 5 minutes. Node counts are
deterministic and reproduce exactly on rerun.

Hence a(11) = 49. ∎

**Remark.** The excess sequence N − a(n) for n = 2..11 is
0, 0, 0, 1, 0, 1, 2, 2, 4, 6.

## 5. n = 12: 57 ≤ a(12) ≤ 61 [PENDING: 60 if the k = 61 run refutes]

*Lower bound (CERTIFIED).* The tree (0,1,1) (0,2,1) (1,3,1) (2,4,4) (5,6,6)
(7,8,8) (2,7,9) (5,9,14) (7,5,15) (6,10,16) (5,11,29) covers [1, 57]
(`witnesses/n12_k57.txt`, checked; 9 excess pairs). OEIS recorded a(12) ≥ 55.
Witness hunts at k = 58 and 59 (single worker each, 30 and 25 minutes) found
nothing, which is not evidence of nonexistence.

*Upper bound (CERTIFIED, single engine).* `cover_search 12 62` reports
`found=0` after 4 863 094 430 nodes (4 706 s on one core, sharing the
machine): no tree on 12 vertices covers [1, 62], so a(12) ≤ 61.
[PENDING: k = 61 on three workers.] For scale, k = 64 and 63 need no run
(Lemma 3 refutes k = 66, 65 at the root; 64 and 63 are implied by 62).

## 6. The distinct-sum variant (maximum Leech index)

Varghese, Lakshmanan and Arumugam (J. Discrete Math. Sci. Cryptogr. 25 (2022)
2237–2247; abstract read via the Semantic Scholar API, paper paywalled) define
the *Leech index* k(T) of a tree T as the largest k such that some labelling
with all edge labels and all path weights distinct realises 1..k. The maximum
of k(T) over trees of order n is the distinct-sum analogue of a(n); it is at
most a(n), and the two problems differ from n = 8 on. Engine flag `-d`
prunes any repeated path sum (values above k are tracked individually, at
most B of them exist); Lemmas 1–6 apply unchanged, the block candidates are
further required to have no internal repeat and no hit on a covered value,
and chosen blocks in the exact cover must be disjoint.

**Theorem 2 (CERTIFIED, two engines).** The maximum Leech index
over trees of order n = 2, …, 12 is

| n | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| max_T k(T) | 1 | 3 | 6 | 9 | 15 | 20 | 25 | 30 | 37 | 45 | 47 |
| a(n) (repeats allowed) | 1 | 3 | 6 | 9 | 15 | 20 | 26 | 34 | 41 | 49 | ≥ 57 |

Witnesses (all checked by `check_cover.py --distinct`) are in
`witnesses/distinct_n*_k*.txt`; e.g. n = 11, k = 45: (0,1,1) (2,3,2) (0,4,3)
(2,5,5) (6,7,6) (3,6,8) (4,8,9) (8,7,11) (1,9,18) (5,10,28), whose 55 sums are
1..45 and ten larger distinct values up to 91; n = 12, k = 47: (0,1,1)
(2,3,2) (4,5,3) (2,6,4) (7,8,5) (0,9,7) (1,10,9) (4,7,11) (5,11,12) (9,11,13)
(8,6,18). Refutations: the main engine refutes every k from C(n,2) down to
max_T k(T) + 1 (n = 11: 364 140 to 853 310 nodes per k, ≈ 1.5 s each;
n = 12: 3.05 M to 5.85 M nodes per k, ≈ 13 s each; `runs/`), and the
minimal second engine `code/plain_search.c` (weight-window recursion,
budget and repeat pruning only, no block bounds, parity or canonical forms)
reproduces every value for n ≤ 12 (at n = 12 it refutes k = 66..48 in 8.2 M to 9.65 M nodes each and finds the same witness at k = 47; `runs/run_plain_n12_distinct.txt`). The minimal engine also refutes the repeat-allowed k = 42 at n = 10 (43 182 621 nodes; `runs/run_plain_n10_k42.txt`), so a(10) = 41 is two-engine on both sides.
For n ≤ 7 both modes were also confirmed by brute force over every tree
shape and every weight vector within the edge-weight bound
(`code/brute_small.c`, 3 min).

The sequence 1, 3, 6, 9, 15, 20, 25, 30, 37, 45, 47 is not in OEIS (searched
today). Whether Varghese et al. or Lakshmanan–Eldho (Discrete Math. 2024)
tabulated the maximum over all trees of small order could not be checked
(both papers paywalled); the abstracts speak of families of trees and bounds.

## 7. Caveats

- The n = 11 refutations are single-engine exhaustive searches (one C
  program, run split into worker prefixes); the engine's soundness rests on
  Lemmas 1–6 above and on its exact agreement with (i) the published ladder
  n ≤ 10, (ii) a variant of itself that generates children by brute force
  instead of from the block candidate lists (identical node counts, e.g.
  3 247 390 at n = 10, k = 43), and (iii) the SAT engine where it was run.
  A second, independently written engine at n = 11 is the obvious next step.
- "a(11) ≥ 48" in OEIS is unattributed; the witness here is our own.
- Leech 1975 and Guy §C10 were not read; their content is taken from OEIS
  and from Ghodsi 2026 (secondary).

## References

- J. Leech, Another tree labelling problem, Amer. Math. Monthly 82 (1975)
  923–925 (secondary).
- H. Taylor, Odd path sums in an edge-labeled tree, Math. Mag. 50 (1977)
  258–259 (secondary, via Ghodsi).
- L. A. Székely, H. Wang, Y. Zhang, Some non-existence results on Leech
  trees, Bull. ICA 44 (2005) (secondary, via Ghodsi).
- W. C. Calhoun, K. Ferland, L. Lister, J. B. Polhill, Minimal distinct
  distance trees, JCMCC 61 (2007) 33–57 (secondary, via Ghodsi).
- M. Ghodsi, Nonexistence of a Leech tree of order 18: a computer-assisted
  proof, arXiv:2609.20492 (17 Sep 2026). Read in full today.
- OEIS A007187 (read today), A000055.
- R. K. Guy, Unsolved Problems in Number Theory, §C10 (secondary).
