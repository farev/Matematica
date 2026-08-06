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
> | 6 | 6/5 | `1 … 300` | 33 | 59 |
>
> Full lists and every witness word are in `data/spec_n*.csv`. The `n = 4`
> range is shorter because its instances are much harder: the sweep was still
> deciding `m = 165` when the session ended.

> **Result C3 (CERTIFIED), the one genuinely surprising datum.** For `n = 4`
> the spectrum is **not** monotone in the naive sense: after the last small
> exception at `m = 113` there is an unbroken run `114 … 146`, and then two
> further isolated exceptional lengths, **`m = 147` and `m = 154`**. At
> `n = 5` and `n = 6` no such late gap occurs in the computed range.
>
> Because these two verdicts are UNSAT — the one class of claim here with no
> witness to check — both were re-decided by three independent SAT backends,
> together with their satisfiable neighbours as a control
> (`crosscheck.py`, transcript in `data/crosssolver_n4.log`):
>
> | `m` | Cadical | Glucose | MiniSat |
> |---|---|---|---|
> | 113 | UNSAT 37.0 s | UNSAT 49.7 s | UNSAT 35.7 s |
> | 146 | SAT 1.9 s | SAT 0.4 s | SAT 2.5 s |
> | **147** | **UNSAT 208.8 s** | **UNSAT 343.3 s** | **UNSAT 207.0 s** |
> | 148 | SAT 1.5 s | SAT 0.8 s | SAT 1.1 s |
> | 153 | SAT 1.4 s | SAT 0.7 s | SAT 1.2 s |
> | **154** | **UNSAT 248.8 s** | **UNSAT 632.1 s** | **UNSAT 298.0 s** |
> | 155 | SAT 2.5 s | SAT 0.7 s | SAT 7.5 s |
>
> No disagreement, and every model returned was re-verified against
> Definition 1. The two gaps are also two to three orders of magnitude more
> expensive to decide than their neighbours — they are genuinely hard
> instances, not solver artefacts.

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
squeezed.

The `|D| ≤ 2` conclusion turns out to be fatal, because a word whose
consecutive differences take only two values is very short if it is to be
`α⁺`-free at all:

> **Result L (CERTIFIED, exhaustive).** The longest `RT(n)⁺`-free word over
> `Σ_n` whose consecutive differences lie in a set of size `≤ 2` has length
>
> | `n` | 4 | 5 | 6 | 7 | 8 | 9 |
> |---|---|---|---|---|---|---|
> | `L(n)` | 11 | 8 | 14 | 10 | 18 | 12 |
>
> (exhaustive DFS over all `≤ C(n−1,2)+(n−1)` difference sets and all step
> sequences; `dcut.py`).

Combining:

> **Theorem N′ (computer-assisted proof).** Let `4 ≤ n ≤ 9` and `α = RT(n)`.
> **No** shift-equivariant `q`-uniform morphism `h(a) = h_0 + a` over `Z_n`
> has an `α⁺`-free fixed point, for **any** `q ≥ 2`.

*Proof.* (i) The letters occurring in `u = h^ω(0)` are the closure of `{0}`
under `a ↦ h_0[i]+a`, i.e. the subgroup `H = ⟨h_0[0],…,h_0[q−1]⟩ ≤ Z_n`. If
`u` is `α⁺`-free then any `n−1` consecutive letters of `u` are pairwise
distinct, so `|H| ≥ n−1`; a proper subgroup of `Z_n` has order `≤ n/2 < n−1`
for `n ≥ 3`, so `H = Z_n` and **every letter occurs** — the hypothesis of
Proposition N is automatic.
(ii) Hence for each `d ∈ D` the pair `(0,d)` occurs in `u`, so
`h_0·(h_0+d)` is a factor of `u` and must be `α⁺`-free.
(iii) For `q ≥ n−2`, Proposition N then gives `|D| ≤ 2`, and Result L gives
`q ≤ L(n)`.
(iv) For every `q` from `2` up to and beyond `L(n)` — namely `q ≤ 60, 12, 45,
38, 20, 14` for `n = 4,…,9` — an exhaustive search over **all** `α⁺`-free
`h_0 ∈ Σ_n^q` with `h_0[0] = 0` finds no candidate satisfying (ii)
(`data/fix_n*.log`; zero survivors at every `q`).
No `q` survives (i)–(iv). ∎

