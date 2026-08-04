# Doubly saturated Ramsey graphs: an independent rediscovery, a circulant census, and examples at order 22

**Session:** 2026-08-04. AI assistance (Claude) was used throughout; see §10.

> ## Rediscovery notice — read this first
>
> The object this session set out to find, **a doubly saturated (4,5)-Ramsey
> graph on 19 vertices, is already published.** It appears in Przybocki, Mackey,
> Heule and Subercaseaux, arXiv:2604.21187 (April 2026), as the circulant on
> `Z₁₉` with distance set `{4,5,6,8}`, and as the `t = 5` member of a proved
> infinite family. The graph found here, `Cay(Z₁₉, ±{1,3,5,6})`, is that graph:
> `{4,5,6,8} × 4 ≡ {1,3,5,6} (mod 19)`, and both sets appear among the nine that
> this session's exhaustive circulant sweep returned. **Nothing in §4 is new.**
>
> The session was selected on a secondary report that the `n = 19` case was
> undecided. That report quoted a real sentence from the paper — CaDiCaL failing
> after a core-day — but it was the setup for the paragraph in which the authors
> make a circulant ansatz and solve it. The identical ansatz is what worked here.
> See `WRITEUP.md` §2 for how the error was made and caught.
>
> What survives as possibly-new is small and is confined to §5–§7: examples at
> order 22, and an exhaustive circulant census. It is labelled *not known to be
> new*, not *new*.

## Abstract

A graph `G` is *R(s,t)-good* if it contains no `K_s` and no independent set of
size `t`; it is **doubly saturated** if additionally adding any missing edge
creates a `K_s` and deleting any existing edge creates an independent `t`-set
(and neither `G` nor `Ḡ` is complete). We record elementary structure (§3):
double saturation is exactly simultaneous maximality of `G` among `K_s`-free
graphs and of `Ḡ` among `K_t`-free graphs, equivalently `G` is an *isolated
vertex* of the single-edge-flip graph on `R(s,t)`-good graphs — from which no
flip-based local search can ever reach one. We then report an exhaustive
enumeration of doubly saturated **circulants** for `3 ≤ s ≤ t ≤ 6` plus `(3,7)`
to `(3,9)` (§6), which independently reproduces every published value we are
aware of, and exhibits **220 doubly saturated (4,5)-good graphs on 22 vertices**
invariant under a fixed-point-free automorphism of order 11 (§5) — none of them
circulant. All headline objects ship witness certificates checkable by a 60-line
verifier.

---

## 1. Definitions

Graphs are finite, simple, undirected; `Ḡ` is the complement; `s, t ≥ 3`.

**Definition 1.** `G` is **R(s,t)-good** if it contains no `K_s` and no
independent set of size `t`. (No constraint on the order; a graph on `n` vertices
can be `R(s,t)`-good exactly when `n < R(s,t)`.)

**Definition 2.** An `R(s,t)`-good graph `G` is **doubly saturated** if

* **(A)** `G + uv` contains a `K_s` for every non-edge `uv`; and
* **(B)** `G − uv` contains an independent `t`-set for every edge `uv`;

and neither `G` nor `Ḡ` is complete. Clause (A)/(B) is the unpacking of "any
single edge flip destroys `R(s,t)`-goodness": adding an edge cannot create an
independent set, deleting one cannot create a clique. The final clause excludes
degenerate cases where one quantifier is vacuous.

**Definition 3.** `DS(s,t) := min{ n : some doubly saturated R(s,t)-good graph
has n vertices }`.

*Example.* `C₅` is doubly saturated for `(3,3)`.

---

## 2. What the literature says

**No primary source was opened.** Every direct fetch — `arxiv.org`, `oeis.org`,
`erdosproblems.com`, `mathoverflow.net`, `en.wikipedia.org`, `api.crossref.org` —
was refused with HTTP 403 at the egress proxy (`connect_rejected: gateway
answered 403 to CONNECT`). Only a web-search tool running outside the sandbox
was available. **Every item below is (secondary): a machine paraphrase of a
paraphrase.** One transcription drawn from these summaries is demonstrably
garbled — see §8 — which is a direct measurement of their reliability.

From Przybocki, Mackey, Heule, Subercaseaux, *Doubly Saturated Ramsey Graphs: A
Case Study in Computer-Assisted Mathematical Discovery*, arXiv:2604.21187,
CICM 2026, all **(secondary)**:

