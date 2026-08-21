# The plus–minus weighted Davenport constant of C₅⊕C₁₅ and C₇⊕C₂₁, and a census of maximal dissociated sets in abelian groups of order ≤ 255

**Session 2026-08-21.** AI-assisted (Claude); disclosed per repository
policy. All computations in this note are exact integer arithmetic; every
number has an emitting script in this directory.

## Abstract

For a finite abelian group `G`, the plus–minus weighted Davenport constant
`D±(G)` is the least `ℓ` such that every sequence of `ℓ` elements of `G`
admits a nonempty subsequence and signs `aᵢ ∈ {+1,−1}` with `Σ aᵢgᵢ = 0`.
Via the elementary equivalence *±-zero-sum-free ⟺ dissociated* (all `2^ℓ`
subset sums distinct), we determine by certified exhaustive search the two
smallest cases reported open in the literature around Marchan–Ordaz–Schmid
(2014): **`D±(C₅⊕C₁₅) = 6`** (the counting bound is *not* attained;
reportedly the last unresolved group of order ≤ 100) and
**`D±(C₇⊕C₂₁) = 8`** (the counting bound *is* attained). The extremal
structures could not differ more: `C₇⊕C₂₁` has exactly 2016 maximum
dissociated sets forming a *single* orbit under `Aut(G)` — the extremal
set is unique up to automorphism — while `C₅⊕C₁₅` has 85 155 maximum sets
in 193 orbits, none extendable. We then compute `D±(G)` for **all 493
abelian groups of order ≤ 255** (plus selected larger groups), apparently
the first such table: 484 of 493 attain the counting bound
`D± = ⌊log₂|G|⌋ + 1`, and the nine exceptions are catalogued exactly.
The exceptional set exhibits phenomena we did not find in the literature:
deficiency is not monotone in the packing density `2^ℓ/|G|`; there are
groups (`C₃³⊕C₅`, `C₂⊕C₃⁴`) where *neither* the product lower bound nor
the counting upper bound is tight; and mixing primes can strictly beat
every per-Sylow construction. As a corollary the family `D±(C_p⊕C_{3p})`
is settled for the primes `p ≤ 17`: it equals `⌊log₂ 3p²⌋ + 1` except at
exactly `p = 5`. Characterizing the deficient groups is proposed as an
open problem.

## 1. Definitions and the equivalence

Let `G` be a finite abelian group, written additively. A sequence
`S = (g₁,…,g_ℓ)` over `G` (repetition allowed) is **±-zero-sum free**
(±-zsf) if there is no nonempty `I ⊆ [ℓ]` and signs `aᵢ ∈ {+1,−1}` with
`Σ_{i∈I} aᵢgᵢ = 0`. Then `D±(G)` = least `ℓ` such that no ±-zsf sequence
of length `ℓ` exists (Marchan–Ordaz–Schmid, Int. J. Number Theory 10
(2014) 1219–1239; definition confirmed via search snippets, (secondary)).

A finite subset `S ⊆ G` is **dissociated** if its `2^{|S|}` subset sums
are pairwise distinct as indexed by subsets — equivalently, if no
nontrivial `{−1,0,+1}`-combination of distinct elements of `S` vanishes.
Write `ℓ_max(G)` for the maximum size of a dissociated subset of `G`.

**Lemma E (equivalence).** A sequence `S = (g₁,…,g_ℓ)` is ±-zsf iff its
`2^ℓ` subset sums `σ_I = Σ_{i∈I} gᵢ` are pairwise distinct. Consequently
a ±-zsf sequence has distinct, nonzero terms, contains at most one of
each pair `{g, −g}`, and
`D±(G) = ℓ_max(G) + 1`.

