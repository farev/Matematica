# Chromatically constrained multicolour Ramsey numbers F(j,k) (Sawin, 2026)

Colour the edges of K_n with k colours so that every colour class is
triangle-free **and** vertex j-colourable; F(j,k) is the largest possible n
(Will Sawin, [MathOverflow 513849](https://mathoverflow.net/q/513849),
2 Aug 2026). Trivially F(j,k) ≤ j^k; Sawin shows F(2,k) = 2^k and asks whether
lim_k F(j,k)/j^k = 0 for some j; Fabius Wiesner conjectures
F(j,k) ≥ Σ_{i≤j} S(k+1,i). The problem looked tractable because the first
open cells are small SAT instances in the "type" formulation (vertices are
distinct points of [j]^k, an edge may only take a coordinate where its
endpoints differ, no monochromatic triangle), and because the j = 3 case of
Wiesner's formula, (3^k+1)/2, is the size of a natural set of ternary words.

Write-up page: fabianarevalo.com/chromatic-ramsey (pending; see `PAGE.md`).

**Status:** active
**Sessions:** 2026-09-06

## Results

| Claim | Label | Where |
|---|---|---|
| F(3,k) ≥ C(k,t)·2^{k−t} for all t, hence ≥ 3^k/(k+1) and ~ 3^k·3/(2√(πk)); lim F(3,k)^{1/k} = 3 (previous rate 2^{3/2}) | PROVED | NOTE §3, `antichain.py` + `verify_colouring.c` (checked to K_1792, 8 colours) |
| F(j,k) ≥ j^k/(2k+2)^{d_j}, so lim F(j,k)^{1/k} = j — unconditional for j ≤ 4 | PROVED | NOTE §4 (Theorem 4.2, Lemma 4.3, Corollary 4.4); j ≥ 5 uses the OpenAI/Alon et al. saturated-map lemma (secondary) |
| F(j,k+l) ≥ F(j,k)F(j,l); lim F(j,k)/j^k exists; F(j,k) ≤ 2j^{k−1} | PROVED (folklore-level) | NOTE §2 |
| F(3,3) = 14 | CERTIFIED | witnesses (three, verified) + DRUP proof `certs/F33_n15.*` checked by `rup_check` |
| F(3,4) = 41 PENDING_F34 | CERTIFIED | witnesses; upper bound PENDING_F34_UPPER |
| F(3,5) ≥ 122; F(3,6) PENDING_F36 | CERTIFIED | `data/witnesses/col_even0_k5.txt`, `circ_122_5_3.json` |
| F(4,3) = 16, F(4,4) ≥ 44 | CERTIFIED (+ Greenwood–Gleason for ≤ 16) | `witness2_F4_3_n16.txt`, `circ_44_4_4.json` |
| No circulant witness for F(4,4) ≥ 45; no circulant triangle-free 4-colouring of K_46, K_50, K_51 | CERTIFIED (SAT UNSAT, no proof file) | `circ_sat.py` |
| The even-weight set E_k is colourable for k ≤ 5 (odd set for k ≤ 4); extremal 14-sets of [3]^3 form 37 orbits | CERTIFIED | `fixed_sat.py`, `enum_extremal.py` |
| Antichain palette constructions cannot exceed max_t C(k,t)2^{k−t} (LYM) | PROVED | NOTE Remark 3.2 |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `code/fjk_sat.py j k n` | SAT: is F(j,k) ≥ n? (type formulation, CaDiCaL) | 0.1 s at (3,3,15); 0.2 s at (3,4,41) | witness file |
| `code/fjk_sat2.py j k n [--cnf f]` | same with implied subcube bounds as cardinality constraints; DIMACS export | | |
| `code/fixed_sat.py k parity` | colour the even/odd-weight set E_k / O_k | 2.7 s at k = 5 | `col_even*_k*.txt` |
| `code/circ_sat.py n k j [out.json]` | circulant witnesses on Z_n with explicit proper colourings | < 5 s for n ≤ 122 | `circ_*.json` |
| `code/antichain.py K t out.bin` | the Theorem 3.1 construction, dense matrix | seconds | input to the verifier |
| `code/blockconstruct.py K t s base out.bin` | the Theorem 4.2 step r = 3 → 4 with the (3,2) gadget | seconds | input to the verifier |
| `code/saturated.py H s` | SAT for saturated map pairs | instant for (3,2); (4,3) not solved in 5 min | the gadget in NOTE §4 |
| `code/enum_extremal.py j k n` | all n-point colourable vertex sets, orbits under S_j ≀ S_k | 8 min at (3,3,14) | 33,831 sets / 37 orbits; `reps_3_3_14.json` |
| `code/cube42.py reps.json [--prove]` | cube-and-conquer F(3,4) ≤ 41 (one cube per extremal 14-set orbit) | PENDING_CUBE_TIME | PENDING_F34_UPPER |
| `code/sym_cyc.py k`, `sym_search.py k` | colourings invariant under the global swap / cyclic shift | seconds | `col_sym_k3.txt` |
| `code/tower.py`, `tower2.py`, `induct.py` | failed attempts at an inductive rule (kept as the record of what does not work) | minutes | see WRITEUP |
| `code/verify_witness.py`, `verify_circulant.py`, `verify_colouring.c` | from-definition checkers (no solver, no shared code) | ≤ 2 s | "VERIFIED …" |
| `code/inspect_witness.py w k` | layer / line / plane profile of a witness | instant | |

Run from inside this directory:

```bash
cd conjectures/chromatic-ramsey/code && python3 fjk_sat.py 3 3 15      # UNSAT in 0.1 s
python3 fjk_sat.py 3 4 41 && python3 verify_witness.py witness_F3_4_n41.txt
python3 circ_sat.py 122 5 3 w.json && python3 verify_circulant.py w.json
gcc -O2 -o verify_colouring verify_colouring.c && python3 antichain.py 8 3 ac.bin && ./verify_colouring ac.bin
gcc -O2 -o rup_check ../../../tools/satcert/rup_check.c && ./rup_check ../certs/F33_n15.cnf ../certs/F33_n15.drup
```

Requires python-sat (`pip install python-sat`); everything else is the
standard library and gcc.

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/witnesses/witness_F3_3_n14.txt`, `witness_F3_4_n41.txt`, `witness2_F4_3_n16.txt` | `fjk_sat.py` / `fjk_sat2.py` | type witnesses for F(3,3) ≥ 14, F(3,4) ≥ 41, F(4,3) ≥ 16 |
| `data/witnesses/col_even0_k{2,3,4,5}.txt`, `col_even1_k{2,3,4}.txt` | `fixed_sat.py` | colourings of E_k (sizes 5, 14, 41, 122) and O_k (4, 13, 40) |
| `data/witnesses/circ_{5_2_3,14_3_3,41_4_3,122_5_3,44_4_4}.json` | `circ_sat.py` | circulant witnesses with explicit proper colourings |
| `data/witnesses/col_sym_k3.txt` | `sym_cyc.py` | Z_2 × Z_3-invariant colouring of E_3 |
| `data/reps_3_3_14.json` | `enum_extremal.py` | the 37 orbit representatives of extremal 14-sets in [3]^3 |
| `certs/F33_n15.cnf`, `certs/F33_n15.drup` | `fjk_sat2.py --cnf`, Glucose 4 | F(3,3) ≤ 14: 3,280-clause CNF and its 8,366-line DRUP refutation (sha256 in WRITEUP) |
| PENDING_CERT_ROW | | |

## Known defects and open threads

- The general-j rate theorem (Corollary 4.4) is self-contained only for
  j ≤ 4; for j ≥ 5 it relies on the saturated-map lemma of the OpenAI chapter
  (attributed there to Alon–Ben-Eliezer–Shangguan–Tamo, JCTB 2020), which was
  read in the chapter but not in the JCTB paper.
- r_3(3) = 17 and r_3(4) ≤ 62 are cited through Radziszowski's dynamic
  survey (secondary).
- The circulant non-existence results and the extremal-set census are SAT
  verdicts without proof files (the enumerations are exhaustive by
  construction; the UNSATs at n = 45, 46, 50, 51 have no DRUP log).
- Sharpest open question: does E_k admit a valid colouring for every k
  (Wiesner's j = 3 conjecture, giving lim F(3,k)/3^k ≥ 1/2)? Every local rule
  tried fails; see NOTE §6 and WRITEUP.
- F(3,5) ∈ {122, 123} and F(4,4) ∈ [44, 61] are undecided.

## Prior work

Sawin's question (Aug 2026) is the source; no earlier paper defines, computes
or bounds F(j,k) as far as a literature search on 2026-09-06 could find. The
palette-block recursion is the one of OpenAI's *Ten Advances* (Aug 2026),
Chapter 9, "Super-exponential lower bounds for R(3,…,3)" (Theorem 1.1:
R_k(3) ≥ (c k^{1/3}/log k)^k; Proposition 3.1 keeps χ(colour class) ≤ j+1 at
stage j), and Rob Morris's exposition "The OpenAI lower bound on R_k(3)"
(erdosproblems.com/static/183-Morris.pdf; Theorem 2.1 there gives
F(3,2k) ≥ 2^{3k−o(k)}). Wiesner's follow-up MathOverflow 513991 (6 Aug 2026)
asks for explicit maps on restricted-growth strings and has no construction.
The two K_16 colourings with Clebsch classes are Kalbfleisch–Stanton (1968)
(secondary); OEIS A007051 lists (3^n+1)/2 with the Stirling-sum reading but
no Ramsey interpretation.
