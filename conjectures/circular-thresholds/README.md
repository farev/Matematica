# Circular repetition thresholds (Currie, Mol & Rampersad, 2019–2020)

A *circular word* of length `m` is a word read around a cycle; its factors are
the factors of `w^ω` of length at most `m`. Writing `RT(n)` for the ordinary
repetition threshold (`7/4` at `n = 3`, `7/5` at `n = 4`, `n/(n−1)` for
`n ≥ 5`), the question is how much harder it is to avoid repetitions
*cyclically* than in a line. Three thresholds arise, depending on whether one
asks for good circular words at infinitely many lengths (`CRT_W`), at all
large lengths (`CRT_I`), or at every length (`CRT_S`).

**Conjecture (Currie–Mol–Rampersad).** `CRT_I(n) = CRT_W(n) = RT(n)` for all
`n ≥ 4`. Known: `CRT_W(n) = RT(n)` for `n ≥ 45` (Mol–Rampersad,
arXiv:1912.11388). **Open: `CRT_W(n) = RT(n)` for `4 ≤ n ≤ 44`, and
`CRT_I(n) = RT(n)` for every `n ≥ 4`.** *(All of this is secondary-sourced —
see the sourcing note below.)*

The fault line this session pushed on: circular `α⁺`-freeness is *not* a
bounded-window condition, which is what stops the usual morphism machinery.
Widening the window by exactly two letters fixes that, and turns "infinitely
many lengths" into two finite searches.

**Status:** active
**Sessions:** [2026-08-03](../../log/2026-08-03-circular-thresholds.md)

> **Sourcing.** This session ran with egress blocked (HTTP 403 to every host,
> `arxiv.org` and `oeis.org` included). **No primary source was read.** Every
> statement about what is known or open is marked **(secondary)** in
> [`NOTE.md`](NOTE.md) and must be checked before publication. The
> mathematics is self-contained; the novelty claims are not.

## Results

| Claim | Label | Where |
|---|---|---|
| **Lemma A (circular pumping).** A `q`-uniform `α⁺`-free-preserving morphism maps `S_2(n,m)` into `S_2(n,qm)`, where `S_2` widens the factor window by 2. One morphism + one seed ⟹ circular threshold words at every length `q^j m_0` | **PROVED** | [`NOTE.md`](NOTE.md) §3 |
| **Theorem C.** A *decidable* sufficient criterion for `CRT_W(n) = RT(n)`: both hypotheses are finite searches | **PROVED** | [`NOTE.md`](NOTE.md) §6 |
| **Theorems M / M′.** Finite criteria for a uniform morphism to preserve `α⁺`-freeness (resp. to have an `α⁺`-free fixed point), with hypotheses (H1)(H2) chosen so the boundary loss vanishes | **PROVED** — but **expected to be a rediscovery** of known power-free-morphism tests | [`NOTE.md`](NOTE.md) §4–5 |
| **Proposition N.** A shift-equivariant uniform morphism over `Z_n` (`n ≥ 4`) with an `α⁺`-free fixed point has difference set of size `≤ 2` — vacuous at `n = 3`, severe above it. This is *why* the ansatz that works at `n = 3` cannot work at `n ≥ 4` | **PROVED** | [`NOTE.md`](NOTE.md) §8 |
| End-to-end instance: `CRT_W(3) = RT(3) = 7/4`, via a `q = 28` morphism and a length-20 seed, with the pumped words verified directly at lengths 20, 560, 15 680, 439 040 | **PROVED**, and a **known result** — reported only as a positive control | [`NOTE.md`](NOTE.md) §7 |
| Circular threshold spectra `C(n)` for `n = 3,4,5,6`: exact sets of realizable and exceptional lengths | **CERTIFIED** | [`NOTE.md`](NOTE.md) §2, `data/spec_n*.csv` |
| `n = 4` has **late** exceptional lengths `m = 147` and `m = 154`, after an unbroken run `114 … 146` — a finite sweep stopping early would have looked cofinite and been wrong | **CERTIFIED** | [`NOTE.md`](NOTE.md) §2, Result C3 |
| **Theorem N′.** For `4 ≤ n ≤ 9`, **no** shift-equivariant `q`-uniform morphism over `Z_n` has an `RT(n)⁺`-free fixed point, **for any `q`** — not "none was found", none exists. The normal form that works at `n = 3` is provably unavailable above it | **PROVED** (computer-assisted: two exhaustive finite searches) | [`NOTE.md`](NOTE.md) §8 |
| Result L: the longest `RT(n)⁺`-free word over `Σ_n` with only two distinct consecutive differences has length `11, 8, 14, 10, 18, 12` for `n = 4…9` | **CERTIFIED** (exhaustive) | [`NOTE.md`](NOTE.md) §8, `dcut.py` |
| The `n = 4` late gap at `m = 147` confirmed UNSAT by three independent SAT backends (Cadical 209 s, Glucose 343 s, MiniSat 207 s) | **CERTIFIED** | [`NOTE.md`](NOTE.md) §2 |

