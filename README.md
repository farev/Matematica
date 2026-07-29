# Matematica

Daily attempts at open problems in mathematics.

Every day I pick an unsolved conjecture — or an open thread in a recent paper —
and spend a session on it. Most days produce nothing but a record of what
failed. Occasionally a session produces something real: a new exact constant, a
sharpened inequality, an empirical law, or an audit of someone else's recent
work. Everything goes in this repository, successes and dead ends alike.

The failures are the point as much as the results. A research log that only
shows the wins is not a research log.

## Status vocabulary

Every claim in this repository carries exactly one of three labels. This is the
most important convention here, and it is not negotiable.

| Label | Meaning |
|---|---|
| **PROVED** | A theorem with a written proof. Holds for all cases in its stated scope. |
| **CERTIFIED** | An exact computation — rational or integer arithmetic, no floating point in the critical path — that is reproducible and ships a verifiable certificate. True for the range computed, not beyond. |
| **NUMERICAL** | Monte Carlo, curve fits, heuristics, floating-point exploration. Evidence, not proof. May be wrong. |

A computation is never described as a proof. "Verified for all rows up to
455,052,510" is a CERTIFIED statement; it is not evidence that the conjecture is
true, only that no counterexample lives below that bound.

## Conjectures

| Conjecture | Status | Headline |
|---|---|---|
| [Gilbreath's conjecture](conjectures/gilbreath/) | active | Sharpened the Chase–Hunter–Tao lower bound by a factor of 2; computed the first new exact constants c₄, c₅, c₆ of their continuous model |

### Gilbreath's conjecture (Proth 1878, Gilbreath 1958)

Write the primes in a row and repeatedly take absolute differences of adjacent
entries. The conjecture: every row after the first begins with 1. Open.

Session of 2026-07-28 — full account in
[`WRITEUP.md`](conjectures/gilbreath/WRITEUP.md), research note in
[`NOTE.md`](conjectures/gilbreath/NOTE.md):

- **PROVED** — `c_n ≥ 2·exp(−Σ_{k<n} c_k)` for `n ≥ 2`, a factor-2 sharpening
  of Chase–Hunter–Tao Proposition 2.1, giving `Σ_{i≤n} c_i ≥ log(2n − 2 + e²)`
  and improving their Theorem 1.4 by an additive `log 2`.
- **PROVED** — the sign arrangement of the continuous model realises all
  `2^{i(i+1)/2}` chambers: every sign history occurs.
- **CERTIFIED** — exact rational values of `c₄`, `c₅`, `c₆`, extending the
  `c₀…c₃` of Chase–Hunter–Tao, each with a partition-of-unity certificate in ℚ.
  `c₆` is a 153-digit over 154-digit fraction.
- **CERTIFIED** — Gilbreath's conjecture holds for the first 455,052,510 rows
  (primes below 10¹⁰), via Odlyzko's propagation criterion.
- **NUMERICAL** — a *submask law* `c_i ≈ C·i^{−α}·Σ_{m ⊆ i} q^m` with
  `α ≈ 0.80`, `q ≈ 0.685`: `R² = 0.98` in-sample, and `R² = 0.90` as a pure
  out-of-sample prediction on `i ∈ [1024, 4095]` from parameters fitted only on
  `i ∈ [64, 1023]`. This contradicts a pure `c_i ≍ 1/i` decay in the accessible
  range.

An OEIS submission draft for the `c_i` numerators and denominators is in
[`oeis_draft.txt`](conjectures/gilbreath/oeis_draft.txt).

## Layout

```
conjectures/<name>/   one directory per conjecture, self-contained
log/                  daily entries, YYYY-MM-DD-<conjecture>.md
tools/                utilities shared across conjectures
```

Each conjecture directory holds its own README, research note, writeup, code,
data and certificates. They are deliberately self-contained so any one of them
can be split out later with `git subtree split` if it grows into its own paper
or package.

## Running things

```bash
python3 -m pip install -e .
```

Requires Python 3.11+, NumPy and SciPy. Developed on Python 3.12.6 with
NumPy 2.3.5 and SciPy 1.17.0.

Scripts read and write data files by relative name, so **run them from inside
their own conjecture directory**:

```bash
cd conjectures/gilbreath && python3 verify.py 1e6
```

Each conjecture's README lists what every script does and roughly what it costs
to run. Some are seconds; the 10¹⁰ verification needs ~3 GB of RAM, and the
exact `c₆` computation took 11 minutes across 11 cores.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Corrections are especially welcome — if
something here is wrong, or rediscovers known work without saying so, please
open an issue.

## On AI assistance

These sessions are run with substantial AI assistance (Claude). This is
disclosed here, in each research note, and in any preprint that comes out of
this work. AI systems are not listed as authors, consistent with COPE guidance
and publisher policy. Every proof is checked by hand; every computational claim
ships code you can rerun.

## License

Code is [MIT](LICENSE-CODE). Prose, research notes and writeups are
[CC BY 4.0](LICENSE-PROSE) — compatible with the arXiv distribution license.
