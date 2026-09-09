# Unit-step walks with no three collinear points: seven letters suffice, by the dragon curve

**Session 2026-09-09.** Research note; AI-assisted (Claude), every proof
checked by hand and every computation reproducible from `code/`.

## Abstract

Shallit (arXiv:2609.05780, 5 Sep 2026) proved that there is an infinite walk
in ℕ¹⁶ using only the standard unit steps whose vertices contain no three
collinear points, and asked for the least dimension k_min for which this is
possible, known only to satisfy 4 ≤ k_min ≤ 16. Equivalently (Shallit,
Prop. 1; Korsky, arXiv:2608.07906, §2), k_min is the least alphabet size
admitting an infinite word with no two adjacent nonempty blocks of equal
letter-frequency vector (no *weak abelian square*; we say *3-free*).

We prove **k_min ≤ 7**. The construction is the Heighway dragon curve: let
u_n ∈ {1, i, −1, −i} be its n-th step direction and δ_n ∈ {±1} its n-th turn.
The word b_n = (u_n, δ_n) over eight letters is 3-free (Theorem 1), and it
stays 3-free after the two letters (1, +1) and (−1, +1) are identified
(Theorem 2), which gives seven letters. The proofs are short and elementary:
the dragon curve satisfies the same 2-adic valuation identity as the Gaussian
walk of Cambie–Kalviainen and Shallit whenever the two endpoint directions are
equal, its turns are ±90° only, and two telescoping indicator sums force equal
endpoint directions on any weak abelian square. The eight-letter word is the
fixed point of an explicit 2-uniform morphism.

We also record: (i) an independent review of Kalviainen's unpublished
six-dimensional construction (repository draft, 5 Sep 2026): no gap found, all
its numerical claims reproduced; (ii) exhaustive finite facts — no coding of
the dragon word onto ≤ 6 letters is 3-free beyond length 3000, in the
periodic sign/order family of Gaussian digit walks the letter-coding minimum
is 6, and no cyclic uniform morphism of length ≤ 16 over four letters has a
3-free fixed point beyond length 1500; (iii) growth data suggesting that
3-free words over four letters are unbounded in length, so k_min = 4 is not
excluded by search.

Labels: Theorems 1–2 and Lemmas 1–4 are **PROVED**. The review in §5 is a
reading of someone else's draft, not a result of ours. Every statement in §6
is a finite computation (**CERTIFIED** for the range stated, or **NUMERICAL**
where marked).

## 1. Problem and background

For a finite word x over an alphabet Σ, ψ(x) ∈ ℕ^Σ is its Parikh vector and
|x| its length. Two adjacent nonempty blocks x, y of an infinite word form a
*bad pair* (a weak abelian square) if ψ(x)/|x| = ψ(y)/|y|; the word is
*3-free* if it has no bad pair. Writing P_n = ψ(b_0 ⋯ b_{n−1}) ∈ ℕ^Σ, the
points P_0, P_1, … are the vertices of a unit-step walk, and three of them
P_α, P_β, P_γ (α < β < γ) are collinear iff the blocks b_α⋯b_{β−1} and
b_β⋯b_{γ−1} form a bad pair, because the two displacements are
ψ(x), ψ(y) with coordinate sums |x|, |y| (Shallit, Prop. 1). Hence

  k_min = min{ |Σ| : there is an infinite 3-free word over Σ }.

Known before this session (primary sources read on 2026-09-09):

- Brown (1971): every ternary word of length 8 contains an abelian square,
  so L(3) = 7 and k_min ≥ 4 (a bad pair with |x| = |y| is an abelian square).
- Korsky (arXiv:2608.07906): L(d), the longest 3-free word over d letters,
  satisfies log₂log₂ L(d) ≥ (2/5)d − O(1); no small L(d) is computed.
- Cambie–Kalviainen (arXiv:2609.01766, 1 Sep 2026): an infinite walk in ℤ³
  with sixteen step vectors and no collinear triple, settling Erdős Problem
  193; the tool is the Gaussian walk z_n = Σ_{j<n} i^{s_2(j)} and the
  identity ν₂(|z_n − z_m|²) = ν₂(n − m) when i^{s_2(m)} = i^{s_2(n)}.
- Shallit (arXiv:2609.05780): k_min ≤ 16 via the letters (t_n, t_{n+1}),
  t_n = s_2(n) mod 4; four unproved candidate morphisms for k = 5, 6, 7, 8.
