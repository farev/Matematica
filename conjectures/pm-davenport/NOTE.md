# Plus–minus weighted Davenport constants: the last open group of order ≤ 100, and a census of maximum dissociated sets

**Session date.** 2026-08-25. Cloud sandbox, 4 cores, 15 GB RAM, Python
3.11.15, gcc; no network access to primary literature (WebSearch snippets
only — see §8).

**Abstract.** For a finite abelian group `G`, the plus–minus weighted
Davenport constant `D±(G)` is the least `ℓ` such that every sequence of
`ℓ` elements of `G` has a nonempty subsequence with a signed sum
(coefficients `±1`) equal to zero; equivalently, `D±(G) − 1 = μ(G)`, the
maximum size of a *dissociated* subset of `G`. Marchan, Ordaz and Schmid
(Int. J. Number Theory 10 (2014) 1219–1239) determined `D±(G)` for every
`|G| ≤ 100` with a single exception, `C₅ ⊕ C₁₅`, left as "either 6 or 7"
(secondary — see §8). We decide it: **`D±(C₅ ⊕ C₁₅) = 6`**, by exhaustive
search run in three independent implementations, two of which enumerate
the identical census of 85,155 maximum dissociated 5-subsets and the third
of which re-derives that census by unpruned brute force. We also determine
**`D±(C₇ ⊕ C₂₁) = 8`** — this group *attains* the pigeonhole upper bound
`⌊log₂|G|⌋ + 1` while `C₅ ⊕ C₁₅` does not — and compute `μ(G)` for every
abelian group of order ≤ 192 and for thirteen larger groups in the
families `C₃⊕C₃ₙ`, `C₅⊕C₅ₙ`, `C₇⊕C₇ₙ`, plus `C₇³`, `C₅²⊕C₁₅`, `C₁₃²`.
Attainment of the pigeonhole bound is the norm; the deficient groups in
range form a short, structured list. All extremal witnesses found for
gap-groups arise from a *checksum* mechanism which we isolate as a proved
construction lemma. AI assistance disclosure: this session was run with
substantial AI assistance (Claude); all proofs below are elementary and
self-contained.

---

## 1. Definitions and conventions

Let `G` be a finite abelian group, written additively. A *sequence* over
`G` is a finite multiset. A sequence `S = g₁ ⋯ g_ℓ` is **plus–minus
zero-sum-free** (pm-zsf) if there is no nonempty subsequence `T` and signs
`ε_g ∈ {+1, −1}` with `Σ_{g ∈ T} ε_g g = 0`.

* `D±(G)` := least `ℓ` such that no pm-zsf sequence of length `ℓ` exists
  (every length-`ℓ` sequence has a plus–minus zero-sum subsequence).
* `μ(G)` := maximum length of a pm-zsf sequence, so `D±(G) = μ(G) + 1`.

A set `S ⊆ G` is **dissociated** if the only `ε ∈ {−1, 0, 1}^S` with
`Σ_{g ∈ S} ε_g g = 0` is `ε = 0`. Marchan–Ordaz–Schmid note the identity
of pm-zsf sequences with dissociated sets (secondary, §8); Lemma 1 makes
it precise. Throughout, `t(G) := ⌊log₂ |G|⌋`.

For `G = C_{d₁} ⊕ ⋯ ⊕ C_{d_r}` we write elements as coordinate tuples.
The *class* of `g ≠ 0` is `{g, −g}`.

## 2. Elementary lemmas (all PROVED here, self-contained)

**Lemma 1 (normalization and dissociativity).**
(a) A pm-zsf sequence contains no zero, no repeated element, and never
both `g` and `−g`; hence it is a set meeting each class at most once.
(b) Replacing an element by its negative preserves the pm-zsf property.
(c) A set `S` is pm-zsf **iff** its `2^|S|` subset sums are pairwise
distinct **iff** `S` is dissociated. In particular `μ(G)` is the maximum
size of a dissociated subset of `G`.

