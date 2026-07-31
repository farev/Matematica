# The reduction: what axioms give Gilbreath, and what axioms cannot

*Session of 2026-07-29 (part 4). Companion to MICROSCOPE.md. Sources: CHT
arXiv 2607.08712 read in full (§3–§6); simulation `reduction_check`
(transcript); claim labels per repository discipline.*

## 1. The CHT engine, as actually proved (their §5, read verbatim)

Contrapositive form: assume (i) entries ≤ 2^M, (ii) no 0-valued block of
length L, and a bad apex a_{(N−1,1)} > 1. Their machine (coarse
monotonicity 5.2 → locating a large triangle 5.3 → good blocks 5.4–5.5 →
strict upward monotonicity 5.7 → small-or-huge dichotomy 5.8 → towers
3.13 + pigeonhole) then *constructs* a {0,d}-valued block of length
≥ R_m − 3R_{m−1} at depth ≤ 2R_{m−1} in the right half, with
2^{M−m} < d ≤ 2^{M−m+1}. So (iii) fails. The bad objects the hypotheses
must exclude are therefore exactly:

- **Z(L):** 0-valued blocks of length L ≍ log¹⁰N at any depth;
- **B(d, i, k):** {0,d}-valued blocks of length k ≥ 8^M·max(i, 100L)
  at depth i ≤ 2R_{M−1}, right half.

## 2. The conditional theorem, with the lens-trimmed axiom

**Axiom C (Cramér, normalized).** p_{n+1} − p_n ≪ log²p_n; hence array
entries ≪ log²N ≤ 2^M.

**Axiom P (residual pattern axiom — what the lenses do NOT already
prove).** For all large N, the array of normalized prime gaps contains:
(P1) no zero-block of length ≥ L at depth ≥ 2 [depth 1 is **PROVED**
unconditionally: Cor. M5, CPAP-primorial]; (P2) no {0,d}-block as in
B(d,i,k) with i ≥ 1; (P3) no {0,2^s}-block as in B at depth 0 [depth-0
blocks with d of odd part > 1 are **PROVED** impossible: Cor. M7; and
P3 itself follows from any twin-clustering bound at density
1/(9 log log N): Cor. M9].

**Theorem R1 (conditional Gilbreath). PROVED reduction.** Axioms C + P
imply a_{(N−1,1)} ∈ {0,1} for all sufficiently large N, i.e. Gilbreath's
conjecture holds for all but finitely many rows; combined with the
CERTIFIED verification of rows ≤ 4.55×10⁸ this would give Gilbreath
outright if the finite threshold were effective. *Proof.* CHT Thm 1.6
with the instantiation of their §1.4; hypothesis (ii) at depth 1 and
hypothesis (iii) at depth 0 for non-2-adic d are discharged
unconditionally by Cor. M5 and Cor. M7; the rest is C + P. ∎
(The content over CHT's own remark is the *trimming*: P is strictly
narrower than their (ii)+(iii) — depth-1 zero-blocks and all
odd-part-d depth-0 blocks are now theorems, and P3 reduces to twin
clustering.)

## 3. The insufficiency theorem: fixed-order statistics can never do it

CHT remark that their hypotheses "look difficult to establish
rigorously, even if one assumes strong conjectures on the primes such as
the Hardy–Littlewood prime tuples conjecture." The following makes that
a theorem: *no axiom system consisting of fixed-order gap-pattern
asymptotics can imply eventual Gilbreath.*

**Theorem R2 (insufficiency of fixed-order statistics). PROVED (proof
below; erosion step verified numerically to the row).** There exists a
sequence (a_n) of non-negative integers such that:

(α) for every fixed k and every pattern v ∈ ℤ_{≥0}^k, the counts
#{n ≤ x : (a_{n+1},…,a_{n+k}) = v} agree with those of the i.i.d.
geometric (Cramér-model) sequence up to an additive O_k(log log x) —
in particular every fixed-order Hardy–Littlewood-analogue asymptotic,
with any error quality the random model itself enjoys, holds for (a_n);

(β) the Gilbreath array of (a_n) has a_{(n−1,1)} > 1 for infinitely
many n.

Hence the implication "fixed-order pattern asymptotics ⇒ eventual
Gilbreath" is false for gap sequences, and any proof of Gilbreath must
consume information about patterns of *unbounded* length (Cramér-type
pointwise exclusions), not merely fixed-order statistics however
precise.

*Proof.* Background: b_n i.i.d. geometric with fixed parameter; by CHT
Thm 1.3 its array a.s. cools (leads ∈ {0,1} eventually). Plant positions
n_j = 2^{2^j}; set a_{n_j} = V_j := n_j² and a_n = b_n otherwise.
(α): at most log log x plants below x, each altering one entry, so each
fixed-k pattern count moves by ≤ k·log log x. ∎(α)
(β): the left edge of the plant's light cone obeys the mirrored CHT
telescope a_{(t, n_j−t)} ≥ V_j − Σ_{s<t} a_{(s, n_j−s−1)}, and the
subtracted entries lie strictly left of the cone, hence are
plant-independent background values with E Σ ≤ C·n_j. Markov and
Σ_j n_j⁻¹ < ∞ give, a.s. for all large j, arrival value
≥ V_j − n_j² / 2 ≥ 2 at column 1, depth n_j (the light-cone arrival
depth): the lead exceeds 1 there. Plants are too sparse to interact. ∎(β)
*Numerical check:* background (12,000 geometric entries) cools at row
14; a plant V = 3m at position m = 6000 derails the lead first at depth
m exactly (index m − 1 in the trace; the always-open diagonal Pascal
channel C(t,t) = 1), arriving with value 14,962 = V − erosion. ∎

**Remark (sharpness of the construction).** The plant needs V ≳ n_j
(erosion is ≍ position), i.e. a single gap comparable to the index —
grossly non-Cramér. This is forced: under any bound a_n = o(n) the
plant's value dies before reaching the lead. R2 therefore does *not*
rule out:

**Open Problem R3.** Is eventual Gilbreath a formal consequence of
[fixed-order gap statistics] + [a_n = o(n)] (or + Cramér)? Equivalently:
can a sequence with perfect fixed-order Cramér statistics and
subrationally growing entries have infinitely many bad leads? By R2's
sharpness analysis, any counterexample must use *extended structures*
(long two-valued highways) rather than lone values — and those leave
fixed-order fingerprints (twin-density excesses of size L/log L per
structure, by the M8 mechanism) that appear to violate the statistics
they must preserve. Resolving R3 in the affirmative would be a
conditional proof of Gilbreath from standard-type conjectures; in the
negative, a strengthening of R2. This is, in our view, the sharpest
well-posed question this program has produced.

## 4. Status after the reduction

| statement | label |
|---|---|
| C + P ⇒ eventual Gilbreath (R1) | **PROVED** (reduction; via CHT 1.6 + M5 + M7) |
| depth-1 zero-blocks, odd-part-d depth-0 blocks | **PROVED** unconditionally (this program) |
| P3 ⇐ twin-clustering bound | **PROVED** reduction (M8/M9) |
| fixed-order statistics ⇒ eventual Gilbreath | **FALSE** (R2) |
| fixed-order + o(n) entries ⇒ eventual Gilbreath | OPEN (R3) — attacked 2026-07-29, see [R3.md](R3.md): every finite order fails even with bounded entries (Thm R3.5); the all-orders question reframed with an affirmative proof skeleton |
| P from any standard conjecture | OPEN; R2 shows it needs unbounded-length input |
