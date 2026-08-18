# Undirected repetition thresholds at the open frontier `k ≥ 22`: exact certificates, structural lemmas, and a descent criterion

Session 2026-08-18. One session so far. Run with substantial AI assistance
(Claude); every proof below was produced and checked within the session and
should be treated as one-session-old until independently verified.

**Sourcing caveat.** This session ran with all primary literature blocked
(WebFetch egress denied; search snippets only). Every statement about the
literature — including the definition conventions of Currie–Mol — is
**(secondary)** and so marked. The mathematics below is self-contained: all
definitions are stated explicitly, and no proof depends on an unread source.

## Abstract

An *undirected `r`-power* is a word `x y x′` with `x` nonempty,
`x′ ∈ {x, xᴿ}` and `|xyx′|/|xy| = r`. The undirected repetition threshold
`URT(k)` is the infimum of the `r` such that undirected `r`-powers are
avoidable over `k` letters. Currie and Mol proved `URT(k) ≥ (k−1)/(k−2)`
for `k ≥ 4`, conjectured equality, and confirmed it for `4 ≤ k ≤ 21`; the
conjecture is open for every `k ≥ 22` (all (secondary)). This session
attacked `k = 22`. It did not settle it. It produced: **(1)** exhaustive
micro-certificates (451–550 nodes) that undirected exponents `≥ (k−1)/(k−2)`
are unavoidable over `k` letters for `k = 22, 23, 24, 25` — an independent,
in-repo re-derivation of the lower bound at these `k`, with the sharp
maximal lengths `k+3`; **(2)** certified `(21/20)⁺`-free words over 22
letters of length 20 000 (and length 5 000 for `k = 23, 24, 25`), quadruply
cross-checked; **(3)** proofs that the natural binary Pansiot ansatz is
empty at these thresholds for every alphabet `20 ≤ n ≤ 23` — threshold
witnesses are forced to use distance-`(n−2)` recurrences; **(4)** exact
reversal-transfer identities for the binary Pansiot code; **(5)** a proved
finite-check **descent criterion** (Theorem D) reducing U-freeness of any
uniform-morphic fixed point to three checkable conditions; and **(6)**
certified emptiness of the entire affine sub-ansatz `φ(x) = m·x + B₀` at
`k = 22` for all ten multipliers `m`. The general uniform-morphic search
remains open and is the sharpest next step.

## 1. Definitions and conventions

Alphabet `Σ_n = {0, …, n−1}`. A finite or infinite word `w` over `Σ_n` is
indexed from 0. `wᴿ` is the reversal of `w`.

**Definition 1 (undirected offender).** Fix a rational `α = num/den > 1`.
An *undirected offender* in `w` is an occurrence
`(i, ℓ, g, type)`, `ℓ ≥ 1`, `g ≥ 0`, with `den·(2ℓ+g) > num·(ℓ+g)`, of
either

- *ordinary*: `w[i .. i+ℓ) = w[i+ℓ+g .. i+2ℓ+g)`, or
- *reversed*: `w[i .. i+ℓ) = ( w[i+ℓ+g .. i+2ℓ+g) )ᴿ`.

`w` is **U-`α⁺`-free** if it has no undirected offender (exponents equal to
`α` are allowed). Replacing the strict inequality by
`den·(2ℓ+g) ≥ num·(ℓ+g)` defines **U-`α`-free** (exponent `α` itself also
forbidden). This matches the factor formulation: `xyx′` with `x′ ∈ {x, xᴿ}`
has exponent `|xyx′|/|xy| = (2ℓ+g)/(ℓ+g)`.

**Definition 2 (URT; convention (secondary)).** `URT(k)` is the infimum of
the set of `r` such that some infinite word over `Σ_k` contains no
undirected offender of exponent `≥ r`. The statements below are phrased so
that they do not depend on the `≥ r` versus `> r` reading of "avoids
`r`-powers": an infinite U-`α⁺`-free word shows `URT(k) ≤ α` under either
reading, and unavoidability of exponents `≥ α` shows `URT(k) ≥ α` under
either reading.

