# Plus–minus weighted Davenport constants (Marchan–Ordaz–Schmid, 2014)

For a finite abelian group G, D±(G) is the least ℓ such that every sequence
of ℓ elements of G has a nonempty subsequence with a ±1-weighted zero sum.
Marchan, Ordaz and Schmid (IJNT 2014, (secondary)) determined D± for every
abelian group of order ≤ 100 **except one**: C₅⊕C₁₅, left as "6 or 7". The
fault line: the deciding search is finite and small, so a session with clean
certification machinery can close the table's last cell below 100 and then
push past 100, where (as far as snippets showed) no values are published.

**Status:** active
**Sessions:** 2026-08-24

## Results

| Claim | Label | Where |
|---|---|---|
| D±(C₅⊕C₁₅) = 6 — the open cell closes at the concatenation bound; four independent implementations, A/C node counts match at 139 052; strata (4,2), (3,3) of the nonexistence proof done by hand | CERTIFIED (lower bound PROVED) | NOTE §4, §6 |
| Full independent table of d± for all 184 abelian group types, order ≤ 100; 17 bracket-open cells decided, 12 attain the pigeonhole bound, 5 the concatenation bound | CERTIFIED (167 forced cells PROVED) | NOTE §5, `data/table_le100.csv` |
| Beyond order 100 (possibly first published values, (secondary)): all types of order 101–135 + targeted cells to 243; D±(C₇⊕C₂₁) = 8, D±(C₅⊕C₃₀) = 8, D±(C₃⊕C₅₁) = 8, …; first cell strictly inside both bounds: d±(C₃⊕C₃⊕C₁₅) = 6 ∈ (5,7) | CERTIFIED | NOTE §7, `data/table_101_135.csv`, `data/beyond.csv` |
| Elementary bound/reduction lemmas (pigeonhole, cyclic, concatenation/quotient, saturation, exponent-3 = 𝔽₃-rank) | PROVED | NOTE §2–§3 |
| Extremal census for C₅⊕C₁₅: 85 155 maximum ±-zsf 5-sets, stratified 3 375/13 500/29 040/27 960/11 280; the 3 375 = 135×25 explained exactly | CERTIFIED | NOTE §4.2 |
| Conjecture A (split-or-pigeonhole; holds at every computed group) and Conjecture C (C₇⊕C₇ₙ tight, n ≤ 5 verified) | conjectures, machine-tested only | NOTE §8 |
| Interim Conjecture B (C₃⊕C₃ₙ always tight) **refuted by this session's own sweep**: d±(C₃⊕C₄₅) = 6 < 7 at n = 15 | CERTIFIED refutation | NOTE §8 |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `dpm_core.py` | canonical engine (impl A): DFS over sign-class subsets, exact reachable sets | seconds/group | `python3 dpm_core.py 5 15` |
| `bruteforce_check.py` | impl B: full C(nc,L)×patterns integer sweep, shares no method with A | ~95 s for the headline | 0 ±-zsf 6-sets; 85 155 5-sets |
| `dpm_fast.c` | impl C: bitset DFS in C, same tree as A (node counts must match); `-s i/k` shards | `gcc -O2`; ms–minutes | all beyond-100 cells |
| `verify_strata.py` | impl D: stratified verification of Theorem 1 by |S∩H| | 21 s | all five strata empty |
| `verify_witness.py` | standalone pure-int certificate checker | instant | validates any witness JSON |
| `controls.py` | positive/negative control suite (must pass before trusting anything) | 6 s | 0 failures |
| `run_table.py` | order-range sweep driver (4 workers), CSV + JSON certs | ~12 core-min for ≤ 100 | `data/table_le100.csv` |

Run from inside this directory, e.g.:

```bash
cd conjectures/plusminus-davenport
python3 controls.py && python3 dpm_core.py 5 15
gcc -O2 -o dpm_fast dpm_fast.c && ./dpm_fast 5 15   # expect nodes=139052
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/cert_C5xC15.json` | `dpm_core.py` | headline certificate: witness, node count, full 85 155-set census |
| `data/table_le100.csv` + `_certs.json` | `run_table.py 2 100` | the complete ≤ 100 table with per-group status/witness/nodes |
| `data/table_101_135.csv` + `_certs.json` | `run_table.py 101 135` | complete 101–135 table |
| `data/beyond.csv` | `dpm_fast` runs | targeted cells 136–243 with node counts |
| `data/sweep_101_135.log` | sweep | raw run log |

## Known defects and open threads

- The three strata (2,4), (1,5), (0,6) of Theorem 1 are machine-certified,
  not hand-proved; the theorem's label is CERTIFIED until they are.
- Every literature statement is (secondary) — the sandbox could not reach any
  primary source. In particular *whether the headline cell was still open* is
  as strong as the 2026-08-24 snippet trail (MOS 2014 + 2017 survey + active
  2024–2026 papers, none claiming it); the Perez-Lavin thesis (2021) is the
  main unread risk. NOTE §9 lists everything to re-check.
- The C₂-heavy forced cells ≥ order 96 have node-capped confirmations (values
  PROVED by bounds, recorded in CSV as such).
- Sharpest open thread: Conjecture A for rank 2; and whether C₅⊕C₅ₙ is ever
  pigeonhole-tight at odd n ≥ 3.

## Prior work

Marchan–Ordaz–Schmid (IJNT 2014; arXiv:1308.3316) — the table this session
completes and extends; D±(C_n) = ⌊log₂ n⌋+1 (Adhikari et al.); the 2017
survey chapter on plus-minus weighted zero-sum constants; active
2024–2026 arithmetic line (Merito–Ordaz–Schmid and others). All (secondary),
reconstructed from search snippets on 2026-08-24; see NOTE §1/§9.
