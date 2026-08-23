# Odd Giuga numbers and odd primary pseudoperfect numbers: certified factor-count bounds

**Session:** 2026-08-23. **Status of this note:** working research note;
labels per repository convention (PROVED / CERTIFIED / NUMERICAL).

## Abstract

A Giuga number is a composite `n` such that `p | (n/p − 1)` for every prime
`p | n`; a primary pseudoperfect number (PPN) is an `n > 1` with
`1/n + Σ_{p|n} 1/p = 1`. All thirteen known Giuga numbers and all ten known
PPNs are even; whether odd ones exist is open, and any counterexample to
Giuga's 1950 primality conjecture must be an odd Giuga number. The recorded
lower bound on the number of prime factors of an odd Giuga number is 14
(secondary: attributed to Borwein–Borwein–Borwein–Girgensohn 1996); for odd
PPNs nothing beyond the trivial consequence of Butske–Jaje–Mayernik's
complete census (no odd PPN with ≤ 8 prime factors) appears to be recorded.

We prove that the odd members of both families with `m` prime factors are
exactly the odd-prime solution sets of `Σ 1/p_i + ε/(p_1⋯p_m) = 1`
(`ε = −1` Giuga, `ε = +1` PPN) once `m ≤ 1411`, that `m` must be even, and
we exhaust these equations by a certified exact branch-and-bound. Every
claim below states its label; the headline computational results are in
`README.md` and the run records in `results/`.

## 1. Setup and classification

Throughout, `p_1 < p_2 < ⋯ < p_m` are distinct primes, `n = p_1⋯p_m`,
`A = Σ_i n/p_i`, and for `ε ∈ {−1, +1}` we study

    E_ε :  1/p_1 + ⋯ + 1/p_m + ε/n = 1 .

**Lemma 1 (integer form). PROVED.** The set `{p_1,…,p_m}` solves `E_ε` iff
`A + ε = n`.

*Proof.* Multiply `E_ε` by `n`. ∎

**Lemma 2 (Giuga classification). PROVED.** For composite squarefree `n`:
`p | (n/p − 1)` for every prime `p | n` iff `T(n) := Σ_{p|n} 1/p − 1/n`
is a positive integer; and a Giuga number is automatically squarefree.
Moreover the solutions of `E_{−1}` in distinct primes with `m ≥ 2` are
exactly the Giuga numbers with `T(n) = 1`.

*Proof.* Squarefreeness: if `p² | n` and `p | (n/p − 1)` then `p | n/p`
and `p | n/p − 1`, impossible. For squarefree `n`, `T(n) = (A − 1)/n`.
Modulo any `p_j`, every term `n/p_i` with `i ≠ j` is divisible by `p_j`,
so `A − 1 ≡ n/p_j − 1 (mod p_j)`. Hence `n | A − 1` iff `p_j | (n/p_j − 1)`
for all `j` (CRT, `n` squarefree). Positivity: `A − 1 ≥ 0` always, and
`A = 1` forces `m = 1`, excluded by compositeness; so `T ∈ ℤ` implies
`T ≥ 1`. Finally `T = 1` iff `A − 1 = n` iff `E_{−1}` holds. ∎

**Lemma 3 (PPN classification). PROVED.** An integer `n > 1` with
`1/n + Σ_{p|n} 1/p = 1` is squarefree, and the solutions of `E_{+1}` in
distinct primes are exactly the PPNs. Every such `n` satisfies
`p | (n/p + 1)` for all prime `p | n` (the all-prime, possibly improper,
Znám condition).

*Proof.* If `p^a ‖ n` with `a ≥ 2`, multiply the equation by `n`:
`1 + Σ_p n/p = n`. Each `n/q` for `q ≠ p` is divisible by `p^a`, and
`n/p` by `p^{a−1} ≥ p`, so the left side is `≡ 1 (mod p)` while the right
is `≡ 0`, a contradiction. For squarefree `n` the equation is `A + 1 = n`,
i.e. `E_{+1}`. Reducing `A + 1 = n` mod `p_j` gives
`p_j | (n/p_j + 1)`. ∎

