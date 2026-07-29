# tools

Utilities shared across conjectures.

Nothing lives here yet. The first candidates, once a second conjecture needs
them, are the pieces already written for Gilbreath:

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
