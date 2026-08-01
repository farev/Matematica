# 2026-08-01 — additive-squares

**Target.** The Pirillo–Varricchio / Halbeisen–Hungerbühler problem: is there an
infinite word over a finite subset of ℤ containing no two adjacent equal-length
blocks with equal sums (an "additive square")? Open since the 1990s. It looked
tractable for a session because the arithmetic is exact integer arithmetic (so
results are certifiable, not merely suggestive), the search decomposes cleanly,
and — as vetting confirmed — there is **no published table of exact maxima** for
any integer alphabet and **no classification of four-letter alphabets** for
squares, only for cubes.

**Result.** PROVED: a **Quotient Lemma** — additive-square-freeness depends on an
alphabet only through its relation lattice Λ(A), and quotienting by any
sublattice M ⊆ Λ(A) can only increase L, so `L(A) ≤ L(A_M)` where `A_M` is a
canonical alphabet of integer *vectors*. One finite computation therefore bounds
L for every alphabet realising a given integer relation. Consequences: PROVED
`L(A) = 7` for **every** three-element alphabet in characteristic 0 (uniform
witness `0,1,0,t,0,1,0`, twelve hand-checked inequalities, plus a 354-node
search); PROVED-reduction + CERTIFIED-constant `L(A) ≤ 60` for every four-element
alphabet with a+d=b+c — which is **Freedman's published bound, reproduced
clean-room in three lines** from the single relation (1,1,−1), the constant
falling out of a 7,707,828-node tree closure. CERTIFIED: that bound is
**attained** — `L({0,1,5,6}) = 60`, with 29 alphabets in the sweep reaching it.
CERTIFIED: exact L for 34 four-letter integer alphabets — `L({0,1,2,3}) = 50`,
`L({0,1,2,4}) = 62`, `L({0,1,2,5}) = 86`, `L({0,1,3,5}) = 88` — apparently the
first such table. CERTIFIED structural observation: node counts saturate at
exactly 7,707,828 from `{0,1,9,10}` onward, i.e. a spread-out integer alphabet's
search tree becomes *literally identical* to the universal quotient alphabet's.
Negative and interesting: among primitive relation classes of sup-norm ≤ 2,
(1,1,−1) is so far the **only** one whose tree closes — the 3-term-AP class
(1,1,0) reached ≥ 440 and a+b+c=0 reached ≥ 996 without closing. **Nothing here
resolves PVHH, and nothing claims to.**

**Connectivity check.** arxiv.org, oeis.org, erdosproblems.com and
mathoverflow.net were **all blocked** at the egress proxy (HTTP 403 on CONNECT,
confirmed by both WebFetch and curl; `recentRelayFailures` empty, so it is
policy, not failure). Web **search** worked and was the only literature channel.
**No primary source was read this session.** Every citation in `NOTE.md` §7 is
marked (secondary). Freedman's venue is unresolved between two candidates and is
flagged as such.

**The three-candidate slate.**
1. *No-three-in-line* (discrete geometry): is there a 2n-point subset of the
   n×n grid with no three collinear? Source checked: search snippets of
   Flammenkamp's chronology + arXiv listings, 2026-08-01. Believed open for
   n = 47 for ~30 years. **This was wrong, and vetting caught it**: n = 47 fell
   in September 2025 (Prellberg), and by 20 July 2026 solutions were known for
   all n ≤ 70 plus 72 and 74 (Prellberg; Heule), via symmetry-restricted CP-SAT
   and a purpose-built SAT solver on HPC. Dead as a target; dropped.
2. *Odd covering systems* (Erdős–Selfridge, combinatorial number theory): does a
   covering system exist with distinct odd moduli > 1? Source: search snippets
   of erdosproblems.com tag pages and arXiv:1901.11465, 2026-08-01. Confirmed
   open; Hough–Nielsen and Balister–Bollobás–Morris–Sahasrabudhe–Tiba have
   narrowed it to "some modulus divisible by 9 or 15". Dropped: the remaining
   gap needs Hough's distortion method, and reconstructing a delicate argument
   from snippets with no access to the papers is the bottleneck-of-ideas case
   that compute does not touch.
3. *PVHH / additive squares* (combinatorics on words). Source: search snippets
   of arXiv:1106.5204, arXiv:2506.21200 (Vukusic, Amer. Math. Monthly 2025,
   which calls it open), arXiv:2408.15390, 2026-08-01. Confirmed open. Selected.

**Internal-thread assessment.** The strongest live internal thread is Gilbreath
**Open Lemma R3.11** (persistent-alignment cost for slow crossings) — the single
analytic statement separating the current noose from a theorem that generic-strip
sequences seal the lead. Significant progress would change the Gilbreath row.
It lost on criterion (a): R3.11 needs a renewal argument, not cycles, and the
previous session had already measured everything measurable and isolated the
missing step as analytic. Chowla's and Erdős–Gyárfás's named next steps both
begin "fetch primary sources from an unblocked network", which this sandbox
cannot do. Three consecutive Gilbreath-family sessions had already run
(07-28, 07-29 ×2), so the standing rule sends this one elsewhere regardless.
External won on (a) compute-breakable bottleneck, (b) two vetted gaps in the
literature, (c) it extends Freedman and is the square analogue of
Lietard–Rosenfeld's cube classification — where it would be cited.

**What failed.**
- *No-three-in-line*, the initially-preferred target: premise eleven months
  stale. Cost was ~10 minutes because it was vetted by a subagent **in parallel**
  with building, not after.
- *A `strtok` nesting bug* in the vector searcher: the inner tokenizer clobbered
  the outer one's static state, so only the first letter of each alphabet parsed
  and every search returned L = 1. Caught by running the d=1-reproduces-scalar
  sanity check first on the new binary. Fixed with `strtok_r`.
- *The cell-decomposition plan was overkill and was discarded.* The original
  route to the degenerate family was to enumerate ~2,200 exceptional rationals
  t = −P/Q with |P|,|Q| ≤ 60 and exhaust each. Most of the scaffolding was
  written before I noticed the Quotient Lemma's linear map does it in one line
  with no case analysis.
- *No second Freedman-type class was found.* The natural next relations —
  (1,1,0) and (1,1,1) — give long words, not short ones, and did not close.
  So the session produced exactly one finite relation class: the known one.
- *Budget-limited lower bounds are not measurements.* The sweep's
  L ≥ 111/134/290/350 figures are artifacts of a fixed node budget, recorded as
  certified lower bounds and explicitly disclaimed as growth data.
- *Theorem 4 is very likely folklore* and is presented as such; it is included
  because it calibrates the method, not as a contribution.

**Next.** Settle whether the 3-term-AP class v = (1,1,0) has L(A_v) = ∞ — a deep
run on the neighbouring class v = (2,1,0) already reached the 3,000 depth cap
without a square, so an infinite class probably exists, and Rao–Rosenfeld's ℤ²
result says it should. Knowing *which* relations are infinite is what decides
whether the Quotient Lemma can reach PVHH for four letters at all. Then: find a
proof, rather than a 7.7-million-node tree closure, that (1,1,−1) forces
finiteness — it would likely generalise. And from an unblocked network, verify
Freedman's paper and venue, check Ochem's heuristic page, and check whether the
Quotient Lemma and the exact values are already in the literature; until then
every novelty claim here stays hedged.
