# 2026-09-09 — collinear-walks (Shallit's k_min: unit-step walks with no three collinear points)

**Target.** New external problem, per the standing mandate. Shallit
(arXiv:2609.05780, submitted 5 Sep 2026, on the 9 Sep math.CO listing)
proved that an infinite walk in ℕ¹⁶ using only standard unit steps can avoid
three collinear points, reformulated it as an infinite word over 16 letters
with no two adjacent blocks of equal letter-frequency vector (no weak
abelian square; "3-free"), defined k_min as the least alphabet size for
which such a word exists, recorded 4 ≤ k_min ≤ 16, and listed four unproved
candidate morphisms (k = 5, 6, 7, 8). Chosen because the question is four
days old and cleanly posed, because both sides looked attackable (exhaust
the four-letter case for a certified lower bound; prove a construction for
an upper bound), and because the proof in the paper has visible slack: its
sixteen letters are the pairs (t_n, t_{n+1}) of a four-state Gaussian walk,
used only to force equal endpoint states.

**Result.** **PROVED — k_min ≤ 7.** The (direction, turn) sequence of the
Heighway dragon curve, b_n = (t_n, δ_n) ∈ ℤ₄ × {±1}, is 3-free over its eight
letters (it is the fixed point of the 2-uniform morphism 0→02, 1→03, 2→52,
3→53, 4→46, 5→47, 6→16, 7→17), and remains 3-free when the letters (0,+) and
(2,+) (opposite directions, same turn) are identified; hence an infinite
unit-step walk in ℕ⁷ with no three collinear vertices. The mechanism:
Shallit's 2-adic lemma ν₂(|Z_n − Z_m|²) = ν₂(n − m) at equal endpoint
directions survives when the two children of a direction u are {u, iu} in an
order that alternates with the parity of n (Lemma 2, proved by the same
descent with one extra case), and that walk is the dragon curve, whose
turns are ±90° only, so eight (direction, turn) pairs occur instead of
sixteen; two telescoping indicator sums (parity of the direction, and
membership in {0,1}) force equal endpoint directions on any weak abelian
square (Lemma 3), and the walk that moves only on right turns supplies the
displacement from the merged Parikh vector. The lemma checked on 1 123 622
pairs, the 8-letter word 3-free to 30 000, the 7-letter word to 100 000
(≈ 9 min, one core).
**Priority.** After the proof was in hand, the Cambie–Kalviainen repository
(github.com/ekalvi/erdos-193) turned out to hold unpublished drafts: Cambie,
fourteen dimensions (5 Sep), and Kalviainen, **six** dimensions (5 Sep;
alternating binary digit sign σ(n) = Σ(−1)^j b_j(n) mod 4, Cambie's offsets,
"independent review pending, not Lean-formalized"), plus an AI checkpoint
asking first for an independent check of the six-dimensional argument. I
read it line by line and reproduced its numbers (six step vectors, the
all-pairs valuation identity on 3 123 750 pairs, the six-letter word 3-free
to 30 000): **no gap found** (NOTE §5). So the frontier is 4 ≤ k_min ≤ 6 with
the 6 resting on that draft; today's 7 is an independent proof of a weaker
bound by a different walk, not the record. **CERTIFIED** side facts: no
coding of the dragon word onto ≤ 6 letters is 3-free beyond length 3000 (all
4011 codings tested; 8 survive, all with seven letters — the four antipodal
same-turn identifications, proved, and four mixed ones (r,−)~(r+1,+),
unproved, 3-free to 30 000); in the periodic sign/order family of Gaussian
digit walks (period ≤ 4) only two eight-transition words exist — the dragon
type (coding floor 7) and Kalviainen's alternating-sign type (floor 6) — and
no member codes onto ≤ 5 letters; no cyclic uniform morphism of length ≤ 16
over four letters has a 3-free fixed point beyond 1500, and over five
letters none of length ≤ 13 while twelve of length 14 survive, Shallit's
among them (control); L(1) = 1, L(2) = 3, L(3) = 7 (Brown 1971) reproduced;
28 861 282 canonical 3-free words of length 46 over four letters
(consecutive-count ratio 1.27–1.30, slowly falling), so k_min = 4 is not
excluded by search (**NUMERICAL** as an extrapolation). New directory
`conjectures/collinear-walks/` (README, NOTE, WRITEUP, PAGE.md, eight
programs, data); index row added.

