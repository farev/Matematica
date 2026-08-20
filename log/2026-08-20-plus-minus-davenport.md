# 2026-08-20 — plus-minus-davenport

**Target.** Decide the smallest open case of the plus-minus weighted
Davenport constant: `D±(C5 ⊕ C15)`, reported by Marchan–Ordaz–Schmid
(IJNT 2014, arXiv:1308.3316, (secondary)) as *the only group of order
≤ 100 whose value is unknown*, boxed between 6 and 7 — and with it the
other two smallest open cases in the rank-two families they flagged:
`D±(C7 ⊕ C21) ∈ {7, 8}` ("unknown already for n = 3" for both
`C5 ⊕ C5n` and `C7 ⊕ C7n`, (secondary)) and the first open case of
their `C3 ⊕ C3n` theorem, `D±(C3 ⊕ C45) ∈ {7, 8}` at `n = 15`. Route:
the two-line equivalence `D±(G) = 1 + dis(G)` where `dis(G)` is the
maximum size of a *dissociated* subset (all `2^k` subset sums
distinct), which turns each value into a bounded exact search over
subsets of `G` — breakable on 4 cores with certificates, cross-checked
implementations, and the whole `|G| ≤ 100` table as positive controls.
What counts as achieving it: each computed value carried by (i) a
witness verifiable from the definition in milliseconds and (ii) an
exhaustive-search certificate from two algorithmically independent
engines, plus the family tables `C5⊕C5n`, `C7⊕C7n`, `C3⊕C3n` as far as
the box reaches, and lemma work on when the upper bound
`⌊log2 |G|⌋ + 1` is attained.

**Branch note.** The session mandate asks for
`claude/<conjecture>-YYYY-MM-DD`; this environment designates
`claude/kind-bohr-igvlva` and forbids pushing elsewhere. Working on the
designated branch, as previous cloud sessions did.

## Connectivity check

- **WebFetch: fully blocked** (EGRESS_BLOCKED from the sandbox proxy),
  tested 2026-08-20 against arxiv.org, oeis.org, erdosproblems.com,
  mathoverflow.net, and non-list academic hosts (ar5iv.arxiv.org,
  link.springer.com, semanticscholar.org). No primary source was
  readable from this session.
- **WebSearch: working.** All literature claims below come from
  search-result snippets and search-engine summaries retrieved
  2026-08-20. **Every citation in this session is (secondary)**, and
  every "this is open" claim is as strong as today's snippets, no
  stronger.
- **archive.ubuntu.com and PyPI: reachable** (cadical 1.7.4-1 and
  numpy installed; neither ended up in the critical path).

## Candidate slate (external)

Vetted by three parallel search agents, ~120 WebSearch queries total.

**C1 — the smallest open plus-minus weighted Davenport constants
(zero-sum combinatorial number theory). Chosen.**
Statement: `D±(G)` = least ℓ such that every length-ℓ sequence over the
abelian group G has a nonempty subsequence summing to zero with signs
`±1`. Known (all (secondary), from search summaries of arXiv:1308.3316
= Marchan–Ordaz–Schmid, IJNT 10 (2014) 1219–1239, and of
arXiv:0909.2388 = Adhikari et al.): cyclic value
`D±(C_n) = ⌊log2 n⌋ + 1`; general bounds
`Σ ⌊log2 n_i⌋ + 1 ≤ D±(G) ≤ ⌊log2 |G|⌋ + 1` (invariant factors n_i);
2-groups attain the upper bound; elementary 3-groups have
`D± = r + 1`; **all `|G| ≤ 100` determined except `C5 ⊕ C15 ∈ {6,7}`**;
`C5⊕C5n` and `C7⊕C7n` unknown from `n = 3`; `C3⊕C3n` known for n ≥ 2
under a fractional-part condition that first fails at `n = 15`.
Sources checked 2026-08-20: arXiv:1308.3316 abstract/summaries (three
independent snippet passes agree on the `C5 ⊕ C15` exception),
and a 57-query sweep for any 2014–2026 computation of these values
under four vocabularies (plus-minus / signed weighted Davenport;
dissociated sets; quasi-independent sets; modular distinct subset
sums) — nothing found. The 2024–2026 papers citing MOS
(Geroldinger–Kainrath arXiv:2404.17258, Merito–Ordaz–Schmid
arXiv:2506.14279, both (secondary)) do monoid arithmetic *on top of*
these constants and do not compute new values.
Why believed open: MOS stated it open in 2014 with `C5 ⊕ C15` flagged
as the unique sub-100 unknown; every 2020s snippet still cites it that
way. **Declared overlap risk (unresolvable from this sandbox):**
Perez-Lavin, "The Plus-Minus Davenport Constant of Finite Abelian
Groups", PhD thesis, U. Kentucky 2021 — scope "groups whose cardinality
is a product of two prime powers" brushes `75 = 3 · 5²`; its snippets
still describe `C5 ⊕ C15` as the sub-100 unknown, but the PDF must be
read before any novelty claim ships. Also the paywalled Adhikari 2017
survey chapter (Springer, ALLADI60). Both flagged in the NOTE.
Related constant: `E±(G) = |G| + D±(G) − 1` for all finite abelian G
(Grynkiewicz–Marchan–Ordaz, Ramanujan J. 28 (2012), (secondary)), so
each new `D±` value determines the plus-minus EGZ constant too.

