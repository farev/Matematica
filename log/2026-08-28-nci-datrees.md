# 2026-08-28 — nci-datrees (minimal counterexample to the Non-Cancelling-Intersections conjecture)

**Target.** First lower bound for the open problem posed *yesterday* in
arXiv:2608.27416 (H. Wilhelm, "Refutation of the Non-Cancelling-Intersections
Conjecture", §9 Open Problem 1): *what is the smallest lattice on which no
winning dot-algebra tree exists?* The conjecture of Amarilli–Monet–Suciu
(arXiv:2401.16210) that every finite lattice admits a winning da-tree was
refuted 2026-08-27 by a first-moment argument at ~1.1·10^15 elements, with no
explicit counterexample and no lower bound at all. Plan: exhaustively decide
winnability for every lattice with ≤ 14 elements (stretch: 15), by streaming
interior posets from `nauty-genposetg` and deciding each lattice by an exact
closure computation.

**Result.** (filled at session close — see below)

**What failed.** (filled at session close)

**Next.** (filled at session close)

---

## Connectivity check (2026-08-28)

| source | status | access path |
|---|---|---|
| arxiv.org | reachable | WebFetch and curl (abs, PDF, API) |
| oeis.org | reachable | curl only (WebFetch gets 403 through the sandbox proxy) |
| erdosproblems.com | reachable | curl only (WebFetch 403; site: 1217 problems, 565 solved) |
| mathoverflow.net | **unreachable** | blocked for both access paths |

The `conjecture-research` skill named in CLAUDE.md is not installed in this
cloud sandbox (`.claude/` holds only `settings.json`); the session follows the
CLAUDE.md discipline directly. Session branch:
`claude/awesome-lovelace-c8mtn6` (the branch provisioned for this remote
session; pushes are restricted to it, so the `claude/<conjecture>-<date>`
naming scheme is not available).

Environment: 4 cores, 15 GB RAM, gcc 13.3, Python 3.11.15, Debian nauty
2.8.8 (`nauty-genposetg`), poppler-utils; installed this session: numpy,
sympy, gmpy2, python-sat. No floating point anywhere in today's pipeline;
no random seeds (fully deterministic).

## Candidate slate (three external problems, three subfields)

**A. Smallest lattice with no winning da-tree** (order theory / database
theory). Source: arXiv:2608.27416 §9 OP1 (posted 2026-08-27, fetched
2026-08-28); original conjecture arXiv:2401.16210 (Amarilli–Monet–Suciu
2024); left-linear precursor arXiv:2608.19414. Openness: the problem is one
day old; arXiv full-text search for "non-cancelling" returns only these three
papers. The refutation is non-constructive (first-moment, ~1.1·10^15
elements); AMS's own search verified their set-family form only over ground
sets of ≤ 5 elements. No bound of any kind exists on the minimal lattice.
Attack shape: all lattices with n ≤ 14 elements arise uniquely as bounded
extensions of (n−2)-element posets; `nauty-genposetg` streams those, a
bitmask closure decides winnability exactly per lattice. CERTIFIED deliverable
either way (a bound, or an explicit counterexample).

**B. Zarankiewicz z(16,17;3,3) ∈ [132,133]** (extremal graph theory).
Sources checked 2026-08-28: OEIS A001198 (k₃(17) unknown; a(16) by Tan, Oct
2022, arXiv:2203.02283 — SAT on one laptop); arXiv:2608.08154 (2026-08-08)
leaves z(16,17;3) open as a certified interval [132,133]; arXiv:2608.26603
(2026-08-27) improves nearby lower bounds but not this cell. One SAT decision
(272 vars, 380,800 minor clauses + cardinality) with DRUP logging decides the
cell. Concern: the lane is being actively farmed this month by several
groups (three arXiv postings in August 2026), and dense UNSAT at 133 ones on
4 cores is unpredictable.

**C. Erdős #148 — compute F(9)** (number theory / Egyptian fractions).
Sources checked 2026-08-28: erdosproblems.com/148 (OPEN); OEIS A006585 =
1, 0, 1, 6, 72, 2320, 245765, 151182379 — a(8) by Dethridge, Jan 2004,
frozen 22 years, keyword "hard"; companion A002966 likewise. Bounds
Konyagin (lower; site thread repaired a proof gap 2025), Elsholtz–Planitzer
(upper). Attack: depth-9 exact enumeration with algebraic resolution of the
last two levels (divisor iteration on q² from tracked factorizations).
Estimated 20–200 core-hours — on this 4-core box the high end does not fit,
and a partial run yields nothing.

Also surveyed and passed over (with reasons, all checked 2026-08-28):
Asayama–Matsumoto discrepancy census at n=17 (arXiv:2608.21585; clean but
"verification at second open order" headline, plantri dependency);
ORS₂₀(2) ∈ {78,79} (arXiv:2608.14695; deficit-1 sweep likely 50× their n=19
cost — too heavy for 4 cores); queens-attacking-exactly-3 formula A051756
(proof engineering on 24-hour-old machinery of arXiv:2608.27432 — highest
ceiling, highest variance; that paper itself settled its k ≤ 1 cases twice
over within five days, so the family is hot); γ(Q₂₆) ∈ {13,14} (A075458,
open since 2001 — C(676,13) search space, structure theory needed, months);
Schütte f(4) ≥ 48 (erdosproblems.com/902; dense UNSAT stall risk); Erdős
#385 exception census 10^8 → 10^12 (guaranteed but evidence-only); ex(41;C₄)
∈ [132,133] (A006855/McKay's live table; his own enumeration is the
bottleneck); Erdős #885 k=5 factor-difference witness (25 simultaneous
square conditions; k=4 needed a paper).

