# Plus–minus weighted Davenport constants (Marchan–Ordaz–Schmid, 2014)

`D±(G)` is the least `ℓ` such that every sequence of `ℓ` elements of the
finite abelian group `G` has a nonempty subsequence summing to zero when
each term may be added or subtracted. Marchan, Ordaz and Schmid determined
`D±` for every group of order ≤ 100 except one — `C₅ ⊕ C₁₅`, bracketed to
`{6, 7}` and left open since 2014 (secondary) — and flagged the `n = 3`
members of both families `C₅ ⊕ C₅ₙ`, `C₇ ⊕ C₇ₙ` as unknown in 2013. The
fault line for a session: both cells are bounded exhaustive searches (the
75-element group has only 37 sign classes), exactly what certificates are
for.

**Status:** active
**Sessions:** 2026-08-22

## Results

| Claim | Label | Where |
|---|---|---|
| `D±(C₅ ⊕ C₁₅) = 6` — resolves the last unknown group of order ≤ 100 to the lower end of the 2014 bracket `{6,7}`; four independent verification paths + maximality certificate over all 85,155 extremal sets | **CERTIFIED** | NOTE §3, Thm 7 |
| `D±(C₇ ⊕ C₂₁) = 8` — upper end of the derived bracket `{7,8}`; no published value found; three verification paths | **CERTIFIED** | NOTE §3, Thm 8 |
| Extremal sequence of `C₇ ⊕ C₂₁` is **unique** up to `Aut(G)` and signs (single orbit of size 2016 = \|GL(2,7)\|); all its elements have nonzero `C₃`-part | **CERTIFIED** | NOTE §4, Thm 10 |
| Extremal 5-sets of `C₅ ⊕ C₁₅`: exactly 85,155 in **193 Aut-orbits**, with `C₃`-support profile `3375/13500/29040/27960/11280` | **CERTIFIED** | NOTE §4, Thm 11 |
| Complete `D±` table, all abelian groups of order ≤ 150; ≤ 100 half (184 groups) matches every snippet-recoverable published value/bound (MOS Thm 3.1, exception list, `C₃⊕C₃ₙ` family) | **CERTIFIED** | NOTE §5, `table_*.csv` |
| Class model (free sequences = free sign-class subsets), elementary-2/3 linear-independence values, product bound, reduction lemma over `F₅²⊕Z₃`, saturation of maximal free sets, case (4,2) of the 6-set nonexistence | **PROVED** | NOTE §2 |
| In every computed cell `D±(G)` equals a Theorem 3.1 bound; the five sub-binary groups ≤ 100 all attain the lower bound (Question A) | observation on CERTIFIED data | NOTE §5 |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `dpm.c` | census DFS for `L(G)`/`D±(G)` over sign classes; `--raw` multiset mode; `--enum S` extremal enumeration; `--target`, `--maxdepth` | `5 15`: 0.1 s; `7 21`: 34 s; `--raw 7 21`: ~19 min | `L 5 / DPM 6`; `L 7 / DPM 8` |
| `dpm_indep.py` | clean-room Python re-implementation (tuples, immutable reach sets) | `5 15`: 27 s | census match, digit for digit |
| `verify_witness.py` | definition-level witness checker (all `3^k−1` signed sums); `--selftest` has 1 positive + 3 negative controls | ms | `VERIFIED` / `SELFTEST PASS` |
| `verify_maximality.py` | checks every enumerated extremal set is free and non-extendable — independent of both engines' DFS | 85,155 sets: ~9 min | `MAXIMALITY PASS` × 2 |
| `case_audit.py` | 4th path for `C₅⊕C₁₅`: enumeration in the `F₅² ⊕ Z₃` decomposition (NOTE Lemma 4); also proves `L(F₅²)=4` + saturation | ~4 min | `CASE AUDIT PASS`, min-violations 2 |
| `classify_extremal.py` | Aut-orbit classification of extremal sets (`--p 5` / `--p 7`) | 10 min / 1 min | 193 orbits; **1 orbit** |
| `sweep.py` | all abelian groups in an order range through `dpm`; CSV + formula controls | 2–100: ~6 min; 101–150: ~1 h | `table_002_100.csv`, `table_101_150.csv` |

