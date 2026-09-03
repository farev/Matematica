# 2026-09-03 — bit-deletion (OEIS A398916)

**Target.** New external problem, per the standing mandate. The Bit Deletion
game of OEIS A398916 (Do Thanh Nhan, added 14 Aug 2026, approved 20 Aug):
delete one binary digit of n, drop leading zeros, whoever removes the last
nonzero digit wins. The entry conjectures that the Sprague–Grundy values
never exceed 3 (checked to 5·10^6) and that a(4n) = a(n) (checked to 10^6).
Chosen because a five-second computation showed the values at every
bit-length splitting exactly 3 : 1 with the parity of the bit-length — the
fingerprint of a finite rule — and because no literature analyses the game.
What counted as success: a proof of both conjectures, ideally via the exact
Grundy function.

**Result.** **PROVED.** The Sprague–Grundy function is determined
completely: writing n in binary as `1 0^{z_1} 1 0^{z_2} 1 ⋯ 1 0^{z_{m+1}}`
(empty blocks allowed), with L the bit-length and t the number of initial
odd-length zero-blocks,

    G(n) = (L mod 2) + 2·[t odd].

Both OEIS conjectures follow (values ≤ 3; multiplying by 4 appends `00`,
changing neither the parity of L nor any block parity), together with:
exactly `2^{L−3}` of the L-bit numbers have value 2 or 3 (L ≥ 3), the number
of P-positions below `4^k` is `2^{2k−1} − 1`, and — **PROVED** — the misère
P-positions are exactly the positions of normal value 1 (odd L, even t),
`4^k` of them below `2^{2k+1}`. The proof is an induction on the bit string
whose entire content is three single-deletion lemmas (NOTE §2). **CERTIFIED:**
both theorems recomputed from the definition for all n < 2^32 (4.29·10^9
positions; 0 mismatches; no value above 3; 177 s on 4 threads, 4 GB), plus an
exhaustive check of the induction step for all 524,287 strings of length
≤ 18. **Rediscovery, marked:** the win/lose rule alone (P iff L even and t
even) and the reduction of base-b digit deletion to the binary zero-pattern
are folklore among solvers of Project Euler 961 "Removing Digits" (Sep 2025,
the decimal form of the game; unrefereed write-ups, cited as secondary);
the Grundy values, the bound, the 4n invariance and the misère theorem have
no source we could find. New directory `conjectures/bit-deletion/`
(README, NOTE, WRITEUP, PAGE.md, code, certificate); index row added.

**Side observation (PROVED, log only).** OEIS A399155 (20 Aug 2026)
conjectures that repeatedly subtracting the largest prime factor never takes
more steps than repeatedly subtracting the smallest. Three lines: for even n
the smallest-factor walk is n → n−2 → ⋯, so f(n) = n/2, while any walk
subtracting a prime factor ≥ 2 at each step has at most n/2 steps; for odd
composite n with least prime factor p and largest P, f(n) = 1 + (n−p)/2 and
g(n) ≤ 1 + (n−P)/2 ≤ f(n); primes give f = g = 1. Its "each positive value
finitely often" observation also holds: a subtract-2 step happens only at a
power of two, a decreasing walk visits each power of two at most once, so
g(n) ≤ n/3 + log₂ n and a(n) = f(n) − g(n) ≥ n/6 − log₂ n for even n
(the odd case reduces to the even one after the first step). Verified
against the published data to 20,000. Not worth a directory; recorded so a
local session can forward it to the OEIS entry if desired.

**Connectivity.** arxiv.org reachable via the standard fetcher (listing
page and API). oeis.org, erdosproblems.com and mathoverflow.net return 403
to the fetcher's user agent but serve curl normally (MathOverflow also via
the Stack Exchange API); all four consulted live today. pip reachable.

**Candidate slate** (three externals, three subfields; all statements and
status checked against the sources on 2026-09-03):

