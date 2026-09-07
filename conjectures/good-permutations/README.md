# Good permutations and Mersenne numbers (MathOverflow 514690, P. Weiss, 2026)

A permutation of {1, …, n}, n odd, is *good* if no proper consecutive block of length ≥ 2
has an integer average. The MathOverflow question 514690 (27 Aug 2026) asks whether good
permutations exist exactly when n is a Mersenne prime: they exist for 3, 7, 31 (an explicit
construction), the thread proves n must be 2^m − 1, and a search covers odd n ≤ 41. The
first undecided case was the composite Mersenne number n = 63. It looked tractable for a
session because the thread's 2-adic lemma suggested the search space is not 63! but the
2^57 automorphisms of a binary tree — small enough to exhaust if the reduction could be
made rigorous.

**Write-up page:** *(pending — see PAGE.md; this was the session's hedge line, run by a
subagent alongside the ordinary-lines attack)*

**Status:** active
**Sessions:** 2026-09-05 (run by a subagent alongside the ordinary-lines session)

## Results

| Claim | Label | Where |
|---|---|---|
| **Theorem 1.** No good permutation of {1, …, 63} exists: the 2^57 candidates left by Lemmas A, B, B′ are exhausted by two independent programs (1,433,402,570 nodes each, 20.0 s and 200.9 s, one core). | CERTIFIED | NOTE §4, `data/run63.txt`, `data/b2_63_m2.txt` |
| **Lemma B.** For n = 2^m − 1 a permutation is good iff (i) v₂(a_y − a_x) = v₂(y − x) for all 0 ≤ x < y ≤ n (with a₀ = 0) and (ii) no proper odd-length block has integer average; the maps satisfying (i) are the 2^{2^m−1−m} tree automorphisms fixing 0. | PROVED | NOTE §2 |
| **Lemma B′.** Exact description of the admissible values at each position given (i) on the earlier ones (2^{m−1−⌊log₂ t⌋} candidates), which makes the search exhaustive. | PROVED | NOTE §2 |
| **Proposition C.** The asker's construction 1, p−1, p, p−3, p−2, …, 2, 3 is good iff p is prime; for composite p the only offending blocks are prefixes [1, L] with L an odd divisor of p. | PROVED | NOTE §3 |
| **Corollary 2.** The MO conjecture holds for all odd n < 255: good permutations exist for n ∈ {3, 7, 31, 127} and for no other odd n below 255. | PROVED + CERTIFIED | NOTE §4 |
| Lemma-free brute force: for odd n ≤ 43 good permutations exist only for 3, 7, 31, with exactly 2, 4, 4 of them (the construction and its reversal/complement images). Extends the asker's n ≤ 41. | CERTIFIED | `data/brute33_41.txt`, `data/brute43.txt`, `data/sols_m*.txt` |
| **Lemma E.** Exact criterion for the two block lengths 2^{m−1} ± 1 to have integer average, in terms of the high bits of the values in the block. | PROVED | NOTE §6 |
| At n = 63 the lengths {3,5,7} leave 4228 tree automorphisms, odd lengths ≤ 13 leave 680, and every one of the 680 is killed by lengths 31 and 33; n = 127: the construction is the first leaf of the search, count not exhaustive; n = 255: 41.2·10⁹ nodes, depth 78/255, no information. | NUMERICAL | NOTE §5–6, `data/exp63*.txt`, `data/analyze680.txt`, `data/run127.txt`, `data/run255.txt` |
| **Conjecture D (rigidity).** For n = 2^m − 1 every good permutation is one of the four images of the construction (true for m = 2, 3, 5; consistent with m = 4, 6). | NUMERICAL | NOTE §6 |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `check.py` | independent from-the-definition checker (prefix sums, all blocks); also builds the construction c(p) and the even-n construction | `python3 check.py --construction 63`: instant | reports the first offending block |
| `brute.c` | lemma-free backtracking over all permutations with block pruning | `./brute 31`: 2.2 s; `./brute 41`: 160 s; `./brute 43`: 358 s | counts of good permutations for odd n ≤ 43 |
| `tree.c` | structured exhaustive search over the tree automorphisms of Lemma B′, pruning with odd blocks; `-e` audits even blocks, `-L` restricts the enforced lengths (experiments), `-o` writes solutions | `./tree 6`: 20 s (n = 63); `./tree 5`: < 0.01 s | 0 good permutations for n = 63 |
| `brute2.c` | second implementation: mode 1 filters only with the thread's Lemma A, mode 2 tests condition (i) explicitly against every earlier position and checks all block lengths | `./brute2 63 2`: 201 s | 0 for n = 63, identical node count |
| `tree2.c` | the structured search in construction-first order with a time cap, for the ladder n = 127, 255 | `./tree2 7 -c -t 300` | construction found at n = 127 |
| `lemma_check.py` | checks Lemma B(i) and the tree-automorphism structure on a file of permutations | instant | all solutions for n = 7, 31 pass |

