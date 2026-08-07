# 2026-08-06 — circular repetition thresholds (session 2)

**Target.** `CRT_W(4) = RT(4) = 7/5` — the most prominent open case of the
Currie–Mol–Rampersad conjecture — via the one route the 2026-08-03 session
proved is not yet closed: uniform binary morphisms in **Pansiot's encoding**,
where Proposition N does not apply. Secondary targets `n = 6, 8` (even), for
the reason under *Prior-work discovery* below. The session plan: prove an
exact repetition-transfer lemma between an `n`-ary word and its Pansiot
codeword, search exhaustively for uniform binary codeword morphisms compatible
with the symmetric-group structure, certify a hit by a finite criterion, and
close with a monodromy-trivial circular seed via Lemma A/Theorem C (2026-08-03,
already PROVED).

**Result.** **PROVED — `CRT_W(6) = RT(6) = 6/5`**, an open case of the
Currie–Mol–Rampersad conjecture (openness (secondary): Mol–Rampersad 2020
list `4 ≤ n ≤ 44` open; Tunev's Dec-2025 constructions are reported only for
*odd* `n ≥ 5`, and `6` is even). **PROVED — `CRT_W(5) = RT(5) = 5/4`**
(flagged as a plausible rediscovery of Tunev-type results pending a read of
arXiv:2512.24581). Both via new machinery, all **PROVED** today: a slot
lemma (decoded patterns are bit-intrinsic), an exact repetition-transfer
lemma between a word and the monodromy structure of its Pansiot codeword, a
finite certificate (Theorem MC) that a uniform binary code morphism
preserves code-freeness, and a circular pumping lemma in the code (Lemma
PC). Instances: certified `k = 21` morphisms for `n = 5, 6` with seeds
extracted from **session 1's own certified spectrum witnesses**; pumped
words directly verified to lengths 17 199 (`n = 6`) and 12 348 (`n = 5`),
with session 1's independent checker confirming where it can reach. The
machinery re-derives `CRT_W(3) = 7/4` end to end as a control (`k = 19`
generators). **CERTIFIED** — the same ansatz is *empty* at `n = 4`: no
viable pair over all pooled monodromy classes for `k ≤ 46` (every pooled
pair refuted by an explicit offender), nothing in the two-level engine
ranges. Pansiot's exceptional alphabet resists inside its own encoding.

**What failed.** (1) The first filter (preservation on all valid 14-blocks)
was too strong and its pool too narrow — half the day went to discovering
that the right requirements are fixed-point freeness plus a complete
monodromy classification. (2) `n = 4`, the day's declared target: empty at
every rung (letterwise `k ≤ 46`, two-level engine, preservation filter) —
the pre-registered mid-session pivot was taken, and then the `n = 5, 6`
sweeps unexpectedly crossed their viability thresholds (`k = 21`).
(3) `n = 8`: 44 viable pairs at `k = 28`, all failing Theorem MC's
first/last-bit injectivity hypotheses — the criterion, not the search, is
the bottleneck there. (4) The `(σ, ρ)` two-level engine found nothing
anywhere. (5) One filter bug ((Hc) checked the wrong side) was caught before
any certification; one margin (`N_0`) was strengthened during proof-writing
with all certificates surviving unchanged.

**Next.** (1) Read Tunev (arXiv:2512.24581) and Moulin Ollagnier from an
unblocked network; fix the novelty map for `n = 5` and the "open for
`4 ≤ n ≤ 44`" statements. (2) A synchronization-based variant of Theorem MC
without (Ha)/(Hb) — it would likely unlock `n = 8` immediately (candidates
are already in `data/`), then `n = 10, 12, …`: each even case is a
potential new settled case. (3) `n = 4`: either push the certified emptiness
into an impossibility proof for the code ansatz, or find the first candidate
beyond `k = 46`. (4) This is the second consecutive session on this
conjecture — the next session works something else regardless.

---

## 1. Connectivity check

