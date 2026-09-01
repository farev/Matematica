# 2026-08-27 — balanced-colorings

**Target.** Erdős Problem #617 (Erdős–Gyárfás, *Split and balanced colorings
of complete graphs*, Discrete Math. 200 (1999) (secondary)): call an edge
r-colouring of a complete graph **balanced** if every set of r+1 vertices
spans all r colours; the conjecture is that K_{r²+1} admits no balanced
r-colouring for any r ≥ 3. Known: proved for r = 3, 4; false for r = 2;
K_{r²} admits balanced colourings for some r but fails for infinitely many r
(all (secondary), from the problem page and the Lean formalization — see
connectivity). Today's target is the **first open case, r = 5: does K₂₆
admit a balanced 5-colouring?** Chosen because the bottleneck is
compute-shaped and the structure is tight: a pre-selection derivation today
shows AG(2,5) gives a balanced 5-colouring of K₂₅ (three-line pigeonhole:
each parallel class has 5 lines, so 6 points always contain two on a common
line in *every* direction; merge two direction classes), so T(5) ≥ 25 and
the whole question concentrates on one decidable instance; Turán counting
(each colour class needs ≥ 55 of the 325 edges, since its complement must be
K₆-free, ex(26;K₆) = 270) leaves only 50 slack edges across five classes —
rigidity that helps both a SAT refutation and a possible hand proof.
Achieved means: a certified verdict at K₂₆ — UNSAT at 5 colours with a
checked DRUP proof (the r = 5 case settled, first new case since 1999), or a
verified balanced 5-colouring (the conjecture refuted) — plus the K₂₅
construction verified exactly and machine certificates reproducing the
r = 3, 4 theorems. Partial credit: certified exclusion of structured witness
classes at K₂₆ and proved counting lemmas constraining any witness.

**Result.** PROVED + CERTIFIED (K₂₆ itself undecided at close — long runs
still going, see Next).

- **PROVED + CERTIFIED (construction).** T(r) ≥ r² for prime powers:
  colour K_{r²} on AG(2,r) by parallel classes with two merged; every
  (r+1)-set contains two points collinear in *every* direction
  (pigeonhole over the r lines of each class). K₂₅'s balanced
  5-colouring verified from the definition over all 177,100 6-subsets
  (K₉: 126, K₁₆: 4,368 likewise); equivalently the Reed–Solomon
  [5,2,4]₅ code. So r = 5 concentrates entirely on K₂₆.
- **PROVED (Fact A).** Balanced ⇒ no monochromatic K_{r+1} ⇒ at
  K_{r²+1} every colour class is an (r+1,r+1)-Ramsey graph (ω, α ≤ r)
  and every complement is K_{r+1}-free with χ ≥ r+1. Kills all
  partition-structured witnesses in two lines (the session's first
  proof used the Singleton bound via a codes⟺structured-colourings
  equivalence, kept in NOTE §2 for the construction framework); frames
  r = 2's C₅ as exactly the escape conjectured impossible for r ≥ 3.
- **CERTIFIED (sharp counting barrier).** With E*(N,s) = max edges with
  no K_s, no I_s: existence at K_{r²+1} forces E*(r²+1, r+1) ≥
  (r−1)/r·C(r²+1,2). Computed: **E*(10,4) = 31** vs threshold 30 — the
  proved r = 3 case is missed by ONE edge (UNSAT at 32 in 4.6 s);
  E*(17,5) ≥ 104 vs 102; **E*(26,6) ≥ 265** vs 260 (all witnesses
  definition-verified and committed). At r = 2 the threshold is tight
  and realized (C₅). The pure-counting and exact-rigidity routes to
  r = 5 are dead; the conjecture lives in the joint structure.
- **CERTIFIED (exclusions at K₂₆).** (i) The affine family (50 free
  pairs) does not extend to K₂₆: UNSAT with a 1,160-line DRUP proof
  checked by `tools/satcert/rup_check`; q = 2 positive control finds
  the 2 known K₄→K₅ extensions. (ii) No vertex-regular witness:
  invariant classes must have exactly 65 edges (2a+b = 5, PROVED),
  unsolvable over Z₂₆; over D₁₃ all 3,198 admissible classes fail
  α ≤ 5 (exhaustive, controlled). The r = 2 counterexample is a
  circulant; at r = 5 that door is provably shut.
- **CERTIFIED (modulo BreakID) + NUMERICAL (hardness).** The direct CNF
  is pigeonhole-hard: K₁₀ (135 vars!) defeats CaDiCaL, Glucose, kissat
  and RoundingSat unaided; with BreakID symmetry breaking K₁₀ is UNSAT
  in 3.1 s — the Erdős–Gyárfás r = 3 theorem machine-reproduced. K₁₇
  and K₂₆ (broken + Lemma-1 cardinality totalizers) outlasted the
  session's windows.

