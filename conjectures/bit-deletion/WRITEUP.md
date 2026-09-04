# Session narrative — Bit Deletion game (2026-09-03)

## How the problem was chosen

The mandate for the day was an external open problem, biased toward the
new. The survey (details in `log/2026-09-03-bit-deletion.md`) went through
the erdosproblems.com list of finitely checkable problems, the recent
arXiv listings, MathOverflow's open-problems tag and the OEIS entries added
in August 2026 that carry a "Conjecture" line. The Erdős candidates that
looked computational (#647, #993, #743, #287) all turned out to be crowded
by AI-assisted 2026 efforts with searches at scales this sandbox cannot
touch (see the log). The OEIS sweep produced A398916 — a three-week-old
impartial game with two clean conjectures, no literature, and a 3 : 1 split
of values at every bit-length in the first minutes of computation. That
split is exactly the fingerprint of a finite rule, so the session went
there.

## Finding the rule

The reference implementation from the OEIS entry gives the values below
2^21 in seconds. Three observations from that table drove everything:

1. At every bit-length L ≥ 3, exactly one quarter of the numbers take the
   high value (2 for even L, 3 for odd L), the rest the low value
   (0 or 1). So `G(n) ≡ L (mod 2)` always, and the interesting bit is a
   single Boolean `h(n)` = "value is high".
2. Numbers whose bits after the leading one begin with `1` are never high;
   numbers beginning with `01v` are high exactly when `v` is *not* high;
   numbers beginning with `001v` are never high; `0001v` behaves like `01v`.
3. Pure powers of two alternate (proved already in the OEIS entry).

Writing the bits after the leading one as zero-blocks
`0^{z_1} 1 0^{z_2} 1 ⋯ 1 0^{z_{m+1}}`, the observations say
`h = [z_1 odd] ∧ ¬h(rest)`, which unrolls to: `h = 1` iff the initial run
of odd-length blocks has odd length. That is the whole theorem
(`NOTE.md`, Theorem 1); it was conjectured from the table and then proved
by an induction whose only content is three statements about single
deletions (Lemma D). The proof took about half an hour once the invariant
was in hand; the invariant took about as long to see.

## Verification

- `grundy.py`: closed form equals the definition for all n < 2^20;
  reproduces the 34 published terms; the induction step of Theorem 1 and
  the three deletion lemmas were then checked exhaustively for every
  string of length ≤ 18 (524,287 strings, 0 failures) — an independent
  check of the case analysis, not a substitute for the proof.
- `grundy_check.c`: an OpenMP recomputation from the definition for every
  n < 2^32, comparing both the normal-play closed form and the misère rule:
  0 mismatches, no value above 3, and exactly `2^{L−3}` high values at each
  bit-length. 177 s on 4 threads, 4 GB RAM. Deterministic; no seeds.
- `variants.py`: the misère outcomes computed from the definition for
  n < 2^20 agree with "P ⟺ G = 1" with 0 disagreements, with exactly `4^k`
  misère P-positions below `2^{2k+1}` at every checkpoint; and the base-3,
  4, 5 and 10 games computed directly from their definitions to 3^13, 4^10,
  5^9, 10^6 agree with the binary formula applied to the zero/nonzero
  pattern — 0 mismatches in each base (~1 min).

## What the literature check found, and when

The proof was complete before the literature agent reported back. Its
report changed the framing: Project Euler Problem 961 "Removing Digits"
(21 Sep 2025) is the decimal version of the game, and public solution
write-ups (unrefereed; likely machine-written) state the zero-pattern
reduction and the P/N rule — i.e. Corollary 2 and Remark 3 of the note are
rediscoveries, and are marked so everywhere. The OEIS conjectures are about
the Grundy *values*, which the P/N rule does not determine; the search
found no source for those, nor for the misère result. Sources searched
(all 2026-09-03): OEIS full-text (only A398916 mentions the game), the
arXiv API (26 queries on deletion/digit/subsequence games), Fraenkel's
*Combinatorial Games: Selected Bibliography* (EJC DS2, 2012 version),
MathOverflow and Math.SE via the Stack Exchange API, and competition
archives (Codeforces, AtCoder, CSES, olympiad collections). The PE forum
thread is login-walled and unread. Conway's "Digit Deletions" (ONAG) is a
different game.

## What failed or was set aside

- **The ambitious slate died before the attack.** Every finitely checkable
  Erdős problem with a computational flavour that the survey turned up had
  been swept in 2026 far beyond this machine's reach (#647 to ≈ 9·10^18 with
  Lean-certified segments; #993 exhaustively to 32 vertices in August;
  #743 to n = 11 already in 1990; #287 with a Lean-checked finite reduction
  to 4·10^9). None offered an order-of-magnitude move. This is the second
  session in a row to record that the "computable" Erdős problems are
  swarmed; the comparative advantage is in problems that need an idea plus
  modest computation, which is where today's result sits.
- **A399155** (another August 2026 OEIS conjecture: subtracting the largest
  prime factor never takes more steps than subtracting the smallest) fell
  to a three-line argument during vetting and is recorded in the log rather
  than here; it is too small for a directory.
- Nothing in the attack itself failed; the honest caveat is that the
  result is small. The day's mandate was to aim high, and the survey did
  not find a high target that was also open to this hardware.

## Reproducibility record

Hardware: 4 cores, 15 GB RAM (cloud sandbox). Python 3.11.15, gcc with
OpenMP. All arithmetic on small integers; no floating point anywhere; no
random seeds. Commands and costs in `README.md`.