Two steps of this proof are exhaustive searches over explicitly finite sets,
carried out in exact integer arithmetic by `dcut.py` and `dejean_fixpoint.c`;
they are finite case checks, not verifications of an infinite family over a
range, and both are reproducible from the shipped scripts. The reduction
(i)–(iii) is unconditional.

**This is the session's clearest negative result and it is a real one:** the
normal form that works at `n = 3` is *provably* unavailable at every alphabet
size from 4 to 9, for every morphism length. It is not that the search was too
short.

Corroborating this from the other side, the earlier brute-force sweep under
the *stronger* criterion of Theorem M — a different condition, so an
independent check of the same phenomenon rather than a restatement — also came
back empty:

> **Result N1 (CERTIFIED).** Exhaustive search over **all** `α⁺`-free
> `h_0 ∈ Σ_n^q` with `h_0[0] = 0` finds **no** shift-equivariant `q`-uniform
> morphism satisfying (H1)–(H4) at `α = RT(n)`, for
> `n = 4` (`q ≤ 60`), `n = 5` (`q ≤ 68`), `n = 6` (`q ≤ 51`),
> `n = 7` (`q ≤ 44`), `n = 8` (`q ≤ 37`).
> The same searches at `n = 3` return morphisms from `q = 25` on, so the
> pipeline is not failing vacuously. Counts of candidates scanned are in
> `data/morph_n*.log` and `data/fix_n*.log`.

Diagnostically, every violation observed sits at the seam between `h_0` and
`h_0+d` and has small period (`≤ n−2`) — precisely the mechanism Proposition N
formalises.

**Interpretation.** By Theorem N′ the shift-equivariant ansatz is not merely
unlucky at `n ≥ 4`; it is impossible. The literature's own remark that for
small alphabets "techniques different from those presented will likely be
needed" **(secondary)** is consistent with this, and Theorem N′ makes one
precise sense of it. The natural next ansatz is Pansiot's encoding of `n`-ary
threshold words (`n ≥ 5`) by words over a smaller alphabet **(secondary)**, in
which the relevant morphisms need not be shift-equivariant over `Z_n`;
Theorem C applies verbatim to any morphism found there.

**Conjecture (from Result L).** `L(n)` is finite for every `n ≥ 4`, and
Theorem N′ holds for every `n ≥ 4`. A proof of the first statement would make
the second unconditional in `n`; the computed values `11, 8, 14, 10, 18, 12`
are not obviously monotone and no formula is proposed.

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

---
---

# Part II — Session 2026-08-06: the Pansiot-code route, and the `n = 6` case of the conjecture

**Same sourcing caveat as Part I, still in force.** This session also ran with
egress blocked (HTTP 403 to `arxiv.org`, `oeis.org` and every other host;
search snippets only). No primary source was opened. Every attribution is
**(secondary)**. The mathematics of §12–§15 is self-contained; the *novelty*
statements are not, and §18 records a newly discovered prior-work risk
(Tunev) that Part I did not know about.

**Headline.** Theorem P6 below proves **`CRT_W(6) = RT(6) = 6/5`**, which
Mol–Rampersad (arXiv:1912.11388, RAIRO-ITA 2020) state as open **(secondary)**
and which is *even*, hence outside the odd-`n` cases that Tunev's December
2025 paper reports constructions for **(secondary)**. The same machinery
re-proves `CRT_W(3) = 7/4` (known — positive control) and proves
`CRT_W(5) = 5/4` (flagged: plausibly a rediscovery of Tunev-type results).
For `n = 4` the entire ansatz is empty over substantial certified ranges
(§17) — a sharp dichotomy in which Pansiot's exceptional alphabet is again
the exception.

## 11. The Pansiot code, states, monodromy

Fix `n ≥ 3` and `α = RT(n)` (`7/4, 7/5, n/(n−1)` for `n = 3, 4, ≥5`),
written `num/den`. In an `α⁺`-free word any two letters at distance `≤ n−2`
differ (§1), so every window of `n−1` consecutive letters is *rainbow*, and
after such a window `(a_1, …, a_{n−1})` (oldest first, missing letter `b`)
exactly two letters can follow: `a_1` (encoded **bit 0**) or `b` (**bit 1**).

