# OEIS submission draft: A007187, new term a(11) = 49

**Sequence:** A007187, Leech's tree-labeling problem for n nodes.

**Proposed change.** Extend the data by a(11) = 49 and replace the comment
"a(11) >= 48, a(12) >= 55" by "a(12) >= 57" (witness below).

**Data.** 1, 3, 6, 9, 15, 20, 26, 34, 41, 49 (offset 2).

**Example (proposed).** a(11) = 49: the tree on vertices 0..10 with weighted
edges (0,1,1), (2,3,1), (0,4,2), (5,6,4), (3,6,5), (5,7,7), (6,8,8), (5,9,11),
(2,10,22), (0,3,24) has path sums covering 1..49 (with 1, 11, 23, 25, 26, 39
each occurring twice); an exhaustive search shows no tree on 11 vertices
covers 1..50.

**Second example.** a(12) >= 57: edges (0,1,1), (0,2,1), (1,3,1), (2,4,4),
(5,6,6), (7,8,8), (2,7,9), (5,9,14), (7,5,15), (6,10,16), (5,11,29).

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


# Second draft: a new sequence, maximum Leech index over trees of order n

**Name.** Largest k such that some tree on n nodes with positive integer edge
labels has all C(n,2) path sums distinct and realizes every integer 1..k.

**Data (offset 2).** 1, 3, 6, 9, 15, 20, 25, 30, 37, 45, 47

**Comments.** The maximum over trees of order n of the Leech index k(T)
defined by S. Varghese, A. Lakshmanan S. and S. Arumugam, J. Discrete Math.
Sci. Cryptogr. 25 (2022) 2237-2247. a(n) <= A007187(n), with equality for
n <= 7 and strict inequality for 8 <= n <= 11. a(n) = C(n,2) iff a Leech tree
of order n exists (n = 2, 3, 4, 6 among n <= 24). a(n+1) >= a(n) (attach a
pendant vertex by a sufficiently large weight).

**Example.** a(11) = 45: edges (0,1,1), (2,3,2), (0,4,3), (2,5,5), (6,7,6),
(3,6,8), (4,8,9), (8,7,11), (1,9,18), (5,10,28) give the 55 distinct sums
1..45, 48, 49, 56, 58, 60, 63, 69, 72, 73, 91.

**Crossrefs.** A007187, A004137 (sparse rulers; paths), A000055.
