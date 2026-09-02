# Consecutive eighth-power residues: Λ(8,2) (Erdős #436; Brillhart–Lehmer–Lehmer, 1964)

For a prime `p` let `r(k,2,p)` be the least `r ≥ 1` such that `r` and `r+1` are both
`k`-th power residues mod `p`, and `Λ(k,2) = limsup_p r(k,2,p)`. Erdős problem #436
asks whether `Λ(k,2)` is finite for all `k` (Hildebrand 1991: yes) and "how large are
they?". Brillhart, Lehmer and Lehmer (Math. Comp. 18, 1964) computed `Λ(k,2)` exactly for
`k = 2, …, 7` (9, 77, 1224, 7888, 202124, 1649375) by a machine-executed case analysis
over the `k`-th power characters of small primes, and for `k = 8` gave only the lower
bound `Λ(8,2) ≥ 1,200,744`: the first case "not covered by the theorem", because for
`p ≡ 1 (mod 8)` the prime 2 is a quadratic residue and its character index must be
even. The fault line: the same case analysis, with `R(2)` restricted to even values, is a
day's computation on modern hardware. It was carried out today by a subagent working to a
written specification and audited independently (pairs-file factorisations, certificate
re-check, regeneration of the `k ≤ 7` controls).

Page: *(none yet — see PAGE.md)*.

**Status:** active
**Sessions:** 2026-09-02

## Results

| Claim | Label | Where |
|---|---|---|
| **`Λ(8,2) ≤ 1,508,324`** — the first explicit upper bound: an exhaustive case tree over the 8th-power characters of the 62 primes `< 300` (with `R(2)` even; one child per orbit of the unit group `(Z/8)^*`) has 3,499,913 leaves, every leaf settled by a pair `(n, n+1)` of consecutive 293-smooth 8th-power residues with `n ≤ 1,508,324`; certificate checked by an independent streaming checker (2 m 0 s); a first certificate with the primes `≤ 113` gives `1,794,897` (3,270,936 leaves, 1 m 52 s) | CERTIFIED (unconditional) | `NOTE.md` §3–5, `data/cert_P300.log`, `data/k8_cert.log` |
| BLL's lower bound `Λ(8,2) ≥ 1,200,744` re-verified: their Table V case vector has least pair exactly `1200744 = 2³·3⁴·17·109`, `1200745 = 5·7²·13²·29` (exact sieve over all `n < 1,200,744`) | CERTIFIED (realisability of the vector via Mills 1963, as invoked by BLL; (secondary)) | `data/tableII_k8.txt`, `verify_witness.py` |
| Controls: the same programs reproduce `Λ(k,2)` for `k = 2..7` exactly (tree at `L = Λ` has no unsettled leaf; at `L = Λ − 1` it has gaps: 8, 63, 12,046 for `k = 3, 5, 7`), BLL Table II vectors re-verified, and the consecutive-smooth-pair counts match OEIS A002071 (869 pairs for the first 13 primes) | CERTIFIED | `data/a002071_check_*.txt`, `NOTE.md` §4 |
| Attempts to raise the lower bound: BLL's vector cannot be repaired by re-choosing the six primes at its impasse (complete search, no solution below 1.3 M); greedy extension of the 108 unsettled vectors at `L = 1.5 M`, `S ≤ 300` stalls at `≤ 1,088,867` | NUMERICAL (negative) | `NOTE.md` §6 |

So `1,200,744 ≤ Λ(8,2) ≤ 1,508,324`; the exact value is not determined.

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md) for the
session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `smoothpairs.py` | all consecutive `S`-smooth pairs `(n, n+1)`, `n ≤ L`, with factorisations | seconds | `data/pairs_P113_L10000000.txt` (12,946 pairs) |
| `exceptional.py` | brute-force check of the exceptional primes (BLL §3) for `k ≤ 8` | seconds | 17, 41, 113 for `k = 8` |
| `tree2.c` | the exhaustive case tree (BLL "dimension window", unit-orbit branching); writes a gzip certificate | 2 s (`k = 7`) to 1 min (`k = 8`) | `Λ(k,2) ≤ max settling pair` |
| `check_tree2.py` | independent streaming checker: exhaustiveness up to the unit stabiliser at every node, every leaf settled under its own assignment, `n ≤ L` | 2 min for `k = 8` | `data/check_k8.log` |
| `audit_pairs.py` | independent check that every pairs-file line factorises correctly (`sympy.isprime`) | seconds | this session's audit |
| `verify_witness.py` | exact sieve: least `n` with `n, n+1` both residues under a full assignment | seconds | lower-bound re-verification |
| `witness.c`, `casetest.c` | complete DFS with backjumping / BLL repair heuristic for lower-bound witnesses | minutes | negative results only |

