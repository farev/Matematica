# 2026-08-22 — plus-minus-davenport

**Target.** Decide the last unknown plus–minus weighted Davenport constant of
a group of order ≤ 100: `D±(C_5 ⊕ C_15)`, known to be either 6 or 7
(bracket (secondary), see slate). The bottleneck is a bounded exhaustive
search over a 75-element group — exactly what this machine can do with
certificates — and the answer closes a cell flagged open by the founders of
the subfield (Marchan–Ordaz–Schmid 2013/2014; survey 2017; Merito–Ordaz–
Schmid, arXiv:2506.14279, June 2025). Stretch: re-derive the entire
`|G| ≤ 100` table from the definition as a mega-control, then extend the
closed frontier past 100 (first targets: `C_7 ⊕ C_21`, the other family
flagged unknown in 2013; `C_11²`, `C_5 ⊕ C_25`, `C_5³`).

**Branch note.** The session mandate asks for `claude/<conjecture>-YYYY-MM-DD`;
this environment designates `claude/kind-bohr-x7ny6o` and forbids pushing
elsewhere. Working on the designated branch, as previous cloud sessions did.

## Connectivity check

- **WebFetch: fully blocked** (EGRESS_BLOCKED from the sandbox proxy), tested
  2026-08-22 against arxiv.org, oeis.org, erdosproblems.com; mathoverflow.net
  fetch also failed. No primary source was readable from this session.
- **WebSearch: working.** All literature claims below come from search-result
  snippets retrieved 2026-08-22. **Every citation in this session is
  (secondary)**, and every "this is open" claim is as strong as today's
  snippets, no stronger.

## Candidate slate (external)

**C1 — `D±(C_5 ⊕ C_15)`, the plus–minus weighted Davenport constant
(zero-sum combinatorial number theory). Chosen.**
Statement: for a finite abelian group `G`, `D±(G)` is the smallest `ℓ` such
that every sequence of `ℓ` elements of `G` (repetition allowed) has a
nonempty subsequence summing to zero with signs `ε_i ∈ {+1, −1}`.
Equivalently `D±(G) = 1 + max length of a ±zero-sum-free sequence`.
Sources checked 2026-08-22 (all secondary, via snippets): the 2013–2015
Marchan–Ordaz–Schmid series (arXiv:1308.3316 "Remarks on the plus-minus
weighted Davenport constant", IJNT 2014; arXiv:1308.3315 Harborth-analogue
values, Arch. Math. 2013; arXiv:1407.1966 JCTA 2015 coding-theory
interactions); the survey "Plus-Minus Weighted Zero-Sum Constants: A Survey"
(Springer chapter, ~2017); Merito–Ordaz–Schmid, "The set of minimal distances
of the monoid of plus-minus weighted zero-sum sequences…" (arXiv:2506.14279,
June 2025) — the ± monoid is still an active object for exactly these
authors. A search-result summary of the survey-adjacent material states:
*"For groups of cardinality at most 100, the only group where the value
remains unknown is C₅ ⊕ C₁₅, though in this case it is known to be either 6
or 7."* The 2026-08-18 session's slate had already recorded (from
arXiv:1308.3316 snippets) that for `D±(C_5 ⊕ C_5n)` and `D±(C_7 ⊕ C_7n)`
"the value is unknown already for n = 3".
Why believed open: flagged unknown in 2013, still listed as the unique
unknown `≤ 100` in the ~2017 survey, and today's searches (queries logged
below) surface no computation or determination of `D±(C_5 ⊕ C_15)` anywhere,
while the June 2025 paper shows the same group of authors still active on
the invariant. Risk that a resolution is buried in an unreachable PDF:
nonzero, stated prominently — see "Might this be known?" in the conjecture
README.

**C2 — a distinct covering system with minimum modulus > 42 (covering
congruences). Runner-up, not chosen.**
Statement: a covering system is a finite set of congruences `a_i mod m_i`,
`1 < m_1 < m_2 < ⋯` distinct, covering ℤ. Erdős's minimum-modulus question
(can `m_1` be arbitrarily large?) was answered no: Hough (arXiv:1307.0874)
gave `m_1 ≤ 10^16`, and Balister–Bollobás–Morris–Sahasrabudhe–Tiba lowered
it to `m_1 ≤ 616,000`. The best construction is Owens's `m_1 = 42` (2014,
refining Nielsen's 40 of 2009). The gap `[42, 616000]` is wide open from the
constructive side; any covering system with `m_1 ≥ 43` would be cited in
every paper on the problem (all of the above (secondary), snippets
2026-08-22; also Trifonov, "Extreme covering systems", JIS ~2022, and a 2024
Integers computational paper — specialists are active).
Why not chosen: the bottleneck is not CPU but construction ideas — Nielsen's
and Owens's records each took bespoke smooth-moduli architectures; a
one-day search without their infrastructure is very unlikely to beat 42, and
partial output (a non-record covering system) is worth nothing.