*Proof.* (a) `0` alone is a zero-sum; `g, g` gives `g − g = 0`; `g, −g`
gives `g + (−g) = 0` (signs `+1, +1`). (b) Signs absorb the change.
(c) If `A ≠ B ⊆ S` have `σ(A) = σ(B)` (subset sums), then assigning `+1`
on `A ∖ B` and `−1` on `B ∖ A` gives a plus–minus zero-sum on the
nonempty `A △ B`. Conversely a signed zero-sum with support `T`, positive
part `A`, negative part `B` (disjoint, `A ∪ B = T ≠ ∅`) gives
`σ(A) = σ(B)` with `A ≠ B`. A `{−1,0,1}`-relation is precisely such a
signed zero-sum on its support. ∎

**Lemma 2 (extension rule; correctness of the search).** For a
dissociated set `C` and `g ∉ ±C ∪ {0}`, let
`A(C) = { Σ_{c ∈ C'} ε_c c : C' ⊆ C, ε ∈ {±1}^{C'} } ∪ {0}` (all signed
subset sums, a symmetric set). Then `C ∪ {g}` is dissociated **iff**
`g ∉ A(C)`, and `A(C ∪ {g}) = A(C) ∪ (A(C) + g) ∪ (A(C) − g)`.

*Proof.* A relation on `C ∪ {g}` not involving `g` is a relation on `C`.
One involving `g` with sign `ε` rewrites as `g = −ε·(signed sum over a
subset of C) ∈ A(C)` by symmetry of `A(C)`; note `0 ∈ A(C)` covers the
singleton relation `±g = 0`. The recursion for `A` is immediate. Since
dissociativity of a set does not depend on the order of its elements, a
depth-first search over sets of class representatives in a fixed index
order, pruned by this rule, visits exactly the dissociated class-rep
sets, each once; its maximum depth is `μ(G)`, and its node count is the
number of nonempty dissociated class-rep sets — an isomorphism invariant
used as a cross-check below. ∎

**Lemma 3 (the bracket).** For `G = C_{d₁} ⊕ ⋯ ⊕ C_{d_r}`:
`Σᵢ ⌊log₂ dᵢ⌋ ≤ μ(G) ≤ ⌊log₂ |G|⌋ = t(G)`.
Both inequalities are due to Adhikari–Grynkiewicz–Sun (secondary, §8);
proofs included for self-containment.

*Proof.* Upper: by Lemma 1(c) the `2^{μ}` subset sums of a maximum
dissociated set are distinct elements of `G`, so `2^μ ≤ |G|`. Lower: in
coordinate `i` take `Bᵢ = {2^j eᵢ : 0 ≤ j < ⌊log₂ dᵢ⌋}`. A signed
combination of distinct powers `2^j`, `j < s`, is a nonzero integer of
absolute value ≤ `2^s − 1` (the top power dominates the rest), and
`2^{⌊log₂ dᵢ⌋} − 1 < dᵢ`; so any `{−1,0,1}`-relation on `⋃ᵢ Bᵢ` has zero
coefficient block in every coordinate. ∎

**Lemma 3′ (superadditivity).** For any direct sum of finite abelian
groups, `μ(G₁ ⊕ G₂) ≥ μ(G₁) + μ(G₂)`.

*Proof.* Take dissociated `Sᵢ ⊆ Gᵢ` of maximum size and embed them in
the two summands. A `{−1,0,1}`-relation on `S₁ ∪ S₂` projects to a
relation on each `Sᵢ` because the sum is direct; both are trivial. ∎
(This subsumes the lower bound of Lemma 3 and can beat it: for
`C₃² ⊕ C₁₅` the invariant-factor concatenation gives 5, but the split
`C₃ ⊕ (C₃ ⊕ C₁₅)` gives `1 + 5 = 6`, which is sharp.)

**Lemma 4 (elementary 2- and 3-groups).** `μ(C_p^r) = r` for `p ∈ {2,3}`.

*Proof.* For `p = 3`: `{−1, 0, 1}` is all of `F₃`, so dissociated =
linearly independent over `F₃`; maximum size `r`, attained by a basis.
For `p = 2`: `±1 ≡ 1 (mod 2)`, so a `{−1,0,1}`-relation with support `U`
says `Σ_{g ∈ U} g = 0` over `F₂`, i.e. dissociated = `F₂`-independent. ∎

