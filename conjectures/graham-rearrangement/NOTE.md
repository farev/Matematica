# Certified small-prime closure of Graham's rearrangement conjecture

**Session 1 note — 2026-08-30.** Research assisted by an AI system
(Claude); every claim below is labelled per the repository's discipline and
every computational claim ships code, data and an independent verifier.

## Abstract

Graham's rearrangement conjecture (Erdős problem #475; also "G-ADMS" after
Archdeacon–Dinitz–Mattern–Stinson) states that for a prime p, every subset
A ⊆ F_p ∖ {0} can be ordered so that its partial sums are pairwise
distinct mod p. It was recently proved for all sufficiently large p by the
combination of four ineffective asymptotic results, and is proved for
|A| ≤ 12 (refereed), |A| ≤ 20 (2026 preprint), and for nonzero-sum A of
size p−1, p−2, p−3. The largest published per-prime verification was the
uncertified 2016 random search of ADMS through cyclic order 25.

This session closes every prime p ≤ 37 by certified exhaustive
computation: all 1,954,471,973 dilation orbits of nonempty subsets
(70,066,181,009 subsets), every one receiving an explicit witness
ordering, with orbit counts matching an independent Burnside computation
on all 173 (p,t) cells, zero failures. The smallest prime at which the
conjecture is not fully decided (by proof or certified computation) is
now 41. Separately, the zero-sum size-(p−3) layer — which the
Hicks–Ollis–Schmitt construction provably cannot reach, and which the
published record treats inconsistently — is certified for every prime
7 ≤ p ≤ 61.

## 1. Statement and vocabulary

For A = {a₁,…,a_t} ⊆ F_p ∖ {0}, an ordering (a_{σ(1)},…,a_{σ(t)}) is
**valid** if the partial sums s_m = a_{σ(1)}+⋯+a_{σ(m)}, 1 ≤ m ≤ t, are
pairwise distinct in F_p (0 may occur among them, once). Graham's
conjecture: every A has a valid ordering. A **sequencing** additionally
demands s_m ≠ 0 for all m (possible only if ΣA ≠ 0); for ΣA = 0 the
analogous notion is a **rotational sequencing** (s_t = 0, all earlier
s_m distinct and nonzero — for zero-sum sets this coincides with a valid
ordering in which 0 appears only as the final sum). Sequenceable ⟹ has a
valid ordering.

## 2. Results

**R1 (CERTIFIED).** For every prime p ≤ 37 and every t with 2 ≤ t ≤ p−1,
every subset A ⊆ F_p ∖ {0} with |A| = t admits a valid ordering.
Verified exhaustively at orbit level: 1,954,471,973 canonical
dilation-orbit representatives decided (45,590,075 across p ≤ 31;
1,908,881,898 at p = 37), covering 70,066,181,009 subsets. Every
representative received an explicit witness ordering; no set failed; the
per-cell representative counts equal the independent Burnside counts
exactly on all 173 cells. (Sizes t ≤ 1 are trivial.)

**R2 (CERTIFIED).** For every prime 7 ≤ p ≤ 61, the zero-sum sets of size
p−3 — precisely the sets Z_p ∖ {0, x, −x} — admit valid orderings.
(One dilation orbit per prime, Lemma L2; witness for the representative
{2,…,p−2} committed and independently re-verified for each p.)

**L1 (PROVED, elementary).** If c ∈ F_p^* and (a₁,…,a_t) is a valid
ordering of A, then (ca₁,…,ca_t) is a valid ordering of cA. Hence
admissibility is a dilation-orbit invariant, and it suffices to decide one
representative per orbit. ∎ (partial sums scale by c, distinctness is
preserved)

**L2 (PROVED, elementary).** The sets Z_p ∖ {0, x, −x}, x ≠ 0, form a
single dilation orbit, represented by {2,…,p−2}. ∎ (dilation by x⁻¹ maps
{x,−x} to {1,−1})

**O1 (observation, exact for these runs).** In the full sweeps at p = 29
and p = 31, exactly one subset per prime resisted both the shuffle tier
(64 random orderings) and the local-search tier: the full set
F_p ∖ {0} itself — the t = p−1 case that Graham proved in 1971. Every
other orbit fell to 64 shuffles or to swap local search. At p = 37 the
same statement holds [checked against the completed run log].

