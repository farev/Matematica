# PAGE handoff — antidiagonal-anomaly (new page)

1. **Headline claim.** The conjecture of Gil–Liang–Odetola–Weiner (arXiv:2609.01562, §7)
   is true: for every n ≥ 496, an obstruction on the antidiagonal of the n×n path grid
   never moves the point of maximal traffic from (1,1) to the boundary point (1,0).
   **PROVED** (analytic for n ≥ 3000; exact integer computation for 496 ≤ n ≤ 2999 with a
   committed certificate).

2. **Contributions.**
   1. PROVED — the anomaly criterion R_n(a) > 1 of [GLOW, Prop. 7.2] is the integer
      inequality a(n−2a+1)·C(n,a)² > (n−1)·C(2n−2,n−1): the obstruction's deficit
      exceeds the Catalan number Cat(n−1). (NOTE Lemma 1.)
   2. PROVED — ρ(n) = max_a R_n(a) < 0.9939 for all n ≥ 3000 (Robbins–Stirling bounds;
      the final numeric inequality certified in rational arithmetic, `check_bound.py`).
      (NOTE Theorem A.)
   3. CERTIFIED — ρ(n) < 1 for every 496 ≤ n ≤ 2999 (12 s, exact integers; the largest
      value is ρ(497) = 0.99995528…). Together with 2: the conjecture, PROVED. (NOTE
      Theorem A′.)
   4. PROVED — ρ(n) → c₀ = √(8/π)·e^{−1/2} = 0.967882…, with
      ρ(n) = c₀(1 + 1/√(2n) + O(1/n)); the envelope crosses 1 at n ≈ 454. (NOTE Theorem B.)
   5. PROVED — R_n(a) is log-concave in a with an explicit consecutive ratio; CERTIFIED —
      the integer maximiser is within 1 of n/2 − (√(2n+1) − 1)/4 for all 3 ≤ n ≤ 3000.
      (NOTE Proposition C.)
   6. CERTIFIED — the exact anomalous set below 496: every 3 ≤ n ≤ 375 and the 82 values
      377, 379–422, even 424–462, 464, odd 465–495 (455 in all; the paper printed only
      "intermittently up to 495"); NUMERICAL — the rounding-penalty model explaining the
      parity alternation. (NOTE §6.)
   7. CERTIFIED — control: the paper's reduction re-derived from the definition of
      traffic at every grid point for all antidiagonal obstructions, 9 ≤ n ≤ 120,
      0 mismatches.

3. **Figure specs.**
   - *Figure 1 — ρ(n) through the transition.* Data: `transition_table.csv`, columns
     n and floor_1e9_rho/10⁹ for 370 ≤ n ≤ 500, points coloured by parity of n, with the
     horizontal line ρ = 1 and the envelope c₀(1 + 1/√(2n)) as a dashed curve. Sentence:
     "The ratio hugs a smooth curve that dips below 1 near n = 454; whether a given n is
     anomalous depends on how well an integer can approximate the real optimum, and the
     even and odd n take turns being the lucky ones."
   - *Figure 2 — the rounding mechanism.* Data: `transition_table.csv`, columns n,
     delta_n (rounding offset) and anomaly flag for 420 ≤ n ≤ 496. Sentence: "The
     anomaly survives exactly when the rounding offset is small."
   - *Figure 3 (optional) — the long view.* Data: `certificate_3_3000.csv`, column
     floor_1e9_rho/10⁹ against n on a log-x axis for 8 ≤ n ≤ 3000 with the limit c₀.
     Sentence: "After 495 the ratio never returns to 1; it settles towards 0.968."

4. **Caveats the page must carry.**
   - The proof is computer-assisted on 496 ≤ n ≤ 2999 (exact integer arithmetic, 12 s,
     certificate committed); the analytic bound alone starts at n = 3000.
   - The "no anomaly" statement rests on the paper's own ten-point theorem and
     Proposition 7.2, used as published and re-checked from the definition only for
     n ≤ 120.
   - Robbins' Stirling bounds are cited (via Feller, secondary), not re-derived.
   - The rounding-penalty explanation of the sporadic pattern is a model (NUMERICAL);
     the anomalous list and all ρ(n) values are exact.
   - Theorem B's O(1/n) is not explicit.
   - The source paper is three days old (v1, 1 Sep 2026); no later version or citing
     work existed on 2026-09-04. The result answers questions (1) and (2) of its §7;
     question (3), about the bound n ≥ 9 in the ten-point theorem, is not addressed.

5. **Existing page:** none. New page.