| source | reachable | how |
|---|---|---|
| `arxiv.org`, `export.arxiv.org` | **no** — HTTP 403 (CONNECT rejected at egress proxy) | WebFetch, curl |
| `oeis.org` | **no** — HTTP 403 | WebFetch, curl |
| `erdosproblems.com` | **no** — HTTP 403 | WebFetch, curl |
| `mathoverflow.net` | **no** | WebFetch |
| web search tool | **yes** | titles, URLs, synthesized snippets |
| `pypi.org` | yes (proxy bypass list) | pip works |

The proxy status endpoint (`__agentproxy/status`) reports the denials as
gateway policy ("connect_rejected … policy denial"), same as 2026-08-03, so
they were not retried or routed around. **No primary source was opened at any
point today. Every citation in every document from this session is
(secondary), and every "this is still open" claim is a search-snippet claim.**
Mitigation as on 08-03: a problem whose mathematics is self-contained, and
calibration of every pipeline against published constants before any claim.

Machine: 4 cores, 15 GB RAM, Python 3.11.15, gcc. Branch note: the platform
assigned this session the branch `claude/kind-bohr-6n8uoj` with an instruction
to push only there; it plays the role of `claude/circular-thresholds-2026-08-06`.

## 2. The three external candidates

Built by three parallel subagent surveys (additive/combinatorial number
theory; discrete geometry and designs; open problems in papers from the last
24 months), each instructed to double-source openness from search snippets.
Full reports preserved in the session transcript; the slate spans three
subfields.

### E1 — `a(10)` of OEIS A276661: least largest element of a 10-element distinct-subset-sums set *(additive number theory)*

*Statement.* `S ⊂ Z_{>0}`, `|S| = n`, has distinct subset sums (DSS) if all
`2^n` subset sums differ. `a(n)` = least `k` such that an `n`-element DSS set
fits in `{1,…,k}`. Known `a(1..9) = 1, 2, 4, 7, 13, 24, 44, 84, 161`
(Lunnon through `a(8)`, Grossman `a(9)`); `220 < a(10) ≤ 309`, the upper
bound being the 10th Conway–Guy number (DSS-certified by Bohman, PAMS 1996).
Determine `a(10)`.

*Source (secondary, seen 2026-08-06).* OEIS A276661 snippet: "Only the first
nine numbers of this sequence are known … a(10) > 220"; erdosproblems.com #1
snippet marks the parent Erdős $500 problem OPEN with Bohman's `0.22002·2^n`
still the best construction (unimproved since 1998).

*Why open.* OEIS is the canonical registry for exactly this number and lists
nine terms; no search result claims a tenth. Recent activity around the
problem (arXiv:2510.06032, arXiv:2606.24139) leaves the term unclaimed.

*Assessment.* (a) Compute-breakable in principle — exact branch-and-bound over
`m = 221…309` — but the tree size is unknown and its being open for a decade
is weak evidence it is large. Scout's estimate ~25–35% for full determination.
(b) Novelty check is clean (OEIS as registry). (c) Extends Lunnon (Math.
Comp. 1988), Grossman, Bohman; cited in OEIS and on erdosproblems.com #1.

### E2 — the CRIM even-rank conjecture *(combinatorial game theory, paper of 2026-06-15)*

*Statement.* CRIM is the impartial game on integer partitions where a move
removes one row or one column of the Young diagram and re-sorts; last move
wins. Conjecture (Bašić–Gottlieb–Krnc, arXiv:2606.16828, June 2026): every
P-position has even Dyson rank (largest part minus number of parts).

*Source (secondary, seen 2026-08-06).* arXiv:2606.16828 snippets: "The
authors conjecture that every losing partition has even rank"; "holds for
(thick) hooks and rectangles … the converse fails … on odd staircases."

*Why open.* Seven-week-old conjecture; three snippet pulls show it live, no
citing follow-up found. (Openness of something this fresh cannot be
double-sourced; recorded as "no evidence of resolution as of 2026-08-06".)

*Assessment.* (a) Fully compute-breakable: exact DP over all partitions of
`m ≤ N`, `N ≈ 85` in-session; a refutation (odd-rank P-position) or a
certified verification range is guaranteed by construction — scout's
P ≈ 0.9 for *some* labelled result. But the authors' own verification range
is invisible in snippets, so the likely outcome — "verified to N" — risks
being exactly the comfortably-finishable sweep the mandate excludes.
(b) Duplication: the three authors are actively working this. (c) Extends one
fresh paper.

