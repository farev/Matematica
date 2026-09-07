# Session narrative — chromatic-ramsey

## Session 1 — 2026-09-06

### How the problem was chosen

The day's survey (five parallel literature agents over the Erdős Problems
database, the last six weeks of arXiv math.CO/math.NT, the newest OEIS
entries with unproved conjectures, MathOverflow's unanswered questions, and
the repository's own open threads) is recorded in the daily log. The
MathOverflow sweep turned up Sawin's question 513849 of 2 August: F(j,k), the
largest n with a k-edge-colouring of K_n whose colour classes are triangle-free
and j-colourable, with the limit question lim_k F(j,k)/j^k = 0?, and in the
comments Wiesner's Stirling-sum conjecture F(j,k) ≥ Σ_{i≤j} S(k+1,i). Nobody
had posted a single value beyond F(2,k) = 2^k. The first thing I checked was
whether the two triangle-free 3-colourings of K_16 (Clebsch classes) give
F(3,3) = 15 by deleting a vertex: the Clebsch graph minus one or two vertices
is still 4-chromatic (SAT), so F(3,3) was genuinely undetermined.

### The type formulation and the first values

Lemma 1.1 of the NOTE turns F(j,k) into a search over subsets of the cube
[j]^k: 27 candidate types for (3,3), 81 for (3,4). The SAT model (`fjk_sat.py`:
selection variables per type, colour variables per pair and differing
coordinate, "selected pair needs a colour", "no monochromatic triangle",
cardinality ≥ n) decided F(3,3) ≥ 15 UNSAT in 0.1 s and F(3,3) ≥ 14 SAT in
0.0 s — exactly Wiesner's 14 — and then F(3,4) ≥ 41 SAT in 0.2 s, again
Wiesner's value. The witnesses had a striking profile: in every direction the
three layers had sizes (5,5,4) at k = 3 and (14,14,13) at k = 4, lines carried
at most two points, planes 4 or 5. That is the profile of the set E_k of
ternary words with an even number of 2's, whose size (3^k+1)/2 is Wiesner's
number for j = 3. Fixing the vertex set to E_k (`fixed_sat.py`) gave valid
colourings instantly for k = 2, 3, 4 and in 2.7 s for k = 5, hence
F(3,5) ≥ 122.

### Failed attempts at a general rule for E_k (the bulk of the afternoon)

The obvious target was a theorem: colour E_k for every k. Everything tried
failed, and the failures are informative.

1. *Coordinate-first rules.* Colouring a pair by its first differing
   coordinate is triangle-free exactly when every prefix has at most two
   continuations — the binary cube. Any "deflection" rule that sends the
   {0,2}-type pairs (or the {1,2}-type) to a later coordinate produces a
   monochromatic triangle in E_k, e.g. 202, 212, 022 all in colour 2.
2. *Pattern-invariant rules.* A rule depending only on the coordinate-wise
   difference pattern of a pair is the same as a colouring invariant under all
   single-coordinate swaps 0 ↔ 1. Such colourings do not exist for k ≥ 2:
   with x = (2,2,0,…), y = 0 and z = e_c, the pairs (x,y) and (x,z) have the
   same pattern, and whichever of the two 2-coordinates the rule picks, one of
   the triangles {x,y,e_c}, {x,y,e_d} is monochromatic. Proof by hand,
   confirmed by SAT on E_2.
3. *Bipartite colour classes.* If every G_c is bipartite then a two-colour
   product argument caps |S| at 2^k (this is F(2,k)); so any positive-density
   construction needs odd cycles in every class — the K_5 = C_5 ∪ C_5 base
   case already shows it.
