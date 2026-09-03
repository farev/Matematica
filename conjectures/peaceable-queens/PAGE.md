# PAGE.md — handoff for the peaceable-queens page (update)

A page exists at `fabianarevalo.com/peaceable-queens` (built after session 1,
2026-08-17). This is an **update**, not a rebuild.

## 1. Headline claim

**CERTIFIED.** a(17) = 42: the second consecutive open case of OEIS A250000
decided — an exhaustive refutation of 43 + 43 queens on the 17 × 17 board
(21,454,699,264 search nodes, 1712 s on 4 cores) plus a checker-verified
42 + 42 placement — so the exact-value table now reads a(1..17) with
a(16) = 37 and a(17) = 42, both first determined in this repository.

## 2. Contributions (session 2 only; session 1's list stands)

1. **CERTIFIED** — a(17) ≤ 42: SYM16 engine, 16 resumable chunks, all
   UNSAT, 21,454,699,264 nodes, 1712 s wall on 4 workers (6,086 s engine
   time), run record `results/n17_m43_bnb_sym_chunk*.txt` and
   `results/n17_m43_run.log`. The recorded bracket had been [42, 72] since
   2014 (Pratt, OEIS; secondary).
2. **CERTIFIED** — a(17) ≥ 42: the 42 + 42 placement from the OEIS A250000
   link file (Kamenetsky 2019, attributing the value to Ainley 1977) passes
   the from-definition checker; `witnesses/witness_n17_m42_kamenetsky.txt`.
3. Hence **a(17) = 42**, confirming Ainley's 1977 value and ⌊7n²/48⌋ at
   n = 17.
4. Growth data for the page's "cost per rung" story: boundary refutation
   nodes 4.78·10⁸ (n = 13), 2.26·10⁹ (14, plain), 1.48·10⁹ (15, SYM16),
   5.03·10⁹ (16, SYM16), 2.15·10¹⁰ (17, SYM16) — `results/ladder_bnb.csv`.

## 3. Figure specs

- **Figure A (update the witness gallery).** Data:
  `witnesses/witness_n17_m42_kamenetsky.txt` (17 rows of `.`/`W`/`B`).
  Draw the board with the two armies. Sentence: *"42 white and 42 black
  queens share a 17 × 17 board with no queen of either color attacking the
  other, and no 43 + 43 arrangement exists."*
- **Figure B (extend the existing growth chart).** Data:
  `results/ladder_bnb.csv`, columns n, m, nodes, wall — add the n = 17 point
  (2.15·10¹⁰ nodes, 1712 s). Sentence: *"Each rung of the ladder costs about
  four times the previous one; n = 17 took half an hour."*

## 4. Caveats the page must carry

- **Single-engine exhaustion at n = 17.** a(16) was refuted by two
  independent engines; a(17) only by the SYM16 engine (the plain-engine
  replication is ≈ 9× the work, 4–5 h, not yet run). The verdict rests on
  the engine's validation record (Lemma 6′; 16/16 agreement with the plain
  engine on the ladder and at n = 16).
- The 42-witness comes from the OEIS link file (secondary provenance) but
  is verified from the definition here, so the lower bound does not depend
  on that provenance.
- Pratt's bracket [42, 72] and Ainley's 1977 table are cited as secondary
  (OEIS A250000 comments, fetched 2026-09-03); OEIS A250000 itself still
  lists only a(1..15).
- If the capped engine witness search recorded in
  `log/2026-09-03-peaceable-queens.md` found a 42-placement of its own, the
  page may say the witness was also found independently; otherwise it
  must not.

## 5. What changed since the page was written

- New result a(17) = 42 (items 1–3 above) and the single-engine caveat.
- The README's status line now reads two sessions; results row 6 added;
  NOTE §6b and §7(1) updated; WRITEUP has a session-2 section.
- Nothing about a(16) or the ladder changed.
