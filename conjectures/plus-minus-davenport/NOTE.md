# The plus–minus weighted Davenport constants of C₅⊕C₁₅ and C₇⊕C₂₁, and the complete table for all abelian groups of order ≤ 162

*Research note, 2026-08-22 session. AI-assisted (Claude); disclosed per
repository policy. All literature citations in this note are* (secondary)*:
the session's sandbox could not fetch any primary source (arXiv, HAL,
publisher pages all egress-blocked), so every statement about the
literature comes from search-result snippets retrieved 2026-08-22 and must
be re-verified against the papers before any external use.*

## Abstract

For a finite abelian group `G`, the plus–minus weighted Davenport constant
`D±(G)` is the least `ℓ` such that every sequence of `ℓ` elements of `G`
has a nonempty subsequence summing to zero with signs `±1`. Marchan, Ordaz
and Schmid (IJNT 2014) determined `D±(G)` for every `|G| ≤ 100` except one:
`C₅ ⊕ C₁₅`, which they bracketed to `{6, 7}` (secondary). We decide it:

**`D±(C₅ ⊕ C₁₅) = 6`** — the *lower* end of the bracket, and the unique
group of order ≤ 100 outside the elementary-3-group family whose constant
falls below the binary upper bound `⌊log₂|G|⌋ + 1`.

We also determine **`D±(C₇ ⊕ C₂₁) = 8`** — the *upper* end of its bracket
`{7, 8}` — for the second family (`C₇ ⊕ C₇ₙ`) whose `n = 3` member the same
paper flagged as unknown (secondary); we found no published value for this
group at all. Both are exhaustive, cross-verified computations
(**CERTIFIED**): four independent verification paths for `C₅ ⊕ C₁₅`, three
for `C₇ ⊕ C₂₁`, including definition-level maximality certificates for
every extremal set.

The inverse problems are solved as well: `C₅ ⊕ C₁₅` has exactly **85,155**
±zero-sum-free sets of maximal length 5 in **193 orbits** under
`Aut(G)`, while `C₇ ⊕ C₂₁` has exactly **2016 = |GL(2,7)|** extremal
7-sets forming a **single orbit** — its extremal sequence is unique up to
automorphisms and signs, and every element of it has nonzero `C₃`-part.

Finally we compute `D±(G)` from the definition for **every abelian group
of order ≤ 162** — 312 groups. The 184 of order ≤ 100 agree with every
published value and bound we could extract from snippets (the
Marchan–Ordaz–Schmid Theorem 3.1 bounds, their exception list, their
`C₃ ⊕ C₃ₙ` family values); the 15 cells past 100 where the bounds leave a
gap appear to be new. Among them: **`D±(C₃² ⊕ C₁₅) = 7` (order 135) and
`D±(C₃³ ⊕ C₆) = 7` (order 162) lie strictly between their Theorem 3.1
bounds `{6, 8}`** — the constant is not always at an endpoint — and
`D±(C₃ ⊕ C₄₅) = 7` attains the *lower* bound in a family that hits the
upper bound at every other gap cell in range. The five groups of order
≤ 100 strictly below the binary bound (`C₃²`, `C₃³`, `C₃⁴`, `C₃² ⊕ C₉`,
`C₅ ⊕ C₁₅`) all attain the lower bound exactly.

## 1. Definitions and background

A *sequence* over `G` is a finite multiset of elements. `S = g₁ ⋯ g_k` is
**±zero-sum-free** (here: *free*) if there is no nonempty `I ⊆ {1..k}` and
signs `ε_i ∈ {+1, −1}` with `Σ_{i∈I} ε_i g_i = 0`. Then

```
D±(G) = 1 + L(G),   L(G) = max length of a free sequence over G.
```

Known results used as controls (all (secondary), from snippets of:
Adhikari–Rath, Integers 6 (2006) #A30; Marchan–Ordaz–Schmid ["MOS"],
IJNT 10 (2014) 1219–1239 = arXiv:1308.3316; Marchan–Ordaz–Santos–Schmid,
JCTA 133 (2015) = arXiv:1407.1966; Perez-Lavin, PhD thesis, U. Kentucky
2021):

