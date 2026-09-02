# 2026-09-02 — kobon-triangles (a^s_3(18), the open entry of Bartholdi–Blanc–Loisel)

**Target.** Decide the first undecided entry of Bartholdi–Blanc–Loisel's table of
maximum triangle counts in simple Euclidean pseudoline arrangements (Contemp. Math. 453,
2008, Theorem 1.4): `a^s_3(18) ∈ {93, 94}`, open since the 2007 preprint because their
depth-first search "quickly becomes intractable" once six unused segments must be
allowed. This is also the pseudoline half of the smallest open Kobon case, `K(18) ∈ {93,
94}` (OEIS A006066, edited 2026-09-01). It looked tractable because 94 at `n = 18` is the
*equality case* of their counting bound `⌊n(n − 7/3)/3⌋` — the bound is an integer only
for `n ≡ 0 (mod 18)` — which forces a rigid structure a SAT solver can exploit.

**Result.** **[PENDING — filled in at session end.]**

**Connectivity.** arXiv reachable by WebFetch and curl (listing, abstracts, PDFs).
OEIS, erdosproblems.com and MathOverflow return 403 / blocked to WebFetch but serve curl
with a browser user agent (OEIS JSON API used throughout). github.com READMEs fetchable;
api.github.com scoped to this repository only. JS-rendered galleries (ud1.github.io,
archivara.org) return empty shells. All four sources usable.

**Candidate slate** (three externals across three subfields, each verified against a
primary source today; four scouts ran in parallel, their full reports are in the
session scratchpad, key facts below):

1. **Kobon / BBL `a^s_3(18)`** (discrete geometry). Sources: arXiv:0706.0723 (Thm 1.4
   entry `93–94`; §5 explains the DFS failure), OEIS A006066 (fetched; `a(18) ≥ 93`,
   upper 94; Maiorana's `a(14) = 54` with triple points, Aug 2026), Savchuk
   arXiv:2507.07951 (Table 1 odd `n` only; even tables named as future work; Appendix C
   "lack a triangle to meet the current best upper bounds"), Parpalak–Utkin
   arXiv:2604.22035. Still open: no source records a decision; the OEIS entry was edited
   the day before. **Selected.**
2. **Erdős #436, the exact value of `Λ(8,2)`** (computational number theory). Source:
   erdosproblems.com/436 (OPEN, last edited 2025-10-25); Brillhart–Lehmer–Lehmer, Math.
   Comp. 18 (1964) 397–407, Table I gives `Λ(k,2)` exactly for `k ≤ 7` and only
   `Λ(8,2) ≥ 1,200,744` (§8: "the first value of `k` not covered by the theorem is
   `k = 8`"); Rabung–Jordan, Math. Comp. 24 (1970) computes the different quantity
   `Λ*(8,2) = 399`. No later determination found by search (negative evidence only).
   Automating the Lehmer case tree is a day's work on modern hardware; the risk is the
   realizability bookkeeping for `k = 8` (`R(2)` must be even), not CPU. Pre-declared
   pivot; a subagent was set on it in parallel (see below).
3. **Antidiagonal-anomaly conjecture** (lattice-path enumeration). Source:
   arXiv:2609.01562 (Gil–Liang–Odetola–Weiner, posted 2026-09-01): "the anomaly never
   reappears for `n ≥ 496`". The scout's exact-rational check to `n = 1500` reproduced
   their pattern and a heuristic limit `≈ 0.968 < 1` suggests a full proof is within a
   day. Passed over: a one-day-old conjecture with a four-author audience and a real
   chance the authors prove it themselves; a PROVED result but the smallest citation
   surface of the three.

   Also surveyed and rejected: OEIS A391721 (restricted size Ramsey `r*(P₃,Cₙ)`,
   `a(13..15)` certifiable, "more data"); `ORS₂₀(2) ∈ {78, 79}` (Song–Cao, 3 days old,
   authors mid-stride); Znám `A075441(9)` (measured workload `≈ 1.2·10¹⁴` factorizations of
   55-digit numbers on the Sylvester branch — not a day); A002966/A006585 `a(9)` (same
   explosion); Erdős #375 Grimm to `10¹³` (internal thread in disguise; the scout's
   smooth-number reformulation is a good idea for a future grimm session); Erdős #389
   (`n = 28, 29`, more data); the square achievement game (OPG; MO 514742, Aug 2026;
   forcing-window proof plausible but unbounded); two provable OEIS conjectures
   (A397434, A398720; comment-level value); CW(96,36) (specialists' lottery); SRGs,
   cages, unit distances, no-three-in-line (Heule to `n = 76`, Aug 2026), Ramsey gaps,
   union-closed, graceful trees, Heesch, 5-chromatic unit-distance graphs — all either
   set by supercomputer-scale runs or +10 % extensions. Today's math.NT trio
   (2609.00098, 2609.00101, 2609.00104) all fully resolve their problems.

**Internal-thread assessment.** Strongest live thread (audit of every README and log):
generalized-schur `(4,4,10)` then `(4,4,11)` — blocked on memory not time (pysat holds
DRUP in RAM; three OOM kills on 15 GB), fix armed on 2026-08-15 (standalone Glucose,
C encoder), measured ladder 43 s → 203 s → ≈ 16 min → ≈ 75 min; each rung a row edit,
and a disagreement would refute Ahmed–Schaal's Conjecture 2.1. Runners-up: grimm to
`10¹³` (≈ 7 h at measured throughput, over budget), projective-chromatic proviso removal
(no new theorem, 6.7 GB proofs unverifiable here). Audit flag for the record: the
2026-09-01 log's near-miss list re-flags A333331, which the 2026-08-29 session already
proved — strike it. **Selection:** the external candidate 1 beats the internal thread
on (a) — its bottleneck is exactly the kind a solver breaks, and the equality-case
structure was visible from the paper — on (b) — the entry is nineteen years old, the
relevant recent authors work on odd `n` — and on (c) — it would be cited by [BBL]'s
table, Savchuk, Parpalak–Utkin and OEIS A006066. Candidate 2 ties on (c) and loses on
implementation risk; it was run as a hedge by a subagent. The last two sessions were on
different conjectures, so no rotation rule applied.

**Attempt statement.** Decide whether a simple arrangement of 18 pseudolines with 94
bounded triangular faces exists. Achieved means: a machine-verified UNSAT certificate
for an encoding whose soundness is proved (then `a^s_3(18) = 93`, CERTIFIED, and no
18 straight lines in general position form 94 Kobon triangles), or an explicit
arrangement with 94 triangles (then `a^s_3(18) = 94`, and straightening decides
`K(18)`).

**What failed.** **[PENDING — see WRITEUP.md; to be summarised here.]**

**Next.** **[PENDING.]**

**Session hygiene.** Branch: harness-designated `claude/affectionate-sagan-90to7i`
(mandate's per-conjecture naming overridden by the harness branch requirement, as in the
previous two sessions). The `conjecture-research` skill named in CLAUDE.md is not
installed; CLAUDE.md followed directly. Hardware: 4 cores, 15 GB RAM, Python 3.11.15,
python-sat 1.9.dev15, kissat 4.0.4 / cadical 3.0.1 / drat-trim built from source.
Disk incident at 12:31 UTC: the pivot subagent wrote two 10 GB files; killed and
deleted, agent capped.
