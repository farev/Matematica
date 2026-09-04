# 2026-09-04 — antidiagonal-anomaly (new; secondary target: peaceable-queens a(18))

**Target.** Conjecture 7.4 of Gil–Liang–Odetola–Weiner, arXiv:2609.01562 (posted
1 Sep 2026): for lattice paths (0,0) → (n,n) avoiding an obstruction B = (a, n−a) on
the antidiagonal, the point of maximal traffic migrates from (1,1) to the boundary
point (1,0) exactly when an explicit ratio ρ(n) of binomial coefficients exceeds 1;
the authors verified the criterion to n = 495 (anomaly at every 8 ≤ n ≤ 375 and
sporadically to 495) and conjecture ρ(n) ≤ 1 for all n ≥ 496. Chosen because the
statement is an explicit binomial inequality — Stirling bounds for large n, exact
integers below — three days old, and not the kind of problem large computing groups
swarm. What counted as success: a proof for all n ≥ 496 with every finite part
certified, plus answers to the paper's §7 questions (simplify the criterion; explain
the irregular pattern).

**Result.** **PROVED** (computer-assisted on 496 ≤ n ≤ 2999) — Conjecture 7.4 in
strict form: ρ(n) < 1 for all n ≥ 496. Lemma 1 rewrites the criterion as the integer
inequality a(n−2a+1)·C(n,a)² > (n−1)·C(2n−2,n−1) (the obstruction's deficit exceeds the
Catalan number Cat(n−1)); Theorem A (Robbins' Stirling bounds + the entropy inequality
(1+t)log(1+t)+(1−t)log(1−t) ≥ t²) gives ρ(n) < U(n) with U decreasing and
U(3000) < 0.9939, the numeric step certified in rational arithmetic (Machin bracketing
for π, Taylor sum for e, e^y ≤ 1/(1−y)); **CERTIFIED** — exact integer verification for
496 ≤ n ≤ 2999 (12 s, one core, certificate committed; the worst case is
ρ(497) = 0.99995528…, so the conjectured threshold is razor-thin but right).
**PROVED** — ρ(n) → c₀ = √(8/π)·e^{−1/2} = 0.967882…, more precisely
ρ(n) = c₀(1 + 1/√(2n) + O(1/n)) (the envelope crosses 1 at n ≈ 454); R_n(a) is
log-concave in a with an explicit consecutive ratio. **CERTIFIED** — the exact anomalous
set below 496 (all 3 ≤ n ≤ 375 plus 82 sporadic values: 377, 379–422, even 424–462,
464, odd 465–495; the paper printed only "intermittently up to 495"), and a control
re-deriving the paper's reduction from the definition of traffic at every grid point
for 9 ≤ n ≤ 120 (0 mismatches). **NUMERICAL** — the sporadic pattern explained as the
rounding of the real maximiser n/2 − (√(2n+1) − 1)/4 to an integer, with a penalty
≈ 8δ²/n that alternates between the parity classes of n (even n win near x* = 7.0,
n ≈ 420; odd n near x* = 7.5, n ≈ 480). New directory `conjectures/antidiagonal-anomaly/`
(README, NOTE, WRITEUP, PAGE.md, four scripts, certificate); index row added.

