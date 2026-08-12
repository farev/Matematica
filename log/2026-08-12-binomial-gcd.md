# 2026-08-12 — binomial-gcd (Erdős #699: common prime factors of binomial coefficients)

**Target.** Erdős problem #699 (Erdős–Szekeres 1978): for
1 ≤ i < j ≤ ⌊n/2⌋ there is a prime p ≥ i dividing both C(n,i) and C(n,j);
strengthening: p > i outside a finite exceptional set. Statement pinned
2026-08-12 from the Lean formalization (`google-deepmind/formal-conjectures`,
both statements `research open`) and status `falsifiable` (open) from
`teorth/erdosproblems`. Selected from a three-candidate external slate
(below) on measured feasibility: the bottleneck is exact digit conditions
(Kummer) over the prime factors of short windows n, n−1, …, n−i+1 — CPU
plus lemmas, not ideas. The specific result attempted, stated after the
scoop-guard surfaced prior art (a January 2026 public scan to 10^7): (1)
independently confirm that scan and extend the verified range by ≥ 2 orders
of magnitude; (2) prove structure theorems for the two exceptional families
(2^k at i=2, 3^m+1 at i=3) and push the family censuses beyond the scan's
k ≤ 27, m ≤ 17 by the exact criterion; (3) an honest numerical verdict on
the strengthening's finite-exceptional-set form.

**Result.**
- **CERTIFIED** — **two new exceptional ("tight") triples**, the first
  since the January census. (2^41, 2, 285920731515):
  gcd(C(2^41,2), C(2^41,·)) is a power of 2 — found by the family
  criterion sweep, n ≈ 2.2·10^12, ~200,000× beyond the previous record.
  And **(2^67, 2, 23206563898901803639)** — n ≈ 1.5·10^20, found by
  **prediction**: the exact-density model (below) flagged k = 67 (Cole's
  1903 factorization 2^67−1 = 193707721·761838257287) as the strongest
  undecided exponent (E = 1.85, computed before the enumeration), and the
  enumeration produced exactly one tight j. Both triples verified by a
  standalone checker (factorizations re-proved by multiplication +
  primality; Kummer by carry-propagation, no shared code) and both j's
  unique by dual-codebase scans (9.07·10^7 and 1.94·10^8 candidates).
  `conjectures/binomial-gcd/certs/`.
- **PROVED** — Theorem 7: at n = 2^k, (n,2,j) is tight iff j ≤ 2^{k−1} is
  base-q dominated by n for every prime q | 2^k−1 (and counterexamples are
  impossible there); if 2^k−1 is a Mersenne prime there is **no** tight
  triple — explaining why the family is k ∈ {4, 9, 11, 41, 67} (all with
  2^k−1 semiprime, OEIS A085724) and not the Mersenne exponents
  {2,3,5,7,13,…}. Theorem 8: for m = 2 or m odd with (3^m+1)/4 prime and
  (3^m−1)/2 a prime power, (3^m+1, 3, (3^m+1)/2) is tight — the hypotheses
  hold exactly for m ∈ {2,3,5,7,13}, i.e. every known i=3 member. Plus the
  reduction machinery (Props 0–6: E–S gcd>1 theorem with proof, window
  criterion, danger zone i ≤ n − prevprime(n), exact tightness criterion).
- **CERTIFIED** — independent confirmation of the January 2026 scan:
  #699 holds for 4 ≤ n ≤ 10^7 with exactly the 9 known tight pairs
  (different algorithm: danger-zone reduction + CRT candidate enumeration;
  30 s on 4 cores vs their ~120 core-hours — a ~5000× algorithmic speedup,
  which is what makes everything else reachable). Family censuses by the
  exact criterion: n = 2^k complete at **every danger level for k ≤ 63**
  (the 17 levels past the Python enumeration cap were closed CLEAN by a
  compiled u128 enumerator, up to 4.4·10^9 candidates each; 2^64's two
  levels remain undecided at 5.15·10^10); i=2 decided at every semiprime
  exponent through k = 109 **except k = 101** (min dominated set
  7.4·10^12); n = 3^m+1 complete at i ≥ 2 for m ≤ 40, plus m = 41, 43
  decided clean (m = 43 is the next sufficiency-theorem candidate and
  fails the digit criterion); nine levels at m ∈ {42,...,48} undecided
  (min sizes ≥ 10^11, measured). **Final sweep bound: the deep run
  (target 4·10^9) was stopped at the 15:30 checkpoint after its
  per-segment cost collapsed at n ≈ 1.3·10^9 (smooth-window fallback
  scales linearly in n); the certified contiguous prefix is
  4 ≤ n ≤ 1,371,537,407 (654 complete 2^21-segments) — a 137× extension
  of the recorded bound, with exactly the 9 known tight triples and no
  counterexample.** Deep-sample audit over the full certified range: 258
  random n re-decided independently, 0 failures.
