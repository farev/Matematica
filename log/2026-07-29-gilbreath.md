# 2026-07-29 — gilbreath

**Target.** Build the "microscope": specify precisely the micro-scale
prime-configuration control that a proof of Gilbreath via the CHT
criterion requires, prove whatever lenses are buildable with existing
tools, and calibrate every dangerous pattern against the real primes.

**Result.** Mixed, labelled. PROVED: translation lemmas M1–M3 (depth-1
zero-blocks of the CHT array = arithmetic progressions of consecutive
primes; top-row {0,d}-blocks = two-valued gap runs; zero-blocks descend
to constant blocks), and Corollary M5 — via the classical primorial
rigidity argument (Prop. M4, KNOWN mechanism), prime APs below x have
length ≤ 1.25 log x + O(1), so CHT hypothesis (ii) restricted to depth 1
holds unconditionally with a log⁹x margin. NUMERICAL: calibration bench
(`microscope_bench.py`) at x = 10⁶..10⁹ (10¹⁰ running): all dangerous
patterns grow like ≤ 1.4·log x, 12+ orders below thresholds; fastest fuel
is alternating parity runs (Lemke Oliver–Soundararajan bias observed
directly). Full spec in `conjectures/gilbreath/MICROSCOPE.md`.

**What failed.** The primorial mechanism dies at depth ≥ 2: once
intermediate signs of iterated differences can alternate, no small
modulus is forced to divide anything, so signed-polynomial progressions
of consecutive primes have no known upper bound. Two-valued runs worse:
Shiu guarantees the fuel exists; zero upper bounds known. Sieve-side
route to the UHL first-moment blocked by C^k·k! losses in uniform
prime-tuple upper bounds at k growing with x.

**Second pass (same day).** Pushed the divisibility mechanism further.
PROVED: Lemma M6 (two-valued rigidity: odd q | B−A, q ∤ A kills {A,B}
runs at length q−1) ⇒ Corollary M7: **CHT hypothesis (iii) at depth 0
holds unconditionally for every d whose odd part exceeds 1** — the
surviving enemy is exactly d = 2^s. Verified sharp on primes < 10⁹
(bounds attained at d = 5, 7, 10, 14; `lens_check.py`). Lemma M8: pure-B
stretches in surviving runs collapse to ≤ 1.25 log B (primorial), so
long {2,B}-runs force twin pairs at density 1/(1.3 log B) ⇒ Cor. M9:
depth-0 (iii) fully reduced to a twin-clustering bound with log x/loglog
slack over the expected truth. Prop. M10: Montgomery–Vaughan kills
bounded-gap runs at absolute length (e.g. {2,6} ≤ ~27,000 forever).
Lemma M11: periodic-sign depth-2 structures annihilated; only aperiodic
survive. Meta-principle recorded: sieves are structurally blind in
polylog windows — the microscope must be divisibility-based.

**What failed (second pass).** Aperiodic sign sequences at depth 2 evade
every covering argument tried (the ±w walk mod q can dodge 0 forever
without periodicity); sieve routes to the surviving d = 2^s case are
blocked by the blindness principle.

**Third pass (aperiodic campaign).** PROVED Lemma M13 (dichotomy): for
depth-1 constant blocks with parameter w, every odd prime q | w forces
either window ≤ q−1 primes or full imprisonment in a residue class mod
q; long blocks escaping imprisonment have w = 2^s exactly, with forced
gap alternation mod 2^{s+1}. Verified on 388,068 blocks < 10⁹: zero
violations; 922 blocks saturate the covering threshold at exactly q−1
primes; imprisonment realized 56,555× (mod 3), 4,658× (mod 5), 1× (mod
7). Also PROVED: quadratic-tracking mod any single odd q forces constant
signs (collapses to the GRH-killed M12 case). Formulated the 2-adic
kernel principle: covering cannot touch 2-power-moduli patterns (primes
only forbid evenness), so every surviving enemy is (I) 2-adic (d = 2^s,
w = 2^s) or (II) behind same-class runs — and three independent routes
(multi-modulus pigeonhole, first moments, sieves) all hit the
short-window equidistribution wall. Initial M13 scan had two off-by-one
bugs producing phantom violations; corrected and documented.

**Fourth pass (the reduction).** Read CHT §3–§6 in full (their tower /
good-block engine, verbatim). PROVED Theorem R1 (conditional reduction):
Cramér + residual pattern axiom P ⇒ Gilbreath for all but finitely many
rows, with P strictly narrower than CHT's own hypotheses thanks to the
lenses (depth-1 zero-blocks and odd-part-d depth-0 blocks now theorems;
2-adic depth-0 reduced to twin clustering). PROVED Theorem R2
(insufficiency): a sequence exists with all fixed-order Cramér pattern
statistics (perturbation O_k(loglog x): one entry per plant, plants at
n_j = 2^{2^j}) whose Gilbreath leads fail infinitely often — plants
V = n² ride the always-open diagonal Pascal channel; the mirrored CHT
telescope bounds erosion; simulation confirms derailment at exactly row
m−1. Hence NO axiom system of fixed-order gap statistics implies
eventual Gilbreath: the first rigorous substantiation of CHT's
"difficult even assuming Hardy–Littlewood" remark. Formulated Open
Problem R3 (fixed-order statistics + o(n) entries: plants provably
fail; extended highways leave fixed-order fingerprints) — the sharpest
question the program has produced. All in REDUCTION.md.

**Next.** R3 is the frontier: either a Cramér-compatible counterexample
(strengthening R2) or a proof that bounded-entry sequences with perfect
fixed-order statistics cool (a conditional Gilbreath from standard-type
conjectures). Page update: the program arc (constants + Theorem 2 +
lenses M1–M13 + R1/R2/R3) is now complete and self-contained;
recommended.
