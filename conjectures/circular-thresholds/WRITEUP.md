# Session narrative — 2026-08-03, circular repetition thresholds

Written as it happened, including the parts that went nowhere. Not edited to
look smarter in hindsight.

## 0. The sandbox, first

The connectivity check came back worse than expected: `WebFetch` and `curl`
both return HTTP 403 from the egress proxy for **every** host — `arxiv.org`,
`oeis.org`, `erdosproblems.com`, `mathoverflow.net`, `api.crossref.org`,
`export.arxiv.org`. Only the search tool worked, and it returns titles, URLs
and a synthesized summary, not the document. So: **no primary source was read
today**. That single fact shaped every decision below. It rules out auditing a
recent paper (you cannot audit what you cannot read), and it makes novelty
claims soft. The response was to pick a problem whose mathematics I could
state and develop entirely from scratch, and to mark every citation
`(secondary)`.

## 1. Choosing

Three subagents surveyed in parallel — combinatorics on words, number
theory/additive combinatorics, and combinatorial games/finite search — while
I probed covering systems and cap sets myself. The slate is in the daily log.
The winner was the Currie–Mol–Rampersad conjecture on circular repetition
thresholds, for three reasons: the open region is a *finite* list of alphabet
sizes (`4 ≤ n ≤ 44`), the per-case question is a search, and I could define
everything myself and check my definitions against two independently reported
published constants (`CRT_S(k)` and `CRT_I(3)`) without reading a paper. That
last property is worth a lot when the library is closed.

Before committing I had already built the SAT encoder and run `n = 3, 4, 5`
to length 140, so the choice was made with data rather than hope.

## 2. What worked

**The encoding.** A circular word of length `m` is `α⁺`-free iff no
`(start, period)` pair carries the shortest over-exponent window. That is
`O(m²)` clauses with exact rational `α`. Cadical decides `m ≈ 300` in well
under a second for `n = 5, 6`. Every satisfiable witness is re-verified by an
`O(m³)` checker written from the definition; a vectorised checker was
cross-validated against the naive one on 700 random words with zero
mismatches.

**Two calibrations against published numbers, before any claim.** With `α` set
to the reported `CRT_S(k)` — `3/2, 4/3, 4/3, 5/4` at `k = 4,5,6,7` — every
length `1…60` must be realizable, and every length was. With `α = RT(3)`, the
spectrum must be cofinite because `CRT_I(3) = 7/4` is known, and it was:
exceptional set exactly `{5,7,9,10,14,16,17,22}` inside `1…300`. I would not
have trusted anything downstream without these.

**Lemma A.** The real obstruction to using morphisms here is that circular
`α⁺`-freeness is not a bounded-window property: a circular word of length `m`
constrains periods up to `≈ m(n−1)/n`, so you cannot run the usual de Bruijn /
transition-graph argument. The fix took a while to see and is two lines once
seen: widen the window from `m` to `m+2`. A factor of `h(w)^ω` of length
`≤ qm+2` is covered by `⌈(qm+2)/q⌉+1 = m+2` letters of `w^ω` — exactly, for
every `q ≥ 2`. So `S_2` is preserved by the morphism and `S_1` is not. That
turns "infinitely many lengths" into "one morphism plus one seed", both finite
searches.

**Theorem M.** I needed a criterion for a uniform morphism to preserve
`α⁺`-freeness. The naive synchronization argument loses `2(q−1)` letters at
the two ends of the repetition and only yields `exp ≥ α − 2q/p` — useless,
since `α` is exactly the threshold. Adding **(H1)** distinct first letters and
**(H2)** distinct last letters makes the loss vanish: a partial block at the
left end still matches in its *last* letter, which by (H2) identifies the
letter, so the block can be absorbed; symmetrically on the right with (H1).
The count then comes out at `⌈(s+ℓ)/q⌉ − ⌊s/q⌋ ≥ ℓ/q` with no loss at all. I
expect this is known — power-free morphism tests are a developed subject — and
have said so in the note rather than dressing it up.

**The `n = 3` positive control, end to end.** Morphism found by exhaustive
search (`q = 28`), (H1)–(H4) verified twice by implementations sharing no code
(C and Python, identical verdicts), seed found by SAT at `m_0 = 20`, and the
pumped words verified *directly against the definition* — not via the theorem
— at lengths 20, 560, 15 680 and 439 040. That re-derives `CRT_W(3) = 7/4`,
which is known. It is in the note purely as evidence that the machinery
produces correct theorems.

## 3. What failed

**The main attack failed.** No morphism was found for any `n ∈ [4,8]`, so no
open case was settled. In order:

- **First approach: search shift-equivariant morphisms `h(a) = h_0 + a` under
  the full (H1)–(H4).** Exhaustive over all `α⁺`-free `h_0`: zero hits at
  `n = 4 (q ≤ 60)`, `5 (q ≤ 68)`, `6 (q ≤ 51)`, `7 (q ≤ 44)`, `8 (q ≤ 37)`,
  against hits at `n = 3` from `q = 25` on. Millions of candidates scanned;
  the synchronization filter passed almost everything, so (H4) was doing the
  killing.

- **Second approach (a genuine change, not a retry): weaken the requirement.**
  Lemma A has a relativised form needing only `h(X) ⊆ X` for a factor-closed
  `X` of `α⁺`-free words. Taking `X = Fac(h^ω(0))` makes `h(X) ⊆ X` free, and
  the requirement collapses to "the fixed point has no *short* over-exponent
  factor" (Theorem M′), which is far weaker than (H4). Implemented, and it
  found the `n = 3` morphisms as it should. For `n ≥ 4` it failed **harder**:
  the cheapest necessary condition — `h_0·(h_0+d)` `α⁺`-free for each
  difference `d` occurring in `h_0` — was satisfied by *zero* candidates at
  `n = 4, 5, 6, 7`. Not one, at any `q`.

- **Diagnosing that, which is the one place a failure paid.** Every violation
  sat at the seam between `h_0` and `h_0+d`, with period `≤ n−2`. That is
  exactly the regime where `RT(n)`-freeness says *all* letters at distance
  `≤ n−2` differ, and it gives a proof: the `n−2` differences
  `h_0[q−1] − h_0[k]`, `k = 0..n−3`, are distinct and must all avoid `D`, so
  `|D| ≤ 2` (Proposition N). At `n = 3` this is vacuous — `D ⊆ {1,2}` always —
  and at `n ≥ 4` it is nearly fatal. So the ansatz that works at `n = 3` is
  *structurally* the wrong normal form above it, and the negative search is
  explained rather than merely reported.

**Two dead ends before Lemma A, recorded so they are not re-walked.**

- *Pumping without a morphism.* I looked for a closure property of the
  spectrum — `m ∈ C(n) ⟹ 2m ∈ C(n)`, or an insertion that grows a circular
  threshold word by a fixed block. The data kills the first immediately:
  `5, 10 ∈ C(5)` but `20 ∉ C(5)`. No insertion rule survived contact either;
  the wrap-around constraint is global, and that is the whole difficulty.
- *Using `β > RT(n)` slack.* `CRT_W(n) = RT(n)` only needs, for each
  `β > RT(n)`, infinitely many lengths — and at fixed `β` there is linear
  slack at large periods, which makes each individual construction much
  easier. But it must hold for a sequence `β_k ↓ RT(n)`, so one needs a
  *uniform family* of constructions, not a search per `β`. That is the shape
  of the published `n ≥ 45` proof, and it is not a one-afternoon object.

## 4. The datum I did not expect

`n = 4` has late exceptional lengths. After the last small gap at `m = 113`
there is an unbroken run `114 … 146`, and then `m = 147` and `m = 154` admit
no circular `7/5⁺`-free word. I had written "then becomes an unbroken run" into
the note on the strength of the `n = 5, 6` behaviour and had to correct it
against the `n = 4` output. That is the useful lesson of the day: at `n = 4` a
sweep stopping anywhere in `114…146` reports a clean cofinite-looking spectrum
and is wrong. `n = 4` is also precisely where `RT(4) = 7/5` breaks the
`n/(n−1)` pattern, so it is the alphabet one should have expected to
misbehave.

## 4b. The failure that turned into the best theorem

The negative was originally going to be reported as "no morphism found in the
range searched" — a bounded CERTIFIED statement, and a weak one. Pushing on
*why* the seam always breaks gave Proposition N (`|D| ≤ 2`), and then the
obvious follow-up question — how long can an `RT(n)⁺`-free word be if it has
only two distinct consecutive differences? — turned out to have a very small
answer: `11, 8, 14, 10, 18, 12` for `n = 4…9`. That closes every large `q` at
a stroke, and the existing exhaustive searches already covered every small `q`.
So the bounded negative became **Theorem N′**: for `4 ≤ n ≤ 9` no
shift-equivariant morphism has a threshold fixed point *at any length*. Not
"none was found" — none exists. That is a better outcome than the search I
actually set out to run would have given if it had merely kept coming up
empty, and it is the one place today where being stuck paid.

## 5. Honest accounting

Nothing here settles an open case. What the session produced is a reduction
(Lemma A, Theorem C) that makes the open cases mechanical *given the right
normal form*, a theorem that the obvious normal form provably cannot work at
any morphism length for `4 ≤ n ≤ 9` (Proposition N + Theorem N′), certified
spectra including one genuinely surprising irregularity — triple-checked
across three SAT backends — and a worked instance reproducing a known
theorem. The single
most valuable next step is small and specific: redo the Theorem C search in
Pansiot's encoding.

