# 2026-08-13 — distinct-subset-sums

**Target.** Decide `a(10)` of OEIS A276661: the least possible largest element
`f(10)` of a 10-element set of positive integers all of whose 2^10 subset sums
are distinct. This is the data frontier of Erdős's distinct subset sums
problem — erdosproblems.com #1, the problem Erdős called "perhaps my first
serious problem" ($500). Exact values are known only for n ≤ 9:
f(1..9) = 1, 2, 4, 7, 13, 24, 44, 84, 161 (Lunnon 1988 exhaustively for
n ≤ 8; J. P. Grossman for n = 9). f(10) is open: the Conway–Guy set gives
f(10) ≤ 309, conjectured sharp; the OEIS records only `a(10) > 220`.
Plan: exhaustive descending branch-and-bound over the largest element
m = 161..308, with exact integer prunes (sum bound, second-moment bound,
per-position minima from the re-derived ladder, incremental bitset collision
detection). Every completed m is a certified `f(10) > m`; completing the sweep
plus a local validation of the Conway–Guy 10-set certifies `f(10) = 309`.
A found set below 309 would refute Conway–Guy optimality at n = 10 — either
outcome is a result.

## Connectivity check

- **WebFetch: fully blocked.** arxiv.org, oeis.org, erdosproblems.com,
  mathoverflow.net all return EGRESS_BLOCKED from the sandbox proxy; so do
  en.wikipedia.org, combinatorics.org, api.semanticscholar.org. No primary
  page was readable from this session.
- **WebSearch: working.** Search snippets can quote the blocked sites, which is
  how every literature claim below was obtained. Accordingly **every citation
  in this session is (secondary)** — search-snippet evidence retrieved
  2026-08-13, primary sources unread. Claims of openness are as strong as
  today's snippets of OEIS A276661 and erdosproblems.com/1, no stronger.
- Package registries (PyPI) are reachable if needed.

## Candidate slate (external)

**C1 — f(10), Erdős distinct subset sums (additive number theory).**
Statement: determine the least possible maximum element of an n-element set of
positive integers with pairwise distinct subset sums, at n = 10.
Sources checked 2026-08-13 (all secondary, via snippets): oeis.org/A276661
("only the first nine numbers of this sequence are known", terms
1,2,4,7,13,24,44,84,161; "Lunnon found a(0)–a(8) and J. P. Grossman found
a(9)"; Grossman's optimal 9-set {77,117,137,148,154,157,159,160,161};
a comment recording a(10) > 220); erdosproblems.com/1 (history: Conway–Guy
N ≤ 2^{n-2}, Bohman N ≤ 0.22002·2^n upper bounds; Erdős–Moser second-moment
lower bound, √(2/π) constant due to unpublished Elkies–Gleason); arXiv
2502.19182 (Feb 2025) still quotes "only the first nine numbers are known".
Why open: OEIS is the ledger this exact value would land in, and it does not
have it; the Feb 2025 preprint corroborates.

**C2 — next open queens-domination value γ(Q_n) (graph theory / SAT).**
Statement: minimum number of queens dominating the n×n board, first
undetermined n. Sources: arXiv 2508.11945 "Queen Domination by SAT Solving"
(Rostami–Bright, Aug 2025, DRAT certificates); emergentmind topic page:
UNIDOM determined γ(Q_n) for all n ≤ 25; OEIS A075458. Why open beyond 25:
each increment roughly squares SAT cost; 26 is presumed open.
Why not chosen: the frontier is actively held by a dedicated SAT group with
far more compute; a one-session outsider attempt at n = 26 UNSAT is
low-probability, and their open-case list was not readable to confirm the
exact target.

**C3 — weak Schur number WS(6) lower bound (Ramsey-type partition
combinatorics).** Statement: improve the best weakly-sum-free 6-partition
record. Sources: Rowley, INTEGERS 21 (2021) #A59 "New lower bounds for weak
Schur partitions"; snippets record WS(6) ≥ 582 (2017-era) after ≥ 575
(Eliahou et al. 2012), WS(7) ≥ 2146, WS(8) ≥ 6976. Why open: exact WS(k) is
unknown for k ≥ 5; records move by construction. Why not chosen: beating
template/tabu specialists with session compute is a coin flip; the repo
worked the adjacent Schur/Rado family on 08-07 and 08-08, and the current
record could not be pinned down precisely through snippets.

Subfields spanned: additive number theory, graph domination/SAT, Ramsey-type
partition combinatorics.

## Internal-thread assessment

Audited the last five logs and all conjecture READMEs (subagent sweep).
Rotation rule: last two sessions were reciprocal-rado (08-08) and
signed-difference-sets (08-09) — no conjecture is at two consecutive, nothing
is blocked today. Top three live threads:

