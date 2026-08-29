# 2026-08-29 — parking-polytope

**Target.** OEIS A333331 (entry by Richard Stanley, Mar 2020): the number
a(n) of lattice points of P_n = conv(PF_n), the convex hull in R^n of the
parking functions of length n. Two conjectures stand in the entry, both
checked live today against the primary source: Howroyd (Jan 2024):
e.g.f. exp(−log(1−T)/2 + T/2 − T²/4) with T = −W(−x) the tree function;
Wiseman (Mar 2024): a(n) equals the number of "choosable" loop-graphs on
[n] with n edges (each edge can pick a distinct vertex). Amanbayeva–Wang
(arXiv:2104.08454, read in full today) determine a(n) only as a sum of
Postnikov-formula evaluations over sum-slices (their Theorem 5.2, not a
closed form — which is why the entry has been stuck at eight terms since
2020; terms from n = 9 on are only "expected" values derived from the
conjectured e.g.f., never independently computed), and their §6(b) asks
for the Ehrhart polynomial. Today's attempt: **prove a(n) = number of
loop-graphs on [n] with n edges all of whose components are unicyclic**
— which by two auxiliary lemmas (Hall's theorem for choosability; species
calculus for the e.g.f.) would prove both OEIS conjectures at once and
give the closed form Amanbayeva–Wang's theorem lacks — and, independently,
**certify new terms a(9), a(10), …** by exact integer dynamic programming
over Stanley's facet description, testing Howroyd's e.g.f. beyond its
8-term fitting range. Achieved means: the written proof plus certified
terms. Partial credit: proved reformulation lemmas, certified terms, and
an exact verdict on the e.g.f. at n ≥ 9.

**Result.** PROVED + CERTIFIED — the target theorem landed in full, plus
an Ehrhart theorem not planned at selection.

- **PROVED (Theorem A).** a(n) = number of loop-graphs on [n] with n
  edges, every component unicyclic; e.g.f.
  exp(−½log(1−T) + T/2 − T²/4). This proves **both** standing A333331
  conjectures (Howroyd Jan 2024, Wiseman Mar 2024) and **answers the
  open enumeration question of Selig, Electron. J. Combin. 31(3) (2024)
  §6** (|StoRec_n|, recurrent states of the stochastic sandpile on
  K_n^0), including its asymptotics half: a(n) ~ C n^{n−1/4},
  C = e^{1/4}√(2π)/(2^{1/4}Γ(1/4)) ≈ 0.746492. Proof chain: Stanley's
  facet description (via Amanbayeva–Wang, read in full) → polymatroid of
  edge-incidence ∂ → Hall/partial orientations → lift to Σ Δ_{{0,i,j}} →
  Postnikov Thm 11.3 with y = (0,1,…,1), every raising factorial = 1 →
  draconian sequences = "sparse multiforests" (multiplicity-≤2
  multigraphs, components tree/unicyclic; the identification is Lemma 4,
  the coned counterpart of Postnikov's forests example) → labeled
  dissymmetry (trees + edge-doubled trees = loop-rooted trees) →
  Wiseman's objects.
- **PROVED (Theorem B).** Ehrhart polynomial of P_n:
  i(P_n,t) = Σ_{sparse multiforests} t^s (t(t+1)/2)^d, closed e.g.f.
  (1−τ)^{−1/2} exp((2−t)τ/2t − τ²/4t), τ = T(tx) — answers
  Amanbayeva–Wang §6(b). The sum-form specializes Liu–Thawinrak
  (arXiv:2512.14199, Dec 2025) Cor 7.6, found mid-session in the novelty
  check and credited; the index-set identification and closed form are
  new.
- **CERTIFIED.** a(1)–a(40) (`a_values.txt`) — the first independent
  computation of any term past a(8); all 8 published terms reproduced;
  Howroyd's e.g.f. matched exactly to n = 40 (its previous support: 8
  fitted terms). Twelve-check verification battery, all exact
  arithmetic, incl. u(8) = a(8) over 30.2M subsets in C, exact rational
  hull membership at n = 3,4, and Ehrhart reciprocity (interior counts
  0, 0, 5, 96 at n = 2..5).

