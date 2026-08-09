# 2026-08-09 — signed difference sets (closing open cells of Gordon's database)

**Target.** A signed difference set SDS(v,k,λ) in a finite abelian group G of
order v is an element A of the group ring Z[G] with coefficients in
{−1,0,+1}, exactly k nonzero, satisfying A·A^(−1) = k·e + λ(G−e) — difference
sets are the all-plus case, circulant weighing matrices the λ=0 cyclic case.
Gordon introduced them (Designs, Codes and Cryptography 91 (2023) 2107–2115,
arXiv:2212.10630) with a companion database (github.com/dmgordo/
signed-difference-sets) recording, for every admissible (v,k,λ,G), a status:
87 Yes, 59 All, 2,574 No, and **67,823 Open** — including 35 cells with
v ≤ 30. His exhaustive searches ran on cyclic groups (and not even all of
those); the non-cyclic small cells are open wholesale because nobody has run
even a basic search on them. The specific result attempted today, stated
before the production runs: **decide, with certified dual-implementation
exhausts or independently verified witnesses, at least ten previously-Open
cells of the database, prioritizing the complete v ≤ 30 block**; stretch:
the v ≤ 50 shelf and any structural lemma the pattern of decisions suggests.
Mid-session pivot pre-committed to Erdős #699 (below) if the engine had not
produced certified decisions by 16:30 UTC.

**Result.** *(finalized at session close — see §6)*
- **CERTIFIED** — new decisions of previously-Open cells of the database,
  each by exhaustive search in a validated C engine, with every witness
  re-verified by an independent Python checker and small cells additionally
  reproduced exactly (identical witness lists) by an independent pure-Python
  exhaust. Running count at first freeze: 6 (all NONEXIST):
  SDS(9,8,1,[3,3]), SDS(18,15,2,[3,6]), SDS(20,17,8,[2,10]),
  SDS(20,11,2,[2,10]), SDS(24,18,2,[2,12]), SDS(24,18,2,[2,2,6]).
- **CERTIFIED (audit)** — 147 of the 280 witness sets stored in the
  published database fail its own defining equation (21 of 144
  witness-bearing cells affected, all cyclic; no symmetry of the definition
  can repair a non-constant correlation profile, so this is not a
  convention mismatch — 123 cells including all Paley, all He–Chen–Ge and
  23 orbit-exhaust cells verify perfectly under the same checker). For the
  one affected cell small enough to re-exhaust immediately,
  SDS(20,11,2,[20]) (status "All", 4 stored sets, all invalid): the cell's
  existence status is **correct** — the complete enumeration has exactly 40
  labeled sets in 2 translation classes, and the stored sets are true sets
  with elements swapped between P and M (nearest true set at symmetric
  difference 4), pointing at an export-stage defect rather than a broken
  exhaust.

**What failed.**
- Engine v1's interval pruning double-removed pairs adjacent to
  decided-zero elements (openp underflow → false NONEXIST on the known
  cell SDS(11,6,1,[11])). Caught immediately by the known-cells control
  battery, fixed, and the fixed engine then reproduced the full v ≤ 24
  decided database (42 cells) with zero contradictions. The defect class
  "prune soundness only ever tested on cells where nothing exists" is now
  covered by EXIST controls.
- *(remainder finalized at close)*

**Next.** *(finalized at close)*

---

## 1. Connectivity check

| source | reachable | how |
|---|---|---|
| `arxiv.org` | **no** — EGRESS_BLOCKED at proxy (also `export.arxiv.org`, `www.arxiv.org`) | WebFetch/curl |
| `oeis.org` | **no** — EGRESS_BLOCKED | WebFetch |
| `erdosproblems.com` | **no** — EGRESS_BLOCKED | WebFetch |
| `mathoverflow.net` | **no** | WebFetch |
| `en.wikipedia.org`, `api.semanticscholar.org`, `papers.cool`, `alphaxiv.org`, `terrytao.wordpress.com`, `dmgordon.org`, `combinatorics.org` | **no** (scout probes) | WebFetch |
| web search | **yes** | main literature channel; snippets carry abstract text verbatim |
| `raw.githubusercontent.com` | **yes** | **primary-source channel**: Gordon's SDS database (today's deciding source), `teorth/erdosproblems` YAML (1217 problems), `google-deepmind/formal-conjectures` Lean statements, OEIS mirror `oeis/oeisdata` |
| `pypi.org` | yes (proxy bypass) | python-sat 1.9.dev11 |

The `conjecture-research` skill named in CLAUDE.md is still not installed in
this sandbox (ListSkills: no match); its written discipline is followed
directly. Working branch is the environment-provisioned
`claude/kind-bohr-ba93bm` (the harness forbids pushing elsewhere), not the
`claude/<conjecture>-<date>` naming the task prompt describes. Branch tip at
session start equals `origin/main` (245f33a; the 08-08 session is merged).