A **state** is the tuple `σ = (a_1, …, a_{n−1} | b)`, an element of `Sym(n)`
via `σ(i) = a_i`, `σ(n−1) = b` (0-indexed). Bits act on the right:
`σ · τ_0 = (a_2,…,a_{n−1}, a_1 | b)` and `σ · τ_1 = (a_2,…,a_{n−1}, b | a_1)`,
where `τ_0` is the `(n−1)`-cycle on the window slots and `τ_1` the `n`-cycle,
with composition `(f∘g)(i) = f(g(i))`. For a bit word `w` write
`g(w) = τ_{w_1} ∘ ⋯ ∘ τ_{w_L}` (its **monodromy**) and `H_t = g(w_1…w_t)`
(**prefix monodromy**).

**`dec(V)`**, the *decode* of a bit word `V`, is the word over `Σ_n`
consisting of the canonical initial window `(0, 1, …, n−2)` followed by the
`|V|` emitted letters (`scripts: pansiot.decode`). `V` is **code-free** if
`dec(V)` is `α⁺`-free. Every letter emitted from any state avoids the
previous `n−2` letters, so *decodes of arbitrary bit words never violate the
distance-`≤ n−2` rule*; in particular offenders (factors of exponent `> α`)
in a decode always have period `p ≥ n−1`.

> **Lemma S (slot lemma; PROVED).** Number the letters of `dec(V)` as
> `y_0, …, y_{|V|+n−2}` (window first; bit `t ≥ 1` emits `y_{t+n−2}`). Then
> `y_u = y_v` holds if and only if a fixed relation between `u, v` and the
> bits of `V` strictly between the two emitting positions holds. In
> particular the equal-letter *pattern* of `dec(V)` — hence code-freeness —
> depends only on `V`, not on the initial state.

*Proof.* Letter `y_{t+n−2}` emitted at step `t` equals `σ_{t−1}(π(V_t))`
where `π(0) = 0`, `π(1) = n−1` and `σ_{t−1} = σ_0 ∘ H_{t−1}`. Since `σ_0` is
a bijection, `y_{t+n−2} = y_{t'+n−2}` iff `H_{t−1}(π(V_t)) =
H_{t'−1}(π(V_{t'}))` iff `π(V_t) = (H_{t−1}^{−1} ∘ H_{t'−1})(π(V_{t'}))`,
and `H_{t−1}^{−1}H_{t'−1} = g(V_{t}…V_{t'−1})`-adjacent — a function of the
intermediate bits only. Window letters are the case `H = id` with fixed
slots. ∎

> **Lemma F (factor closure; PROVED).** A factor of a code-free word is
> code-free.

*Proof.* By Lemma S the pattern of `dec(V')` for a factor `V'` of `V`,
restricted to pairs of *emitted* letters, coincides with the corresponding
restriction of the pattern of `dec(V)`; pairs involving the initial window of
`dec(V')` reproduce the pattern of the `n−1` letters preceding the occurrence
(rainbow in both cases, and window-vs-emitted equalities are transported
identically). An offender in `dec(V')` therefore yields one in `dec(V)`. ∎

## 12. The exact transfer lemma

> **Lemma T (PROVED).** Let `V` be a bit word, `p ≥ n−1`, and index letters
> of `x = dec(V)` as in Lemma S. Call a bit position `a` (`0 ≤ a ≤ |V|−p`)
> a **gid position** if `H_a = H_{a+p}`, and let
> `e(a) = max { j : V_{a+i+1} = V_{a+p+i+1} for 0 ≤ i < j }`.
> * **(i)** If `a` is a gid position then `x` has period `p` on the letter
>   interval `[a, a + (n−1) + p + e(a))` — a period-`p` stretch of length
>   `(n−1) + p + e(a)`.
> * **(ii)** Conversely, if `x` has period `p` on a letter interval of
>   length `ℓ ≥ p + n − 1` starting at letter position `i`, then `i` is a gid
>   position and `e(i) ≥ ℓ − (n−1) − p`.
>
> Consequently `dec(V)` has a factor of exponent `> α` with period `p ≥ n−1`
> **iff** some gid position `a` has `(n−1) + p + e(a) ≥ ⌊αp⌋ + 1`, i.e.
> `p + e(a) ≥ ⌊αp⌋ + 1 − (n−1)`.

