# PAGE.md — handoff for the reciprocal-rado write-up page (new page)

## 1. Headline claim

**CERTIFIED.** The first certified table of reciprocal Rado numbers: nine
exact values of f_r(k) — the least n such that every r-coloring of
{1,…,n} has a monochromatic solution of 1/x₁+⋯+1/x_k = 1/x_{k+1} —
including f₂(7) = 150, f₃(2) = 3276 and f₃(3) = 585, showing that the
sharp lower bound 3k²+1 of Gaiser–Ramezanpour (arXiv:2607.04373, July
2026) is **not attained at any computed odd prime power, with excess
shrinking 13, 5, 3 at k = 3, 5, 7**.

## 2. Contributions

1. **CERTIFIED** — the two-color ladder: f₂(2)=60, f₂(3)=40, f₂(4)=48,
   f₂(5)=80, f₂(6)=108, f₂(7)=150, f₂(8)=192. Each value = DRUP proof of
   UNSAT at f (checked by an independent RUP checker) + witness coloring
   at f−1 (verified by two independent checkers, Python and C).
2. **CERTIFIED** — sharpness of f₂(p^m) ≥ 3k²+1 fails at k = 3, 5, 7
   (excesses +13, +5, +3), while the theorem-anchored controls
   reproduce: f₂(6) = 108 = 3·6² exactly as their 3·2^m theorem states,
   and SAT witnesses exist at 3k² for k = 3, 5, 7 as their bound
   requires. k=9 was in flight at session close (prediction logged
   before the run: 245–246).
3. **CERTIFIED** — first multi-color values: f₃(2) = 3276 (their bound:
   32 — off by 102×), f₃(3) = 585 (bound 189), and f₄(2) > 60000
   (verified 4-coloring witness; the n=150000 instance was still in the
   solver at close).
4. **Conjecture B** (new): f₂(k) = 3k² for every even k ≥ 4 — attained
   at k = 4 and 6, and then **f₂(8) = 192 = 3k², stated before the k=8
   run and confirmed by it**. Mechanism: for even k, "half-diagonal"
   solutions k/2·(1/a + 1/b) = 1/y, parametrized by d₁d₂ = (ky/2)²,
   knit the diagonal chains {j, jk, jk²} into a rigid web at n = 3k²;
   for odd k this family does not exist. Within k = 2^m, only k = 2
   escapes (f₂(2) = 60 = 5·3k²).
5. Structure of the extremal colorings: odd-k optima are an interval
   core plus sparse high corrections (displayed for k = 5, 7); the
   f₃(2) extremal 3-coloring of [1, 3275] has χ(z) ≠ χ(2z) at all 1637
   applicable pairs.

## 3. Figure specs

- **Fig 1 — the Δ column.** Data: `data/values.csv` (columns k, f, and
  3k²). Bar or lollipop of Δ = f₂(k) − 3k² for k = 2..7 (values +48,
  +13, 0, +5, 0, +3), with the odd prime powers highlighted. Sentence a
  reader should say: "the excess over 3k² is zero exactly at even k ≥ 4
  and shrinks along the odd primes 13 → 5 → 3."
- **Fig 2 — the k = 7 extremal coloring.** Data:
  `certs/f2_7_n149.witness` (149 colors). A 1×149 color strip annotated
  with the blocks [3..16]∪{18,20} and the sparse points {119,133,136,147}.
  Sentence: "the optimum is an interval construction plus a handful of
  surgical corrections."
- **Fig 3 — f₃(2)'s dyadic rigidity.** Data: `certs/f3_2_n3275.witness`.
  A strip (or z vs χ scatter for z ≤ 200) with pairs (z, 2z) linked.
  Sentence: "in the extremal 3-coloring, z and 2z never share a color —
  all 1637 pairs."

## 4. Caveats the page must carry

- Every statement about the contents of arXiv:2306.04029 and
  arXiv:2607.04373 is from abstract-level snippets (the PDFs are
  egress-blocked in the session sandbox) and is (secondary); the
  theorems used as controls were reproduced computationally, which is
  the strongest verification available in-sandbox.
- The Gaiser–Ramezanpour paper reports its own computational table,
  which could not be read. Small-k values here (certainly f₂(3), likely
  more of the f₂ ladder and possibly f₃ values) may reproduce entries
  of that table; the page must say so. The certificates are new
  regardless (no certificates are reported there (secondary)); the
  k = 7 value, the f₄ bound, and the structural/conjectural material
  are claimed as new with that hedge.
- Δ-pattern remarks ((k−2)Δ(k) = 15 at k = 5, 7) are two-point
  observations, not fits or laws.
- "First certified table / first multi-color values" is subject to the
  unread-table hedge above; no OEIS sequence exists for the family
  (search-based absence, (secondary)).

## 5. Existing page

None — this is a new conjecture directory and a new page.
