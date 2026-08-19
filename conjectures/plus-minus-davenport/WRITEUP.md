# Session writeup — 2026-08-19 (session 1)

The narrative, including what failed. Companion to `NOTE.md` (results) and
`log/2026-08-19-plus-minus-davenport.md` (selection record).

## How the problem was found

The session mandate: pick an external open problem, vet it, attack it. Three
subagent scouts ran in parallel (~30 searches each; WebFetch fully
egress-blocked, so snippets only): one on the Erdős problems database, one
on recent arXiv conjectures, one dedicated to vetting the plus-minus
Davenport candidate that surfaced early. The full slates are in the daily
log. The decisive vetting evidence (all secondary, snippet-level):

- Two independent snippet digests of the Marchan–Ordaz–Schmid 2014 PDF
  (arXiv:1308.3316 / HAL hal-00835688), one reading "The only group of
  cardinality at most 100 where the value of the plus-minus weighted
  Davenport constant remains unknown is C5 ⊕ C15, where it is either 6
  or 7."
- The Perez-Lavin 2021 thesis abstract describing the state of the art as
  "primarily known when the rank of G is at most two and the cardinality of
  G is less than or equal to 100" — i.e. seven years later the ≤ 100
  exception apparently still stood.
- ~15 later papers (2014–2026) checked by the vetting agent; none shows
  these values computed. The agent's 66 queries are listed in its report;
  the load-bearing ones are reproduced in the log.

An early surprise shaped the session: the prototype decided C5⊕C15 in
**1.5 seconds of Python** — before selection was even final. The natural
inference "if it takes 1.5 s, it cannot be open" turned out to be wrong;
the vetting held up. The honest reading is that the plus-minus community
proves theorems and did not, apparently, point a computer at the one
leftover cell. That shallowness is why this note leans so hard on
verification redundancy and structure, not on compute.

## What was built

Engine E1 (C, DFS over sign-representative multisets with the signed-sum
set as state), E2 (independent Python reimplementation, exact node-count
agreement required), E3 (from-definition brute force, tiny groups), E4
(plain combinations + 3^l sign checks, no DFS), E5 (the Lemma R
class-injectivity reduction over F_p², a mathematically different route),
a from-definition witness verifier, a randomized witness hunter with
positive/negative controls, a 339-cell sweep driver, and the table
consolidator computing best-decomposition floors exactly. Validation
chain before any open cell was trusted:

1. E1 = E2 node-for-node on every shared cell (139,052 at C5⊕C15;
   16,528,742 at C7⊕C21; full ≤ 100 log in `data/cross_check.log`).
2. E3 agreement on 12 tiny groups; 15 cyclic groups vs the ⌊log₂ n⌋ + 1
   formula (proved independently as NOTE Lemma 4).
3. Literature controls: C2⊕C4 = 4, C3⊕C3 = 3, C3⊕C9 = 5, and the
   below-cap C3⊕C3⊕C9 = 6 — the one nontrivial published rank-3 value the
   vetting surfaced — reproduced exactly.
4. The 2^l sign-orbit identity between reduced and unreduced censuses,
   classwise, at both headline groups.
5. E4's census agreement (85,155 maximum sets at 75) and its two zero
   counts at size 6 (2.3M and 185.3M combinations).
6. E5's seven-way infeasibility, arriving through different mathematics.

## What failed, and what the failures taught

- **The naive dichotomy conjecture died in-session.** After the first ~150
  cells all landed at floor-or-cap, "dim± ∈ {floor, cap} always" looked
  like the theorem of the day. C3⊕C3⊕C15 (order 135) landed at 6, strictly
  inside its {5, 7} window, killing the general statement within the hour
  and demoting the observation to a rank-2 phenomenon (empirical, NOTE
  Q2). Lesson as old as the repo: conjectures born from a table die by the
  table's next row.
- **The hand-proof timebox for "no dissociated 6-set in 75" failed
  productively.** Two counting attacks (fiber counting over the Z5²
  projection; the ν: x ↦ σ−x involution structure on the 22-element
  class-0 value set) both end with "22 ≤ 25, no contradiction" — and the
  Lemma R reduction then *explains* the failure: the three class sizes
  22/21/21 fit inside F₅² with room to spare, so no cardinality argument
  can work. What survives is the reduction itself (now the sixth
  verification engine, and the sharpest open thread: a human-checkable
  F₅² statement).
