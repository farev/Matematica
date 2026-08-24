# 2026-08-24 — plusminus-davenport

**Target.** Determine D±(C₅⊕C₁₅), the plus–minus weighted Davenport constant
of the one abelian group of order ≤ 100 whose value Marchan–Ordaz–Schmid
(IJNT 2014) could not determine — their bounds give "6 or 7" — by certified
exhaustive search; then recompute their whole table independently and extend
it past order 100, where no values appear to be published. External problem,
new conjecture directory. What counts as achieving it: the cell decided with
independent cross-verified certificates, controls anchored to every
snippet-visible published value, and the table extension; stretch goal, any
hand-provable structure on top.

**Branch note.** The session mandate asks for `claude/<conjecture>-YYYY-MM-DD`;
this environment designates `claude/kind-bohr-ckdwfr` and forbids pushing
elsewhere. Working on the designated branch, as previous cloud sessions did.
The `conjecture-research` skill named in CLAUDE.md is not present in this
sandbox (`.claude/` holds only settings); followed CLAUDE.md directly.

## Connectivity check

- **WebFetch: fully blocked** (EGRESS_BLOCKED), tested 2026-08-24 against
  arxiv.org, oeis.org, erdosproblems.com, mathoverflow.net, and non-list
  academic hosts (hal.science, uknowledge.uky.edu, math.univ-paris13.fr).
  No primary source was readable.
- **WebSearch: working.** Every literature claim this session is
  **(secondary)**, from search snippets retrieved today; every "this is
  open" claim is exactly as strong as those snippets.

## Candidate slate (external)

**C1 — D±(C₅⊕C₁₅) (zero-sum combinatorial number theory). Chosen.**
Statement: D±(G) = least ℓ such that every length-ℓ sequence over G has a
nonempty subsequence with ±1-weighted zero sum; for G = C₅⊕C₁₅ the value is
6 or 7, the single undetermined case of the Marchan–Ordaz–Schmid table of
all |G| ≤ 100. Sources checked 2026-08-24 (secondary): arXiv:1308.3316
snippets (the bracket and the "all ≤ 100 except one" statement); the 2017
survey chapter (Springer 978-3-319-68376-8_1) still listing it; active
2024–2026 school papers on the arithmetic side (2404.17258, 2506.14279,
2607.02132) with no new-values claims; seven differently-phrased searches
found no statement of the value. Known risk, flagged in every document: the
unreadable 2021 Kentucky thesis (Perez-Lavin, *The Plus-Minus Davenport
Constant of Finite Abelian Groups*, focus "primes 2 and 3" per abstract).
Why chosen: the bottleneck is a bounded exhaustive search (an afternoon,
with certification); extends a named table the active school still cites.

**C2 — least critical exponent of balanced sequences, odd alphabets
(combinatorics on words). Not chosen.**
Rampersad–Shallit–Vandomme's conjecture ((d−2)/(d−3)) was refuted for
d ≥ 11 by Dvořáková–Opočenská–Pelantová–Shur (TCS 2022, (secondary)):
the truth is ≥ (d−1)/(d−2), attained for all even d ≥ 12; revised
conjecture (d−1)/(d−2) for all d ≥ 11, with odd d open (snippet ambiguity
whether d = 11 itself or only d ≥ 13 remains). Not chosen: their
construction machinery (Sturmian colorings by constant-gap sequences,
bispecial-factor critical-exponent formula) is paper-specific and the papers
are unreadable from here; medium confidence in both openness and a one-day
implementation.

**C3 — R₅(x+3y=3z), 5-color Rado number (arithmetic Ramsey theory). Not
chosen.** Known > 296 > 3⁵ = 243 — the b^k pattern R_k(b) = b^k (Chang–De
Loera–Wesley line, SAT-computed for k ≤ 4) breaks at k = 5, per a 2025
SSRN/arXiv line with an explicit 5-coloring witness ((secondary)). Deciding
the exact value is one SAT instance, but 5-color threshold instances at
n ≈ 300+ can cost far more than a 4-core day (repo precedent: w(2;4,7)
needed an 18.4M-line proof), and an active group visibly owns the thread.

Subfields spanned: zero-sum combinatorial number theory, combinatorics on
words, arithmetic Ramsey theory.

## Internal-thread assessment

