# Ordinary lines — session write-up

## Session 1 — 2026-09-05

### How the problem was chosen

Six scouts ran in parallel over the Erdős Problems database, the newest arXiv listings,
recent OEIS conjectures, MathOverflow and the Open Problem Garden, and the repository's
own threads (details in `log/2026-09-05-ordinary-lines.md`). The idea for this problem
did not come from a scout: while they ran I asked which classical extremal problem in
discrete geometry has a small open case that a SAT solver could plausibly settle,
remembered that the Dirac–Motzkin conjecture is proved only for n ≥ n₀ with n₀
unspecified, and sent a scout to check what is actually known for small n. It came back
with the OEIS table (exact values only to n = 14 and for 16, 18, 22), the Green–Tao remark
that n₀ might be 14, the bracket 7 ≤ t₂(15) ≤ 9 assembled from Csima–Sawyer and Böröczky,
and no computational attack anywhere in 2020–2026 arXiv. That made n = 15 the smallest
genuinely open case of the conjecture in the strong form t₂(n) ≥ n/2.

### The encoding, and the first surprise

The natural abstraction of a point configuration with collinearities is a rank-3
chirotope χ: triples → {−, 0, +}. A first encoder (`chiro_sat.py`) with only alternation,
simplicity, the three-term Grassmann–Plücker sign relations and a cardinality constraint
on ordinary pairs reproduced t₂(5..8) = 4, 3, 3, 4 in under a second each — but the
refutation side at n = 9 (no configuration with ≤ 5 ordinary lines) did not finish in six
minutes with CaDiCaL, and a Kissat run of the plain instance was killed at the same
point. Symmetric UNSAT instances are the classic hard case for CDCL.

### Melchior's inequality as a case splitter

The fix was arithmetic, not solver tuning. Melchior's inequality t₂ ≥ 3 + Σ(k−3)t_k and
the pair-counting identity Σ C(k,2) t_k = C(n,2) leave, for n = 15 and t₂ = 7, exactly one
line-type distribution: two 5-point lines, twenty-six 3-point lines, no 4-point line
(`distributions.py`). Fixing the big lines up to relabelling (`cubes.py`) gives two
cubes: the 5-lines share a point (cube A) or are disjoint (cube B). The same split
reproduces the known ladder instantly on the refutation side: at n = 9 the single cube
(one 5-line) is UNSAT in 25 ms; at n = 10 and 11 there is no admissible distribution below
the known value at all, so t₂ ≥ 5, resp. 6, follows from counting alone; n = 12 (m = 5,
one cube) refutes in 18 s. Positive controls (m = t₂(n)) are SAT in the expected cubes; the
found n = 9 model passes the independent full-axiom check (`verify_chirotope.py`: general
chirotope axiom (B2), 10 three-point lines, 6 ordinary).

### n = 15: monolithic cubes stall, sub-cubes fly — for cube B

Kissat on the two n = 15 cubes (92k variables, 656k clauses each) ran 30 minutes without
a verdict. The structure inside a cube suggested the next split: for a in L₁∖L₂ and b in
L₂∖L₁ the line ab is either ordinary or carries exactly one free point, and each free
point appears at most once per row and column of this 5×5 (cube B) or 4×4 (cube A) array
— a partial Latin square with at most seven holes. Sub-cubing on the hole pattern up to
row/column permutations (260 classes for B, 131 for A) with value precedence on the free
points, and on the two isotopy classes of Latin squares of order 5 for the hole-free case,
turned cube B into 261 refutations of 1.5–540 seconds with drat-trim-verified proofs —
55 minutes of wall time on two cores. Half of the s = 7 classes were known to be void by a
parity argument (Lemma 5.6) before they ran; they refute in 3 s each and were run anyway.

A "double-lex + value precedence" alternative — sound by a fixpoint argument I wrote out
(sorting rows, sorting columns and canonical relabelling all weakly decrease the row-major
word) — was implemented (`lexcubes.py`) and was *slower*: four minutes without a verdict
on the s = 1, 2, 3 instances that the star-pattern sub-cubes settle in about a minute.

### Cube A resists

The same sub-cubes did not work for the meeting case. Its array is 4×4 with six symbols —
loose where cube B's is a Latin square — and the star-free class alone has 411 fillings
up to symmetry. Fixing the array completely ("fill mode", `fillcubes.py`) refutes each
filling in seconds with a checked proof, and that closed the star-free class (Theorem 6.2)
in 45 minutes. But the other 47 feasible classes have 151 449 fillings between them, the
unfixed sub-cubes run for tens of minutes without verdict on both Kissat and CaDiCaL, and
every intermediate idea I tried made things no better: exact type-vector counts (which
are pretty — they show s = 7 impossible in cube B and s ≥ 6 impossible in cube A by
parity), per-point parity constraints (every point lies on an even number of ordinary
lines), fixing one free point's four cells. Incremental solving with the arrays as
assumption sets measured 0.6–0.9 s per array on average, with a heavy tail concentrated on
arrays whose six free points carry (3, 3, 3, 2, 2, 2) mixed lines — the arrays without a
perspectivity defined on all four points of a line. That is 25 CPU-hours for the meeting
case, and the session had four cores and an afternoon.

So the day ends with a certified half: a 15-point set with seven ordinary lines, if it
exists, has its two 5-point lines meeting, between one and five ordinary lines among the
sixteen pairs joining them, and even ordinary degree at every point. Not the theorem
t₂(15) ≥ 8, and the write-up says so at every level.

### What failed

* Plain chirotope encoding without a case split: hopeless already at n = 9 (UNSAT side).
* Monolithic n = 15 cubes: > 30 min without verdict on Kissat, abandoned for sub-cubes.
* Double-lex symmetry breaking: sound, implemented, slower than sub-cubing.
* Cube A: star-pattern sub-cubes (20 min, 15 min without verdict), type-vector refinement
  (one instance 14 s, the next > 10 min), one-symbol fixing (300 s timeout), CaDiCaL instead
  of Kissat (10 min timeout) — all failed to close even the s = 1 class.
* The n = 13, m = 5 calibration cube (a single 5-point line) ran more than 35 minutes with
  a 2.4 GB proof; single-line structures need their own split.
* Three shell commands killed themselves through `pkill -f` / `pgrep -f` patterns that
  matched their own command line; the n = 15 runs were relaunched twice (cost: about
  fifteen minutes). Use `pattern[x]` bracket tricks or PIDs.
* The `time` builtin does not exist in `sh`; use `bash -c` or `SECONDS`.

### Hedge line (subagent): good permutations, MathOverflow 514690

A one-core subagent ran the day's hedge in parallel: it settled the first undecided case
n = 63 of the "good permutations and Mersenne primes" question (no good permutation,
CERTIFIED with two implementations), proved the reduction lemmas and the construction
criterion, and pushed the lemma-free search to n = 43. That work has its own directory,
`conjectures/good-permutations/`.
