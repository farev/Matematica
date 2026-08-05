# 2026-08-05 — powerful progressions (van Doorn's consecutive-triples conjecture)

**Target.** Van Doorn's May-2026 conjecture (arXiv:2605.06697 **(secondary)**)
that infinitely many 3-term APs consist of three *consecutive* powerful
numbers, whose entire published evidence base is the list of 18 such triples
below 10^14. It looked tractable because the census is an exact integer sweep
costing `√X` — so four cores buy five orders of magnitude — and because the
published frontier is a single number (18 at 10^14) that the pipeline can
reproduce as a calibration gate before making any new claim. Chosen from a
three-candidate external slate per the mandate; selection argument in §4.

**Result.**
- **CERTIFIED** — complete census to **10^19**: exactly **346** triples
  (152 below 10^18; 18 below 10^14, matching van Doorn exactly), all 346
  re-verified by an independent implementation, the 10^18 prefix replicated
  with independent segmentation, counts anchored to OEIS A118896 at
  10^10–10^12 **(secondary)**. No 4-term AP of consecutive powerful numbers
  below 10^19.
- **PROVED** — Lemma 1′: exact criterion for which integer multiples of a
  gcd-1 triple are componentwise powerful (mandatory primes + valuation
  bound); Lemma 2: two squares in a consecutive triple force `d > √x`.
- **CERTIFIED** — structure: the 346 triples are 16 primitive triples up to
  rational scaling; every chain is the set of consecutive survivors among the
  Lemma-1′ multiples of a gcd-1 **root**. (1728, 1764, 1800) = 36·(48, 49, 50),
  36 being that root's minimal admissible multiplier; one root has common
  difference 7. One chain holds 272 of the 346 triples and first loses a
  multiple at m = 288; the smallest such failure anywhere is
  2·(1728, 1764, 1800) broken by the intruder 3481 = 59². **P15** at
  4.15×10^17 is the unique primitive with **no** perfect-square element —
  the other fifteen have exactly one.
- **NUMERICAL** — primitive count 6 → 16 across 10^14 → 10^19: new primitives
  arrive across the whole range; supports but does not prove the conjecture.

Everything in `conjectures/powerful-progressions/` (README, NOTE, WRITEUP,
code, data, verification transcripts). Also kept: `tools/satcert/`, a
validated DRUP-certification toolkit built before selection (see §5).

**What failed.**
- Reading any primary source: proxy 403s on arxiv/oeis/erdosproblems/
  mathoverflow and five mirror attempts. Every citation today is (secondary);
  van Doorn's family "A₁" stays undefined here, so our primitive
  decomposition is *not* compared to his family structure.
- The "every primitive contains exactly one square" pattern — true for all
  15 primitives below 10^18's fifteenth, killed by P15. Salvaged as Lemma 2
  ("at most one" is a theorem when d ≤ √x).
- The integer-multiplier chain model: a defensive assert fired on P15's
  chain (members at ratio 45/2 to the primitive); replaced by the root model
  and Lemma 1′.
- The first analyzer (full admissible enumeration to X/z): infeasible at
  K ~ 5×10^14; redesigned to first-missing scans.
