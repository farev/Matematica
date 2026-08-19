# 2026-08-19 — plus-minus-davenport

**Target.** Decide the last unknown plus-minus weighted Davenport constant of
order ≤ 100: Marchan–Ordaz–Schmid (IJNT 2014, (secondary)) determined
`D±(G)` for every abelian group of order ≤ 100 **except `C5 ⊕ C15`**, where
they could only show `D± ∈ {6, 7}`. Decide it, and the first open case of the
next family, `D±(C7 ⊕ C21) ∈ {7, 8}` (order 147, outside their range). Wrap
both in the first systematic exact table of `D±` over all abelian groups of
rank ≤ 4 in reach of a 4-core afternoon, with every value carrying a
triple-verified exhaustive certificate, plus the floor/cap structure theory
(dissociated-set reformulation) that the table exposes.

**Branch note.** The session mandate asks for `claude/<conjecture>-YYYY-MM-DD`;
this environment designates `claude/kind-bohr-phpifj` and forbids pushing
elsewhere. Working on the designated branch, as previous cloud sessions did.

**Skill note.** CLAUDE.md mandates the `conjecture-research` skill; it is not
installed in this sandbox (`.claude/` contains only `settings.json`). Followed
the written discipline in CLAUDE.md directly.

## Connectivity check

- **WebFetch: fully blocked** (EGRESS_BLOCKED from the sandbox proxy), tested
  2026-08-19 against arxiv.org, oeis.org, erdosproblems.com,
  mathoverflow.net, and non-list hosts hal.science and export.arxiv.org.
  No primary source was readable from this session.
- **WebSearch: working.** All literature claims below come from search-result
  snippets retrieved 2026-08-19. **Every citation in this session is
  (secondary)**, and every "this is open" claim is as strong as today's
  snippets, no stronger.
- Machine: 4 cores, 15 GB RAM, Python 3.11.15.

## Candidate slate (external)

Three vetting sweeps were run in parallel (two scout subagents + one
dedicated openness-vetting subagent; 28–66 search queries each, all
snippet-level). Full evidence trails preserved in `WRITEUP.md` of the
conjecture directory.

**C1 — the plus-minus weighted Davenport constants `D±(C5⊕C15)` and
`D±(C7⊕C21)` (zero-sum combinatorial number theory). Chosen.**
Statement: for finite abelian `G`, `D±(G)` is the least `ℓ` such that every
sequence of `ℓ` elements of `G` has a nonempty subsequence with signs
`ε_i ∈ {±1}` making `Σ ε_i g_i = 0`. Sources checked 2026-08-19 (all
secondary, via snippets): Marchan–Ordaz–Schmid, "Remarks on the plus-minus
weighted Davenport constant", Int. J. Number Theory 10(5) 2014 1219–1239
(arXiv:1308.3316, HAL hal-00835688): snippet from the HAL PDF — "The only
group of cardinality at most 100 where the value of the plus-minus weighted
Davenport constant remains unknown is C5 ⊕ C15, where it is either 6 or 7";
a second independent digest agrees. `C7⊕C21` (order 147) has bounds {7, 8}
and lies outside their determination; no snippet names it with a value.
Later work checked: Perez-Lavin's 2021 U. Kentucky thesis ("The Plus-Minus
Davenport Constant of Finite Abelian Groups": state of the art "primarily
known when the rank of G is at most two and |G| ≤ 100"; computed values in
100 < |G| ≤ 200 "with some exceptions" — coverage of 147 unresolvable from
snippets, caveat carried below); Adhikari's 2017 survey; the 2024–2026
monoid-line papers (2404.17258, 2506.14279, Merito–Ordaz–Schmid 2025);
Mondal–Paul–Paul 2021–2026 (cyclic only). None shows these values computed.
Why believed open: the ≤ 100 statement is explicit; 12 years of citing
literature restates rather than resolves it.