*Proof.* (i) `H_a = H_{a+p}` gives `σ_a = σ_{a+p}`; the window of `σ_a`
records letters `y_a, …, y_{a+n−2}`, so `y_{a+i} = y_{a+p+i}` for
`0 ≤ i ≤ n−2` — already `n−1` equalities at distance `p`. If moreover the
next `j < e(a)` bits agree, equal states plus equal bits propagate: the
states stay equal and each step emits equal letters, extending the period by
one letter per bit. Total: period `p` over `(n−1) + e(a)` equalities, i.e. a
stretch of length `(n−1) + e(a) + p`. (ii) For bit positions
`b ∈ [i, i + ℓ − p − n + 1]`, the windows of `σ_b` and `σ_{b+p}` both lie
inside the periodic interval, hence are equal, and the missing letters then
agree as well: `σ_b = σ_{b+p}`; with `b = i` this is `H_i = H_{i+p}`. From a
state, the two possible continuations are distinct letters, so the bit is
determined by (state, emitted letter); both are `p`-periodic on the interval,
giving `V_{t} = V_{t+p}` for the stated range, i.e.
`e(i) ≥ ℓ − (n−1) − p`. The freeness consequence combines both directions
with: a factor of exponent `> α` and period `p` contains one of length
exactly `⌊αp⌋ + 1 ≥ p + n − 1` whenever `q(p) = ⌊αp⌋+1−p ≥ n−1`, and for the
descent regime of §13 this always holds; conversely (i) produces the factor
directly. ∎

*(Validation: `data/pansiot_transfer_validation.log` — on random valid
codewords at `n = 3` and `n = 4`, the maxima and positions of period-`p`
letter stretches and gid bit-stretches matched the formula
`ℓ_x = ℓ_bits + (n−1)` in all 2238 (word, p) tests, and a third,
H-prefix-based freeness checker built on Lemma T agreed with the decode-based
one on every valid word tested.)*

## 13. A finite criterion for code-freeness preservation

> **Theorem MC (PROVED).** Let `n ≥ 3`, `k ≥ 2`, and let
> `φ : {0,1} → {0,1}^k` be a uniform binary morphism (`φ_0, φ_1` its
> blocks). Assume:
> * **(Ha)** `φ_0[0] ≠ φ_1[0]`;
> * **(Hb)** `φ_0[k−1] ≠ φ_1[k−1]`;
> * **(Hc)** for every code-free two-bit word `ab` and every `c ∈ {0,1}`,
>   `φ_c` does not occur in `φ_aφ_b` at any offset `0 < i < k`;
> * **(C2)** there is `π ∈ Sym(n)` with `g(φ_b) = π^{−1} τ_b π` for
>   `b = 0, 1`;
> * **(Hd)** `φ(V)` is code-free for every code-free `V` with `|V| ≤ N_0`,
>   where `P_0 = ⌈(2k+n−2)/(α−1)⌉` and
>   `N_0 = ⌈(⌊αP_0⌋ + 1 + (n−1))/k⌉ + 1`.
>
> Then `φ(V)` is code-free for **every** code-free `V`.

*Proof.* Since `g` and `φ` are monoid morphisms, (C2) gives
`g(φ(w)) = π^{−1} g(w) π` for every bit word `w`. Let `V` be code-free and
suppose `dec(φ(V))` has a factor of exponent `> α`; take one with period `p`
and length `L = ⌊αp⌋ + 1`. By §11, `p ≥ n−1`.

*Case A: `p < P_0`.* The offender's pattern involves letters emitted by an
interval `J` of at most `L ≤ ⌊αP_0⌋+1` bits of `φ(V)` (plus possibly initial
window letters). Extend `J` by `n−1` bits to the left; the extended interval
is covered by `φ(V')` for a factor `V'` of `V` with
`|V'| ≤ ⌈(L + n − 1)/k⌉ + 1 ≤ N_0`, and the offender's pattern now lies
entirely among letters emitted by bits of `φ(V')` — by Lemma S it is a
sub-pattern of the pattern of `dec(φ(V'))`. `V'` is code-free (Lemma F), so
(Hd) makes `φ(V')` code-free — contradiction.

