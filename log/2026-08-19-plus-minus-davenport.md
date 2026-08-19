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