- Unpublished, in the repository github.com/ekalvi/erdos-193 (read
  2026-09-09; not on arXiv; "independent review pending", not formalised):
  Cambie, *A unit-step walk in fourteen dimensions* (5 Sep) — offsets
  identify two pairs of Shallit's sixteen steps; Kalviainen, *A
  six-dimensional unit-step walk with no collinear triple* (5 Sep) — the
  alternating signed rule σ(n) = Σ_j (−1)^j b_j(n) mod 4 has only the turns
  +1, +2, and Cambie's offsets identify two pairs among its eight
  transitions. See §5.

So the state of the art is: 4 ≤ k_min ≤ 16 in the arXiv literature, and
4 ≤ k_min ≤ 6 if the repository drafts are accepted. Our Theorem 2 gives
k_min ≤ 7 by a different mechanism and a self-contained proof; it does not
beat the draft bound 6.

## 2. The dragon walk

Define Gaussian units u_n and the walk Z_n by u_0 = 1, Z_0 = 0,

  u_{2n} = u_n,  u_{2n+1} = i·u_n   if n is even,
  u_{2n} = i·u_n, u_{2n+1} = u_n    if n is odd,        (2.1)
  Z_n = Σ_{j<n} u_j.

Equivalently u_n = i^{t_n} with t_{2n} = t_n + ε_n, t_{2n+1} = t_n + 1 − ε_n
(mod 4), ε_n = n mod 2, t_0 = 0. In every case {u_{2n}, u_{2n+1}} = {u_n, i u_n},
so pairing consecutive terms gives, for ε ∈ {0, 1},

  Z_{2n} = (1 + i) Z_n,   Z_{2n+ε} = (1 + i) Z_n + ε u_{2n}.      (2.2)

**Lemma 1 (turns).** For every n ≥ 0, u_{n+1} = i^{δ_n} u_n with δ_n ∈ {+1, −1}.
Moreover δ_{2m} = (−1)^m and δ_{2m+1} = δ_m.

*Proof.* n = 2m: u_{2m+1}/u_{2m} = i (m even) or i^{−1} (m odd), so
δ_{2m} = (−1)^m. n = 2m + 1: u_{2m+2}/u_{2m+1} = i^{ε_{m+1}} u_{m+1} / (i^{1−ε_m} u_m)
= i^{ε_{m+1} + ε_m − 1} (u_{m+1}/u_m) = u_{m+1}/u_m since ε_m + ε_{m+1} = 1; so
δ_{2m+1} = δ_m, and induction on n (base u_1/u_0 = i) gives δ_n ∈ {±1}. ∎

Consequently t_{n+1} − t_n ∈ {±1}, so t_n ≡ n (mod 2), and (δ_n) is the regular
paperfolding sequence (δ_n = f(n+1) with f(4j+1) = 1, f(4j+3) = −1,
f(2n) = f(n)): the walk Z_n is the Heighway dragon curve, u_n its direction
and δ_n its turn. We only use (2.1), (2.2) and Lemma 1.

For w = x + iy ∈ ℤ[i] write ν(w) = ν₂(|w|²) = ν₂(x² + y²) (ν(0) = ∞). Facts:
ν((1+i)w) = ν(w) + 1; |w|² is odd iff x + y is odd ("odd parity"); a sum of
an odd number of units has odd parity; the sum of two odd-parity elements has
even parity; and 2 = (1+i)(1−i) with (1−i)·(unit) of even parity.

**Lemma 2 (valuation at equal directions).** If 0 ≤ m < n and u_m = u_n,
then Z_n ≠ Z_m and ν(Z_n − Z_m) = ν₂(n − m).

*Proof.* Strong induction on n − m. If n − m is odd, Z_n − Z_m is a sum of an
odd number of units: odd parity, ν = 0. Let n − m be even, m = 2a + ε,
n = 2b + ε, and write ε_a = a mod 2, ε_b = b mod 2. By (2.2),

  Z_n − Z_m = (1+i)(Z_b − Z_a) + ε(u_{2b} − u_{2a}).         (2.3)

By (2.1), u_{2a} = i^{ε_a} u_a, u_{2a+1} = i^{1−ε_a} u_a, and likewise for b.

*Case b − a even.* Then ε_a = ε_b, and u_m = u_n gives u_a = u_b (divide by
the common power of i) and u_{2a} = u_{2b}. The correction in (2.3) vanishes,
and by induction ν(Z_b − Z_a) = ν₂(b − a), so ν(Z_n − Z_m) = 1 + ν₂(b − a) = ν₂(n − m).