**Lemma 5 (checksum construction).** Let `m ≥ 2`, `H` a finite abelian
group, and `T = {h₁, …, h_k} ⊆ H` a set (any internal relations allowed)
such that every nonzero `ε ∈ {−1,0,1}^k` with `Σ εᵢ hᵢ = 0` has
sign-weight `w(ε) := Σᵢ εᵢ ≢ 0 (mod m)`. Then
`{(1, h₁), …, (1, h_k)} ⊆ C_m ⊕ H` is dissociated. Writing `ν_m(H)` for
the largest such `k`: `μ(C_m ⊕ H) ≥ ν_m(H) ≥ μ(H)`.

*Proof.* A relation `Σ εᵢ (1, hᵢ) = 0` reads `w(ε) ≡ 0 (mod m)` in the
first coordinate and `Σ εᵢ hᵢ = 0` in `H`; by hypothesis `ε = 0`. The
second inequality holds because a dissociated `T` has no relations at
all. ∎

**Lemma 6 (graded counting).** Let `S` be a dissociated subset of
`C₃ ⊕ H` with `3 ∤ |H|`. Sign-normalize so every element has
`C₃`-coordinate in `{0, 1}` (Lemma 1(b)), and let `k₁` be the number of
elements with coordinate 1, `k₀ = |S| − k₁`. Then for every
`c ∈ {0,1,2}`: `2^{k₀} · Σ_{j ≡ c (3)} C(k₁, j) ≤ |H|`.

*Proof.* By Lemma 1(c) the map `A ↦ σ(A)` is injective on subsets of `S`.
The `C₃`-coordinate of `σ(A)` is `|A ∩ S₁| mod 3`, so all subsets with
`|A ∩ S₁| ≡ c (mod 3)` map injectively into the coset `{c} × H`, of size
`|H|`. Their number is `2^{k₀} Σ_{j≡c} C(k₁, j)`. ∎

*Remark (near-miss).* For `G = C₅ ⊕ C₁₅ ≅ C₃ ⊕ C₅²` and `|S| = 6`,
Lemma 6 eliminates the profiles `k₁ ≤ 2` (counts 64, 32, 32 > 25) but
allows `k₁ ∈ {3,4,5,6}` (max class counts 24, 24, 22, 22 ≤ 25). The
refutation of those four profiles — hence Theorem 7 — is computational;
finding a conceptual proof of this one bit is open (§7).

## 3. Main computational results

**Theorem 7 (CERTIFIED).** `μ(C₅ ⊕ C₁₅) = 5`, i.e. **`D±(C₅ ⊕ C₁₅) = 6`**.

*Certificate.* Lower bound: the explicit dissociated set
`{(0,1), (0,2), (0,4), (1,0), (2,0)}` (the Lemma 3 concatenation), plus
85,154 others; each of the 85,155 verified by direct enumeration of all
signed combinations. Upper bound: exhaustive refutation — **no
dissociated 6-subset exists** — by three independent implementations:

| engine | method | result | agreement |
|---|---|---|---|
| A (`dpm.py`, Python) | class-set DFS with signed-sum-set pruning (Lemma 2) | μ = 5; 85,155 extremal 5-sets; 139,051 DFS nodes; 3.8 s | — |
| B (`dpm_fast.c`, C) | same spec, independent code: membership flags + append-log undo | μ = 5; 85,155; 139,051 nodes; < 0.1 s | matches A exactly |
| C (`refute_brute.c`, C) | **no pruning shared**: all C(37,6) = 2,324,784 class-rep 6-subsets × direct ternary enumeration | 0 dissociated 6-sets; positive control at size 5 finds exactly 85,155 | census matches A and B |

This closes the single case of order ≤ 100 left open by
Marchan–Ordaz–Schmid (secondary, §8), at the **lower** end of their
bracket {6, 7}: the pigeonhole bound `t + 1 = 7` is not attained.

