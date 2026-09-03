# The Bit Deletion game: a complete Sprague–Grundy analysis

*Research note, 2026-09-03. AI assistance (Claude) was used throughout; every
proof below was checked by hand and every computational claim ships code.*

## Abstract

The Bit Deletion game (OEIS A398916, Do Thanh Nhan, 14 Aug 2026) is played on
a positive integer written in binary: a move deletes one binary digit, leading
zeros are then discarded, and the player who removes the last nonzero digit
wins. We determine the Sprague–Grundy function completely. Writing the binary
expansion as `1 0^{z_1} 1 0^{z_2} 1 ⋯ 1 0^{z_{m+1}}` (blocks may be empty),
let `L` be the number of binary digits and `t` the number of *initial* blocks
of odd length. Then

    G(n) = (L mod 2) + 2·[t is odd].

This proves both conjectures recorded in A398916 (`G(n) ≤ 3` for all `n`, and
`G(4n) = G(n)`), gives the exact distribution of values (exactly one quarter of
the `L`-bit numbers, `L ≥ 3`, have value 2 or 3), and settles the misère form:
the misère P-positions are exactly the positions of normal Grundy value 1. The
outcome classes (Corollary 2) turn out to be folklore among solvers of Project
Euler Problem 961, which is the decimal form of the same game; the Grundy
values, the bound, the `4n` invariance and the misère analysis are new. Both
theorems are additionally verified by exhaustive computation for all
`n < 2^32`.

## 1. The game and notation

**Positions.** Nonnegative integers. From `n ≥ 1` with binary expansion
`d_1 d_2 ⋯ d_L` (`d_1 = 1`) a move deletes one digit `d_i`; the remaining
`L − 1` digits, read as a binary numeral with leading zeros discarded, form the
new position. The position `0` has no moves. Normal play: the player who moves
to `0` (removes the last nonzero digit) wins.

`G(n)` denotes the Sprague–Grundy value, `G(0) = 0`,
`G(n) = mex{G(n') : n' an option of n}`.

**Block decomposition.** For `n ≥ 1` write `bin(n) = 1u` with
`u ∈ {0,1}^{L−1}`, and decompose `u` by its ones:

    u = 0^{z_1} 1 0^{z_2} 1 ⋯ 1 0^{z_{m+1}},   m = number of ones in u,  z_i ≥ 0.

Empty blocks are allowed: `z_1` is the number of zeros before the first one of
`u`, `z_{m+1}` the number after the last one; if `m = 0` then `u = 0^{z_1}`.
Define

    t(u) = max{ t ≥ 0 : z_1, …, z_t are all odd }   (0 ≤ t ≤ m+1),
    h(u) = t(u) mod 2,
    P(u) = (|u| + 1) mod 2 = L mod 2.

Two facts used constantly: `h(0^z) = [z odd]`, and for `m ≥ 1`, with
`u = 0^{z_1} 1 v`,

    h(u) = [z_1 odd] · (1 − h(v)).                                      (1)

(If `z_1` is even then `t(u) = 0`; if `z_1` is odd then `t(u) = 1 + t(v)`.)

**Options in this notation.** From `n = 1u`:

- **(D)** delete a digit of `u`: the option is `1u_i`, where `u_i` is `u`
  with its `i`-th character removed; `|u_i| = |u| − 1`, so `P(u_i) = 1 − P(u)`.
- **(J)** delete the leading one: if `m ≥ 1` and `u = 0^{z_1} 1 v`, the
  option is the number `1v`; since `L(1v) = |u| − z_1`, we get
  `P(v) = P(u)` iff `z_1` is odd. If `m = 0` the option is `0`.

## 2. Main theorem

**Theorem 1.** For every `n ≥ 1`, with `u`, `L`, `t` as above,

    G(n) = (L mod 2) + 2·[t(u) odd] = P(u) + 2h(u).

In particular `G(n) ∈ {0,1,2,3}`, `G(n) ≡ L (mod 2)`, and the value is `≥ 2`
exactly when the initial run of odd-length zero-blocks has odd length.

The proof is an induction on `n` (equivalently on `|u|`), and it rests on three
statements about single deletions that involve only `h`.

**Lemma D (deletion lemmas).** Let `u` contain at least one `1`,
`u = 0^{z_1} 1 v`, and write `b_1 = z_1 mod 2`.

