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
**Sessions:** [2026-08-09](../../log/2026-08-09-signed-difference-sets.md),
[2026-08-12](../../log/2026-08-12-signed-difference-sets.md)
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

## Results (2026-08-12 session: review of Masselot's census)

Masselot's `certified-small-sds-census` v1.0 (2026-08-12) resolves all
68 Open cells of order ≤ 36 in the same frozen snapshot, 58 of them
agreeing with this census (his novelty screen credits this repository;
zero conflicts, confirmed from our side), plus the 10 cells left open
here: signed (32,20,4) sets exist in an abelian group of order 32 iff
the group is noncyclic, and no signed (36,29,4) set exists at order 36.
Reviewed at his request; full report in
[`masselot-review/REVIEW.md`](masselot-review/REVIEW.md).

| Claim | Label | Where |
|---|---|---|
| All 16 of Masselot's existence witnesses (incl. the six (32,20,4) noncyclic constructions) pass this repo's independent checker; the six order-32 file hashes match his note | CERTIFIED | `masselot-review/out/witness_verification.csv` |
| All four of his nonexistence legs re-derived by complete searches with independent code and no symmetry reduction: (32,20,4,[32]) via C8→C16→C32 (2,985,984 refinements, 0), (36,29,4) in [2,18] and [3,12] via full quotient systems (0 each), and in [6,6] via 16,964,640 marginal-consistent vectors (0), solver-free; every §5–§7 count of his note (9,528 / 56 / 12 / 248,832 / 144 / 420 / 106,353 / 9) reproduced exactly | CERTIFIED | `masselot-review/check_targets.py`, `out/targets_report.json` |
| **The C18 quotient system of (36,29,4) is empty**, so no SDS(36,29,4) exists in C36 or C2×C18: the abelian order-36 classification no longer needs the database's unreplicated cyclic exhaust | CERTIFIED (complete enumeration; projection lemma PROVED in NOTE §5.1) | `masselot-review/out/targets_run_log.txt` |
| Gordon's paper and He–Chen–Ge read in full (session 1 had them secondary-only): neither states the T1/T2 transfers, so the session-1 rediscovery caveat is lifted; Lemma 1 = Gordon's Lemma 1.1 + He–Chen–Ge Lemma 2.2 | resolved caveat | NOTE §2 remarks (updated) |
| His v1.1 revision (paper dated 2026-08-21, checked 2026-08-25) verified: the six constructions printed in its Appendix A match the pinned witness files exactly; the new C18 stage counts reconcile (his 19,152 = the norm ≤ 33 slice of the full 23,184 parity-matching refinements; 7,560 at norm 33; 0 solutions); his adapted C6×C6 rerun reproduces 36 pairs / 16,964,640 / 0; review attribution and AI-boundary description accurate, pinned commit resolves | CERTIFIED | `masselot-review/check_v11_revision.py`, `out/v11_revision_checks.txt` |

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
| `masselot-review/verify_witnesses.py` | re-verify Masselot's 16 witnesses with `sdslib` | 2 s |
| `masselot-review/validate_pipeline.py` | known-answer controls for the review's search machinery (must all PASS) | 10 s |
| `masselot-review/check_targets.py` | complete independent re-derivation of his four nonexistence legs + the C18 observation | 55 s |
| `masselot-review/check_v11_revision.py <pdf>` | v1.1 revision checks: Appendix A constructions vs pinned witnesses, C18 stage counts with norm histogram | 30 s |

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

- ~~The (32,20,4) family across all seven abelian groups of order 32
  survives both criteria and is beyond today's exhaust budget (naive
  5.5·10¹¹ per group).~~ Closed externally by Masselot (v1.0,
  2026-08-12): exists iff the group is noncyclic. Fully verified here
  (session 2); the quotient-ladder route that cracked it costs seconds,
  not core-hours — the lesson for the ~22k remaining Open cells is that
  layered quotient refinement beats raw DFS wherever the marginal
  systems are tight.
- The remaining Open shelf (~22k cells) passes T1/T2; which stronger
  classical tests (multiplier theorems, Mann test, field descent)
  transfer to signed sets is the open theory question — ramified
  primes escape self-conjugacy here (Gauss sums realize \|α\|² = p).
- Gordon's equivalence convention for "All" cells (how his set lists are
  normalized) is not pinned; complete enumerations here report labeled
  counts and translation classes instead. Pin before contributing
  upstream.
- The audit and closures should be reported to Gordon
  (dmgordo@gmail.com per his README) — now best coordinated with
  Masselot, whose census closes the whole order ≤ 36 shelf; suggested
  in the review reply.
- ~~Everything cites the paper only at abstract level (egress-blocked).~~
  Session 2 read Gordon and He–Chen–Ge in full: neither states the
  T1/T2 transfers (rediscovery caveat lifted); Gordon's Lemma 5.2 is
  the moment form of the quotient projection lemma; his sporadic table
  and He–Chen–Ge's families do not touch the ten closed cells.

## Prior work

Gordon (2023) introduced SDS, built the database, ran cyclic orbit
exhausts (2,574 No cells, 87 Yes, 59 All); read in full 2026-08-12.
He–Chen–Ge (Des. Codes Cryptogr. 92 (2024), arXiv:2306.05631) added
PDS-based constructions (ten Yes cells credited in the DB); read in
full 2026-08-12. Masselot's `certified-small-sds-census` v1.0
(2026-08-12, github.com/NicolasMasselot, Zenodo 10.5281/zenodo.21901581)
closes all 68 Open cells of order ≤ 36, replicating this repo's 58
decisions (credited, zero conflicts) and adding the ten this repo left
open; reviewed and verified here, see `masselot-review/`. The
nonexistence criteria used here are classical: the even-order square
condition of symmetric-design theory and Turyn's self-conjugacy
argument (Pacific J. Math. 1965, still secondary). No other work on
signed difference sets was findable by search (2024–2026: nothing).
