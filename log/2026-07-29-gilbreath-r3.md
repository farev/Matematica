# 2026-07-29 — gilbreath (R3)

**Target.** Open Problem R3 (REDUCTION.md §3): does [fixed-order Cramér gap
statistics] + [a_n = o(n)] imply eventual Gilbreath? Executed the four
experiments of R3-ATTACK.md in order, then followed the evidence.

**Result.** Mixed, substantial.
PROVED: the parity-transform package (erosion-path parity = S·rev(y), lead
parity = S·y, S involutive, SσS = I+σ, dyadic doubling; corridor systems
always solvable, solution space = anchored 2^B-periodic strings; deep
parity rows vanish below depth 2^B). PROVED: bounded-entry a.s. failure of
Gilbreath for a_n = 2·geometric (via CHT Thm 1.2 plus pairwise-independent
lead parities at depths 2^j), making CHT's one-sentence remark precise.
Theorem R3.5 (construction and statistics PROVED, bad-lead persistence
NUMERICAL): for every K an independent bounded-entry sequence with
model-quality window statistics to order K and leads > 1 at positive
density, so every finite-order axiom set fails even with bounded entries,
and CHT Thm 1.3's 2-separated axiom (ii) is necessary, invisibly to every
fixed order. NUMERICAL laws: cooling race (period-P structure survives iff
entry scale μ ≳ P^{3/2}; boundary P* ≈ 24·μ^{2/3}) and front pinning (a
{0,2} ocean cannot invade a cooled {0,1} strip; penetration ≤ 2 columns
over 12k+ rows). Also verified the CHT arXiv reference resolves as cited
(standing repo caveat discharged). Everything in conjectures/gilbreath/R3.md.

**What failed.** The brief's corridor idea, three ways, each with the
mechanism identified. (1) Plant corridors: nilpotency means the corridor
zeroes the whole deep parity cone, forcing non-cooling to {0,2}; erosion
stays 0.71/row (worse than i.i.d. control) and the small plant dies.
(2) Layered growing periods: the exact parity replication law works (lead
parity replays mod 2^c, verified exactly), but even patches over a cooled
sea are value-0, not value-2; sealed at the first generic band.
(3) Nested blocks: the fresh block content cools the array during the
pre-period band; the all-even regime arrives empty (dead beyond depth 66
at P₂ = 4096). Also the hoped-for hierarchical R3-weak counterexample:
front pinning blocks all heat imports from the right, so the whole
negative route is exhausted.

**Second phase (same day): agent fan-out on the three live hypotheses.**
PROVED: Lemma R3.6 (lead-parity rigidity: lead parities vanishing beyond
s₀ force exact 2^⌈log₂ s₀⌉-periodicity of the top parities; involution
one-liner, machine-verified both directions) and Corollary R3.7 (any
sequence with all-orders weak statistics has odd leads infinitely often:
the first unconditional consequence of the full hierarchy at the lead;
kills the "leads eventually even" failure mode, the mode of every
counterexample built today). PROVED conditionally: Lemma R3.8 (ballistic
erosion bound: path parities of a traveler crossing a cooled i.i.d.
strip are pairwise-independent Bernoulli(1/2), so erosion concentrates
at d/2 by Chebyshev). NUMERICAL, agent runs: (a) front pinning is robust
at entry scales up to μ = 4096, interface value scale exactly 2
independent of μ, mutual pinning both ways; the stress test isolated a
second transport channel, ballistic single-value transit (range ≈ 2.3μ,
measured toll 0.52 per row, reseals permanently afterward), which o(n)
kills at scale; (b) the cooling-race boundary is P* ≍ μ^{0.84±0.04}
over a factor 32 in μ (the earlier 2/3 fit is dead; all candidate
closed forms rejected; μ = 512 smears, heavy-tailed cooling), and P*
matches the directly measured cooling time within 20 percent, confirming
the race mechanism; (c) persistence of Theorem R3.5's bad-lead density
is stationary to depth 49,150.

**Third phase (same day): the theory agent's CHT adaptation.** PROVED
(reductions, audited in the main thread): Theorem R3.9, interior strip
cooling (bulk-rooted heat in a generic strip dies below depth
O(ε⁻¹ D₀ log W); direct corollary of CHT Prop. 4.1 on interior cones,
with the root-localization consequence via the hot-parent lemma), and
Theorem R3.10, fast-crossing suppression (≤2-valued transport paths pay
an independent uniform parity bit per leftward step, distinct leading
columns; crossings at speed above v* ≈ 0.773, the root of H(v) = v, are
exponentially suppressed). Lemma R3.6 survived an adversarial audit
(4000 cases; two wording repairs; biconditional sharpened with exact
threshold 2^B). The remaining analytic core of the whole program is now
one named statement, Open Lemma R3.11 (persistent-alignment cost for
slow crossings): the Lucas periodicity of parity forms near the front
gives the adversary a finite constraint budget per column; the missing
renewal argument would give P(penetration ≥ j) ≤ 2^{−cj} uniformly in
time, and the same budget count already predicts the measured Θ(1)
penetration.

**Next.** Prove Open Lemma R3.11 (slow-crossing renewal): it is the
single statement separating the noose from a theorem that generic-strip
sequences seal the lead. Then (S2) localization via R3.9. The boundary
exponent b ≈ 0.84 has no derivation. Whether Prop. R3.4 / Thm R3.5 are
worth a short note to CHT (letter_to_cht.md predates this session).
