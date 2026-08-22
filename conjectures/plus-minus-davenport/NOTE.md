# The plus–minus weighted Davenport constants of C₅⊕C₁₅ and C₇⊕C₂₁, and the complete table for all abelian groups of order ≤ 150

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

Finally we recompute `D±(G)` from the definition for every abelian group
of order ≤ 150: the 184 groups of order ≤ 100 agree with every published
value and bound we could extract from snippets — the Marchan–Ordaz–Schmid
Theorem 3.1 bounds, their exception list, and their `C₃ ⊕ C₃ₙ` family
values — and the orders 101–150 (sweep transcript and CSV committed)
appear to be new except where the general bounds already coincide. In
every computed cell, `D±(G)` equals one of the two Theorem 3.1 bounds;
the five groups of order ≤ 100 sitting strictly below the binary bound
(`C₃²`, `C₃³`, `C₃⁴`, `C₃² ⊕ C₉`, `C₅ ⊕ C₁₅`) all attain the lower bound
exactly.

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
| V2 | `dpm.c --raw` over 146 raw elements | run recorded in `run_7_21_raw.txt`; the acceptance criterion is max length 7 with all seven counts equal to `2^k ×` V1 |
| V3 | `verify_maximality.py` on all 2016 extremal sets | each free (`3⁷−1 = 2186` sums) and non-extendable by any of the 73 classes: `MAXIMALITY PASS` |

(V2 and a clean-room Python census were still running when this note was
first drafted; the committed transcripts are the record — see WRITEUP for
final status of each.) A free 7-witness, hand-checkable:
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

## 5. The complete table to 150

`sweep.py` ran `dpm` on **every** abelian group of order 2–150 (280
groups; elementary `C₂^r, C₃^r` of rank ≥ 7 filled in by Lemma 2). Orders
≤ 100 (184 groups): **every** value consistent with MOS Theorem 3.1
(neither bound ever violated), with the blanket `⌊log₂|G|⌋ + 1` claim and
its exception list, and with the `C₃ ⊕ C₃ₙ` family equalling the upper
bound for all `2 ≤ n ≤ 11` in range (secondary sources as in §1). Full
data: `table_002_100.csv`, `table_101_150.csv`.

Observations across `2 ≤ |G| ≤ 150`:

1. `D±(G)` **always equals one of the two Theorem 3.1 bounds** — no group
   in range takes a strictly intermediate value. (Verified over the ≤ 100
   table; the 101–150 verdict is read off `table_101_150.csv` — see the
   figures in §5a below, filled in from the finished sweep.)
2. The groups strictly below the binary bound `⌊log₂|G|⌋ + 1` in the
   ≤ 100 range are exactly `C₃², C₃³, C₃⁴, C₃² ⊕ C₉, C₅ ⊕ C₁₅`, and each
   attains the lower bound `Σ⌊log₂ n_i⌋ + 1` exactly.
3. Families:
   `D±(C₅ ⊕ C₅ₙ) = 5, 6, 6, 7, 7` for `n = 1..5` — the `n = 3` cell is
   the unique lower-bound holdout in range;
   `D±(C₇ ⊕ C₇ₙ) = 6, 7, 8` (n = 1, 2, 3) — upper bound throughout.

### 5a. Orders 101–150 (from the finished sweep)

_(figures inserted after `table_101_150.csv` completed; see below)_

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
2. Questions A and B of §5.
3. Push the table past 150 — orders with wide Theorem 3.1 gaps and rank
   ≥ 3 (e.g. 162 = `C₃³ ⊕ C₆`, bracket `{6, 7, 8}`) are the natural
   hunting ground for either a middle value (refuting A) or more
   lower-bound groups.
4. The coding-theory route (JCTA 2015 links `D±` to intersecting codes
   (secondary)): does the uniqueness in Theorem 10 correspond to a known
   optimal code?
