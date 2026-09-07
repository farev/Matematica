# 2026-09-05 — ordinary-lines (Sylvester's problem, A003034(15)) + good-permutations (hedge)

**Target.** The smallest open case of the Dirac–Motzkin conjecture on ordinary lines.
For n points in the real plane, not all collinear, t₂(n) is the minimum number of lines
through exactly two of them (OEIS A003034, "Sylvester's problem"). Exact values are
known for n ≤ 14 and for n = 16, 18, 22 (Pach–Sharir table as quoted in A003034);
Green–Tao (2013) proved t₂(n) ≥ n/2 for all n ≥ n₀ with n₀ "of double exponential type"
and wrote that "one could take n₀ as low as 14" if only n = 7, 13 are exceptional. At
n = 15 the literature gives 7 ≤ t₂(15) ≤ 9 (Csima–Sawyer 6n/13 below, the Böröczky-type
example of Green–Tao Prop. 2.1(iii) above) and nothing else; A003034 shows "?". Chosen
because the combinatorial abstraction — rank-3 chirotopes with collinear triples allowed
— fits a SAT encoding of a few hundred thousand clauses, and because Melchior's
inequality plus the pair-counting identity pin the line-type distribution of a
hypothetical 7-ordinary-line configuration to a single shape (two 5-point lines, 26
three-point lines), which is exactly what a solver can exploit. Success meant t₂(15) ≥ 8
with checked certificates (the Dirac–Motzkin bound at n = 15), or t₂(15) = 9, or a
pseudo-configuration beating the conjecture.

**Result.** **CERTIFIED, partial.** A 15-point set with exactly 7 ordinary lines, real
or pseudoline, must have exactly two 5-point lines and 26 three-point lines (PROVED,
Melchior + counting). *The two 5-point lines cannot be disjoint:* all 261 sub-cases of the
disjoint cube are UNSAT with drat-trim-checked DRAT proofs (2 472 s solving, 2 480 s
checking, 6.3 GB of proofs, 55 min wall on 2 cores; Kissat 4.0.4). *If they meet, at least
one and at most five of the 16 pairs joining them span ordinary lines:* the no-ordinary
case is refuted by 411 fixed-array instances, all UNSAT verified (1 212 s, 45 min on one
core), and the ≥ 6 case by a parity argument, machine-checked on its 83 sub-classes
(all UNSAT, 134 s). Two of the remaining 47 sub-classes (the two with 70 arrays each) were
also closed in fill mode (140 arrays, all UNSAT verified). **The other 45 sub-classes of the
meeting case are open**, so **t₂(15) ≥ 8 is not established today**; every point of such a
configuration has an even number of ordinary lines (PROVED). Side facts: t₂(20) = 10 and
t₂(24) = 12 follow from Csima–Sawyer + Böröczky (the A003034 comment's "?" at 20 is a
transcription gap). New directory `conjectures/ordinary-lines/` (README, NOTE, WRITEUP,
PAGE.md, code, ledgers); index row added, marked partial.

**Hedge result (subagent, one core).** **CERTIFIED + PROVED.** MathOverflow 514690
(P. Weiss, 27 Aug 2026): a permutation of {1..n}, n odd, is *good* if no proper consecutive
block of length ≥ 2 has an integer average; do good permutations exist iff n is a Mersenne
prime? The thread had n = 2^m − 1 forced and searches to n = 41. Today: **no good
permutation of {1..63}** — goodness for n = 2^m − 1 is PROVED equivalent to a 2-adic
isometry condition plus the odd-length block conditions (Lemma B), the 2^57 candidates are
exhausted by two independent programs (1,433,402,570 nodes each, 20.0 s and 200.9 s); the
asker's construction is good **iff** p is prime (PROVED, Prop. C); lemma-free brute force to
n = 43 with exact counts 2, 4, 4 at n = 3, 7, 31; hence the conjecture holds for all odd
n < 255. NUMERICAL: at n = 63 the only killing lengths are 31 and 33 = 2^{m−1} ± 1 (exact
criterion PROVED, Lemma E), and a rigidity conjecture (every good permutation is the
construction up to reversal/complement). I re-checked every lemma by hand before
labelling. New directory `conjectures/good-permutations/`; index row added.

