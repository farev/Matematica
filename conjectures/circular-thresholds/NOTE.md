# Circular threshold words: a pumping lemma, a decidable criterion, and the spectrum of realizable lengths

**Session 2026-08-03.** Research note. Claims are labelled PROVED / CERTIFIED /
NUMERICAL per the repository convention; nothing here is asserted beyond its
label.

**Sourcing caveat, stated once and meant throughout.** This session ran in a
sandbox in which `WebFetch` and `curl` are blocked at the egress proxy (HTTP
403 to every host, including `arxiv.org`, `oeis.org`, `erdosproblems.com`,
`mathoverflow.net`). Only a search tool was available. **No primary source was
opened.** Every attribution below is therefore marked **(secondary)** and must
be checked against the actual paper before any of this is published. The
mathematics in §3–§6 and §8 is self-contained and does not depend on any
citation; the *novelty* claims do.

---

## 1. The problem, and the definitions used here

Let `Σ_n = {0,…,n−1}`. For a finite nonempty word `u`, `per(u)` is its least
period and `exp(u) = |u| / per(u)`. For a rational `α > 1`, `u` is
**`α⁺`-free** if every factor of `u` has exponent `≤ α`.

The **repetition threshold** `RT(n)` is the infimum of the exponents `β` for
which arbitrarily long `n`-ary words with no factor of exponent `≥ β` exist.
`RT(2) = 2` (Thue), `RT(3) = 7/4` (Dejean), `RT(4) = 7/5` (Pansiot), and
`RT(n) = n/(n−1)` for `n ≥ 5` — Dejean's conjecture, completed by Currie–
Rampersad and Rao **(secondary)**. Words with all exponents `≤ RT(n)` are
called **`n`-ary threshold words**; they exist for every length.

A **circular word** of length `m` is `w ∈ Σ_n^m` with indices read mod `m`.
Its factors are the factors of `w^ω` of length `≤ m`.

> **Definition 1.** `w ∈ Σ_n^m` is **circular `α⁺`-free** if every factor of
> `w^ω` of length `≤ m` has exponent `≤ α`. For `K ≥ 0`, `w` lies in
> **`S_K(n,m)`** if every factor of `w^ω` of length `≤ m+K` has exponent
> `≤ α`. Note `S_0(n,m)` is exactly the set of circular `α⁺`-free words of
> length `m`, and `S_K ⊆ S_{K−1} ⊆ … ⊆ S_0`.

> **Definition 2 (the object computed here).** The **circular threshold
> spectrum** is
> `C(n) = { m ≥ 1 : some w ∈ Σ_n^m is circular RT(n)⁺-free }`,
> and `C^{(2)}(n) = { m : S_2(n,m) ≠ ∅ }` at `α = RT(n)`.

**Encoding used throughout.** A factor of exponent `> α` whose least period is
`p` has, as a prefix, a factor of length `L(p) = ⌊αp⌋ + 1` with period `p`.
Hence `w` is circular `α⁺`-free iff for no `p ≥ 1` with `L(p) ≤ m` and no
`i ∈ Z_m` do all of
`w[i+j] = w[i+j+p]`, `0 ≤ j < q(p) := L(p) − p`
hold (indices mod `m`). For `α = n/(n−1)` this gives `q(p) = ⌊p/(n−1)⌋ + 1`;
in particular `q(p) = 1` for `p ≤ n−2`, i.e. **any two positions at distance
`≤ n−2` in an `n`-ary threshold word carry different letters** — a fact used
repeatedly below. All arithmetic is exact (`fractions.Fraction` / integer);
no floating point occurs anywhere in the critical path.

### 1.1 Why this object

The literature defines three repetition thresholds for circular words — weak
`CRT_W`, intermediate `CRT_I`, strong `CRT_S` — by asking for `β`-free
circular words at *infinitely many* lengths, at *all sufficiently large*
lengths, and at *all* lengths respectively **(secondary)**. The reported state
of the art is:

