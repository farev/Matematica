# Session narrative — 2026-08-01, additive squares

Written as it happened, including the parts that were wrong. Not edited to look
smarter in hindsight.

## How this problem got picked

The session opened with a connectivity check, and it failed in an informative
way: `arxiv.org`, `oeis.org`, `erdosproblems.com` and `mathoverflow.net` all
returned HTTP 403 at the egress proxy's CONNECT layer, confirmed by `curl` as
well as by the fetch tool. Web **search** worked. So the session had
search-snippet access to the literature and no primary sources at all. That
constraint shaped everything: it ruled out "audit a recent paper" as a session
type, and it made "verify open status before spending hours" the single highest
-value early move.

Three external candidates were assembled, spanning three subfields:

1. **No-three-in-line** (discrete geometry): is there a `2n`-point subset of the
   `n × n` grid with no three collinear? The state of the art I had in memory,
   and which search initially confirmed, was "all `n ≤ 46`, plus 48, 50, 52",
   with `n = 47` open for ~30 years — an attractive record to chase, verifiable
   in exact integer arithmetic.
2. **Odd covering systems** (Erdős–Selfridge, combinatorial number theory): does
   a covering system exist with distinct odd moduli > 1? Confirmed open;
   Hough–Nielsen and Balister–Bollobás–Morris–Sahasrabudhe–Tiba have narrowed it
   to "some modulus divisible by 9 or 15".
3. **PVHH / additive squares** (combinatorics on words): is there an infinite
   word over a finite subset of `ℤ` with no two adjacent equal-length blocks of
   equal sum? Confirmed open as of 2026.

A subagent was sent to vet (1) properly while I probed (3). **That vetting
saved the session.** The no-three-in-line premise was eleven months stale:
`n = 47` fell in September 2025 (Prellberg), and by July 2026 solutions were
known for all `n ≤ 70` plus 72 and 74, driven by purpose-built CP-SAT and by
Heule's SAT solver on HPC. Attacking `n = 47` with generic search would have
burned the whole session on a solved problem. The lesson is not subtle: on a
record-chasing target, vet the record *first*, and in parallel.

