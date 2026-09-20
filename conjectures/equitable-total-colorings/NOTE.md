# The smallest Type 1 cubic graphs with no equitable 4-total colouring

Research note, hedge computation of the 2026-09-08 session (run by an AI subagent on
one core, ≈ 61 min; re-checked by the session lead on one counterexample with the
SAT-free enumerator). AI-assisted (Claude).

## 1. Definitions, as read from arXiv:2609.05259

The paper (Adauto, de Figueiredo, Sasaki, Schneider, "Equitable total colorings of
cubic graphs", 4 Sep 2026) uses, verbatim:

* "A k-total coloring of a graph G assigns one of k colors to each vertex and each
  edge of G in such a way that adjacent vertices, adjacent edges, and any vertex and edge
  that are incident receive distinct colors. The least k for which G admits a k-total
  coloring is the total chromatic number χ′′(G)."
* "Graphs with χ′′(G) = ∆(G) + 1 are said to be Type 1, and graphs with
  χ′′(G) = ∆(G) + 2 are Type 2 […] every cubic graph is either Type 1 (χ′′ = 4) or
  Type 2 (χ′′ = 5)."
* "A k-total coloring is equitable if the cardinalities of any two of its color classes
  differ by at most one, and the equitable total chromatic number χ′′_e(G) is the least
  k for which G admits an equitable k-total coloring." The classes are counted over all
  `5n/2` elements (paper §2).
* "every graph G is simple, finite, and cubic (3-regular) unless stated otherwise."
* **Question 7.1.** "Does every Type 1 cubic graph of order less than 20 admit at least
  one equitable 4-total coloring? Equivalently, is R a Type 1 cubic graph with
  χ′′_e = 5 of minimum order?" The paper adds that "the question is within reach of a
  systematic computational verification over the catalogue of connected cubic graphs of
  order at most 18 [3], for instance through integer programming or SAT formulations",
  and reduces to connected graphs: "if each component has an equitable 4-total
  coloring, then the colors can be independently permuted in the components so that
  […] the resulting 4-total coloring is equitable."

`R` (Dantas et al., [5] in the paper) is a Type 1 cubic graph of order 20 with
`χ′′_e(R) = 5`, given in the paper only as Figure 1.

## 2. Method

**Generation.** All connected cubic graphs of order `n = 4, 6, …, 18` from nauty 2.8.8
(`geng -c -d3 -D3 n`, built from the pynauty source distribution because GitHub is
blocked from the sandbox). Counts 1, 2, 5, 19, 85, 509, 4060, 41301 agree with OEIS
A002851 (fetched live) and with the paper's total of 45 982.

**Encoding** (`code/tc.py`). One Boolean variable per (element, colour), elements being
the `n` vertices and `3n/2` edges. Clauses: exactly one colour per element; for every
edge `uv` and colour `c`: `¬x_{u,c} ∨ ¬x_{v,c}`, `¬x_{uv,c} ∨ ¬x_{u,c}`,
`¬x_{uv,c} ∨ ¬x_{v,c}`; for every vertex, every pair of its incident edges and every
colour: `¬x_{e,c} ∨ ¬x_{f,c}`. The equitable instance adds, per colour,
`⌊N/4⌋ ≤ Σ_i x_{i,c} ≤ ⌈N/4⌉` with `N = 5n/2` (python-sat sequential counters). An
optional symmetry-breaking prefix fixes vertex 0 to colour 0 and its three edges to
colours 1, 2, 3 (sound: these four elements are pairwise adjacent or incident, so every
colouring can be permuted to this form, and permutations preserve class sizes); every
certified UNSAT below also has a proof *without* it.

**Verification.** Every satisfying assignment is decoded and checked by
`code/verify_tc.py`, written from the definition (all elements coloured, endpoints
differ, edge differs from both endpoints, incident edges pairwise distinct, class sizes
counted over all elements; negative controls rejected). Every UNSAT verdict that the
result depends on carries a DRUP proof from Glucose 4, checked by the repository's
from-the-definition checker `tools/satcert/rup_check` (negative controls: a truncated
proof and a proof with a bogus clause are rejected). Independently, `code/brute.py` is a
SAT-free backtracking enumerator of all 4-total colourings (proper vertex colourings in
canonical colour order, then compatible edge colourings, with the definition-derived
bounds `v_i ≤ |c_i| ≤ (n+v_i)/2` when restricted to equitable ones).

**Controls** (`code/controls.py`): K4, K3,3, the Möbius ladders M8–M14 and L10 are
Type 2; L6, L8, L12, L14, L18, Petersen, G(6,2), G(9,2) and the paper's H16, H18 are
Type 1 with equitable colourings of exactly the configurations the paper states
(L6: (4,4,4,3), H16: (10,10,10,10), H18: (12,11,11,11)); the four certificates in the
paper's appendix verify. `R` was reconstructed from Figure 1 (four K_{2,3} gadgets
with poles coloured 4, wired Top.L–Left.R, Top.R–Right.L, Top.C–Bottom.C,
Left.C–Right.C, Left.L–Bottom.L, Right.R–Bottom.R; graph6
`S]o??KEH_???AB?J?@_?????@?W_?o?@o`): the transcribed Figure-1 colouring is a valid
4-total colouring with configuration (14,12,12,12), and the equitable instance is UNSAT
with checked proofs (1 314 and 8 198 lines). Caveat: two outer ports are clipped in the
figure (their colours are forced); isomorphism with the graph of Dantas et al. was not
verified.

## 3. Results (CERTIFIED as stated in §4)