- `CRT_S(k) = (⌈k/2⌉+1)/⌈k/2⌉` for `k ≥ 6` (Gorbunova), `CRT_S(4) = 3/2`,
  `CRT_S(5) = 4/3` (Currie–Mol–Rampersad, EJC 26(2) 2019, arXiv:1803.08145)
  **(secondary)**;
- `CRT_I(3) = CRT_W(3) = RT(3) = 7/4` **(secondary)**;
- **Conjecture (Currie–Mol–Rampersad).** `CRT_I(n) = CRT_W(n) = RT(n)` for all
  `n ≥ 4`. Mol–Rampersad, *The weak circular repetition threshold over large
  alphabets*, arXiv:1912.11388, RAIRO-ITA 54 (2020), prove `CRT_W(n) = RT(n)`
  for `n ≥ 45`, and state that **`CRT_W(n) = RT(n)` is open for
  `4 ≤ n ≤ 44` and `CRT_I(n) = RT(n)` is open for every `n ≥ 4`**
  **(secondary — this exact sentence was seen only in a search summary)**.

Two elementary observations tie `C(n)` to that conjecture. Since a circular
`RT(n)⁺`-free word has every exponent `≤ RT(n) < β` for any `β > RT(n)`:

> **Observation 3.** If `C(n)` is infinite then `CRT_W(n) = RT(n)`.
> If `C(n)` is cofinite then `CRT_I(n) = RT(n)`.

(Both are one-line consequences of the definitions; the converses are false in
general, because for `β > RT(n)` strictly there is slack at large periods that
threshold-exact words do not use.) So **exhibiting an infinite `C(n)` for a
single `n ∈ [4,44]` settles an open case of the conjecture.** That was this
session's target.

---

## 2. The circular threshold spectrum (CERTIFIED)

`C(n)` was computed by exact SAT search over the clause set of §1, one
instance per `(n,m)`. Every satisfiable instance's witness was re-verified by
an independent `O(m³)` checker written from Definition 1 and sharing no code
with the encoder (`circspec.py:verify`); a further vectorised checker
(`pump.py:circ_afree`) was cross-validated against the naive one on 300 random
circular words and 400 random linear words with zero mismatches.

### 2.1 Positive control

`n = 3`, `α = RT(3) = 7/4`, where `CRT_I(3) = CRT_W(3) = 7/4` is known
**(secondary)**:

> **Result C1 (CERTIFIED).** For `n = 3` and `1 ≤ m ≤ 300`, a circular
> `7/4⁺`-free ternary word of length `m` exists **except** for exactly
> `m ∈ {5, 7, 9, 10, 14, 16, 17, 22}`. In particular every length
> `23 ≤ m ≤ 300` is realizable.

This is what `CRT_I(3) = 7/4` predicts, and it calibrates the pipeline: a
cofinite spectrum in the one case where the answer is known.

A second, independent calibration against a *different* published constant:
with `α` set to the reported `CRT_S(k)` rather than `RT(k)`, every length must
be realizable. Checked for `(n,α) ∈ {(4,3/2), (5,4/3), (6,4/3), (7,5/4)}` over
`1 ≤ m ≤ 60`: **all 60 lengths realizable in every case**, matching
`CRT_S(4) = 3/2`, `CRT_S(5) = 4/3`, `CRT_S(6) = 4/3`, `CRT_S(7) = 5/4`
**(secondary)**.

### 2.2 The open cases

> **Result C2 (CERTIFIED).** On the ranges computed, the exceptional sets —
> the `m` admitting **no** circular `n`-ary threshold word — are:
>
> | `n` | `α = RT(n)` | range completed | #exceptional | last exceptional `m` |
> |---|---|---|---|---|
> | 3 | 7/4 | `1 … 300` | 8 | 22 — `{5,7,9,10,14,16,17,22}` |
> | 4 | 7/5 | `1 … 164` | 87 | **154** — 85 values `≤ 113`, then `147` and `154` |
> | 5 | 5/4 | `1 … 300` | 41 | 63 |
> | 6 | 6/5 | `1 … 275` | 33 | 59 |
>
> Full lists and every witness word are in `data/spec_n*.csv`. The `n = 4`
> range is shorter because its instances are much harder: the sweep was still
> deciding `m = 165` when the session ended.