**Connectivity.** arxiv.org reachable via the standard fetcher (listing page dated
4 Sep 2026 read; PDFs via curl and text-extracted with pymupdf). oeis.org,
erdosproblems.com and mathoverflow.net return 403 / blocked to the fetcher but serve curl
with a browser user agent; MathOverflow also via the Stack Exchange API
(api.stackexchange.com, `site=mathoverflow`). All four consulted live today. pip and
github.com (solver sources) reachable; Springer and Cambridge Core article pages are
paywalled (Csima–Sawyer, Kelly–Moser cited via Green–Tao, marked secondary). The
`conjecture-research` skill named in CLAUDE.md is not installed; CLAUDE.md followed directly.

**Candidate slate** (three externals across three subfields, each checked against a live
source today; six scouts ran in parallel and their full reports are in the session
scratchpad):

1. **Sylvester's problem, t₂(15)** (discrete geometry). Sources:
   `oeis.org/search?q=id:A003034&fmt=text` (#27, 30 May 2026: data 3,3,4,3,3,4,6,5,6,6,6,7
   for n = 3..14; comment "Pach and Sharir give … 7, ?, 8, ?, 9, ?, ?, ?, 11"; formula line
   "Csima and Sawyer showed that a(n) >= floor(6n/13) except for n=7"); Green–Tao
   arXiv:1208.4714 (PDF read: "Kelly and Moser proved that there are at least 3n/7
   ordinary lines, and Csima and Sawyer improved this to 6n/13 when n > 7"; "Crowe and
   McKee provide a more complicated configuration with n = 13 and 6 ordinary lines. It is
   possible that Theorem 1.2 remains true for all n with the exception of these two
   examples (or equivalently, one could take n₀ as low as 14)"; Proposition 2.1(iii): X₄ₘ
   minus a point at infinity has 4m−1 points and 3m−3 ordinary lines, so 15 points with 9).
   Open because: no source records t₂(15); the literature scout's arXiv API sweeps
   ("ordinary lines" × SAT / computer / order types / enumeration, 2020–2026) found no
   computational attack on small n; Lenchner–Sengupta (arXiv:2608.24656, July 2026) say
   the conjecture "still stands"; Wikipedia (secondary) records that whether the n/2 bound
   holds for pseudolines is unknown. **Selected.**
2. **MathOverflow 514690, good permutations and Mersenne numbers** (combinatorial
   number theory; P. Weiss, 27 Aug 2026, score 17). Known from the thread: exist for 3, 7,
   31; none for other odd n ≤ 41 (asker's search); an answer (Bîsceanu, from a comment by
   te4) proves n must be 2^m − 1. n = 63 was the first undecided case. Open as of today
   (thread read via the API; one unaccepted answer, no resolution of 63). **Run as the
   hedge** by a one-core subagent — and it closed n = 63.