**Lemma 4 (only the first integer class matters here). PROVED, constants
CERTIFIED.** Let `S_odd(m)` be the sum of the reciprocals of the `m`
smallest odd primes. Then `S_odd(m) ≤ S_odd(1411) < 2`, with the partial
sums first exceeding 2 at `m = 1412` (exact rational computation,
`lemmas.py`). Consequently, for sets of at most 1411 **odd** primes:

- Giuga side: `T = Σ 1/p_i − 1/n = k ≥ 2` needs
  `Σ 1/p_i = k + 1/n > 2 > S_odd(m)`, impossible. So an odd Giuga number
  with `m ≤ 1411` has `T = 1`, i.e. solves `E_{−1}`.
- PPN side: `Σ 1/p_i + 1/n = k ≥ 2` needs `Σ 1/p_i = k − 1/n ≥ 2 − 1/n`
  with `n ≥ 3^m`, so it needs `S_odd(m) ≥ 2 − 3^{−m}`; `lemmas.py`
  certifies `S_odd(m) < 2 − 3^{−m}` for every `m ≤ 1411` by exact
  rational comparison. So an odd PPN-type set with `m ≤ 1411` solves
  `E_{+1}`.

The all-primes analogue: the partial sums of `Σ 1/p` over the smallest
primes (2 included) first exceed 2 at `m = 59` — reproducing exactly the
classical "at least 59 prime factors for `sum − prod ≥ 2`" constant
(secondary: MathWorld) from scratch.

**Lemma 5 (parity). PROVED.** If all `p_i` are odd and `{p_1,…,p_m}`
solves `E_ε`, then `m` is even.

*Proof.* Each `n/p_i` is a product of `m − 1` odd primes, hence odd, so
`A ≡ m (mod 2)`. By Lemma 1, `A = n − ε` with `n` odd and `ε = ±1`, so `A`
is even. ∎

**Lemma 6 (analytic floor). PROVED, constant CERTIFIED.**
`S_odd(8) < 1 < S_odd(9)` (exact rationals in `lemmas.py`). Hence an odd
solution of `E_{−1}` has `m ≥ 9` — reproducing the classical "an odd Giuga
number has at least 9 prime factors" — and so does an odd solution of
`E_{+1}`: it needs `Σ 1/p_i = 1 − 1/n` with `n = p_1⋯p_m ≥ 3·5⋯`, and for
`m ≤ 8`, `1 − S_odd(8) > 1/n` fails only if `n ≤ 1/(1 − S_odd(8)) < 877`,
while already `n ≥ 3·5·7·11·13·17·19·23 > 10^8`. With Lemma 5, `m ≥ 10`
in both families.

**Lemma 7 (Giuga's conjecture connection). PROVED.** A composite `n`
satisfies Giuga's congruence `Σ_{k=1}^{n−1} k^{n−1} ≡ −1 (mod n)` iff `n`
is squarefree and, for every prime `p | n`, both `p | (n/p − 1)` and
`(p−1) | (n/p − 1)`. Such `n` is odd, and is in particular a Giuga number;
so every lower bound proved here for odd Giuga numbers applies to
counterexamples to Giuga's conjecture (the dedicated record for those is
far stronger: ≥ 4771 prime factors, secondary: Borwein–Maitland–Skerritt
2013).

