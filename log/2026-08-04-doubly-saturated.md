# 2026-08-04 — doubly saturated Ramsey graphs

**Target.** Decide whether a *doubly saturated* `R(4,5)`-good graph on 19
vertices exists — a graph with no `K₄` and no independent 5-set such that adding
any missing edge creates a `K₄` and deleting any existing edge creates an
independent 5-set. A survey subagent reported (secondary) that Przybocki, Mackey,
Heule and Subercaseaux (arXiv:2604.21187, CICM 2026) had shown no such graph has
≤ 18 vertices and that at 19 vertices CaDiCaL did not terminate after a day on a
single core. A quantified one-core-day wall is the right size of target for four
cores plus one idea; almost every other candidate on the slate needed 10³–10⁶×.

**Result. Rediscovery — the target was already solved in the paper I selected
from.** The 19-vertex graph exists; I found it in milliseconds as
`Cay(Z₁₉, ±{1,3,5,6})` by sweeping all 512 circulants. It is **the same graph the
paper publishes** (their distance set `{4,5,6,8}`, which is literally one of the
nine hits my sweep printed — `{4,5,6,8}·4 ≡ {1,3,5,6} mod 19`), and it is the
`t = 5` member of a proved, Lean-formalised infinite family on `6t−11` vertices.
`DS(4,5) = 19` is established in that paper. The secondary report was a
truncation: the CaDiCaL sentence is the setup for the paragraph in which the
authors make the same circulant ansatz and solve it.

What survives, all labelled *not known to be new* or *confirmation*:

- **CERTIFIED** — 220 doubly saturated `R(4,5)`-good graphs on **22 vertices**,
  9-regular, 99 edges, invariant under a fixed-point-free automorphism of order
  11, forming one orbit under the family's symmetries; none is a circulant.
  Witness certificate committed. *Not known to be new* — the paper concerns the
  minimum order and may not record other orders.
- **CERTIFIED** — `G₁₉` is the **only** doubly saturated `R(4,5)`-good circulant
  on `n ≤ 24`, the entire feasible range since `R(4,5) = 25`. Partial support for
  the paper's *unproved* suggestion that the 19-vertex graph is unique.
- **CERTIFIED** — exhaustive circulant census for `3 ≤ s ≤ t ≤ 6` plus `(3,7)`–
  `(3,9)`. Doubly saturated circulants exist exactly at `n = 5` (3,3), `13` (3,5),
  `35` (3,9), `13, 17` (4,4), `19` (4,5), `25` (4,6), `29, 37, 41` (5,5); none for
  (3,4), (3,6), (3,7), (3,8) in range. The set of orders is not always
  `{R(s,t)−1}`, not always a single order, not always non-empty.
- **CERTIFIED** — independent confirmation of the published `6t−11` family at
  `t = 4,5,6,7`.
- **PROVED, almost certainly folklore** — double saturation ⟺ `G` maximal
  `K_s`-free **and** `Ḡ` maximal `K_t`-free ⟺ `G` is an *isolated vertex* of the
  single-edge-flip graph on `R(s,t)`-good graphs. Hence **no flip-based local
  search can ever reach one**, which is why the prescribed-symmetry ansatz is the
  right instrument and, presumably, why the paper's authors reached for one too.

**What failed.**

- *The selection itself.* I picked on a quoted compute-wall sentence without the
  surrounding paragraph. A "we could not decide X" line is exactly what a paper
  writes immediately before explaining how it got around X; with no primary-source
  access that pattern should be the default assumption. What saved the session
  from being an unmarked rediscovery is that the definition-verification subagent
  was launched *before* the result existed, not after it, and that its evidence
  was decisive rather than suggestive.
- *The paper's Conjecture 2 could not be tested.* The only statement of it
  available was a machine paraphrase; instantiated at `t = 9, 11` the circulant it
  describes **contains a triangle**, so it cannot be what the authors wrote. That
  is a measurement of the sources, not of the conjecture.
- *Brute-force Python verification does not scale.* Re-checking the `(5,5)` hit at
  `n = 41` from the definition needs `C(41,5)` subsets rescanned per edge flip; it
  timed out. Replaced by witness certificates — faster and a stronger artifact.
- *The `(5,5)` hits at `n = 37` and `n = 41` have no independent certificate*,
  for that same scaling reason; they rest on the C sweep alone. Recorded as a
  defect. (`(3,9)` at `n = 35` was briefly recorded the same way on the strength
  of an apparent timeout that turned out to be the shell wrapper rather than the
  job; its certificate is complete and verifies. Corrected before commit.)
- *`n ≤ 18` non-existence was not reproduced.* Corroborated only within structured
  families: none of 5211 `R(4,5)`-good graphs on 18 vertices invariant under an
  order-9 fixed-point-free automorphism is doubly saturated.