| Reported | Our census (§6) |
|---|---|
| `C₅` is the unique doubly saturated `R(3,3)`-good graph | agrees (`n = 5`, one graph) |
| **Theorem:** for all `t ≥ 4` there is a doubly saturated `R(4,t)`-good graph on `6t−11` vertices, circulant with distances `{m} ∪ [2m+1, 3m]`, `m = t−2`; Lean-formalised | **confirmed independently for `t = 4,5,6,7`** (`n = 13,19,25,31`), `family.py` |
| `DS(4,5) = 19`; the 19-vertex example is the circulant with distances `{4,5,6,8}` | that exact distance set is one of our nine hits at `n = 19` |
| `DS(4,4)`-relevant: smallest prime `p` with Paley(`p`) doubly saturated `R(s,s)`-good is `5, 13, 29, 53` for `s = 3,4,5,6` | agrees at `s = 3,4,5` (`n = 5, 13, 29`); `s = 6` is outside our swept range |
| `(3,4)` and `(3,6)` conjectured to admit **no** doubly saturated graph at any order | agrees among circulants (`n ≤ 8` and `n ≤ 17`) |
| smallest doubly saturated `R(3,7)`-good graph has 20 vertices | we find **no** `(3,7)` circulant for `n ≤ 22`, so theirs is not circulant |
| two non-isomorphic doubly saturated `R(3,8)`-good graphs on 25 vertices | we find no `(3,8)` circulant for `n ≤ 27`, so neither is circulant |
| `DS(s,t) ≥ 2s + 2t − 7` | not tested |
| **Open — Question 1:** is `DS(4,t) = 6t−11` for all `t ≥ 4`? | untouched |
| **Open — Conjecture 2:** a `(3,t)` circulant family on `5t−10` vertices for odd `t ≥ 17`, checked to `t ≤ 63` | **could not be tested** — see §8 |
| Uniqueness at `n = 19` is *suggested*, not proved (a parallel solver returned one isomorphic solution) | §6 gives a certified partial result |

Also **(secondary)**: the notion is attributed to a 1982 question of Grinstead
and Roberts (*On the Ramsey numbers R(3,8) and R(3,9)*, JCTB 33, 27–51); we could
not obtain their wording and that attribution is **unverified**. A search for the
notion under other names — "Ramsey saturated" (Balister–Lehel–Schelp 2006, a
different notion about `G` as an arrowing target), "`R(s,t)`-critical" (a graph on
`R(s,t)−1` vertices, no saturation condition), "Ramsey-minimal", "`K_r`-saturated"
(Erdős–Hajnal–Moon 1964, the one-sided ancestor) — turned up **no** earlier name
for this two-sided property.

Standard background used only to bound sweep ranges, never inside a proof, and
**not verified against primary sources**: `R(4,5) = 25` (McKay–Radziszowski
1995), `R(4,4) = 18`, `R(3,5) = 14`, `R(3,9) = 36`; Turner (1967), that every
vertex-transitive graph of prime order is a circulant.

---

## 3. Elementary structure (PROVED; almost certainly folklore)

**Lemma 4 (local criterion).** *An `R(s,t)`-good `G` is doubly saturated iff*
*(A′) every non-edge `uv` has a `K_{s−2}` inside `N_G(u) ∩ N_G(v)`, and*
*(B′) every edge `uv` has an independent `(t−2)`-set inside
`V ∖ (N_G[u] ∪ N_G[v])`.*

*Proof.* A clique of `G+uv` not already in `G` contains `u` and `v`; one of size
`s` is `{u,v} ∪ C` with `C` an `(s−2)`-clique in `N(u) ∩ N(v)`, and conversely.
Dually for independent sets in `G − uv`. ∎

**Lemma 5 (complement duality).** *`G` is doubly saturated for `(s,t)` iff `Ḡ` is
doubly saturated for `(t,s)`.* *Proof.* Adding an edge to `G` is deleting one from
`Ḡ`; a `K_s` of `G+uv` is an independent `s`-set of `Ḡ−uv`. So (A) for `G` is (B)
for `Ḡ` and conversely. ∎

**Theorem 6 (both-maximal characterisation).** *`G` is doubly saturated for
`(s,t)` iff `G` is a maximal `K_s`-free graph and `Ḡ` is a maximal `K_t`-free
graph.*

