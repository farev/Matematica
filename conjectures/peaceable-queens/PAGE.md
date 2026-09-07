# PAGE handoff — peaceable-queens (page update)

1. **Headline claim.** a(18) = 47: the third consecutive open case of OEIS A250000
   decided (bracket [47, 81] since 2014), by an exhaustive refutation of 48 + 48 queens
   on the 18 × 18 board plus a checker-verified 47-queen placement. **CERTIFIED**
   (single-engine exhaustion, as at n = 17).

2. **Contributions (new since the a(17) page).**
   1. CERTIFIED — a(18) ≤ 47: the SYM16 engine's 16-chunk exhaustion of army size 48,
      119,110,352,726 nodes, 32,695 s of engine time (≈ 9.1 core-hours; 15,431 s wall
      on four shared cores), every chunk UNSAT, chunk records committed.
   2. CERTIFIED — a(18) ≥ 47: Kamenetsky's 47 + 48 placement from the OEIS link file
      (attributed to Ainley 1977) passes the from-definition checker; deleting any black
      queen gives 47 + 47.
   3. The ladder of node counts now reads 1.48·10⁹ (n = 15), 5.03·10⁹ (16), 2.15·10¹⁰
      (17), 1.19·10¹¹ (18): growth ×3.4, ×4.3, ×5.55 per rung.

3. **Figure specs.**
   - *Update the ladder figure*: add the point n = 18 (nodes 119,110,352,726, engine time
     32,695 s) to the existing boundary-refutation cost plot (data: the chunk files
     `results/n18_m48_bnb_sym_chunk*.txt`). Sentence: "Each rung costs four to five
     times the last; n = 19 is a day of four cores."
   - *Update the board figure*: the 47 + 48 placement `witnesses/witness_n18_m47_kamenetsky.txt`
     (18 × 18, W/B/. characters). Sentence: "Forty-seven white and forty-eight black
     queens, and no two of different colours see each other."

4. **Caveats the page must carry.**
   - Single-engine exhaustion (the plain-engine replication, ≈ 9× the nodes, was not
     run); the verdict rests on the proved pruning lemmas and the validation battery
     (plain/SYM16 agreement on every ladder boundary and at n = 16).
   - The lower bound is a literature placement verified from the definition, not an
     engine-found one.
   - Wall time was inflated by shared cores; engine time is the reproducible figure.
   - OEIS A250000 still ends at a(15); a(16), a(17), a(18) from this repository are not
     yet in the entry (submission is a decision for the local session).

5. **Existing page:** yes — <https://fabianarevalo.com/peaceable-queens>. Changes since it
   was written: the a(18) result (sessions row 2 → 3), the ladder figure gains a point,
   the caveat list gains the "literature witness only" item.
