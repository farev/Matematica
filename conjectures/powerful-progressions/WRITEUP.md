# Session write-up — 2026-08-05

## Morning state

Ninth logged session; the mandate for the day was external-first: survey open
problems beyond this repository, build a three-candidate slate, and only pick
an internal thread if it clearly won. Connectivity check failed exactly as on
08-02 and 08-03: the egress proxy 403s arxiv.org, oeis.org, erdosproblems.com,
mathoverflow.net and every mirror tried (huggingface/papers, alphaxiv,
emergentmind); only web-search summaries and pypi got through. So the session
was again run under the rule: every citation (secondary), every "still open"
claim is a search-summary claim.

## Infrastructure detour (kept)

Two of the three candidate branches under consideration (exact Rado-type
numbers; anything SAT-shaped) would need UNSAT verdicts that are actually
certified, which the 08-03 session lacked (its known defect: solver verdicts
with no checked proof). Before selection I built the missing piece:

- `tools/satcert/rup_check.c` — a forward DRUP (reverse-unit-propagation)
  proof checker written from the definition, no code shared with any solver.
- `tools/satcert/check_coloring.c` — an independent brute-force verifier for
  coloring witnesses.
- `tools/satcert/rado.py` — encoder + bisection driver: Cadical for
  bracketing, Glucose42 with proof logging only at the boundary, RUP check of
  the proof, witness re-verified by the C checker.

Validation: rup_check verifies a real Glucose proof of PHP(6,5) and rejects
an injected non-RUP clause and a truncated proof; the pipeline reproduced
R₂(x+y=z)=5, R₃(x+y=z)=14, R₂(x+y=2z, nontrivial)=9, R₃(x−y=z)=14 in 0.09 s
with every UNSAT step proof-checked, and then R₄(x+y=z)=45 end-to-end
(witness at 44 independently verified: 946 solutions checked, none
monochromatic; UNSAT at 45 with DRUP proof RUP-VERIFIED). The naive
incremental driver was too slow for R₄ — solving every n from 1 up — and was
replaced by exponential climb + bisection with boundary-only certification;
the proof-logged Glucose solve at n=45 dominated the 28.5-minute wall time.

None of this was used by the problem eventually selected. It is committed
because it closes a recorded defect class and is calibrated, and any future
Rado/Schur-type session starts from it.

## The slate and the selection

Three scouts ran in parallel (number theory; arithmetic Ramsey; graph
conjectures). Full details in the daily log; the short version:

- **E1 (selected): van Doorn's consecutive-powerful-triples conjecture**
  (arXiv:2605.06697, May 2026, evidence = 18 triples below 10^14). The
  novelty check is *decisively clean* under today's constraints: the
  published frontier is a single number that my code reproduced exactly
  before any new claim was made.
- **E2: off-diagonal generalized Schur / 3-color Rado values.** Killed by
  rule 3: the field is active (Song–Mao Apr 2026 on exactly the target
  conjecture; a distributed farm on the neighboring 4-color case; a
  cluster group extending the (a,b,b) tables), and the one 4-core-sized
  family requires knowing Ahmed–Schaal's 26 published values — in a PDF the
  proxy blocks. I could have computed values today but could not have known
  which were new. Unverifiable novelty is not novelty.
- **E3: refuting a recent graph-invariant conjecture.** Killed by
  competition: the scout found two dedicated AI "refutation factories"
  actively harvesting exactly this genre in 2026, one of which flagged the
  best candidate internally eight weeks ago, plus a definition-freezing
  hazard (Graffiti glossary semantics) that requires the blocked PDFs.
- **Internal thread (passed over): circular-thresholds Pansiot-encoding
  search.** Concrete and compute-breakable, but five sweeps in that session
  came back empty across five alphabets, the published route to the theorem
  uses non-uniform families, and the conjecture was worked two days ago.

## The attack, in order