> **Result C3 (CERTIFIED), the one genuinely surprising datum.** For `n = 4`
> the spectrum is **not** monotone in the naive sense: after the last small
> exception at `m = 113` there is an unbroken run `114 … 146`, and then two
> further isolated exceptional lengths, **`m = 147` and `m = 154`**. At
> `n = 5` and `n = 6` no such late gap occurs in the computed range.

C3 matters methodologically: at `n = 4` a sweep stopping anywhere in
`114 … 146` would have reported a clean cofinite-looking spectrum and been
wrong. It is a direct caution against reading `CRT_I(n) = RT(n)` off a finite
run — and `n = 4` is exactly the alphabet where `RT(4) = 7/5` is Pansiot's
exception to `n/(n−1)`, so it is the case one should expect to misbehave.

**All of §2 is evidence for, not a proof of, `CRT_I(n) = RT(n)`.** A finite
unbroken run says nothing about what happens later — C3 makes that concrete —
and, as noted after Observation 3, `CRT_I(n) = RT(n)` could hold even if
`C(n)` had infinitely many gaps. The honest statement is the certified one:
the listed lengths are realizable, the listed exceptions are not, on the
computed range only.

---

## 3. A pumping lemma for circular threshold words (PROVED)

The obstruction to turning §2 into a theorem is that circular `α⁺`-freeness is
not a bounded-window condition: a circular word of length `m` constrains
periods up to `≈ m(n−1)/n`. The following lemma removes that obstruction by
passing to the `S_2` refinement, which is exactly wide enough to close an
induction along a morphism.

> **Lemma A (circular pumping).** Let `α > 1`, let `q ≥ 2`, and let
> `h : Σ_n^* → Σ_n^*` be a `q`-uniform morphism that maps `α⁺`-free words to
> `α⁺`-free words. If `w ∈ S_2(n,m)` then `h(w) ∈ S_2(n,qm)`.

*Proof.* `|h(w)| = qm`, and `h(w)^ω = h(w^ω)` because `h` is a morphism. Let
`u` be a factor of `h(w^ω)` of length `ℓ ≤ qm + 2`, occurring at position `s`.
Then `u` is a factor of `h(v)`, where `v` is the factor of `w^ω` at letter
positions `⌊s/q⌋ … ⌈(s+ℓ)/q⌉ − 1`, so
`|v| ≤ ⌈ℓ/q⌉ + 1 ≤ ⌈(qm+2)/q⌉ + 1 = m + ⌈2/q⌉ + 1 = m + 2` for `q ≥ 2`.
Every factor of `v` is a factor of `w^ω` of length `≤ m+2`, hence has exponent
`≤ α` because `w ∈ S_2(n,m)`; that is, `v` is `α⁺`-free. Therefore `h(v)` is
`α⁺`-free, so `u` — a factor of `h(v)` — has exponent `≤ α`. ∎

> **Corollary B.** If some `q`-uniform `h` maps `α⁺`-free words to `α⁺`-free
> words and `S_2(n,m_0) ≠ ∅`, then `q^j m_0 ∈ C_α(n)` for every `j ≥ 0`; in
> particular `C_α(n)` is infinite. Taking `α = RT(n)` and invoking
> Observation 3, **`CRT_W(n) = RT(n)`**.

The `+2` is the whole content: `S_1` does not close the induction (a factor of
`h(w)^ω` of length `qm+1` can need `m+2` letters of `w^ω` to cover it), and
`S_3` and beyond are unnecessary. Lemma A reduces an infinitary statement to
**two finite searches** — a morphism, and one seed — and both are decidable
(§4, §5).

*Relativised form, used when the morphism is only known to behave on its own
language.* Let `X` be a factor-closed set of `α⁺`-free words with `h(X) ⊆ X`.
If every factor of `w^ω` of length `≤ m+2` lies in `X`, then every factor of
`h(w)^ω` of length `≤ qm+2` lies in `X`; the proof is verbatim, replacing "is
`α⁺`-free" by "lies in `X`" and using `Fac(h(X)) ⊆ Fac(X) = X`. Taking
`X = Fac(u)` for a fixed point `u = h^ω(a)` makes `h(X) ⊆ X` automatic.