- **NUMERICAL** — the calibrated density model (exact dominated-set
  counts by digit DP, no sampling): E_k = Θ(1) at exactly the five
  members (2.67, 1.0, 1.97, 0.55, 1.85), E = 0.2–0.7 at the decided-clean
  balanced semiprimes (23, 37, 59, 103, 109 — Poisson-consistent misses),
  E ≤ 10^−5 everywhere else. Along balanced semiprimes E_k does not decay,
  and with semiprime density ≍ (log k)/k the heuristic ΣE_k **diverges**:
  the model predicts infinitely many i=2 tight triples — against the
  finite-exceptional-set form of the strengthening as formalized in
  Lean — with five members below 2^67 being the expected order. The i=3
  mechanism needs simultaneous near-primality of (3^m±1)/{2,4}
  (probability ≍ 1/m² per m): convergent, finite family expected
  (observed cutoff m = 13 through m ≤ 48). The k = 67 prediction-then-
  discovery is the model's strongest validation; its independence
  assumption remains untested beyond the census itself.

**What failed.**
- The selection-time framing ("first recorded verification bound") was
  dead on arrival: the 08-09 session's banked note "no recorded bound
  anywhere" was stale against a 2026-01-03 forum post + public Rust repo
  that only a targeted scout query surfaced. Scoop-guarding must be re-run
  the same day even for recently vetted problems, and must include forums.
- v1 of the deep sweep was 6× too slow, and the first optimization
  attacked the wrong bottleneck (list rebuilds); the real cost was
  candidate volume at i = 1 — a level that is *provably vacuous* (Prop 0).
  The fix was the theorem, not the code. Lesson re-learned: profile
  against the mathematics before the datastructures.
- First 4·10^9 launch projected 15 h (a Python job pinning one of four
  cores + misread early-segment timing); killed, remeasured, relaunched.
  Segment-completion markers added so an interrupted run still certifies
  a prefix.
- The family checker died twice on dominated-set blowups before getting
  streaming enumeration + catch-and-mark-UNKNOWN semantics. Its "min
  size" figures for UNKNOWN levels are capped partial products (lower
  bounds), which briefly misled the closure planning: the true minima at
  the 3^m levels are ≥ 10^11, not ~10^8.
- **The u128 bug that mattered**: the first compiled enumerator stored
  primes as u64; the k ≥ 83 semiprime jobs (factors up to 1.4·10^25)
  silently truncated and spewed a 355 MB flood of false "EXC" rows.
  Caught by inspection before any claim was written (j-values in
  arithmetic progressions = carries misfiring), fixed to full u128,
  a JOBFAIL canary added (> 10^4 hits aborts the job), and the earlier
  job batch audited clean (no prime ≥ 2^64 — its results stood). Every
  claimed triple was then re-derived in the fixed engine AND by the
  no-shared-code verifier. Lesson: a tool that can only ever emit a
  handful of hits must enforce that expectation itself.
- Process hygiene cost real time: a `; cat` suffix masked the exit code
  of the first closure batch (it died silently at 2^64's 5·10^10-node
  level and looked "completed"); and a pkill pattern matched the wrapper
  but not the binary, leaving a zombie burning a core against the
  4·10^9 sweep for half an hour. Both now standing lessons: exit codes
  unmasked, kills verified by ps afterwards.
- Two "UNKNOWN at i=1" rows in the 3^m log are vacuous (Prop 0 settles
  i=1) — cosmetic checker defect, documented rather than hand-edited.

**Next.** (1) Decide (2^101, 2) — the model's strongest open prediction
(E = 0.78; min dominated set 7.4·10^12 wants a meet-in-the-middle
intersection algorithm or ~a day of CPU); then 2^131 (needs >128-bit) and
A085724 beyond. (2) The sharpest open thread: make the divergence
heuristic a conditional theorem (under standard heuristics for Mersenne
factorizations, the expected number of i=2 tight triples diverges) — or
find the flaw in its independence assumption; either outcome bears
directly on the formalized strengthening. (3) Report the 2^41 and 2^67
triples to the erdosproblems #699 forum thread and the erdos_699_rust
repository after human check (needs a machine with forum access). (4) A
structural proof that i=2 tightness forces n = 2^k would turn the census
pattern into a theorem. (5) Mop-up: 2^64's two levels (5·10^10
candidates), the nine 3^m levels at m ∈ {42..48} (≥ 10^11 each), and
i ≥ 3 at 2^k, k > 64.

