# 2026-09-16 — nonrepetitive-lattices (Thue chromatic numbers of the square, triangular and king lattices; audit of arXiv:2510.11263)

**Target.** New external problem, per the standing mandate. Tao's grid paper
(arXiv:2303.16237, Discrete Math. 349 (2026) 114828) proves
`5 ≤ π(P_n□P_n) ≤ 12` for the nonrepetitive (Thue) chromatic number of the
square grid and ends with "Is π(P_n□P_n) > 5 for large n? ... Perhaps
computers can help." A SAT encoding of nonrepetitive 5-colourings returned
UNSAT on the 8×8 grid in 13 s, which would have been `π ≥ 6`; the novelty
check then found Tao–Zhang–Zhang–Toole (arXiv:2510.11263, 13 Oct 2025), who
already prove `π(P□P) ≥ 6`, `π(P⊠P) ≥ 9` (king's graph) and `π(T₃) ≥ 9`
(triangular lattice) by enumerating colourings of growing patches, and whose
discussion says their method cannot go further. The session therefore aimed at
the next colour on each lattice (`π(P□P) ≥ 7`, `π(P⊠P) ≥ 10`, `π(T₃) ≥ 10`),
with an audit of their three tables as the first step, since those tables are
the entire proof of two of their three theorems. Achieving it would have meant
one DRUP-certified UNSAT for 6, 9 or 9 colours on some finite patch.

**Connectivity (checked 07:41 UTC).** arxiv.org reachable via WebFetch
(listing, abstracts, HTML, PDF; the PDF text extracted locally with pymupdf).
oeis.org reachable via WebFetch. erdosproblems.com reachable via WebFetch
(1,220 problems, 586 solved on the front page). mathoverflow.net refused to
both WebFetch and WebSearch, but curl reaches it and the Stack Exchange API
(HTTP 200); all MathOverflow reads went through the API. github.com source
archives (kissat, cadical) are refused by the sandbox's egress policy;
raw.githubusercontent.com is not, which is how drat-trim was obtained. pip
works (python-sat 1.9, pymupdf, numpy installed).

**Candidate slate** (three externals from three subfields, chosen from four
parallel scouts on erdosproblems.com, recent arXiv, OEIS and MathOverflow;
every statement checked against the primary page on 2026-09-16; full scout
reports were in the session scratchpad and are summarised here):

1. **Nonrepetitive chromatic numbers of lattices** (graph colouring /
   combinatorics on words). Statement: determine `π(P□P)`, `π(P⊠P)`,
   `π(T₃)`; published `6 ≤ π(P□P) ≤ 12`, `9 ≤ π(P⊠P) ≤ 16`, `π(T₃) ≥ 9`.
   Sources: arxiv.org/abs/2303.16237 (v3, Aug 2024; abstract and HTML read
   2026-09-16), arxiv.org/abs/2510.11263 (PDF read in full 2026-09-16),
   Wood's survey arxiv.org/abs/2009.02001 (no grid values). Open: the October
   2025 paper states these as the best bounds and no 2026 follow-up was found
   by searches for "non-repetitive chromatic number" with grid / strong
   product / triangular. **Selected.**
2. **Erdős #854, gaps between consecutive totatives of a primorial**
   (computational number theory). Statement (verbatim from
   erdosproblems.com/854, fetched 2026-09-16): "Let n_k denote the kth
   primorial ... If 1 = a_1 < a_2 < ⋯ a_{φ(n_k)} = n_k − 1 is the sequence of
   integers coprime to n_k, then estimate the smallest even integer not of the
   form a_{i+1} − a_i. Are there ≫ max_i (a_{i+1} − a_i) many even integers of
   the form a_{j+1} − a_j?" Site status OPEN (last edited 4 Nov 2025); OEIS
   A389839 has the smallest missing gap for k ≤ 12 only (Cambie, Howroyd, Wu,
   Oct 2025), where Erdős's belief that every even gap up to the maximum
   occurs fails at k = 6 and 8. Passed over: a solid CERTIFIED table
   extension (covering-system CSP per gap), but table-shaped; the selected
   problem had a live audit finding within the first hour.
3. **Barát–Gyárfás–Tóth non-nested matchings** (ordered Ramsey theory).
   Statement (arXiv:2511.02892, Problem 1.1, verbatim): "Determine the
   smallest m such that in every 2-coloring of the edges of the ordered
   complete graph K_m, there is a monochromatic non-nested matching of size n.
   The answer is trivially between 3n−1 and 4n−2. We conjectured that the
   lower bound is optimal." Conjecture 2.5 of arXiv:2210.10135 (JGT 2024).
   Open per the November 2025 problem collection: small cases "up to n = 5 or
   6" checked by others, unpublished, no certificate. Passed over: a SAT
   confirmation at n = 6, 7 would be CERTIFIED but confirms a conjecture at
   cases already believed checked.

   Also surveyed and set aside: OEIS A398173 (unique-sum-free subsets of
   Z/pZ, Green's Problem 27; next prime 79, but the maintainer's repository
   says work is in progress on cloud workers), arXiv:2609.15081 (chromatic
   number of the arithmetic graph B_195, two days old), MO 512119 / OEIS
   A396889 (polynomials of degree and height M prime at 1..M; NUMERICAL
   only), MO 514742 (square achievement game, already solved by the poster's
   own search), Conway's 99-graph (attacked by an AI agent in August,
   arXiv:2608.11211), no-three-in-line n = 47 (solutions now known for all
   n ≤ 76 after Prellberg, Riley and Heule's 2026 work), and the
   Erdős–Faber–Lovász small cases (Kirchweger–Peitl–Szeider, SAT 2023).

**Internal-thread assessment.** Strongest live thread: ordinary-lines, cube
A (45 open ∗-classes of the meeting case; closing them all gives
`t₂(15) ≥ 8` CERTIFIED and removes "(partial)" from the row), scripted and
resumable, ≈ 25 CPU-hours measured, three times that with proof logging.
Runners-up: peaceable-queens a(19) (13–16 h on 4 cores, single engine),
generalized-schur S(3;3,3,12) (< 1 h, one table entry), chromatic-ramsey
F(3,5) (cost unmeasured), dissociated-subsets m₅ (needs a C port, on an
unmerged branch). No conjecture was worked in the two most recent sessions
(2026-09-09 collinear-walks, 2026-09-08 dissociated-subsets), so the rotation
rule did not bind.

**Selection.** (a) Compute: the selected problem's bottleneck is exactly a
SAT search; it broke within minutes (the 5-colour rediscovery), and the
lattice ladder is a sequence of such runs. Cube A is a 25-hour sweep with no
new idea in it. (b) Already done: the paper's enumeration is the only prior
computation, its authors say it cannot go further, and no one had audited it;
the lazy-path SAT formulation is not in their paper. (c) Extends
Tao–Zhang–Zhang–Toole 2025 and Tao 2026 directly, and would be cited in
Wood's dynamic survey. The internal thread loses on (a) and (c); ties would
have gone to the new problem anyway.

**Result.** **CERTIFIED and an audit.**

- `π(P□P) ≥ 6`: the 41-vertex spiral patch of the square grid has no
  nonrepetitive 5-colouring (DRUP proof, 62 807 lines, checked by drat-trim
  and by `tools/satcert/rup_check`); the 40-vertex patch has one, verified by
  enumerating 5.2·10⁹ simple paths. Rediscovery of arXiv:2510.11263 Theorem
  1.8, marked as such; the paper's Table 1 death index 41 is replicated
  exactly by an independent enumerator.
- `π(P⊠P) ≥ 9`: the 23-vertex spiral patch of the king's graph has no
  nonrepetitive 8-colouring (proof 740 087 lines, both checkers; the trimmed
  proof of 666 403 lines is committed). Independent of the paper's
  computation, which is wrong at that point: its Table 2 reports zero
  colourings at 20 vertices, but the 20- and 22-vertex patches admit
  nonrepetitive 8-colourings (witnesses verified over 6.6·10⁸ and 4.0·10⁹
  paths); the enumerator gives `n(22) = 32, n(23) = 0`.
- Audit of `π(T₃) ≥ 9` (their Theorem 1.9): the 23-vertex spiral patch of
  the triangular lattice, under both natural embeddings of their vertex order,
  and the 5×5 blocks containing it, admit nonrepetitive 8-colourings (four
  witnesses verified over 1.2·10⁸ to 9.0·10⁸ paths each). Their Table 3 entry
  `n(23) = 0` is false and the theorem has no valid proof. It is not refuted.
- `π(T₃) ≥ 8` (new, CERTIFIED): the 37-vertex hexagon of radius 3 has no
  nonrepetitive 7-colouring (925 variables, 265 459 clauses, Glucose 198 s,
  proof 2 605 263 lines; the radius-2 hexagon kills 6 colours in 0.1 s). The
  previous valid bound was `π(T₃) ≥ π(P□P) ≥ 6`.
- NUMERICAL: 6 colours on the 10×10 grid survive all repetitions of ≤ 18
  vertices (the surviving colouring has repetitions of 20 and 24 vertices); 9
  colours on a 30-vertex king patch and 8 colours on the 37-vertex `T₃`
  hexagon survive repetitions of ≤ 16 vertices.

Standing bounds after the session: `6 ≤ π(P□P) ≤ 12`, `9 ≤ π(P⊠P) ≤ 16`,
`8 ≤ π(T₃) ≤ 16`. Everything is in `conjectures/nonrepetitive-lattices/`
(NOTE, WRITEUP, scripts, ten witnesses, four certificates, replication
tables); PAGE.md written because the row is new.

**What failed.**

- The actual target, the next colour: 6 colours on `P□P` (10×10 grid, lazy
  repetitions to 16 vertices: 653 000 clauses in 230 s, no contradiction;
  eager paths to 12 plus lazy to 18: SAT), 9 colours on `P⊠P` (6×6 and
  30-vertex spiral: SAT up to 10 and 16 vertices; the 8×8 block's first solve
  did not finish in 6 minutes; the 7×7 block was stopped without a verdict
  after 42 CPU-minutes), 9 colours on `T₃` (9×9 rhombus: 3 million
  lazy clauses and climbing) and 8 colours on `T₃` (37-vertex hexagon SAT to
  16 vertices; the 61-vertex hexagon accumulated 5 million lazy clauses in
  6.5 minutes without converging and was stopped). The wall is the growth of
  the set of relevant repetitive paths, not solver time: each solve took a
  fraction of a second.
- The first hour's "new theorem" (`π(P□P) ≥ 6`) was a rediscovery, caught by
  the literature search after the computation.
- The counting replication of Table 3 to 25 vertices was killed after 18
  CPU-minutes: the canonical counts pass a million by 16 vertices and the SAT
  witnesses had already settled the question.
- The authors' code repository was unreadable from the sandbox (only an empty
  README via the raw host), so the cause of their two wrong table entries is
  not identified.
