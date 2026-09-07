# PAGE.md — handoff for the ordinary-lines page (new page; partial result — say so)

1. **Headline claim (one sentence, labelled).** CERTIFIED — if fifteen points in the plane
   span only seven ordinary lines (one less than the Dirac–Motzkin conjecture allows), their
   two forced 5-point lines must meet: the disjoint case is refuted by 261 SAT sub-cases
   with checked proofs, and the meeting case is refuted when no ordinary line joins the two
   5-point lines; the remaining meeting case (45 sub-cases) is **open**, so t₂(15) ≥ 8 is
   *not* proved. The page must lead with the partial nature of the result.

2. **Contributions (numbered, labelled).**
   1. CERTIFIED (Theorem 6.1): no 15-point configuration, real or pseudoline, with exactly 7
      ordinary lines and two disjoint 5-point lines. 261 sub-cubes, all UNSAT, all DRAT
      proofs checked by drat-trim; 2 472 s solving + 2 480 s checking (single-core seconds),
      6.3 GB of proofs, largest sub-cube 540 s, 55 min wall on 2 cores.
   2. CERTIFIED (Theorem 6.2): the meeting case with no ordinary line among the 16 pairs
      joining the two 5-point lines is impossible: 411 arrays, all UNSAT, verified
      (1 212 s solving, proofs 13.1 GB, 45 min on 1 core).
   3. PROVED (Cor. 5.3, Lemma 5.6): Melchior's inequality plus pair counting force a
      7-ordinary-line 15-point set to have exactly two 5-point lines and twenty-six 3-point
      lines; in the meeting case between 1 and 5 of the 16 cross pairs are ordinary; every
      point lies on an even number of ordinary lines.
   4. PROVED (reduction, Cor. 6.4): the Dirac–Motzkin bound t₂(15) ≥ 8 is equivalent to the
      unsatisfiability of the 45 remaining ∗-classes (151 309 arrays, measured ≈ 25
      CPU-hours in incremental fill mode); the 83 parity-void classes were machine-checked
      and two 70-array classes closed in fill mode (all UNSAT, verified).
   5. PROVED (from literature, secondary): t₂(20) = 10 and t₂(24) = 12 follow from
      Csima–Sawyer and Böröczky; the "?" at n = 20 in the A003034 comment is a gap in the
      quoted table.
   6. Method: a sound SAT encoding of rank-3 chirotopes with collinearities whose
      unsatisfiability needs only necessary conditions (no completeness theorem), calibrated
      on t₂(9..12) and positive-controlled on an explicit configuration.

3. **Figure specs.**
   - *Figure 1 — the case tree.* Data: `distributions.py 15 7` (one distribution), `cubes.py
     15 7` (cubes A, B), `subcubes.py B 7 --dry` (260 ∗-classes + 2 Latin squares),
     `certs/ledger_B_m7.jsonl` (per-s counts 2/1/3/6/16/34/69/130, all UNSAT), cube A: 131
     classes = 1 (closed, 411 arrays) + 2 (closed, 70 arrays each) + 45 (open) + 83 (void by
     parity, machine-checked). Sentence: "Every
     branch of the disjoint case is closed with a checked proof; the meeting case is closed
     only where no cross pair is ordinary."
   - *Figure 2 — solve time versus number of ordinary cross pairs.* Data:
     `certs/ledger_B_m7.jsonl` (fields `stars`, `solve_s`, `verify_s`). Sentence: "The hard
     sub-cases are the ones with few forced ordinary lines; once the array is nearly a Latin
     square the solver needs minutes, otherwise seconds."
   - *Figure 3 — the two 5-point lines and the array φ.* Data: the definition in NOTE §5
     (Lemma 5.5) and `poscontrol.py`'s explicit rational configuration (t₂ = 43) as an
     illustration of a real two-5-line configuration. Sentence: "Each pair of points on the
     two lines either spans an ordinary line or passes through exactly one free point, so
     the free points fill a partial Latin square."
   - No figure for the incremental-solving measurements (a table in the NOTE suffices).

4. **Caveats the page must carry.**
   - The headline is a partial result; t₂(15) is still unknown (7 ≤ t₂(15) ≤ 9 before this
     work; the disjoint case and the s = 0 meeting case are now excluded for t₂ = 7).
   - Kelly–Moser (1958) and Csima–Sawyer (1993) are cited via Green–Tao's introduction and
     A003034 — (secondary); the pseudoline extension relies on Melchior's inequality for
     pseudolines (Bokowski–Pokora, abstract read) and the topological representation
     theorem (Björner et al., not consulted) — (secondary).
   - The sub-7 line-type shapes were not machine-checked (excluded by Kelly–Moser); the n = 13
     and n = 14 refutation controls did not finish in the session.
   - Proof files were checked and deleted; ledgers with CNF hashes and the deterministic
     generators are the certificate.
   - All solver runs used Kissat 4.0.4 and drat-trim; single-solver per instance (the
     verification is by an independent checker, not a second solver).

5. **Existing page:** none — this is a new conjecture directory.
