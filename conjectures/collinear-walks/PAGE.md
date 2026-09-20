# PAGE.md — handoff for the `collinear-walks` page (new page)

Path: `fabianarevalo.com/collinear-walks`. Session 2026-09-09. No page exists yet.

## 1. Headline claim

**PROVED.** There is an infinite walk in ℕ⁷ using only the seven standard unit
steps whose vertices contain no three collinear points: the (direction, turn)
sequence of the Heighway dragon curve, with the two letters "east, left turn"
and "west, left turn" identified, has no two adjacent blocks with the same
letter frequencies. This improves Shallit's published bound 16 (arXiv:2609.05780,
5 Sep 2026) by an independent mechanism; an unpublished draft by Kalviainen
(5 Sep 2026) claims 6, and we reviewed it and found no gap, so the frontier is
4 ≤ k_min ≤ 6 with 6 resting on that draft and 7 on this note.

## 2. Contributions

1. **PROVED** — the eight-letter dragon word (fixed point of the morphism
   0→02, 1→03, 2→52, 3→53, 4→46, 5→47, 6→16, 7→17) is 3-free; unit-step walk in
   ℕ⁸ with no collinear triple. (NOTE Thm 1)
2. **PROVED** — its seven-letter coding (identify letters 0 and 4, i.e.
   (0,+) and (2,+)) is 3-free; k_min ≤ 7. (NOTE Thm 2) The proof: the dragon
   walk obeys ν₂(|Z_n − Z_m|²) = ν₂(n − m) whenever the endpoint directions are
   not antipodal (Lemma 2, 2′); two telescoping indicators force equal endpoint
   directions on any weak abelian square (Lemma 3); the right-turn-only walk
   supplies the displacement.
3. **Review** — Kalviainen's six-dimensional draft: read line by line, no gap
   found; six step vectors, all-pairs valuation identity on 3 123 750 pairs,
   word 3-free to 30 000 reproduced. (NOTE §5)
4. **CERTIFIED** — no coding of the dragon word onto ≤ 6 letters is 3-free
   beyond length 3000 (4011 codings tested; 8 survive, all with 7 letters).
5. **CERTIFIED** — in the periodic sign/order family of Gaussian digit walks
   (period ≤ 4), exactly two eight-transition words exist (coding floors 7 and
   6); no member codes onto ≤ 5 letters (length 1200).
6. **CERTIFIED** — no cyclic uniform morphism of length ≤ 16 over four letters
   has a 3-free fixed point beyond 1500; over five letters, none of length ≤ 13
   and twelve of length 14 (Shallit's among them).
7. **CERTIFIED / NUMERICAL** — L(1) = 1, L(2) = 3, L(3) = 7 (controls);
   28 861 282 canonical 3-free words of length 46 over four letters, with the
   consecutive-count ratio ≈ 1.27–1.30 and slowly falling (table
   `data/tf4_46.txt`), so k_min = 4 is not excluded by search.
8. **NUMERICAL** — Shallit's four candidates 3-free to 20 000; the seven-letter
   word to 100 000; the four unproved mixed identifications to 30 000.

## 3. Figures

- **Figure 1 (the walk).** Data: `data/dragon8_prefix4096.txt` decoded via
  `code/dragon.py` — plot the dragon curve Z_n for n ≤ 1024 in the plane, with
  steps coloured by the seven letters (letter = direction + turn, letters 0 and
  4 the same colour). Sentence: "The seven letters are the direction of each
  step together with whether the next turn is left or right; the walk is the
  classical dragon curve."
- **Figure 2 (why it works).** Data: `code/defect.py` output — for pairs
  m < n ≤ 2048, scatter ν₂(|Z_n − Z_m|²) against ν₂(n − m), split by whether
  the endpoint directions are equal, perpendicular, or antipodal. Sentence:
  "The 2-adic size of a chord equals the 2-adic size of its time span unless
  the endpoints point in opposite directions, and the letters are chosen so
  that a weak abelian square can never have opposite endpoints."
- **Figure 3 (the landscape).** Data: `data/codings_3000.txt`,
  `data/family_1500.txt` — a small table/graphic: alphabet size 16 (Shallit,
  proved), 14 (Cambie, draft), 8 and 7 (this note, proved), 6 (Kalviainen,
  draft, reviewed), 5 (Shallit's candidate, 3-free to 38 416 per the
  repository, unproved), 4 (open; count ratio ≈ 1.27–1.30 per letter).
  Sentence: "Everything from 16
  down to 6 is one family of Gaussian-integer walks; 5 and 4 need a new idea."
- **Figure 4 (growth).** Data: `data/tf4_46.txt` — log-count of canonical
  3-free words over four letters by length. Sentence: "Four-letter words with
  no weak abelian square keep multiplying, so nobody will settle k_min = 4 by
  exhaustion."

## 4. Caveats the page must carry

- Kalviainen's 6 and Cambie's 14 are repository drafts (github.com/ekalvi/erdos-193,
  5 Sep 2026), not arXiv papers; their own label is "independent review
  pending, not Lean-formalized". Our reading found no gap; that is our reading.
- Our 7 is *not* the best bound if the draft stands; it is an independent
  proof by a different walk (alternating child order vs alternating digit
  sign). Say so plainly.
- k_min ≥ 4 is Brown 1971 (via abelian squares); Keränen 1992 and Dekking
  1979 are cited only for context and were checked by a scout, not read in
  full (secondary).
- Every "3-free to N" is a prefix check. Only Theorems 1–2 (and the drafts,
  if accepted) concern infinity.
- The twelve five-letter survivors are unreduced modulo symmetry and unproved.
- The dragon-curve/paperfolding identification (Davis–Knuth 1970) is classical
  and cited for orientation only; the note proves what it uses.
- The growth ratio 1.27–1.30 is read off counts for lengths ≤ 46 and is
  slowly falling; it is not a theorem and does not exclude a finite L(4).

## 5. Existing page

None. New page.
