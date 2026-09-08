# Dissociated subsets (Erdős Problem #963, 1965)

A set of reals is *dissociated* if all its subset sums are distinct. Erdős asked for
`f(n)`, the largest `k` such that every `n`-element set of reals contains a
dissociated `k`-subset, noted the greedy bound `f(n) ≥ ⌊log₃ n⌋`, and asked whether
`f(n) ≥ ⌊log₂ n⌋`. Asymptotically `f(n) ≥ (1−o(1)) log₂ n` is known from an argument
on the problem page (KoishiChan, Dec 2025), but the inequality itself and every exact
value were open, and the page's own searches were confined to sets of positive integers
in short windows. The fault line: sign flips and zero never help a dissociated subset,
so `f(n) = g(⌈(n−1)/2⌉)` with `g` the same minimum over distinct positive reals, and
for each `k` the question has a single first instance, "do `2^{k−1}` distinct positive
reals always contain a dissociated `k`-subset?" — a finite exact case analysis over the
hyperplane arrangement of ±1 relations.

Page: *(none yet — `PAGE.md` is the handoff)*.

**Status:** active
**Sessions:** 2026-09-08

## Results

| Claim | Label | Where |
|---|---|---|
| `f(n) = g(⌈(n−1)/2⌉)` for all `n`; Erdős's inequality ⇔ every `2^{k−1}` distinct positive reals contain a dissociated `k`-subset | PROVED | NOTE §2 |
| Every 7 distinct positive reals contain a dissociated 4-subset; six need not (`{1,…,6}`, `{1,2,3,5,7,8}`, …); every 4 contain a dissociated triple | CERTIFIED (four engines; JSON case trees checked by an independent checker) | NOTE §4, `certs/`, `data/checker_log.txt` |
| `f(n)` exactly for `n ≤ 27` (`0,1,1,2,2,2,2,3,3,3,3,3,3,4,…,4`); `f(n) ≥ ⌊log₂ n⌋` for all `n ≤ 31`, strict at `n = 14, 15` | PROVED (given the certified theorem) | NOTE Cor. 4.2 |
| Every element of a set with no dissociated `k`-subset is a signed sum of any dissociated `(k−1)`-subset; the 6 / 26 relation patterns of a sorted 4- / 5-subset | PROVED / CERTIFIED | NOTE §3 |
| Sets with no dissociated 5-subset of every size `m ≤ 13` (e.g. `{1,2,3,5,6,7,8,9,10,12,13,15}`); `m = 8` with a checked certificate | CERTIFIED | `data/witnesses.txt`, `certs/D_k5_m8.json` |
| `A₂₄ = {1,…,21,24,25,27}` has no dissociated 6-subset (`g(24) ≤ 5`, `m₆ ≥ 25`; the interval bound was 24) | CERTIFIED (two independent exact programs) | NOTE §6, `code/sa/` |
| The `k = 5` threshold: `14 ≤ m₅ ≤ 41` (lower bound: BAKKAOUI's 13-set; upper: greedy); the exhaustive decision was **not** reached — engine G's enumeration has 1.07 M phase-1 configurations (census in `data/G_runs/`), the four 2-hour runs covered ≈ 2 % of it (best found: 12), ≈ 30 h per order would be needed in Python | open (NUMERICAL evidence only that `m₅ = 14`) | NOTE §5, `data/G_runs/` |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

All engines decide, for given `k` and `m`, whether a set of `m` distinct positive reals
with no dissociated `k`-subset exists, by exact case analysis (integer/rational
arithmetic; floating LPs are used only to *find* certificates that are then verified
exactly). Arguments: `k m [max_solutions] [certificate.json] [...]`.

| file | what it does | cost | headline output |
|---|---|---|---|
| `code/dissoc_search.py` (engine A) | fail-first branching, Fourier–Motzkin leaves with multiplier tracking; writes JSON certificates | `4 7`: 0.9 s, 290 nodes | `g(7) ≥ 4` |
| `code/dissoc_engineB.py` (engine B) | independent implementation: row-echelon state, prefix-first branching, certified LP pruning at every node, exact simplex fallback | `4 7`: 2 s, 1099 nodes | `g(7) ≥ 4`, `g(8) ≥ 4` |
| `code/dissoc_engineC.py` (engine C) | engine A's branching + engine B's pruning, vectorised, subspace memoisation; certificates | `4 7`: 0.6 s, 111 nodes; `5 11`: 92 s | `g(7) ≥ 4`; witnesses for `k = 5` |
| `code/dissoc_engineD.py` (engine D) | the dissociation case split (a 4-subset is dissociated or carries a relation; if dissociated, the rest are signed sums); certificates | `4 7`: 0.6 s, 62 nodes; `5 12`: 128 s | `g(7) ≥ 4`; `m = 12` witness |
| `code/dissoc_engineE.py` (engine E) | enumeration in the 4-parameter family of a dissociated 4-set (sign vectors + ≤ 3 integer cuts, then integer arithmetic) | `4`: seconds (exhaustive); `5`: unfinished | `m₄ = 7`; `k = 5` records |
| `code/dissoc_engineF.py` (engine F) | engine E with the seven-smallest normalisation (three small vectors first, then only vectors above the maximum of the seven) | `4`: 12 s (exhaustive); `5`: unfinished | `m₄ = 7` |
| `code/dissoc_engineG.py` (engine G) | engine F with exact extreme-ray arithmetic instead of LPs (validated: identical `k = 4` enumeration counts, 3 968 random decisions vs LP) | `4`: 0.4 s (exhaustive); `5`: see the status row | `m₄ = 7`; `k = 5` status |
| `code/checker.py` | independent verifier of the JSON case trees (recomputes the relation patterns, checks every branching, pruning and leaf certificate, brute-forces every witness) | seconds per certificate | `data/checker_log.txt` |
| `code/sa/sa.c`, `dval.c`, `bruteforce_d.py` | simulated annealing over `m`-subsets of `{1..W}` minimising the number of dissociated `k`-subsets; two independent exact evaluators of `d(A)` | 8 s for `A₂₄` | `A₂₄` |

Run from inside this directory:

```bash
cd conjectures/dissociated-subsets/code
python3 dissoc_search.py 4 7 1 ../certs/A_k4_m7.json      # engine A, certificate
python3 checker.py ../certs/A_k4_m7.json                    # independent check
python3 dissoc_engineD.py 5 12 1 -                          # a 12-set with no dissociated 5-subset
python3 dissoc_engineE.py 4 -                               # exhaustive k = 4: m_4 = 7
gcc -O2 -o sa sa/sa.c && ./sa 24 6 40 1 8 3000 3 0.05 0 2   # rediscover A_24
```

Requires Python 3.11+, numpy, scipy, sympy (exact simplex fallback), gcc.

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `certs/A_k4_m7.json`, `C_k4_m7.json`, `D_k4_m7.json` | engines A, C, D | complete case trees proving `g(7) ≥ 4` (290 / 111 / 62 nodes), checker-verified |
| `certs/C_k4_m8.json` | engine C | the same at `m = 8` (138 nodes) |
| `certs/A_k3_m4.json` | engine A | `g(4) ≥ 3` (2 nodes) |
| `certs/A_k4_m6.json`, `D_k4_m6.json`, `D_k5_m8.json` | engines A, D | counterexample certificates (families with witnesses) |
| `data/checker_log.txt` | `checker.py` | verification output for every certificate above |
| `data/witnesses.txt` | session | all witness sets, each re-verified by brute force |
| `code/sa/RESULTS.md` | annealing hedge | the `A₂₄` record and its two verifications |

## Known defects and open threads

- The `k = 4` theorem is CERTIFIED, not PROVED: no human-readable proof was written
  (engine D's 62-node tree is the skeleton of one).
- **`m₅` undecided.** Engine G (seven-smallest normalisation, exact extreme-ray
  arithmetic, ≈ 40 phase-2 nodes/s) is the fastest exact enumerator here, but its
  `k = 5` enumeration has 1 103 785 phase-1 nodes (1 069 068 small-triple
  configurations, 644 760 of them numeric points) and about four phase-2 nodes per
  phase-1 node: ≈ 30 h per candidate order in Python. Four runs (two orders, two
  shuffles; 2 h caps) covered ≈ 2 % each and found nothing beyond 12; engine D's
  certified tree needs 27 minutes for the first 13-set. Neither an `m = 14` family nor
  an exhaustive "none" was obtained. Next step: a C port of engine G (small-integer
  arithmetic only), or four days of the Python engine split over the first small index.
- Engines E, F and G have no independent checker and no certificate format (their
  soundness rests on the code, on identical `k = 4` enumerations across E/F/G and
  agreement with the certified engines A–D at `k = 4`, on 3 968 random region decisions
  checked against the LP, and on the completeness control that finds the published
  13-set in 5 nodes when its vectors lead); a `k = 5` verdict from them alone would be
  single-engine.
- `F(7..9)` (Lemma 3.2) are cited from OEIS A276661 without re-computation; only
  `F(1..6)` and `d({1..24})` were recomputed here.
- The original sources [Er65] and [Va99, 1.22] were not consulted (secondary, via the
  problem page). The problem page's history (status OPEN as of 23 Jan 2026, with Bloom's
  comment that the asymptotic argument "looks good") should be re-read before citing.
- The annealing hedge's `d ≤ 4` and `d ≤ 5` non-findings are heuristic (NUMERICAL).

## Prior work

- Erdős Problem #963 (erdosproblems.com/963, read 2026-09-08): statement, greedy bound
  `⌊log₃ n⌋`, KoishiChan's `(1−o(1)) log₂ n` argument (Dec 2025) with Tao's and Tang's
  remarks, Bloom's inclination to mark it solved (23 Jan 2026), BAKKAOUI's integer-window
  searches (3 Sep 2026): `A* = {1,…,10,12,13,15}` has `d = 4`, so `{1,…,n}` is not
  extremal; no 13-subset of `{1,…,34}` has `d ≤ 3`; no OEIS entry. Nobody in the thread
  states the reduction to positive sets, which turns their `f(13) ≤ 4` into `f(13) = 3`.
- Distinct-subset-sum sets (Conway–Guy, Lunnon, Bohman; OEIS A276661, A005318) supply the
  interval upper bounds; this repository's `distinct-subset-sums` directory has `F(10) > 262`.
- Dissociated sets in harmonic analysis (Rudin) use the same definition; no small-case
  tables were found (arXiv/OEIS/Scholar via the page's own literature check by StijnC,
  Oct 2025).
