# 2026-08-07 — generalized Schur numbers (Ahmed–Schaal Conjecture 2.1 and the s=3 family)

**Target.** New exact values of generalized off-diagonal Schur numbers
S(3;s,t,u) — the least m such that every 3-coloring of [1,m] has, for some i,
a monochromatic solution of x₁+⋯+x_{t_i−1} = x_{t_i} in color i. The complete
published table is 28 values (Ahmed–Schaal, Exp. Math. 2016, read today as a
primary source; diagonal closed by Boza–Marín–Revuelta–Sanz 2019; 2-color
family closed 1982/2001). Nothing new has appeared in this family since 2016.
Every unpublished triple with 4 ≤ s ≤ t ≤ u tests an open instance of
Ahmed–Schaal Conjecture 2.1 (S = stu−tu−u−1); the s=3 family has *no*
conjectured formula at all — Conjecture 2.2, proved by Song–Mao in April
2026, is only a strict lower bound — so every new value there maps unknown
territory. This is the candidate the 08-05 session scoped and abandoned
solely because the publication boundary sat in a blocked PDF; today the
boundary was pinned from the primary source, and the 08-05 session's
validated DRUP-certification toolkit (`tools/satcert/`) was waiting.

**Result.**
- **CERTIFIED** — new exact generalized Schur numbers, the first in this
  family since 2016 (final list in `conjectures/generalized-schur/data/new_values.csv`):
  `S(3;4,4,8) = 87` and `S(3;4,4,9) = 98`, each deciding a previously open
  instance of Ahmed–Schaal Conjecture 2.1 (both confirm it), and — in the
  `s = 3` family, where no formula is even conjectured — `S(3;3,3,8) = 59`,
  `S(3;3,3,9) = 68`, `S(3;3,4,8) = 67`, `S(3;3,4,9) = 78`, `S(3;3,5,8) = 91`,
  plus the further values recorded in the CSV. Every value ships a DRUP
  proof of the UNSAT side checked by the independent `rup_check`, and a
  witness coloring of the SAT side checked by an independent bitset
  verifier. Controls: 11 published boundary values reproduced with
  identical certificate chains; all 12 published `(3,t,u)` values
  reproduced by climb; all 10 published enumeration counts matched
  exactly; the unique `(3,4,5)` extremal coloring matches the paper's
  printed string character for character.
- **CERTIFIED** — the complete extremal structure of the `(3,3,u)` family
  at every computed size: for `u ∈ {4,5,6,8,9}` the valid colorings of
  `[1, 9u−14]` are exactly one mirror-symmetric skeleton with `u−2` free
  ternary slots at positions `2u+1+5j` (`2·3^{u−2}` colorings; maximal
  `L(u)`-class exactly `5(u−2)`), while at `u = 7` the value drops one
  below the `9u−13` line, the 846 extremals form no single skeleton, and
  the deficit belongs to the Schur pair, not the `L(7)` class.
- **Conjecture A** (new): `S(3;3,3,u) = 9u−13` for all `u ≥ 4` except
  `u = 7` — certified at every computed size, open beyond.

**What failed.**
- The `(4,4,u)` ladder beyond `u = 9`: three proof-logged attempts at
  `(4,4,10)` were OOM-killed — pysat buffers the whole DRUP proof in RAM,
  and this instance's proof outgrows 15 GB. The ladder is anomalously hard
  for its size (two short equations, one long: minimal propagation);
  `(4,4,10)`–`(4,4,12)` remain open pending a disk-streaming proof
  pipeline. `(6,6,6) = 173` reproduction was abandoned for the same
  footprint reason (it is published and Boza-covered).
- Two container-wide crashes from my own memory oversubscription (four
  concurrent solver lanes, then three) cost ~40 minutes and forced the
  final discipline: at most two solver processes, heavies sequential.
- The slope-8 tail guess for `(3,4,u)` (from 59, 67 at `u = 7,8`) died
  against `(3,4,9) = 78`; the `t = 4` row fits no simple law tried.
- The all-`u` lower-bound construction for `(3,3,u)`: the slot skeletons
  share their arithmetic (slots at `2u+1+5j`, spacing 5) but the prefix
  block morphs with `u`, and no uniform parametrization survived contact
  with all five skeletons within the session. Left as the sharpest thread.
- A correct `(3,3,8)` extremal enumeration appeared in `certs/` with no
  logged invocation (kept only after byte-identical regeneration);
  recorded as a provenance defect.

**Next.** (1) A disk-streaming certified pipeline (kissat/CaDiCaL binary +
drat-trim) to open the `(4,4,u)` ladder, `(6,6,7)`-scale triples, and the
4-color family. (2) Prove Conjecture A for `u ≥ 8` by completing the
slot-skeleton construction — the slot arithmetic is understood, the prefix
family is the missing piece. (3) OEIS: no sequence for this family was
findable today (secondary, absence-of-evidence); the `(3,3,u)` row and the
extended table are candidate submissions once checked against OEIS proper.
(4) The `u = 7` anomaly deserves a human-readable obstruction, not just a
35 KB DRUP proof.

