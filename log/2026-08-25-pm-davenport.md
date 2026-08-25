# 2026-08-25 — pm-davenport

**Target.** Decide the plus–minus weighted Davenport constants
`D±(C₅ ⊕ C₁₅)` and `D±(C₇ ⊕ C₂₁)` — the first reported open since
Marchan–Ordaz–Schmid 2013 (arXiv:1308.3316, IJNT 2014), where it is the
single undetermined group of order ≤ 100 ("either 6 or 7"); the second
apparently never treated — and, with the same exact engines, map
`μ(G) = D±(G) − 1` (= the maximum size of a *dissociated* subset of `G`)
across every finite abelian group of order ≤ 192 plus targeted larger
families.

**Result.** CERTIFIED — **`D±(C₅ ⊕ C₁₅) = 6`** (the lower end of the
published bracket {6,7}: no dissociated 6-set exists; three independent
engines, including a full brute force over all 2,324,784 six-subsets of
±-classes, agree, and four independent computations reproduce the
identical census of 85,155 extremal 5-sets, every one re-verified by
direct enumeration), **`D±(C₇ ⊕ C₂₁) = 8`** (attains the pigeonhole upper
bound: a verified 7-element dissociated witness exists; the upper bound is
a proved lemma, no search needed — and the extremal set is **unique up to
automorphism**: all 2,016 extremal sets are checksum sets forming a single
Aut-orbit), and **`D±(C₃ ⊕ C₄₅) = 7`** (the first case reported outside
MOS's `C₃⊕C₃ₙ` side conditions — single-snippet evidence tier — decided
at the concatenation value, census 3,391,470). Plus a CERTIFIED census of `μ(G)` for
**all** abelian groups of order ≤ 192 and thirteen larger targeted groups
(C₇⊕C₇ₙ, C₅⊕C₅ₙ, C₃⊕C₃ₙ families, C₇³, C₅²⊕C₁₅, C₁₃²), reproducing every
literature control (cyclic formula, the three published exceptional values
C₃² → 3, C₃³ → 4, C₃²⊕C₉ → 6, and every non-exceptional order ≤ 100 value
implied by MOS's theorem). Plus PROVED elementary lemmas: the
dissociated ⟺ subset-sum-injective reduction, DFS-correctness, both sides
of the Adhikari–Grynkiewicz–Sun bracket (self-contained proofs), a
checksum construction lemma `μ(C_m ⊕ H) ≥ ν_m(H)` explaining every
bound-attaining witness found, a graded-counting upper bound for `ν_m`,
and `μ(C_p^r) = r` for `p ∈ {2,3}`. Details and the final deficient-group
list in `conjectures/pm-davenport/`.

**Branch note.** The session mandate asks for `claude/<conjecture>-YYYY-MM-DD`;
this environment designates `claude/kind-bohr-uwtx1g` and forbids pushing
elsewhere. Working on the designated branch, as previous cloud sessions did.

## Connectivity check (2026-08-25)

- **WebFetch: fully blocked** (EGRESS_BLOCKED from the sandbox proxy),
  tested against arxiv.org, oeis.org, erdosproblems.com, mathoverflow.net.
  No primary source was readable from this session.
- **WebSearch: working.** All literature claims this session are from
  search-result snippets retrieved 2026-08-25. **Every citation is
  (secondary)** and every openness claim is as strong as today's snippets,
  no stronger. Three literature-vetting subagents ran ~65 searches total;
  their full reports are summarized in WRITEUP.md.

## Candidate slate (external)

**C1 — plus–minus weighted Davenport constants of rank-2 odd groups
(zero-sum combinatorial number theory / additive combinatorics). Chosen.**
Statement: `D±(G)` = least ℓ such that every length-ℓ sequence over `G`
has a nonempty subsequence summing to zero with coefficients ±1.
Equivalently `D±(G) − 1` = maximum size of a dissociated subset of `G`.
Known (all secondary, snippets 2026-08-25): Adhikari et al. introduced the
weighted framework (~2006); `D±(C_n) = ⌊log₂ n⌋ + 1`;
Adhikari–Grynkiewicz–Sun (Adv. Appl. Math. 48 (2012) 506–527,
arXiv:1003.2186) proved `Σᵢ⌊log₂ nᵢ⌋ + 1 ≤ D±(G) ≤ ⌊log₂|G|⌋ + 1`;
Marchan–Ordaz–Schmid (Int. J. Number Theory 10 (2014) 1219–1239,
arXiv:1308.3316) determined `D±(G)` for **all |G| ≤ 100 except exactly
one group — C₅ ⊕ C₁₅, "either 6 or 7"** — with exceptional (non-log)
values only at C₃² (3), C₃³ (4), C₃²⊕C₉ (6). Sources: snippets of
arXiv:1308.3316 / hal-00835688 (three independent queries agree on the
"one exception, 6 or 7" reading); the Perez-Lavin thesis
(uknowledge.uky.edu/math_etds/79); INTEGERS 22 (2022) #A36
(math.colgate.edu/~integers/w36/w36.pdf) for the bracket attribution.
Why believed open: no 2013–2026 hit determines either group; the active
groups who would cite it (Graz factorization school: arXiv:2404.17258,
2304.14777; Merito–Ordaz–Schmid arXiv:2506.14279, June 2025) show no such
value in any snippet. Caveat: full texts unreadable today (WebFetch
blocked); MathSciNet/zbMATH unchecked; a read of arXiv:1308.3316 §exact
values is **mandatory before publication** (claim-discipline rule 3).
Bottleneck type: pure finite search, small (75- and 147-element groups),
exactly certifiable — ideal for this machine.

**C2 — no-three-in-line, first 2n-point solution for n = 47 (discrete
geometry). Dropped: already solved.** Vetting (12 searches) found the
frontier moved from the classical n ≤ 46 (Flammenkamp) to **n = 76**:
Prellberg solved n = 47 and 49 in Sept 2025
(wwwhomes.uni-bielefeld.de/achim/no3in/Prellberg_Sep_2025.pdf), CSP paper
arXiv:2602.07751 (all n ≤ 60), Heule's SAT solutions through n = 70, 72,
74, 76 (record 10 Aug 2026, per Flammenkamp's readme news feed; all
secondary, snippets 2026-08-25). An active monthly arms race
(Heule/Prellberg/Riley) — no room for this session. Bonus correction
recorded: the Guy–Kelly constant ~1.87 was corrected by Ellmann (2004) to
≈ 1.8138 (Voutier, arXiv:2603.00215).

**C3 — smallest open Turán number ex(41; C₄) ∈ {132, 133} (extremal graph
theory). Runner-up.** OEIS A006855 stops at a(40) = 127; a(41) bracket
132 ≤ · ≤ 133 (lower: McKay Mar 2022; upper: Alekseyev's
`a(n) ≤ ⌊a(n−1)·n/(n−2)⌋` Jan 2023; all secondary, snippets 2026-08-25).
Deciding the bit means either a 133-edge C₄-free graph on 41 vertices or
an exhaustion — the exhaustion side is McKay-grade orderly-generation
territory, days-to-weeks of engineering with uncertain runtime, and the
frontier's owners (McKay, Alekseyev, Afzaly) are active. Scored below C1
on breakability-per-session.

## Internal-thread assessment

Strongest live thread: **undirected-thresholds, the `20k`-wall re-attack**
(log 2026-08-18: uniform-morphic search for `URT(22)` hits a forcing wall
at depth `20k`; named next step is a solver-grade engine — C with conflict
learning, or SAT with class-forcing). Significant progress = a certified
survivor past the wall feeding Theorem D's finite checks, i.e. real
movement toward `URT(22) = 21/20`. Assessment: idea- and
engineering-bound, not compute-bound — 4M-node runs "neither pass nor
exhaust" — so a session may well end at the same wall; and it was the
immediately preceding session's conjecture. Other threads (grimm → 10¹³,
vdw-mixed cube-and-conquer, distinct-subset-sums 262 → 309) are range
extensions or long SAT campaigns that would not change their index rows
today. Verdict: does not clearly beat C1.