---

## Connectivity check (11:42–11:50 UTC)

| source | reachable | note |
|---|---|---|
| arxiv.org | **no** — EGRESS_BLOCKED | also export/ar5iv/alphaxiv |
| oeis.org | **no** — EGRESS_BLOCKED | mirror `oeis/oeisdata` on raw.githubusercontent.com works (4-char shard paths) |
| erdosproblems.com | **no** — EGRESS_BLOCKED | content reachable via search snippets; `teorth/erdosproblems` raw is the machine-readable mirror |
| mathoverflow.net | **no** | |
| web search | **yes** | main literature channel; snippets carry page text |
| raw.githubusercontent.com | **yes** | primary-source channel all session |
| renyi.hu (Erdős archive) | **no** (403) | regression vs the 08-09 log, which reported it reachable — the E–S 1978 paper stays (secondary) |
| pypi.org | yes | numpy/sympy installed |

`conjecture-research` skill: still not installed (ListSkills: no match);
its written discipline followed directly. Branch: environment-provisioned
`claude/kind-bohr-g5y8j5` (harness forbids other names), tip = origin/main
(a6a0805) at start. Hardware: 4 cores, 15 GB RAM, Python 3.11.15,
gcc 13.3.0.

## The three external candidates

Slate built by three parallel scout subagents (vetting #699;
graph-theory/OEIS hunter; words/geometry hunter + FMMS re-vet), all
sources fetched or snippet-verified 2026-08-12. Spans number theory,
graph theory/chess domination, combinatorics on words.

### E1 — Erdős #699, binomial gcd (number theory) — SELECTED

Statement above. *Openness:* Lean formalization `research open` (primary,
fetched today); `teorth/erdosproblems` status `falsifiable`, last update
2025-08-31 (primary mirror); zero mentions in the AI-contributions wiki
(frozen Jun 30, 2026); no 2025–2026 arXiv activity on this exact problem
(adjacent binomial problems 684/400 are active, this one untouched).
*Prior computational work found by the scoop-guard* (the decisive fact of
the day): `conglu1997/erdos_699_rust` + erdosproblems forum thread —
verified n ≤ 10^7 (run log committed 2026-01-03, 9,999,997 rows,
`weak_counterexample:false`), 9 tight pairs with (n,i,j) in the committed
`scan.jsonl`, family scans 2^k (k ≤ 27), 3^m+1 (m ≤ 17). The 1978 E–S
paper itself unreachable (renyi.hu regressed to 403) — its exception
remarks are (secondary) via erdosproblems.com snippets. *Feasibility:*
measured, not estimated — by selection time the brute force had reproduced
the known census to n = 3000 and the C engine had confirmed 10^7 in 30 s.
*Cites:* erdosproblems.com/699 (records bounds), the Lean formal-conjectures
repo (strengthening formalized open), Cong Lu's repo, Guy UPINT B31
(secondary).

### E2 — Knight domination number a(22), OEIS A006075 (graph theory)

