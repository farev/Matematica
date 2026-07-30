# The microscope: a specification of the missing tool for Gilbreath

*Session of 2026-07-29. Companion to NOTE.md/WRITEUP.md. Code:
`microscope_bench.py`, `bench_1e10.py`; data: `microscope_bench.csv`.*

Analytic number theory's proven theorems see primes in aggregate
("telescopes"); a proof of Gilbreath's conjecture via the Chase–Hunter–Tao
criterion (arXiv 2607.08712, Thm 1.6) needs configuration-level control of
consecutive primes in windows of polylogarithmic length ("a microscope").
This document specifies that instrument precisely: what it must exclude,
what parts already exist, what parts are genuinely missing, and calibration
data from the real primes. Claim labels follow the repository discipline
(PROVED / CERTIFIED / NUMERICAL / CONJECTURAL / KNOWN).

## 1. The requirement (from CHT Theorem 1.6, instantiated)

For the normalized-gap array (top row a_j = (p_{j+2}−p_{j+1})/2 − 1,
iterated absolute differences), Gilbreath for row N−1 follows from:

- (i) entries ≪ log¹⁰N (Cramér-strength gap bound);
- (ii) **no all-zero block of length ~ log¹⁰N at any depth**;
- (iii) **no {0,d}-valued block (d ≥ 2) of depth i and length ≫ 8^M·i**,
  M ≍ 10 log log N.

The microscope = theorems excluding (ii)- and (iii)-patterns *everywhere,
forever* — not on average, not almost surely.

## 2. Translation lemmas: what the patterns are in prime language

**Lemma M1 (depth-1 zero-blocks are CPAPs). PROVED.** A zero-block of
length L at depth 1 means a_{(0,j)} = … = a_{(0,j+L)} are equal, i.e. L+1
equal consecutive prime gaps, i.e. **L+2 consecutive primes in arithmetic
progression** (a CPAP of length L+2). ∎

**Lemma M2 (top-row {0,d}-blocks are two-valued gap runs). PROVED.**
a_{(0,·)} ∈ {0,d} on a length-L window ⇔ L+1 consecutive prime gaps all
lie in the two-element set {2, 2d+2}. ∎

**Lemma M3 (zero-blocks descend to constant blocks). PROVED.** A
zero-block of length L at depth i ≥ 1 forces a constant block of length
L+1 at depth i−1 (|x−y| = 0 ⇔ x = y). Iterating: a depth-i zero-block of
length L forces, at the top row, a window of L+i consecutive gaps whose
iterated ±differences vanish at level i — the gap sequence lies on a
"signed-polynomial" family of degree < i (polynomial when all
intermediate signs are constant). ∎ Depth-1 recovers M1 (degree-0 =
constant gaps = AP).

## 3. The lens that already exists (depth 1) — and its proof

**Proposition M4 (prime APs are short). KNOWN (folklore mechanism);
proof included for completeness.** Let a, a+d, …, a+(k−1)d be primes,
all > k. Then every prime q ≤ k divides d. *Proof.* If q ∤ d, the k ≥ q
terms cover all residues mod q, so some term ≡ 0 (mod q); that term is a
prime divisible by q, hence equals q ≤ k, contradicting all terms > k. ∎
Hence d ≥ ∏_{q ≤ k} q = e^{θ(k)}, and the AP spans (k−1)d ≥ e^{θ(k)}.
With θ(k) ≥ 0.8k (k ≥ 100, Rosser–Schoenfeld), any prime AP inside
(k, x] has

  **k ≤ 1.25 log x + O(1).**

**Corollary M5 (depth-1 microscope lens). PROVED.** Consecutive primes
are in particular primes, so CPAPs below x have length ≤ 1.25 log x +
O(1). By Lemma M1, the CHT array on primes ≤ x has **no zero-block at
depth 1 of length exceeding ≈ 1.25 log x** — a full factor log⁹x below
the danger threshold log¹⁰x. Hypothesis (ii), restricted to depth 1,
holds unconditionally for all large N. ∎

This is the model of what a microscope component looks like: a rigidity
mechanism (small moduli force divisibility of the common difference) that
converts a micro-pattern into an exponential cost, valid at *every*
location. The rest of the instrument needs analogues of this mechanism
for richer patterns — and none are known.

## 4. The missing lenses (precisely)

1. **Depth ≥ 2 zero-blocks** (signed-polynomial progressions of
   consecutive primes, Lemma M3). The primorial mechanism fails: once
   the intermediate signs can alternate, the gap values range over a
   coset-like family and small moduli are no longer forced to divide
   anything. MISSING. Even "no (log x)¹⁰ consecutive primes with
   second-order gap structure" has, to our knowledge, no proof.
