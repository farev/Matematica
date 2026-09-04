# 2026-09-04 — peaceable-queens (secondary target, same day as antidiagonal-anomaly)

**Target.** a(18) of OEIS A250000: decide whether 48 + 48 peaceable queens
fit on the 18 × 18 board (recorded bracket [47, 81], Pratt 2014, secondary;
A250000 still ends at a(15) as fetched today). The day's primary session was
external (`log/2026-09-04-antidiagonal-anomaly.md`, which carries the
connectivity check, the slate and the internal-thread assessment); it did
not need the cores, and the audit had named a(18) the one internal thread
breakable in an afternoon (projection 8.6–9.1·10¹⁰ nodes, 2.0–2.4 h on
4 dedicated workers from the ×3.4, ×4.3 growth at n = 16, 17). Launched at
11:54 UTC after a calibration run reproduced a recorded n = 15 chunk to the
node.

**Result.** **CERTIFIED — a(18) = 47.** (i) Upper bound: exhaustive
refutation of army size 48 by the SYM16 engine rebuilt from source: 16
resumable chunks, every chunk UNSAT, NODES_TOTAL nodes, ENGINE_S s of engine
time (≈ ENGINE_H core-hours), WALL_S s wall on 4 workers that were shared
with other jobs for about two hours (chunk sizes MINCHUNK to MAXCHUNK nodes;
records `results/n18_m48_bnb_sym_chunk*.txt`, committed one by one as they
completed). (ii) Lower bound: Kamenetsky's 47 + 48 placement from the
A250000 link file passes `check_peaceable`
(`witnesses/witness_n18_m47_kamenetsky.txt`). Node growth over n = 17:
×GROWTH. Documents updated: README (row 7, reproduction, caveats), NOTE §6c
and §7, WRITEUP session-3 section, PAGE.md (page update), index row.

**Caveat, stated as a defect.** Single-engine exhaustion (as at n = 17): the
plain-engine replication (≈ 9× the nodes, ≈ NODES_PLAIN, ≈ HOURS_PLAIN h)
was not run. No engine-found witness this time: the lower bound is the
checker-verified literature placement only.

**What failed.** Nothing in the run. The wall time nearly doubled the
projection because the cores were shared: a 15-minute census, an
enumeration for the triangulation problem that cost seven core-hours instead
of the twenty minutes estimated (paused after an hour, resumed at the tail),
and three background processes left behind by scouting agents. Engine time,
not wall time, is the figure to compare across rungs.

**Next.** (1) Plain-engine replications of n = 17 and n = 18 to restore the
two-engine standard. (2) a(19): Ainley's 52; the m = 53 refutation at ×4–5
per rung is ≈ NEXT_NODES nodes, ≈ NEXT_HOURS h on 4 dedicated cores — a
full session, launched first thing. (3) Submit a(16..18) to OEIS A250000
with the witnesses and chunk records — a decision for the local session.