Candidate (2) was dropped for a different reason — the machinery
(Hough's distortion method) is heavy, the remaining gap is narrow, and with no
access to the papers I would have been reconstructing a delicate argument from
snippets. That is exactly the bottleneck-of-ideas case that compute does not
touch.

So: additive squares. The bottleneck there is genuinely computational, the
arithmetic is exact integer arithmetic throughout (so results are certifiable
rather than merely suggestive), and — as the second vetting agent established —
there is **no published table of exact `L(A)` for any integer alphabet** and
**no classification of four-letter integer alphabets for squares** (only for
cubes, by Lietard–Rosenfeld). Two clean gaps.

## The internal alternative

The repository's own strongest live thread is Gilbreath **Open Lemma R3.11**
(persistent-alignment cost for slow crossings) — the single analytic statement
separating a noose from a theorem that generic-strip sequences seal the lead.
It is well-isolated and would genuinely change the Gilbreath row.

It lost on criterion (a). R3.11 needs a renewal argument, not cycles; the
previous session had already measured everything measurable and identified the
missing step as analytic. Three consecutive Gilbreath-family sessions had
already run (2026-07-28, 07-29 ×2), and the standing rule sends the next session
elsewhere regardless. Chowla and Erdős–Gyárfás both end in "fetch primary
sources from an unblocked network", which this sandbox cannot do. External it
was, and the tie-break rule points that way anyway.

## What I went after

The plan: compute `L(A)` exactly for small integer alphabets, look for
structure, and try to turn the structure into a theorem covering infinitely many
alphabets at once.

## What worked, in order

**The searcher.** An incremental DFS: if a word is additive-square-free,
appending a letter can only create a square that *ends* at the new position, so
with prefix sums `S` the test is `S[n] + S[n-2k] ≠ 2·S[n-k]` for all `k ≤ n/2`.
`O(n)` per node, exact integers. Positive controls first: binary alphabets gave
`L = 3` (hand-checked: all sixteen length-4 binary words do contain an additive
square) and ternary gave `L = 7`, matching the classical abelian-square-free
maxima.

**The first surprise.** Every three-letter alphabet tried — `{0,1,2}`,
`{0,1,20}`, `{0,7,11}`, fifteen of them — returned **exactly 7**. That is not a
coincidence to be reported; it is a theorem to be found.

**The second surprise, and the session's actual idea.** Writing out why, the
reason is that block-sum differences are `p·a + q·b + r·c` for bounded integers
`p,q,r`, so additive-square-freeness depends on the alphabet *only through which
integer combinations of the letters vanish* — the **relation lattice**. Quotient
by any sublattice of relations and you get a canonical alphabet of integer
**vectors**, with fewer squares, hence longer words. That is the Quotient Lemma,
and it is four lines.

It immediately does three things:
- three letters: quotient to the free `ℤ²` alphabet, where additive = abelian,
  so `L ≤ 7`; and `0,1,0,t,0,1,0` is additive-square-free for *every* `t`, so
  `L = 7` uniformly. Twelve inequalities, all hand-checkable.
- four letters: the free bound is vacuous (Keränen: abelian squares are
  avoidable on four letters), which is precisely why four letters is the open
  case. A nonzero relation is *required*.
- the degenerate family `a+d = b+c`: it always satisfies the single relation
  `(1,1,-1)`, so one computation over one `ℤ²` alphabet bounds the whole
  infinite family.

That last computation returned **60** — exactly Freedman's published constant.
Getting a published number out of a machine that had never seen it is the
strongest validation the session got, and it arrived before I knew whether the
bound was tight.

**Sharpness.** The sweep then found 29 integer alphabets attaining 60, first at
`{0,1,5,6}`. Better, the *node counts* saturate at exactly 7,707,828 — the node
count of the generic quotient alphabet — from `{0,1,9,10}` onward. Once the
letters are spread far enough, the integer alphabet's search tree is literally
identical to the universal one. The cell-decomposition picture made visible.

**Cross-checks that actually ran.** An independent `O(n²)` verifier written from
the definition (not from the incremental test) re-checked every extremal word; a
negative control confirmed no letter extends any of them; the `d = 1` vector
searcher reproduced the scalar searcher; the Freedman constant came out
identically through three different unimodular completions, node counts and all;
and `{0,2,3,4}` returned the same value and the same node count as its
reflection `{0,1,2,4}`, checking the normalisation.

## What failed

- **The no-three-in-line target**, comprehensively — dead for eleven months. See
  above. The cost was one subagent and about ten minutes, because it was vetted
  in parallel rather than after building.
- **`strtok` nesting** in the vector searcher: the inner tokenizer clobbered the
  outer one's static state, so only the first letter of every alphabet parsed
  and every search returned `L = 1`. Caught immediately because the `d = 1`
  sanity check against the scalar searcher was the *first* thing run on the new
  binary, not the last. Fixed with `strtok_r`.
- **The cell-decomposition plan was overkill.** The original plan for the
  degenerate family was to enumerate ~2,200 exceptional rationals `t = -P/Q`
  with `|P|,|Q| ≤ 60` and exhaust each one separately. I wrote most of the
  scaffolding before noticing that the Quotient Lemma's linear map does the
  whole thing in one line and needs no case analysis at all. The scaffolding was
  discarded. The enumeration would have given the same answer far more slowly.
- **Hoping for a second Freedman-type class.** The obvious next relations —
  `(1,1,0)` (alphabet contains a 3-term arithmetic progression) and `(1,1,1)`
  (`a+b+c = 0`) — do **not** yield short words. They reached ≥ 440 and ≥ 996
  respectively without closing. So the session produced exactly one finite
  relation class, the already-known one. That is a real negative result and the
  most interesting thing left on the table: Freedman's relation appears to be
  singular, by a wide margin, and I do not know why.
- **Budget-limited lower bounds are not data.** An early temptation was to read
  the sweep's `L ≥ 111, 134, 290, 350...` numbers as a growth law in the
  alphabet's diameter. They are not: with a fixed node budget the depth reached
  is an artifact of the budget. They are recorded as certified lower bounds and
  explicitly disclaimed as measurements.

## Honest assessment of what this is worth

The Quotient Lemma is elementary — four lines, no machinery. Someone who has
thought about additive powers has very likely written it down; I could not check,
because the literature was unreachable. What I am comfortable claiming is that
it *organises* the subject usefully: Freedman's theorem becomes the single
instance `v = (1,1,-1)` of a general construction, and the natural question
"which relations force finiteness?" becomes computable, one finite search per
class.

The exact table appears to be new — no published values were found for any
integer alphabet — but "not found under a blocked network" is weak evidence and
is labelled as such everywhere it appears.

Theorem 4 is almost certainly folklore and is presented as such.

Nothing here touches PVHH itself. The honest summary is: one known theorem
re-derived cheaply and shown to be attained, one apparently-new table of exact
values, one new organising lemma of uncertain novelty, and one sharp negative
finding — that Freedman's relation looks singular among small relations.

## Next

1. Settle whether `L(A_v) = ∞` for the 3-term-AP class `v = (1,1,0)`. If some
   `v` has `L(A_v) = ∞`, the Quotient Lemma route to PVHH for four letters is
   blocked there, and knowing *where* is worth a lot. Rao–Rosenfeld's `ℤ²`
   result suggests such a `v` exists.
2. Why is `(1,1,-1)` special? A proof that it forces finiteness — rather than a
   7.7-million-node tree search — would probably generalise, and would replace
   the certified constant with a real theorem.
3. Push the exact table to the non-degenerate alphabets that did not close
   (`{0,1,2,6}` and up). The trees grow fast; `{0,1,2,5}` already took 1.2 × 10⁹
   nodes.
4. From an unblocked network: verify Freedman's paper and venue, check Ochem's
   heuristic page, and check whether the exact values and the Quotient Lemma are
   already in the literature. Until that is done the novelty claims here stay
   hedged.