Run from inside this directory:

```bash
cd conjectures/power-residue-pairs
gcc -O2 -o tree2 tree2.c
python3 smoothpairs.py 113 10000000 data/pairs_P113_L10000000.txt      # or use the committed file
./tree2 8 data/pairs_P300_L10000000.txt 1508324 cert_k8_P300_L1508324.gz --even 2   # ~1 min
python3 check_tree2.py 8 data/pairs_P300_L10000000.txt cert_k8_P300_L1508324.gz       # ~2 min
./tree2 8 data/pairs_P113_L10000000.txt 1800000 cert_k8_P113_L1800000.gz --even 2     # the first certificate
python3 audit_pairs.py data/pairs_P300_L10000000.txt
./tree2 7 data/pairs_P113_L10000000_x491.txt 1649375 cert_k7.gz && python3 check_tree2.py 7 data/pairs_P113_L10000000_x491.txt cert_k7.gz
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/pairs_P113_L10000000.txt`, `..._x491.txt` | `smoothpairs.py` | consecutive 113-smooth pairs to 10⁷ (with 491 for the `k = 7` control); every line audited |
| `cert_k8_P300_L1508324.gz` (20.97 MB) and `cert_k8_P113_L1800000.gz` (19.5 MB), **not committed** — above the repository's size threshold; regenerate in ~1 min each with the commands above | `tree2` | the `k = 8` certificates: 3,499,913 and 3,270,936 leaves; SHA-256 of both in `data/k8_cert_sha256.txt` |
| `data/pairs_P300_L10000000.txt` | `smoothpairs.py` | consecutive 293-smooth pairs to 10⁷ (78,834), every line audited |
| `data/sweepP300_*.log`, `data/cert_P300.log`, `data/audit.log` | this session | the `L`-sweep with `S < 300`, the certificate run and check, the audit |
| `data/k8_cert.log`, `data/check_k8.log` | `tree2`, `check_tree2.py` | run and check logs (`L = 10⁷` variant: 2,528,327 leaves, `U = 9,927,575`) |
| `data/tableII_k8.txt` | `verify_witness.py` | BLL Table V vector and its least pair |
| `data/gaps_k8_P300_L1500000.txt` | `tree2 --dry` | the 108 unsettled case vectors at `L = 1.5 M`, `S ≤ 300` — the sharpest open thread |

## Known defects and open threads

- Two implementations (generator and checker) by the same author (a subagent); the audit
  today re-ran the checker, verified the pairs file independently and regenerated the
  `k = 2..7` controls, but no human has read `tree2.c`.
- The lower bound's realisability rests on Mills' theorem (Canad. J. Math. 15, 1963) as
  invoked by BLL; the subagent read Mills' paper, this session did not (text layer
  unusable) — marked (secondary).
- The bound `1,508,324` is what the primes `< 300` give; the 108 case vectors unsettled
  at `L = 1,508,323` are all settled by the single pair `(1508324, 1508325)`. Deciding those
  108 vectors with a larger prime set (a complete extension search, or a tree with
  `S ≤ 1000` on each) would either lower the certified bound further or, via a realisable
  full assignment, raise the lower bound past `1.2 M`. The exact value is the open question.

## Prior work

- J. Brillhart, D. H. Lehmer, E. Lehmer, *Bounds for pairs of consecutive seventh and
  higher power residues*, Math. Comp. 18 (1964) 397–407 — read (PDF text); Tables I, II, V; §8.
- D. H. Lehmer, E. Lehmer, W. H. Mills, *Pairs of consecutive power residues*, Canad. J.
  Math. 15 (1963) 172–177; W. H. Mills, *Characters with preassigned values*, ibid. 169–171
  (secondary: read by the subagent only).
- J. Rabung, J. Jordan, Math. Comp. 24 (1970) 737–740 — the different quantity `Λ*(8,2) = 399`.
- A. Hildebrand, *On consecutive k-th power residues II*, Michigan Math. J. 38 (1991) — finiteness (secondary).
- erdosproblems.com/436 (fetched 2026-09-02): OPEN, no mention of an upper bound for `k = 8`.
