# PAGE.md — handoff for the site build (fabianarevalo.com/plus-minus-davenport)

New page (no existing page for this conjecture). Strongest-result row added
to the top-level README this session.

## 1. Headline claim (one sentence, labelled)

The last unknown plus-minus weighted Davenport constant of order ≤ 100 is
decided: **D±(C5⊕C15) = 6** (lower bound PROVED, upper bound CERTIFIED by
six independent exhaustive computations across three distinct methods) —
the single cell Marchan–Ordaz–Schmid's 2014 determination of all groups of
order ≤ 100 left open (secondary).

## 2. Contributions (numbered, labelled)

1. **D±(C5⊕C15) = 6** — lower PROVED (explicit dissociated 5-set
   {(0,1),(0,2),(0,4),(1,0),(2,0)}, two-line proof via binary sets in the
   factors), upper CERTIFIED: no dissociated 6-set, established by
   (i) DFS census over sign-representatives, 139,052 nodes, C and Python
   implementations agreeing node-for-node; (ii) the same DFS with no
   sign reduction, 3,520,083 nodes, matching the predicted 2^l identity in
   every size class; (iii) plain combination enumeration, 2,324,784
   (sign-reps) and 185,250,786 (all elements) six-element sets, zero
   dissociated; (iv) a class-injectivity reduction to F₅² (Lemma R),
   all seven splits infeasible.
2. **D±(C7⊕C21) = 8** — upper PROVED (subset-sums cap ⌊log₂147⌋ = 7),
   lower CERTIFIED (explicit 7-set verified against all 2,186 signed
   subsets; 2,016 maximum sets counted up to sign). First case of the next
   family reported open "already for n = 3" (secondary). **Caveat that the
   page must carry:** a 2021 PhD thesis computed many values with
   100 < |G| ≤ 200 "with some exceptions" — whether order 147 is among
   them was not verifiable from the sandbox.
3. **CERTIFIED table of dissociation numbers** dim±(G) = D±(G) − 1 for
   ⟨N_FINAL⟩ groups of rank ≤ 4 (all rank-2 of order ≤ 256, rank-3 to
   order 200, cyclic to 128, targeted cells to order ~450), every value
   from exhaustive search with exact cross-engine node-count agreement
   (`data/table.csv`).
4. **PROVED window + forced families**: floor ≤ dim± ≤ cap with
   floor = max Σ⌊log₂ nᵢ⌋ over cyclic decompositions, cap = ⌊log₂|G|⌋
   (subset-sum argument valid for all G, not only odd order); all
   2-groups and the C2⊕C2n family forced (recovering known values,
   (secondary), with two-line proofs).
5. **Structure findings (CERTIFIED data + PROVED where stated):** at rank 2
   every computed gap cell sits at an endpoint of its width-1 window —
   only C3⊕C3 and C5⊕C15 stuck at the floor; the first strictly
   intermediate value appears at rank 3 (dim±(C3⊕C3⊕C15) = 6, window
   {5,…,7}); appending a C₂ factor can raise dim± by 2 (C5⊕C15 → C5⊕C30:
   5 → 7) though the easy bound is +1 (PROVED).
6. **Lemma R (PROVED)**: dissociativity in C_p⊕C_{3p} is equivalent to a
   subset-sum injectivity system over F_p²; it shows no counting argument
   can decide C5⊕C15 (class sizes 22/21/21 inside 25) and localizes the
   75-vs-147 contrast to a finite field-plane statement.

## 3. Figure specs

1. **The window chart.** Data: `data/table.csv` (columns order, dim, floor,
   cap, verdict), rank-2 rows. Plot dim± minus floor (0 or 1 or the MID
   fraction) vs order, colored FORCED/FLOOR/CAP/MID. Sentence a reader
   should say: "Almost every small group sits exactly at its upper window
   endpoint — the rare exceptions, all built from the primes 3 and 5,
   include exactly one group below order 100."
2. **The two extremal cells.** Data: `certs/e1_c5c15_signred.txt`,
   `certs/e1_c7c21_signred.txt` (bysize censuses). Side-by-side bar chart
   of the per-size counts of dissociated sets for |G| = 75 and 147, with
   the hard stop at size 5 vs the spike at size 7. Sentence: "75 has
   85,155 maximum five-element dissociated sets and not a single
   six-element one; 147 packs seven elements 2,016 different ways."
3. **The verification matrix.** Data: NOTE §3 Thm 1 table (six rows).
   A small table graphic, engines × methods, all agreeing. Sentence:
   "The negative result is not one program's word: two DFS censuses, two
   brute enumerations and a finite-field reduction all return zero."
   (No plot data beyond the NOTE table — if that fails the no-sentence
   test, drop this figure.)

## 4. Caveats the page must carry

- Every literature statement is **(secondary)**: the sandbox could not open
  arXiv, HAL, OEIS, or any journal page; all sourcing is search-snippet
  level, including the headline "only unknown ≤ 100" quote (two
  independent snippet digests agree, but the PDF itself was unreadable).
  Primary-source verification (arXiv:1308.3316, the Perez-Lavin thesis,
  the Adhikari survey chapter) is required before any external claim.
- The Perez-Lavin thesis caveat on D±(C7⊕C21) (contribution 2) and on all
  table rows with 100 < |G| ≤ 200.
- The upper bound in the headline result is CERTIFIED, not PROVED — a
  finite exhaustive computation, however redundant; the sharpest open
  thread is a human proof via Lemma R.
- Structural observations (endpoint dichotomy, C₂-jump) are new-to-us;
  novelty against the unreachable literature is unassessed.
- The "23, 46, 47" motivation for the C23⊕C23 attempt is a snippet whose
  context could not be verified; the attempt itself is undecided (a
  failed randomized hunt proves nothing).

## 5. Existing page

None — new conjecture directory, new index row this session.