- `D±(C_n) = ⌊log₂ n⌋ + 1` (Adhikari–Rath).
- **MOS Theorem 3.1**: for `G ≅ C_{n₁} ⊕ ⋯ ⊕ C_{n_r}` with `n_i | n_{i+1}`,
  `Σ_i ⌊log₂ n_i⌋ + 1 ≤ D±(G) ≤ ⌊log₂ |G|⌋ + 1`.
- MOS, blanket claim as rendered by the search engine: for `|G| ≤ 100`,
  `D±(G) = ⌊log₂|G|⌋ + 1` except `C₃² → 3`, `C₃³ → 4`, `C₃² ⊕ C₉ → 6`, and
  `C₅ ⊕ C₁₅ ∈ {6, 7}` unknown. (Our table shows `C₃⁴ → 5` also lies below
  the binary bound; its absence from the rendered list is presumably a
  snippet truncation — the value `r + 1` for `C₃^r` is forced by Lemma 2
  below, so there is no conflict.)
- The bracket sentence, near-verbatim from two independent queries: *"The
  only group of cardinality at most 100 where the value of the plus-minus
  weighted Davenport constant remains unknown is C₅ ⊕ C₁₅ … the value is
  either 6 or 7."* Provenance: MOS 2014 itself; restated in the 2021
  Perez-Lavin thesis. Eleven targeted searches on 2026-08-22 found no
  later resolution, and no `D±` value for `C₇ ⊕ C₂₁` anywhere.

## 2. Structure lemmas

**Lemma 1 (class model).** *A free sequence has pairwise distinct elements,
none zero, and contains at most one element of each sign class
`{g, −g}`. Replacing an element by its negative preserves freeness. Hence
free sequences of length `k` correspond exactly to free `k`-subsets of the
sign classes, and* `L(G)` *is the maximum size of a free set of class
representatives.*

*Proof.* `g` repeated gives `g − g = 0`; `g` and `−g` together give
`g + (−g) = 0`; `0` alone is a zero subsum. Negating one element induces a
bijection on signed subset sums (flip that coefficient), so freeness is
preserved; pick the representative of each class. ∎

**Lemma 2 (elementary 2- and 3-groups).** *For `p ∈ {2, 3}`,
`L(C_p^r) = r`, so `D±(C_p^r) = r + 1`.*

*Proof.* For `p ∈ {2, 3}` the coefficient set `{−1, 0, +1}` reduced mod `p`
is all of `F_p`. So a signed zero subsum is exactly a nontrivial linear
dependence over `F_p`, and free sets are exactly linearly independent
subsets of `F_p^r`. ∎ (Surely classical; stated for self-containment.
Consistent with the values credited to MOS/JCTA-2015 in snippets.)

**Lemma 3 (product bound).** *`L(G ⊕ H) ≥ L(G) + L(H)`.*

*Proof.* Concatenate free sequences supported on `G ⊕ 0` and `0 ⊕ H`; a
signed zero subsum projects to a signed zero subsum in each component, so
both parts must be empty. ∎ (This is the lower half of MOS Theorem 3.1
applied inductively; included for completeness.)

**Lemma 3b (binary upper bound).** *`D±(G) ≤ ⌊log₂|G|⌋ + 1`, i.e.
`L(G) ≤ ⌊log₂|G|⌋`.*

*Proof.* If `ℓ > ⌊log₂|G|⌋` then `2^ℓ > |G|`, so two distinct `{0,1}`-
subset sums of any `ℓ` elements coincide; the symmetric difference of the
two subsets, signed `+1`/`−1`, is a nonempty signed zero subsum. ∎
(The upper half of MOS Theorem 3.1; the pigeonhole proof is standard.)

**Lemma 3c (cyclic groups).** *`L(C_n) = ⌊log₂ n⌋`, so
`D±(C_n) = ⌊log₂ n⌋ + 1` (Adhikari–Rath (secondary); in-house proof).*

*Proof.* `{1, 2, 4, …, 2^{k−1}}` with `2^k ≤ n` is free: a signed sum of
distinct powers of two is a nonzero integer of absolute value `< 2^k ≤ n`,
hence nonzero mod `n`. Lemma 3b gives the matching upper bound. ∎