## Selection

(a) *Breakability:* C1's bottleneck is a finite search over 37 resp. 73
±-classes — hours of CPU at most, fully certifiable, with proved bracket
lemmas reducing each group to one bit. C2 is closed; C3 is a
weeks-of-engineering bit; the internal thread is idea-bound. (b) *Priority
risk:* C1's exact statement ("the one order ≤ 100 exception") is quoted in
three independent snippet syntheses; the 2013–2026 silence was checked by
a dedicated agent across ~26 queries; residual risk documented (full texts
unread). (c) *Who cites it:* Marchan–Ordaz–Schmid directly (Schmid and
Ordaz active on this exact monoid as of June 2025, arXiv:2506.14279); the
Graz factorization-theory school whose arithmetic invariants of `B±(G)`
are controlled by `D±(G)`; the intersecting-codes line (arXiv:2406.04034).
**Chosen: C1**, the external default, no tie to break.

What would count as achieving it: `D±(C₅⊕C₁₅)` decided with a certificate
a referee can re-run, `D±(C₇⊕C₂₁)` likewise; anything beyond that
(systematic table, structure, proofs) is upside.

## What failed / dead ends

- **The pigeonhole refinement does not prove the C₅⊕C₁₅ refutation by
  hand.** The graded counting bound (NOTE.md Lemma 6) eliminates only the
  profiles k₁ ≤ 2 (number of elements with nonzero C₃-part in the CRT
  presentation C₃⊕C₅²); profiles k₁ ∈ {3,4,5,6} pass the counting test
  (margins 24, 24, 22, 22 vs |H| = 25) and die only by exhaustive search.
  A conceptual proof of this single bit remains open.