- **(D1)** If `b_1 = 1`, some deletion `u_i` has `h(u_i) = 0`.
- **(D2)** If `b_1 = 0` and `h(v) = 1`, some deletion `u_i` has `h(u_i) = 0`.
- **(D3)** If `b_1 = 1` and `h(v) = 0`, some deletion `u_i` has `h(u_i) = 1`.

Moreover, if `u = 0^z` with `z` odd, the deletion `0^{z−1}` has `h = 0`.

*Proof.* (D1): `z_1` is odd, hence `≥ 1`; deleting one zero of the first block
makes `z_1` even, so `t(u_i) = 0` and `h(u_i) = 0`.

(D2): `h(v) = 1` forces the first block of `v` to have odd length `z_2 ≥ 1`
(by (1) applied to `v`, or `h(0^{z_2}) = [z_2 odd]` if `v` has no one).
Deleting one zero of that block leaves the first block of `u` untouched, so
`t(u_i) = 0` because `z_1` is even, and `h(u_i) = 0`.

(D3): Let `z_2` be the length of the first block of `v` (so `v = 0^{z_2}` or
`v = 0^{z_2} 1 w`). By (1), `h(u_i) = 1 − h(v_i)` for every deletion that
happens inside `v`, so it suffices to find a deletion `v_i` of `v` with
`h(v_i) = 0`, or to use the deletion of the first one of `u`.

- If `z_2` is odd (so `z_2 ≥ 1`): delete one zero of that block; the first
  block of the result has even length, so `h(v_i) = 0`.
- If `z_2` is even and `v = 0^{z_2}` (i.e. `m = 1`): delete the one of `u`;
  the result is `0^{z_1+z_2}` with `z_1 + z_2` odd, so `h = 1` directly.
- If `z_2` is even and `v = 0^{z_2} 1 w`: delete the last character of `u`
  (it lies in `v`). Whether that character is a zero of the last block, the
  last one (when `w` is empty, the result is `0^{z_2}`), or the last one
  followed by nothing, the first block of the resulting `v_i` is still
  `0^{z_2}`, of even length, so `h(v_i) = 0`.

The final statement is `h(0^{z−1}) = [z − 1 odd] = 0`. ∎

*Proof of Theorem 1.* Induction on `|u|`. Assume the formula for every
position with a shorter `u` (and `G(0) = 0`). Let `D` be the set of values of
the (D)-options and `J` the value of the (J)-option. By induction and
`P(u_i) = 1 − P(u)`,

    D ⊆ { 1 − P(u) + 2h(u_i) } ⊆ { 1 − P(u), 3 − P(u) },

and `J = P(v) + 2h(v)` if `m ≥ 1`, `J = 0` if `m = 0`.

**Case A: `|u|` even, i.e. `P(u) = 1`.** Then `D ⊆ {0, 2}`, so the values
`1` and `3` can only come from `J`, and the claimed value is
`1 + 2h(u)`.

- *A1, `m = 0`*, `u = 0^{z}` with `z` even. `J = 0`. If `z = 0` there are no
  deletions and `G = mex{0} = 1`; if `z ≥ 2` the only deletion is `0^{z−1}`
  with value `0 + 2·[z−1 odd] = 2`, and `G = mex{0,2} = 1`. The formula gives
  `1 + 2·[z odd] = 1`. ✓
- *A2, `m ≥ 1`, `z_1` even.* Then `P(v) = 0`, so `J = 2h(v) ∈ {0,2}`, all
  option values are even, and `G = 1` as soon as `0` is an option value. If
  `h(v) = 0` then `J = 0`; if `h(v) = 1` then (D2) supplies a deletion with
  `h(u_i) = 0`, i.e. value `0`. The formula gives `1 + 2·0 = 1` by (1). ✓
- *A3, `m ≥ 1`, `z_1` odd.* Then `P(v) = 1`, so `J = 1 + 2h(v) ∈ {1,3}`, and
  (D1) puts `0 ∈ D`. If `h(v) = 1`: `J = 3`, the options are contained in
  `{0,2,3}` and contain `0`, and `1` is not an option, so `G = 1`; the formula
  gives `1 + 2·(1 − 1) = 1`. ✓ If `h(v) = 0`: `J = 1`, and (D3) puts `2 ∈ D`;
  the option set is exactly `{0,1,2}` (the value `3` cannot occur), so
  `G = 3`; the formula gives `1 + 2·1 = 3`. ✓