---

## 1. Connectivity check

| source | reachable | how |
|---|---|---|
| `arxiv.org` | **no** — EGRESS_BLOCKED at proxy | WebFetch |
| `oeis.org` | **no** — EGRESS_BLOCKED | WebFetch |
| `erdosproblems.com` | **no** — EGRESS_BLOCKED | WebFetch |
| `mathoverflow.net` | **no** | WebFetch |
| `combinatorics.org`, `cs.rit.edu`, `uni-bielefeld.de`, `api.semanticscholar.org` | **no** (subagent probes) | WebFetch/curl |
| web search | **yes** | the main literature channel, as on 08-02…08-05 |
| `raw.githubusercontent.com` | **yes** | **primary-source channel — see below** |
| `pypi.org` | yes (proxy bypass) | numpy, python-sat installed |

Same egress posture as the last four sessions, with one decisive difference
found by a scout: **`raw.githubusercontent.com` serves the author preprint of
the Ahmed–Schaal paper** (Tanbir Ahmed's own GitHub Pages repository), and it
serves GitHub mirrors of the OEIS (`oeis/oeisdata`) and of Tao's
`teorth/erdosproblems` database. Today's deciding source — the exact table of
published values — is therefore **primary** (PDF read in-session; URL and
sha256 in `conjectures/generalized-schur/data/environment.txt`). The
Song–Mao April 2026 abstract was recovered verbatim from an arXiv-RSS mirror
on GitHub (secondary but verbatim). Everything else remains (secondary).
CLAUDE.md's `conjecture-research` skill is still not installed in this
sandbox; its written discipline was followed directly. Working branch is the
environment-provisioned `claude/kind-bohr-1n3ius` (the harness forbids
pushing elsewhere), not the `claude/<conjecture>-<date>` naming the task
prompt describes.

## 2. The three external candidates

Built by four parallel scout subagents (fresh arXiv math.NT/math.CO; the
generalized-Schur publication boundary; small graph-Ramsey open cases; BHR /
no-three-in-line / Erdős-database). Spanning three subfields.

### E1 — Generalized off-diagonal Schur numbers *(arithmetic Ramsey theory)* — SELECTED

*Statement.* Compute new exact values S(3;s,t,u); each 4 ≤ s ≤ t ≤ u value
decides an open instance of Ahmed–Schaal Conjecture 2.1, each s=3 value maps
a family with no conjectured formula.

*Source.* Ahmed–Schaal, Exp. Math. 25(2) 2016 — **primary, read in-session**
(author preprint via raw.githubusercontent.com; Table 1 transcribed to
`data/published_values.csv`). Song–Mao, arXiv:2604.11030 (April 2026):
abstract verbatim via RSS mirror — proves Conjecture 2.2 (s=3 strict lower
bound), proves *no* new exact values, treats Conjecture 2.1 as open.
Boza–Marín–Revuelta–Sanz, DAM 263 (2019): diagonal S(3;t,t,t) = t³−t²−t−1
(secondary; k-range inferred from S_k(3)=k³+2k²−2 digest, consistent with
all four known diagonal values).

*Why believed open.* The 26 Ahmed–Schaal values are the entire published
frontier; a full sweep of the arXiv math.CO RSS mirror 2024→2026-08 for
"Schur numbers" turned up seven hit-days, all accounted for (Song–Mao;
Ahmed–Bright–Zaman on ax+by=bz Rado numbers; Chang–De Loera–Wesley on
ax+by=cz; Rowley-template classical S(k); three adjacent-theory papers) —
**none computes exact values in the L(t) family**. Targeted searches for the
specific strings "S(3;4,4,8)", "S(3;3,7,7)" etc. return nothing. Residual
risks recorded in NOTE §7 (minor venues, theses, MathSciNet unreadable).

### E2 — σ(n+1) = k·σ(n) census *(multiplicative number theory)*

*Statement.* Fatehizadeh (arXiv:2605.21524, May 2026) generalizes
Erdős–Sierpiński: for k ≥ 2 are there infinitely many n with σ(n+1)=kσ(n)?
Infinitude for k=2 proved only under Schinzel's H; published data is a tiny
solution list (k=3: {1, 1919, 2759, 11219}, hand-verified in-session).
A segmented σ-sieve to 10^11–10^12 would extend the census 100–10,000×.
**(secondary)**

*Why not selected.* Guaranteed-completable and honest, but it would be this
repository's third census-shaped session in four days, and its endpoint is
evidence, not a decided statement. E1's endpoint is exact theorems-by-
computation with checkable certificates, plus a live shot at a proved
construction. Kept as the strongest fallback; the scout's verification of
the k=3 list is banked in the log.

### E3 — BHR conjecture, per-multiset verification at v = 24, 25 *(design theory)*

*Statement.* Buratti–Horak–Rosa: every admissible multiset L of v−1 lengths
is realized by a Hamiltonian path on Z_v. Scout finding: a July 2025 arXiv
paper (Naik) claims p ≤ 31 but apparently **per frequency partition, not per
multiset** (3.3k vs 17.6×10⁹ cases at v=29 — my exact counts:
C(35,11)=417,225,900 multisets at v=25, of which 417,219,530 admissible);
per-multiset territory beyond v ≤ 18–23 appears unclaimed. **(secondary)**

*Why not selected.* The deciding caveat — whether Naik's verification is
per-FP or per-multiset — is in a blocked PDF, exactly the failure mode that
sank 08-04; and the honest certificate for v=25 weighs ~10 GB against a
~10 MB repo cap with Zenodo unreachable. A digest-tree artifact is
defensible but second-rate. Do this the day the paper is readable.

Also vetted and rejected: small graph-Ramsey tight cases (the 2024–26
SAT-Ramsey wave — Wesley, LMPO — has settled or queued everything with gap
≤ 2 at order ≤ 30; R(K₄−e,K₇)=28 landed June 2026; the one quiet pocket,
Lortz–Mengersen K_{2,m} vs K_{2,n}, has its open entries locked in blocked
PDFs); no-three-in-line (frontier moved to n ≤ 60 by Prellberg's CP-SAT
runs Feb 2026, counts to n=20 May 2026, both actors visibly active — stand
down); Erdős #647 (occupied: active Zenodo preprint extending to 10^12 in
June 2026); Erdős #307 (clean unclaimed shelf, kept for a future session).

