# Undirected repetition thresholds (Currie–Mol, 2019–2021)

An *undirected `r`-power* is a word `x y x′` with `x′ ∈ {x, xᴿ}` and
`|xyx′|/|xy| = r`; `URT(k)` is the infimum of the `r` such that undirected
`r`-powers are avoidable over `k` letters.

**Conjecture (Currie–Mol).** `URT(k) = (k−1)/(k−2)` for all `k ≥ 4`.
Proved `≥` for all `k ≥ 4`; confirmed with equality for `4 ≤ k ≤ 21`;
open for every `k ≥ 22`. *(secondary — this session ran with primary
sources unreadable; see NOTE §1)*

**Status:** active — `k = 22` attacked, not settled; certified two-sided
structure at the threshold, ansatz exclusions, and a proved descent
criterion for future construction attempts.
**Sessions:** [2026-08-18](../../log/2026-08-18-undirected-thresholds.md)

## Results

| Claim | Label | Where |
|---|---|---|
| **Theorem T1.** For every `n ≥ 5`, the maximal length of a word over `Σ_n` with no undirected exponent `≥ (n−1)/(n−2)` is exactly **`n+3`**, with unique extremal word `0 1 ⋯ (n−2) 0 (n−1) 1 3` — hence `URT(n) ≥ (n−1)/(n−2)` for all `n ≥ 5` by an elementary self-contained proof (the bound is Currie–Mol's (secondary); the sharp length and uniqueness look new (secondary)) | **PROVED** | NOTE §4, `case_tree.py` |
| Exhaustive certificates of the same at `k = 22, 23, 24, 25` (451/483/516/550-node trees), found before the proof and corroborating it | **CERTIFIED** | NOTE §4, `lower_bounds.py` |
| U-`(21/20)⁺`-free words over `Σ_22` of length **20 000** exist (lex-least canonical witness; 4 independent checkers); length 5 000 for `k = 23, 24, 25`; 1 606 755 canonical words at length 55 | **CERTIFIED** | NOTE §5, `certify_witness.py`, `data/witness_*` |
| The binary Pansiot class (gaps `≥ n−1`) is **empty** at `α = (n−1)/(n−2)` for `n = 20..23`: max 4 code bits — threshold witnesses must use distance-`(n−2)` recurrences | **CERTIFIED** (+ PROVED micro-lemmas) | NOTE §6, `code_class.py` |
| Local structure: gap `≥ n−2`; no palindromic factor of length ≥ 2; reversed adjacent pairs `ab…ba` need distance ≥ 40 (at `n = 22`); no eventually periodic witness | **PROVED** | NOTE §2 |
| Reversal transfer in the binary Pansiot code: `rτ_b r = τ_b^{−1}`, `code(wᴿ) = code(w)ᴿ`, `g(Vᴿ) = r·g(V)^{−1}·r`, anti-gid correspondence | **PROVED** (R4 sketch-level) | NOTE §7 |
| **Theorem D**: a finite-check descent criterion — sync + reversal-exclusion + short-factor check ⟹ U-freeness of any `k`-uniform-morphic fixed point | **PROVED** | NOTE §8 |
| The affine ansatz `φ(x) = m·x + B₀` is empty at `k = 22, 23, 24` for all ten units `m` (and `m = 1` at further `k ≤ 36`, see scan logs); general uniform-morphic search inconclusive (forcing wall at depth `20k`) | **CERTIFIED** (stated ranges) | NOTE §8, `affine_search.py`, `selfsim_search.py` |

(The interim "Conjecture C3" of this session was upgraded to Theorem T1
the same day.)

## Scripts

| file | what it does | cost |
|---|---|---|
| `urt.py` | exact undirected-freeness checkers (4 independent impls, strict + non-strict), Pansiot code, monodromy | — |
| `tests_urt.py` | full control suite (checker agreement, pansiot.py cross-check, reversal identities, language facts) | 30 s |
| `lower_bounds.py` | Result C1 certificates (k = 22..25) | 1 s |
| `case_tree.py` | Theorem T1 corroboration: identical parametric case tree, n ∈ {5..31, 40, 60, 100} | 4 min |
| `code_class.py` | Result C6 certificates (n = 20..23) | 1 s |
| `certify_witness.py <k> <L>` | lex-least witness of length L + 4-checker verification | 80 s at L = 20 000 |
| `letterdfs.py <n> <num> <den> <depth>` | canonical language DFS (counts, death detection) | varies |
| `affine_search.py <kmin> <kmax> <depth>` | exhaustive affine-ansatz search (GF(2)×GF(11) elimination) | ~1–2 min/k |
| `selfsim_search.py` | general uniform-morphic self-similar search | capped runs |
| `probe.py`, `lazy_additive.py`, `enumerate_lang.py`, `scan_affine.py` | probes, offline additive scan, code-language counts, scan driver | varies |

Run everything from inside this directory. `python3 tests_urt.py` first.

## Known defects / caveats

- Everything literature-facing is **(secondary)**: the session could not
  read Currie–Mol's papers; the URT definition conventions were taken from
  search snippets. Verify against the primary sources before publication.
- Theorem D and the §7 identities are one-session-old proofs, machine-
  spot-checked but not independently verified.
- `selfsim_search.py` runs are node-capped, not exhausted: the general
  uniform-morphic ansatz at `k = 21, 22` is **not** excluded.
- The affine scans beyond the stated ranges (`m = 1, k = 44, 52`; `m ≠ 1,
  k ≥ 24`) hit caps or were not run to exhaustion; see the scan logs.