Lemmas 3, 3b, 3c make every cell of the table where the two Theorem 3.1
bounds coincide **PROVED in-house** — engine runs there are confirmations,
not the source of truth. In particular the two sweep cells whose census
timed out (`C₂⁵ ⊕ C₄` at order 128 and `C₂⁵ ⊕ C₅` at order 160, both
1800 s) have `D± = 8` proved outright: product lower `5·1 + 2 + 1 = 8`
(resp. `4·1 + 3 + 1 = 8`) meets the pigeonhole upper `⌊log₂128⌋ + 1 = 8`
(resp. `⌊log₂160⌋ + 1 = 8`).

**Lemma 4 (reduction over `G = V ⊕ Z₃`, `V = F₅²`).** *Sign-normalize a
free set `S` so every element has `Z₃`-part `t ∈ {0, 1}` (Lemma 1); write
`S = S₀ ⊔ S₁` by `t`-part, with `V`-parts `u` (for `S₀`) and `v_i` (for
`S₁`). All `v_i` are distinct, and `S` is free iff*

1. *`S₀` is a free subset of `V ∖ {0}`, and*
2. *for every nonempty signed subset of `S₁` with `#(+) ≡ #(−) (mod 3)`
   ("balanced"), its `V`-part `w` satisfies `w ∉ {0} ∪ Reach(S₀)`,*

*where `Reach(S₀)` is the set of all nonempty signed subset sums of `S₀`.*

*Proof.* If two normalized elements of `S₁` shared a `V`-part they would be
equal (same `t = 1`), and an element pair normalizing to the same value
came from a `±` pair, excluded by freeness. A zero signed subsum uses a
signed subset `I₀ ⊆ S₀` and `I₁ ⊆ S₁`; its `Z₃`-part is `#(+) − #(−)` over
`I₁`, which must vanish mod 3, i.e. `I₁` balanced (possibly empty). If
`I₁ = ∅` the relation lives in `S₀` (condition 1). If `I₁ ≠ ∅` with
`V`-part `w`, a completing `I₀` exists iff `w ∈ {0} ∪ (−Reach(S₀))`, and
`Reach` is `±`-symmetric. ∎

**Lemma 5 (saturation).** *Every maximal-size free subset `S₀` (size
`L(V)`) of a finite abelian `V` has `Reach(S₀) = V ∖ {0}`.*

*Proof.* Freeness of `S₀ ∪ {v}` for `v ∉ ±S₀` is exactly `v ∉ Reach(S₀)`
(a relation involving `v` uses it once, with sign). If some nonzero
`v ∉ Reach(S₀)` then (noting `±S₀ ⊆ Reach(S₀)`) the set `S₀ ∪ {v}` is free
and larger — contradiction. ∎

**Corollary 6 (case (4,2) of Theorem 7, by hand).** In `G = F₅² ⊕ Z₃`, a
free 6-set with `|S₀| = 4, |S₁| = 2` is impossible: `L(F₅²) = 4` (CERTIFIED
below; also (secondary) via `D±(C₅²) = 5` in the MOS ≤100 table), so `S₀`
is maximal in `V`, `Reach(S₀) = V∖{0}` by Lemma 5, and the balanced pair
difference `w = v_x − v_y ≠ 0` has nowhere to live. ∎

**Remark (pigeonhole for case (0,6)).** For `|S₁| = 6` the balanced
patterns include all `(2,2)` quadruples, so the six `V`-parts would need
all disjoint-support pair differences distinct — a Sidon-type condition.
Six points in `F₅²` have `15` unordered pair-difference classes among only
`12` available, forcing at least three coincidences; coincidences with
disjoint support kill the set directly, but shared-index coincidences
(`2x = y + z`, 3-term progressions) are not `±`-expressible, so pigeonhole
alone does not finish this case. The machine audit below shows every
configuration in fact violates ≥ 2 constraints. A fully hand-written proof
of Theorem 7 remains open.

