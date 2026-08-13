# OEIS submission draft: Liouville sign-pattern coverage numbers

**Status: draft, not submitted. Terms k = 1..24 certified (Run A,
exhaustive scan of n ≤ 10^9); k = 25..27 certified by the extension run
(exhaustive to 6·10^9); k = 28..30 by a further exhaustive scan to
2.23·10^10 with completing positions independently recomputed.**

## Proposed sequence: a(k) = least x such that every ±1 pattern of length k
occurs as (λ(n), λ(n+1), …, λ(n+k−1)) for some n ≤ x, where λ is the
Liouville function (A008836)

```
2, 9, 14, 33, 122, 347, 571, 1141, 2659, 6277, 15848, 47815, 69395,
142848, 336841, 757959, 1644906, 4114874, 6736484, 16599609, 30787956,
59092365, 128387085, 293427643, 722808938, 1312765349, 2794709788,
5542425842, 11647289153, 22249147014
```

(30 terms.)

**Name.** Least m such that every sign pattern of length n occurs in the
Liouville function lambda at some starting point <= m.

**Comments.**
- a(n) exists for all n if and only if every ±1 pattern occurs in λ, which
  is implied by (and much weaker than) Chowla's conjecture; occurrence of
  all patterns is proved only for lengths <= 3 with positive density
  (Matomäki–Radziwiłł–Tao 2015). The listed terms certify occurrence for
  all lengths <= 30 by exhibition.
- The uniform coupon-collector model predicts a(n) ≈ 2^n (n log 2 + γ);
  the ratio a(n)/[2^n(n log 2 + γ)] has mean 1.008 for 10 <= n <= 30 with
  scatter (sd 0.12) consistent with the model's own Gumbel fluctuation
  (e.g. n = 24: ratio 1.016), quantifying the fair-coin behavior of
  λ-sign windows in an extreme statistic.
- Computed by an exact integer segmented sieve with first-occurrence
  indices retained for every pattern; data and code:
  conjectures/chowla/ in the Matematica repository (fineA_firstocc.npz).

**Crossrefs.** A008836 (λ), A090410 (L(10^n)), A028488 (n with L(n) = 0).

**Keywords.** nonn,hard,more

**Author.** Fabian Arevalo, Jul 29 2026. (AI-assisted computation,
disclosed.)

## Possible companion sequence (not yet drafted in full)

b(n) = first occurrence index of the all-minus pattern of length n
(runs of consecutive λ = −1), and the analogous all-plus sequence.
NOTE (checked 2026-07-29): A395823 / A395824 already record run-length
records for odd/even Ω; the run companions are likely redundant with
those and should not be submitted without a careful diff; the coverage
sequence a(k) above has no OEIS overlap.