2. **Two-valued gap runs** (Lemma M2 and its depth-i analogues, feeding
   hypothesis (iii)). The partial-sum walk mod q branches when the two
   gap values differ mod q, so no residue class is forced. MISSING.
   Worse, Shiu's theorem (KNOWN) shows arbitrarily long runs of
   consecutive primes in a fixed class mod 4 *exist* — constant-parity
   fuel does occur; the question is purely quantitative (lengths ~
   fractional powers of log x infinitely often, vs the log¹⁰x danger
   threshold — but with **no known upper bound at all**).
3. **Uniformity**. The natural axiom powering a first-moment proof of
   (ii)+(iii) is a Hardy–Littlewood prime-tuples statement **uniform in
   the tuple size k up to k ~ log¹¹x** with error terms uniform over all
   admissible tuples in windows of length log¹¹x — call it UHL. Under
   UHL, each dangerous pattern of length L has frequency ≤ ρ^L with
   ρ < 1, and Σ over positions and patterns converges doubly
   exponentially at L ~ log¹⁰N; Borel–Cantelli then leaves finitely many
   exceptions. CONJECTURAL — and note CHT's own caution that their
   hypotheses "look difficult to establish rigorously, even if one
   assumes strong conjectures on the primes such as the Hardy–Littlewood
   prime tuples conjecture": the standard HL conjecture is stated for
   *fixed* k, and nothing in the literature supplies the required
   uniformity. Writing the UHL ⇒ (ii)+(iii) derivation in full, with
   the exact uniformity strength needed, is the sharpest open subproject
   this document proposes; the sieve-side obstacle is that unconditional
   upper-bound sieves lose factors like C^k·k!, which overwhelm the
   pattern deficit ρ^L once k grows with x.

## 5. Calibration (the test bench). NUMERICAL.

Maximal dangerous-pattern lengths in the actual primes
(`microscope_bench.py`; run-length scans on the full gap sequence):

| x | CPAP (primes) | |Δgap| const | gaps ≡0 (4) | gaps ≡2 (4) | 2-valued | danger log¹⁰x |
|---|---|---|---|---|---|---|
| 10⁶ | 4 | 9 | 12 | 16 | 7 | 2.5×10¹¹ |
| 10⁷ | 5 | 9 | 14 | 24 | 8 | 1.2×10¹² |
| 10⁸ | 5 | 9 | 15 | 26 | 9 | 4.5×10¹² |
| 10⁹ | 6 | 11 | 19 | 28 | 9 | 1.5×10¹³ |
| 10¹⁰ | 6 | 11 | 23 | 32 | 10 | 4.5×10¹³ |

Readings. (a) Every observed dangerous pattern grows like c·log x with
c ≤ 1.4 — the patterns behave exactly as the random model predicts, 12+
orders of magnitude below the thresholds. (b) The fastest-growing fuel is
the *alternating* parity run (≡2 mod 4, c ≈ 1.35) — the Lemke
Oliver–Soundararajan anti-repetition bias of consecutive primes, visible
directly in our data as alternation outpacing repetition (c ≈ 0.9 for
≡0 mod 4). (c) CPAP lengths (4, 5, 5, 6) match the known search records
for maximal CPAPs below these bounds, validating the bench.

## 6. Program status

| lens | status |
|---|---|
| depth-1 zero-blocks (CPAPs) | **PROVED** unconditionally (Prop. M4 + Cor. M5), margin log⁹x |
| depth ≥ 2 zero-blocks | MISSING; precise obstruction identified (§4.1) |
| {0,d}/two-valued blocks | MISSING; existence of fuel KNOWN (Shiu); zero upper bounds |
| UHL ⇒ (ii)+(iii) reduction | CONJECTURAL; formalization = next session's target |
| calibration bench | NUMERICAL, 5 scales, random-model consistent |

An honest summary in one sentence: one lens of the microscope exists and
is elementary (and correspondingly, the depth-1 part of the danger is
gone unconditionally); every deeper lens requires a rigidity mechanism
for consecutive-prime configurations that current mathematics does not
possess, and the cleanest formal target for building one is the UHL
reduction of §4.3.

## 7. Session-2 lenses: the divisibility mechanism composes further

*(Second pass, same day. Verification: `lens_check.py` on primes < 10⁹.)*

**Lemma M6 (two-valued rigidity). PROVED.** Let p_j < … < p_{j+L} be
consecutive primes > L with all gaps in {A, B}, and let q be an odd prime
with q | (B−A), q ∤ A, q ≤ L+1. Then no such run exists; equivalently,
any {A,B}-gap run has length L ≤ q − 2 for every such q. *Proof.* All
gaps ≡ A (mod q), so p_{j+m} ≡ p_j + mA (mod q); as m runs over
0..q−1 ≤ L this covers every residue class mod q, in particular 0 — a
prime > L ≥ q divisible by q. ∎

