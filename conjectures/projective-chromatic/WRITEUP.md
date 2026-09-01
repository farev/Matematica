# Session writeup — 2026-09-01 (session 1)

The unedited narrative, kept honest: what was tried, in order, including
what failed and the two self-inflicted wounds.

## Why this problem

The scheduled mandate was to survey outside the repo and default to a new
external problem. Three agents swept erdosproblems.com (all 1,217 problem
pages), recent arXiv, and OEIS. The winning candidate — χ₂(8) ∈ {5,6},
Problem 1 of Bishnoi–Cames van Batenburg–Ravi (arXiv:2512.01760) — was
the only one on the slate that is a *discrete open decision* rather than
a frontier extension: 255 points, 10,795 lines, a 1,275-variable direct
encoding, no solver work in the paper, nine months without follow-up,
and a loud payoff on one side (χ₂(8) = 5 ⟹ R(3;5) ≥ 257 vs the known
162). The statements were verified against the arXiv v3 text before
selection; the runner-up slate and the internal-thread assessment are in
the daily log.

## Timeline of the attack

1. **Controls first.** Pipeline rebuilt from scratch: line generator
   (counts checked against the closed form and OEIS A006095), SAT
   decisions reproducing χ₂(2..5) exactly, witnesses re-verified from
   the definition. The (6,4) UNSAT probe already refused to terminate in
   2 minutes — an early warning that the pigeonhole-shaped UNSAT side of
   this family is CDCL-hostile, exactly as the 2026-08-27
   balanced-colorings session found one repo over.
2. **Raw attacks launched in background** (they never landed): kissat
   plain + --sat on the full n = 8 instance; a simulated annealer that
   spent the whole session bouncing off a floor of 35 monochromatic
   lines, restart after restart. That floor being flat across 73
   restarts was the first hint of real rigidity.
3. **Algebraic ansätze.** Identify F₂⁸ with F₂₅₆; sweep all subgroups
   of the multiplicative-plus-Frobenius family, coloring orbit cells.
   Everything died, two ways: cosets of any subgroup of order divisible
   by 3 contain full lines (F₄*-cosets *are* lines — a two-line proof
   once seen), and the surviving quotients came back UNSAT. First
   certified structure: **no Frobenius-invariant witness** (35 cells,
   DRUP-verified). A second sweep over ~24 block-diagonal
   Singer/twisted/swap subgroups of GL(8,2) died even faster — any
   transitive block action is dead on arrival because a punctured
   invariant subspace sits inside one cell. Lesson recorded: for THIS
   problem, algebraic niceness is anti-correlated with feasibility —
   which is itself the interesting phenomenon, given that the analogous
   Ramsey-type objects at r = 2 (Paley-like) are algebraic.
4. **Local search, done right.** Plain min-conflicts gets stuck at ONE
   monochromatic line even at n = 7, where witnesses exist and CDCL
   finds them in a second — a striking rigidity signature. Adding
   breakout clause-weighting (bump weights of currently-monochromatic
   lines at local minima) cracked n = 7 instantly (~5·10³ flips per
   witness). The same engine at n = 8: ≈ 5×10⁹ flips (estimated), two seeds, nothing.
   This asymmetry is the strongest numerical evidence of the day for
   χ₂(8) = 6.
5. **The hyperplane pivot.** Lemma A (every class meets every
   hyperplane; every restriction is a full 5-witness of PG(6,2)) turned
   the problem into an extension question: sample witnesses of PG(6,2),
   try to extend over the affine half. Built a randomized-CDCL sampler
   (random GL(7,2) relabelings + kissat seeds), a structural
   fingerprint, and the 640-var extension SAT. Result: 1,000 samples,
   999 distinct fingerprints (the witness space is enormous;
   enumeration is hopeless), 0 extensions. A capacity analysis via
   exact Walsh–Hadamard spectra and Hoffman bounds shows capacity ≈ 2×
   requirement — so the obstruction lives at the packing level, which
   killed the cheapest theorem route (Σα < 128 would have *proved*
   χ₂(8) = 6 via Lemma A; the data says no such luck).