1. **generalized-schur** — open the (4,4,u) ladder (S(3;4,4,10) ?= 109…),
   named in the 08-07 log. Row-changing if done, but blocked on tooling: the
   DRUP pipeline OOM-killed at 15 GB three times because pysat buffers proofs
   in RAM, and no kissat/cadical binary is installable (source egress
   blocked). Fixing the toolchain inside the sandbox is possible but eats the
   session.
2. **signed-difference-sets** — the (32,20,4) family across all seven groups
   of order 32; README itself prices it at ~2 CPU-weeks or a day of new
   canonicalization code. Not a one-session win on this box.
3. **circular-thresholds** — n = 8 via a synchronization variant of Theorem
   MC; idea-bound, CPU alone buys nothing.

None clearly beats the slate. Default-external applies.

## Selection

Chose **C1** on the mandate's criteria:
(a) the bottleneck is a finite search — descending branch-and-bound with exact
integer prunes, embarrassingly parallel over prefixes, on a problem whose last
exact value (n = 9) was computed on hardware decades weaker than this box;
(b) "already done?" is answerable: this value's ledger is OEIS A276661, which
does not have it, and a Feb 2025 preprint still calls nine values the known
state; (c) the result extends the exact-values line (Lunnon 1988 → Grossman's
a(9)) that the active Costa–Dalai–Della Fiore papers (DAM 2023, DAM 2025) and
Steinerberger (IJNT 2023) cite as context, and it lands directly in OEIS
A276661/A005318 and on erdosproblems.com/1's data notes.
What counts as achieving it: a certified value of f(10) — either 309 with an
exhaustive-emptiness certificate for m ≤ 308, or a witness set beating
Conway–Guy. Graceful degradation: certified `f(10) > m` for the largest m the
session clears, which supersedes the recorded 220.

Mid-session checkpoint: if by mid-session the calibration (full re-derivation
of the n ≤ 9 ladder) says the n = 10 tree is out of reach, pivot to the
largest certified partial sweep plus the ladder re-derivation, and say so.

## Result

**CERTIFIED.** `f(10) > 262` — no 10-element distinct-subset-sums set has
largest element `≤ 262` (the recorded floor was 220; Conway–Guy gives
`f(10) ≤ 309`, re-validated locally). Every cleared maximum `m` is an
independent certified row in `conjectures/distinct-subset-sums/data/n10_sweep.csv`
with exact node counts; the sweep is resume-safe and continues in future
sessions. Also **CERTIFIED**: from-scratch re-derivation of
`f(1..9) = 1, 2, 4, 7, 13, 24, 44, 84, 161` (agreeing with A276661 at every
level, all optimal sets enumerated — the ladder assumed no OEIS value), and
the exclusion of every witness below 309 whose deficiency profile lies
within L1-distance 8 of the Conway–Guy profile (19,125,539 sets checked).
**PROVED (classical method)**: exact finite second-moment floors
`f(10) ≥ 192` and `f(11) ≥ 362`. **NUMERICAL**: search-tree growth
~×1.203 per unit of the maximum (fit on m ∈ [230, 250] only).

Verification architecture: four implementations of the identical search
tree (three C engines + a Python reference) with exact node-count equality
checked on full traversals (exhaustively for n ≤ 7, on a 42-case battery
for n ≤ 8, and at n = 9 for m ∈ {150, 155}: 429,697,049 and 769,328,147
nodes, identical per-depth profiles); a zero-cleverness brute validator
with positive and negative controls; every reported solution re-validated
independently; OEIS values used as assertions, not inputs.

## What failed

- **Simulated annealing for a sub-309 witness** failed its own positive
  control: with the cap at 309, where the Conway–Guy set exists, energy
  stalls at 3–5 across restarts (uniform and local moves). No heuristic
  evidence claimed; replaced by the certified CG-neighborhood exhaustion.
- **A fourth-moment prune** was derived but shelved: it binds only where
  the second-moment prune already kills the branch.
- **The full a(10) decision** is out of reach on this box with this
  engine: ~×40 tree growth per +20 of m prices the remaining range at
  CPU-months. Mid-session checkpoint re-scoped the target to the certified
  frontier + machinery + resumable campaign.
- **A soundness bug in the tight prune was caught before deployment**
  (truncating the candidate pool at f(r) would have over-pruned; only the
  largest remaining element must clear f(r)).
- **Session hygiene**: one certificate run invalidated by recompiling the
  engine binary mid-run (discarded, redone); one self-matching pkill
  killed the session's own shell; binaries briefly committed, untracked in
  a follow-up.

## Next

Resume `sweep10.py` (every completed m is permanent). The algorithmic
lever worth a session by itself: the multi-m deficiency-vector engine
(NOTE §6.2) — equal-cardinality collisions are m-independent, so one tree
over deficiency profiles with per-node alive-m intervals replaces ~150
per-m trees (projected 5–10×). After a(10): f(11) ∈ [362, 594] with the
same machinery.
