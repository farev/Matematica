# 2026-07-30 — erdos-gyarfas

**Target.** A conjecture that dies by counterexample: the Erdős–Gyárfás
problem (erdosproblems.com #64) — must every graph with minimum degree ≥ 3
contain a cycle of length 2^k? Erdős and Gyárfás believed no. Plan: rebuild
the computational frontier from scratch with validated tooling, extend it
where 4 cores allow, and hunt the window where a minimal cubic
counterexample must live.

**Result.** CERTIFIED: no counterexample has ≤ 17 vertices — every
connected C4-free graph with min degree ≥ 3 on n ≤ 17 vertices contains an
8-cycle (34.8M graphs at n=17 scanned by geng + exact DFS checker; class
and checker validated against OEIS A007112/A002851/A014372, networkx
cross-check 71/71, split-consistency checks, and a positive-control
{4,8}-free graph that the filter correctly retains). Supersedes the
reported Royle–Markström bound ("at least 17", i.e. none ≤ 16); the n=18
sweep to push it further is running at session-write time — this entry is
updated when it lands. Also CERTIFIED: cubic {4,8}-free censuses:
none with n ≤ 22; a {4,8}-free graph at n=24 recovered by annealing and
triple-verified (networkx + SAT + relabelings: spectrum {16} only); full
n=24 census sweep running. 24 named cubic graphs incl. Foster (girth 10)
all conform. NUMERICAL: annealing hunts at n = 54..62: best energy so far
E=6 at n=56 — a graph with no C4/C16 and only three 8-cycles (spectrum
{8,32}).

**What failed.** The original plan — hunt at n = 26..30 — was obsolete
before it started: recon showed Markström's unpublished search already
covers cubic {4,8,16}-avoidance to n ≤ 52; the live window is 54 ≤ n ≤ 62.
Primary literature was almost entirely egress-blocked (arXiv, Wikipedia,
journals, authors' pages 403), so every paper-level statement in the note is
secondary-sourced and marked. Cage data (the 18 (3,9)-cages — the sharpest
untouched candidates) unreachable; the repo-mirror route was denied by the
permission classifier. A container restart killed the first n=24 sweep
mid-run; one driver bug (stale per-part logs summed after a mod change)
briefly produced an inflated count, caught by an unsplit control run.

**Next.** (1) The 18 (3,9)-cages at n=58: girth 9 kills {4,8}; screen them
for C16/C32 — nobody appears to have published this check. (2) Exhaust
n=19 min-degree-3 (~5×10⁸ C4-free graphs — a long weekend run), and build
generation-time C8 pruning for n ≥ 20. (3) Longer/hotter annealing in the
54–62 window; the chains get within a handful of 8-cycles of zero energy.
(4) Fetch primary sources (Markström 2004, Exoo 2014, Erdős's problem
papers) from an unblocked network and upgrade the secondary-sourced
citations. (5) Research page for fabianarevalo.com/erdos-gyarfas.
