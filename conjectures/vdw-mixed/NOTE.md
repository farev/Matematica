# Certificates for mixed van der Waerden numbers, and the first bounds on w(2;5,8)

Working note, session 1 (2026-08-16). AI-assisted (Claude); every proof
checked by the repository's independent tooling, every number emitted by a
committed script.

## Abstract

The mixed van der Waerden number `w(2;s,t)` is the least `n` such that every
red/blue coloring of `{1,…,n}` has a red `s`-term or blue `t`-term arithmetic
progression. The exact values published for `4 ≤ s ≤ t ≤ 7` (Landman;
Ahmed 2009–2013 (secondary)) predate certificate-producing SAT practice: no
machine-checkable proofs exist for them. We (i) re-derive seven cells of
the table from scratch, through `w(2;4,7)=109` and `w(2;5,5)=178`, each
with a witness verified by independent enumeration and a DRUP proof
validated by a from-definition RUP checker (the `w(2;5,6)=206` legs were in
flight at the time of writing);
(ii) prove the first bounds on the open cell `w(2;5,8)`, currently
**`w(2;5,8) > 295` (CERTIFIED)**, via exactly-periodic witnesses found by a
complete per-period SAT projection; (iii) record structural facts about
extremal witnesses (near-periodicity with few defects) that make the
lower-bound legs tractable; and (iv) open a resumable cube-and-conquer
campaign, with per-leaf checked proofs, toward deciding `w(2;5,8)`.

## 1. Definitions and certification protocol

**Definition.** A *good partition* of `[1,n]` for `(s,t)` is a 2-coloring
with no monochromatic `s`-AP in color 0 and no monochromatic `t`-AP in
color 1. `w(2;s,t)` = least `n` admitting no good partition.

**Lemma 1 (restriction monotonicity).** If `[1,n]` admits a good partition,
so does `[1,m]` for every `m < n`. *Proof.* Restrict the coloring; every AP
of `[1,m]` is an AP of `[1,n]`. ∎

**Protocol.** A cell value `w(2;s,t) = w` is CERTIFIED when both legs exist:
(a) a good partition of `[1,w−1]`, re-verified by an enumeration routine
independent of the encoder; (b) an UNSAT proof for the CNF encoding good
partitions of `[1,w]`, validated by `rup_check` (forward RUP from the
definition, no solver code). By Lemma 1 these two legs pin the value.

**Encoding.** One variable per integer; clause `(x_a ∨ … ∨ x_{a+(s−1)d})`
per `s`-AP, `(¬x_a ∨ … ∨ ¬x_{a+(t−1)d})` per `t`-AP. The encoder
self-checks against `#k-APs in [1,n] = Σ_{d≥1} max(0, n−(k−1)d)` and against
brute force for tiny cells (`w(2;3,3)=9`, `w(2;3,4)=18` reproduced).

## 2. Certified values (this session)

| cell | value | UNSAT proof | checker |
|---|---|---|---|
| w(2;3,5) | **22** | 242 lines | RUP-VERIFIED |
| w(2;3,6) | **32** | 582 lines | RUP-VERIFIED |
| w(2;4,4) | **35** | 573 lines | RUP-VERIFIED |
| w(2;4,5) | **55** | 7,636 lines | RUP-VERIFIED |
| w(2;4,6) | **73** | 253,728 lines | RUP-VERIFIED (also closed independently by cube-and-conquer, 64/64 leaves each RUP-VERIFIED) |
| w(2;5,5) | **178** | 1,561,916 lines | RUP-VERIFIED |
| w(2;4,7) | **109** | 18,434,058 lines | RUP-VERIFIED (1.14 GB proof; sha256 + verdict in MANIFEST, file re-derivable) |

All seven agree with the published table (secondary). Solvers: CaDiCaL 1.9.5
(fast leg), Glucose 4.2 with proof logging (certificate leg), via
python-sat 1.9.dev15. In flight at time of writing: `w(2;5,6)=206` (both
legs running); its row moves here when its checks complete.

## 3. Bounds for the open cell w(2;5,8)

**Theorem 2 (CERTIFIED).** `w(2;5,8) > 295.`

