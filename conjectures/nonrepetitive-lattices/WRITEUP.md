# Session write-up, 2026-09-16: nonrepetitive colourings of lattices

Lab notebook of the session, in order, including the parts that failed. The
presentable statements are in `NOTE.md`; this file is the record of how they
were reached and of the wrong turns.

## 1. How the problem was chosen

The survey (three external candidates, an internal-thread audit; details in
`log/2026-09-16-nonrepetitive-lattices.md`) started from Tao's grid paper
(arXiv:2303.16237, `5 ≤ π(P_n□P_n) ≤ 12`), whose concluding question reads
"Is π(P_n□P_n) > 5 for large n? ... Can this approach be further developed or
refined? Perhaps computers can help." That is an explicit invitation to a SAT
attack. Within twenty minutes a first encoding (all paths of at most 10
vertices on the 8×8 grid, 5 colours) returned UNSAT in 13 s, which would have
been `π(P□P) ≥ 6`.

The novelty check then found arXiv:2510.11263 (Tao, Zhang, Zhang, Toole,
October 2025): they had already proved `π(P□P) ≥ 6`, and also `π(P⊠P) ≥ 9`
and `π(T₃) ≥ 9`, by enumerating nonrepetitive colourings of growing patches.
So the 13-second result was a rediscovery, recorded as such. The session
retargeted on what that paper leaves open: its discussion says the method is
memory-bound and cannot deliver better bounds, so the next colour on each
lattice was the target, with an audit of their three tables as the natural
first step (their computation is the only support for two of the three
theorems).

## 2. Tooling

- python-sat 1.9 (CaDiCaL 1.5.3 for search; Glucose 4.2 for proof logging,
  since python-sat does not return CaDiCaL proofs). Kissat and CaDiCaL source
  archives on github.com are refused by the sandbox's egress policy; only
  raw.githubusercontent.com answers, which is how Heule's `drat-trim.c` was
  obtained and compiled. `rup_check` is the repository's own checker.
- Encoding: one-hot colours, equality variables `E_uv` forced true by equal
  colours, one clause per even path. Symmetry breaking: three colour-fixing
  clauses at the centre.
- The eager encoding (all paths up to length L) scales badly: the 10×10 grid
  with all paths of at most 12 vertices is 2.3 million clauses, and paths of 14
  vertices would be ten times that. The lazy loop (`nrsat.py` + `repcheck.c`)
  encodes short paths eagerly and adds only the repetitive paths that actual
  solver models exhibit. The 5-colour 7×7 instance went from 109 048 eager
  path clauses and 11 s to 906 lazy clauses and 1 s.