**C2 — Erdős #1107 / OEIS A056828: integers that are not the sum of at most
three powerful numbers (computational number theory). Runner-up.**
Six known terms 7, 15, 23, 87, 111, 119; Mollin–Walsh (1986) conjectured
completeness; Heath-Brown proved finiteness; OEIS records "no other terms
less than 40,000,000" — a ~20-year-old frontier. A 4×10⁷ → 10¹¹ certified
sieve (≈ 2,500×, ~12.5 GB bitmap, 1–2 h on this box) is feasible. Not chosen:
it is a range-extension, not a decision of a named constant; and it is
subject-adjacent to this repo's powerful-progressions directory (mandate
prices novelty). Recorded as a strong future session.

**C3 — γ(Q₇³), the 3-D queens domination number at n = 7 (chessboard
combinatorics / graph domination). Not chosen.**
Ramani, "On the Structure of 3D Queen Domination" (arXiv:2604.03793, Apr
2026) certifies γ(Q_n³) for n ≤ 6 by ILP ("for n = 6 … approximately 5
seconds") and leaves n = 7 the smallest open case (343 vertices). Feasible
in principle, but the 2-D history says UNSAT/optimality blowup at the lower
bound is the real cost, the author demonstrably owns better tooling, and it
would be the second queens-flavored session in three days.

Also vetted and held for future sessions (recorded so the searches are not
redone): `s(5,1) ∈ {11,12,13}` from Gao–Hui–Jiang–Li–Wang / Sun
(arXiv:2606.18234, June 2026; conjectured `s(p,1) = 2p+1`; definitional
reconstruction from snippets has one unresolved reading — pin against the
PDF first); exact `f(17), f(18)` for Erdős #584 (no two cycles of equal
length; exact values stop at n = 16 since 1988); the plus-minus Harborth
constants `g±(C3⊕C3n)` (unpublished per today's snippets). Killed with
evidence: Erdős #82/G(6) (Dyson–McKay arXiv:2604.08215 own it), #587
square-sum-free (AlphaEvolve shadow), minimum overlap (LLM-optimization
arms race), #11 (2⁵⁰ frontier), odd covering systems (idea-bound),
1/3–2/3 at 15 (order-14 census closed July 2026, arXiv:2607.23926).

Subfields spanned: zero-sum/additive combinatorics, computational number
theory, chessboard combinatorics/graph domination.

## Internal-thread assessment

Read the 08-14..08-18 logs and the vdw-mixed / generalized-schur READMEs.
Rotation rule: last two sessions were peaceable-queens (08-17) and
undirected-thresholds (08-18) — no conjecture is at two consecutive sessions;
nothing is blocked.

Strongest live internal threads:

1. **peaceable-queens a(17)** (08-17 "Next"): recorded bracket [42, 72]; the
   boundary refutation was priced in-session at ~5–8× the n = 16 cost — an
   hour-scale run on this hardware with a validated engine. Row-changing (a
   second new A250000 term). This is the single strongest internal thread.
2. **generalized-schur (4,4,u)** (08-07 "Next"): the ladder was blocked on
   DRUP-in-RAM (pysat OOM); apt cadical un-blocks it (verified installable
   08-17). Row-changing if several values land, but it would be the third
   Rado/Schur DRUP session in two weeks.
3. **vdw-mixed w(2;5,8)**: resumable cube-and-conquer campaign; the exact
   value is CPU-months away; extending the lower bound past 295 is the
   excluded "extend by 10%" shape.
4. **undirected-thresholds**: yesterday's conjecture; the 20k-wall needs a
   solver-grade engine (a full session of engineering, unclear payoff).

## Selection

C1 wins on all three criteria, against the slate and against the internal
threads. (a) Compute-breakability was not estimated but **demonstrated
during vetting**: a 40-line prototype decided both headline groups before
selection was final (C5⊕C15 in 1.5 s / 139,052 DFS nodes; C7⊕C21 in 35 s /
16.5M nodes), validated on 15 cyclic controls, 8 brute-forced rank-2 groups,
and — after the vetting report landed — on every published value it names
(C2⊕C4 = 4, C3⊕C3 = 3, C3⊕C3⊕C9 = 6, 2-groups at the cap, cyclic
⌊log₂n⌋+1). The bottleneck was never compute; it is that nobody with the
2014 paper open apparently ran the search. (b) "Already done?" was vetted
by a dedicated 34-search subagent: the ≤ 100 statement names C5⊕C15 as the
unique unknown; the one residual risk (the 2021 thesis's partial
100–200 coverage, for C7⊕C21 only) is carried as a prominent caveat, not
ignored. (c) The result completes a specific published table
(Marchan–Ordaz–Schmid IJNT 2014), answers the state of the art quoted in a
2021 PhD thesis, and feeds an active line (the B±(G) monoid papers,
2024–2026, whose arithmetic depends on D± values). The internal thread
(peaceable-queens a(17), hour-scale, row-changing) loses: it is another
term of a sequence whose smallest open case this repo already took, in a
groove worked two days ago, versus deciding a constant left explicitly open
in print for 12 years in a subfield this repo has never touched.
Default-external applies and the argument is not close. Rotation rule
satisfied (last two sessions: peaceable-queens, undirected-thresholds).

**Today's specific attempt.** (1) `D±(C5⊕C15)`: decide 6 vs 7 with an
exhaustive, cross-verified, committed certificate. (2) `D±(C7⊕C21)`: decide
7 vs 8; the upper bound is a one-line proved lemma (subset sums of a
dissociated set are distinct), so a verified witness alone decides it.
(3) The systematic table: every abelian group of rank ≤ 4 with every cell
carrying exhaustive certificates from ≥ 2 independent engines (target:
all |G| ≤ 256 at rank ≤ 2 plus targeted larger cells and rank-3/4 cells).
(4) The structure the table exposes, proved where possible: the
floor/cap two-value window, forced families, the dissociated-set
reformulation, cap-achievement phenomenology. Success = (1) and (2)
decided with certificates; the table and structure are the body of the
note. Mid-session checkpoint: if the exhaustive negatives do not
cross-validate, ship only what does, labeled honestly.

**Result.**
**CERTIFIED (headline) — D±(C5⊕C15) = 6**: the last unknown plus-minus
weighted Davenport constant of order ≤ 100 (per MOS-2014's determination,
(secondary)) is decided. Lower bound **PROVED** (explicit dissociated
5-set via binary sets in the factors; also from-definition verified);
upper bound CERTIFIED by six independent exhaustive computations across
three distinct methods: DFS census over sign-representatives (139,052
nodes; C and Python engines agreeing node-for-node), the same DFS with no
sign reduction (3,520,083 nodes; per-size counts matching the predicted
2^l identity in every class), plain combination enumeration over both
universes (2,324,784 and 185,250,786 six-element sets, zero dissociated),
and a class-injectivity reduction over F₅² (Lemma R; all seven splits
infeasible).
**CERTIFIED — D±(C7⊕C21) = 8**: first case of the next open family
("unknown already for n = 3", (secondary)). Upper bound **PROVED**
(subset-sums cap, NOTE Lemma 2 — valid for all G, not just odd order);
lower bound an explicit 7-set verified against all 2,186 signed subsets;
2,016 maximum dissociated 7-sets counted up to sign. Carries a prominent
caveat: the 2021 Perez-Lavin thesis computed values in 100 < |G| ≤ 200
"with some exceptions" and its coverage of order 147 could not be checked
from this sandbox.
**CERTIFIED — first open case of the Perez-Lavin thesis conjecture**: the
thesis conjectures D±(C2⊕C3^r) fails the basic upper bound as r grows
((secondary)); the table decides where failure begins — attained for
r ≤ 3, first failure at r = 4 (dim±(C2⊕C3⁴) = 6 < 7, order 162; E2
re-verification of the cell in `certs/`), same coverage caveat as C7⊕C21.
**CERTIFIED — the table**: dissociation numbers dim± = D± − 1 for 300+
groups of rank ≤ 4 (exact count in `data/table.csv`), every cell an
exhaustive search with node count = #±zsf multisets, cross-checked
engine-vs-engine; literature controls (C2⊕C4, C3⊕C3, C3⊕C9, C3⊕C3⊕C9 = 6,
2-groups at cap, cyclic ladder) all reproduced.
**PROVED** — the floor/cap window (subset-sum cap for every finite abelian
G; concatenation floor maximized over cyclic decompositions), forced
families (all 2-groups; C2⊕C2n recovering the known formula), cyclic
values, dim±(G⊕C2) ≥ dim±(G)+1, and **Lemma R** (dissociativity in
C_p⊕C_3p ⟺ class-injective subset sums in F_p²), which also shows no
counting argument can decide C5⊕C15 (class sizes 22/21/21 ≤ 25).
**Structure findings (data)**: every rank-2 group computed sits at an
endpoint of its window — only C3⊕C3 and C5⊕C15 stuck at floor; first
strictly-intermediate value at rank 3 (dim±(C3⊕C3⊕C15) = 6 ∈ (5,7));
appending C2 can add 2 (C5⊕C15 → C5⊕C30: 5 → 7); 75 = 3·5² fails its cap
while 147 = 3·7² achieves a tighter one.

**What failed.**
- The "1.5-second computation ⟹ cannot be open" inference — vetting
  (34-search dedicated agent) says it really was open; the community
  apparently never ran the search. The session's weight moved to
  verification redundancy and structure accordingly.
- The naive dichotomy conjecture ("dim± ∈ {floor, cap} always") died at
  order 135: C3⊕C3⊕C15 = 6, strictly inside its width-2 window — killed
  by the table within the hour of being formed. Demoted to a rank-2
  question (NOTE Q2).
- The hand-proof timebox for the 75 negative: two counting attacks (fiber
  counting over the Z5² projection; a ν: x ↦ σ−x involution structure on
  the class-0 value set) both end at "22 ≤ 25, no contradiction". Lemma R
  then explains why counting must fail. Productive failure — it became
  engine E5 and the sharpest open thread.
- Aut(G)-orbit search reduction: designed (orbit-block soundness argument
  worked out), then discarded — it complicates the exhaustiveness
  argument certificates rest on for a ~3× saving that mattered nowhere.
- Process hygiene, twice: a `pgrep -f`-based kill matched the invoking
  shell's own command line and killed it (exit 144) — the exact failure
  class in the 08-13 and 08-17 logs; switched to literal-PID kills. A
  background verification run silently wrote nothing because its shell
  was in the repo root and `certs/` didn't exist there (swallowed
  redirect failure); relaunched with explicit `cd`.
- The C23⊕C23 stretch (window {8,9}, motivated by an unverified
  "23, 46, 47" snippet): the seeded hunter that finds 147's maximum set
  in 366 restarts found no 9-set in its 30-minute box. Proves nothing;
  recorded as such.

**Next.**
1. Read the primary sources (arXiv:1308.3316, Perez-Lavin thesis, Adhikari
   survey) from a machine with egress — every citation this session is
   (secondary), and the thesis's 100–200 coverage decides whether
   D±(C7⊕C21) = 8 is new or a confirmation.
2. Human proof of the F₅² infeasibility behind Theorem 1 via Lemma R
   (finite, structured; the b = 6 case is six elements of F₅² with subset
   sums injective on |A| mod 3 classes).
3. The rank-2 endpoint dichotomy (NOTE Q2): prove or refute; a
   characterization of cap-achievement would decide infinitely many D±
   values at once.
4. C23⊕C23 ∈ {9, 10}: longer witness hunt (decides at cap if found, by
   Lemma 2 alone) or a ~10¹¹-node exhaustive campaign.
5. The plus-minus Harborth constants g±(C3⊕C3n) — apparently uncomputed
   ((secondary), conference-abstract-level evidence), one fixed-length
   constraint away from this engine family.