4. *Inductive layer towers.* E_{k+1} = E_k×{0,1} ∪ O_k×{2}. Lifting a fixed
   colouring of the layers is UNSAT at k+1 = 3 without a twist and SAT with
   the O-layer colouring twisted by a swap (`tower.py`, `tower2.py`); a family
   of 64 sign-based inductive rules for the cross pairs (`induct.py`, rules
   "new colour iff the layer sign equals the point's sign at the colouring
   coordinate", forced by the line triples) all die by k = 3.
5. *Symmetry.* A colouring of E_k invariant under the global swap and the
   cyclic coordinate shift exists for k = 3 and k = 5 but not k = 4 (the
   triangle 0000, 1111, 2222 is fixed by the shift). Reading a rule off the
   k = 3 solution (17 orbits) did not succeed.
6. *Cyclotomy.* Circulant witnesses exist on Z_14, Z_41, Z_122 (found by
   SAT), but the natural cyclotomic candidate — quartic residues mod 41
   rotated by powers of 3 — has 4-chromatic classes, and (3^k+1)/2 is prime
   only rarely, so no uniform algebraic family emerged.
7. *Uniqueness.* Enumerating all 14-point colourable subsets of [3]^3 gave
   33,831 sets in 37 orbits, so E_3 is one natural extremal set among many;
   there was no rigidity to exploit.

### The theorem that did come out

Reading the literature agent's summary of the OpenAI chapter (the recursion
that gives R_k(3) ≥ k^{k/3−o(k)}: blocks indexed by palettes, cross edges
coloured inside P△Q via a "two-sided coordinate cover" f,g : [H]^s → [H]^s), I
noticed that for binary labels the cover is trivial — f = id, g = −id, s = 1 —
so every t-subset of [k] can be a palette and the block sizes need no
Ramsey-type loss. That is Theorem 3.1: F(3,k) ≥ C(k,t)2^{k−t}, whence
F(3,k) ≥ 3^k/(k+1) and the exponential rate 3, against Morris's stated
2^{3/2}. The proof is half a page; the construction was verified mechanically
for k ≤ 8 (up to K_1792, `verify_colouring.c`). The same idea with the general
cover gives the rate j for every fixed j (Theorem 4.2 with the power-sum
palette families of Lemma 4.3), self-contained for j ≤ 4 with an explicit
(3,2)-gadget found by SAT and verified; the r = 3 → 4 step was checked on
K_56 and K_98. The LYM inequality shows antichain palettes cannot beat
max_t C(k,t)2^{k−t}, which explains why the E_k structure — all even subsets
as palettes, nested — is needed for density 1/2, and why the local rules above
kept failing: the nested cross pairs are the whole difficulty.

### Certificates

F(3,3) ≤ 14: Glucose 4 with DRUP logging on the 3,280-clause instance, 8,366
proof lines, checked by the repository's `rup_check` (0.2 s).
sha256: `1425bf4c…812b` (cnf), `f6fc7b2f…523b` (drup); full hashes in
`certs/`.

F(3,4) ≤ 41: the plain SAT run (n = 42, 81 types, with the implied line /
plane / cube cardinality bounds added) did not finish in 50 minutes of
CaDiCaL, nor in 73 minutes of proof-logged Glucose. A cube-and-conquer
split on the layer x_4 = 0 (which must be one of the 37 extremal 14-set
orbits, up to a symmetry of the first three coordinates) refuted all 37 cubes
in 228 s of CaDiCaL, and the proof-logged Glucose rerun produced 37 DRUP
proofs (167 s; 0.3–37 MB each, 380 MB in total), every one of which
`rup_check` verified (about 15 minutes on four cores; log and hashes in
`certs/`). The census that the split rests on was itself
re-derived with proof logging: the final UNSAT of the blocking-clause
enumeration (37,097 clauses) has a 1,529,304-line DRUP proof (109 MB),
verified in 3 min 59 s, and an independent recount of the 33,831 sets gives
the same 37 orbits (sizes 27, 216, 324, 432, 432, thirteen of 648, eighteen
of 1296; the orbit of size 27 is E_3). The large proof files are not
committed (hashes in `certs/SHA256SUMS_large.txt`; the scripts regenerate
them).

F(3,6) ≥ 365: the circulant search on Z_365 with six classes timed out at
50 minutes without a verdict, but the direct SAT on E_6 (365 vertices,
10.9 M clauses streamed into CaDiCaL, 45 s to build) returned a colouring
after 238 s, verified over all 8,038,030 triples in 5 s.

Circulant witnesses are verified by `verify_circulant.py` from the JSON
files, which carry the explicit proper colourings.

### What did not get done

- A valid colouring of E_k for all k (Wiesner's j = 3 conjecture) — the
  question this session most wanted to answer — remains open; the note records
  every rule shape that fails.
- F(3,5) ∈ {122,123} was not attempted beyond a circulant check (no
  circulant witness for 123; 243 types, and the n = 42 UNSAT already needed
  cube-and-conquer over a certified census).
- F(4,4): the plain SAT for n = 45 (256 types, 4.2 M clauses) ran 25 minutes
  without a verdict; only the circulant 44 is certified.

### Side observation (log only)

The OEIS survey agent found that A398259's conjecture "these 26 zeros are all
the zeros" is false; an independent C implementation from the entry's
definition reproduces the 26 zeros and the published checkpoints and finds
a(700000442) = 0 (a(700000441) = 699999999 has digit sum 78, a value that
never occurs as a term below it). Recorded in the daily log.

### Hardware and time

4 cores, 15 GB, Python 3.11.15, python-sat 1.9.dev15 (CaDiCaL 1.5.3, Glucose
4), gcc 13.3. All searches are seconds except the enumerations (8 min
CaDiCaL; 68 s Glucose plus 4 min of proof checking), the n = 42 refutation
(228 s CaDiCaL, 167 s Glucose, about 15 min of parallel proof checking), the
E_6 colouring (283 s), and the three runs that produced nothing in their
time limit (plain n = 42: 50 + 73 min; F(4,4) ≥ 45: 25 min; circulant
K_365: 50 min).