**O2 (observation / small proved remark).** No ordering of
Z_p ∖ {0, 1, −1} is a run of a geometric progression: a length-(p−3) run
of powers of a primitive root g misses two *consecutive* powers, while 1
and −1 are never consecutive powers for p > 3 (g = −1 is not primitive).
The affine variant (a_i = c·g^{i−1}(g−1) + β, which for g = 2 primitive
and β = 1 reproduces the set exactly as {1 − 2^{i+1}}) has partial sums
αg^k + βk + γ; injectivity of that map fails already at p = 11. So the
"telescoping" route to a uniform construction for R2's layer is closed.

## 3. Method

**Transversal.** Enumerate subsets containing 1; keep A iff its bitmask is
minimal among the |A| dilations (1/a)·A, a ∈ A (each such dilation again
contains 1). This picks exactly one set per orbit; correctness of the
implementation is witnessed by the exact Burnside match on every cell
(the count identity is (1/(p−1))·Σ_{d | gcd(p−1,t)} φ(d)·C((p−1)/d, t/d)).

**Per-set decision** (deterministic given the run seed): T1 — 64 seeded
shuffles; T2 — swap-move local search minimizing the number of collided
partial-sum slots (8 restarts × 30k moves); T3 — 16 randomized-order DFS
restarts with growing node budgets; T4 — deeper local search (192 × 250k);
T5 — complete deterministic DFS (exhaustive; its exhaustion would exhibit
a counterexample). Every returned witness is re-scanned from the
definition before being reported. In the entire computation nothing
reached T4 or T5.

**Controls.**
- *Negative control*: in `-z` mode (partial sums additionally forbidden to
  be 0) the engine's complete DFS correctly refutes {x, −x} — a zero-sum
  pair has no sequencing — exercising the exhaustive path.
- *Independent verifier* (`check_witnesses.py`, clean-room): re-checks
  every committed witness from the definition, re-checks canonicality,
  re-decides random samples with its own enumeration and search (60 sets
  per layer at p = 29, 31: zero failures), and carries self-tests with
  planted invalid witnesses.
- *Determinism*: every per-set decision is a pure function of
  (p, t, subset rank, seed). A full p = 29 rerun (under heavy CPU
  contention) reproduced the result lines identically and the
  witness-sample file byte-for-byte. (Line *order* in witness files is
  written under a mutex and is in principle scheduler-dependent; the
  decisions and per-line content are not.)

**Cost.** 4 threads, Intel Xeon @ 2.80 GHz: p = 29 in 13 s, p = 31 in
58 s, p = 37 in ≈ 2.5 h wall (times per layer in data/results_p37.txt);
seeds and full tables in data/.

## 4. Data and reproduction

See README.md for the script table and commands. Committed artifacts:
per-layer result lines for every prime (data/results_p*.txt), ~47k
sampled witnesses (every 1000th orbit for p ≤ 31, every 100000th at
p = 37, plus every tier-3+ set), the gray-zone witnesses for p ≤ 61, and
the lex-min witnesses used in the construction hunt. Everything else is
reproducible bit-for-bit from the seeds; per-set decisions are pure
functions of (p, t, subset rank, seed).

## 5. Relation to prior work (all quotes verified against the PDFs read today, except where marked)

- **Proved ranges.** |A| ≤ 12 for all primes: Costa–Pellegrini 2020
  (Arch. Math. 115, arXiv:2003.05939), Prop. 4.2, via Alon's
  Nullstellensatz with exact integer coefficients whose gcd is 2³ —
  "G-ADMS conjecture holds for subsets of size k ≤ 12 of cyclic groups of
  prime order." Extended by CDORF22 (Electron. J. Combin. 29(3) #P3.33) to
  sequencings for |A| ∈ {11,12}. **|A| ≤ 20 in any abelian group**:
  Costa–Della Fiore–Fontana–Vena, arXiv:2603.20961 (21 Mar 2026,
  **unrefereed preprint**), Thm 1.4; zero-sum |A| ≤ 22, Thm 1.5. R1 is
  independent of all of these (it re-decides every size from scratch) and,
  at p ∈ {17,…,37}, is an independent confirmation of the preprint's
  range at those primes.