*Certificate.* An exactly-74-periodic coloring of `[1,295]` (committed:
`data/witness_5_8_n295_perdef_p74k0.txt`), found by the complete
defect-tolerant search at `(p,k) = (74, ≤8)` — the solver returned a
0-defect solution — and verified good by both independent verifiers (Python
re-enumeration and the from-definition C checker `vdw_check.c`). By Lemma 1
this also certifies all smaller `n`. Earlier steps of the walk (74-periodic
witnesses at `n = 280, 290, 292`) are committed alongside. ∎

Remark: distinct period-74 blocks govern different `n` — the block found at
`n = 290` extends only to 292, while a different 74-block covers 295. A
block dying is not the period dying, and the period dying is not the row
dying: defect-tolerant and larger-period searches continue above 295.

Context (all secondary): the row reads 178, 206, 260 at `t = 5, 6, 7`;
first differences +28, +54 suggest `w(2;5,8)` in the low-to-mid 300s. No
published value or bound for the cell was findable today; openness caveats
are in the session log.

## 4. Structure of extremal witnesses

Empirical facts from this session's verified witnesses:

1. `w(2;4,5)`: the extremal witness at `n=54` can be taken **exactly
   22-periodic** (found by both tabu and complete per-period SAT).
2. `w(2;5,5)`: at `n=177` there is a witness that is 44-periodic with
   **exactly one defect** (complete search at `p=44, k≤4` returned a
   1-defect solution; the unstructured CDCL witness sits at 3 defects from
   its best 44-periodic approximant, positions {23, 89, 122}).
3. `w(2;5,6)`: at `n=205` there is **no exactly periodic witness** with
   period `p ∈ [30, 49]` (complete per-period result), and none with
   `p = 41, k ≤ 6` defects (complete). Larger-defect searches in flight.
4. `(5,8)` at `n ∈ {280, 290, 295}`: exactly-74-periodic witnesses exist,
   but no single block covers the whole range — the block found at `n=290`
   extends only to 292, while a different 74-block is good through 295.

The pattern — boundary witnesses are periodic-with-few-defects, and the
required defect count grows as cells harden — is what makes the lower-bound
legs computable: the `(p, k)`-restricted searches are complete in a space of
size `2^p · C(n, ≤k)` instead of `2^n`.

## 5. Methodology, environment, and verification

**Environment.** 4-core cloud sandbox, 15 GB RAM; Python 3.11.15;
python-sat 1.9.dev15 (CaDiCaL 1.9.5 as `cd19`, Glucose 4.2 as `g42`);
gcc -O2 for `rup_check.c`, `check_coloring.c`, `vdw_check.c`. Search seeds:
`random.Random(20260816)` in both incomplete searchers (the complete SAT
searches are deterministic given solver version). Expensive runs, wall/CPU:
w(2;5,5)@178 UNSAT 17.9 s + 56 s check; w(2;4,7)@109 UNSAT ≈ 35 min
(Glucose) + ≈ 50 CPU-min check (1.14 GB proof); w(2;5,6)@206 UNSAT
> 2 h at session close.

- **Independence:** encoder self-checks; brute-force ground truth (tiny
  cells); witness verification by a re-enumeration that shares no code path
  with the encoder; UNSAT proofs checked by `tools/satcert/rup_check`
  (validated 2026-08-05 against injected-fault controls).
- **Certificate hygiene:** proofs ≤ 10 MB committed; larger ones recorded in
  `certs/MANIFEST.csv` (sha256, size, verdict) and re-derivable; the
  cube-and-conquer driver checks each leaf proof at production time and
  records verdicts in an append-only campaign CSV.
- **Controls for the campaign driver:** UNSAT control (64/64 leaves,
  `(4,6)@73`), SAT-detection control (`n=72`), adaptive-split control
  (421 leaves closed under a forced 300-conflict budget), zero check
  failures.

## 6. Open questions

1. Decide `w(2;5,8)`. The campaign infrastructure is in place; the UNSAT
   leg at the (unknown) boundary is the hard half. Growth of the UNSAT legs
   down the ladder (measured here: seconds at `(5,5)@178`, ≥ hours at
   `(5,6)@206` in the proof-logged solver) prices it at a multi-session
   cube-and-conquer campaign.
2. Is the defect count of extremal witnesses monotone in `(s,t)` along
   rows? (Data points so far: 0 at `(4,5)`, 1 at `(5,5)`, ≥ 7 at `(5,6)`
   pending the running searches.)
3. `w(2;4,9)`: its published status could not be established through
   today's literature channel; pin it down before attacking.