### E3 — no-three-in-line numbers on the discrete torus, `T(Z_m × Z_n)` for `8 ≤ m ≤ 12` *(discrete geometry)*

*Statement.* On `Z_m × Z_n`, lines are cosets of cyclic subgroups;
`T(Z_m × Z_n)` = max size of a subset with no 3 collinear points. Exact
values known for `2 ≤ m ≤ 7`, `2 ≤ n ≤ 19` (Fowler–Groot–Pandya–Snapp 2012,
Gröbner bases); `T ≤ 2gcd(m,n)`; prime gcd fully solved (Misiak et al.,
Discrete Math 2016). Open: composite-gcd pairs with `m ≥ 8`, e.g.
`T(Z_8×Z_8)`, `T(Z_9×Z_9)`, `T(Z_{12}×Z_{12})`.

*Source (secondary, seen 2026-08-06).* arXiv:1203.6604 snippet (table bounds);
search synthesis of the Misiak et al. line: "exact values are only
definitively known when gcd(m,n) is prime, leaving composite values as open
cases."

*Why open.* Last exhaustive table 2012; last movement in the subarea 2019 (a
"periodicity" paper whose contents are not visible — the main duplication
risk); the 2018 successor paper moved to higher dimensions instead.

*Assessment.* (a) Fully compute-breakable: ~50 ILP/SAT instances on ≤ 228
cells each; scout's P ≈ 0.85. (b) The unread 2019 paper may cover some
values. (c) Extends a quiet 2012–2016 thread; value modest (table extension +
possible OEIS sequence).

*Scouted and set aside* (recorded because the negative space is informative):
Bohman's DSS record and sum-free(13) (same scout as E1); RT_rich(4)
(conjectured target value not extractable from snippets); Halve Nim
(rules/tables unfetchable); γ(Q_26) (25-year frontier but an active SAT group
— Rostami–Bright arXiv:2508.11945 — owns the toolchain); knight domination
A006075; and a ruled-out ledger showing the 2025–26 SAT/LLM wave has swept
no-three-in-line (grid ≤ 60), Kobon 11/21, small-n Heilbronn, Oberwolfach
≤ 100, queens enumeration ≤ 19, srg(85,14,3,2) — the traditional cheap
targets in these subfields are being harvested industrially, which raises the
relative value of problems needing bespoke theory over raw search.

## 3. The internal thread, and a prior-work discovery that reshapes it

**The repo's strongest live thread** is the one the 2026-08-03 session named:
run the Theorem C search in **Pansiot's encoding**, where morphisms need not
be shift-equivariant over `Z_n` and the Proposition N obstruction does not
apply. Lemma A + Theorem C (PROVED, 08-03) reduce `CRT_W(n) = RT(n)` to two
finite searches; Theorem N′ (PROVED, 08-03) closed the naive normal form for
`4 ≤ n ≤ 9`, so the encoded normal form is exactly what remains. Significant
progress today = a morphism-plus-seed hit at any open `n`, which settles an
open case of a published conjecture and changes the conjecture's row; the
honest fallback = an exhaustive negative in the encoded ansatz over stated
ranges (a Theorem N′-style result), which also changes the row.

Runner-up internal thread (recorded for completeness): additive-squares —
close the `v = (1,1,0)` tree for a second Freedman-type theorem. Concrete,
but the 08-01 session's probes suggest a depth-~440 tree whose full closure
cost is unknown, and it lacks the leverage of two already-proved reduction
theorems waiting for input.

