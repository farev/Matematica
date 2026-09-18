# OEIS submission draft: A007187, new term a(11) = 49

**Sequence:** A007187, Leech's tree-labeling problem for n nodes.

**Proposed change.** Extend the data by a(11) = 49 and replace the comment
"a(11) >= 48, a(12) >= 55" by "a(12) >= [PENDING]" (whatever this session's
n = 12 witness gives; at least 55).

**Data.** 1, 3, 6, 9, 15, 20, 26, 34, 41, 49 (offset 2).

**Example (proposed).** a(11) = 49: the tree on vertices 0..10 with weighted
edges (0,1,1), (2,3,1), (0,4,2), (5,6,4), (3,6,5), (5,7,7), (6,8,8), (5,9,11),
(2,10,22), (0,3,24) has path sums covering 1..49 (with 1, 11, 23, 25, 26, 39
each occurring twice); an exhaustive search shows no tree on 11 vertices
covers 1..50.

**Comment (proposed).** a(11) = 49 by exhaustive computer search
(Sep 2026): edges are exposed in nondecreasing weight order, the next weight
is at most the least uncovered value, and the number of pairs whose path sum
repeats a value or exceeds k is bounded by C(n,2) − k; the search for k = 50
visited 1.40·10^9 nodes. Code and run records: [link to this directory].

**Link (proposed).** This repository, `conjectures/leech-tree-labelling/`,
with `code/cover_search.c`, the witness files and the run records.

**Checks done before submitting.** a(2..10) re-derived from scratch by the
same program (matches the entry); the witness verified by an independent
checker; k = 50 refuted on four independent worker prefixes; node counts
reproduce on rerun. Not done: a second independently written engine at
n = 11 (the SAT engine here replicates the search only for n ≤ 9).
