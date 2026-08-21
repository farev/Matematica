# Session writeup — 2026-08-21 (session 1)

The narrative, including what failed. NOTE.md has the results; this file
has the day.

## How the target was found

The mandate was external-first. The 08-18 session's slate had already
surfaced the plus–minus weighted Davenport constant `D±(C₅⊕C₁₅)` as a
runner-up — rejected that day only because its openness could not be
verified from the sandbox. Today's searches added a second secondary
snapshot (Marchan–Ordaz–Schmid determined `D±` "for all groups up to
order 100 except one") consistent with the first ("unknown already for
n = 3" in the `C₅⊕C₅ₙ` and `C₇⊕C₇ₙ` families). Two other external
candidates (k-Göbel integrality lengths; Gaussian moat beyond √36) were
vetted and rejected — the first for collision risk with an unreadable
Feb-2025 paper on exactly the planned computation, the second for
unpriceable cost. The internal thread (peaceable queens a(17), priced at
about an hour with a validated engine) was passed over on the mandate's
novelty default; the log records the argument.

## The reduction that made it computable

The observation that a ±-zero-sum-free sequence is exactly a
*dissociated set* (all `2^ℓ` subset sums distinct) turned each open
constant into a width-one window: `2^ℓ ≤ |G|` gives the cap
`⌊log₂|G|⌋`, direct sums of cyclic binary ladders give the floor. For
order 75 the window was `{5, 6}`, for order 147 `{6, 7}` — one
exhaustive search each. The suspicious part (recorded in the log the
moment it was noticed): if the order-75 case is a 2.3-million-subset
enumeration, why would it be open for a decade? Possible answers: the
zero-sum community states values via theorems and nobody published the
search; or the snippets are garbled and the value is known. The NOTE
carries the caveat prominently rather than pretending certainty.

## What was built

Two DFS engines (Python and C) over ±-classes with incremental
subset-sum bitsets, deliberately identical in traversal so node counts
must match exactly (they do, on every group tried: e.g. 136 463 at
`C₅⊕C₁₅`); a from-scratch brute-force verifier sharing no search logic;
orbit machinery for `Aut(G) = GL(2,p) × Aut(C₃)`; a census driver with
three cell classes (pinned / Theorem T3 / search). Controls before any
claim: Lemma E validated against the raw `{−1,0,+1}^ℓ` definition on
eight groups; cyclic and elementary-p formulas reproduced; a planted
non-dissociated set rejected; DFS vs brute force agreement on assorted
groups.

## The day's surprises

1. `C₅⊕C₁₅` and `C₇⊕C₂₁` resolved in *opposite directions* (75
   deficient, 147 attaining) — within an hour of engine-complete.
2. The 147 extremal set is unique up to automorphism: the exhaustive
   count (2016) matched the orbit size on the nose. At 75, by contrast,
   85 155 maximum sets in 193 orbits, none extendable.
3. The census (493 groups, 40 s) found only nine deficient groups below
   256 — and they refuse every simple invariant tried: attainment is not
   monotone in packing density (`C₃⊕C₅⊕C₉` fails at 0.948 while
   `C₇⊕C₂₁` attains at 0.871); two groups (`C₃³⊕C₅`, `C₂⊕C₃⁴`) have
   *neither* bound tight; the 147 witness beats every per-Sylow
   construction.
4. The `C₇²` family keeps attaining in its windows (147, then 441 after
   a 740M-node search); the `C₅²` family keeps failing (75, then 275
   after a 3.49G-node, 25.6-minute exhaustion). No explanation yet.

## What failed

- **First controls run hung**: `C₃⁵` was placed in the Python control
  suite, whose full exhaustion (~10⁹ nodes) is C-engine territory; the
  suite was re-scoped to `r ≤ 4` and `C₃⁵` later verified in C
  (131 590 491 nodes).
- **verify_75.c had an off-by-one in its verdict message** (`D± = 7`
  instead of 6): the computation (zero 6-sets among 2 324 784) was
  right, the label wrong. Caught immediately against the DFS engines'
  output; fixed before any claim left the directory. A reminder that
  the weakest part of a verifier is its print statement.
- **The 256–330 census sweep crashed** on order 258: pinned-cell
  verification by DFS witness search is not cheap at packing density
  0.992 (the witness is essentially the cyclic binary ladder, which
  index-ascending DFS reaches only after deep backtracking). Fixed
  properly: pinned cells now verify by *constructing* the product
  witness from the optimal regrouping and checking it at definition
  level. The ≤ 255 census was re-run under the new scheme (canonical
  CSV); the old run's search-verification of all 447 pinned cells
  stands as an extra validation layer in git history.
- **A first "family closed for all p" claim was wrong**: the sandwich
  argument for `C_p⊕C_{3p}` does not pin `p = 19, 29, 31, 37, …`
  (window primes, `p/2^{⌊log₂ p⌋}` in two critical intervals). Caught
  by re-deriving the arithmetic carefully before writing the NOTE;
  Corollary F now claims exactly `p ≤ 17` plus the pinned residues.
- **Background-job hygiene**, again (the 08-13 and 08-17 logs both
  warned): one run launched with a relative path from the wrong working
  directory (exit 127), one launched with shell `&` whose survival then
  had to be confirmed by hand. No results were lost, but both cost
  minutes.

## Judgement calls

- The headline claims stay CERTIFIED, not PROVED, even though three
  independent programs agree — the certificates are search logs plus
  witnesses, not human-checkable arguments. NOTE §4 Q4 sketches the
  case analysis that could upgrade order 75 to PROVED; it was not
  completed today.
- `C₁₉⊕C₅₇` (the first open window prime, order 1083) got a witness
  hunt launched mid-session rather than an exhaustion: if it attains,
  cheap; if it is deficient, the exhaustion is beyond today's budget
  and honesty requires "open", not a half-run.
- OEIS-adjacent packaging (a sequence `ℓ_max` over group orders) was
  considered and deferred: the natural index is the group, not the
  order, and the primary sources must be read first.