**Prior-work discovery (made during today's survey, step 2).** A December
2025 arXiv paper — **arXiv:2512.24581, Igor N. Tunev, "On Circular Threshold
Words and Other Stronger Versions of Dejean's conjecture", in Russian** — is
an edited write-up of the author's 2011/2013 student theses. Snippets state:
"In a 2011 work, new methods of proving the Dejean conjecture were proposed
**for some odd cases n ≥ 5** … the constructed threshold words are
cyclic/ring threshold words (**where any cyclic shift is a threshold word**)."
A length-`m` word all of whose cyclic shifts are threshold words is precisely
a circular threshold word of length `m` (both conditions say every factor of
`w^ω` of length `≤ m` has exponent `≤ RT(n)`), and a proof of Dejean for
alphabet `n` produces them at infinitely many lengths — so **Tunev's
construction, if it is what the snippet says, settles `CRT_W(n) = RT(n)` for
some odd `n ≥ 5`, from late 2025** (with the caveat that the companion
peer-reviewed Tunev–Shur MFCS 2012 paper covered two *different*
strengthenings — growth, and finitely many distinct repetitions — which is
consistent with Mol–Rampersad 2020 still calling all of `4 ≤ n ≤ 44` open).
Which odd cases, and whether the argument is complete, cannot be determined
from snippets; the paper is in Russian and unfetchable here. **(secondary)**

Consequences adopted today: (i) the target moves to **`n = 4`** — outside
"odd `n ≥ 5`" under every reading, the alphabet where `RT(4) = 7/5` is
Pansiot's exception, and the case with the strangest spectrum data (late gaps
147, 154) — with even `n = 6, 8` as secondary targets; (ii) any `n = 5`
result today is treated as a probable rediscovery of Tunev-type results and
labelled so (useful as a positive control, like the `n = 3` control on
08-03); (iii) the existing conjecture documents get a Tunev caveat regardless
of today's outcome, since their "open for 4 ≤ n ≤ 44" line is now doubtful
for some odd `n`.

## 4. Selection

Scores against the mandate's criteria:

- **(a) compute-breakable?** E2 and E3 fully (but with modest ceilings:
  a verification range of unknown novelty, resp. a table extension); E1 in
  principle (tree size unknown; decade of neglect is mild evidence it is
  big). Internal: the two finite searches are demonstrably cheap — today's
  first probe already enumerates the valid-block language (36 blocks at
  length 14 for `n = 5`) and finds group-compatible morphism pairs from
  `q = 11` — the open question is whether a *survivor* exists, i.e. the same
  existence-lottery shape as E1, but each ticket costs seconds, the whole
  space to practical depth costs an afternoon, and an exhaustive miss is
  itself a theorem-shaped negative (as Theorem N′ was on 08-03).
- **(b) already done?** E1 clean (OEIS registry). E2 risky (authors' own
  range invisible). E3 risky (unread 2019 paper). Internal: mapped in detail
  today — Tunev covers some odd `n ≥ 5`; `n = 4` and even `n` are outside
  every reading of the snippet, and Mol–Rampersad 2020 states them open.
- **(c) whose work does it extend?** Internal wins outright: a hit extends
  Mol–Rampersad (their own stated open case), Currie–Mol–Rampersad, and
  complements Tunev's fresh paper — the tightest citation triangle on offer.
  E1 extends a lineage (Lunnon/Bohman/OEIS) with no active paper; E2 one
  seven-week-old paper; E3 a quiet thread.

**Selected: the internal thread, target `CRT_W(4) = RT(4)`.** The argument
that it clearly beats the externals: it dominates E2 and E3 on value (their
realistic outcomes are range/table extensions — the kind of result the
mandate explicitly discounts — while a hit here settles a named open case,
and even the exhaustive-miss branch produces a citable structural negative
with the machinery already half-built); against E1 it splits (a) (both are
existence lotteries; the internal one's tickets are cheaper and its miss is
worth more), wins (b) after today's Tunev mapping, and wins (c). Two further
factors, stated honestly: the repo carries two PROVED reduction theorems
(Lemma A, Theorem C) plus calibrated SAT/checker infrastructure that only
this choice can leverage — roughly half a session of validated tooling — and
the Tunev discovery makes documenting this conjecture's true state of the art
obligatory today anyway. This is session 2 of 2 permitted consecutive
sessions on this conjecture; tomorrow works something else regardless of
outcome.

