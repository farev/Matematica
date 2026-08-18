# Graham's 105 problem (Erdős–Graham–Ruzsa–Straus 1975, erdosproblems #376)

Are there infinitely many n with gcd(C(2n,n), 105) = 1? Graham offers $1000;
by Kummer this asks for n with base-3 digits ≤ 1, base-5 digits ≤ 2 and
base-7 digits ≤ 3 simultaneously (OEIS A030979). Provably not settleable by
finite computation — what a session can move is the evidence layer: the
complete-census frontier (10^70 since Nov 2015), the companion claim that
n = 3160 is the last term additionally coprime to 11, and the count data
behind the N^0.02595 heuristic.

**Status:** active
**Sessions:** [2026-08-14](../../log/2026-08-14-graham-105.md)
**Write-up page:** [fabianarevalo.com/graham-105](https://fabianarevalo.com/graham-105)

## Results

| Claim | Label | Where |
|---|---|---|
| Complete census of A030979 below 3^600 ≈ 1.87·10^286: **585,823,270 terms** (published frontier: 1374 terms below 10^70 — a 216-order extension) | CERTIFIED | NOTE §3 C1, `data/` |
| n = 3160 is the last n < 3^600 with C(2n,n) coprime to 1155 (Graham's finiteness prediction, verified 216 orders beyond the published census) | CERTIFIED | NOTE §3 C2 |
| G grows in bursts: only 82 of 601 base-3 lengths inhabited; **no term at all in [3^474, 3^530)** — a 26.7-decimal-order desert — then 39M terms at length 531; 82.6% of all terms have length ≥ 564 | CERTIFIED | NOTE §5, `data/structure600.txt` |
| Count table G(3^k), k ≤ 600 — first counts beyond 10^70; global fit N^0.0248 vs heuristic N^0.02595, local band exponents swinging 0.0144–0.0408 | CERTIFIED (counts) / NUMERICAL (fit) | NOTE §3 C3, C5, `data/counts600.txt` |
| Thompson's 2015 frontier re-derived from scratch (1374 terms ≤ 10^70); Alekseyev's 2008 range re-verified by an unrelated second algorithm (complete below 3.66·10^19) | CERTIFIED (replication) | NOTE §3 C4 |
| Largest known term of A030979: a 286-digit number (was 66 digits) | CERTIFIED | `data/max600.txt` |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `brute.py` | zero-cleverness scan to 2·10^7 with literal `math.comb` gcd checks | ~30 s | 13 terms, definition-level control |
| `ref.py` | bottom-up Python DFS over sums of distinct powers of 3 | seconds–minutes | leaf-count identity vs digit-DP closed form |
| `engine.c` | bottom-up C Gray-code grid, 32768 resume-safe ascending tasks to (3^45−1)/2 | ~2.3 s/task | independent verification below 3.66·10^19 (`data/grid45_w*.csv`) |
| `topdown.py` | top-down interval-pruned reference (Lemma 2) | 0.7 s to 10^70 | fingerprints, node-identical to C |
| `engine_td.c` | production top-down engine: digit-array state, O(1) prune, full/taskgen/tasks/max/tables modes | 18 s at 3^300; 10.7 core-h at 3^600 | the census ladder (`data/prod*`) |
| `validate_terms.py` | independent digit + Lucas + literal-comb validation of any term file | ~1 ms/term | 0 failures across every emitted file |
| `analyze.py` | counts table, band exponents, heuristic fit, 1155 expectation | seconds | `data/counts600.txt`, NOTE §5 |
| `campaign.py`, `status.py`, `validate_hits.py` | Gray-campaign driver / frontier report / hit validator | — | `data/gray_final_status.txt` |

```bash
cd conjectures/graham-105
gcc -O3 -march=native -o engine_td engine_td.c
./engine_td full 148 100000 0        # reproduces Thompson's 1374 terms, <1 s
python3 topdown.py 148               # same, independently; diff the outputs
./engine_td taskgen 600 130 > data/tasks600_130.txt   # 3754 tasks; task 0 = [0, 3^470)
./engine_td taskgen 470 130 > data/tasks470_130.txt   # task 0 re-split into 4906 subtasks
# L=600 split: classes 1..3 start at tasks 1..3; class 0 starts at task 4
# (task 0 is excluded — it runs as the L=470 sub-campaign below)
for w in 1 2 3; do ./engine_td tasks 600 130 data/tasks600_130.txt $w 4 999999 \
  2000 100000 data/prod600_w$w.csv data/prod600_terms_w$w.txt & done
./engine_td tasks 600 130 data/tasks600_130.txt 4 4 999999 2000 100000 \
  data/prod600_w0.csv data/prod600_terms_w0.txt &
for s in 0 1 2 3; do ./engine_td tasks 470 130 data/tasks470_130.txt $s 4 999999 \
  2000 100000 data/prod470_s$s.csv data/prod470_terms_s$s.txt & done; wait
python3 merge600.py
python3 validate_terms.py data/prod600_terms_w*.txt data/prod470_terms_s*.txt --sample 500
python3 analyze.py 600 data/prod600_hist_w*.log --terms data/terms_3e250_full.txt
```

## Data and certificates

| file | what it is |
|---|---|
| `data/terms_3e200_full.txt` | complete term list below 3^200 (10,215 lines, b-file-style) |
| `data/terms_3e250_full.txt.gz` | complete term list below 3^250 (95,861 terms) |
| `data/prod{400,500}_terms.txt`, `data/prod600_terms_w*.txt` | heads (first 2000), samples (every 100,000th), all 1155-flagged terms |
| `data/prod{400,500}.log`, `data/prod600_*` | fingerprints, per-length histograms, per-task CSVs |
| `data/counts600.txt` | G(3^k) for k ≤ 600 + band exponents + fit |
| `data/structure600.txt` | burst/desert structure: 82 inhabited lengths, top spikes, longest term-free runs |
| `data/census600_summary.txt` | composite-campaign merge audit (task coverage, node identity, fingerprints) |
| `data/max600.txt` | the largest term below 3^600 |
| `data/grid45_w*.csv`, `data/gray_final_status.txt` | bottom-up engine's exhaustive tasks and certified bound |
| `cert/` | validation transcripts: T35 cross-checks, 1e12 anchors, fingerprint logs |

## Known defects and caveats

- **Every literature claim is (secondary)** — the sandbox could not read
  oeis.org, arxiv.org, erdosproblems.com or Pomerance's PDFs. The b-file
  extent ("complete up to 10^70", 1374 terms, Thompson Nov 2015) is quoted
  consistently across five independent snippets and matched exactly by our
  count, but check the live entry before citing externally. An unconfirmed
  "10^104" search bound for the 1155 companion could not be sourced.
- Full term lists are committed only to 3^250; larger rungs commit
  heads/samples/extremes/histograms/fingerprints (repo ~10 MB data cap).
  Every rung is reproducible by one command.
- The base-11 flag is computed for every term, but no dedicated OEIS
  sequence for the 1155 case exists to cross-check against (only Graham's
  comment and A129489's a(4) = 3160, verified).
