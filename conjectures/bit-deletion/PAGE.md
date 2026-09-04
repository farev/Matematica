# PAGE.md — handoff for the Bit Deletion page (new page)

No page exists for this conjecture yet. Proposed path:
`fabianarevalo.com/bit-deletion`.

## 1. Headline claim

**PROVED.** The Bit Deletion game (OEIS A398916: delete one binary digit,
drop leading zeros, last nonzero digit wins) has Sprague–Grundy value
`G(n) = (L mod 2) + 2·[t odd]`, where L is the number of binary digits of n
and t is the number of initial zero-blocks of odd length in the expansion
`1 0^{z_1} 1 0^{z_2} 1 ⋯ 1 0^{z_{m+1}}` — a complete solution of the game
that settles both conjectures in the OEIS entry.

## 2. Contributions

1. **PROVED** — Theorem 1, the closed form above, by an induction on the
   bit string whose entire content is three single-deletion lemmas
   (NOTE §2). Plain-language version for the page: the value's parity is
   the parity of the number of digits; the value is "high" (2 or 3) exactly
   when, reading the zero-runs between the ones from the left, an odd number
   of odd-length runs come before the first even-length run.
2. **PROVED** — both OEIS A398916 conjectures: `G(n) ≤ 3` for every n
   (the entry had checked this to 5,000,000) and `G(4n) = G(n)` (checked in
   the entry to 1,000,000); plus the sharper statement that the sequence
   `G(n), G(2n), G(4n), …` has period exactly 2.
3. **PROVED** — exact counts: among the `2^{L−1}` numbers with L ≥ 3 binary
   digits, exactly `2^{L−3}` have value 2 or 3; the number of losing
   positions (previous player wins) below `4^k` is `2^{2k−1} − 1`
   (e.g. 7 below 16, 31 below 64, 127 below 256).
4. **PROVED** — misère form (whoever removes the last nonzero digit loses):
   the losing-to-move positions are exactly those of normal value 1, i.e.
   odd digit-count and even t; there are `4^k` of them below `2^{2k+1}`.
5. **PROVED (rediscovery, marked)** — the win/lose rule itself (Corollary 2:
   a position is a loss for the mover iff it has an even number of digits
   and t is even) and the reduction of base-b digit deletion to the binary
   zero-pattern are folklore among solvers of Project Euler Problem 961,
   the decimal form of the game, in unrefereed write-ups (secondary). The
   page must say this plainly; the Grundy values, the bound, the `4n`
   invariance and the misère theorem are the new part.
6. **CERTIFIED** — Theorems 1 and 2 recomputed from the definition for all
   `n < 2^32 = 4,294,967,296`: 0 mismatches, no value above 3, exact
   `2^{L−3}` counts at every bit-length. 177 s on 4 threads, 4 GB RAM
   (`data_grundy_check_2e32.txt`). Independent pure-Python check to 2^20 and
   exhaustive check of the proof's induction step for all 524,287 strings
   of length ≤ 18.

## 3. Figure specs

- **Figure 1 — the rule on an example.** Data: none needed beyond the
  example `n = 37 = 100101₂` (the OEIS entry's own worked example, value 0)
  and `n = 5 = 101₂` (value 3). Draw the bits, bracket the zero-runs after
  the leading one (37: runs 2, 1, 0 → t = 0; 5: runs 1, 0 → t = 1), and
  annotate `G = (L mod 2) + 2·[t odd]`. Sentence the reader should be able
  to say: *"I can compute the value of any position by hand: count the
  digits for the parity, then count how many odd-length zero-runs come
  before the first even-length one."*
- **Figure 2 — values by bit-length.** Data: `data_grundy_check_2e32.txt`
  (columns: L, counts of values 0/1/2/3). A stacked bar per L from 1 to 32
  (log scale or normalised to 1) showing even L split 3 : 1 between 0 and 2,
  odd L split 3 : 1 between 1 and 3. Sentence: *"At every length the values
  split exactly three to one, and the parity of the value is the parity of
  the length."*
- **Figure 3 — losing positions.** Data: from `grundy.py` (list of n < 256
  with G(n) = 0: 3, 9, 10, 12, 13, 14, 15, 33, 34, 36, …). A 16 × 16 grid of
  n = 0..255 shaded by value (four colours), losing positions outlined.
  Sentence: *"Losing positions only occur at even digit-counts, and they
  are three quarters of those."*

## 4. Caveats the page must carry

- Corollary 2 (the P/N rule) and the base-b reduction are **not new**
  (Project Euler 961 folklore; unrefereed write-ups such as
  github.com/cirosantilli/project-euler-solutions `solvers/961.md`;
  cited as secondary — the PE forum itself is login-walled and unread).
- The literature search (OEIS, arXiv API, Fraenkel's bibliography,
  MathOverflow/Math.SE, competition archives; all 2026-09-03) found no
  Sprague–Grundy analysis of the game; "new" means "not found by that
  search", not a certainty.
- Conway's "Digit Deletions" (ONAG) is a different game and is cited only
  through OEIS A120442 (secondary).
- The CERTIFIED range is `n < 2^32`; the theorem covers all n, and the
  computation is a check of the proof, not its source.
- The OEIS entry's own checked ranges (5·10^6 and 10^6) should be quoted as
  stated there (fetched 2026-09-03, entry version #12 of 20 Aug 2026).

## 5. Existing page

None. This is a new page and a new row in the index.