**What failed.** The Singleton-bound proof of structured-sector
emptiness (superseded by Fact A's two-liner, same afternoon). The
pure-counting kill (E* < threshold) — refuted at r = 3, 4, 5 by the
machine within minutes of formulation; its sharpness is the salvage.
The rigidity kill (E*(26,6) = 260) — refuted by a 261-edge witness.
RoundingSat without symmetry breaking — timed out even at K₁₀.
Second-order pair counting — reduces to twice the single-class bound,
no gain (recorded in WRITEUP so it isn't retried). Two
process-management mishaps (self-matching pkill; an orphaned solver
launch) cost ~15 minutes. The first circulant sweep printed half the
true edge count (α/ω filtering unaffected); caught against a hand
count, fixed, re-run.

**Next.** (1) The K₂₆ decision: the symmetry-broken + cardinality
instance needs verified symmetry breaking at scale (VeriPB-style),
cube-and-conquer, or an interaction lemma over the near-E* catalogue —
the running kissat windows may yet land (results to be appended to the
conjecture README when they stop). (2) Pin E*(26,6) (bracket [265, 269])
and E*(17,5) ([104, 108] — *correction 2026-08-28: the session's final
reasoned bracket is [104, 107], by Turán uniqueness of T₄(17); see the
conjecture README, which is authoritative*) exactly — new certified
extremal numbers
either way. (3) From an unblocked machine: read ErGy99 and
Füredi–Ramamurthi 2002 — the construction and the codes⟺MOLS remark may
be theirs; every (secondary) mark must be resolved before any external
claim. (4) The E*-catalogue route: if near-extremal (6,6)-graphs on 26
vertices are few, Proposition-4-style rigidity may survive in weakened
form (classes ∈ [56, 60] once E* is pinned).

## Connectivity check

2026-08-27, cloud sandbox, egress-proxied. Direct fetch BLOCKED: arxiv.org,
oeis.org, erdosproblems.com, mathoverflow.net, en.wikipedia.org,
api.semanticscholar.org, api.crossref.org, zbmath.org, sciencedirect,
journal sites, personal pages (empty or EGRESS_BLOCKED through the proxy).
WORKING: WebSearch (content snippets), raw.githubusercontent.com (full OEIS
entries via the oeis/oeisdata git mirror — primary OEIS text; also
teorth/erdosproblems `data/problems.yaml`, today's snapshot, and
google-deepmind/formal-conjectures Lean statements), PyPI (python-sat,
sympy installed). Consequence: every literature statement today is
**(secondary)** — search-snippet reconstruction — except OEIS entry text
and the two GitHub-mirrored databases named above. The `conjecture-research`
skill required by CLAUDE.md is not installed in this sandbox (ListSkills:
empty); CLAUDE.md discipline applied manually, as on 08-26. Environment:
4 cores, 15 GB RAM, Python 3.11.15, gcc 13.3.0, python-sat 1.9.dev15,
tools/satcert/rup_check compiled. Branch: claude/kind-bohr-4rq08f (the
session's provisioned branch; the mandate's claude/<conjecture>-date pattern
is overridden by the harness branch assignment).

## Candidate slate (external)

Three scouts ran in parallel (Erdős database via the teorth YAML snapshot +
domain-restricted search; OEIS via the oeisdata mirror; recent problem
lists/papers via search). Full reports in the session transcript. The slate,
spanning graph theory / number theory / combinatorics on words:

1. **Erdős #617, balanced colourings** (graph theory / generalized Ramsey).
   Statement above. Source: https://www.erdosproblems.com/617 (snippets,
   checked 2026-08-27: "proved it for r=3 and r=4 … false for r=2 … fails
   for infinitely many r if we replace r²+1 by r²", page last updated
   2026-04-01); teorth/erdosproblems problems.yaml (primary, today):
   status `falsifiable` (open subtype); `FormalConjectures/ErdosProblems/
   617.lean` tagged `research open` (formalized 2026-01-24). Open-status
   evidence: no solving paper or computational work under ~10 queries
   (scout log); the curated page records r=3,4 only. Believed open:
   high confidence. Caveat: ErGy99 and Füredi–Ramamurthi (JGT 2002, the
   only follow-up found) are unreadable here; their exact content is
   (secondary) throughout.
2. **Bala's 2023 supercongruence conjectures** on the classical
   plane-partition products (number theory / algebraic combinatorics).
   A049505 (symmetric plane partitions in the n-cube): a(p) ≡ 2^((p+1)/2)
   (mod p³) for primes p ≥ 3, checked by Bala to p = 1009; two further
   congruences at p², p³ (checked to 89). A005157 (totally symmetric plane
   partitions): a(p) ≡ 2^((p+5)/6) or 2^((p+1)/6) (mod p²) per p mod 6,
   checked to 1009. Source (primary, mirror read 2026-08-27):
   oeisdata seq/A049/A049505.seq (#41, Feb 19 2023 — untouched 3.5 years)
   and seq/A005/A005157.seq (#118, Jun 09 2026), conjecture lines
   unannotated. No proof found in searches; the 2026 prove-OEIS-conjectures
   ecosystem (Kallat arXiv:2607.18313, Fried arXiv:2607.24832 (secondary))
   has not touched the p-adic plane-partition cluster. In-session check
   today: both congruence families verified sharp at small primes (mod p²
   holds / mod p³ fails for A005157; mod p³ holds / mod p⁴ fails for
   A049505), and both product formulas reduced to factorial forms exactly.
3. **Additive cubes over 3-letter integer alphabets** (combinatorics on
   words). Quoted from the literature (secondary, checked 2026-08-27):
   "The cases {0, 1, 2}, {0, 1, 3}, {0, 1, 4} and {0, 2, 5} are left open"
   (Rao 2015 lineage; Lietard–Rosenfeld DLT 2020 ask to characterize
   avoidable ternary alphabets); Rao's conjecture: {0,i,j} coprime, j ≥ 6
   avoidable. Longest published {0,1,2} additive-cube-free word: 1288.
   No 2021–26 result closing any case was found. Compute shape: certified
   morphism search (decision algorithm of Currie–Mol–Rampersad–Shallit,
   arXiv:2111.07857 (secondary)) + exact avoidance-maxima DFS with this
   repo's additive-squares machinery.

Also surveyed and set aside (scouts' full arguments in transcript): queens
domination a(26) ∈ {13,14} (A075458 — witness branch is a lottery,
refutation plausibly 1–3 orders beyond a 4-core day; certified a(20)–a(25)
floor noted for a future session); peaceable queens on the torus a(19)
(A279405 — day-sized with this repo's engine but the entry moved twice in
ten weeks, Padhi/Harries clearly en route; also arguably an internal thread,
see below); C&C 2025 Problems 5.1/5.2 (2-homogeneous colourings of cubic
graphs — strong candidate, but a third consecutive cubic-graph SAT census
day for the same audience as 08-26); Erdős #287 (unit-fraction gaps — an
unread 18-post forum thread makes the frontier unverifiable from here);
Erdős #307 (Barbeau — clean but modest floor); Gaiser's restricted Schur
numbers (18-day-old paper whose own tables are unrecoverable from
snippets); Erdős #699 (kill-risk on the unreadable Erdős–Szekeres
original); #647 (solved this month, arXiv:2608.17880 (secondary) — the
certified-search niche moves fast); w(2;3,20) (n = 389 UNSAT, out of
4-core reach); 5-edge-connected 5-regular Class 2 census (order 16 wall);
A240443 a(11) (backup; modest audience).

## Internal-thread assessment

Recent sessions: 08-26 strong-truncations, 08-25 signed-difference-sets,
08-23 odd-giuga; no two-consecutive rule in force. Strongest live internal
threads: (i) **strong-truncations, Conjecture C's open half** (balloon-free
⇒ χ′ₛ(T(H)) = 6) — the sharpest mathematically, and a proof would upgrade
the row to a complete characterization; but the census already stands at
order 18, more census changes no row, and the open half's hard core is the
2-edge-connected case, which *contains* the intended reading of Kardoš's
problem — idea-bound, not day-shaped. (ii) **peaceable-queens family
continuation** (flat a(17), torus a(19), both named in the 08-17 log) —
genuinely day-sized with the validated SYM16 engine, but the torus entry is
being actively advanced by two named contributors this summer (scoop-heavy),
and the family has already produced its row. (iii) vdw-mixed w(2;5,8)
(≈ 296): the (4,7) certificate was an 18.4M-line proof; (5,8) at n = 296 is
far past a 4-core day. (iv) signed-difference-sets order > 36: documented
collision with Masselot's own continuation. Scored against the slate: no
internal thread beats the externals on bottleneck shape (a) — (i) is
idea-bound, (ii) is a scoop race on (b), (iii)–(iv) fail (a) or (b)
outright. The mandate's default (external) stands.

**Selection.** #617 over Bala and additive cubes: (a) the bottleneck is one
decidable instance plus structured probes (SAT with DRUP, exact
constructions), where Bala's headline needs a p-adic proof to land (its
certified arm alone is range extension) and the additive-cube morphism hunt
is a lottery against six years of prior mining; (b) #617 shows no trace of
any computational attack, and its first open case is cleanly delimited by
today's snapshot of two curated databases; (c) the audience is the Erdős
database, a living co-author's community, and the generalized-Ramsey f(n,p,q)
line — and either verdict at K₂₆ changes the problem page. Bala stays the
strongest fallback if K₂₆ stalls early.
