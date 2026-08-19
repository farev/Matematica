# The plus-minus weighted Davenport constant of C5⊕C15 and C7⊕C21, with a certified table of dissociation numbers of small abelian groups

**Session date:** 2026-08-19. **Status of this note:** research artifact of a
one-day session; written with substantial AI assistance (Claude), disclosed
per repository policy. Every computational claim ships code in this
directory; every literature claim is marked **(secondary)** — the sandbox
that ran this session could not open any primary source (all egress blocked
except web-search snippets), so every citation below awaits primary-source
verification before any external use.

## Abstract

For a finite abelian group G, the plus-minus weighted Davenport constant
D±(G) is the least ℓ such that every sequence of ℓ elements of G has a
nonempty subsequence summing to zero after some choice of signs ±1.
Marchan, Ordaz and Schmid (Int. J. Number Theory 10 (2014) 1219–1239,
(secondary)) determined D±(G) for every abelian group of order ≤ 100 with a
single exception, C5⊕C15, where they showed D± ∈ {6, 7}. We decide it:

**D±(C5⊕C15) = 6** (lower bound PROVED; upper bound CERTIFIED by six
independent exhaustive computations across three distinct methods), and

**D±(C7⊕C21) = 8** (upper bound PROVED; lower bound CERTIFIED by an
explicit, from-definition-verified dissociated set), the first case of the
next open family per the same source.

Around the two decided cells we compute a certified table of D±(G) — equiv-
alently, of the maximum size dim±(G) of a *dissociated* subset of G — for
343 groups of rank ≤ 4, every value produced by an exhaustive search whose
node count equals the number of ±zero-sum-free multisets and is reproduced
exactly by an independent second implementation. The table exposes clean
structure: every group satisfies floor ≤ dim±(G) ≤ cap with
floor = max Σ⌊log₂ nᵢ⌋ over cyclic decompositions and cap = ⌊log₂|G|⌋; at
rank 2 every computed group sits at an endpoint of its (width ≤ 1) window,
while at rank 3 strictly intermediate values occur (dim±(C3⊕C3⊕C15) = 6
with floor 5, cap 7). C5⊕C15 (stuck at its floor) and C7⊕C21 (achieving its
cap) are extremal in opposite directions — both have shape 3p², and the
packing margin of the cap is *tighter* for 147 than for 75, so no counting
argument separates them; a complete reduction to a subset-sum statement
over F_p² (Lemma R) locates the difference and yields the sixth,
structurally different verification of the C5⊕C15 negative.

## 1. Definitions

Let G be a finite abelian group, written additively. A finite sequence over
G (repetition allowed, order irrelevant) is **±zero-sum-free (±zsf)** if no
nonempty subsequence admits signs ε_i ∈ {+1, −1} with Σ ε_i g_i = 0. Then

    D±(G) = 1 + maxlen±(G),

where maxlen±(G) is the maximum length of a ±zsf sequence: every sequence
of length maxlen±+1 has a signed zero-sum, and some sequence of length
maxlen± has none. This is the standard weighted Davenport constant for
weight set A = {+1, −1} (Marchan–Ordaz–Schmid, (secondary); introduced in
the context of norms of principal ideals in quadratic number fields, where
the weights arise from the Galois action, (secondary)).

A subset Λ ⊆ G is **dissociated** if no nontrivial {−1, 0, +1}-combination
of its elements vanishes. Write **dim±(G)** for the maximum size of a
dissociated subset ("dissociation number"). Dissociated sets are a standard
object of additive combinatorics and harmonic analysis (Rudin/Sidonicity
circle of ideas, (secondary)); we are not aware of a prior systematic exact
table of dim± over small groups, but the two literatures (weighted zero-sum
constants; dissociativity) overlap and a table could exist under either
name — this is flagged as the principal rediscovery risk in §7.

## 2. Basic lemmas

**Lemma 0 (sequences = sets).** maxlen±(G) = dim±(G).

*Proof.* A ±zsf sequence contains no element twice (signs (+1, −1) on the
two copies give 0), never {g, −g} (signs (+1, +1)), and not 0. So ±zsf
sequences are sets, and for sets the two conditions are verbatim identical.
∎

**Lemma 1 (normalization).** If (g_1, …, g_l) is ±zsf, so is
(σ_1 φ(g_1), …, σ_l φ(g_l)) for any signs σ_i ∈ {±1} and φ ∈ Aut(G). Hence
searches may restrict elements to one representative of each pair {g, −g}.

