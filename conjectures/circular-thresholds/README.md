# Circular repetition thresholds (Currie, Mol & Rampersad, 2019–2020)

A *circular word* of length `m` is a word read around a cycle; its factors are
the factors of `w^ω` of length at most `m`. Writing `RT(n)` for the ordinary
repetition threshold (`7/4` at `n = 3`, `7/5` at `n = 4`, `n/(n−1)` for
`n ≥ 5`), the question is how much harder it is to avoid repetitions
*cyclically* than in a line.

**Conjecture (Currie–Mol–Rampersad).** `CRT_I(n) = CRT_W(n) = RT(n)` for all
`n ≥ 4`. Known before this log: `CRT_W(n) = RT(n)` for `n ≥ 45`
(Mol–Rampersad, arXiv:1912.11388). *(secondary — see sourcing note)*

**Status:** active — **the weak case `n = 6` is settled here (session 2),
and `n = 5` too (possible overlap with Tunev 2025, see below)**
**Sessions:** [2026-08-03](../../log/2026-08-03-circular-thresholds.md),
[2026-08-06](../../log/2026-08-06-circular-thresholds.md)
**Write-up page:** [fabianarevalo.com/circular-thresholds](https://fabianarevalo.com/circular-thresholds)

> **Sourcing.** Both sessions ran with egress blocked (HTTP 403 everywhere;
> search snippets only). **No primary source has been read.** Every
> "known/open" statement is **(secondary)** and must be checked before
> publication — in particular against **Tunev, arXiv:2512.24581 (Dec 2025,
> Russian)**, discovered during session 2, which reportedly constructs
> circular threshold words for *some odd* `n ≥ 5` (it cannot cover the even
> case `n = 6`).

## Results

| Claim | Label | Where |
|---|---|---|
| **Theorem P6 (session 2).** `C(6) ⊇ {39·21^j}`: circular `6/5⁺`-free words of length `39·21^j` for every `j` — hence **`CRT_W(6) = RT(6) = 6/5`**, an open case of the conjecture settled (openness (secondary)) | **PROVED** | [`NOTE.md`](NOTE.md) §15.1 |
| **Theorem P5 (session 2).** `C(5) ⊇ {28·21^j}` — hence **`CRT_W(5) = RT(5) = 5/4`** (odd case: plausibly rediscovers Tunev-type results) | **PROVED** | [`NOTE.md`](NOTE.md) §15.2 |
| **Lemmas S, F, T; Theorem MC; Lemma PC; Theorem C-code (session 2).** Pansiot-code machinery: exact repetition transfer between a word and its codeword monodromy structure; a finite certificate that a uniform binary code morphism preserves code-freeness; circular pumping in the code | **PROVED** | [`NOTE.md`](NOTE.md) §11–§14 |
| Result P3′ (session 2): the same machinery re-derives `CRT_W(3) = 7/4` with `k = 19` binary generators | **PROVED** — known result, control | [`NOTE.md`](NOTE.md) §15.3 |
| **Result N2 (session 2).** `n = 4`: the whole code ansatz is empty — no viable pair over all pooled monodromy classes for `k ≤ 46`, none in the two-level engine ranges, with per-pair explicit refutations | **CERTIFIED** (stated ranges) | [`NOTE.md`](NOTE.md) §17 |
| Lemma A (circular pumping on `Σ_n`), Theorem C, Theorems M/M′, Proposition N, Theorem N′ (session 1) | **PROVED** (M/M′ expected rediscoveries) | [`NOTE.md`](NOTE.md) §3–§8 |
| Circular threshold spectra `C(n)`, `n = 3,4,5,6`; the `n = 4` late gaps at `m = 147, 154`; three-solver cross-check | **CERTIFIED** | [`NOTE.md`](NOTE.md) §2 |

`CRT_W(4)` remains open — sharpened by N2. `CRT_I(n)` untouched for all
`n ≥ 4`.

## Scripts

| file | what it does | cost |
|---|---|---|
| `pansiot.py` | session-2 library: code/decode, monodromy, exact freeness checkers, circular verifier (conventions in the docstring) | — |
| `pansiot_search.py <n> <kmin> <kmax>` | exhaustive letterwise sweep over monodromy-pooled block pairs with fixed-point filtering | seconds–minutes per `k` |
| `pansiot_certify.py <n> <phi0> <phi1>` | checks (Ha)(Hb)(Hc)(C2)(Hd) of Theorem MC, exact arithmetic | seconds–minutes |
| `pansiot_seed.py check/encode/pump …` | seed conditions (M)(S2); Pansiot-encoding of witnesses; pump-and-verify directly from Definition 1 | seconds–minutes |
| `circspec.py`, `pump.py`, `dejean_morph.c`, `dejean_fixpoint.c`, `dcut.py`, `crosscheck.py` | session-1 tools (see git history for that README) | as before |

Reproduce the `n = 6` theorem end to end:

```bash
cd conjectures/circular-thresholds
python3 pansiot_certify.py 6 010101101101011010110 101011010110110101101
python3 pansiot_seed.py check 6 101011011010110101101101011010110110101
python3 pansiot_seed.py pump 6 010101101101011010110 101011010110110101101 \
        101011011010110101101101011010110110101 2
```

## Data and certificates

| file | what it is |
|---|---|
| `data/pansiot_certified.txt` | all certified morphism pairs + seeds + verification tables |
| `data/pansiot_sweep_n{3,4,5,6,8}.log` | full sweep transcripts (the `n = 4` zeros are the Result N2 certificate) |
| `data/pansiot_engine_n4_{a,b}.log`, `data/pansiot_preservation_n4.log` | two-level engine and preservation-filter negatives |
| `data/spec_n*.csv`, `data/cal_n*`, `data/morph_n*`, `data/fix_n*`, `data/crosssolver_n4.log` | session-1 spectra and certificates |

## Known defects and open threads

- **Session-2 proofs are one-session-old.** Lemma T / Theorem MC / Lemma PC
  were derived, written and machine-instantiated in a single day; the `n = 3`
  control re-derives a known theorem through them, but no independent human
  or formal check exists yet. This is the main trust bottleneck.
- **Tunev must be read** (arXiv:2512.24581, Russian) before any novelty claim
  for `n = 5`; the session-1 "open for `4 ≤ n ≤ 44`" line is doubtful for
  some odd `n`.
- `n = 8`: 44 fixed-point-viable pairs at `k = 28`, none satisfying the MC
  hypotheses (mostly (Ha)/(Hb)); a synchronization-based criterion without
  first/last-bit injectivity would likely unlock `n = 8, 10, …`.
- Session-1 defects stand (UNSAT verdicts single-solver for the bulk of the
  spectra; DRAT proofs not emitted).