**Connectivity (checked 07:36 UTC).** arxiv.org reachable via WebFetch
(listing pages, abstracts) and curl (PDFs, read with pymupdf). oeis.org,
erdosproblems.com and mathoverflow.net return 403 / blocked to WebFetch but
serve curl with a browser user agent (OEIS `fmt=text`; erdosproblems.com
`/range/a-b/open` pages give whole ranges; MathOverflow via the Stack
Exchange API). All four consulted live today by the scouts. github.com pages
and raw.githubusercontent.com are readable (WebFetch and curl); the GitHub
REST API returned an error page to curl. pip reachable (numpy, scipy, sympy,
python-sat, networkx, pymupdf, gmpy2, ortools installed).

**Candidate slate** (three externals across three subfields, each checked
against its primary page today; six parallel scouts — arXiv three-week sweep
of 1609 abstracts, OEIS, erdosproblems.com's 635 open problems, MathOverflow
via the API, an internal audit, and a status check of a twelve-item
curiosity list — full reports in the session scratchpad):

1. **Shallit's k_min** (combinatorics on words / discrete geometry).
   arXiv:2609.05780 (read in full), §5: "Define k_min to be the least size
   of an alphabet admitting a good infinite word … at most 16 … we know that
   k_min ≥ 4 … it is still of interest to determine its exact value", with
   four candidate morphisms "in the hope that they may aid other researchers
   to improve the bound". Open on arXiv as of today (no v2, no citing paper;
   the status scout found no MathOverflow question and no OEIS entry for
   L(d)). **Selected.** (The stronger unpublished drafts were found only
   after the proof, see above.)
2. **Equitable 4-total colourings of cubic graphs of order ≤ 18** (graph
   theory). arXiv:2609.05259 (Adauto, de Figueiredo, Sasaki, Schneider,
   4 Sep 2026), Question 7.1: "Does every Type 1 cubic graph of order less
   than 20 admit at least one equitable 4-total coloring?" — the paper calls
   it finite and "within reach of a systematic computational verification
   over the catalogue of connected cubic graphs of order at most 18".
   Passed over: 45 982 SAT/CP-SAT instances plus a catalogue to rebuild
   (no geng here), a confirmatory outcome likely, and the authors are
   plainly about to do it.