- Certification chain: `validate_nrsat.py` (independent re-derivation of every
  clause's meaning) → Glucose proof → drat-trim → rup_check. Witness chain:
  `brute_check.c`, which enumerates every simple path and tests the
  definition; it was written separately from `repcheck.c` on purpose.

## 3. What happened, in order

1. **Positive controls.** 4 colours: 5×5 grid with paths of ≤ 6 vertices UNSAT
   (consistent with Tao's hand proof of `π ≥ 5`). 5 colours: 8×8 with paths ≤ 8
   SAT, with paths ≤ 10 UNSAT (13 s). The lazy loop reproduces the UNSAT on the
   7×7 grid in 1 s, on the 41-vertex spiral in 1 s, and the 40-vertex spiral
   is SAT, exactly the death index in the paper's Table 1.
2. **Square grid, 6 colours (the original target).** 8×8 and 10×10 with paths
   up to 12 vertices: SAT within seconds. Lazy loop from paths ≤ 8 with
   repetitions up to 16 vertices on 10×10: 3 300 iterations, 653 000 clauses,
   230 s, no convergence (killed). Eager paths ≤ 12 plus lazy repetitions up to
   18 vertices on 10×10: SAT after 147 iterations (36 s); the colouring has
   repetitions of 20 and 24 vertices. Conclusion: a 6-colour contradiction, if
   reachable, needs long repetitions and probably a larger region. Parked.
3. **King's graph, 9 colours.** 6×6 with repetitions ≤ 10: SAT in 1 s. 8×8
   with all paths ≤ 6 eager: the first solve did not finish in 6 minutes
   (killed; the instance is near the boundary, which is interesting but not
   actionable today). 30-vertex spiral with repetitions ≤ 16: SAT. 7×7 run
   left in the background; see the log's Next section for its outcome.
4. **Triangular lattice, 9 colours.** 7×7 rhombus, repetitions ≤ 12: SAT.
   9×9 rhombus, repetitions ≤ 16: 3 million lazy clauses in 3 minutes and
   climbing (killed).
5. **Triangular lattice, 8 colours (the paper's `T₃` control).** This is where
   the session turned. The paper's Table 3 has zero 8-colourings at 23
   vertices. The 6×6 rhombus with repetitions ≤ 12, then ≤ 20, was SAT. The
   5×5 rhombus with all repetitions (≤ 24 vertices in a 25-vertex graph, so a
   complete check) was SAT. Suspecting an embedding mismatch (their Figure 1
   draws `T₃` with offset rows), `nrsat.py` was rewritten to take arbitrary
   patch shapes: rectangles, offset-row blocks, hexagons, the paper's spiral
   in both embeddings. The 5×5 offset block: SAT, complete check. The
   23-vertex spiral: SAT in both embeddings, complete check. Every witness was
   then verified by `brute_check.c` (0.12 to 0.9 billion directed simple
   paths each, zero repetitions). The 23-vertex spiral is inside the 5×5
   block for every convention, so Table 3's zero cannot be right for `T₃`.
6. **Counting replication.** `count_colourings.c` re-implements their
   algorithm with full colour canonicalisation. Square, 5 colours: death at 41
   as in Table 1, our counts below theirs by a factor rising from 1.25 to 2
   (their convention canonicalises only the initial four vertices). King, 8
   colours: our `n(20) = 186`, `n(21) = 278`, `n(22) = 32`, `n(23) = 0`
   against their `n(20) = 0`; SAT confirms (22 SAT with a brute-force-verified
   witness over 3.98 billion paths, 23 UNSAT). `T₃`, 8 colours: our counts
   exceed theirs from `i = 15` on in both embeddings, which is impossible for
   the same graph under their looser convention; the 25-vertex run was killed
   after 18 CPU-minutes when the SAT witnesses had already settled the point.
7. **Certificates.** Four UNSAT instances re-solved by Glucose with proof
   logging and checked twice: square spiral 41 / 5 colours (proof 62 807
   lines), king spiral 23 / 8 colours (740 087 lines; drat-trim's trimmed
   proof of 666 403 lines is the committed one, re-checked by rup_check; only
   5 107 of 43 838 clauses are in the core), `T₃` hexagon radius 2 / 6
   colours (4 946 lines), `T₃` hexagon radius 3 / 7 colours (2 605 263 lines,
   Glucose 198 s, drat-trim 234 s, rup_check 762 s). That proof is 170 MB
   (25 MB trimmed and gzipped), too large to commit. drat-trim reports only
   20 069 of the 265 459 clauses in the core, so the core was extracted
   (`drat-trim -c`), the structural clauses restored, the path list rebuilt
   by matching clauses back to their paths, and the 22 121-clause instance
   validated and re-solved: Glucose 77 s, but the proof is still 2.5 million
   lines. A short instance does not mean a short proof here; only the CNFs
   are committed and `certify.py` regenerates the proofs.
8. **Ladder on `T₃`.** 6 colours die on the 19-vertex hexagon in 0.1 s
   (`π(T₃) ≥ 7`); 7 colours die on the 37-vertex hexagon after 193 lazy
   iterations and 210 s (`π(T₃) ≥ 8`). 8 colours on the 37-vertex hexagon:
   SAT up to 16-vertex repetitions (1 901 iterations, 490 000 clauses, 33 s).
   8 colours on the 61-vertex hexagon with repetitions up to 20 vertices: 4.2
   million lazy clauses after 4 minutes and still growing when the write-up
   started; outcome in the log.

## 4. Mistakes and near-misses worth recording

- The first hour's "new theorem" was a rediscovery caught only by the
  literature search. The lesson is the standing one: search for the newest
  paper before believing a 13-second UNSAT.
- The first `T₃` control used a rhombus and repetitions of at most 12
  vertices, and its SAT verdict was briefly read as a bug in the encoder.
  Two independent checks (a complete-path SAT run and exhaustive enumeration)
  were needed before trusting it against a published table.
- `pkill -f` with a pattern that appears in the calling shell's own command
  line kills the shell; three tool calls died this way before a helper script
  was used.
- The lazy loop's greatest weakness is that a SAT verdict says nothing
  beyond the path bound; every SAT witness that is claimed as a colouring of a
  finite patch had to be checked exhaustively, which limits such claims to
  patches of about 25 vertices (billions of paths).

## 5. Publication paths

- Contact the authors of arXiv:2510.11263 (emails on the paper) with the
  three brute-force-verified 8-colourings of `T₃` patches and the 20- and
  22-vertex king witnesses: the concrete objects that contradict Tables 2 and 3.
- A short arXiv note (math.CO) with the certified bounds and the audit, if the
  authors do not amend; MSC 05C15, 05C85, 68R15.
- The `n(i)` sequences are not OEIS material (they depend on a vertex order).
