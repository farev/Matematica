# Lattice points of the parking-function polytope (OEIS A333331; Stanley, 2020)

How many lattice points does the convex hull P_n of the parking functions
of length n contain? Stanley computed eight terms in 2020;
Amanbayeva–Wang (2022) answered the question only as an unwieldy double
sum and asked for the Ehrhart polynomial; two conjectures stood in the
OEIS entry (Howroyd's e.g.f., Wiseman's loop-graph equivalence); and
Selig (EJC 2024) asked for exactly this enumeration in sandpile language
(recurrent states of the stochastic sandpile on a complete graph). It
looked tractable for a session because the bottleneck was a single
combinatorial identification: the facet description is subset-sum-shaped,
which smelled like a polymatroid, hence like Postnikov's draconian
machinery — and the conjectured answer was already known to 8 terms.

**Status:** active (theorem proved; upstream reporting pending)
**Page:** <https://fabianarevalo.com/parking-polytope>
**Sessions:** 2026-08-29

## Results

| Claim | Label | Where |
|---|---|---|
| a(n) = # loop-graphs on [n], n edges, every component unicyclic; e.g.f. exp(−½log(1−T) + T/2 − T²/4). Proves Howroyd's and Wiseman's A333331 conjectures; answers Selig's (EJC 2024, §6) enumeration question for stochastic-sandpile recurrent states | PROVED | [`NOTE.md`](NOTE.md) Thm A, Cor A1–A3 |
| Ehrhart polynomial: i(P_n,t) = Σ over sparse multiforests of t^s (t(t+1)/2)^d, with closed e.g.f.; answers Amanbayeva–Wang §6(b). Sum-form specializes Liu–Thawinrak Cor 7.6 (Dec 2025); the index-set identification and closed form are new | PROVED | [`NOTE.md`](NOTE.md) Thm B |
| a(n) ~ C·n^{n−1/4}, C = e^{1/4}√(2π)/(2^{1/4}Γ(1/4)) ≈ 0.746492 (second half of Selig's question) | PROVED | [`NOTE.md`](NOTE.md) Cor A4 |
| a(1)–a(40), the first independent computation past a(8) (all 8 published terms reproduced; 12-way cross-check table) | CERTIFIED | [`a_values.txt`](a_values.txt), NOTE §7 |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `count_lattice_points.py` | a(n) by exact DP over Stanley's facet description | seconds to n=40 | `terms_dp.txt`, a(9) = 167 341 283 |
| `controls.py` | 4 independent checks: literal facet brute force, partial-orientation enumeration, loop-graph brute force, exact e.g.f. | ~2 min | all agree, positive control detects corruption |
| `verify_theorem.py` | S_n enumeration, component identity, Ehrhart 3-way (DP/formula/e.g.f.), exact rational hull membership | ~1 min | every link of Thm A/B verified at small n |
| `asymptotics_check.py` | terms to n=40, e.g.f. regression, asymptotic ratio, Ehrhart reciprocity | ~20 s | `a_values.txt`; ratio → 0.984 at n=40 |
| `count_loopgraphs.c` | u(n) by C(n(n+1)/2, n) brute force in C | u(8): ~3 min | u(8) = 7 501 422 = a(8) |

Run from inside this directory:

```bash
cd conjectures/parking-polytope && python3 count_lattice_points.py 40
python3 controls.py 5 && python3 verify_theorem.py && python3 asymptotics_check.py
gcc -O2 -o u8 count_loopgraphs.c && ./u8 8
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `a_values.txt` | `asymptotics_check.py` | a(1)–a(40), exact (b-file-ready) |
| `terms_dp.txt` | `count_lattice_points.py` | a(1)–a(24) as first computed mid-session |
| `u8_result.txt` | `count_loopgraphs.c` | u(8) brute-force output |

## Known defects and open threads

- The proof leans on two published theorems not re-proved here: Stanley's
  facet description of P_n (as established in Amanbayeva–Wang) and
  Postnikov's Theorem 11.3. Both were read in the original today; the
  facet description is additionally verified end-to-end by exact rational
  hull membership at n = 3, 4.
- Upstream reporting not yet done (needs the local machine / identity):
  OEIS A333331 update (formula now proved, terms extendable), a note to
  Selig and to Howroyd/Wiseman, possibly a short arXiv note. See PAGE.md
  while it exists, and NOTE §9 for the mathematical open threads
  (bijective refinement via the stochastic burning algorithm; h-vector;
  the complete-bipartite analogue; interior-point involution).
- Asymptotic ratio at n = 40 is 0.984, not yet 1; the o(1) is real but
  slow (O(n^{-1/2})-type corrections). Not a defect of the proof, just of
  impatience.

## Prior work

Stanley (AMM Problem 12191; OEIS A333331), Amanbayeva–Wang (ECA 2022):
polytope, facets, volume, slice-sum lattice count. Postnikov (IMRN 2009):
draconian sequences, Theorem 11.3; his Example 11.4 (permutohedron ↔
forests) is the un-coned shadow of our Lemma 4. Liu–Thawinrak
(arXiv:2512.14199, Dec 2025): general draconian-sum Ehrhart formula for
u-parking polytopes — found mid-session during the novelty check;
Theorem B's sum-form is its classical-case specialization and is credited
as such (NOTE §6, §8). Selig (EJC 2024): the sandpile reading and the
open enumeration question. Howroyd and Wiseman (2024): the conjectures,
here proved. Lemmas 1–3 (the polymatroid/Minkowski-sum realization) are
marked as independent rediscovery — implicit in Liu–Thawinrak Ex. 7.4.