*Proof.* `R(s,t)`-goodness says `G` is `K_s`-free and `Ḡ` is `K_t`-free. (A) says
adding any non-edge to `G` makes a `K_s`, i.e. `G` is maximal `K_s`-free. (B) says
that for each edge `uv` of `G`, `Ḡ + uv` has a `K_t`; as `uv` runs over the edges
of `G` it runs over exactly the non-edges of `Ḡ`, so (B) says `Ḡ` is maximal
`K_t`-free. ∎

**Corollary 7 (self-complementary criterion).** *If `G ≅ Ḡ` and `G` is maximal
`K_s`-free, then `G` is doubly saturated for `(s,s)`.*
*Proof.* `Ḡ ≅ G` is `K_s`-free, so `G` has no independent `s`-set and is
`R(s,s)`-good; and `Ḡ ≅ G` is maximal `K_s`-free. Apply Theorem 6 with `t = s`. ∎

Corollary 7 halves the work for self-complementary graphs and accounts for every
`(s,s)` census row: `C₅`, Paley(13), Paley(17), Paley(29), Paley(37).

**Proposition 8 (isolated vertices of the flip graph).** *Let `F(s,t;n)` have as
vertices the `R(s,t)`-good graphs on `[n]`, adjacent when they differ in one edge.
Then `G` is doubly saturated iff `G` is isolated in `F(s,t;n)`.*

*Proof.* `Ḡ − e ⊆ Ḡ` is `K_t`-free automatically, so `G+e` is `R(s,t)`-good iff
`G+e` is `K_s`-free, i.e. iff (A) fails at `e`; dually `G−e` is `R(s,t)`-good iff
(B) fails at `e`. So `G` has a neighbour iff (A) or (B) fails somewhere. ∎

**Corollary 9 (local search cannot find them).** *Any procedure exploring
`R(s,t)`-good graphs on `n` vertices by single edge flips, never leaving the
class, outputs a doubly saturated graph only if initialised at one.* *Proof.* An
isolated vertex is unreachable by a walk that did not start there. ∎

Corollary 9 is the practical content: the standard toolkit for producing Ramsey
graphs — annealing and tabu search over edge flips — is provably blind to these
objects, so a search must be exhaustive or must guess the graph outright. That is
why a prescribed-symmetry ansatz is the right instrument, and it is presumably
why the authors of arXiv:2604.21187 reached for one too.

> **Novelty caveat.** Lemmas 4–5, Theorem 6, Corollary 7, Proposition 8 and
> Corollary 9 are one- or two-line consequences of the definitions. They are very
> likely folklore; Proposition 8 is plausibly the motivation for the notion and so
> presumably known to the authors. They are recorded so this note stands alone,
> not as claims of priority.

---

## 4. Order 19 — rediscovery, no novelty claimed

**Fact 10 (CERTIFIED; published, arXiv:2604.21187).** `G₁₉ = Cay(Z₁₉, ±{1,3,5,6})`
is 8-regular with 76 edges, has no `K₄` and no independent 5-set, each of its 95
non-edges creates a `K₄` when added, and each of its 76 edges creates an
independent 5-set when deleted.

Certificate `data/cert_n19_45.txt` (3.2 kB) lists the edges and all 171 witnesses;
`check_cert.py` re-derives everything from the edge list, enumerating all
`C(19,4) = 3876` quadruples and `C(19,5) = 11628` quintuples. Booleans and small
integers only; no floating point.

* `|Aut(G₁₉)| = 38`, exactly the dihedral group `⟨x↦x+1, x↦−x⟩` (`aut.py`).
* Exactly nine connection sets `S ⊆ {1..9}` give a doubly saturated circulant on
  19 vertices: `{1,2,6,8}, {1,3,4,9}, {1,3,5,6}, {1,4,5,7}, {2,3,4,7}, {2,5,8,9},
  {2,6,7,9}, {3,7,8,9}, {4,5,6,8}`. They are one orbit under `Z₁₉^*` (`orbit.py`),
  so exactly **one** such graph up to isomorphism. `{4,5,6,8}` is the paper's
  stated set; `{3,7,8,9} = {m} ∪ [2m+1,3m]` with `m = 3` is the `t=5` member of
  the paper's `6t−11` family.
* Of the 512 circulants on 19 vertices, 21 are `R(4,5)`-good and 9 are doubly
  saturated.