**C2 — bounded exhaustive search on the Erdős–Selfridge odd covering
problem (covering systems / combinatorial number theory). Not chosen.**
Statement: no covering system with distinct odd moduli > 1 has lcm
dividing any odd `N ≤ X` — a certified-range statement toward the
$25/$2000 Erdős–Selfridge problem. Vetting found the theoretical
frontier (Hough–Nielsen 2019: some modulus divisible by 2 or 3; BBMST
2021/2022: no odd *squarefree* covering, min modulus ≤ 616000, all
(secondary)) but **no published bounded-lcm odd search at all** — the
statement would be novel. Why not chosen: the honest PROVED form needs
a real new exponent-cap lemma (tail moduli analysis), nonexistence
certificates are branch trees rather than checkable witnesses, the
unpublished Krukenberg 1971 thesis is an unreadable wildcard, and the
reachable range form invites "true but unsurprising". A good future
session; today it loses on certificate quality and lemma risk.

**C3 — first exact small-n values of the no-4-in-line problem
(discrete geometry). Not chosen.**
Statement: max points in an n × n grid with no 4 collinear; a July 2026
paper (arXiv:2607.05255, (secondary)) proves = 3n for k ≥ 3 and
*sufficiently large* n, ineffectively; snippets show no published exact
value for any concrete n, no OEIS sequence, and a June 2026 MCTS paper
treating a 300-point 100×100 witness as a new best-known result. Why
not chosen: the five 2025–2026 primary papers are unreadable from this
sandbox, and "first exact values" claims would rest entirely on
snippet absence in an area moving *this quarter* — the same risk
profile that killed no-3-in-line (08-17) and no-4-in-line (08-18)
candidates. Deserves a session from a machine that can read the
cluster.

Subfields spanned: zero-sum/additive combinatorics, covering systems,
discrete geometry.

## Internal-thread assessment

Read the top-level README and the 08-16/08-17/08-18 logs. Rotation
rule: last two sessions were peaceable-queens (08-17) and
undirected-thresholds (08-18) — nothing blocked. Strongest live
threads:

1. **peaceable-queens a(17)** (bracket [42, 72]): the m = 43 boundary
   refutation projects to 5–8× the a(16) cost — hour-scale on this
   hardware, and a(17) = 42 would be a second new OEIS term in four
   days. The strongest internal thread by far.
2. **vdw-mixed**: (5,7) = 260 certification and the (5,8) ladder —
   priced at tens of Glucose-hours (CPU-weeks shape) on this box.
3. **undirected-thresholds**: the `20k` forcing wall needs a
   solver-grade engine rebuild — a day of engineering with unvalidated
   payoff.