Throughout, for alphabet size `k` the target threshold is
`α = (k−1)/(k−2)`; for `k = 22` that is `21/20`.

**Known (all (secondary), from search snippets of arXiv:1904.10029,
arXiv:2006.07474 = TCS 2021, and Shur ToCS 2024):** `URT(3) = 7/4`;
`URT(k) ≥ (k−1)/(k−2)` for `k ≥ 4`; equality conjectured for all `k ≥ 4`
and confirmed for `4 ≤ k ≤ 21`; open for `k ≥ 22`; Shur's entropy-compression
bounds are asymptotic and decide no individual `k`.

## 2. Elementary structure (PROVED)

Fix `k = n`, `α = (n−1)/(n−2)`, and let `w` be U-`α⁺`-free over `Σ_n`.
All three proofs are direct calculations with Definition 1.

**Lemma L1 (gaps).** Equal letters in `w` sit at distance `≥ n−2`.
*Proof.* Equal letters at distance `d` form an ordinary offender with
`ℓ = 1`, `g = d−1`, exponent `(d+1)/d`, and `(d+1)/d > (n−1)/(n−2)` iff
`d < n−2`. ∎

**Lemma L2 (no palindromes).** `w` has no palindromic factor of length
`≥ 2`. *Proof.* An even palindrome `u uᴿ` is a reversed offender with
`g = 0`, exponent 2. An odd palindrome `u c uᴿ` with `|u| = ℓ ≥ 1` is a
reversed offender with `g = 1`: `(2ℓ+1)/(ℓ+1) > (n−1)/(n−2)` iff
`ℓ(n−3) > 1`, true for all `ℓ ≥ 1`, `n ≥ 5`. (Length-2 palindromes are
squares, exponent 2.) ∎

**Lemma L3 (reversed pairs).** If `w[i]w[i+1] = ab` and `w[j]w[j+1] = ba`
with `j ≥ i+2`, then `j − i ≥ 2(n−3) + 2`; for `n = 22`: `j − i ≥ 40`.
*Proof.* Arms of length `ℓ = 2` and gap `g = j−i−2` form a reversed
offender iff `g < (n−3)·ℓ = 2(n−3)`. ∎

**Lemma L4 (aperiodicity).** No eventually periodic infinite word is
U-`α⁺`-free for any finite `α`. *Proof.* A tail with period `Q` contains
ordinary offenders `(i, ℓ, Q−ℓ)` of exponent `(Q+ℓ)/Q → ∞`. ∎
*Consequence: every witness for `URT(k) = (k−1)/(k−2)` is aperiodic; in
particular no "twisted-periodic" word `w[i+P] = σ(w[i])` with `σ` of finite
order can be a witness, since it is periodic with period `P·ord(σ)`.*

## 3. Checker architecture (methods; the certificates depend on it)

Four independent implementations of Definition 1 (`urt.py`):

| checker | method |
|---|---|
| `u_offender_naive` | brute triple loop over `(i, ℓ, g)`, both types |
| `u_offender` | run-scan per period (ordinary) + per mirror-sum center walk (reversed) |
| `u_free_np` | numpy batch, run-length algebra per period / per center |
| `UInc` | incremental push/pop: suffix run arrays per period + mirror-run arrays per center |

Agreement was verified on 4 000 random words spanning five thresholds
(342 free / 3 658 unfree; `tests_urt.py t1`), plus 300 randomized push/pop
replays (`t1b`), plus a separate 3 000-word validation of the non-strict
(`≥`) mode against a dedicated naive. Decode/monodromy conventions were
cross-checked against `circular-thresholds/pansiot.py` on 500 random
instances (`t2`). Alive/dead pipeline controls: at known-true thresholds the
letter-space DFS stays alive (`k = 3` at `7/4`, `k = 4` at `3/2`, `k = 5`
at `4/3`, `k = 21` at `20/19`); strictly below known thresholds it dies
(`k = 3` at `3/2` and `k = 4` at `4/3`, both dead at length 6). All
arithmetic in every checker is integer arithmetic.

