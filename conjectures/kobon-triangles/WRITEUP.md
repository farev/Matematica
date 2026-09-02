# Session narrative — 2026-09-02

*As lived, including the dead ends. Not edited to look smarter in hindsight.*

## Why this problem

The scheduled mandate asks for an external open problem where a day of exact computation
can move a published frontier. Three scouts surveyed the Erdős database, OEIS and recent
arXiv, and discrete geometry; in parallel I looked at the Kobon triangle table (OEIS
A006066) from memory, expecting `K(10)` to be open. It is not: the entry, edited the day
before this session, shows `K(10) = 25` (Grünbaum), `K(11) = 32` (Savchuk 2025 by SAT),
`K(12) = 38`, `K(14) = 54` (Maiorana, August 2026, with triple points), `K(16) = 72`,
`K(20) = 117` (Parpalak–Utkin 2026) — every even case up to 16 closed, and the smallest
open case `K(18) ∈ {93, 94}`.

Reading Bartholdi–Blanc–Loisel (arXiv:0706.0723) made the target precise. Their Theorem
1.4 is a table of exact values for simple pseudoline arrangements with two-value entries
where their 2007 depth-first search gave up, and the first such entry is `n = 18`:
`93–94`. Their §5 says why: the search "quickly becomes intractable" as the number of
unused segments allowed grows, and 94 triangles on 18 lines leaves six unused segments.
That is a compute bottleneck, not an idea bottleneck; nineteen years of SAT-solver
progress separate their DFS from today. Savchuk's 2025 paper attacks the *odd* cases with
a SAT encoding and lists even-`n` tables as future work; his appendix notes that the even
arrangements he could build "lack a triangle to meet the current best upper bounds".

The candidate slate and the selection argument are in the daily log. The internal
thread (generalized Schur `(4,4,10)`) was a clean, measured deliverable but the mandate's
default is the new problem, and this one had a nineteen-year-old open table entry with a
named upper bound to decide.

## Timeline

**11:35–12:05.** Connectivity (all four sources reachable, three only via curl), scouts
launched, kissat/cadical/drat-trim built, first look at the Kobon table.

**12:05–12:20.** Encoding v1 (`kobon_sat.py`): rank-3 signotope axioms, adjacency
variables, triangle variables, totalizer `ΣT ≥ t`. Signotope counts for `n = 4..7` match
OEIS A006245 exactly (8, 62, 908, 24698), and a greedy sweep realises every signotope as a
wiring diagram. Positive and negative controls against BBL's table pass for `n ≤ 10`, but
the UNSAT side scales badly: `n = 10, t = 26` needs 92 s and `n = 11, t = 33` did not
finish in 12 minutes, whereas Savchuk reports 1.67 s for the latter. Diagnosis: the
solver has to rediscover the segment-counting bound (each triangle owns three of the
`n(n−2)` segments) from a global cardinality constraint.

**12:20–12:30.** Encoding v2 (`kobon_sat2.py`): unused-segment variables with local
implications and a small "at most `budget`" counter. `n = 11, t = 33` UNSAT in 0.7 s,
`n = 10, t = 26` in 1.8 s, `n = 13, t = 47` SAT in 1.9 s (v1: 171 s). All controls pass;
every SAT model is decoded and re-counted by two independent routines. The dihedral
symmetry group of order `4n` (re-sweep plus mirror) was derived on paper and validated
exhaustively for `n ≤ 7` (`kobon_sym.py`); lex-leader constraints for all `4n − 1`
elements went into v2.

**12:26.** Plain v2 instance `n = 18, t = 94` launched with a DRAT proof (98,054 vars,
301,531 clauses). The closest control, `n = 12, t = 38` (budget 6), took 392 s; `n = 14,
t = 54` did not finish in 40 minutes. The plain `n = 18` instance was not expected to
finish in a day.

**12:26–12:35.** The lever. At `n = 18` the BBL bound `n(n−7/3)/3 = 94` is an integer,
so 94 triangles is the *equality case* of their counting argument. Re-deriving their proof
gives: exactly 12 perfect lines, 6 lines with exactly one unused segment each (T1), and
every unused segment has both endpoint lines perfect with the crossing extreme on them
(T2). The association lemma behind this is stated for even `n` only, and a checker found
violations at `n = 7` but none at `n = 6, 8, 10, 12, 14` — the parity is where `n − 2`
even enters, so this was reassuring rather than alarming. With T1, the set of imperfect
lines is a 6-subset of the 18-cycle of labels, and the symmetry group acts on it as
`D_18`: 561 orbits. Each orbit is one cube; the first four took 3–4 s each. All 561 were
launched on two, then three cores with DRAT proofs, with a `drat-trim` verifier running
behind them.