## Internal-thread assessment

Strongest live internal thread: **peaceable queens a(17)** (recorded OEIS
bracket [42,72], Rob Pratt Dec 2014, unchanged as of today — A250000 still
lists data only through a(15), so even the repo's a(16)=37 is not yet
recorded there). The 2026-08-17 session's own projection prices the m=43
boundary refutation at 5–8× the n=16 run (≈ 40–70 min here), the engine is
generic in n, and either outcome changes the row (a(17)=42 decided, or a
certified a(17) ≥ 43). Honest P(row change) ≈ 0.6–0.65. Runners-up:
vdw-mixed finishing w(2;5,6)=206 (both legs genuinely unfinished; measured
×400 proof-logged cost jump plus a witness search that failed its positive
controls — P ≈ 0.3); strong-truncations Conjecture C open half (idea-bound,
"not day-shaped" per yesterday's own log). Balanced-colorings K₂₆ is not
day-shaped: the README's solver table shows a 135-var instance of an
already-proved theorem still `unknown` after 3 h here.

Defects noticed en route (fixed this session, separate commit): the
vdw-mixed README still described 2026-08-16 runs as "in flight"/"pending"
twelve days after that session's container died with no (5,6) certificates
landed; the 2026-08-27 log wrote E*(17,5) ⊆ [104,108] where the
balanced-colorings README's reasoned final value is [104,107].

## Selection

Chosen: **candidate A**, the NCI minimal-lattice frontier. Scoring per the
session mandate: (a) the bottleneck is exactly a CPU-day — `nauty-genposetg`
was measured at ~2.5M posets/s/core here, putting all 1.10·10^9 posets on 12
points (→ all 16,873,364 lattices on 14 elements) within minutes and the
3.4·10^10 posets on 13 points (→ all 152,233,518 lattices on 15 elements)
within ~2 h at 4-way parallelism, with the per-lattice decision an exact
bounded closure; (b) already-done risk is as close to zero as this game
allows — the problem was posed yesterday, names exhaustive search as newly
conceivable, and has no recorded bound; (c) the result slots directly into
the follow-up literature of a conjecture refuted this week (Wilhelm;
Amarilli–Monet–Suciu are the conjecture's authors and ran their own n ≤ 5
family search in 2024). Candidate B loses on (b) (three postings in the lane
this month) and carries 4-core UNSAT risk; candidate C's honest cost
estimate does not fit this machine and fails closed. The internal thread
(peaceable a(17)) matches A on feasibility but loses the mandated tie-break
to the new problem in a subfield this log has never touched; it stays queued.
Mid-session pivot criterion, set in advance: if by +3 h the per-lattice
closure cost explodes (fraction of lattices needing the full quadratic
closure ≫ 1%, projected n=14 wall > 4 h), fall back to peaceable a(17).

Result attempted, stated before the run: decide winnability for **every**
lattice with ≤ 14 elements (stretch 15). Success = a CERTIFIED statement
"the minimal lattice with no winning da-tree has more than N elements" with
generator counts matching OEIS A000112/A006966 at every size, a dual
independent implementation, and machine-verified explicit winning trees for
controls — or, jackpot, an explicit small counterexample (which would
strengthen a one-day-old refutation with the first explicit witness).

## Session narrative

(see `conjectures/nci-datrees/WRITEUP.md` for the full account)
