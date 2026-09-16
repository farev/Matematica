# PAGE.md — handoff for the site page `fabianarevalo.com/nonrepetitive-lattices`

New page (no page exists for this conjecture).

## 1. Headline claim

`π(T₃) ≥ 8` for the triangular lattice, CERTIFIED (the 37-vertex hexagon of radius 3 has no nonrepetitive 7-colouring, DRUP proof checked by drat-trim and by the repository's own checker), and an audit of arXiv:2510.11263: its `π(P⊠P) ≥ 9` is confirmed with an independent certificate, but its `π(T₃) ≥ 9` has no valid proof because the 23-vertex patch its table declares uncolourable admits nonrepetitive 8-colourings (explicit, exhaustively checked).

## 2. Contributions

1. CERTIFIED: `π(P□P) ≥ 6`, rediscovering Theorem 1.8 of arXiv:2510.11263 with a checkable proof: the 41-vertex spiral patch of the square grid has no nonrepetitive 5-colouring (859 variables, 20 251 clauses, proof 62 807 lines, both checkers `s VERIFIED`); the 40-vertex patch has one (witness checked over 5 214 680 104 directed simple paths). Mark plainly as a rediscovery.
2. CERTIFIED: `π(P⊠P) ≥ 9` by an independent proof: the 23-vertex spiral patch of the king's graph has no nonrepetitive 8-colouring (435 variables, 43 838 clauses, proof 740 087 lines, trimmed 666 403, both checkers). Table 2 of the paper reports the count reaching zero at 20 vertices; the 20- and 22-vertex patches do have nonrepetitive 8-colourings (witnesses checked over 659 935 616 and 3 980 417 538 paths), and the exact death index in their vertex order is 23 (independent enumerator: `n(22) = 32`, `n(23) = 0`).
3. CERTIFIED witnesses: the 23-vertex spiral patch of `T₃`, under both natural embeddings of the paper's vertex order (offset rows as in their Figure 1, and sheared coordinates), and the two 5×5 blocks containing it, all admit nonrepetitive 8-colourings (paths enumerated: 194 113 939; 119 984 959; 898 699 089; 871 141 833; zero repetitions). Hence Table 3's `n(23) = 0` is wrong and Theorem 1.9 (`π(T₃) ≥ 9`) is unproved. Not refuted: `π(T₃) ≥ 9` remains open.
4. CERTIFIED: `π(T₃) ≥ 8` (37-vertex hexagon, 7 colours, 925 variables, 265 459 clauses, Glucose 198 s, proof 2 605 263 lines) and `π(T₃) ≥ 7` (19-vertex hexagon, 6 colours, proof 4 946 lines). Previously the only valid bound was `π(T₃) ≥ π(P□P) ≥ 6`.
5. NUMERICAL: the 10×10 grid has a 6-colouring free of repetitions on paths of ≤ 18 vertices (but with 20- and 24-vertex repetitions); a 30-vertex king patch has a 9-colouring free up to 16-vertex paths; the 37-vertex `T₃` hexagon has an 8-colouring free up to 16-vertex paths. These say where the method stalls, nothing about the true values.

Bounds after the session: `6 ≤ π(P□P) ≤ 12`, `9 ≤ π(P⊠P) ≤ 16`, `8 ≤ π(T₃) ≤ 16`.

## 3. Figures

1. **The 23-vertex triangular patch with its 8-colouring** (data: `data/witnesses/sp_trioff23_c8.sat.txt`, lines `r c colour`; embed with `x = c + r/2, y = r·√3/2`; draw all lattice edges among the 23 vertices, colour the discs, and outline the 5×5 offset block it sits in). Sentence the reader should say: "This is the patch the paper says cannot be 8-coloured without a repeated colour pattern along some path, and here is an 8-colouring of it that has none."
2. **The three spirals and their death indices** (data: `data/tables/table1_square_c5_spiral41.txt`, `table2_king_c8_spiral23.txt`, `table3_tri_offset_c8_spiral16.txt`; plot `n(i)` on a log scale against `i`, marking the paper's claimed death indices 41, 20, 23). Sentence: "Our counts die at 41 and 23 where the paper says 41 and 20, and for the triangular lattice they are still growing at 16 where the paper's are already falling."
3. **The lazy loop at work** (data: iteration logs are not committed; use the numbers in NOTE §3 Thm 4: 193 iterations, 241 053 lazy clauses out of 259 350 path clauses for the 37-vertex hexagon, 210 s). Optional; only if a bar chart of eager versus lazy clause counts (109 048 vs 906 for the 5-colour 7×7 grid) reads at a glance. Sentence: "Almost all path constraints are never needed; the solver's own wrong answers tell you which ones are."

## 4. Caveats the page must carry

- Contribution 1 is a rediscovery of a published theorem; the page must say so in the first sentence about it.
- Contribution 3 refutes a proof, not a statement: `π(T₃) ≥ 9` may still be true. The page must not say the theorem is false.
- The audit assumes the vertex order described in the paper (Figure 3) and considers both natural embeddings into `T₃`; the authors' code was not readable from the sandbox, so the source of their error is unidentified. The 5×5-block witnesses cover every placement of that order inside a 5×5 block.
- Every citation of Kündgen–Pelsmajer (2008), Fertin–Raspaud–Reed (2004), Alon et al. (2002) and Toole's thesis is secondary, taken from arXiv:2510.11263; Tao's journal reference (Discrete Math. 349 (2026) 114828) is as printed in that paper's bibliography.
- The proofs are produced by one solver (Glucose 4.2) but checked by two independent checkers; the exploratory verdicts (CaDiCaL) carry no proofs and are not relied on. The proof for the headline `π(T₃) ≥ 8` instance (2.6 million lines) is too large for the repository and is regenerated from the committed CNF by `certify.py` (about four minutes); the page should say the certificate is reproducible rather than downloadable.
- NUMERICAL items are bounded-path colourings only; none of them is a nonrepetitive colouring of its patch.

## 5. Existing page

None.