**Theorem 8 (CERTIFIED; upper bound PROVED).** `μ(C₇ ⊕ C₂₁) = 7`, i.e.
**`D±(C₇ ⊕ C₂₁) = 8`**, attaining the pigeonhole bound
`⌊log₂ 147⌋ + 1 = 8`.

*Certificate.* Lower bound: the dissociated 7-set
`{(0,1), (0,2), (1,1), (1,5), (2,1), (2,10), (3,19)}`, verified by direct
enumeration of all `3⁷ − 1` signed combinations (`verify_witness.py`);
2,015 further witnesses exist (census below). Upper bound: Lemma 3
(`2⁸ = 256 > 147`) — **no search needed**. Engines A and B additionally
agree on the full census: 2,016 extremal 7-sets, 16,528,741 DFS nodes
(A: 973 s, B: ≈ 2 s). Under CRT, `C₇ ⊕ C₂₁ ≅ C₃ ⊕ C₇²`, and after
normalization every witness found is a checksum set (Lemma 5): its
`C₃`-coordinates are all nonzero. Hence `ν₃(C₇²) = 7` while
`μ(C₇²) = 5`.

**Theorem 8′ (CERTIFIED).** `μ(C₃ ⊕ C₄₅) = 6`, i.e.
**`D±(C₃ ⊕ C₄₅) = 7`** — again the concatenation value, refuting the
pigeonhole value 8; the extremal census has 3,391,470 six-sets. Evidence
tier for openness: **weaker than Theorem 7's** — one snippet synthesis
reports that MOS's `C₃ ⊕ C₃ₙ` theorem carries side conditions whose
"first value of n not covered is 15", i.e. exactly this group; that
reading rests on a single search result (secondary) and must be checked
against the paper before any claim of priority.

**Theorem 9 (CERTIFIED; census).** For every finite abelian group with
`|G| ≤ 192` — 336 groups — `μ(G)` equals `t(G) = ⌊log₂|G|⌋` **except**
for the deficient groups listed below; the concatenation lower bound of
Lemma 3 is met with equality in every deficient case in range.

| deficient `G` | `\|G\|` | `μ(G)` | `t(G)` | deficiency | `D±(G)` | extremal sets |
|---|---|---|---|---|---|---|
| `C₃²` | 9 | 2 | 3 | 1 | 3 | 6 |
| `C₃³` | 27 | 3 | 4 | 1 | 4 | 234 |
| `C₅ ⊕ C₁₅` | 75 | 5 | 6 | 1 | **6** | 85,155 |
| `C₃² ⊕ C₉` | 81 | 5 | 6 | 1 | 6 | 103,518 |
| `C₃⁴` | 81 | 4 | 6 | 2 | 5 | 63,180 |
| ⟨PENDING: any further deficient groups in 101–192⟩ | | | | | | |

Controls reproduced by the same engines (see `controls.py`,
`controls_output.txt`): the cyclic formula `μ(C_n) = ⌊log₂ n⌋` for all
`2 ≤ n ≤ 64` (Lemma 3 makes this proved, not just literature);
`μ(C₂^r) = r`, `μ(C₃^r) = r` (Lemma 4); the three exceptional values
published by MOS (`D± = 3, 4, 6` for `C₃², C₃³, C₃²⊕C₉` — secondary) and
a sample of their non-exceptional values. Note our census finds `C₃⁴`
(value 5) deficient as well; it is forced by Lemma 4 and was surely known
to MOS — the three-item exceptions list we quote is a snippet and may be
truncated (§8).

**Theorem 10 (CERTIFIED; beyond order 192).** ⟨PENDING: table of the
targeted larger groups — `C₇⊕C₂₈`, `C₇⊕C₃₅`, `C₇⊕C₄₂`, `C₇⊕C₄₉`,
`C₅⊕C₅₅`, `C₅⊕C₆₀`, `C₃⊕C₈₇`, `C₃⊕C₉₀`, `C₃⊕C₉₃`, `C₃⊕C₉₆`, `C₁₃²`,
`C₁₁⊕C₃₃`, `C₇³`, `C₅²⊕C₁₅` — with values, attainment, and witnesses.⟩

## 4. Structure of the extremal sets