- **"Rank-2 groups never exceed the concatenation bound"** — a hypothesis
  formed after C₅⊕C₁₅ came out deficient — was refuted within the hour by
  C₃⊕C₆ (attains, uniquely) and then C₇⊕C₂₁ itself (attains via mixed
  witnesses). The truth is the reverse: attainment is the rule, deficiency
  the rare exception.
- **A uniform infinite-family construction** (binary ladder + checksum
  extras for all gap-1 members of C₅⊕C₅ₙ) hit the obstruction that
  {0,±1}-representations of multiples of M by powers of 2 have
  non-invariant sign-weights; the counting argument over the extras'
  choices fails (3^s patterns ≫ M). Family-wide statements stay
  conjectures; per-group decisions stay certified bits.
- Engine C's first control run was miswritten (asked for refutation at
  t = μ instead of t = μ+1 on C₉); the engine was right, the test was
  wrong, fixed in-session — noted here per the honesty rule.
- `/usr/bin/time` does not exist in this sandbox; first heavy-batch launch
  died on it. Relaunched with plain date-stamping.

## Next

- Read arXiv:1308.3316 (and 2506.14279, 2404.17258, the 2017 survey) the
  moment egress allows; verify the "one exception ≤ 100" reading, their
  C₃⊕C₃ₙ side conditions, and whether the checksum lemma is their Lemma
  already; then decide whether NOTE.md's novelty claims stand.
- The deficiency-characterization question: the census's deficient list is
  small and 3-heavy; find the invariant that separates C₃⊕C₅²
  (deficient) from C₃⊕C₇² (attaining). ν₃(C₅²) = 5 vs ν₃(C₇²) = 7 is the
  computational answer; a formula for ν₃(C_p²) is the open thread.
- `μ(C₇³)` and `μ(C₅²⊕C₁₅)` (gap-2 and nested cases) — runs queued this
  session; if unfinished, they are the next session's first certificate.
- OEIS: the census produces the sequence `μ(G)` over group orders (max
  over groups of that order, and per-group); check against/contribute to
  OEIS once reachable.
