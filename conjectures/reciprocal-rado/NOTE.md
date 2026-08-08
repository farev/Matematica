# Certified reciprocal Rado numbers, the failure of sharpness at odd prime powers, and the first multi-color values

*Session note, 2026-08-08. AI-assisted (Claude); all computational claims
ship certificates reproducible from this directory. Statements about the
contents of arXiv:2306.04029 and arXiv:2607.04373 are from abstract-level
snippets — the PDFs were unreachable from this sandbox — and are marked
(secondary) where not independently reproduced here.*

## Abstract

The reciprocal Rado number f_r(k) is the least n such that every
r-coloring of {1,…,n} contains a monochromatic solution of
1/x₁ + ⋯ + 1/x_k = 1/x_{k+1} (repeats allowed). Gaiser–Ramezanpour
(July 2026) proved f₂(3·2^m) = 3k² for m ≥ 1 and f₂(p^m) ≥ 3k²+1 for odd
prime powers, leaving sharpness open. We compute certified exact values
settling sharpness negatively at every odd prime power in reach —
f₂(3) = 40, f₂(5) = 80, f₂(7) = (…) — each strictly and irregularly above
3k²+1, and map the uncovered k = 2^m family: f₂(2) = 60 (far above 3k²),
f₂(4) = 48 = 3k² exactly. We give the first values of the family at three
colors, f₃(2) = 3276 and f₃(3) = 585, showing the known lower bounds
(2^r−1)k^r and 4^r/2 are off by two orders of magnitude at k = 2, and (…
f₄(2) outcome …). Every UNSAT boundary carries a machine-checked DRUP
proof; every SAT boundary a machine-verified witness coloring.

## 1. Definitions and conventions

f_r(k): least n such that every function χ : {1,…,n} → {0,…,r−1} admits
x₁, …, x_k, y ∈ [1,n], monochromatic under χ, with Σᵢ 1/xᵢ = 1/y. The xᵢ
need not be distinct. Positivity forces y < xᵢ for all i, so a solution's
support set {y, x₁, …, x_k} has between 2 and k+1 elements, and the
integer 1 can appear in a solution only as y (then Σ 1/xᵢ = 1 is an
Egyptian representation of 1 by k unit fractions).

Monotonicity: a valid coloring of [1,n] restricts to [1,n′] for n′ < n,
so {n : valid coloring exists} is an initial segment; f_r(k) is exactly
the first n with no valid coloring. All boundary claims below certify the
pair (SAT at f−1, UNSAT at f).

## 2. Methodology

Solutions are enumerated by exact integer arithmetic (64-bit with
128-bit intermediate products, overflow-checked) via the standard
bounded Egyptian-fraction DFS; for k = 2 an independent divisor-form
enumerator (x = z+d₁, y = z+d₂, d₁d₂ = z², d₁ ≤ z, via an SPF sieve)
cross-checks it. CNF: for each integer an at-least-one-color clause; for
each solution support set S and color c, the clause ⋁_{v∈S} ¬(v has
color c). No at-most-one clauses are needed: any satisfying assignment
projects to a valid coloring. Bracketing uses CaDiCaL 3.0.0 without
proofs; the claimed value rests only on the boundary pair — Glucose 4.2.1
(pure-RUP DRUP output, streamed to disk) proves UNSAT at f, checked by
the independent forward-RUP checker `tools/satcert/rup_check`; the SAT
witness at f−1 is re-verified by `verify_witness.py`, a per-class
restricted enumeration sharing no code with the encoder.

## 3. Controls

1. Enumerator vs OEIS A002966 (Egyptian representations of 1 by k unit
   fractions): counts 1, 3, 14, 147 reproduced for k = 2,3,4,5.
2. C DFS ≡ Python DFS ≡ brute force (Fraction arithmetic over all
   multisets) on a grid of small (k, n); C DFS ≡ divisor enumerator for
   k = 2 at n = 60, 500, 3276.
3. Theorem anchors (Gaiser–Ramezanpour): f₂(6) = 108 = 3·6² reproduced
   exactly (their 3·2^m theorem at m = 1); SAT witnesses exist at
   n = 3k² for k = 3, 5, 7 (their odd-prime-power lower bound requires
   exactly this).
4. Certificate integrity: every DRUP proof re-checked by `rup_check`
   (validated 08-05 against injected non-RUP and truncated proofs);
   every witness re-verified; a deliberately corrupted witness is
   rejected (§7).

## 4. The two-color ladder

(table and discussion at close of session)

## 5. Three and four colors

(f₃(2) = 3276, f₃(3) = 585, further values and the f₄(2) outcome)

## 6. Structure of the extremal colorings

The k = 4 witness at n = 47 is exactly the three-interval construction
A = {1,2} ∪ [3k, 3k²−1], B = [3, 3k−1]: B is solution-free because k
terms from [3, 3k−1] sum to more than k/(3k) ≥ 1/3 ≥ 1/y for y ≥ 3, and
A because k·y-type diagonal solutions need ky ≤ n. At odd k the optimum
exceeds 3k² through sparse corrections to this skeleton (at k = 5:
B = [3,12] ∪ {14, 65, 75, 78} with 13 moved to A) whose exact-hit
avoidance is delicate; no uniform parametrization was found this session.

## 7. Reproducibility

(commands, runtimes, environment at close)

## 8. Open questions

1. Exact f₂(p^m) at odd prime powers: the surpluses over 3k² computed
   here (13, 5, …) fit no law tried; is there a closed form?
2. Is f₂(k) = 3k² for all even k ≥ 4? (Their theorem: k = 3·2^m, m ≥ 1;
   here also k = 4, (8?).)
3. Growth of f_r(2): 60, 3276, … — is a closed form or even the right
   growth rate (in r) accessible? The dyadic pair constraints {z, 2z}
   alone force alternation on dyadic chains; the interaction with
   3-support solutions is where the truth lives.
4. OEIS: no sequence for this family exists by search (secondary);
   submission candidate once the paper table is readable.
