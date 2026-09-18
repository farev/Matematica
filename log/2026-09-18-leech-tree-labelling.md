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

**Result.** **CERTIFIED — a(11) = 49**, the first new term of OEIS A007187
since Leech's 1975 table, one more than the bound "a(11) ≥ 48" the entry has
carried unattributed. Lower bound: the tree (0,1,1) (2,3,1) (0,4,2) (5,6,4)
(3,6,5) (5,7,7) (6,8,8) (5,9,11) (2,10,22) (0,3,24), whose 55 path sums are
1..49 with 1, 11, 23, 25, 26, 39 doubled (independent checker; four
witnesses in all, one per worker). Upper bound: exhaustive budgeted search
refuting k = 50 in 1 400 728 816 nodes over four worker prefixes (259–304 s
each), after refuting k = 55..51 (2.4 M, 26.5 M, 27.9 M, 121 M, 493 M
nodes). Positive control: the same program re-derives a(2..10) = 1, 3, 6, 9,
15, 20, 26, 34, 41 from scratch (witnesses checked, refutations with
recorded node counts, n = 10 in 15 s). **CERTIFIED — a(12) ≥ 57** (OEIS:
≥ 55), witness found in 95 s and checked; hunts at 58 and 59 (30 and 25 min)
found nothing; **a(12) ≤ [PENDING]** by exhaustive refutation of
k = [PENDING] ([PENDING] nodes). **CERTIFIED — a new sequence:** with all
path sums required distinct (the maximum over trees of order n of the Leech
index of Varghese–Lakshmanan–Arumugam 2022), the values for n = 2..12 are
1, 3, 6, 9, 15, 20, 25, 30, 37, 45, 47, not in OEIS; witnesses checked with a
distinctness option, every larger k refuted, and every value through n = 11
reproduced by a deliberately minimal second engine (n = 12: [PENDING]);
n ≤ 7 in both modes confirmed by brute force over all shapes and weight
vectors. **PROVED:** the six pruning lemmas the searches rely on (weight
window, monotone excess, budgeted parity after Taylor, edge load, budgeted
whole-block bounds after Ghodsi 2026 Thm 4.1, isomorphic-component
symmetry), NOTE §2. Caveats: the n = 11 and n = 12 repeat-allowed
refutations are single-engine (two variants of the engine agree to the
node; the SAT engine replicates n = 7, 8 fully and 17/47 shapes of n = 9);
Leech 1975, Guy §C10 and the two Leech-index papers were not readable
(paywalled) and are cited (secondary). New directory
`conjectures/leech-tree-labelling/` (README, NOTE, WRITEUP, PAGE.md,
OEIS_DRAFT.md, code, witnesses, run records); index row added.

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

**What failed.**
- Two global-buffer bugs in the C engine (a `static` undo buffer; candidate
  lists and canonical strings shared across recursion depths). Both were
  invisible to a single verdict and caught only by re-running the whole
  known ladder and by comparing node counts between two engine variants
  (which now agree exactly: 3 247 390 nodes at n = 10, k = 43). The stale
  canonical strings could in principle skip a needed branch; in fact they
  had only weakened the symmetry rule at n ≤ 10.
- The exact block cover as a general rule: cut nodes 8× at n = 9 but cost
  150 µs per node; only worthwhile near the leaves (≤ 4 components,
  remaining budget ≤ 2, capped and fail-open).
- The first distinct-sum mode forbade repeats only among values ≤ k; the
  checker's distinctness option rejected the n = 10 witness (39 and 57
  repeated above k). Fixed by tracking the at most B large values
  individually. A related 128-bit overflow of the sumset mask, harmless in
  repeat-allowed mode (lost sums are excess anyway), was guarded in
  distinct mode; it never triggered.
- The SAT engine (one CNF per shape, unary adders) is correct but slow:
  1–3 minutes per shape at n = 9, so it cannot replicate n = 11.
- Witness hunts at n = 12, k = 58, 59: nothing in 30 and 25 minutes; the
  refutation of 58 (budget 8) is projected at ~10¹¹ nodes, a day of four
  cores, so a(12) stays open today.
- Primary sources: Leech 1975 (JSTOR), Guy §C10, Varghese et al. 2022 and
  Lakshmanan–Eldho 2024 are paywalled; abstracts only.

**Next.** (1) a(12): refute k = 58 with the engine split over many prefixes
(~10¹¹ nodes; a day of four cores, or an idle-time job), or find a witness
at 58 with a randomised search order; the distinct-sum value at n = 13
(78 pairs) should be minutes. (2) A second independently written engine at
n = 11, k = 50, to lift the single-engine caveat; the minimal engine
`plain_search.c` is the natural base but needs the block bound to finish.
(3) Submit a(11) = 49 and the new distinct-sum sequence to OEIS
(`OEIS_DRAFT.md`), and write to Varghese–Lakshmanan–Arumugam / Ghodsi, whose
Leech-index and whole-block ideas this extends. (4) Georgiou's k-tile
incomparable-tiling exceptional sets (candidate 2) remain a good target.
