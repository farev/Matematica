# Session narrative — 2026-08-04

Written during and immediately after the session. Not edited to look smarter in
hindsight; the mistake in §2 is the main thing worth reading.

## 1. How this problem got picked

The network was down for literature purposes — every direct fetch refused with
HTTP 403 at the egress proxy — so the survey ran entirely through a web-search
tool, via five parallel subagents: number theory, discrete geometry/extremal,
games/automata, recent-2025/26-papers-with-stated-gaps, and one vetting a
candidate of my own (Kolakoski density bounds).

The Kolakoski agent came back and killed my own idea cleanly: the rigorous
density interval was improved in 2012 and the method is published, publicly
implemented on GitHub, and already pushed by professionals; a 4-core day is at
or below what the record-holder had. That was the right call and it saved the
session. The other three surveys produced the usual mix: good problems whose
bottleneck is a cluster, and good problems whose bottleneck is an idea.

The recent-papers agent produced one item that stood out on the only criterion
that matters for a one-day session — *is the bottleneck breakable* — namely a
2026 paper reporting a quantified compute wall: **one core-day of CaDiCaL, no
answer**, on whether a doubly saturated `R(4,5)`-good graph on 19 vertices
exists. A stated 1× failure is the right size of target for 4 cores plus one
idea, where almost everything else on the slate needed 10³–10⁶×.

## 2. The mistake

**I selected on a truncated quotation, and the truncation inverted the
conclusion.** The secondary report said, accurately, that the authors found
nothing on ≤ 18 vertices and that CaDiCaL did not terminate after a core-day at
19. What it omitted is that the very next sentences of the paper make a circulant
ansatz and solve `n = 19`. `DS(4,5) = 19` is established *in that paper*.

So the sequence of the day was: within about twenty minutes of picking the
problem I had the graph; within another hour I had a census, certificates, two
new orders' worth of sweeps and a small stack of lemmas; and only when the
definition-verification subagent came back — a job I had launched at the same
time as the first verification, precisely because the definition was
secondary-sourced — did it become clear that the graph was published, that it is
the `t = 5` member of a *proved infinite family* on `6t−11` vertices, and that
the identical circulant ansatz is the paper's own central move.

Two things made this recoverable rather than embarrassing:

* The vetting agent was launched **before** the result existed, not after. It was
  commissioned to check the definition, not to bless a finding.
* The evidence was decisive rather than suggestive. The paper's stated distance
  set `{4,5,6,8}` is *literally one of the nine hits my sweep printed*, and the
  family member `{3} ∪ [7,9] = {3,7,8,9}` is another. There was nothing to argue
  about.

What I would do differently: when a survey reports "authors state they could not
decide X", treat that as a claim about a *narrative beat* until the surrounding
paragraph is seen. A compute-wall sentence is exactly the kind of sentence a
paper writes right before explaining how it got around the wall. In a session
with no primary-source access, that pattern should be assumed by default.

## 3. What actually worked, and why

The instrument was right even though the target was already hit. The reason is a
two-line observation (Proposition 8 in [`NOTE.md`](NOTE.md)): a doubly saturated
graph is precisely an **isolated vertex of the single-edge-flip graph** on
`R(s,t)`-good graphs. Adding an edge can only create a clique, deleting one can
only create an independent set, so "no flip stays inside the class" is the whole
definition. Two consequences follow immediately:

* Flip-based local search — annealing, tabu, the standard toolkit for Ramsey
  lower bounds — can *never* reach one of these graphs, because an isolated
  vertex is unreachable by a walk that did not start there.
* A CDCL solver on the unrestricted encoding is looking for a needle among
  `2^171` assignments where the solutions are few and highly symmetric, which is
  the regime CDCL is worst at.

So the search must be exhaustive or must guess. Guessing a symmetry costs
nothing: at `n = 19` there are only `2⁹ = 512` circulants, and 9 of them are
doubly saturated. The sweep is milliseconds against a stated core-day. That gap
is the actual lesson of the day, and it is not a lesson about this problem.

## 4. Controls, and why they mattered

Before believing anything I ran the pipeline on graphs whose status is forced:

* `C₅` for `(3,3)` — doubly saturated ✓
* the unique `(3,5,13)` graph `C₁₃(1,5)` ✓
* Paley(17) for `(4,4)` ✓, Paley(13) ✓, Paley(29) for `(5,5)` ✓
* the Wagner graph `V₈` for `(3,4)` as a **negative** control — my code reports
  it fails at four edge deletions, which is correct and which I initially thought
  was a bug, having misremembered `e(3,4,8) = 1` when it is 3.

Then the census reproduced, without being told any of it, every published value
the vetting agent later surfaced: `C₅` unique for `(3,3)`; nothing for `(3,4)` or
`(3,6)`; Paley smallest primes `5, 13, 29` for `s = 3,4,5`; the `6t−11` family at
`t = 4,5,6`; and no circulant for `(3,7)` or `(3,8)`, consistent with their
20- and 25-vertex examples not being circulants. Independent agreement on ten
separate facts is the strongest evidence in this directory that the code is right
— stronger than any single verification.

Every headline object also ships a witness certificate checked by a verifier that
re-derives all claims from the edge list alone, so a reader need not trust the
search code at all.

## 5. What failed

* **The main target had already been hit.** §2.
* **The paper's Conjecture 2 could not be tested.** The only available statement
  of it is a machine paraphrase; instantiated at `t = 9` and `t = 11` the graph it
  describes contains a triangle, so it cannot be what the authors wrote. This is
  a measurement of the sources rather than of the conjecture, and it is the
  clearest evidence in the session for why claim-rule 5 exists.
* **A brute-force Python re-check does not scale.** Verifying the `(5,5)` hit at
  `n = 41` from the definition means re-scanning `C(41,5)` subsets once per edge
  flip. It timed out. The fix — witness certificates, verified once — is both
  faster and a stronger artifact, but it took a wasted run to see that.
* **The `(5,5)` hits at `n = 37` and `n = 41` have no independent certificate**,
  for that same scaling reason. Recorded as a defect rather than papered over.
  (I initially recorded `(3,9)` at `n = 35` as uncertified too, on the strength of
  a run that appeared to time out; the timeout was the shell wrapper, not the job,
  and that certificate is in fact complete and verifies — including the full
  `C(35,9) ≈ 7·10⁷` scan. Corrected before commit.)
* **`n ≤ 18` was not independently reproduced.** Only structured families were
  swept there.
* **Order 21 and 23 got only the circulant sweep**, since neither admits the
  `k = 2` prescribed-symmetry family.

## 6. What survives

Modest, and labelled as such: an exhaustive circulant census with certificates;
the certified statement that the 19-vertex graph is the only doubly saturated
`R(4,5)` circulant across the entire feasible range `n ≤ 24` (partial support for
the paper's *unproved* uniqueness suggestion); 220 doubly saturated `R(4,5)`-good
graphs on **22** vertices, which the paper — concerned with the minimum order —
may well not record, marked *not known to be new*; and independent confirmation
of the published `6t−11` family at four values of `t`.

No page was written. A rediscovery plus a small new data point is not
page-worthy, and the pipeline's rule is that no page-worthy result means no
`PAGE.md`.

## 7. Cost

4 cores, 15 GB RAM. Circulant census: the whole table in under two minutes. The
`2²⁴` prescribed-symmetry sweep at `n = 24` was the longest single run, a few
minutes. Certificate generation is seconds per graph except at `n = 35`, which
was abandoned. **No randomness anywhere in this session** — every search is
exhaustive and deterministic, so there are no seeds to record.