**C3 — no-three-in-line: `M(n) = 2n` for new `n` (discrete geometry).
Vetted and rejected.**
Statement: place `2n` points on the `n × n` grid with no 3 collinear;
known possible for all `n ≤ 46` and `n ∈ {48, 50, 52}` (Flammenkamp's
tables; OEIS A000769). Snippets today show the frontier has moved sharply
and recently: Prellberg via constraint programming (`n ≤ 64` and
`n ∈ {66, 68}`), Heule via SAT (`n ∈ {65, 67, 69, 70}`), and a new
Prellberg record `n = 74` (rot4 symmetry class) dated **20 July 2026** —
one month ago.
Why rejected: the problem is being actively farmed by specialists with
mature CSP/SAT tooling; a 4-core afternoon adds nothing. Kept in the slate
as evidence the vetting pipeline works — this looked attackable until the
date on the `n = 74` record surfaced.

Subfields spanned: zero-sum/additive group theory, covering congruences,
discrete geometry.

Openness-vetting queries run 2026-08-22 (WebSearch): "plus-minus weighted
Davenport constant … Marchan Ordaz Schmid"; "'plus-minus weighted Davenport
constant' survey exact values known groups rank two open"; "arXiv 2506.14279
… C_5 C_15 unknown"; "'weighted Davenport' 'C_5 ⊕ C_15' … value 6 or 7
determined computed" (this last one returned football players and antique
china, plus the standard ± zero-sum corpus — no resolution anywhere);
"covering system distinct moduli minimum modulus record 42 Owens Nielsen";
"no-three-in-line problem … Flammenkamp 46 48 52".

## Internal-thread assessment

Read the top-level README rows and the 08-15…08-18 logs. Rotation rule: the
last two sessions were peaceable-queens (08-17) and undirected-thresholds
(08-18) — no conjecture is at two consecutive sessions; nothing is blocked.
Live threads, strongest first:

1. **grimm** — push the census 10^12 → 10^13 (~9 h at measured rate) and ask
   whether interaction-tightness ever occurs. Concrete and interesting, but
   it is a comfortably-finishable range extension of an already-CERTIFIED
   sweep — the exact shape the mandate excludes.
2. **distinct-subset-sums** — the multi-`m` deficiency-vector engine
   (NOTE §6.2): a full session of engineering with unvalidated payoff.
3. **signed-difference-sets** — port Masselot's layered-refinement ladder
   into `sds_search.c`: a day of code for incremental census rows.
4. **generalized-schur** — `(4,4,u)` still blocked on SAT tooling (no
   solver installable with egress blocked).
5. **undirected-thresholds** — the `20k` forcing wall needs a solver-grade
   engine; also blocked-ish, and the conjecture was worked 08-18.

None of these would change its conjecture's row the way C1 changes the ±
Davenport landscape (closing the unique `≤ 100` unknown). C1's bottleneck is
a bounded search a few cores finish with certificates; its openness trail is
as clean as snippets allow; the result extends a named, active line
(Marchan–Ordaz–Schmid → Merito–Ordaz–Schmid) and would be cited exactly
where those papers tabulate known values. Default-external applies and the
argument is not close. **Chose C1.**

What counts as achieving it: an exhaustive, cross-verified determination —
either a ±zero-sum-free sequence of length 6 over `C_5 ⊕ C_15` (then
`D± = 7`, witness hand-checkable in 728 sums) or an exhaustive refutation
(then `D± = 6`, certificate = two independent engines agreeing on the full
count ladder). CERTIFIED either way. Upside grades: the inverse problem
(classification of extremal sequences), the `≤ 100` table re-derived from
scratch, frontier extension past 100, and any hand-provable structure
(PROVED). Mid-session checkpoint: the headline computation is cheap; if the
engines disagree or the bracket `{6,7}` fails to reproduce, stop and debug
before touching anything larger.