*Proof.* If `σ_A = σ_B` with `A ≠ B`, then
`Σ_{A∖B} gᵢ − Σ_{B∖A} gᵢ = 0` is a ±-weighted zero-sum on the nonempty
subsequence indexed by `A△B`. Conversely a ±-weighted zero-sum on
`I = P ⊎ N` (signs `+1` on `P`, `−1` on `N`) gives `σ_P = σ_N` with
`P ≠ N`. The consequences are immediate (a repeated term `g` gives
`g − g = 0`; a zero term is a zero-sum; `g` and `−g` give `g + (−g) = 0`;
and any sequence of length `ℓ_max + 1` fails, while a maximum dissociated
set is a ±-zsf sequence). ∎

Lemma E is elementary and dissociativity is a standard notion in additive
combinatorics; we claim no novelty for it and use it as the computational
lever. It is validated end-to-end in `dissoc.py controls`, which compares
maximum ±-zsf sequence length by the raw `{−1,0,+1}^ℓ` definition against
maximum dissociated set size on eight small groups (they agree).

**Proposition B (standard bounds).** For `G = ⊕ᵢ C_{nᵢ}`:

1. `ℓ_max(G) ≤ ⌊log₂|G|⌋` (the `2^ℓ` sums are distinct in `G`), so
   `D±(G) ≤ ⌊log₂|G|⌋ + 1`.
2. `ℓ_max(C_n) = ⌊log₂ n⌋`, witnessed by `{1, 2, 4, …, 2^{⌊log₂ n⌋−1}}`
   (subset sums are the integers `0 … 2^{⌊log₂ n⌋}−1 < n`).
3. If `S₁ ⊆ G`, `S₂ ⊆ H` are dissociated then
   `(S₁×0) ∪ (0×S₂) ⊆ G⊕H` is dissociated, so `ℓ_max` is superadditive
   over direct sums. Maximizing over regroupings of the prime-power
   factors into cyclic factors (distinct primes per factor) gives the
   **product lower bound** `LB(G)`.

Both bounds are classical in substance ((secondary) for their appearance
in the `D±` literature; proofs above are complete). We call `G`
**pinned** if `LB(G) = ⌊log₂|G|⌋` — then `ℓ_max` is determined — and
**deficient** if `ℓ_max(G) < ⌊log₂|G|⌋`.

Every abelian 2-group is pinned (`LB = Σeᵢ = log₂|G|`). Every cyclic
group is pinned.

**Theorem T3 (elementary p-groups, p = 2, 3).**
`ℓ_max(C₂^r) = ℓ_max(C₃^r) = r`, hence `D±(C₂^r) = D±(C₃^r) = r + 1`.

*Proof.* Over `F₂` and `F₃` the coefficient set `{−1,0,+1}` is the whole
prime field, so "no vanishing `{−1,0,+1}`-combination" is exactly linear
independence: `ℓ_max = r`, witnessed by a basis. ∎

(The values `D±(C₂^r) = r+1` — where `D± = D` — and `D±(C₃^r) = r+1` are
surely known, (secondary); the proof is included for self-containedness.)

## 2. The two reported-open constants

**Openness status (secondary, prominent caveat).** The primary sources
are egress-blocked from this sandbox. Two independent secondary snapshots
report the openness: a summary of Marchan–Ordaz–Schmid stating they
determined `D±` "for all groups up to order 100 (except one)", and a
snippet of the surrounding literature stating that for `D±(C₅⊕C_{5n})`
and `D±(C₇⊕C_{7n})` "the value is unknown already for n = 3" — i.e.
`C₅⊕C₁₅` (order 75, consistent with being the one exception ≤ 100) and
`C₇⊕C₂₁` (order 147). Searches for any later determination returned
nothing. **If either value is in fact in print, the contribution of this
section reduces to independent certification and the extremal-structure
results, and this note should be amended — that check requires primary
sources.**

Both groups sit in a window of width one:
`LB(C₅⊕C₁₅) = 5`, cap `⌊log₂ 75⌋ = 6`;
`LB(C₇⊕C₂₁) = 6`, cap `⌊log₂ 147⌋ = 7`.

**Theorem A (CERTIFIED). `D±(C₅⊕C₁₅) = 6`.**
No dissociated 6-set exists in `C₅⊕C₁₅`: the counting bound is not
attained, and the product construction
`{(0,1),(0,2),(0,4),(1,0),(2,0)}` (5 elements, verified ±-zsf by the raw
definition) is maximum. Verified three independent ways:

1. DFS exhaustion, Python engine (`dissoc.py 5 15`): 136 463 nodes.
2. DFS exhaustion, C engine (`./dissoc 5 15`): 136 463 nodes —
   node-for-node equality with (1); the isomorphic presentation
   `C₅⊕C₅⊕C₃` gives an independent traversal (136 421 nodes), same
   verdict.
3. Brute-force enumeration of all `C(37,6) = 2 324 784` six-subsets of
   the 37 ±-classes by a from-scratch verifier sharing no search logic
   (`verify_75.c`): zero dissociated 6-sets.

Additionally (4): all 85 155 dissociated 5-sets were enumerated and none
extends to a 6-set (`orbit_75.py`).

**Theorem B (CERTIFIED). `D±(C₇⊕C₂₁) = 8`,** and the extremal set is
unique up to automorphism. A dissociated 7-set attaining the counting
bound exists, e.g. (in `C₇×C₂₁` coordinates)

```
(0,1) (0,2) (1,1) (1,5) (2,1) (2,10) (3,19)
```

verified against the raw `{−1,0,+1}⁷` definition. Exhaustive enumeration
of all `C(73,7) = 1 629 348 612` seven-subsets of the 73 ±-classes
(`verify_147.c`, 1.63×10⁹ subsets) finds **exactly 2016** dissociated
7-sets; the orbit of the witness under
`Aut(G) = GL(2,7) × Aut(C₃)` (order 4032, acting with `−id` trivial on
±-classes) has exactly 2016 members, all dissociated (`orbit_147.py`).
Hence `Aut(G)` is transitive on maximum dissociated sets: **the packing
of 128 subset sums into 147 slots is unique up to symmetry.** The
independent descending-order DFS finds a witness in the same orbit.

**Contrast of extremal structures.** In `C₅⊕C₁₅` the maximum (5-)sets
are abundant and loose: 85 155 of them in **193** Aut-orbits (orbit sizes
15–480; the size-15 orbit is `{C₃-generator} ∪ S` with `S` a symmetric
dissociated 4-set in `C₅²`), and none extends. In `C₇⊕C₂₁` the maximum
(7-)sets are rigid: one orbit. Deficiency at 75 comes with abundance
below the cap; attainment at 147 comes with uniqueness at the cap.

## 3. The census to order 255

`census.py` computes `ℓ_max(G)` for every abelian group of order ≤ 255
(493 groups; the per-order group counts match the partition-product
formula). Methodology per group: **pinned** cells (447) are proved by
Proposition B and verified by *constructing* the product witness from an
optimal regrouping and checking it against the definition (an earlier
committed run additionally verified every pinned cell ≤ 255 by DFS
witness search; both runs are in git history); **Theorem T3** cells (4:
`C₃^r`, `r = 2..5`) are proved and search-verified for order ≤ 100 (and
`C₃⁵` by a separate full C-engine exhaustion: 131 590 491 nodes,
`run_243_verify.log`); **search** cells (42) are decided by the C
engine — a found witness settles attainment, a completed DFS exhaustion
settles deficiency (CERTIFIED). Cross-validation: the pure-Python engine
recomputed all 184 groups of order ≤ 100 with **exact node-count
equality** (`verify_census.py`). Canonical census runtime 40 s
(sequential, 1 core per group).

**Result (CERTIFIED / PROVED as marked): 484 of 493 groups attain the
counting bound** `D± = ⌊log₂|G|⌋ + 1`. The complete list of deficient
groups of order ≤ 255 (from `summarize.py`):