- **Near-full sizes.** t = p−1: Graham 1971. t = p−2: Bode–Harborth 2005
  *(secondary — paywalled; statement as quoted by ADMS16/HOS19)*, reproved
  constructively as HOS19 Thm 4.3. t = p−3 **with ΣA ≠ 0**: HOS19
  Thm 4.6 (J. Combin. Des. 27, arXiv:1809.02684) — their construction
  orders Z_p ∖ {0, d, r+1} for 1 ≤ d < r (p = 2r+1), and the zero-sum
  layer is exactly d = r, outside the parametrization; their Lemma 4.4
  moreover produces *nonzero* partial sums, impossible for zero-sum sets.
- **The zero-sum p−3 discrepancy.** CDORF22 assert (intro): "Regarding
  Theorem 3.3 [k = n−3, n prime, ΣS ≠ 0], we note that the case ΣS = 0
  was not considered in [13] but, as we shall see in the next section,
  the calculations there work in this case too, without modification",
  and later "the above discussion shows that the same calculations also
  prove Theorem 3.3 when ΣS = 0." The discussion referenced is the
  reduction of their t = 1 polynomial to the polynomial of HOS19 — the
  *fixed-k* Nullstellensatz computations (k ≤ 10/12), which cannot apply
  at k = p−3 (the coefficient computations are per fixed k). Kravitz
  (INTEGERS 24 (2024) #A113, arXiv:2407.01835) still states: "the state
  of the art is still essentially that Conjecture 1.1 holds when |A| ≤ 12
  … and when A is a non-zero sum set of size p−2 or p−3." R2 settles the
  layer by certificate for 7 ≤ p ≤ 61 regardless of how that textual
  discrepancy resolves; a uniform proof remains open (see §6).
- **Per-prime verifications.** ADMS16 (JCMCC 98 (2016) 327–342,
  arXiv:1501.06872): "We have checked that Conjecture 1 is true up to
  n = 25" — random permutations in Mathematica, "programmed … and run on
  a laptop PC", no code or witness files published. CMPP18
  (Discrete Math. 341, arXiv:1706.00042) verified valid orderings for all
  abelian groups of order ≤ 23. Nothing beyond order 25 is in the
  literature for any group; p = 29, 31, 37 were unverified before today.
- **Asymptotics (all ineffective at small p).** Kravitz 2024
  (t ≲ log p/log log p — effective but vacuous below p ~ 10³);
  Bedert–Kravitz arXiv:2409.07403 ("Let p be a large prime");
  Costa–Della Fiore arXiv:2602.19989; Pham–Sauermann arXiv:2602.15797
  (constant "sufficiently large with respect to α"); Bedert–Bucić–
  Kravitz–Montgomery–Müyesser arXiv:2508.18254 (|S| ≥ |G|^{1−c},
  unspecified c); Müyesser–Pokrovskiy arXiv:2204.09666 ((1−o(1))|G|).
  Consequently no explicit p₀ exists in print bounding the "finite check"
  that erdosproblems.com's DECIDABLE badge refers to; the frontier moves
  prime by prime, and R1 moves it to 41.
- The erdosproblems.com/475 page (last edited 2026-03-05) still lists
  t ≤ 12 and "p−3 ≤ t ≤ p−1" without the zero-sum caveat; both lines are
  out of date as described above.

## 6. Open questions

1. **p = 41**: ~27.4G orbits (5.5·10¹¹ subsets) — one notch beyond this
   session's engine (≈ 20× the p = 37 cost); reachable with either a
   week of background compute or meet-in-the-middle canonicality.
2. **A uniform construction for the zero-sum p−3 layer** (all p, not
   p ≤ 61): three natural families are dead (§WRITEUP); the lex-min
   witnesses (data/lexmin_pminus3.txt) suggest an ascending prefix with a
   twizzled tail à la HOS19. A proof would close the CDORF22/Kr24
   discrepancy permanently.
3. **Where is the search hardness?** O1 says the *full set* is the unique
   locally-hard instance at each prime in range. Is F_p^* asymptotically
   the extremal set for number of valid orderings relative to t!?
