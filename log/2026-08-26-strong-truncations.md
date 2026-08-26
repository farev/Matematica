# 2026-08-26 — strong-truncations

**Target.** A new external problem, per the session mandate: Kardoš's
Problem 4.1 from the 33rd Cycles and Colourings workshop list
(arXiv:2511.02892, Nov 2025 (secondary)) — is every diamond-free
claw-free cubic graph strongly 6-edge-colorable, equivalently is
χ′ₛ(T(G)) = 6 for every cubic G? Chosen because the bottleneck is
exactly a compute-shaped one: tiny SAT/backtracking instances over an
exhaustively generatable family, certified either way, on a 9-month-old
named open problem with a clear audience (Kardoš, Lin–Lin, Han–Cui).

**Result.** PROVED + CERTIFIED — the answer to the diamond-free
claw-free phrasing is **no**.

- **PROVED (Balloon Lemma).** If a cubic multigraph H contains a
  *balloon* — a doubled edge whose endpoints share their third
  neighbour, i.e. an expanded loop — then the truncation T(H) has no
  strong 6-edge-coloring. Ten-line palette argument in a dart
  reformulation of strong 6-colorings of truncations (both proved in
  NOTE.md §1–2), machine-confirmed by exhaustive enumeration of the
  balloon piece's boundary states (zero exist).
- **CERTIFIED.** G₁₈ = T(H₆), an 18-vertex claw-free diamond-free cubic
  graph with χ′ₛ = 7: UNSAT at 6 colors with a DRUP proof checked by
  `tools/satcert/rup_check`, verified 7-coloring, two independent
  enumeration paths (geng over all 41,301 cubic graphs on 18 vertices +
  claw/diamond filter; multig quotients + truncation) converging on the
  same graph (equal canonical forms). G₁₈ is the **unique smallest**
  such graph (prism aside, χ′ₛ = 9); Lin–Lin's tight examples for their
  7-bound all contain diamonds (secondary), so diamonds are not needed
  for tightness. Infinite family: balloon quotients exist at every
  admissible order, chain family certified χ′ₛ = 7 for k ≤ 8.
- **CERTIFIED (census).** All truncations of cubic multigraphs of order
  ≤ 16 decided by two independent engines (backtracking C engine + SAT,
  no shared code), every 6-witness re-verified from the definition by a
  third implementation, every NOT6 confirmed UNSAT by the second engine
  and given a verified 7-coloring: orders 2–16 = 1, 2, 6, 20, 91, 509,
  3608, 31856 quotients with 0, 0, 1, 4, 19, 102, 682, 5497 having
  χ′ₛ = 7. **Exact empirical characterization: χ′ₛ(T(H)) = 7 ⟺ H
  contains a balloon** (the sole balloon-free exception being the triple
  edge, whose truncation is the prism, χ′ₛ = 9). Order 18 appended
  under a lighter protocol: all 287,459 balloon-free quotients have
  6-colorable truncations (654 engine caps SAT-resolved; witnesses
  verified), the 52,957 balloon quotients are ≥ 7 by the lemma with a
  500-sample UNSAT-confirmed — the conjecture's open half verified for
  all 317,246 balloon-free quotients ≤ 18.
- **PROVED (wire calculus) + CERTIFIED (claw-free census).** A general
  bridge-interface lemma reduces any 2-terminal piece of a cubic graph
  to a 60-state transfer relation; the three basic pieces are a
  trichotomy — diamond: color preserved / pairs disjoint; dumbbell:
  color changed / pair preserved; balloon: empty (the obstruction).
  Composing through a diamond gives exactly {S_a ≠ S_b}, so inserting a
  diamond into a bridge never destroys strong 6-colorability (first
  hand derivation over-claimed "universal joint"; the machine check
  refuted it and the closed form was corrected — see WRITEUP). Census
  of the whole claw-free class (diamonds allowed), orders 4–20:
  1,1,1,1,3,3,5,11,15 graphs, of which 0,–,0,1,0,3,1,5,5 have
  χ′ₛ = 7 (prism: 9); the 10-vertex instance is the unique smallest
  claw-free cubic graph with χ′ₛ = 7 (novelty vs Lin–Lin unchecked).
- **CERTIFIED (the intended reading survives).** Every truncation of a
  connected **simple** cubic graph on ≤ 20 vertices — 556,471 quotients,
  T on up to 60 vertices — is strongly 6-edge-colorable
  (definition-checked witness per instance; engine-capped stragglers
  SAT-resolved). First systematic verification beyond Han–Cui's
  truncated prisms (secondary).

## Connectivity check

From the cloud sandbox (egress-proxied), 2026-08-26: direct fetch to
arxiv.org (+export mirror), oeis.org, erdosproblems.com **blocked**;
mathoverflow.net unreachable (also to the search crawler). WebSearch
works and returns content snippets; raw.githubusercontent.com works
(OEIS text via the official oeisdata git mirror; A000421/A002851
confirmed there). PyPI reachable (numpy, sympy, python-sat, pynauty
sdist — the latter carrying the full nauty 2.8.8 source, whence geng /
multig / labelg were built and cross-checked). Every literature
statement this session is **(secondary)** — statements reconstructed
from search snippets, not read in the original. The `conjecture-research`
skill is not installed in this sandbox; CLAUDE.md discipline applied
manually. Environment: 4 cores, 15 GB RAM, Python 3.11.15, gcc 12.

