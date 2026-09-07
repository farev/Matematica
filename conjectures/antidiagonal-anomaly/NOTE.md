# The antidiagonal anomaly of Gil–Liang–Odetola–Weiner disappears for n ≥ 496

*Research note, session of 2026-09-04. AI-assisted (Claude); see the repository README.*

## Abstract

Gil, Liang, Odetola and Weiner [GLOW] (arXiv:2609.01562, posted 1 Sep 2026) count
monotone lattice paths from (0,0) to (n,n) that avoid a forbidden point B and ask which
point A carries the most B-avoiding traffic. They prove that for n ≥ 9 the maximum is
attained at one of ten near-corner points whatever B is, observe that an obstruction
B = (a, n−a) on the antidiagonal moves the maximum from (1,1) to the boundary point (1,0)
for every 8 ≤ n ≤ 375 and sporadically up to n = 495, and conjecture (their Conjecture
7.4) that this "anomaly" never reappears for n ≥ 496. We prove the conjecture. Their criterion is the
integer inequality a(n−2a+1)·C(n,a)² > (n−1)·C(2n−2,n−1) (Lemma 1); a Robbins–Stirling
bound shows that the ratio ρ(n) = max_a R_n(a) is below 0.994 for every n ≥ 3000
(Theorem A), and exact integer arithmetic settles 496 ≤ n ≤ 2999 (Theorem A′, certificate
shipped). We also prove ρ(n) → c₀ = √(8/π)·e^{−1/2} = 0.96788…, more precisely
ρ(n) = c₀(1 + 1/√(2n) + O(1/n)) (Theorem B), which places the transition at n ≈ 454, and
we show that R_n(a) is log-concave in a with real maximiser n/2 − x*(n),
x*(n) = (√(2n+1) − 1)/4, so that the sporadic pattern on 376 ≤ n ≤ 495 is the rounding of
n/2 − x*(n) to an integer, alternating with the parity of n (Proposition C). This answers
the three questions of [GLOW, §7].

## 0. Setting (from [GLOW])

Let 𝒫_n be the set of lattice paths from (0,0) to (n,n) with unit north and east steps.
For grid points A, B let f_B(A) be the number of paths in 𝒫_n through A avoiding B. With
A = (a₁,b₁), B = (c,d) and A south-west of B,

    f_B(A) = C(a₁+b₁, a₁)·[ C(2n−a₁−b₁, n−a₁) − C(c+d−a₁−b₁, c−a₁)·C(2n−c−d, n−c) ].

[GLOW] prove (Theorems 3.6, 4.4, 5.1) that for n ≥ 9 and every B the maximum of f_B is
attained at one of the ten points (1,0), (0,1), (1,1), (2,1), (1,2) and their images under
(x,y) ↦ (n−x, n−y). For B = (a, n−a) on the antidiagonal with 2a < n they show
([GLOW, Proposition 7.2]) that f_B(1,0) > f_B(1,1) exactly when R_n(a) > 1, where

    R_n(a) = G(n,a)/D(n),   G(n,a) = ((n−2a+1)/(n−a))·C(n,a)·C(n−2,a−1),   D(n) = C(2n−2,n−1)/n,

and they set ρ(n) = max_{1 ≤ a < n/2} R_n(a). The *anomaly* at n is the event ρ(n) > 1.
Their data ("we verified the criterion for all n up to 495"): ρ(n) > 1 for 8 ≤ n ≤ 375
and for some n ≤ 495; we reproduce this exactly in §4 and list the sporadic n. Their
**Conjecture 7.4** reads "ρ(n) ≤ 1 for all n ≥ 496"; we prove the strict inequality.

Throughout, x := n/2 − a, so 0 ≤ x ≤ n/2 − 1 when 1 ≤ a ≤ n/2, and 2x + 1 = n − 2a + 1.

## 1. The exact form of the criterion

**Lemma 1.** For n ≥ 3 and 1 ≤ a ≤ n/2,

    G(n,a) = C(n,a)² · a(n−2a+1) / (n(n−1)),    D(n) = C(2n−2,n−1)/n = Cat(n−1),