**Corollary M7 (CHT (iii) at depth 0, unless d is a power of two).
PROVED.** Top-row {0,d}-blocks are {2, 2d+2}-gap runs (Lemma M2); here
B−A = 2d, A = 2, so any odd prime q₀ | d gives runs of length ≤ q₀−2 ≤
d ≪ every CHT threshold. **Hypothesis (iii) at depth 0 therefore holds
unconditionally for every d whose odd part exceeds 1; the surviving
enemy is exactly d ∈ {1, 2, 4, 8, …}.** ∎ Sharpness: on primes < 10⁹
the bound is *attained exactly* at d = 5, 7, 10, 14 (runs of length
3, 5, 3, 5 vs bounds 3, 5, 3, 5), and d with 3 | d cannot even reach two
gaps — all verified (`lens_check.py`).

**Lemma M8 (B-block collapse inside surviving runs). PROVED.** Within a
{2,B}-run, a maximal pure-B stretch of ℓ gaps is ℓ+1 consecutive primes
in AP with difference B, so (Prop. M4 mechanism) every prime ≤ ℓ+1
divides B and ℓ ≤ 1.25 log B + O(1) — loglog-of-x scale, since
B ≤ 2^{M+1}. Consequently a {2,B}-run of length L contains at least
L/(1.3 log B) − 1 gaps equal to 2, i.e. **twin-prime pairs at density
≥ 1/(1.3 log B) along the run**. ∎ (Verified: max pure-B stretch over
primes < 10⁹ is 5, at B = 30, vs bound 5.3.)

**Corollary M9 (reduction of the surviving case to twin clustering).
PROVED reduction; hypothesis CONJECTURAL.** If one could show that among
any L ≥ (danger threshold) consecutive primes below x the proportion of
twin gaps is < 1/(1.3·(M+1) log 2) ≍ 1/(9 log log x), then hypothesis
(iii) at depth 0 would hold in full. The expected truth is ~ 2C₂/log x —
the needed bound has log x/log log x slack over the truth. This is the
weakest-looking statement whose proof would finish depth 0; it is still
open, because sieve bounds cannot control windows of polylog length
(see the principle below).

**Proposition M10 (absolute kill for dense runs). KNOWN ingredients,
assembled.** If all gaps in a run of length L are ≤ g₀, the run spans
W ≤ g₀L and contains L+1 primes; Montgomery–Vaughan's uniform bound
π(y+W) − π(y) ≤ 2W/log W forces log(g₀L) ≤ 2g₀, i.e. **L ≤ e^{2g₀}/g₀ —
an absolute bound, independent of x**. E.g. {2,6}-runs never exceed
~27,000 gaps, anywhere in the primes, forever. ∎

**Lemma M11 (periodic-sign kill at depth 2). PROVED.** In a window where
|G_{j+1} − G_j| = w > 0 (a depth-1 constant block, the gate to depth-2
zero-blocks), suppose the sign sequence of G_{j+1} − G_j is P-periodic
over a stretch of length L. The P-strided subsequences of primes are APs
with common difference S_P = (sum of one period of gaps) ≤ P·max gap, so
Prop. M4 gives L ≤ P·(1.25 log(P·G_max) + O(1)). Every period
P ≪ L/log x is annihilated; **only aperiodic sign sequences survive at
depth 2**. ∎

**The blindness principle.** Every lens above is divisibility-based
(covering a small modulus forces a prime to be composite). This is not
an accident: density tools — sieves — bound prime counts in a window of
span W by ~2W/log W, which *exceeds the trivial count* once the window
is of polylog length, so sieves are structurally blind exactly at the
microscope's working scale; they bite only on runs of bounded gap values
(M10). The missing lenses — aperiodic depth-2 sign sequences, power-of-2
two-valued runs, general depth-i blocks — must come from divisibility
rigidity, from the UHL program of §4.3, or from a genuinely new
mechanism.

**Lemma M12 (degree-2 progressions: covering meets least split primes).
PROVED reduction; closure conditional on GRH.** In a depth-1 constant
block with constant signs (the gap sequence increases or decreases by w
each step — the gateway subcase of depth-2 zero-blocks), the primes obey
p_m = p₀ + mG₀ + w·m(m−1)/2, an explicit integer quadratic f(m). For any
prime q ≤ L at which f has a root mod q, the run dies (covering: some
p_m ≡ 0 mod q). Hence L ≤ 2·q_split(f), the least prime where f splits.
The discriminant is ≍ w·p₀ (it involves the prime p₀ itself, size ~x),
so unconditional least-split bounds are useless here — but under GRH,
q_split ≪ log²|D| ≍ log²x ≪ log¹⁰x, so **on GRH the constant-sign
depth-2 case closes**. Unconditionally OPEN — and this localizes exactly
where the microscope needs GRH-strength character information. ∎

