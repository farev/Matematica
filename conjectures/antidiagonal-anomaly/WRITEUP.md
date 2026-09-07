# Session narrative — antidiagonal-anomaly

## 2026-09-04 (session 1)

**How it was chosen.** The day's survey (log entry `log/2026-09-04-antidiagonal-anomaly.md`)
was looking for open statements young enough not to be swarmed by large computing groups
and concrete enough to settle in a day. arXiv:2609.01562 had been posted three days
earlier; its Section 7 conjectures that an explicitly computable ratio ρ(n) of binomial
coefficients stays below 1 for all n ≥ 496, after being above 1 for every 8 ≤ n ≤ 375 and
sporadically up to 495. A conjecture of the form "an explicit ratio of binomials is
eventually < 1" is exactly the shape a Stirling bound settles for large n and an exact
computation settles below that — the only question was whether the gap between the
conjectured threshold (496) and whatever the analysis gives could be closed by a
computation of reasonable size. The 2026-09-02 session had already noticed the paper
(then one day old) and computed a heuristic limit ≈ 0.968 < 1, but passed it over
because the authors might prove it themselves. Three days later nobody had, the value of
a clean proof was the same, and the work was small enough to run alongside an internal
compute thread (peaceable queens a(18)) on the remaining cores.

**Reading the paper.** The HTML version was read in full. The ingredients used:
the traffic formula f_B(A), the ten-point theorem (their Theorems 3.6, 4.4, 5.1), and
Proposition 7.2, which reduces the antidiagonal case to R_n(a) = G(n,a)/D(n) > 1 with
G(n,a) = ((n−2a+1)/(n−a))·C(n,a)·C(n−2,a−1) and D(n) = C(2n−2,n−1)/n. Two things were
checked before any analysis: (i) the paper's data — an exact integer computation
(`verify_anomaly.py`) reproduces "every n ≤ 375, sporadically to 495, none after" to the
letter (and gives the sporadic list, which the paper does not print); (ii) the reduction
itself — `allpoints_control.py` evaluates f_B at *every* grid point for every
antidiagonal B and 9 ≤ n ≤ 120 and confirms both that the argmax is among the ten points
and that (1,0) beats (1,1) exactly when the criterion holds. Both are the positive
controls the repository's tool discipline asks for; both passed with 0 mismatches.

**The reduction.** Writing C(n−2,a−1) = C(n,a)·a(n−a)/(n(n−1)) collapses the ratio to

    R_n(a) = a(n−2a+1)·C(n,a)² / ((n−1)·C(2n−2,n−1)),

so the anomaly is "obstruction deficit a(n−2a+1)C(n,a)²/(n(n−1)) exceeds the Catalan
number Cat(n−1)". That is the answer to the paper's first question and it also makes
the exact check a one-line running-product computation.

**First analytic attempt (too crude).** Bounding C(n,a)² by the central binomial squared
times e^{−4x²/n} (x = n/2 − a), the central binomial from below by 4^{n−1}/√(π(n−1)),
and then maximising (2x+1)e^{−4x²/n} by the crude split 2x·e^{−4x²/n} + e^{−4x²/n}
≤ √(n/2)e^{−1/2} + 1 gives ρ(n) < 0.9679·√(n/(n−1)) + 2.2568/√(n−1), which is < 1 only
from n ≈ 5000 on. Perfectly usable (the exact check to 5000 would take a minute), but
ugly.

**Second attempt (used).** Two changes: keep the exact maximiser
x* = (√(2n+1) − 1)/4 of φ_n(x) = (2x+1)e^{−4x²/n}, where φ_n(x*) = (n/(s−1))e^{−1/2}
e^{(s−1)/(2n)} with s = √(2n+1); and use Robbins' two-sided Stirling bounds throughout so
that every error factor is an explicit e^{±1/(12m)}. The entropy inequality
(1+t)log(1+t) + (1−t)log(1−t) ≥ t² (two integrations of f″ = 2/(1−t²) ≥ 2) replaces the
usual Chernoff-type bound and is exact enough. Result: ρ(n) < U(n) with U decreasing and
U(3000) < 0.9939. The threshold 3000 was chosen because the exact check to 3000 takes
12 s; 2000 would also work (U(2000) ≈ 0.9992) but with no margin to spare.

**Certifying the numeric step.** U(3000) involves π, e, and square roots. Rather than
trust a floating-point evaluation, `check_bound.py` bounds each of them by a rational in
the safe direction (Machin's formula with alternating-series bracketing for π, a Taylor
partial sum for e, r² ≥ q for square roots, e^y ≤ 1/(1−y)) and evaluates the product in
`fractions.Fraction`. The first draft of the note claimed U(3000) < 0.9937 from a
hand-rounded chain; the rational evaluation gave 0.993849, so the statement was
corrected to 0.9939 before anything was committed. Small, but exactly the kind of slip
the rational check exists to catch.

**The limit.** With the same tools in the other direction (Robbins lower bounds, the
upper half of the entropy inequality f(t) ≤ t² + t⁴/(6(1−t²)), and the concavity of
F_n(x) = log φ_n(x) − log(1 + 2x/n)) one gets the two-sided expansion
ρ(n) = c₀(1 + 1/√(2n) + O(1/n)), c₀ = √(8/π)e^{−1/2} = 0.96788…. The 1/√(2n) term is
the difference of two √(2/n)-size effects (the position of x* relative to √(n/8), and
the factor n/(n−a)); the numerics agree with it to 4·10⁻⁴ at n = 3000. The envelope
crosses 1 at n ≈ 454, in the middle of the paper's transition zone 376–495.

**The sporadic pattern.** Once ρ(n) is seen as "smooth envelope minus a rounding
penalty", the pattern the paper calls irregular becomes legible: the integer maximiser
a_n must approximate the real maximiser n/2 − x*(n), the penalty is ≈ 8δ_n²/n with
δ_n ≤ 1/2 the rounding distance, and δ_n alternates between the parity classes of n
because n/2 is an integer or a half-integer. The table in `transition_table.csv` shows
even n winning around x* = 7.0 (n ≈ 420) and odd n winning around x* = 7.5 (n ≈ 480),
which is precisely "even n anomalous up to 462, odd n up to 495". This part is a model
and is labelled NUMERICAL; the list and every ρ(n) are exact.

**A counting slip, caught.** The note's first draft said "56 sporadic values"; the
script's count of anomalous n in [376, 495] is 82 (377; 379–422; even 424–462; 464;
odd 465–495: 1 + 44 + 20 + 1 + 1 + 15). The draft number was a mental tally and was
wrong; the number in the note is the script's.

**What failed.** Nothing in the mathematics. The honest limitations: the proof is
computer-assisted between 496 and 2999 (a Stirling-type bound sharp to 5·10⁻⁵ at n = 497
is not realistic), the O(1/n) term of Theorem B is not explicit, and the ten-point
theorem is taken from the paper (re-checked only to n = 120). The result is a small,
complete answer to a small, new question; it does not pretend to be more.

**Runtime.** Every script runs in under a minute on one core (Python 3.11, standard
library); no seeds, no floating point in any certified path (floats appear only in the
display columns x*, δ of the transition table).