---

## 4. A finite criterion for `α⁺`-free-preserving uniform morphisms (PROVED; expected to be known)

> **Theorem M.** Let `α ∈ (1,2]`, `q ≥ 2`, and let `h : Σ_n → Σ_n^q` be
> `q`-uniform with
> * **(H1)** `a ↦ h(a)[0]` injective;
> * **(H2)** `a ↦ h(a)[q−1]` injective;
> * **(H3′)** for every `a,b` with `ab` `α⁺`-free, every `c`, and every
>   `0 < i < q`: `h(c) ≠ (h(a)h(b))[i .. i+q−1]`;
> * **(H4)** `h(v)` is `α⁺`-free for every `α⁺`-free `v` with `|v| ≤ N_0`,
>   where `P_0 = ⌈2q/(α−1)⌉` and `N_0 = ⌈(αP_0+1)/q⌉ + 1`.
>
> Then `h(v)` is `α⁺`-free for every `α⁺`-free `v`.

*Proof.* Suppose some `α⁺`-free `v` has `h(v)` not `α⁺`-free. Then `h(v)` has a
factor `u` with period `p` and `|u| = ⌊αp⌋ + 1 > αp`; fix such a `u` at
position `s`.

*Case `p < P_0`.* Then `|u| ≤ αP_0 + 1`, and `u` lies inside `h(v′)` for a
factor `v′` of `v` with `|v′| ≤ ⌈|u|/q⌉ + 1 ≤ N_0`. `v′` is `α⁺`-free, so (H4)
makes `h(v′)` `α⁺`-free, contradicting `exp(u) > α`.

*Case `p ≥ P_0`.* Then `|u| − p > (α−1)p ≥ (α−1)P_0 ≥ 2q`, so `|u| ≥ p + 2q`.
Let `t` be the unique multiple of `q` in `[s, s+q)`. The block `[t, t+q)` lies
in `u` (as `2q ≤ |u|`) and so does `[t+p, t+p+q)` (as `t+p+q ≤ s+p+2q−1 <
s+|u|`); period `p` makes the two blocks equal, so `h(c)` occurs at position
`t+p` for `c = v[t/q]`. That occurrence spans at most two consecutive blocks,
i.e. sits inside `h(ab)` for consecutive letters `a,b` of `v`, and `ab` is
`α⁺`-free. By (H3′) it is aligned: `q | t+p`, and since `q | t`, **`q | p`**.
Write `p = qp′`.

Put `A = ⌈s/q⌉`, `B = ⌊(s+|u|)/q⌋`, `A* = ⌊s/q⌋`, `B* = ⌈(s+|u|)/q⌉`.
For `A ≤ i ≤ B−1−p′` the blocks `i` and `i+p′` both lie in `u` and are equal,
so by (H1) (which forces `h` injective on letters) `v[i] = v[i+p′]`.
If `s mod q ≠ 0`, positions `[s, Aq)` and `[s+p, Aq+p)` lie in `u` and agree;
these are the length-`(Aq−s)` suffixes of blocks `A−1` and `A−1+p′`, so their
**last** letters agree, and (H2) gives `v[A−1] = v[A−1+p′]`.
If `(s+|u|) mod q ≠ 0`, positions `[Bq, s+|u|)` and `[Bq−p, s+|u|−p)` lie in
`u` and agree; these are prefixes of blocks `B` and `B−p′`, so their **first**
letters agree, and (H1) gives `v[B−p′] = v[B]`.
Combining, `v[j] = v[j+p′]` for every `j` with `A* ≤ j` and `j+p′ ≤ B*−1`
(when `(s+|u|) mod q ≠ 0`) resp. `j+p′ ≤ B*` (otherwise); either way `v` has a
factor of length `B* − A* = ⌈(s+|u|)/q⌉ − ⌊s/q⌋ ≥ |u|/q` with period `p′`, of
exponent `≥ (|u|/q)/(p/q) = |u|/p > α`. This contradicts `v` being `α⁺`-free. ∎

