# Good permutations and Mersenne primes (Weiss, MathOverflow 514690, 2026)

Call a permutation a_1, …, a_n of {1, …, n} **good** if no proper consecutive
block of two or more terms has an integer average. For even n the permutation
2, 1, 4, 3, … is always good. For odd n, Weiss (MO 514690, 27 Aug 2026) found
good permutations only at n = 3, 7, 31 among n ≤ 41, exhibited the family
W(p) = 1, p−1, p, p−3, p−2, …, 2, 3 for Mersenne primes p, and asked:
**do good permutations exist for odd n if and only if n is a Mersenne
prime?** Bîsceanu's answer in the thread shows odd n must be a Mersenne
number 2^m − 1, so the question lives on the composite ones: 63, 255, 511,
1023, 2047, … It looked tractable because that structure theorem, sharpened
to a "triangular bijection" statement, cuts the n = 63 search to 2^57
candidates with strong local pruning, and because the construction's failure
pattern at composite p suggested a clean theorem.

**Status:** active
**Sessions:** 2026-09-07
**Write-up page:** pending (`PAGE.md` handoff)

## Results

| # | Claim | Label | Where |
|---|---|---|---|
| 1 | **No good permutation of {1, …, 63} exists.** Exhaustive search over the structure of Lemma 2 (2^57 candidates), two independently organised engines: 1,433,402,570 nodes each (identical), 344 s / 128 s single-core. First undecided case of Weiss's question settled in the conjecture's favour; with W(127) good (Thm 4), the answer is "iff Mersenne prime" for all odd n ≤ 127 | **CERTIFIED** | `results/n63_mode1_run1.txt`, `results/n63_bits_run1.txt`; NOTE §5 |
| 2 | W(p) is good **iff p is prime**: for p = 2^m − 1 the only bad blocks are the prefixes of odd length L with L \| p (prefix sum ≡ −p mod L); blocks avoiding position 1 and even-length prefixes are never bad | **PROVED** | NOTE §3, Thm 4 |
| 3 | Structure of good permutations of 2^m − 1: a_t mod 2^k depends only on t mod 2^k through a bijection fixing 0 (Lemma 2; the counting step made explicit, giving a_{2^{m−1}} = 2^{m−1}), and then every even-length block is automatically fine (Lemma 3), so goodness is a condition on odd block lengths alone | **PROVED** | NOTE §2 |
| 4 | Exact counts: good permutations of [n] number 1, 2, 2, 2, 0, 2, 4, 8, 0, 2, 0, 4, 0, 2 for n = 1..14 (plain engine = brute force), 0 at n = 15, 4 at n = 31 (plain engine 181,519,993 nodes and structural engines agree); at n = 7 and 31 the good permutations are exactly W(p) and its three images under reversal and complement | **CERTIFIED** | `results/counts_mode0_1_14.txt`, `results/n31_mode0.txt`, NOTE §5 |
| 5 | W(p) verified good from the definition for p = 7, 31, 127, 8191, 131071, 524287 and bad for 15, 63, 255, 511, 1023, 2047, 4095, in each composite case first at the prefix whose length is the least prime factor | **CERTIFIED** | `results/construction_large.txt`; `check_good construction p` |
| 6 | Relaxation probe: with the structure imposed, the minimal sets of odd block lengths that exclude everything at n = 15 are {3,5,7}, {3,5,9}, {3,7,11}, {3,9,11} (lengths not dividing 15 are needed); survivors of short-length relaxations at n = 15, 31 are W-type or "near-identity" (a_t ≡ t mod 2^k) permutations | **CERTIFIED** (the counts) / observation | `goodperm_subset`, NOTE §4 |
| 7 | 2, 1, 4, 3, …, n, n−1 is good for every even n (block sums are L·mid ± 1 or half-integral multiples) | **PROVED** (folklore, stated in the thread) | NOTE §1 |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `goodperm.c` | engine A: backtracking over positions, prefix-sum block tests; mode 0 plain (any n), mode 1 with the Lemma 2 residue structure (n = 2^m − 1) | n = 31: 4.7 s (mode 0) / 0.05 s (mode 1); n = 63 mode 1: 344 s | counts, node counts, the permutations |
| `goodperm_bits.c` | engine B: searches the bit-functions b_k of Lemma 2 directly (bijectivity automatic), sliding per-length accumulators, odd lengths only | n = 63: 128 s | same counts and node counts as engine A |
| `goodperm_cpsat.py` | method C: OR-Tools CP-SAT model over the same bits, one modular constraint per odd block; enumerates or decides | n = 31 enumeration 17 s | status, count, solutions re-verified |
| `goodperm_subset.c` | relaxation probe: structure + block constraints for a chosen set of lengths only; counts/prints survivors | seconds at n ≤ 31 | which lengths carry the obstruction |
| `check_good.c` | independent from-definition checker (also `construction p` lines) | O(n²) | GOOD / BAD with the first bad block |
| `goodperm_small.py` | brute-force counts n ≤ 14 (positive control for engine A mode 0) | 4 min | the 14 counts |
| `construction_test.py` | Python check of W(p) at Mersenne numbers ≤ 8191, first five bad blocks | seconds | the failure pattern |