**Remark (missing-set data for cases (3,3) and (2,4)).** Writing
`M(S₀) = V ∖ ({0} ∪ Reach(S₀))` in sign classes: over all 180 free 3-sets
of `F₅²`, `|M| = 2` for 120 of them and `|M| = 5` for 60; over all 66 free
2-sets, `|M| = 8` for 60 and `|M| = 10` for 6. For the 120 sets with
`|M| = 2`, case `(3,3)` dies by counting alone (the four derived classes
`v_x − v_y, v_x − v_z, v_y − v_z, v_x + v_y + v_z` cannot fit, and their
coincidences are either fatal `±`-relations or 3-AP degeneracies handled
directly); the 60 sets with `|M| = 5` need the structure of `M`, and case
`(2,4)` (13 derived values into ≤ 10 classes, some coincidences legal)
likewise — both closed here only by the audit.

## 3. The two determinations

**Theorem 7 (CERTIFIED).** `D±(C₅ ⊕ C₁₅) = 6`.

The lower bound is Lemma 3 with `L(C₅) = 2`, `L(C₁₅) = 3` (or MOS Thm 3.1:
`⌊log₂5⌋ + ⌊log₂15⌋ + 1 = 6`); the witness
`(1,0) (2,0) (0,1) (0,2) (0,4)` is verified by `verify_witness.py`
(all `3⁵ − 1 = 242` signed sums nonzero). The upper bound — **no free
6-set** — was established four independent ways:

| # | method | result |
|---|---|---|
| V1 | `dpm.c` census DFS over 37 sign classes | free-set counts `k = 1..5`: **37, 666, 7338, 45855, 85155**; zero at `k = 6`; 792,672 nodes, 0.098 s |
| V2 | `dpm.c --raw`: DFS over raw element multisets (74 elements, repetitions allowed, no class model) | max length 5; counts `74, 2664, 58704, 733680, 2724960` — exactly `2^k ×` V1 as Lemma 1 predicts; 46.7M nodes, 4.39 s |
| V3 | `dpm_indep.py`: clean-room Python engine (tuple arithmetic, immutable reach sets) | reproduces the V1 census digit for digit |
| V4 | `case_audit.py`: enumeration in the `F₅² ⊕ Z₃` decomposition via Lemma 4, no shared code with V1–V3 | all five cases `(|S₀|,|S₁|) = (4,2)…(0,6)` empty; every candidate configuration violates ≥ 2 constraints |

plus the definition-level **maximality certificate**
(`verify_maximality.py`): each of the 85,155 sets from the `--enum 5` run
is free (brute-force `3⁵−1` sums) and extends by no class
(`MAXIMALITY PASS`). The count 85,155 is confirmed by V1 = V2/2⁵ = V3.

**Theorem 8 (CERTIFIED).** `D±(C₇ ⊕ C₂₁) = 8`.

Bracket `{7, 8}` from MOS Thm 3.1 (`2 + 4 + 1 = 7 ≤ D± ≤ ⌊log₂147⌋ + 1 =
8`) (secondary). Verification:

| # | method | result |
|---|---|---|
| V1 | `dpm.c` census over 73 classes | counts `k = 1..7`: **73, 2628, 60468, 914526, 7151382, 8397648, 2016**; zero at `k = 8`; 166.8M nodes, 33.7 s |
| V2 | `dpm.c --raw` over 146 raw elements (multisets, repetitions allowed, no class model) | max length 7; **all seven counts equal `2^k ×` V1 exactly** (146, 10512, 483744, 14632416, 228844224, 537449472, 258048); 17,204,330,175 nodes, 2725.7 s |
| V3 | `verify_maximality.py` on all 2016 extremal sets | each free (`3⁷−1 = 2186` sums) and non-extendable by any of the 73 classes: `MAXIMALITY PASS` |
| V4 | `dpm_indep.py`: clean-room Python census (≈ 1.7 h) | reproduces the V1 census digit for digit, same maximum and witness orbit |

A free 7-witness, hand-checkable:
`(0,1) (1,1) (2,1) (0,2) (4,2) (1,5) (2,10)` — verified by
`verify_witness.py`.

**Corollary 9.** In MOS's flagged families the two ends of Theorem 3.1 are
both attained at `n = 3`: `D±(C₅ ⊕ C₁₅)` equals the *lower* bound,
`D±(C₇ ⊕ C₂₁)` the *upper*.

## 4. Inverse theorems (extremal structure)

