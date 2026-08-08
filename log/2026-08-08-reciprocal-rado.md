# 2026-08-08 — reciprocal Rado numbers (Gaiser–Ramezanpour sharpness at odd prime powers)

**Target.** New certified exact values of reciprocal Rado numbers f_r(k) —
the least n such that every r-coloring of {1,…,n} has a monochromatic
solution of 1/x₁ + ⋯ + 1/x_k = 1/x_{k+1} (repeats allowed). A paper one
month old (Gaiser–Ramezanpour, arXiv:2607.04373, July 2026) proves
f₂(3·2^m) = 3k² for m ≥ 1, proves f₂(p^m) ≥ 3k²+1 for odd prime powers
**without a matching upper bound**, leaves k = 2^m covered by neither
theorem, and reports computational values for f₂ and f₃ in a table this
sandbox cannot read. The specific result attempted today, stated before
production: a certified table of f₂(k) across small k — including enough
odd-prime-power cases (k = 3, 5, 7, 9, …) to decide whether the sharp
lower bound 3k²+1 is attained, and the uncovered k = 2^m cases (4, 8) —
plus f₃(k) as far as feasible (f₃(2) ≥ 32 from their 4^r/2 bound), every
value carrying a DRUP proof of UNSAT at f checked by the independent
`rup_check` and a witness coloring at f−1 checked by an independent
verifier. Values inside their unseen computed range are honestly marked
as possible rediscoveries; certificates are new regardless. Stretch: a
proved upper-bound construction at some parameter family, or a refutation
of sharpness at some odd prime power.

**Result.** (session in progress — filled at close)

**What failed.** (filled at close)

**Next.** (filled at close)

---

## 1. Connectivity check