**What failed.** Two reformulation guesses killed by arithmetic in
minutes (Tutte evaluation: T(K_3;3,1) = 13 ≠ 17; a zonotope guess: 7 ≠ 3
at n = 2) — recorded in WRITEUP so they are not retried. The planned
burning-bijection route was superseded by the Postnikov route before it
produced anything (survives as an open question: a bijective Theorem A
via Selig's stochastic burning algorithm). A scout-level summary of
Liu–Thawinrak ("no lattice points content") was wrong and would have
produced an over-claim in Theorem B; caught by reading the PDF in full
before writing claims — no over-claim was ever committed. WebFetch is
403-blocked on oeis/erdosproblems/MathOverflow (curl works); some arXiv
/html/ versions 404 (PDF + pdftotext throughout).

**Next.** Upstream reporting from the local machine: OEIS A333331 edit
(conjectures → theorems, terms to n = 40, A368951 cross-reference), notes
to Selig (his §6 question), Howroyd/Wiseman, and possibly a short arXiv
note (math.CO) — NOTE.md is written to be its skeleton. Mathematical
threads (NOTE §9): bijective refinement via the stochastic burning
algorithm; the complete-bipartite analogue (Selig–Zhu WALCOM 2025 — the
same draconian machinery over K_{a,b} + cone should identify bipartite
sparse multiforests; a natural future session); AW §6(a) h-vector;
sign-reversing involution for interior points.

## Connectivity check

2026-08-29, cloud sandbox, egress-proxied. All four mandated sources
reachable today — a materially better day than 08-26/08-27 (when all were
blocked): arxiv.org works via WebFetch (listing + abs + html pages);
oeis.org works via curl (JSON API; WebFetch gets 403); erdosproblems.com
works via curl (problem pages + forum threads; WebFetch gets 403);
mathoverflow.net works via curl (WebFetch blocked). Consequence: openness
checks and quoted statements today are **primary-sourced** unless marked
(secondary). The `conjecture-research` skill required by CLAUDE.md is not
installed in this sandbox (no `.claude/skills/`; not in the session skill
list); CLAUDE.md discipline applied manually, as on 08-26/08-27.
Environment: 4 cores, 15 GB RAM, Python 3.11.15, gcc 13.3.0, kissat 4.0.4
built, python-sat/sympy/numpy/gmpy2 installed. Branch:
claude/awesome-lovelace-mfd66d (the session's provisioned branch; the
mandate's claude/<conjecture>-date pattern is overridden by the harness
branch assignment).

## Candidate slate (external)

Three scouts ran in parallel (Erdős database + forum threads via curl and
the teorth/erdosproblems mirror; recent arXiv 2024-09→2026-08 via WebFetch;
OEIS JSON API + MathOverflow via curl). Full reports preserved in the
session transcript. The slate, spanning algebraic combinatorics / additive
combinatorics / extremal combinatorics:

1. **A333331, lattice points of the parking-function polytope** (algebraic
   /enumerative combinatorics). Statement above. Sources checked today:
   oeis.org/A333331 (JSON, both conjecture comments verbatim, keyword
   `more`, 8 terms); arXiv:2104.08454 full text (Theorem 5.2 gives no
   closed form; §6(b) explicitly open); WebSearch for scoops finds the
   2022-2025 generalized-parking-polytope literature (2212.06885,
   2403.07387, 2512.14199) — Ehrhart results there are for the *weakly
   increasing* polytope (Catalan-many points, not this object) and the
   normal fan; nothing touches a(n). Why believed open: both conjecture
   comments stand unannotated in today's entry; the parking-polytope
   literature through Dec 2025 does not claim the count.
2. **Erdős #475, Graham's rearrangement conjecture — the verification
   frontier** (additive combinatorics / number theory). Statement
   (erdosproblems.com/475, fetched today): every A ⊆ F_p∖{0} can be
   ordered so all partial sums are distinct. Status DECIDABLE: the
   2024-26 theory (Bedert–Kravitz; Costa–Della Fiore; Pham–Sauermann;
   BBKMM/Müyesser–Pokrovskiy) proves it for all sufficiently large p with
   ineffective thresholds; the strongest published exhaustive check is
   Archdeacon–Dinitz–Mattern–Stinson (arXiv:1501.06872): all Z_n∖{0}
   subsets for n ≤ 25, by random search in Mathematica ("n = 24 took
   roughly 3 days" on a laptop). Attack shape: bitmask DFS + multiplier
   symmetry, p = 29, 31, 37 in a 4-core day (2^28 → 6.9×10^10 subsets),
   p = 41 a stretch. Guaranteed yield (frontier moves or counterexample),
   but the deliverable is verification-only; no structural theorem in
   reach.
3. **Non-nested ordered Ramsey numbers, Barát–Freschi–Tóth** (extremal
   combinatorics). arXiv:2512.15461 (Dec 2025) + C&C list 2511.02892
   Problem 1.1 (both fetched today): smallest m such that every 2-coloring
   of ordered K_m has a monochromatic non-nested matching of size n;
   trivially 3n−1 ≤ m ≤ 4n−2, conjectured = 3n−1, proved ≤ (2+√3)n
   asymptotically; posers "checked the small cases up to n = 5 or 6".
   Attack: SAT with DRUP proofs (no symmetry to break in ordered Ramsey),
   exact values for k = 6, 7, possibly 8 — first exact table, either
   confirming 3k−1 at new values or refuting the conjecture. Risk:
   encoding subtlety for "non-nested matching of size k"; Ramsey blowup
   past k = 7. Damnjanović–Đorđević (2607.06817, Jul 2026) did the
   *nested* analogue by SAT, not this one.

Also surveyed and set aside (scouts' full arguments in transcript): Cohen's
66 cyclic-number conjectures, arXiv:2508.08335/JIS 25.4.7 — the strongest
fallback: the paper's own verification pipeline is demonstrably buggy
(Ibarra 2607.09793 found a counterexample to its Conjecture 66 *inside*
the claimed verified grid, author-confirmed; scout reproduced it in exact
arithmetic today), so an independent certified audit + 10-1000× extensions
is guaranteed-yield — passed over because the target is diffuse across ~60
small conjectures rather than one theorem, but it stays first in line for
a future session. Tree Packing Conjecture first open case n = 12 (Erdős
#743; n ≤ 11 is Guichard–Massman 1990; thread moved twice in August,
memory-blowup risk on 15 GB). Erdős #64 (2^k-cycles; three groups touched
it in 100 days, incl. an uncertified SMS claim to n ≤ 31). Bicritical
snarks almost-Z₄/Z₂²-connectivity (C&C Problem 7.1, verified for THREE
graphs — tempting, but a third cubic-census session in four days for the
same audience). Lužar–Soták 2-homogeneous colorings (same genre concern).
Rajník ½-flow-pair census (poser's group owns the pipeline). A334086
(Sun's 216-term list, 100× extension validated at 10^7 — companion-grade,
not a primary target). A289587 mesh-pattern g.f. (proof possibly routine
for specialists). A181018 a(17) (solver-wall risk). Erdős #366 powerful
pairs to 10^23 (overlaps this repo's powerful-progressions machinery;
better as a planned continuation there). Erdős #375/#647/#993 all burnt by
2026 forum activity — the certified-search niche moves in weeks.

## Internal-thread assessment

Recent sessions: 08-27 balanced-colorings, 08-26 strong-truncations (no
two-consecutive rule in force). Strongest live internal thread: the
**balanced-colorings K₂₆ decision** (Erdős #617, r = 5) — a verdict would
change that row outright, and second place is pinning E*(26,6) ∈ [265,269]
/ E*(17,5) ∈ [104,108] exactly. Scored against the slate: fails criterion
(a) on its own session's measured evidence — the direct instance is
pigeonhole-hard (135-var K₁₀ defeats four modern solvers unaided; K₂₆
with BreakID + cardinality totalizers outlasted every window on this same
4-core class of machine), and the named unlock (verified symmetry
breaking at scale, cube-and-conquer) is a multi-day engineering build,
not a session. strong-truncations' open half is idea-bound (its hard core
contains the 2-edge-connected case); signed-difference-sets order > 36
collides with Masselot's active continuation; odd-giuga m = 13 is
measured at ~10¹⁵ nodes. No internal thread beats the externals on (a);
the mandate's default (external) stands.

**Selection.** A333331 over #475 and the Ramsey table: (a) all three are
compute-shaped for 4 cores, but A333331 uniquely pairs a guaranteed
certified deliverable (new terms via an exact DP over Stanley's facet
description — the first independent computation past a(8) ever) with a
provable-looking core lemma, and a session preference goes to "a proved
lemma that is new" over verification-only yield; (b) already-done risk
checked this morning against the live entry, the AW paper in full, and
the 2022–25 polytope literature — no trace of the count; #475 and the
Ramsey table both also pass (b) but their upside is a table, not a
theorem; (c) the result would extend Amanbayeva–Wang (closing the gap
their Theorem 5.2 leaves), prove two standing OEIS conjectures by named
active contributors (Howroyd, Wiseman) in an entry authored by Stanley,
and feed the active parking-function-polytope line (Hanada–Lentfer–
Vindas-Meléndez 2023, Liu–Thawinrak Dec 2025) plus Selig's sandpile link.
Working reformulation derived and hand-checked at n = 2, 3 before
selection: subtracting 1 from every coordinate, Stanley's inequalities
say exactly that the shifted lattice points are the integer points of the
polymatroid with rank function ∂(I) = #{edges of K_n meeting I}
(equivalently the Minkowski sum of the C(n,2) triangles conv{0,eᵢ,eⱼ}) —
i.e., the **in-degree vectors of partial orientations of K_n** — a
tractable combinatorial handle on both the computation and the proof.
