# PAGE.md — handoff for the site page (update to the existing page `fabianarevalo.com/peaceable-queens`)

1. **Headline claim.** a(18) = 47 (CERTIFIED): the third consecutive open
   case of OEIS A250000 decided — 48 + 48 peaceable queens do not fit on the
   18 × 18 board (exhaustive refutation), and Ainley's 1977 placement, verified
   from the definition, gives 47 (with 48 black queens, even).

2. **Contributions (session 3, 2026-09-07).**
   1. CERTIFIED — a(18) ≤ 47: SYM16 engine, `run_chunked.py 18 48 16 4
      ./bnb_sym`, 16 chunks all UNSAT, 119,110,352,726 nodes, 32,544 s of
      engine CPU time (≈ 9 core-hours; 13,470 s wall on four niced workers
      under contention). Single-engine exhaustion, like n = 17.
   2. CERTIFIED — a(18) ≥ 47: the OEIS link-file placement (Kamenetsky 2019
      / Ainley 1977) passes `check_peaceable` with 47 white and 48 black
      queens.
   3. The ladder of decided cases is now a(16) = 37, a(17) = 42, a(18) = 47,
      each equal to ⌊7n²/48⌋ (Ainley's construction), against the 2014
      brackets [37, 64], [42, 72], [47, 81].

3. **Figures.**
   - *The 18 × 18 board.* Data: `witnesses/witness_n18_m47_kamenetsky.txt`.
     Sentence: "Forty-seven white and forty-eight black queens, no two of
     different colours on a line — and no way to fit forty-eight of each."
   - *The node-count ladder.* Data: README rows 1, 6, 7 — 5.03·10⁹,
     2.15·10¹⁰, 1.19·10¹¹ nodes at n = 16, 17, 18 (×4.3, ×5.6). Sentence:
     "Each rung costs about five times the last; a(19) is a fifty-core-hour
     job."

4. **Caveats the page must carry.**
   - n = 17 and n = 18 are single-engine exhaustions (the plain-engine
     replication was run only at n = 16); the verdicts rest on the proved
     pruning lemmas and the validation battery in NOTE §4.
   - The lower bound's provenance (Ainley 1977 via Kamenetsky's OEIS file)
     is secondary; the placement itself is verified here from the
     definition.
   - Wall time at n = 18 is not comparable with n = 17: the workers ran at
     nice 19 under the day's other searches; CPU time is the honest figure.
   - a(16), a(17), a(18) are not yet in the OEIS entry (still ends at a(15)
     as fetched 2026-09-07); submitting them is a local-session decision.

5. **What changed since the page was written.** The page currently ends at
   a(17) = 42 (session 2, 2026-09-03). Add the n = 18 rung, the 47 + 48
   witness, the updated ladder figure, and the deepened single-engine
   caveat; nothing earlier on the page changes.
