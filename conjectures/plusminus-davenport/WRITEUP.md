# Session writeup — 2026-08-24

## How the problem was chosen

The scheduled mandate: pick an external open problem, anywhere in
mathematics, where a few CPU cores and several hours can actually break the
bottleneck. The sandbox had web search but no page fetches (every primary
source egress-blocked), so candidate vetting ran entirely on search snippets.

Slate (details in the daily log): (C1) the undetermined plus–minus weighted
Davenport constant D±(C₅⊕C₁₅) — flagged as runner-up in the 2026-08-18
session's slate, re-vetted today; (C2) least critical exponent of balanced
sequences over odd alphabets d ≥ 11; (C3) the 5-color Rado number
R₅(x+3y=3z) > 296. C1 won on all three criteria: the bottleneck is a small
finite search; the openness trail is as clean as snippets allow (the 2014
paper states the gap itself, the 2017 survey still lists it, the active
2024–2026 school works arithmetic questions, not new values); and the result
completes a named table (Marchan–Ordaz–Schmid) that the same school still
builds on. The one sour note, found during vetting and kept prominently: a
2021 Kentucky thesis on exactly this constant that we could not read. If it
decides the cell, today is an independent confirmation. We searched seven
different ways for any statement of the value; none surfaced.

An honest observation recorded at selection time: for a cell this small, the
fact that it was open since 2013 means either nobody bothered to run the
search, or somebody did and we cannot see it. That risk was accepted
knowingly, and the session was designed so that most of its value (the
independent full table, the beyond-100 extension, the lemmas and structure)
survives even the worst case.

## What happened

**The headline fell in the first probe.** A 30-line sizing script answered
the question before the real engine existed: max ±-zsf set size 5, tree of
139 052 nodes, 4.6 s. D±(C₅⊕C₁₅) = 6. The rest of the session is what
separates a probe from a result: independent implementations, controls,
anchors, the stratified proof, and the table around it.

**Engine.** The set-based Python DFS was too slow for the control suite
(cyclic groups to C₆₅ blew past ten minutes); rewritten with numpy boolean
indicator vectors and precomputed permutation tables — exact boolean/integer
arithmetic, ~20× faster. Controls then passed in 6 s: the cyclic law
d±(C_n) = ⌊log₂ n⌋ across n = 2–48 and 63/64/65, the hand-checked
d±(C₃⊕C₃) = 2, the published anchor D±(C₉⊕C₃⊕C₃) = 6 (secondary) —
the convention match with the literature hangs on that anchor — forced
cells, isomorphism invariance in three presentations, and a negative
control.