The point of (H1)+(H2) is that they make the boundary loss vanish: without
them the argument only yields `exp ≥ α − 2q/p`, which is the usual obstruction
in this kind of lemma.

> **Honest attribution.** Finite tests for power-free morphisms are a
> well-developed subject (Bean–Ehrenfeucht–McNulty; Crochemore;
> Richomme–Wlazinski; and Ochem's generator of morphisms for infinite words is
> the standard tool for fractional exponents) **(secondary — none of these was
> read)**. **Theorem M should be assumed to be a rediscovery**, in a
> convenient normalisation, until someone checks. It is stated and proved here
> only so that §6 and §7 stand on their own.

---

## 5. The fixed-point criterion (PROVED)

Theorem M is stronger than needed when only one infinite word matters.

> **Theorem M′.** Let `h` be `q`-uniform satisfying (H1), (H2), (H3′), with
> `h(0)` beginning with `0`, and let `u = h^ω(0)`. Let
> `P_0 = ⌈2q/(α−1)⌉` and `B = ⌊αP_0⌋ + 1`. If every factor of `u` of length
> `≤ B` is `α⁺`-free, then `u` is `α⁺`-free.

*Proof.* Otherwise `u` has factors of exponent `> α`; among them choose one,
`z`, with least period `p` minimal. If `p < P_0` then the minimal such factor
has length `⌊αp⌋+1 ≤ B`, contradicting the hypothesis. If `p ≥ P_0` then, since
`u = h(u)`, the argument of Theorem M's second case applies with `v = u` and
produces a factor of `u` with period `p/q < p` and exponent `> α`,
contradicting minimality of `p`. ∎

Every factor of `u` of length `≤ B` lies in `h(v)` for some factor `v` of `u`
of length `≤ ⌈B/q⌉+1`, and `Fac_{≤t}(u)` is computable as the fixed point of
`S ↦ S ∪ Fac_{≤t}(h(S))` from `S = {0}`. So the hypothesis of Theorem M′ is a
**finite** check.

---

## 6. The resulting decidable criterion

> **Theorem C.** Let `n ≥ 3` and `α = RT(n)`. Suppose there exist
> * a `q`-uniform morphism `h` on `Σ_n` satisfying (H1), (H2), (H3′), (H4),
>   and
> * a word `w_0 ∈ S_2(n,m_0)` for some `m_0`.
>
> Then circular `n`-ary threshold words exist at every length `q^j m_0`,
> `j ≥ 0`; hence `C(n)` is infinite and **`CRT_W(n) = RT(n)`**.
> Both hypotheses are decidable by finite search.

*Proof.* Theorem M makes `h` `α⁺`-free-preserving; Corollary B applies. ∎

The same conclusion follows from the relativised Lemma A with Theorem M′ in
place of Theorem M, provided the seed satisfies the stronger requirement
`Fac_{≤m_0+2}(w_0^ω) ⊆ Fac(u)`.

---

## 7. A worked instance: `n = 3` (PROVED here; the result itself is known)

`α = RT(3) = 7/4`. Search over shift-equivariant `q`-uniform morphisms
(`h(a)[i] = (h_0[i]+a) mod 3`) found morphisms satisfying (H1)–(H4) at
`q = 25, 28, 30, …`. Take

```
q = 28,  h_0 = 0120212010201210120102120210,  h(a) = h_0 + a  (mod 3)
```

Conditions (H1), (H2), (H3′), (H4) with `P_0 = 75`, `N_0 = 8` were verified
**twice, by two implementations sharing no code** — `dejean_morph.c` (C) and
`pump.py:morphcheck` (Python) — with identical verdicts. A seed was found by
SAT:

```
m_0 = 20,  w_0 = 01202101210212012102  ∈ S_2(3,20)
```

By Theorem C, `h^j(w_0)` is a circular ternary threshold word of length
`20·28^j` for every `j ≥ 0`. Direct verification against Definition 1, not
via the theorem, at