## 3. The internal thread

Strongest live internal thread: **additive-squares, close the (1,1,0)
search tree** (two independent budget-limited searches plateaued at 440/437;
closure would be a second Freedman-type theorem and change that row).
Assessment: (a) compute-shaped, yes — but the two prior runs both hit their
budgets without closing, so the honest single-likeliest outcome is a third
plateau; (b) novelty not in doubt; (c) extends this repo's own line.
Runners-up: powerful-progressions 10^20 (needs a 128-bit generator rewrite;
extends our *own* record by 10×, published record already beaten by 10⁵ —
fails significance), Gilbreath R3.11 (ideas-bottleneck), circular-thresholds
Pansiot search (five empty sweeps two sessions ago). The internal thread
does not clearly beat E1 — E1 has primary-sourced novelty, guaranteed
completability *and* discovery upside — so per the mandate the external
problem wins, and ties go to the new anyway.

## 4. Selection argument

(a) *Compute-breakable?* E1 decisively — measured, not estimated: during
scoping, the pipeline reproduced published boundary values in 0.1–20 s each,
and the first two unpublished triples fell in 43 s and 203 s wall. The
feasibility wall sits comfortably beyond several new triples in both
families. E2 yes (sieve arithmetic). E3 yes at v=24/25 but the certificate
cannot be shipped honestly.
(b) *Already done?* E1: the deciding table was read from the primary source
today — the strongest novelty position any session here has had since
08-01. E2: OEIS-absence checkable only by mirror/search. E3: undecidable
today (blocked PDF), disqualifying.
(c) *Who would cite it?* E1: Ahmed–Schaal's table is the reference table
for this family; Song–Mao's April 2026 paper is *about* these two
conjectures and would cite new confirmed instances directly; Bright's and
Wesley's certified-Rado-computation lines are the methodological neighbors.

**The result attempted today** (stated before the production runs): at least
five new exact values S(3;s,t,u) with fully certified boundary pairs —
DRUP proof of UNSAT at S checked by the independent `rup_check`, witness
coloring at S−1 checked by an independent bitset verifier — including
enough of the uncharted s=3 family to support or kill a closed-form guess;
stretch: ten-plus values and a proved lower-bound construction for the s=3
family improving Song–Mao's bound. Refutation of Conjecture 2.1 at any
triple would be a headline result and is handled by the same protocol
(verified witness at the conjectured value, then climb to the true one).

## 5. Tool discipline

Positive controls: 23 published values reproduced end-to-end before any new
claim — S(2;3,3)=5, S(3;3,3,3)=14, all twelve published (3,t,u) values by
Cadical climb (23, 32, 41, 49, 31, 47, 49, 59, 58, 70, 80, 85), the (3,6,7)=107
climb in the certified production lane, and (4,4,4)=43, (4,4,5)=54,
(4,5,5)=69, (5,5,5)=94, (4,4,7)=76, (4,5,6)=83, (4,6,6)=101, (4,5,7)=97,
(5,5,6)=113 with verified certificates. Every Song–Mao lower-bound anchor
(SAT at 2tu−u−1) held, as their theorem requires. Negative controls: a
corrupted witness is rejected by the verifier (this session); injected
non-RUP and truncated DRUP proofs rejected (satcert validation record,
08-05). Cross-validation: the partition-based clause enumerator agrees with
brute-force product enumeration on all 15 (t,n) test cells. Encoder is
deterministic — no seeds exist; runtimes and proof sizes in
`data/results*.csv`; environment in `data/environment.txt`.