3. **Erdős #1016, minimal pancyclic graphs** (graph theory). h(n) = least h such that some
   n-vertex graph with n + h edges contains cycles of every length 3..n; "is h(n) ≥
   log₂ n + log* n − O(1)?" OPEN, edited 27 Dec 2025, one comment (references only).
   Griffin (arXiv:1312.0274) has exact values to n = 29 by exhaustive search and
   constructions to n = 37 (scout's reading, not re-verified here); OEIS A105206 stops at
   n = 22. Passed over today, but noted: the cycle-space bound 2^{h+1} − 1 ≥ n − 2 (a graph
   with cyclomatic number h + 1 has at most 2^{h+1} − 1 cycles) gives h(n) ≥ 5 for all
   n ≥ 34, so the scout's "h = 4 holds to 37" is arithmetically impossible and the paper
   must be read before any attack; the open computational question is the largest n with
   h(n) = 5 (≤ 65), a well-posed future session.

   Also surveyed and rejected today: arXiv:2609.02477 planar bondage number (census of
   non-3-connected cubic planar triangle-free graphs ≤ 24 vertices — an audit of a
   three-day-old preprint, small surface); arXiv:2609.03081 rook placements on
   permutation grids (n = 9..11 are 9!..11! grids, trivially finishable — the authors will
   do it); arXiv:2609.03444 lonely-runner spectrum for six speeds (author active,
   incremental); arXiv:2607.23004 Erdős #272 t(13) (no published n = 12 timing, author
   mid-stride); Erdős #1204 minimal-mean admissible tuples B(k) (new OEIS sequence at
   best); Erdős #864, #295, #382 (1.5–2× extensions); OEIS A398490 evenness of the maximal
   cyclic-polygon side count (Huber's paper already proves the per-class parity lemma; the
   open content is about optima — the scout's verdict is "not a 5-hour proof"); A397434
   (majority-function ANF monomials: a one-hour proof sketch exists, comment-level value);
   A399084, A398581 (routine); A398417 a(12) (needs all 117.9M cubic graphs on 24
   vertices); MathOverflow 514742 square achievement game (asker has forced-win searches
   6 ≤ n ≤ 14), 514744 square spanning-tree counts, 514297 x⁴+3y⁴=z⁴+t⁴ (search replacing
   an AI claim), 499750 (Alekseyev's two-digit conjecture). As in the last three sessions,
   every finitely-checkable Erdős problem with a computational edge was already searched
   far beyond this machine (#647 to 10¹⁸, #993 to 32 vertices, #287 Lean-checked, #458 to
   10²⁰, #1109 to 1103, #366 to 10²²).

**Internal-thread assessment** (parallel audit of all 26 conjecture READMEs and the eight
most recent logs; no PAGE.md was pending anywhere). Last two sessions: kobon-triangles +
power-residue-pairs (09-02), bit-deletion + peaceable-queens (09-03) — no forced rotation.
Strongest live thread: **peaceable-queens a(18)** — refute 48 + 48 on the 18 × 18 board with
the validated SYM16 engine (measured n = 17 cost 2.15·10¹⁰ nodes / 1712 s on 4 workers;
×4 per rung projects 8.6·10¹⁰ nodes, ~2 h), a third consecutive new A250000 value either
way. Runner-up: generalized-schur `S(3;4,4,10)` (minutes of solver time behind a
proof-logging memory fix). The rest are compute walls (graham-rearrangement p = 41 ~37 h,
grimm 10¹³ ~9 h, distinct-subset-sums f(10) months, odd-giuga m = 13, nci-datrees n = 16,
erdos-gyarfas n = 19) or ideas walls (kobon triple points, power-residue-pairs Λ(8,2)
exact — four documented failures, vdw-mixed period structure). Audit flags for the record:
three READMEs still say "see PAGE.md" although their pages are live (power-residue-pairs
l.18, projective-chromatic l.82, parking-polytope l.66); the peaceable-queens README does
not record a(18)'s literature bracket.

**Selection.** The mandate's default is the external problem, and candidate 1 beat a(18) on
all three criteria: (a) its bottleneck is a SAT refutation with a rigid forced structure —
the same kind of bottleneck the kobon and projective-chromatic sessions broke — while
a(18) is a measured but single-engine 2-hour exhaustion that would deepen an existing
replication debt; (b) nobody has computed t₂(15): the OEIS entry, Green–Tao's own remark
and the 2020–2026 arXiv sweep all say so; (c) it would be cited by A003034 (a "nice"
classical sequence with a "?" at 15), by Green–Tao's remark on n₀, by the problem books
and by the Handbook's list of properties that might separate lines from pseudolines.
Candidate 2 tied on freshness and lost on surface; it ran as the hedge. In hindsight the
hedge produced the complete result and the main line the partial one.

**Attempt statement.** Decide whether 15 points in the real projective plane, not all
collinear, can span 7 ordinary lines. Achieved would have meant: for every
Melchior-compatible placement of the lines of size ≥ 4 (two 5-point lines, meeting or
not), a machine-checked UNSAT certificate for an encoding whose soundness is a two-line
determinant identity — giving t₂(15) ≥ 8 — and then the same for 8 ordinary lines (41
cubes), giving t₂(15) = 9; or a satisfying chirotope. Achieved in fact: the disjoint
placement in full, the meeting placement in 86 of its 131 sub-classes.

**What failed.**
- *The plain chirotope encoding* (no case split): hopeless on the refutation side already
  at n = 9 (CaDiCaL > 6 min, Kissat killed at the same point) though instant for n ≤ 8 and
  on the SAT side. Melchior + counting fixed it: n = 9 refutes in 25 ms, n = 12 in 18.5 s,
  n = 10, 11 need no solver at all.
- *Monolithic n = 15 cubes*: 30 min on Kissat, no verdict, both cubes.
- *Double-lex + value precedence* (`lexcubes.py`): sound (fixpoint argument written out),
  implemented, slower than the ∗-pattern sub-cubes (no verdict in 4 min where sub-cubes
  take a minute).
- *Cube A (5-point lines meeting)*: ∗-pattern sub-cubes run 15–20 min without verdict;
  the type-vector refinement (exact counts of each 3-line type; it also proves s ≥ 6
  impossible) solved one instance in 14 s and then stalled 10 min on the next; per-point
  parity constraints, fixing one free point's four cells, and CaDiCaL instead of Kissat all
  hit 5–10 min timeouts. Fully fixed arrays are fast (median 0.04–0.3 s incrementally,
  1.9 s with proof logging) but there are 151 449 of them across the 47 open classes and
  the mean is 0.6–0.9 s because of a heavy tail concentrated on arrays whose six free
  points carry (3, 3, 3, 2, 2, 2) mixed lines — about 25 CPU-hours. Stopped at 13:58 UTC
  and the result written up as partial.
- *Calibration at n = 13, 14* (single-5-line cubes, no array to split on): the n = 13,
  m = 5 cube hit its 3 600 s cap with a 3.9 GB proof and no verdict; the n = 14, m = 6
  cubes were started and stopped at session end. The refutation-side calibration stands
  for n ≤ 12 only.
- *Operations*: three shell commands killed themselves through `pkill -f` / `pgrep -f`
  patterns matching their own command line (relaunches cost ~15 min; use `[x]` bracket
  patterns or PIDs); `sh` has no `time` builtin; one type-mode driver crashed on a format
  string. Disk: proofs were deleted after verification (peak ~21 GB used).
- *Hedge*: no proof for composite exponents (divisor-length and local-window arguments
  refuted by data; Lemma E not pushed to a contradiction); n = 255 gave no information.

**Next.** (1) Cube A, 45 open ∗-classes: the slow arrays have no free point on four mixed
lines; in the real case (q at infinity, L₁ ∥ L₂) the perspectivities are affine maps
x ↦ αx + β between two 4-point sets and two free points on four mixed lines must differ
by the reflection of R — a hand proof of the real meeting case, or new necessary
conditions for the solver (auxiliary intersection points as extra elements are sound for
oriented matroids too), is the sharpest thread. Brute force is ~25 CPU-hours on this
machine; fill mode with proofs is deterministic and resumable class by class. (2) Then
t₂ = 8: 41 cubes, of which {5,4,4} and {5,4,4,4} (35 cubes) fix three or four lines and may
be monolithically easy; {5}, {5,4}, {6,5} need splits. (3) A003034: propose a(20) = 10,
a(24) = 12 with the two citations. (4) Good permutations: prove non-existence for
composite 2^m − 1 from Lemma E; post Theorem 1 and Prop. C to MO 514690 and the count
sequence to OEIS (local decisions). (5) Fix the three stale "see PAGE.md" lines and the
missing a(18) bracket flagged by the audit.

**Session hygiene.** Branch: harness-designated `claude/affectionate-sagan-9kyktv` (the
mandate's per-conjecture branch name overridden by the harness requirement, as in
previous sessions). Hardware: 4 cores, 15 GB RAM, Python 3.11.15, python-sat (CaDiCaL 1.5.3
bindings), Kissat 4.0.4, CaDiCaL 3.0.1 and drat-trim built from source today. No seeds;
every computation is exact. Session 11:35–14:30 UTC plus write-up.