- **Aut(G)-orbit reduction was designed and then discarded.** A
  first-element orbit reduction is sound (the orbit-block argument was
  worked out in full), but it complicates the exhaustiveness argument that
  certificates rest on, for a ~3× saving that mattered nowhere. The
  committed engines use only the sign-flip reduction (Lemma 1) — and run
  it both on and off, with the classwise 2^l identity binding the two.
- **Process hygiene, again — three distinct self-inflicted failures.**
  (i) A `pgrep -f`/`kill` pattern matched the invoking shell's own command
  line and killed the session's shell mid-command — the *exact* failure
  class recorded in the 2026-08-13 and 2026-08-17 logs (exit 144, twice,
  before switching to literal-PID kills). (ii) A background verification
  run silently produced nothing: launched without `cd`, its relative
  `certs/` redirect failed in the wrong directory and the wrapper swallowed
  the error. (iii) Worst: a priority-cell driver was launched three times
  without its `cd` line while the *diagnosis* ("cwd wrong, so it did
  nothing") was itself wrong — the tool's cwd persistence meant the
  "dead" drivers were all alive, and five copies of the same 225-element
  search ended up racing on one tmp file (a real, if unrealized,
  corruption risk — caught because `ps` showed five identical workers).
  Recovery: kill by PID chain (worker → timeout wrapper → parent loop),
  purge all partial tmp files, and relaunch exactly one driver from a
  script file with an absolute `cd` baked in. The repo lesson, now
  three sessions old and counting: background compute belongs in
  committed script files with absolute paths, never in ad-hoc shell
  one-liners; and process kills go by numeric PID only.
- **Redundant compute was left running and had to be culled.** The
  scratchpad-era sweep kept burning cores after the committed sweep
  superseded it; on a 4-core box that halved throughput for ~15 minutes.
  Sequencing error, not correctness error: the committed sweep re-runs
  every cell with the committed binary regardless.
- **The C23⊕C23 stretch target has not fallen** (yet): the randomized
  hunter, which finds a maximum 7-set at order 147 in 366 restarts, has
  spent its first half-hour at order 529 / target 9 without a hit. A
  failed hunt proves nothing (stated explicitly in the tool and NOTE);
  either a longer hunt or a real exhaustive campaign (≈ 10¹¹–10¹² nodes)
  is future work, and the "23, 46, 47" snippet that motivates it is
  itself unverified in context.

## Judgment calls a referee should know about

- **Labels.** Theorem 1's upper bound is CERTIFIED (finite exhaustive
  computations, however redundant), not PROVED; the six-way agreement is
  defense in depth, not a proof. Theorem 2's upper bound IS proved
  (Lemma 2 is a two-line argument); its lower bound is a finite witness
  check (3⁷ − 1 sign patterns) — kept CERTIFIED since a human would not
  realistically verify 2,186 cases unaided.
- **The thesis caveat is load-bearing.** Perez-Lavin's thesis computed
  values in 100 < |G| ≤ 200 "with some exceptions" (snippet). C7⊕C21
  (order 147) may be among them. Theorem 2 and every table row in
  (100, 200] is phrased with that risk explicit. C5⊕C15 (Theorem 1) is
  not subject to this caveat — it is below 100, where the thesis itself
  restates the exception.
- **Everything literature-related is (secondary).** No primary source was
  readable from this sandbox. The NOTE says so at the top; nothing should
  leave this repository before arXiv:1308.3316, the thesis PDF, and the
  Adhikari survey are read from a machine with real egress. That includes
  confirming the *definition* conventions (sequences vs sets is harmless
  here by NOTE Lemma 0, but the literature's exact statement of the
  ≤ 100 determination and of the C_n⊕C_n coverage must be quoted, not
  paraphrased from snippets).

## Session arc (compressed timeline)

Connectivity check (all four primary sites blocked; WebSearch alive) →
three scouts launched in parallel → prototype written *during* the wait as
a feasibility probe; C5⊕C15 = 6 landed in 1.5 s → controls (cyclic ladder,
8 brute-forced groups) → C engine, node-for-node agreement → C7⊕C21 = 8
(35 s Python, 2 s C) → vetting report landed: 75 confirmed as the named
unique ≤ 100 unknown → slate written, selection argued, first push →
sweep of 339 cells (3 workers) → dichotomy conjecture formed and killed
(order 135) → hand-proof timebox → Lemma R + E5 → verification matrix
completed (2^l identities, E4 double zero, E5 seven-way infeasible) →
documents, table consolidation, cross-check log, PAGE handoff.