*Proof.* Signed zero-sums correspond bijectively (compose the weight vector
with σ and apply φ⁻¹). ∎

**Lemma 2 (distinct subset sums; the cap).** A set Λ is dissociated **iff**
all 2^|Λ| subset sums of Λ are pairwise distinct. Consequently

    dim±(G) ≤ ⌊log₂ |G|⌋   for every finite abelian G.

*Proof.* If Σ_A λ = Σ_B λ with A ≠ B, then Σ_{A∖B} λ − Σ_{B∖A} λ = 0 is a
nontrivial {−1,0,1}-combination (the two sets are disjoint, not both
empty). Conversely a vanishing combination with plus-part P and minus-part
N gives Σ_P = Σ_N with P ≠ N. The bound follows from injectivity of
A ↦ Σ_A λ into G. ∎

*Remark.* The plus-minus literature we could see states the general upper
bound D±(G) ≤ ⌊log₂|G|⌋ + 1 (secondary); the subset-sum argument above
needs no hypothesis on |G| (in particular no odd-order/invertibility-of-2
argument). Lemma 2 also says dim± is exactly the group analog of Erdős's
distinct-subset-sums problem (Erdős #1; cf. `conjectures/distinct-subset-
sums/` in this repository, where G = Z).

**Lemma 3 (concatenation; the floor).**
dim±(G ⊕ H) ≥ dim±(G) + dim±(H).

*Proof.* Place maximum dissociated sets on the two coordinates; a vanishing
combination projects to a vanishing combination in each factor. ∎

**Lemma 4 (cyclic groups).** dim±(C_n) = ⌊log₂ n⌋, i.e.
D±(C_n) = ⌊log₂ n⌋ + 1. ((secondary) — known; re-proved here for
self-containment.)

*Proof.* Upper bound: Lemma 2. Lower: {1, 2, 4, …, 2^{k−1}} with
k = ⌊log₂ n⌋ is dissociated in Z_n: a nontrivial {−1,0,1}-combination is a
nonzero integer of absolute value ≤ 2^k − 1 < n. ∎

**Proposition 5 (the window).** For any cyclic decomposition
G ≅ C_{n_1} ⊕ ⋯ ⊕ C_{n_r},

    floor(G) := max Σ_i ⌊log₂ n_i⌋  ≤  dim±(G)  ≤  ⌊log₂ |G|⌋ =: cap(G),

the maximum over all cyclic decompositions of G (equivalently, over all
partitions of the multiset of primary components into pairwise-coprime
cells, by CRT). In particular:

(a) every abelian 2-group is **forced**: floor = cap = log₂|G|, so
    dim± = log₂|G| exactly;
(b) C₂ ⊕ C_{2n} and C₂ ⊕ C₂ ⊕ C_{2n} are forced for every n — recovering
    the known value of D±(C₂⊕C_{2n}) ((secondary): the 2014 paper covers
    this family) with a two-line proof;
(c) for rank-2 groups, cap − floor ∈ {0, 1} when floor is computed from
    the invariant decomposition C_a⊕C_b (since
    ⌊x⌋+⌊y⌋ ≤ ⌊x+y⌋ ≤ ⌊x⌋+⌊y⌋+1); merging coprime factors can only
    increase the floor, so gap cells are those with
    {log₂ a} + {log₂ b} ≥ 1 under the best decomposition.

*Proof.* Lemmas 2–4 and CRT; (a) Σ a_i = log₂ |G| for invariant factors
2^{a_i}; (b) ⌊log₂ 2n⌋ + 1 = ⌊log₂ 4n⌋ and ⌊log₂ 2n⌋ + 2 = ⌊log₂ 8n⌋. ∎

**Lemma 6 (appending C₂).** dim±(G ⊕ C₂) ≥ dim±(G) + 1: append the
involution (0,1); a vanishing combination cannot use it (its C₂-coordinate
would be 1). The table shows the inequality is not always tight:
dim±(C5⊕C30) = 7 = dim±(C5⊕C15) + 2.

## 3. Main results

**Theorem 1.** D±(C5⊕C15) = 6, i.e. dim±(C5⊕C15) = 5.

*Lower bound (PROVED).* {(0,1), (0,2), (0,4), (1,0), (2,0)} ⊂ Z5×Z15 is
dissociated: Lemmas 3+4 (binary sets in the two factors), or directly by
the from-definition checker (`verify_witness.py`, 3⁵−1 = 242 signed
subsets).

*Upper bound (CERTIFIED).* No dissociated 6-subset exists. Six independent
exhaustive computations, three distinct methods:

| engine | method | search space | result |
|---|---|---|---|
| E1 (`dpm_search.c`) | DFS over sign-representative multisets, signed-sum-set state | 139,052 nodes = 1 + #±zsf multisets | maxlen 5; 85,155 maximum sets |
| E1 `--no-signred` | same DFS, all 74 nonzero elements (no Lemma-1 reduction) | 3,520,083 nodes | maxlen 5; per-size counts equal 2^l × sign-rep counts for every l (predicted identity, §5) |
| E2 (`dpm_python.py`) | independent Python implementation of the DFS | 139,052 nodes — **exact node-count match** | maxlen 5 |
| E4 (`enum_check.c`) | plain combinations of sign-reps, per-set 3^l check; no DFS, no shared state logic | C(37,6) = 2,324,784 sets | 0 dissociated; 85,155 at size 5 (**matches E1's census**) |
| E4 `--full` | combinations of all 74 nonzero elements | C(74,6) = 185,250,786 sets | 0 dissociated |
| E5 (`reduction_check.py`) | class-injectivity reduction over F₅² (Lemma R — different mathematics) | all 7 splits (a,b) | infeasible in every split |

**Theorem 2.** D±(C7⊕C21) = 8, i.e. dim±(C7⊕C21) = 7.

*Upper bound (PROVED).* Lemma 2: ⌊log₂ 147⌋ = 7.

*Lower bound (CERTIFIED).* The explicit set
{(0,1), (0,2), (1,1), (1,5), (2,1), (2,10), (3,19)} ⊂ Z7×Z21 is
dissociated — verified from the definition (3⁷−1 = 2,186 signed subsets,
`verify_witness.py`), and found independently by E1's exhaustive DFS
(16,528,742 nodes, node count reproduced exactly by E2) and by the
randomized hunter (366 restarts). C7⊕C21 has exactly 2,016 maximum
dissociated 7-sets up to sign normalization (258,048 = 2⁷ × 2,016 as raw
sets — the identity holds classwise, §5).

*Context ((secondary), from the vetting evidence in WRITEUP.md).* The 2014
paper determines every |G| ≤ 100; snippets of its PDF state C5⊕C15 is the
only unknown of order ≤ 100 ("either 6 or 7"). C7⊕C21 = 147 lies outside
that range; for the families C5⊕C_{5n} and C7⊕C_{7n} the value was reported
unknown "already for n = 3" — exactly the two cells decided here (n = 1, 2
are forced or inside the ≤ 100 determination). Theorem 1 lands **below**
the basic upper bound; per the snippet record, the known below-cap groups
were 3-groups and 5-groups, and 75 = 3·5² is assembled from exactly those
two primes. Theorem 2 lands **at** the cap. **Caveat (hard rule 3):** a
2021 PhD thesis (Perez-Lavin, U. Kentucky, (secondary)) computed D± for
many groups with 100 < |G| ≤ 200 "with some exceptions"; whether order 147
is among its values or its exceptions could not be determined from this
sandbox. Theorem 2's novelty is therefore provisional in a way Theorem 1's
is not. Both await the primary sources.

## 4. The table

`data/table.csv` (produced by `make_table.py` from `data/sweep/`): one row
per isomorphism type — 343 groups: all rank-2 groups of order ≤ 256, all
rank-3 groups C_a⊕C_b⊕C_c (a|b|c) of order ≤ 200, cyclic groups to 128
(controls for Lemma 4), C2⁴, C3⁴, and 20 targeted deeper cells (orders to
343). Columns: invariant factors, order, dim±, D±, floor, cap, verdict
(FORCED / FLOOR / CAP / MID), DFS node count, one maximum witness.

Summary (final numbers in the committed CSV):

- **No bound violation anywhere**; every cyclic value equals ⌊log₂ n⌋
  (Lemma 4), every 2-group sits at its forced value (Prop. 5a).
- **Rank-2 dichotomy (empirical).** Every rank-2 gap cell computed lands at
  an endpoint: FLOOR or CAP, never strictly between. The FLOOR (stuck)
  cells are rare: C3⊕C3 (9) and C5⊕C15 (75) are the only rank-2 examples
  in the sweep. Cap-achievers include 18, 36 (both structures), 45, 49,
  72 (both), 81 (C3⊕C27), 90, 98, 144 (all three structures), 147, 150,
  162, 169 (C13⊕C13), 180 (both), 189 (C3⊕C63), 196, …
- **Rank ≥ 3 has MID cells.** dim±(C3⊕C3⊕C15) = 6 with floor 5, cap 7.
  Stuck-at-floor rank-≥3 cells exist too (C3³, C3⁴, C3⊕C3⊕C9 — the last
  matching the published value 6 = 5+1 ((secondary), a below-cap value the
  2014 paper proved by a dedicated argument, reproduced exactly by our
  engines).
- **The two headline groups are extremal opposites.** 75 = 3·5² stuck at
  floor; 147 = 3·7² at cap — although 147's packing margin 147/128 ≈ 1.15
  is tighter than 75/64 ≈ 1.17, so no counting argument separates them.
- **Appending C₂ can add 2** (Lemma 6 is not tight): C5⊕C15 → C5⊕C30 goes
  5 → 7.

## 5. Verification methodology

Three invariants tie the engines together beyond value agreement:

1. **Node-count = census.** The DFS engines have no pruning beyond the
   legality test, so (#nodes − 1) equals the number of ±zsf multisets —
   compared **exactly** between C (E1) and Python (E2) on every cell both
   run (all |G| ≤ 100 in the committed cross-check log, plus both headline
   groups: 139,052 and 16,528,742).
2. **The 2^l identity.** For odd |G|, every dissociated l-set has 2^l
   sign-variants, all distinct as sets, exactly one of which is
   sign-normalized. So the reduction-free census must satisfy
   N_full(l) = 2^l · N_rep(l) for every l — verified classwise on both
   headline groups (all 6 classes at 75, all 8 at 147).
3. **Cross-method census agreement.** E4 (combinations + 3^l checks,
   no DFS) reproduces E1's count of maximum sets at 75 (85,155) and its
   zero at size 6, over both universes (sign-reps and all 74 elements).

Positive and negative controls: 15 cyclic groups against Lemma 4; 12 tiny
groups against the from-definition brute (E3, `dpm_brute.py --selftest`);
the witness checker rejects five planted non-dissociated sets
(`verify_witness.py --selftest`); the randomized hunter finds known
witnesses (75: instantly; 147: 366 restarts) and fails on the known-
impossible size-6 target at 75 (46M restarts, as expected); published
values reproduced: C2⊕C4 = 4, C3⊕C3 = 3, C3⊕C9 = 5, C3⊕C3⊕C9 = 6, the
C2⊕C2n family, 2-groups at cap, cyclic ⌊log₂n⌋+1 (all (secondary)).

## 6. Lemma R: reduction to F_p², and why counting cannot decide 75

**Lemma R.** Let G = Z_p² ⊕ Z₃ ≅ C_p ⊕ C_{3p} (p ≢ 0 mod 3 prime). After
sign normalization every element has Z₃-part 0 or 1. A size-s candidate
with parts S₀ (Z₃-part 0) and S₁ (Z₃-part 1), |S₁| = b, is dissociated
**iff** the s-tuple (h_i) of F_p²-parts has A ↦ Σ_{i∈A} h_i injective on
each class {A ⊆ [s] : |A ∩ S₁| ≡ r (mod 3)}, r = 0, 1, 2.

*Proof.* A signed combination with plus-part P and minus-part N (disjoint)
vanishes iff both coordinates vanish. The Z₃-coordinate is
|P∩S₁| − |N∩S₁| (mod 3), which vanishes iff P and N lie in a common class
(subtracting |P∩N∩S₁| = 0); the F_p²-coordinate vanishing is Σ_P h = Σ_N h.
Conversely any same-class collision Σ_A h = Σ_B h yields the vanishing
combination on (A∖B, B∖A). ∎

For s = 6, p = 5 the three classes have sizes 22/21/21 (b = 6) etc., all
≤ 25 = |F₅²| — **counting alone can never refute a size-6 set**; the
obstruction is genuinely structural. E5 checks all seven splits (a, b) by
direct enumeration over F₅²-tuples and finds every one infeasible —
a sixth verification of Theorem 1's upper bound through different
mathematics — while the analogous system for p = 7, s = 7 is feasible
(unit-tested on the Theorem 2 witness, which has b = 7). The p = 5 vs
p = 7 contrast is thus localized to a finite subset-sum statement over
F_p²; a human proof of the p = 5 infeasibility is the sharpest open thread
of this session.

## 7. Prior work and novelty (all (secondary) — snippet-level evidence only)

- Marchan–Ordaz–Schmid, *Remarks on the plus-minus weighted Davenport
  constant*, Int. J. Number Theory 10(5) (2014) 1219–1239
  (arXiv:1308.3316): the sandwich bounds; determination of all |G| ≤ 100
  except C5⊕C15 ∈ {6,7}; C2⊕C2n and further families; the
  "unknown already for n = 3" statement for C5⊕C5n and C7⊕C7n; the
  below-cap 3-group results incl. C3⊕C3⊕C9 = 6.
- Perez-Lavin, *The Plus-Minus Davenport Constant of Finite Abelian
  Groups*, PhD thesis, U. Kentucky 2021: state of the art "primarily known
  for rank ≤ 2 and |G| ≤ 100"; values for 100 < |G| ≤ 200 "with some
  exceptions" (coverage of specific cells not visible from here — the
  principal caveat on Theorem 2 and on our 100–200 table rows); fractional-
  part-of-log₂ lower-bound improvements; 2-groups attain the cap; 3-groups
  and 5-groups are the known non-attainers.
- Adhikari (survey chapter, Springer PROMS 221, 2017): plus-minus zero-sum
  constants survey — tables unchecked (unreachable).
- The B±(G) monoid line (arXiv:2404.17258; arXiv:2506.14279;
  Merito–Ordaz–Schmid 2025): arithmetic invariants of monoids of ±-weighted
  zero-sum sequences, which consume D± values.
- Dissociated sets: asymptotic/structural literature (Lev, *On the size of
  dissociated bases*, EJC 2011-ish; standard harmonic-analysis usage);
  no small-group exact tables surfaced in today's searches.
- The two computed constants were, per every snippet visible today, open:
  the ≤ 100 statement names 75 as the unique unknown; 147 sits outside
  every determination we could see, with the thesis caveat above.
- Novelty of the structural observations (floor/cap window as stated,
  rank-2 endpoint dichotomy, MID cells at rank 3, the C₂-append jump) is
  **unassessed against unreachable literature** — treat as new-to-us, not
  new, until the primary sources are read.

## 8. Open questions

1. **Human proof for 75** via Lemma R: show the seven F₅² class-injectivity
   systems are infeasible by hand (the b = 6 case is 6 distinct elements of
   F₅² with subset sums injective on |A| mod 3 classes; note the ν: x ↦ σ−x
   involution structure derived in WRITEUP.md).
2. **Rank-2 dichotomy.** Is dim±(C_a⊕C_b) ∈ {floor, cap} for every rank-2
   group? (True for all 100+ rank-2 groups computed today.) A
   characterization of the CAP/FLOOR split would decide infinitely many
   D± values at once; the data (only 9 and 75 stuck) suggests FLOOR is
   rare and tied to the primes 3 and 5.
3. **The C_n⊕C_n family.** A snippet (context unverified) suggests n = 23,
   46, 47 are the first undecided diagonal cases; C23⊕C23 (order 529,
   window {8, 9}) needs either a dissociated 9-set (decides at cap by
   Lemma 2 — our randomized hunter has not found one yet) or an exhaustive
   refutation (≈ 10¹¹–10¹² DFS nodes — days, not this session).
4. **How large can dim±(G⊕C₂) − dim±(G) be?** (≥ 2 happens: 75 → 150.)
5. The plus-minus Harborth constants g±(C3⊕C3n) appear uncomputed
   ((secondary), conference-abstract-level evidence only) and are within
   this engine family's reach with a fixed-length constraint added.

## 9. Reproducibility

Environment: 4-core sandbox, 15 GB RAM, Python 3.11.15, gcc -O2; no
floating point in any critical path; all runs single-machine. Every number
above is emitted by a committed script (§ headers name them); the sweep is
rerunnable cell-by-cell (`run_sweep.sh`, resumable, per-cell timeout
3600 s). Runtimes: C5⊕C15 exhaustive 0.02 s (E1) / 1.5 s (E2);
C7⊕C21 exhaustive ≈ 2 s (E1) / 35 s (E2); E1 no-signred at 147 ≈ 90 s;
E4 full-universe at 75 ≈ 186 s; E5 all splits ≈ 25 min; full sweep ≈ 2 h
of 3-worker wall time. Seeds: witness_hunt runs use --seed 42 (committed
outputs) and --seed 1 (controls); all other computations are
deterministic.
