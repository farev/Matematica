# Session narrative — good permutations (2026-09-07)

Written as it happened; not edited to look smarter afterwards.

## Morning: the slate

The survey ran as six parallel scouts (OEIS, arXiv, erdosproblems.com,
MathOverflow and standing lists, a status check on a personal curiosity
list, and the internal audit). The erdosproblems crawl (all 1220 problems)
confirmed what the last three sessions recorded: every open problem there
with a visible numerical frontier has been swept by AI-assisted posters
since January. The arXiv scout's best items were mid-stride papers by
active authors (ORS_20(2), Caragea–Lee at 105/110, Chvátal at n = 9 — the
last needed 52 cores for n = 8). The status check closed several doors I
had been curious about (lonely runner through 13 runners, 1/3–2/3 through
14 elements). The MathOverflow scout brought the winner: Weiss's question
of 27 August about permutations with no consecutive block of integer
average — good permutations exist for n = 3, 7, 31 and no other odd
n ≤ 41; an in-thread theorem forces n = 2^m − 1; the first composite
Mersenne number, 63, had never been tested. The count sequence is not in
OEIS. Selected at 12:00 UTC.

Two things ran alongside from the start: the peaceable-queens a(18)
refutation on niced background workers (the internal audit's top thread;
its literature witness verified first), and a time-boxed subagent probe of
the two f(6) orientation instances Garcia left open in arXiv:2609.04686 —
the paper whose Theorem 2.1 (no counterexample to Erdős–Gyárfás below 24
vertices) I found on today's listing and recorded against the repo's own
Erdős–Gyárfás row before anything else.

## The construction test told the story first

Before writing any search code I tested Weiss's family W(p) = 1, p−1, p,
p−3, p−2, …, 2, 3 at every Mersenne number up to 8191. It is good at 7, 31,
127, 8191 and bad at 15, 63, 255, 511, 1023, 2047, 4095 — and at every
composite p the *first* bad block is the prefix whose length is the least
prime factor of p (3 at 15, 63, 255, 1023, 4095; 7 at 511; 23 at 2047).
That pattern is a theorem: the prefix of odd length L has sum ≡ −p
(mod L), and no other block of W(2^m − 1) is ever bad (NOTE §3, Theorem
4). So the family is good exactly when p is prime, and the whole question
is whether some *other* permutation works at a composite Mersenne number.

## Engine A, validation, and the 63 run

The structure theorem from the thread says a_t mod 2^k depends only on
t mod 2^k. I re-derived it with the counting step made explicit (a
position class of size u − 1 cannot host a residue class of size u), which
also gives σ_k(0) = 0 and a_q = q, and then noticed that the same structure
makes every even-length block automatically fine (Lemma 3), so only odd
lengths need testing. Engine A (`goodperm.c`) is a plain backtracking over
positions with prefix-sum block tests and an optional residue-structure
filter (mode 1). Validation: mode 0 reproduces the brute-force counts of a
Python script for all n ≤ 14 (1, 2, 2, 2, 0, 2, 4, 8, 0, 2, 0, 4, 0, 2);
mode 1 agrees with mode 0 at n = 3, 7, 15 and at n = 31, where both return
the same four permutations (mode 0: 181,519,993 nodes, 4.7 s; mode 1:
298,120 nodes, 0.05 s). The four are W(31) and its images under reversal
and complement.

n = 63, mode 1: **count 0**, 1,433,402,570 nodes, 344 s on one core. No
good permutation of {1, …, 63} exists.

## Engine B and CP-SAT

A second engine (`goodperm_bits.c`) searches the bit-functions of Lemma 2
directly (bijectivity is then automatic, no used-value bookkeeping) and
tracks block sums with one sliding accumulator per odd length instead of
prefix sums. It reproduces engine A's counts *and node counts* exactly at
n = 7, 15, 31 (60, 1748, 298,120), as it must, since both enumerate the
same tree. Its n = 63 run is recorded in the README. A third method, a
CP-SAT model over the same bit variables with one modular constraint per
odd block (`goodperm_cpsat.py`), enumerates exactly the four solutions at
n = 31 in 17 s and proves n = 15 infeasible in 0.2 s; its n = 63 verdict is
also in the README.

## Engine C: the pairing pays for itself

Engines A and B check only blocks that end at the newest position, so the
partner half of the permutation (positions q+1..n, forced by a_{t+q} =
a_t ⊕ q) is never tested until the end. Assigning positions in the order
1, q−1, 2, q−2, … makes three intervals of known values grow at once — the
head, a middle interval around a_q = q fed from both sides, and the tail —
and every odd block inside them can be tested at once. That is
`goodperm_mid.c`; it reproduces the counts at 7, 15, 31 with 21×, 4×, 11×
fewer nodes, and settles n = 63 in 1.65 s and 7,091,512 nodes (200× fewer
than A/B). Its growth per doubling is ×21, ×64, ×267, so n = 127 became
worth trying (run record in the README) while 255 (of order 10^13 nodes) did
not. The same engine took an optional list of block lengths, which made the
relaxation ladders at 63 a matter of seconds.

## What the relaxation probe says about a proof

With the residue structure imposed, at n = 15 the odd lengths {3, 7, 11}
already exclude every candidate, and the minimal excluding sets are
{3,5,7}, {3,5,9}, {3,7,11}, {3,9,11}. Two of the lengths in each set do not
divide 15, so the obstruction is not "a divisor of n forces a bad block";
it is an interaction between the binary structure and short odd windows.
At n = 63 the picture changed: the short lengths {3,5,7} that kill 15 leave
2,114 candidates (with a_1 < 32), all odd lengths up to 29 leave 260, and
the length 31 = q − 1 kills every one of them; at n = 31 the ladder reaches
the true count exactly when 15 = q − 1 enters. So the decisive constraint
is the "resonant" length 2^{m−1} − 1, and NOTE §4a works out why: such a
block misses exactly one residue class mod q, and q ≡ 1 modulo its length,
so its sum is congruent to (number of top bits set in the block) − (the
missing residue). Written out, the length-(q−1) conditions say that a
±1-step walk built from the top bits must avoid the residue permutation
pointwise. I did not find a proof of nonexistence for composite Mersenne
numbers today; the note states the mechanism and the question precisely.

## What failed / was not done

- No proof for composite Mersenne numbers in general; the divisor-based
  guess was refuted by the probe within minutes of being formed.
- n = 127 (is W(127) unique up to symmetry?) is out of reach for the
  backtracking engines: node counts grow ×170 and ×4800 across the last two
  doublings, so 127 is of order 10^13 nodes. Left open.
- n = 255 by exhaustive search is likewise out of reach; whether CP-SAT can
  do better is noted in the README from today's timing.
