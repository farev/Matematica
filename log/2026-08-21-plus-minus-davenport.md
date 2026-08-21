# 2026-08-21 — plus-minus-davenport

**Target.** Determine the plus–minus weighted Davenport constants
`D±(C₅⊕C₁₅)` (order 75) and `D±(C₇⊕C₂₁)` (order 147) exactly — both
reported open in the literature around Marchan–Ordaz–Schmid (secondary; see
slate) — via the equivalence *±-zero-sum-free sequence ⟺ dissociated set*
(all `2^ℓ` subset sums pairwise distinct), which turns each value into a
finite exhaustive search in a window of width one:
`D±(G) − 1 = ℓ_max(G) ∈ {⌊log₂|G|⌋ − ε, ⌊log₂|G|⌋}`. Then push a complete
certified census of `ℓ_max(G)` over **all** finite abelian groups of order
`≤ N` (target `N ≥ 255`), reproduce every published `D±` value reachable
from this sandbox as controls, map where the counting bound
`ℓ_max = ⌊log₂|G|⌋` is attained, and hunt for provable structure. Success =
the two constants decided with reproducible certificates + the census +
at least one proved lemma. This is a first session on a new problem, in a
subfield (zero-sum theory / additive combinatorics) the repository has not
touched.

**Branch note.** The mandate asks for `claude/<conjecture>-YYYY-MM-DD`; this
environment designates `claude/kind-bohr-4o8200` and forbids pushing
elsewhere. Working on the designated branch, as previous cloud sessions did.

## Connectivity check

Tested 2026-08-21 from the sandbox:

- **arxiv.org — BLOCKED** (EGRESS_BLOCKED), also `export.arxiv.org`.
- **oeis.org — BLOCKED.**
- **erdosproblems.com — BLOCKED.**
- **mathoverflow.net — BLOCKED** (fetch fails).
- Also blocked: `hal.science`, `web.archive.org`, `quantamagazine.org` —
  the egress policy is effectively a whitelist; no academic host was
  readable this session.
- **WebSearch — WORKING.** All literature claims below come from
  search-result snippets retrieved 2026-08-21. **Every citation in this
  session is (secondary)** unless it points at code/data in this repository.
- Reachable for tooling: pypi.org, files.pythonhosted.org (noProxy list),
  archive.ubuntu.com (per 08-17 log).

## Candidate slate (external)

**C1 — The plus–minus weighted Davenport constant of `C₅⊕C₁₅` and
`C₇⊕C₂₁` (zero-sum combinatorial number theory). Chosen.**
Statement: `D±(G)` is the least `ℓ` such that every sequence `g₁,…,g_ℓ`
over `G` has a nonempty subsequence and signs `a_i ∈ {+1,−1}` with
`Σ a_i g_i = 0` (Marchan–Ordaz–Schmid, "Remarks on the plus-minus weighted
Davenport constant", Int. J. Number Theory 10 (2014) 1219–1239 =
arXiv:1308.3316; definition confirmed verbatim in snippets, (secondary)).
Sources checked 2026-08-21, all secondary via snippets: the MOS paper (HAL
hal-00835688 exists but is egress-blocked); a search summary of it stating
they "found the plus-minus weighted Davenport constant for all groups up to
order 100 (except one)"; the 08-18 session's snippet of the surrounding
literature: "for `D±(C_5 ⊕ C_5n)` and `D±(C_7 ⊕ C_7n)` the value is unknown
already for n = 3" — i.e. exactly `C₅⊕C₁₅` (order 75 ≤ 100, consistent
with being MOS's one exception) and `C₇⊕C₂₁` (order 147); the survey
"Plus-Minus Weighted Zero-Sum Constants: A Survey" (Springer, in
Combinatorial and Additive Number Theory II, chapter 978-3-319-68376-8_1)
surfaced but its content is unreadable from here; active 2024–2026 work on
the plus-minus monoid `B±(G)` (arXiv:2404.17258, arXiv:2506.14279,
arXiv:2304.14777) cites `D±` as a live invariant. Targeted searches for
`D±(C_5⊕C_15)` / "order 75" / post-2014 computations of these two values
returned nothing.
Why believed open: two independent secondary snapshots (the MOS-era family
statement and the "except one ≤ 100" summary) say so; no later
determination surfaced in today's searches. **Honesty caveat, prominent:**
the primary sources are unreadable from this sandbox; the openness of these
two specific cells rests on snippets. The equivalence with dissociated sets
makes the order-75 case a small computation, which is *suspicious* — a
session deliverable is to state plainly that if either value is already in
print, today's contribution reduces to the census, the certificates, and
whatever structure is new.

