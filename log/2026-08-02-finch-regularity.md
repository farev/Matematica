# 2026-08-02 — Finch's regularity conjecture for 1-additive sequences

**Target.** New cases of Finch's conjecture on which 1-additive (Ulam-type)
sequences `U(a,b)` are regular. It looked tractable because of one mechanical
fact: if `U(a,b)` has finitely many even elements `E`, then for odd `x` any
representation `x = u+v` has exactly one even summand, so `x ∈ U` iff
`#{e ∈ E : x−e ∈ U} = 1` — which reads only a bounded window below `x`. A
bounded window is a finite automaton, and a repeated automaton state *proves*
periodicity forever after. That makes the whole question a finite, exactly
checkable certificate rather than an open-ended search.

**Result.**

- **PROVED** — Theorem 1: three finite conditions (P) periodicity of the window
  state, (C) a residue-cover condition mod the period, (F) a finite check on
  even numbers below an explicit bound `B = 2X₁+4P+2W+4` — together imply that
  `U(a,b)` is regular, that its even set is exactly `E`, and that its
  fundamental difference is exactly `P`. The reduction is self-correcting: it
  cannot be satisfied with an incomplete even set.
- **CERTIFIED** — regularity of **32 sequences**, each with an exact
  certificate, **20 of them in cases the literature reports as open**:
  `U(4,b)` for `b ≡ 3 (mod 4)`, `b ∈ {7,11,19,23,27,35,39,43}`; `U(6,7)`,
  `U(6,11)`; `U(8,9)`, `U(8,11)`; `U(10,11)`, `U(10,13)`, `U(10,17)`;
  `U(12,13)`, `U(12,17)`; `U(14,15)`; `U(16,17)`; `U(18,19)`. The remaining 12
  reproduce Cassaigne–Finch (`a=4`, `b ≡ 1 mod 4`) and were kept as controls.
- **CERTIFIED** — an exceptional family. For all 255 odd `b` with `5 ≤ b ≤ 513`
  (no gaps), the even elements of `U(4,b)` below `6b²+4000` are exactly
  `{4, 2b+4, 4b+4}` — except for the seven values `b = 2^k−1`, `k = 3..9`, where
  exactly one more appears, always equal to **`4b² + 2b − 4`**
  (206, 926, 3902, 15998, 64766, 260606, 1045502). For `b = 7` the certificate
  closes this absolutely: `U(4,7)` has exactly four even elements and no more.
  Every `2^k−1` is `≡ 3 (mod 4)` — the residue class Cassaigne–Finch omit — and
  their argument is reported to run through "precisely three even terms", which
  is exactly what fails here.
- **CERTIFIED / conjectural** — the 2-adic period law
  `P(4,b) = 2^{⌊log₂(b−1)⌋+3}(b+1)`, exact for all twelve tested `b ≡ 1 (mod 4)`
  (`5 ≤ b ≤ 49`) and also for `b = 19`; every other tested `b ≡ 3 (mod 4)` has a
  period carrying a large prime factor (e.g. `P(4,23) = 2·14929`,
  `P(4,39) = 2²·3·11·4703`). The individual periods are exact; the *law* is a
  pattern over a tested range, not a theorem.

`U(4,7)`'s fundamental difference is `P = 11,301,098` — about 5000× that of any
neighbouring `U(4,b)` with `b ≤ 49`. The exceptional family is quantitatively
as well as structurally different.

Two independently written implementations of Theorem 1 exist: `certify.py`
(hash-table cycle detection) and `verify_cert.c` (Brent, O(1) memory, written
from the theorem rather than ported). The C one produced all 32 rows; the Python
one independently reproduced **23** of them and agrees with the C one on `E`,
`P` and `|R|` on every one of those 23. The other nine rows rest on the C
verifier alone — the Python implementation's memory grows with the period and
could not reach them — which is a real asymmetry in the evidence and is recorded
as a defect in the conjecture README.

**Connectivity check.** Run first, per the mandate, and it failed. `arxiv.org`,
`oeis.org`, `erdosproblems.com`, `mathoverflow.net`, plus `en.wikipedia.org`,
`semanticscholar.org`, `doi.org`, `zbmath.org`, `link.springer.com` — **all
refused with HTTP 403 on CONNECT** at the egress proxy, which logged each as
`connect_rejected: gateway answered 403 (policy denial or upstream failure)`.
Only `api.github.com` and `raw.githubusercontent.com` were reachable, and GitHub
access is scoped to this repository, so the GitHub mirrors of the Erdős database
(`teorth/erdosproblems`) and `google-deepmind/formal-conjectures` were refused
too. WebSearch works (it runs outside the sandbox) and was the only literature
channel. **Consequence: no primary source was read this session. Every citation
in the conjecture directory is marked (secondary), and every "this is still
open" claim is unverified.** This is the single biggest caveat on the session
and it is repeated at the top of the conjecture README.

**Three-candidate slate (external).**

1. **Wilf's conjecture** (numerical semigroups; commutative algebra / additive
   NT). `e·n ≥ c` for every numerical semigroup. Source: search summaries of
   Delgado–Eliahou–Fromentin arXiv:2310.07742 (J. Algebra 2025) and Delgado's
   survey arXiv:1902.03461, checked 2026-08-02 (secondary). Open: every source
   through Bacher arXiv:2604.25051 (Apr 2026) treats it as open; verified by
   computer to genus 100, and to 120 when `m | c`.
