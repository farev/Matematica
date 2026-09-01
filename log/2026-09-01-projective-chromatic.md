# 2026-09-01 — projective-chromatic (χ₂(8), Problem 1 of Bishnoi–Cames van Batenburg–Ravi)

**Target.** Decide χ₂(8) ∈ {5, 6}: can the 255 nonzero vectors of F₂⁸ be
partitioned into 5 sum-free sets (equivalently, can PG(7,2) be properly
5-colored so no line is monochromatic)? This is the first half of Problem 1
in Bishnoi–Cames van Batenburg–Ravi, *The chromatic number of finite
projective spaces* (arXiv:2512.01760, v3 May 2026), verified open against
the paper today. A positive answer gives R(3;5) ≥ 257 against the known
162 ≤ R(3;5) ≤ 307 (bounds as cited in their §6.1); a negative answer
settles their smallest open case. The paper contains no solver work on
n = 8; the encoding is small (255 points, 10,795 lines); the collineation
group is huge — exactly the shape where one day of exact computation can
say something new.

**Result.** χ₂(8) itself: **undecided today** — but the session produced a
new structural theorem about it, mixed PROVED + CERTIFIED:

- **PROVED (Lemma B, "Mersenne obstruction").** For any n, k: no proper
  k-coloring of PG(n−1,2) is invariant under any collineation of order
  3, 7, 31, or 127 (any prime p = 2^d − 1 with d ≥ 2). Reason: such an
  element has an irreducible d-dimensional invariant subspace on which it
  permutes the 2^d − 1 = p nonzero points in a single orbit; that orbit
  spans lines, so any invariant coloring makes them monochromatic.
- **CERTIFIED.** No proper 5-coloring of PG(7,2) is invariant under any
  element of order 17 (one Sylow class; 75-var contracted instance UNSAT,
  131-line DRUP proof, verified by `tools/satcert/rup_check`), nor under
  the Frobenius x ↦ x² of F₂₅₆ (35 orbit cells, UNSAT, 5,227-line DRUP,
  verified).
- **CERTIFIED (landed in-session after color-WLOG breaking).** Both
  conjugacy classes of order-5 elements ([C,C] and [C,I], C the
  companion matrix of x⁴+x³+x²+x+1) — the only remaining odd prime
  order by Lemma B + Cauchy — are **UNSAT**: [C,I] by Glucose42 in
  5.5 s with a 307,292-line pure-DRUP proof verified by the repo's own
  `rup_check` (shipped), independently confirmed by kissat + drat-trim;
  [C,C] by kissat in ~40 min (812 MB DRAT, **drat-trim-verified in
  2,174 s**; too large to commit — hash and regeneration command
  shipped). **Theorem 1: the automorphism group of any proper
  5-coloring of PG(7,2) is a 2-group** — a χ₂(8) = 5 witness, if one
  exists, has essentially no odd symmetry. Sole proviso: the two-line
  color-WLOG lemma (proved in NOTE §4); the unbroken instances were
  left running to remove even that.
- **CERTIFIED (contrast).** At n = 7 an order-5-invariant proper
  5-coloring *does* exist (witness shipped and re-verified from the
  definition, class sizes [21,21,25,27,33]) — and its symmetric family is
  large (≥ 10⁵ raw invariant cell-colorings). Whatever kills 5-colorings
  at n = 8 is not visible one level down.
- **PROVED (Lemma A, hyperplane restriction).** In any proper 5-coloring
  of PG(7,2), every color class meets every hyperplane, and the
  restriction to every one of the 255 hyperplanes is a proper 5-coloring
  of PG(6,2) using all five colors (else 4 colors would properly color
  PG(6,2), contradicting χ₂(7) = 5). Consequence: no class is contained
  in an affine hyperplane — the natural "one class = maximum sum-free
  set" ansatz is impossible.
