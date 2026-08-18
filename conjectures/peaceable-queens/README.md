# Peaceable queens (OEIS A250000)

**Statement.** a(n) is the largest m such that m white and m black
queens fit on an n × n board with no queen attacking a queen of the
opposite color (attacks are not blocked; no line — row, column or
diagonal — may carry both colors). Before this session, known exactly
only for n ≤ 15 (secondary: OEIS A250000; arXiv:2406.06974), with the
n = 16 bracket recorded as [37, 64] since 2014. **This session:
a(16) = 37 (CERTIFIED).**

**Status.** Active, 1 session (2026-08-17). See
[`NOTE.md`](NOTE.md) for theorems and proofs,
[`WRITEUP.md`](WRITEUP.md) for the session narrative.
**Write-up page:** [fabianarevalo.com/peaceable-queens](https://fabianarevalo.com/peaceable-queens)

## Results (labels per repo convention)

| # | Result | Label |
|---|---|---|
| 1 | **a(16) = 37** — smallest open case of A250000 decided: exhaustive refutation of 38+38 (5.03B nodes, 462 s, 16 chunks, SYM16 engine) + checker-verified 37+37 witness found by both engines | **CERTIFIED** |
| 2 | Line-labeling reformulation + exact B&B with proved pruning lemmas and canonical forms (NOTE Lemmas 1–6′) | **PROVED** |
| 3 | Full ladder a(1..15) = 0,0,1,2,4,5,7,9,12,14,17,21,24,28,32 re-derived from scratch: exhaustive refutations at a(n)+1, checker-verified witnesses at a(n); first reproducible artifacts for a(14), a(15) (provenance caveat in NOTE §1) | **CERTIFIED** |
| 4 | a(16) ≤ 41 en route (m = 42 exhausted: 607M nodes, 174 s) — recorded bracket had been [37, 64] | **CERTIFIED** |
| 5 | Two-engine node-count equality; 40/40 SAT cross-validation (n ≤ 8, all m); DRUP-certified anchors n ≤ 7; sym-vs-plain 16/16 on ladder boundaries | validation record |

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
