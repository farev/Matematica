# 2026-09-18 — leech-tree-labelling (Leech's tree-labelling problem, OEIS A007187, Guy UPINT C10)

**Target.** New external problem, per the standing mandate. Leech (1975) asked
for the largest k = a(n) such that some tree on n vertices with positive integer
edge weights realises every integer 1, 2, …, k as a path sum (the covering
relative of the perfect "Leech tree" problem, where the C(n,2) path sums must be
exactly 1..C(n,2)). OEIS A007187 lists a(2..10) = 1, 3, 6, 9, 15, 20, 26, 34, 41
with keywords `hard, more`, and the only statement beyond n = 10 is the unsigned
comment "a(11) >= 48, a(12) >= 55"; Guy's *Unsolved Problems in Number Theory*
§C10 is the reference. Nothing past n = 10 has been decided since the 1975
paper, as far as a same-day literature check could establish (details below).
Chosen because the excess budget (only C(n,2) − k pairs may be wasted) turns the
search into a near-Leech-tree search, and Ghodsi's order-18 Leech-tree
nonexistence proof posted yesterday (arXiv:2609.20492) gives an
exact-cover pruning idea that transfers, budget and all. What counted as
success: a(11) determined exactly with a checked witness and an exhaustive
refutation, a(12) if it fell too, and the ladder a(2..10) re-derived from
scratch as the positive control.

**Result.** [PENDING — filled at the end of the session]

**Connectivity (checked 07:40 UTC).** arxiv.org reachable via WebFetch
(math.NT and math.CO listings dated today, abstracts; PDFs via curl and
extracted locally with pymupdf). oeis.org reachable via WebFetch today
(search pages and entries, `/internal` format). erdosproblems.com reachable
via WebFetch (front page: 1220 problems, 586 solved; tag pages). mathoverflow.net
blocked to WebFetch ("unable to fetch"); reached through the Stack Exchange API
with curl by the MathOverflow scout (363 questions since June screened). All
four consulted live today. pip reachable (numpy, python-sat 1.9.dev15, pymupdf
installed into the sandbox). JSTOR (Leech's 1975 *Monthly* note) and Guy's book
are not reachable, so both are cited (secondary), through OEIS and Ghodsi.

**Candidate slate** (three externals across three subfields, each checked
against a live source today; four scouts ran in parallel — OEIS, Erdős
database, MathOverflow via the API, and the internal audit — with their full
reports in the session scratchpad):

1. **OEIS A007187, Leech's tree-labelling problem** (graph labelling /
   combinatorics). Statement above. Source: https://oeis.org/A007187 and
   https://oeis.org/A007187/internal (2026-09-18): terms through n = 10 only,
   the unattributed comment `a(11) >= 48, a(12) >= 55`, references Guy UPINT
   C10 and Leech 1956/1975, keywords `nonn,hard,nice,more`; no b-file, no
   link to any computation. A web search for the covering variant at n = 11
   found only the perfect-Leech-tree literature (Székely–Wang–Zhang 2005,
   Calhoun–Ferland–Lister–Polhill 2007, Varghese–Lakshmanan–Arumugam 2020,
   Ghodsi 2026), none of which touches a(n). Open as far as I can tell; the
   1975 paper itself is (secondary). **Selected.**
2. **Georgiou, arXiv:2609.19536 (posted yesterday): exceptional sets for
   k-tile incomparable tilings of squares** (discrete geometry). He proves
   27 is the smallest side of a square tiled by pairwise incomparable integer
   rectangles (Croft–Falconer–Guy Problem C5) and lists in §5, as untouched:
   "For each k ≥ 7, exactly which n admit a k-tile incomparable tiling of
   the n × n square? Croft, Falconer and Guy assert that for each such k
   only finitely many n fail […] we have not found the exceptional sets
   recorded anywhere." His computations settle only k = 7, n ≤ 27; he
   exhibits tilings for n = 28..31. A day-old, compute-shaped question with
   an OEIS-ready answer (which n, minimal tile count per n). Passed over
   today only because the author is plainly mid-stride on the same code base
   and because candidate 1 is older and better documented; it is a good next
   target.
