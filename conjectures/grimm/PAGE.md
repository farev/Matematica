# PAGE.md — handoff for the local publish pass (new page: fabianarevalo.com/grimm)

New conjecture, new page. Row added to the top-level README index this
session.

## 1. Headline claim (one sentence, labelled)

**CERTIFIED** — Grimm's conjecture (1969) verified for all n ≤ 10¹², a 52×
extension of the record that had stood since 2006, together with the first
census of the gap members that make the conjecture nontrivial: the
{{TOTAL_CRIT}} "critical" members below 10¹², each with its factorization,
its explicitly assigned prime, and the exact Hall margin of its gap.

## 2. Contributions

1. **CERTIFIED** — Grimm's conjecture holds for all n ≤ 10¹²: every maximal
   prime gap with left prime p < 10¹² carries an explicit system of
   distinct prime representatives. Previous record n ≤ 1.9236701629×10¹⁰
   (Laishram–Shorey 2006, (secondary)); factor 52 extension; under an hour
   of 4-core wall time for the whole range (c1–c4: 8.9 s + 44.7 s +
   335.7 s + {{C4_WALL}}).
2. **CERTIFIED** — the critical-interval census: {{TOTAL_CRIT}} critical
   members in {{TOTAL_GAPSC}} gaps below 10¹², with factorizations,
   matchings, exact Hall margins; per-decade table in
   `data/stats_by_decade.csv`; no margin is negative (a negative margin
   would be a Grimm counterexample).
3. **CERTIFIED** — every tight gap (margin 0) below 10¹² is *prime-power
   tight*: all {{TIGHT_TOTAL}} of them contain a prime power p^a with
   p ≤ k, and none requires a genuine multi-member interaction; the
   largest is at p = {{LAST_TIGHT_P}} (containing {{LAST_TIGHT_WITNESS}}).
4. **PROVED** (elementary) — Lemma 2.1 (reduction to critical members;
   classical in substance, stated with proof in NOTE §2, no novelty
   claimed); Lemma 5.1 + Proposition 5.2: margin-≤-0 gaps occur infinitely
   often (powers 2^a, a ≡ 3 mod 6, force them), so the tightness the census
   sees never dies out entirely — only its interaction form can.
5. **CERTIFIED** (controls) — π(10⁸), π(10⁹), π(10¹⁰), π(10¹¹), π(10¹²)
   reproduced exactly; first-occurrence maximal gaps 86/220/282/354/464
   reproduced; exhaustive independent re-derivation on three windows and
   250–300 sampled gaps per chunk, zero discrepancies.

## 3. Figure specs

1. **Criticals per decade.** Data: `data/stats_by_decade.csv` (columns:
   decade, critical_rows) + prime counts from `data/c*.summary.txt`.
   Log-scale bars of critical members per decade against composites per
   decade. Sentence: "The members that make Grimm's conjecture nontrivial
   number a few million per decade against a trillion integers — and the
   verification gets *relatively* easier as numbers grow."
2. **Where criticals live.** Data: `data/crit_by_k.csv` (criticals by gap
   length) over `data/c*.gaphist.csv` (all gaps by length). Sentence: "A
   random gap almost never contains a critical member; long gaps almost
   always do — criticality is a large-deviation phenomenon of prime gaps."
3. **The tight gaps.** Data: `data/tight.csv` (p, k, m, factorization,
   margin) — scatter of tight-gap positions p (log x-axis) with marker =
   the prime power responsible (2^a, 3^a, 5^a, …). Sentence: "Every gap
   below 10¹² where Hall's condition is tight is tight because of a prime
   power sitting in it — never because several members genuinely compete
   for the same primes."
4. **A worked example: the 72-gap after 31397.** Data: the ten census rows
   `grep '^31397,'` (in NOTE §5 / this handoff): bipartite diagram, ten
   critical members left, their assigned primes {2,3,5,7,13,17,19,41,43,67}
   right. Sentence: "Even the busiest gap below 10⁹ — ten critical members
   — matches its members to distinct primes with room to spare."

## 4. Caveats the page must carry

- Every literature statement is **(secondary)**: the sandbox could not read
  any primary source (arxiv/oeis/erdosproblems all egress-blocked; search
  snippets only). In particular: the exact Laishram–Shorey record value and
  runtime, the Erdős–Selfridge and RST attributions, and the claim that no
  larger verification exists (absence-of-evidence from search). Re-verify
  against the papers during the publish pass — the record claim is the one
  a referee will poke first.
- The maximal-gap anchor values used as controls are from memory
  ((secondary)); they agreed five-for-five with the sweep, and the π
  anchors agreed exactly, but say so on the page.
- "Verified for all n ≤ 10¹²" is a statement about that range only —
  evidence of no counterexample, not evidence for the conjecture.
- Census completeness rests on the C engine, cross-verified exhaustively on
  three windows and by sampling elsewhere (250–300 gaps per chunk, seed
  20260815); the full ~{{TOTAL_CRIT}}-row censuses are not in the repo
  (size rule) — sha256 hashes are committed and regeneration is one
  50-minute command.
- The infinitude in Proposition 5.2 is of margin-**≤-0** gaps; margin
  exactly 0 for all of them is conditional on Grimm (unconditionally they
  could in principle be negative — none is, below 10¹²).

## 5. Existing page

None — this is a new conjecture directory and a new page. Add the row to
the site index at fabianarevalo.com/math.
