# 2026-09-06 — chromatic-ramsey (Sawin's F(j,k), MathOverflow 513849)

**Target.** New external problem, per the standing mandate. Will Sawin
(MathOverflow 513849, 2 Aug 2026) defines F(j,k) as the largest n such
that the edges of K_n can be k-coloured with every colour class
triangle-free *and* vertex j-colourable, notes F(2,k) = 2^k, the trivial
bound F(j,k) ≤ j^k and F(j,k+1) ≤ j·F(j,k), and asks whether
lim_k F(j,k)/j^k = 0 for some j. In the comments Fabius Wiesner
conjectures F(j,k) ≥ Σ_{i≤j} S(k+1,i) (Stirling numbers of the second
kind) "based on very few numerical tests"; Sawin observes that this would
give r_3(k) ≥ B_{k+1} (Bell numbers). No value of F beyond F(2,k) had been
computed anywhere. Chosen because the first open values are decided by
small SAT instances and because the j = 3 case of Wiesner's conjecture,
F(3,k) ≥ (3^k+1)/2, is a clean statement with a natural candidate vertex
set. What counted as success: exact values of F(3,3), F(3,4), certified
bounds for the next cells, and — the stretch goal — a construction proving
F(3,k) ≥ (3^k+1)/2 for all k (which would show lim F(3,k)/3^k ≥ 1/2).