*Proof.* Fix `p^a ‖ n`. Group `k ∈ {1,…,n−1}` by residue mod `p`: the
multiples of `p` contribute `0 (mod p)`, each nonzero residue class has
exactly `n/p` members, so `Σ k^{n−1} ≡ (n/p)·Σ_{r=1}^{p−1} r^{n−1}
(mod p)`. The inner sum is `−1 (mod p)` if `(p−1) | (n−1)` and `0`
otherwise (cyclic group `F_p^×`). So the congruence mod `p` forces
`(p−1) | (n−1)` and `n/p ≡ 1 (mod p)`; the latter gives `p ∤ n/p`, i.e.
squarefreeness, and then the two mod-`p` conditions for all `p` are also
sufficient by CRT since `−1` is the claimed value mod each prime divisor.
The identity `n − 1 = (p−1)(n/p) + (n/p − 1)` converts
`(p−1) | (n−1)` into `(p−1) | (n/p − 1)`. Oddness: if `n` were even with
an odd prime divisor `p`, then `(p−1) | (n−1)` fails as `n−1` is odd and
`p−1` even; `n = 2` is prime and `n = 2^a` is not squarefree for `a ≥ 2`;
`n = 2p` fails `p | (n/p − 1) = 1`. ∎

## 2. The search tree (engine soundness)

`search.py` enumerates solution sets of `E_ε` with `m` primes (all-primes
mode or odd-only mode) by choosing `p_1 < p_2 < ⋯` left to right.
State: `P = p_1⋯p_j`, `A = Σ_{i≤j} P/p_i` (so the running sum is `A/P`),
`D = P − A`.

**Lemma 8 (internal-node invariant). PROVED.** At any proper prefix of a
solution, `0 < A < P`, i.e. `D ≥ 1`.

*Proof.* The completed sum satisfies `Σ_all = 1 − ε/n < 1 + 1/n`. A prefix
sum `A/P ≥ 1` would need the remaining primes to contribute
`1 − ε/n − A/P ≤ 1/n − (A/P − 1)`. If `A/P = 1` this is `≤ 1/n`, but the
next reciprocal alone is `1/q > 1/n`. If `A/P > 1` then `A ≥ P + 1` and
the remainder is negative while all future terms are positive. ∎

**Lemma 9 (windows, t ≥ 3 primes remaining). PROVED.** Let `d = D/P` be
the deficit, `t ≥ 3` the number of primes still to choose, `p` the next
prime. Any completion satisfies

  (i)  `1/p < d + 1/(3P)`  — since the total future contribution is
       `d − ε/n` and `1/n < 1/(3P)`;
  (ii) `t/p > d − 1/(3P)` — since the `t` remaining reciprocals are
       distinct and all `≤ 1/p`, their sum is `< t/p`, and it must reach
       `d − ε/n > d − 1/(3P)`;
  (iii) for `ε = +1`: `1/p < d` exactly (future sum is `d − 1/n < d`);
  (iv) for `ε = −1`: `t/p > d` exactly (future sum is `d + 1/n > d`).

The implemented integer bounds `3P/(3D+1) < p` and `p ≤ 3Pt/(3D−1)` (and
the mode-specific `P/D < p`, `p ≤ tP/D`, each padded by one) are supersets
of (i)–(iv), so no feasible `p` is excluded.

**Lemma 10 (closure with two primes left). PROVED.** With prefix `(P, A)`,
`D = P − A ≥ 1`, the final two primes `q < r` satisfy

    (Dq − P)(Dr − P) = P² + εD =: N*,

`u := Dq − P ≥ 1`, `r = (Pq + ε)/u`, and `P/D < q ≤ (P + √N*)/D`.
Moreover `gcd(u, D) = 1`, and consequently `u | (Pq + ε)` **iff**
`u | N*`.

