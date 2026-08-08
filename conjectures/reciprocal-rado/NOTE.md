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
f₂(3) = 40, f₂(5) = 80, f₂(7) = 150 — with excess over 3k² shrinking
(13, 5, 3), and map the uncovered k = 2^m family, which splits:
f₂(2) = 60 = 5·3k², while f₂(4) = 48 and f₂(8) = 192 equal 3k² exactly.
We conjecture f₂(k) = 3k² for all even k ≥ 4, identify the even-k parity
mechanism behind it, and record that the conjecture predicted the k = 8
value before its computation. We give the first values of the family at three colors,
f₃(2) = 3276 and f₃(3) = 585 — the known lower bounds 4^r/2 and
(2^r−1)k^r are off by factors of 102 and 3.1 — plus the verified bound
f₄(2) > 60000. Every UNSAT boundary carries a machine-checked DRUP
proof; every SAT boundary a witness coloring verified by two
independent checkers.

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
witness at f−1 is re-verified by per-class restricted enumeration
sharing no code with the encoder, implemented twice independently
(`verify_witness.py` and `check_class.c`). At k ≥ 7, where full
enumeration is infeasible, values come from a CEGAR loop whose UNSAT
verdicts are sound by construction (every clause is the support of an
exactly-verified solution; a subset of true constraints being UNSAT
implies the full encoding is) and whose SAT verdicts are accepted only
when the complete independent checker passes the model.

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

| k | f₂(k) | 3k² | Δ = f₂(k)−3k² | theorem context |
|---|---|---|---|---|
| 2 | **60** | 12 | +48 | k = 2^m: covered by neither GR theorem |
| 3 | **40** | 27 | +13 | odd prime power: GR bound 28; **not sharp** |
| 4 | **48** | 48 | 0 | k = 2^m: attains 3k² |
| 5 | **80** | 75 | +5 | odd prime power: GR bound 76; **not sharp** |
| 6 | **108** | 108 | 0 | GR theorem (k = 3·2^m): reproduced exactly |
| 7 | **150** | 147 | +3 | odd prime power: GR bound 148; **not sharp** |
| 8 | **192** | 192 | 0 | k = 2^m: attains 3k²; **predicted by Conjecture B before the run** |

(GR = Gaiser–Ramezanpour, arXiv:2607.04373, statements (secondary).)

Three observations the table forces:

1. **Sharpness fails at every odd prime power computed, but the excess
   shrinks**: Δ = 13, 5, 3 at k = 3, 5, 7. Whether Δ(k) → 1 (their bound
   eventually sharp), Δ(k) → some constant, or neither, is the sharpest
   question this data poses. Note (k−2)·Δ(k) = 15 at both k = 5 and 7 —
   a two-point coincidence, recorded as such (the k = 9 run tests it;
   prediction logged before the run: f₂(9) ∈ {245, 246}).
2. **The even column is exactly 3k² at k = 4, 6, 8** — the k = 8 value
   was stated by Conjecture B before its run and confirmed. Note 8 = 2³:
   within the 2^m family, 4 and 8 attain 3k² and only k = 2 escapes.
3. **k = 2 is a different animal**: f₂(2) = 60 = 5·3k². The k = 2
   solution set (the optic equation 1/x+1/y = 1/z) is divisor-sparse —
   supports {z, x, y} with x = z+d₁, y = z+d₂, d₁d₂ = z² — and the
   dyadic pairs {z, 2z} (from d₁ = d₂ = z) dominate the constraint
   graph. The 2^m family is not one family: 2 behaves like neither 4
   nor the odd primes.

**Conjecture B.** f₂(k) = 3k² for every even k ≥ 4.

Mechanism sketch supporting Conjecture B (not a proof): at n = 3k² the
diagonal solutions (k copies of ky, target y) give edges {y, ky} for
y ≤ 3k, whose chains {j, jk, jk²} (j ≤ 3) force χ(jk²) = χ(j) in any
valid 2-coloring; for **even** k there are additionally "half-diagonal"
solutions — k/2 copies each of a and b with 1/a + 1/b = 2/(ky),
parametrized by d₁d₂ = (ky/2)² exactly as in the optic equation, e.g.
support {y, 3ky/4, 3ky/2} whenever 4 | ky — which knit the chains
together. For odd k the half-diagonal family does not exist (k/2 is not
an integer — k cannot be split into two equal multiplicity blocks; the
nearest analogues have unequal weights and different, sparser
divisibility patterns), the constraint web at 3k² is strictly poorer, and
the computed colorings indeed survive to 3k²+Δ. The odd-k extremals
(§6) show exactly where the extra room lives.

## 5. Three and four colors

