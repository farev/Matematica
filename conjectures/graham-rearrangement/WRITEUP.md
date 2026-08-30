# Session write-up — 2026-08-30 (session 1)

Cloud sandbox, 4 threads on an Intel Xeon @ 2.80 GHz, 15 GB RAM, no NumPy.
Network egress worked for arxiv.org directly and for erdosproblems.com /
oeis.org / mathoverflow.net via curl (their WAFs 403 the default fetcher).

## How this conjecture was chosen

Mandate for the day: an external open problem, chosen from the live
literature, with a bottleneck a few CPU-cores can actually break. Three
candidates were vetted in parallel by literature subagents:

1. **Erdős #475** (Graham's rearrangement conjecture) — DECIDABLE badge on
   erdosproblems.com; four asymptotic papers 2024–26 settle all sufficiently
   large p; nobody had ever verified p = 29 or 31.
2. **Erdős #273** (covering system with all moduli p−1, p ≥ 5) — genuinely
   open, and the reciprocal-sum landscape is inviting (Σ 1/m over usable
   divisors of 55440 is already 1.0437 > 1), but two unrefereed AI-assisted
   2026 attacks (a July forum/GitHub campaign and a Zenodo note) already
   claim exactly the small-lcm ground a day of SAT could plough: UNSAT for
   every lcm dividing 55440/110880/166320/720720 and lcm ≥ 393120. A session
   here would be an audit of unrefereed certificates, not fresh territory.
3. **γ(Q₂₆) ∈ {13,14}** (smallest open queens-domination value, A075458) —
   open, but the 2017 Bird thesis calls n = 26 "thousands of processors"
   scale, and the 2026 proof-producing SAT framework (Rostami–Bright)
   certifies enumeration only to n = 19 at ~2 CPU-days. Not a one-day,
   four-core problem.

\#475 won on all three criteria (breakable bottleneck, verifiably nobody has
done it, a hot 2024–26 literature that would cite a small-prime closure).
The internal candidate (balanced-colorings K₂₆) lost to it on (a): its SAT
instances defeated four solvers three days ago and there is no reason
today's four cores change that.

## What happened, in order

**Engine v1** (naive): random shuffles then plain DFS. Correct on p = 17
(35 orbits, matching Burnside) but 5.7 s for what should be milliseconds —
dense sets fail 6 shuffles almost surely and plain DFS wanders ~10⁷ nodes
to a first witness.

**Engine v2** (+ orbit reduction, randomized restarts with growing
budgets): 800× faster on p ≤ 19, exact Burnside match on every cell tried —
and then **stuck for 12+ CPU-minutes on a single t = 18 set at p = 23**.
Diagnosis: near-full sets have witnesses that are *rare relative to t!*;
unbounded randomized DFS on such a set keeps re-exploring dead regions.

**Engine v3** (the shipped `verify_grc.c`): tiered decision — 64 shuffles,
then swap-based local search on the collision count (8 × 30k moves), then
16 randomized bounded DFS restarts, then a big local-search pass, then a
final *deterministic complete* DFS as adjudicator. The tier that matters is
the local search: the p = 23 window that v2 could not finish went from
stuck-forever to **0.16 s, zero sets past tier 2**. Controls: the `-z` mode
(forbid 0 as a partial sum) correctly refutes {x, −x} by complete DFS, and
the witness scan validates every returned ordering before it is reported.

**The runs.** Full range t = 2..p−1 for every prime 3 ≤ p ≤ 31 (13 s for
p = 29, 58 s for p = 31, 4 threads, seed 12345), then p = 37 (t = 2..36,
5473 s ≈ 91 min; the peak layer t = 18 alone holds 252,088,496 orbits).
Every one of the per-(p,t) orbit counts equals the independent Burnside
computation exactly, every orbit produced a witness, zero failures, zero
adjudications. The only two sets in all of p ≤ 31 that needed tier 3 are
the full sets F₂₉^* and F₃₁^* themselves — Graham's original t = p−1 case
really is the hardest instance in practice. At p = 37 that hardness
spreads into the near-full band t ≥ p−5: 124 tier-3 orbits, resistant
fraction rising from 36/1641 (t = 32) through 70/199 (t = 33) and 16/18
(t = 34) to 1/1 at t = 35 and 36, max 2.55×10⁷ DFS nodes — a clean
empirical picture of where the conjecture is search-hard.

**The p = 41 bonus slice.** With the engine idle after p = 37, the dense
half of the new frontier prime was affordable: t = 28..40 in full
(227,999,052 orbits, 9.12·10⁹ subsets, ≈ 2.6 h, Burnside-exact on all 13
cells, zero failures). The resistant band there starts at t = p−7 —
4,585 tier-3 orbits, max 1.79×10⁸ DFS nodes, still nothing beyond
tier 3 — so p = 41's open window is now 13 ≤ t ≤ 27.

