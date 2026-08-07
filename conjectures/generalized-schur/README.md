# Generalized Schur numbers (Ahmed–Schaal Conjecture 2.1 and the s = 3 family)

For an equation `L(t): x₁ + x₂ + ⋯ + x_{t−1} = x_t` (repeats allowed), the
generalized Schur number `S(k; t₀,…,t_{k−1})` is the least `m` such that every
`k`-coloring of `{1,…,m}` has, for some color `i`, a monochromatic solution of
`L(t_i)` in color `i`. The classical Schur number is `S(k;3,…,3)`.

Ahmed–Schaal (Exp. Math. 2016) computed the 26 values that were the entire
published frontier and conjectured `S(3;s,t,u) = stu − tu − u − 1` for
`4 ≤ s ≤ t ≤ u` (Conjecture 2.1); for the `s = 3` family they conjectured only
a strict inequality (Conjecture 2.2), proved by Song–Mao in April 2026 — no
formula for `S(3;3,t,u)` is known or conjectured. **No new exact value in this
family had been published since 2016** (the diagonal became a theorem in 2019:
Boza–Marín–Revuelta–Sanz, `S(3;t,t,t) = t³−t²−t−1`).

The fault line for a session: modern SAT solvers plus the repo's certified-
UNSAT toolkit (`tools/satcert/`) decide these boundaries in seconds-to-minutes
at sizes the 2015 search stopped at, and every verdict ships a checkable
certificate — a DRUP proof for the UNSAT side, an explicitly verified coloring
for the SAT side.

**Status:** active
**Sessions:** [2026-08-07](../../log/2026-08-07-generalized-schur.md)

## Results

Every value below carries a DRUP proof at `S` checked by
`tools/satcert/rup_check` and an independently verified witness coloring at
`S−1`, both in `certs/`; authoritative list in `data/new_values.csv`.

| Claim | Label | Where |
|---|---|---|
| New exact values, `s ≥ 4` (first since 2016), each **confirming** an open instance of Conjecture 2.1: `S(3;4,4,8) = 87`, `S(3;4,4,9) = 98` | CERTIFIED | `data/new_values.csv`, `certs/` |
| New exact values in the unmapped `s = 3` family: `S(3;3,3,8) = 59`, `S(3;3,3,9) = 68`, `S(3;3,4,8) = 67`, `S(3;3,4,9) = 78`, `S(3;3,5,8) = 91` (+ further, see CSV) | CERTIFIED | `data/new_values.csv`, `certs/` |
| Complete extremal structure of `(3,3,u)`, `u ∈ {4,5,6,8,9}`: one mirror-symmetric skeleton + `u−2` free ternary slots at `2u+1+5j`; `2·3^{u−2}` extremals; max `L(u)`-class `5(u−2)`; all of it breaks at `u = 7` except the class law | CERTIFIED | `NOTE.md` §6, `data/skeletons_33u.txt`, `certs/*.extremals` |
| `S(3;3,3,u) = 9u−13` for all `u ≥ 4` except `u = 7` (Conjecture A) | conjecture; CERTIFIED at computed `u` | `NOTE.md` §6 |
| 11 published boundary values + 12 published climb values + all 10 published enumeration counts reproduced; unique `(3,4,5)` extremal matches the paper character-for-character | CERTIFIED (controls) | `data/results_controls.csv`, NOTE §4 |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `schur3.py` | CNF encoder/decider for `S(k;t₀,…)` boundaries: per-color equation clauses (deduped support sets), Glucose42 + DRUP for proofs, Cadical for exploration; `--enum` enumerates **all** valid colorings (exactly-one encoding) | ms–minutes per instance | UNSAT/SAT verdicts + certificates |
| `verify_witness.py` | independent witness checker — iterated-sumset bitsets, an algorithm disjoint from the encoder | instant | `WITNESS OK` / violating tuple |
| `schur_search.py` | exact-value climb: Cadical probes from a proved lower bound, then certified Glucose boundary pair | seconds per probe | `S = … CERTIFIED` |
| `new_values.py` | certified boundary-pair driver for conjectured values; handles the refutation branch (verified witness + climb) | seconds–hours per triple | `data/results_a1.csv` |
| `witness_blocks.py` | run-length structure of witness colorings | instant | block decompositions |
| `make_table.py` | aggregates lane logs into `data/new_values.csv`, aborts on any control mismatch | instant | the results table |

Run from inside this directory:

```bash
cd conjectures/generalized-schur
gcc -O2 -o ../../tools/satcert/rup_check ../../tools/satcert/rup_check.c   # once
python3 schur3.py 3,3,3 14            # UNSAT, rup_check VERIFIED  (control)
python3 schur3.py 4,4,8 87            # UNSAT at the first new value
python3 schur3.py 4,4,8 86 --no-proof # SAT; then verify:
python3 verify_witness.py work/s4_4_8_n86.witness
python3 schur3.py 3,3,4 22 --enum     # 18 extremal colorings (paper: 18)
python3 make_table.py                 # rebuild the results table
```

## Data and certificates

| file | what it is |
|---|---|
| `data/published_values.csv` | the complete published boundary (Table 1 of Ahmed–Schaal, primary source, URL + sha256 in `data/environment.txt`) |
| `data/new_values.csv` | every value computed this session, control vs NEW, Conjecture 2.1 status |
| `data/results_a1.csv` | per-run details: times, proof sizes, CNF sha256, verification status |
| `certs/*.drup` | DRUP proofs of every UNSAT boundary (checked by `rup_check`) |
| `certs/*.witness` | verified colorings at every `S−1` (checked by `verify_witness.py`) |
| `certs/*.extremals` | complete extremal-coloring enumerations (counts match the paper's Theorems 2.1–2.10 in all ten published cases) |
| `data/lane_*.log` | raw run transcripts with timings |

CNF files are not stored: the encoder is deterministic, so
`python3 schur3.py s,t,u N` regenerates each byte-identically;
`data/results_a1.csv` records the sha256 of every boundary CNF.

## Known defects and open threads

- The Ahmed–Schaal preprint is the **author version** (journal PDF paywalled);
  page range and abstract match the journal listing. The Boza et al. diagonal
  theorem and the Song–Mao abstract are **(secondary)** — verbatim abstract via
  an arXiv-RSS mirror, k-range of the diagonal formula inferred from the
  digest. Minor venues (INTEGERS full texts, theses, MathSciNet) were
  unreachable; an isolated value there could predate one of ours.
- *(open threads filled at session end)*

## Prior work

Ahmed–Schaal, *On Generalized Schur Numbers*, Exp. Math. 25(2) 2016, 213–218
(**primary — read in session**); Song–Mao, arXiv:2604.11030 (Apr 2026)
(secondary, verbatim abstract); Boza–Marín–Revuelta–Sanz, DAM 263 (2019)
(secondary); Robertson–Schaal 2001 (2-color, quoted in the primary);
Beutelspacher–Brestovansky 1982; Heule, *Schur Number Five*, arXiv:1711.08076
(secondary). Full sourcing in `NOTE.md` §7.