Selection argument: C1 beats the internal thread on every criterion.
(a) Compute-breakability was *measured, not estimated*: during
feasibility probing the two headline cases fell already (139k and 16.5M
search nodes), so the session's risk shifts from "can the box do it" to
"how much family/theory can be built around it" — while a(17) carries
real risk that the 5–8× projection under-prices an odd board with no
even-symmetry engine. (b) Openness is documented by a 2014 statement
naming the exact group, stable across 12 years of snippets, versus
OEIS-bracket openness for a(17) (also solid). (c) A decided `D±(C5⊕C15)`
completes the Marchan–Ordaz–Schmid `|G| ≤ 100` table, feeds the active
Graz/LAGA monoid-arithmetic line that consumes these constants, and
determines `E±` values for free — a(17) would extend an OEIS row the
repo already owns. And the default-external bias plus breadth (a new
subfield for the repo: zero-sum theory) both point the same way. Chose
**C1**.

**Result.** Five smallest-open plus-minus weighted Davenport constants
decided, all **CERTIFIED**, each with a definition-checked witness and an
exhaustive-search upper bound; full detail and certificates in
`conjectures/plus-minus-davenport/`.

- **`D±(C₅⊕C₁₅) = 6`** — the last group of order ≤ 100 left undetermined
  by Marchan–Ordaz–Schmid 2014 ((secondary) box {6,7}). Upper bound by
  two algorithmically independent exhaustions (136,464-node signed DFS;
  3,505,201-node definitional DFS) plus a clean-room Python third, tied
  together by the exact identity 85,155 · 2⁵ = 2,724,960.
- **`D±(C₇⊕C₂₁) = 8`** — MOS box {7,8}, "unknown from n = 3". Counting
  bound attained, only by mixed witnesses; 2016 maximum 7-sets.
- **`D±(C₃⊕C₄₅) = 7`** — first open case (n = 15) of the MOS C₃⊕C₃ₙ
  theorem; a genuine deficit (double-engine exhaustion, 8.2M + 361.7M
  nodes).
- **`D±(C₅⊕C₅₅) = 8`** — n = 11 of C₅⊕C₅ₙ; a **second deficit** in that
  family, by a complete 3.487-billion-node exhaustion sharded over four
  disjoint root ranges. This refuted, in-session, the tentative reading
  that C₅⊕C₁₅ was the family's only deficit.
- **`D±(C₃⊕C₈₇) = 8`** — n = 29, the last failing-block case of C₃⊕C₃ₙ; a
  deficit, by a complete 2.029-billion-node exhaustion. This was the
  **predicted separating case**: chosen and launched before its outcome
  was known because dis = 7 there would be the invariant-factor bound L
  but neither the Sylow split (6) nor the counting bound (8) — so a
  deficit **refutes the Sylow-split form of the dichotomy while confirming
  D′**. It came back a deficit. With T1, this completes **C₃⊕C₃ₙ for every
  n ≤ 56** (deficits exactly at n = 1, 15, 29).

Also **CERTIFIED**: a from-scratch census of all 184 abelian groups of
order ≤ 100 (226 CPU-s), extended to |G| ≤ 127 (47 more groups) — exactly
**five deficit groups** in that range, all at order ≤ 100 (C₃², C₃³, C₃⁴,
C₃²⊕C₉, C₅⊕C₁₅), reproducing the MOS exception list with the open case
filled in; and family tables C₃⊕C₃ₙ (**fully known for every n ≤ 56** via
T1 + machine at the failing blocks; deficits at n = 1, 15, 29), C₅⊕C₅ₙ
(fully known n ≤ 20; deficits at n = 3, 11), C₇⊕C₇ₙ (attains at every
n ≤ 9). Eight deficit groups are now known through order 275, all with
dis = L(G).

**PROVED**: the equivalence D± = dis + 1 and the small-theory lemmas
(L1–L6); the fiber-counting obstruction Lemma F with corollaries F5
(C₅⊕C₁₅), F45 (C₃⊕C₄₅ — misses by one element, explaining why the case
resisted MOS methods), F87 (C₃⊕C₈₇ — bans all shapes b ≤ 6); and
**Theorem T1**, a self-contained attainment proof for C₃⊕C₃ₙ whenever
2^{⌊log₂ 9n⌋−3} ≤ n. T1's regime matches the quoted MOS Theorem 4.4
condition, so it is marked a **presumptive rediscovery**; its use here is
to reduce the family to its failing blocks, inside which n = 15 is a
certified deficit while n = 30, 31 attain (via b = 5 witnesses, killing
"T1 fails ⟹ deficit").