so that

    R_n(a) = a(n−2a+1)·C(n,a)² / ((n−1)·C(2n−2,n−1)),

and R_n(a) > 1 if and only if a(n−2a+1)·C(n,a)² > (n−1)·C(2n−2,n−1).

*Proof.* C(n−2,a−1) = (n−2)!/((a−1)!(n−a−1)!) = C(n,a)·a(n−a)/(n(n−1)); substitute into
G and cancel n−a. The second identity is the definition of the Catalan number. ∎

So the "baseline margin" f(1,1) − f(1,0) = D(n) in the unobstructed grid is a Catalan
number, and the obstruction B = (a, n−a) subtracts G(n,a) from it. This is the
simplification asked for in [GLOW, §7, question (1)].

## 2. Stirling tools

**Lemma 2 (Robbins 1955).** For every integer m ≥ 1,

    √(2πm)·(m/e)^m·e^{1/(12m+1)} < m! < √(2πm)·(m/e)^m·e^{1/(12m)}.

(H. Robbins, *A remark on Stirling's formula*, Amer. Math. Monthly 62 (1955) 26–29;
standard, checked against the statement in Feller, vol. I, §II.9.)

**Lemma 3.** For 1 ≤ a ≤ n−1,

    C(n,a) < √( n / (2π a(n−a)) ) · n^n/(a^a (n−a)^{n−a}) · e^{1/(12n)},
    C(n,a) > √( n / (2π a(n−a)) ) · n^n/(a^a (n−a)^{n−a}) · e^{1/(12n+1) − 1/(12a) − 1/(12(n−a))}.

*Proof.* Apply Lemma 2 to n!, a! and (n−a)!; for the upper bound drop the factors
e^{−1/(12a+1)}, e^{−1/(12(n−a)+1)} < 1. ∎

**Lemma 4.** Let f(t) = (1+t)log(1+t) + (1−t)log(1−t) for 0 ≤ t < 1. Then

    t² ≤ f(t) ≤ t² + t⁴ / (6(1−t²)).

Consequently, with a = n/2 − x (so t = 2x/n),

    2^n · e^{−2x²/n − 4x⁴/(3n³(1−t²))} ≤ n^n/(a^a (n−a)^{n−a}) ≤ 2^n · e^{−2x²/n}.

*Proof.* f(0) = f′(0) = 0 and f″(t) = 2/(1−t²) = 2∑_{k≥0} t^{2k}, so
f(t) = ∑_{m≥1} t^{2m}/(m(2m−1)); the first term is t², every coefficient with m ≥ 2 is at
most 1/6, which gives both bounds. For the consequence write a = (n/2)(1−t),
n−a = (n/2)(1+t): a^a(n−a)^{n−a} = (n/2)^n·exp((n/2)f(t)), and (n/2)·t² = 2x²/n,
(n/2)·t⁴/(6(1−t²)) = 4x⁴/(3n³(1−t²)). ∎

**Lemma 5.** For m ≥ 1,

    (4^m/√(πm)) · e^{−1/(6m)} < C(2m,m) < 4^m/√(πm).

*Proof.* Lemma 2 for (2m)! and (m!)²: the quotient of the bounds is
4^m/√(πm) times e^{1/(24m+1) − 2/(12m)} > e^{−1/(6m)} on the lower side and
e^{1/(24m) − 2/(12m+1)} < 1 on the upper side (as 12m+1 < 48m). ∎

## 3. The analytic bound

Let φ_n(x) = (2x+1)·e^{−4x²/n} for x ≥ 0 and

    x*(n) = (√(2n+1) − 1)/4,     s = √(2n+1).

**Lemma 6.** φ_n increases on [0, x*] and decreases on [x*, ∞), and

    φ_n(x*) = ( n/(s−1) ) · e^{−1/2} · e^{(s−1)/(2n)}  ≤  √(n/2) · e^{−1/2} · (1 − 1/√(2n))^{−1} · e^{1/√(2n)}.

