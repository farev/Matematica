# PAGE.md — handoff for the local publish pass

New conjecture directory; new page needed at `fabianarevalo.com/parking-polytope`.
Link it from the top-level README row (already added) and from this
conjecture README header once live.

## 1. Headline claim

**PROVED.** The number of lattice points of the parking-function polytope
(the convex hull of all parking functions of length n) equals the number
of loop-graphs on n labeled vertices with n edges in which every
connected component contains exactly one cycle — equivalently, the
e.g.f. is exp(−½log(1−T) + T/2 − T²/4) with T the tree function. This
proves both open conjectures in OEIS A333331 (Howroyd Jan 2024, Wiseman
Mar 2024) and answers the open enumeration question of Selig,
Electron. J. Combin. 31(3) (2024) §6, for the recurrent states of the
stochastic sandpile model on complete graphs.

## 2. Contributions

1. **PROVED (Theorem A).** a(n) = u(n) (unicyclic-component loop-graphs);
   e.g.f. exp(−½log(1−T) + T/2 − T²/4). Corollaries: Howroyd's A333331
   e.g.f. conjecture; Wiseman's choosability conjecture; Selig's open
   question — |StoRec_n| = u(n).
2. **PROVED (Theorem B).** Ehrhart polynomial of P_n:
   i(P_n, t) = Σ_M t^{s(M)} (t(t+1)/2)^{d(M)} over "sparse multiforests"
   M (multigraphs on [n], pair multiplicities ≤ 2, every component a tree
   or unicyclic), with closed e.g.f. (1−τ)^{−1/2} exp((2−t)τ/(2t) −
   τ²/(4t)), τ = T(tx). Answers Amanbayeva–Wang's question 6(b). The
   sum-form specializes Liu–Thawinrak (Dec 2025) Cor. 7.6 — the page must
   carry this credit; the identification of the index set and the closed
   form are new.
3. **PROVED (Corollary A4).** a(n) ~ C·n^{n−1/4},
   C = e^{1/4}√(2π)/(2^{1/4}Γ(1/4)) = 0.7464918… (the asymptotics half of
   Selig's question). The hull holds ~0.2746·n^{3/4} times more lattice
   points than there are parking functions.
4. **CERTIFIED.** a(1)–a(40) by exact DP over Stanley's facet
   description — the first independent computation of any term past a(8);
   all 8 published terms reproduced; Howroyd's e.g.f. (previously
   supported by 8 fitted terms) matched exactly through n = 40. Key new
   values: a(9) = 167 341 283, a(10) = 4 191 140 394,
   a(11) = 116 425 416 531.
5. Twelve-check verification battery, all exact arithmetic (NOTE §7):
   three independent computations of a(n) at small n; the graph side
   brute-forced independently in Python (n ≤ 7) and C (n = 8, 30.2M
   subsets); Ehrhart three ways; exact rational hull membership at
   n = 3, 4; Ehrhart reciprocity vs brute interior counts.

## 3. Figure specs

1. **The n = 3 picture.** Data: none needed (17 = 16 + 1 is drawable by
   hand: the 16 parking functions of length 3 plus the one extra lattice
   point (2,2,2) of their hull; the hull is a 3-dimensional polytope —
   draw the sum-slice at Σ = 6, a hexagon-ish permutohedron slice, with
   (2,2,2) in its center). Reader sentence: "The convex hull of parking
   functions contains lattice points that are not parking functions —
   the first one is (2,2,2) — and counting them all is the problem."
2. **The dictionary figure.** Data: the 17 loop-graphs for n = 3 are
   listed verbatim in OEIS A333331 (Wiseman's comment, quoted in
   NOTE §1/§8 context). Draw the 17 loop-graphs in a grid (loops as
   circles at a vertex). Reader sentence: "Each lattice point corresponds
   to one of these graphs: n edges on n vertices, every piece carrying
   exactly one cycle."
3. **Growth against the conjectured-then-proved e.g.f.** Data:
   `a_values.txt` (n, a(n)) for n ≤ 40. Plot a(n)/(C·n^{n−1/4}) vs n
   (values 0.998 → 0.984; from `asymptotics_check.py` output). Reader
   sentence: "The proved asymptotic law a(n) ≈ 0.7465·n^{n−1/4} is
   already accurate to within 2% by n = 40."

## 4. Caveats the page must carry

- The proof stands on two published theorems used as black boxes:
  Stanley's facet description of P_n (established in Amanbayeva–Wang,
  ECA 2022 — additionally verified computationally here at n = 3, 4 by
  exact rational hull membership) and Postnikov's Theorem 11.3 (IMRN
  2009). Both were read in the original today (primary sources).
- Theorem B's **sum-form is a specialization of Liu–Thawinrak,
  arXiv:2512.14199 (Dec 2025), Corollary 7.6** — state this prominently;
  what is new is the combinatorial identification of the draconian index
  set (sparse multiforests) and the closed e.g.f. Lemmas 1–3 (the
  Minkowski-sum realization) are marked as independent rediscovery,
  implicit in their Example 7.4.
- The asymptotic constant's numerical ratio at n = 40 is 0.984 (slow
  O(n^{-1/2})-type corrections); the law is proved, the convergence is
  visibly incomplete at n = 40 — the figure should say so.
- All citations were verified against primary sources read today
  (Amanbayeva–Wang, Postnikov §9/§11, Selig, Liu–Thawinrak §7, live OEIS
  entries A333331/A368596/A368951). No (secondary) marks remain in the
  note.
- Upstream reporting (OEIS edit, notes to Selig/Howroyd/Wiseman, possible
  arXiv note) is pending and needs the local identity — the page should
  not claim it has happened.

## 5. Existing page

None — new page.