- *Orders 21 and 23 got only the circulant sweep*, neither admitting a `k = 2`
  prescribed-symmetry family.

**Next.** The paper's **Question 1** — is `DS(4,t) = 6t−11` for all `t ≥ 4`?
Existence at `6t−11` is proved there and confirmed here at four values; the open
half is minimality, a non-existence statement over all graphs of smaller order,
which by the isolation lemma is exactly the direction local search cannot touch.
Before any of that: **open arXiv:2604.21187 itself.** Whether the order-22
examples are new, whether the Grinstead–Roberts attribution is right, and what
Conjecture 2 actually says are all unanswerable from this sandbox.

---

## 1. Connectivity check

| source | reachable | how |
|---|---|---|
| `arxiv.org`, `export.arxiv.org` | **no** — HTTP 403 on CONNECT | WebFetch, curl |
| `oeis.org` | **no** — 403 | WebFetch, curl |
| `erdosproblems.com` | **no** — 403 | WebFetch, curl |
| `mathoverflow.net` | **no** — 403 | WebFetch, curl |
| `en.wikipedia.org`, `api.crossref.org` | **no** — 403 | curl |
| `raw.githubusercontent.com` | yes | used by a subagent for octal-game tables |
| web search tool | **yes** | runs outside the sandbox; the only literature channel |
| `pypi.org` | yes (proxy bypass list) | installed numpy/scipy/pysat |

The proxy status endpoint logged each refusal as
`connect_rejected: gateway answered 403 to CONNECT (policy denial or upstream
failure)` — organisation egress policy, not a TLS or configuration fault, so
nothing was retried or routed around.

**Consequence, stated prominently: no primary source was opened at any point
today.** Every citation in this session's documents is marked **(secondary)**.
This session then produced a hard measurement of what that costs: one formula
transcribed from search summaries was demonstrably garbled (§ *What failed*),
and — far more expensively — the selection itself rested on a quotation that was
accurate but truncated in a way that inverted its meaning.

## 2. The three external candidates

Built by four parallel survey subagents (number theory; discrete geometry /
extremal / design / coding; games / automata / TCS; recent-2025-26 papers with
stated gaps) plus a fifth vetting a candidate of my own. Spanning four subfields.

### E1 — Doubly saturated Ramsey graphs, `n = 19` for `(4,5)` *(extremal graph theory)* — SELECTED

*Statement.* A graph is `R(s,t)`-good if it has no `K_s` and no independent
`t`-set; doubly saturated if additionally every edge addition creates a `K_s` and
every edge deletion creates an independent `t`-set. Does a doubly saturated
`R(4,5)`-good graph on 19 vertices exist?

*Source.* Przybocki, Mackey, Heule, Subercaseaux, *Doubly Saturated Ramsey
Graphs: A Case Study in Computer-Assisted Mathematical Discovery*,
arXiv:2604.21187, CICM 2026. Seen 2026-08-04 via search summary, quoting: "There
are no doubly saturated R(4,5)-good graphs on 18 or fewer vertices"; "For 19
vertices, a SAT solver (CaDiCaL) does not terminate after a day on a single
core." **(secondary)**

*Why I believed it open.* The quoted sentence states a compute wall with no
resolution attached. **This was wrong** — see §5.

### E2 — Minimal critical exponent of balanced sequences over odd `d ≥ 13` *(combinatorics on words)*

*Statement.* For a `d`-letter alphabet, is `inf{E(u) : u balanced}` equal to
`(d−1)/(d−2)`? The lower bound is proved for all `d ≥ 11`; attainment is known for
`d = 11` and all even `d ≥ 12`.

*Source.* Dvořáková, Opočenská, Pelantová, Shur, arXiv:2112.02854 and
arXiv:2208.00366, quoting "it remains an open problem to prove this conjecture
also for all odd numbers `d ≥ 13`". **(secondary)**

*Why still open.* Two 2022 papers state it; nothing 2023–2026 surfaced closing it.
Confidence ~85%.

### E3 — Buratti–Horak–Rosa conjecture, certified verification past `v = 23` *(design theory)*

*Statement.* For a multiset `L` of `v−1` lengths from `{1,…,⌊v/2⌋}`, a Hamiltonian
path in `K_v` on `Z_v` with edge-length multiset exactly `L` exists iff for every
`d | v` the number of elements of `L` divisible by `d` is at most `v−d`.

