# vdw-mixed — session writeup

Session 1, 2026-08-16. Narrative including everything that failed; the
labelled results live in README.md and NOTE.md.

## How the target was chosen

The session opened external-first per the mandate. Three candidates were
slated (see log/2026-08-16-vdw-mixed.md): the mixed van der Waerden frontier,
the open cells of the Dec-2025 EJC paper on two-colour Rado numbers, and
tightness of ART(5). The Rado cells died on literature access (the paper —
and even the definition of its key term — is unreadable through the egress
proxy; attacking "their open cells" without being able to state them fails
honesty), ART(5) died on being idea-bound in a specialist school, and the
glamour vdW target w(2;3,20) died on feasibility arithmetic: its predecessor
w(2;3,19)=349 cost ~196 CPU-years on 200 Opterons in 2011 (secondary). What
survived: the mixed table's exact frontier at desktop scale — last moved by
Ahmed's w(2;5,7)=260 in 2013, before proof-logging became standard practice —
with w(2;5,8) as the open cell above it.

## Timeline and dead ends

1. **Encoder + brute controls** went cleanly: AP-count identity, brute-force
   w(2;3,3)=9 and w(2;3,4)=18, then certified (3,5)=22, (3,6)=32, (4,4)=35,
   (4,5)=55, (4,6)=73 in under a minute total, every UNSAT leg RUP-verified.

2. **Git choked on proofs.** The (5,5)@178 and (4,7)@109 UNSAT proofs are
   103 MB and 1.14 GB of DRUP; `git add` on 1.2 GB blew through two command
   timeouts and a container restart killed the in-flight solvers. Fix:
   `certs/.gitignore` excludes `*.drup`, small proofs are force-added
   individually, `certs/MANIFEST.csv` (sha256, size, verdict, solver) is the
   committed record, oversized proofs are re-derivable from committed
   scripts. Lesson recorded: proof-logged SAT at this scale needs a size
   policy *before* the first big run, not after.

3. **The binding constraint is extremal witnesses, not UNSAT proofs.**
   Expected the UNSAT legs to be the wall; wrong at first contact. CaDiCaL
   finds the (5,5)@177 boundary witness in 0.24 s but was still empty-handed
   after 15+ min at (5,6)@205 and 35+ min at (5,7)@259. CDCL is known to be
   weak on satisfiable vdW instances (the literature uses local search for
   lower bounds); reproduced that here the hard way.

4. **Sample-based tabu failed its positive control.** The first local search
   (best-of-48 sampled flips) stalled at cost 13 on the known-SAT point
   (5,7)@259 and could not even close a *single* defect from a cost-1 seed at
   (5,5)@177. Upgraded to WalkSAT-style violated-AP moves: still could not
   close that defect (the basin needs coordinated multi-flips). Local search
   as implemented was abandoned for witnesses.

5. **Structure to the rescue, incompletely.** This session's own witnesses
   show strong near-periodicity: (4,5)@54 is *exactly* 22-periodic and
   (5,5)@177 is 44-periodic with just 3 interior defects (positions 23, 89,
   122). A periodic-ansatz tabu over blocks (numpy full-string cost) found an
   exact 22-periodic witness at (4,5)@54 (control) and reached cost 1 at
   (5,5)@177, cost 12 at (5,6)@205, cost 49 at (5,7)@259 — near-misses only.
   Warm-starting CaDiCaL from those seeds (polarity hints via `set_phases`)
   closed none of them within 2–4 min budgets.

6. **Complete periodic projection.** The right tool: for period p, project
   the CNF onto p block variables (every AP clause collapses mod p); CaDiCaL
   then decides *completely, per period* whether an exactly-p-periodic
   witness exists at length n. Controls and production runs of this scan were
   in flight at the time of writing; results in README/NOTE.

7. **Ladder-vs-frontier re-scope at the mid-session checkpoint.** With
   witness legs resistant and the (5,6)@206 UNSAT leg already >1 h in
   Glucose, the honest projection for deciding w(2;5,8) this session went to
   ~nil. Re-scoped: primary result = certificate-backed ladder as deep as
   feasible (these cells have never shipped checkable proofs), stretch =
   (5,7)=260 certified, frontier work = certified lower bound for w(2;5,8)
   plus a resumable cube-and-conquer campaign. The cube-and-conquer driver
   passed its three controls (64/64 leaves closed on (4,6)@73; SAT cube
   detected at n=72; adaptive deepening closed 421 leaves under a forced
   300-conflict budget, zero check failures).

## Verification posture

Four independent legs: (i) encoder self-check against the AP-count identity;
(ii) brute-force ground truth for tiny cells; (iii) every witness re-verified
by a separate enumeration routine before being written; (iv) every UNSAT
proof checked by `tools/satcert/rup_check`, a from-definition C checker
sharing no code with any solver. Published values are used as *assertions to
reproduce*, never as inputs.
