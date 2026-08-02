# R3 attack brief

**STATUS: executed 2026-07-29 (session part 5). Outcome in [R3.md](R3.md).**
All four experiments were run in order. Experiment 1's corridor is always
solvable (the linear algebra is a triangular involution) but self-destructs
dynamically; the negative route died to the cooling race and front pinning,
not to rank or statistics; Theorem R3.5 (every finite order insufficient
with bounded entries) is what survived. This brief is kept as prepared, for
the record.

*Prepared 2026-07-29 at the close of the microscope/reduction session, to
make the next session self-sufficient. Read REDUCTION.md §3 first for the
statement of R2 and R3; MICROSCOPE.md for the lenses; CHT arXiv 2607.08712
§3–§4 for the machinery cited below (their Lemma 3.10 = parity linearity,
Remark 4.5 = exponential-entry counterexample, Thm 1.3 = probabilistic
cooling).*

## The question

**R3.** Is eventual Gilbreath (leads ∈ {0,1} for all large n) a formal
consequence of [fixed-order gap-pattern asymptotics of the Cramér model]
+ [a_n = o(n)]? The o(n) bound is unconditional for primes (BHP), so an
affirmative answer derives Gilbreath from Hardy–Littlewood-type
statistics; a negative answer strengthens R2.

## What this session already knew

- R2's lone plants need V ≳ position, because the mirrored telescope
  gives erosion ≍ Σ (background values along the cone's left edge) ≍
  c·distance for statistically typical backgrounds. Under o(n) entries,
  lone plants die. (REDUCTION.md, Remark on sharpness.)
- The staircase heuristic points the same way: corrupting the lead at
  depth n via the second column pushes the requirement rightward as
  "value ≳ distance from the left edge" — same wall.
- Extended {0,d} highways transport values without decay inside their
  own cone, but the cone never reaches column 1; left-leakage erodes at
  ~2/row. Long highways also leave fixed-order twin-type fingerprints
  (M8 mechanism), which is the informal reason to hope R3 is affirmative.

## NEW — the corridor / parity-steering idea (route to a NEGATIVE answer)

Erosion is not a law of nature; it is the background's nonzero values
along one specific diagonal path. CHT Lemma 3.10 makes array parities
LINEAR in the top-row parities (XOR–Pascal). In cooled regions the
values lie in {0,1}, so **parity 0 forces value 0 exactly**. Therefore:

1. Pick plant position m. The erosion path is the ~m cells
   a_{(s, m−s−1)}, s = 1..m−1.
2. Each cell's parity is an explicit F₂-linear functional of the top
   parities (binomial supports, Lucas).
3. Solving ~m linear equations over F₂ in the ~m prefix parity bits
   zeroes the cooled part of the path: a **corridor**. The uncooled
   shallow segment (first ~T_cool rows) contributes only O(T_cool)
   erosion, so a plant of value O(T_cool) — far below o(n), possibly
   O(log) — arrives at the lead intact.
4. If corridors can be built while preserving fixed-order statistics,
   R3 is FALSE and R2 strengthens dramatically.

## NEW — the over-determination obstruction (route to a POSITIVE answer)

Each corridor imposes ≈ m_j independent F₂ conditions on the parities of
the prefix [1, m_j]. Infinitely many derailments need corridors at
m_1 < m_2 < …, all satisfied by ONE sequence. With m_j = 2^{2^j} the
stacked system on prefix [1, m_j] has rank ≈ m_j on ≈ m_j variables —
**critical again** (the knife-edge that has appeared at every depth of
this program). Moreover the solution spaces are Sierpiński-rigid, and
rigid parity patterns have digit-sum-biased k-window frequencies, i.e.
they fight (α). The positive route: prove that any parity assignment
satisfying corridor systems at infinitely many scales has fixed-k window
frequencies bounded away from the i.i.d. ones. That would show (α)
forbids corridors, and combined with an erosion lower bound for
corridor-free sequences (typical-path zero-density bounded below by
window statistics — needs care: path cells overlap, no independence),
gives R3 affirmative.

## First experiments (cheap, decisive, in order)

1. **Build one corridor numerically.** m ≈ 300–1000: assemble the F₂
   system from Lucas supports (GF(2) elimination; numpy int8), solve,
   impose the parities on a geometric background (adjust each a_j by ±1
   to hit the parity), plant V ~ 3·T_cool, verify the lead derails at
   depth m. If no solution exists or erosion persists, the corridor idea
   dies immediately — also informative.
2. **Measure the statistical price.** For the corridor sequence, compare
   k-window frequencies (k ≤ 6) against the model: total-variation per
   window count vs the O_k(log log x) budget of (α). Rigid solution ⇒
   visible bias expected; measure it.
3. **Stack two corridors** (m₁ ≪ m₂): rank of the joint system,
   consistency, and the statistics damage growth. Extrapolate to
   infinitely many.
4. If corridors are statistically fatal: attempt the erosion lower
   bound — simulate typical-path zero-densities conditioned on window
   statistics, then look for a proof via counting cooled {0,1} rows
   (parity equidistribution from (α)?).

## Cautions

- CHT Remark 4.5 lives at entries ~2^n; nothing there settles o(n).
- The corridor only zeroes the cooled segment. Quantify T_cool for the
  geometric model (empirically ~15 rows at θ = 1 − 2/log 10⁸; it grows
  with the entry ceiling).
- Parity forcing changes values by ±1: check this does not itself
  reheat the array along the path (the corridor must survive its own
  construction — verify numerically before any claim).
- Claim discipline as always: PROVED / CERTIFIED / NUMERICAL /
  CONJECTURAL, and the novelty check against CHT §4 before writing.
