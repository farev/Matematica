# Draft letter to Chase, Hunter, and Tao

*Draft for Fabian to send from his own address. Not sent by any automated
system. Keep the AI disclosure — it is repository policy and basic
courtesy.*

---

Subject: Follow-ups to arXiv 2607.08712 — exact c₄–c₆, a sharpening of
Prop. 2.1, and a proof of your "difficult even assuming HL" remark

Dear Professors Chase, Hunter, and Tao,

I have been running a series of computational research sessions on
Gilbreath's conjecture built directly on your July preprint (arXiv
2607.08712), and several of the outcomes speak so directly to specific
lines of your paper that I wanted to share them. Everything below comes
with code, data, and machine-checked certificates in a public
repository, and a summary page with the proofs:
https://fabianarevalo.com/gilbreath ·
https://github.com/farev/Matematica/tree/main/conjectures/gilbreath

1. **Exact c₄, c₅, c₆** (your Section 1.3, "with more effort, one can
   compute..."): c₄ = 778959731701/1447295850000, c₅ and c₆ as exact
   fractions (c₆ has a 153-digit numerator; 2,097,152 sign chambers).
   Each computation carries an exactness certificate — the chamber
   measures sum to exactly 1 in ℚ — which proved necessary: a first run
   lost 1.7×10⁻⁷ of measure to degenerate triangulations and produced a
   value wrong by 1.25×10⁻⁷ that Monte Carlo could not detect (0.8σ).

2. **A factor-2 sharpening of your Proposition 2.1**: c_n ≥
   2·exp(−Σ_{k<n} c_k) for n ≥ 2, hence Σ_{i≤n} c_i ≥ log(2n − 2 + e²),
   via the reversal symmetry of the triangle: the apex is |A − B| =
   (A−B)⁺ + (B−A)⁺ with A, B the two depth-(n−1) entries, and each term
   admits your telescoping argument from its own end, with the two noise
   sums independent of the opposite channel's source.

3. **On Remark 1.5** (c_i ≍ 1/i): a tiered Monte Carlo to depth 4095,
   anchored on the exact values, finds c_i governed by the binary
   expansion of i — a submask law c_i ≈ C·i^{−α}·Σ_{m⊆i} q^m with
   q ≈ 0.68, α ≈ 0.80 (R² = 0.98; out-of-sample R² = 0.90 on the two
   octaves above the fitting range). Partial sums fit 10.84·n^{1/5} to
   0.4% two octaves out of sample; adjacent indices differ by up to
   ×6.8 (c₂₀₄₇ vs c₂₀₄₈). Uniform[0,1] initial data kills the
   oscillation, consistent with a tail-activated Lucas-channel
   mechanism.

4. **On your remark that hypotheses (ii)/(iii) "look difficult to
   establish rigorously, even if one assumes strong conjectures such as
   Hardy–Littlewood"**: this is now a theorem in the following sense.
   There is a gap sequence whose every fixed-order pattern count matches
   the i.i.d. geometric model to within O_k(log log x), whose Gilbreath
   leads exceed 1 infinitely often (single planted values at
   doubly-exponentially sparse positions, riding the diagonal Pascal
   channel; the erosion is bounded by the mirror of your telescope).
   So no axiom system of fixed-order gap statistics implies eventual
   Gilbreath. The plants require entries comparable to their position,
   which suggests the sharp remaining question: **does fixed-order
   statistics + a_n = o(n) imply eventual Gilbreath?** The o(n) bound
   is unconditional for primes, so an affirmative answer would derive
   Gilbreath from Hardy–Littlewood-type statistics alone.

5. Smaller items possibly of use: covering-congruence lemmas discharge
   parts of Theorem 1.6's hypotheses unconditionally for the primes
   (depth-1 zero-blocks via the primorial bound on APs of consecutive
   primes; top-row {0,d}-blocks for every d with odd part > 1, with the
   caps attained exactly in data below 10⁹); and a first empirical audit
   of (ii)/(iii) on the primes to 10⁹ (worst zero-block 31 vs threshold
   ~3×10¹²; worst length/depth ratio 11 vs ~10²⁶).

Full disclosure: this work was produced in research sessions I ran with
an AI system (Claude, Anthropic), with every proof verified numerically
step-by-step and every exact value certified algebraically; the
methodology and all failures are documented in the repository. I would
of course welcome any corrections — especially if any of the above is
already known to you or in the literature.

With admiration for the paper,

Fabian Arevalo
fabiareor@gmail.com · fabianarevalo.com/math