**Certification.** Four implementations, no shared method: the numpy DFS
(A), a full combinations×sign-patterns sweep (B: 2 324 784 six-subsets, zero
±-zsf; 85 155 five-subsets, exactly matching A's census), a C bitset DFS (C)
reproducing A's node count to the digit, and a stratified enumerator (D)
that re-proves the theorem stratum by stratum. The A/C node-count identity
(139 052) and the A/B census identity (85 155) are the two strongest checks.

**The proof work.** Writing G = C₅⊕C₅⊕C₃ and stratifying a hypothetical
6-set by its kernel part: the (4,2) stratum dies by a one-line saturation
lemma (a maximum ±-zsf set reaches every nonzero element — obvious once
said; we first computed all 135 kernel extremal sets and only then noticed
their saturation needs no computation). The (3,3) stratum reduced to
"allowed sets of ±-zsf 3-sets are sum-free", which closed by hand after the
machine revealed the two-type classification (60 line-type, 120 generic;
both verified against a hand count). The (2,4) stratum resisted: 13
constraint values in an allowed set of ≥ 16, no counting obstruction, no
clean structure found today — it stays machine-certified, honestly. So the
theorem is CERTIFIED with a two-fifths hand proof, not PROVED; the label
discipline stands.

**The table.** All 184 abelian types of order ≤ 100 from scratch
(~12 core-minutes): 167 cells forced by the elementary bounds, 17 decided by
search. The surprise worth the session by itself: **twelve of the seventeen
attain the pigeonhole bound**, refuting the naive additivity guess
d±(A⊕B) = d±(A)+d±(B) all over the table (first failure at order 18:
d±(C₃⊕C₆) = 4 > 1+2). C₅⊕C₁₅'s lower-bound behavior is the *exception* —
which retroactively explains why the 2014 authors could not settle it with
bound machinery: its neighbors genuinely go the other way. Beyond 100:
complete types 101–135, plus C-engine cells to order 243. New landscape
facts: the C₇⊕C₇ₙ and C₃⊕C₃ₙ families keep hitting the pigeonhole bound
(D±(C₇⊕C₂₁) = 8 at n = 3, the case the 2014 snippet calls unknown);
C₅⊕C₃₀ — the n = 6 sibling of the headline — is *also* pigeonhole-tight,
isolating C₅⊕C₁₅ further; and C₃⊕C₃⊕C₁₅ (order 135) is the first cell
strictly between both bounds, explained by a better direct-sum split. That
observation crystallized into Conjecture A (split-or-pigeonhole), which
holds at every cell computed today.

**A conjecture lived for one hour.** From the ≤ 100 data (C₃⊕C₃ₙ tight at
every computed n ≥ 2) we formulated Conjecture B: the family is always
pigeonhole-tight. The order-101–135 sweep refuted it the same afternoon:
d±(C₃⊕C₄₅) = 6 < 7 at n = 15, double-engine certified, with the maximum
witness being exactly the concatenation {1}∪{1,2}∪{1,2,4} across
C₃⊕C₅⊕C₉. In hindsight the failure mode is visible: tightness at
n = 3m rides on splits like C₉⊕C₃ₘ reaching the bound, and at n = 15 the
cofactor arithmetic (⌊log₂15⌋ = 3, just below the 2⁴ boundary) leaves every
split one short. We kept the dead conjecture in NOTE §8 on purpose: it is
the sharpest small example this repository has produced of why a family law
fitted to a dozen cells is evidence, not truth — and it turned into support
for Conjecture A, which permitted both outcomes and matched the realized
one.

## Predictions registered before the late runs finished

Lemma C applied with the *computed* table (rather than invariant factors)
forces several cells that were still in the search queue when this paragraph
was written (13:10 UTC), because a best split meets the pigeonhole bound:
d±(C₁₅⊕C₁₅) = 7 via (C₃⊕C₁₅)⊕C₅ = 5+2; d±(C₃⊕C₆₃) = 7 via C₉⊕C₂₁ = 3+4;
d±(C₇⊕C₂₈) = 7 via C₄⊕(C₇⊕C₇) = 2+5; d±(C₁₄⊕C₁₄) = 7 via
(C₇⊕C₇)⊕(C₂⊕C₂) = 5+2; d±(C₃⊕C₃⊕C₂₇) = 7 via C₃⊕(C₃⊕C₂₇) = 1+6. The
searches, therefore, are confirmations for these five; the genuinely open
searches in the queue are C₃⊕C₅₇ (Conjecture B predicts 7), C₃⊕C₃⊕C₂₁, and
C₉⊕C₃⊕C₃⊕C₃. If any of the five forced cells comes back different, a lemma
or an engine is wrong and the session fails loudly.

## What failed

- The first engine design (Python sets) died on the control suite; rewritten.
- A shell-level timeout silently killed the first C₁₃⊕C₁₃ run mid-search
  (only detected because the batch log ended without its line); re-run
  sharded 4-way after validating the shard bookkeeping on the headline cell
  (shard node counts must sum to the unsharded count plus k−1 root
  recounts — they do, exactly).
- No hand proof for strata (2,4), (1,5), (0,6) — attempted counting and
  quotient arguments both fall short; the constraint systems are too loose
  for pigeonhole and too rich for the sum-free trick.
- The 135-extremal-set computation for C₅⊕C₅ was superseded by a one-line
  lemma minutes after it ran — kept in the writeup as a small lesson in
  looking for the trivial reason first.
- Two candidate slate problems (balanced sequences, R₅(x+3y=3z)) were left
  unattacked; both remain live and are recorded in the log with their
  vetting trails.

## Where this goes

OEIS: the sequence n ↦ D±(C_n) is ⌊log₂ n⌋+1 (surely present); but
n ↦ max{D±(G) : |G| = n} and the table of noncyclic values may be
submission-worthy once primary sources are checked. A short note (4–6 pages)
around Theorem 1 + the table + Conjecture A is the natural writeup once the
(secondary) flags are resolved against the actual papers — the note's
audience is exactly the school that left the cell open. Before any of that:
read Marchan–Ordaz–Schmid 2014 and the Perez-Lavin thesis from a connected
machine.