**Theorem 10 (CERTIFIED).** *The 2016 free 7-sets of `C₇ ⊕ C₂₁` form a
single orbit under `Aut(G) ≅ GL(2,7) × Aut(C₃)`: the extremal sequence is
unique up to automorphism and signs. Every element of every extremal set
has nonzero `C₃`-component. The effective stabilizer is trivial: the orbit
size equals `|GL(2,7)| = 2016`, the order of `Aut(G)/{±1}` (global `−1`
acts trivially on sign classes).*

Representative (in `(a, b) ∈ Z₇ × Z₂₁` coordinates):
`(0,1) (0,2) (1,1) (1,5) (2,1) (2,10) (3,19)`.

**Theorem 11 (CERTIFIED).** *The 85,155 free 5-sets of `C₅ ⊕ C₁₅` fall
into exactly 193 orbits under `Aut(G) ≅ GL(2,5) × Aut(C₃)` (order 960,
effective 480): 167 regular orbits of size 480, 17 of size 240, 7 of size
120, one of size 60 and one of size 15. None avoids the `C₃`-part: the
number of elements with nonzero `C₃`-component ranges over `{1,…,5}` with
distribution `3375 / 13500 / 29040 / 27960 / 11280`. Exactly 23 sets are
supported on the two visible cyclic factors `(C₅ × 0) ∪ (0 × C₁₅)`.*

(Both computed by `classify_extremal.py`; the orbit closure check — every
automorphism image of an enumerated set is again an enumerated set — is a
further consistency test of the censuses, and it passed.)

## 5. The complete table to 162, and two strictly intermediate values

`sweep.py` ran `dpm` on **every** abelian group of order 2–162: 312
groups, of which 309 were engine-censused, one (`C₂⁷`) recorded by
Lemma 2, and two (`C₂⁵⊕C₄`, `C₂⁵⊕C₅`) timed out at 1800 s but are PROVED
`= 8` by Lemmas 3 + 3b (coinciding bounds), so the table is complete.
Engine time ≈ 91 min total across the three sweeps (plus the two timeout
burns), dominated by the order-128 and order-160 2-groups. Full data:
`table_002_100.csv`, `table_101_150.csv`, `table_151_162.csv`; analysis
transcript: `analysis_2_162.txt`.

**Concordance (orders ≤ 100, 184 groups):** every value consistent with
MOS Theorem 3.1 (neither bound ever violated anywhere in the table), with
the blanket `⌊log₂|G|⌋ + 1` claim and its exception list, and with the
`C₃ ⊕ C₃ₙ` family equalling the upper bound for all `2 ≤ n ≤ 11` in that
range (secondary sources as in §1). A further control found after the
fact: 111 sweep rows are coprime products of prime-power cyclics (hence
cyclic in disguise, e.g. `C₅⊕C₂₇ ≅ C₁₃₅`); all 111 match `⌊log₂n⌋ + 1`.

**Theorem 12 (CERTIFIED).** `D±(C₃² ⊕ C₁₅) = 7` (order 135) and
`D±(C₃³ ⊕ C₆) = 7` (order 162), while their Theorem 3.1 brackets are both
`{6, 8}`: **the plus–minus Davenport constant can lie strictly between
the MOS bounds**, and these are the only two such groups of order ≤ 162.
Verification for both: census + a second census under a different factor
encoding (different DFS tree, identical count vectors:
`67, 2211, 46449, 632138, 4105426, 2186496` for `C₃²⊕C₁₅`;
`81, 3240, 83200, 1422850, 12783888, 6654960` for `C₃³⊕C₆`) + verified
witnesses. For `C₃²⊕C₁₅` additionally: raw-multiset run (5.66G nodes,
824 s) matching the exact `2^k` relation on all six counts, and a
clean-room Python census reproducing the census digit for digit — the
full Theorem-7 battery. The companion order-135 cell `C₃⊕C₄₅ = 7` (the
family deviation) carries the same battery: second encoding
(`3+5+9` vs `3+45` — identical counts `67, 2211, 46452, 633074, 4220095,
3391470`), raw run (7.48G nodes, 1075 s, `2^k` relation PASS), verified
witness, and a clean-room Python census matching digit for digit
(`run_135_c3c45_indep.txt`) — the full four-path battery for both
order-135 cells.