*Proof.* φ_n′(x) = e^{−4x²/n}·(2 − (8x/n)(2x+1)); the bracket is decreasing in x and
vanishes at 16x² + 8x − 2n = 0, i.e. at x*. At x*, (8x*/n)(2x*+1) = 2 gives
2x*+1 = n/(4x*), and 4x*²/n = (s−1)²/(4n) = (2n+2−2s)/(4n) = 1/2 − (s−1)/(2n); hence the
displayed value. Finally √(2n) < s < √(2n) + 1 gives √(2n) − 1 < s − 1 < √(2n), so
n/(s−1) < n/(√(2n) − 1) = √(n/2)/(1 − 1/√(2n)) and (s−1)/(2n) < 1/√(2n). ∎

**Theorem A.** For every n ≥ 3000 and every integer a with 1 ≤ a ≤ n/2,

    R_n(a) < U(n) := c₀ · √(n/(n−1)) · (1 − 1/√(2n))^{−1} · exp( 1/√(2n) + 1/(3(n−1)) ),
    c₀ = √(8/π)·e^{−1/2} = 0.967882…,

and U(n) ≤ U(3000) < 0.9939. In particular ρ(n) < 1 for all n ≥ 3000.

*Proof.* Put x = n/2 − a ∈ [0, n/2 − 1]. By Lemma 1, the upper bound of Lemma 3 squared,
the upper bound of Lemma 4 squared, and Lemma 5 (lower bound, m = n−1),

    R_n(a) = a(2x+1)·C(n,a)² / ((n−1)·C(2n−2,n−1))
          < a(2x+1) · [ n/(2π a(n−a)) ] · 4^n e^{−4x²/n} e^{1/(6n)}
                     · √(π(n−1)) e^{1/(6(n−1))} / ( (n−1)·4^{n−1} )
          = (2/√π) · ( n/(n−a) ) · φ_n(x) / √(n−1) · e^{1/(6n) + 1/(6(n−1))}.          (3.1)

Since a ≤ n/2 we have n/(n−a) ≤ 2, and 1/(6n) + 1/(6(n−1)) < 1/(3(n−1)). By Lemma 6,
φ_n(x) ≤ φ_n(x*) ≤ √(n/2)·e^{−1/2}·(1 − 1/√(2n))^{−1}·e^{1/√(2n)}. Hence

    R_n(a) < (4/√π)·√(n/2)·e^{−1/2}/√(n−1) · (1 − 1/√(2n))^{−1} · exp( 1/√(2n) + 1/(3(n−1)) ) = U(n),