Build and run from inside this directory:

```bash
cd conjectures/good-permutations
gcc -O2 -o brute brute.c && ./brute 31
gcc -O2 -o tree tree.c && ./tree 6            # n = 63, 20 s
gcc -O2 -o brute2 brute2.c && ./brute2 63 2   # independent confirmation, 200 s
python3 check.py --verbose --construction 63
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/run63.txt` | `tree 6` | the n = 63 exhaustion: 0 solutions, 1,433,402,570 nodes, per-depth node counts, 20.0 s |
| `data/b2_63_m2.txt` | `brute2 63 2` | independent exhaustion, same node count, 200.9 s |
| `data/brute33_41.txt`, `data/brute43.txt`, `data/batch1.txt` | `brute` | lemma-free counts for odd n ≤ 43 and construction checks for p ≤ 2047 |
| `data/counts_n2_15.txt` | `brute` | counts of good permutations for n = 2..15 (even n included) |
| `data/sols_m2.txt`, `sols_m3.txt`, `sols_m5.txt`, `sols_m7.txt` | `tree -o` | all good permutations for n = 3, 7, 31 and the n = 127 witness |
| `data/exp15.txt`, `exp63.txt`, `exp63b.txt`, `analyze680.txt` | `tree -L`, `analyze680.py` (scratch) | restricted-length experiments and the killing-length analysis of the 680 survivors |
| `data/run127.txt`, `data/run255.txt` | `tree2` | capped ladder runs (NUMERICAL) |

No random seeds; everything is deterministic integer arithmetic.

## Known defects and open threads

- The n = 63 certificate is a search log, not an independently checkable proof object; its
  soundness rests on Lemmas A, B, B′ (proved in NOTE §2 and re-checked by hand) and on two
  programs agreeing. A third implementation in another language, or a SAT encoding with a
  DRAT proof, would raise the standard.
- The general composite case is open. The next composite Mersenne numbers, 255 and
  2047 = 23·89, are far beyond search (2^{247} and 2^{2036} candidates); a proof is needed.
  Lemma E (lengths 2^{m−1} ± 1) is where the data says the obstruction lives at n = 63.
- Conjecture D (rigidity) is untested beyond m = 5 for the positive cases; an exhaustive
  count at n = 127 needs a smarter search than `tree2.c`.
- The count sequence 2, 2, 2, 0, 2, 4, 8, 0, 2, 0, 4, 0, 2, 0 (n = 2..15) is not in the OEIS;
  a local session may submit it, and may post Theorem 1 and Proposition C to the MO thread.

## Prior work

- MathOverflow 514690 (P. Weiss, 27 Aug 2026): the question, the construction for Mersenne
  primes, the search to n = 41; answer by S. A. Bîsceanu (from a comment by te4) proving
  n = 2^m − 1 — read via the Stack Exchange API on 2026-09-05. Everything else here is new to
  our knowledge (OEIS and web searched the same day; negative evidence only).