1. **Calibrate before claiming.** 10^10 run: powerful count 214122 (matches
   OEIS A118896), gap-1 pairs (8,9), (288,289), (675,676), (9800,9801)
   (matches A060355), smallest triple (1728, 1764, 1800) d=36 (matches the
   paper's summary). Then the decisive control: at 10^14, **exactly 18
   triples** — van Doorn's number.
2. **Extend.** 10^16 (31 triples, 23 s), 10^17 (62, 77 s), then a segmented
   rewrite for memory and 10^18 (152, 3m29s), 10^19 (346, 7m52s). Two bugs
   were caught in review before any run: triples wholly inside the
   segment-boundary carry were double-counted, and the AP4 check was skipped
   by the same guard.
3. **Decompose.** Union-find over componentwise rational ratios: 152 triples
   → 15 chains at 10^18; 346 → 16 at 10^19. The first structural surprise:
   an assert I had written defensively — "chain members are integer multiples
   of the smallest member" — **fired**. P15's chain contains members at
   ratios 5/2 and 45/2 to its primitive. The model was wrong, not the code:
   the right object is the gcd-1 root, of which all members are integer
   multiples, and the right criterion is Lemma 1′ (mandatory primes +
   valuation bound), proved and then mechanically re-checked against every
   observed multiplier (zero exceptions).
4. **Roots.** (1728, 1764, 1800) = 36·(48, 49, 50) — the census's most
   famous triple is a scaled AP of *consecutive integers*, and 36 is exactly
   the minimal Lemma-1′ multiplier of that root. P6's root has common
   difference 7. No root is itself powerful (consistent with
   Erdős–Mollin–Walsh for the d₀=1 root).
5. **Patterns tested, one killed.** At 10^17 every primitive contained
   exactly one perfect square, 8 of 11 in the middle — looked like a law.
   At 10^18 **P15 broke it** (zero squares). What survives: Lemma 2 proves
   "at most one" whenever d ≤ √x (14 of 16 primitives); "at least one" is
   false. This is the session's cleanest example of why range extensions
   matter: the pattern had held for 15 chains and 40 years of horizon.
6. **Saturation.** For each root, ascending scan for the first admissible
   multiplier whose multiple is *not* consecutive. Every long chain loses
   multiples (P8, the 272-member chain, first at m=288; P1 at m=72 — the
   intruder is 3481 = 59² inside (3456, 3600)); one short chain (P6, the
   d₀=7 root) is saturated so far. This kills the naive route to the
   conjecture (scale one triple forever) and quantifies exactly how it dies.

## What failed

- **Reading the paper.** Five mirror attempts, all 403. Consequence: van
  Doorn's family "A₁" is undefined here, so the primitive decomposition
  cannot be compared to his family structure — stated as a defect everywhere
  the comparison would matter.
- **The one-square law** (above): true 15 times, false the 16th.
- **First analyzer design**: enumerating all admissible multipliers up to
  X/z is infeasible for old primitives (K ~ 5×10^14); redesigned to a
  first-missing scan. A cosmetic bug (vacuous "SATURATED" when zero
  admissible multipliers fall under the scan cap) was found by reading the
  output against P16 and fixed.
- **The naive incremental Rado driver** (infrastructure detour): correct but
  unusably slow at the R₄ tier; replaced.
- **External count anchor at 10^19**: not found in search summaries
  (A118896 values surfaced only through 10^12), so the 10^19 total rests on
  internal evidence plus the asymptotic sanity check.

## Costs

4 cores, 15 GB, single-threaded C++ throughout. Census: 1.5 s at 10^14,
77 s at 10^17 (monolithic, 5.6 GB), 3m29s at 10^18 and 7m52s at 10^19
(segmented, ≤ 2.5 GB). Verification: 24 s (152 triples), 1m51s (346).
Analysis: 1.2 s. SAT validation battery: 0.09 s; R₄ end-to-end 28.5 min.
No randomness anywhere in any pipeline.
