# 2026-09-03 — peaceable-queens (secondary target, same day as bit-deletion)

**Target.** a(17) of OEIS A250000: decide whether 43 + 43 peaceable queens
fit on the 17 × 17 board (recorded bracket [42, 72], Pratt 2014, secondary;
A250000 itself still ends at a(15) as fetched today). The day's primary
session was the external Bit Deletion game (`log/2026-09-03-bit-deletion.md`,
which carries the connectivity check, the three-candidate slate and the
internal-thread assessment); it finished early, and the audit had named
a(17) the one internal thread breakable on this hardware in an afternoon
(session 1 projected 5–8× its 462-second n = 16 refutation). So the run was
launched on the freed cores rather than saved for a third session.

**Result.** **CERTIFIED — a(17) = 42.** (i) Upper bound: exhaustive
refutation of army size 43 by the session-1 SYM16 engine, rebuilt from
source: 16 resumable chunks, every chunk UNSAT, 21,454,699,264 nodes, 1712 s
wall on 4 workers (6,086 s engine time; chunk sizes 7.2·10⁷ to 2.56·10⁹
nodes). (ii) Lower bound: the 42 + 42 placement published by Kamenetsky in
the A250000 link file (2019; attributed to Ainley 1977) passes the
from-definition checker `check_peaceable` (42 white, 42 black, no attacking
pair) — `witnesses/witness_n17_m42_kamenetsky.txt`. Node growth over the
n = 16 boundary ×4.26, inside the ladder's ×3–5 per rung. Documents
updated: README (row 6, caveats, reproduction), NOTE §6b and §7, WRITEUP
session-2 section, PAGE.md (page update), index row.

**Caveat, stated as a defect.** This is a *single-engine* exhaustion. At
n = 16 the verdict was replicated by the plain engine (independent
canonical form, 45·10⁹ nodes, ~1 h); at n = 17 that replication is ≈ 9× the
SYM16 count (≈ 1.9·10¹¹ nodes, 4–5 h) and was not run. The label CERTIFIED
follows the repository's convention for exact, reproducible, chunk-recorded
exhaustions by a validated engine (16/16 plain/SYM16 agreement on the
ladder and at n = 16), and the README says exactly this.

**Witness search by the engines.** A capped (25 min, one core each)
attempt to have the SYM16 and plain engines find a 42 + 42 placement of
their own, as they did at n = 16 in under 30 s, was launched alongside the
write-up. Outcome: the **SYM16 engine found one in 116 s** (678,816,342
nodes, S = 255, T = 7199), a placement different from Kamenetsky's, and
`check_peaceable` accepts it (`witnesses/witness_n17_m42.txt`) — so
a(17) ≥ 42 now stands on the repository's own search, with the literature
placement as a second verified witness. The plain engine reproduced the
same placement (same canonical sets S = 255, T = 7199) in 212 s and
1,357,765,356 nodes (`results/n17_m42_sat_plain.txt`), as the two engines
did at n = 16.

**What failed.** Nothing in the run. The honest shortfall is the missing
second-engine replication, a time budget decision.

**Next.** (1) Plain-engine replication of the m = 43 refutation (~4–5 h;
`python3 run_chunked.py 17 43 16 4 ./bnb` — the plain driver default) to
restore the two-engine standard. (2) a(18): Ainley's 47; the m = 48
refutation at ×4 per rung is ≈ 8.6·10¹⁰ nodes, ~2 h on 4 cores — a full
session's main course, not a side dish. (3) Submit a(16) = 37 and a(17) = 42
to OEIS A250000 with the witnesses and chunk records — a decision for the
local session per repo policy.