Run from inside this directory:

```bash
cd conjectures/plus-minus-davenport
gcc -O2 -o dpm dpm.c
./dpm 5 15                 # the headline: L 5, DPM 6
./dpm 7 21                 # L 7, DPM 8
python3 verify_witness.py --selftest
python3 case_audit.py
python3 sweep.py 2 100 --out table_002_100.csv
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `run_5_15_census.txt`, `run_5_15_raw.txt`, `run_5_15_indep.txt` | dpm / dpm_indep | the three machine censuses for `C₅⊕C₁₅` (raw counts = `2^k ×` census, exactly) |
| `run_7_21_census.txt`, `run_7_21_raw.txt`, `run_7_21_indep.txt` | dpm / dpm_indep | same for `C₇⊕C₂₁` (see WRITEUP for the status of each at session close) |
| `enum_5_15_size5.txt` (85,155 lines), `enum_7_21_size7.txt` (2016 lines) | `dpm --enum` | every extremal free set of both groups |
| `max_5_15.txt`, `max_7_21.txt` | verify_maximality | definition-level maximality certificates (`PASS`) |
| `case_audit_out.txt` | case_audit | the five-case decomposition audit (`PASS`) |
| `classify_5_15.txt`, `classify_7_21.txt` | classify_extremal | orbit classifications (193 orbits / 1 orbit) |
| `table_002_100.csv`, `table_101_150.csv` | sweep | the full `D±` table with per-group census, witness, nodes, seconds |
| `sweep_100.log`, `sweep_150.log` | sweep | run logs (control mismatches would appear here; none did) |

## Known defects and open threads

- **All literature statements are (secondary)** — this sandbox could fetch
  no primary source. The openness of both headline cells therefore rests
  on snippet-level evidence (MOS 2014 bracket + 2021 thesis restatement +
  27 fruitless resolution-searches). Re-verify against the actual papers
  before citing; NOTE §7 lists exactly what to check.
- The hand proof of `D±(C₅⊕C₁₅) = 6` is complete only for case `(4,2)`
  (plus a pigeonhole start on `(0,6)`); the other cases rest on the
  machine audit. NOTE §8.
- `dpm_indep.py` on `C₇⊕C₂₁` — see WRITEUP for whether the Python census
  finished in-session; the 147 determination stands on
  census + raw + maximality regardless.
- Sharpest open thread: **Question A** (NOTE §5) — is `D±(G)` always one
  of the two MOS Theorem 3.1 bounds? True in every cell ≤ 150. Order 162
  (`C₃³⊕C₆`, bracket `{6,7,8}`) is the first real test.

## Prior work

(All (secondary), snippets 2026-08-22.) Adhikari–Chen–Friedlander–
Konyagin–Pappalardi introduced weighted zero-sum constants (Discrete Math.
2006); Adhikari–Rath: `D±(C_n) = ⌊log₂ n⌋+1` (Integers 2006).
Marchan–Ordaz–Schmid, "Remarks on the plus-minus weighted Davenport
constant" (IJNT 10, 2014, arXiv:1308.3316): Theorem 3.1 bounds, the ≤ 100
table, the `{6,7}` bracket for `C₅⊕C₁₅`, `C₃⊕C₃ₙ` family, `C₃²⊕C₉ = 6`;
the 2013 companion arXiv:1308.3315 (Harborth analogues);
Marchan–Ordaz–Santos–Schmid JCTA 2015 (multi-wise, elementary rank ≤ 2 and
`C₃³`, link to intersecting codes). Adhikari's 2017 survey chapter
(Springer, Alladi volume). Perez-Lavin PhD thesis (Kentucky 2021) restates
the ≤ 100 landscape and the open bracket. Merito–Ordaz–Schmid
(arXiv:2506.14279, June 2025) and Geroldinger et al. (2304.14777,
2404.17258) work on the ± monoid without new small-group values. Nothing
found resolving either headline cell; if a resolution exists in the
unreadable full texts, this session's contribution reduces to independent
certification — that risk is flagged in NOTE §7.