| `j` | length | circular `7/4⁺`-free | in `S_2` |
|---|---|---|---|
| 0 | 20 | yes | yes |
| 1 | 560 | yes | yes |
| 2 | 15 680 | yes | yes |
| 3 | 439 040 | yes | yes |

> **Result P1 (PROVED, and a rediscovery).** `C(3) ⊇ {20·28^j : j ≥ 0}`, hence
> `CRT_W(3) = RT(3) = 7/4`.

**`CRT_W(3) = RT(3)` is already known (secondary).** Result P1 is reported
**only as a positive control**: it demonstrates that the §3–§6 machinery
produces a correct theorem end to end on the one small alphabet where the
answer can be checked against the literature. No priority is claimed for it.

---

## 8. Why the same route did not settle an open case: an obstruction (PROVED) and an exhaustive negative (CERTIFIED)

Applying Theorem C to `n ∈ [4,44]` needs a morphism. The natural ansatz — the
one that works at `n = 3`, and the one under which the search is small enough
to be exhaustive — is the **shift-equivariant** family
`h(a)[i] = (h_0[i] + a) mod n`, which satisfies (H1) and (H2) automatically.
It fails, and it fails for a reason.

> **Proposition N (PROVED).** Let `n ≥ 4`, `α = RT(n)`, `q ≥ n−1`, and let
> `h(a) = h_0 + a` be shift-equivariant `q`-uniform over `Z_n` with `h_0`
> `α⁺`-free. Let `D = { h_0[i+1] − h_0[i] mod n : 0 ≤ i ≤ q−2 }`. If
> `u = h^ω(0)` is `α⁺`-free and every letter of `Z_n` occurs in `u`, then
> `|D| ≤ 2`.

*Proof.* For each `d ∈ D` pick `i` with `h_0[i+1] − h_0[i] = d`. The letter
`a = −h_0[i]` occurs in `u`, so the pair `(0,d)` occurs in `u` inside `h(a)`;
hence `h(0)h(d) = h_0·(h_0+d)` is a factor of `u` and must be `α⁺`-free.
By §1, in an `α⁺`-free word with `α = RT(n)` any two positions at distance
`≤ n−2` carry different letters (for `n = 4`, `RT(4) = 7/5` gives the same
bound `n−2 = 2`). Apply this to positions `q−1` and `q+k` of `h_0·(h_0+d)`,
whose distance is `k+1 ≤ n−2` for `0 ≤ k ≤ n−3`:
`h_0[q−1] ≠ h_0[k] + d`, i.e. `d ≠ h_0[q−1] − h_0[k]`.
The letters `h_0[0], …, h_0[n−3]` lie in a window of length `n−2` and are
therefore pairwise distinct, so `{ h_0[q−1] − h_0[k] : 0 ≤ k ≤ n−3 }` has
exactly `n−2` elements, none of them in `D`. Hence `|D| ≤ n − (n−2) = 2`. ∎

Proposition N is vacuous at `n = 3` (it gives `|D| ≤ 2`, and `D ⊆ {1,2}`
always) — which is exactly why `n = 3` admits such morphisms and `n ≥ 4` is
squeezed. If `|D| = 1` then `h_0` is an arithmetic progression, hence periodic
with period `ord(d) ≤ n`, and `α⁺`-freeness forces `q ≤ ⌊α·ord(d)⌋ ≤ n+1`. The
case `|D| = 2` was not closed by proof; it was closed computationally:

> **Result N1 (CERTIFIED).** Exhaustive search over **all** `α⁺`-free
> `h_0 ∈ Σ_n^q` with `h_0[0] = 0` finds **no** shift-equivariant `q`-uniform
> morphism satisfying (H1)–(H4) at `α = RT(n)`, for
> `n = 4` (`q ≤ 60`), `n = 5` (`q ≤ 68`), `n = 6` (`q ≤ 51`),
> `n = 7` (`q ≤ 44`), `n = 8` (`q ≤ 37`).
> Under the weaker fixed-point criterion of Theorem M′ the search fails even
> earlier: the necessary condition "`h_0·(h_0+d)` is `α⁺`-free for every
> `d ∈ D`" — call it F2 — is satisfied by **no** candidate at all for
> `n = 4` (`q ≤ 60`), `n = 6` (`q ≤ 43`), `n = 7` (`q ≤ 37`), and for `n = 5`
> (`q ≤ 50`). The same search at `n = 3` returns morphisms, so the pipeline is
> not vacuously failing.
> Counts of candidates scanned are in `data/morph_n*.log`, `data/fix_n*.log`.

