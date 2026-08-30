# 2026-08-30 — graham-rearrangement

**Target.** New external problem, per the standing mandate. Erdős #475,
Graham's rearrangement conjecture: every subset A ⊆ F_p ∖ {0} has an
ordering whose partial sums are pairwise distinct mod p. Chosen for a
certified per-prime closure of the small primes the four 2024–26 asymptotic
papers cannot touch (their constants are ineffective at specific small p),
starting with p = 29 and 31, which no one had ever verified.

**Connectivity.** arxiv.org reachable via the standard fetcher.
erdosproblems.com, oeis.org and mathoverflow.net 403 the default fetcher's
user agent but serve curl normally — all four consulted live today.
(Cited-paper PDFs pulled from arXiv and publisher pages and read directly;
the one exception, Bode–Harborth 2005, is paywalled and stays (secondary).)

**The slate** (three external candidates, two subfields, all vetted against
primary sources by parallel literature agents; full notes in the session
scratchpad, key facts in conjectures/graham-rearrangement/NOTE.md §5):

1. *Erdős #475* (additive combinatorics). DECIDABLE on erdosproblems.com
   (page last edited 2026-03-05, and out of date: it still says t ≤ 12,
   superseded by the unrefereed 2026-03-21 preprint arXiv:2603.20961 with
   t ≤ 20). Largest published per-prime closure: cyclic groups of order
   n ≤ 25 — Archdeacon–Dinitz–Mattern–Stinson, JCMCC 98 (2016) — an
   *uncertified random-permutation Mathematica run*, "We have checked that
   Conjecture 1 is true up to n = 25" (quote verified in their PDF).
   p = 29, 31: never verified by anyone. All four asymptotic papers
   (Kravitz; Bedert–Kravitz; Pham–Sauermann; BBKMM) are ineffective at
   small p — Kravitz's effective bound gives only t ≤ 2 at p = 43.
2. *Erdős #273* (covering systems). "Is there a covering system all of
   whose moduli are p−1 for primes p ≥ 5?" Open; original source verified
   (Erdős–Graham 1980, p. 24, distinct moduli required by their
   definition). But two unrefereed AI-assisted 2026 attacks (July: a forum
   + GitHub campaign with exact-rational certificates; a GPT-assisted
   Zenodo note, DOI 10.5281/zenodo.21613011) already claim UNSAT for every
   lcm dividing 55440, 110880, 166320, 720720 and lcm ≥ 393120. A session
   here would audit unrefereed certificates rather than break ground. My
   own probe: Σ 1/m over usable divisors of 55440 is 1.0437 > 1, yet
   greedy covering leaves 14.5% uncovered against a 4.4% slack —
   consistent with their UNSAT claims. Filed for a future session (first
   unclaimed lattices: 332640, 1441440, 2162160, 4324320).
3. *γ(Q₂₆)* (graph domination / OEIS A075458). Smallest open queens-
   domination value, bracket {13, 14} since Östergård–Weakley 2001; a 2017
   thesis puts n = 26 at "thousands of processors"; the 2026
   proof-producing SAT framework certifies enumeration only to n = 19 in
   ~2 CPU-days. Expert expectation is 14 via Weakley 2022's structure
   theory (a monochromatic 13-set is provably impossible; a bichromatic
   one would refute his Conjecture 4). Not decidable on 4 cores in a day.

**Internal thread assessed.** Strongest live thread was balanced-colorings
(2026-08-27): decide K₂₆ or pin E*(26,6) ∈ [265, 269]. Its direct SAT
instances defeated four solvers three days ago; nothing about today's
hardware changes that, and the mandate's default is the new problem. #475
beats it on breakability and on citation surface (five active papers
2024–26). Selected: #475. Ties and defaults all pointed the same way.

**Result.** **CERTIFIED.** (1) Graham's rearrangement conjecture holds for
*every* subset of F_p ∖ {0}, all sizes t = 2..p−1, for **every prime
p ≤ 31** — 45,590,075 dilation orbits decided (1,346,704,310 subsets), a
witness ordering found for every orbit, zero failures; the p = 37 sweep
(1,908,881,898 orbits expected) is in flight and its completion note below
records the outcome. Per-(p,t) orbit counts match an independent Burnside
computation exactly on all 173 cells. Prior record: uncertified n ≤ 25
(2016). The smallest prime at which the conjecture is not fully decided is
now **41**. (2) The zero-sum size-(p−3) layer — one dilation orbit per
prime; the HOS19 construction provably cannot reach it (their removed
pairs {d, r+1} need d < r, zero-sum forces d = r) and CDORF22's
one-sentence claim to it rests on fixed-k polynomial calculations that
cannot apply at k = p−3 — **certified for every prime 7 ≤ p ≤ 61** with
independently re-verified witnesses. (3) Deterministic engine + clean-room
verifier + 46k committed sampled witnesses; the only tier-3-hard sets in
all of p ≤ 31 were F₂₉^* and F₃₁^* themselves.
*(p = 37 completion note: appended below when the sweep finishes.)*

**What failed.** The hoped-for PROVED bonus — an explicit uniform ordering
of Z_p ∖ {0, ±1} closing the zero-sum p−3 layer for *all* p — died three
times: two-block zigzag families (interval sum-sets must tile each other's
complement — measure-zero), all rotated variants (0 valid parameter pairs
across 74 primes ≤ 397), and a geometric-telescope attempt that founders
on a pretty obstruction: {2,...,p−2} *is* the shifted GP {1 − 2^{i+1}}
when 2 is a primitive root, but shifting adds a linear term that destroys
sum-injectivity (collision at p = 11 already), and an unshifted GP-run
can never miss the antipodal pair {1, −1}. Also: two engine generations
(naive DFS; budgeted randomized DFS) could not decide dense layers —
swap-based local search on the collision count is what makes the whole
computation cost seconds. Details in WRITEUP.md.

**Next.** (1) p = 41 is the new frontier: ~5.4·10¹¹ subsets ≈ 27G orbits,
roughly 20× today's p = 37 cost — feasible with a week of background cores
or one algorithmic notch (meet-in-the-middle canonicality, or trusting
CDFV26's t ≤ 20 to cut the window to t = 21..37). (2) The zero-sum p−3
layer as a theorem: the lex-min witnesses' ascending-prefix structure
suggests trying HOS19's graceful-permutation machinery with a "twizzled"
tail; a proof would close the CDORF22/Kr24 discrepancy for all p. (3)
Report the stale t ≤ 12 line on erdosproblems.com/475 (now t ≤ 20 via
arXiv:2603.20961) once this session's results are public, and consider
writing to the CDFV26 authors — this closure is an independent check of
their theorem at seven primes. (4) Erdős #273's unclaimed lattices, as an
audit-plus-extension session.