3. **Erdős #366** (number theory, https://www.erdosproblems.com/366, VERIFIABLE):
   "Are there any 2-full n such that n+1 is 3-full?" Known examples in the
   other orientation 8/9 and 12167/12168; the page's frontier "no other
   examples for n < 10^22" is inherited from a 2011 b-file of consecutive
   powerful pairs, not a dedicated search; abc implies finiteness (comment,
   Apr 2026). A dedicated 3-full enumeration to ~10^26 is a few hours on four
   cores. Passed over: a null result citable mainly through the problem page.

   Also surveyed and rejected (scout reports): MO 515241 (minimum rank of
   Latin squares; ideas-bound), MO 514920 (characteristic polynomials of
   binary strings; data-rich but a formula is the ideas part), MO 513565
   (a poset conjecture implying union-closed; a counterexample hunt),
   MO 512461 (nonnegative Littlewood polynomials; certified recount only),
   A397578/A397554 (a(6) is a free certified term, a(7) needs hours),
   A397315 (Kagey's Problem 001; the author keeps a pre-registration ledger),
   A399620 (monochromatic rectangles; 9 × 9 optimality unpriced),
   A399491/A399755 (a one-page proof of a Pell-equation converse; low ceiling),
   A399793 (its stated conjecture is refuted by its own data), Erdős #261
   (TUZ 2020 greedy to 10^6; range extension), #1108 (powerful sums of
   factorials to 10^25; range extension), #336 (h(4) ∈ {10, 11}; ideas),
   Ghodsi's next Leech-tree order 25 (his order-18 search took 8.6·10^9
   nodes; order 25 is out of reach for a session), and Chen–Chen–Qi's
   z_SL = z_RL question (arXiv:2609.20071; niche).

**Internal-thread assessment.** The audit read every "Known defects and open
threads" section, every `**Next.**` line on main, and the branch-only logs.
Strongest thread: generalized-schur, "climb (3,3,12) [Conjecture A predicts
S(3;3,3,12) = 95], then (3,3,13)/(3,3,14) and the eight queued climbs", each
minutes with the existing certified pipeline; it would change the row from
eleven to twelve-plus new exact values. Runners-up: ordinary-lines cube A
(t₂(15) ≥ 8; 19–28 h of 4-core wall with proof logging — does not fit) and
grimm to 10^13 (8–9 h; fits only barely, modest citation). Peaceable queens
a(19) (13–16 h), graham-rearrangement p = 41 (days), good-permutations
n = 127 (≥ 9 h per slice) and nonrepetitive-lattices (last session) were
excluded on their own recorded numbers.

**Selection.** Scores (a) compute-breakable / (b) already done? / (c) who
cites. A007187: (a) yes — a budgeted version of the forced-least-missing-
weight recursion, sized by the positive control on n ≤ 10; (b) no trace of
any computation past n = 10 in OEIS, the Leech-tree papers or the web; (c)
OEIS (new terms of a `hard, more` sequence), Guy C10, and the Leech-tree
authors (Ghodsi 2026, Varghese et al. 2020). Georgiou's exceptional sets:
(a) yes, (b) day-old and the author is active, (c) Georgiou/CFG. Erdős #366:
(a) yes, (b) no dedicated search on record, (c) problem page only. Internal
generalized-schur: (a) yes, (b) no, (c) Ahmed–Schaal readership, but an
incremental row change. The default goes to the external problem, and A007187
wins on (b) and (c): a fifty-year-old value nobody has computed beats a
twelfth Schur value. Attempted result: **a(11) exactly**, with a
checker-verified witness for the lower bound and an exhaustive, reproducible
refutation for the upper bound; a(12) as a stretch.

**What failed.** [PENDING]

**Next.** [PENDING]
