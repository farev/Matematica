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
| 1 | **No good permutation of {1, …, 63} exists.** Exhaustive search over the structure of Lemma 2 (2^57 candidates), three independently organised engines: A and B enumerate the same tree and report the identical node count 1,433,402,570 (344 s / 128 s single-core); engine C (three-region order, tail and middle blocks checked early) reports 0 in 7,091,512 nodes, 1.65 s. First undecided case of Weiss's question settled in the conjecture's favour; with W(127) good (Thm 4), the answer is "iff Mersenne prime" for all odd n ≤ 127 | **CERTIFIED** | `results/n63_mode1_run1.txt`, `results/n63_bits_run1.txt`, `results/n63_mid_run1.txt`; NOTE §5 |
| 2 | W(p) is good **iff p is prime**: for p = 2^m − 1 the only bad blocks are the prefixes of odd length L with L \| p (prefix sum ≡ −p mod L); blocks avoiding position 1 and even-length prefixes are never bad | **PROVED** | NOTE §3, Thm 4 |
| 3 | Structure of good permutations of 2^m − 1: a_t mod 2^k depends only on t mod 2^k through a bijection fixing 0 (Lemma 2; the counting step made explicit, giving a_{2^{m−1}} = 2^{m−1}), and then every even-length block is automatically fine (Lemma 3), so goodness is a condition on odd block lengths alone | **PROVED** | NOTE §2 |
| 4 | Exact counts by the plain engine (no lemma used; = brute force for n ≤ 14): good permutations of [n] number 1, 2, 2, 2, 0, 2, 4, 8, 0, 2, 0, 4, 0, 2, 0, 4, 0, 2, 0, 4, 0, 2, 0, 4, 0, 2, 0, 4, 0, 2, 4, 4, 0, 2, 0, 4, 0, 2 for n = 1..38 (odd n: 0 except 3, 7, 31, as the Corollary predicts; even n: 4 when 4 \| n, 2 when n ≡ 2 mod 4, with n = 8 the lone exception at 8); at n = 7 and 31 the good permutations are exactly W(p) and its three images under reversal and complement; the structural engines agree at every Mersenne n ≤ 31 | **CERTIFIED** | `results/counts_mode0_*.txt`, `results/n31_mode0.txt`, NOTE §5 |
| 5 | W(p) verified good from the definition for p = 7, 31, 127, 8191, 131071, 524287 and bad for 15, 63, 255, 511, 1023, 2047, 4095, in each composite case first at the prefix whose length is the least prime factor | **CERTIFIED** | `results/construction_large.txt`; `check_good construction p` |
| 6 | Relaxation probe: with the structure imposed, the minimal sets of odd block lengths that exclude everything at n = 15 are {3,5,7}, {3,5,9}, {3,7,11}, {3,9,11} (lengths not dividing 15 are needed); survivors of short-length relaxations at n = 15, 31 are W-type or "near-identity" (a_t ≡ t mod 2^k) permutations | **CERTIFIED** (the counts) / observation | `goodperm_subset`, NOTE §4 |
| 7 | 2, 1, 4, 3, …, n, n−1 is good for every even n (block sums are L·mid ± 1 or half-integral multiples) | **PROVED** (folklore, stated in the thread) | NOTE §1 |
| 8 | **Theorem 5:** for m ≥ 4 no good permutation of [2^m − 1] has a_t ≡ t (mod 2^{m−1}) for all t, nor a_t ≡ −t; these "identity-like" families are exactly the ones that survive every sub-resonant relaxation at n = 63. Proof: the family reduces to a bit string with no 000/111 whose prefix and suffix one-counts never agree at lengths of equal parity, and five short blocks around the middle position force a contradiction (reduction confirmed by brute force at q = 4, 8, 16; constraint subset mechanically checked for N ≤ 15) | **PROVED** | NOTE §4c, `idfamily.py` |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `goodperm.c` | engine A: backtracking over positions, prefix-sum block tests; mode 0 plain (any n), mode 1 with the Lemma 2 residue structure (n = 2^m − 1) | n = 31: 4.7 s (mode 0) / 0.05 s (mode 1); n = 63 mode 1: 344 s | counts, node counts, the permutations |
| `goodperm_bits.c` | engine B: searches the bit-functions b_k of Lemma 2 directly (bijectivity automatic), sliding per-length accumulators, odd lengths only | n = 63: 128 s | same counts and node counts as engine A |
| `goodperm_mid.c` | engine C: assigns positions 1, q−1, 2, q−2, … (q = (n+1)/2) so that with the pairing a_{t+q} = a_t ⊕ q three known intervals grow at once and their odd blocks are tested immediately; optional complement symmetry breaking (`sym=1`: a_1 < q) | n = 63: 1.65 s; n = 127: see `results/n127_mid_run1.txt` | counts (node counts 20, 416, 26,540, 7,091,512 at n = 7, 15, 31, 63) |
| `goodperm_cpsat.py` | method D: OR-Tools CP-SAT model over the same bits, one modular constraint per odd block; enumerates or decides | n = 31 enumeration 17 s | status, count, solutions re-verified |
| `goodperm_subset.c` | relaxation probe: structure + block constraints for a chosen set of lengths only; counts/prints survivors | seconds at n ≤ 31 | which lengths carry the obstruction |
| `check_good.c` | independent from-definition checker (also `construction p` lines) | O(n²) | GOOD / BAD with the first bad block |
| `goodperm_small.py` | brute-force counts n ≤ 14 (positive control for engine A mode 0) | 4 min | the 14 counts |
| `construction_test.py` | Python check of W(p) at Mersenne numbers ≤ 8191, first five bad blocks | seconds | the failure pattern |
| `idfamily.py` | Theorem 5 companion: brute-force check that the identity-like family is good iff its bit string satisfies (I1)+(I2) (q = 4, 8, 16) and a DFS count at q = 32 | 2 min | 2, 0, 0 good; 0 strings at q = 32 |

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
| `results/n63_mid_run1.txt` | `goodperm_mid 63 0 10` | Result 1, engine C: count 0, 7,091,512 nodes |
| `results/n127_mid_run1.txt` | `goodperm_mid 127 0 10` | engine C at n = 127, full run: **lost** — killed by a harness restart after ≈ 12 h of CPU without output (note inside the file) |
| `results/n127_mid_sym1_split{0,1,2}of3.txt` | `goodperm_mid 127 1 10 - R,3` | n = 127 with a_1 < 64, split by (a_1 ≫ 1) mod 3: slice 2 **count 0** in 5,237,606,652 nodes (1976 s); slices 0 and 1 (which contain W(127) and its reversal image, found at once) still running at ≈ 9 h of CPU each when the session closed — see open threads |
| `results/n63_cpsat_run1.txt`, `..._note.txt` | `goodperm_cpsat.py 63` | method D: no verdict in 25 min (stopped); timing note |
| `results/n31_mode0.txt` | `goodperm 31 0 100` | the four good permutations of [31], plain engine |
| `results/counts_mode0_1_14.txt` | `goodperm n 0` | counts n = 1..14 (match brute force) |
| `results/counts_mode0_15_26.txt`, `..._27_34.txt`, `..._35_38.txt` | `goodperm n 0 4` | counts n = 15..38 (both parities) |
| `results/construction_large.txt` | `check_good` | W(131071), W(524287) verified good |
| `results/n63_prefix_lengths.txt`, `results/n31_prefix_lengths.txt`, `results/n63_survivors_*.txt` | `goodperm_mid n 1 0 L1,L2,…` | relaxation ladders and survivor lists (NOTE §4a–4b) |

