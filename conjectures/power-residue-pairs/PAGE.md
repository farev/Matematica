# PAGE.md — handoff for the site page `fabianarevalo.com/power-residue-pairs`

New page (no page exists).

## 1. Headline claim

**CERTIFIED:** `Λ(8,2) ≤ [[U]]` — the first explicit upper bound on the limit superior of
the least pair of consecutive eighth-power residues (Erdős #436), against
Brillhart–Lehmer–Lehmer's 1964 lower bound `1,200,744`; so `1,200,744 ≤ Λ(8,2) ≤ [[U]]`.

## 2. Contributions

1. **CERTIFIED.** Exhaustive case tree over the 8th-power characters `R(q) ∈ Z/8` of the
   primes `≤ [[S]]`, `R(2)` even, one child per orbit of `(Z/8)^*`: [[leaves]] leaves, all
   settled by a pair `(n, n+1)` of consecutive smooth 8th-power residues with
   `n ≤ [[U]]`; certificate `cert_k8_P[[S]]_L[[L]].gz` (SHA-256 in `data/`), verified by
   `check_tree2.py` in about two minutes; pairs files audited line by line.
2. **CERTIFIED (controls).** The same programs give `Λ(k,2) = 9, 77, 1224, 7888, 202124,
   1649375` for `k = 2..7` (trees with no unsettled leaf at `L = Λ`) and unsettled leaves
   at `L = Λ − 1` (8, 63, 587 for `k = 3, 5, 7`); OEIS A002071 pair counts reproduced.
3. **CERTIFIED (re-verification).** BLL's Table V vector has least pair exactly
   `1,200,744 = 2³·3⁴·17·109`, `1,200,745 = 5·7²·13²·29` (realisability via Mills 1963, as
   in BLL; secondary).
4. **NUMERICAL (negative).** No better lower-bound vector found: complete search over the
   six impasse primes of BLL's vector, greedy extensions of the 108 gap vectors.

## 3. Figure specs

* **Figure 1 — gaps versus L.** Data: `data/sweepP300_bisect.log`, `data/sweepP300_tight.log`
  and NOTE §5 table (unsettled leaves as a function of `L`, for `S ≤ 113` and `S ≤ 300`).
  Sentence: "As the search bound grows, the number of character vectors with no settling
  pair drops to zero exactly at `[[U]]`."
* **Figure 2 — a leaf.** Data: one line of the certificate (`q=v …| n`) with the pair's
  factorisations. Sentence: "Each leaf is a partial assignment of characters to small primes
  under which two consecutive smooth integers are both eighth powers."
* **Figure 3 — the k ladder.** Data: NOTE §4 table (`k`, `Λ(k,2)`, leaves). Sentence: "The
  case trees for `k = 2..7` reproduce the Lehmers' 1963–64 values and are sharp one
  below each."

## 4. Caveats

* Upper bound unconditional; lower bound conditional on Mills' theorem exactly as in BLL.
* Generator and checker written by one (AI) author; the session's audit re-ran the checker,
  regenerated all controls and verified the pairs files, but no human has read `tree2.c`.
* The exact value is open; the 108 gap vectors at `L = 1.5 M` are the next step.

## 5. Existing page

None.
