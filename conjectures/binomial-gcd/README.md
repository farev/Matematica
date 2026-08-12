# Common prime factors of binomial coefficients (Erdős–Szekeres 1978, Erdős problem #699)

For $1 \le i < j \le \lfloor n/2\rfloor$, is there always a prime $p \ge i$
dividing both $\binom{n}{i}$ and $\binom{n}{j}$? Erdős–Szekeres conjectured
yes, and that $p > i$ works outside a finite exceptional set. The fault
line: the exceptional ("tight") triples are governed by exact digit
conditions (Kummer) at structured $n$, so both a deep certified sweep and
family censuses far beyond it are one afternoon of the right algorithm.
Status of #699 verified open 2026-08-12 from `teorth/erdosproblems`
(`falsifiable`) and the Lean formalization (both `research open`).

**Status:** active
**Sessions:** 2026-08-12

## Results

| Claim | Label | Where |
|---|---|---|
| #699 holds for $4 \le n \le 10^7$ — independent confirmation of the Jan 2026 scan (different algorithm, 30 s vs ~120 core-h) | CERTIFIED | NOTE §4 R1 |
| **New tight triple $(2^{41},\,2,\,285920731515)$** — largest known, unique $j$ at $(2^{41},2)$, verified by standalone checker | CERTIFIED | NOTE §4 R3, `certs/` |
| Complete tight-triple census $n \le 10^7$: the 9 known + the new one; families $2^k$ ($k\le 44$ all levels; $k\le 64$ minus 19 marked levels) and $3^m{+}1$ ($m \le 40$, $i\ge2$): members are exactly $k \in \{4,9,11,41\}$, $m \in \{2,3,5,7,13\}$ | CERTIFIED | NOTE §4 R2/R4 |
| Mersenne exclusion: $2^k{-}1$ prime ⇒ no tight triple at $(2^k, 2)$; exact criterion for any $k$ | PROVED | NOTE Thm 7 |
| $i=3$ family mechanism: $m=2$ or ($m$ odd, $(3^m{+}1)/4$ prime, $(3^m{-}1)/2$ a prime power) ⇒ $(3^m{+}1, 3, n/2)$ tight — explains all five known members | PROVED | NOTE Thm 8 |
| Reduction machinery: gcd>1 theorem, window criterion, danger zone $i \le n - \mathrm{prevprime}(n)$, exact tightness criterion | PROVED | NOTE Props 0–6 |
| $i=3$ family heuristically finite ($\sum 1/m^2$); $i=2$ family shows *no decay* — strengthening's finite-set form is unrefuted but not supported | NUMERICAL | NOTE §4 R5 |

Deeper full sweep in flight; the bound in R1 moves only when it completes.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `sweep699.c` | full certified sweep $n \le N$ (danger-zone + CRT algorithm) | $10^7$: 15 s; $4{\cdot}10^9$: ~2.5 h (4 cores) | `census699.csv`, stats |
| `brute699.py` | independent reference sweep (full prime matrix) | $n \le 3000$: 60 s | `brute699_out.csv` |
| `family699.py` | exact criterion at $n = 2^k$, $3^m{+}1$ (sympy factoring + dominated-set enumeration) | $k \le 64$, $m \le 40$: ~25 min | `family_census.csv` |
| `verify_triple.py` | standalone verifier for claimed tight triples + uniqueness scan | ~2 min | `certs/verify_2_41.txt` |
| `audit699.py` | deep-sample audit: random $n$ re-decided independently vs census | ~min/1000 samples | audit report |

Run from inside this directory:

```bash
cd conjectures/binomial-gcd && gcc -O2 -march=native -fopenmp -o sweep699 sweep699.c -lm
./sweep699 10000000 2        # N, IMIN (use IMIN=1 for the Prop-0 control battery)
python3 brute699.py 3000     # independent reference
python3 verify_triple.py     # re-verify the new triple from scratch
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/census_brute3000.csv` | brute699.py | reference census $n \le 3000$ (concordance control) |
| `data/census_1e7_imin1.csv` | sweep699 (IMIN=1) | census $n \le 10^7$ with the i=1 theorem-control on |
| `data/family_census.csv` | family699.py | per-$(k/m)$, per-level decisions incl. UNKNOWN marks |
| `data/family_unknown_levels.csv` | family699.py log | all 28 undecided levels (19 at $2^k$, 9 at $3^m{+}1$), with min dominated-set sizes |
| `certs/verify_2_41.txt` | verify_triple.py | independent verification transcript of the new triple |

## Known defects and open threads

- The deep-sweep bound (target $4\cdot10^9$) is **not yet certified** — run
  in flight at session close; only $10^7$ is claimed. See log.
- 19 family levels $(k,i)$ for $2^k$ ($45 \le k \le 64$) and 9 for $3^m{+}1$ ($m \ge 42$) are UNKNOWN (dominated sets
  $> 10^8$ elements); a compiled enumerator would close them.
- Sharpest question: is the $i=2$ family infinite? (NOTE §5 Q3 — would
  refute the strengthening as formalized.)

## Prior work

Erdős–Szekeres 1978 (secondary — unreachable; exceptions at $i=2,3$ and
$(28,5,14)$ attributed to them via erdosproblems.com). Cong Lu's Rust scan
(Jan 2026): $n \le 10^7$ + families $k \le 27$, $m \le 17$, 9 tight pairs —
independently confirmed here, then extended. This session's new
contributions: the $2^{41}$ triple, the family censuses to $k \le 64$ /
$m \le 40$, Theorems 7–8, and the reduction that makes deep sweeps cheap.
