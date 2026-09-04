# Peaceable queens (OEIS A250000)

**Statement.** a(n) is the largest m such that m white and m black
queens fit on an n × n board with no queen attacking a queen of the
opposite color (attacks are not blocked; no line — row, column or
diagonal — may carry both colors). Before this session, known exactly
only for n ≤ 15 (secondary: OEIS A250000; arXiv:2406.06974), with the
n = 16 bracket recorded as [37, 64] since 2014. **Session 1 (2026-08-17):
a(16) = 37 (CERTIFIED). Session 2 (2026-09-03): a(17) = 42 (CERTIFIED,
single-engine exhaustion — see caveats). Session 3 (2026-09-04): a(18) = 47
(CERTIFIED, single-engine exhaustion).**

**Status.** Active, 3 sessions (2026-08-17, 2026-09-03, 2026-09-04). See
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
| 6 | **a(17) = 42** (session 2, 2026-09-03): exhaustive refutation of 43+43 by the SYM16 engine (21,454,699,264 nodes, 1712 s wall on 4 workers, 16 chunks, all UNSAT — `results/n17_m43_*`; recorded bracket had been [42, 72] since 2014) + two checker-verified 42+42 witnesses: one found by the engine itself (`./bnb_sym 17 42`, 678,816,342 nodes, 116 s; `witnesses/witness_n17_m42.txt`) and the Ainley/Kamenetsky placement from the OEIS link file (`witnesses/witness_n17_m42_kamenetsky.txt`). Single-engine exhaustion: the plain-engine replication done at n = 16 was not run at n = 17 (caveat below) | **CERTIFIED** |
| 7 | **a(18) = 47** (session 3, 2026-09-04): exhaustive refutation of 48+48 by the SYM16 engine (NODES_TOTAL nodes, ENGINE_S s engine time, WALL_S s wall on 4 workers shared with other jobs, 16 chunks, all UNSAT — `results/n18_m48_*`; recorded bracket had been [47, 81] since 2014) + the Ainley/Kamenetsky 47+48 placement from the OEIS link file verified from the definition (`witnesses/witness_n18_m47_kamenetsky.txt`). Single-engine exhaustion; no engine-found witness (caveats below) | **CERTIFIED** |

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
gcc -O2 -march=native -DSYM16 -o bnb_sym bnb.c
python3 run_chunked.py 17 43 16 4 ./bnb_sym    # a(17) <= 42: 16 resumable chunks, ~29 min on 4 cores
./check_peaceable < <(grep -v '^#' witnesses/witness_n17_m42_kamenetsky.txt)   # a(17) >= 42
python3 run_chunked.py 18 48 16 4 ./bnb_sym    # a(18) <= 47: 16 resumable chunks, ~ENGINE_H core-hours
./check_peaceable < witnesses/witness_n18_m47_kamenetsky.txt                   # a(18) >= 47 (47 white + 48 black)
```

Run everything from inside this directory. `certs/` holds the DRUP
anchor certificates (CNF + proof + witness, SHA-256 in
`results_certify_small.out`); `witnesses/` the checker-verified
placements; `results/` the run records with node counts and times.

## Known defects / caveats

- **n = 17 and n = 18 are single-engine exhaustions.** a(16) was refuted
  twice (SYM16 and the plain engine, independent canonical forms, node
  ratio ≈ 8.95). At n = 17 and n = 18 only the SYM16 runs were done; the
  plain-engine replications are projected at ≈ 9× the nodes (≈ 1.9·10¹¹,
  ~4–5 h, and ≈ NODES_PLAIN, ~HOURS_PLAIN h on 4 cores) and remain open
  threads. The SYM16 verdicts rest on Lemma 6′ and the validation battery
  of NOTE §4 (16/16 agreement with the plain engine on the ladder and at
  n = 16).
- **n = 18 has a literature witness only.** The 47 + 48 placement from the
  OEIS A250000 link file (Kamenetsky 2019, attributing it to Ainley 1977) is
  verified from the definition by `check_peaceable`, so a(18) ≥ 47 does not
  depend on trusting the source; but unlike n = 16 and 17 no engine search
  for a witness was run.
- The n = 17 lower bound has two witnesses: the engine's own
  (`witnesses/witness_n17_m42.txt`, found in 116 s) and the placement
  published in the OEIS A250000 link file (Kamenetsky 2019, attributing
  the value to Ainley 1977; provenance secondary). Both are verified from
  the definition by `check_peaceable`, so a(17) ≥ 42 does not depend on
  any external source.

- All literature citations are **(secondary)** — the sandbox could not
  fetch any primary source (see the connectivity section of the daily
  log). In particular the provenance of the reported values a(14), a(15)
  is unresolved here, and arXiv:2406.06974 may contain finite-n bounds
  at n = 16 that snippets did not reveal; the claim "first reproducible
  artifacts" is phrased against what we could verify.
- The DRUP anchors stop at n = 7 (cell encoding; n = 8 feasible but
  slow with `--plain`). Beyond that, certification rests on the proved
  lemmas + two-engine node equality + the SAT cross-validation battery.