**Theorem 11 (CERTIFIED; uniqueness for C₇⊕C₂₁).** Under
`C₇ ⊕ C₂₁ ≅ C₃ ⊕ C₇²`, all 2,016 maximum dissociated 7-sets have every
element with nonzero `C₃`-coordinate (after Lemma 1(b) normalization) —
i.e. **every** maximum dissociated set is a checksum set in the sense of
Lemma 5 — and they form a **single orbit** under
`Aut(G) = {±1} × GL(2,7)` (order 4,032; global negation acts trivially
on class-rep sets, and 2,016 = 4,032/2, so the action on extremal sets
is as free as possible). The maximum dissociated subset of `C₇ ⊕ C₂₁`
is therefore **unique up to automorphism**, with canonical
representative
`{(1;0,1), (1;0,3), (1;1,0), (1;1,1), (1;2,4), (1;3,0), (1;5,5)}`
(coordinates `(C₃; C₇, C₇)`). Computed by `orbit_analysis.py 7 7`, whose
census DFS (written independently of engines A/B, in CRT coordinates)
re-derives the count 2,016.

**C₅⊕C₁₅ profile census.** The orbit script's independent DFS in the
`C₃ ⊕ C₅²` presentation re-derives the extremal count 85,155 — a
*fourth* independent computation. Profiles (k₁ = number of elements with
nonzero `C₃`-part): k₁ = 1: 3,375; 2: 13,500; 3: 29,040; 4: 27,960;
5: 11,280. No extremal 5-set lies entirely in `{0} × C₅²` (consistent with
`μ(C₅²) = 4`); every profile `k₁ ∈ {1,…,5}` occurs, including 11,280
pure checksum sets (so `ν₃(C₅²) = 5`, contrasting `ν₃(C₇²) = 7`) — the
deficient group shows none of the rigidity of Theorem 11. **Aut-orbit
decomposition: 193 orbits** (167 free of size 480, 17 of size 240, 7 of
120, 1 of 60, 1 of 15; sizes sum to 85,155 exactly). The unique smallest
orbit — the most symmetric extremal set, stabilizer of order 64 — is
precisely the Lemma 3 concatenation construction
`{(0;0,1), (0;0,2), (0;1,0), (0;2,0), (1;0,0)}`. Rigidity at
attainment (one orbit), abundance at deficiency (193 orbits).

## 5. Reproduction

```bash
cd conjectures/pm-davenport
gcc -O2 -o dpm_fast dpm_fast.c && gcc -O2 -o refute_brute refute_brute.c
python3 dpm.py 5 15 --all          # Engine A, headline group
./dpm_fast 5 15                    # Engine B
./refute_brute 6 5 15              # Engine C refutation (≈ 7 s)
./refute_brute 5 5 15 | tail -1    # Engine C positive control (85,155)
python3 verify_witness.py "7,21" "(0,1) (0,2) (1,1) (1,5) (2,1) (2,10) (3,19)"
python3 controls.py                # full control battery
python3 sweep.py 192               # the census (≈ 20 min, sweep.csv)
python3 orbit_analysis.py 7 7      # structure of the C₇⊕C₂₁ extremals
```

Hardware for the recorded timings: 4-core cloud sandbox, 15 GB RAM,
Python 3.11.15, gcc -O2. All arithmetic exact (machine integers well
below overflow: sums of ≤ 8 coordinates each < 2¹⁶); no floating point in
any critical path; deterministic, no seeds.

## 6. Conjectures from the data

**Conjecture A (split dichotomy).** For every finite abelian `G`,
either `μ(G) = t(G) = ⌊log₂|G|⌋` (attainment) or
`μ(G) = max { μ(G₁) + μ(G₂) : G = G₁ ⊕ G₂ a proper direct
decomposition }` (split-sharpness). Since every direct decomposition of
a finite abelian group comes from partitioning its primary cyclic
factors (Krull–Schmidt), this is checkable from the census:
`dichotomy_check.py` verifies it for **every** group in the ≤ 192 census
⟨PENDING: final run output; the seven deficient groups known so far all
satisfy it, `C₃²⊕C₁₅` — where μ = 6 lies strictly between the
invariant-factor concatenation bound 5 and t = 7 — only via the
non-invariant split `C₃ ⊕ (C₃⊕C₁₅)`⟩. Informally: below full
pigeonhole packing, no mechanism beats gluing optimal pieces.