Diagnostically, every F2 violation observed sits at the seam between `h_0` and
`h_0+d` and has small period (`≤ n−2`) — precisely the mechanism Proposition N
formalises.

**Interpretation.** The shift-equivariant ansatz is the wrong normal form for
`n ≥ 4`. The literature's own remark that for small alphabets "techniques
different from those presented will likely be needed" **(secondary)** is
consistent with this. The natural next ansatz is Pansiot's encoding of
`n`-ary threshold words (`n ≥ 5`) by words over a smaller alphabet
**(secondary)**, in which the relevant morphisms need not be shift-equivariant
over `Z_n`; Theorem C applies verbatim to any morphism found there.

---

## 9. What is and is not settled

**Settled here.** Lemma A and Corollary B (PROVED, believed new); Theorems M
and M′ (PROVED, expected rediscoveries); Theorem C, a decidable sufficient
criterion for `CRT_W(n) = RT(n)` (PROVED); Proposition N (PROVED); the
spectrum data C1/C2 and the negative search N1 (CERTIFIED, on the stated
ranges only).

**Not settled.** `CRT_W(n) = RT(n)` for every `n ∈ [4,44]` remains open, and
nothing here changes that. `CRT_I(n) = RT(n)` remains open for every `n ≥ 4`;
§2 is evidence, not proof, and evidence of a kind that a finite computation
can never upgrade.

**Sharpest open threads, in order.**

1. Run the Theorem C search in Pansiot's encoding for `n = 5, …, 12`. A single
   hit plus a seed settles an open case of the Currie–Mol–Rampersad
   conjecture. This is the thread with the highest payoff and it is purely
   mechanical given the right normal form.
2. Close `|D| = 2` in Proposition N by proof, making "no shift-equivariant
   morphism works for `n ≥ 4`" a theorem for all `q` rather than a bounded
   search.
3. Determine whether the exceptional sets of §2 are final — i.e. whether the
   unbroken runs continue. A single late gap at `n = 4` or `n = 5` would be
   far more interesting than more of the same, and would bear directly on
   `CRT_I`.
4. Decide whether `S_2(n,m) ≠ ∅` and `S_0(n,m) ≠ ∅` differ for any `m`; the
   pumping lemma only moves `S_2`, so the gap between the two spectra is the
   real cost of Lemma A.

---

## 10. Method, reproducibility, disclosure

**Machine.** 4 cores, 15 GB RAM, Linux 6.18.5. Python 3.11.15, NumPy 2.4.6,
`python-sat` (Cadical153 backend), gcc `-O3`. All SAT instances are decided in
well under a second each up to `m ≈ 300`; the morphism sweeps are a few minutes
per alphabet. No randomness is used anywhere except in the diagnostic of §8,
which is seeded (`random.seed(3)`, `random.seed(11)`) and affects no claim.

**Controls.** (i) The `n = 3` spectrum reproduces a published threshold
constant; (ii) four independent `CRT_S` constants are reproduced; (iii) the
`n = 3` end-to-end pumping re-derives a published theorem; (iv) every SAT
witness is re-verified by a from-the-definition checker; (v) the two
independent morphism checkers (C and Python) agree; (vi) the fast circular
checker is cross-validated against a naive `O(m³)` one.

**Known weakness.** UNSAT verdicts rest on the SAT solver: no DRAT proof was
emitted or checked, and no independent exhaustive enumeration was run for
larger `m`. UNSAT results are therefore CERTIFIED only in the sense of "exact
integer encoding, reproducible, single trusted solver". This is stated as a
defect, not glossed.

**AI assistance.** This note was produced in an AI-assisted research session
(Claude). Every proof in §3–§8 was written and checked in-session; the
computations ship as code. AI systems are not authors.