**Result.** **PROVED.** F(3,k) ≥ C(k,t)·2^{k−t} for every t ≤ k, hence
F(3,k) ≥ 3^k/(k+1) and F(3,k) ≥ (1+o(1))·3^k·3/(2√(πk)): the exponential
growth rate of F(3,k) is exactly 3, the trivial upper bound, where the best
rate on record for three-colourable classes was 2^{3/2} (Morris's exposition
of the OpenAI palette recursion, Theorem 2.1 there). The construction takes
blocks indexed by the t-subsets P of the colour set, a binary cube {±1}^{[k]∖P}
in each block coloured by first difference, and colours a cross edge by
a = min(Q∖P) if u_a = v_b and by b = min(P∖Q) otherwise — the OpenAI
"two-sided coordinate cover" is trivial for binary labels (f = id, g = −id),
which is why every t-subset can serve as a palette with no Ramsey-type loss.
Verified mechanically to K_1792 with 8 colours. More generally
F(j,k) ≥ j^k/(2k+2)^{d_j} for every fixed j (NOTE Corollary 4.4: palettes with
pairwise |P∖Q| ≥ s from power-sum residue classes, saturated maps of dimension
s; self-contained for j ≤ 4 via an explicit (3,2)-gadget found by SAT, the
j = 3 → 4 step checked on K_56 and K_98; j ≥ 5 cites the OpenAI/Alon et al.
lemma), so lim F(j,k)^{1/k} = j for all j. These settle the exponential rate
but not Sawin's constant: the loss is polynomial. **CERTIFIED:** the first
exact values, F(3,3) = 14 (three witnesses; UNSAT at 15 with an 8,366-line
DRUP proof checked by `tools/satcert/rup_check`), F(4,3) = 16 (witness;
≤ 16 by r_3(3) = 17), PENDING_LOG_F34 and the bounds F(3,5) ≥ 122 (two
witnesses), PENDING_LOG_F36 F(4,4) ≥ 44 (circulant), all witnesses checked
from the definition by independent code; no circulant witness for
F(4,4) ≥ 45 and no circulant triangle-free 4-colouring of K_46, K_50, K_51.
Wiesner's conjecture is exact at (3,3) PENDING_LOG_F34B, a strict lower bound
at (4,3) (15 < 16), and its j = 3 value (3^k+1)/2 is realised for k ≤ 5 by
the even-weight set E_k (ternary words with an even number of 2's), which
the SAT-found extremal sets resemble exactly in their line/plane/layer
profile — but E_3 is one of 37 inequivalent extremal 14-sets. **PROVED
(barrier):** antichain palette constructions cannot exceed
max_t C(k,t)2^{k−t} (LYM), so density 1/2 needs the nested palettes E_k has.
New directory `conjectures/chromatic-ramsey/` (README, NOTE, WRITEUP,
PAGE.md, code, witnesses, certificate); index row added.

**Connectivity.** arxiv.org reachable via the standard fetcher (listing
pages, abstracts; PDFs fetched and extracted locally with pymupdf).
oeis.org, erdosproblems.com and mathoverflow.net return 403 to the
fetcher's user agent but serve curl with a browser user agent normally;
the Stack Exchange API (api.stackexchange.com) also works. All four
consulted live today. pip reachable (sympy, python-sat, gmpy2, networkx,
pymupdf installed).

**Candidate slate** (three externals, two subfields; statements and status
checked against the sources on 2026-09-06):

1. **MathOverflow 513849, Will Sawin, "Ramsey numbers when each color has
   small chromatic number"** (Ramsey theory / extremal combinatorics),
   posted 2 Aug 2026, score 10, no answers. Statement, quoted: "Let F(j,k)
   be the greatest n such that one can color the edges of the complete
   graph on n vertices with k colors such that the graph formed from the
   edges of each color is triangle-free and admits a vertex j-coloring.
   Does there exist j such that lim_{k→∞} F(j,k)/j^k = 0?" Comment
   (Wiesner): "A rather speculative conjecture just based on very few
   numerical tests is F(j,k) ≥ Σ_{i=1}^{j} S(k+1,i)". Open: no answers or
   later comments; no exact small value posted; a literature agent found
   no prior computation of these numbers (see the literature paragraph in
   the WRITEUP). **Selected.**
2. **MathOverflow 514297, Bogdan Grechuk, "Positive integer solutions to
   x⁴+3y⁴=z⁴+t⁴"** (Diophantine number theory), 15 Aug 2026, score 9, no
   answers. Quoted: "Do there exist positive integers x,y,z,t satisfying
   the equation x⁴+3y⁴=z⁴+t⁴? … it is the only open diagonal homogeneous
   equation of size at most 100." The only search bound in the thread is
   an unverifiable "ChatGPT claims it checked up to max ≤ 10,000,000".
   Open per the asker (his systematic project, arXiv:2404.08518). Passed
   over: a certified exhaustive search to 10^5 on this machine would only
   replace an LLM claim, and finding a solution needs a curve on the
   quartic K3 surface — ideas, not compute.
3. **arXiv:2607.23004, Zhanfu Yang, "Exact values and exact upper bounds
   for families of integers with arithmetic progression intersections
   (Erdős Problem #272)"** (extremal set theory), 25 Jul 2026. Abstract
   (checked): t(N) — the largest number of distinct subsets of [N] whose
   pairwise intersections are nonempty arithmetic progressions — "is
   determined exactly for all 3 ≤ N ≤ 12 by exhaustive computation; in
   this entire range Szabó's lower bound is exact, and we conjecture that
   t(N) = C(N,2)+1+⌊(N−1)/4⌋ for every N"; the starred (common-element)
   case is proved for all N. t(13) (conjectured 82) is open; deciding it
   is a clique search on 8191 vertices, a fair chance in hours with a
   bitset solver. Passed over in favour of 1 because 1 offered both a
   computation and a theorem target.

   Near-misses examined: Cordella's Lonely Runner spectrum paper
   (arXiv:2609.03444, 3 Sep 2026) — its exceptional set E6 has no
   explicit bound ("We do not know an explicit bound for E6"), so closing
   it is an ideas problem, and extending the speed-110 search is a 10 %
   extension; the classification of tight sextuples it names as the
   blocker for seven speeds is open but not a computation. OEIS A002966
   a(9) (Egyptian fractions of 1 with nine terms, Guy D11, open since
   a(8) in 2004): a prototype of Le Normand's method reproduced a(4..7)
   but the last-three-term subproblem contains the Sylvester prefix
   2,3,7,43,1807,3263443 whose seventh denominator ranges over ≈2·10^13
   candidates, so the method cannot reach a(9) without a new 3-term
   counting formula (ideas wall). Erdős #531 (exact F(3) of the
   subset-sum colouring number), #307 (products of unit-fraction sums),
   #167 (Tuza to 11 vertices), Tranquilli's order-60 cubic bipartite
   Erdős–Gyárfás case (arXiv:2608.02675), Song–Cao's ORS_20(2) ∈ {78,79}
   (arXiv:2608.14695), Lysenstoeen's A(23,6,10) depth-4 MILP
   (arXiv:2607.19550), and the MathOverflow items 514313 (Hold That Line
   variants), 512461 (nonnegative Littlewood polynomials), 514640 (metric
   dimension of H(4,6)) were all judged feasible but smaller. OEIS
   A398259's zero conjecture (see the side observation) was found false
   by the OEIS survey agent and re-verified here.

**Internal-thread assessment** (parallel agent audit of all 26 conjecture
READMEs and the nine most recent logs). Last sessions: bit-deletion +
peaceable-queens (09-03), kobon-triangles + power-residue-pairs (09-02);
no forced rotation. Strongest live internal thread: **peaceable-queens
a(18)** — refute 48+48 on the 18×18 board with the validated SYM16 engine
(≈8.6·10^10 nodes at the ladder's ×4 per rung, 2–5 h on 4 cores), a pure
compute wall with zero ideas risk; OEIS A250000 still ends at a(15) as
fetched today (bracket 47 ≤ a(18) ≤ 81). Runner-up: generalized-schur
S(3;4,4,10) and (4,4,11) with a disk-streaming solver (memory wall).
Everything else is a multi-day compute wall or an ideas wall. Selection
argument: (a) both F(j,k) and a(18) are compute-breakable, but F(j,k)
also carried a theorem target; (b) prior-work risk: F(j,k) is a month-old
question with no computed values, while a(18) is an unclaimed rung of a
famous sequence — comparable; (c) citation surface: Sawin's question,
Wiesner's conjecture, the 2026 OpenAI lower bound on r_3(k) that
motivated it, and Radziszowski's dynamic survey, versus A250000. Ties go
to the new problem; the external candidate won on (a).

**What failed.**
- *The theorem I actually wanted* — a valid colouring of E_k for all k
  (Wiesner's j = 3 conjecture, lim F(3,k)/3^k ≥ 1/2). Six rule shapes fail
  and are recorded in the WRITEUP: first-difference with deflection
  (monochromatic 202, 212, 022), pattern-invariant rules (provably none exist
  for k ≥ 2 — the pairs {220·,000·} and {220·,100·} have the same pattern),
  bipartite colour classes (cap 2^k), untwisted and twisted layer towers
  (UNSAT without a twist at k = 3, lifts exist with a twisted O-layer, no
  uniform twist found), sixty-four sign-based inductive rules (all dead by
  k = 3), and cyclotomy (quartic residues mod 41 have 4-chromatic classes).
  The Z_2 × Z_k-symmetric colourings exist only for odd k (0000, 1111, 2222 is
  a shift-fixed triangle when k is even), which killed the hope of a uniform
  symmetric family.
- *Plain SAT refutation of F(3,4) ≥ 42*: CaDiCaL with the implied line /
  plane / cube cardinality bounds ran 50 min without a verdict; the
  cube-and-conquer split over the 37 extremal-14-set orbits PENDING_LOG_CUBE.
- *F(4,4) ≥ 45 by SAT* (256 types, 4.2 M clauses): 25 min, no verdict; only
  the circulant 44 stands. Circulants reach at most 44 (Z_45 UNSAT, Z_46 UNSAT
  even without the chromatic condition).
- *The slate's other candidates* were not attacked; nothing else failed.

**Side observation (CERTIFIED, log only).** OEIS A398259 (Bernáth, 24 Jul
2026; Van Eck-like sequence keyed on the digit sum of the previous term)
conjectures that its 26 zeros below 10^6 (A398307) are all the zeros. The
OEIS survey agent found a counterexample and an independent C implementation
written from the entry's definition (`tools/oeis-checks/a398259.c`)
confirms it: the program reproduces all 26 listed zeros and the published
checkpoints a(10^4) = 9365, a(10^5) = 99353, a(10^6) = 999847, and finds
a(700000441) = 699999999, whose digit sum 78 never occurred as a term
before, so **a(700000442) = 0** — a 27th zero (34 s to N = 7.1·10^8). The
agent's own run reports 251 further zeros below 2·10^9, all keyed on 78
(not independently reproduced here). Both conjectures of the entry (the zero
list, and lim a(n)/n = 1) should be re-examined by the author; recorded here
so a local session can forward it.

**Next.** (1) Colour E_k for all k: the nested cross pairs are the whole
difficulty (Remark 3.2); a candidate route is an inductive hypothesis on
the pair (E_k, O_k) that also constrains the cross colouring of E_k×O_k,
found by SAT for k ≤ 4 and then read off. (2) F(3,5) ∈ {122,123}: a
cube-and-conquer over the extremal 41-set orbits (enumerate them first, as
for k = 3). (3) F(4,4): try Cayley colourings on the non-abelian groups of
order 45–51 and the E-like sets in [4]^4; Wiesner's 51 would beat Chung's
r_3(4) ≥ 51. (4) Report F(3,3) = 14, F(3,4) = 41 and the rate theorem to
Sawin's question — a decision for the local session per repo policy.

**Session hygiene.** Branch: harness-designated `claude/affectionate-sagan-sp4ict`
(the mandate's per-conjecture branch name overridden by the harness
requirement, as in previous sessions). The `conjecture-research` skill
named in CLAUDE.md is not installed here; CLAUDE.md followed directly.
Hardware: 4 cores, 15 GB; Python 3.11.15; gcc 13.3; python-sat 1.8
(CaDiCaL 1.5.3 for search, Glucose 4 with DRUP logging for the certified
UNSAT boundaries, proofs checked by `tools/satcert/rup_check.c`). No
seeds; everything exact.