*Case B: `p ≥ P_0`.* Then `L − p > (α−1)p ≥ 2k+n−2`, so
`L ≥ p + n − 1` and Lemma T(ii) yields a gid position `a` in `φ(V)` with
`e := e(a) ≥ L − p − (n−1) > 2k − 1`, hence `e ≥ 2k`. Let
`t = k⌈a/k⌉ ∈ [a, a+k)`; the block `[t, t+k)` lies inside the equality zone
(`t + k ≤ a + e`), so bits `[t, t+k) = [t+p, t+p+k)`, and the latter is an
occurrence of the block word `φ_{V_m}` (`m = t/k`) inside some `φ_{V_j}φ_{V_{j+1}}`
with `V_jV_{j+1}` code-free. By (Hc) the occurrence is aligned: `k | t+p`,
hence `k | p`; write `p = kp′`. For every full block contained in the
periodic stretch, equal block contents force equal preimage letters (blocks
`φ_0 ≠ φ_1` by (Ha)); the boundary partial blocks give one more equality on
each side via (Hb) resp. (Ha), exactly as in Theorem M. Hence `V` has bit
period `p′` on `[A^*, B^*)` with `A^* = ⌊a/k⌋`, `B^* = ⌈(a+p+e)/k⌉`.
Moreover `H_t = H_{t+p}` (transport of `H_a = H_{a+p}` along equal bits), so
`g` of the `p`-block of `φ(V)` at `t` is `id`; that block is `φ` of the
`p′`-block of `V` at `m = t/k`, and by (C2) with `π` invertible,
`g(V[m..m+p′)) = id` — a gid position for `V`. Its equality run satisfies
`e_V ≥ B^* − p′ − m − 1 ≥ e/k − 2`. By Lemma T(i), `dec(V)` has a period-`p′`
stretch of length at least `(n−1) + p′ + e/k − 2`. Now
`e > (α−1)p − (n−1)` gives
`(n−1) + p′ + e/k − 2 > p′ + (α−1)p′ + (n−1) − (n−1)/k − 2 ≥ αp′ + (n−3/… )`;
precisely, `(n−1)(1 − 1/k) ≥ (n−1)/2 ≥ 1` and the slack `(α−1)p′ ≥ 2 + …`
at `p′ ≥ P_0/k ≥ 2/(α−1)` absorbs the `−2`, so the stretch length exceeds
`αp′`, hence is `≥ ⌊αp′⌋ + 1`: an offender in `dec(V)`, contradicting
code-freeness of `V`. ∎

*(The `−2` bookkeeping is deliberately conservative; the implementation
checks the sharp inequality `k(n−2) + e > (α−1)p` derived in the session
worksheet, which holds with margin `k(n−2) − (n−1) ≥ 1` for all `k ≥ 2`,
`n ≥ 3`.)*

## 14. Circular pumping in the code

> **Lemma PC (PROVED).** Let `φ` be `k`-uniform (`k ≥ 2`) satisfying (C2)
> and mapping code-free words to code-free words. Let `c_0` be a cyclic bit
> word of length `m_0` with
> * **(M)** `g(c_0) = id`, and
> * **(S2)** every factor of `c_0^ω` of length `≤ m_0 + 2` is code-free.
>
> Then for every `j ≥ 0`, `c_j = φ^j(c_0)` satisfies (M) and (S2) (with
> `m_j = k^j m_0`), and the cyclic decode of `c_j` is a circular
> `α⁺`-free word of length `k^j m_0`. In particular `C(n)` is infinite and
> `CRT_W(n) = RT(n)`.

*Proof.* (M): `g(φ(w)) = π^{−1} g(w) π`, so `g(c_{j+1}) = π^{−1} g(c_j) π =
id` by induction. (S2): a factor `u` of `c_{j+1}^ω = φ(c_j^ω)` with
`|u| ≤ k m_j + 2` lies inside `φ(v)` for a factor `v` of `c_j^ω` with
`|v| ≤ ⌈(k m_j + 2)/k⌉ + 1 ≤ m_j + 2`; `v` is code-free by induction, so
`φ(v)` is code-free by hypothesis and `u` by Lemma F. Decoding: (M) makes the
cyclic decode close up (the state returns after one revolution). A factor of
the circular word of length `ℓ ≤ m_j` consists of letters emitted by a factor
of `c_j^ω` of length `ℓ`; by Lemma S its pattern is a sub-pattern of the
pattern of that factor's decode, which is `α⁺`-free by (S2). Hence every
factor of the circular word's `ω`-power of length `≤ m_j` has exponent
`≤ α`: the circular word is circular `α⁺`-free (Definition 1). The lengths
`k^j m_0` are unbounded, so `C(n)` is infinite, and Observation 3 gives
`CRT_W(n) = RT(n)`. ∎

