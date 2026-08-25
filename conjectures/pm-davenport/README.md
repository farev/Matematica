# Plus–minus weighted Davenport constants (maximum dissociated sets)

**Problem.** For a finite abelian group `G`, `D±(G)` is the least `ℓ`
such that every sequence of `ℓ` elements has a nonempty subsequence
summing to zero with coefficients `±1`. Equivalently `D±(G) − 1 = μ(G)`,
the maximum size of a **dissociated** subset of `G` (all subset sums
distinct). Adhikari–Grynkiewicz–Sun (2012, (secondary)) bracket:
`Σ⌊log₂ dᵢ⌋ + 1 ≤ D±(G) ≤ ⌊log₂|G|⌋ + 1`. Marchan–Ordaz–Schmid
(IJNT 2014, (secondary)) determined `D±` for all `|G| ≤ 100` except one
group: `C₅ ⊕ C₁₅`, "either 6 or 7".

**Status: active.** Session 1 (2026-08-25):

| result | label |
|---|---|
| `D±(C₅ ⊕ C₁₅) = 6` — the last open group of order ≤ 100, decided at the *lower* end of the bracket; no dissociated 6-set exists (2,324,784 subsets exhausted; three independent engines; identical census of 85,155 extremal 5-sets) | **CERTIFIED** |
| `D±(C₇ ⊕ C₂₁) = 8` — attains the pigeonhole bound; verified 7-element witness; upper bound is a proved lemma (no search) | **CERTIFIED** |
| `μ(G)` for **every** abelian group of order ≤ 192; deficient groups in range: `C₃², C₃³, C₃⁴, C₃²⊕C₉, C₅⊕C₁₅` ⟨plus any found in 101–192 — see NOTE §3⟩ | **CERTIFIED** |
| Bracket lemmas, `μ(C_p^r) = r` for `p ∈ {2,3}`, checksum construction `μ(C_m⊕H) ≥ ν_m(H)`, graded counting bound (NOTE §2) | **PROVED** |
| Family values beyond order 192 (`C₃⊕C₃ₙ`, `C₅⊕C₅ₙ`, `C₇⊕C₇ₙ`, `C₁₃²`, `C₇³`, `C₅²⊕C₁₅`) | **CERTIFIED** (see NOTE §3, some runs pending) |

**Caveat (novelty).** All literature statements are (secondary) —
WebSearch snippets, 2026-08-25; primary sources were unreachable from the
session sandbox. NOTE.md §8 lists the mandatory pre-publication checks
(read arXiv:1308.3316 first).

## Scripts

| script | what it does | cost |
|---|---|---|
| `dpm.py n1 [n2 …] [--all]` | Engine A: exact `μ(G)`, witnesses, extremal census (Python set-DFS) | ms–minutes |
| `dpm_fast.c` → `./dpm_fast n1 [n2 …]` | Engine B: same spec, independent C implementation | ms–minutes; large N up to hours |
| `refute_brute.c` → `./refute_brute t n1 [n2 …]` | Engine C: unpruned brute force — all t-subsets × all ternary sign vectors | `C(37,6)`: 7 s |
| `verify_witness.py "n1,n2" "(a,b) …"` | independent witness verifier (all `3^k − 1` signed sums) | instant |
| `controls.py` | full control battery (cyclic formula, `C_p^r`, MOS values, planted rejection, A≡B) | ~10 min |
| `sweep.py MAXN` | census over all abelian groups of order ≤ MAXN → `sweep.csv` | 192: ~30 min |
| `orbit_analysis.py p t` | extremal-set census, CRT profiles, Aut-orbit decomposition for `C₃⊕C_p²` | minutes |

## Reproduce the headline

```bash
cd conjectures/pm-davenport
gcc -O2 -o dpm_fast dpm_fast.c && gcc -O2 -o refute_brute refute_brute.c
./dpm_fast 5 15            # mu = 5, 85155 extremal, 139051 nodes
./refute_brute 6 5 15      # 0 dissociated 6-sets among 2324784
./dpm_fast 7 21            # mu = 7 (witness printed)
python3 controls.py        # everything checked against proved/known values
```

## Data

- `sweep.csv` — the census (group, `μ`, `t`, attained/deficient, census, nodes).
- `sweep_log.txt`, `heavies*.txt`, `controls_output.txt`, `orbits_*.txt` — run transcripts.
- `certs/` — witness files for the headline groups (verified by `verify_witness.py --file`).

## Known defects

- Runtimes recorded under CPU oversubscription (several engines sharing
  4 cores); treat them as upper bounds.
- `sweep.py` re-runs each group in two presentations for the invariance
  check; it does not deduplicate isomorphic invariant-factor inputs
  beyond that.
