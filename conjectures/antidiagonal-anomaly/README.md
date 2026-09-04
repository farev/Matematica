# Antidiagonal traffic anomaly (Gil–Liang–Odetola–Weiner, 2026)

Count the monotone lattice paths from (0,0) to (n,n) that avoid a forbidden point B, and
ask which point A of the grid the most B-avoiding paths pass through. Gil, Liang, Odetola
and Weiner (arXiv:2609.01562, 1 Sep 2026) prove that for n ≥ 9 the answer is always one
of ten points hugging the two corners, but notice an *anomaly*: when B = (a, n−a) lies on
the antidiagonal, the winner can move from the near-corner point (1,1) to the boundary
point (1,0). This happens for every 8 ≤ n ≤ 375, then sporadically up to n = 495, and
they conjecture it never happens again for n ≥ 496. The criterion is an explicit ratio
ρ(n) of binomial coefficients exceeding 1, so the conjecture is a concrete inequality —
provable by Stirling-type bounds for large n and checkable exactly below that.

Write-up page: <https://fabianarevalo.com/antidiagonal-anomaly> (pending; see `PAGE.md`).

**Status:** closed (the conjecture is settled; two refinements listed as open threads)
**Sessions:** 2026-09-04

## Results

| Claim | Label | Where |
|---|---|---|
| ρ(n) < 0.9939 for every n ≥ 3000 and every obstruction (a, n−a), via Robbins–Stirling bounds (analytic; the final numeric step certified in rational arithmetic) | PROVED | NOTE §3, Theorem A; `check_bound.py` |
| ρ(n) < 1 for every 496 ≤ n ≤ 2999 (exact integer arithmetic, certificate shipped; the largest value is ρ(497) = 0.99995528…) | CERTIFIED | NOTE §4; `verify_anomaly.py`, `certificate_3_3000.csv` |
| **The conjecture of [GLOW, §7]: the antidiagonal anomaly never occurs for n ≥ 496** (Theorem A + the finite check) | PROVED (computer-assisted on 496 ≤ n ≤ 2999) | NOTE §4, Theorem A′ |
| The criterion is the integer inequality a(n−2a+1)·C(n,a)² > (n−1)·C(2n−2,n−1), i.e. the obstruction deficit exceeds the Catalan number Cat(n−1) | PROVED | NOTE §1, Lemma 1 |
| ρ(n) → c₀ = √(8/π)·e^{−1/2} = 0.967882…, and ρ(n) = c₀(1 + 1/√(2n) + O(1/n)) | PROVED | NOTE §5, Theorem B |
| R_n(a) is log-concave in a; explicit ratio; the maximiser is within 1 of n/2 − (√(2n+1) − 1)/4 for 3 ≤ n ≤ 3000 | PROVED (log-concavity) / CERTIFIED (maximiser location) | NOTE §6, Proposition C; `certificate_3_3000.csv` |
| The sporadic pattern on 376 ≤ n ≤ 495 (82 anomalous n: 377, 379–422, even 424–462, 464, odd 465–495) is the rounding of the real maximiser to an integer, alternating with the parity of n | CERTIFIED (the list and every ρ(n)) / NUMERICAL (the rounding-penalty model) | NOTE §6; `transition_table.py` |
| [GLOW, Proposition 7.2] and their ten-point theorem re-checked from the definition at every antidiagonal B for 9 ≤ n ≤ 120 (all grid points scanned; 0 mismatches) | CERTIFIED | `allpoints_control.py`, `results_allpoints_control_120.txt` |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `verify_anomaly.py N1 N2 [cert.csv]` | exact integer evaluation of the criterion for all n in [N1, N2], all 1 ≤ a ≤ n/2; writes the per-n certificate | 12 s for [3, 3000], one core, no dependencies | anomalous n = [3, 375] ∪ 82 sporadic values ≤ 495; none in [496, 3000] |
| `check_bound.py` | certifies U(3000) < 0.9939 (Theorem A's numeric step) using Fractions only: Machin bracketing for π, Taylor sum for e, rational square-root and e^y ≤ 1/(1−y) bounds | < 1 s | `ALL CERTIFIED`, U(3000) ≤ 0.993849 |
| `allpoints_control.py N` | for 9 ≤ n ≤ N and every antidiagonal B, computes f_B at *all* grid points; checks the argmax is among the ten points and that (1,0) beats (1,1) iff the integer criterion holds | 50 s for N = 120 | 0 mismatches |
| `transition_table.py [N1 N2] [out]` | table of n, integer maximiser a_n, real maximiser x*, rounding offset δ_n, ⌊10⁹ρ(n)⌋, anomaly flag | 1 s | `transition_table.csv` |

Run from inside this directory:

```bash
cd conjectures/antidiagonal-anomaly && python3 verify_anomaly.py 3 3000 certificate_3_3000.csv
python3 check_bound.py && python3 allpoints_control.py 120 && python3 transition_table.py
```

Python 3.11, standard library only.

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `certificate_3_3000.csv` | `verify_anomaly.py 3 3000` | per n: maximising a, number of a with R_n(a) > 1, ⌊10⁹·ρ(n)⌋ (all exact integers) |
| `results_verify_3_3000.txt` | same | the run summary (anomalous runs, largest ratio, elapsed) |
| `results_check_bound.txt` | `check_bound.py` | the certified inequality chain for U(3000) |
| `results_allpoints_control_120.txt` | `allpoints_control.py 120` | the control's verdict |
| `transition_table.csv` | `transition_table.py` | the §6 table for 370 ≤ n ≤ 500 |

## Known defects and open threads

- The proof is computer-assisted on 496 ≤ n ≤ 2999: an exact finite computation
  (12 s, reproducible) closes the gap between the conjectured threshold 496 and the
  analytic threshold 3000. Lowering the analytic threshold to 496 would need bounds
  sharp to 5·10⁻⁵ at n = 497 (ρ(497) = 0.999955), which Stirling-type estimates do not
  give without the same kind of finite computation.
- Theorem B's O(1/n) term is not made explicit. An explicit lower bound
  ρ(n) ≥ c₀(1 + 1/√(2n) − C/n) would turn the §6 explanation of the sporadic pattern
  from a model into a theorem describing the exact anomalous set.
- The ten-point theorem and Proposition 7.2 of [GLOW] are used as published (and
  re-checked here only for n ≤ 120); Theorem A′'s "consequently" depends on them.
- The Robbins bounds are cited, not re-derived.

## Prior work

- J. Gil, Z. Liang, A. Odetola, M. Weiner, *Points of maximal traffic on a grid with
  obstruction*, arXiv:2609.01562 (1 Sep 2026): the problem, the ten-point theorem,
  Proposition 7.2, the data to n = 495 and the conjecture proved here. Read in full on
  2026-09-04; no later version and no citing paper existed on that date.
- H. Robbins, *A remark on Stirling's formula*, Amer. Math. Monthly 62 (1955) 26–29
  (bounds quoted from Feller vol. I — secondary).
- No earlier analysis of the ratio ρ(n) was found (arXiv full-text and web search on
  the paper's terms, 2026-09-04).