γ(knight graph on n×n): certified terms end at a(21) = 68 (Huchala, Jun
2021); Rubin's 2002 heuristic covers give a(22) ≤ 75 … a(26) ≤ 102
(comments in A006075, fetched from the OEIS mirror today; Fisher's and
Rubin's Ars Combin. 2003 papers (secondary), PDFs unreachable). *Open:*
last term 2021; no 2023–2026 knight-optimality work found; the active
certified-SAT chess-domination line (Rostami–Bright arXiv:2508.11945) is
queens-only. *Feasibility:* SAT decision at 74 knights, 484 vars, short
clauses + cardinality; DRAT-certifiable; **but the UNSAT depth is
unmeasured** — could be minutes or a cluster-month; fallback only a
certified lower bound. *Cites:* OEIS A006075/A006076, the Rostami–Bright
line. Rejected on unmeasured (a): a one-day session cannot bound the
solver risk, against an alternative with measured feasibility.

### E3 — Fici–Saarela minimum abelian squares / FMMS 2026 (combinatorics on words)

Every binary word of length n contains ≥ ⌊n/4⌋ distinct abelian-square
factors (Fici–Saarela, Dagstuhl 2014 (secondary)); extended with
per-Parikh-vector minima M(x,n) and conjectured extremal words by
Fazekas–Mammoliti–Mercaş–Simpson, arXiv:2604.23188 (Apr 2026) — PDF
unreachable by every channel again today (their base cases "n ≤ 10 easily
checked" and Theorems 3/12 recovered from snippets, all (secondary)).
*Open:* no v2, no citing paper, latest indexed statements call it open.
*Feasibility:* branch-and-bound on the prefix tree with monotone counts;
n ≥ 30 exact plausible in a day; OEIS gap confirmed (no matching sequence
found). *Cites:* FMMS authors, Fici–Saarela–Puzynina. Not selected: their
own verification tables remain invisible (the same blocked-PDF novelty
handicap that deferred this candidate on 08-09), so every census value
risks silent overlap; the novelty-safe parts (testing *their* conjectured
extremal words) depend on reconstructing those words from snippets.
Strong future candidate from a machine that can read the PDF. The
words/geometry scout also re-confirmed: Mäkelä's ternary abelian-square
conjecture open (period-2..5 gap; Rao/Rosenfeld frontier, all (secondary));
lonely-runner n=8 now *closed* (M. Rosenfeld, arXiv:2509.14111) — both
banked as intel.

### Also killed by scouts today (banked)

Gold-partition/1/3–2/3 conjecture: verified through 14 elements by
arXiv:2607.23926 (Jul 2026) — n=15 is ~4·10^13 posets, lane hot and owned.
3-decomposition conjecture: SAT-modulo-symmetries specialists own it (CP
2025, ≤ 28 vertices). Peaceable queens A250000: active contested lane.
Queens a(26): Rostami–Bright own the pipeline. Burning-number ≤ 28-vertex
exhaustive verification: viable and unclaimed (kept as a future
candidate).

## The internal thread

Strongest live internal thread: reciprocal-rado k = 9 — the 08-08 session
left f₂(9) ∈ {245, 246} on record (n = 243 decide killed in flight), and
k = 10 tests Conjecture B fresh; would change that row. Runner-up:
generalized-schur (4,4,u) with the rebuilt disk-streaming glucose; SDS
(32,20,4) needs ~2 CPU-weeks (out of range); Erdős–Gyárfás n = 19 via
Carr's constraints rests on unverified (secondary) structure. Not selected:
the mandate's default is external, the tie-break goes to the new, and E1's
measured feasibility plus verified-today openness beat the internal
option's marginal-value case. No two-consecutive-session constraint binds
(08-08 rado, 08-09 SDS).

## Selection argument

(a) *Compute-breakable?* E1: yes — measured at three scales before
selection was final (brute census n ≤ 3000 in 5 s; engine 10^7 in 30 s;
family criterion validated on all 9 known members). E2: unmeasured SAT
depth — the one disqualifying unknown. E3: yes for the census, but see
(b). Internal: yes (measured 08-08).
(b) *Already done?* E1: prior art FOUND and pinned (repo + forum, fetched
today) — the remaining targets (independent confirmation, range extension,
family structure, finiteness analysis) verified new against it. E3: prior
tables exist but are INVISIBLE (blocked PDF) — unbounded silent-overlap
risk. Known-prior beats unknown-prior for honest claiming.
(c) *Who cites?* E1: erdosproblems.com #699 + forum (records verification
bounds), formal-conjectures (strengthening formalized open), Cong Lu's
repo, Guy B31 lineage. E2: OEIS + the certified chess-domination line.
E3: FMMS/Fici–Saarela.
E1 wins (a) decisively and (b) on checked novelty; ties would break to
new-to-repo anyway. Mid-session pivot pre-committed: if by 15:30 UTC the
deep sweep was failing AND the family theorems had gaps, fall back to E3's
novelty-safe core. Not fired — the 2^41 discovery landed at 12:33.

## Tool discipline

Controls before any claim: sieve π(x) cross-checks; Kummer implementation
vs direct big-int divisibility (all (n,k,p), n ≤ 120: 0 mismatches);
dual-implementation census concordance (C engine vs Python brute,
n ≤ 3000, exact); third-codebase concordance (vs the 2026 Rust scan at
10^7, exact); family-checker positive controls (all 9 known members,
incl. both levels at n=28) and negative controls (2^6, 3^17+1); the i=1
theorem-assertion battery (Prop 0) clean over 10^7; the new triple
verified by a no-shared-code checker incl. an independent uniqueness scan;
deep-sample audit (random n re-decided in Python vs the C census). No
randomness in any result-bearing path; runtimes and core counts in
WRITEUP; artifacts and their producers tabulated in the conjecture README.
