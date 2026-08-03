# 2026-08-03 — circular repetition thresholds

**Target.** The Currie–Mol–Rampersad conjecture `CRT_I(n) = CRT_W(n) = RT(n)`
for circular words, open for `4 ≤ n ≤ 44` in the weak form and for every
`n ≥ 4` in the intermediate form. It looked tractable because the open region
is a *finite* list of alphabet sizes, each case is a search rather than an
idea, and — decisive given the connectivity situation below — the whole
problem can be stated from scratch and calibrated against two independently
reported published constants without reading a paper.

**Result.** **PROVED** — Lemma A (circular pumping): a `q`-uniform
`α⁺`-free-preserving morphism carries `S_2(n,m)` into `S_2(n,qm)`, where `S_2`
widens the circular factor window by exactly two letters; hence one morphism
plus one seed gives circular threshold words at every length `q^j m_0`, and
`CRT_W(n) = RT(n)` becomes **decidable by two finite searches** (Theorem C).
**PROVED** — Theorem N′ (computer-assisted): for `4 ≤ n ≤ 9` **no**
shift-equivariant `q`-uniform morphism over `Z_n` has an `RT(n)⁺`-free fixed
point, for **any** `q`. The reduction is Proposition N (such a morphism forces
a difference set of size `≤ 2`, vacuous at `n = 3` and fatal above it) plus
Result L (an `RT(n)⁺`-free word with only two distinct consecutive differences
has length at most `11, 8, 14, 10, 18, 12` for `n = 4…9`, exhaustively), which
kills every large `q`, while the exhaustive morphism searches kill every small
one. **PROVED but expected to be a rediscovery** — Theorems M/M′,
finite criteria for a uniform morphism to preserve `α⁺`-freeness. **CERTIFIED**
— circular threshold spectra for `n = 3,4,5,6`, including the unexpected late
exceptional lengths `m = 147, 154` at `n = 4` after an unbroken run `114…146`;
plus an exhaustive negative (no shift-equivariant morphism satisfies (H1)–(H4)
at `n = 4..8` over the `q` ranges searched). **No open case was settled.**

**What failed.** The main attack. Both morphism searches came back empty for
every `n ∈ [4,8]`; two pumping ideas that avoid morphisms died on the data or
on the shape of the problem. Details in §3 of
[`WRITEUP.md`](../conjectures/circular-thresholds/WRITEUP.md); the short
version is below under *Attack and failures*.

**Next.** Redo the Theorem C search in **Pansiot's encoding** of `n`-ary
threshold words, where the morphisms need not be shift-equivariant over `Z_n`
and Proposition N does not apply. Theorem C applies verbatim to any morphism
found there; a single hit plus a seed settles an open case of the conjecture.

---

## 1. Connectivity check

| source | reachable | how |
|---|---|---|
| `arxiv.org` (and `export.arxiv.org`) | **no** — HTTP 403 from the egress proxy | WebFetch, curl |
| `oeis.org` | **no** — HTTP 403 | WebFetch, curl |
| `erdosproblems.com` (and the `teorth.github.io` mirror) | **no** — HTTP 403 | WebFetch, curl |
| `mathoverflow.net` | **no** | WebFetch |
| `api.crossref.org` | **no** — HTTP 403 | curl |
| web search tool | **yes** | returns titles, URLs and synthesized summaries |
| `pypi.org` | yes (proxy bypass list) | `pip install` worked |

The proxy status endpoint reports the denials as organization egress policy,
not TLS or configuration failures, so they were not retried or routed around.

**Consequence, stated prominently as the mandate requires: no primary source
was opened at any point today.** Every citation in every document from this
session is marked **(secondary)**, and every "this is still open" claim is
unverified against the actual paper. The response was to choose a problem
whose mathematics is fully self-contained, and to calibrate the computational
pipeline against *published constants reported in search summaries* before
making any claim — see §4.

## 2. The three external candidates

Built by three parallel subagent surveys (words; number theory / additive
combinatorics; games and finite search) plus my own probes on covering systems
and cap sets. Spanning three subfields.

### E1 — Circular repetition thresholds *(combinatorics on words)* — SELECTED

*Statement.* For circular words define `CRT_W(n)`, `CRT_I(n)`, `CRT_S(n)` as
the infimum of exponents `β` such that `β`-free circular `n`-ary words exist
at infinitely many lengths / all large lengths / all lengths. Conjecture
(Currie, Mol, Rampersad): `CRT_I(n) = CRT_W(n) = RT(n)` for all `n ≥ 4`.

*Source.* Mol & Rampersad, *The weak circular repetition threshold over large
alphabets*, arXiv:1912.11388, RAIRO-ITA 54 (2020). Seen 2026-08-03 via search
summary of `https://arxiv.org/abs/1912.11388`, quoting: "we prove that
`CRT_W(n)=RT(n)` for all `n≥45`… the conjecture that `CRT_W(n) = RT(n)`
remains open for all `4 ≤ n ≤ 44`, and the stronger conjecture that
`CRT_I(n) = RT(n)` remains open for all `n ≥ 4`." Companion:
Currie & Mol, arXiv:1803.08145, EJC 26(2) (2019), `CRT_S(4)=3/2`,
`CRT_S(5)=4/3`; Gorbunova, EJC 19(4) (2012). **(secondary)**

