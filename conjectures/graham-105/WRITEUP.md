# Session writeup — 2026-08-14 — Graham's 105 problem

The narrative, including what went wrong. Numbers here are the session's
own; labels per repository convention.

## How the target was chosen

The scheduler's mandate: survey outside the repository first, three
candidates across at least two subfields, then attack whichever survives
vetting best. Three subagents ran the vetting concurrently with early
engine work: one on this problem's exact computational frontier, one on
discrete-geometry/graph candidates (no-three-in-line — dead for a 4-core
box, the 2025–26 wave took every reachable rung to n = 70+72; C4-free
subgraphs of Q9 — genuinely attractive, vacant ledger row, kept as
runner-up), one on Erdős's ternary powers of 2 (frontier 2·3^45, Saye
2022 — out of reach) and Ankeny–Artin–Chowla (disproved 2024 — struck
from consideration; the slate must be problems that are actually open).

The 105 problem won on the mandate's criteria: the bottleneck is pure
enumeration, the ledger is unambiguous (OEIS A030979 + erdosproblems
#376), and the beneficiaries are identifiable (Thompson's census,
Pomerance's heuristic discussion, Graham's 1155 remark).

## The wrong-frontier detour, in full

The OEIS display line for A030979 ends at 24991943715007537 ≈ 2.5·10^16,
and the session's first hours were spent building a bottom-up engine on
the assumption that this was the known frontier: a Gray-code walk over
sums of distinct powers of 3 (the base-3-valid integers), staged
mod-5^8/mod-7^6 byte-table filters, 32768 resume-safe ascending tasks
covering [0, (3^45−1)/2 ≈ 1.48·10^21], ~2.3 s per 2^30-leaf task. It
validated beautifully: brute force with literal math.comb gcds at the
bottom; Python DFS ≡ C recursive ≡ C Gray grid at 10^8, 10^12, and over
the entire display range (where it re-found all 23 displayed terms and 20
more just above them — the first hint the display was not the frontier);
leaf counts equal to a digit-DP closed form, exactly, per task.

Then the literature agent reported the b-file: **complete up to 10^70**,
1374 terms, Thompson, Nov 2015. The campaign in flight was a replication
of the bottom 10^-49-th of the known range. Decision: stop at a clean
ascending prefix — 2140 tasks, complete below 36,647,386,166,054,954,105
(> 3^41, i.e. covering the range attributed to Alekseyev's 2008
computation) — and keep it as one leg of the verification web. Cost of
the wrong assumption: about two hours of wall clock. The lesson is
step-2 discipline: an OEIS display line is not the extent of knowledge;
the b-file line is, and it must be hunted down before an attack is sized.

## The right algorithm

The terms have density ~N^0.026, so the search must visit only what
survives. Fixing base-3 digits from the top, a prefix confines every
completion to an interval of width (3^(L−d)−1)/2; above the scale of that
width, the base-5 and base-7 digit strings of everything in the interval
are one of two consecutive strings (Q and Q+1), and if both violate the
digit caps the subtree is dead (NOTE Lemma 2). That prune keeps the tree
within a constant factor of the output: measured, ~125–126 nodes per term
at every rung — a constant that became one of the session's quiet
self-checks.

Thompson's entire 10^70 range costs 0.7 s in the *Python* implementation
of this. That number is the whole story of the detour: the bottom-up
engine was a good implementation of the wrong algorithm.

The C production engine carries the prefix as digit arrays in bases
5/7/11 simultaneously (add/subtract precomputed digit arrays of 3^k with
exact carries; no bignum library, no division in the hot path), maintains
counts of over-cap digits above the moving thresholds, and decides the
Q/Q+1 test in O(carry run). A deliberate simplification: the straddle
refinement (only consider Q+1 when the interval crosses a b^e boundary)
was measured at 1.25× node savings and dropped so that the C and Python
engines implement *identical* logic — they agree node-for-node, which is
worth more than 20% speed.