Read the top-level index and the 08-15..08-18 logs. Rotation rule: last two
sessions were vdw-mixed (08-16), peaceable-queens (08-17),
undirected-thresholds (08-18) — no conjecture at two consecutive sessions;
nothing blocked. Strongest live internal threads: (1) undirected-thresholds
— re-attack the depth-20k forcing wall with a solver-grade engine; a day of
engineering with uncertain payoff, one session old. (2) grimm — push the
verification to 10¹³ (~9 h, extends own 10¹² record 10×; the weakest kind of
new result by the mandate's own standards). (3) generalized-schur —
(4,4,u) still blocked on a DRUP toolchain that egress-blocking prevents
installing. None beats C1: C1's bottleneck is decisively compute-breakable
today, its openness trail is explicit in the source paper, and the result
lands in a living table. Default-external and the argument is not close.
Chose **C1**.

**Result.** Two headline items, labels per claim discipline:

**CERTIFIED — D±(C₅⊕C₁₅) = 6** (max ±-zero-sum-free sequence length 5; the
concatenation lower bound is the truth, the pigeonhole bound 7 is not
attained). Four independent implementations: numpy-DFS (139 052 nodes,
exhaustive), full C(37,6) = 2 324 784-combination integer sweep (zero ±-zsf
6-sets), C bitset DFS (node count matches the Python DFS exactly), and a
stratified enumerator (all five strata of the kernel-size case split empty).
Census of all 85 155 maximum 5-sets, with the stratum counts
3 375/13 500/29 040/27 960/11 280 and 3 375 = 135×25 explained exactly.
Lower bound PROVED (concatenation + cyclic lemmas + standalone-verified
witness); strata (4,2) and (3,3) of the upper bound PROVED by hand
(saturation lemma; sum-free classification of allowed sets of ±-zsf 3-sets
in 𝔽₅², 60 line-type + 120 generic, hand-checkable tables in NOTE §4.1).

**CERTIFIED — the table around it.** Independent recomputation of d± for all
184 abelian group types of order ≤ 100 (167 forced by in-house-proved
bounds, 17 decided by search; the published anchor D±(C₉⊕C₃⊕C₃) = 6
reproduced); extension to all types of order 101–135 and
targeted C-engine cells to order 243, apparently the first values past 100
((secondary)): D±(C₇⊕C₂₁) = 8 and D±(C₅⊕C₃₀) = 8 (both pigeonhole-tight;
16.5M and 24.6M nodes), D±(C₁₃⊕C₁₃) = 8 (54.45M nodes, 4-shard exhaustive),
D±(C₃⊕C₅₁) = D±(C₃⊕C₅₇) = 8, D±(C₃⊕C₃⊕C₂₁) = 8 (115.9M nodes, an open
[6,7]-cell decided at the top), and D±(C₉⊕C₃⊕C₃⊕C₃) = 8 (order 243, the
session's largest search: 736.6M nodes, 4-shard exhaustive — sharply
contrasting its order-81 subgroup C₉⊕C₃⊕C₃, which sits at the lower
bound), more in `conjectures/plusminus-davenport/data/`. Landscape: 12 of the 17 open cells
≤ 100 attain the pigeonhole bound — C₅⊕C₁₅ (lower) is the exception, not
the rule; d± separates four of the five order-81 groups; first cell strictly
between both bounds at order 135 (C₃⊕C₃⊕C₁₅, d± = 6 ∈ (5,7), explained by
the split C₃⊕(C₃⊕C₁₅)). **PROVED lemmas:** pigeonhole, cyclic, quotient
concatenation, saturation, exponent-3 = 𝔽₃-rank. **Conjecture A**
(split-or-pigeonhole: every G has d± = ⌊log₂|G|⌋ or splits), verified
mechanically at every computed group; the noncyclic "atoms" ≤ 100 are
exactly C₃⊕C₃ₘ (m = 2,4,5,8,9) and C₇⊕C₇. An interim **Conjecture B**
(C₃⊕C₃ₙ always pigeonhole-tight, formulated from the n ≤ 11 data) was
**refuted by this same session's sweep an hour later**: d±(C₃⊕C₄₅) = 6 < 7
at n = 15 (double-engine certified) — reported in full in NOTE §8 as the
cautionary exhibit; Conjecture A allowed both values there and survives.
**Conjecture C** (C₇⊕C₇ₙ tight) stands at n = 1–5, first open case
n = 6 (order 294).

**What failed.**
- The set-based Python engine was ~20× too slow for the control suite;
  rewritten on numpy boolean indicators (exact ops only).
- No hand proof found for strata (2,4), (1,5), (0,6) of the upper bound —
  counting and quotient arguments both fall short; they stay
  machine-certified, so Theorem 1 is CERTIFIED, not PROVED. Recorded as the
  sharpest proof gap.
- A shell timeout silently killed the first C₁₃⊕C₁₃ run; caught by log
  inspection, re-run sharded (shard bookkeeping validated exactly on the
  headline cell first: Σ shards = 139 052 + 3).
- The 135-extremal-set computation for C₅⊕C₅ was obsoleted minutes later by
  the one-line saturation lemma — compute first, then notice the trivial
  reason; kept as a lesson.
- Novelty remains (secondary)-limited: if the Perez-Lavin thesis or any
  unread source already decided the cell, today is an independent
  confirmation; this is flagged in NOTE/README/WRITEUP prominently.

**Next.** (1) Read Marchan–Ordaz–Schmid 2014, the 2017 survey, and the
Perez-Lavin thesis from a connected machine; resolve every (secondary) flag
and the novelty question. (2) Prove Conjecture A for rank 2, or refute it —
first unforced rank-2 cells beyond today's range: C₂₃⊕C₂₃, C₂₉⊕C₂₉,
C₅⊕C₅₅. (3) Hand-close the (2,4) stratum. (4) Complete orders 136–200
(C engine + sharding, CPU-hours). (5) If the literature check clears:
a short note to the school that owns the table, and an OEIS submission for
the noncyclic-maximum sequence.
