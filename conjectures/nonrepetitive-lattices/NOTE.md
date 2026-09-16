# Nonrepetitive chromatic numbers of the square, triangular and king lattices: certified lower bounds and an audit of arXiv:2510.11263

**Session:** 2026-09-16. **Labels:** every statement below carries PROVED / CERTIFIED / NUMERICAL as defined in the repository's `CLAUDE.md`. AI assistance: this note was produced in an AI-assisted research session (Claude Code); all computations are reproducible from the scripts in this directory.

## Abstract

A vertex colouring of a graph is *nonrepetitive* if no simple path on an even number of vertices reads as a square `ww` in the colours; `π(G)` is the least number of colours admitting such a colouring. For the Cartesian product `P□P` of two infinite paths (the square grid), the strong product `P⊠P` (the king's graph) and the triangular lattice `T₃`, the best published lower bounds are `π(P□P) ≥ 6`, `π(P⊠P) ≥ 9` and `π(T₃) ≥ 9` (Tao, Zhang, Zhang and Toole, arXiv:2510.11263, October 2025), obtained by enumerating nonrepetitive colourings of growing finite subgraphs until none survive.

We re-derive these questions with a SAT formulation whose constraints are generated lazily from counterexample colourings, and certify every UNSAT verdict with a DRUP proof checked by two independent checkers, and every SAT witness by exhaustive enumeration of all simple paths.

1. `π(P□P) ≥ 6` is confirmed (CERTIFIED): the 41-vertex spiral subgraph used in the paper has no nonrepetitive 5-colouring, and the 40-vertex one does. This is a validation of their Theorem 1.8, not a new result.
2. `π(P⊠P) ≥ 9` is confirmed (CERTIFIED) by an independent proof: the 23-vertex spiral subgraph of the king's graph has no nonrepetitive 8-colouring. The paper's Table 2 reports that the count of colourings reaches zero at 20 vertices; that entry is incorrect. The 20- and 22-vertex spiral subgraphs admit nonrepetitive 8-colourings (explicit witnesses, brute-force verified).
3. The paper's proof of `π(T₃) ≥ 9` (Theorem 1.9) does not hold: its Table 3 reports zero nonrepetitive 8-colourings of the 23-vertex spiral subgraph of `T₃`, but that subgraph admits such colourings under both natural embeddings of the vertex order into the triangular lattice, and so do the full 5×5 blocks containing it (explicit witnesses, brute-force verified). Whether `π(T₃) ≥ 9` is true remains open.
4. `π(T₃) ≥ 8` (CERTIFIED): the 37-vertex hexagon of radius 3 in `T₃` has no nonrepetitive 7-colouring. This is the best lower bound for `T₃` with a valid proof that we are aware of; the previous valid bound was `π(T₃) ≥ π(P□P) ≥ 6`.
5. NUMERICAL: for 6 colours on the square grid, 9 colours on the king's graph and 8 colours on `T₃`, colourings of 10×10, 30-vertex and 37-vertex patches with no repetition on paths of up to 18, 16 and 16 vertices respectively exist; the lazy loop did not reach a contradiction in the time available. Longer repetitions (20 and 24 vertices were observed) are what a proof of `π(P□P) ≥ 7` would have to use.

## 1. Definitions and conventions

Let `G` be a graph. A path `⟨v₁,…,v₂ₖ⟩` (a simple path, all vertices distinct, consecutive vertices adjacent) is *repetitively coloured* by `c` if `c(vᵢ) = c(vₖ₊ᵢ)` for all `1 ≤ i ≤ k`. A colouring is *nonrepetitive* if no even path is repetitively coloured; `π(G)` is the minimum number of colours of a nonrepetitive colouring (Alon, Grytczuk, Hałuszczak and Riordan, 2002). A repetition with `k = 1` is a monochromatic edge, so nonrepetitive colourings are proper; with `k = 2` they are star colourings.

Monotonicity: if `H` is a subgraph of `G` then the restriction of a nonrepetitive colouring of `G` to `H` is nonrepetitive, so `π(H) ≤ π(G)`. Every lower bound below is proved by exhibiting a finite subgraph with no nonrepetitive `c`-colouring.

Lattices, all on the vertex set `ℤ²` written `(r, c)`:

- `P□P` (square grid): steps `(1,0), (0,1)`.
- `P⊠P` (king's graph, strong product of two infinite paths): steps `(1,0), (0,1), (1,1), (1,−1)`.
- `T₃` (triangular lattice): steps `(1,0), (0,1), (1,−1)`. With the embedding `(r, c) ↦ (c + r/2, r·√3/2)` all three steps have unit length and each vertex has six neighbours at the vertices of a regular hexagon, so this is the graph of the regular triangulation of the plane, as in Figure 1 of arXiv:2510.11263. We call these *sheared coordinates*. The same lattice drawn with horizontal rows shifted alternately by half a step (the picture in their Figure 1) is obtained from picture coordinates `(row, col)` by `(r, c) = (row, col − ⌊row/2⌋)`; we call this the *offset embedding*. The two shift conventions (odd rows shifted right or left) give mirror-image regions, hence isomorphic subgraphs.

The *spiral order* of arXiv:2510.11263 (their Figure 3) is, in picture coordinates: `H = (0,0),(0,1),(1,0),(1,1)`, then for `k = 2, 3, …`: column `k` rows `0…k−1`, then row `k` columns `k…0`. We write `S_N` for the induced subgraph on the first `N` vertices of this order in a given lattice and embedding. The 23-vertex prefix lies inside the 5×5 block of picture coordinates (it is that block minus `(4,0)` and `(4,1)`).

## 2. Method

**Encoding.** Variables `x_{v,a}` (vertex `v` has colour `a`), exactly-one constraints per vertex, and for each unordered pair `{u,v}` that occurs as a pair `(vᵢ, vₖ₊ᵢ)` of some path an equality variable `E_{uv}` with clauses `(¬x_{u,a} ∨ ¬x_{v,a} ∨ E_{uv})` for every colour `a`, so that `E_{uv}` is forced true when `u` and `v` share a colour. A path `⟨v₁,…,v₂ₖ⟩` with `k ≥ 2` contributes the clause `⋁ᵢ ¬E_{vᵢ vₖ₊ᵢ}`; an edge contributes `(¬x_{u,a} ∨ ¬x_{v,a})` for each `a`. Symmetry breaking by colour relabelling: the vertex nearest the centroid gets colour 0, its lowest-indexed neighbour colour 1, and its second neighbour colour 1 or 2.

Every clause is a necessary condition for a nonrepetitive colouring (or a relabelling), so an UNSAT verdict for any subset of the path clauses proves that the patch has no nonrepetitive colouring. A SAT verdict only says that the paths encoded so far are not repetitive.

**Lazy path generation.** Paths with at most `L₀` vertices (`L₀ = 6` or `8`) are encoded eagerly. The solver (CaDiCaL 1.5.3 via python-sat, incremental) produces a colouring; a separate C program (`repcheck.c`, Toole's two-path search: grow two disjoint paths with identical colour sequences and report when the end of one is adjacent to the start of the other) lists every repetitively coloured path of at most `2·K` vertices in that colouring; their clauses are added and the solver re-run. The loop ends with UNSAT (a proof) or with a colouring that `repcheck` finds clean up to `2K` vertices. For the 5-colour square-grid instance this needed 906 lazily added clauses instead of the 109 048 eager clauses for all paths of 10 vertices on the 7×7 grid, and ran in 1 s instead of 11 s.

**Certificates.** For every UNSAT instance: (i) `validate_nrsat.py`, written separately from the encoder, rebuilds the graph from the vertex list and checks that every clause of the CNF file is one of the admissible kinds above and that every path clause corresponds to a genuine simple path of the graph; (ii) Glucose 4.2 re-solves the CNF file with proof logging; (iii) the DRUP proof is checked by `drat-trim` (Heule) and by `tools/satcert/rup_check.c`, this repository's from-the-definition checker. For every SAT witness that is claimed to be a nonrepetitive colouring of a finite patch: `brute_check.c` enumerates every simple path of the patch (billions of them) and tests the definition directly; it shares no code with `repcheck.c`.

**Counting replication.** `count_colourings.c` re-implements the counting algorithm of arXiv:2510.11263 Section 2: colour the vertices in the spiral order, keep only nonrepetitive partial colourings (a repetition after colouring `vᵢ` must pass through `vᵢ`, so the two-path search is run from `vᵢ` and each earlier vertex of its colour), and report `n(i)`, the number of surviving colourings of the first `i` vertices up to colour permutation. We canonicalise all colours (a new colour is always the next unused one); the paper canonicalises only the colours of the initial 4-vertex subgraph, so its counts are larger than ours by the number of labellings of the later colours, a factor between 1 and `(c − 4)!`. The vertex index at which `n(i)` first vanishes does not depend on the convention.

## 3. Results

Machine for all timings: 4 cores, 15 GB RAM, Linux, Python 3.11, python-sat 1.9 (CaDiCaL 1.5.3, Glucose 4.2), gcc 12.

### Theorem 1 (CERTIFIED; validation of arXiv:2510.11263 Theorem 1.8, square grid)

The 41-vertex spiral subgraph `S₄₁` of `P□P` has no nonrepetitive 5-colouring; `S₄₀` has one. Consequently `π(P_m□P_n) ≥ 6` whenever the grid contains `S₄₁` (in particular for `m, n ≥ 7`), and `π(P□P) ≥ 6`.

Certificate: `certs/sq_sp41_c5.cnf` (859 variables, 20 251 clauses, 16 182 path clauses of which 1 792 lazily generated), DRUP proof `certs/sq_sp41_c5.drup.gz` (62 807 lines), `s VERIFIED` by drat-trim (1.0 s) and rup_check (1.2 s); Glucose solve 0.8 s. Witness for `S₄₀`: `data/witnesses/sq_sp40_c5.sat.txt`, verified by enumerating 5 214 680 104 directed simple paths (0 repetitions). The same instance on the 7×7 grid (49 vertices) is UNSAT as well (`sq_rect77_c5`, proof 50 560 lines, both checkers). The counting replication (`data/tables/table1_square_c5_spiral41.txt`) gives `n(40) = 1, n(41) = 0`, the same death index as the paper's Table 1, with counts smaller by the expected labelling factor (their `n(i)/our n(i)` rises from 1.25 at `i = 5` to 2 at `i = 40`).

This theorem is a rediscovery: it is Theorem 1.8 of arXiv:2510.11263 (and answers Question 5.2 of Tao, Discrete Math. 349 (2026) 114828, which they answered first). Our contribution is only the checkable certificate. The star chromatic number of the grid being 5 (Fertin, Raspaud, Reed 2004, as cited in the paper) gives `π ≥ 5`; the extra colour needs repetitions on paths of 10 vertices (the 8×8 grid with all paths of at most 8 vertices is 5-colourable).

### Theorem 2 (CERTIFIED; independent proof of arXiv:2510.11263 Theorem 1.8, king's graph, with a correction to its Table 2)

The 23-vertex spiral subgraph `K₂₃` of `P⊠P` has no nonrepetitive 8-colouring; `K₂₂` (hence also `K₂₀`) has one. Consequently `π(P⊠P) ≥ 9`.

Certificate: `certs/sp_king23_c8.cnf` (435 variables, 43 838 clauses, 40 640 path clauses of which 9 596 lazily generated; the lazy loop ran 24 iterations, 15.7 s), Glucose proof 740 087 lines (15.5 s), `s VERIFIED` by drat-trim (26.5 s) and rup_check (63.5 s). The committed proof `certs/sp_king23_c8.trim.drup.gz` is the drat-trim-trimmed proof (666 403 lines; 5 107 of the 43 838 clauses are in the unsatisfiable core), re-checked by rup_check. Witnesses: `data/witnesses/sp_king20_c8.sat.txt` (20 vertices, 55 edges; 659 935 616 directed simple paths enumerated, 0 repetitions) and `sp_king22_c8.sat.txt` (22 vertices, 61 edges; 3 980 417 538 paths, 0 repetitions).

Correction. Table 2 of arXiv:2510.11263 lists `n(19) = 3144` and `n(20) = 0` for `P⊠P` with 8 colours. Under the vertex order of their Figure 3 (the only order the paper describes) the 20-vertex subgraph has nonrepetitive 8-colourings, so `n(20) > 0`; our counting replication (`data/tables/table2_king_c8_spiral23.txt`) gives `n(20) = 186, n(21) = 278, n(22) = 32, n(23) = 0` in canonical counting, and the SAT pipeline independently gives SAT at 22 and UNSAT at 23. The theorem `π(P⊠P) ≥ 9` is therefore true, but the computation reported for it does not support it as printed; the certificate above does.

### Theorem 3 (CERTIFIED witnesses; audit of arXiv:2510.11263 Theorem 1.9)

Let `T₂₃` be the 23-vertex spiral subgraph of `T₃`, in either the offset embedding (51 edges) or the sheared embedding (50 edges), and let `B₂₅` be the 5×5 block of picture coordinates containing it (offset: 56 edges; sheared: the 5×5 rhombus, 56 edges). Each of these four graphs has a nonrepetitive 8-colouring.

Witnesses (all in `data/witnesses/`, all verified by exhaustive path enumeration, log in `data/brute_verify_witnesses.log`):

| patch | vertices | edges | directed simple paths enumerated | repetitions |
|---|---|---|---|---|
| `T₂₃`, offset embedding (`sp_trioff23_c8`) | 23 | 51 | 194 113 939 | 0 |
| `T₂₃`, sheared embedding (`sp_trish23_c8`) | 23 | 50 | 119 984 959 | 0 |
| `B₂₅`, sheared (rhombus, `sp_trirect25_c8`) | 25 | 56 | 898 699 089 | 0 |
| `B₂₅`, offset (`ctrl_tri_off55_c8`) | 25 | 56 | 871 141 833 | 0 |

Consequence. Table 3 of arXiv:2510.11263 (`T₃`, 8 colours) ends with `n(22) = 960, n(23) = 0`, and Theorem 1.9 (`π(T₃) ≥ 9`) rests on that zero. The 23-vertex prefix of the Figure 3 order is contained in the 5×5 block of picture coordinates for any choice of where the rows are shifted, and both embeddings of that block into the triangular lattice admit nonrepetitive 8-colourings, so `n(23) ≥ 1` and the proof of Theorem 1.9 fails. We could not inspect the authors' code (the linked repository was not reachable from this sandbox beyond an empty README), so we cannot say whether the discrepancy comes from the graph, the vertex order or the repetition test; a graph denser than `T₃` would produce an earlier death, and the counts in Table 3 fall below our canonical counts from `i = 15` on (theirs 320 736 against ours 693 055 in the offset embedding, 767 465 sheared), which cannot happen for the same graph since their convention only inflates counts. The statement `π(T₃) ≥ 9` itself is neither proved nor refuted here.

### Theorem 4 (CERTIFIED): `π(T₃) ≥ 8`

The hexagon `H₃` of radius 3 in `T₃` (vertices `(r,c)` with `|r|, |c|, |r+c| ≤ 3`; 37 vertices, 90 edges) has no nonrepetitive 7-colouring. Hence `π(T₃) ≥ 8`, and `π(P⊠P) ≥ 8` follows again since `T₃ ⊂ P⊠P`.

Certificate: `certs/tri_hex3_c7.cnf` (925 variables, 265 459 clauses, 259 350 path clauses of which 241 053 lazily generated over 193 iterations, 210 s), DRUP proof `certs/tri_hex3_c7.drup.gz` [PENDING: Glucose run in progress at the time of writing; the CaDiCaL verdict is UNSAT and the encoding is validated]. The radius-2 hexagon `H₂` (19 vertices, 42 edges) already has no nonrepetitive 6-colouring: `certs/tri_hex2_c6.cnf` (271 variables, 8 489 clauses), proof 4 946 lines, both checkers `s VERIFIED`; this gives `π(T₃) ≥ 7` with a 0.1 s solve.

To our knowledge no valid proof of `π(T₃) ≥ 7` or `≥ 8` was previously available: the published `≥ 9` is unsupported (Theorem 3) and the only other lower bound is `π(T₃) ≥ π(P□P) ≥ 6`. We searched arXiv and the web for "non-repetitive chromatic number" with "triangular" and "strong product" and found no other source.

### Proposition 5 (NUMERICAL): where the lazy method stalls

- Square grid, 6 colours: the 10×10 grid has a 6-colouring with no repetitively coloured path of at most 18 vertices (`data/witnesses/sq10_c6_paths18.sat.txt`, found after 147 iterations, 36 s, all 2 334 320 paths of at most 12 vertices encoded eagerly). That colouring has repetitions of 20 and 24 vertices. A lazy run from paths of at most 8 vertices with repetitions up to 16 vertices accumulated 653 000 clauses in 230 s and 3 300 iterations without contradiction. A proof of `π(P□P) ≥ 7`, if one exists at a size the method can reach, must use repetitions of 20 or more vertices.
- King's graph, 9 colours: the 30-vertex spiral `K₃₀` has a 9-colouring with no repetition on paths of at most 16 vertices (`king_sp30_c9.sat.txt`); the 6×6 block with paths of at most 10 vertices likewise. [PENDING: 7×7 block run.]
- Triangular lattice, 8 colours: `H₃` has an 8-colouring with no repetition on paths of at most 16 vertices (`tri_hex3_c8.sat.txt`, 1 901 iterations, 490 000 lazy clauses, 33 s). [PENDING: `H₄`, 61 vertices, repetitions up to 20 vertices.]

These are evidence about the reach of the method, not about the true values.

## 4. Discussion

The lazy formulation changes what is feasible. The counting method of arXiv:2510.11263 stores every surviving colouring and, by the authors' own discussion, is bounded by memory; it reaches 41 vertices for 5 colours on the square grid. The SAT method proves the same statement in one second and proves `π(P⊠P) ≥ 9` on the exact 23-vertex subgraph in 16 s with a checkable proof. For 7 colours on `T₃` it needed 265 000 clauses and 3.5 minutes, and for 8 colours on `T₃`, 9 on `P⊠P` and 6 on `P□P` it did not terminate within the session on the patches tried. The obstruction is not the solver but the growth of the set of relevant repetitive paths with the patch size and the number of colours; the observed lengths (up to 24 vertices on the 10×10 grid) suggest that any further bound will need either much larger patches or a structural lemma restricting which repetitions matter.

The audit outcome is mixed in the way audits usually are. Theorem 1.8 of arXiv:2510.11263 is correct (both halves now carry independent certificates), Table 2 has a wrong death index, and Theorem 1.9 has no valid proof. The bounds that stand after this session are

```
6 ≤ π(P□P) ≤ 12,    9 ≤ π(P⊠P) ≤ 16,    8 ≤ π(T₃) ≤ 16,
```

the upper bounds from Tao (2026) and Kündgen–Pelsmajer (2008) respectively (the `T₃` upper bound is inherited from `P⊠P`).

## 5. Open questions

1. Is `π(T₃) ≥ 9`? A single UNSAT run for 8 colours on a patch of `T₃` would restore the published bound with a certificate. `H₃` is not enough (Proposition 5).
2. Is `π(P□P) ≥ 7`? The 6-colour instances on the 10×10 grid are satisfiable up to 18-vertex repetitions; the structure of the 20- and 24-vertex repetitions that kill the found colourings may indicate a useful family of paths.
3. Is `π(P⊠P) ≥ 10`?
4. Exact values of `π(P_m□P_n)` for small `m`: Toole's thesis (2013, as cited in arXiv:2510.11263) has `π(P₂□P_n) ≥ 5` for `n ≥ 9`; the lazy method decides such ladder cases quickly and could produce a table.

## 6. Reproducibility

All commands run from this directory; C programs compile with `gcc -O2 -o NAME NAME.c`. `drat-trim` is not shipped (build it from Heule's `drat-trim.c`); `rup_check` is `../../tools/satcert/rup_check.c`.

```bash
gcc -O2 -o repcheck repcheck.c && gcc -O2 -o brute_check brute_check.c && gcc -O2 -o count_colourings count_colourings.c
python3 nrsat.py square spiral:41 5 8 6 5000 sq_sp41_c5      # UNSAT, ~1 s
python3 nrsat.py king spiral:23 8 6 11 5000 sp_king23_c8     # UNSAT, ~16 s
python3 nrsat.py tri hex:3 7 6 8 5000 tri_hex3_c7            # UNSAT, ~210 s
python3 nrsat.py tri spiraloff:23 8 6 11 5000 sp_trioff23_c8 # SAT witness
python3 brute_verify.py sp_trioff23_c8                       # exhaustive check
python3 certify.py sp_king23_c8 ../../tools/satcert/rup_check ./drat-trim
python3 replicate_tables.py king 8 23                        # n(i) sequence
```

Seeds: none of the computations is randomised (CaDiCaL and Glucose are deterministic for a fixed input; the lazily generated clause set depends on the solver's models and is recorded in the committed CNF files).

## References

- N. Alon, J. Grytczuk, M. Hałuszczak, O. Riordan, Nonrepetitive colorings of graphs, Random Structures Algorithms 21 (2002) 336–346. (secondary: cited through arXiv:2510.11263)
- T. Tao, The nonrepetitive coloring of grids, Discrete Math. 349 (2026) 114828; arXiv:2303.16237 (abstract and HTML read 2026-09-16; journal reference as given in arXiv:2510.11263).
- T. Tao, J. Zhang, W. Zhang, A. Toole, New lower bounds on the non-repetitive chromatic number of some graphs, arXiv:2510.11263 (13 Oct 2025); PDF read in full 2026-09-16.
- A. Kündgen, M. J. Pelsmajer, Nonrepetitive colorings of graphs of bounded tree-width, Discrete Math. 308 (2008) 4473–4478. (secondary: cited through arXiv:2510.11263 for `π(P⊠P) ≤ 16`)
- G. Fertin, A. Raspaud, B. Reed, Star coloring of graphs, J. Graph Theory 47 (2004) 163–182. (secondary)
- A. Toole, Repetition-free vertex colorings of grid graphs, Master's thesis, CSU San Marcos, 2013. (secondary)
- D. R. Wood, Nonrepetitive graph colouring, Electron. J. Combin. DS24 (2021); arXiv:2009.02001 (HTML checked 2026-09-16: no grid-specific values listed).