| n | connected cubic | Type 1 | Type 2 | Type 1 with an equitable 4-total colouring | Type 1 with χ''_e = 5 |
|---|---|---|---|---|---|
| 4 | 1 | 0 | 1 | 0 | 0 |
| 6 | 2 | 1 | 1 | 1 | 0 |
| 8 | 5 | 4 | 1 | 4 | 0 |
| 10 | 19 | 9 | 10 | 9 | 0 |
| 12 | 85 | 60 | 25 | 60 | 0 |
| 14 | 509 | 461 | 48 | 461 | 0 |
| 16 | 4060 | 3833 | 227 | 3817 | **16** |
| 18 | 41301 | 39198 | 2103 | 39191 | **7** |

**Theorem 3.1 (CERTIFIED).** Question 7.1 has a negative answer. Exactly 23 connected
Type 1 cubic graphs of order less than 20 admit no equitable 4-total colouring: 16 of
order 16 and 7 of order 18 (three of them bipartite). Every Type 1 cubic graph of order
at most 14 admits an equitable 4-total colouring. The minimum order of a Type 1 cubic
graph with `χ''_e = 5` is 16; `R` is not of minimum order.

The 23 graphs (graph6, as generated): order 16 —
`O???CB?wB@F?@o@oB_?s?` `O???CB?oR@BGM?D_@o@K?` `O???CB?gGwB_S_Q_CW@I?`
`O???C@_[F?P_E_E_?w?J?` `O???C@_FAoF?w?`_?w?F?` `O???C@_cSoAgB_B_KOB@?`
`O???C@_cSQAoD_R?DOB@?` `O???C@_cSQBC[?P_@o@K?` `O???C@_oJABGe?D_Co?[?`
`O???C@_WN?R?EO@oAo?[?` `O???C@_cN?L?B_B_Ag?e?` `O???C@_cKaHGY?B_Ao@K?`
`O???C@_SN?PGEOD_Co?[?` `O??CA?_sF?D_EGBG?w?e?` `O??CA?_sF?DCEGF??w?M?`
`O??CA?oB@oE_b?OWGWCC_`; order 18 — `Q??????wF?R?U?D_?w?L?AW?`_?`
`Q??????wF?R?T?E_Co?F?@W?H_?` `Q??????wE_P_W_IO@g?L?CW?Q_?` (bipartite)
`Q????A?oB_M?aGHGB_?M??s?J??` `Q????A?WE_[?J?E_B_?J??w?BO?` `Q????A?WB_L?F?E_OECB?@o?F??`
`Q???C@?GE_X?D_D_Ca@O_AW?B_?`. Invariants of the order-16 ones: all non-bipartite,
girth 3 or 4, fourteen 2-connected and two with a bridge, automorphism groups of order
2, 4, 8 or 16; not all contain K_{2,3}.

**Proposition 3.2 (CERTIFIED, SAT-free).** Each order-16 counterexample has between 16
and 240 4-total colourings up to colour permutation (64, 240, 80, 40, 24, 96, 96, 32,
96, 64, 48, 28, 116, 28, 16, 96 in the order above), every one with class configuration
(11,10,10,9) — consistent with the paper's Theorem 5.3, which allows only (10,10,10,10)
and (11,10,10,9) at order 16. The order-18 counterexamples' plain witnesses have
configuration (12,12,11,10).

**Order 20 (partial).** Three of the ten `geng` residue classes (161 130 graphs) contain
20 further Type 1 graphs with `χ''_e = 5`, all with configuration (14,12,12,12) like
`R`, none isomorphic to `R` (whose class was not scanned); each verdict is certified as
in §4, the census is incomplete.

## 4. What exactly is certified

* SAT side: all 43 543 equitable witnesses and the 23 plain witnesses (`n ≤ 18`) were
  verified by `verify_tc.py` (the scan aborts on any rejection; none occurred). They were
  not stored; `scan.py` regenerates them in 411 s.
* UNSAT side: DRUP proofs checked by `rup_check` for the equitable instances of all 23
  counterexamples, with and without symmetry breaking (46 proofs, committed in
  `certs/proofs_counterexamples/`), for `R` (2 proofs, committed), for the 2 416 Type 2
  plain instances with and without symmetry breaking (4 832 proofs, 520 MB, manifests
  committed, files regenerable with `post.sh`), and for the 20 order-20 examples (40).
* SAT-free cross-checks (`brute.py`): 0 equitable colourings for all 23 counterexamples
  and for 3 of the order-20 ones; all colourings of the 16 order-16 graphs enumerated;
  0 colourings for all 86 Type 2 graphs of order ≤ 14; equitable colourings found for
  30 sampled Type 1 graphs.
* The session lead re-ran `brute.py` on the first order-16 counterexample: 0 equitable
  colourings, 64 colourings in total, all (11,10,10,9).
* Not certified: Type 2 verdicts at order 20; the seven unscanned residue classes at
  order 20; the isomorphism of the reconstructed `R` with the published one.

## 5. Open threads

1. Priority: check Adauto's dissertation and Stemock's work for these 23 graphs before
   any claim of novelty; then report the answer to the authors of arXiv:2609.05259.
2. Complete the order-20 census (≈ 1.5 h more on one core at the measured rate) and
   determine the full list of `χ''_e = 5` graphs of order 20, including `R`.
3. Do the order-18 counterexamples admit (12,12,12,9) colourings? (Not examined.)
4. A structural characterisation of the 23 graphs (bridges, K_{2,3} gadgets) in the
   spirit of the paper's Section 5.
