# Nonrepetitive chromatic numbers of the square, triangular and king lattices (Tao 2026; Tao–Zhang–Zhang–Toole 2025)

A colouring of a graph is nonrepetitive (Thue) if no simple path on an even
number of vertices reads as a square `ww` in the colours; `π(G)` is the least
number of colours. Thue's theorem is `π(path) = 3`. For the square grid `P□P`,
the king's graph `P⊠P` and the triangular lattice `T₃`, the published state is
`6 ≤ π(P□P) ≤ 12`, `9 ≤ π(P⊠P) ≤ 16` and `π(T₃) ≥ 9` (arXiv:2510.11263, which
enumerates nonrepetitive colourings of growing finite patches until none
survive, and says in its discussion that the method cannot go further). The
fault line: a SAT formulation with lazily generated path clauses reaches the
same finite patches in seconds with checkable proofs, so it can audit the
published tables and try the next colour.

**Status:** active
**Sessions:** 2026-09-16

## Results

| Claim | Label | Where |
|---|---|---|
| `π(P□P) ≥ 6`: the 41-vertex spiral patch has no nonrepetitive 5-colouring, the 40-vertex one does (rediscovery of arXiv:2510.11263 Thm 1.8, with a DRUP proof) | CERTIFIED | NOTE §3 Thm 1, `certs/sq_sp41_c5.*` |
| `π(P⊠P) ≥ 9`: the 23-vertex spiral patch of the king's graph has no nonrepetitive 8-colouring; the 20- and 22-vertex patches do, so Table 2 of arXiv:2510.11263 (`n(20) = 0`) is wrong while its theorem stands | CERTIFIED | NOTE §3 Thm 2, `certs/sp_king23_c8.*`, `data/witnesses/sp_king2{0,2}_c8.sat.txt` |
| The 23-vertex spiral patch of `T₃` and the 5×5 blocks containing it have nonrepetitive 8-colourings under both embeddings, so the published proof of `π(T₃) ≥ 9` (Thm 1.9, Table 3) fails; `π(T₃) ≥ 9` is open | CERTIFIED (witnesses, exhaustively checked) | NOTE §3 Thm 3, `data/witnesses/sp_tri*.sat.txt`, `data/brute_verify_witnesses.log` |
| `π(T₃) ≥ 8`: the radius-3 hexagon (37 vertices) has no nonrepetitive 7-colouring; the radius-2 hexagon has no 6-colouring | CERTIFIED | NOTE §3 Thm 4, `certs/tri_hex3_c7.*`, `certs/tri_hex2_c6.*` |
| Counting replication: death indices 41 (square, 5 colours) and 23 (king, 8 colours) in the paper's vertex order; no death by 25 vertices for `T₃` with 8 colours | CERTIFIED (exact enumeration, cross-checked by SAT) | `data/tables/` |
| 6 colours on the 10×10 grid, 9 on a 30-vertex king patch, 8 on the 37-vertex `T₃` hexagon: colourings with no repetition on paths of ≤ 18 / 16 / 16 vertices; longer repetitions (20, 24) present | NUMERICAL | NOTE §3 Prop 5, `data/witnesses/` |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `nrsat.py LATTICE SHAPE C LBASE KMAX [cap] [tag]` | lazy-path SAT search for a nonrepetitive `C`-colouring of a lattice patch; writes `tag.cnf/.paths/.verts` on UNSAT, `tag.sat.txt` on SAT | 1 s to minutes | UNSAT for `square spiral:41 5`, `king spiral:23 8`, `tri hex:3 7` |
| `repcheck.c` | lists all repetitively coloured paths of ≤ 2K vertices in a colouring (two-path search); called by `nrsat.py` | ms | |
| `brute_check.c`, `brute_verify.py TAG..` | from-the-definition check of a witness: enumerates every simple path | seconds to minutes (10⁹ paths) | all ten committed witnesses pass |
| `validate_nrsat.py TAG` | independent check that every clause of a committed CNF is a necessary condition for a nonrepetitive colouring | seconds | VALID for all four certificates |
| `certify.py TAG [rup_check] [drat-trim]` | validator + Glucose 4.2 proof logging + drat-trim + rup_check | 1 s to 5 min | `s VERIFIED` twice per certificate |
| `count_colourings.c`, `replicate_tables.py LAT C N` | replicates the counting algorithm of arXiv:2510.11263 §2 in the Figure 3 spiral order (`LAT` in square, king, tri-off, tri-sh) | seconds | `data/tables/*.txt` |