**Case B: `|u|` odd, i.e. `P(u) = 0`.** Then `D ⊆ {1, 3}`, so the value `0`
can only come from `J`, `2` never occurs as an option value, and the claimed
value is `2h(u)`.

- *B1, `m = 0`*, `u = 0^{z}` with `z` odd. `J = 0`; the deletion `0^{z−1}`
  has value `1 + 2·0 = 1`; so `G = mex{0,1} = 2 = 0 + 2·[z odd]`. ✓
- *B2, `m ≥ 1`, `z_1` even.* `P(v) = 1`, so `J ∈ {1,3}`; every option value
  is odd, hence `G = 0`, and the formula gives `2·0 = 0`. ✓
- *B3, `m ≥ 1`, `z_1` odd.* `P(v) = 0`, so `J = 2h(v)`. If `h(v) = 1`:
  `J = 2`, all options lie in `{1,2,3}`, so `G = 0 = 2·(1 − 1)`. ✓ If
  `h(v) = 0`: `J = 0`, and (D1) gives a deletion with `h(u_i) = 0`, i.e.
  value `1`; the options are contained in `{0,1,3}` and contain `0` and `1`,
  so `G = 2 = 2·(1 − 0)`. ✓

All cases agree with the formula, completing the induction. ∎

## 3. Consequences

**Corollary 1 (the two OEIS conjectures).** `G(n) ≤ 3` for all `n`, and
`G(4n) = G(n)` for all `n ≥ 1`.

*Proof.* The first is immediate. Multiplying by 4 appends `00` to the binary
expansion: `L` increases by 2 and the last block `z_{m+1}` increases by 2,
which changes neither `L mod 2` nor any block parity, hence not `t`. ∎

Also `G(2n) ≢ G(n) (mod 2)` for every `n ≥ 1` (the bit-length changes by one),
so the sequence `G(n), G(2n), G(4n), …` has period exactly 2 — the "period
dividing 2" the OEIS entry derives from Conjecture 2 is never period 1.

**Corollary 2 (outcome classes).** `n ≥ 1` is a P-position (previous player
wins) if and only if `L` is even and `t(u)` is even. Equivalently, with
`u = 0^{z_1} 1 v`: an even-length position is a P-position iff `z_1` is even,
or `z_1` is odd and the position `1v` is an N-position; every odd-length
position is an N-position.

*Provenance.* This corollary is **not new**: Project Euler Problem 961,
"Removing Digits" (21 Sep 2025, linked from the OEIS entry), is the decimal
form of the game, and public solution write-ups state exactly this P/N rule
together with the reduction of Remark 3 (see `README.md`, Prior work; those
write-ups are unrefereed and are cited as *secondary*). It is recorded here
because it falls out of Theorem 1, and because the Grundy values — which the
P/N rule does not determine — are what the OEIS conjectures are about.

**Corollary 3 (distribution of values).** For `L ≥ 3`, exactly `2^{L−3}` of
the `2^{L−1}` numbers with `L` binary digits have Grundy value in `{2,3}`; the
other `3·2^{L−3}` have value in `{0,1}`. Hence, for `k ≥ 1`, the number of
P-positions below `4^k` is `2^{2k−1} − 1`.

*Proof.* Let `A_ℓ` be the number of `u ∈ {0,1}^ℓ` with `h(u) = 1`, and
`B_ℓ = 2^ℓ − A_ℓ`. Classifying `u` by its first block (`u = 0^ℓ`, or
`u = 0^z 1 v`, `|v| = ℓ − 1 − z`) and using (1),

    A_ℓ = [ℓ odd] + Σ_{z odd, z ≤ ℓ−1} B_{ℓ−1−z}.

Subtracting the same identity for `ℓ − 2` (the indicators agree and the sums
differ by the single term `z = 1`) gives `A_ℓ − A_{ℓ−2} = B_{ℓ−2}` for all
`ℓ ≥ 2` (with `A_0 = 0`, `A_1 = 1`), i.e. `A_ℓ = A_{ℓ−2} + 2^{ℓ−2} − A_{ℓ−2} =
2^{ℓ−2}`. The `L`-bit numbers correspond to `ℓ = L − 1`. By Theorem 1 the
P-positions are the `L`-bit numbers with `L` even and `h = 0`: one for `L = 2`
(namely `n = 3`) and `3·2^{L−3}` for each even `L ≥ 4`; summing over
`L = 2, 4, …, 2k` gives `1 + 6(1 + 4 + ⋯ + 4^{k−2}) = 2^{2k−1} − 1`. ∎