Infrastructure rebuilt before selection (candidate-agnostic): satcert C
tools compiled (`rup_check`, `check_coloring`); `glucose_static` 4.2.1
rebuilt from the python-sat sdist (streams DRUP to disk; toy UNSAT
proof-checked "s VERIFIED" by `rup_check`); CaDiCaL 3.0.0 built; pysat
Cadical153 importable. None of it ended up on today's critical path (the
selected attack is pure exact search), but it is standing for tomorrow.
Hardware: 4 cores, 15 GB RAM, Python 3.11.15, gcc 13.3.0.

## 2. The three external candidates

Built from four parallel scout subagents (fresh-arXiv quantity hunter;
Erdős-database computational shelves; flagged-papers reader + scoop guard;
non-Ramsey diversifier) plus my own vetting passes. Slate spans design
theory, combinatorial number theory, and combinatorics on words.

### E1 — Signed difference sets: close Open cells of Gordon's database *(design theory)* — SELECTED

*Statement.* As in the Target. Each Open cell is a concrete existence
question; a decision is a new labeled result either way (construction or
nonexistence).

*Source.* **Primary**: the database itself, fetched today from
`raw.githubusercontent.com/dmgordo/signed-difference-sets/main/`
(`sds.json`, sha256 `39bab9fc…ca85`; `sds_code.py` with Gordon's own
Sage checker `is_sds`, from which the definition was pinned; his README
declaring the JSON "all the data from the paper", CC-BY-4.0). The paper
arXiv:2212.10630 itself is egress-blocked (secondary, abstract-level); the
follow-up He–Chen–Ge, arXiv:2306.05631 (secondary) is already absorbed into
the database (ten cells credited "PDS construction of He, Chen and Ge").

*Why believed open.* Openness is recorded **per cell in the primary
artifact itself**, maintained by its author (Zenodo-versioned, contribution
culture). Scout searches for "signed difference sets" 2024–2026 return only
the two 2023 papers — no closure notes, no SAT sweeps, no AI-pipeline
activity. The scout validated the definition against a known cell and
exhausted the smallest Open cell (2,304 candidates, nonexistence, <1 s)
during vetting — unswept territory, not battle-hardened residue.

*Feasibility (measured, not estimated).* With |P| = (k+s)/2, |M| = (k−s)/2
forced by s = √(k+λ(v−1)), 27 of the 56 Open cells with v ≤ 32 have naive
cost below 10⁹ before pruning; the scout's one-cell demo and the in-session
engine (below) confirmed decision times of milliseconds-to-minutes per cell.

*Who cites it.* Gordon's database (updates credited; the DB is the area's
reference artifact); He–Chen–Ge's group for the next constructions paper.

### E2 — Erdős #699: Erdős–Szekeres common prime factors of binomial coefficients *(combinatorial number theory)* — pre-committed pivot

*Statement* (from the Lean formalization in
`google-deepmind/formal-conjectures`, fetched today — primary within that
mirror): is it true that for every 1 ≤ i < j ≤ n/2 there is a prime p ≥ i
dividing gcd(C(n,i), C(n,j))? [Erdős–Szekeres 1978]. Strengthening: apart
from a finite exceptional set of (n,i,j), one can take p > i.

*Why believed open.* Status "falsifiable" in `teorth/erdosproblems`
(fetched today, actively maintained — Jul–Aug 2026 status flips present);
zero mentions in the AI-contributions wiki (through Jun 30, 2026, absorbing
the DeepMind Gemini sweep arXiv:2601.22401 and the GPT-5 experiments
arXiv:2511.16072); no 2026 arXiv hit, while the *adjacent* binomial
problems #684/#400 have active summer-2026 papers (arXiv:2606.08216,
2605.21221, 2606.23661) — a hot neighborhood with this exact problem
untouched. No recorded verification bound anywhere; residual risk that
[ErSz78] itself contains small checks (paper unreachable — (secondary)).

*Feasibility.* Lucas-theorem bitsets: p ∤ C(n,i) iff every base-p digit of
i is dominated by n's; per-n descending-i sweep with running ORs,
≈ N³/(384 ln N) word-ops ≈ 2·10¹¹ for N = 10⁵ — hours in C. Upside: a
counterexample falsifies an Erdős problem; floor: first recorded bound plus
the census of exceptional triples for the p > i strengthening (OEIS-able).

*Why not selected.* Beaten by E1 on (b) — E1's openness is verified
per-cell from the primary artifact, #699's frontier is "no bound found",
an absence — and on measured (a). It is today's pre-committed pivot and a
strong future session.

### E3 — Minimum abelian squares in binary words: the Fici–Saarela ⌊n/4⌋ conjecture and the April 2026 extremal-word conjecture *(combinatorics on words)*

