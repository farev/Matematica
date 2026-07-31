# 2026-07-30 — erdos-gyarfas

**Target.** A conjecture that dies by counterexample: the Erdős–Gyárfás
problem (erdosproblems.com #64) — must every graph with minimum degree ≥ 3
contain a cycle of length 2^k? Erdős and Gyárfás believed no. Plan: rebuild
the computational frontier from scratch with validated tooling, extend it
where 4 cores allow, and hunt the window where a minimal cubic
counterexample must live.

**Result.** CERTIFIED: **no counterexample has ≤ 18 vertices** — every
connected C4-free graph with min degree ≥ 3 on n ≤ 18 contains an 8-cycle
(834,711,846 graphs at n=18, 34.8M at n=17, scanned by geng + exact DFS
checker; class and checker validated against OEIS A007112/A002851/A014372,
networkx cross-check 71/71, split-consistency checks, and a
positive-control {4,8}-free graph that the filter correctly retains).
Supersedes the reported Royle–Markström bound ("at least 17", i.e. none
≤ 16) by two. Also CERTIFIED: cubic {4,8}-free censuses: none with n ≤ 22;
at n=24 exactly FOUR {4,8}-free cubic graphs (9.47M C4-free scanned) —
clean-room reproduction of Markström 2004; all girth 3, C16 counts
330/315/207/228 (exact manifold minimum at 24: 207), exactly one planar,
and that planar one is isomorphic to the graph the annealer had already
found independently — the Markström graph itself, triple-verified
(networkx + SAT + relabelings). Bipartite cubic girth ≥ 6:
none {4,8}-free at n ≤ 26. 24 named cubic graphs incl. Foster (girth 10)
all conform. NUMERICAL: hunts in the minimal cubic window n ∈ [54,62]
(focused-move annealing + steepest-descent polish + basin hopping): chains
at n = 54/56/58/60 all reach C4=C16=0 with only 3–4 disjoint 8-cycles; on
the {4,8}-free manifold the minimum C16 count achieved falls steeply with
order — exactly 207 at n=24 (census), ≤ 56 at n=56, ≤ 37 at n=58 (record
graphs committed, spectra {16,32}, verified by networkx + SAT). All
extremal graphs are triangle-rich, girth 3 — the same shape as
Markström's. No {4,8,16}-free graph found; the steep fall of the curve is
the session's strongest hint that the window may contain one.

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
citations. (5) ~~Research page for fabianarevalo.com/erdos-gyarfas~~ —
done next morning: `note_artifact.html` published; domain route pending.
