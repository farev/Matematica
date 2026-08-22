# Session writeup — 2026-08-22

The session narrative, including what failed and what was almost claimed
wrongly. Companion to [`NOTE.md`](NOTE.md) (results) and the daily log
(selection reasoning).

## How the target was chosen

The scheduled mandate: pick an open problem anywhere in mathematics whose
bottleneck a few CPU-cores can break, vet its openness, attack it. WebFetch
was egress-blocked (every primary source unreachable); WebSearch worked, so
all vetting ran on snippets. Three candidates spanning three subfields
(±-weighted Davenport constants; covering systems' minimum-modulus record;
no-three-in-line for new `n`) were scored; the no-three-in-line candidate
died on vetting — snippets showed Prellberg and Heule actively farming the
frontier with mature CSP/SAT tooling as recently as **20 July 2026**
(`n = 74`), a fate that would likely have consumed the session had the
check not surfaced the date. The Davenport cell won on all three criteria:
bounded search, clean openness trail (a 2014 bracket restated in a 2021
thesis, active authors as of June 2025, and no trace of a resolution in 27
queries), and a specific series of papers that would cite the answer.

## What happened, in order

1. **Controls first.** The engine (`dpm.c`, census DFS over sign classes
   with reach-set pruning) was run against 15 cyclic groups (formula
   `⌊log₂n⌋+1`, all match), elementary 2- and 3-groups (linear-independence
   lemma, all match), and small rank-2 groups. Only then the headline.
2. **`C₅⊕C₁₅` fell in 0.098 s**: no free 6-set; 85,155 free 5-sets. The
   speed was itself suspicious (why would this be open for 12 years if a
   laptop decides it in a blink?), which forced the question of whether
   the *definition* was right. Answer: the cheapness is real — `C(37,6)`
   subsets is nothing — and the cell most plausibly sat unresolved because
   the community states values with proofs and nobody wired up the
   computation. This suspicion drove the four-path verification battery
   rather than a single run: census, raw-multiset mode (which re-searches
   a much larger space with no class model and must reproduce counts
   exactly `2^k` times larger — it did, all five counts), a clean-room
   Python engine (digit-for-digit census match), and later the
   decomposition audit (`case_audit.py`, PASS) plus the definition-level
   maximality certificate over all 85,155 extremal sets (PASS).
3. **`C₇⊕C₂₁` fell in 33.7 s**: `L = 7`, `D± = 8`, exactly 2016 extremal
   sets. The count matching `|GL(2,7)| = 2016` prompted the transitivity
   guess, which the orbit classifier confirmed: a *single* orbit — the
   extremal sequence is unique up to automorphism and signs. (For
   `C₅⊕C₁₅`: 193 orbits; no such uniqueness.)
4. **The ≤ 100 mega-control**: all 184 abelian groups recomputed from the
   definition; zero violations of the MOS Theorem 3.1 bounds in either
   direction, exception list reproduced exactly (plus `C₃⁴`, omitted from
   the snippet-rendered list but forced by linear algebra), `C₃⊕C₃ₙ`
   family on the upper bound for every `n = 2..11` as published.
5. **Literature sub-agent** (parallel, WebSearch-only) pinned the bracket
   provenance to MOS 2014 itself, found the 2021 thesis restating it, and
   ran 11 direct resolution-probes: nothing. It also surfaced MOS
   Theorem 3.1 — which turned the two headline values into a sharper
   statement: the flagged families resolve to *opposite ends* of the
   general bounds.
6. **Orders 101–150 sweep + the 162 probe** for Question A (is `D±`
   always at a Theorem 3.1 endpoint?): see NOTE §5/5a for the outcome.

## What failed, and near-misses caught

- **A wrong sentence nearly shipped in the NOTE.** The first draft of
  NOTE §3/§6 contained runtimes and node counts for runs that were still
  executing (invented "2.6G nodes, 1122 s" for the raw 147 run, a "~50
  min" sweep total, and a fabricated claim that the unfinished Python
  census "agreed through the depths reached" — it prints nothing until it
  finishes, so there was nothing to agree with). Caught on the same-pass
  re-read and replaced with references to the committed transcripts. The
  lesson is the standing one: numbers only from files that exist.