- **CERTIFIED.** No witness at n = 8 is invariant under any nontrivial
  subgroup of the multiplicative/Frobenius family sweepable today:
  all cyclic multiplicative subgroups (orders 3, 5†, 15, 17, 51, 85, 255;
  † = order-5-with-Frobenius variants; pure order-5 pending as above) are
  DEAD (an orbit contains a full line — e.g. F₄*-cosets *are* lines) or
  UNSAT; ditto ~20 block-diagonal Singer/twisted/swap families (all DEAD:
  transitive block action puts a punctured subspace inside one cell).
- **NUMERICAL.** (i) 1,000 χ₂(7) witnesses sampled by randomized CDCL:
  1,000 distinct structural fingerprints (the witness space is enormous
  and unstructured), and **none extends** over a fixed hyperplane to a
  χ₂(8) = 5 witness (each non-extension is an individually solver-decided
  UNSAT of a 640-var instance); the order-5-symmetric witness does not
  extend either. (ii) The extension bottleneck is *packing*, not
  capacity: Hoffman/ratio bounds from exact Cayley-graph spectra
  (Walsh–Hadamard, integer arithmetic) give Σ_c α-capacity ≈ 265–274 ≫
  128 needed, and greedy already packs ≈ 155 — yet simultaneous packing
  always fails. (iii) Local search: plain min-conflicts stalls at 1
  monochromatic line even at n = 7 (where witnesses exist); with breakout
  weighting n = 7 falls in ~5×10³ flips, while n = 8 has produced
  nothing in ≈ 5×10⁹ flips across two engines (estimated from measured
  rate; exact counters lost when the engines were retired) — consistent with χ₂(8) = 6.
- **Controls.** The published table χ₂(n) = 2,3,3,4,5,5 (n = 2..7)
  reproduced end-to-end: SAT witnesses re-verified from the definition at
  every n, UNSAT decisions at (n,k) = (3,2),(4,2),(5,3) solver-decided;
  (6,4) and (7,4) are theory (R(3;4) ≤ 62), as in the paper. Line counts
  cross-checked against (2ⁿ−1)(2ⁿ−2)/6 and OEIS A006095.

**Connectivity.** arXiv reachable (WebFetch). OEIS reachable (curl JSON
API; WebFetch 403). erdosproblems.com reachable (curl; WebFetch 403).
MathOverflow reachable (curl; WebFetch blocked). All four usable.

**Candidate slate** (three externals, three subfields, all verified open
against sources today):

1. **χ₂(8) ∈ {5,6}** (finite geometry / additive combinatorics / Ramsey).
   Source: arXiv:2512.01760 v3 (fetched today), Problem 1, table entry
   [5,6]; no computational attack in the paper; no follow-up found citing
   a resolution. **Selected.**
2. **Erdős #1074 / #1072, Pillai primes** (computational number theory).
   Source: erdosproblems.com/1074 (fetched today; status OPEN). Exhaustive
   Pillai frontier is A063980's b-file ending at p = 213,043 (2013-era);
   one 4-core sweep to 10⁷ decides Pillai-ness for every p ≤ 10⁷ (47×)
   and yields the first density curve at scale, plus Erdős #1072's f(p)
   distribution as a rider. Passed over: a density/frontier play, not a
   decision, and the 2026 forum shows AI-assisted swarms on the
   computable Erdős problems — the quiet ones are quiet partly because
   they only move a density estimate.
3. **A006946 de Bruijn independence numbers a(14)–a(16)** (graph theory).
   Source: OEIS A006946 (fetched today) + Majer–Novaga arXiv:2604.14671
   (Apr 2026), which settled odd prime orders and left composites open;
   von Brömssen's lift makes an even-order lower-bound search
   self-certifying at the recorded conjectured values. Passed over:
   a search lottery whose upper bounds are already published; newest
   adjacent paper is 4 months old with active authors.

   Near-misses surveyed and rejected (details in agent reports, kept out
   of the repo): ORS₂₀(2) ∈ {78,79} (3-week-old paper, authors mid-stride),
   quaternary Legendre pair ℓ = 42 (KKW have serious compute; likely
   nonexistence-day), Erdős #1107 cubefull sums (first-data play,
   prototype confirmed shape in minutes — good rainy-day target),
   Erdős #385 F(n) (conflicting informal blog numbers to settle; Tao-blog
   visibility), A240114 triangular-grid 3n−11 first break, A333331
   parking-function polytope identification (guaranteed-deliverable DP;
   the conjectured identification looks provable — flagged for a future
   session).

