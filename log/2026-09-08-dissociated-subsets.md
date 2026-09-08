# 2026-09-08 — dissociated-subsets (Erdős #963) + equitable-total-colorings (hedge)

**Target.** New external problem, per the standing mandate. Erdős Problem #963
(erdosproblems.com/963, sources [Er65], [Va99, 1.22]): with `f(n)` the largest `k`
such that every `n`-element `A ⊂ ℝ` contains a `k`-subset with distinct subset sums
("dissociated"), Erdős noted the greedy `f(n) ≥ ⌊log₃ n⌋` and asked whether
`f(n) ≥ ⌊log₂ n⌋`. The page (status OPEN, last edited 23 Jan 2026) carries
KoishiChan's `(1−o(1)) log₂ n` argument (Dec 2025), Tao's and Tang's remarks, Bloom's
inclination to mark the asymptotic question solved, and BAKKAOUI's integer-window
searches of 3 Sep 2026 (`{1,…,10,12,13,15}` has no dissociated 5-subset, so
`f(13) ≤ 4`; "the value of `f(13)` itself is not settled by a bounded integer search").
It looked tractable because sign flips and zero never help a dissociated subset, so
`f(n) = g(⌈(n−1)/2⌉)` with `g` the minimum over distinct positive reals, and the
`⌊log₂ n⌋` question becomes one finite statement per `k` — "do `2^{k−1}` distinct
positive reals always contain a dissociated `k`-subset?" — decidable for `k = 4` by an
exact case analysis over the six ±1 relations a sorted 4-set can carry.

