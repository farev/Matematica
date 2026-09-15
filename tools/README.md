# tools

Utilities shared across conjectures.

- [`build_index.py`](build_index.py) — emits the repo-root `ATTEMPTED.md`, the
  one-line-per-problem index a session reads instead of sweeping every
  conjecture README and log entry (about 1k tokens against 166k). Covers
  unmerged `claude/*` branches, so problems attacked on a branch that never
  landed still show as taken. Run it from the repository root after a merge.
  Its `ALIASES` map is hand-maintained: add an entry whenever one problem
  turns up under a second directory name.

- [`satcert/`](satcert/) — certified-UNSAT toolkit: a from-the-definition
  DRUP proof checker, an independent coloring-witness verifier, and a
  bisection driver for exact Rado/Schur-type numbers. Built and validated
  2026-08-05 (see its README for the validation record); not yet used by a
  shipped result — it exists so future SAT verdicts can ship checked proofs
  instead of the 2026-08-03 session's cross-solver defect.

Other candidates, once a second conjecture needs them, are the pieces
already written for Gilbreath:

- **segmented sieve** — `conjectures/gilbreath/verify.py:primes_up_to`, plus the
  segmented variant in `verify_big.py` that reaches 10¹⁰ in about 3 GB.
- **exact rational linear algebra** — `ck_exact.py` carries a Bareiss
  determinant, primitive-vector normalisation and Delaunay ray construction over
  ℚ. Genuinely reusable for any cone-decomposition computation.
- **certification harness** — the partition-of-unity check in
  `ck_exact_certified.py`: verify that chamber measures sum to exactly 1 in ℚ
  before reporting a constant as CERTIFIED.

The rule from [CLAUDE.md](../CLAUDE.md): conjecture directories never import
from each other. When two of them need the same code, it moves here and both
import from `tools/`. Until then, duplication is preferable to coupling — each
conjecture directory has to survive `git subtree split` on its own.