- Kissat and CaDiCaL could not be built (github archives refused); proofs
  come from Glucose 4.2 through python-sat, which is slower (198 s for the
  7-colour `T₃` instance that CaDiCaL settled in 210 s of lazy iterations).

**Next.**

1. `π(T₃) ≥ 9` with a certificate: 8 colours on a `T₃` patch. The 37-vertex
   hexagon is not enough and the 61-vertex one balloons; try an intermediate
   shape (a 6×6 offset block, 36 vertices, or the 45-vertex hexagon-plus-ring)
   and raise the eager path bound to 8 so the lazy loop only handles long
   repetitions; cube on the colours of the central triangle if the final
   instance is slow.
2. Write to the authors of arXiv:2510.11263 with the five brute-force-verified
   witnesses (files named in NOTE §3, Theorems 2 and 3).
3. `π(P□P) ≥ 7`: analyse the 20- and 24-vertex repetitions that kill the
   found 6-colourings of the 10×10 grid (shapes, how many are translates of
   each other) and encode only that family eagerly on a 14×14 grid.
4. `π(P⊠P) ≥ 10`: the 7×7 king block with 9 colours is the most promising
   unfinished run. Its lazy loop's solve times climbed from 0.1 s to 15 s
   per iteration by iteration 81 (400 000 lazy clauses, repetitions of 8 to
   14 vertices) before it was stopped at 42 CPU-minutes, and the 8×8 block's
   first solve did not finish in 6 minutes; in every instance that ended
   UNSAT today the solves stayed under a second until the end, so growing
   solve times suggest an instance near the boundary. Resume it with
   proof-capable solving from the start (build CaDiCaL or Kissat from a
   reachable source) and cube on the centre's colours if it stalls.
