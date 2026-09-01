# Session writeup — 2026-08-29

The narrative, including the wrong turns. Companion to NOTE.md.

## How the problem was found

Today's slate came from three parallel scouts (Erdős database + forum
threads, recent arXiv, OEIS/MathOverflow) on a day when, unusually, all
four literature sources were reachable from the sandbox (the two previous
sessions ran fully blocked). The OEIS scout surfaced A333331: a
Stanley-authored entry, stuck at eight terms since 2020, carrying two
2024 conjectures (Howroyd's e.g.f., Wiseman's graph equivalence) and a
link to Selig's sandpile paper. The pre-selection check found the
Amanbayeva–Wang paper answering the count only as a slice-sum and asking
for the Ehrhart polynomial — so the *question* was open in print, not
just in a database comment. Mid-session, Selig's EJC 2024 paper turned
out to pose the same enumeration as an explicit open question. That is
the best possible shape for a session: the same number wanted by three
independent communities, none of which had computed a ninth term.

## Timeline of the attack

1. **Facet description → sorted-prefix characterization.** Stanley's
   inequalities depend only on subset size, so integer membership reduces
   to top-k prefix sums against σ(k). Hand-checked at n = 2, 3 against
   the published 3 and 17 before anything else.
2. **DP for terms.** A multiplicity DP with exact multinomials (with a
   convexity argument for checking only run endpoints — Lemma proved in
   passing, worth keeping as it makes the DP O(poly)). Reproduced all 8
   published terms; produced a(9)–a(24) immediately. a(9)–a(11) matched
   the values Howroyd had listed as "expected" from his conjectured
   e.g.f. — the first independent confirmation, and instantly a 3×
   extension of the e.g.f.'s tested range.
3. **Reformulations.** Shifting by 1 turns the facets into the
   polymatroid of ∂(I) = #edges of K_n meeting I; Hall gives "in-degree
   vectors of partial orientations of K_n"; enumeration confirmed the
   correspondence as sets (not just counts) for n ≤ 5.
4. **Literature deep-read.** Selig: SR states = lattice points
   (Thm 26), subset-sum characterization (Thm 18) — which is exactly the
   complement of the partial-orientation picture — and the §6 open
   question. Postnikov §9/§11 read for the draconian machinery.
5. **The key step.** Lifting the polymatroid to Σ Δ_{{0,i,j}} and
   applying Postnikov's Theorem 11.3 with y = (0, 1, …, 1) makes every
   raising-factorial factor equal 1, so a(n) is *the number of draconian
   sequences*. Unwinding the dragon condition: every union bound is
   {0} ∪ V(F), so the condition is exactly "every component of the
   multiplicity multigraph has #E ≤ #V" — trees and unicyclic components,
   with doubled pairs as 2-cycles, multiplicity ≤ 2 forced. Verified by
   enumeration against a(n) for n ≤ 5 before trusting it.
6. **The count.** Per component: trees + edge-doubled trees = k^{k−2} +
   (k−1)k^{k−2} = k^{k−1} = loop-rooted trees (labeled dissymmetry /
   Cayley arithmetic); cycle-length-≥ 3 components are literally shared.
   So the sparse multiforests are equinumerous with Wiseman's unicyclic
   loop-graphs, componentwise. Everything else (e.g.f., Howroyd's form,
   Wiseman's Hall lemma, Selig's corollary, asymptotics) followed in an
   hour of careful writing.
7. **Novelty check → near-miss discovery.** A targeted pass over the
   Dec 2025 Liu–Thawinrak paper (the newest paper on these polytopes)
   found their Corollary 7.6: the general draconian-sum Ehrhart formula
   for u-parking polytopes, via the same lift. Their Example 7.4 with
   p = 0, q = 1 is (a translate of) our sum of triangles. They never
   specialize the draconian set, never touch A333331 or the enumeration.
   Theorem B was reframed as their specialization plus the new
   identification; Theorem A is untouched. This is exactly what hard
   rule 3 is for, and the note is more useful for citing them.
8. **Verification battery.** Twelve checks, all exact (NOTE §7): three
   independent computations of a(n) at small n plus the graph side in
   both Python and C (u(8) = a(8) over 30.2M subsets), the Ehrhart
   formula three ways, exact rational hull membership at n = 3, 4
   (a from-scratch phase-1 simplex over fractions — no floats), Ehrhart
   reciprocity against brute interior counts, and the asymptotic
   constant against a(40).

## What failed or was discarded

- **Two wrong reformulation guesses, killed by arithmetic.** (i) The
  guess that the count might be a Tutte evaluation of K_n: T(K_3; 3, 1)
  = 13 ≠ 17. (ii) The guess that the shifted polytope is the zonotope of
  {e_i − e_j} ∪ {e_i}: its lattice-point count at n = 2 is 7 ≠ 3.
  Both died in minutes on paper; recorded so they are not retried.
- **The burning-bijection route not needed.** Before finding the
  draconian route, the plan was to extend Dhar/Cori–Rossin burning to
  Selig's stochastic algorithm and read off unicyclic components from
  the burning record. Plausible but unfinished — superseded by the
  Postnikov route. It survives as NOTE §9's open question 1, and would
  give the *bijective* version of Theorem A.
- **A misleading first fetch.** The initial WebFetch summary of
  Liu–Thawinrak ("normal fans only, no lattice points", via a scout)
  was wrong — the full PDF has an Ehrhart section. The session rule
  "read the actual paper before claiming novelty" caught it; a claim
  written an hour earlier would have over-stated Theorem B. Nothing was
  ever committed with the over-claim.
- **Small tooling friction.** WebFetch is 403-blocked on oeis.org,
  erdosproblems.com, mathoverflow.net (curl works for all three);
  arXiv's /html/ links 404 for some papers (v3 of Selig) — PDFs via
  /pdf/ + pdftotext worked throughout. The first OEIS JSON parse assumed
  a dict where the API returns a bare list for some queries.
- **Selection cost.** Steps 1–3 of the mandate (connectivity, slate,
  internal assessment) consumed roughly the first fifth of the session;
  within budget.

## Reproducibility

Environment: cloud sandbox, 4 cores, 15 GB RAM, Python 3.11.15,
gcc 13.3.0. No randomness anywhere; no floats in any certified path
(floats appear only in the asymptotic-ratio display). Total compute for
everything in NOTE §7: under ten minutes; the only long-ish run is
u(8) in C (~3 min single-core).

## Honest assessment

The theorem is real but the proof is assembly: Stanley's facets,
Postnikov's Theorem 11.3, and elementary counting. The two things that
were genuinely found today are the identification "draconian sequences
for the coned triangle configuration = sparse multiforests" (Lemma 4 —
the coned counterpart of Postnikov's own forests example) and the fact
that this closes, at once, two OEIS conjectures, Amanbayeva–Wang's
question, and Selig's open question, with certified data to n = 40
behind it. The right upstream moves (OEIS edit, notes to the four people
named) need the local machine.
