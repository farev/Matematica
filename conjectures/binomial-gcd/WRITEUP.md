# Session write-up — 2026-08-12 (session 1)

AI-assisted session (Claude). This is the narrative, including what failed;
the theorems and labelled results are in `NOTE.md`, the day's full context
(candidate slate, selection argument, connectivity) in
`log/2026-08-12-binomial-gcd.md`.

## Arc

The problem was selected from a three-candidate external slate as the one
whose feasibility was *measured* rather than estimated: before selection
was final, a 40-line brute force had already reproduced the small end of
what turned out to be the known census, in seconds. The plan was "first
recorded verification bound" — that died within the hour when the
scoop-guard scout surfaced a January 2026 Rust scan to $10^7$ posted on the
erdosproblems forum (`conglu1997/erdos_699_rust`). Rather than pivot, the
session re-aimed at what the scan left open: structure. That re-aim paid
off: the digit-criterion machinery (NOTE Props 1–6) made the families
$2^k$ and $3^m{+}1$ checkable at sizes no full sweep reaches ($2^{64}$,
$3^{48}$), and the very first family run found a **new tight triple at
$n = 2^{41} \approx 2.2\cdot10^{12}$** — 200,000× beyond the previous
largest — which a standalone verifier then confirmed, including uniqueness
of $j$ among $9.07\cdot10^7$ dominated candidates.

## Timeline (UTC)

- 11:42 session start; connectivity check (all four canonical literature
  sites egress-blocked; raw.githubusercontent.com and web search work).
- 11:50 three scout subagents launched (#699 vetting; graph/OEIS slate;
  words/geometry slate). Brute-force prototype written and run meanwhile:
  census matches what was later identified as the known list.
- 12:05 scout returns: prior art found ($10^7$ scan, 9 tight pairs,
  family scans $k \le 27$, $m \le 17$). "First bound" framing dead;
  re-aim at structure + extension.
- 11:55–12:03 C engine (danger-zone + CRT) written; exact concordance with
  the independent brute force at $n \le 3000$; reproduces the entire known
  census at $10^7$ in 30 s (the Rust scan took ~43.5 ms/row ≈ 120 core-h;
  different algorithm, so this is genuine independent confirmation).
- 12:10 family checker validated on all 9 known members + negative
  controls; **~12:33 the $2^{41}$ triple appears** in the $k \le 64$ run.
- 12:15–12:23 v1 deep sweep killed (too slow); v2 with the Prop-0
  level cut, validated; production sweep to $4\cdot10^9$ launched 12:23.
- 12:40 slate complete (knight domination $a(22)$; Fici–Saarela abelian
  squares). Selection formalized: #699 on measured feasibility + checked
  novelty; the mid-morning discovery made the argument easy. Full
  selection argument in the log.
- 12:50 standalone verifier passes on the new triple (factorizations
  re-proved, Kummer carries, uniqueness scan); 3^m side clean through
  $m \le 40$; extension to $m \le 48$ launched.
- 13:20 3^m extension done ($m = 43$, the next sufficiency-candidate:
  decided clean). Theorems 7–8 written with proofs; documents; audit and
  the deep-sweep close-out follow.

## What failed (kept per repo policy)

1. **The original target was already taken.** "First recorded verification
   bound for #699" was the selection-time framing; the 08-09 session's
   banked intelligence ("no recorded bound anywhere") was three days stale
   against a January 2026 forum post that only a targeted scout query
   found. Lesson: the scoop-guard is not optional even for problems vetted
   days ago; forum threads don't show up in arXiv sweeps.
2. **v1 engine was 6× too slow for the deep sweep**, and the first fix
   attacked the wrong bottleneck. Profiling assumption (admissible-list
   rebuild) was wrong; the real cost was candidate volume at level
   $i = 1$ — which is *mathematically vacuous* (Prop 0 settles it). The
   right fix was a theorem, not code: skip $i=1$ in production, keep it in
   validation as a control. 30.5 s → 15.4 s at $10^7$; the incremental
   best-two bookkeeping bought almost nothing.
3. **First 4·10⁹ launch projected 15 h** because a Python family job was
   pinning a core and early-segment timing was misread. Killed once,
   relaunched after measuring the true rate. Per-segment completion
   markers were added so that even an interrupted deep run yields a
   certifiable prefix — worth keeping as standard practice.
4. **The family checker died twice on dominated-set blowups** (first at
   $2^{40}$ with a materializing enumerator, then at $2^{44}$ with a cap).
   Fixed by a streaming enumerator with range pruning, then by
   catch-and-mark-UNKNOWN semantics. 28 levels remain honestly UNKNOWN
   rather than silently skipped; they are listed with their sizes in
   `data/family_unknown_levels.csv`.
5. **The i=1 "UNKNOWN" rows at $3^{37}{+}1$, $3^{39}{+}1$ are vacuous**
   (Prop 0) but the checker still reports them — cosmetic defect, kept
   as-is and documented, since deleting them by hand would break the
   log-equals-artifact discipline.

## Controls that carried weight

- The engine's i=1 levels are a *theorem assertion* (Prop 0): any hit there
  is an engine bug. Ran clean over $10^7$ n's in validation mode.
- Dual implementation: C engine (sieve factoring, CRT enumeration) vs
  Python brute (full prime divisibility matrix) — exact census equality at
  $n \le 3000$; vs the 2026 Rust scan (third codebase) — exact equality of
  the nine-pair census at $10^7$.
- Family checker positive controls: all 9 known members found, including
  both levels at $n=28$; negative controls at $2^6$ and $3^{17}{+}1$.
- The new triple's verifier shares no code with the discovery engine and
  uses carry-propagation instead of digit domination; factorizations are
  re-proved by multiplication + primality inside the transcript.
- Prime sieve π(x) checks; Sylvester–Schur emptiness assertion never fired.

## Where this should go next

The 19+9 UNKNOWN family levels are a compiled enumerator away. The
$i{=}2$-family infinitude question (NOTE §5 Q3) is the mathematically live
one: the semiprime pattern (A085724) plus measured non-decaying coincidence
densities make "the exceptional set is infinite" a serious possibility —
which would falsify the strengthening as formalized in
`formal-conjectures`. Both the erdosproblems forum thread and the
`erdos_699_rust` repository are natural places to report the $2^{41}$
triple once this repository's results are checked by a human.
