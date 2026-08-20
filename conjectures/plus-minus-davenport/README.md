# Plus-minus weighted Davenport constants (Marchan–Ordaz–Schmid, 2014)

For a finite abelian group G, `D±(G)` is the least ℓ such that every
sequence of ℓ elements of G has a nonempty subsequence summing to zero with
signs ±1. Equivalently (two-line lemma) `D±(G) = dis(G) + 1`, where `dis(G)`
is the largest size of a *dissociated* subset — all 2^k subset sums
distinct. Marchan–Ordaz–Schmid (IJNT 2014, (secondary)) determined D± for
every abelian group of order ≤ 100 **except C₅⊕C₁₅** (boxed {6, 7}), and
left both rank-two families C₅⊕C₅ₙ, C₇⊕C₇ₙ open from n = 3 and C₃⊕C₃ₙ open
first at n = 15. The fault line: each value is a bounded exact search.

**Status:** active
**Sessions:** 2026-08-20
**Page:** *(pending local publish)*

## Results

| Claim | Label | Where |
|---|---|---|
| D±(C₅⊕C₁₅) = 6 — the last open group of order ≤ 100; five smallest-open cases decided in all | CERTIFIED | NOTE §5.1, `data/c5c15_certificate.txt` |
| D±(C₇⊕C₂₁) = 8, exactly 2016 maximum 7-sets | CERTIFIED | NOTE §5.2, `data/c7c21_certificate.txt` |
| D±(C₃⊕C₄₅) = 7 — first open case (n=15) of the C₃⊕C₃ₙ family, a deficit | CERTIFIED | NOTE §5.3, `data/c3c45_certificate.txt` |
| D±(C₅⊕C₅₅) = 8 — n=11 of the C₅⊕C₅ₙ family, a second family deficit (3.49B-node sharded exhaustion) | CERTIFIED | NOTE §5.4, `data/c5c55_shard*.txt` |
| D±(C₃⊕C₈₇) = 8 — n=29 failing-block case; deficit, and the case separating Conjecture D′ from its Sylow variant (2.03B-node exhaustion) | CERTIFIED | NOTE §6, `data/c3_n29.txt` |
| C₃⊕C₃ₙ determined for **every n ≤ 56** (T1 + machine at the failing blocks); deficits exactly at n = 1, 15, 29 | CERTIFIED + PROVED | NOTE §6 |
| Census: all 184 abelian groups of order ≤ 100; exactly 5 miss ⌊log₂\|G\|⌋+1 | CERTIFIED | NOTE §7, `data/census.csv` |
| Attainment for C₃⊕C₃ₙ whenever 2^{⌊log₂9n⌋−3} ≤ n (rediscovers MOS regime) | PROVED | NOTE §6 (Theorem T1) |
| Equivalence, bounds, normalization, fiber obstruction (L1–L6, F, F5, F45) | PROVED | NOTE §2–§3 |
| Dichotomy D′: dis(G) = ⌊log₂\|G\|⌋ or the MOS bound L(G) = Σ⌊log₂ dᵢ⌋ — never both strict; 184/184 groups + all values beyond | NUMERICAL (conjecture) | NOTE §7 |
| Family tables C₃⊕C₃ₙ, C₅⊕C₅ₙ, C₇⊕C₇ₙ (ranges in NOTE §6) | CERTIFIED | `data/families.csv` |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `dis_search.c` | primary engine: signed-sum DFS over ± representatives; modes max / all / decide; `-r` root sharding | ms–hours by group | every dis value |
| `verify_defn.c` | independent definitional engine (subset-sum distinctness, no reductions) | ~25× primary | second exhaustions |
| `dis_reference.py` | clean-room Python DFS + definitional witness checker | slow | third confirmations |
| `census.py` | all abelian groups of order ≤ N → `data/census.csv` | 226 s at N=100 | the ≤ 100 table |
| `make_tables.py` | parses run logs, **re-verifies every witness from the definition**, audits bounds | seconds | `data/families.csv` |
| `check_dichotomy.py` | verifies Conjecture D′ on every computed group value | seconds | "violations: 0" |

Run from inside this directory:

```bash
gcc -O2 -march=native -o dis_search dis_search.c
gcc -O2 -march=native -o verify_defn verify_defn.c
./dis_search max 5 15          # D±(C5⊕C15)=6 in <0.2 s
./verify_defn 5 15 6           # independent: no dissociated 6-set
python3 census.py 100 > data/census.csv
python3 make_tables.py         # audit everything
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/c5c15_certificate.txt` | three engines | the headline value, both bounds, cross-check identity 85155·2⁵ = 2724960 |
| `data/c7c21_certificate.txt` | dis_search + checker | witness + maximum-set count 2016 |
| `data/c3c45_certificate.txt` | both C engines | 8.2M-node + 361.7M-node exhaustions |
| `data/census.csv` | census.py | 184 groups ≤ 100: dis, D±, attainment |
| `data/controls.txt` | dis_search | 25 literature controls, `control_failures=0` |
| `data/family_le200.txt`, `data/gap_probes.txt`, `data/c3_n29.txt` … | dis_search | family sweeps and gap-case decisions |
| `data/families.csv` | make_tables.py | audited union of all group values |

## Known defects and open threads

- Every literature citation is **(secondary)** (sandbox egress blocked;
  snippets only). The **Perez-Lavin 2021 U. Kentucky thesis** covers orders
  that are products of two prime powers and *must be read* before any
  novelty claim about C₅⊕C₁₅ leaves this repository. Same for the Adhikari
  2017 survey chapter. NOTE §9.
- The three headline upper bounds are exhaustive searches (CERTIFIED), not
  proofs; the hand-proof of dis(C₅⊕C₁₅) ≤ 5 is open (NOTE §8), and Lemma F
  shows any proof must beat a one-element slack.
- Sharpest open questions: Conjecture D′ (dichotomy); the C₅⊕C₅ₙ deficit
  pattern (n = 3, 11 deficit; 6, 12 attain — does deficit = odd n hold? the
  n = 21 probe tests it); C₃⊕C₃ₙ at n = 57…63; dis(C₂₃²) ∈ {8, 9}.

## Prior work

Marchan–Ordaz–Schmid, IJNT 10 (2014) 1219–1239 (arXiv:1308.3316) — the
source of the problem and of every "known" value used as a control; all
(secondary). Adhikari et al. 2006/2009 for the cyclic case ((secondary)).
E± corollaries via Grynkiewicz–Marchan–Ordaz, Ramanujan J. 28 (2012),
(secondary). Theorem T1's regime matches the quoted MOS Theorem 4.4
condition and is marked a presumptive rediscovery. Dissociated-set
vocabulary: Rudin; no rank-two exact values found under it (57-query
snippet sweep, 2026-08-20).
