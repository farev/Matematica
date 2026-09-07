# Good permutations — session write-up

## Session 1 — 2026-09-05 (hedge line, run by a subagent on one core)

This problem was the day's hedge: the main session attacked the ordinary-lines problem
(`conjectures/ordinary-lines/`), and a subagent with one core, 2 GB and about two and a half
hours was given the MathOverflow question 514690 with three tasks — reproduce the thread's
facts lemma-free, look for a proof for composite exponents, and attack n = 63.

**Reproduction first.** A plain backtracking program over all permutations (`brute.c`, no
lemma) reproduced the asker's search: for odd n ≤ 41 good permutations exist only for
n = 3, 7, 31, and there are exactly 2, 4, 4 of them. It then went one step further, to n = 43
(34·10⁹ nodes, 6 min). The four solutions at n = 7 and n = 31 are the construction and its
images under reversal and complement — the first hint of the rigidity conjecture.

**The reduction.** The thread proves a_{t+2^k} ≡ a_t (mod 2^k) (Lemma A). The subagent
sharpened this to an equivalence (Lemma B): for n = 2^m − 1, goodness is exactly "a is a
2-adic isometry of Z/2^m fixing 0" plus the odd-length block conditions; the even-length
conditions are then automatic. The isometries are the automorphisms of a binary tree, 2^57 of
them for n = 63 — and Lemma B′ gives, at each position, exactly which values keep the
isometry property, so a depth-first search can enumerate them without ever generating a
non-isometry. The subagent wrote the proofs (PROOFS.md in its scratch directory) and the
session re-checked every step by hand before anything was labelled: Lemma A's counting of
residue classes, the "⇐" direction of Lemma B (u complete residue systems mod 2^j sum to
2^{j−1} mod 2^j), the three-term valuation argument in B′, and the six cases of Proposition C.

**n = 63 falls in twenty seconds.** `tree.c` visited 1,433,402,570 nodes and found nothing.
Because a twenty-second refutation of a problem that looked hard is exactly the kind of result
one should distrust, a second program (`brute2.c`, mode 2) was written with a different code
path — it scans all unused values and tests the isometry condition explicitly against every
earlier position, then checks every block length — and reached the same count of
1,433,402,570 nodes and the same verdict in 201 s. Both programs also reproduce the counts 4,
0, 4 for n = 7, 15, 31, and an audit flag confirms that even-length blocks never prune
anything, as Lemma B predicts.

**The construction.** Proposition C settles the asker's claim that 1, p−1, p, p−3, p−2, …, 2, 3
is good for Mersenne primes, and shows precisely how it fails for composite p: only prefixes
[1, L] with L | p have integer average. So the construction cannot decide the composite case,
and neither can any divisor-based argument (see below).

**Proof attempts for composite exponents (failed).** Restricting the enforced block lengths
(`tree.c -L`) mapped where the obstruction at n = 63 lives: the divisor lengths {3, 7, 9, 21}
leave thousands of tree automorphisms alive, the odd lengths ≤ 13 leave 680, and every one of
those 680 is killed by the lengths 31 and 33 = 2^{m−1} ± 1. Lemma E gives an exact criterion
for those two lengths in terms of the high bits of the values in the block; for the good
construction at n = 31 the criterion misses by exactly one at every position. The subagent did
not manage to turn this into a contradiction for composite exponents, and honestly says so.

**Ladder.** In construction-first order the search finds c(127) as its first leaf (n = 127,
prime) and nothing at n = 255 within 900 s and 41·10⁹ nodes at depth ≤ 78 of 255 — no
information, and recorded as such.

**Labels.** Theorem 1 (n = 63) is CERTIFIED: an exhaustive exact search whose reduction lemmas
are proved and re-checked and whose verdict is reproduced by an independent implementation.
It is not PROVED — there is no proof, only an exhaustion. Lemmas B, B′, E and Proposition C are
PROVED. Conjecture D and the restricted-length observations are NUMERICAL.

**What a next session should do.** Try to prove non-existence for composite 2^m − 1 using
Lemma E: the two lengths q ± 1 impose, for every window, a condition on the number of "high"
values in it, and these conditions interact with the tree structure; the 680 survivors at
n = 63 are the test set. Alternatively, an exhaustive count at n = 127 (Conjecture D) needs
symmetry reduction beyond `tree2.c`.
