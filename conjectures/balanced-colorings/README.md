# Balanced colourings of complete graphs (Erdős #617; Erdős–Gyárfás 1999)

An edge r-colouring of K_N is **balanced** if every r+1 vertices span all
r colours. Erdős–Gyárfás conjectured K_{r²+1} has no balanced r-colouring
for r ≥ 3, proved it for r = 3, 4, and noted it fails for r = 2
(all (secondary)). **r = 5 — does K₂₆ admit one? — is the first open
case** and this directory's target. It looked tractable because the
bottleneck seemed to be one SAT decision plus small certified
constructions; the session found the instance family is
resolution-/symmetry-hard (which is presumably why no computational
attack exists in the literature) and instead built the structural
reduction machinery around it.

**Status:** active — K₂₆ undecided; construction side settled (T(5) ≥ 25),
structured and vertex-regular witness routes excluded, extremal programme
E* running.
**Sessions:** 2026-08-27

## Results

| Claim | Label | Where |
|---|---|---|
| T(r) ≥ r² for prime powers r: AG(2,r)/Reed–Solomon balanced colouring; K₂₅ witness verified over all 177,100 6-subsets (K₉, K₁₆ likewise) | PROVED (construction) + CERTIFIED (witnesses) | NOTE §2, `construction.py`, `data/K25_balanced_5col.txt` |
| Balanced ⇒ no mono K_{r+1} ⇒ at K_{r²+1} every colour-complement is K_{r+1}-free with χ ≥ r+1; structured (r-partite-complement) witnesses impossible | PROVED | NOTE §1 |
| Codes with pairwise agreement ≤ 1 ⟺ partition-structured balanced colourings (Singleton cap r²; = MOLS question at r²) | PROVED | NOTE §2 |
| T(2) = 5 reproduced end-to-end (2¹⁵ exhaustion + SAT both directions) | CERTIFIED (control) | `construction.py`, `encoder.py` |
| Erdős–Gyárfás r = 3 theorem (K₁₀ has no balanced 3-colouring) machine-reproduced: BreakID SBPs + kissat, UNSAT 3.1 s (SBPs trusted, not DRUP-derived — see NOTE §6) | CERTIFIED (modulo BreakID) | NOTE §6 |
| E*(10,4) = 31 (max edges, K₄- and I₄-free, 10 vertices) — the r = 3 counting threshold is 30: **the per-class counting barrier misses by exactly one edge** | CERTIFIED | `ramsey_max.py`, `data/ramsey_10_4_ge31.txt` |
| E*(17,5) ≥ 104 (threshold 102: barrier confirmed at r = 4) | CERTIFIED | `data/ramsey_17_5_ge104.txt` |
| E*(26,6) ≥ 261 (threshold 260: barrier sharp at r = 5; kills the pure-counting and exact-rigidity routes) | CERTIFIED | `data/ramsey_26_6_ge261.txt` |
| Max circulant on Z₂₆ with no K₆/I₆: 221 edges (exhaustive over 2¹³ connection sets) | CERTIFIED | `circulant.py` |
| The AG(2,5) family (5 direction colours + 50 free pairs) does not extend to a balanced K₂₆: UNSAT, DRUP proof checked by `tools/satcert/rup_check`; q = 2 positive control finds the 2 known K₅ extensions | CERTIFIED | `extend_code.py`, `certs/extend_code_unsat.drup` |
| No Z₂₆-circulant witness (profile arithmetic 2a+b=5) and **no D₁₃-invariant witness** (0 of 3,198 admissible 65-edge classes has α ≤ 5, exhaustive) — no vertex-regular witness, in contrast to r = 2 whose witness is C₅ | PROVED (arithmetic) + CERTIFIED (exhaustion) | NOTE §5, `dihedral.py` |
| Direct CNF is CDCL-hard already at K₁₀ (135 vars): CaDiCaL/Glucose/kissat/RoundingSat all fail unaided; BreakID cures K₁₀ but not K₁₇/K₂₆ within session windows | NUMERICAL (hardness observation) | NOTE §6, WRITEUP |

The K₂₆ decision itself is **open**. Session-close solver campaign (all
kissat 4.0.4 on BreakID-broken instances, cardinality totalizers where
noted; 4-core sandbox):

| instance | window | outcome |
|---|---|---|
| K₁₀ r=3 (broken) | — | **UNSAT 3.1 s** (ErGy r=3 reproduced) |
| K₁₇ r=4 (broken) | 10 min | unknown |
| K₁₇ r=4 (broken+card), default and `--unsat` modes | ~3 h / 70 min | unknown (see below) |
| K₂₆ r=5 (broken+card) | 3 h | unknown (see below) |
| E*(17,5) ≥ 106 / 108 (broken+card) | 20 min each | unknown → bracket [104, 107] (107 by Turán uniqueness: the unique 108-edge K₅-free graph on 17 vertices is T₄(17), whose 5-part is an I₅) |
| E*(26,6) ≥ 266 / 267 / 269 (broken+card) | 60–90 min each | unknown → bracket [265, 269] (269 likewise via T₅(26)) |