Run from inside this directory:

```bash
cd conjectures/nonrepetitive-lattices
gcc -O2 -o repcheck repcheck.c && gcc -O2 -o brute_check brute_check.c && gcc -O2 -o count_colourings count_colourings.c
gcc -O2 -o rup_check ../../tools/satcert/rup_check.c
python3 nrsat.py king spiral:23 8 6 11 5000 sp_king23_c8      # UNSAT in ~16 s
python3 nrsat.py tri spiraloff:23 8 6 11 5000 sp_trioff23_c8  # SAT: an 8-colouring
python3 brute_verify.py sp_trioff23_c8                        # exhaustive check
python3 certify.py sp_king23_c8 ./rup_check /path/to/drat-trim
```

Needs `python-sat` (pip) and a C compiler; `drat-trim` is Heule's single C file.

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `certs/sq_sp41_c5.{cnf,paths,verts,drup.gz}` | `nrsat.py`, `certify.py` | 41-vertex square spiral, 5 colours: UNSAT, proof 62 807 lines, drat-trim and rup_check verified |
| `certs/sp_king23_c8.{cnf,paths,verts,trim.drup.gz}` | same | 23-vertex king spiral, 8 colours: UNSAT, trimmed proof 666 403 lines (full proof 740 087 lines also verified) |
| `certs/tri_hex2_c6.*`, `certs/tri_hex3_c7.*` | same | `T₃` hexagons of radius 2 (6 colours) and 3 (7 colours): UNSAT with verified proofs |
| `data/witnesses/*.sat.txt` | `nrsat.py` | colourings (`r c colour` per line); those named in NOTE Thms 1–3 are exhaustively verified nonrepetitive, the rest are NUMERICAL (paths bounded) |
| `data/brute_verify_witnesses.log` | `brute_verify.py` | path counts and verdicts for the audit witnesses |
| `data/tables/*.txt` | `replicate_tables.py` | canonical counts `n(i)` in the paper's vertex order |

## Known defects and open threads

- The proofs are single-solver (Glucose 4.2) but checked by two independent checkers; the CaDiCaL verdicts of the lazy loop are not proof-logged (python-sat does not expose CaDiCaL proofs), so every UNSAT instance is re-solved from the CNF file by Glucose for the certificate.
- The authors' code (github.com/WentaoZhangT-Zero/Nonrepetitive) could not be read from the sandbox, so the cause of the Table 2 and Table 3 discrepancies is not identified; the audit rests on the vertex order the paper describes (Figure 3) and both natural embeddings of it into `T₃`.
- Sharpest open question: is `π(T₃) ≥ 9`? An UNSAT run for 8 colours on some patch would restore the published bound; the 37-vertex hexagon is not enough. Then `π(P□P) ≥ 7` (repetitions of 20+ vertices needed) and `π(P⊠P) ≥ 10`.

## Prior work

Thue (1906): `π(P) = 3`. Alon–Grytczuk–Hałuszczak–Riordan (2002) introduced `π(G)`. Kündgen–Pelsmajer (2008): `π(P⊠P) ≤ 16` (secondary, via arXiv:2510.11263). Fertin–Raspaud–Reed (2004): star chromatic number of the grid is 5, so `π(P□P) ≥ 5` (secondary). Tao, Discrete Math. 349 (2026) 114828 (arXiv:2303.16237): `5 ≤ π(P□P) ≤ 12`, asked whether 5 is tight and whether computers can help. Tao–Zhang–Zhang–Toole, arXiv:2510.11263 (Oct 2025): `π(P□P) ≥ 6`, `π(P⊠P) ≥ 9`, `π(T₃) ≥ 9` by enumeration; Theorem 1 here is a rediscovery of the first, Theorem 2 an independent certificate of the second, Theorem 3 an audit finding that the third is unproved. Wood's dynamic survey (EJC DS24, 2021) lists no grid-specific values.