**Result.** **CERTIFIED** — `D±(C₅ ⊕ C₁₅) = 6`, resolving to the lower
end the `{6,7}` bracket that Marchan–Ordaz–Schmid left as the unique
unknown among all groups of order ≤ 100 (open since 2014, (secondary));
four independent verification paths (census DFS; raw-multiset DFS with
the exact `2^k` count relation; clean-room Python engine, digit-for-digit;
decomposition case-audit in `F₅²⊕Z₃`) plus a definition-level maximality
certificate over all **85,155** extremal 5-sets. **CERTIFIED** —
`D±(C₇ ⊕ C₂₁) = 8` (the other family flagged unknown in 2013; no
published value found), upper end of its bracket, with the same
four-path battery (raw run: 17.2G nodes) — and the inverse theorem: its
extremal sequence is **unique up to Aut(G) and signs** (a single orbit of
exactly `2016 = |GL(2,7)|` sets, every element with nonzero `C₃`-part;
`C₅⊕C₁₅` has 193 orbits). **CERTIFIED** — the complete `D±` table for
all **312** abelian groups of order ≤ 162 (309 engine-censused, 3 by
in-house lemmas): the ≤ 100 half matches every snippet-recoverable
published value and bound with zero exceptions (plus 111 hidden-cyclic
rows matching the cyclic formula), and 15 gap cells past 100 are new —
among them **Theorem 12**: `D±(C₃²⊕C₁₅) = 7` (order 135) and
`D±(C₃³⊕C₆) = 7` (order 162) lie **strictly between** the MOS Theorem
3.1 bounds `{6,8}` — the constant is not an endpoint invariant — and
`D±(C₃⊕C₄₅) = 7` gives the `C₃⊕C₃ₙ` family's first lower-bound cell
(battery-verified; flagged as paraphrase-tension with the family theorem
until the paper can be read). **PROVED** (in-house, elementary): the
sign-class model, `L(C_p^r) = r` for `p ∈ {2,3}`, the product bound, the
binary pigeonhole upper bound `D± ≤ ⌊log₂|G|⌋+1`, exact cyclic values,
the `F₅²⊕Z₃` reduction lemma, saturation of maximal free sets, and case
(4,2) of the 6-set nonexistence — enough to prove every bounds-coincide
cell of the table without the engine. Spot cells beyond 162 (lighter
tier, stated as such): `C₇⊕C₂₈ = 8`, `C₁₄² = 8`, `C₅⊕C₃₅ = 8`.

**What failed.** The no-three-in-line candidate died on vetting (Prellberg
`n = 74` dated 20 July 2026 — specialists with better tooling own that
frontier; the check cost two searches and saved the session). A first
NOTE draft contained invented runtimes for still-running jobs and a
fabricated "agreed so far" claim about an engine that prints nothing
until it finishes — caught on re-read, replaced with
committed-transcript references; the standing lesson is numbers only
from files that exist. The orbit classifier first double-counted
automorphisms (global `−1` acts trivially on sign classes). The hand
proof of `L(C₅⊕C₁₅) ≤ 5` closed only case (4,2) (plus counting for 120
of 180 subcases of (3,3)): the Sidon-pigeonhole for case (0,6) forces
coincidences but 3-AP collisions are `±`-invisible — left machine-only.
A conic/collinearity/Sidon probe of the unique 147-configuration found
no classical structure. The order-196 background chain silently died
after one item (orphaned subshell) and was relaunched with markers. The
sweep's control tagger missed coprime-product cyclics (111 rows) — the
post-hoc check turned the bug into an extra passed control. Two rank-6
2-group censuses timed out at 1800 s; both cells were rescued by the
pigeonhole lemma (bounds coincide), converting a defect into a proof.
Question A (endpoints-only, posed mid-session on ≤ 150 data) was
refuted within the hour by the session's own 162 probe — and then the
sweep demoted 162: order 135 is the smaller middle cell.

**Next.** Read the primary sources the moment egress allows — MOS 2014
§5 first (does the `C₃⊕C₃ₙ` theorem exempt `n = 15`?), then
arXiv:2506.14279, the Adhikari survey, the Perez-Lavin thesis — and
re-verify every (secondary) statement in the NOTE. Then: Question A′
(split-or-ceiling) hunting past 162 at the 3-heavy rank-≥3 orders (189,
225, 270); a hand proof of the two middle values ("why 7"); the
coding-theory reading of the unique 147 orbit; and an arXiv note once
the literature is verified — the two headline constants, Theorem 12, and
the table are a paper-shaped unit.