## Scripts

| file | what it does | cost |
|---|---|---|
| `construction.py` | AG(2,q) balanced colourings for q=3,4,5, verified from the definition; T(2)=5 controls | 30 s |
| `encoder.py` | exact CNF (model ⟺ balanced colouring), pysat solve, witness re-verification, DIMACS export | K₂₆ build ~10 s |
| `encoder2.py` | Lemma-1 Turán-floor totalizers; `--append-to` composes with BreakID output (sound order proved in header) | seconds |
| `opb_emit.py` | native pseudo-Boolean (OPB) emission for cutting-planes solvers | seconds |
| `ramsey_max.py` | E*(N,s) via SAT: decide ≥ m, verify witnesses from the definition | seconds–hours |
| `circulant.py` | exhaustive circulant sweep for E* lower bounds (bitset clique/independence check) | ~1 min for Z₂₆ |
| `extend_code.py` | the 50-free-pairs + new-vertex extension instance; `--proof` emits DRUP | instant |
| `dihedral.py` | D₁₃ Cayley-class exhaustion (Lemma 6 profiles, α-filter with controls) | ~4 min |
| `packing_sat.py` | independent SAT cross-check of the codes⟺partitions equivalence at N = r² (SAT, verified packing) | seconds at N=25 |

Reproduce (from inside this directory; external tools: kissat 4.0.4 and
BreakID 3 built from their public sources, drat-trim optional):

```bash
pip install python-sat
python3 construction.py                    # T(5) >= 25 + controls
python3 extend_code.py                     # UNSAT: family does not extend
python3 dihedral.py                        # no D13-invariant witness
python3 ramsey_max.py 10 4 31 && python3 ramsey_max.py 10 4 32   # E*(10,4)=31
python3 encoder.py dimacs-only 10 3 --dimacs /tmp/K10.cnf        # then:
# breakid /tmp/K10.cnf /tmp/K10b.cnf && kissat /tmp/K10b.cnf     # UNSAT 3 s
```

## Data and certificates

| file | what it is |
|---|---|
| `data/K25_balanced_5col.txt` (+ K9, K16) | affine witnesses, definition-verified |
| `data/ramsey_10_4_ge31.txt`, `..._17_5_ge104.txt`, `..._26_6_ge260.txt`, `..._26_6_ge261.txt` | E* lower-bound graphs, definition-verified |
| `certs/extend_code.cnf.gz`, `certs/extend_code_unsat.drup` | the non-extension certificate (rup_check: VERIFIED, 1,160 lines) |
| `data/K5_balanced_2col_sat.txt`, `data/K9_balanced_3col_sat.txt` | SAT-side control witnesses |

## Known defects and open threads

- **All literature is (secondary).** ErGy99 and Füredi–Ramamurthi (JGT
  2002) were unreadable from this sandbox; the r = 3, 4 attribution, the
  "fails at r² infinitely often" remark, and the openness of r = 5 rest
  on the erdosproblems.com page (checked 2026-08-27), the teorth
  problems.yaml snapshot (primary, same day) and the DeepMind Lean
  formalization. Read the two papers before any external claim; they may
  contain the code correspondence and possibly E*-style bounds.
- The K₁₀ machine reproduction trusts BreakID's symmetry-breaking
  predicates (satisfiability-preserving by construction, but not
  DRUP-derivable from the base formula). A fully certified chain needs
  VeriPB-logged breaking or hand-proved WLOG constraints.
- Exact E*(17,5) and E*(26,6) are unfinished (lower bounds 104, 265;
  upper bounds open — UNSAT probes are expensive for the same hardness
  reasons as the main instance). E*(N,s) = E(s,s,N) in Radziszowski's
  DS1 notation; whether these values are tabulated there is UNCHECKED
  (all DS1 mirrors egress-blocked from this sandbox) — treat as possibly
  known until the survey is read.
- The main K₂₆ decision: next tools in order — verified symmetry
  breaking at scale, cube-and-conquer over colour-degree or K₆-pattern
  cubes on the broken+cardinality formula, or an interaction lemma over
  the E*-extremal catalogue (NOTE §7).

## Prior work

(secondary throughout; see NOTE §0 and the citation caveat above.)
Erdős–Gyárfás, Discrete Math. 200 (1999) 79–86 — the problem, r = 3, 4,
r = 2 failure, r² remarks. Füredi–Ramamurthi, JGT 2002 — splittable
colorings, extends the framework to hypergraphs. Erdős Problems database
#617 (open, "falsifiable"; page updated 2026-04-01); DeepMind
formal-conjectures `617.lean` (research open, 2026-01-24). The
codes/MOLS connection at r² is presented here without novelty claims
pending the paper reads.
