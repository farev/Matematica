# PAGE handoff — circular repetition thresholds

New page. Nothing exists for this conjecture yet; this is a first build.
Suggested slug: `circular-thresholds` → `fabianarevalo.com/circular-thresholds`.

> **Publish-pass note.** The top-level README row was added **without** a page
> link, to avoid a dead link while the page does not exist. When the page goes
> live, append `· [page ↗](https://fabianarevalo.com/circular-thresholds)` to
> that row and to the conjecture README header, then delete this file.

---

## 1. Headline claim

**PROVED.** Asking for circular threshold words at infinitely many lengths —
the open Currie–Mol–Rampersad conjecture `CRT_W(n) = RT(n)` for `4 ≤ n ≤ 44` —
is *decidable*: it follows from two finite searches, because widening the
circular factor window by exactly two letters makes the property survive a
uniform morphism.

## 2. Contributions

1. **Lemma A, the pumping lemma (PROVED).** Circular `α⁺`-freeness is not a
   bounded-window condition, which is what blocks the standard machinery. Let
   `S_2(n,m)` be the circular words of length `m` all of whose `w^ω`-factors of
   length `≤ m+2` have exponent `≤ α`. If `h` is `q`-uniform and preserves
   `α⁺`-freeness, then `h` maps `S_2(n,m)` into `S_2(n,qm)`. The constant 2 is
   exact: `⌈(qm+2)/q⌉ + 1 = m+2` for every `q ≥ 2`, and `S_1` does not close
   the induction.
2. **Theorem C (PROVED).** Consequently, one morphism plus one seed word
   `w_0 ∈ S_2(n,m_0)` gives circular `n`-ary threshold words at **every** length
   `q^j m_0`, hence `CRT_W(n) = RT(n)`. Both hypotheses are finite searches.
3. **Worked instance, `n = 3` (PROVED — and a known result, no priority
   claimed).** A `q = 28` morphism `h(a) = h_0 + a mod 3` with
   `h_0 = 0120212010201210120102120210`, and the seed
   `w_0 = 01202101210212012102` of length 20, give circular ternary threshold
   words of lengths **20, 560, 15 680, 439 040, …** — each verified directly
   against the definition, not via the theorem. This re-derives the published
   `CRT_W(3) = RT(3) = 7/4` end to end and is included **only as a positive
   control**.
4. **Proposition N (PROVED).** For `n ≥ 4`, a shift-equivariant uniform
   morphism over `Z_n` whose fixed point is a threshold word must have a
   difference set of size at most **2**. At `n = 3` this says nothing (the
   difference set lives in `{1,2}` anyway); at `n ≥ 4` it is nearly fatal. This
   is *why* the construction that works on three letters cannot be pushed up.
5. **Certified spectra (CERTIFIED).** The exact set of lengths admitting a
   circular `n`-ary threshold word: `n = 3` (`m ≤ 300`, 8 exceptions, the last
   at 22), `n = 4` (`m ≤ 164`, 87 exceptions), `n = 5` (`m ≤ 300`, 41
   exceptions, the last at 63), `n = 6` (`m ≤ 275`, 33 exceptions, the last at
   59).
6. **The surprise (CERTIFIED).** At `n = 4` the exceptional lengths do **not**
   stop: after the last small one at `m = 113` there is an unbroken run
   `114 … 146`, and then `m = 147` and `m = 154` admit no circular threshold
   word at all. A sweep halting anywhere in `114…146` would have reported a
   clean cofinite spectrum and been wrong.
7. **Exhaustive negative (CERTIFIED).** No shift-equivariant `q`-uniform
   morphism satisfies the criterion at `α = RT(n)` for `n = 4 (q ≤ 60)`,
   `5 (q ≤ 68)`, `6 (q ≤ 51)`, `7 (q ≤ 44)`, `8 (q ≤ 37)` — while the same
   search returns morphisms at `n = 3`, so it is not failing vacuously.

**Not achieved:** no open case of the conjecture was settled. The page must say
so plainly and early, not bury it.

## 3. Figures

**Figure 1 — the spectrum strips.** Four horizontal strips, one per
`n = 3,4,5,6`, `m` on the x-axis from 1 to the computed maximum; a cell is
filled if a circular `n`-ary threshold word of that length exists, blank if
none does. Mark the two late blanks at `n = 4` (`m = 147`, `154`) with a
callout.
*Data:* `data/spec_n3.csv`, `data/spec_n4.csv`, `data/spec_n5.csv`,
`data/spec_n6.csv` (columns `m`, `exists`, `witness`).
*Sentence a reader should be able to say:* "Short lengths are erratic, long
lengths almost all work — except on four letters, where two gaps come back
after the pattern looked settled."

**Figure 2 — the pumping ladder.** The seed `01202101210212012102` drawn as a
ring of 20 letters, with an arrow labelled `h` to a ring of 560, then 15 680,
then 439 040 (the last two indicated schematically, not letter by letter).
*Data:* reproduce with
`python3 pump.py chain 3 0120212010201210120102120210 01202101210212012102`.
*Sentence:* "One 28-letter substitution rule turns a single 20-letter circular
word into circular threshold words of infinitely many lengths — which is the
whole content of the conjecture for that alphabet."

**Figure 3 (optional; drop if it does not earn its place).** The seam picture
behind Proposition N: `h_0` followed by `h_0 + d`, with the `n−2` positions
either side of the join highlighted, showing the `n−2` forbidden differences.
*Data:* none — a schematic.
*Sentence:* "Every failure happens at the join, and counting the forbidden
differences there is exactly what caps the difference set at 2."

## 4. Caveats the page must carry

- **Egress was blocked all session** (HTTP 403 to `arxiv.org`, `oeis.org`,
  `erdosproblems.com`, `mathoverflow.net`). **No primary source was read.**
  Every citation — Mol–Rampersad arXiv:1912.11388, Currie–Mol arXiv:1803.08145,
  Gorbunova EJC 19(4), Dejean/Pansiot/Rao, and the claim that `4 ≤ n ≤ 44` is
  open — is **secondary**, taken from search summaries. The page must say this
  where a reader will see it.
- **Theorem M (the morphism criterion) is expected to be a rediscovery.**
  Finite tests for power-free morphisms are a developed subject
  (Bean–Ehrenfeucht–McNulty, Crochemore, Richomme–Wlazinski, Ochem). It is
  proved here for self-containedness, not claimed as new. Say so.
- **`CRT_W(3) = RT(3)` is known.** Contribution 3 is a control, not a result.
  A reader must not come away thinking a case was settled.
- **The spectra are CERTIFIED only on the ranges computed** — `m ≤ 300`
  (`n=3,5`), `≤ 275` (`n=6`), `≤ 164` (`n=4`). Nothing is claimed beyond.
  Contribution 6 is the reason to be strict about this.
- **UNSAT verdicts rest on a single SAT solver.** No DRAT proof was emitted or
  checked; no independent exhaustive enumeration was run at larger `m`.
  Satisfiable verdicts *are* independently verified (witness plus a
  from-the-definition checker). This asymmetry should be stated.
- The definitions of `CRT_W` / `CRT_I` / `CRT_S` used here are restated from
  scratch; their agreement with the literature's is itself secondary-sourced,
  though the pipeline reproduces five published constants (`CRT_S(4,5,6,7)`
  and the cofiniteness predicted by `CRT_I(3)`), which is the best check
  available without the papers.

## 5. Existing page

None. This is a new page.
