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
