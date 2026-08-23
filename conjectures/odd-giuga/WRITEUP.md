# Session write-up — 2026-08-23 (session 1)

The narrative, including what failed. The polished statements are in
`NOTE.md`; the labelled results in `README.md`.

## Why this problem

The scheduled survey (see `log/2026-08-23-odd-giuga.md`) put three
candidates on the slate: the smallest open queens-domination case
(γ(Q_26) — priced at CPU-months by the revealed behavior of three
specialist groups 2017–2025), weak Schur records (now held by algebraic
template constructions that out-ran search entirely), and the odd-Giuga
factor bound. The last won on all three selection criteria: the recorded
bound (≥ 14 prime factors) dates to a 1996 Maple computation whose
companion code was never published; the even side of the same equation
family is demonstrably alive (first 9-factor primary pseudoperfect number
in April 2026, a 10^24 exhaustion eleven days before this session) while
the odd side sat untouched for thirty years; and the bottleneck is exactly
certified CPU — a branch-and-bound over prime sets with exact integer
arithmetic.

A bonus discovered during setup: both families are the two signs of one
equation, `Σ 1/p_i + ε/n = 1`, so one engine attacks both, and the even
side supplies positive controls with published answers (the ≤ 8-factor
Giuga and PPN censuses) before the odd frontier runs are believed.

## Order of events

1. **Connectivity check** — every literature site egress-blocked;
   WebSearch snippets only. All external citations (secondary). pypi.org
   reachable: gmpy2, sympy, numpy installed.
2. **Lemma layer first.** The classification (`A + ε = n`), parity
   (odd ⟹ even number of factors), the `T = 1` reduction below 1412 odd
   factors, and the engine-soundness lemmas were derived before the
   engine ran; the exact constants (1412, 59, 26, 9) came out of
   `lemmas.py` and two of them — 59 and 9 — matched the classical
   constants found in the literature snippets, an independent
   corroboration of the setup.
3. **Engine v1** (pure gmpy2, next_prime walks): reproduced the entire
   ≤ 7-factor Giuga and ≤ 7-factor PPN censuses in under a second —
   19 published numbers, term for term, node counts of a few thousand.
   Odd runs to m = 11: all empty, trees tiny (1207 nodes at m = 11).
4. **v1 hits the wall.** m = 12 odd and m = 8 even both stalled: py-spy
   showed one worker walking two-primes-left windows with next_prime
   (Miller–Rabin per odd integer) while three workers starved. The cost
   of a run is essentially the summed width of all closure windows
   (2.8×10^10 at m = 12): the walk pays microseconds per candidate.
5. **The right closure test.** For the final two primes,
   `u = Dq − P` must divide `N* = P² + εD` (NOTE Lemma 10; the gcd
   argument makes the divisibility equivalent to the defining one). That
   test needs no primality in the hot loop, and below `P < 2^62` it fits
   in unsigned 128-bit arithmetic: a 40-line C kernel scans every odd `q`
   at ~10 ns each. A second version added a wheel filter (skip `q` when
   some prime ≤ 61 divides `u` but not `N*` — one residue class mod `p`
   each) killing ~86% of candidates before the division.
