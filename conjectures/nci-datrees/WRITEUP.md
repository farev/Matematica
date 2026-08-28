# Session write-up — 2026-08-28 (session 1)

The unedited narrative, failures included. The polished statements live in
`NOTE.md`; the selection argument and candidate slate live in
`log/2026-08-28-nci-datrees.md`.

## How the target was found

The scheduled session's survey fanned out three scouts (Erdős database,
OEIS frontiers, recent arXiv) plus an internal-thread assessor. The arXiv
scout flagged that the Non-Cancelling-Intersections conjecture had been
refuted *the previous day* (arXiv:2608.27416), that the refutation was
non-constructive at ~10¹⁵ elements, and that its §9 explicitly invites
exhaustive search for the smallest counterexample. Nobody can have
published a bound on a question posed yesterday; the machinery needed
(poset streaming + an exact closure decision) matched the machine.

## What worked, in order

1. **Feasibility measurements before commitment.** `nauty-genposetg`
   streams ~2.5M posets/s/core here; the Python prototype decided all
   lattices with ≤ 12 elements in two minutes, with the *median* closure
   size at win a single-digit number of states. That settled the pivot
   question early (the pre-registered fallback, peaceable queens a(17),
   was never needed).
2. **The poset→lattice route.** Lattices with n elements = posets on n−2
   points whose bounded extension has all joins. Debian nauty ships
   `genposetg` (n ≤ 16, with work splitting). The filter's count matching
   OEIS A006966 at every size is a strong end-to-end anchor — it caught
   both of the session's pipeline bugs (below) within seconds.
3. **Early-win detection.** Deciding "target reachable" by closure is fast
   only if wins are found early. Two accelerations mattered: checking, on
   every state insertion, whether the target-complement is already present
   (the root of a winning tree is a disjoint union of two built states);
   and running a leaf-only closure before the full pair closure. In the
   final design the left-linear BFS (leaves as right operands only) runs
   first, and since a left-linear win is a win, the general machinery runs
   only on lattices that fail it. In range, none did — the full pair
   closure never executed in the production runs.
4. **The left-linear pivot.** Mid-session, reading the companion paper
   (arXiv:2608.19414) showed its §9 asks for a lower bound too, and its own
   certified counterexample size is 10^(10^2215). Tracking left-linear
   winnability separately cost one BFS per lattice and turned one certified
   bound into three headline consequences (general bound, left-linear
   bound, no small separation) — and would have surfaced an explicit
   separating lattice automatically had one existed in range.
5. **Controls.** Hand-computed M₃/N₅ Möbius values and trees; an
   artificial negative control exercising the "not winning" path; the
   published Figure 3.1 lattice reconstructed (poppler's layout mode made
   the figure text readable) and passed through both implementations, with
   µ matching the paper's stated values; OEIS anchors at every size; a
   full independent Python implementation agreeing at every decided size
   it could reach in reasonable time.

## What failed, and how it was caught

- **First n = 14 launch produced zero output in all eight parts.** Cause:
  `genposetg -m x 8` — the splitting option is a bare `m x y`, not a dash
  flag; the generator rejected it silently behind a redirected stderr.
  Caught immediately by the aggregation script's A000112/A006966 mismatch
  (0 ≠ 1.1·10⁹). Fix: bare syntax, verified on k = 8 (parts summing to
  16,999) before relaunch.
- **The census driver's single-part path emitted nothing for n ≤ 7.**
  Cause: `genposetg` refuses `m` splitting below 6 vertices ("Need at
  least 6 vertices for splitting"). Again caught by the count checks, never
  by eyeballing. Fix: run unsplit when PARTS = 1. (An intermediate attempt
  to patch the driver through a quoted heredoc broke on quoting and
  changed nothing — the counts caught that too, in the sense that the
  rerun still mismatched; the lesson stands: patch scripts with real
  editing tools, not string-replace one-liners.)
- **The witness verifier "failed" its first randomized test.** It asserted
  "input is not a lattice" on three random k = 9 posets — correctly:
  random posets are usually not lattices. Bad test design, not a bug; the
  test was rebuilt to sample from filtered lattices and from the recorded
  worst-case lines.
- **Environment friction (recorded for future sessions).** The sandbox has
  4 cores (not the 32 the scheduled prompt imagines), no numpy/SciPy until
  pip-installed, no SAT solver until installed (pysat's CaDiCaL bindings
  solve but do not expose proofs; Glucose42 does), no `kissat` package in
  Ubuntu 24.04, and `pdftotext` only after installing poppler-utils.
  None of this touched the final pipeline (which needs only gcc, nauty and
  Python), but an hour of the session went to discovering it.
- **Scope ceiling accepted.** n = 16 needs 1.34·10¹² posets (~40× n = 15)
  — days at this generator's rate. The honest ceiling today is n = 15.
  The right tool for n ≥ 16 is a canonical-construction-path generator of
  lattices directly (the literature's own route to A006966(19)); noted as
  the sharpest next step rather than attempted in this session's last
  hours.

## Judgement calls a referee should see

- The certificate for "all lattices ≤ N winning" is the reproducible
  pipeline + OEIS count anchors + dual implementation + mechanically
  verified sample trees — not a per-lattice witness archive (171.5M
  winning trees would be data without a reader). Anyone can re-run any
  slice and extract any witness with the committed tools.
- Corollary B (set-family form) chains through [1]'s §4 equivalences,
  which were checked at statement level, not re-proved. The label says so.
- The digraph6 edge-direction convention is load-bearing for *individual*
  lattices but not for the census (duality argument in NOTE §3); it was
  additionally pinned down empirically by the count anchors.