**Fact 11 (CERTIFIED; confirms a published theorem).** The circulant on `6t−11`
vertices with distances `{t−2} ∪ [2t−3, 3t−6]` is doubly saturated `R(4,t)`-good
for `t = 4, 5, 6, 7` (`n = 13, 19, 25, 31`) — `family.py`, checked from
Definition 2. This is an independent confirmation of the paper's theorem at four
instances, not a new result.

## 5. Order 22 — the one possibly-new construction

**Result 12 (CERTIFIED; not known to be new).** *There is a 9-regular doubly
saturated `R(4,5)`-good graph `G₂₂` on 22 vertices with 99 edges, invariant under
a fixed-point-free automorphism of order 11 with two vertex orbits.*

Certificate `data/cert_n22_45.txt`, checked by `check_cert.py`: no `K₄` among the
`C(22,4) = 7315` quadruples, no independent 5-set among the `C(22,5) = 26334`
quintuples, 132 addition witnesses, 99 deletion witnesses. Found by `semireg.c`,
then reconstructed independently in Python by `decode.py`, which rebuilds the edge
set from the orbit encoding and re-checks Definition 2 directly before emitting
the certificate.

Among the `2²¹` graphs on 22 vertices invariant under that automorphism, 1430 are
`R(4,5)`-good and **220** are doubly saturated; all 220 form a single orbit under
the obvious symmetries of the family (`Z₁₁` multipliers, relative shift of the
second orbit, orbit swap) — `iso22.py`. No doubly saturated `R(4,5)` circulant on
22 vertices exists (§6), so these are not circulants.

Why this may still not be new: the paper computes `DS(4,5) = 19`, i.e. the
*minimum* order, and says nothing we know of about the full set of orders. A
group with their tooling would find order 22 quickly. **Claimed only as "not
known to be new".**

## 6. Exhaustive circulant census (CERTIFIED for the ranges stated)

`census.c` enumerates every circulant `Cay(Z_n, S)`, `S = −S`, and applies
Lemma 4, using vertex-transitivity twice: a `K_s` exists iff `N(0)` contains a
`K_{s−1}`, and (A′)/(B′) need be checked only for pairs `(0,d)`, `d = 1..⌊n/2⌋`.
Every sweep is exhaustive over its range — no sampling, no seeds, no randomness
anywhere in this session.

| `(s,t)` | `n` swept | orders with a doubly saturated circulant | identification |
|---|---|---|---|
| (3,3) | 5–5 | **5** | `C₅` = Paley(5) |
| (3,4) | 5–8 | none | consistent with the reported `(3,4)` exception |
| (3,5) | 5–13 | **13** | `C₁₃(1,5)`, the unique `(3,5,13)` graph |
| (3,6) | 5–17 | none | consistent with the reported `(3,6)` exception |
| (3,7) | 5–22 | none | so the reported 20-vertex example is not circulant |
| (3,8) | 5–27 | none | so the reported 25-vertex examples are not circulant |
| (3,9) | 5–35 | **35** | `C₃₅(4,6,7,9)` + 3 multiplier images |
| (4,4) | 5–17 | **13, 17** | Paley(13) (= `6t−11` at `t=4`), Paley(17) |
| (4,5) | 5–24 | **19** | `G₁₉` (§4) |
| (4,6) | 5–39 | **25** | includes `{4,9,10,11,12}` = `6t−11` at `t=6` |
| (5,5) | 5–45 | **29, 37, 41** | Paley(29), Paley(37); at 41, 20 sets not of Paley type |

Two consequences worth isolating:

**Result 13 (CERTIFIED).** *`G₁₉` is the only doubly saturated `R(4,5)`-good
circulant on at most 24 vertices* — 24 being the largest possible order, since
`R(4,5) = 25`. This is a certified partial result toward the paper's unproved
suggestion that the 19-vertex graph is the unique doubly saturated `R(4,5)`-good
graph: it settles uniqueness within the circulant class over the entire feasible
range of orders, and says nothing outside it.

**Result 14 (CERTIFIED).** *The set of orders admitting a doubly saturated
circulant is not always `{R(s,t)−1}`, not always a single order, and not always
non-empty.* It is `R(s,t)−1` for (3,3), (3,5), (3,9), (4,4); but the `(4,5)`
example sits at 19 not 24, `(4,6)` at 25 while `R(4,6) ≥ 36`, `(5,5)` at 29, 37,
41 while `R(5,5) ≥ 43`; `(4,4)` has two orders; and (3,4), (3,6), (3,7), (3,8)
have none in range.