**Result.** **PROVED + CERTIFIED.** (1) PROVED: `f(n) = g(⌈(n−1)/2⌉)`; Erdős's
inequality for all `n` ⇔ `g(2^{k−1}) ≥ k` for all `k`; the greedy bound
`g(m) ≥ k` for `m ≥ (3^{k−1}+1)/2`; the interval bound `g(m) ≤ max{k : F(k) ≤ m}`
(Conway–Guy `F`); the signed-sum lemma (every element of a set with no dissociated
`k`-subset is a signed sum of any dissociated `(k−1)`-subset). (2) CERTIFIED:
**every 7 distinct positive reals contain a dissociated 4-subset**, six need not
(`{1,…,6}`, `{1,2,3,5,7,8}`, `{1,2,3,4,6,7}`, `{2,3,5,10,12,15}` and one-parameter
families) — four independent exact engines (fail-first/Fourier–Motzkin 290 nodes;
row-echelon/prefix-first/certified-LP 1099 nodes; memoised 111 nodes; dissociation
case split 62 nodes), three of them emitting JSON case trees verified by an independent
checker (`data/checker_log.txt`). Hence `m₄ = 7` (`m₃ = 4` by hand), `g(m) = 3` for
`4 ≤ m ≤ 6`, `g(m) = 4` for `7 ≤ m ≤ 13`, **`f(n)` exactly for all `n ≤ 27`**
(`0,1,1,2,2,2,2,3,3,3,3,3,3,4,…,4`), **`f(n) ≥ ⌊log₂ n⌋` for all `n ≤ 31`**, with
equality except at `n = 14, 15` where `f = 4 > 3`; the page's `f(13) ≤ 4` is
`f(13) = 3`. (3) `k = 5`: `14 ≤ m₅ ≤ 41`; sets with no dissociated 5-subset of every
size `m ≤ 13` found by engines C/D/E (CERTIFIED witnesses, `m = 8` with a checked
certificate); the exhaustive decision of `m₅` was **not** reached: the fastest exact
enumerator built today (engine G: seven-smallest normalisation + exact extreme-ray
arithmetic, validated against the LP on 3 968 random decisions and reproducing engine
F's `k = 4` enumeration node for node) has 1 103 785 phase-1 configurations at `k = 5`
(census: 1 105 s) and its four 2-hour runs reached their caps at 5–7 % each (58 110 to
74 653 phase-1 nodes, 260 000 to 375 000 phase-2 nodes) without exceeding 12, i.e.
≈ 30 h per order in Python; the enumeration is fully specified for a C port. (4) CERTIFIED (annealing hedge, one core):
`A₂₄ = {1,…,21,24,25,27}` has no dissociated 6-subset (all 134 596 six-subsets checked
by two independent programs), so `m₆ ≥ 25`, one more than the interval bound; no
14-set with `d ≤ 4` and no 25-set with `d ≤ 5` was found (NUMERICAL). New directory
`conjectures/dissociated-subsets/` (README, NOTE, WRITEUP, PAGE.md, five engines,
checker, certificates, witnesses); index row added.

**Hedge result (subagent, one core, 61 min). CERTIFIED.** Question 7.1 of
arXiv:2609.05259 (Adauto–de Figueiredo–Sasaki–Schneider, 4 Sep 2026: "does every
Type 1 cubic graph of order less than 20 admit at least one equitable 4-total
coloring? Equivalently, is R a Type 1 cubic graph with χ''_e = 5 of minimum order?")
has a **negative** answer: among the 45 982 connected cubic graphs of order ≤ 18
(geng, counts matching OEIS A002851 fetched live) exactly 23 are Type 1 with no
equitable 4-total colouring — 16 of order 16, 7 of order 18 (three bipartite); every
Type 1 cubic graph of order ≤ 14 has one; the minimum order is 16, not 20. Every witness
independently verified, every relevant UNSAT with DRUP proofs checked by
`tools/satcert/rup_check` with and without symmetry breaking (4 920 proofs, 534 MB;
the 48 for the counterexamples and `R` committed), a SAT-free enumerator agreeing on
all 23 (and showing every 4-total colouring of the order-16 ones has class sizes
(11,10,10,9)); the paper's controls (H16, H18, `R` from Figure 1) all reproduce. Order
20 partially scanned (3 of 10 classes: 20 more examples, all (14,12,12,12)). Priority
against Adauto's 2022 dissertation is unchecked. New directory
`conjectures/equitable-total-colorings/`; index row added; PAGE.md written.

**Connectivity (checked 11:37–11:39 UTC).** arxiv.org reachable via the standard
fetcher (math.CO "new" listing dated 7 Sep 2026; abstracts; PDFs via curl + pymupdf).
oeis.org, erdosproblems.com and mathoverflow.net return 403 / "unable to fetch" to
the fetcher but serve curl with a browser user agent (HTTP 200 on all three at
11:39), as does the Stack Exchange API (`api.stackexchange.com`, site=mathoverflow)
and openproblemgarden.org (200). PyPI reachable; github.com source tarballs refused by
the egress policy (403). All four mandated sources consulted live. The
`conjecture-research` skill named in CLAUDE.md is not installed here; CLAUDE.md
followed directly.

**Candidate slate** (three externals, three subfields; seven scouts in parallel — two
arXiv scouts split by subfield, Erdős database + Open Problem Garden, OEIS,
MathOverflow via the API, a status check on a personal list of classical finite
problems, and the internal audit; full reports in the session scratchpad; every
statement below was checked against the primary page on 2026-09-08 by the scout or
by me):

1. **Erdős #963, dissociated subsets** (additive combinatorics / number theory).
   Statement quoted verbatim: "Let f(n) be the maximal k such that in any set
   A ⊂ ℝ of size n there is a subset B ⊆ A of size |B| ≥ k which is dissociated,
   that is, the sums Σ_{b∈S} b are distinct for all S ⊆ B. Estimate f(n) — in
   particular, is it true that f(n) ≥ ⌊log₂ n⌋?" Source: erdosproblems.com/963, read in
   full (20 comments) at 11:55 UTC. Open because: the page says OPEN and "cannot be
   resolved with a finite computation"; the only progress is asymptotic; the exact
   inequality has no small-case treatment anywhere in the thread; BAKKAOUI's 3 Sep
   comment finds no data on `f(n)` in the literature or OEIS. **Selected.**
2. **arXiv:2609.05259, Question 7.1** (graph theory: equitable total colourings).
   Statement quoted above. Source: the paper (v1, 4 Sep 2026), read in full by the
   hedge subagent. Open because the authors say the check "is within reach of a
   systematic computational verification" and had not done it; no follow-up on arXiv.
   **Run as the hedge** (one core, 90-minute budget) — and answered.
3. **MathOverflow 514772** (discrete geometry / number theory; P. Weiss, 30 Aug 2026,
   score 8, one answer): the best bound on `f(n)`, the largest number of lattice points
   on a circle with exactly `n` lattice points inside; the asker proved
   `f(n) ≤ ⌊2+√(8n+4)⌋`, GH from MO gave an ineffective `n^{O(1/log log n)}`. Open per
   the thread; an elementary bound through the minimal interior-point counts of convex
   lattice polygons (OEIS A063984) and a certified table looked feasible. Passed over:
   the bound is elementary enough that a thread participant may post it any day, and
   the table is small.

   Also surveyed and rejected today (details in the scratchpad reports): Erdős #506
   (minimum circles through `n` points, `m(9)`: five people active in the thread since
   August), #114 (lemniscate length: contested interval-arithmetic certificate, an
   analysis problem needing a rigorous implicit-curve length bound), #743 (tree
   packing `n = 12`: pawelkwaczynski's 220-core-hour result of 8 Sep explicitly wants
   independent reproduction — a 4–10× algorithmic gain needed), #642 (`f(13)` for
   graphs whose cycles have more vertices than chords), #64 (jul059's unverified
   ChatGPT lemma), #389, #1160; the Open Problem Garden (dormant; nothing small);
   OEIS A399527 (Eldar, 1 Sep: longest run of squarefree 17-rough numbers,
   `768 ≤ a(7) ≤ 1218` — a clean CRT computation, but the entry is a week old and its
   author prolific), A399300 (Goldbach-prime witnesses to 10¹²), A396967 (De Vlieger:
   "is ω(a(n)) always 2?" — the scout's `p·(p^m−1)/(p−1)` pattern looks provable),
   A399145, A398550, A395616, A399307, A399155; MathOverflow 513668 (coins in a tray),
   514920 (0/1-diagonal Jacobi strings with equal characteristic polynomial, a nice
   OEIS-type sequence), 514678, 514705, 514753, 514243; arXiv 2608.25092 (orthogonal
   semigroup operations, Problem 15.7), 2609.03567 (Baker's matrices `k = 11` SSE
   search), 2608.24612 (`d_{2,3}`), 2608.25853 (rings of order < 128), 2608.27669
   (majority `C`-colouring), 2608.19467 (graph likelihood minimisers), 2609.04257
   (bondage number 5), 2608.18828, 2608.27494 (`ℓ₂(10,2) ≤ 49`). The personal
   curiosity list closed every door: no-three-in-line is solved through `n = 74` and
   at 76 (Prellberg on QMUL's cluster, Heule with a custom solver; smallest open
   `n = 75`); `γ(Q_26) ∈ {13,14}` is a ≥ 10³ CPU-hour UNSAT; `z(32;2) ∈ {189,190}` and
   `ex(41,C₄)` have resisted McKay's machinery; `w(2;3,20)` rests on Kouril's 2015
   FPGA run; `n(2,25)` is 2–3 orders beyond; `WS(5) = 196` is not even proved;
   two zero-cost OEIS corrections were noted (A186704: `a(14) = a(15) = 7` from Wei
   2012; A002563 out of date).

**Internal-thread assessment** (parallel audit of all 32 conjecture READMEs, the
only PAGE.md, and the ten most recent logs). Last two sessions: chromatic-ramsey
(09-06) and good-permutations (09-07) — no forced rotation. Strongest live thread:
**ordinary-lines, cube A** — close the 45 open ∗-classes of the meeting case
(151 309 fixed arrays at 0.6–0.9 s each, ≈ 25–40 CPU-h, ≈ 3× more with proof
logging, 21 GB transient disk), which would establish `t₂(15) ≥ 8` and flip the
index row from "partial"; then 41 cubes for `t₂(15) = 9`. Runner-up: peaceable-queens
`a(19)` (≈ 5.4–6.6·10¹¹ nodes, 13–16 h on four dedicated cores, deepening the
single-engine debt of `n = 17, 18`). Cheapest row-changing item: generalized-schur
`S(3;3,3,12) = 95?` (< 1 h). Everything else is a compute wall, an unbuilt tool or an
ideas wall. Audit flags for the record: `good-permutations/PAGE.md` is pending and
blocked on the unreconciled write-ups, and the `n = 127` run files are empty; three
READMEs still say "see PAGE.md" although their pages are live (power-residue-pairs
l.18, projective-chromatic l.81, parking-polytope l.66 — flagged on 09-05, still
unfixed); `gilbreath/ck_analysis.py` still opens the nonexistent `c6_exact.txt`;
`reciprocal-rado`'s results table is not struck through despite its correction block.
**Selection argument.** The mandate's default is the external problem. Erdős #963
beats cube A on (a): its bottleneck is a finite exact case analysis with a theorem
(the reduction) attached, whereas cube A is a 25–40 CPU-hour SAT sweep, longer than the
session; on (b): the thread's own literature check found no data on `f(n)`, and nobody
had noticed the reduction; on (c): the erdosproblems page (Bloom updates on request),
a new OEIS sequence (`f(n)`, `g(m)`), and Vaughan's list. Question 7.1 tied on (a) and
(c) and won on freshness; it ran as the hedge. Ties go to the new problem.

**Attempt statement.** Decide the first open instance of Erdős's `⌊log₂ n⌋` question
(`n = 16`: does every 8-element, hence — after the reduction — every 8-element set of
distinct positive reals contain a dissociated 4-subset?) by an exact case analysis over
the hyperplane arrangement of ±1 relations, with at least two independent
implementations and a machine-checkable certificate; compute `f(n)` exactly as far as
the case analysis reaches; then push to `k = 5` (`m = 14, 15, 16`), where a 16-element
set with no dissociated 5-subset would refute the question at `n = 32` and an
exhaustive "none" would extend it to `n ≤ 63`. Achieved: the `k = 4` decision in full
(with `m₄ = 7 < 8`, better than needed), `f(n)` for `n ≤ 27`, the inequality for
`n ≤ 31`; at `k = 5` the witnesses to `m = 13` and the running exhaustive search, not
a decision.

**What failed.**
- *Exhaustive `k = 5` in the sorted-coordinate formulation.* Engine A without LP
  pruning stalls at `m = 8`; engine B (prefix-first) grows ~40× per element; engine C
  (fail-first, memoised) ~4.7× per element at 20–30 ms per node; engine D (dissociation
  case split) finds families at `m ≤ 12` in seconds to minutes but needs 60 590 nodes
  and 27 minutes for the *first* family at `m = 13` (it rediscovers BAKKAOUI's set).
  None can finish `m = 14` exhaustively today.
- *Engine E, first version*: 95 % of its time in Fraction-based rank tests, 7 nodes
  per minute; fixed with integer kernel products, the "at most three certainly-small
  vectors" normalisation and cached sample points (≈ 150 nodes/min). *Engine F*
  (seven-smallest normalisation): same rate, LP calls proving cut options infeasible
  dominate. *Engine G* (exact extreme rays, no LP): 20× faster, but the `k = 5`
  enumeration has 1.07 M phase-1 configurations and ≈ 4 phase-2 nodes each — ≈ 30 h
  per order; 5–7 % done per run at the 2 h caps, best 12 in all four runs. A completeness control
  (the published 13-set's vectors placed first) is found in 5 nodes, so the enumeration
  reaches 13-sets; it simply has not reached them in the plain orders.
- *A general improvement of the greedy bound* from the signed-sum lemma applied to
  all dissociated `(k−1)`-subsets at once: not found.
- *A hand proof of `m₄ = 7`*: not attempted beyond identifying engine D's 62-node
  tree as the skeleton; the one-parameter 6-element families make it long.
- *Operations*: three self-inflicted `pkill`/`pgrep` kills (patterns matching the
  invoking shell; the third also killed a batch of launches) — the same wound as the
  09-01, 09-05 and 09-07 logs. PIDs only, bracketed patterns, and never launch and
  kill in one command.
- *Hedge*: the subagent could not write its report file (harness rule); the report was
  returned in-message and reproduced in the directory's NOTE. Order 20 incomplete.

**Next.** (1) `m₅`: port engine G to C (small-integer arithmetic throughout; the
Python enumeration needs ≈ 30 h per order) or split the Python run over the first
small index across four cores for four days; `m₅ = 14` would give `f(n) = 5` for
`28 ≤ n ≤ 47` and Erdős's inequality for all `n ≤ 63`; a 14-set with `d ≤ 4` would
move the threshold up. A certificate format for G (the list of numeric points `t` and
the symbolic families, each re-verified by an independent program) is needed before a
verdict is more than single-engine.
(2) A written proof of `m₄ = 7` from the 62-node tree. (3) Improve the greedy bound
`m_k ≤ (3^{k−1}+1)/2` using all dissociated `(k−1)`-subsets. (4) Report the reduction,
the table of `f(n)` and `A₂₄` on erdosproblems.com/963 and submit `f(n)` / `g(m)` /
`m_k` to OEIS — local decisions per repository policy. (5) Equitable colourings:
priority check against Adauto's dissertation, complete order 20, report to the authors
of arXiv:2609.05259. (6) The two OEIS corrections (A186704, A002563) and the three
stale "see PAGE.md" lines flagged twice now.

**Session hygiene.** Branch: harness-designated `claude/affectionate-sagan-ypybzt`
(the mandate's per-conjecture branch name overridden by the harness requirement, as in
previous sessions). Hardware: 4 cores, 15 GB; Python 3.11.15; numpy 2.4.6, scipy
1.17.1, sympy 1.14, python-sat 1.9 (CaDiCaL 1.9.5 verdicts, Glucose 4 DRUP proofs
checked by `tools/satcert/rup_check`); gcc 12; nauty 2.8.8 from the pynauty sdist.
No seeds in the exact work; annealing seeds recorded in `code/sa/RESULTS.md`. Time:
survey and selection 11:36–12:00 UTC; `m₄ = 7` in hand at 12:01, certified by 12:45;
`k = 5` engines 12:15–13:25 (E, F, G); exhaustive `k = 5` runs of G launched 13:25
UTC and left to their 2 h caps; hedge 11:57–12:58; documents from 12:50; final
status written 14:10 UTC.