**Operational defect, recorded.** A cleanup glob (`rm data/err_p*.txt`)
ran after the p = 37 job had opened its stderr redirect and unlinked the
live file, so the run's stderr banner channel was lost. No information
was lost with it: counterexamples are recorded in two other places (the
per-layer `fail` counters on stdout, all zero, and the witness file,
which logs every tier-3+ set and would carry a NO-VALID-ORDERING marker;
it carries none, re-verified line by line post-run). Lesson: never glob
a directory that a live run writes into.

**The verifier caught a real divergence.** `check_witnesses.py` is a
clean-room re-implementation; its sampling mode canonicalized orbits by
"minimum mask over *all* dilations", the engine by "minimum mask over
dilations *containing 1*" — different transversals of the same orbits (a
set containing 1 always has bit 1 set, which a {2,...}-set beats). An
assert tripped on the first p = 29 sample; the verifier was aligned to the
engine's rule. The Burnside identity is what proves the engine's rule is a
transversal, independently of any of this.

**Gray zone.** The zero-sum size-(p−3) sets — Z_p ∖ {0, x, −x} — form a
single dilation orbit per prime (dilate by x⁻¹), so one witness per prime
settles the layer. Certified for every prime 7 ≤ p ≤ 61, each witness
re-verified in Python from the definition. Primary sources were read
directly for the surrounding claims (see NOTE §5): the HOS19 k = p−3
construction is parametrized by removed pairs {d, r+1} with 1 ≤ d < r and
the zero-sum pair needs d = r, so it provably never reaches this layer;
CDORF22's one-sentence extension claim points at fixed-k polynomial
calculations that cannot reach k = p−3; Kravitz 2024 still states the
record as "non-zero sum set of size p−2 or p−3".

## What failed (kept per policy)

1. **Uniform construction for the zero-sum p−3 layer** — the would-be
   PROVED headline. Three explicit families died:
   - *Two-block zigzags* (all +k then all −k, ±alternating, parity splits):
     8 variants, valid for at most 1 of 106 primes. The two phases produce
     interval-like partial-sum sets that would have to tile each other's
     complement exactly.
   - *Rotated two-block* (cut points a, c in each phase): **zero** valid
     (a,c) pairs for any prime 11 ≤ p ≤ 397 — the family is structurally
     dead, same mirror-collision mechanism.
   - *Interleaved zigzag with rotated second pass*: zero hits, all p ≤ 300.
   - *Geometric telescope*: partial sums of c·gⁱ are automatically
     distinct, and {2,...,p−2} is exactly the shifted run {1 − 2^{i+1}}
     when 2 is a primitive root — a genuinely pretty coincidence — but the
     shift adds a linear term to the sums (α gᵏ + k), injectivity dies
     (first collision already at p = 11), and the unshifted run cannot
     work: the two missing values of a GP-run are consecutive powers,
     while {1, −1} are antipodal. Recorded as an obstruction: no pure or
     shifted GP ordering exists for this layer.
   Lex-min witnesses (mined for p ≤ 31 via the `-l` mode) show a long
   ascending prefix 2,3,4,...,~p/2 with a greedy irregular tail — no
   visible closed form. Conclusion: this layer wants the graceful-
   permutation machinery of HOS19, i.e. a real sub-project, and the session
   kept it CERTIFIED-only.
2. **Engine v1/v2's unbounded randomized DFS** — see above; the fix (local
   search) is the reason the whole computation costs seconds.
3. **Erdős #273 as the day's target** — dropped at selection, not attacked;
   the vetting is filed in the log for a future session (first unclaimed
   lattices: L = 332640, 1441440, 2162160, 4324320).

## Reproduction

```
gcc -O3 -march=native -o verify_grc verify_grc.c -lpthread
./verify_grc 29 2 28 4 12345 data/witness_sample_p29.txt 1000 > data/results_p29.txt
python3 summarize.py            # re-asserts Burnside on every cell
python3 check_witnesses.py hard data/witness_sample_p29.txt
python3 check_witnesses.py sample 29 13 26 60 777
```

Seeds: engine 12345 (all runs; decisions are deterministic given it);
independent-sampler seeds 777 (p = 29, t ≤ 19, 60/layer, first pass),
778/779/781 (full windows at 29/31/37 — every layer 13 ≤ t ≤ p−3 —
25/25/15 per layer, zero failures). Wall times in data/results_p*.txt;
machine as above. The first sampler pass used a DFS-only fallback and
crawled on dense layers; the shipped verifier adds an insertion-move
repair loop (deliberately a different move type from the engine's swaps)
which decides dense layers in seconds.