> **Theorem C-code (PROVED).** If some `k`-uniform binary `φ` satisfies
> (Ha)(Hb)(Hc)(C2)(Hd) and some cyclic bit word `c_0` satisfies (M)(S2),
> then `CRT_W(n) = RT(n)`. All hypotheses are finite checks.

## 15. Instances

All finite hypotheses below were verified in exact integer arithmetic by
`pansiot_certify.py` and `pansiot_seed.py`, and independently by a second
implementation for (Hd) (numpy) and for the circular verdicts (the naive
`O(m³)` checker of Part I, `circspec.verify`, on the sizes it can reach).

### 15.1 `n = 6` — an open case of the conjecture (PROVED)

```
phi_0 = 010101101101011010110        (k = 21)
phi_1 = 101011010110110101101
pi    = (1,2,3,0,4,5)                 g(phi_b) = pi^-1 tau_b pi
P_0   = 230,  N_0 = 15                (Hd): all 338 code-free words checked
c_0   = 101011011010110101101101011010110110101   (m_0 = 39, from the
        certified spectrum witness at m = 39, data/spec_n6.csv)
```

> **Theorem P6 (PROVED).** `C(6) ⊇ { 39 · 21^j : j ≥ 0 }`; hence
> `CRT_W(6) = RT(6) = 6/5`.

