# Session write-up — 2026-08-18, undirected repetition thresholds

The narrative, including everything that failed. The polished statements
live in `NOTE.md`; this file is the honest order of events.

## Why this problem

Survey (log, §candidate slate): three external candidates across three
subfields; URT(22) chosen because the bottleneck looked like search plus
two provable lemmas, the openness trail was clean through 2024, and the
repository owns adjacent machinery (circular-thresholds' Pansiot-code
certificates). The plan at selection time: extend the repo's binary
Pansiot machinery with a reversal-aware transfer lemma and preservation
criterion, then search for a certified morphism pair at `n = 22`.

## Act I: the binary plan, and its collapse

Built the exact undirected-freeness checkers first (four independent
implementations before any search — this paid off all day), the control
suite, and the reversal identities in code space (`NOTE §7`): reversal of
an in-class word is bit-reversal of its code, states reverse through
`r`-conjugation, `g(Vᴿ) = r g(V)^{−1} r`. The morphism-search plan was
palindromic block pairs (`rev(φ_b) = φ_b`), for which parity forces odd
`k`, mid-bits 0/1, and (C2) forces the conjugator to commute with `r` —
all derived and ready.

Then the floor vanished: enumerating U-code-free binary words at `n = 22`
gave 2, 3, 3, 1, 0 words at lengths 1..5. **The entire binary class is
empty beyond four bits.** The mechanism: `00` forces exponent `23/21`,
`111` forces `24/22`, and the survivors die on reversed adjacent pairs
(`ab … ba` within distance 39, forbidden by Lemma L3) that the rigid
distance-21 recurrences cannot avoid. Checked at `n = 20, 21, 23` too:
empty everywhere — including alphabets where Currie–Mol *proved* witnesses
exist. So threshold witnesses simply do not live in the rainbow-window
class, and the session's opening hypothesis (that Currie–Mol's binary
`f_k` are Pansiot codes of witnesses) was wrong regardless of what their
`f_k` actually are. Two hours of derivation kept as reusable lemmas; the
plan discarded.

## Act II: is the conjecture even true at 22?

With the nice subclass dead, the raw question: does the letter-space
language (avoid undirected exponents `> 21/20` over 22 letters) survive at
all? Controls first: the DFS correctly stays alive at four known-true
thresholds and correctly dies at two known-false ones. Then `n = 22`:
**alive**, with 1.6 M canonical words at length 55 (an early "unique
bottleneck at length 50" reading was an artifact of a node-capped run —
caught and corrected when the uncapped run finished). Random probes reach
length 800 with 24 backtracks; lexicographic greedy reaches 20 000 with 22
backtracks. Also ran the *non-strict* variant: avoiding exponents
`≥ 21/20` dies at length exactly 25 = k+3, in a 451-node tree — which is
an independent certificate of the lower bound `URT(22) ≥ 21/20`, and the
same at 23, 24, 25 (all `k+3`; Conjecture C3). The two-sided picture at
the threshold is now certified sharp.

## Act III: constructions — three ansätze, three walls

An infinite witness needs structure, not probes. Attempts, in order:

1. **Twisted-periodic** (`w[i+P] = σ(w[i])`): killed on paper before
   coding — such words are periodic with period `P·ord(σ)`, and no
   periodic word is U-free (Lemma L4). (Fifteen minutes from idea to
   refutation; the refutation is the lemma.)
2. **Additive/affine morphisms** `φ(x) = m·x + B₀ (mod 22)` — fixed
   points are digit-sum words generalizing Thue–Morse; the search space is
   one block. A first concrete-space search was hopeless (the first 20
   letters are all distinct, so concrete enumeration is ~21! redundant);
   a canonical-space search with a partial letter-injection had a
   soundness hole (constraints with unassigned sources bind
   retroactively); the correct engine carries symbolic affine forms over
   the free variables with incremental GF(2)×GF(11) elimination and
   injectivity pruning. Verdict: **empty**. `m = 1`: dead by depth ≤ 47
   for every `k ≤ 36` (exhausted). All ten units `m` at `k = 22`: dead by
   depth ≤ 3k (exhausted). A momentary "survivor" at `(k, m) = (22, 9)`
   was an artifact of a shallow depth target — it died at exactly `3k` on
   the deep rerun. The deaths cluster at depths `2k`–`3k`: the second
   block, a constant shift of `B₀`, collides with `B₀` through reversed
   pairs.
3. **General uniform-morphic fixed points** (any blocks): searched in
   canonical space with union-find class forcing (`W[q]` forced equal to
   `W[q′]` when parents carry equal letters and offsets agree). First run
   had two bugs (class (0,0) unbound; depth far too shallow to ever force
   anything — identical node counts across `k` were the tell). Fixed:
   the search hits a hard wall at depth exactly `20k` — the first parent
   repetition, where block reuse begins — and 4 M-node runs thrash
   against it without exhausting. **Inconclusive.**

Meanwhile the criterion side firmed up: block-level reversal-*closure*
is impossible in letter space (an `ℓ = 1` pigeonhole kills every twist
family — with 22 letters one cannot exclude `y = γ(x)` for nearby pairs
beyond `γ = id`), so the right design is reversal-*exclusion*: forbid
`(B_y)ᴿ` from occurring in any two-block window at all. Self-similarity
then turns preservation into an infinite descent on the single word `W`.
That became **Theorem D** (NOTE §8), proved with exact constants
(`L₀ = 42k−20`), including the boundary-extension bookkeeping and the
square-fallback when the parent arm exceeds its period.

## What failed, compressed

- The session-opening plan (binary Pansiot + reversal-closed pairs):
  class certified empty. Kept: checkers, reversal lemmas.
- Twisted-periodic ansatz: refuted by a two-line lemma.
- Reversal-closure designs (`ρ = swap` bit-level; letter-level twist
  families): killed by descent-closure analysis and the `ℓ = 1`
  pigeonhole respectively, before implementation.
- Concrete-space block search: symmetry explosion, abandoned.
- First canonical+injection search: soundness hole, replaced.
- Affine family: certified empty (the one "survivor" was a depth
  artifact).
- General uniform search: wall at `20k`, node-capped, honest
  inconclusive.
- Early mis-readings caught in-session: the "unique bottleneck at 50"
  (cap artifact); the "binary death explains their k ≤ 21 wall" guess
  (the class is empty at 20 and 21 too, where their theorem holds — so
  it explains nothing about their proof and instead says witnesses use
  distance-`(n−2)` recurrences).

## Where a future session should start

1. The `20k` wall in `selfsim_search.py` with a solver-grade engine
   (C with conflict learning, or a SAT encoding of class-forcing +
   incremental U-constraints). Everything needed for certification
   afterwards exists (Theorem D + checkers).
2. Prove Conjecture C3 (`k+3`) by hand; the trees are tiny and the
   extremal words look classifiable.
3. The 3-choice automaton for the true `gap ≥ n−2` class (NOTE §9.3).
4. Read Currie–Mol (both papers) the moment egress allows; re-verify
   every (secondary) statement, especially the definition conventions
   and their `f_k` construction — and check nobody has done `k ≥ 22`
   since 2024.

## Session hygiene notes

Two background-run artifacts nearly became wrong claims (the bottleneck
uniqueness, the `(22, 9)` survivor); both were caught by rerunning
uncapped/deeper before anything was written down. The discipline that
every number must be regenerated by a committed script (`lower_bounds.py`,
`code_class.py`, `certify_witness.py`) was applied at the end to every
table in the NOTE.
