# PAGE.md — handoff for the good-permutations page (new page)

1. **Headline claim (one sentence, labelled).** CERTIFIED — the first undecided case of the
   MathOverflow question "do only Mersenne primes have good permutations?" is settled: no
   permutation of {1, …, 63} has every proper consecutive block averaging to a non-integer,
   so the conjecture holds for every odd n below 255.

2. **Contributions (numbered, labelled).**
   1. CERTIFIED (Theorem 1): no good permutation of {1..63}. The 2^57 candidates left by the
      2-adic reduction are exhausted by two independent programs, 1,433,402,570 nodes each,
      20.0 s and 200.9 s on one core.
   2. PROVED (Lemma B): for n = 2^m − 1 a permutation is good iff it is a 2-adic isometry of
      Z/2^m fixing 0 (a binary-tree automorphism; there are 2^{2^m−1−m} of them) and no
      proper odd-length block has integer average — even-length blocks come for free.
   3. PROVED (Lemma B′): the exact set of admissible values at each position, which makes the
      search exhaustive.
   4. PROVED (Proposition C): the asker's construction 1, p−1, p, p−3, p−2, …, 2, 3 is good iff
      p is prime; for composite p it fails exactly at prefixes whose length divides p.
   5. CERTIFIED: lemma-free brute force for odd n ≤ 43 (extending the asker's n ≤ 41): good
      permutations only for 3, 7, 31, with exactly 2, 4, 4 of them (n = 43: 33,982,657,297
      nodes, 358 s). Corollary: the conjecture holds for all odd n < 255.
   6. PROVED (Lemma E) + NUMERICAL: an exact criterion for the two block lengths 2^{m−1} ± 1,
      which kill all 680 near-solutions at n = 63; Conjecture D (rigidity): every good
      permutation is one of the four images of the construction (true for m = 2, 3, 5).

3. **Figure specs.**
   - *Figure 1 — the binary tree of candidates.* Data: `data/run63.txt` (nodes per depth for
     n = 63, 1..63). Sentence: "The search space is a binary tree of depth 63 with 2^57 leaves,
     and the odd-length block conditions prune it to 1.4 billion nodes, none surviving."
   - *Figure 2 — which block lengths kill.* Data: `data/exp63.txt`, `data/exp63b.txt`,
     `data/analyze680.txt` (survivors of odd lengths ≤ 13: 680; smallest killing length
     distribution 15/19/29/31 → 16/16/128/520; lengths 31 and 33 kill all 680). Sentence:
     "Small block lengths and divisor lengths are not the obstruction; the two lengths just
     below and above 32 are."
   - *Figure 3 — the good permutations that exist.* Data: `data/sols_m3.txt`,
     `data/sols_m5.txt` (the four solutions for n = 7 and n = 31 are the construction and its
     reversal/complement images). Sentence: "Every known good permutation is the same
     zig-zag construction up to reversal and complement."

4. **Caveats the page must carry.**
   - Theorem 1 is an exhaustive search, not a proof; its soundness rests on Lemmas A, B, B′
     (proved, re-checked by hand) and on two programs agreeing; no independent proof object.
   - The n = 127 run found the construction but did not count solutions (2^{120} candidates,
     300 s cap); n = 255 gave no information (2^{247} candidates, 900 s cap).
   - Lemma A is from the MathOverflow thread (te4, Bîsceanu), read via the Stack Exchange API;
     no other literature found (OEIS and web search, negative evidence only).
   - The general composite case (255, 2047 = 23·89, …) is open; Conjecture D is numerical.
   - The count sequence 2, 2, 2, 0, 2, 4, 8, 0, 2, 0, 4, 0, 2, 0 is not in the OEIS.

5. **Existing page:** none — new directory (hedge line of the 2026-09-05 session).