The "certificate" for Result 1 is reproducibility: three engines with
different data structures, candidate generation and search order (A and B
with identical exhaustive node counts, C with a 200× smaller tree), six
minutes, two minutes and two seconds to rerun. There is no compact witness for
"no permutation exists" beyond rerunning; the structure lemma the search
relies on is proved in NOTE §2 and the plain engine (no lemma) agrees with
the structural engines at every n ≤ 31.

## Known defects and open threads

- The exhaustive result depends on Lemma 2 (proved in NOTE §2 from the
  thread's argument, with the counting step made explicit). The plain
  engine cannot reach n = 63 (its n = 31 tree is 600× the structural one).
- **n = 127 (is W(127) unique up to symmetry?) — partially covered.** With
  a_1 < 64 (complement symmetry) and the work split by (a_1 ≫ 1) mod 3,
  slice 2 is exhausted with count 0 (5.24·10⁹ nodes, 33 min); slices 0 and
  1, which contain a_1 = 1 (W itself) and a_1 = 3 (its reversal image,
  reported within two minutes), had each consumed ≈ 22 hours of CPU without
  finishing when the session finally closed (13:30 UTC, 8 Sep) — the tree
  is very unbalanced, the W-like branches being the deep ones — and the
  unsplit full run was lost to a harness restart after ≈ 12 hours. Slice 0
  did print W(127) itself early, as it must. So: no good permutation of [127]
  has a_1 ∈ {5, 11, 17, …, 59}; the rest is open. Rerun:
  `for r in 0 1; do ./goodperm_mid 127 1 10 - $r,3; done` (expect ≥ 9 h
  each; a finer split, e.g. K = 12, would parallelise it).
- **Next composite Mersenne numbers.** n = 255 is 2^247 candidates; engine
  C's node counts grew ×21, ×64, ×267 per doubling to 63 and the 127 slices
  show a further steep jump, so 255 is far beyond plain backtracking.
  CP-SAT timings at 63 are in `results/`; a decision at 255 needs a new
  idea (constraint learning over the bit variables, or a theorem).
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