**Internal-thread assessment.** Strongest live thread: balanced-colorings
(Erdős #617) — pin E*(26,6) ∈ [265,269] and E*(17,5) ∈ [104,108] exactly,
or decide K₂₆. Rejected on criterion (a): the 2026-08-27 session's own
solver campaign measured exactly these instances timing out (20 min–3 h
windows, four modern solvers, BreakID-broken included) on this hardware
class; nothing changed since. Odd-giuga's next rung needs ~50 CPU-days or
a new lemma; grimm's next step is a self-range extension (excluded by
mandate); strong-truncations' open half is idea-bound. The external
slate's #1 beat all of these on (a) tractable-bottleneck and (c)
citation-surface; also the last two sessions were on two different
conjectures, so no forced rotation applied.

**What failed.**
- *Raw CDCL on the full 1,275-var instance*: kissat (plain and --sat), >
  1 h each, no verdict — as expected from the balanced-colorings
  experience with pigeonhole-shaped instances.
- *Simulated annealing*: stalls at 35 monochromatic lines from every
  restart (73 restarts × 4×10⁷ moves); the plateau is structural, not a
  schedule artifact — breakout weighting fixed it at n = 7 instantly and
  still produced nothing at n = 8.
- *Naive invariant ansätze*: every transitive block action is dead on
  arrival (a punctured invariant subspace is a single cell and contains
  lines) — 20 of 24 block-diagonal families died this way; only the
  order-5 families with split block action were live, and they are
  exactly the hard pending instances.
- *The "Σα < 128 local obstruction" theorem route*: refuted by
  computation — capacity sums are ≈ 2× the requirement; the obstruction
  is global. (This killed the cheapest path to a proved χ₂(8) = 6.)
- *Python-side per-instance alarms*: SIGALRM does not interrupt a running
  C solver; the first ansatz sweep hung on a weakly-contracted cell.
  Re-architected with per-call conflict budgets (and, for kissat,
  separate processes).
- *An early self-inflicted wound*: `pkill -f` with a pattern matching the
  invoking shell's own command line kills the session's shell. PIDs only.

**Next.** (1) Close the order-5 gap: if either [C,C]/[C,I] run is still
open, cube-and-conquer them (they are 255/315-var instances — within
reach of a dedicated day); that finishes the 2-group theorem cleanly.
(2) The 2-element classes (transvections etc.) are untouched: deciding
those would push the theorem to "trivial automorphism group only".
(3) The extension experiment scales: exhaust extensions over the
*symmetric* n = 7 family (quotient-enumerable) rather than random
samples. (4) The real prize is still χ₂(8) itself: the UNSAT side wants
verified symmetry breaking (VeriPB-style) over GL(8,2) — the technology
the balanced-colorings session also named; a shared tooling investment
would serve both conjectures. (5) If χ₂(8) = 6 falls, χ₂(9) ∈ [6,7] and
the χ₃ ladder open next; if 5, R(3;5) ≥ 257 goes straight to the Ramsey
survey.

**Session hygiene notes.** Branch: harness-designated
`claude/awesome-lovelace-h8dg2v` (mandate's per-conjecture branch naming
overridden by harness branch requirement). The `conjecture-research`
skill named in CLAUDE.md is not installed in this environment; CLAUDE.md
followed directly. Hardware: 4 cores, 15 GB RAM; kissat 4.0.4 built from
source; python-sat 1.8.dev17 (Cadical195/Glucose42); seeds recorded in
scripts and outputs committed under `conjectures/projective-chromatic/`.
