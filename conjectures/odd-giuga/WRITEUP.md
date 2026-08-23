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

## Endgame

(Filled at close: the official frozen-engine ladder, the m = 14 runs, the
final bounds, and the verification pass.)
