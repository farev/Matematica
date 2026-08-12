# PAGE.md — signed-difference-sets (update to the existing page)

A page already exists at fabianarevalo.com/signed-difference-sets.
This is an **update**, not a rebuild. Everything from the 08-09 session
stands; the change is that the page's advertised open target has been
settled externally and we verified the settlement.

## 1. Headline claim (one sentence)

The (32,20,4) door this page left open is now closed: signed
(32,20,4) difference sets exist in an abelian group of order 32
exactly when the group is noncyclic, and no abelian group of order 36
admits a signed (36,29,4) difference set (Masselot, v1.0, 2026-08-12;
every leg independently verified in this repository) — CERTIFIED, with
one new fact of ours: the C18 quotient system of (36,29,4) is empty,
so the order-36 classification no longer leans on the database's
unreplicated cyclic exhaust.

## 2. Contributions of this session (numbered, labelled)

1. **CERTIFIED.** Masselot's census cross-checked cell by cell: his 68
   targets are exactly the 68 Open cells of order ≤ 36 in the frozen
   snapshot; 58/58 verdict agreement with our census (zero conflicts,
   his novelty screen credits this repo); his 10 novel cells are
   exactly our 10 undecided ones.
2. **CERTIFIED.** All 16 of his existence witnesses (including the six
   noncyclic (32,20,4) constructions) pass this repo's independent
   checker; the six order-32 witness-file hashes match his note's
   table byte for byte.
3. **CERTIFIED.** All four nonexistence legs re-derived with
   review-owned code, complete searches, no symmetry reduction:
   C32 via C8→C16→C32 (2,985,984 final refinements, 0 solutions);
   C2×C18 and C3×C12 via full quotient systems (0 solutions each);
   C6×C6 via 16,964,640 marginal-consistent ternary vectors (0
   survive), so the one SAT/DRAT leg of his proof now has a
   solver-free independent proof. Every count in his note's §5–§7
   (9,528 / 56 / 12 / 248,832 / 144 / 420 / 106,353 / 9) reproduced
   exactly. Controls first: 4/4 known-answer checks, including exact
   40-set equality with our (20,11,2) complete enumeration.
4. **CERTIFIED (new fact).** The C18 quotient system of (36,29,4)
   (cells in [−2,2], sum 13, norm 33, all shifts 8) is empty, so
   SDS(36,29,4) is impossible in C36 and C2×C18 at once. NOTE §5.1.
5. **Caveat resolved.** Gordon's paper and He–Chen–Ge read in full
   (session 1 was egress-blocked): neither states the T1/T2 transfers,
   so the page's "possible rediscovery" hedge on the two criteria can
   be dropped; Lemma 1 = Gordon's Lemma 1.1 + He–Chen–Ge Lemma 2.2.

## 3. Figure specs

1. **The (32,20,4) row across order 32.** Data:
   `masselot-review/out/targets_report.json` (verdicts) +
   `masselot-review/out/witness_verification.csv` (witness validity),
   seven groups: [32] empty, all six noncyclic exist. Style it like
   the existing (32,28,12) seven-group exhibit so the two rows sit
   together. Sentence a reader should say after looking: "At
   (32,20,4) existence splits exactly at cyclicity, and at (32,28,12)
   it splits at containing Z₄×Z₄, so no single subgroup rule explains
   order 32."
2. **The quotient ladder, one panel.** Data: the stage counts in
   `masselot-review/out/targets_run_log.txt` (C8: 9,528 → 56; C16:
   492,096 tried → 144; C32: 2,985,984 tried → 0). Sentence: "A
   search priced at 48 core-hours collapses to six seconds when you
   walk it down a quotient ladder, because the correlation identity
   already kills almost everything at C8."

No figure for the C18 observation (it is one sentence; put it in
prose next to the order-36 paragraph).

## 4. Caveats the page must carry

- The six (32,20,4) constructions are Masselot's (CC BY 4.0),
  verified here; the page must credit
  github.com/NicolasMasselot/certified-small-sds-census v1.0 and
  Zenodo doi:10.5281/zenodo.21901581 as the source of the closure.
  We verified; we did not discover.
- His C6×C6 DRAT certificate was not re-checked here; it was made
  non-load-bearing by our direct search instead. Say "two independent
  proofs" (his checked DRAT + our search), not "we audited the DRAT".
- Our C36/C2×C18 statement via C18-emptiness is CERTIFIED computation
  (complete enumeration), with the projection lemma (NOTE §5.1
  Lemma 3) as the PROVED step.
- Timeline for the record: his v1.0 released 2026-08-12 09:50 UTC;
  his ledger discovered our repo at the final-audit stage after his
  decisions were made, so the 58-cell agreement is genuinely
  independent replication in both directions.
- Secondary-source hedges that remain: Turyn 1965 and the classical
  even-order square condition are still cited secondhand.

## 5. What changed vs. the live page

- Open question 1 (the (32,20,4) family, advertised as "the natural
  next target") is settled: update that paragraph and the open-questions
  list; keep the 08-09 census numbers unchanged (they are untouched).
- Add the session-2 block: verification of Masselot + the C18
  observation + the two figures above.
- Drop the "possible rediscovery" hedge on T1/T2 (per contribution 5),
  keeping the "criteria are classical in substance" sentence.