**The result attempted today, in one paragraph.** Prove `CRT_W(4) = RT(4) =
7/5` (secondary targets `n = 6, 8`) by: (1) proving an exact two-way transfer
lemma between repetitions in a 4-ary word and (bit-period, trivial-monodromy)
runs in its Pansiot codeword; (2) exhaustively searching uniform binary
codeword morphisms `φ` compatible with the `S_4`-structure
(`g(φ(b)) = π⁻¹ τ_b π`) that preserve code-freeness, certified by a finite
Theorem-M-style criterion built on (1); (3) exhibiting a monodromy-trivial
cyclic seed codeword with the `+2` window margin; (4) concluding by Lemma
A/Theorem C (08-03) that circular 4-ary threshold words exist at lengths
`k^j m_0` for all `j`, hence `C(4)` is infinite and `CRT_W(4) = RT(4)`.
Success = any single `(φ, seed)` pair passing all finite checks, each check
re-verified by an independent from-the-definition implementation. Mid-session
checkpoint pre-registered: if no `φ` survives the necessary preservation
filter for any `n ∈ {4, 5, 6}` at block lengths within reach by mid-session,
pivot to (i) relaxations (morphism powers `φ ∘ φ`, non-uniform `φ` with an
`S_3` margin variant of Lemma A, seed-relative preservation), and if those
also come up empty, (ii) consolidate the exhaustive negative as a theorem
with stated ranges, document the Tunev correction, and log the miss.

---

*(Sections below written as the session progressed.)*

## 5. Attack narrative (what was tried, in order)

1. **Probe: letterwise binary code morphisms, preservation filter.** C2
   conjugacy pools at `n = 4, 5, 6`, `k ≤ 26`: thousands of pooled pairs,
   zero passing preservation-on-14-blocks. Diagnosed as the wrong filter.
2. **Theory pass 1.** Slot lemma (patterns are bit-intrinsic) ⟹ the
   relativised route needs only fixed-point freeness; monodromy
   compatibility classified (C2 / sign / collapse-1 / collapse-2) ⟹ pool
   enlarged. `n = 3` control: candidates from `k = 7` — pipeline validated
   (and the `n = 4` emptiness thereby shown to be real signal, not a bug).
3. **Deep sweeps.** `n = 4`: zero through `k = 46` (full pool). Two-level
   `(σ, ρ)` engine: zero everywhere it ran (`r ≤ 10, s ≤ 5`; `r ≤ 7,
   s ≤ 6`; one capped cell at `r = 7, s = 7` disclosed). Autopsy: seam
   deaths, periods 3–10, 89 % within two generations.
4. **Mid-session checkpoint (pre-registered) taken:** re-scoped to
   machinery + `n = 3` control + certified negatives.
5. **Theory pass 2 (certification core).** Exact transfer lemma T with the
   `(n−1)` left-extension; empirically validated to exactness (2 238
   (word, p) tests, zero mismatches after the bare-block correction);
   Theorem MC (finite preservation certificate) proved — the descent closes
   in one shot because the return direction of T regains the `n−1` letters.
6. **The turn.** Recovered sweep logs: `n = 5` (533 candidates, `k ≤ 40`)
   and `n = 6` (380, `k ≤ 33`). Certification chain passes 4 pairs at
   `n = 6`, 3 at `n = 5` (smallest: `k = 21` both). Seeds found by
   Pansiot-encoding session 1's certified spectrum witnesses (`m = 39` at
   `n = 6`, `m = 28` at `n = 5`). Lemma PC assembles the theorems; direct
   verification tables computed; session 1's independent checker concurs
   where feasible.
7. **Opportunistic `n = 8`:** 44 candidates at `k = 28`, none passing
   (Ha)/(Hb) — logged as the sharpest tool gap.

## 6. Cost

4 cores, 15 GB RAM. Letterwise sweeps: seconds to ~2 min per `k` (the
`n = 6` levels near `k = 33` are the slow end, ~5 min). Engine grids:
seconds to ~90 s per cell. Certification: seconds per pair (pure Python)
after a numpy pre-pass. Pump verification to length 17 199: seconds; the
137 180-length `n = 3` word: ~2 min. No randomness affects any claim; the
transfer-lemma validation uses seeded randomized DFS (`seed=7`, `seed=13`)
and the validation suite `seed=11`.

**Deliverable labels, summarised.** PROVED: Lemmas S/F/T/PC, Theorem MC,
Theorem C-code, Theorems P5/P6, Result P3′ (control, known). CERTIFIED:
Result N2 (`n = 4` emptiness on stated ranges), sweep tables, certified
instances file. Openness of the settled cases: (secondary) throughout.