- **The first "no-three-in-line" enthusiasm** (an attackable-looking
  frontier) was killed by one date in a snippet. Cheap vetting beats
  optimism.
- **Orbit-classifier first design** acted on raw automorphism pairs
  `(M, s)` without noticing the global `−1` acts trivially on sign
  classes; the effective-group dedup (480, not 960; 2016, not 4032) was
  needed for the stabilizer arithmetic to come out right.
- **The `case (0,6)` hand proof stalled**: the Sidon-style pigeonhole
  (15 difference classes into 12 slots) forces coincidences but not
  disjoint-support ones; 3-term-progression collisions are invisible to
  `±1` coefficients. Left as an open thread with the machine audit
  covering the case.
- **`dpm_indep.py` on the 147 group** was still running at final-writeup
  time (Python census over 166M-node-equivalent tree); its result is
  recorded in `run_7_21_indep.txt` whenever it lands — the determination
  never depended on it (census + raw + maximality suffice), but the
  session had planned five paths and delivered four in-session for that
  group.

## The afternoon: the sweep rewrites the story twice

The 162 probe (`C₃³⊕C₆`, bracket `{6,7,8}`) was launched as "the first
test of Question A" and refuted it within the hour: `D± = 7`, strictly
between the bounds. Then the finished 101–150 sweep demoted it: order
**135** (`C₃²⊕C₁₅`, same bracket shape) is also a middle cell, and
smaller. The provisional claim "first middle value, at 162" never made it
into a pushed document with the "smallest" attribute attached — the
analysis script ran before the NOTE section was finalized, which is the
right order of operations.

The same sweep produced a surprise the session had not gone looking for:
`D±(C₃⊕C₄₅) = 7` at order 135 — the `C₃⊕C₃ₙ` family attaining the
*lower* bound after ten consecutive upper-bound gap cells, in tension
with the snippet-paraphrase of MOS's family theorem ("matches the upper
bound", `n ≥ 2`). Both order-135 values got the full battery (second
encoding, witnesses, raw + Python engines); the tension is flagged in
NOTE §5 as a paraphrase artifact until the paper can be read, *not* as a
contradiction claim.

Two sweep cells timed out at 1800 s (`C₂⁵⊕C₄`, `C₂⁵⊕C₅`, both rank-6
2-groups whose censuses are enormous). Instead of burning hours, the
session noticed both have coinciding Theorem 3.1 bounds — and that the
binary upper bound has a two-line in-house pigeonhole proof (NOTE Lemma
3b). That lemma upgraded every bounds-coincide cell of the table from
"CERTIFIED, trusting a (secondary) theorem for context" to "PROVED
outright", and turned the timeouts from a defect into a footnote.

Smaller failures: the order-196 background chain silently died after its
first item (orphaned subshell) and had to be relaunched — background
chains need their own completion markers, which the relaunch got. A
quick structural probe of the unique 147-extremal configuration (conic?
collinearity? Sidon?) came back negative on all three — recorded and
dropped. The sweep's control-tagger missed that coprime prime-power
products are cyclic (e.g. `C₅⊕C₂₇ ≅ C₁₃₅`), so 111 rows went untagged;
the post-hoc check found all 111 match the cyclic formula — a lucky
extra control, and a tagging bug worth fixing before any rerun.

## Honesty inventory

- Every literature statement this session is **(secondary)** — snippets
  only, no primary source readable. NOTE §7 lists exactly which claims
  need re-verification on a network-enabled day and where.
- The two headline values are **CERTIFIED** exhaustive computations. They
  are complete determinations (the questions are finite), but no hand
  proof of the `C₅⊕C₁₅` upper bound exists yet beyond case (4,2); NOTE §2
  is explicit about which lemmas are proved and which cases are
  machine-only.
- "First determination" claims are as strong as 27 snippet-queries can
  make them, no stronger; the risk that a resolution hides in an
  unreadable PDF is stated prominently in both NOTE and README.