## 4. Misère play

In misère play the player who removes the last nonzero digit *loses*; the
position `0` is then a win for the player to move (the opponent has just
lost).

**Theorem 2.** In misère play, `n ≥ 1` is a P-position if and only if
`G(n) = 1`, i.e. iff `L` is odd and `t(u)` is even. For `k ≥ 0` there are
exactly `4^k` misère P-positions below `2^{2k+1}`.

*Proof.* Induction on `n`, the statement being that "misère P" coincides with
"`G = 1`" on all options. A position is misère-P iff none of its options is
misère-P, i.e. (by induction) iff no option has Grundy value 1. If `G(n) = 1`
then `1` is not an option value, so `n` is misère-P. If `G(n) ≥ 2` then `1` is
an option value, so `n` is misère-N. If `G(n) = 0` we must exhibit an option
of value `1`: by Theorem 1 this is Case B2 or Case B3 with `h(v) = 1`. In B2,
`J ∈ {1,3}`; if `J = 1` we are done, and if `J = 3` then `h(v) = 1` and (D2)
gives a deletion with `h(u_i) = 0`, whose value is `1 − P(u) + 0 = 1`. In B3,
(D1) gives a deletion with `h(u_i) = 0`, again of value `1`. Finally `n = 0`
is misère-N and `G(0) = 0 ≠ 1`, so the base case is consistent. The count
follows from Corollary 3: `n = 1`, plus `3·2^{L−3}` positions for each odd
`L` with `3 ≤ L ≤ 2k+1`, i.e. `1 + (4^k − 1) = 4^k`. ∎

## 5. Remarks

**Remark 3 (other bases).** Play the same game on base-`b` digits, `b ≥ 2`
(delete one digit, discard leading zeros, last nonzero digit wins). Only the
pattern of zero versus nonzero digits matters: the map `μ` replacing every
nonzero digit by `1` sends the options of `n` exactly onto the options of
`μ(n)`, so `G_b(n) = G(μ(n))` by induction, and Theorems 1–2 apply verbatim
with "zero-blocks" read in base `b`. This reduction is also part of the
Project Euler 961 folklore (secondary). Verified directly for bases
3, 4, 5, 10 (`scratch` runs recorded in `WRITEUP.md`).

**Remark 4 (sums).** By the Sprague–Grundy theorem, a disjunctive sum of
Bit Deletion positions `n_1, …, n_r` is a P-position iff
`G(n_1) ⊕ ⋯ ⊕ G(n_r) = 0`, with each `G(n_j) ∈ {0,1,2,3}` read off from
Theorem 1 in linear time; e.g. `5 + 5` (values `3 ⊕ 3`) is a P-position while
`5 + 2` (`3 ⊕ 2 = 1`) is not.

## 6. Computational verification (CERTIFIED)

`grundy_check.c` recomputes, from the definition, the Grundy value and the
misère outcome of every `n < 2^32 = 4,294,967,296`, level by bit-length (all
options of an `L`-bit number have fewer bits, so each level is embarrassingly
parallel), and compares both with the closed forms. Result: **0 mismatches for
Theorem 1, 0 mismatches for Theorem 2, no value exceeds 3**, and at every
bit-length `L ≥ 3` the count of values in `{2,3}` is exactly `2^{L−3}`
(Corollary 3). Runtime 177 s on 4 threads, 4 GB RAM; output in
`data_grundy_check_2e32.txt`. `grundy.py` is an independent pure-Python
implementation: it agrees with the closed form for `n < 2^20`, reproduces the
34 terms published in A398916, and exhaustively checks the induction step of
Theorem 1 and Lemma D for every string `u` with `|u| ≤ 18` (524,287 strings;
0 failures). The OEIS entry had checked Conjecture 1 to `5·10^6` and
Conjecture 2 to `10^6`.

## 7. Open questions

1. The same game with *two* digits deleted per move, or with deletion of a
   contiguous block of equal digits, has not been analysed; the block-parity
   invariant of Theorem 1 does not obviously survive.
2. Partizan versions (each player may delete only certain digit values —
   Project Euler 963 "Removing Trits" is of this type) are open in the same
   sense.
