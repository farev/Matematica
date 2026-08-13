# Session writeup — 2026-08-13 (session 1)

The narrative, including what failed. Companion to
[`NOTE.md`](NOTE.md) (results) and the daily log (selection process).

## How the target was chosen

The sandbox turned out to have **zero access to primary literature** —
arxiv.org, oeis.org, erdosproblems.com, mathoverflow, Wikipedia, even the
EJC dynamic survey all EGRESS_BLOCKED; only web-search snippets worked.
That constraint shaped the slate: the chosen problem had to be one whose
statement is definitional (no methodology to reconstruct from papers),
whose openness is attested by snippet-quotable ledgers (OEIS), and whose
attack is pure computation. `a(10)` of A276661 fits exactly: the last
exact value of `f` dates to Grossman's `a(9)`, the Feb-2025 arXiv
preprint 2502.19182 still quotes nine known values, and OEIS carried only
`a(10) > 220`.

Two slate alternatives — the next open queens-domination value (an active
SAT group owns that frontier, arXiv 2508.11945) and a weak-Schur WS(6)
record (specialist tabu searchers own those) — scored worse on "can this
box actually break the bottleneck today".

## What was built

Chronologically:

1. **v1/v2 engine** (`dss_search.c`): descending branch-and-bound,
   bitset-of-sums state, exact prunes P1–P4, OpenMP over depth-3 prefixes.
   First calibration shock: `n = 9, m = 155` = 7.7×10⁸ nodes / 146 s on
   4 threads. Extrapolation put the full `n = 10` sweep at CPU-weeks.
2. **Python reference** (`dss_reference.py`), **brute validator with
   controls** (`validate_set.py`), **ladder driver** (`ladder.py`).
   First real bug of the day: comparing node counts between C and Python
   on an exists-mode FOUND run — counts are only well-defined on full
   traversals. The cross-check was restricted to NONE rows + enum reruns.
3. **v3 engine** (`dss_search3.c`): state = difference set `D` of the
   achievable sums plus its bit-reversal `R`, updated by shifted ORs;
   candidate tests become O(1) bit lookups. 4.1× faster than v2 at
   identical node counts (verified to the node at `n = 9`,
   `m ∈ {150, 155}`).
4. **Tight mode**: exact per-candidate caps over the true candidate pool
   `V = [1, c−1] \ D` via a once-per-node descending array with prefix
   sums/squares. Another ~15% node cut and ~10% time cut at `n = 9`.
   **A soundness bug was caught here before it ran**: the first version
   truncated `V` at `f(r)`, but only the *largest* remaining element must
   clear `f(r)` — smaller remaining elements may legitimately lie below
   it. Demanding `r` valid candidates above the floor would have
   over-pruned. The shipped version scans `[1, c−1]` and was verified
   against the exact engines on the full 42-case battery (statuses and
   solution lists identical, node counts never larger).
5. **`a(10)` probes**: `m = 230` (1.1×10⁸ nodes, 16 s), `m = 250`
   (4.5×10⁹, 566 s). Growth ×1.203 per unit `m` ⇒ full decision ≈
   CPU-months on this box. **Mid-session checkpoint invoked**: goal
   re-scoped from "decide `a(10)`" to "push the certified frontier as far
   as the session reaches, build the machinery, and leave a resumable
   campaign" — with the witness side probed separately.
6. **Witness side, two attempts.**
   - *Simulated annealing*: failed its own positive control — with the
     cap at 309, where the Conway–Guy set exists, energy stalls at 3–5
     over dozens of restarts (uniform and local ±δ moves). Near-optimal
     DSS sets look isolated in the move graph. Kept in the tree as a
     documented dead end; no evidence claimed from it.
   - *CG-neighborhood exhaustion*: every set `{m − d_i}` with deficiency
     profile within L1-distance 8 of Conway–Guy's, for every `m ≤ 308` —
     19.1M sets, zero DSS. This is the certified replacement for the
     annealer's missing evidence: **if `f(10) < 309`, the witness is not
     a small perturbation of the Conway–Guy structure.**
7. **The ladder** (v2 uniform, full sweeps `n = 2..9` + enum at each
   `f(n)`): re-derives every known value from scratch, cross-checked
   against Python (`n ≤ 7` exhaustively) and OEIS, all optimal sets
   enumerated. An earlier partial ladder run was **discarded and redone**
   because the engine binary had been recompiled mid-run — a
   mixed-binary certificate is no certificate.

## What failed, and why

- **Annealing for a witness** — failed positive control (above). Reason:
  the DSS property is a conjunction of ~3^10 exact integer non-equalities;
  single-element moves almost always break several while fixing one.
- **Fourth-moment prune** — derived on paper (distinct same-parity values
  force `E[X⁴] ≥ ~N⁴/5`, giving an *upper* bound on `Σ a_i⁴` from
  `3(Σa²)² − 2Σa⁴`); shelved after estimating it binds only where P3
  already kills the branch. Not implemented, so not claimed sound.
- **Multi-`m` deficiency engine** — the clean idea of the day (equal-
  cardinality collisions are `m`-independent; unequal-cardinality
  collisions each exclude a single `m`), projected ~5–10×, but the
  k-graded difference bookkeeping was too much implementation risk for a
  session whose certificate story was already three-engines-deep. Written
  up as the named next step instead (NOTE §6.2).
- **The full `a(10)` decision** — out of reach by ~3 orders of magnitude
  of CPU on this box with this engine. The session's honest product is
  the certified prefix + machinery, not the value.

## Session hygiene notes

- One engine recompile invalidated a running certificate sweep (redone).
- One self-matching `pkill` pattern killed the session's own shell
  (recovered; lesson: kill by PID).
- The compiled binaries were briefly committed against repo convention,
  then untracked in a follow-up commit.

## Where the next session picks up

`python3 sweep10.py` resumes the frontier from `data/n10_sweep.csv`
exactly where this session stopped; every completed `m` is permanent.
The multi-`m` engine sketch is the algorithmic lever if grinding is to be
replaced by thought.