*Proof.* Clearing denominators in `A/P + 1/q + 1/r + ε/(Pqr) = 1` gives
`Dqr − Pq − Pr = ε`; multiply by `D` and factor. `u ≤ √N*` is `q ≤ r`.
`u > 0`: if both factors were negative then `q, r < P/D`, so
`1/q + 1/r > 2D/P > D/P + ε/(Pqr)`, contradicting the cleared equation
read as `1/q + 1/r = D/P + ε/(Pqr)`. For the gcd: `gcd(u, D) | P` (from
`u = Dq − P`) and any common prime of `P` and `D = P − A` divides
`A = Σ_i P/p_i ≡ Π_{j≠i} p_j (mod p_i)`, which is nonzero mod `p_i` as
the `p_j` are distinct primes. Finally `D(Pq + ε) = P·u + N*`, so
`u | D(Pq+ε)` always; with `gcd(u, D) = 1` the two divisibilities are
equivalent. ∎

**Lemma 11 (last prime). PROVED.** With one prime left,
`p_m = (P + ε)/D` exactly (integrality, primality, `p_m >` previous prime
and parity are then checked; the completed set is finally verified by the
integer identity `A_final + ε = n` recomputed from scratch).

**Lemma 12 (probable-prime one-sidedness). PROVED.** The engine's
primality tests (GMP `mpz_probab_prime_p`: trial division + Miller–Rabin)
can err only by declaring a composite "probably prime", never by declaring
a prime composite. Pruning a branch on a *composite* verdict is therefore
always sound, and an erroneous "prime" verdict can only create a spurious
candidate solution, which the final identity of Lemma 11 together with the
independent verifier (`verify_solution.py`, deterministic primality for
the ranges involved) would expose. The same one-sidedness applies to
`next_prime` (it never skips a true prime). The single place where a
pseudoprime could threaten *completeness* — treating a composite as prime
inside a factorization used for divisor enumeration — is guarded
separately: factors are re-verified and any factor `≥ 2^64` (beyond the
verified BPSW range, secondary: Feitsma–Galway) is reported per run in
`bpsw_factors`; the frontier runs below report none.

**Lemma 13 (wheel filter soundness). PROVED.** The C kernel skips a
candidate `q` only when some prime `p ≤ 61` divides `u = Dq − P` but not
`N*`; such `u` cannot divide `N*`. Candidate indices with `p | u` form one
residue class mod `p` because `u` moves in the arithmetic progression
`u(i) = u(0) + 2D·i` and the degenerate case `p | 2D`, `p | u(0)`,
`p ∤ N*` (which would kill the whole window) cannot occur: `p | D` and
`p | u(0)` force `p | P`, contradicting `gcd(P, D) = 1`.

## 3. Computational results

See `README.md` for the labelled results table, exact commands, run
records, wall times and certificates, and `WRITEUP.md` for the narrative.
Headlines (all CERTIFIED, produced by `search.py`, cross-checked by
`engine2.py` on overlapping ranges, every run record carrying engine
hashes, node counts and complete/incomplete flags):

- Positive controls, all-primes mode: the engine reproduces exactly the
  known Giuga numbers with ≤ 7 prime factors (7 numbers: 30, 858, 1722,
  66198, 2214408306, 24423128562, and the three 7-factor ones) and the
  known PPNs with ≤ 8 prime factors (2, 6, 42, 1806, 47058, 2214502422,
  52495396602, plus the 8-factor term at m = 8), matching OEIS
  A007850/A054377 (secondary) term for term.
- Odd-mode exhaustion of `E_{−1}` and `E_{+1}` for all `m ≤ M_final`
  (value in README): no solutions. With Lemmas 2–6 this proves the
  factor-count bounds stated in the README.

## 4. Open questions

- Push `m` further: the tree grows by roughly two orders of magnitude per
  even rung; `m = 18` looks like dedicated-cluster territory.
- The same engine with the Carmichael side-conditions
  `(p−1) | (n/p − 1)` bolted on would attack the Giuga-conjecture record
  (≥ 4771 factors) directly; the pruning there is congruential, not just
  metric, and BMS 2013's exclusion-bound machinery (paper unavailable in
  this sandbox) should be compared first.
- Odd proper Znám solutions of length ≤ M are also excluded by the
  `E_{+1}` runs; the proper/improper distinction deserves its own note.
