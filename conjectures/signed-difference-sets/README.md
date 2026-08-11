# Signed difference sets (Gordon, 2023)

A signed difference set SDS(v,k,λ) in a finite abelian group G of order v
is an element A of Z[G] with coefficients in {−1,0,+1}, exactly k nonzero,
with A·A^(−1) = k·e + λ(G−e) — difference sets are the all-plus case,
circulant weighing matrices the λ=0 cyclic case. Gordon introduced them
(Des. Codes Cryptogr. 91 (2023), arXiv:2212.10630) with a companion
database (github.com/dmgordo/signed-difference-sets): 70,543 cells, of
which **67,823 were Open** in the snapshot fetched 2026-08-09. The fault
line for a session: the non-cyclic small cells were open wholesale (his
exhausts ran on cyclic groups), nobody had applied the classical
character-theoretic nonexistence machinery to the shelf, and the primary
artifact is machine-readable — openness verifiable per cell.

**Status:** active
**Sessions:** [2026-08-09](../../log/2026-08-09-signed-difference-sets.md)
**Write-up page:** [fabianarevalo.com/signed-difference-sets](https://fabianarevalo.com/signed-difference-sets)

## Results (2026-08-09 session)

| Claim | Label | Where |
|---|---|---|
| Two nonexistence criteria for SDS (classical transfers; proofs in NOTE §2): **T1** — v even ⇒ k−λ a perfect square; **T2** — m \| exp(G), m > 2, p ∤ m self-conjugate mod m, v_p(k−λ) odd ⇒ no SDS | PROVED (criteria classical; transfer routine; possible overlap with the unread Gordon paper marked in NOTE) | `NOTE.md` §1–2, `theory.py` |
| **45,328 of the 67,823 Open cells closed** by T1 (23,997) + T2 (21,331), each with a checkable one-line certificate; 0 violations on the 146 Yes/All cells; 984 of Gordon's 2,574 exhaust-No cells retro-covered | PROVED (per cell, via the criteria) | `data/theory_closures.csv` |
| **58 previously-Open cells decided by exhaustive search** — **10 EXIST** (new SDS, no published source: a λ=1 set in Z₅×Z₅; (27,10,1) and (27,14,5) in both non-cyclic groups of order 27; (27,17,8) in Z₃³; (32,28,12) in Z₄×Z₈ and Z₂×Z₄×Z₄; (36,11,2) in Z₆×Z₆ and Z₃×Z₁₂), **48 NONEXIST**; every witness independently re-verified; engine validated by full v ≤ 24 concordance (42 decided cells, 0 discrepancies) and exact dual-implementation agreement on 8 cells; 0 conflicts with the criteria. **Open shelf: 67,823 → 22,453** | CERTIFIED | `data/values.csv`, `certs/`, `data/results.csv` |
| **Group structure decides existence at fixed (v,k,λ)**: at order 27 the cyclic group is empty across all ten parameter triples while Z₃×Z₉ and Z₃³ carry SDS at three of them; SDS(36,11,2) exists exactly when the 3-Sylow is non-cyclic; SDS(32,28,12) exists in exactly the two order-32 groups containing Z₄×Z₄ (7-point pattern, observation only) | CERTIFIED (tables) / NUMERICAL (the Z₄×Z₄ pattern) | NOTE §5 |
| **Witness audit of the published database: 147 of 280 stored witness sets fail the defining equation** (21 of 144 witness-bearing cells, all cyclic; not repairable by any symmetry of the definition); plus one witness stored in undeclared Z₃×Z₃×Z₂ coordinates that verifies once decoded | CERTIFIED (rerun `check_db.py` / `make_audit.py`) | `data/witness_audit.csv` |
| Forensics on SDS(20,11,2,[20]) ("All", 4 stored sets, all invalid): complete enumeration finds **exactly 40 labeled SDS in 2 translation classes**; stored sets are true sets with P↔M swaps (nearest at symmetric difference 4) — status correct, export corrupt | CERTIFIED | `certs/audit_20_11_2_c20_full.txt` |
| **Swap-repair of the corrupted witnesses**: 22 of the 147 invalid sets are ≤2 P↔M swaps from a valid SDS (each repaired set independently re-verified), recovering witnesses for **12 of the 21 affected cells** (all sets of (20,11,2), (35,21,10), (247,127,63), (499,250,123); one each for eight more up to v = 499); 9 cells remain witness-less | CERTIFIED | `data/repaired_witnesses.csv` |

## Scripts

| file | what it does | cost |
|---|---|---|
| `sdslib.py` | independent checker (no code shared with Gordon's `is_sds`): parser, group tables, full verification | instant |
| `check_db.py` | control battery: verify all 280 stored witnesses + corruption negative controls | 13 s |
| `make_audit.py` | writes `data/witness_audit.csv` (per-set verdicts) | 13 s |
| `sds_search.c` | exhaustive DFS engine: forced \|P\|/\|M\| split, incremental correlations, open-pair interval pruning, translation reduction (0 ∈ P); `--all` for complete unreduced enumeration | ms–hours per cell |
| `check_engine.py` | dual-implementation control: independent Python exhaust must match engine witness lists exactly on 8 cells | 2 s |
| `sweep.py` | production driver: run cells, verify witnesses independently, append `data/results.csv`, write `certs/` | varies |
| `theory.py` | T0/T1/T2 criteria over all 70,543 cells + cross-checks (Yes/All violations must be 0; exhaust conflicts must be 0) | 1 s |
| `repair.py` | ≤2-swap repair search over all invalid stored witnesses; repaired sets re-verified independently | 70 s |
| `make_values.py` | aggregates `data/results.csv` → authoritative `data/values.csv`; aborts on conflicts | instant |

Reproduce (from inside this directory):

```bash
gcc -O2 -o sds_search sds_search.c
python3 check_db.py          # witness audit controls (exit 1 by design: DB defect)
python3 check_engine.py      # dual-implementation validation
python3 theory.py            # 45,328 closures + zero-conflict cross-checks
python3 sweep.py --vmax 24   # reproduce the 42-cell concordance + first decisions
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/sds.json` | fetched 2026-08-09 | pinned snapshot of Gordon's database (sha256 `39bab9fc…ca85`), with his `sds_code.py`, README, LICENSE (CC-BY-4.0) |
| `data/theory_closures.csv` | `theory.py` | 45,328 closed Open cells with per-cell criterion certificates |
| `data/witness_audit.csv` | `make_audit.py` | verdict for each of the 280 stored witness sets |
| `data/results.csv` | `sweep.py` | append-only run log: every engine run with node counts, wall time, engine+source sha256 |
| `data/values.csv` | `make_values.py` | authoritative table of the 58 decided previously-Open cells |
| `data/repaired_witnesses.csv` | `repair.py` | swap-repair verdicts for all 147 invalid stored sets; 22 repaired+re-verified |
| `certs/*.txt` | `sweep.py` | per-cell certificates: command, result, witnesses in index+coordinate form, provenance hashes |

## Known defects and open threads

- The (32,20,4) family across all seven abelian groups of order 32
  survives both criteria and is beyond today's exhaust budget (naive
  5.5·10¹¹ per group). Automorphism-orbit canonicalization (huge for
  [2,2,2,2,2]: \|GL(5,2)\| ≈ 10⁷) would collapse it; the engine only
  uses translation reduction.
- The remaining Open shelf after this session (~22k cells) passes T1/T2;
  which stronger classical tests (multiplier theorems, Mann test, field
  descent) transfer to signed sets is the open theory question — ramified
  primes escape self-conjugacy here (Gauss sums realize \|α\|² = p).
- Gordon's equivalence convention for "All" cells (how his set lists are
  normalized) is not pinned; complete enumerations here report labeled
  counts and translation classes instead. Pin before contributing
  upstream.
- The audit and closures should be reported to Gordon
  (dmgordo@gmail.com per his README) — an upstream contribution pass is
  queued for a session with email/github access.
- Everything cites the paper only at abstract level (egress-blocked);
  criteria marked as possible rediscoveries of statements his paper may
  contain. The per-cell closures are new to the database regardless.

## Prior work

Gordon (2023) introduced SDS, built the database, ran cyclic orbit
exhausts (2,574 No cells, 87 Yes, 59 All). He–Chen–Ge (arXiv:2306.05631)
added PDS-based constructions (ten Yes cells credited in the DB). The
nonexistence criteria used here are classical: the even-order square
condition of symmetric-design theory and Turyn's self-conjugacy argument
(Pacific J. Math. 1965), both (secondary). No other work on signed
difference sets was findable by search (2024–2026: nothing).