**C2 — k-Göbel integrality lengths `N_k` (integer sequences / p-adic
number theory). Not chosen.**
Statement: for the k-Göbel recurrence, `N_k` = index of the first
non-integral term; Matsuhira–Matsusaka–Tsuchida (arXiv:2307.09741) proved
`N_k ≥ 19` for all `k ≥ 2`; Gima–Matsusaka–Miyazaki–Yara
(arXiv:2402.09064, J. Integer Seq. 27 (2024)) extended to `(k,l)`-Göbel;
Kobayashi–Seki (arXiv:2410.23240) proved non-integrality for classes of
`(k,l)`. Whether `N_{k,l} < ∞` always is open. A large certified sweep of
`N_{k,l}` was the plan. Why not chosen: vetting surfaced
arXiv:2502.17448 "On the length over which k-Göbel sequences remain
integers" (Feb 2025) — a paper on exactly this question whose content is
unreadable from the sandbox; collision risk too high to spend the session.

**C3 — Gaussian moat beyond √36 (computational number theory). Not
chosen.**
Statement: extend Tsuchimura's 2004/2005 record (moat of width √36;
IEICE E88-A(5):1267, METR 04-13) — the frontier of "walk to infinity on
Gaussian primes". Sources checked 2026-08-21 (secondary): Tsuchimura's
√36 required ≈5000× the computation of Gethner–Wagon–Wick's √26; no
extension since 2005 surfaced (a 2020 Springer chapter and 2019 arXiv
notes recompute or survey; a Jan 2024 claimed impossibility proof,
arXiv:2401.08441, was withdrawn). Why not chosen: the next rung's cost is
unpriceable from here (plausibly CPU-weeks even today), and the
20-year-quiet record status is exactly the kind of claim rule 3 wants
verified against primary sources this sandbox cannot read.

Also vetted and killed during the survey (recorded so the next session
does not redo the searches): **no-three-in-line** — the frontier moved
again since the 08-17 kill: snippets now report solutions for all
`n ≤ 70` (June 2026) and a new `n = 74` rot4 record by Prellberg
(20 July 2026), an active specialist race with CP/annealing tooling and
more compute than this sandbox; gaps at `n ∈ {71,72,73}` are exactly the
cases their tools have so far failed on.

Subfields spanned by the slate: zero-sum combinatorial number theory,
p-adic/integer sequences, computational analytic number theory.

## Internal-thread assessment

Read the top-level README and the last five logs. Rotation rule: last two
sessions were peaceable-queens (08-17) and undirected-thresholds (08-18) —
no conjecture is at two consecutive sessions; nothing is blocked.

Strongest live internal thread, clearly: **peaceable-queens a(17)** (08-17
"Next" item 3): the boundary refutation `m = 43` at `n = 17` was priced at
5–8× the a(16) cost — roughly an hour on this hardware with the validated
SYM16 engine — and would deliver a second new exact term of A250000
(recorded bracket [42, 72]), a certain row change. Weaker threads:
undirected-thresholds' `20k` wall (needs a solver-grade engine, unpriced),
distinct-subset-sums' multi-m engine (a session of engineering,
CPU-months from deciding f(10)), generalized-schur's (4,4,u) ladder
(un-blocked by apt cadical but third-in-two-weeks on the same groove).

Selection argument: a(17) beats every external candidate on
certainty-of-payoff — the engine exists and the cost is measured. It loses
on every axis the mandate actually scores: (a) both a(17) and C1 are
CPU-breakable, but C1's bottleneck is a *new* search problem, not rung 17
of a ladder built four days ago; (b) "already done?" is *cleaner for C1
than for a(17)* in one respect — nobody else has the SYM16 engine, but
A250000's next term is a when-not-if for this repo, while C1's two
constants have sat (per the snippets) open since 2013 in a family the
Geroldinger–Schmid school still actively cites; (c) a(17) extends the same
three papers as the 08-17 session; C1 extends a different literature
(MOS 2014, the CANT-II survey, the 2024–2026 `B±(G)` monoid papers) and
the dissociated-set framing additionally lands in mainstream additive
combinatorics (Chang's lemma neighborhood). The mandate's default is
external, ties go to the new problem, and this is not even a tie on
novelty. **Chose C1.** a(17) remains on the shelf and will still be there
when the rotation forces variety.

**Today's specific attempt** (one paragraph): prove the ±-zsf ⟺
dissociated equivalence cleanly (with the resulting window
`⌊log₂|G|⌋ ≤ D±(G) − 1 + ε`), build a two-engine exhaustive search over
dissociated sets with automorphism-quotient pruning and
positive/negative controls, decide `D±(C₅⊕C₁₅)` and `D±(C₇⊕C₂₁)` with
certificates, then run the first complete census of
`ℓ_max(G) = D±(G) − 1` over all abelian groups of order ≤ 255 (stretch:
further), map exactly where the counting bound is attained, and try to
convert the map into at least one proved theorem. Mid-session checkpoint:
if the order-147 decision or the census stalls, ship what is decided with
honest pricing and record the wall.

**Result.** *(session in progress — filled at end)*

**What failed.** *(filled at end)*

**Next.** *(filled at end)*