2. **Cap sets in AG(n,3)** (extremal combinatorics / finite geometry). Maximum
   size `a_n` of a subset of `F_3^n` with no three collinear points. Sources:
   summaries of Potechin (Des. Codes Cryptogr. 2008, `a₆=112`), FunSearch
   (*Nature* 624, 2023, `a₈ ≥ 512`), Thackeray arXiv:2206.09804, checked
   2026-08-02 (secondary). Open: exact values known only for `n ≤ 6`;
   `a₇ ∈ [236, 288 or 291]`.
3. **Lonely Runner Conjecture** (Diophantine approximation / view obstruction).
   For `n` runners with distinct integer speeds, each is at some time `≥ 1/n`
   from all others. Sources: summaries of Perarnau–Serra survey arXiv:2409.20160
   (Computer Science Review 58, 2025), Rosenfeld arXiv:2509.14111,
   Sungkawichai–Trakulthongchai arXiv:2604.23906, checked 2026-08-02
   (secondary). Open: from 14 runners upward.

**Internal-thread assessment.** The strongest live internal thread is
additive-squares: close the search tree for the 3-term-AP relation class
`v = (1,1,0)`, where a sweep plateaued at 440 and an independent randomised
probe with a 66× larger depth cap plateaued at 437. Significant progress would
be a second Freedman-type finiteness theorem, which would change that row of the
top-level README. It is concrete and it is a computation, not a hope. But it
extends an existing repo result rather than opening a new problem, its outcome
is binary and might well have been "still running at the depth cap", and the
mandate's default is external. Not chosen; ties go to the new problem.

**Selection argument.** All three external candidates failed criterion (a) — is
the bottleneck breakable by a few cores in a few hours? Lonely Runner: the
frontier moved from 7 runners to 13 between September 2025 and April 2026, with
a group shipping every two months and single prime checks costing tens of hours;
four cores is not competitive. Cap sets: `a₇ ≥ 236` has not moved since 1994 and
`a₈ ≥ 512` not since 2023, through FunSearch, AlphaEvolve, PatternBoost and
X-evolve; that record table is not falling to 4 cores. Wilf: the bottleneck is
an idea, and decisively so — at depth 4 the standard `W₀(S) ≥ 0` method
*provably* cannot work, since near-misses with `W₀ = −1` exist there with
arbitrarily large embedding dimension. Finch's conjecture beat all four on (a)
because of the automaton reduction, which converts compute into proof rather
than into evidence; on (b) because the exact `(a,b)` pairs attempted are
enumerable and the certificate is self-checking, so a rediscovery would be
visible rather than silent; and on (c) because a result extends
Cassaigne–Finch (1995) and Schmerl–Spiegel (1994) directly, in the precise
residue class Cassaigne–Finch left out.

**What failed.**

- *Condition (C) written as "≥ 2 representations".* Wrong: the requirement is
  "≠ 1", and an even residue class with **zero** forced representations is
  perfectly acceptable. `U(4,5)` and `U(4,9)` failed spuriously on classes
  12, 20, 164 mod 192 until this was fixed. I initially looked for an arithmetic
  bug that was not there.
- *Trusting the first sweep horizon.* At `N = 10⁴` the exceptional family looked
  like `{7,15,31}`. `b = 63`'s extra element is at 15998, above that horizon, so
  the scan was silently truncating. Only rerunning every `b` out to `6b²+4000`
  gave the real answer. The `N = 10⁴` "finite-looking" verdicts for `a ≥ 22`
  in the first landscape sweep are similarly untrustworthy and were not used.
- *Hash-table cycle detection.* Storing every window state costs memory
  proportional to the period and could not reach `U(4,7)` (`P = 11,301,098`).
  Replaced by Brent's algorithm, O(1) memory, which certified it.
- *`U(4,15)`, `U(4,31)`, `U(4,63)` not certified.* For `U(4,15)` and `U(4,31)`
  Brent's algorithm closed no cycle within `1.5·10⁹` automaton steps, so
  `max(preperiod, period) > 1.5·10⁹` for both — against periods in the thousands
  for neighbouring `b`. Windows are `~4b²` bits wide. Still unknown whether the
  periods are enormous or the transients merely long: `U(4,35)` has
  `X₁ = 1,666,723` with period only 5326, so long transients do occur.
- *`U(20,21)` and several `b ≡ 3 (mod 4)` cases* hit the memory cap on `B` or
  the Brent step cap. Resource limits, not obstructions.
- *The clean story is wrong.* "`b ≡ 1 (mod 4)` smooth, `b ≡ 3 (mod 4)` wild"
  fails at `b = 19`, which obeys the 2-adic law despite being `≡ 3`. The real
  dichotomy is something else and I do not know what.

**Next.** Sharpest thread: **prove Conjecture A** — that `U(4,b)` has a fourth
even element iff `b = 2^k − 1`, of value `4b²+2b−4`. The two handles are the
identity `4b²+2b−4 = b(4b+4) − (2b+4)` (the new element is `b` times the largest
generic even element minus the middle one) and the 2-adic period law, in which
`b = 2^k−1` is exactly the case where `b+1` is a pure power of 2 and the law
degenerates. With Conjecture A in hand, a version of Theorem 1 made uniform in
`b` would settle the whole Cassaigne–Finch gap `b ≡ 3 (mod 4)`, which is the
actual prize. Second, and cheap the moment there is a network: read
`oeis.org/FinchSadd.html` — Finch's own table of cases, periods and fundamental
differences — since Conjecture A and the period law may already be sitting
there, and verify the four secondary citations. Third: certify `U(4,15)` and
`U(4,31)`, whose cycles survived `1.5·10⁹` steps unclosed — settling whether the
exceptional family's periods grow like `b²` or far faster.