**Endpoint attribution over all 310 valued cells** (312 minus the two
timeout cells, which are lower=upper anyway): bounds coincide for 278;
value = lower bound only: 6; value = upper bound only: 24; strictly
between: the 2 of Theorem 12.

**The fifteen genuinely new determinations past 100** (cells where the
Theorem 3.1 bounds differ, so no known result forces the value —
everything else in 101–162 is forced by the bounds): in
`(order, invariant factors, D±, {bracket})` form —
108 `(3,3,12) → 7` and `(3,6,6) → 7` (upper); 135 `(3,45) → 7` (**lower**)
and `(3,3,15) → 7` (**middle**); 144 `(3,48), (6,24), (12,12), (2,6,12),
(2,2,6,6) → 8` (upper); 147 `(7,21) → 8` (upper, Theorem 8); 150
`(5,30) → 8` (upper); 153 `(3,51) → 8` (upper); 162 `(3,54) → 8`,
`(3,3,18) → 8` (upper) and `(3,3,3,6) → 7` (**middle**, Theorem 12).

**Families.**
`D±(C₅ ⊕ C₅ₙ) = 5, 6, 6, 7, 7, 8, 8` for `n = 1..7` — `n = 3` remains
the unique sub-binary cell; `n = 6` (order 150, bracket `{7,8}`)
resolves **upper**; `n = 7` (order 175, bounds coincide) is
lemma-forced and engine-confirmed. `D±(C₇ ⊕ C₇ₙ) = 6, 7, 8, 8`
(`n = 1..4`) — upper throughout, including the new `n = 4` gap cell
(order 196, 2.57G-node census, 10,782,828 extremal 7-sets).

**Beyond 162 (spot cells, lighter verification tier).** Three gap or
family cells past the systematic table, each a single census plus a
`verify_witness.py`-checked witness (no second encoding or raw run —
stated so the tier is not mistaken for the headline battery):
`D±(C₇ ⊕ C₂₈) = 8` (bracket `{7,8}`, upper), `D±(C₁₄ ⊕ C₁₄) = 8`
(bracket `{7,8}`, upper; 3.22G nodes), `D±(C₅ ⊕ C₃₅) = 8` (bounds
coincide, so PROVED by Lemmas 3+3b+3c independently of the run).
`D±(C₃ ⊕ C₃ₙ)` for `n = 2..18`: `5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7,
7, 8, 8, 8` — **the `n = 15` cell (order 135, bracket `{7,8}`) attains
the lower bound**, the family's first deviation from the binary value in
our data. ⚠ A search-engine paraphrase of MOS 2014 says the family value
"is known for n ≥ 2 … and matches the upper bound"; if their theorem
really covers all `n ≥ 2` unconditionally, our `n = 15` value would
contradict it — far more likely the paraphrase dropped a hypothesis or
their range. **Do not cite the `n = 15` tension until MOS §5 is read in
full**; the computation itself is battery-verified (Theorem-12-level
checks, plus the identical `3+5+9` vs `3+45` encodings).

**Question A — answered.** The session's early data (≤ 150 at the time)
suggested `D±(G)` might always sit at a Theorem 3.1 endpoint; Theorem 12
refutes that at orders 135 and 162. The refined pattern in range: writing
`P(G) = max` over direct-sum splits `G = A ⊕ B` of `L(A) + L(B)` *with
exact component values from this table*, every below-binary group is
split-tight — `L(C₅⊕C₁₅) = L(C₅) + L(C₁₅) = 2 + 3`,
`L(C₃²⊕C₁₅) = L(C₃) + L(C₃⊕C₁₅) = 1 + 5`,
`L(C₃³⊕C₆) = L(C₃) + L(C₃) + L(C₃⊕C₆) = 1 + 1 + 4` — while the "mixing"
groups (`C₃⊕C₆`, `C₃⊕C₁₅`, `C₇²`, `C₇⊕C₂₁`, …) strictly exceed every
split and sit on the binary ceiling. The middle values exist exactly
because a split can capture a mixing component whose own value already
beats its invariant-factor estimate.

