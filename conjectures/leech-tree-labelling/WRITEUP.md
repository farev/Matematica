# Session write-up, 2026-09-18: Leech's tree-labelling problem (A007187)

Narrative record, failures included. The presentable statement is
[`NOTE.md`](NOTE.md); the index is [`README.md`](README.md).

## How the problem was chosen

The morning arXiv listing carried Ghodsi's computer-assisted proof that no
Leech tree of order 18 exists (arXiv:2609.20492, 17 Sep 2026). Reading it in
full pointed at OEIS A007187, the *covering* relative of the Leech-tree
question: the largest k such that some n-vertex tree with positive integer
edge weights realises every path sum 1..k. The entry stops at n = 10 with an
unattributed "a(11) ≥ 48, a(12) ≥ 55" and the keywords `hard, more`. The
perfect problem (all C(n,2) sums distinct and equal to 1..C(n,2)) has fifty
years of nonexistence results; the covering problem has none since Leech's
own table. The excess budget B = C(n,2) − k is small (6 at n = 11, k = 49),
so a covering tree is a Leech tree with at most B "wasted" pairs, and
Ghodsi's forced-weight recursion plus whole-block exact cover looked like it
would transfer with a budget attached. Other candidates and the internal
audit are in the daily log.

## The engine, and what broke on the way

**Prototype (Python, 40 lines).** Edges added in nondecreasing weight order,
next weight in [previous, mex], all component pairs and ports, prune on
excess > B. It reproduced a(2..9) = 1, 3, 6, 9, 15, 20, 26, 34 on the first
run (289 s for n = 9), which fixed the semantics: positive weights, sums over
unordered pairs, values 1..k must each appear at least once.

**Engine 1 (C, same recursion).** First version returned a(6) = 12: the undo
buffer for newly covered values was declared `static` and was clobbered by
deeper recursion levels, so covered flags were never restored. Fixed; the
ladder was reproduced but n = 10, k = 43 needed 428 s (31 M nodes).

**Engine 2 (bitsets).** Uncovered values as a 128-bit mask; the block bound
(Lemma 5a) computed by shifting the sumset mask of two components' depth
profiles over all route lengths L; parity DP; edge-load bound; canonical
strings for isomorphic components. 12× faster per node. Node histograms
showed 80 % of all nodes at two or three remaining components with the
budget already spent, i.e. the Leech-exact regime.

**Exact block cover (Lemma 5c).** A first implementation cut nodes 8× at
n = 9 but cost 150 µs per node (the DFS over candidate blocks exploded when
the remaining budget was ≥ 1). Gating it (≤ 4 components, remaining budget
≤ 2, product of candidate-list sizes ≤ 2·10^5, 5000-step cap, fail-open) and
skipping port pairs whose sumset already repeats more than the budget allows
gave a net 2.3×.

**Children from candidates.** The admissible candidate blocks with L in the
weight window *are* the children of a node, so generating children from the
list instead of re-simulating every (weight, pair, ports) merge removed most
of the deep-node cost. Two bugs surfaced here, both caught by the positive
control and by comparing node counts between engine variants:

1. the candidate buffers were global, so a child's block analysis overwrote
   the parent's list mid-iteration (a(6) came out as 13); buffers are now
   indexed by depth;
2. the canonical-form strings were global too, so after returning from a
   child the class-representative test read stale strings. This one is
   subtle: it can skip a merge that should be explored. At n ≤ 10 it had
   only *weakened* the symmetry rule (node counts fell from 18 264 to 7 500
   at n = 8, k = 27 once fixed, with the same verdict), but it could have
   gone the other way. Strings are now per depth, and the two engine
   variants (children by brute force vs. children from candidates) agree to
   the node: 3 247 390 nodes at n = 10, k = 43.

Final engine `code/cover_search.c`: n = 10, k = 42 refuted in 11.9 s
(14.06 M nodes); n = 11, k = 53 in 28.6 s (27.9 M nodes), k = 52 in 106 s
(121 M), k = 51 in 2 × 210 s (239 M + 255 M nodes on two workers). Growth is
about ×4 per unit of excess budget at n = 11.