**Nothing here settles any open case of the conjecture, and nothing here
claims to.** What it does is reduce the open cases to a mechanical search in
the right normal form, and rule out the obvious normal form.

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `circspec.py` | exact SAT search for circular `α⁺`-free words, one instance per `(n,m)`; every witness re-verified by a from-the-definition `O(m³)` checker | ms to seconds per `m` | `data/spec_n*.csv`, the spectra |
| `pump.py` | independent re-check of (H1)–(H4) in Python; SAT search for `S_2` seeds; iterates a morphism and verifies each pumped word directly | seconds | the `n = 3` chain to length 439 040 |
| `dejean_morph.c` | exhaustive search over shift-equivariant `q`-uniform morphisms satisfying (H1)–(H4) | seconds to minutes per `q` | `data/morph_n*.log` |
| `dejean_fixpoint.c` | the same under the weaker fixed-point criterion (Theorem M′) | seconds per `q` | `data/fix_n*.log` |
| `dcut.py` | longest `RT(n)⁺`-free word whose consecutive differences lie in a 2-element set — step (iv) of Theorem N′ | ~1 min for `n ≤ 9` | `L(n) = 11, 8, 14, 10, 18, 12` |

Run from inside this directory:

```bash
cd conjectures/circular-thresholds
python3 -m pip install python-sat numpy
gcc -O3 -o dejean_morph dejean_morph.c
gcc -O3 -o dejean_fixpoint dejean_fixpoint.c

python3 circspec.py spectrum 5 1 300 --out data/spec_n5.csv   # the spectrum
python3 circspec.py spectrum 6 1 60 --alpha 4/3               # CRT_S calibration
./dejean_morph 3 2 30 7 4 3                                   # ternary morphisms
python3 pump.py morphcheck 3 0120212010201210120102120210     # (H1)-(H4)
python3 pump.py seed 3 20 --ext 2                             # an S_2 seed
python3 pump.py chain 3 0120212010201210120102120210 01202101210212012102
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/spec_n{3,4,5,6}.csv` | `circspec.py` | one row per length: realizable or not, and a witness word when realizable |
| `data/cal_n*_*.csv` | `circspec.py --alpha` | `CRT_S` calibration: all lengths `1…60` realizable at the four published constants |
| `data/morph_n*.log` | `dejean_morph` | candidate counts scanned and hits, per `q` |
| `data/fix_n*.log` | `dejean_fixpoint` | the same under Theorem M′, with the F2 filter counts |

## Known defects and open threads

- **UNSAT verdicts rest on SAT solvers, not on checked proofs.** No DRAT proof
  was emitted or checked. The load-bearing ones — the `n = 4` late gaps and
  their neighbours at `m = 113, 146, 147, 148, 153, 154, 155` — were re-decided
  by three independent backends (Cadical, Glucose, MiniSat) with identical
  verdicts, but the bulk of the sweep was decided once. Satisfiable verdicts
  are fully independent (witness + from-the-definition checker); unsatisfiable
  ones are not. This is the weakest link in the CERTIFIED claims.
- No primary source was readable this session; every attribution is
  `(secondary)` and needs checking. In particular the claim that
  `4 ≤ n ≤ 44` is open was seen only in a search summary.
- Sharpest thread: **run the Theorem C search in Pansiot's encoding of `n`-ary
  threshold words**, where the morphisms need not be shift-equivariant. One
  hit plus a seed settles an open case.
- Second thread: prove `L(n) < ∞` for every `n ≥ 4` (Result L is exhaustive
  only for `n ≤ 9`), which would make Theorem N′ unconditional in `n`.
- Third: push `n = 4` further. The late gaps at 147 and 154 are the most
  interesting numbers here; whether more follow is unknown.

## Prior work

Gorbunova (EJC 19(4), 2012) introduced the circular repetition threshold;
Currie–Mol–Rampersad (EJC 26(2), 2019, arXiv:1803.08145) settled
`CRT_S(4) = 3/2` and `CRT_S(5) = 4/3`, the last cases of Gorbunova's
conjecture; Mol–Rampersad (RAIRO-ITA 54, 2020, arXiv:1912.11388) proved
`CRT_W(n) = RT(n)` for `n ≥ 45` and stated the conjecture attacked here.
Dejean's conjecture (`RT(n) = n/(n−1)`, `n ≥ 5`) is due to Dejean, with the
last cases by Currie–Rampersad and Rao. Finite tests for power-free
morphisms are classical (Bean–Ehrenfeucht–McNulty; Crochemore;
Richomme–Wlazinski; Ochem). Pansiot's encoding of `n`-ary threshold words is
the normal form §8 points to. **All of these are cited from memory and search
summaries; none was read this session.** Theorem M in particular should be
treated as a rediscovery until checked.