Claim discipline note: I came close to writing "the spectrum becomes cofinite"
and to letting Theorem M stand unqualified as new. Both were caught — the
first by the `n = 4` data, the second by asking what the power-free-morphism
literature almost certainly already contains. The second correction cost
nothing and the note is better for it.

---

# Session 2 — 2026-08-06

**Plan at start.** Run the Theorem C search in Pansiot's encoding — session
1's named next step — targeting `n = 4` first, after the day's survey turned
up Tunev's December 2025 paper (odd `n ≥ 5` cyclic threshold words,
(secondary)) and pushed the priority to even alphabets.

**What actually happened, including the failures.**

1. *Feasibility probe, wrong filter.* First search: letterwise binary code
   morphisms with a group-compatibility condition (simultaneous conjugacy
   C2), filtered by *preservation* — images of all valid 14-blocks stay
   code-free. Thousands of C2 pairs at `n = 4, 5, 6`, zero survivors
   anywhere. Diagnosis: the filter was needlessly strong *and* the pool
   needlessly narrow.
2. *Two theory corrections mid-day.* (a) Freeness of a decode is intrinsic
   to the bits (the slot lemma) — so the relativised route only needs the
   *fixed point* free, not preservation on all words. (b) The monodromy
   condition classifies completely (C2 / sign-collapse / level-`t`
   collapse), enlarging the pool. Rebuilt filters accordingly.
3. *`n = 4` still empty, `n = 3` abundant.* The full-pool sweep with the
   corrected filter: `n = 3` produces candidates from `k = 7`; `n = 4`
   produces zero through `k = 46` with tens of thousands of pooled pairs per
   length. Autopsy: 89 % of `n = 4` fixed points die at block seams within
   two generations, offender periods 3–10 — the code-level shadow of session
   1's Proposition N mechanism.
4. *Mid-session checkpoint (pre-registered) taken.* The `n = 4` hit-hunt was
   declared failed on the reachable ranges; the day's deliverable was
   re-scoped to the machinery + the `n = 3` control + certified negatives.
   Then the two-level engine and the deep sweeps were left running.
5. *The turn.* The recovered overnight-style logs showed `n = 5` (533) and
   `n = 6` (380) candidates — the sweeps had quietly crossed the viability
   threshold around `k = 21` and `k = 32`. The certification theorem
   (Theorem MC), written for the `n = 3` control, applied verbatim: four
   `n = 6` pairs and three `n = 5` pairs pass every hypothesis.
6. *Seeds from session 1's own data.* The certified spectrum witnesses of
   session 1 (`spec_n5.csv`, `spec_n6.csv`), Pansiot-encoded, contain
   monodromy-trivial cyclic codewords with the required `+2` margin — the
   seed for `n = 6` is the session-1 witness at `m = 39` and for `n = 5` at
   `m = 28`. Session 1's SAT data thus became load-bearing input to session
   2's theorems.
7. *End-to-end.* `CRT_W(6) = RT(6)` and `CRT_W(5) = RT(5)` proved; pumped
   words directly verified (to length 17 199 resp. 12 348), with session 1's
   independent `O(m³)` checker confirming the `n = 6` words it could reach.
   The `n = 3` control re-derives `CRT_W(3) = 7/4` with `k = 19` generators
   and the session-1 seed re-encoded.
8. *What failed at the end.* `n = 8`: 44 viable pairs at `k = 28`, all
   rejected by (Ha)/(Hb) — the criterion, not the candidates, is the
   bottleneck there. A first-bit-injectivity-free variant of Theorem MC is
   the clear next tool. The `(σ, ρ)` two-level engine found nothing anywhere
   it was run — every positive result today came from the letterwise class
   it generalises.

**Corrections made along the way.** One real bug (the (Hc) filter skipped
pairs based on image validity instead of source validity — fixed before any
certification); one formula strengthened after proof-writing exposed a
margin (`N_0` gains `+(n−1)`; all previously certified instances re-certify
unchanged); one scanner blind spot (bare monodromy-id blocks) caught by the
transfer-lemma validation and folded into the lemma's final form.

**Honest bottom line.** The theorems P5/P6 rest on three short lemmas proved
today and machine-checked hypotheses; the strongest independent evidence is
the `n = 3` end-to-end control and the direct verification of the first
pumped words. Novelty for `n = 6` rests on two (secondary) sources; for
`n = 5` it is genuinely uncertain (Tunev). Everything is committed for a
referee to attack.