## 4. The threshold exponent is unavoidable: certified lower bounds

**Result C1 (CERTIFIED).** For `k = 22, 23, 24, 25` and
`α = (k−1)/(k−2)`: every word over `Σ_k` of length `≥ k+4` contains an
undirected offender of exponent `≥ α`. The maximal U-`α`-free lengths are
exactly `k+3`:

| k | α | max length of U-α-free word | search-tree nodes (exhaustive, canonical) |
|---|---|---|---|
| 22 | 21/20 | 25 | 451 |
| 23 | 22/21 | 26 | 483 |
| 24 | 23/22 | 27 | 516 |
| 25 | 24/23 | 28 | 550 |

Each row is an exhaustive canonical DFS (letters named by first occurrence,
which loses no generality since Definition 1 is renaming-invariant), tree
fully exhausted, in the non-strict checker mode. Reproduce:
`python3 lower_bounds.py` (writes `data/lower_bound_certificates.txt`).
Runtime < 1 s total.

**Corollary C2 (CERTIFIED certificate + trivial argument).**
`URT(k) ≥ (k−1)/(k−2)` for `k = 22, 23, 24, 25`. *Proof.* Every infinite
word over `Σ_k` contains, in each window of length `k+4`, an undirected
offender of exponent `≥ (k−1)/(k−2)` (Result C1), so no infinite word
avoids undirected `r`-powers for any `r ≤ (k−1)/(k−2)`. ∎

This re-derives, for these four `k`, the lower-bound theorem of Currie–Mol
(they prove it for all `k ≥ 4` (secondary)); the value here is that the
certificate is primary, in-repo, and tiny.

**Conjecture C3 (from the data).** For all `k ≥ 22`, the maximal length of
a word over `Σ_k` with no undirected exponent `≥ (k−1)/(k−2)` is `k+3`.
(Certified only at `k = 22..25`. A hand proof looks tractable and would
give the lower bound uniformly.)

## 5. Above the threshold the language is thick: certified witnesses

**Result C4 (CERTIFIED).** There is a word over `Σ_22` of length **20 000**
with no undirected offender of exponent `> 21/20` — namely the
lexicographically least canonical U-`(21/20)⁺`-free word of that length,
committed as `data/witness_n22_L20000.txt`. Verified independently by
`UInc` (during generation), `u_offender`, and `u_free_np` over the full
length, and by the brute checker on the length-400 prefix. Reproduce:
`python3 certify_witness.py 22 20000 400` (53 s generation + 26 s
verification; deterministic, no seed).

Likewise length 5 000 for `k = 23, 24, 25` (`witness_n{23,24,25}_L5000.txt`,
`python3 certify_witness.py <k> 5000 300`).

**Result C5 (CERTIFIED counts).** Over `Σ_22` at `21/20⁺` there are
**1 606 755** canonical U-free words of length 55 (exhaustive DFS with
50 M-node budget, tree exhausted to that depth). The lex-DFS needed only
22 backtracks to reach length 20 000: the language is not thin.
Letter-gap spectra of words at length 55 lie in `{20, …, 25}`.

Together with C1 this gives a sharp certified picture at `k = 22`: at
exponent cutoff `≥ 21/20` everything dies by length 25; at cutoff
`> 21/20` the language is thick to length 20 000. If the Currie–Mol
conjecture holds at `k = 22`, the threshold is attained only in the `⁺`
sense — exactly as in Dejean's theorem.

## 6. The binary Pansiot ansatz is empty (CERTIFIED + PROVED micro-lemmas)