**Conjecture B (families).** `D±(C₃ ⊕ C₃ₙ) = ⌊log₂ 9n⌋ + 1` for all
`n ≥ 2` ⟨PENDING: confirm against the n ≤ 32 data⟩; `D±(C₅ ⊕ C₅ₙ) =
⌊log₂ 25n⌋ + 1` for all `n ≥ 4` with the single exception n = 3;
`D±(C₇ ⊕ C₇ₙ) = ⌊log₂ 49n⌋ + 1` for all `n ≥ 1` in the computed range.

## 7. Open questions

1. A conceptual (non-computational) proof that `C₅ ⊕ C₁₅` has no
   dissociated 6-set; Lemma 6 leaves exactly the profiles
   `k₁ ∈ {3,4,5,6}`.
2. A formula for `ν_m(C_p²)` (Lemma 5): the computed values
   `ν₃(C₅²) = 5 < 6 ≤ W-bound` and `ν₃(C₇²) = 7 = W-bound` ask which of
   the two the truth follows in general.
3. `μ(C₇³)` and the behaviour at gap 2 ⟨PENDING: may be resolved by the
   queued run⟩.
4. Structure: are the extremal sets of the attaining rank-2 groups
   `C_p ⊕ C_{3p}` always a single `Aut`-orbit?

## 8. Sources and caveats (claim discipline)

**Network state.** WebFetch to arxiv.org / oeis.org / journal hosts was
egress-blocked throughout the session; **every citation below is
(secondary)**, reconstructed from WebSearch snippets dated 2026-08-25,
and must be verified against the actual papers before any public claim
of novelty. Specific pre-publication checks required:

1. Marchan, Ordaz, Schmid, *Remarks on the plus-minus weighted Davenport
   constant*, Int. J. Number Theory 10 (2014) 1219–1239 = arXiv:1308.3316
   (open access; also HAL hal-00835688). Verify: (a) that `C₅ ⊕ C₁₅` is
   indeed their single undetermined group of order ≤ 100 with bracket
   {6,7} (three independent snippet syntheses agree on this reading);
   (b) their exceptions list (our census says it must include `C₃⁴ → 5`);
   (c) their `C₃ ⊕ C₃ₙ` side conditions — one snippet says the first `n`
   not covered is 15, i.e. `C₃ ⊕ C₄₅` ⟨PENDING: our value for it⟩;
   (d) whether Lemma 5 (checksum) appears there as their lower-bound
   technique — their abstract says the paper's contributions are "mainly
   lower bounds", so **Lemma 5 may well be known**; we claim only the
   computations as new.
2. Adhikari–Grynkiewicz–Sun, *On weighted zero-sum sequences*, Adv. Appl.
   Math. 48 (2012) 506–527 (arXiv:1003.2186): the Lemma 3 bracket
   attribution (quoted via INTEGERS 22 (2022) #A36 snippet).
3. `D±(C_n) = ⌊log₂ n⌋ + 1` attributed to Adhikari et al. (~2006)
   (INTEGERS #A36 and Perez-Lavin thesis snippets).
4. The 2017 survey (Springer PROMS 221, DOI 10.1007/978-3-319-68376-8_1)
   and the 2023–2025 monoid papers (arXiv:2304.14777, 2404.17258,
   2506.14279 — Merito–Ordaz–Schmid, June 2025): confirm none contains
   these values (checked by snippet only; the June 2025 paper is the
   closest active work).
5. MathSciNet / zbMATH have not been searched at all (no access).

If (1a) fails — i.e. the actual paper determines `C₅ ⊕ C₁₅` — then
Theorem 7 becomes an independent verification and this note's headline
must be downgraded accordingly; the same applies to Theorem 8 should any
source be found for it.

**AI assistance.** This session was run with substantial AI assistance
(Claude), per repository policy. AI systems are not authors.