because (4/√π)·√(n/2) = √(8/π)·√n, so (4/√π)·√(n/2)·e^{−1/2}/√(n−1) = c₀·√(n/(n−1)).
Each of the factors √(n/(n−1)), (1 − 1/√(2n))^{−1} and exp(1/√(2n) + 1/(3(n−1))) is
decreasing in n, so U(n) ≤ U(3000) for n ≥ 3000. Numerically, with rational bounds only
(script `check_bound.py`, exact rational arithmetic; the bound e^y ≤ 1/(1−y) for
0 ≤ y < 1 replaces the exponential):

    π > 3.1415 (Machin's formula with alternating-series bracketing) and e > 2.71828
    (Taylor partial sum) give c₀² = 8/(πe) < 0.936798, so c₀ < 0.96808;
    √(3000/2999) < 1.00017;   u = 1/√6000 < 0.01291, so (1 − u)^{−1} < 1.013079;
    y = u + 1/8997 < 0.0130212 ⇒ e^y ≤ 1/(1 − y) < 1.013194;
    U(3000) < 0.96808 · 1.00017 · 1.013079 · 1.013194 < 0.99385.

Therefore R_n(a) < 0.9939 < 1 for all n ≥ 3000 and all admissible a. ∎

## 4. The conjecture

**Theorem A′ ([GLOW, Conjecture 7.4], in strict form).** ρ(n) < 1 for every n ≥ 496. Consequently,
for every n ≥ 496 and every obstruction B = (a, n−a) on the antidiagonal, the boundary
point (1,0) carries strictly less traffic than (1,1): the antidiagonal anomaly never
reappears.

*Proof.* For n ≥ 3000 this is Theorem A. For 496 ≤ n ≤ 2999 the script
`verify_anomaly.py` evaluates, in exact integer arithmetic (running-product binomials,
no floating point), the inequality of Lemma 1 for every 1 ≤ a ≤ n/2 and finds no a with
a(n−2a+1)·C(n,a)² > (n−1)·C(2n−2,n−1); the per-n record (maximising a, number of
anomalous a, ⌊10⁹·ρ(n)⌋) is the committed certificate `certificate_3_3000.csv`
(12 s on one core). The largest value of ρ(n) on 496 ≤ n ≤ 2999 is
ρ(497) = 0.99995528…, attained at a = 241. The "consequently" is [GLOW, Proposition 7.2]
combined with their ten-point theorem. ∎

The same computation reproduces [GLOW]'s data below 496: ρ(n) > 1 for every 3 ≤ n ≤ 375,
and on 376 ≤ n ≤ 495 exactly for

    n ∈ {377, 379, 380, …, 422, 424, 426, 428, …, 462, 464, 465, 467, 469, …, 495}

— i.e. 377, all of 379–422, the even numbers 424–462, then 464 and the odd numbers
465–495 (82 values; 455 anomalous n in [3, 3000] in all). Note how thin the margin is at
the threshold: ρ(495) = 1.000024 and ρ(497) = 0.999955.

Remark (label). Theorem A is a proof for n ≥ 3000; the finite range 496 ≤ n ≤ 2999 is
an exact, reproducible computation with a certificate. Together they prove the
conjecture for all n ≥ 496; the repository labels the combined statement PROVED
(computer-assisted on a finite range, in the sense of an exact finite case analysis),
and the finite-range part on its own CERTIFIED.

## 5. The limit of ρ(n)

**Theorem B.** ρ(n) → c₀ = √(8/π)·e^{−1/2} = 0.9678828980…; more precisely

    ρ(n) = c₀ · ( 1 + 1/√(2n) + O(1/n) ).

In particular the "envelope" c₀(1 + 1/√(2n)) crosses 1 at n ≈ 454.

*Proof.* Write F_n(x) = log φ_n(x) − log(1 + 2x/n) = log(2x+1) − 4x²/n − log(1 + 2x/n)
on x ≥ 0, so that (3.1) reads R_n(a) < (4/√π)·e^{F_n(x)}/√(n−1)·e^{1/(3(n−1))}, using
n/(n−a) = 2/(1 + 2x/n).

(i) *F_n is concave.* F_n″(x) = −4/(2x+1)² − 8/n + 4/(n+2x)² < 0 because 4/(n+2x)² < 8/n.

(ii) *Location of the maximiser.* F_n′(x) = 2/(2x+1) − 8x/n − 2/(n+2x). At x* the first
two terms cancel (Lemma 6), so F_n′(x*) = −2/(n+2x*) ∈ (−2/n, 0), while
F_n″ ≤ −8/n + 4/n² ≤ −7/n (n ≥ 4) gives F_n′(x*−1) ≥ F_n′(x*) + 7/n > 0. Hence the
maximiser x̂ of F_n lies in (x*−1, x*), and by concavity
F_n(x̂) ≤ F_n(x*) + F_n′(x*)(x̂ − x*) ≤ F_n(x*) + 2/n.

(iii) *Upper bound.* From (3.1), (ii):
ρ(n) < (4/√π)·e^{F_n(x*)}/√(n−1)·e^{2/n + 1/(3(n−1))}, and
e^{F_n(x*)} = φ_n(x*)/(1 + 2x*/n) = (n/(s−1))·e^{−1/2}·e^{(s−1)/(2n)}/(1 + (s−1)/(2n)).
With s = √(2n+1) = √(2n)·(1 + 1/(4n) + O(n^{−2})) one has (s−1)/(2n) = 1/√(2n) + O(1/n)
and n/(s−1) = √(n/2)·(1 + 1/√(2n) + O(1/n)); therefore
e^{F_n(x*)} = √(n/2)·e^{−1/2}·(1 + 1/√(2n) + O(1/n)), and since
(4/√π)√(n/2)e^{−1/2}/√(n−1) = c₀√(n/(n−1)) = c₀(1 + O(1/n)),
ρ(n) ≤ c₀(1 + 1/√(2n) + O(1/n)).

(iv) *Lower bound.* Let a_n be an integer with |n/2 − a_n − x*| ≤ 1/2 (for n ≥ 8 such an
a_n lies in [1, n/2]), and x_n = n/2 − a_n. The lower bounds of Lemmas 3, 4 and the upper
bound of Lemma 5 give, exactly as in (3.1),

    R_n(a_n) > (4/√π)·e^{F_n(x_n)}/√(n−1) · exp( −8x_n⁴/(3n³(1−t²)) − 1/(6a_n) − 1/(6(n−a_n)) ),

t = 2x_n/n. For n ≥ 3000, x_n ≤ x* + 1/2 ≤ √(n/2), so t² ≤ 2/n, 8x_n⁴/(3n³(1−t²)) ≤ 4/(3n),
and (as a_n ≥ n/2 − √(n/2) ≥ n/4) 1/(6a_n) + 1/(6(n−a_n)) ≤ 1/n; all three corrections
are O(1/n). By Taylor's formula with the concavity of (i),
F_n(x_n) ≥ F_n(x*) − |F_n′(x*)|·|x_n − x*| − ½·sup|F_n″|·(x_n − x*)²
        ≥ F_n(x*) − 1/n − (1/8)(1/x*² + 8/n),
where on x ≥ x* − 1/2 one has (2x+1)² ≥ 4x*², so |F_n″| ≤ 4/(2x+1)² + 8/n ≤ 1/x*² + 8/n,
and 1/x*² ≤ 8.3/n for n ≥ 3000 (x*² ≥ (n/8)(1 − √(2/n))). So F_n(x_n) ≥ F_n(x*) − 3.1/n, and
ρ(n) ≥ R_n(a_n) ≥ c₀(1 + 1/√(2n) + O(1/n)) by the same expansion as in (iii). ∎

Numerically, n·(ρ(n)/c₀ − 1 − 1/√(2n)) is 0.707 at n = 3000, 0.705 at n = 10000 and
0.557 at n = 30000 (exact ratios: ρ(3000) = 0.980606160, ρ(10000) = 0.974795079,
ρ(30000) = 0.971852232), consistent with an O(1/n) remainder of size about 0.6/n.

## 6. The maximiser and the sporadic pattern

**Proposition C.** (a) For n ≥ 3 the sequence a ↦ R_n(a), 1 ≤ a ≤ ⌊(n−1)/2⌋, is
log-concave, hence unimodal:

    R_n(a+1)/R_n(a) = (n−a)²(n−2a−1) / ( a(a+1)(n−2a+1) )

is a product of three positive factors each decreasing in a. So ρ(n) is attained at the
unique a (or a tie of two consecutive a) with (n−a)²(n−2a−1) < a(a+1)(n−2a+1) and
(n−a+1)²(n−2a+1) ≥ (a−1)a(n−2a+3).

(b) The integer maximiser a_n satisfies |a_n − (n/2 − x*(n))| ≤ 1 for every 3 ≤ n ≤ 3000
(exact computation; the certificate records a_n).

(c) *Explanation of the sporadic pattern.* By Theorem B and its proof, ρ(n) equals the
smooth envelope E(n) = (4/√π)e^{F_n(x̂_n)}/√(n−1)·(1 + O(1/n)) diminished by the rounding
penalty exp(F_n(x_n) − F_n(x̂_n)) ≈ exp(−8δ_n²/n), where δ_n = |x_n − x̂_n| ≤ 1/2 is the
distance from the real maximiser to the nearest admissible x_n = n/2 − a. Near the
threshold the envelope exceeds 1 by only 0.1–0.3 % (E(n) − 1 ≈ c₀/√(2n) − (1 − c₀)
vanishes at n ≈ 454), while the rounding penalty ranges from 0 to 8·(1/2)²/n ≈ 0.4 %.
Hence for 376 ≤ n ≤ 495 the anomaly occurs exactly when δ_n is small. Since x̂_n ≈ x*(n)
drifts slowly (x* = 7.00 at n = 420, 7.50 at n = 480) and n/2 is an integer for even n
but a half-integer for odd n, δ_n alternates between the two parity classes: around
n = 420 the even n have δ_n ≈ 0 and the odd n have δ_n ≈ 1/2, around n = 480 the roles
are reversed. This is precisely the observed pattern (even n anomalous up to 462, odd n
up to 495) — see the table `transition_table.csv` (n, a_n, x*, δ_n, ρ(n)) produced by
`transition_table.py`. The model in this paragraph is explanatory (NUMERICAL); the table
entries ρ(n) and a_n are exact (CERTIFIED).

## 7. Answers to the questions of [GLOW, §7]

1. *Can the criterion R_n(a) > 1 be simplified or better understood?* Yes: it is
   a(n−2a+1)·C(n,a)² > (n−1)·C(2n−2,n−1) (Lemma 1), i.e. the obstruction's deficit
   G(n,a) = a(n−2a+1)C(n,a)²/(n(n−1)) exceeds the Catalan number Cat(n−1); asymptotically
   R_n(n/2 − x) ≈ √(8/(πn))·(x + ½)·e^{−4x²/n}, maximal near x = √(n/8) with value
   c₀(1 + 1/√(2n) + O(1/n)).
2. *Why the irregular pattern?* Rounding of the real maximiser n/2 − x*(n) to an integer
   in the narrow window where the envelope is within 0.3 % of 1, with the parity of n
   deciding which residue class rounds well (Proposition C(c)).
3. *Can the bound n ≥ 9 be improved?* Not addressed here (it concerns their ten-point
   theorem, not the anomaly).

Open: an explicit description of the *exact* set of anomalous n (all n ≤ 375 plus the 56
listed values) from the cubic of Proposition C(a) and Theorem B's expansion with explicit
constants; a lower bound on ρ(n) of the form c₀(1 + 1/√(2n) − C/n) with a numerical C
would make the transition analysis fully rigorous rather than explanatory.

## 8. Reproducibility

- `verify_anomaly.py N1 N2 [cert.csv]` — exact integer verification and certificate;
  `python3 verify_anomaly.py 3 3000 certificate_3_3000.csv` takes 12 s on one core
  (Python 3.11, no dependencies).
- `check_bound.py` — the rational-arithmetic evaluation of U(3000) in Theorem A
  (Fractions only).
- `allpoints_control.py N` — independent control of [GLOW, Prop. 7.2]: for 9 ≤ n ≤ N and
  every antidiagonal B it computes f_B at *all* grid points and checks that the argmax
  lies among the ten points and that (1,0) beats (1,1) iff the integer criterion holds
  (N = 120: 0 mismatches).
- `transition_table.py` — the table of §6.

## References

- [GLOW] J. Gil, Z. Liang, A. Odetola, M. Weiner, *Points of maximal traffic on a grid
  with obstruction*, arXiv:2609.01562 (1 Sep 2026), v1. Read in full (HTML version) on
  2026-09-04; Proposition 7.2 and the §7 conjecture quoted from it.
- H. Robbins, *A remark on Stirling's formula*, Amer. Math. Monthly 62 (1955), 26–29.
  (Bounds as stated in Feller, *An Introduction to Probability Theory*, vol. I, §II.9 —
  secondary; the inequality itself is classical and was not re-derived here.)