Three real bugs were caught by the planned gates before any production
run: a wrong-stride array cast that misindexed the base-7 threshold
comparison (would have mangled e_7 tables), task prefixes mis-decoded
when the split depth was not a multiple of 4 (would have silently skipped
subtrees in parallel runs — the kind of bug that fabricates a census),
and a missing node-reconciliation path (needed to prove task-mode ≡
full-mode). The fixed engine then matched the Python reference exactly —
nodes, terms, three checksums, term lists — at L = 35, 148, 200, 250,
300, and the 4-worker task mode reconciled with full mode at L = 300 to
the last node (36,417,860 + 13,037 taskgen = 36,430,897).

## The runs

Ladder, full-mode: L = 148 (1374 terms — Thompson's count, from scratch,
matching the b-file exactly including a(1) = 0), 200, 250, 300, 350, 400,
500; then the composite task-mode campaign for L = 600. Final:
**585,823,270 terms below 3^600**, 73.9 billion tree nodes, 12.5
core-hours for the whole ladder, the nodes-per-term constant pinned at
126.16 at every height it was measured.

## What the data revealed

The plan was "extend the census and tabulate G(N) against the N^0.02595
heuristic". The tabulation turned out to be the discovery. The counting
function does not creep — it detonates. Only 82 of the 601 base-3
lengths carry any terms at all. The interval [3^474, 3^530) — nearly 27
decimal orders of magnitude — contains not a single term (a certified,
exact statement), and then length 531 alone contributes 39 million. Four
of the five biggest bursts sit at lengths 564–600, carrying 82.6% of the
entire census. The independence heuristic, which predicts tens of
millions of terms inside that desert, is qualitatively wrong locally
even as its global exponent survives (fit 0.0248 vs predicted 0.02595
across 240 orders).

The mechanism is visible in the geometry: a term of length k is confined
to n/3^(k−1) ∈ [1, 1.5), so its leading base-5 and base-7 digit blocks
are dictated by the fractional parts of (k−1)·log_5 3 and (k−1)·log_7 3
— two incommensurate rotations. Where both land well, a burst; where
either lands badly and the cascade compounds, a desert. Turning that
picture into predicted burst positions is the sharpest question the
session leaves open (NOTE §7), and the first max-mode probes were the
right tool at the right moment: when the histogram showed 21 consecutive
empty lengths, three millisecond-scale max queries at intermediate
heights confirmed the desert independently before it was believed.

## The task-skew fix

The depth-130 split of the L = 600 tree has a design flaw: task 0, the
all-zero prefix, is the entire [0, 3^470) subtree — by itself a complete
L = 470 census, hours of single-threaded work while the other workers
drain thousands of small tasks. The fix used the split's own structure:
because the pruning thresholds satisfy W(600, 130+d) = W(470, d), the
task-0 subtree *is* the L = 470 tree, node for node and value for value.
So task 0 was removed from the top split (its class-0 worker restarted at
task 4) and run as its own depth-130 sub-campaign of 4906 subtasks —
`merge600.py` composes the two campaigns and checks the accounting
identity nodes(600) = taskgen(600) + Σ split tasks 1..3753 + taskgen(470)
+ Σ subtasks, the same identity validated against a monolithic run at
L = 300.

## Session hygiene, honestly

- A self-matching pkill killed the session's own shell mid-migration —
  the *same* failure the 08-13 log recorded. The resume-safe task design
  absorbed it. The pattern-with-brackets idiom is now in both engines'
  drivers.
- The Python L = 300 anchor was left running long after the C engine had
  made it redundant; killed. Python's role is validation, not production.
- The Result section of the daily log was drafted, at one point, with
  projected numbers for runs still executing. Caught within minutes and
  replaced with an explicit "to be filled from data only" skeleton — but
  it happened, and the fact that it happened is worth recording: the
  pressure to narrate a finished result before it exists is the exact
  failure mode the claim discipline exists to block.

## What the session did not do

- No new upper or lower bound on anything: the infinitude question is
  untouched, as it must be by computation.
- No claim of novelty for the enumeration *method*: interval-pruned
  digit searches are folklore (Thompson presumably did something similar
  in 2015; his code and cost are unpublished). The novelty claim is
  confined to the range, the 1155 verification height, the count table,
  and the public, reproducible, cross-verified form of the whole thing.
- No OEIS submission from the sandbox (no access); the b-file-style
  extension to 3^200 is committed here for a later session to submit.
