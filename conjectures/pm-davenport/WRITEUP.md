# Session writeup — 2026-08-25 (session 1)

The honest narrative, including what failed. Companion to NOTE.md (the
paper-shaped artifact) and the daily log entry
`log/2026-08-25-pm-davenport.md` (slate, selection argument).

## How the problem was chosen

The scheduled-session mandate: survey three external candidates spanning
two subfields, assess the repo's internal threads, pick with a bias to
the new. WebFetch was egress-blocked all session (arxiv.org, oeis.org,
erdosproblems.com, mathoverflow.net all EGRESS_BLOCKED); WebSearch
snippets were the only literature channel, so three vetting subagents ran
~65 targeted searches. Slate:

1. **Plus–minus weighted Davenport constants** `D±(C₅⊕C₁₅)`,
   `D±(C₇⊕C₂₁)` — carried over as last session's unexamined runner-up;
   vetting found the strongest possible framing: `C₅⊕C₁₅` is the *single*
   group of order ≤ 100 left undetermined by Marchan–Ordaz–Schmid 2013
   ("either 6 or 7"), unresolved in any 2013–2026 snippet, with the
   original authors still active on the adjacent monoid theory
   (June 2025). **Chosen.**
2. **No-three-in-line, n = 47** — vetting killed it: solved by Prellberg
   in Sept 2025, frontier now n = 76 (Heule, Aug 2026), an active
   monthly arms race. Dropped; the vetting report is preserved in the
   log since the "known to n = 46" folklore is badly stale.
3. **ex(41; C₄) ∈ {132, 133}** — real and open (OEIS A006855), but the
   exhaustion side is orderly-generation engineering the session could
   not credibly finish, on a frontier owned by McKay and Alekseyev.
   Runner-up.

Internal threads (URT(22) 20k-wall, grimm 10¹³, vdw-mixed SAT campaign)
were assessed and none beat candidate 1 on
breakability-today × certifiability. Full scoring in the log.

## Timeline of the attack

1. **Bracket arithmetic first.** Before any code: for rank-2 invariant
   factors `d₁ | d₂`, the AGS bracket
   `⌊log₂d₁⌋+⌊log₂d₂⌋ ≤ μ(G) ≤ ⌊log₂ d₁d₂⌋` has width ≤ 1 (floors), so
   every rank-2 group is a *single decidable bit*, and `C₅⊕C₁₅` asks:
   does a dissociated 6-set exist in a 75-element group? `C(37,6) ≈
   2.3 M` class-rep subsets — trivially exhaustible. The session's risk
   was therefore never compute; it was correctness and novelty.
2. **Engine A** (Python, transparent set-DFS from the extension rule,
   Lemma 2) ran the controls (cyclic ≤ 64, `C₂^r`, `C₃^r`) and then
   decided the headline in 3.8 s: `μ(C₅⊕C₁₅) = 5`, refuting the
   pigeonhole value. Immediately after: `μ(C₇⊕C₂₁) = 7`, *attaining* it.
   The two open cases split in opposite directions — better than any
   single answer.
3. **Engine B** (C, same spec, independent implementation) reproduced
   both, including the exact extremal-census and node counts (85,155 /
   139,051 for the first group; 2,016 / 16,528,741 for the second, the
   latter also matched by Engine A in 973 s). One real bug was caught at
   review before B ever ran: the first draft's undo logic used
   membership *counters* and double-decremented; rewritten to
   membership flags + append-log, which is also simpler.
4. **Engine C** (C, deliberately dumb: every 6-subset × every ternary
   sign vector, no shared pruning) confirmed the refutation
   (2,324,784 subsets, 0 dissociated, 6.6 s) and — run at size 5 as a
   positive control — re-derived 85,155 from scratch.
5. **Census.** `sweep.py` enumerated every abelian group of order ≤ 192
   (invariant factors; each group also re-run in its prime-power
   presentation with `(μ, census, nodes)` asserted equal — an
   isomorphism-invariance check on the engines) plus targeted larger
   families. Deficient groups are rare and 3-heavy; full list in
   NOTE.md §3.
6. **Structure.** CRT-decomposing the `C₇⊕C₂₁` witnesses exposed the
   *checksum* mechanism (all `C₃`-coordinates nonzero: the `C₃` factor
   blocks every relation whose sign-weight ≢ 0 mod 3, freeing the `C₇²`
   parts to pack beyond dissociativity), which became proved Lemma 5 and
   explains the unique `C₃⊕C₆` extremal set the same way (`C₂`-checksum
   over `F₃²`). The census sizes 2,016 = |GL(2,7)| and 1,008 =
   |GL(2,7)|/2 motivated the orbit analysis (§4 of NOTE.md).