**Second external result (afternoon): triangulation-discrepancy.** Basti–Cremaschi
(arXiv:2608.21585, 21 Aug 2026) prove disc(T) ≤ n − 2⌈(n+2)/3⌉ for plane triangulations
with n ≢ 5 (mod 6) and leave the class n ≡ 5 (mod 6) open (checked at n = 11 only).
**PROVED** — the refined bound for every triangulation on n = 11, 17 and 23 vertices
(the first three orders of the open class), and for every n ≡ 5 (mod 6) whenever the
balanced 4-colouring's big class has at most two vertices of degree ≥ 5; the route is a
structure theorem for a counterexample on n = 6m+5 vertices — it carries a 4-colouring
with classes (3m+2, m+1, m+1, m+1) whose big class is fully mixed (every link shows all
three colour pairs, so no degree 4), has ≥ 2m+3 vertices of degree 3 and 3..m−1 of
degree ≥ 5, every other vertex lies on a face avoiding the big class, no vertex has more
than 2m+1 degree-3 neighbours in it, and every "single flip" is blocked — closed for
h ≤ 2 high-degree vertices by an Euler-formula count on the subgraph induced by their
links (Lemma 8), so a counterexample needs n ≥ 29. **CERTIFIED**, as independent
confirmations at the two new orders — disc ≤ U(n) for all 129,664,753 triangulations on
17 vertices (full census, 15 min, 2,652 extremal, exact distributions for 13 ≤ n ≤ 17
extending the paper's table) and for all ≈ 6·10¹⁰ on 23 vertices, via the structure
theorem: 109,507,132 two-connected plane graphs on 12 vertices from plantri, 948,057
surviving configurations, all of discrepancy 1 and every one admitting a single flip
(277 s / 365 s). The general residue class stays open for n ≥ 29; the obstruction (three
or more high-degree big-class vertices whose links cover the flips) is described
exactly. New directory
`conjectures/triangulation-discrepancy/` (README, NOTE, WRITEUP, PAGE.md, code, data);
index row added.

**Secondary target (internal, on the otherwise idle cores): peaceable-queens a(18).**
See `log/2026-09-04-peaceable-queens.md`.

**Connectivity.** arxiv.org reachable by WebFetch (listings, abstracts, HTML full
text) and by web search. oeis.org, erdosproblems.com and mathoverflow.net return 403 /
"unable to fetch" to WebFetch but serve `curl` with a browser user agent (OEIS text
format, erdosproblems pages and forum, MathOverflow HTML and the Stack Exchange API);
all four consulted live today. pip reachable (numpy, sympy, python-sat, networkx,
gmpy2 installed at session start; nothing beyond the standard library was needed for
the result).

**Candidate slate** (three externals across three subfields; five scouts ran in
parallel — four external surveys and one internal audit — their reports are in the
session scratchpad; the facts below were re-checked against the sources by the
session):

1. **Antidiagonal anomaly, arXiv:2609.01562 Conjecture 7.4** (lattice-path
   enumeration). Statement as above. Source: the paper's HTML version, read in full on
   2026-09-04; v1 only, no citing work (web and arXiv search). Open because the paper is
   three days old and states it as a conjecture verified only to n = 495. The 2026-09-02
   session had noticed the paper at one day old and passed it over ("the authors may
   prove it themselves"); three days later nobody had. **Selected.**
2. **Lonely Runner spectrum for six speeds, arXiv:2609.03444 (Cordella, 3 Sep 2026),
   Conjecture 6.2 / Question 6.6** (Diophantine approximation). Theorem 6.1: every
   near-tight sextuple (ML < 1/6) outside a finite, non-effective exceptional set E₆
   has ML = (P−1)/(6P) with P ≡ ±1 (mod 6), hence odd denominator; Conjecture 6.2 says
   E₆ is empty; Question 6.6 asks whether max vᵢ < 3q always; Question 6.7 says an
   effective version of their Lemma 2.4 would make the theorem unconditional. Checked
   exhaustively by the author for all speeds ≤ 110 (2·10⁹ sextuples, code on Zenodo).
   Open per the paper. Passed over: the honest one-day product is a range extension
   (speeds ≤ 160, ~10× the tuples) — "more data" — while the real bottleneck, an
   effective Lemma 2.4, is an ideas problem.
3. **Refined discrepancy bound for plane triangulations in the open residue class
   n ≡ 5 (mod 6), arXiv:2608.21585 (Basti–Cremaschi, 21 Aug 2026)** (graph colouring).
   disc(T) ≤ n − 2⌈(n+2)/3⌉ is proved for n ≢ 5 (mod 6) and stated open for n ≡ 5
   (mod 6); their census covers all 9,150 triangulations with n ≤ 12 (n = 11: all 1,249
   satisfy it). The next open order is n = 17 with 129,664,753 triangulations — a
   1–2 h census on 4 cores giving a CERTIFIED verdict either way. Passed over today
   because the cores were committed to the a(18) run and the expected outcome (all
   satisfy) changes no theorem; a good future target, and a counterexample would be
   page-worthy.

   Also surveyed and rejected (scout reports): Greaves–Tan arXiv:2609.02218 Question 5.2
   (smallest Neumaier graph of coherent rank five; finite search over the
   Hanaki–Miyamoto schemes of order ≤ 38, likely "none small"); Nagy–Vajda
   arXiv:2608.18584 (Kasami APN conjecture, verification n ≤ 13 → 18, safe but "more
   data"); Guedes–Machado arXiv:2609.03091 (a 2023 NNTDM reprint; OEIS A084699-level
   questions); Rampone arXiv:2608.23652 (n₆(4), undecided semiregular types after
   millions of models); Pak–Soskin arXiv:2608.03281 (n = 45 took 20 h on 32 cores);
   Hu–Liu arXiv:2609.00583 (unit-area rectangles, r ≤ 21).
   Scout B (OEIS, ~330 entries screened): A392714/A147681 — Shah–Kiselev's conjecture
   (arXiv:2605.11137, Remark 5) that the signed count of late-growing permutations is
   ±1 (proof route: a sign-reversing involution; the scout found the sharper alternation
   by N mod 4 for N ≤ 11); A398490 — Huber's "a(n) is even" for maximal integer-sided
   cyclic polygons (his document proves the prime and semiprime cases and leaves parity
   open; a reduction to Gaussian π-blocks sketched, unverified); A398446/A395725 —
   Norton's conjectured closed forms for 1324-avoiders with the maximum d places from the
   end; A397153 (Goupil's 12×n snakes g.f., provable by a max-plus transfer matrix).
   Scout C (erdosproblems.com, 636 open problems parsed, ~40 forum threads read):
   #817 — exact values of the Erdős–Sárközy function g₃(n) (no exact value recorded
   anywhere; the scout certified g₃(1..6) = 1, 3, 8, 22, 60, 168 during scouting — a
   future session's OEIS-level target; Korsky arXiv:2606.24139 has the 3ⁿ/√n bound);
   #176 — N(15,2) and the UNSAT side of N(17,2) = 274 (Doc_dent, forum, Aug 2026, DRAT
   for k = 13; a few-hour SAT job for k = 15, a stretch for k = 17); #272 — t(N) for
   N ≤ 12 unconditionally (max-clique; StijnC's forum values are conditional); the Open
   Problem Garden's associahedron chromatic number (χ unknown from n = 11; likely still
   4); #1066 (construction against Pach–Tóth's 5/16, high risk). Rejected with reasons:
   #82, #552, #583, #217, #1093, #1188/1189 (chenhaoyu, 3 Sep 2026), #835, #634, #1056,
   #1142, #961, #689 — all swarmed or beyond 4 cores.
   Scout D (MathOverflow API, six months, plus West's list): Zhi-Wei Sun's prime-
   difference determinant conjecture (OEIS A228638; MO 514613, Aug 2026; det ≠ 0 checked
   mod a prime to 1500; a Levinson recursion reaches 10⁶ in hours — "more data");
   MO 512325 (two arcs of a strong tournament on the same Hamiltonian paths); the finite
   calculation left open in Jain–Kravitz Theorem 1.3 (S₁(4) ∩ (1/4, 1/2], MO 512117);
   Timothy Chow's Hold-That-Line variants (MO 514313); perfect trading schedules for odd
   n (MO 510979). None chosen: each is either a range extension or a small exact
   computation without a proof edge; the Jain–Kravitz calculation is the one worth a
   future look.

   **Second external target, taken up after the first was finished (13:00 checkpoint
   not needed):** Basti–Cremaschi's open residue class, the scout's candidate 3 above —
   see `conjectures/triangulation-discrepancy/` and the Result section below.

**Internal-thread assessment** (parallel audit of all 25 conjecture READMEs and the
ten most recent logs). Last two sessions: kobon-triangles/power-residue-pairs (09-02)
and bit-deletion with a peaceable-queens secondary (09-03) — no forced rotation.
Strongest live thread: **peaceable-queens a(18)** — refute army size 48 on the 18×18
board with the validated SYM16 engine (n = 15/16/17 took 1.48·10⁹ / 5.03·10⁹ /
2.15·10¹⁰ nodes, growth ×3.4, ×4.3; projection 8.6–9.1·10¹⁰ nodes, 2.0–2.4 h wall on
4 workers), with the 47-queen witness from Kamenetsky's A250000 link file verified by
`check_peaceable` before any run (47 white + 48 black, no attacks). Either verdict
changes the row (a(18) = 47, or a(18) ≥ 48 beating Ainley). Everything else is a
compute wall (graham-rearrangement p = 41 at 12–17 h, grimm 10¹³ at 7–9 h, nci-datrees
n = 16, erdos-gyarfas n = 19, odd-giuga m = 13 at ~50 CPU-days, distinct-subset-sums
f(10) in months) or an ideas wall (strong-truncations Conjecture C, finch Conjecture A,
circular-thresholds n = 8). Selection argument: the mandate's default is external, and
candidate 1 beat the internal thread on (a) — a proof, not a search — and on (b) —
three days old, nobody else on it; it loses on citation surface (a four-author paper
versus OEIS A250000). Ties go to the new problem. Because the external attack is
CPU-free (proof plus a 12-second computation) and the a(18) run needs only cores and
patience, the internal thread was launched as a **secondary target** in the
background at 11:54 UTC rather than instead — the same division as on 09-03.

**Attempt statement.** Prove that ρ(n) < 1 for every n ≥ 496, where
ρ(n) = max_{1≤a<n/2} R_n(a) and R_n(a) = ((n−2a+1)/(n−a))·C(n,a)·C(n−2,a−1)·n/C(2n−2,n−1),
with every finite part exact and reproducible; achieved means a written proof for
n ≥ N₀ and an exact certificate on [496, N₀).

**What failed.**
- *First analytic bound* (central-binomial squared with the crude split of the
  maximisation): < 1 only from n ≈ 5000; replaced by the exact maximiser of
  (2x+1)e^{−4x²/n} and Robbins' two-sided bounds (threshold 3000; 2000 would do).
- *Hand-rounded constants*: the first draft claimed U(3000) < 0.9937; the rational
  certification gave 0.993849, so the statement became 0.9939. A first mental count of
  the sporadic values (56) was wrong; the script's count is 82.
- *Theorem B(iv)*: the first write-up of the lower bound forgot the first-order term
  F′(x*)(x_n − x*) (F′(x*) ≠ 0 because of the factor n/(n−a)); corrected — it is O(1/n)
  and changes nothing, but the proof as first written was incomplete.
- *Nothing else in the first problem*: it was smaller than the day, which is why a
  second external problem was taken up.
- *The general proof for n ≡ 5 (mod 6)* (triangulation-discrepancy): the single-flip
  argument closes the case where the big class has only degree-3 vertices, but a
  vertex of degree ≥ 5 in the big class can block every flip (its link has the flipped
  vertex next to an S-vertex and an F–B edge elsewhere). Three approaches were tried
  and are recorded in the NOTE §6: general flipped sets X ⊆ V₂ (closed under the
  blocking relation — whole Kempe components are closed and always miss by exactly one,
  as they must), Kempe-chain constraints (all (i,j)-components inside W balanced; a
  unique (1,i)-component with a surplus of colour 1), and a counting bound on blocking
  capacity (Σ_H deg ≤ 3|H| + 2m − 1, not enough for m ≥ 4). The computation at n = 23
  shows every structured candidate has discrepancy 1 — far from tight — so the missing
  argument should be soft; it was not found today.
- *Operations*: a census driver relying on `/usr/bin/env time` (absent) produced empty
  logs on its first run; a stray invocation of the same driver inside the repository
  directory created junk files (deleted); two background jobs left by a scouting agent
  competed with the a(18) run for an hour before being noticed and killed.

**Next.** (1) The residue class n ≡ 5 (mod 6) in full: prove that some single flip
survives the blocking by high-degree big-class vertices (NOTE §6 of
triangulation-discrepancy lists the facts already in hand), or push the flip lemmas
into the generation to certify n = 29 (plane graphs on 15 vertices with 32–39 edges —
plantri counts measured at the end of the session). (2) Explicit constants in Theorem
B's O(1/n) term (antidiagonal-anomaly), which would turn the rounding explanation of
the sporadic set into a theorem describing it exactly. (3) Cordella's Question 6.6
(max vᵢ < 3q for near-tight sextuples) as a proof target, since an effective Lemma 2.4
would make his Theorem 6.1 unconditional. (4) Erdős #817 exact values g₃(7), g₃(8) and
an OEIS entry (scout C's certified g₃(1..6) are in the session scratchpad only and
should be recomputed before use).

**Session hygiene.** Branch: harness-designated `claude/affectionate-sagan-drm6st`
(the mandate's per-conjecture branch name overridden by the harness requirement, as in
previous sessions). The `conjecture-research` skill named in CLAUDE.md is not installed
here; CLAUDE.md followed directly. Hardware: 4 cores, 15 GB; Python 3.11.15; gcc. No
seeds; no floating point in any certified path.