| source | reachable | how |
|---|---|---|
| `arxiv.org` | **no** — EGRESS_BLOCKED at proxy | WebFetch |
| `oeis.org` | **no** — EGRESS_BLOCKED | WebFetch + curl (CONNECT 403) |
| `erdosproblems.com` | **no** — EGRESS_BLOCKED | WebFetch |
| `mathoverflow.net` | **no** | WebFetch |
| web search | **yes** | main literature channel; snippets include blocked-domain content |
| `raw.githubusercontent.com` | **yes** | primary-source channel (as on 08-07): OEIS mirror `oeis/oeisdata` live (A000040, A003415 fetched); `teorth/erdosproblems` ground-truth YAML (1217 problems) fetched and parsed; `google-deepmind/formal-conjectures` Lean statements fetched (#307, #488, #848, #672, #364) |
| `codeload.github.com` (tarballs) | **no** — 403 | curl |
| `pypi.org` / `files.pythonhosted.org` | yes (proxy bypass) | python-sat 1.9.dev8 installed; its sdist downloaded |

The `conjecture-research` skill named in CLAUDE.md is still not installed
in this sandbox (ListSkills: no match); its written discipline is followed
directly. Working branch is the environment-provisioned
`claude/kind-bohr-6bd70z` (the harness forbids pushing elsewhere), not the
`claude/<conjecture>-<date>` naming the task prompt describes.

Infrastructure unlocked before selection (candidate-agnostic): the
python-sat sdist on PyPI bundles pristine upstream solver sources; built
standalone `glucose-4.2.1` (`glucose_static`) — which **streams DRUP
proofs to disk**, removing the 08-07 15 GB pysat RAM ceiling — and
`cadical-rel-3.0.0` for uncertified exploration. Glucose's `-certified`
output on a toy UNSAT verified by `tools/satcert/rup_check`. The 08-05
satcert calibration battery re-run clean (R₂(x+y=z)=5, R₃(x+y=z)=14,
R₂(x+y=2z,nae)=9, R₃(x−y=z)=14, 0.35 s). Hardware: 4 cores, 15 GB RAM,
Python 3.11.15, gcc 13.3.0.

## 2. The three external candidates

Built from two parallel scout subagents (arithmetic-Ramsey frontier; four
non-SAT directions) plus my own vetting of the Erdős-database
"computational" shelves (statuses decidable/falsifiable/verifiable parsed
from the ground-truth YAML). Slate spans two subfields.

### E1 — Reciprocal Rado numbers *(arithmetic Ramsey theory / unit fractions)* — SELECTED

*Statement.* f_r(k) as above. Gaiser (Discrete Math 347 (2024) #114156,
arXiv:2306.04029) introduced the quantity and proved f₂(k) = O(k³);
Gaiser–Ramezanpour (arXiv:2607.04373, July 2026) prove f₂(3·2^m) = 3k²
(m ≥ 1), f₂(p^m) ≥ 3k²+1 (p odd prime, m ≥ 1, sharpness **open**),
f_r(2) ≥ 4^r/2, f_r(k) ≥ (2^r−1)k^r, and report unpublished-to-me
computational values.

*Source.* Abstract-level snippets of arXiv:2607.04373 and 2306.04029,
consistent across five searches (secondary — the PDFs are egress-blocked;
no author code or data repository findable). Definition wording ("not
necessarily distinct") seen verbatim in snippets of both papers.

*Why believed open.* The July 2026 paper itself frames odd-prime-power
sharpness as unresolved; no newer work found; no SAT/certification group
active on it; the DeepMind Erdős sweep (arXiv:2601.22401) did not touch
Rado-type exact values (scout check, (secondary)). Residual risk: their
own table may contain small-k exactness — handled by a reproduce-first
protocol and honest overlap marking.

### E2 — Checkerboard no-three-in-line, exact D_mono(n) past n = 16 *(discrete geometry)*

*Statement.* D_mono(n) = max points in one parity class of the n×n grid
with no three collinear. Prellberg (arXiv:2605.09215, May 2026) proves
D_mono(n) ≤ 2n−2, computes exact values for 2 ≤ n ≤ 16 (LP floor = exact
except at four side lengths, gap 1 there), and conjectures a limiting
density at the middle root of 401α³−1744α²+2240α−768.

*Why not selected.* Strong candidate — my own observation that the parity
class is a rotated √2-scaled Z² (so this is no-3-in-line on a diamond
region) makes the encoding clean, and a SAT table extension would test a
named conjecture. Two decisive negatives: the author is the most active
computational player in exactly this problem space (GPU record
constructions on the classic problem, March 2026 — being scooped by his
own v2 is likely), and none of his 15 exact values are visible in
snippets, so the only definitional control is a pattern fingerprint
(four gap-1 exceptions), weaker than E1's theorem-anchored controls.
Kept as the strongest future-session candidate of the day.

### E3 — Three-color off-diagonal Rado numbers for x+y+c_i = z *(arithmetic Ramsey theory)*

*Statement.* Least N such that every 3-coloring of [N] has an i-colored
solution of x+y+c_i = z for some i. Adak–Bakshi–Chandran–Nanoti (IISc;
arXiv:2602.23954 + 2603.28216, Feb/Mar 2026) settle the 2-color
off-diagonal pairs exactly and defer >2 colors to future work; the
3-color table appears nowhere. Diagonal anchor R₃(x+y+c=z) = 13c+14
(Schaal 1995, (secondary)).

*Why not selected.* Guaranteed open, guaranteed one-day feasible
(N ≲ 400, existing `rado.py` handles it unmodified) — but purely
exploratory: no named conjecture to decide, and the value of a first
table is lower than the value of settling a sharpness question a
month-old paper explicitly leaves open. Designated same-day pivot if E1's
semantics fail their control battery.

*Also vetted and set aside* (details kept for future sessions): Erdős
#307 (product of two prime-reciprocal sums = 1; my reduction: equivalent
to a 2-cycle M′=N, N′=M of the arithmetic derivative with M, N squarefree
and coprime, whence P∩Q=∅, Σ_{P∪Q} 1/p = a+1/a ≥ 2, so ≥ ~60 primes and
min(M,N) astronomically large — integer-range search worthless; honest
session shape is theory-only; Ufnarovski–Åhlander no-2-cycles conjecture
is the same wall, (secondary)); Kauers–Koutschan guessed-recurrence batch
(arXiv:2303.02793 — live but actively harvested by Niu/Fried notes
through Jul 2026); Treblecross ·007 Grundy frontier (GoNC6 2025 states
2^25; real frontier hidden behind blocked pages, active hobbyist
competitor); weak-Schur off-diagonal WS(2;k₁,k₂) gaps (open instances
locked in a paywalled table); w(2;3,t≥20) (12 years stuck, not one day);
Ahmed–Bright–Zaman ax+ay=bz grids (open cells cost 58 CPU-hours+ each);
classic and checkerboard-adjacent no-3-in-line variants (GPU arms race,
2025–26); octal .106 (settled: period 328,226,140,474, (secondary));
Erdős #364/#488/#848 (respectively: pair-structure makes triple search
non-finite; near-extremal constructions live at unreachable scales;
Sawhney solved asymptotically, remaining finite check has unknown N₀).