## Candidate slate (external)

Three scouts (Erdős database, OEIS conjectures, recent arXiv/MO open
problems) ran in parallel; full reports preserved in the session
transcript. The slate:

1. **Kardoš Problem 4.1** (graph coloring, C&C 2025 list,
   arXiv:2511.02892 (secondary)). Open per searches; partial results:
   Lin–Lin χ′ₛ ∈ {6,7} for claw-free cubic ≠ prism (tight examples all
   with diamonds), Han–Cui truncated prisms = 6. Bottleneck: exhaustive
   small-order decision — pure compute. Audience: the C&C community;
   the list exists to be answered.
2. **Bala's conjectures on A004123** (integer sequences / continued
   fractions; OEIS entry, conjectures dated 2022 (secondary)): prove the
   Stieltjes continued fraction for the g.f. and the mod-k eventual
   periodicity for the class G(eˣ−1). Provable-looking but idea-bound;
   periodicity prong possibly folklore; no compute leverage.
3. **Erdős #11** (number theory: odd n = squarefree + 2^k; Hercher
   arXiv:2411.01964 verified to 2⁵⁰ (secondary)). Compute-shaped but the
   frontier is GPU-industrial; a 4-core half-day yields 4–8×, not an
   order of magnitude.

Also surveyed and set aside: Erdős #366 (powerful-number pair census —
strong overlap with this repo's existing powerful-progressions
machinery, and the certified-frontier provenance needs a day of its own
to pin), #127 (Erdős–Gyárfás — already an internal thread here),
A094960 refute-by-search (low success prior), A181142/A220433
recurrence proofs (clean but small), Alexeev–Mixon size-4 Sidon
non-extenders (hot area, scoop-prone, statements only snippet-verified).

## Internal-thread assessment

Recent sessions: 08-25 signed-difference-sets, 08-23 odd-giuga (no
two-consecutive rule in force). Strongest live internal thread:
signed-difference-sets — port Masselot's layered quotient refinement
into `sds_search.c` and attack the ~22,453 still-Open cells at order
> 36; significant progress would move that row. Scored against the
externals: (a) compute fits, but each new order is a wall, not a sweep;
(b) collision risk is real — Masselot is active on exactly this
continuation with better tooling; (c) audience identical to what two
sessions already served. Runner-up (odd-giuga m = 13) is explicitly
measured at ~10¹⁵ nodes — out of reach. The mandate's default (new
external problem) stood: Kardoš's problem beat the internal thread on
(a) and (b) outright.

**Selection.** Kardoš Problem 4.1, with the day's target: decide strong
6-edge-colorability exhaustively over all truncations of cubic
multigraphs to the largest reachable order, certified both ways, and
extract structure — achieved means either a counterexample family or a
verified-range statement plus proved lemmas.

## What failed / dead ends

- First bulk engine run (order 12) spent nine minutes because NOT6
  instances escalated to exact-χ′ₛ computation inline and 46 borderline
  instances thrashed against a 2×10⁸ node cap; split the pipeline into
  decide-then-resolve (SAT fallback) and the same order ran in seconds.
- A sed-based negative control silently failed to corrupt the witness
  file (pattern didn't match), making the verifier look vacuous; caught
  it, redid the corruption in Python, verifier rejects as intended.
- An empty leftover file (`census010.txt`) shadowed the real order-10
  census in the first χ′ₛ = 7 certification pass (789 ≠ 808 instances);
  caught by count reconciliation, removed, pass completed.
- The candidate uniform construction for the converse (3-edge-coloring
  × sign flips with the canonical opposite-color t) reduces to three
  GF(2) parity systems that are *not* always solvable — recorded in
  NOTE §6 as a sufficient condition and attack line, not a proof.
- MathOverflow could not be scouted at all (blocked even via search).

## Next

- Prove Conjecture C's open half: balloon-free (≠ triple edge) ⇒
  χ′ₛ(T(H)) = 6. The dumbbell transfer relation (same spare pair, stem
  colors differ) + the GF(2) construction are the live tools.
- From a machine with full egress: read Kardoš's Problem 4.1, Lin–Lin,
  and Han–Cui in the original (every citation today is (secondary));
  re-run the novelty search; then decide whether G₁₈ and the Balloon
  Lemma warrant a short arXiv note (the C&C list is the natural venue
  to answer) — and whether to write Kardoš.
- The census over claw-free cubic graphs *with* diamonds (which of
  Lin–Lin's class need 7) is a one-command extension of the pipeline.
- OEIS: 1, 4, 19, 102, 682, 5497, … (balloon quotients / χ′ₛ = 7
  truncations by order) matched nothing findable by search; check
  against OEIS proper and consider submitting.