*Statement.* Fici–Saarela: every binary word of length n contains at least
⌊n/4⌋ abelian squares. Fazekas–Mammoliti–Mercaş–Simpson (arXiv:2604.23188,
Apr 25, 2026) slightly extend the conjecture, prove it for words with ≤ 3
occurrences of one letter, and exhibit per-Parikh-vector words conjectured
extremal — all (secondary), snippet-reconstructed.

*Own scoping computation (banked for a future session).* A 4-second
brute force over all binary words of n ≤ 18 (complement+reversal reduced)
shows: under both the distinct-factors and the nonequivalent counting, the
minimum is **exactly** ⌊n/4⌋ at every n ≤ 18, attained among others by
single-1 words 0^a 1 0^b with a+b balanced (whose abelian squares are
exactly the 0^{2j}, giving ⌊⌈(n−1)/2⌉/2⌋ = ⌊n/4⌋ — so the conjecture's
content is the lower bound); under the occurrences counting the minimum is
the irregular 0,0,0,1,2,3,4,4,5,6,7,8,10,11,12,14,15,17 (n ≤ 18), which
matches no OEIS sequence findable by search — a candidate new sequence.
The 2019 Triki claim that surfaced in a garbled snippet was disambiguated
today: it targets the Fici–Mignosi *maximum*-count conjecture, not this one.

*Why not selected.* The authors' own verification range and per-(a,b)
tables are in the blocked PDF, so every "new" value risks silent overlap —
the weakest novelty position of the three (the same handicap the 08-08
session had to manage). Kept as a strong future candidate, ideally on a
machine that can read the PDF first.

### Also vetted and set aside today

Permutational (reflective/dihedral) Ramsey grid, arXiv:2607.06817 (Jul
2026; freshest quantity of the day, natural DRAT certificates — but the
definitions and all published cell values sit in blocked PDFs, so semantic
controls reduce to reconstruction-from-abstracts; too much convention risk
for a certified session); Zarankiewicz z(m,n;3,3) gap-1 cells from
arXiv:2605.01120 (41 open cases, some within one edge — but *which* cells
are gap-1 is in the blocked PDF and no author data repository exists);
Erdős #366 (consecutive powerful pairs with a cube-full member: the 10²²
frontier has primary provenance in OEIS A060355's b-file and a cube-full
enumeration reaches 10²⁴ in ~2 CPU-hours — strong, but census-shaped four
days after the 08-05 powerful-numbers census; banked); Erdős #458 (lcm
across prime gaps to 10¹⁶ with a margin table — clean but lowest
mathematical content of the shelf); planar-difference-set PPC verification
(stuck at 2·10⁹ since 2004 — needs Gordon's two PDFs committed locally
first); Folkman gaps from arXiv:2605.16542 (Radziszowski/Van Overberghe
own the tooling); the CW sibling database (2,773 Open but 25 years of
Arasu–Strassler effort — hard residue, unlike the unswept SDS cells);
zero-sum small cases (an AI-driven pipeline is visibly harvesting exactly
this niche — arXiv:2607.14379); Erdős DB kills recorded by the scout with
one-line reasons (#19, #475, #506, #547, #556, #580, #742, #23, #107,
#617 (r=4 now proved, r=5 ≈ 1.15M-clause 5-coloring UNSAT — out of hours
range), #723, #779, #1082, …) — full list in the scout report, banked in
this log's history.

### Intelligence surfaced by the scoop-guard scout (acted on today)

- **arXiv:2608.02675 (Tranquilli, Aug 2, 2026)**: certified exhaustive
  computation — every cubic bipartite graph on ≤ 58 vertices contains a
  cycle of length 4, 8 or 16, so cubic bipartite Erdős–Gyárfás
  counterexamples need ≥ 60 vertices. **Supersedes this repository's
  bipartite-cubic shelf** (girth-≥6 bipartite cubic, n ≤ 26, 2026-07-30).
  Recorded today in `conjectures/erdos-gyarfas/README.md` (secondary).
- **arXiv:2605.22844 (Carr, May 2026)**: minimal Erdős–Gyárfás
  counterexamples have deg-≥4 vertices independent, every vertex adjacent
  to a degree-3 vertex, ≥ 4/7 of vertices of degree 3. Composes with the
  repo's certified n ≤ 18 into a cheaper n = 19 closure — recorded as an
  open thread (secondary; his proofs unread).
- **arXiv:2606.23721 (Muney, Jun 2026)**: valid-extension sets of finite
  Gilbreath sequences can have interior holes (smallest at (2,3,5,9,15));
  corrected extension theory with exact criterion. Flagged in
  `conjectures/gilbreath/README.md` (secondary).