Certificates are committed and verified for the (3,3), (3,5), (4,4)×2, (4,5),
(4,6), (5,5)@29 and (3,9)@35 rows — the last of these does enumerate all
`C(35,9) ≈ 7·10⁷` subsets to confirm there is no independent 9-set, and passes.
The remaining rows, `(5,5)` at `n = 37` and `n = 41`, rest on `census.c` alone:
the independent Python check at `n = 41` timed out (it rescans `C(41,5)` subsets
per edge flip) and was not rerun in certificate form. That asymmetry is a defect,
recorded in the README.

## 7. Prescribed-symmetry sweeps beyond circulants (CERTIFIED for the families)

`semireg.c` enumerates graphs on `Z_m × [k]` (`n = mk`) invariant under
`σ(x,i) = (x+1,i)`, choosing membership per `σ`-orbit of vertex pairs. `k = 1` is
the circulant case and reproduces the census exactly (21 good / 9 doubly saturated
at `n = 19`; 2 / 2 at `n = 17`), which is how the program was validated.

| `n` | `m` | `k` | pair orbits | space | `R(4,5)`-good | doubly saturated |
|---|---|---|---|---|---|---|
| 16 | 8 | 2 | 16 | `2¹⁶` | 5560 | 0 |
| 18 | 9 | 2 | 17 | `2¹⁷` | 5211 | 0 |
| 20 | 10 | 2 | 20 | `2²⁰` | 1430 | 0 |
| 22 | 11 | 2 | 21 | `2²¹` | 1430 | **220** |
| 24 | 12 | 2 | 24 | `2²⁴` | 192 | 0 |

The `n = 18` row is weak independent corroboration of the reported `n ≤ 18`
non-existence: 5211 structured `R(4,5)`-good graphs, none doubly saturated. The
equality of the good-counts at `n = 20` and `n = 22` (both 1430) is unexplained
and was not investigated; it is flagged as something to re-check.

Orders 21 and 23 admit no `k = 2` family (both odd), so only the circulant sweep
applies there; 23 is prime, so by Turner's theorem (secondary) that covers all
vertex-transitive graphs of that order.

## 8. What failed, and a measurement of source reliability

The paper's **Conjecture 2** — a `(3,t)` circulant family on `5t−10` vertices for
odd `t ≥ 17` — could not be tested. The only statement of it available was a
machine paraphrase, which transcribed to distances
`[t−4,t−3] ∪ [t+1,(3t−9)/2] ∪ {(3t−5)/2} ∪ {2t−4}`. Instantiated at `t = 9` and
`t = 11` (`n = 35, 45`) the resulting circulant **contains a triangle**, so it is
not `R(3,t)`-good and certainly is not what the authors wrote; at `t = 13` it is
triangle-free but not deletion-critical. The conclusion is about the source, not
the conjecture: **these summaries are not reliable enough to instantiate a formula
from.** They were reliable enough to identify a graph, which is how the
rediscovery was caught.

Curiously, our `(3,9)` census hit sits at `n = 35 = 5·9 − 10`, matching the
conjecture's order formula three steps below its stated range, though with a
different connection set. We cannot tell whether that is meaningful.

## 9. Open questions

1. **The paper's Question 1:** is `DS(4,t) = 6t−11` for all `t ≥ 4`? Existence is
   proved there; minimality is open. Untouched here.
2. **Uniqueness at `n = 19`** beyond the circulant class (Result 13 settles it
   within that class for every feasible order).
3. **Decide `n = 20, 21, 23, 24` for `(4,5)` outside the searched families.**
   Corollary 9 rules out flip-based local search, so this needs exhaustive
   generation or SAT.
4. **The full set of orders** admitting a doubly saturated `R(s,t)`-good graph,
   for each `(s,t)` — Result 14 shows it has no simple shape.
5. **Is every Paley graph `P_q` with `ω = α = s−1` maximal `K_s`-free?** By
   Corollary 7 that would give doubly saturated `(s,s)` graphs for infinitely many
   `s`; the paper reports ≈75% of prime-order Paley graphs are doubly saturated
   (secondary), so the answer is *no* in general — which makes the question of
   *which* ones the interesting form.

## 10. AI assistance

Produced in a single automated research session with substantial AI assistance
(Claude). All computations are reproducible from the committed code; the two
constructions ship certificates a reader can check without trusting any program
here beyond a 60-line verifier. AI systems are not authors.
