# 2026-09-07 — good-permutations (MO 514690, Weiss's Mersenne-prime question)

**Target.** New external problem, per the standing mandate. MathOverflow
514690 (Philip Weiss, 27 Aug 2026, score 17, one answer): for odd n, call a
permutation a_1, …, a_n of {1, …, n} *good* if every proper consecutive block
of length ≥ 2 has non-integer average. Weiss found good permutations for
n = 3, 7, 31 and no other odd n ≤ 41, exhibited the family
1, p−1, p, p−3, p−2, …, 2, 3 for Mersenne primes p, and asked whether good
permutations exist iff n is a Mersenne prime. Bîsceanu's answer (from te4's
comment) proves that any odd n with a good permutation is a Mersenne number
2^m − 1, so the question is exactly the composite Mersenne numbers
63, 255, 511, 1023, 2047, …; n = 63 had never been tested. Chosen because the
in-thread structure theorem turns n = 63 into a search of measurable size,
because the question is eleven days old and not in OEIS (the count sequence
1, 2, 2, 2, 0, 2, 4, 8, 0, 2, 0, 4, 0, 2 returns "No results"), and because a
proof looked within reach on at least one side.

**Connectivity (checked 11:42 UTC).** arxiv.org reachable via WebFetch
(listing pages, abstracts, PDFs — read locally with pymupdf after the
fetcher's summariser choked on binary). oeis.org (search, fmt=text),
erdosproblems.com and mathoverflow.net return 403 / blocked to WebFetch but
serve curl with a browser user agent; MathOverflow also via the Stack
Exchange API. All four consulted live. OEIS rate-limited one scout (HTTP 429)
after ~10 minutes; it fell back to the oeisdata git mirror. pip reachable.
github.com source downloads (kissat, cadical, drat-trim) are refused by the
session's egress policy; pallini.di.uniroma1.it fails TLS through the proxy.
Workarounds: nauty 2.8.8 built from the pynauty sdist on PyPI (geng
validated: 112 connected graphs on 6 vertices), plantri 5.5 from the ANU
tarball, SAT via python-sat 1.9 (cadical195/300, kissat404, glucose42),
proofs checkable with `tools/satcert/rup_check`.

**Candidate slate** (three externals, three subfields; six parallel scouts —
OEIS, arXiv, erdosproblems.com, MathOverflow + standing lists, a status check
on a personal curiosity list, and the internal audit — full reports in the
session scratchpad; every statement below was checked against the primary
page on 2026-09-07):

1. **MO 514690, good permutations** (combinatorial number theory).
   Statement above. Source: mathoverflow.net/q/514690 (created 2026-08-27),
   answer by Bîsceanu (score 11), comments by te4 and Peter Taylor (partial
   "k-good" searches for n ≤ 39). Open: the answer settles only the Mersenne
   form; n = 63 untested; no OEIS entry; no paper found. **Selected.**
2. **Erdős #36 / OEIS A393584, minimum overlap** (additive number theory).
   M(n) = min over partitions of [2n] into equal halves of the maximum
   number of pairs with a given difference; exact values known for n ≤ 33
   (Sungkawichai, Sievers, Dobbelaere, Kesarwani, Feb–Mar 2026) and equal
   floor(5n/13) so far, which must fail since c < 0.380876 (White 2022 lower
   bound 0.379005; TTT-Discover 2026 upper bound, per erdosproblems.com/36).
   Passed over: the entry's four contributors are actively racing on it, and
   exact M(34) is a search whose cost nobody has published.
3. **Song–Cao ORS_20(2) ∈ {78, 79}** (extremal graph theory, arXiv:2608.14695
   v2, 30 Aug 2026): ordered Ruzsa–Szemerédi numbers at matching size two,
   exact for n ≤ 19; depth 80 excluded by exhaustive search over the
   510,489 cubic graphs on 20 vertices, 79 undecided; Lean-formalised
   characterisation. Passed over: the authors posted v2 eight days ago and
   are plainly mid-stride; a constructive depth-79 witness is a lottery.

   Also surveyed and rejected (details and dates in the scratchpad
   reports): Caragea–Lee principal-minor conjecture at N = 105, 110
   (arXiv:2608.17746, 2608.22119; specialist, medium risk); Chvátal's
   conjecture at n = 9 (n = 8 took 52 cores × 2 h with 14 GB of VIPR
   certificates, arXiv:2608.06432); minimum non-unique-product set in the
   Promislow group, sizes 8–13 in the radius-7 ball (arXiv:2607.18346;
   the author's CP-SAT model does not terminate); Erdős #272 t(13)
   (arXiv:2607.23004 predicts 82; the author is listed as "currently
   working on" the problem); n_6(4) semiregular types at n = 63
   (arXiv:2608.23652); geodesic Leech wheels W_14..W_40 (arXiv:2609.02544);
   Garcia's two open f(6) orientation instances (arXiv:2609.04686, probed
   in parallel — see below); Manabe's necessity conjecture for purely
   periodic three-move subtraction games (arXiv:2609.05358, 45 pages,
   Lean-formalised, three days old); OEIS A397434 (majority-function
   monomials, Lucas-theorem proof looks routine), Bala's fractional-
   factorial integrality family, A398270 grid feedback-vertex numbers
   (small provable OEIS conjectures, kept as fallbacks); MO 512325 (arcs of a
   tournament with identical Hamiltonian-path sets), MO 514613 (Z.-W. Sun's
   |i−j|-prime matrices, nonsingularity certifiable to 10^4 by one Toeplitz
   LU), MO 511219 (associahedron log-concavity to n = 15); Erdős #1073
   (n!+1 composite divisors: a 4-order-of-magnitude table extension, no
   decision); the whole erdosproblems computational shelf (the scout crawled
   all 1220 problems: every open problem with a visible numerical frontier
   was swept by AI-assisted posters between January and August 2026 —
   #413 to 10^8, #458 to 10^20, #583 all graphs n ≤ 11, #1142 to 2^128,
   #1093 k ≤ 160, #409 to 10^7). Status checks on my own curiosity list
   closed several doors: the lonely runner conjecture is now proved through
   13 runners (arXiv:2509.14111, 2511.22427, 2512.01912, 2604.23906), the
   1/3–2/3 conjecture through 14 elements (Gupta, arXiv:2607.23926, all
   1.34×10^12 posets), Chvátal at n = 8 (above), Erdős–Faber–Lovász n ≤ 12
   by SAT, no girth-7 snark to order 42, K_64 still the smallest open
   perfect-1-factorisation order, 236 ≤ cap(7) ≤ 288.

**Superseded shelf noticed on the way.** Garcia (arXiv:2609.04686, 4 Sep
2026): every graph of minimum degree ≥ 3 on ≤ 23 vertices has a 4- or
8-cycle, DRAT-certified level by level — this supersedes this repository's
Erdős–Gyárfás Theorem C1 (n ≤ 18, 2026-07-30); recorded in that README and
its index row this morning (commit 5317e96). He also states that the "17"
of the secondary sources (repeated in our row) has no primary source.

**Internal-thread assessment** (parallel audit of all 27 conjecture READMEs
and the eleven most recent logs). Last two sessions: kobon-triangles
(09-02) and bit-deletion with peaceable-queens secondary (09-03) — no forced
rotation. Strongest live thread: **peaceable-queens a(18)** — refute
48 + 48 on the 18 × 18 board with the validated SYM16 engine (n = 16:
5.03×10⁹ nodes / 462 s; n = 17: 2.15×10¹⁰ nodes / 1712 s on 4 workers;
projected 0.7–1.1×10¹¹ nodes, 2–3 h), literature witness a(18) ≥ 47
(Ainley/Kamenetsky) ready to verify; OEIS A250000 still ends at a(15) and
records 47 ≤ a(18) ≤ 81. Everything else is a compute wall (graham-
rearrangement p = 41 window t = 13..27 at 20–40 h, nci-datrees n = 16,
odd-giuga m = 13, distinct-subset-sums f(10), balanced-colorings K₂₆), an
unbuilt tool (power-residue-pairs' extension search; generalized-schur's
disk-streaming pipeline for (4,4,10)), or an ideas wall. Cheapest
row-changing internal item: generalized-schur (3,3,12) = 95? (< 1 h; not run
today). **Selection argument.** The mandate's default is the external
problem. MO 514690 beats a(18) on (a) — a decision whose search tree the
in-thread lemma makes measurable, plus a theorem within reach on the
construction side — and on the kind of result (an existence question with a
conjecture behind it, versus one more table entry); a(18) wins on citation
surface (A250000). Ties go to the new problem, and the two are not
exclusive: a(18) was launched at 11:55 UTC on niced background workers
exactly as the 09-03 session did, with the literature witness verified first
(47 white + 48 black queens, checker-accepted). Garcia's f(6) orientation
instances were probed by a time-boxed subagent in parallel.

**Result.** **CERTIFIED — no good permutation of {1, …, 63} exists.** Three
independently organised engines agree: A (backtracking over positions with
prefix-sum block tests and the residue structure of Lemma 2) and B (search
over the bit-functions of Lemma 2, sliding per-length accumulators) enumerate
the same tree and report the identical node count 1,433,402,570 (344 s and
128 s, one core); C (positions 1, q−1, 2, q−2, … so that the pairing
a_{t+q} = a_t ⊕ q makes three known intervals grow at once, with every odd
block inside them tested immediately) reports 0 in 7,091,512 nodes and
1.65 s. All three reproduce the plain-engine counts at every n ≤ 31 (the
plain engine uses no lemma: 1, 2, 2, 2, 0, 2, 4, 8, 0, 2, 0, 4, 0, 2 for
n ≤ 14, 0 at 15, 4 at 31 in 181,519,993 nodes). So Weiss's conjecture
survives its first undecided case, and for all odd n ≤ 127 good
permutations exist exactly at the Mersenne primes 3, 7, 31, 127.
**PROVED:** (i) Weiss's family W(p) = 1, p−1, p, p−3, p−2, …, 2, 3 is good
iff p is prime — blocks avoiding position 1 are never bad, even prefixes are
never bad for Mersenne p, and the prefix of odd length L has sum ≡ −p
(mod L) (NOTE Thm 4; the thread asserts goodness for Mersenne primes without
proof and does not state the converse); (ii) the triangular structure
theorem in the form used by the engines — a_t mod 2^k depends only on
t mod 2^k through a bijection fixing 0, whence a_q = q and the pairing —
with the counting step made explicit, and (iii) Lemma 3: under that
structure every even-length block is automatically fine, so goodness is a
condition on odd block lengths only. **CERTIFIED** side facts: W(p) verified
from the definition at p = 7, 31, 127, 8191, 131071, 524287 and shown bad at
15, 63, 255, 511, 1023, 2047, 4095, always first at the prefix whose length
is the least prime factor; at n = 7 and 31 the good permutations are
exactly W(p) and its three images under reversal and complement; the
counts for all n ≤ 26 (even n: 2 or 4, with 8 at n = 8) — none of this is
in OEIS. **Relaxation data (CERTIFIED counts, observation):** the
obstruction at composite Mersenne numbers is not divisibility of n — at
n = 15 the minimal excluding sets of odd lengths are {3,5,7}, {3,5,9},
{3,7,11}, {3,9,11}; at n = 63 all odd lengths up to 29 leave 260 candidates
(with a_1 < 32) and the length 31 = q − 1 kills every one; at n = 31 the
ladder reaches the true count exactly when 15 = q − 1 enters. NOTE §4a
explains why lengths 2^k − 1 are resonant (a block of that length misses
one residue class mod 2^k, and 2^k ≡ 1 modulo the length), and writes the
length-(q−1) conditions as a ±1-step walk in the top bits that must avoid
the residue permutation pointwise. The survivors of every sub-resonant
relaxation at 63 are identity-like (a_t ≡ ±t mod 16, with 16-flips mod 32),
and for the exactly identity-like families that observation became a
theorem: **PROVED (Theorem 5)** — for m ≥ 4 no good permutation of
2^m − 1 has a_t ≡ t (mod 2^{m−1}) for all t, nor a_t ≡ −t; the family
reduces to a bit string x on the top bits with (I1) no 000/111 and (I2)
prefix and suffix one-counts never equal at lengths of equal parity, and
five blocks of length 3, 5, 7 around the middle position force a
contradiction (reduction confirmed by brute force at q = 4, 8, 16, the
constraint subset checked mechanically for all odd N ≤ 15). n = 127 (uniqueness of W(127) up to
symmetry): engine C launched at 12:26 UTC, still running at the time this
entry was written (74 % of one core under contention); its outcome is
recorded in `conjectures/good-permutations/results/n127_mid_run1.txt` and
the README when it lands, and is not claimed here. New directory
`conjectures/good-permutations/` (README, NOTE, WRITEUP, PAGE.md, three
engines, checker, CP-SAT model, run records); index row added.

**Secondary results.** (1) peaceable-queens a(18): the m = 48 SYM16
refutation (`run_chunked.py 18 48 16 4 ./bnb_sym`, 16 chunks on four niced
workers) was launched at 11:55 UTC after the literature witness
(Ainley/Kamenetsky, 47 white + 48 black queens) passed `check_peaceable`;
**all 16 chunks UNSAT — a(18) = 47, CERTIFIED** (single-engine, as at
n = 17): 119,110,352,726 nodes, 32,544 s of engine CPU time (chunks
4.6·10⁸ to 1.41·10¹⁰ nodes), 13,470 s wall at nice 19 underneath the
good-permutations searches; every completed chunk was committed as it
landed (15:41 UTC for the last). Node growth over n = 17: ×5.55. The
third consecutive open case of A250000 decided, each equal to ⌊7n²/48⌋;
peaceable-queens README/NOTE §6c/WRITEUP session 3/PAGE.md and the index
row updated. Caveat as before: no plain-engine replication (≈ 80
core-hours at n = 18). (2)
Garcia's two open f(6) orientation instances (arXiv:2609.04686 §5), probed
by a 60-minute subagent (`conjectures/erdos-gyarfas/f6_orientations/`):
exhaustive enumeration of the girth-14 connection sets of AGL(1,29) and
AGL(1,31) gives exactly two and four base graphs (CERTIFIED); one of the
six admits no admissible orientation by counting alone (PROVED from
certified cycle counts: its 62 pure-g 15-cycles force ≥ 186 t-edge choices
while its 14-cycles allow ≤ 155), two more are forced to use no t-edge and
are then UNSAT in seconds (two solvers, two encodings, no DRAT), every
constant and Z_p-invariant orientation is UNSAT on all six, and the three
remaining graphs — the only ones that could give 12,180 or 13,950 — were
undecided after 5–20 minutes per solver, as in the paper.

**Attempt statement.** Decide whether a good permutation of {1, …, 63}
exists, by an exhaustive backtracking search that uses the residue
structure every good permutation of a Mersenne number must satisfy
(re-proved in NOTE.md, Lemma 2, from the thread's argument) to prune and
tests every proper block incrementally; validate the engine against a
structure-free brute force for n ≤ 14 and at n = 31 (both modes must return
the same four permutations, i.e. the construction and its three images under
reversal and complement); then run 63, and push to 255 if the tree allows.
Achieved means: a checker-verified good permutation of [63] (refuting the
"iff Mersenne prime" conjecture) or a reproducible exhaustive zero with node
counts (CERTIFIED), plus the theorem the construction test suggested — that
the family 1, p−1, p, … is good exactly when p is prime.

**What failed.**
- *A proof for composite Mersenne numbers.* The first guess — a proper
  divisor d of n forces a bad block of length d — was refuted by the
  relaxation probe within minutes: at n = 15 the lengths 7 and 11 (coprime
  to 15) are needed, and at 63 the decisive length is 31, not 3, 7, 9 or
  21. The second guess — the short odd lengths {3,5,7} suffice for every
  even exponent, as they do at 15 — died at 63 (2,114 survivors). What is
  left is the resonant-length mechanism of NOTE §4a, identified but not
  turned into a proof.
- *CP-SAT as a fourth method.* OR-Tools CP-SAT over the 57 bit variables
  with 960 modular block constraints reproduces the counts at 7, 15, 31
  (enumeration at 31: 17 s) but did not decide n = 63 in 25 minutes on two
  workers and was stopped; the structure-aware DFS is four orders of
  magnitude faster here. Not a route to 255.
- *Engine-A-style relaxation probes at 63* were too slow (the single-length
  probe {3} did not finish in 25 minutes) and were superseded by the
  length filter in engine C, which answers each in about a second.
- *Operations.* A `pkill -f` whose pattern matched the invoking shell's
  own command line killed that shell (the 2026-09-01 log recorded the same
  wound; PIDs only, again). Two background probe launches lost their
  relative paths to the harness's working-directory reset. github.com
  source downloads are refused by the egress policy, so kissat/cadical/
  drat-trim were not rebuilt; nauty came from the pynauty sdist instead.

**Next.** (1) n = 255: engine C's tree grows ×21, ×64, ×267 per doubling
(20, 416, 26,540, 7,091,512 nodes), so 255 is of order 10^13 nodes — out
of reach without a new idea; the resonant-length reformulation (NOTE §4a)
is the candidate idea: treat the length-(2^k − 1) conditions at all levels
k as constraints on the higher-bit sums and search the top bits last.
(2) A proof that composite Mersenne numbers have no good permutation,
starting with even exponents (3 | n): the survivors of the short-length
relaxations are W-type and near-identity triangular maps, suggesting
"force the family, then kill it". (3) Post the n = 63 result and Theorem 4
as an answer on MO 514690 and submit the count sequence to OEIS — decisions
for the local session per repository policy. (4) Erdős–Gyárfás f(6): the
three undecided AGL orientation instances want a proper cube-and-conquer
run with DRAT proofs; the 12,180 route is a single 812-vertex graph.
(5) peaceable-queens a(19): ≈ 6.5·10¹¹ nodes at ×5.5 per rung — a
dedicated multi-session run, and the plain-engine replications of n = 17
and 18 are still owed.

**Session hygiene.** Branch: harness-designated `claude/affectionate-sagan-w2uu1s`
(the mandate's per-conjecture branch name overridden by the harness
requirement, as in previous sessions). The `conjecture-research` skill
named in CLAUDE.md is not installed here; CLAUDE.md followed directly.
Hardware: 4 cores, 15 GB; Python 3.11.15; gcc 12; OR-Tools 9.15;
python-sat 1.9. No seeds; everything exact. Time: survey and selection
11:36–12:00 UTC; the n = 63 zero was in hand at 12:12; engines B and C,
the ladders and the documents by 12:45; long runs (127, a(18)) continued
after that.
