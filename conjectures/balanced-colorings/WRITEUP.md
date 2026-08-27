# Session writeup — 2026-08-27 — Erdős #617 at r = 5

The narrative, including what failed. NOTE.md has the statements and
proofs; README.md the reproduction table. Nothing here is edited to look
smarter in hindsight.

## Why this problem

Chosen by the day's mandate (external, compute-shaped, verifiably open):
Erdős Problem #617 — no balanced r-colouring of K_{r²+1} for r ≥ 3 —
with the r = 5 case (K₂₆) open since the 1999 Erdős–Gyárfás paper proved
r = 3, 4. Three scouted alternatives (Bala's plane-partition
supercongruences; additive cubes over ternary alphabets; queens/torus
OEIS frontiers) and the internal threads are recorded in the daily log
with the selection argument. The deciding fact: no trace of any
computational attack on #617 anywhere reachable, and the instance sits
at a size (325 edge variables, 5 colours) that looked SAT-decidable.
That last impression was wrong in an instructive way — see "The hardness
wall" below.

## What worked

1. **The affine construction, before writing any solver.** Deriving the
   K₂₅ witness (AG(2,5), merge two parallel classes, three-line
   pigeonhole) pinned T(5) ≥ 25 and concentrated the whole problem on
   K₂₆. Definition-level verification over all 177,100 6-subsets ran in
   seconds. The general form (Lemma 2: distance-(r−1) codes give
   balanced colourings) later organized everything: the K₂₅ witness is
   the Reed–Solomon [5,2,4]₅ code, the structured sector of the problem
   is exactly the MOLS existence question at r², and the r = 2
   counterexample (C₅) is exactly the escape that codes cannot make.

2. **Small facts before big computations.** Fact A (no monochromatic
   K_{r+1} ⇒ every complement has χ ≥ r+1 at r²+1) came from asking why
   the first Singleton-bound proof of Corollary A1 felt too heavy; the
   two-line counting proof replaced it the same afternoon. The order of
   discovery is preserved in NOTE §2's remark: Singleton survives as the
   route to the codes⟺structured-colourings equivalence, not as the
   proof of emptiness.

3. **The extremal reframing.** Realizing that every colour class of a
   K₂₆ witness is a (6,6)-Ramsey graph (α ≤ 5 from coverage, ω ≤ 5 from
   Fact A) turned the conjecture into a statement about E*(26,6) = max
   edges of such graphs, with the exactly-tight threshold 260. The
   morning's hope — E*(26,6) < 260 would prove the r = 5 case by pure
   counting — died honestly at both calibration points: E*(10,4) = 31
   misses the r = 3 threshold (30) by one edge, and a 29-second SAT run
   found a 260-edge (6,6)-graph on 26 vertices. The afternoon's sharper
   hope — E*(26,6) = 260 exactly would force total rigidity
   (Proposition 4) — died just as fast: 261 is satisfiable (verified
   witness committed). The barrier being *sharp* at all three r is a
   finding in its own right: the conjecture lives strictly in the joint
   structure of the five classes, not in any per-class extremal bound.

4. **Structured refutation hunts, both decisively negative.**
   - The affine family on K₂₅ has exactly 50 free pairs (the dropped
     parallel class); extension to K₂₆ is a 375-variable SAT instance
     over the free pairs + 25 new edges. UNSAT in 0.1 s, DRUP proof
     checked by `tools/satcert/rup_check`. The q = 2 analogue (K₄ → K₅,
     where extensions DO exist) passes as positive control, found
     exactly the 2 C₅-type completions.
   - Lemma 6's profile arithmetic (2a + b = 5 per colour, so every
     invariant class has exactly 65 edges) kills Z₂₆ outright and
     reduces D₁₃ to 3,198 candidate classes; not one has α ≤ 5. So no
     vertex-regular witness exists — a proved asymmetry with r = 2,
     whose witness is a circulant.

5. **Controls everywhere.** The encoder reproduced T(2) = 5 against a
   2¹⁵ exhaustion; every SAT witness was re-verified by an independent
   definition-level checker; the α-filter in `dihedral.py` passes the
   221-edge circulant and rejects a bare matching; the E* witnesses were
   re-verified from files. The one bug the controls caught: the first
   circulant sweep printed half the true edge count (the class-size
   formula divided by 2 twice); the α/ω filtering was unaffected, the
   count display was fixed, and the sweep re-run before anything was
   committed on top of it.

## The hardness wall (the day's main negative result)

The direct CNF for "K₁₀ has a balanced 3-colouring" — 135 variables, 810
clauses — is beyond CaDiCaL, Glucose and kissat unaided (minutes to
hours, no verdict), and beyond RoundingSat's cutting planes on the OPB
form (> 120 s). Diagnosis: the refutation is a pigeonhole-like counting
argument; resolution needs exponential size, and the S_N × S_r symmetry
(26! · 5! at the target size) multiplies every subproof. BreakID's
symmetry-breaking predicates cure K₁₀ (3.1 s, UNSAT — the r = 3 theorem
machine-reproduced). But scaling collapses: K₁₇ (r = 4, a known theorem)
survived >10 min symmetry-broken, and both the broken and the
broken+cardinality (Lemma-1 totalizers) K₁₇/K₂₆ runs were still open at
this writeup's deadline — see README for their final state. Conclusion
recorded for the next session: the direct instance needs *verified*
symmetry breaking at scale (VeriPB-style certified SBPs) or the
structural route (E* catalogue + interaction lemmas), not more solver
time. This hardness also explains why no computational resolution of
#617 exists in the literature: the natural attack genuinely does not
work.

## What failed, in order

- **Singleton as the emptiness proof** — superseded by the two-line
  Fact A argument (kept for the equivalence; no harm done, an
  afternoon's detour).
- **The pure counting kill** (E* < threshold) — refuted at all three r
  by the machine within minutes of being formulated. The sharpness
  (miss-by-one at r = 3, miss-by-zero-slack at r = 5) was not
  anticipated and is the interesting residue.
- **The rigidity kill** (E*(26,6) = 260) — refuted by the 261-edge
  witness.
- **RoundingSat without symmetry breaking** — timed out even at K₁₀;
  PB conflict analysis alone does not overcome the orbit blowup.
- **A first foray at second-order counting** (pairs/triples of classes
  jointly) — the pair bound reduces to twice the single bound (110 =
  2·55, attainable), no gain; recorded so the next session does not
  retry it naively.
- **Chained background solver launches** — two process-management
  mishaps (a pkill pattern that matched its own command line; a wrapper
  exit that orphaned one of two solver launches) cost ~15 minutes and
  one redundant kissat run before the launch pattern was fixed to one
  tracked task per solver.

## Where this leaves the problem

K₂₆'s verdict is open at session end unless the running jobs land (see
README for their outcome). The session's permanent yield: the
T(5) ≥ 25 certified witness and construction lemmas; the E* programme
with three certified values and the sharp-barrier finding; the two
exclusion theorems (no code-family extension — DRUP-certified; no
vertex-regular witness); the hardness diagnosis with the BreakID cure at
r = 3; and a reproducible pipeline (encoder + controls + independent
verifiers) that the next session can point at cube-and-conquer or
VeriPB. The sharpest next questions are NOTE §7's: exact E*(26,6), and
whether the E*-extremal catalogue plus the 65-edge-average constraint
supports an interaction lemma.