- **Scoop guard, clean negatives**: no v2 of Gaiser–Ramezanpour, nobody
  computing f₂(9)/f₂(10), no even-k theorem — reciprocal-rado safe; nothing
  after Song–Mao on S(3;s,t,u) — generalized-schur safe. Adjacent new:
  arXiv:2605.15147, 2608.03661 (Schur-like equation thresholds),
  2607.15034 (S(k+2) ≥ 10·S(k)+2, S(8) ≥ 5362). The Quanta piece
  "Why the Legendary Erdős Problems Are Falling to AI" (Aug 3) confirms
  harvesting pressure on proof-shaped problems — the certificate-shaped
  niche this repository occupies remains comparatively quiet.

## 3. The internal thread

Strongest live internal thread: **reciprocal-rado, k = 9** — the 08-08
session left a prediction on record (f₂(9) ∈ {245, 246} against the
Gaiser–Ramezanpour bound 244) with the n = 243 decide in flight at close,
and k = 10 is Conjecture B's first genuinely new test. Both would change
the row; the toolchain was rebuilt and validated this morning. (a)
compute-shaped: yes, measured yesterday. (b) novelty: certain. (c) cites:
Gaiser–Ramezanpour directly. Runner-up: generalized-schur (4,4,u ≥ 10) —
the 08-07 OOM blocker is exactly what today's rebuilt disk-streaming
glucose removes. Newly surfaced third option: Erdős–Gyárfás n = 19 closure
via Carr's constraints (above) — real, but generation-heavy (the n = 19
class was measured at ~30× the n = 18 scan) and resting on unverified
(secondary) structural theorems.

The internal thread does not clearly beat E1: reciprocal-rado would be a
second consecutive session on the same conjecture against a mandate whose
default is external and whose tie-break goes to the new; and E1's novelty
position (per-cell primary verification) is strictly stronger than any
internal option's marginal-value case. External it is.

## 4. Selection argument

(a) *Compute-breakable?* E1: yes — measured at three scales before
selection (scout's 1-second cell; my cost table with |P|/|M| forced by s;
27 cells under 10⁹ naive). E2: yes (word-op arithmetic done, ~hours), E3:
yes but with unbounded-depth risk in the B&B. Internal: yes.
(b) *Already done?* E1: openness is per-cell ground truth in the author's
own maintained artifact, fetched today — the strongest novelty position of
any candidate this repository has had (better even than 08-07's
primary-read paper, because here the *frontier itself* is machine-readable).
E2: absence-of-evidence frontier. E3: their table is in a blocked PDF.
(c) *Citing target.* E1: the database itself (versioned, credited), the
He–Chen–Ge line. E2: erdosproblems.com + the active binomial cluster.
E3: the April 2026 authors.

E1 wins (b) outright and ties or wins (a); ties break to the newest
subfield for this repository regardless. E2 is the pre-committed pivot
(trigger: no certified decisions by 16:30 UTC — not fired; first certified
decisions landed ~12:50 UTC).

## 5. Tool discipline

Positive controls, all run before any new claim:
- **Definition control**: independent Python checker (`sdslib.py`, no code
  shared with Gordon's Sage `is_sds`) run against **every witness stored in
  the database**: 133/280 sets in 123/144 witness-bearing cells verify —
  including all 44 Paley cells, all 10 He–Chen–Ge cells, and 23
  orbit-exhaust cells — pinning the definition; the 147 failures
  concentrate in 21 cells and are themselves a *finding* (§6), not a
  checker defect: no symmetry of the definition (translation, decimation,
  automorphism, global flip, inversion) can repair their non-constant
  correlation profiles, and the one re-exhausted cell proves the true sets
  sit two P/M-swaps from the stored ones.
- **Negative control**: 8/8 sign-corrupted witnesses rejected by the
  checker.
- **Engine controls**: the C engine reproduces the **entire decided
  database at v ≤ 24** — 42 cells, every No → NONEXIST, every Yes/All →
  EXIST with independently verified witnesses, zero contradictions; on 8
  small cells (including two Open ones) an independent pure-Python exhaust
  reproduces the engine's witness lists **exactly**; the engine v1 pruning
  bug was caught by exactly this battery (What failed).
- **Soundness of the one search reduction**: translation by −p for p ∈ P
  maps any SDS to one with 0 ∈ P and preserves the defining equation, so
  restricting the exhaust to A(0) = +1 preserves existence and
  nonexistence; |P| ≥ 1 holds in every admissible cell (s ≤ k). Parity and
  integrality of s are checked per cell (violations reported as trivial
  nonexistence, none encountered in swept cells).
- Determinism: no randomness anywhere; runtimes, node counts, engine and
  source sha256 in `data/results.csv`; database snapshot sha256 pinned in
  every certificate. Environment: 4 cores, 15 GB RAM, gcc 13.3.0,
  Python 3.11.15.

## 6. Results

*(finalized at session close)*
