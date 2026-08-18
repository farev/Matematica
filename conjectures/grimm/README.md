# Grimm's conjecture (C. A. Grimm, 1969)

If `n+1, n+2, …, n+k` are all composite, there exist **distinct** primes
`p₁, …, p_k` with `pᵢ | n+i`. Published in Amer. Math. Monthly 76 (1969)
1126–1128; Guy, UPINT §B32. Deceptively strong: by Erdős–Selfridge it
implies prime-gap bounds beyond what the Riemann hypothesis gives
((secondary) — no primary source readable from this sandbox, see NOTE §1).

The fault line for a session: the computational record — verified for all
`n ≤ 1.9236701629×10¹⁰` (Laishram–Shorey, Int. J. Number Theory 2 (2006),
(secondary)) — has stood for twenty years, is *not* subsumed by prime-gap
tables (no explicit `k ≤ f(n)` theorem bridges the gap tables' 4×10¹⁸), and
the per-gap structure that makes verification possible (the rare members
with no prime factor exceeding the gap length, and their Hall matchings)
had never been tabulated. One afternoon of sieve engineering reaches 10¹² —
a 52× extension — and yields that census as a by-product.

**Status:** active
**Sessions:** [2026-08-15](../../log/2026-08-15-grimm.md)

## Results

| Claim | Label | Where |
|---|---|---|
| Grimm's conjecture holds for all `n ≤ 10¹²` — every maximal prime gap with left prime `p < 10¹²` carries an explicit system of distinct prime representatives; 52× the 2006 record, 52.1 min of 4-core wall time | CERTIFIED | `data/c*.summary.txt`, censuses (regenerable, sha256 in `data/census_hashes.txt`) |
| The critical-member census: **18,575,022** members (gap members whose prime factors are all ≤ the gap length `k`) in 18,400,995 gaps, each factored, matched, with exact Hall margin; **no margin is negative** (one would be a counterexample) | CERTIFIED | `data/stats_by_decade.csv`, `data/tight.csv`, `data/multi.csv`, `data/extremes.csv`, `data/crit_by_k.csv` |
| **Every tight gap (margin 0) below 10¹² is prime-power tight** — all 133 contain a prime power `pᵃ ≤ k`-smooth achieving the minimum alone; interaction tightness (≥ 2 criticals sharing too few primes — the only way Grimm can actually fail) never occurs in range; largest tight gap: `31⁸` at p = 852,891,037,337 (k = 109) | CERTIFIED | `data/tight.csv`, `analyze_tight.py` output in WRITEUP |
| Reduction lemma: Grimm on every window of a gap ⇔ the gap's criticals admit a matching into primes ≤ k (classical in substance; stated and proved in NOTE §2, no novelty claimed) | PROVED (folklore) | `NOTE.md` §2 |
| Tight gaps occur infinitely often: powers `2ᵃ`, `a ≡ 3 (mod 6)`, force margin ≤ 0 forever (= 0 under Grimm) | PROVED (elementary) | `NOTE.md` §5, Prop. 5.2 |
| π(10⁸), π(10⁹), π(10¹⁰), π(10¹¹), π(10¹²) and six first-occurrence maximal gaps (86, 220, 282, 354, 464, 540) reproduced exactly | CERTIFIED (controls) | `data/c*.summary.txt`, WRITEUP |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `grimm_sweep.c` | 4-thread segmented sieve + cache-blocked smooth-part sieve + per-gap critical detection, Hall matching, exact margins; census + histogram + summary per range. `--selftest` runs matcher/factor unit tests incl. a constructed Hall failure | ~2.8 s per 10⁹ per 4 cores | census.csv, gaphist.csv, summary.txt |
| `verify_census.py` | independent verifier (sympy: isprime/factorint/nextprime; no code shared with the C engine). `--window LO HI CENSUS` = exhaustive re-derivation on a window; `--check CENSUS --sample N` = light pass on all rows + heavy sampled gap re-verification (primality, maximality, completeness) | window: min/10⁵ ints; check: ~s/gap | `errors=0` |
| `mine_stats.py` | streams the chunk censuses into the committed artifacts (per-decade stats, tight/multi subsets, extremes, sha256 manifest) | seconds | `data/*.csv` |
| `run_production.sh` | the production sweep, decade chunks `c2..c4` | ~50 min total | `data/c*.{census,gaphist,summary}` |

Run from inside this directory:

```bash
gcc -O2 -march=native -pthread -o grimm_sweep grimm_sweep.c
./grimm_sweep --selftest
./grimm_sweep 2 300000 1 data/ctl_small
python3 verify_census.py --window 2 299000 data/ctl_small.census.csv   # errors=0
./grimm_sweep 2 1000000000 4 data/c1        # ~9 s
./run_production.sh                          # chunks to 1e12, ~50 min
python3 mine_stats.py c1 c2 c3 c4
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/c{1,2,3,4}.summary.txt` | grimm_sweep | per-chunk verdict, prime counts (π anchors), max gap, extremes, timings |
| `data/c{1,2,3,4}.gaphist.csv` | grimm_sweep | gap-length histogram per chunk (left prime in chunk) |
| `data/stats_by_decade.csv` | mine_stats | criticals, tight gaps, max s, min margin, per decade |
| `data/tight.csv` | mine_stats | every critical row of every Hall-margin-≤ 0 gap below 10¹² |
| `data/multi.csv` | mine_stats | every row of every gap with ≥ 4 criticals |
| `data/extremes.csv` | mine_stats | record gaps (max criticals, last tight gap, max L, max m) |
| `data/census_hashes.txt` | mine_stats | sha256 + row counts of the full chunk censuses |

The full censuses (~10⁷ rows) are **not committed** (repo size rule); they
regenerate byte-identically by the commands above in ~50 minutes on 4 cores,
and their hashes are committed. Everything committed is either small data
mined from them or the summaries the engine wrote directly.

## Known defects and open threads

- All literature statements are **(secondary)** — the sandbox could not read
  any primary source (arxiv/oeis/erdosproblems/MathWorld all egress-blocked;
  WebSearch snippets only). Before publishing anything: read Laishram–Shorey
  2006 (exact record + method), Erdős–Selfridge 1971, Laishram–Murty 2012,
  and check whether any verification beyond 1.9236701629×10¹⁰ exists in a
  thesis or forum unindexed by search.
- The maximal-gap anchor values used as controls (86 after 155921, 220 after
  47326693, 282 after 436273009, 354 after 4302407359) are from memory,
  (secondary); they matched the sweep's output exactly, and π(10⁸), π(10⁹),
  π(10¹⁰) anchors matched published values exactly.
- Completeness of the census rests on the C engine (exhaustively
  cross-checked against sympy on three windows and sampled everywhere);
  the sampled heavy verification covers a few hundred gaps per chunk, not
  all ~10⁷ critical gaps.
- Sharpest open threads: (i) the *uncomputed* function here is the exact
  margin distribution's tail — does the min margin over gaps in [10^d,
  10^{d+1}) grow, i.e., is there a last genuinely-interacting tight gap?
  (ii) push to 10¹³ (~9 h at measured throughput); (iii) the weak Grimm
  function g(n) against the Laishram–Murty n^{0.45} window.

## Prior work

Grimm, AMM 76 (1969) (secondary); Erdős–Selfridge 1971 (Hall's theorem,
`m > n^{π(n)}`) (secondary); Ramachandra–Shorey–Tijdeman, Crelle 1975/76
(`g(n) ≫ (log n / log log n)³`) (secondary); Laishram–Shorey, IJNT 2 (2006)
(record `n ≤ 1.9236701629×10¹⁰`) (secondary); Laishram–Murty, Michigan MJ 61
(2012) (`g(n) = O(n^{0.45})` unconditional, smooth-number framing)
(secondary); Tao–Teräväinen arXiv:2512.01739 and van Doorn–Li–Tang
arXiv:2603.28636 (adjacent Erdős #375 corner, active 2025–26) (secondary).
No prior tabulation of critical members / Hall margins was found by search
(absence-of-evidence, (secondary)).