*Case b − a odd.* Then ν₂(n − m) = 1, ε_a ≠ ε_b, and Z_b − Z_a is a sum of an
odd number of units, of odd parity. If ε = 0 there is no correction and
ν(Z_n − Z_m) = 1. If ε = 1, the hypothesis u_{2a+1} = u_{2b+1} reads
i^{1−ε_a} u_a = i^{1−ε_b} u_b, so u_b = i^{ε_b − ε_a} u_a and
u_{2b} − u_{2a} = i^{ε_b} u_b − i^{ε_a} u_a = u_a (i^{2ε_b − ε_a} − i^{ε_a}) ∈ {−2u_a, −2i u_a}
(the two cases (ε_a, ε_b) = (0, 1), (1, 0)). Hence
Z_n − Z_m = (1+i)[(Z_b − Z_a) + (1−i)·v] with v a unit; the bracket is the sum
of an odd-parity and an even-parity element, so it has odd parity and
ν(Z_n − Z_m) = 1. ∎

**Lemma 2′.** If u_n ≠ −u_m then ν(Z_n − Z_m) = ν₂(n − m). (If u_n = ±i u_m
then t_n − t_m is odd, so n − m is odd by Lemma 1 and ν = 0.) Only antipodal
endpoint directions escape the identity; §6 shows the defect there is
unbounded in both directions.

**Lemma 3 (two-valued telescoping).** Let a, b, c ∈ {0, 1} and p, q > 0 with
q(a − b) = p(b − c). Then a = b = c.

*Proof.* If b = 1 the left side is ≤ 0 and the right side ≥ 0, so both vanish
and a = c = 1. If b = 0 then qa = −pc forces a = c = 0. ∎

## 3. The eight-letter word and its seven-letter coding

Let Γ = ℤ₄ × {+1, −1} and b_n = (t_n, δ_n) ∈ Γ (direction, turn). Writing the
letter (r, δ) as the digit 2r + [δ = −1], b begins

  0 2 5 2 4 7 5 2 4 6 1 7 4 7 5 2 4 6 1 6 0 3 1 7 4 6 1 7 4 7 5 2 …

**Proposition (morphism).** b is the fixed point, starting from (0, +1), of the
2-uniform morphism on Γ

  (r, δ) ↦ (r, +1)(r+1, δ)   if r is even,
  (r, δ) ↦ (r+1, −1)(r, δ)   if r is odd;

in digits 0 ↦ 02, 1 ↦ 03, 2 ↦ 52, 3 ↦ 53, 4 ↦ 46, 5 ↦ 47, 6 ↦ 16, 7 ↦ 17.

*Proof.* By Lemma 1, ε_n = n mod 2 = t_n mod 2, so (2.1) and Lemma 1 give
b_{2n} = (t_n + ε_n, (−1)^n) and b_{2n+1} = (t_n + 1 − ε_n, δ_n), both functions
of b_n alone, as displayed. The image of (0, +1) starts with (0, +1). ∎
(Checked mechanically against the recursion on 30 000 letters.)

**Theorem 1.** The word b over the eight letters Γ is 3-free. Hence there is
an infinite unit-step walk in ℕ⁸ with no three collinear vertices.

**Theorem 2.** Let τ: Γ → Σ₇ identify the two letters (0, +1) and (2, +1) and
be injective otherwise. The word τ(b) over seven letters is 3-free. Hence
**k_min ≤ 7**: there is an infinite unit-step walk in ℕ⁷ with no three
collinear vertices.

Theorem 1 follows from Theorem 2 (a bad pair of b is a bad pair of τ(b),
since τ acts linearly on Parikh vectors). We prove Theorem 2.

*Proof of Theorem 2.* Suppose x = b_α ⋯ b_{β−1} and y = b_β ⋯ b_{γ−1}
(α < β < γ) satisfy ψ(τx)/p = ψ(τy)/q with p = β − α, q = γ − β. For any
function g on Σ₇, write g(x) = Σ_{j=α}^{β−1} g(τ b_j); then q·g(x) = p·g(y).
We use three such functions; each is well defined on Σ₇ because it takes the
same value on (0, +1) and (2, +1).

(a) *Parity.* g₁(r, δ) = (−1)^r. Since t_{j+1} − t_j is odd, (−1)^{t_j} =
[t_j even] − [t_{j+1} even], and the sum telescopes: g₁(x) = [t_α even] − [t_β even],
g₁(y) = [t_β even] − [t_γ even]. Lemma 3 gives [t_α even] = [t_β even] = [t_γ even].