## 8. The aperiodic campaign (session 3, same day)

Setup for depth-2: a depth-1 constant block with parameter w means
consecutive primes with second differences ±w; writing gaps
G_m = G₀ + w·T_m (T a ±1 walk), the primes are p_m = p₀ + mG₀ + wU_m
with U the integrated walk. Aperiodic sign sequences evade M11/M12.
Results of the campaign:

**Lemma M13 (dichotomy). PROVED; verified on 388,068 blocks < 10⁹ with
zero violations (`lens_check` session scan).** Let the block span N_p
consecutive primes > q, and let q be an odd prime dividing w. Then mod q
the walk vanishes (all gaps ≡ G₀), so either (a) N_p ≤ q − 1 (the
covering threshold), or (b) q | G₀, and then q divides every gap: the
entire window is a **same-class run mod q**. For long blocks
(N_p > w ≥ any odd factor), (a) is impossible, so every odd prime factor
of w imprisons the block in a residue class; **a long block escaping all
imprisonment has w exactly a power of two**, and then T's parity is
forced (T_m ≡ m + ε mod 2): the gaps alternate deterministically mod
2^{s+1}. ∎ Empirical sharpness: 922 blocks below 10⁹ saturate case (a)
at exactly N_p = q − 1 = 6 primes (w with factor 7, gap patterns like
8, 22, 8, 22, 8 — all gaps ≡ 1 mod 7); the same-class branch (b) is
realized 56,555 times mod 3, 4,658 times mod 5, once mod 7.

**Quadratic-tracking rigidity. PROVED.** If a sign sequence keeps
U_m ≡ f(m) mod q exactly for a quadratic f and any odd q > 2, then
σ_m ≡ f'' is constant: single-modulus "smart tracking" collapses to the
constant-sign case, which closes under GRH (M12). Adversaries must
therefore evade every modulus non-parametrically.

**The 2-adic kernel principle.** Covering arguments run on the fact that
0 mod q is forbidden to primes. Modulo powers of two, primes forbid only
evenness — every odd residue is allowed — so **no covering argument can
constrain a pattern whose modulus support is 2-adic**. Combined with the
blindness principle (§7) this gives a precise characterization of the
remaining difficulty: after sessions 1–3, every surviving enemy of the
CHT criterion either (I) lives in the covering kernel — d = 2^s blocks,
w = 2^s blocks — or (II) hides behind same-class runs mod a small odd
prime (the Shiu wall). Three independent attack routes (multi-modulus
pigeonhole on p₀'s residue vector, first-moment counting, sieve bounds)
all terminate at the same requirement: equidistribution-type control of
primes in short windows — the UHL sector, or GRH-strength character
information. The wall is now *named at every gate*.

**Calibration of the surviving enemy.** Below 10⁹ the longest 2-adic
(w = 2) block spans 12 primes; the danger threshold is ~10¹³. The enemy
is real, tiny, and growing at most logarithmically — but nothing we can
prove today forbids it from one day being large.

### Updated status (supersedes §6)

| lens | status |
|---|---|
| depth-1 zero-blocks (CPAPs) | **PROVED**, ≤ 1.25 log x (Cor. M5) |
| depth-0 {0,d}-blocks, d with odd factor | **PROVED**, ≤ d (Cor. M7), sharp |
| depth-0 {0,d}-blocks, d = 2^s, bounded | **PROVED** absolute (Prop. M10) |
| depth-0 {0,d}-blocks, d = 2^s, large | reduced to twin clustering (Cor. M9); OPEN |
| depth-2 zero-blocks, periodic signs | **PROVED** (Lemma M11) |
| depth-2 zero-blocks, constant signs | closes **on GRH** (Lemma M12); unconditionally OPEN |
| depth-2 blocks, w with odd factor | **PROVED**: imprisoned in a residue class (Lemma M13, dichotomy sharp at q−1) — reduced to same-class-run control |
| depth-2 blocks, w = 2^s, aperiodic | in the covering kernel (§8); needs UHL/GRH-sector input; 12 primes at 10⁹ vs 10¹³ threshold |
| depth ≥ 3, general (iii) at depth ≥ 1 | MISSING |
| hypothesis (i) (Cramér-strength gaps) | MISSING (needs ~Cramér) |