*Why still open.* The 2020 paper states it; two independent searches (mine and
a subagent's) found no 2021–2026 item closing small `n`. The subagent put
confidence at ~80%, flagging six years of silence as the main risk.

### E2 — Size-4 Sidon sets extending to no perfect difference set *(number theory)*

*Statement.* Erdős asked whether every finite Sidon set embeds in a perfect
difference set; it is false. Open: is the minimum size of a non-embeddable
Sidon set 4 or 5? Concretely, does `{0,1,3,11}` (or `{1,2,4,8}`) lie in no
cyclic planar difference set of **prime-power** order?

*Source.* Alexeev & Mixon, arXiv:2510.19804 / PNAS (size 5, `{1,2,4,8,13}`,
Lean-formalised; and size 4 for prime moduli); Niu, arXiv:2604.25214 (Apr
2026), "empirical evidence for size-4 counterexamples" — checks the Singer
affine-orbit condition for every prime power `q ≤ 317` and every modulus
`v ≤ 133`, and says a complete proof is open. Seen via search summaries.
**(secondary)**

*Why still open.* The April-2026 title is literally "empirical evidence"; no
later item surfaced. Note `erdosproblems.com` marks #707 itself *solved*, so
the residual question is under-watched.

### E3 — Steiner systems `S(2,6,v)` for undecided `v` *(design theory)*

*Statement.* For which `v` satisfying the divisibility conditions does a
`2-(v,6,1)` design exist? 27 values remain undecided after
`S(2,6,226)` and `S(2,6,441)` were constructed; smallest open `v = 51`.

*Source.* Banakh, Hetman & Ravsky, *Steiner systems S(2,6,226) and S(2,6,441)
do exist!*, arXiv:2511.05191, which quotes the 29-value undecided list; Hetman
arXiv:2604.04975 (Apr 2026) resolves further cases for `k = 7, 8`. Seen via
search summaries. **(secondary)**

*Why still open.* The April-2026 paper states the remaining counts as live.

## 3. The internal thread

The repository's strongest live thread is **Gilbreath, Open Lemma R3.11**
(`conjectures/gilbreath/R3.md` §7): a persistent-alignment / renewal estimate
showing that occupying column `W−j` on an unbounded set of rows costs `j`
affine parity equations, giving `P(penetration ≥ j) ≤ C·2^{−cj}` uniformly in
time. It is named as "the single analytic core separating the noose from a
theorem", so proving it *would* change that conjecture's row in the top-level
README — it is a genuine significant-progress target.

**Assessment against the selection criteria.** (a) R3.11 is an
anti-concentration statement about an adversarially scheduled process; it is a
bottleneck of *ideas*, and the surrounding numerics are already done — four
CPU cores buy nothing. (b) Novelty is not in doubt, but neither is difficulty:
one full session already reduced the problem to exactly this lemma and
stopped. (c) It would extend the repository's own Chase–Hunter–Tao line.
E1 beats it on (a) decisively — E1's bottleneck is a search that a few CPU
hours can actually execute — and the mandate's default is external in any
case. Gilbreath was also the subject of three of the seven logged sessions.
**Selected: E1.**

### Selection argument among the externals

- (a) *Compute-breakable?* E1 yes: per-case existence is a SAT instance, and
  the infinitary step reduces (via Lemma A, found today) to a finite morphism
  search. E2 yes but incremental — extending `q ≤ 317` is a certified sweep,
  not a proof. E3 yes, and a hit is self-certifying, but the search is a
  Kramer–Mesner run whose obvious cases are being harvested by an active group
  at ~4 papers/year.
- (b) *Already done?* E3 has the highest duplication risk (live competition).
  E2's frontier is explicitly stated and would be a clear extension. E1's
  per-length spectra at the *Dejean* threshold do not appear in any summary I
  saw, and if they were known the conjecture would be better informed.
- (c) *Whose work does it extend?* E1 extends Mol–Rampersad and
  Currie–Mol–Rampersad directly, and would be cited in the circular-words
  literature. E2 extends Alexeev–Mixon/Niu. E3 extends Banakh–Hetman–Ravsky.

E1 also has a property the others lack and that mattered a great deal with the
library closed: **it can be calibrated against published constants without
reading a paper.** `CRT_S(4), CRT_S(5), CRT_S(6), CRT_S(7)` and `CRT_I(3)` are
each a prediction my code must reproduce, and all five did (§4).

**The result attempted today.** Prove `CRT_W(n) = RT(n)` for at least one
`n ∈ [4,44]` by exhibiting an infinite family of circular `n`-ary threshold
words. Success would mean: a uniform morphism `h` on `n` letters proved to
preserve `RT(n)⁺`-freeness by a finite check, plus one circular seed word,
together yielding threshold words at every length `q^j m_0` — settling an open
case of the Currie–Mol–Rampersad conjecture.

## 4. Calibration before any claim

| prediction (secondary) | what the code must show | outcome |
|---|---|---|
| `CRT_S(4) = 3/2` | at `α = 3/2`, `n = 4`: every length `1…60` realizable | all 60 ✓ |
| `CRT_S(5) = 4/3` | at `α = 4/3`, `n = 5` | all 60 ✓ |
| `CRT_S(6) = 4/3` | at `α = 4/3`, `n = 6` | all 60 ✓ |
| `CRT_S(7) = 5/4` | at `α = 5/4`, `n = 7` | all 60 ✓ |
| `CRT_I(3) = RT(3) = 7/4` | at `α = 7/4`, `n = 3`: cofinite spectrum | exceptions exactly `{5,7,9,10,14,16,17,22}` in `1…300` ✓ |
| the whole pipeline | re-derive the known `CRT_W(3) = 7/4` end to end | done, verified at lengths 20, 560, 15 680, 439 040 ✓ |

Additionally: SAT witnesses re-verified by a from-the-definition `O(m³)`
checker; the vectorised checker cross-validated against the naive one on 700
random words (0 mismatches); (H1)–(H4) verified by two implementations sharing
no code (C and Python) with identical verdicts.

## 5. Attack and failures

1. **Shift-equivariant morphism search under full (H1)–(H4).** Exhaustive over
   all `α⁺`-free `h_0 ∈ Σ_n^q` with `h_0[0]=0`. Zero hits: `n=4 (q ≤ 60)`,
   `n=5 (q ≤ 68)`, `n=6 (q ≤ 51)`, `n=7 (q ≤ 44)`, `n=8 (q ≤ 37)` — against
   hits from `q = 25` at `n = 3`. Millions of candidates; (H4) did the killing.
2. **Approach changed, not retried: the relativised Lemma A with
   `X = Fac(h^ω(0))`,** which needs only Theorem M′ ("the fixed point has no
   short over-exponent factor") instead of preservation on all words. It
   recovered the `n = 3` morphisms, and for `n ≥ 4` failed *earlier*: the
   cheapest necessary condition was met by **zero** candidates at
   `n = 4, 5, 6, 7`, at every `q` searched.
3. **That failure was diagnosed into a theorem.** Every violation sat at the
   seam with period `≤ n−2`, which is exactly the regime where `RT(n)`-freeness
   forces distinct letters — giving Proposition N (`|D| ≤ 2`), vacuous at
   `n = 3` and severe at `n ≥ 4`. Asking how long such a two-difference word
   can be (Result L: at most 11, 8, 14, 10, 18, 12 for `n = 4…9`) then closed
   every large `q`, upgrading a bounded "none found" to Theorem N′: **none
   exists, at any `q`, for `4 ≤ n ≤ 9`**. This is the one place today where
   being stuck paid.
4. **Two morphism-free pumping ideas, both dead.** A closure property of the
   spectrum (killed immediately by the data: `5, 10 ∈ C(5)` but `20 ∉ C(5)`),
   and exploiting the `β > RT(n)` slack (needs a *uniform family* over
   `β_k ↓ RT(n)`, which is the shape of the published `n ≥ 45` proof, not an
   afternoon's object).

**Mid-session checkpoint.** Taken after step 1 returned empty across five
alphabets: the pivot was to weaken the morphism hypothesis (step 2) rather
than to change problem, on the grounds that the reduction (Lemma A) was
already proved and only its input was missing. When step 2 also failed, the
budget went to diagnosing *why* — which produced Proposition N, the session's
second theorem — rather than to a third search.

## 6. Cost

4 cores, 15 GB RAM. SAT instances sub-second to a few seconds each up to
`m ≈ 300` (`n = 4` is the slow case). Morphism sweeps: minutes per alphabet,
up to ~9×10⁶ candidates scanned per `q`-range. No randomness affects any
claim; the one seeded diagnostic uses `random.seed(3)` / `random.seed(11)`.

**Known defect carried forward:** UNSAT verdicts rest on SAT solvers with no
DRAT proof emitted or checked. The load-bearing ones — the `n = 4` late gaps
and their neighbours, `m = 113, 146, 147, 148, 153, 154, 155` — were re-decided
by three independent backends (Cadical, Glucose, MiniSat) with identical
verdicts and no disagreement: `m = 147` UNSAT at 209 s / 343 s / 207 s and
`m = 154` UNSAT at 249 s / 632 s / 298 s, against neighbours decided in
seconds. Script `crosscheck.py`, transcript `data/crosssolver_n4.log`. The
bulk of the sweep was decided once. Satisfiable verdicts are fully
independent.