For ordinary Dejean-threshold words, the classical route (Pansiot) codes an
`(n−1)`-rainbow-window word over `Σ_n` by one bit per letter (bit 0:
repeat at distance `n−1`; bit 1: the unique absent letter). The analogous
class here is the words with all `(n−1)`-windows rainbow, i.e. equal-letter
gaps `≥ n−1` — a strict subclass of U-`α⁺`-free (Lemma L1 forces only
`≥ n−2`).

**Result C6 (CERTIFIED).** For every `n ∈ {20, 21, 22, 23}` at
`α = (n−1)/(n−2)`: the U-code-free binary words (those whose decode is
U-`α⁺`-free) have maximal length **4**; the exhaustive trees have 20 nodes
each. The longest codeword in every case includes `0110`. Reproduce:
`python3 code_class.py` (writes `data/code_class_emptiness.txt`).

**Lemma L5 (PROVED).** At `n = 22`, `α = 21/20`, in-class: two consecutive
0-bits are impossible, and three consecutive 1-bits are impossible.
*Proof.* Bits `00` at steps `t, t+1` emit letters equal to those at
distance 21, giving an ordinary offender with `p = 21, ℓ = 2`, exponent
`23/21 > 21/20`. Bits `111` emit three fresh letters; from the second
onwards the absent letter is the one that left the window 22 steps before,
so steps `t+1, t+2` create an ordinary arm `ℓ = 2` at `p = 22`, exponent
`24/22 > 21/20`. ∎ (The full emptiness in C6 is the certificate; L5 just
exhibits the mechanism.)

**Consequence.** Undirected-threshold witnesses over `Σ_n` must contain
equal letters at distance exactly `n−2` (exponent exactly `α`, unit arms)
— they cannot live in the rainbow-`(n−1)` class where the classical binary
code operates. Any code-based attack needs the 3-choice-per-step automaton
of the `gap ≥ n−2` class. (This also corrects an early working hypothesis
of this session: whatever the binary morphisms `f_k` in Currie–Mol's proofs
are (unread, (secondary)), their images cannot be Pansiot codewords of the
witnesses in this sense, because the class is empty even where their
theorem proves witnesses exist.)

## 7. Reversal in the binary Pansiot code (PROVED)

These identities were derived for the (now dead-ended) binary route, but
they are correct, reusable machinery for any future reversal-aware code
argument, so they are recorded with proofs. Conventions as in
`circular-thresholds/NOTE.md` §11: states `σ = (a_1 … a_{n−1} | b)`
identified with elements of `Sym(n)`, bits acting on the right by `τ_0`
(the `(n−1)`-cycle on window slots) and `τ_1` (the `n`-cycle), monodromy
`g(V) = τ_{V_1} ∘ ⋯ ∘ τ_{V_L}`, decode with canonical initial window.

Let `r ∈ Sym(n)` be the window reversal: `r(i) = n−2−i` for
`0 ≤ i ≤ n−2`, `r(n−1) = n−1`.

**Lemma R1.** `r τ_b r = τ_b^{−1}` for `b ∈ {0, 1}`.
*Proof.* Mechanical on the two generators: for a state
`σ̃ = (w_0 … w_{20} | b)`, the τ₀-predecessor is `(w_20, w_0 … w_19 | b)`
and the τ₁-predecessor is `(b, w_0 … w_19 | w_20)`; applying the window
reversal `R(σ) = σ∘r` to each and comparing with `R(σ̃)·τ_b` gives equality
in both cases. (Verified additionally by machine on `n ∈ {5, 8, 12, 22,
23}`.) ∎

