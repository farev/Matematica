# Peaceable queens (OEIS A250000)

**Statement.** a(n) is the largest m such that m white and m black
queens fit on an n × n board with no queen attacking a queen of the
opposite color (attacks are not blocked; no line — row, column or
diagonal — may carry both colors). Known exactly only for n ≤ 15
(secondary: OEIS A250000; arXiv:2406.06974). At n = 16: 37 ≤ a(16),
conjectured sharp (Ainley's 1977 construction); the OEIS-recorded
finite upper bound was Pratt's a(16) ≤ 64 (ILP, 2014, secondary).

**Status.** Active, 1 session (2026-08-17). See
[`NOTE.md`](NOTE.md) for theorems and proofs,
[`WRITEUP.md`](WRITEUP.md) for the session narrative.

## Results (labels per repo convention)

| # | Result | Label |
|---|---|---|
| 1 | Line-labeling reformulation + exact B&B with proved pruning lemmas (NOTE Lemmas 1–6) | **PROVED** |
| 2 | Full ladder a(1..15) = 0,0,1,2,4,5,7,9,12,14,17,21,24,28,32 re-derived from scratch: exhaustive refutations at a(n)+1, checker-verified witnesses at a(n); first reproducible artifacts for a(14), a(15) (provenance caveat in NOTE §1) | **CERTIFIED** |
| 3 | n = 16 upper-bound walk-down (see NOTE §6 and `results/`) | **CERTIFIED** |
| 4 | Two-engine node-count equality; 40/40 SAT cross-validation (n ≤ 8, all m); DRUP-certified anchors n ≤ 7 | validation record |

## Scripts

| script | what it does | cost |
|---|---|---|
| `bnb.c` | fast exact engine; `./bnb n m [stride offset]`; exit 10 SAT (+witness), 20 UNSAT | a(13) boundary: 99 s; a(15) boundary: minutes (4-way) |
| `bnb.py` | reference engine, node-identical to `bnb.c` | ~100× slower |
| `drive.py` | 4-way parallel wrapper over `bnb` stride splitting; node sums equal serial counts (validated at n=13: 477,786,646 both ways) | — |
| `encode.py` / `encode_lines.py` | independent CNF encoders (cell-level definition / line formulation + counting cuts) | seconds |
| `solve.py` | SAT pipeline: ladder, certify (cadical --plain DRUP + rup_check), solve | n ≤ 8 practical |
| `check_peaceable.c` | independent from-definition witness checker | instant |
| `validate_bnb.py` | B&B vs SAT verdict battery | ~15 min |

## Reproduction

```bash
gcc -O2 -march=native -o bnb bnb.c && gcc -O2 -o check_peaceable check_peaceable.c
./bnb 15 33                                    # UNSAT: a(15) <= 32
./bnb 15 32 | tail -n +2 | ./check_peaceable   # witness: a(15) >= 32
python3 drive.py 16 42                         # parallel n=16 bound run
```

Run everything from inside this directory. `certs/` holds the DRUP
anchor certificates (CNF + proof + witness, SHA-256 in
`results_certify_small.out`); `witnesses/` the checker-verified
placements; `results/` the run records with node counts and times.

## Known defects / caveats

- All literature citations are **(secondary)** — the sandbox could not
  fetch any primary source (see the connectivity section of the daily
  log). In particular the provenance of the reported values a(14), a(15)
  is unresolved here, and arXiv:2406.06974 may contain finite-n bounds
  at n = 16 that snippets did not reveal; the claim "first reproducible
  artifacts" is phrased against what we could verify.
- The DRUP anchors stop at n = 7 (cell encoding; n = 8 feasible but
  slow with `--plain`). Beyond that, certification rests on the proved
  lemmas + two-engine node equality + the SAT cross-validation battery.
