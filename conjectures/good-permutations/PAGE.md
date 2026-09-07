# PAGE.md — handoff for the site page (new page: `fabianarevalo.com/good-permutations`)

1. **Headline claim.** No permutation of {1, …, 63} avoids a consecutive block
   with integer average — so Weiss's "good permutations exist for odd n iff n
   is a Mersenne prime" survives its first undecided case, and holds for all
   odd n ≤ 127 (CERTIFIED for 63, the rest by theorem).

2. **Contributions.**
   1. CERTIFIED — exhaustive search at n = 63 over the 2^57 candidates allowed
      by the structure theorem: 0 good permutations; two independently
      organised engines (value-scanning with prefix sums; bit-function search
      with sliding accumulators) report the identical node count
      1,433,402,570 in 344 s and 128 s on one core. (CP-SAT verdict: see
      `results/n63_cpsat_run1.txt` if it finished.)
   2. PROVED — Weiss's family W(p) = 1, p−1, p, p−3, p−2, …, 2, 3 is good if
      and only if p is prime: no block avoiding position 1 is ever bad, even
      prefixes are never bad for Mersenne p, and the prefix of odd length L
      has sum ≡ −p (mod L). Verified from the definition at p = 7, 31, 127,
      8191, 131071, 524287 (good) and 15, 63, 255, 511, 1023, 2047, 4095 (bad,
      first failing at the least prime factor).
   3. PROVED — structure: in a good permutation of 2^m − 1, a_t mod 2^k depends
      only on t mod 2^k through a bijection fixing 0 (so a_{2^{m−1}} = 2^{m−1}
      and the permutation is determined by 2^m − m − 1 bits), and every block
      of even length is then automatically fine; goodness is a condition on
      odd block lengths only.
   4. CERTIFIED — exact counts of good permutations for every n ≤ 31:
      1, 2, 2, 2, 0, 2, 4, 8, 0, 2, 0, 4, 0, 2, 0, 4, 0, 2, 0, 4, 0, 2, 0, 4, 0, 2
      (n = 1..26), 0 at 27, 29 (theorem), 4 at 31; at 7 and 31 the good
      permutations are exactly W(p) and its three images under reversal and
      complement. Not in OEIS.
   5. Observation (CERTIFIED counts) — the obstruction at composite Mersenne
      numbers is not divisibility of n: at n = 15 the minimal excluding sets
      of odd block lengths are {3,5,7}, {3,5,9}, {3,7,11}, {3,9,11}.

3. **Figures.**
   - *The failure ladder of W(p).* Data: `construction_test.py` output /
     `results/construction_large.txt` — for each Mersenne number p ≤ 8191 the
     length of the first bad prefix (3, 3, 7, 3, 23, 3 at 15, 63, 511, 1023,
     2047, 4095; none at 7, 31, 127, 8191). Sentence: "Weiss's construction
     fails at a composite Mersenne number exactly at the prefix whose length
     is its smallest prime factor, and nowhere else."
   - *The node-count ladder.* Data: README results rows / run records —
     nodes 60, 1748, 298,120, 1,433,402,570 at n = 7, 15, 31, 63 (structural
     engines), 181,519,993 at 31 for the plain engine. Sentence: "The
     structure theorem shrinks the n = 31 search 600-fold, and the tree still
     grows about 5000-fold per doubling of n, which is why 63 is done and 127
     is not."
   - *The permutation W(31) as a 31-point plot* (position vs value): data
     `results/n31_mode0.txt`. Sentence: "A good permutation of 31 looks like
     this, and there are only four of them."

4. **Caveats the page must carry.**
   - The n = 63 result is an exhaustive search resting on the structure lemma
     (proved in NOTE §2); there is no compact certificate beyond rerunning
     (six minutes). Both engines share that lemma; the plain engine confirms
     it only up to n = 31.
   - All statements about the thread (Weiss's search to n ≤ 41, Bîsceanu's
     theorem, Peter Taylor's partial searches) are read from the thread itself
     (primary); no paper on the problem was found.
   - The question remains open at 255, 511, 1023, 2047, …; the "near-identity"
     survivor families are an observation, not a theorem.
   - Even-n counts (2 or 4, with 8 at n = 8) are computed, not explained.

5. No page exists yet.