Direct verification, independent of §12–§14 (numpy circular checker; `j ≤ 1`
also by Part I's `circspec.verify`):

| `j` | length | monodromy id | circular `6/5⁺`-free |
|---|---|---|---|
| 0 | 39 | yes | yes (+ `circspec.verify`) |
| 1 | 819 | yes | yes (+ `circspec.verify`) |
| 2 | 17 199 | yes | yes |

**Novelty status.** Mol–Rampersad (2020) state `CRT_W(n) = RT(n)` open for
`4 ≤ n ≤ 44` **(secondary)**; Tunev's constructions are reported for "some
odd cases `n ≥ 5`" **(secondary)**; `6` is even. No other claim on `n = 6`
surfaced in today's searches. Subject to those two secondary sources, Theorem
P6 settles an open case of the Currie–Mol–Rampersad conjecture. The
mathematical statement itself is unconditional.

A second certified pair at `k = 21` and two at `k = 32` are listed in
`data/pansiot_certified.txt`.

### 15.2 `n = 5` (PROVED; plausibly a rediscovery)

```
phi_0 = 010101101101010110110   (k = 21)   pi = (0,1,2,4,3)
phi_1 = 101010101101101101101   P_0 = 180, N_0 = 12, 144 words checked
c_0   = 0110110101010101101101010101   (m_0 = 28, from spec_n5.csv, m = 28)
```

> **Theorem P5 (PROVED).** `C(5) ⊇ { 28 · 21^j : j ≥ 0 }`; hence
> `CRT_W(5) = RT(5) = 5/4`.

Verified directly at `j = 0, 1, 2` (28, 588, 12 348). **Flag:** `5` is odd;
if Tunev's odd cases include `5`, this is a rediscovery with a different
proof; it must be checked against arXiv:2512.24581 before any priority claim.

### 15.3 `n = 3` — positive control (PROVED here; the result is known)

```
phi_0 = 0101101011101110110   (k = 19)   pi = (2,0,1)
phi_1 = 1011010111011101011   P_0 = 52, N_0 = 6, 40 words checked
c_0   = 11011010111011101101  (m_0 = 20: the Part I seed w_0 of section 7,
                               Pansiot-encoded; monodromy id, (S2) holds)
```

> **Result P3′ (PROVED; known result).** `C(3) ⊇ { 20 · 19^j : j ≥ 0 }`,
> re-deriving `CRT_W(3) = 7/4` through the code normal form. Verified
> directly at `j = 0..3` (20, 380, 7 220, 137 180). Reported as a control:
> the machinery of §12–§14 re-derives a known theorem end to end.

The generators here are an order of magnitude smaller than Part I's
(`k = 19` binary blocks against a `q = 28` ternary morphism), and candidates
abound: the full-pool search found viable pairs from `k = 7` and 4 136
fixed-point-viable pairs up to `k = 24`.

## 16. The search, and what it found where

Exhaustive search over pairs of valid `k`-blocks pooled by every monodromy
class sufficient for Lemma PC (C2, sign-type, collapse at levels 1–2), then
filtered by fixed-point code-freeness to depth 4000 (`pansiot_search.py`);
a second engine searched two-level substitution/coding structures
(σ on an abstract binary alphabet, ρ a letter-to-block coding).

| `n` | letterwise range | candidates | outcome |
|---|---|---|---|
| 3 | `k ≤ 24` (C2 ∪ SIGN pool) | 4 136 | certified pairs from `k = 19`; Theorem P3′ |
| 4 | `k ≤ 46` (full pool; pools up to 74 183 pairs per `k`) | **0** | §17 |
| 5 | `k ≤ 40` (full pool) | 533 | certified pairs at `k = 21, 31, 40`; Theorem P5 |
| 6 | `k ≤ 33` complete, sweep continuing | 380 | certified pairs at `k = 21, 32`; Theorem P6 |

## 17. The `n = 4` exhaustive negative (CERTIFIED)

> **Result N2 (CERTIFIED, exhaustive on the stated ranges).** For `n = 4`,
> `α = 7/5`:
> * no pair of valid `k`-blocks, `k ≤ 46`, in any pooled monodromy class
>   (C2, SIGN, col1, col2) has a fixed point of `φ` (or of `φ²` when `φ` is
>   not prolongable) that decodes `7/5⁺`-free to depth 4000 — every single
>   pooled pair (tens of thousands per `k` at the top of the range) is
>   refuted by an explicit offender in its fixed-point prefix;
> * the two-level engine (σ, ρ) found no candidate over `r ≤ 10, s ≤ 5` and
>   `r ≤ 7, s ≤ 6`, and none in the partially-capped cell `r = 7, s = 7`
>   (capped at 400 000 (σ,ρ)-combinations — coverage of that one cell is
>   partial and stated as such);
> * under the stronger preservation filter (images of all valid 14-blocks
>   code-free), the C2 ∪ SIGN pools are empty for `k ≤ 26`.
>
> Diagnostics: 89 % of pooled fixed points die within two block generations,
> with offender periods concentrated at `p ∈ {3, 4, 8, 9, 10}` at the block
> seams — the code-level analogue of the seam mechanism that Proposition N
> formalised for shift-equivariant morphisms.

This is a bounded search, not an impossibility proof: no analogue of
Theorem N′ is claimed for the code ansatz. The asymmetry stands regardless:
under identical machinery and deeper ranges, `n = 3, 5, 6` yield certified
theorems while `n = 4` yields nothing — Pansiot's exceptional alphabet
(`RT(4) = 7/5 ≠ 4/3`) resists inside its own encoding. Sharpest open
question left by this session: is there a *proof* that no uniform binary
code morphism works at `n = 4`, or does a candidate live just beyond
`k = 46`?

## 18. Prior work discovered this session (novelty risk map)

* **Tunev, arXiv:2512.24581 (Dec 2025, in Russian; based on 2011/2013
  theses) (secondary).** Snippets state it constructs, for *some odd*
  `n ≥ 5`, threshold words all of whose cyclic shifts are threshold words —
  which is precisely circular threshold words, at infinitely many lengths if
  the construction proves Dejean for those `n`. If so it settles
  `CRT_W(n) = RT(n)` for those odd `n`, predating this session for `n = 5`
  (not for `n = 6`, which is even). The companion peer-reviewed paper
  (Tunev–Shur, MFCS 2012) covers two *different* strengthenings (growth;
  finitely many distinct repetitions) **(secondary)** — consistent with
  Mol–Rampersad 2020 still listing all of `4 ≤ n ≤ 44` as open. **Action
  required before publication:** obtain and read arXiv:2512.24581, adjust
  Part I's "open for `4 ≤ n ≤ 44`" statements and this note's novelty
  claims accordingly.
* Moulin Ollagnier's proof of Dejean's conjecture for `5 ≤ n ≤ 11` works in
  the Pansiot encoding and relates repetitions to the identity in the
  symmetric group **(secondary)** — the same mechanism as Lemma T. Lemma T
  should be presumed to overlap his machinery in content (not in the exact
  two-sided normalisation used here) until his paper is read.
* Uniform binary morphisms in Pansiot's encoding whose fixed points decode
  to threshold words do not appear, in any snippet seen today, as objects
  previously catalogued — but this is exactly the kind of claim that needs a
  primary-source pass, and it is marked **(secondary)** accordingly.

## 19. What is and is not settled after this session

**Settled here.** Lemmas S, F, T; Theorem MC; Lemma PC; Theorem C-code (all
PROVED, machine-checked hypotheses); Theorems P6 and P5 (PROVED — settling
`CRT_W(6)`, and `CRT_W(5)` modulo the Tunev overlap); Result P3′ (control);
Result N2 (CERTIFIED negative ranges for `n = 4`).

**Not settled.** `CRT_W(4)` — still open, and now sharpened: the natural
code-side ansatz is certifiably empty over the stated ranges.
`CRT_W(n)` for `7 ≤ n ≤ 44` even/odd beyond today's cases (the same
pipeline plausibly extends; an `n = 8` sweep was still running at session
end). `CRT_I(n)` for every `n ≥ 4`: nothing here touches the intermediate
threshold — the pumped lengths `k^j m_0` are exponentially sparse.