*Source.* arXiv:2105.00980 ("still widely open"), arXiv:2202.07733, arXiv:2507.00059
("prior computational work by Mariusz Meszka, which verified the conjecture for
all primes up to `p = 23`"). **(secondary)**

*Why still open.* Every paper 2021–2026 states it open; Meszka's `p ≤ 23` is
unpublished with no public certificate.

Also surveyed and rejected with reasons recorded by the subagents: octal-game
periodicity (Grossman's 1.4×10¹⁴ values on `.6`), Černý (n = 13 is ~10³–10⁴×
beyond 4 cores), PCP[3,4] survivors, Kolakoski density (record improved 2012, the
method is published *and* publicly implemented — my own candidate, killed by its
own vetting agent), `r₃(N)`, integer complexity of `2ᵏ`, Erdős–Turán `ψ(n)`,
perfect 1-factorisation of `K₆₄`, Steiner `S(2,6,51)`, Oberwolfach past order 60.

## 3. The internal thread

The strongest live internal thread is **additive-squares: close the search tree
for the 3-term-AP relation class `v = (1,1,0)`**, where a budget-limited
exhaustive sweep plateaued at 440 and an independent randomised probe with a 66×
larger depth cap plateaued at 437. The conjecture README names it as the sharpest
open thread and says outright that finiteness there "would be a **second**
Freedman-type theorem" — which would change that row of the top-level README, so
it clears the significance bar.

**Assessment.** (a) The bottleneck is genuinely compute-shaped, and the two
independent estimates agreeing to within three letters is real evidence the value
is finite. (b) Novelty is not in doubt. (c) It would extend this repository's own
additive-squares line and, through it, Freedman. But the outcome is binary and
the likeliest single outcome is "still running at the depth cap", which is what
happened last time; and the mandate's default is external, with ties going to the
new problem. **Not chosen.** The runners-up — Gilbreath's Open Lemma R3.11 and
the circular-thresholds Pansiot-encoding search — were also passed over: R3.11 is
explicitly a bottleneck of ideas that four cores do not touch, and
circular-thresholds was worked on 2026-08-03, one session ago.

## 4. Selection argument

- **(a) Is the bottleneck compute-breakable?** E1 decisively: a *stated,
  quantified* one-core-day failure, against which four cores plus a symmetry
  ansatz is a plausible 10–100×. E2 borderline — the search space estimate was
  10⁶–10¹⁰ evaluations and needs a pruning idea. E3 yes but graded rather than
  binary: `p = 29` is ~1.26×10⁹ orbit representatives, 1–5 hours.
- **(b) Already done?** This is where I got it wrong. I scored E1 as low-risk
  because the authors had *published their failure*, and a published failure looked
  like a guarantee of openness. It is the opposite: a paper that reports a wall in
  its own narrative has usually got past it by the next paragraph. E3's `p ≤ 23`
  frontier is unpublished folklore, which was the honest reason to prefer it.
- **(c) Whose work would it extend?** E1: Przybocki–Mackey–Heule–Subercaseaux
  directly. E2: Dvořáková–Opočenská–Pelantová–Shur. E3: Meszka, and
  Ollis–Pasotti–Pellegrini–Schmitt.

E1 also had the property that mattered most with the library closed: it is
**fully self-contained** — the definition fits in two lines and needs no paper —
and it comes with forced positive controls (`C₅`, the unique `(3,5,13)` graph,
Paley(17)) that the pipeline must reproduce before any claim. All of them did.

**The result attempted.** Exhibit a doubly saturated `R(4,5)`-good graph on 19
vertices, or show none exists. Success would mean an explicit graph with a
complete witness certificate, checkable in milliseconds by exact integer
arithmetic.

## 5. How the rediscovery was caught

A subagent was commissioned to pin down the paper's exact definition **at the
same time as the first verification run** — before there was any result to
protect — because the definition itself was secondary-sourced. It returned the
continuation of the truncated passage: "an ansatz was made that a solution would
be circulant"; "There is a circulant doubly saturated R(4,5)-good graph on 19
vertices with distances {4,5,6,8}"; plus the family theorem "for all `t ≥ 4`,
there is a doubly saturated `R(4,t)`-good graph on `6t−11` vertices".

The evidence was not a judgement call. `{4,5,6,8}` appears verbatim in my own
printed hit list, as does `{3,7,8,9} = {t−2} ∪ [2t−3,3t−6]` at `t = 5`. I then
checked the family at `t = 4,5,6,7` directly from the definition: all four are
doubly saturated. The census had been reproducing a published theorem for an hour
without my knowing it.

The headline was withdrawn, the conjecture README opens with a rediscovery
notice, and no `PAGE.md` was written: a rediscovery plus a small new data point is
not page-worthy.

## 6. Cost

4 cores, 15 GB RAM. Full circulant census: under two minutes. Longest single run:
the `2²⁴` prescribed-symmetry sweep at `n = 24`, a few minutes. **No randomness
anywhere** — every search is exhaustive and deterministic, so there are no seeds
to record. Certificates are seconds per graph except at `n = 35`, abandoned.