**Question A′ (new).** Is `L(G)` always attained either by a direct-sum
split into proper subgroups (with the components' exact values) or by
meeting the binary ceiling `⌊log₂|G|⌋`? True for all 312 groups here. A
counterexample needs a group that exceeds all of its splits yet misses
the ceiling.

**Question A.** Does `D±(G) ∈ {Σ⌊log₂ n_i⌋ + 1, ⌊log₂|G|⌋ + 1}` for every
finite abelian `G`? (True for all 280 groups of order ≤ 150. We found no
such statement in the snippets; MOS's exceptions being exactly
lower-bound-attaining is consistent with it. A counterexample would need
invariant factors whose `⌊log₂⌋`s sum well below `⌊log₂|G|⌋`, i.e. rank ≥ 3
with unbalanced factors — the region past 150 is where to look.)

**Question B.** Is `C₅ ⊕ C₁₅` the *only* group of the family
`C_p ⊕ C_{3p}` (`p ≥ 5` prime) below the binary bound? (`p = 7` is not;
`p = 11`: `C₁₁ ⊕ C₃₃`, order 363, bracket `{9, 9}` — bounds coincide, so
no test there; the next test cases are `C₁₃ ⊕ C₃₉` `{9,10}` at order 507.)

## 6. Methodology and reproducibility

- Machine: cloud sandbox, Intel Xeon @ 2.10 GHz, 4 cores, 15 GB RAM;
  gcc 13.3.0 `-O2`; Python 3.11.15. All runs single-threaded,
  deterministic, exact integer arithmetic throughout (no floating point
  anywhere). No randomness, hence no seeds.
- Headline runtimes: `C₅⊕C₁₅` census 0.098 s (792,672 nodes); raw 4.39 s
  (46.7M nodes); Python census 27.5 s. `C₇⊕C₂₁` census 33.7 s (166.8M
  nodes); raw and per-phase timings as recorded in the committed
  transcripts (`run_7_21_raw.txt`, `max_*.txt`, `sweep_*.log`).
- Certificates committed: census outputs (`run_*_census.txt`,
  `run_*_raw.txt`), extremal enumerations (`enum_5_15_size5.txt`, 85,155
  lines; `enum_7_21_size7.txt`, 2016 lines), maximality transcripts
  (`max_*.txt`), audit transcript (`case_audit_out.txt`), full tables
  (`table_*.csv`).
- Every number in this note is emitted by a committed script; see
  `README.md` for the script-by-script table.

## 7. Might this be known?

Stated prominently, per repository rule 3: the openness of both headline
cells is established only at snippet level (no primary source readable
from this sandbox). The 2014 bracket and its 2021 thesis restatement are
the strongest evidence `C₅ ⊕ C₁₅` was open; for `C₇ ⊕ C₂₁` we found no
published value at all, but the derived bracket `{7,8}` is elementary, and
a resolution could exist in the unreadable full texts (Merito–Ordaz–Schmid
2025, the Adhikari 2017 survey, the Perez-Lavin thesis, or elsewhere).
Twenty-seven literature queries on 2026-08-22 (eleven aimed directly at
these two groups) surfaced nothing. **First follow-up on a
network-enabled day: read MOS 2014 §5, arXiv:2506.14279, the survey, and
the thesis, and re-verify every (secondary) statement above.**

## 8. Open questions

1. Prove Theorem 7 fully by hand (the reduction framework of §2 does case
   `(4,2)`; the audit's "≥ 2 violations everywhere" suggests slack).
   Same question for the two middle values of Theorem 12 — *why* 7?
2. Question A′ and Question B of §5. The next hunting orders for a
   Question A′ counterexample: 3-heavy rank ≥ 3 groups past 162 (189,
   225, 243-neighborhood, 270).
3. Read MOS 2014 §5 on a network-enabled day and settle whether the
   `C₃ ⊕ C₃ₙ` family theorem has hypotheses that exempt `n = 15` — until
   then the family tension in §5 stays a paraphrase artifact, not a
   contradiction claim.
4. The coding-theory route (JCTA 2015 links `D±` to intersecting codes
   (secondary)): does the uniqueness in Theorem 10 correspond to a known
   optimal code? (A quick conic/collinearity/Sidon probe of the unique
   147-configuration found no classical structure — see WRITEUP.)
