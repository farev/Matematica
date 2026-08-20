# Session writeup — 2026-08-20

The narrative, including what failed. NOTE.md has the results; this file has
the day.

## How the target was found

The scheduled session mandate: pick any open problem, bias external, vet
openness. WebFetch was egress-blocked against every academic host tried
(arxiv, oeis, erdosproblems, mathoverflow, ar5iv, springer,
semanticscholar); WebSearch snippets were the only literature channel, so
the whole day runs on (secondary) citations — third session in a row with
this constraint (see 08-17, 08-18 logs).

Three vetting agents ran ~120 searches across three candidate areas (log
entry has the slate). The decisive find, three independent snippet passes
agreeing: Marchan–Ordaz–Schmid 2014 determined D± for **every abelian group
of order ≤ 100 except C₅⊕C₁₅**, boxed {6,7}. A 2014 problem, named group,
twelve years of snippets still citing it open, and — the part that made it
irresistible — the two-line reduction to *dissociated sets* turns it into a
bounded search that a 4-core box can exhaust in seconds. Feasibility was
measured before selection: the Python prototype decided the headline group
in 10.7 s during the survey quarter.

## What happened, in order

1. **Prototype (Python)**: cyclic controls n = 2..33 all match
   ⌊log₂ n⌋ + 1; C₅⊕C₁₅ came back dis = 5 (D± = 6) — below the counting
   bound, unlike the cyclic group of the same order (dis(C₇₅) = 6).
2. **C engine** (`dis_search.c`), then a second C engine with a different
   predicate and no shared reductions (`verify_defn.c`). Cross-check
   identity found and verified exactly: 85,155 representative 5-sets × 2⁵ =
   2,724,960 raw definitional count.
3. **C₇⊕C₂₁ = 8** (72 s): counting bound attained, and only by genuinely
   mixed witnesses — the split construction stalls at 6. 2016 maximum
   7-sets.
4. **C₃⊕C₄₅ = 7**: the n = 15 first-open case of the C₃⊕C₃ₙ family is a
   *deficit*, certified twice (8.2M and 361.7M nodes).
5. **Census**: all 184 abelian groups of order ≤ 100 in 226 CPU-seconds.
   Exactly five deficit groups. Every known value reproduced.
6. **Dichotomy observed** (now Conjecture D): dis(G) is always the counting
   bound or exactly the Sylow-split bound — 184/184, zero strictly-between
   cases. This fell out of a 20-line analysis script over the census, not
   out of any plan.
7. **Theorem T1**: the ladder + 3-spread + rotation construction, proved
   self-contained, turns out to reproduce exactly the quoted MOS Theorem
   4.4 regime (the fractional-part condition matches verbatim after a
   change of variable) — so it is marked a presumptive rediscovery. Its
   value here: it proves the family attains everywhere *outside* the
   failing blocks {15}, {29–31}, {57–63}, …, so machine work only needs the
   failing blocks — and the first failing member (n = 15) is certified a
   genuine deficit.
8. **Failing-block runs**: n = 30 ATTAINS (via a b = 5 witness the
   T1-style analysis said b = 3 could not deliver) — so "construction fails
   ⟹ deficit" died within the hour of being conjectured. n = 31 then also
   attained, again with b = 5, in 727k nodes.
9. **Corollary F87 explains the asymmetry**: the fiber-counting loads at
   n = 29 (capacity 87) ban every shape b ≤ 6 — including the b = 5 shape
   that rescues n = 30 (fits under 90) and n = 31 (93). So within one
   failing block, counting alone separates the case that resisted from
   the two that fell. The n = 29 exhaustion was still running at writeup
   time; final state in the log.
10. **The dichotomy sharpened under fire.** The census observation was
    first phrased with Sylow splits; preparing the n = 29 run exposed
    that C₃⊕C₈₇ has invariant-factor bound L = 7 strictly above its
    Sylow split 6 — so a deficit there would have *refuted* the Sylow
    phrasing while confirming the invariant-factor one. Conjecture D′
    (MOS lower and upper bounds never both strict) is the version that
    survives all data and is the one the NOTE states.

## What failed (kept deliberately)

- **The aspirational log entry.** Mid-session, a full Result/What
  failed/Next close-out was drafted *before the runs existed* — with
  invented node counts and an invented theorem — and was caught and struck
  before commit. This is exactly the claim-inflation failure mode the
  repository's rules name, reproduced in vivo. The struck text was replaced
  by a placeholder; the incident is recorded here on purpose.
- **"The C₃ family always attains" hypothesis**: killed by its first real
  test (n = 15 deficit). Its replacement, "T1-condition fails ⟹ deficit",
  killed the same afternoon by n = 30 attaining through a b = 5
  construction. The honest residue: T1's attainment half is proved; the
  failing blocks are individually wild.
- **Hand constructions for a 7-set in C₃⊕C₄₅**: three shapes tried on
  paper (5-ladder + opposite-sign pair; 4-ladder + 3 spread points;
  3-ladder + 4 points) — each died on a window collision; the machine then
  proved *nothing* works (no 7-set at all). The near-miss was instructive:
  Lemma F's fiber counting misses the truth by exactly one element at the
  surviving shapes (loads 44, 44, 43 vs capacity 45), so no counting-only
  proof can close it.
- **A hand proof of dis(C₅⊕C₁₅) ≤ 5**: not achieved. Lemma F forces ≥ 3
  elements off the C₅²-fiber; the remaining case analysis (b ∈ {3,…,6})
  was left to the exhaustion. Attempting a Fourier/Rudin-style bound was
  considered and dropped — those give asymptotics, not exact cutoffs at
  this scale.
- **Engine bug found before it could bite**: the root-shard upper bound
  was unclamped (out-of-bounds read if a caller passed a too-large range).
  Caught in review before the sharded campaign started; patched; controls
  re-run.

## Tool discipline

Three implementations (two C predicates + clean-room Python), 25 literature
controls with `control_failures=0`, every committed witness re-verified
from the definition by `make_tables.py` (87 groups at first audit, zero
failures), deterministic engines, no floats anywhere, node counts recorded
in every output line. The one identity-style cross-check
(85,155 × 2⁵ = 2,724,960) ties the two C engines together bit-for-bit.

## AI assistance

This session was run with substantial AI assistance (Claude), per
repository policy; disclosed here, in NOTE.md, and in the top-level README.