| order | group | LB | cap | ℓ_max | D± | label | note |
|---|---|---|---|---|---|---|---|
| 9 | C₃⊕C₃ | 2 | 3 | 2 | 3 | PROVED (T3) | |
| 27 | C₃³ | 3 | 4 | 3 | 4 | PROVED (T3) | |
| 75 | C₃⊕C₅⊕C₅ | 5 | 6 | 5 | **6** | CERTIFIED | Theorem A |
| 81 | C₃⁴ | 4 | 6 | 4 | 5 | PROVED (T3) | deficiency 2 |
| 81 | C₃⊕C₃⊕C₉ | 5 | 6 | 5 | 6 | CERTIFIED | |
| 135 | C₃³⊕C₅ | 5 | 7 | 6 | 7 | CERTIFIED | **neither bound tight** |
| 135 | C₃⊕C₅⊕C₉ | 6 | 7 | 6 | 7 | CERTIFIED | |
| 162 | C₂⊕C₃⁴ | 5 | 7 | 6 | 7 | CERTIFIED | **neither bound tight** |
| 243 | C₃⁵ | 5 | 7 | 5 | 6 | PROVED (T3) | deficiency 2 |

Beyond 255, decided the same way (CERTIFIED):

- `C₅⊕C₅₅` (order 275): **deficient**, `ℓ_max = 7 = LB` < cap 8, so
  `D± = 8`. Full exhaustion: 3 487 686 656 nodes, 25.6 min, 1 core.
- `C₇²⊕C₉` (order 441): **attains**, `ℓ_max = 8` = cap, so `D± = 9`
  (witness found after 740 741 480 nodes). With order 147 this is the
  second window the `C₇²` family wins, while the `C₅²` family loses
  both of its computed windows (75, 275).
- Orders 256–330 sweep and the remaining probes (`C₃⊕C₅³`, order 375;
  `C₁₉⊕C₅₇`, order 1083): see `census_256_330.csv` / `run_*.log` as
  committed, and the session log's Next section for anything still
  running at session end.

**Phenomena.** The deficient set resists the invariants we tried:

1. *Not a density threshold.* `C₃⊕C₅⊕C₉` (order 135) fails at packing
   density `2⁷/135 = 0.948`, while `C₇⊕C₂₁` attains at `2⁷/147 = 0.871`
   and `C₂⊕C₃⁴` fails at `2⁷/162 = 0.790`. Attainment is not monotone in
   `2^cap/|G|`.
2. *Neither bound need be tight.* For `C₃³⊕C₅`:
   `LB = 5 < ℓ_max = 6 < cap = 7`, witness
   `(0,0,0,1) (0,0,1,0) (0,1,0,1) (1,0,0,1) (1,1,0,4) (1,2,0,2)` —
   a genuinely mixed construction beating every product of cyclic
   constructions. Likewise `C₂⊕C₃⁴` with witness
   `(0,0,0,0,1) (0,0,0,1,0) (1,0,1,0,0) (1,1,0,0,0) (1,1,1,0,0)
   (1,1,2,0,0)`.
3. *Prime mixing beats Sylow sums.* `ℓ_max(C₇⊕C₂₁) = 7` while
   `ℓ_max(C₇⊕C₇) + ℓ_max(C₃) = 5 + 1 = 6`: the unique extremal 7-set
   projects onto the `C₃` factor with all seven elements (support
   `k = 7`), so no per-Sylow argument can reach it.
4. *Elementary-3 towers.* `C₃^r` has deficiency `⌊r log₂ 3⌋ − r → ∞`
   (PROVED, T3): deficiency is unbounded.

**Corollary F (the family `C_p⊕C_{3p}`).** Write `t = p/2^{⌊log₂ p⌋}`.
The sandwich pins `D±(C_p⊕C_{3p}) = ⌊log₂ 3p²⌋ + 1` unless
`t ∈ (2/√3, 4/3) ∪ (2√2/√3, 2)` (the *window primes*: 5, 7, 19, 29, 31,
37, 41, 53, 59, 61, …). Combining the pinned cases with Theorems A and B:
for `p ∈ {2, 3, 11, 13, 17}` (pinned) and `p = 7` (attains),
`D±(C_p⊕C_{3p}) = ⌊log₂ 3p²⌋ + 1`; for `p = 5` it is
`⌊log₂ 75⌋ = 6`, one below the counting bound. The family is thereby
determined for all `p ≤ 17`; the first open case is the window prime
`p = 19` (order 1083; a witness search is committed if it resolves in
session, else recorded open).