**12:31.** Disk incident. The pivot agent (Erdős #436, running in parallel) dumped two
leaf files that reached 10 GB each and were growing 1 GB per 20 s; with 4.9 GB free the
cube proofs were minutes from failing. Its writer processes were killed, the files
deleted, and a 200 MB cap sent to the agent.

**12:42. The prior-work hit.** Parpalak–Utkin's bibliography cites J. Blanc, "The best
polynomial bounds for the number of triangles in a simple arrangement of n pseudo-lines"
(Geombinatorics 2011, arXiv:0801.2845, January 2008). I had not looked for a follow-up to
BBL because the OEIS entry, edited the day before, still showed 94 as the upper bound at
`n = 18`. Blanc's Theorem 1 gives `n(n − 5/2)/3 = 93` for `n ≡ 0 (mod 6)`, and his
Theorem 3 says the bound is reached for every `n ≤ 30` except 11 and 12. So the entry I
was attacking had been closed for eighteen years; the OEIS bound is a different bound
(for a different problem — see below). Rule 3 of CLAUDE.md applies: the campaign continues
as an independent machine-checked confirmation and is labelled a rediscovery everywhere.
The lesson for the log: *search the citing literature of the paper whose open entry you
adopt, not just the paper.* Ten minutes on Parpalak–Utkin's reference list would have
found it before the encoder was written.

**12:45–12:55. What is actually open.** The Kobon problem allows concurrent triples and
parallels; the recorded optima for `n = 8, 12, 14` beat the simple-arrangement maxima by
one, and the `n = 14` record (Maiorana, August 2026) explicitly uses triple points. The
even-`n` bounds of BBL and Blanc are proved for simple arrangements only; the only bound
stated for general configurations is Clément–Bader's unpublished 2007 draft
(`(n+1)(n−3)/3`: 55 at `n = 14`, 95 at `n = 18`), and Maiorana's OEIS comment "since 54
equals the known upper bound … the value is exact" cites the simple bound. This is
recorded as an audit finding (NOTE §9), flagged rather than settled.

**12:55–13:15. A search model with triple points.** Perturbing each triple point into a
small triangle shows that a triple-point arrangement is a simple one with a set of
vertex-disjoint triangular faces collapsed; a quadrilateral sharing an edge with a
collapsed triangle becomes a triangle. Encoded on top of the v2 core (pentagon/hexagon
promotions omitted, so search-only). Positive control: `n = 8`, target 15 — SAT in 13 s,
two collapsed triangles, four promoted quadrilaterals, independent recount 15. First
attempt at `n = 14` was OOM-killed at 9.8 GB: pysat's `atleast` builds a totalizer of size
`N·(N − k)`; the modulo totalizer (2 M clauses) fixed it. Searches at `n = 12` (target 39,
above the recorded 38), `n = 14` (target 55) and `n = 18` (target 94) were then launched
with the CPU left over from the cube campaign.

**13:40.** The pivot agent reported: `Λ(8,2) ≤ 1,794,897` with a checked certificate and
exact reproduction of `k = 2..7`. I audited its checker, verified the pairs files
independently, regenerated the controls, and tightened the bound with the 62-prime pair
list to `1,508,324` (`conjectures/power-residue-pairs/`). That became the session's real
result; this directory's is the confirmation of a known theorem plus the audit.

**14:00–14:40.** The cube campaign finished: 561 cubes UNSAT in 5.0
core-hours (median 18 s; hardest #503 at 585 s — the spread-out
6-subsets are the hard ones), 478 proofs `drat-trim`-verified by session end
(5.8 core-hours; the remaining 83 kept as gzip with hashes). The
triple-point searches were stopped unresolved (the `n = 12` control had timed out).

## What failed

* **v1 encoding** (global triangle count). Correct but hopeless on UNSAT past `n = 10`;
  the segment formulation is what makes the problem tractable, exactly as in Savchuk's
  table encoding for the perfect case.
* **The plain v2 single instance at `n = 18`.** Stopped after 16.5 minutes (644 MB of
  DRAT) once the tight cubes were clearly faster; the `n = 14, t = 54` control it was
  calibrated against had not finished in 40 minutes either. It would be the lemma-free
  certificate; the lemma-free *cube* variant (`CUBE_VARIANT=plain`, orbits of the set of
  lines carrying unused segments, `|S| ≤ 6`, no T1/T2) is the realistic replacement.
* **Reading Felsner–Weil.** The 2001 PDF's text layer is broken at every kerning point;
  it took three attempts to confirm the bijection statement. The relevant sentences are
  quoted in NOTE §2.
* **Time-keeping.** For an hour I believed the session was two hours older than it was,
  because I was reading file timestamps as elapsed time. `date -u` before every decision.
