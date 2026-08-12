# Common prime factors of binomial coefficients (Erdős–Szekeres 1978, Erdős problem #699)

For $1 \le i < j \le \lfloor n/2\rfloor$, is there always a prime $p \ge i$
dividing both $\binom{n}{i}$ and $\binom{n}{j}$? Erdős–Szekeres conjectured
yes, and that $p > i$ works outside a finite exceptional set. The fault
line: the exceptional ("tight") triples are governed by exact digit
conditions (Kummer) at structured $n$, so a deep certified sweep, family
censuses far beyond it, and a calibrated density model are one afternoon of
the right algorithm. Status of #699 verified open 2026-08-12 from
`teorth/erdosproblems` (`falsifiable`) and the Lean formalization (both
`research open`).

**Status:** active
**Sessions:** 2026-08-12

## Results

| Claim | Label | Where |
|---|---|---|
| **Two new tight triples**: $(2^{41},\,2,\,285920731515)$ and $(2^{67},\,2,\,23206563898901803639)$ — the first new ones since Jan 2026, the largest known ($n \approx 1.5\cdot10^{20}$), each with unique $j$ (dual-codebase scans), each verified by a standalone checker; **$2^{67}$ was predicted by the density model before it was found** | CERTIFIED | NOTE §4 R3, `certs/` |
| #699 holds for $4 \le n \le 1{,}371{,}537{,}407$ — a **137× extension** of the recorded bound (contiguous certified prefix of the deep sweep), independently confirming the Jan 2026 scan at $10^7$ on the way (30 s vs ~120 core-h) | CERTIFIED | NOTE §4 R1 |
| Family censuses: $2^k$ complete at all danger levels for $k \le 63$ (17 levels closed by compiled enumerator, up to $4.4\cdot10^9$ candidates each); $i=2$ at semiprime exponents decided through $k = 109$ except $k=101$; $3^m{+}1$ complete at $i \ge 2$ for $m \le 40$, plus $m = 41, 43$ — members are exactly $k \in \{4,9,11,41,67\}$, $m \in \{2,3,5,7,13\}$ | CERTIFIED | NOTE §4 R2/R4 |
| Mersenne exclusion: $2^k{-}1$ prime ⇒ no tight triple at $(2^k, 2)$; exact criterion for any $k$; the five members all have $2^k{-}1$ semiprime (A085724) | PROVED + observed | NOTE Thm 7 |
| $i=3$ family mechanism: $m=2$ or ($m$ odd, $(3^m{+}1)/4$ prime, $(3^m{-}1)/2$ a prime power) ⇒ $(3^m{+}1, 3, n/2)$ tight — explains all five known members | PROVED | NOTE Thm 8 |
| Reduction machinery: gcd>1 theorem, window criterion, danger zone $i \le n - \mathrm{prevprime}(n)$, exact tightness criterion | PROVED | NOTE Props 0–6 |
| Calibrated density model: $E_k = \Theta(1)$ exactly at the five members and the near-miss semiprimes, collapsing elsewhere; along balanced semiprimes it does not decay, and $\sum E_k$ diverges — the $i=2$ family is heuristically **infinite** (disfavoring the formalized finite-exceptional-set strengthening); $i=3$ heuristically finite ($\sum 1/m^2$) | NUMERICAL | NOTE §4 R5, `data/density_2k.csv` |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `sweep699.c` | full certified sweep $n \le N$ (danger-zone + CRT algorithm; `IMIN=1` turns the Prop-0 control on) | $10^7$: 15 s (4 cores) | `census699.csv` |
| `brute699.py` | independent reference sweep (full prime matrix) | $n \le 3000$: 60 s | `brute699_out.csv` |
| `family699.py` | exact criterion at $n = 2^k$, $3^m{+}1$ (sympy factoring + dominated-set enumeration, cap $10^8$) | $k \le 64$, $m \le 40$: ~25 min | `family_census.csv` |
| `domclose.c` | compiled dominated-set enumerator for levels past the Python cap (u128; JOBFAIL canary) | $10^9$ candidates ≈ minutes | `data/domclose_*.txt` |
| `domclose_driver.py` | regenerates domclose job lines (complete factorizations) from the UNKNOWN-level CSV | seconds | `jobs*.txt` |
| `measure_density.py` | exact dominated-set counts by digit DP → per-$k$ expected tight-$j$ count $E_k$ | seconds | `data/density_2k.csv` |
| `verify_triple.py` | standalone verifier for claimed tight triples + uniqueness scan | ~2 min | `certs/verify_2_41.txt` |
| `audit699.py` | deep-sample audit: random $n$ re-decided independently vs census | ~min/400 samples | `data/audit_1e7_report.txt` |

