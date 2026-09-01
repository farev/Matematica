# PAGE.md — handoff for the projective-chromatic write-up page

New page (no existing page for this conjecture). Built from session 1
(2026-09-01). **Check `data/ord5_status.md` and the final session commit
before building: the two order-5 UNSAT runs were still live at first
push, and their outcome upgrades or trims claims below** (each spot
marked ⏳).

## 1. Headline

**PROVED + CERTIFIED** — On the newest open case of the chromatic number
of projective spaces (χ₂(8) ∈ {5,6}, Problem 1 of
Bishnoi–Cames van Batenburg–Ravi 2025, where the answer 5 would improve
the multicolor Ramsey bound to R(3;5) ≥ 257): any 5-coloring of PG(7,2)
with no monochromatic line — if one exists at all — can have essentially
no symmetry: no collineation of order 3, 7, 31 or 127 (proved, a
Mersenne-prime obstruction valid for every n and k), none of order 17
and no field Frobenius (certified, DRUP-checked), ⏳ and none of order 5
if both pending runs land UNSAT, which would make every witness's
automorphism group a 2-group.

## 2. Contributions

1. **PROVED (Lemma B).** For every prime p = 2^d − 1 (d ≥ 2): no proper
   coloring of any PG(n−1,2), with any number of colors, is invariant
   under a collineation of order p. In GL(8,2) this kills orders 3, 7,
   31, 127 at one stroke; only odd orders 5 and 17 survive the lemma.
2. **CERTIFIED.** No proper 5-coloring of PG(7,2) is invariant under
   any order-17 collineation: single Sylow class, orbit-contracted
   75-var instance, UNSAT with a 131-line DRUP proof verified by the
   repo's independent from-the-definition checker
   (`certs/ord17.{cnf,drup}`). Same for the Frobenius x ↦ x² of F₂₅₆
   (35 cells, 5,227-line DRUP, verified; `certs/frob.{cnf,drup}`).
3. ⏳ **Order 5** (two conjugacy classes, [C,C] 51 cells / [C,I] 63
   cells, instances audited byte-identical by an independent rebuild —
   `audit_contraction.py`): status at page-build time decides whether
   the page says "every witness has a 2-group stabilizer" (both UNSAT)
   or "pending" (still running) or reports an invariant witness (SAT
   would decide χ₂(8) = 5 outright).
4. **CERTIFIED.** PG(6,2) — one level down — *does* admit an
   order-5-invariant proper 5-coloring: explicit witness, class sizes
   [21,21,25,27,33], re-verified from the definition
   (`data/witness_n7_ord5.txt`); ≥ 10⁵ invariant siblings at the
   quotient level. The symmetry death at n = 8 is not inherited from
   n = 7.
5. **PROVED (Lemma A).** Every color class of a hypothetical witness
   meets every one of the 255 hyperplanes; every hyperplane restriction
   is a proper 5-coloring of PG(6,2) using all 5 colors; no class fits
   inside an affine hyperplane (so "take a maximum sum-free set as one
   class" cannot start).
6. **NUMERICAL.** 1,000 randomized-CDCL 5-colorings of PG(6,2) — 1,000
   pairwise-distinct structural fingerprints — and not one extends over
   a hyperplane split to a coloring of PG(7,2); the order-5-symmetric
   witness does not extend either. Per-class capacity is not the
   obstruction: exact-integer Cayley spectra give Hoffman capacity sums
   ≈ 265–274 against the 128 needed (the failure is simultaneous
   packing). Local search with breakout weighting cracks PG(6,2) in
   ~5×10³ flips but produced nothing on PG(7,2) in ≈ 5×10⁹ flips (estimated).
   Everything is consistent with χ₂(8) = 6 and nothing proves it.
7. **Controls.** The published table χ₂(n) = 2,3,3,4,5,5 (n = 2..7)
   reproduced end-to-end with re-verified witnesses; line counts match
   (2ⁿ−1)(2ⁿ−2)/6 (OEIS A006095).

## 3. Figures

- **F1 — the Mersenne obstruction, one picture.** Data: none needed
  (draw PG(2,2), the Fano plane, with one 7-point orbit circled inside
  F₂³). Reader sentence: "An order-7 symmetry sweeps a whole punctured
  subspace into one orbit, and a monochromatic line comes for free."
- **F2 — the symmetry ledger at n = 8.** Data: table inline in NOTE §3–4
  (orders 3,5,7,17,31,127 × verdict × method: lemma / DRUP / ⏳).
  Reader sentence: "Every odd symmetry order is dead — by hand for
  Mersenne orders, by certified UNSAT for 17 ⏳ (and 5)."
- **F3 — n = 7 vs n = 8.** Data: `data/witness_n7_ord5.txt` rendered as
  a 127-point color strip grouped by the 31 orbit cells (5-cell blocks
  visibly constant), next to an empty 255-slot strip. Reader sentence:
  "One level down the symmetric solution exists and is pretty; at
  n = 8 the same symmetry is impossible."
- **F4 — capacity vs packing.** Data: the 12-row table in
  `NOTE §6` / `alpha_fourier.py` output (Hoffman sums 265–274, greedy
  sums 151–170, needed 128, extensions 0). Reader sentence: "Each color
  class has twice the room it needs, and they still cannot share the
  128 points — the obstruction is global, not local."

## 4. Caveats the page must carry

- χ₂(8) itself remains **open**; nothing here decides it. The
  local-search and extension evidence points at 6 but is explicitly
  NUMERICAL (solver-biased sampling, no uniform model).
- R(3;4) ≤ 62 and 162 ≤ R(3;5) ≤ 307 are quoted from
  Bishnoi–Cames van Batenburg–Ravi §6.1 **(secondary)** — not re-derived
  from Radziszowski's survey here.
- The 1,000 non-extensions are Cadical verdicts (each a 640-var
  instance, trivially re-runnable); a 50-witness subsample is
  DRUP-certified end-to-end (50/50 verified), and the
  order-17/Frobenius exclusions ship DRUP certificates in `certs/`.
- ⏳ kissat proofs for the order-5 instances are DRAT and may contain
  RAT steps the repo's strict RUP checker rejects; if so the page must
  say "checked by drat-trim" (different trust base) or "solver verdict
  only", whichever is true at build time.
- The color-symmetry-broken variants (`*_cbrk`) rely on a hand-proved
  WLOG (value precedence under the S₅ color action); any claim built on
  them is "CERTIFIED modulo a trivial hand lemma" and must say so.
- Frobenius powers σ², σ⁴ and all involution classes of GL(8,2) are
  **not** excluded — the theorem genuinely stops at odd order.
- Prior-work check was one day deep: arXiv fulltext + citation search on
  2512.01760 (nothing on χ₂(8) found as of 2026-09-01). The
  sum-free-partition literature on F₂ⁿ is old and broad; a referee
  should specifically ask whether the order-17/order-5 exclusions
  duplicate anything in the Schur-like/cap-set symmetric-search
  literature. We found none, but mark the search shallow.

## 5. Page-update rule

New page; nothing to diff against. Link it from the top-level README row
(currently the row has no page link) and from this conjecture's README
header once live.