1. **OEIS A398916, Bit Deletion game** (combinatorial game theory).
   Statement as above. Source: `oeis.org/search?q=id:A398916&fmt=text`,
   version #12 of 20 Aug 2026 — two explicit conjectures, no proof, no
   cross-references, no later edits; the only link is Project Euler 961.
   Open because the entry says so and a literature agent found no
   Sprague–Grundy analysis of the game anywhere (OEIS full text, arXiv API,
   Fraenkel's bibliography, MO/MSE, competition archives). **Selected.**
2. **Erdős #647** (number theory; Erdős–Selfridge, £25): is there n > 24
   with max_{m<n}(m + τ(m)) ≤ n + 2? Source: erdosproblems.com/647 (page
   edited 7 Apr 2026, status VERIFIABLE) and its forum thread. Open — but the
   thread records exhaustive searches to 10^12 (Idén, Zenodo, Jun 2026) and,
   in a 41-residue-class reduction, to ≈ 6.16·10^17 and ≈ 9.17·10^18 (Hughes,
   Jun 2026; both unrefereed GitHub artifacts), a Lean-checked exclusion to
   10^9 (Mian–Siddique, arXiv:2608.17880, 18 Aug 2026), and Dutta's
   structural constraints (2520 | n, seven linked primes; Hughes's 7-tuple
   prime chains). Guy's UPINT §B8 says only "the next larger is probably
   beyond computer range" (secondary, OCR fragments). My brute-force reproduction to 3·10^7 found only the known
   n ∈ {2,3,4,5,6,8,10,12,24}. Passed over: nothing this machine can add.
3. **Erdős #993** (graph theory; Alavi–Malde–Schwenk–Erdős): the independent
   set sequence of every tree is unimodal. Source: erdosproblems.com/993
   (FALSIFIABLE) and forum. Open — but exhaustively verified for all trees
   on ≤ 32 vertices (109,972,410,221 trees at n = 32, ~27 h, posted 9 Aug
   2026), with log-concavity failures known from 26 vertices (Kadrawi–Levit
   2023) and PatternBoost sampling to 101 vertices. n = 33 is ≈ 3·10^11 trees
   — days on 4 cores for a 10 % extension. Passed over.

   Near-misses examined and rejected: Erdős #743 tree packing (Guichard–
   Massman, JCMCC 8 (1990), verified n ≤ 11 by computer — zbMATH summary,
   secondary — per a 27 Aug 2026 forum correction; the claimed general proof
   arXiv:2410.13840 was withdrawn in v3 on 1 Sep 2026; n = 12 is 5.9·10^12
   tree sequences);
   Erdős #287 unit-fraction gaps (Lean-checked: no counterexample with largest
   denominator ≤ 4·10^9, plus prime-chain certificates forcing n_1 > 3.9·10^19;
   the remaining obstacle is a Sophie-Germain-type input, i.e. parity-barrier
   territory); Erdős #488 (31 comments, active); MathOverflow 514742 square
   achievement game (asker already has forced-win searches for 6 ≤ n ≤ 14);
   OEIS A398490 (integer-sided cyclic polygons — "a(n) is always even"
   conjecture, author actively working, possible future target); A399155
   (trivial, above); arXiv:2606.18462 6-regular (4,1)-graphs (n = 16 needs
   ≈ 1.1·10^11 sextic graphs — beyond a day here). The three-week-old
   erdosproblems forum entries show the same picture the last two sessions
   recorded: the computable Erdős problems are swarmed by AI-assisted groups
   at scales beyond this sandbox.

**Internal-thread assessment** (parallel agent audit of all 24 conjecture
READMEs and the eight most recent logs). Last two sessions: projective-
chromatic (09-01) and graham-rearrangement (08-30) — no forced rotation.
Strongest live internal thread: **peaceable-queens a(17)** — refute army size
43 on the 17 × 17 board with the repo's validated SYM16 engine (n = 16 took
5.03·10^9 nodes / 462 s; the NOTE projects 5–8× for n = 17), then verify a
42-witness; OEIS A250000 still ends at a(15) (fetched today), so a(17) is
open. Everything else is a compute wall (graham-rearrangement p = 41 at
12–17 h, distinct-subset-sums f(10) in months, odd-giuga m = 13 at ~50
CPU-days, nci-datrees n = 16, erdos-gyarfas n = 19, balanced-colorings K₂₆)
or an ideas wall (strong-truncations Conjecture C, finch Conjecture A,
circular-thresholds n = 8). Selection argument: the mandate's default is the
external problem; A398916 beat the internal thread on (a) — a proof, not a
search, was within reach — and on novelty of the *kind* of result (a
complete solution rather than one more table entry); it loses to a(17) on
citation surface (A250000 is a famous sequence). Ties go to the new problem,
and the external attack finished early, so a(17) was launched afterwards as
a **secondary target** in the background (see below) rather than instead.

**What failed.**
- *The ambitious slate.* Every finitely checkable Erdős problem with a
  computational edge was already searched orders of magnitude beyond this
  machine (details above). Half the survey time went into confirming that.
- *Nothing in the attack itself.* The invariant was read off the table
  (high value ⟺ leading block odd and the rest not high), the induction
  went through on the first attempt, and the exhaustive checks found no
  gap. The honest failure is of ambition: the result is a small theorem.
  The literature agent's discovery that the P/N rule is Project Euler
  folklore arrived after the proof and cut the novelty of the outcome-class
  corollary; it is marked as a rediscovery throughout.
- *Secondary target, peaceable-queens a(17).* Launched at the end of the
  session on the freed cores (`run_chunked.py 17 43 16 4 ./bnb_sym`,
  resumable chunks in `conjectures/peaceable-queens/results/`); status at
  session close is recorded in `log/2026-09-03-peaceable-queens.md` if the
  run produced anything, otherwise here: see the "Next" item.

**Next.** (1) Peaceable queens a(17): finish the m = 43 chunks (resumable),
verify Kamenetsky/Ainley's 42-queen placement with `check_peaceable`, and
if UNSAT lands, a(17) = 42 is a new A250000 term. (2) Bit Deletion variants
with genuinely new structure: two deletions per move, deletion of a run of
equal digits, the partizan trit game (Project Euler 963) — the block-parity
invariant does not obviously survive any of them. (3) A398490's evenness
conjecture (integer-sided polygons inscribed in a circle of integer radius)
looked like the one August OEIS conjecture with real number theory in it;
worth a session once the author's linked document has been read.

**Session hygiene.** Branch: harness-designated `claude/affectionate-sagan-aq0rv2`
(the mandate's per-conjecture branch name overridden by the harness
requirement, as in previous sessions). The `conjecture-research` skill named
in CLAUDE.md is not installed here; CLAUDE.md followed directly. Hardware:
4 cores, 15 GB; Python 3.11.15; gcc/OpenMP. No seeds; everything exact.
