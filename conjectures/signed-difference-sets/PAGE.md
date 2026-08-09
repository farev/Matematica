# PAGE.md — handoff for the local page build (signed difference sets)

New conjecture directory; no page exists yet. This session's results
create the row, so a page is due at `fabianarevalo.com/signed-difference-sets`.

## 1. Headline claim (one sentence)

In one session, the open shelf of Gordon's signed-difference-set database
dropped from 67,823 cells to 22,453: **PROVED** — two classical
nonexistence criteria transfer to signed difference sets and close 45,328
open cells; **CERTIFIED** — validated exhaustive search decides 58 more,
finding 10 signed difference sets that exist in no published source; and
a **CERTIFIED** audit shows 147 of the database's own 280 stored example
sets fail its defining equation (22 of them repaired).

## 2. Contributions (numbered, with labels)

1. **PROVED.** For every nontrivial character χ of G, |χ(A)|² = k−λ
   (NOTE Lemma 1). Consequences applied cell-by-cell: (T1) if |G| is
   even, k−λ must be a perfect square; (T2, Turyn transfer) if m | exp(G),
   m > 2, p ∤ m, p^j ≡ −1 (mod m), and v_p(k−λ) is odd, no SDS exists.
   **45,328 of 67,823 Open cells closed** (T1: 23,997; T2: 21,331), each
   with a one-line certificate (`data/theory_closures.csv`). Controls:
   0 violations on all 146 Yes/All cells; 984 of Gordon's 2,574
   exhaust-No cells retro-covered. The criteria are classical and marked
   as possible rediscoveries (the paper is unread in the sandbox — see
   §4); the per-cell closures are new to the database regardless.
2. **CERTIFIED.** 58 previously-Open cells decided by an exhaustive
   engine validated on the entire decided v ≤ 24 database (42 cells,
   zero discrepancies) and by exact witness-list agreement with an
   independent Python implementation on 8 cells. **10 EXIST** — new
   signed difference sets, each with an independently re-verified
   witness: SDS(25,12,1) in Z₅×Z₅ (λ = 1); SDS(27,10,1), SDS(27,14,5)
   in both non-cyclic groups of order 27; SDS(27,17,8) in Z₃³;
   SDS(32,28,12) in Z₄×Z₈ and Z₂×Z₄×Z₄; SDS(36,11,2) in Z₆×Z₆ and
   Z₃×Z₁₂. **48 NONEXIST.** Zero conflicts with the criteria.
3. **CERTIFIED.** Structure-decides-existence exhibits: at order 27 the
   cyclic group is empty across all ten parameter triples while the two
   non-cyclic groups carry SDS at three of them; SDS(36,11,2) exists
   exactly when the 3-Sylow is non-cyclic; SDS(32,28,12) exists in
   exactly the two of seven order-32 groups containing Z₄×Z₄
   (**the Z₄×Z₄ reading is NUMERICAL** — a 7-point observation, not a
   theorem; say so on the page).
4. **CERTIFIED (audit).** 147 of the 280 witness sets stored in the
   published database fail its own defining equation (21 of 144
   witness-bearing cells). Forensics on SDS(20,11,2) in Z₂₀: the cell
   has exactly 40 labeled sets in 2 translation classes and the stored
   sets are true sets with P↔M sign swaps — an export defect, not a
   search error. ≤2-swap repair recovers re-verified witnesses for 22
   sets across 12 of the 21 cells. Upstream report drafted
   (`UPSTREAM.md`), to be sent from a connected machine.

## 3. Figure specs

1. **The shelf collapse.** Data: `data/sds.json` statuses +
   `data/theory_closures.csv` + `data/values.csv`. A single horizontal
   stacked bar (or two bars, before/after): 70,543 cells = 2,720
   decided-before / 45,328 closed by criteria / 58 decided by exhaust /
   22,453 still open. Sentence a reader should say: "Two classical
   theorems and one afternoon of exhaustive search settled two-thirds of
   the open questions in this database."
2. **Group structure decides.** Data: NOTE §5 tables (order-27 and
   order-32 exhibits, machine-readable via `data/values.csv` +
   `data/sds.json`). A small grid: rows = groups of order 32, one column
   = (32,28,12), cells colored exists/empty; beside it the order-27
   grid. Sentence: "The same parameters can have a signed difference set
   in one group of order 32 and none in another — and at order 27,
   cyclic is always the empty one."
3. **The audit.** Data: `data/witness_audit.csv` (+ the profile of one
   corrupt set from WRITEUP/check scripts). Bar chart of the 280 stored
   sets by verdict (133 valid / 147 invalid), with the repaired 22
   highlighted. Sentence: "Half the example sets shipped with the
   database don't satisfy its own equation — most are one sign-swap away
   from sets that do."

## 4. Caveats the page must carry

- Gordon's paper (arXiv:2212.10630) and Turyn 1965 are cited
  **(secondary)** — egress-blocked; the criteria may appear in Gordon's
  paper. The database snapshot, his reference checker, and his README
  are primary (fetched 2026-08-09, sha256 pinned in NOTE/certs).
- Nonexistence-by-exhaust is relative to the validated engine (dual
  implementation, 42-cell concordance, EXIST-side controls); there is no
  independent DRUP-style certificate for a completed search — state the
  validation, not more.
- The Z₄×Z₄ / non-cyclic-Sylow patterns are observations from ≤ 10 data
  points each, not theorems.
- The remaining 9 corrupted cells' Yes/All statuses rest on Gordon's
  original exhaust claims alone.
- He–Chen–Ge (arXiv:2306.05631) is (secondary); their ten cells are
  credited inside the database itself.

## 5. Existing page

None — new conjecture, new page. Index row added to the top-level README
this session.