**Lemma R2 (code of the reversal).** If `w` is in-class (all
`(n−1)`-windows rainbow) with `|w| = L ≥ n−1`, then `wᴿ` is in-class and
`code(wᴿ) = (code(w))ᴿ`. *Proof.* Bit `t` of `code(w)` records whether the
distance-`(n−1)` pair `(w[t+n−2], w[t−1])`* is an equality; this relation
is symmetric in the word's positions, and position-reversal maps the pair
tested by bit `t` of `wᴿ` to the pair tested by bit `L−n+1−t+1` of `w`;
tracking indices gives exactly the reversed bit string. ∎
(*Indexing: bit `t ≥ 1` emits letter `t+n−2`.)

**Lemma R3.** `g(Vᴿ) = r · g(V)^{−1} · r`. *Proof.* By R1,
`r g(V) r = (r τ_{V_1} r) ⋯ (r τ_{V_L} r) = τ_{V_1}^{−1} ⋯ τ_{V_L}^{−1}
= (τ_{V_L} ⋯ τ_{V_1})^{−1} = g(Vᴿ)^{−1}`. ∎

**Lemma R4 (anti-gid transfer, statement).** In `x = dec(V)`, a reversed
letter-match of arm length `ℓ ≥ n−1` between arms starting at letter
positions `a` and ending at `a′+n−2` corresponds exactly to an *anti-gid
pair* `H_a = H_{a′} · r` of prefix monodromies together with the mirrored
bit-agreement run `V_{a+1+t} = V_{a′−t}`, each agreement extending the
match by one letter; quantitatively a reversed match `(ℓ, g)` in the decode
corresponds to a reversed bit-match of length `ℓ − (n−1)` at code positions
with gap `g + n`. *Proof idea.* The window of the state at `a` is the
reverse of the window at `a′` (`R(σ_{a′}) = σ_a`, i.e. `H_a = H_{a′}r`),
and the one-step propagation `R(σ̃·τ_c^{−1}) = R(σ̃)·τ_c` (Lemma R1) turns
forward steps on one arm into backward steps on the other with equal bits.
Verified by machine on random instances (`tests_urt.py t3`, pattern
identity `pattern(dec(Vᴿ)) = pattern((dec V)ᴿ)`). With the binary class
empty (C6) this lemma has no application at these thresholds; it is
recorded for reuse. ∎(sketch: the full induction is the same propagation
argument as circular-thresholds Lemma T(i), mirrored.)

## 8. A descent criterion for uniform-morphic witnesses (PROVED)

The natural remaining construction route is a fixed point `W = φ(W)` of a
`k`-uniform morphism `φ` on `Σ_22` with blocks `B_x := φ(x)`. Theorem D
reduces U-freeness of such a `W` to finite checks. Write `n = 22`,
`α = 21/20 = num/den`, and let `F_j(W)` denote the length-`j` factors
of `W`.

> **Theorem D (descent criterion).** Let `W = φ(W)` be the fixed point of a
> `k`-uniform morphism `φ` prolongable on `W[0]`, and suppose:
>
> * **(D1)** `x ↦ B_x[0]` and `x ↦ B_x[k−1]` are injective on the letters
>   occurring in `W`;
> * **(D2)** for every `xz ∈ F_2(W)` and every letter `y` of `W`, the block
>   `B_y` does not occur in `B_x B_z` at any offset `o` with `0 < o < k`;
> * **(D3)** for every `xz ∈ F_2(W)` and every letter `y` of `W`, the word
>   `(B_y)ᴿ` does not occur in `B_x B_z` at any offset `0 ≤ o ≤ k`;
> * **(D4)** every factor of `W` of length `≤ L₀ := 42k − 20` is
>   U-`α⁺`-free.
>
> Then `W` is U-`α⁺`-free.

*Proof.* Suppose `W` has an undirected offender; choose one, `(i, ℓ, g,
type)`, of minimal span `S = 2ℓ+g`. By (D4), `S > L₀`.