Run from inside this directory:

```bash
cd conjectures/binomial-gcd && gcc -O2 -march=native -fopenmp -o sweep699 sweep699.c -lm
./sweep699 10000000 2          # N, IMIN
python3 brute699.py 3000       # independent reference
python3 verify_triple.py       # re-verify the 2^41 triple from scratch
gcc -O2 -march=native -o domclose domclose.c -lm && python3 domclose_driver.py > jobs.txt && ./domclose < jobs.txt
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/census_brute3000.csv` | brute699.py | reference census $n \le 3000$ (concordance control) |
| `data/census_1e7_imin1.csv` | sweep699 (IMIN=1) | census $n \le 10^7$ with the i=1 theorem-control on |
| `data/family_census.csv` | family699.py | per-$(k/m)$, per-level decisions incl. UNKNOWN marks |
| `data/family_unknown_levels.csv` | family699.py log | the 28 levels past the Python cap, with (lower-bound) sizes |
| `data/domclose_closures.txt` | domclose | 17 of the 19 $2^k$ levels closed CLEAN |
| `data/domclose_highk_semiprimes.txt` | domclose | $i=2$ decisions at $k = 67, 83, 97, 103, 109$ |
| `data/family_3m_41_48.log` | family699.py | the $3^m{+}1$ extension, $m = 41..48$ |
| `data/density_2k.csv` | measure_density.py | exact $E_k$ table, $k \le 64$ plus semiprime $k \le 131$ |
| `data/audit_1e7_report.txt` | audit699.py | 408 random $n \le 10^7$ re-decided independently: 0 failures |
| `data/audit_1p372e9_report.txt` | audit699.py | 258 random $n$ over the full certified range: 0 failures |
| `data/census_prefix_1p372e9.csv` + `data/sweep_segments_done.txt` | sweep699 | the certified-prefix census and its segment evidence |
| `data/domclose_fermat.txt` | domclose | Fermat-side control: $2^{32}{+}1$, $2^{64}{+}1$ clean (suppressed $E$, as modeled) |
| `certs/verify_2_41.txt`, `certs/verify_2_67.txt` | verify_triple.py | independent verification transcripts of the new triples |
| `certs/uniq67.txt` | standalone scan | $2^{67}$ uniqueness: 1.94·10⁸ candidates, one solution |

## Known defects and open threads

- The deep sweep targeted $4\cdot10^9$ but was stopped at its time
  budget: the certified bound is the contiguous prefix
  $n \le 1.372\cdot10^9$. Blocker: the scalar fallback for doubly-smooth
  windows scales linearly in $n$ (fine at $10^7$, dominant at $10^9$) — a
  three-prime CRT or dominated-set fallback would fix it; next session.
- Undecided levels, stated plainly: $(2^{64}, i{=}2,3)$ (min dominated set
  $5.15\cdot10^{10}$); nine $3^m{+}1$ levels, $m \in \{42,44,45,46,47,48\}$
  (min sizes $\gtrsim 10^{11}$, measured); $(2^{101}, 2)$ (min
  $7.4\cdot10^{12}$; $E = 0.78$ — the model's strongest open prediction);
  $(2^{131}, 2)$ (needs >128-bit); $i \ge 3$ at $2^k$, $k > 64$ (unswept).
- Sharpest question: make R5's divergence heuristic a conditional theorem,
  or refute its independence assumption (NOTE §5 Q3).

## Prior work

Erdős–Szekeres 1978 (secondary — unreachable; exceptions at $i=2,3$ and
$(28,5,14)$ attributed to them via erdosproblems.com). Cong Lu's Rust scan
(Jan 2026): $n \le 10^7$ + families $k \le 27$, $m \le 17$, 9 tight pairs —
independently confirmed here, then extended. This session's new
contributions: the $2^{41}$ and $2^{67}$ triples (the latter predicted
before found), the family censuses to $k \le 63$ complete / semiprime
$k \le 109$, Theorems 7–8, the calibrated density model, and the
danger-zone reduction that makes deep sweeps cheap.