**SAT engine.** `code/satcover.py` encodes one CNF per unlabelled tree shape
(shapes from `code/trees.py`, counts checked against A000055 for n ≤ 12):
unary edge weights bounded by Lemma 4, unary path sums through shared
root-ward partial sums with exact unary adders (both clause families), and
one coverage clause per value. It agrees with the search at n = 7 and 8
(a(7) = 20, a(8) = 26, witnesses checked) but takes about a minute per shape
at n = 9 while sharing the machine, so it is a replication tool for n ≤ 9/10,
not for n = 11.

## Results

**a(11) = 49 (CERTIFIED).** The ladder at n = 11 went k = 55 (no tree, the
known nonexistence of a Leech tree of order 11), 54, 53, 52, 51, 50 all
refuted, and k = 49 produced a witness on every one of the four workers
within 70 s: (0,1,1) (2,3,1) (0,4,2) (5,6,4) (3,6,5) (5,7,7) (6,8,8) (5,9,11)
(2,10,22) (0,3,24), path sums 1..49 with 1, 11, 23, 25, 26, 39 doubled and
nothing above 49. All four witnesses pass `check_cover.py`. The k = 50
refutation: 1 400 728 816 nodes, 4 workers, 259–304 s each. So Leech's (or
whoever's) 48 was one short. A k = 48 witness was also found in 1 s, which
reproduces the recorded bound.

**n = 12.** A witness for k = 57 appeared in 95 s (`witnesses/n12_k57.txt`,
checked), so a(12) ≥ 57 against the recorded 55. [PENDING: hunts at 58, 59;
refutations at 62 and 61.]

**Growth.** At n = 11 the exhaustive node count grows by about ×4 per unit of
excess budget (27.9 M, 121 M, 493 M, 1.40 G for B = 2..5) and by about ×9 per
vertex at fixed budget (n = 10 → 11 at B = 2, 3). That puts a full
determination of a(12) (refuting k = 58 if a(12) = 57, budget 8) at roughly
10^11 nodes, a day of four cores, and n = 13 well beyond a session.

**The distinct-sum variant.** A novelty check turned up the *Leech index*
of Varghese–Lakshmanan–Arumugam (2022): the largest k realised by a labelling
with all path weights distinct. That is a different problem from A007187,
whose values our repeat-allowed engine reproduces exactly and whose
witnesses repeat values freely. A `-d` mode (repeats forbidden, values above
k tracked individually) gave the maximum Leech index over trees of order
n = 2..12 as 1, 3, 6, 9, 15, 20, 25, 30, 37, 45, 47. Two things went wrong
before that table was right: the first `-d` implementation only forbade
repeats among values ≤ k (the n = 10 "witness" repeated 39 and 57 above k,
caught by the checker's `--distinct` option), and the 128-bit sumset mask
used by the block filters can lose sums ≥ 128, which in distinct mode would
have turned a valid port pair into a rejected one (guarded now; in
repeat-allowed mode the lost sums are excess anyway, so that mode was never
affected). The minimal second engine `plain_search.c` and the n ≤ 7 brute
force were written after these two incidents, and they agree with the main
engine on every value they reach.

## What failed

- The exact block cover as a general pruning rule: too expensive whenever
  the remaining budget is ≥ 1; it earns its keep only near the leaves.
- Two global-buffer bugs (above), both invisible to a single verdict and
  visible only to the positive control and to node-count agreement between
  variants. The lesson repeats the repository's: run the whole known ladder
  before every claim, and compare two implementations by node count, not
  by verdict.
- The SAT engine at n = 11: a minute per shape at n = 9 extrapolates to
  hours per shape at n = 11; not attempted.

## Publication paths

- OEIS A007187: submit a(11) = 49 with the witness tree and a link to this
  directory (`OEIS_DRAFT.md`), and replace the a(12) comment by the new bound.
- The exact values would interest the Leech-tree authors (Ghodsi 2026,
  Varghese–Lakshmanan–Arumugam 2020): the covering problem is the natural
  "how close to a Leech tree can order n get" question.