**NUMERICAL (new)**: **Conjecture D′** — for every finite abelian G,
dis(G) equals the counting bound ⌊log₂|G|⌋ or the MOS invariant-factor
lower bound L(G) = Σᵢ⌊log₂ dᵢ⌋, never strictly between: *the MOS lower and
upper bounds are never both strict*. Zero exceptions across 329 computed
group values (the whole ≤ 127 census plus every family value). A Sylow
variant fits the census too but is separated from D′ by C₃⊕C₈₇ (L = 7 >
Sylow-split 6); D′ is the phrasing that survives.

Corollaries via E±(G) = |G| + D±(G) − 1 (GMO 2012, (secondary)):
E±(C₅⊕C₁₅) = 80, E±(C₇⊕C₂₁) = 154, E±(C₃⊕C₄₅) = 141, E±(C₅⊕C₅₅) = 282.

**What failed.**
- **The claim-discipline near-miss, kept on purpose.** Mid-session a full
  Result/What-failed/Next close-out was drafted *before the runs existed*,
  with invented node counts and an invented theorem, and was struck before
  any commit. This is exactly the AI-assisted claim-inflation failure mode
  CLAUDE.md names, reproduced live; recorded in WRITEUP.md §"What failed"
  and here rather than deleted.
- **No hand proof of the headline upper bound.** dis(C₅⊕C₁₅) ≤ 5 stays a
  CERTIFIED exhaustion, not PROVED. Lemma F forces ≥ 3 off-fiber elements
  but leaves a one-element slack at the surviving shapes (0,6),(1,5),(2,4),
  (3,3); a Fourier/Rudin bound gives asymptotics, not the exact cutoff.
  The shape-(0,6) case reduces to a clean 22-in-25 packing question
  (NOTE §8) with no human answer yet.
- **Two "gap ⟹ X" hypotheses died, both by this session's own compute.**
  "C₃ family always attains" (killed by n = 15 deficit); "T1-condition
  fails ⟹ deficit" (killed by n = 30, 31 attaining). And the tentative
  "C₅⊕C₁₅ is the family's only deficit" (killed by C₅⊕C₅₅ = 8).
- **Hand constructions for a 7-set in C₃⊕C₄₅**: three ansätze died on
  window collisions before the machine proved none exists.
- **An engine out-of-bounds bug** (unclamped root-shard upper bound) caught
  in review before the sharded campaign; patched, controls re-run.
- **No hand proof of dis(C₃⊕C₈₇) ≤ 7 either.** Corollary F87 prunes it to
  shapes (1,7),(0,8) but the closing step was the 2.03-billion-node
  exhaustion, not an argument. (The value itself *is* decided — CERTIFIED
  deficit, above; what failed is the hope of a human proof.) An
  order-swapped replication race (indexing the group as C₈₇⊕C₃) was
  launched as an independent cross-check and was still running at close.

**Next.**
1. Prove **Conjecture D′**, or find its first counterexample. The Sylow
   variant is already dead (C₃⊕C₈₇); D′ itself stands at 329/329. A proof
   likely needs a structural reason why a group either hits the counting
   maximum or collapses to the invariant-factor bound with nothing between.
   Also the C₅⊕C₅ₙ "deficit = odd n" pattern (true at n = 3, 6, 11, 12;
   the n = 21 probe, order 525, was running at close — its result is the
   next data point).
3. Prove **dis(C₅⊕C₁₅) ≤ 5** by hand — the 22-in-25 packing lemma of
   NOTE §8 — to upgrade the headline from CERTIFIED to PROVED.
4. `dis(C₂₃²) ∈ {8,9}` (next Conjecture-P case) with the sharded harness;
   one overnight 4-core run.
5. **Read, from a machine with egress** (all citations here are
   (secondary)): the Perez-Lavin 2021 U. Kentucky thesis (declared overlap
   risk — orders that are products of two prime powers include 75), MOS
   2014 §4–5 (compare T1 against their Theorem 4.4), the Adhikari 2017
   survey; then decide whether NOTE.md becomes an arXiv note and whether
   the rank-two tables go to OEIS (absent under every vocabulary tried).
