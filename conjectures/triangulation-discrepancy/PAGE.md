# PAGE handoff — triangulation-discrepancy (new page)

1. **Headline claim.** Basti–Cremaschi's refined discrepancy bound disc(T) ≤ n − 2⌈(n+2)/3⌉
   for plane triangulations, open for n ≡ 5 (mod 6), holds at the next two open orders
   n = 17 (all 129,664,753 triangulations, full census) and n = 23 (every configuration
   allowed by the structure theorem, 948,057 of them, has discrepancy 1), and is
   PROVED whenever the balanced four-colouring's big class has no vertex of degree ≥ 5;
   a structure theorem (PROVED) pins down what a counterexample would have to look like.

2. **Contributions.**
   1. PROVED — a counterexample on n = 6m+5 vertices must have a 4-colouring with classes
      (3m+2, m+1, m+1, m+1), a fully mixed big class with ≥ 2m+3 vertices of degree 3,
      1 to m−1 vertices of degree ≥ 5, none of degree 4; every other vertex on a face
      avoiding the big class; no vertex with more than 2m+1 degree-3 big-class neighbours;
      and every single flip blocked (NOTE Theorem 2).
   2. PROVED — disc(T) ≤ 2m−1 when the big class has only degree-3 vertices, i.e. for every
      stellation of an equitably 3-coloured Eulerian triangulation on 3m+3 vertices at
      3m+2 faces (NOTE Theorem 3).
   3. CERTIFIED — disc(T) ≤ 3 for all 129,664,753 triangulations on 17 vertices; 2,652
      attain it (certificates committed). 15 min on one core.
   4. CERTIFIED — n = 23: disc(T) ≤ 5 = U(23) for every triangulation on 23 vertices; the
      948,057 candidate configurations all have discrepancy 1, 277 s (the 60 billion triangulations of that order are far
      beyond brute force; the structure theorem reduces the check to 109.5 million plane
      graphs on 12 vertices).
   5. CERTIFIED — the exact discrepancy distributions for 13 ≤ n ≤ 17, extending the
      authors' Table 2 (n ≤ 12): 4, 422, 89, 14, 2,652 extremal triangulations; the
      refined bound is attained at every order.
   6. CERTIFIED — the published Table 2 reproduced by two independent implementations.

3. **Figure specs.**
   - *Figure 1 — the two bounds and the data.* Data: `results_census_13_17.txt` plus
     [BC] Table 2 for n ≤ 12: for each n from 6 to 17 plot the maximum discrepancy found
     (0,1,0,1,2,1,2,3,2,3,4,3) against the universal bound n − 2⌈n/3⌉ and the refined
     U(n); mark n = 11, 17 (open class) in a different colour. Sentence: "At every order
     the largest discrepancy that actually occurs is the refined bound — including the two
     orders where nobody has proved that it must be."
   - *Figure 2 — how rare the extremal triangulations are.* Data: the same file; fraction
     of triangulations attaining U(n) for n = 10..17 (2/233, 0/1249 at U=1 means all,
     16/7595, 4/49566, 422/339722, 89/2406841, 14/17490241, 2652/129664753) on a log scale.
     Sentence: "Extremal triangulations become vanishingly rare as n grows."
   - *Figure 3 — the shape of a would-be counterexample.* A diagram from NOTE Theorem 2:
     an independent set of (n−1)/2 vertices (mostly degree 3) sitting in the faces of a
     3-coloured plane graph on (n+1)/2 vertices, every outer vertex touching an
     unoccupied triangle. Sentence: "Any counterexample would have to look like this, and
     at n = 17 and 23 nothing that looks like this fails."

4. **Caveats the page must carry.**
   - The residue class is NOT settled: the theorem covers the degree-3 case; the general
     case is open, with the obstruction described precisely.
   - The n = 23 result is a certification through the structure theorem, not a census;
     it relies on plantri generating all 2-connected plane graphs with the stated
     parameters and on Lemmas 1–5.
   - The balanced four-colour theorem is used as stated in its arXiv abstract (secondary).
   - The n ≥ 12 census values come from a single implementation (cross-validated with a
     brute force for n ≤ 11 and against the paper's table for n ≤ 12).
   - Asayama–Matsumoto and Arevalo Loyola et al. are cited via [BC] (secondary).

5. **Existing page:** none. New page.
