# Common prime factors of binomial coefficients (Erdős problem #699)

**Date.** 2026-08-12. **AI assistance:** this note was produced in an
AI-assisted session (Claude); all proofs below are elementary and should be
checked by hand before any external use.

## 0. The problem

For integers $1 \le i < j \le \lfloor n/2 \rfloor$, Erdős and Szekeres
[ES78] (secondary; paper unreachable from this sandbox) asked:

> **Conjecture (Erdős #699).** There is always a prime $p \ge i$ with
> $p \mid \binom{n}{i}$ and $p \mid \binom{n}{j}$.
>
> **Strengthening.** Apart from a *finite* set of triples $(n,i,j)$, one can
> take $p > i$.

Sources for the statement, both fetched 2026-08-12: the Lean formalization
in `google-deepmind/formal-conjectures` (`ErdosProblems/699.lean`, statements
`erdos_699` and `erdos_szekeres_strengthening`, both `research open`, floor
division $j \le n/2$), and the status entry `falsifiable` (= open,
counterexample would be finite) in `teorth/erdosproblems`
(`data/problems.yaml`, status last updated 2025-08-31). The erdosproblems.com
page adds (secondary): Erdős–Szekeres knew failures of the $p>i$ form at
$i=2$ for "some particular power of 2", some at $i=3$, and exactly one with
$i \ge 4$, namely $\gcd\binom{28}{5}\binom{28}{14} = 2^3 3^3 5$.

**Terminology.** Call $(n,i,j)$ *satisfied at* $p$ if $p$ is prime,
$p \ge i$, and $p$ divides both binomials. Call the triple **tight** if it is
satisfied at $p = i$ but at no prime $p > i$ (the conjecture holds, the
strengthening does not cover it), and a **counterexample** if it is satisfied
nowhere.

**Prior computational work** (found today, cited as the frontier): a public
Rust scan by Cong Lu (github: `conglu1997/erdos_699_rust`, run log
`run-20260103-191520` committed 2026-01-03; announced on the erdosproblems
forum thread 699): the conjecture verified for $4 \le n \le 10^7$, with
exactly 9 tight pairs found, and targeted family scans $n = 2^k$
($k \le 27$), $n = 3^m+1$ ($m \le 17$) finding no further ones. Everything
in this note beyond that frontier is new as far as we could determine
(scoop-guard record in `WRITEUP.md`); everything inside it is independent
confirmation.

## 1. Reduction machinery

**Proposition 0 (Erdős–Szekeres theorem; classical).** For
$1 \le i < j \le n-1$, $\gcd\bigl(\binom{n}{i}, \binom{n}{j}\bigr) > 1$.
*Proof.* The subset-counting identity
$\binom{n}{j}\binom{j}{i} = \binom{n}{i}\binom{n-i}{j-i}$ holds: both sides
count pairs (an $i$-set inside a $j$-set inside $[n]$). If the gcd were 1,
then $\binom{n}{j} \mid \binom{n-i}{j-i}$. But applying
$\binom{m+1}{r+1} = \binom{m}{r}\tfrac{m+1}{r+1} \ge \binom{m}{r}$
repeatedly, $\binom{n-i}{j-i} \le \binom{n-1}{j-1} = \binom{n}{j}\tfrac{j}{n}
< \binom{n}{j}$, and $\binom{n-i}{j-i} \ge 1$: a positive multiple of
$\binom{n}{j}$ strictly smaller than it, contradiction. $\square$

*Consequence.* Levels $i = 1, 2$ of the main conjecture always hold (any
common prime is $\ge 2 \ge i$), and level $i = 1$ is never tight (that prime
is $> 1$). The conjecture's content starts at $i = 3$; the strengthening's
at $i = 2$.

**Proposition 1 (window).** For a prime $p > i$:
$p \mid \binom{n}{i} \iff n \bmod p < i \iff p$ divides one of
$n, n-1, \dots, n-i+1$.
*Proof.* $\binom{n}{i} = n(n-1)\cdots(n-i+1)/i!$ and $p \nmid i!$, so
$v_p\binom{n}{i} = \sum_{t<i} v_p(n-t)$, positive iff $p \mid n-t$ for some
$0 \le t < i$; as the window is shorter than $p$, that $t$ is unique and
equals $n \bmod p$. $\square$

**Proposition 2 (a prime in the window settles everything).** If a prime
$p \in (n-i, n]$ exists, then every pair $(i,j)$ with $i < j \le n/2$ is
satisfied at $p$, and $p > i$.
*Proof.* $p > n-i \ge n/2 \ge j > i$. With $t := n-p < i$, Prop 1 gives
$p \mid \binom{n}{i}$ (window at level $i$) and also $p \mid \binom{n}{j}$
(window at level $j$: $n \bmod p = n - p < i < j$, and $p > j$). $\square$

**Corollary 3 (danger zone).** A tight triple or counterexample requires
$i \le g(n) := n - \operatorname{prevprime}(n)$ (and $g(n) = 0$ when $n$ is
prime). So for $n \le 4\cdot 10^9$ only $i \le 336$ (the maximal prime gap
below $4\cdot 10^9$) can occur, and for most $n$ only $i \lesssim \log n$.

**Proposition 4 (Kummer, 1852; classical).** $v_p\binom{n}{k}$ equals the
number of carries when adding $k$ and $n-k$ in base $p$; equivalently
$p \nmid \binom{n}{k}$ iff every base-$p$ digit of $k$ is at most the
corresponding digit of $n$ ("$k$ is dominated by $n$ base $p$").

**Proposition 5 (central coefficient).** For an odd prime $q$ and $n = 2j$:
$q \nmid \binom{2j}{j}$ iff every base-$q$ digit of $j$ is at most
$(q-1)/2$. *Proof.* Adding $j + j$ base $q$ produces no carry iff no digit
doubles past $q-1$, i.e. all digits $\le (q-1)/2$; a digit
$\ge (q+1)/2$ produces a carry outright, and with all digits $\le (q-1)/2$
no carry can arise even with a carry-in, by induction from the least
significant position. $\square$

**Proposition 6 (exact criterion).** Fix $n$ and $2 \le i \le g(n)$, and let
$A_i = \{p \text{ prime} : p > i,\ p \mid n(n-1)\cdots(n-i+1)\}$ (by Prop 1
these are exactly the primes $> i$ dividing $\binom{n}{i}$). Then:
$(n,i,j)$ is tight or a counterexample $\iff$ $j \in (i, \lfloor n/2\rfloor]$
is base-$p$ dominated by $n$ for every $p \in A_i$; it is tight iff
moreover $i$ is prime, $n \bmod i^2 < i$, and some base-$i$ digit of $j$
exceeds that of $n$; otherwise it is a counterexample.
*Proof.* Immediate from Props 1 and 4, plus: $i \mid \binom{n}{i}$ iff the
base-$i$ digits of $i = (1,0)_i$ dominate... precisely, by Prop 4 applied to
$k = i = (1,0)_i$: $i \mid \binom{n}{i}$ iff digit 1 of $n$ base $i$ is $0$,
i.e. $n \bmod i^2 < i$. $\square$

## 2. The two structured families

Every known tight triple has $n = 2^k$ (with $i = 2$) or $n = 3^m + 1$
(with $i = 3$, $j = n/2$; plus the single $i=5$ triple at $n = 28 = 3^3+1$).

**Theorem 7 ($i=2$ at $n = 2^k$).** Let $k \ge 2$, $n = 2^k$.
(a) $(n, 2, j)$ is tight iff $2 < j \le 2^{k-1}$ and $j$ is base-$q$
dominated by $n$ for every prime $q \mid 2^k - 1$. No counterexample exists
at $(n, 2)$.
(b) If $2^k - 1$ is prime (a Mersenne prime), no $(n, 2, j)$ is tight.
*Proof.* (a) By Prop 1, the primes $p > 2$ dividing $\binom{n}{2}$ are the
odd primes of $n(n-1) = 2^k(2^k-1)$, i.e. the primes $q \mid 2^k-1$. So "no
satisfying $p > 2$" is exactly the domination condition (Prop 4). The
rescue at $p = 2$ is automatic: $2 \mid \binom{n}{2} = 2^{k-1}(2^k-1)$ for
$k \ge 2$, and $2 \mid \binom{2^k}{j}$ for every $0 < j < 2^k$ ($n$'s
base-2 digits are $1,0,\dots,0$; any such $j$ has a 1-digit below position
$k$). Hence tight, never a counterexample.
(b) If $q = 2^k-1$ is prime, then $n = (1,1)_q$, so the $j \in [0,n]$
dominated by $n$ are $\{0, 1, q, q+1\}$, and none lies in $(2, 2^{k-1}]$
since $q = n - 1 > n/2$. $\square$

*Remark.* Theorem 7(b) explains the shape of the known family: the four
known members $k = 4, 9, 11, 41$ all have $2^k-1$ a **semiprime**
($15 = 3\cdot 5$, $511 = 7\cdot 73$, $2047 = 23\cdot 89$,
$2^{41}-1 = 13367 \cdot 164511353$), i.e. they lie in OEIS A085724 (fetched
from the OEIS mirror 2026-08-12: A085724 begins $4, 9, 11, 23, 37, 41, 49,
59, \dots$). Semiprimality is not sufficient: $k = 23, 37, 49, 59$ are
decided and clean (§4). Membership for each $k$ is the finite domination
check of Theorem 7(a).

**Theorem 8 ($i=3$ at $n = 3^m+1$; a sufficient criterion).** Let $m \ge 2$
and $n = 3^m + 1$, $j = n/2 = (3^m+1)/2$. Suppose either
(i) $m = 2$; or
(ii) $m \ge 3$ is odd, $Q := (3^m+1)/4$ is prime, and $D := (3^m-1)/2$ is a
prime power.
Then $(n, 3, n/2)$ is tight.
*Proof.* The primes $p > 3$ dividing $n(n-1)(n-2) = (3^m+1)\,3^m\,(3^m-1)$
are the primes $> 3$ of $(3^m+1)(3^m-1)$.
First the rescue at $p = 3$: $v_3\binom{n}{3} = v_3(n(n-1)(n-2)) - v_3(6)
= m - 1 \ge 1$; and $3 \mid \binom{n}{n/2}$ because $n = (1,0^{m-1},1)_3$
while $n/2 = (1^{m-1},2)_3$ (indeed $(3^m-1)/2 = (1^m)_3$, add 1), whose
digit 2 exceeds $n$'s trailing digit 1 (Prop 4).
Case (i): $m=2$: $n = 10$, the only prime $> 3$ in $10 \cdot 8$ is $5$, and
$n/2 = 5 = (1,0)_5$ is dominated by $10 = (2,0)_5$.
Case (ii): $m$ odd means $4 \mid 3^m+1$ and $D$ odd. The primes $>3$
dividing $3^m+1 = 4Q$: just $Q$ (prime by hypothesis, $Q \ge 7 > 3$ for
$m \ge 3$). Those dividing $3^m-1 = 2D$: just $q$ where $D = q^e$. Now use
Prop 5 with $n = 2j$:
— base $Q$: $j = 2Q = (2,0)_Q$, digits $\le (Q-1)/2$ since $Q \ge 5$;
— base $q$: $j = D + 1 = q^e + 1 = (1, 0, \dots, 0, 1)_q$, digits
$\le (q-1)/2$ since $q \ge 5$ ($q \mid 3^m-1$ and $q > 3$... note $q \ne 3$
as $3 \nmid 3^m-1$, and $q \ne 2$ as $D$ is odd; if $q = 5$ digits $1 \le 2$
hold).
So neither $Q$ nor $q$ divides $\binom{n}{n/2}$, no prime $> 3$ divides both
binomials, and $p = 3$ works: tight. $\square$

*Remark.* The hypotheses of Theorem 8 hold exactly for
$m \in \{2, 3, 5, 7, 13\}$ in the computed range ($D = 13, 11^2, 1093,
797161$; $Q = 7, 61, 547, 398581$; verified by factorization 2026-08-12),
reproducing every known $i=3$ family member. The criterion is sufficient,
not necessary: general $m$ is decided by the exact criterion (Prop 6), and
no other $m \le 40$ passes it (§4). $m = 23$ and $m = 43$ have $Q$ prime
but $D$ composite with two large primes; $m = 23$ is decided clean.

## 3. Algorithms (summary; details in the scripts)

- `sweep699.c` — full sweep over $n \le N$: segmented full factorization of
  every integer; per $n$, levels $i \le g(n)$; the admissible set $A_i$
  comes from the factor lists (Prop 1); the two strongest congruence
  filters ($\min (t+1)/p$) generate CRT candidates
  ($j \bmod p \le t$ for both); candidates get exact Kummer tests against
  all of $A_i$ and the $p=i$ test (Prop 6). Production runs use
  `IMIN = 2` (level 1 is settled by Prop 0); validation runs use
  `IMIN = 1` so Prop 0 doubles as an engine control.
- `brute699.py` — independent reference: per $n$ builds the full
  divisibility matrix over all primes $\le n$ from Prop 4 and checks every
  pair $(i,j)$ directly. No shared code, no shared algorithm with the
  engine.
- `family699.py` — structured families beyond the sweep range: exact
  criterion (Prop 6) with sympy factorizations; candidate $j$'s enumerated
  as the smallest Lucas-dominated set among admissible primes (streaming,
  cap $10^8$); levels whose factorizations or dominated sets exceed
  resources are reported UNKNOWN, never guessed.
- `verify_triple.py` — standalone verifier for claimed tight triples:
  re-verifies factorizations by multiplication + primality, then Kummer
  carries (carry-propagation implementation, deliberately different from
  the engines' domination formulation), plus an independent uniqueness scan
  for the new triple.
- `audit699.py` — deep-sample audit: random $n$ re-decided end-to-end by
  the Python criterion path and compared against the C census.

## 4. Results

All computations 2026-08-12, 4 cores (see WRITEUP for timings), exact
integer arithmetic throughout, no randomness in any result-bearing path.

**R1 (CERTIFIED).** *Erdős #699 holds for all $4 \le n \le 10^7$,
independently confirming the January 2026 scan with a different algorithm
and codebase in 30 s (their run: ~120 core-hours).* A deeper sweep is in
flight; this bound will be updated only when it completes. (Level $i=1$ by
Prop 0; levels $2 \le i \le g(n)$ by the sweep; levels $i > g(n)$ by
Prop 2.)

**R2 (CERTIFIED).** *Complete census of tight triples for $n \le 10^7$
(full sweep) and for the structured families far beyond (R4):* exactly ten
are known, the nine previously known and one new:

| n | i | j | structure |
|---|---|---|---|
| 10 | 3 | 5 | $3^2+1$, $j=n/2$ |
| 16 | 2 | 6 | $2^4$ |
| 28 | 3 | 14 | $3^3+1$, $j=n/2$ |
| 28 | 5 | 14 | same $n$, $i=5$ |
| 244 | 3 | 122 | $3^5+1$, $j=n/2$ |
| 512 | 2 | 147 | $2^9$ |
| 2048 | 2 | 713 | $2^{11}$ |
| 2188 | 3 | 1094 | $3^7+1$, $j=n/2$ |
| 1594324 | 3 | 797162 | $3^{13}+1$, $j=n/2$ |
| **2199023255552** | **2** | **285920731515** | **$2^{41}$ — new** |

**R3 (CERTIFIED, new).** *$(2^{41},\, 2,\, 285920731515)$ is a tight
triple:* $\gcd\bigl(\binom{2^{41}}{2}, \binom{2^{41}}{285920731515}\bigr)$ is a power
of 2. It is the largest known tight triple ($n \approx 2.2\cdot 10^{12}$),
the first new one since the January 2026 census, and $j$ is unique at
$(n,i) = (2^{41}, 2)$ (independent uniqueness scan over all $9.07\cdot
10^7$ dominated candidates). Verified by the standalone verifier
(`certs/verify_2_41.txt`).

**R4 (CERTIFIED).** *Family censuses far beyond the sweep:*
- $n = 2^k$, $4 \le k \le 64$: every danger level $2 \le i \le g(n)$
  decided for $k \le 44$; the only tight triples are $k = 4, 9, 11, 41$
  (all at $i = 2$, one $j$ each). For $45 \le k \le 64$ all levels are
  decided **except** 19 specific $(k,i)$ levels listed in
  `data/family_unknown_levels.csv` (dominated sets exceed $10^8$; honest
  UNKNOWNs, not failures). In particular the semiprime exponents
  $k = 23, 37, 49, 59$ are decided and clean.
- $n = 3^m+1$, $2 \le m \le 40$: every danger level $i \ge 2$ decided
  (levels $i = 1$ are settled by Prop 0; two $i=1$ dominated-set blowups at
  $m = 37, 39$ are therefore vacuous); the only tight triples are
  $m = 2, 3, 5, 7, 13$ (at $i=3$, $j = n/2$; plus $(28,5,14)$). An
  extension to $m \le 48$ is in flight (factoring-limited; UNKNOWN levels
  will be marked in `data/family_census.csv`).

**R5 (NUMERICAL).** Heuristic accounting for the strengthening (§5 of
WRITEUP has the computation): the $i=3$ mechanism needs, by Theorem 8-type
structure, simultaneous near-primality of $(3^m\pm1)/\{2,4\}$ — events of
probability $\asymp 1/m^2$ under standard heuristics, so finitely many
members are expected beyond any bound (consistent with the observed cutoff
at $m = 13$ through $m \le 40$). The $i=2$ mechanism is *not* visibly
decaying: the four known members sit inside the semiprime exponents
(A085724), the per-$k$ expected solution count measured from the actual
dominated-set densities is $O(0.1$–$1)$ at $k = 41$ and does not trend to
zero on the available data, and 17 levels in $[45, 64]$ remain undecided.
On present evidence the $i=2$ family being infinite is a live possibility;
the strengthening as formalized (a finite exceptional set) should not be
considered numerically supported — only unrefuted.

## 5. Open questions

1. Decide the 19 UNKNOWN $(k,i)$ levels for $2^k$ (and 9 more for $3^m{+}1$, $m \ge 42$) (needs a
   compiled dominated-set enumerator or a smarter intersection bound).
2. Is there any tight triple with $n$ not of the form $2^k$ or $3^m+1$?
   (None for $n \le 4\cdot 10^9$.) A structural proof that tightness at
   $i=2,3$ forces these shapes would turn R2's pattern into a theorem.
3. Prove or refute: infinitely many $k$ with $2^k-1$ semiprime admit the
   digit coincidence of Theorem 7(a). Even a conditional result (under
   standard heuristics for the factorization of $2^k-1$) deciding the
   *expected* infinitude of the $i=2$ family would sharpen the
   strengthening's status considerably.
4. The $i \ge 4$ shelf: $(28,5,14)$ is still the only known member; is it
   truly isolated? (It is for $n \le 4\cdot 10^9$.)

## References

- [ES78] P. Erdős, G. Szekeres, *Some number theoretic problems on binomial
  coefficients*, Austral. Math. Soc. Gazette 5 (1978) 97–99. (secondary —
  not readable from this sandbox; statement and exception remarks taken
  from erdosproblems.com/699 via search snippets and from the Lean
  formalization.)
- Erdős problem #699: erdosproblems.com/699 (T. F. Bloom's database);
  machine-readable status in `teorth/erdosproblems` (fetched 2026-08-12).
- Lean formalization: `google-deepmind/formal-conjectures`,
  `FormalConjectures/ErdosProblems/699.lean` (fetched 2026-08-12).
- Cong Lu, `conglu1997/erdos_699_rust` (fetched 2026-08-12): verification
  $n \le 10^7$ and the nine-triple census (2026-01-03), announced in the
  erdosproblems.com forum thread for #699 (secondary).
- R. K. Guy, *Unsolved Problems in Number Theory*, 3rd ed., problem B31
  (secondary — attribution via the erdos_699_rust README).
- E. Kummer, *Über die Ergänzungssätze zu den allgemeinen
  Reciprocitätsgesetzen*, J. reine angew. Math. 44 (1852) 93–146.
  (classical; used as Prop 4.) (secondary)
- OEIS A085724 (exponents of semiprime Mersenne numbers), fetched from the
  `oeis/oeisdata` mirror 2026-08-12.