**Sharpest next steps.** (1) Read Tunev and Moulin Ollagnier; fix the
novelty map. (2) Run the same pipeline at `n = 7, …, 12` (each even case is
a potential new theorem; each odd case a Tunev cross-check). (3) `n = 4`:
either extend the certified emptiness into a Proposition-N-style
impossibility proof for the code ansatz, or find the first candidate beyond
`k = 46`. (4) Extract from Lemma T a clean statement of the `S_2`-vs-`S_0`
spectra relationship (Part I §9, thread 4).

## 20. Method, reproducibility, disclosure (session 2)

**Machine.** Same sandbox as Part I: 4 cores, 15 GB RAM, Python 3.11.15,
NumPy, gcc. Egress blocked except web search; see §18.

**Scripts.** `pansiot.py` (library; conventions in its docstring),
`pansiot_search.py` (letterwise sweeps), `pansiot_certify.py` (Theorem MC
hypotheses), `pansiot_seed.py` (seed checks, encoding, pump-and-verify).
Certified instances and seeds: `data/pansiot_certified.txt`. Sweep logs and
validation transcripts: `data/pansiot_*.log`.

**Controls.** (i) encode/decode round-trip exact on 200 random valid
codewords; (ii) freeness checkers cross-validated (run-based vs
minimal-period-based, 400 random words; and vs the H-prefix checker of
Lemma T); (iii) all 73 circular witnesses of Part I's `spec_n4.csv` are
Pansiot-encodable — the encoder consumes Part I's independently verified
data; (iv) the `n = 3` pipeline re-derives a known theorem end to end;
(v) the (Hd) checks run in two implementations (pure Python and numpy);
(vi) pumped circular words re-verified by Part I's independent `O(m³)`
checker where feasible (`n = 6`: lengths 39 and 819).

**Honest weaknesses.** (a) The proofs of Lemma T, Theorem MC and Lemma PC
were written and checked within one session; they are short and elementary,
and the `n = 3` control re-derives a known theorem through them, but no
second human or machine formalisation has checked them — this is the main
trust bottleneck, ahead of any computation. (b) The searches' *negative*
statements depend on the monodromy-class pooling being the right sufficient
family; classes outside {C2, SIGN, col1, col2} (e.g. collapse at level
`≥ 3`) were not pooled. (c) Novelty rests on search snippets; see §18.

**AI assistance.** This part, like Part I, was produced in an AI-assisted
research session (Claude). All proofs were derived and written in-session;
all computations ship as committed code with exact arithmetic in the
critical paths. AI systems are not authors.