(b) *Half-plane.* Let H = {0, 1} ⊂ ℤ₄ and g₂(r, δ) = [r ∈ H] − [r + δ ∈ H].
Its values are 0 on (0,+1), (1,−1), (2,+1), (3,−1); +1 on (0,−1), (1,+1);
−1 on (2,−1), (3,+1); in particular g₂(0,+1) = g₂(2,+1) = 0. Since
r + δ = t_{j+1} when r = t_j, the sum telescopes: g₂(x) = [t_α ∈ H] − [t_β ∈ H],
and Lemma 3 gives [t_α ∈ H] = [t_β ∈ H] = [t_γ ∈ H].

Parity and membership in H determine an element of ℤ₄, so **t_α = t_β = t_γ**,
i.e. u_α = u_β = u_γ.

(c) *Right-turn walk.* g₃(r, δ) = (1 − i) i^r if δ = −1 and 0 if δ = +1
(again equal, namely 0, on the two identified letters). Put
W_n = Z_n + ((1+i)/2) u_n. Since u_{n+1} = i^{δ_n} u_n = iδ_n u_n,

  W_{n+1} − W_n = u_n [1 + (1+i)(iδ_n − 1)/2] = 0 (δ_n = +1) or (1 − i) u_n (δ_n = −1),

so g₃(x) = W_β − W_α = (Z_β − Z_α) + ((1+i)/2)(u_β − u_α) = Z_β − Z_α, using
u_α = u_β; likewise g₃(y) = Z_γ − Z_β. Hence, with X = Z_β − Z_α and
Y = Z_γ − Z_β,

  qX = pY,  so  X/p = Y/q = (X + Y)/(p + q) =: V.

(d) *Valuations.* By Lemma 2 applied to the pairs (α, β), (β, γ), (α, γ), all of
which have equal endpoint directions, X, Y, X + Y are nonzero with
ν(X) = ν₂(p), ν(Y) = ν₂(q), ν(X + Y) = ν₂(p + q). Extending ν₂ to positive
rationals, ν₂(|V|²) = ν(X) − 2ν₂(p) = −ν₂(p), and equally −ν₂(q) and
−ν₂(p + q). So ν₂(p) = ν₂(q) = ν₂(p + q) = d; but then p/2^d and q/2^d are
odd and their sum is even, so ν₂(p + q) ≥ d + 1, a contradiction. ∎

The argument is Shallit's Theorem 5 with three changes: the walk (dragon
instead of Gaussian digits), the boundary lemma (two indicator functionals
instead of the full vector e_{t_n} − e_{t_{n+1}}, which is what lets a pair of
letters be merged), and the displacement functional (the right-turn walk W,
which only needs the turn-(−1) letters).

**Remarks.** (1) By the rotation symmetry of the argument, each of the four
identifications (r, δ) ~ (r + 2, δ) works, with H = {r, r + 1} for the
same-turn pair and W (δ = −1) or its mirror W′ = Z + ((1−i)/2)u (which moves
only on left turns) for the displacement. (2) The four identifications
(r, −1) ~ (r + 1, +1) also survive to length 30 000 (§6) but the displacement
functional collapses for them (every affine-in-δ weight i^r(a + bδ) equal on
the two letters has a − ib = 0), so we have no proof. (3) No identification
of two pairs works: §6.

## 4. Where the eight letters come from, and why they do not go lower

Both Shallit's word and ours are instances of *Gaussian digit walks*: at each
binary level one chooses a sign s ∈ {±1} (the children of a direction u are
{u, i^s u}) and an order rule (fixed: (u, i^s u); alternating: the order
depends on the parity of the parent index). Lemma 2 holds level by level for
any such choice — the descent (2.3) only needs the correction term to vanish
or to be 2·(unit) when the parent indices have opposite parity — so every
member gives a 3-free word on its transition alphabet {(t_n, t_{n+1})}.
The number of letters is the number of transitions that occur:

- all levels fixed, constant sign (Shallit): all sixteen;
- all levels fixed, alternating sign (Kalviainen's rule 85): eight,
  turns +1, +2;
- all levels alternating, any signs (the paperfolding curves, this note):
  eight, turns ±1;
- mixed patterns of period ≤ 4: twelve, fifteen or sixteen (§6, `family.c`).

After that, letters can only be merged by a coding, and §6 shows by
exhaustion that the dragon transition word admits no 3-free coding onto
≤ 6 letters (to length 3000) while Kalviainen's admits one onto 6 and none
onto ≤ 5 (to length 1500). So within this family the floor is six, reached
only by the alternating-sign fixed-order rule, and our seven is the floor for
the alternating-order rules.

## 5. Review of Kalviainen's six-dimensional draft (5 Sep 2026)

Source: `paper/unit_step_walk_N6_short.tex` in github.com/ekalvi/erdos-193,
dated 5 Sep 2026, two pages, labelled by its author "exact written argument,
independent review pending, not Lean-formalized". Its claim: an infinite
unit-step walk in ℕ⁶ with no collinear triple, i.e. k_min ≤ 6.

The construction: σ(n) = Σ_j (−1)^j b_j(n) mod 4 (alternating binary digit
sum), u_n = i^{σ(n)}, z_n = Σ_{r<n} u_r; Cambie's offsets (c_0, …, c_3) =
(0, −1, −1+i, −i); w_n = 2z_n + c_{σ(n)}, h_n = 4n + σ(n); Q_n = (Re w_n, Im w_n, h_n) ∈ ℤ³.
Then: (1) σ(m) = σ(n) ⇒ ν₂(|z_n − z_m|²) = ν₂(n − m); (2) for every m < n,
ν₂(|w_n − w_m|²) = ν₂(h_n − h_m); (3) no three Q_n collinear; (4) the
transitions (σ(n), σ(n+1)) are (r, r+1) and (r, r+2) only; (5) the step
vectors (2i^r + c_s − c_r, 4 + s − r) of the eight transitions take six
values, (0,2) and (1,3) sharing (1,1,6), (2,0) and (3,1) sharing (−1,−1,2);
(6) replacing the six vectors by the six unit vectors of ℕ⁶ gives a unit-step
walk whose collinear triples would project to collinear triples of (Q_n).

What we checked, by hand: (1) — the descent. Since σ(2n) = −σ(n) and
σ(2n+1) = 1 − σ(n), u_{2n} = ū_n and u_{2n+1} = i ū_n, so z_{2n+ε} = (1+i) z̄_n + ε ū_n;
equal endpoint states descend to equal states of the halved indices and the
correction cancels, conjugation preserves norms, and after ν₂(n − m) steps
the chord is a sum of an odd number of units. Correct. (2) — the parity
pattern of the offsets: differences between states of opposite parity have
exactly one odd coordinate and h-differences are odd; between the two
antipodal pairs both coordinates are odd and h-differences are ≡ 2 (mod 4);
equal states reduce to (1). Correct (this is Cambie's argument, which we
also read). (3) — the Cambie–Kalviainen slope argument, applied verbatim.
Correct. (4) — if n ends in k trailing 1's then σ(n+1) − σ(n) = (−1)^k −
Σ_{j<k} (−1)^j ≡ 1 (k even) or 2 (k odd). Correct. (5) — recomputed. (6) —
Cambie's projection lemma (T(P_n) = Q_n and heights strictly increase).
Correct.

What we checked, by machine (`code/g85.py`, `code/checkmorph.c`): the six
vectors are exactly those tabulated; identity (2) holds for all 3 123 750
pairs m < n < 2500; the six-letter word is 3-free to length 30 000.

Verdict: we found no gap. The result k_min ≤ 6 rests on this two-page
argument, which we consider correct; the authors' own status label
("independent review pending") is theirs to change, not ours. Our Theorem 2
is therefore not the best known bound; it is an independent proof of a
weaker bound by a different walk. Together, the two mechanisms show that
both eight-transition Gaussian digit walks (alternating sign, alternating
order) are 3-free on their transition alphabets, and that the codings
available to them differ (six for one, seven for the other).

## 6. Computations

All programs are in `code/`, all run on this machine (4 cores, 15 GB, gcc
13.3, Python 3.11); every check is exact integer arithmetic.

**6.1 Controls.** `tf.c` (exhaustive depth-first search over canonical words,
incremental collinearity test) gives L(1) = 1, L(2) = 3, L(3) = 7 with the
unique-up-to-symmetry longest ternary word 0102010, matching Brown 1971 and
the repository's own ternary certificate. **CERTIFIED.**

**6.2 Growth over four and five letters.** The number of canonical 3-free
words over four letters (first letter 0, new letters introduced in order) is
640 at length 10, 41 349 at length 20, 583 081 at length 30, 7 020 567 at
length 40 and 28 861 282 at length 46 (137 189 394 nodes in total, ≈ 5 min;
table in `data/tf4_46.txt`, produced by `./tf 4 46`). The ratio of
consecutive counts, averaged over ten lengths, falls slowly: 1.303 (20→30),
1.283 (30→40), 1.271 (36→46). Over five letters the tree is far wider. No
exhaustive determination of L(4) is possible this way; the growth is
consistent with L(4) = ∞, i.e. with k_min = 4, but a slowly falling ratio is
also what a language that dies out at a great length would show, so this is
**NUMERICAL** (each count is exact, the extrapolation is not).

**6.3 Verification of the constructions.** `checkmorph.c` tests a given word.
The dragon word (8 letters) is 3-free to 30 000; its seven-letter coding τ(b)
to 100 000 (`data/check7a_1e5.txt`); the four-letter direction word t_n fails
at once (1 2 1 2). Lemma 2 was tested on all 1 123 622 pairs m < n < 3000
with u_m = u_n: no failure (`dragon.py`). The defect ν(Z_n − Z_m) − ν₂(n − m)
is 0 on every pair with u_n ≠ −u_m and ranges over [−8, 9] ∪ {∞} on
antipodal pairs below 2048 (`defect.py`). Shallit's four candidates
(k = 5, 6, 7, 8) are 3-free to 20 000; Kalviainen's six-letter word to
30 000. **CERTIFIED** for the ranges stated, evidence only beyond them.

**6.4 Codings of the dragon word.** `codings.c` applies all 4011 set
partitions of the eight letters into 3 … 7 classes and tests 3-freeness to
length 3000. Exactly eight survive, all with seven classes: the four
same-turn antipodal identifications (r, δ) ~ (r+2, δ) (proved, Theorem 2 and
Remark 1) and the four identifications (r, −1) ~ (r+1, +1) (unproved; the
two representatives are 3-free to 30 000). **CERTIFIED:** *every* coding of
b onto at most six letters has a bad pair among its first 3000 letters, so no
letter-to-letter coding of the dragon word can give k_min ≤ 6.

**6.5 The sign/order family.** `family.c` enumerates all periodic patterns of
period ≤ 4 (sign and order rule per level, 128 patterns after symmetry),
builds the transition word to length 1500, and searches all codings onto ≤ 6
classes when the transition alphabet has ≤ 10 letters. Results
(`data/family_1500.txt`): eight-letter transition alphabets occur only for the
all-alternating patterns (minimum coding > 6) and for the fixed-order
alternating-sign pattern (minimum 6, e.g. the coding 01231454 in the order
01,02,12,13,20,23,30,31, which identifies (0,2)~(2,0) and (1,3)~(3,1) — a
different identification from Kalviainen's offsets, and one we have not
proved); the other patterns have 12–16 transitions. A second run
(`data/family12_p3_full.txt`, length 1200, period ≤ 3) shows that none of the
eight- or twelve-letter transition words in the family has a 3-free coding
onto ≤ 5 letters (2 079 475 partitions tested per twelve-letter alphabet).
**CERTIFIED** as finite statements about prefixes of the stated lengths.

**6.6 Cyclic uniform morphisms.** `morphsearch.c` enumerates every cyclic
uniform morphism φ(r) = c + r (mod k) with c_0 = 0 and c itself 3-free, and
tests the fixed point to length 1500. Over four letters, no morphism of
length L ≤ 16 survives (62 634 candidates at L = 16; `data/morph4.txt`). Over
five letters none of length ≤ 13 survives, and at length 14 exactly twelve
of the 16 470 816 candidates survive to 1500, Shallit's 01213101314310 among
them (control passed; `data/morph5_ctrl.txt`; the twelve are not reduced
modulo the symmetries of ℤ₅). Over eight letters and length 6 there are 624
survivors to length 2000, Shallit's 012560 among them. **CERTIFIED** for the
ranges stated.

## 7. Open questions

1. Is k_min = 4? The growth in 6.2 says searches will not decide it; a
   four-letter construction would need a proof mechanism outside the
   Gaussian family (4 states already force 8 transitions there).
2. Prove one of the mixed identifications (r, −1) ~ (r + 1, +1) of §3, or
   Shallit's five-letter candidate; either needs an invariant that is not a
   2-adic valuation of a Gaussian displacement.
3. A lower bound k_min ≥ 5 would need a structural obstruction over four
   letters; nothing in this note points to one.
