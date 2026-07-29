# Contributing

This is a personal research log, but corrections and collaboration are welcome.

## The most valuable contribution is a correction

If something here is wrong, please open an issue. Specifically:

- **A proof has a gap.** Point at the step. This is the single most useful
  thing you can do.
- **A result is already known.** Give the reference. Rediscovery is a normal
  part of research and gets recorded as such — but only if I find out.
- **A computation does not reproduce.** Tell me your platform, versions and
  what you got. Exact computations should be bit-identical; Monte Carlo results
  should agree within the stated standard error.
- **A citation is misstated.** Especially important where this repository
  characterises someone else's recent paper.

## Claim labels

Every result here is labelled **PROVED**, **CERTIFIED**, or **NUMERICAL** —
see [CLAUDE.md](CLAUDE.md) for exact definitions. If you contribute a result,
label it, and pick the weakest label that honestly applies. A mislabelled
claim is worse than no claim.

## Code

- Python 3.11+, NumPy, SciPy. `pip install -e ".[dev]"` for the dev extras.
- Scripts run from inside their own conjecture directory — they read and write
  data files by relative name.
- Exact computations use rational or integer arithmetic in the critical path
  and emit a certificate that can be checked independently.
- Anything expensive records its runtime, core count, RAM and seed.

## Adding a conjecture

Copy `conjectures/TEMPLATE.md` to `conjectures/<name>/README.md` and fill it
in. Keep the directory self-contained: it should survive being split into its
own repository without edits.

## Formalization

Machine-checked proofs are very welcome. If you formalize any of the elementary
lemmas here in Lean 4 / mathlib, that supersedes the informal proof and I will
say so prominently.

## On AI assistance

This work is produced with substantial AI assistance, disclosed throughout.
That makes independent human verification more valuable, not less. If you check
something here carefully — and especially if you find it wanting — that is a
real contribution and will be credited.