## What failed, in order of instructiveness

- **"Rank-2 never exceeds concatenation."** Formed after the `C₅⊕C₁₅`
  refutation; killed within the hour by `C₃⊕C₆` (attains, unique
  witness) and `C₇⊕C₂₁` itself. Attainment, not deficiency, is the norm.
- **A hand proof of the headline refutation.** The graded-counting
  refinement (Lemma 6) eliminates only profiles `k₁ ≤ 2`; profiles
  `{3,4,5,6}` survive counting by margins of 1–3 and die only
  computationally. The bit appears genuinely non-pigeonhole.
- **A uniform infinite-family construction** for gap-1 members of
  `C₅⊕C₅ₙ` (binary ladder + checksum extras): the natural counting
  argument over the extras fails (`3^s` sign patterns ≫ `M`), and
  sign-weights of `{0,±1}`-representations of multiples of `M` are not
  representation-invariant. Families stay conjectural (NOTE §6).
- **Engine C's first control was miswritten** (refutation asked at
  `t = μ` on `C₉`, which must — and did — find witnesses). The engine
  was right; the test was wrong; fixed and rerun. Recorded because
  silent test rewrites are how fake certainty starts.
- `/usr/bin/time` doesn't exist in the sandbox; the first heavy-batch
  invocation died before computing anything. Relaunched with plain
  date-stamping.
- CPU oversubscription (sweep + heavies + Python census + controls on 4
  cores) roughly doubled several wall-times. Runtimes in NOTE.md marked
  accordingly.

## Pre-registered predictions (written before the runs finished)

Recorded mid-session, before the corresponding computations returned,
so that hits and misses are both auditable:

1. **`C₅⊕C₃₀` (n = 6) and `C₅⊕C₆₀` (n = 12): ATTAINED** (μ = 7, 8).
   Reasoning: they sit at the same fractional log-position as the
   deficient `C₅⊕C₁₅` (150/128 = 300/256 = 75/64 = 1.172), but acquire a
   `C₂` factor usable as a parity checksum — precedent: `C₃⊕C₆ ≅
   C₂⊕C₃²` attains while `C₃²` is deficient.
2. **`C₃⊕C₉₀ ≅ C₂⊕C₃⊕C₉⊕C₅`: ATTAINED** (same repair pattern over the
   newly-found deficient `C₃⊕C₄₅ ≅ C₃⊕C₉⊕C₅`).
3. **`C₇⊕C₂₈ ≅ C₄⊕C₇²`: ATTAINED** (μ = 7; mod-4 checksum room over
   `C₇²`, whose `ν₃ = 7` already showed enough slack).
4. **`C₁₃²`: uncertain, leaning ATTAINED** (homocyclic precedents `C₅²`,
   `C₇²` attained their gap-1 brackets; but the packing ratio 169/128 is
   tighter than either).
5. **`C₇⊕C₄₉`, `C₇³`, `C₅²⊕C₁₅`: no prediction** — genuinely open
   feeling; `C₇³` has the first width-2 bracket in range ({6,7,8}).

**Outcomes** (updated as runs landed): #1 first half — `C₅⊕C₃₀`
**ATTAINED** (μ = 7, only 1,680 extremal sets), hit. #3 — `C₇⊕C₂₈`
**ATTAINED** (μ = 7, 10.8 M extremal), hit. #4 — `C₁₃²` **ATTAINED**
(μ = 7, 257,712 extremal), hit for the lean. Others pending at
writeup time; see NOTE §3.

A by-product observation worth keeping: among attained groups the
extremal census shrinks as the packing ratio `2^{t+1}/|G|` tightens —
`C₇⊕C₂₁` (ratio 1.74… i.e. `2⁸/147`) has a single orbit, `C₅⊕C₃₀` has
1,680 sets, while loosely packed attained groups have millions —
whereas the deficient groups all carry enormous extremal censuses
(85,155 up to 3.4 M). Rigidity concentrates exactly at the attainment
boundary.

## Verification discipline

Every claimed value is either (i) witness-carried (verified by the
independent direct enumerator), (ii) triple-engine-agreed exhaustion, or
(iii) forced by the proved bracket. Controls: cyclic formula (proved
here, so a true engine test), elementary 2-/3-group formulas, the three
published MOS exceptional values, a sample of MOS non-exceptional values,
planted-relation rejection in the verifier, and cross-presentation
isomorphism invariance inside the sweep. Every literature statement is
(secondary) — snippets, 2026-08-25 — and NOTE.md §8 lists the mandatory
pre-publication primary-source checks.