Run from inside this directory:

```bash
cd conjectures/good-permutations
gcc -O2 -march=native -o goodperm goodperm.c && ./goodperm 63 1 10        # Result 1, engine A
gcc -O2 -march=native -o goodperm_bits goodperm_bits.c && ./goodperm_bits 63 10   # engine B
gcc -O2 -o check_good check_good.c && ./goodperm 31 1 10 | head -4 | ./check_good
python3 goodperm_cpsat.py 31 300 1 1                                   # CP-SAT enumeration at 31
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `results/n63_mode1_run1.txt` | `goodperm 63 1 100` | Result 1, engine A: count 0, node count, time |
| `results/n63_bits_run1.txt` | `goodperm_bits 63 100` | Result 1, engine B: count 0, identical node count |
| `results/n63_cpsat_run1.txt` | `goodperm_cpsat.py 63` | method C verdict and solver statistics |
| `results/n31_mode0.txt` | `goodperm 31 0 100` | the four good permutations of [31], plain engine |
| `results/counts_mode0_1_14.txt` | `goodperm n 0` | counts n = 1..14 (match brute force) |
| `results/counts_mode0_15_26.txt` | `goodperm n 0 4` | counts n = 15..26 (both parities) |
| `results/construction_large.txt` | `check_good` | W(131071), W(524287) verified good |
| `results/n63_subsets.txt` | `goodperm_subset 63 …` | relaxation counts at n = 63 |

The "certificate" for Result 1 is reproducibility: two engines with
different data structures and candidate generation, identical exhaustive
node counts, six and two minutes to rerun. There is no compact witness for
"no permutation exists" beyond rerunning; the structure lemma the search
relies on is proved in NOTE §2 and the plain engine (no lemma) agrees with
the structural engines at every n ≤ 31.

## Known defects and open threads

- The exhaustive result depends on Lemma 2 (proved in NOTE §2 from the
  thread's argument, with the counting step made explicit). The plain
  engine cannot reach n = 63 (its n = 31 tree is 600× the structural one).
- **Next composite Mersenne numbers.** n = 255 is 2^247 candidates; node
  counts grew ×170 and ×4800 over the last two doublings, so 127 (the
  uniqueness question for W(127)) is ≈ 10^13 nodes and 255 is far beyond
  plain backtracking. CP-SAT timings at 63 are in `results/`; a decision at
  255 needs a new idea (constraint learning over the bit variables, or a
  theorem).
- **No proof for composite Mersenne numbers.** The relaxation probe rules
  out the naive "a divisor of n forces a bad block" argument; the
  survivors of short-length relaxations are W-type and near-identity
  triangular maps, which suggests a two-step proof (force the family, then
  kill it) that was not attempted.
- The counts for even n (2, 2, 2, 8, 2, 4, 2, …) have no structure theorem
  here.
- Communication with the source (an answer on MO 514690; an OEIS submission
  of the count sequence, which is not in the database) is a decision for
  the local session per repository policy.

## Prior work

Weiss, MathOverflow 514690 (27 Aug 2026): the question, the family W(p),
the search for odd n ≤ 41. Bîsceanu (answer, 28 Aug 2026, from a comment
by te4): odd n with a good permutation is a Mersenne number (the
power-of-two block lemma and the middle-segment argument, NOTE §2
Corollary). Peter Taylor (comment): partial "k-good" searches for
n ≤ 39. All read directly on the thread on 2026-09-07 (primary). No paper
and no OEIS entry on the problem was found (searches for the count
sequence and for the defining phrases return nothing). The observation
that blocks avoiding position 1 of W(p) are never bad, and the "iff prime"
form of Theorem 4, are not stated in the thread; the OP asserts goodness of
W(p) for Mersenne primes without proof.