| r | k | f_r(k) | GR lower bound | ratio |
|---|---|---|---|---|
| 3 | 2 | **3276** | 4³/2 = 32 | 102× |
| 3 | 3 | **585** | (2³−1)·3³ = 189 | 3.1× |
| 4 | 2 | **> 60000** (verified witness) | 4⁴/2 = 128 | > 468× |

f₃(2) = 3276 = 2²·3²·7·13 and f₃(3) = 585 = 3²·5·13. The r-growth of
f_r(2) — 2 (trivial), 60, 3276, > 6·10⁴ — is far beyond the 4^r/2 bound;
the extremal 3-coloring of [1, 3275] satisfies χ(z) ≠ χ(2z) for **all**
1637 applicable pairs (the dyadic constraint is everywhere binding) while
being otherwise highly fragmented (1804 maximal runs; class sizes
1849/1032/394). A 4-color instance at n = 150000 (600000 variables, 1724780 clauses) was
still undecided by CaDiCaL at session close; the verified 60000-witness
stands as the honest bound.

## 6. Structure of the extremal colorings

The k = 4 witness at n = 47 and the k = 8 witness at n = 191 are exactly
the three-interval construction A = {1,2} ∪ [3k, 3k²−1], B = [3, 3k−1]
— at k = 8 with not a single deviation ([1..2]A [3..23]B [24..191]A). B
is solution-free because k terms from [3, 3k−1] sum to more than
k/(3k) ≥ 1/3 ≥ 1/y for y ≥ 3, and A because k·y-type diagonal solutions
need ky ≤ n. At odd k the optimum exceeds 3k² through sparse corrections
to this skeleton (at k = 5: B = [3,12] ∪ {14, 65, 75, 78} with 13 moved
to A; at k = 7: B = [3,16] ∪ {18, 20} ∪ {119, 133, 136, 147} with 17, 19
moved to A) whose exact-hit avoidance is delicate; no uniform
parametrization was found this session. The picture: **even k — the
interval skeleton is optimal; odd k — it is beatable by a shrinking
margin.**

## 7. Reproducibility

Environment: 4-core cloud sandbox, 15 GB RAM, Python 3.11.15, gcc 13.3.0,
python-sat 1.9.dev8 (bracketing via Cadical153), standalone Glucose 4.2.1
(built from the python-sat sdist's pristine bundled source; streams DRUP
to disk) and CaDiCaL 3.0.0 (f₄ bracketing). No randomness anywhere:
enumerators and encoders are deterministic; solvers run default
single-thread configurations. Certificates: every UNSAT boundary ships
`certs/*.drup` checked by `tools/satcert/rup_check`; sweep CNFs are
regenerated byte-identically by the deterministic encoder (sha256 in
`data/results.csv`); CEGAR CNFs are retained on disk (run-history-
dependent) with per-clause provenance in `certs/*.sols`. Every SAT
boundary ships a witness verified by two independent checkers (Python
and C, different code, cross-validated on eight witnesses and one
deliberately corrupted witness, where both find the identical violating
tuple 1/55+1/70+3/77 = 1/14). Headline runtimes: every f₂ value ≤ 30 s
of solver time; f₃(2) = 3276 total ~4 min including its 10 MB DRUP
proof; the f₂(7) certificate re-derives in ~40 s and its recorded run
reproduced byte-identically (equal CNF sha256) on a second execution.

```bash
gcc -O2 -o enum enum.c && gcc -O2 -o enumw enumw.c && \
gcc -O2 -o enum2 enum2.c && gcc -O2 -o check_class check_class.c
gcc -O2 -o ../../tools/satcert/rup_check ../../tools/satcert/rup_check.c
python3 sweep.py 3 3 900 --start=189      # f3(3) = 585, certified pair
python3 cegar.py 7 2 --certify-at=150     # re-derive + re-check f2(7)
python3 make_table.py                     # rebuild the authoritative table
```

## 8. Open questions

1. Exact f₂(p^m) at odd prime powers: the surpluses over 3k² computed
   here (13, 5, …) fit no law tried; is there a closed form?
2. Is f₂(k) = 3k² for all even k ≥ 4? (Their theorem: k = 3·2^m, m ≥ 1;
   certified here also at k = 4 and k = 8, the latter predicted before
   its run.) Proving the upper bound via the half-diagonal web of §4 is
   the natural attack.
3. Growth of f_r(2): 60, 3276, … — is a closed form or even the right
   growth rate (in r) accessible? The dyadic pair constraints {z, 2z}
   alone force alternation on dyadic chains; the interaction with
   3-support solutions is where the truth lives.
4. OEIS: no sequence for this family exists by search (secondary);
   submission candidate once the paper table is readable.
