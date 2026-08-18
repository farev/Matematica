# 2026-08-18 — undirected-thresholds

**Target.** Prove a new case of the Currie–Mol conjecture on the undirected
repetition threshold: `URT(k) = (k−1)/(k−2)` for `k ≥ 4`, known for
`4 ≤ k ≤ 21` (Currie–Mol 2019/2021), open for every `k ≥ 22`. Today's target
is `k = 22`: construct an infinite word over 22 letters containing no
*undirected power* `x y x′` (`x′ ∈ {x, x^R}`) of exponent `> 21/20`, with a
machine-checkable proof. Route: binary Pansiot-code morphisms at `n = 22`
with threshold `α = 21/20 = RT(21)` — the code machinery this repository
built and proved for circular thresholds (Lemmas S/F/T, Theorem MC,
`conjectures/circular-thresholds/NOTE.md` §11–§14) — extended by a new exact
*reversal* transfer lemma and an undirected preservation criterion for
reversal-closed morphism pairs (`φ_1 = rev(φ_0)`). If the criterion lands and
the search finds a certified pair, the session yields a PROVED theorem
`URT(22) = 21/20` (equality quoting Currie–Mol's lower bound, (secondary)).

**Branch note.** The session mandate asks for `claude/<conjecture>-YYYY-MM-DD`;
this environment designates `claude/kind-bohr-8wfcqn` and forbids pushing
elsewhere. Working on the designated branch, as previous cloud sessions did.

## Connectivity check

- **WebFetch: fully blocked** (EGRESS_BLOCKED from the sandbox proxy), tested
  2026-08-18 against arxiv.org, oeis.org, erdosproblems.com,
  mathoverflow.net, and a non-list academic host (cfc.nankai.edu.cn). No
  primary source was readable from this session.
- **WebSearch: working.** All literature claims below come from search-result
  snippets retrieved 2026-08-18. **Every citation in this session is
  (secondary)**, and every "this is open" claim is as strong as today's
  snippets, no stronger.

## Candidate slate (external)

**C1 — URT(22), the undirected repetition threshold (combinatorics on
words). Chosen.**
Statement: an undirected `r`-power is a word `x y x′` with `x` nonempty,
`x′ ∈ {x, x^R}`, `|xyx′|/|xy| = r`; `URT(k)` is the infimum of `r` such that
undirected `r`-powers are avoidable over `k` letters. Currie–Mol:
`URT(3) = 7/4`; `URT(k) ≥ (k−1)/(k−2)` for `k ≥ 4`; conjecture
`URT(k) = (k−1)/(k−2)` for `k ≥ 4`, confirmed for `4 ≤ k ≤ 21`.
Sources checked 2026-08-18 (all secondary, via snippets): arXiv:1904.10029
"The undirected repetition threshold" (Currie–Mol, WORDS 2019); its extension
arXiv:2006.07474 = TCS 2021 "The undirected repetition threshold and
undirected pattern avoidance" ("we confirm this conjecture for
k ∈ {4,5,…,21}", with binary morphisms `f_k : Σ_2* → Σ_2*`); Shur,
"Non-Constructive Upper Bounds for Repetition Thresholds" (ToCS, Aug 2024)
treats undirected repetitions asymptotically ("(1+1/d)-powers avoidable over
d+O(1) letters") and does not decide any individual `k`. No 2022–2026 hit
extends the confirmed range past 21.
Why believed open: the 2021 paper states the conjecture open for `k ≥ 22`;
the 2024 paper still cites it that way; no newer extension surfaced in
today's searches.

**C2 — plus–minus weighted Davenport constant `D±(C_5 ⊕ C_15)` (zero-sum
combinatorial number theory). Runner-up.**
Statement: least `ℓ` such that every sequence of `ℓ` elements of
`C_5 ⊕ C_15` has a nonempty subsequence summing to zero with coefficients in
`{+1, −1}`. A snippet of the literature around Marchan–Ordaz–Schmid
(arXiv:1308.3316, 2013) records that for `D±(C_5 ⊕ C_5n)` and
`D±(C_7 ⊕ C_7n)` "the value is unknown already for n = 3". Order-75 group,
plausibly decidable by exhaustive search with automorphism and sign-symmetry
reduction on this box, with a full certificate.
Why not chosen: the openness statement is from a 2013 paper and the ± weighted
area is active (arXiv:2404.17258 in 2024, arXiv:2506.14279 in 2025 on
adjacent monoid-arithmetic questions); with primary sources unreadable I
cannot rule out that the constant has since been computed. Lower ceiling than
C1 (a CERTIFIED constant vs a PROVED threshold case).

**C3 — exact small-`n` values for the no-4-in-line problem (discrete
geometry). Not chosen.**
Statement: the maximum number of points in an `n × n` grid with at most 3 on
any line. A July 2026 paper (arXiv:2607.05255, "No-(k+1)-in-line problem for
k ⩾ 3") proves the maximum is exactly `kn` for `k ≥ 3` and *sufficiently
large* `n`; exact values for small `n` would complement it and are
CP-SAT-decidable at small sizes.
Why not chosen: there is a dense 2025–2026 cluster on exactly this problem
(arXiv:2502.00176, 2510.17743, 2606.02843, 2601.14465) and none of it is
readable from this sandbox; the risk that small-`n` tables already exist in
one of those five papers is high and undecidable from snippets alone.

Subfields spanned: combinatorics on words, zero-sum/combinatorial number
theory, discrete geometry.

## Internal-thread assessment

Read the 08-12/08-13 logs and conjecture READMEs. Rotation rule: last two
sessions were signed-difference-sets (08-12) and distinct-subset-sums
(08-13) — no conjecture is at two consecutive sessions; nothing is blocked.
Strongest live threads:

1. **distinct-subset-sums** — resume the `a(10)` sweep past `m = 262`, or
   build the multi-`m` deficiency-vector engine (NOTE §6.2, projected 5–10×).
   Resuming without the new engine buys ~10 more values of `m` in a session
   (CPU-months to finish): the excluded "extend by 10%" shape. The new
   engine is a full session of engineering with unvalidated payoff, on a
   conjecture worked yesterday (08-13). Today's search also surfaced an OEIS
   comment (secondary) that `a(12) ≤ 1157 < 1164 = A005318(12)` — someone is
   actively moving the `n = 12` frontier, worth reading properly some session.
2. **signed-difference-sets** — port Masselot's layered-refinement quotient
   ladder into `sds_search.c` and attack the smallest Open cells at order
   > 36; README prices the flat-DFS version at ~2 CPU-weeks; the port is a
   day of new code with real but incremental payoff (more census rows).
3. **generalized-schur** — the `(4,4,u)` ladder, still blocked on the
   DRUP-in-RAM toolchain (pysat OOM at 15 GB; no kissat installable with
   egress blocked). Unchanged since 08-07.

None beats C1 on the selection criteria: C1's bottleneck is a bounded search
plus two provable lemmas with in-house precedent (the exact shape that
settled `CRT_W(6)` on 08-06); its openness trail is as clean as snippets
allow; and the result would extend a named, active conjecture rather than
add rows to a census. Default-external applies and the argument is not
close. Chose **C1**.

What counts as achieving it: a fully certified morphism pair + seed whose
fixed point is proved undirected-`(21/20)⁺`-free over 22 letters — that is,
`URT(22) ≤ 21/20`, hence `= 21/20` with the (secondary) lower bound. Partial
grades that still count: the reversal-transfer machinery PROVED with a
CERTIFIED exhaustive negative over a stated ansatz/range (the honest analog
of session-1 circular-thresholds), or certified long finite
undirected-free words as NUMERICAL/CERTIFIED evidence. Mid-session
checkpoint: if no certified pair by mid-session, either relax the ansatz
(palindromic pair `ρ = id`, larger `k`, two-level morphisms) or write up the
machinery + negative and say so plainly.

**Result.** _(session in progress — filled at close)_

**What failed.** _(filled at close)_

**Next.** _(filled at close)_