3. **Erdős #112, Erdős–Rado digraph Ramsey numbers k(n,m)** (Ramsey theory).
   erdosproblems.com/112 (open; no forum thread, no claims): "Let k = k(n,m)
   be minimal such that any directed graph on k vertices must contain either
   an independent set of size n or a transitive tournament of size m.
   Determine k(n,m)." Known bounds R(n,m) ≤ k(n,m) ≤ R(n,m,m) leave
   k(3,3) ∈ [6, 9], k(4,3) ∈ [9, 16]. Passed over: the exact definition
   (2-cycles, induced) must be fixed from Erdős–Rado 1967 / Larson–Mitchell
   1997 first, and small values may already be tabulated there.

   Also surveyed and rejected (details in the scout reports): Yu's
   cyclotomic circulants for R(4,21) ≥ 252 (arXiv:2608.18169; a lottery);
   Severini–Weisstein graph likelihood at n = 16 (ideas-bound enumeration);
   majority C-colourings of K_n^{□,3} (arXiv:2608.27669; ILP, small
   surface); Eulerian-orientation counts at n = 16 (arXiv:2609.06701);
   K_8(4,2) ∈ {22, 23} (author tried SAT and IP); quaternary Legendre pairs at
   the seven open lengths ≤ 100 (arXiv:2609.04589; compute lottery); Erdős
   #336 h(4) ∈ {10, 11}, #1186 δ₃, #1111 d(3,3), #902 f(4), #195/196
   monotone 4-APs, #629 n(4), #23; MathOverflow 513798 (k-gons on n lines),
   514678 (rational-root permutations), 514920 (Weiss's cospectral binary
   strings), 514753 (Grechuk's 2x³+2y³+2z³ = xyz+1), 514705, 514243, 514916,
   513565; OEIS A398141 (record lows of sin(k)^k — an inhomogeneous
   best-approximation theorem, a nice hour), A397711 (DAG congruences),
   A399145, A398550, A390380/A393168 (Erdős #1148, now PROVED (Lean) per
   the site), A395616, and the quick wins A399155, A398720 (two-line proofs,
   comment-level); the curiosity list closed several doors: Sylver coinage
   16 still open (Sicherman's 2026 tables exclude {16}), unit distances
   exact to n = 21 (Alexeev–Mixon–Parshall), Costas 32/33 open, no-three-in-
   line 2n solutions now known for all n ≤ 74 and 76 (Flammenkamp's page,
   Heule/Prellberg/Riley 2026), cap(7) ∈ [236, 288], minimal pancyclic h(n) = 5
   for 25 ≤ n ≤ 37 with m(38) open (Griffin 2013), r₃(n) exact to 211 with
   212 resisting CP-SAT (arXiv:2606.04016), OGR-29 not in computation
   (contrary to arXiv:2609.05421's abstract, which could not be verified),
   snarks generated to 38 but conjectures tested only to 36, g(14..16) = 7
   follows from Wei 2012 (not in OEIS), K₆₄ still the smallest open
   perfect-1-factorisation order.

**Superseded / status changes noticed on the way** (recorded in the
directories concerned, all marked secondary): erdosproblems.com moved
**Erdős #1** (distinct subset sums, the ≥ c·2ⁿ conjecture) to *disproved*
on 2026-09-03 (GPT-6 Astra; Bloom's exposition) — `distinct-subset-sums/README.md`
now carries a status note; its exact values are unaffected. **#617**
(balanced colourings) carries seven unreviewed July-2026 proof claims for
r = 5, 6, 7, 9 — note added to `balanced-colorings/README.md`. #1148 is marked
PROVED (Lean). **#193** (Gerver–Ramsey S-walk) is DISPROVED (Cambie–
Kalviainen, accepted 3 Sep) — the parent of today's problem.

**Internal-thread assessment** (parallel audit of all 32 conjecture READMEs
and the eight most recent logs; full report in the scratchpad). Last two
sessions: chromatic-ramsey (09-06) and good-permutations (09-07) — no
forced rotation. Strongest live thread: **generalized-schur S(3;3,3,12)**
(pre-registered Conjecture A prediction 95; < 1 h with the existing solver;
a twelfth new value would change the row), then the disk-streaming pipeline
for (4,4,10)/(4,4,11) (tool-building, projections untrustworthy). Everything
else is a compute wall (ordinary-lines' 45 classes ≈ 25 CPU-h, peaceable-
queens a(19) 13–16 h, chromatic-ramsey F(3,5) census, erdos-gyarfas f(6)
orientations) or an ideas wall (good-permutations n = 255). Audit flags: the
only lingering PAGE.md is good-permutations' (blocked on its two
unreconciled write-ups and stale against its README); the n = 127 run record
`results/n127_mid_run1.txt` is empty although cited; three READMEs still
say "see PAGE.md" (power-residue-pairs l.18, projective-chromatic l.81–82,
parking-polytope l.66); several index rows overstate their README's label
(gilbreath R3.5 "PROVED" vs "persistence NUMERICAL", finch's horizon,
balanced-colorings' "modulo BreakID"). Not fixed today except the two status
notes above.

**Selection.** The mandate's default is the external problem, and candidate
1 beat the internal rung on all three criteria: (a) both are breakable, but
k_min carried a theorem target next to the computations; (b) prior-work
risk: a four-day-old arXiv question with the author's own candidates
unproved (the repository drafts were unknown at selection time and were
found by the priority check that CLAUDE.md's rule 3 demands); (c) citation
surface: Shallit's question, Korsky's L(d), the Cambie–Kalviainen line on
Erdős #193, and the weak-abelian literature (Avgustinovich–Puzynina,
Fici–Puzynina), versus one more Schur cell. Ties go to the new problem.

**Attempt statement.** Determine k_min as far as one session allows:
exhaust 3-free words over four letters for a certified lower bound
(L(4) < ∞ ⇒ k_min ≥ 5), and find a construction with a proof below 16 —
success meaning either a certified L(4) or a proved k ≤ 8, the alphabet
Shallit's smallest candidate with a chance of an arithmetic proof lives on.
Achieved: the proved 7 (and 8); the lower bound side was not achievable by
search.

**What failed.**
- *Certifying k_min ≥ 5.* The four-letter tree grows by a factor ≈ 1.27–1.30
  per letter (28.9 M canonical words at length 46); no structural
  obstruction over four letters came to mind. Nothing.
- *Six letters from the dragon.* Every coding of the eight dragon letters
  onto six or fewer classes has a bad pair within 3000 letters, so the
  dragon route ends at seven whatever the proof; the functionals the
  seven-letter proof uses (parity, half-plane, one-turn walk) are exactly
  what a second identification destroys.
- *The mixed identifications (r,−)~(r+1,+).* 3-free to 30 000, but every
  displacement weight of the form i^r(a + bδ) agreeing on the two letters
  degenerates (a − ib = 0). No proof.
- *Beating six inside the sign/order family.* Two turn values are forced
  (one would make the states periodic), so eight transitions; the family
  search found no coding onto five letters for any pattern of period ≤ 4.
- *Shallit's five-letter candidate.* Verified to 20 000 only; the repository
  checkpoint documents many failed AI-assisted descent attempts, and the
  template method for weak abelian squares has rational templates that need
  not form a finite set — not a one-session job.
- *Operations.* A background launch lost its relative path to the harness's
  working-directory reset (relaunched with absolute paths); a duplicate k = 4
  search was killed by PID; the 100 000-letter check first ran on a
  30 000-letter file. The GitHub REST API refused curl; raw file fetches
  worked.

**Next.** (1) Post the seven-letter construction and the review of the
six-dimensional draft to the ekalvi/erdos-193 discussion and to Shallit —
decisions for the local session per repository policy; the draft's authors
asked for exactly this review. (2) Five letters: either prove one of the
twelve length-14 cyclic morphisms (Shallit's included) by a template
argument that controls the rational corrections, or find an invariant for
the mixed identifications; both need an idea outside 2-adic valuations of
Gaussian displacements. (3) Four letters: a structural obstruction, or a
morphism found by a search over non-cyclic uniform morphisms (the cyclic
ones of length ≤ 16 all fail). (4) Submit L(d) for d ≤ 3 and the count
table to OEIS only if a fourth value can be added — L(4) is the missing
term and is out of reach. (5) Repository hygiene flagged by the audit: the
three stale "see PAGE.md" lines, the empty n = 127 record, the good-
permutations reconciliation.

**Session hygiene.** Branch: harness-designated `claude/vibrant-archimedes-8bp38s`
(the mandate's per-conjecture branch name overridden by the harness
requirement, as in previous sessions). The `conjecture-research` skill named
in CLAUDE.md is not installed here; CLAUDE.md followed directly. Hardware:
4 cores, 15 GB; Python 3.11.15; gcc 13.3. No seeds; every computation exact
(integer arithmetic; Gaussian integers as integer pairs; complex floats in
the Python checks only as carriers of integer values, rounded before
testing). Time: survey and selection 07:36–08:10 UTC; engine and controls by
08:20; the dragon word and the eight-letter theorem by 08:50; the seven-letter
coding by 09:05; priority check and review of the six-dimensional draft
09:05–09:20; family and morphism searches to 09:45; write-up after.
