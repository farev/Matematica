# PAGE.md — handoff for the peaceable-queens page (new page)

## 1. Headline claim (one sentence, labelled)

**CERTIFIED** — a(16) = 37: on a 16 × 16 board, 37 white and 37 black
queens can coexist with no queen attacking a queen of the opposite
color, and 38 + 38 cannot — the smallest open case of OEIS A250000,
whose recorded bracket had been [37, 64] since 2014, is decided.

## 2. Contributions (numbered, with the numbers, each labelled)

1. **CERTIFIED** — a(16) = 37. Upper half: exhaustive refutation of
   army size 38 by branch-and-bound over line labelings —
   5,032,610,558 search nodes, 462 s wall on 4 cores, split into 16
   independently completed chunks, every chunk UNSAT
   (`results/n16_m38_bnb_sym_chunk*.txt`). Lower half: an explicit
   37 + 37 placement (`witnesses/witness_n16_m37.txt`) found by both
   engines (177,220,136 nodes / 29 s and 89,333,324 nodes / 17 s) and
   verified by an independent from-the-definition checker.
2. **CERTIFIED** — en route, a(16) ≤ 41 (army size 42 exhausted:
   607,406,702 nodes, 174 s), which already cut the recorded upper
   bound from 64 to 41 before the full decision landed.
3. **CERTIFIED** — the complete known ladder re-derived from scratch
   with no external inputs: a(1..15) = 0, 0, 1, 2, 4, 5, 7, 9, 12, 14,
   17, 21, 24, 28, 32, each value an exhaustive refutation at a(n)+1
   plus a checker-verified witness at a(n) (largest: a(14) at
   2,264,952,960 nodes / 231 s; a(15) at 1,476,498,420 nodes / 156 s).
   For a(14) = 28 and a(15) = 32 no published proof artifact could be
   located (see caveats): these appear to be the first independently
   reproducible derivations.
4. **PROVED** — the line-labeling reformulation (no queen line carries
   both colors, so labeling all 6n−2 lines by {W, B} captures the
   problem exactly: NOTE Lemma 1) and the engine's pruning bounds
   (product, cell, family-sum — Lemmas 3–5) and canonical forms
   (Lemmas 6, 6′), each with a short proof in NOTE.md.
5. Validation stack (the page should present this as the trust story):
   two implementations with node-for-node equality (e.g. 477,786,646
   nodes at the n = 13 boundary, serial and 4-way-parallel alike);
   40/40 verdict agreement against an independent SAT pipeline
   (n ≤ 8, every army size); DRUP-certified UNSAT proofs at the n ≤ 7
   boundaries checked by the repo's own RUP checker; every witness
   re-verified by a checker sharing no code with the search — which
   caught two real bugs during the session (same-cell exclusion
   missing in the first CNF encoder; witness extraction after DFS
   unwinding).

## 3. Figure specs

1. **The a(16) = 37 witness.** Data:
   `witnesses/witness_n16_m37.txt` (17-line text grid: `16 37` header,
   then 16 rows of W/B/.). Render as a 16 × 16 board, white and black
   queens colored. Sentence the reader should say: "37 white and 37
   black queens really do fit — the armies pack into two white and two
   black triangles wedged between the diagonals."
2. **Cost of the exhaustive refutations up the ladder.** Data:
   `results/ladder_bnb.csv` (columns n, m, verdict, nodes, seconds,
   workers, source; use the UNSAT rows, n on the x-axis, nodes on a
   log y-axis, engine change at n = 15 annotated). Sentence: "each
   board size multiplies the exhaustive search by roughly 3–9×, and
   deciding n = 16 took 5 billion nodes — about eight minutes on four
   cores."

No other figures. (A bracket-narrowing timeline was considered and
dropped: two numbers, 64 → 41 → exact, don't need a figure.)

## 4. Caveats the page must carry

- **Every literature citation is (secondary).** The sandbox could not
  fetch arxiv.org, oeis.org, or any primary source (egress-blocked);
  all claims about prior work come from search snippets retrieved
  2026-08-17. In particular: Pratt's 2014 bounds and the values
  a(1)–a(13) attribution (OEIS A250000), the statement that only 15
  terms were known and the 0.1716n² asymptotic bound
  (arXiv:2406.06974, Clinch–Drescher–Huynh–Saffidine), Ainley 1977
  constructions, Bosch 1999 origin.
- **Provenance of a(14), a(15) is unresolved from here**: they are
  reported known (2024 survey) but we could not determine who proved
  them or find a proof artifact. The "first reproducible artifacts"
  claim is phrased against what we could verify and must stay hedged.
- **arXiv:2406.06974 may contain finite-n data at n = 16** invisible
  to snippets; "recorded bracket [37, 64]" is specifically the OEIS
  entry's recorded state, and the page should say "OEIS-recorded".
- **Certification basis differs by n**: DRUP proof files exist for the
  n ≤ 7 boundaries only; for n ≥ 8 the certificate is the proved
  lemmas + the two-engine/SAT-cross-validation stack + committed
  chunk records. Say this plainly; do not imply a DRUP proof of the
  n = 16 result exists.
- **A second, plain-engine full exhaustion of m = 38 was still running
  at session end** (`results/n16_m38_bnb_chunk*.txt`). It is
  redundancy, not a dependency — but if it has completed by page-build
  time, check it reported all-UNSAT and add its node total; if it
  found anything else, STOP and re-open the investigation before
  publishing.
- Attack model: A250000's convention — attacks are not blocked by
  intervening pieces. The ladder controls (a(1..13) reproduced
  exactly) are the operational evidence this is the right model.
- AI assistance (Claude) per repo policy; disclosed on the page.

## 5. Existing page

None — this is a new conjecture directory and a new page
(`fabianarevalo.com/peaceable-queens`). After the page is live, add
the `· [page ↗]` link to the top-level README row.