## 4. Open questions

**Q1 (characterization).** Which finite abelian groups are deficient,
i.e. have `D±(G) < ⌊log₂|G|⌋ + 1`? Equivalently: which `G` contain a
dissociated set of the maximum conceivable size `⌊log₂|G|⌋`? The census
gives the complete answer to order 255; no clean invariant explains it
(see Phenomena 1–3). Is the density of deficient groups (among all
abelian groups, ordered by size) zero?

**Q2 (windows).** In the two-parameter family `C_p⊕C_{qp}` (`q` an odd
prime), window cases computed so far split both ways
(`(p,q) = (5,3)` and `C₅²⊕C₁₁` deficient; `(7,3)` attaining). What
decides a window?

**Q3 (rigidity).** When the counting bound is attained with
`2^{ℓ} / |G|` close to 1, is the extremal set always unique up to
`Aut(G)` (as at order 147)? A second data point either way would be
informative — `C₁₉⊕C₅₇` (density `1024/1083 = 0.945`) is the natural
candidate. At `C₇²⊕C₉` (density `256/441 = 0.58`, so rigidity is not
expected) the found witness alone has an Aut-orbit of 1008 maximum sets
with a 6-element stabilizer (`orbit_441.py`); the full count was not
enumerated (the complete depth-8 tree walk is priced beyond this
session).

**Q4 (hand proof for 75).** The `C₃`-support analysis reduces
`ℓ_max(C₅⊕C₁₅) = 5` to four cases `k ∈ {3,4,5,6}` (`k` = number of
elements with nonzero `C₃`-component; `k ≤ 2` dies by counting
`2^{6−k}·A_t(k) ≤ 25` where `A_t(k) = #{T ⊆ [k] : |T| ≡ t (3)}`).
Each case is a statement about disjoint translates of subset-sum sets in
`C₅⊕C₅` with translation differences constrained to the zero-set of an
autocorrelation. A short human proof looks within reach and would
upgrade Theorem A to PROVED.

## 5. Reproduction

All scripts run from this directory; exact integer arithmetic
throughout; no randomness anywhere (no seeds needed). Hardware for the
quoted timings: 4-core sandbox, single-threaded runs.

```
python3 dissoc.py controls        # Lemma E validation + all controls (~2 s)
python3 dissoc.py 5 15            # Theorem A, Python engine (~1 s)
gcc -O2 -o dissoc dissoc.c && ./dissoc 5 15 && ./dissoc 7 21
gcc -O2 -o verify_75 verify_75.c && ./verify_75          # 0.13 s
gcc -O2 -DG147 -o verify_147 verify_75.c && ./verify_147 # verify_147.time
python3 orbit_147.py              # rigidity at 147 (~3 s)
python3 orbit_75.py               # 85155 sets, 193 orbits (~13 min)
python3 census.py 255             # full census (~1 min)
python3 verify_census.py 100      # two-engine cross-check (~8 s)
python3 summarize.py census.csv   # the table above
```

## 6. Provenance and honesty notes

- Primary sources unreachable (egress-blocked sandbox); **every
  citation is (secondary)** from search snippets dated 2026-08-21. The
  openness of the two headline values rests on the snapshots quoted in
  §2 and must be re-verified against Marchan–Ordaz–Schmid (2014), the
  CANT-II survey "Plus-Minus Weighted Zero-Sum Constants" (Springer,
  2017), and any citing work, from a machine that can read them.
- Lemma E, Proposition B and Theorem T3 are elementary; no novelty is
  claimed for them. The claimed-new content is: the two values (§2), the
  rigidity/abundance dichotomy (§2), the census (§3), Corollary F's
  synthesis, and the phenomena/questions (§3–4).
- The `2016 = |GL(2,7)|` coincidence in Theorem B is explained by the
  orbit computation itself (stabilizer of order 2 = ⟨−id⟩ inside the
  4032-element group), not assumed.
