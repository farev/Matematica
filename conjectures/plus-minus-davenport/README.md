# plus-minus-davenport

**Problem.** Determine the plus–minus weighted Davenport constant `D±(G)`
— the least `ℓ` such that every length-`ℓ` sequence over the finite
abelian group `G` has a nonempty ±-signed zero subsum — for the groups
where it is open; equivalently (Lemma E, `NOTE.md` §1) determine
`ℓ_max(G) = D±(G) − 1`, the maximum size of a *dissociated* subset of
`G`. Program of Marchan–Ordaz–Schmid (Int. J. Number Theory 10 (2014)
1219–1239, (secondary)). Page: <https://fabianarevalo.com/plus-minus-davenport>.

**Status after session 1 (2026-08-21).**

- **CERTIFIED** `D±(C₅⊕C₁₅) = 6` — reportedly the last unresolved group
  of order ≤ 100 ((secondary), see NOTE §2 caveat). Three independent
  exhaustions; the counting bound `⌊log₂ 75⌋ + 1 = 7` is *not* attained.
- **CERTIFIED** `D±(C₇⊕C₂₁) = 8` — the counting bound *is* attained, and
  the extremal 7-set is **unique up to Aut(G)** (2016 = one orbit).
- **CERTIFIED/PROVED** census of all 493 abelian groups of order ≤ 255:
  484 attain `D± = ⌊log₂|G|⌋ + 1`; the 9 exceptions are catalogued
  (NOTE §3). Extras: `C₅⊕C₅₅` deficient (D± = 8), `C₇²⊕C₉` attains
  (D± = 9).
- **PROVED** Lemma E (±-zsf ⟺ dissociated, elementary, not new),
  Theorem T3 (`D±(C₂^r) = D±(C₃^r) = r+1`, not new), Corollary F
  (`D±(C_p⊕C_{3p})` for all `p ≤ 17`; exceptional only at `p = 5`).
- **Open** (NOTE §4): characterize the deficient groups; window primes
  `p ≥ 19`; rigidity in general; hand proof for order 75.

| script | what it does | cost |
|---|---|---|
| `dissoc.py` | Python engine + `controls` (Lemma E validation, formula and negative controls) | seconds |
| `dissoc.c` | C engine, node-count-identical to Python; `need=K`, `order=desc` modes | seconds–minutes |
| `verify_75.c` | independent brute-force refutation for `C₅⊕C₁₅` (`-DG147`: enumeration for `C₇⊕C₂₁`) | 0.13 s / 1.8 min |
| `orbit_147.py` | rigidity: Aut-orbit of the 147-witness = all 2016 maximum sets | 3 s |
| `orbit_75.py` | all 85 155 maximum 5-sets at order 75, 193 orbits, 0 extendable | 13 min |
| `census.py N [start] [out]` | census: pinned cells by constructed witness, `C₃^r` by Theorem T3, the rest by C-engine search | 40 s to N=255 |
| `verify_census.py M` | recompute orders ≤ M in Python, exact node-count equality | 8 s (M=100) |
| `summarize.py *.csv` | the tables quoted in NOTE.md | instant |

```bash
cd conjectures/plus-minus-davenport
gcc -O2 -o dissoc dissoc.c
python3 dissoc.py controls && ./dissoc 5 15 && ./dissoc 7 21
python3 census.py 255 && python3 verify_census.py 100 && python3 summarize.py census.csv
```

Data: `census.csv` (canonical, orders 2–255), `census_256_330.csv`
(extension), `run_*.log` (single-group exhaustions with node counts).
4-core sandbox, single-threaded runs, exact integer arithmetic, no
randomness.

**Known defects / caveats.** All literature citations are (secondary)
— the sandbox cannot reach primary sources; the openness of the two
headline values rests on search snippets (NOTE §2, §6). An earlier
committed census run verified pinned cells by DFS witness search instead
of constructed witnesses (both validate; see git history).