**Reversed case.** Let the arms be `A₁ = [i, i+ℓ)` and
`A₂ = [i+ℓ+g, i+2ℓ+g)`, with `W|A₂ = (W|A₁)ᴿ` and `g < 19ℓ` (Definition 1
at `α = 21/20`: `den(2ℓ+g) > num(ℓ+g) ⟺ g < 19ℓ`). If `ℓ ≥ 2k−1`, then
`A₁` contains a `φ`-aligned block `[tk, tk+k) ⊆ A₁`, carrying `B_y` with
`y = W[t]`. Its mirror image inside `A₂` is an interval of length `k`
carrying `(B_y)ᴿ`. Every interval of length `k` in `W` lies inside two
consecutive aligned blocks `B_x B_z` with `xz ∈ F_2(W)`, so `(B_y)ᴿ`
occurs in some `B_x B_z` at an offset in `[0, k]` — contradicting (D3).
Hence `ℓ ≤ 2k−2` and `S = 2ℓ+g < 21ℓ ≤ 21(2k−2) = 42k−42 < L₀`,
contradicting minimality via (D4).

**Ordinary case.** Arms `W|[i, i+ℓ) = W|[i+p, i+p+ℓ)` with period
`p = ℓ+g ≥ ℓ`, exponent `(p+ℓ)/p > α ⟺ ℓ ≥ ⌊p/20⌋+1`, and `W` has period
`p` on the stretch `[i, i+p+ℓ)`.

*Sub-case `p ≤ 40k−20`.* The occurrence `(i, ℓ′, p−ℓ′)` with
`ℓ′ = ⌊p/20⌋+1 ≤ ℓ` is also an offender, of span
`p + ℓ′ ≤ p + p/20 + 1 ≤ (21/20)(40k−20) + 1 = 42k−20 = L₀`,
contradicting (D4).

*Sub-case `p ≥ 40k−19`.* Then `ℓ ≥ ⌊p/20⌋+1 ≥ 2k`, so `[i, i+ℓ)`
contains an aligned block `[tk, tk+k)`. Its `p`-shifted copy
`W|[tk+p, tk+p+k) = B_{W[t]}` is an occurrence of a block at offset
`p mod k` inside two consecutive blocks; by (D2) the offset is 0, i.e.
`k | p`. Write `p = k p′`.

For every aligned block `[sk, sk+k)` inside the first arm, equality of the
stretch gives `B_{W[s]} = B_{W[s+p′]}` letterwise, and (D1) (say, first
letters) forces `W[s] = W[s+p′]`. Let `[A₁*, B₁*)` be the parent interval
of these `s`; it has length `≥ ⌊(ℓ − (k−1))/k⌋`. If `i` is not aligned,
the partial block at the left end — the last `λ = k⌈i/k⌉ − i ∈ [1, k−1]`
letters of `B_{W[⌈i/k⌉−1]}` — is matched by the stretch to the last `λ`
letters of `B_{W[⌈i/k⌉−1+p′]}`; equal last letters and (D1) force
`W[⌈i/k⌉−1] = W[⌈i/k⌉−1+p′]`, extending the parent equality interval one
step left. Symmetrically on the right with first letters. In each of the
four alignment cases the count works out to: `W[s] = W[s+p′]` for `s` in an
interval of length `E ≥ ℓ/k`. Take `ℓ* = ⌈ℓ/k⌉ ≤ E` (an integer `≥ ℓ/k`).
Then `ℓ* > p′/20` (since `ℓ > p/20`), so `ℓ* ≥ ⌊p′/20⌋+1`: the parent
equality is an ordinary offender pattern of period `p′` and arm `ℓ*` **in
`W` itself** (self-similarity: the parent word of `W = φ(W)` is `W`). If
`ℓ* ≤ p′` this is literally an occurrence `(s₀, ℓ*, p′−ℓ*)`; if
`ℓ* > p′`, the periodic parent stretch of length `p′+ℓ* > 2p′` contains a
square, an offender `(s₀, p′, 0)`. Either way `W` has an ordinary offender
of span `≤ p′ + ℓ* ≤ (p+ℓ)/k + 2 < S` (using `S > L₀ ≥ 42k−20 > 2k+2·k/(k−1)`),
contradicting minimality of `S`. ∎