6. **The symmetry theorem.** Realizing the annealer/ansatz failures
   were data, not noise: classify what symmetry a witness could have.
   Lemma B fell out on paper — for Mersenne prime orders 3, 7, 31, 127
   an invariant subspace is a single orbit containing lines, so *no*
   invariant coloring exists, any n, any k. Cauchy + the factorization
   of |GL(8,2)| leaves odd orders 5 and 17 only. Order 17 is one Sylow
   class: contracted to 75 vars, UNSAT in milliseconds, 131-line DRUP,
   independently checked — the cleanest certificate of the day. Order 5
   has exactly two conjugacy classes ([C,C], [C,I]); both contracted
   instances (255/315 vars) are *hard* — Cadical burns a 2M-conflict
   budget without an answer, kissat was still running at session close
   with proof files in the hundreds of MB. The session's headline
   theorem (stabilizers are 2-groups) is stated conditionally on those
   two runs in the NOTE, and `data/ord5_status.md` carries the final
   word.
7. **Endgame (written after the fact; §6 above is as-lived).** Color-
   precedence breaking (a two-line WLOG lemma over the S₅ color action)
   collapsed both order-5 instances: [C,C] UNSAT in ~40 min (kissat;
   812 MB DRAT, drat-trim-verified in 36 min), [C,I] UNSAT in 5.5 s
   (Glucose42; pure DRUP verified by the repo's own rup_check) and
   independently in ~7 min (kissat + drat-trim). The unbroken [C,I]
   instance then landed UNSAT directly (~90 min, 6.7 GB proof, hash
   recorded), removing the color lemma for that leg. Theorem 1 went
   from conditional to fully machine-verified within the session.
8. **The contrast.** The same order-5 question at n = 7 is SAT: an
   explicit order-5-invariant 5-coloring of PG(6,2) (verified proper +
   invariant), with ≥ 10⁵ raw invariant siblings. And it does not
   extend to n = 8 either. So the n = 8 wall is not "5-fold symmetry is
   impossible in this family" — it is something that happens strictly
   between n = 7 and n = 8.

## What failed, and the wounds

- The Σα < 128 local-obstruction conjecture: refuted by the session's
  own data (capacity ≈ 265–274). The best kind of failure — cheap and
  informative.
- Exact per-class independence numbers via SAT + totalizer: too slow at
  the threshold; replaced by exact-spectrum Hoffman bounds (certified
  upper bounds, no SAT needed).
- Python `signal.alarm` cannot interrupt a C solver call: the first
  ansatz sweep hung on a weakly-contracted cell. Re-architected with
  per-call conflict budgets. (Defect class: *timeouts must live below
  the FFI boundary.*)
- `pkill -f` with a pattern contained in the invoking shell's own
  command line kills your own session. Kill by PID.
- Block-diagonal ansatz families were generated without noticing that
  transitive block action is automatically dead — 20 of 24 cells wasted
  on a structural triviality that ten seconds of thought would have
  predicted. Correct version of the idea: only *splitting* actions
  (order 5 on F₁₆-blocks) are informative — and those are exactly the
  hard pending instances.
- Two kissat + two local-search engines + a sampling run on 4 cores:
  oversubscription slowed the decisive runs mid-session before triage.
- Glucose42 with in-memory proof logging on the [C,C] instance died
  silently (likely memory) — the drat-trim-verified kissat proof stands
  for that leg; a repo-native DRUP for [C,C] is an open nicety.
- The unbroken order-5 [C,C] run and the combined
  order-5-hyperplane-shadow instance outlasted the session (3.4 GB and
  5.9 GB of proof at termination) and are recorded as open threads.

## Cost ledger

4 cores / 15 GB sandbox. Controls + sweeps + sampling ≈ 40 core-minutes
total. Local search ≈ 6 core-hours across engines (seeds 777, 90001,
90002 recorded). The order-5 campaign: ~5 core-hours
across broken/unbroken instances and both verifications. Everything exact-arithmetic end to end; no floats
anywhere in the critical path (the only floating point in the session is
the Hoffman *reporting* — the bound itself is computed as an exact
fraction).