- Candidate E2 (Rado/generalized Schur values) died on unverifiable novelty:
  the deciding table (Ahmed–Schaal's 26 values) is in a blocked PDF.
  Computing values without knowing which are new fails hard rule 3.

**Next.** (1) Replicate the 10^19 sweep with a different segmentation (the
one recorded defect); (2) read van Doorn's actual PDF from a connected
machine: compare the 16 primitives to family A₁, check whether odd-d and
squareless triples are noted, then decide whether this is a letter to van
Doorn and/or an OEIS submission (first elements 1728, 6912, 729000, … appear
OEIS-absent, **(secondary, absence-of-evidence)**); (3) the sharpest
mathematical thread: a density argument for consecutiveness along one chain's
admissible multipliers — Result C5 says the naive construction fails
infinitely often, so the conjecture needs exactly this.

---

## 1. Connectivity check

| source | reachable | how |
|---|---|---|
| `arxiv.org` / `export.arxiv.org` | **no** — HTTP 403 CONNECT at egress proxy | WebFetch, curl |
| `oeis.org` | **no** — 403 | WebFetch, curl |
| `erdosproblems.com` | **no** — 403 | WebFetch |
| `mathoverflow.net` | **no** | WebFetch |
| mirrors (huggingface/papers, alphaxiv, emergentmind) | **no** — 403 | WebFetch |
| web search | **yes** | titles, URLs, synthesized summaries |
| `pypi.org` | yes (proxy bypass) | numpy, python-sat installed |

Same posture as 08-02/08-03 (proxy policy denial, `curl` CONNECT 403).
**No primary source was opened today; every citation in every document from
this session is (secondary), and every "still open" claim is a search-summary
claim.** Also: CLAUDE.md's `conjecture-research` skill is not installed in
this sandbox (.claude/ has only settings.json); its written discipline was
followed directly. Working branch is the environment-provisioned
`claude/kind-bohr-1j68fr` (the harness forbids pushing elsewhere), not the
`claude/<conjecture>-<date>` naming used when sessions provision their own.

## 2. The three external candidates

Built by three parallel scout subagents (number theory / arithmetic Ramsey /
graph conjectures), spanning three subfields.

### E1 — Consecutive powerful triples *(multiplicative number theory)* — SELECTED

*Statement.* Infinitely many 3-APs of three consecutive terms of the
powerful-number sequence (van Doorn, arXiv:2605.06697, May 2026; would answer
a question of Erdős in the negative). Published evidence: the complete list
of 18 below 10^14, smallest (1728, 1764, 1800). **(secondary)**

*Why believed open.* The paper is three months old and states the conjecture
as its own; searches surfaced no follow-up. No OEIS sequence for the triples
was findable. **(secondary, absence-of-evidence)**

### E2 — Off-diagonal generalized Schur numbers S(3; s,t,u) *(arithmetic Ramsey theory)*

*Statement.* Least N such that every 3-coloring of {1..N} has a monochromatic
solution of `x₁+…+x_{tᵢ−1} = x_{tᵢ}` in some color i. Ahmed–Schaal (Exp.
Math. 2016) computed 26 values and conjectured `S(3;s,t,u) = stu−tu−u−1` for
`4 ≤ s ≤ t ≤ u`; Song–Mao (arXiv:2604.11030, Apr 2026) proved the companion
strict lower bound and partial upper bounds, leaving exact values open.
**(secondary)**

*Why not selected.* The exact open boundary — which triples are among the 26
published values — is in PDFs the proxy blocks; a computed value could not be
honestly claimed new (hard rule 3). Environment also crowded: a distributed
farm on the adjacent 4-color ladder, a cluster group extending the (a,b,b)
tables with 58-hour instances.

### E3 — Refuting a fresh graph-invariant conjecture *(graph theory)*

*Statement (best of three vetted).* IRIS "5/3" conjecture: connected subcubic
G ⟹ `Z(G) ≤ (5/3)γ(G) + 4/3` (zero forcing vs domination), verified only for
the 112 connected subcubic graphs on ≤ 7 vertices. **(secondary)**

*Why not selected.* The scout found the genre is an active 2026 harvesting
ground (two dedicated AI refutation groups, four+ search papers; recent kills
within weeks of being flagged), one group flagged this exact target ~8 weeks
ago, and freezing invariant definitions requires the blocked primary sources.
High scoop-risk, high variance, novelty window unknowable from here.

## 3. The internal thread

Strongest live thread: **circular-thresholds, Pansiot-encoding morphism
search** (08-03's named next step) — concrete, compute-breakable, a hit
settles an open case of Currie–Mol–Rampersad. Scored: (a) yes, a finite
search; (b) not done, per 08-03's survey; (c) extends Mol–Rampersad. Against
it: that session's five morphism searches over five alphabets all came back
empty, the published `n ≥ 45` proof uses non-uniform families (weak evidence
that uniform hits at small n do not exist), and the same conjecture was
worked two days ago. Runner-up: additive-squares (1,1,0) tree closure
(branching at depth ~440 unmeasured — could exceed any budget). Neither
clearly beats E1, whose deliverable is guaranteed-completable and whose
novelty check is decisively clean today. Gilbreath R3.11 and the chowla k=28
extension fail the significance bar as before.

## 4. Selection argument

(a) *Compute-breakable?* E1 decisively: the full attack ran during
feasibility scouting (census to 10^18 in 3.5 minutes single-threaded, after
reproducing the paper's 18-at-10^14 exactly). E2 yes for small cases, E3 yes
per-graph — but neither survives (b).
(b) *Already done?* E1: the published frontier is one number, reproduced
here; nothing beyond 10^14 is claimed anywhere searchable. E2: cannot be
determined from this sandbox — disqualifying. E3: actively harvested by
better-resourced groups — poor expected novelty.
(c) *Who cites it?* E1: van Doorn directly, Chan's powerful-AP line, the
erdosproblems powerful-numbers entries; a census 10^5× beyond the paper's own
is exactly what its next version or reader wants. E2: Song–Mao/Ahmed–Schaal.
E3: the automated-conjecturing community.

**The result attempted today** (stated before the main runs): a CERTIFIED
complete census of consecutive-powerful AP3s to at least 10^18 (≥ 10^4× the
published range) with independent per-triple verification and replicated
completeness, plus whatever exact structure the data supports (proved
scaling lemmas, primitive decomposition), each claim labelled. Achieved, and
extended to 10^19.

## 5. Tool discipline

Positive controls: powerful-number counts at 10^10–10^12 vs OEIS A118896;
gap-1 pairs vs A060355; the 18-at-10^14 gate. Cross-checks: monolithic vs
segmented programs at 10^14/10^16; two independent segmentations at 10^18;
independent per-triple verifier (different algorithm, different code path)
on all 346 triples; every observed multiplier re-checked against Lemma 1′
(zero exceptions). Negative controls on the (unused) SAT toolkit: corrupted
and truncated DRUP proofs rejected; monochromatic coloring rejected.
Runtimes/cores in NOTE §4; no randomness anywhere.

Infrastructure kept for future sessions: `tools/satcert/` — DRUP checker +
witness verifier + bisection Rado driver, validated on R₂/R₃ classics and
end-to-end on R₄(x+y=z) = 45 (witness independently verified; UNSAT proof
RUP-checked). Built for the E2 branch before it was rejected; closes the
08-03 defect class (uncertified UNSAT verdicts) for any future SAT-shaped
session.