**Remarks.** (i) The four alignment cases in the boundary extension are
elementary but essential; the uniform outcome `E ≥ ℓ/k` uses that each
non-aligned end loses `< 1` full block from the floor count and regains
exactly 1 from the end-letter argument. (ii) (D2)/(D3) are `O(n³k²)`
integer checks. (iii) (D4) is finite because the factors of length
`≤ L₀` of a morphic fixed point are computable with a stabilization
certificate (iterate `φ` from the seed; the length-`L₀` factor set is
non-decreasing and finite, and once one more iteration adds nothing new at
length `≤ L₀` while every length-`L₀` window of the next level is covered
by images of already-seen factors, the set is closed); at `k = 22`,
`L₀ = 904` and a certified prefix check suffices in practice.

**Status of the hypothesis space (CERTIFIED emptiness so far).** Theorem D
is currently a criterion without a known instance:

* the **affine family** `φ(x) = m·x + B₀ (mod 22)` — whose fixed point is
  the digit-sum word `W[q] = Σ_j m^{j}·B₀[d_j]`-style generalization of
  Thue–Morse, and for which (D1) holds automatically and the search space
  collapses to one block — is **empty at `k = 22, 23, 24` for all
  `m ∈ (Z/22)^× = {1,3,5,7,9,13,15,17,19,21}`**: the exhaustive
  affine-consistent canonical search (`affine_search.py`, GF(2)×GF(11)
  elimination over the letter-injection) dies by depth ≤ 3k for every `m`
  (trees exhausted; `data/scan_affine_m.log`, `scan_affine_m2.log`,
  `scan_affine_m1_fill.log`). For `m = 1` it is additionally empty at
  `k ∈ {21, 26, 30, 36}` and every other `k ≤ 35` covered by the fill
  scan (exhausted; `k = 44, 52` reached node caps without survivors,
  inconclusive). Deaths cluster at depths `2k`–`3k`: the second block,
  a constant shift of `B₀`, collides with `B₀`.
* the **general** `k`-uniform search (`selfsim_search.py`: canonical DFS
  with block-class forcing, subsuming every uniform ansatz) is
  **inconclusive**: at `k = 21, 22` it hits a hard forcing wall at depth
  exactly `20k` — where the first parent-letter repetition forces the first
  block reuse — and 4 M-node runs neither pass it nor exhaust the tree.

## 9. Open questions

1. Find a `φ` satisfying (D1)–(D4) at `k = 22` (any `k`), or prove the
   uniform-morphic ansatz empty. The `20k` wall in the general search is
   where the action is; a solver-grade implementation (C, conflict
   learning; or SAT with the class-forcing encoded) is the concrete next
   step.
2. Prove Conjecture C3 (`max U-α-free length = k+3`) for all `k`; this
   would make the lower bound `URT(k) ≥ (k−1)/(k−2)` certificate-free and
   uniform.
3. Build the 3-choice automaton for the `gap ≥ n−2` class (the correct
   home of threshold witnesses, by §6) and redo the Pansiot-style transfer
   machinery there; §7's reversal identities are the model.
4. Non-uniform morphisms (images of ternary squarefree words) are
   unexplored here.

## 10. Reproducibility

Machine: 4-core sandbox, 15 GB RAM, Python 3.11.15, NumPy 2.4.6. All
searches single-threaded. Every table row above states its script; the
witness files and scan logs are committed under `data/`. Deterministic
unless a seed is shown (`probe.py` runs used seed 7; nothing labelled
CERTIFIED depends on a seeded run). Total session compute ≈ 2.5 h of the
4-core box.

AI assistance: this session (mathematics, code, prose) was produced with
Claude; checked within the session as described; no independent human
verification yet.