6. **Validation discipline for the kernel.** v1-kernel and v2-kernel were
   run against the identical m = 12 tree: same node count, same closure
   count, same summed widths, both empty (94 s vs 60 s equivalent). The
   ≤ 7 regressions re-passed after every engine change. m = 12 odd:
   COMPLETE and empty in 94 s — the first rung past the 1996 frontier's
   interior (the record's exhaustion must have covered m ≤ 13).
7. **Clean-room engine2** (stdlib Fractions + sympy, independently derived
   looser windows, no kernel, no divisor route) agrees: the even censuses
   to m = 6 and odd emptiness to m = 11. Its first draft had a
   non-terminating window loop when the deficit dropped below 1/P —
   caught by inspection before any run; the fixed cut
   (`t/p + 1/(Pp) ≤ rem` ⟹ break) is provably terminating and sound.
8. **Resumability** (per-unit ledger with engine-hash guard) added before
   the long runs, per the vdw-mixed precedent; a mid-run source edit
   cannot relabel a running job's records (engine hash captured at
   import — the 2026-08-13 session's recompile defect class).

## What failed / mishaps

- **The v1 divisor route had a fake timeout**: `factorint` ran to
  completion and only then compared against the cap — a hard composite
  would have blocked a worker for hours. Replaced by a killable
  subprocess with a verified-factorization return path.
- **Two pkill self-kills.** A `pkill -f` pattern matched the wrapping
  shell of the very command issuing it (same defect the 2026-08-16
  session logged) — killed a control batch and, the second time, killed
  the fresh m = 13 job it was clearing the way for. Fixed with
  bracket-pattern pkill and by never combining pkill with a launch in one
  compound command.
- **A provenance bug found before it bit**: run records computed the
  engine hash at record-write time, so editing the source while a run was
  in flight would have stamped the new hash onto old-code results.
  Hash now captured at import.
- **Worker starvation** at split-depth 3–5 (one giant subtree, three idle
  cores): fixed by depth-7 splits (hundreds to thousands of units) sorted
  heaviest-first by deficit.
- **Oversubscription**: exploratory runs competed with each other for the
  4 cores; the official runs are serialized.

## The m = 13 wall (the session's pivot)

The plan was m = 14: exhaust it, apply parity at 15, and beat the
recorded 14 with "≥ 16". The m = 13 rung refused, three engine versions
in a row, and the third failure was informative rather than annoying:
py-spy with `--locals` on a stuck worker exposed a live node with prefix
`(3, 5, 7, 11, 13, 17, 19, 23, 967, 101429, 679364479)` and a
two-primes-left window of width 3.3×10^13. Tracing the arithmetic showed
this is not an implementation defect but the shape of the tree: t = 3
nodes with deficit d ~ 10^-9 branch over every prime in (1/d, 3/d) —
tens of millions of children — and every child is a t = 2 closure of
width ~ 1/d' or a 50-digit factorization. The m ≤ 12 tree totals
2.8×10^10 closure candidates; m = 13 is ~10^15–10^16. No constant-factor
engine improvement crosses five orders of magnitude, so the target moved
from "beat 14" to "certify 14, for both families, and quantify the wall"
— plus a redeployment of the now-fast machinery to where it does break
new ground: the even side at m = 9, which BBBG's 1996 census stopped
short of and nobody has determined since (the known Giuga numbers jump
from twelve with ≤ 8 factors to a sporadic ten-factor find from 2006).

Two consequences worth recording. First, the parity lemma makes m = 13
computation worthless for the bound (13 is odd): m ≤ 12 exhaustion
already gives ≥ 14 for both families, so the wall costs the session
nothing beyond ambition — "≥ 16" needed m = 14, which is two further
orders beyond the wall. Second, the same accounting casts doubt on any
reading of the recorded "14" as a 1996 full odd-tree exhaustion (the
even m ≤ 8 census BBBG demonstrably did is five orders cheaper); their
14 presumably came from the sequence/relaxation or Carmichael-augmented
methods of their paper, which this sandbox cannot read. NOTE §3.1 states
this carefully; our Theorems A and B stand on this session's
certificates alone.

## Tooling milestones on the way

- The two-primes-left identity `(Dq − P)(Dr − P) = P² + εD` with
  `gcd(Dq − P, D) = 1` turns the closure into "divisors of N* in one
  residue class mod D" — testable with one 128-bit remainder per
  candidate (C kernel, wheel-filtered, ~4 ns) or, better when N* is
  factorable, one factorization per node regardless of window width.
- sympy's pure-Python factoring was the wrong tool at 40+ digits;
  `python-flint` (FLINT with qsieve, pip-installable in this sandbox)
  factors the 50-digit N* of the deep nodes in ~0.1 s and a worst-case
  25×26-digit semiprime in 0.5 s — verified in-wrapper (product +
  primality re-check) so a wrong factorization can only degrade to
  "unfactored", never to wrong divisors.
- Every engine change was gated by the same battery: the ≤ 7-factor
  regressions on both signs, and the m = 12 odd fingerprint
  (240,534 closures / width sum 28,131,218,255), which ended up
  reproduced identically by five independent traversals across engine
  versions — plus the clean-room `engine2.py` agreeing on everything it
  can reach (both censuses to m = 6, odd emptiness to m = 11 on both
  signs).

## Endgame

(Final official records, control censuses, and the 9-factor census
outcome are appended to README.md as the frozen-engine driver completes;
the official engine hash is stamped in every run record.)