Two intelligence flags for future sessions, surfaced by the scout:
arXiv:2606.23721 "Holes in Valid-Extension Sets of Finite Gilbreath
Sequences" (Jun 2026) and arXiv:2605.22844 "Every Minimal Counterexample
to the Erdős–Gyárfás Conjecture is Predominantly Cubic" (May 2026) —
both touch active conjectures in this repository and are unread here
(blocked); check before the next session on either.

## 3. The internal thread

Strongest live internal thread: generalized-schur (08-07) left two named
next steps — (i) a disk-streaming certified pipeline to open the (4,4,u)
ladder beyond u = 9, and (ii) proving Conjecture A's lower bound
S(3;3,3,u) ≥ 9u−13 by completing the slot-skeleton construction. Step (i)
became *possible* today (glucose_static streams DRUP to disk), and step
(ii) is a genuine PROVED-label target. Assessment: (a) compute-shaped,
yes; (b) novelty certain; (c) would extend this repo's own 08-07 result
and modestly update one row. But it would be a second consecutive session
on the same conjecture, and it does not clearly beat E1: E1 decides a
named open question from a month-old external paper at guaranteed-feasible
sizes with theorem-anchored controls, and ties go to the new problem by
mandate. The streaming pipeline built today serves the internal thread
whenever it is picked up.

## 4. Selection argument

(a) *Compute-breakable?* E1: yes — instance sizes n ≈ 3k² ≤ ~510 for
every target case, 2–3 colors, and the only new machinery is the solution
enumerator (bounded Egyptian-fraction DFS); the 08-05/08-07 certified
pipeline (Glucose DRUP → `rup_check`, independent witness checker) carries
over whole. E2: yes but optimization-shaped (cardinality bounds), with
UNSAT hardness at n ≥ 17 unknown. E3: yes trivially. Internal: yes.
(b) *Already done?* E1: the sharpness question is stated open in the
paper's own July 2026 abstract; the residual their-table risk is bounded
by reproduce-first and marked-overlap discipline. E2: high scoop risk
(author's own v2). E3: effectively no risk but also no question to settle.
(c) *Citation target.* E1: Gaiser–Ramezanpour directly (their open
question), Gaiser's Discrete Math paper, and the certified-Rado
methodological line (Ahmed–Bright–Zaman; Chang–De Loera–Wesley). E2:
Prellberg. E3: the IISc quartet, Myers–Robertson, Schaal.

E1 wins on (b) and (c) with (a) equal-best; E3 is the pre-committed pivot.
Semantic control battery, defined before production: my encoder must
reproduce f₂(6) = 108 (their theorem, m = 1), must find SAT witnesses at
n = 3k² for k = 3, 5, 7, 9 (their lower-bound theorem requires them), and
the tuple enumerator must agree with an independent brute-force
implementation on a grid of small (k, n). Any control failure halts the
lane and pivots to E3.

## 5. Tool discipline

(filled at close: controls run, seeds/runtimes, cross-checks)
