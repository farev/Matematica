# Polychromatic discrepancy of triangulations, the open residue class (Basti–Cremaschi, 2026)

Colour the vertices of a plane triangulation red and blue so that every face sees both
colours; the *discrepancy* disc(T) is the smallest possible imbalance ||R| − |B||.
Asayama and Matsumoto conjectured disc(T) ≤ n/3; Basti and Cremaschi (arXiv:2608.21585,
August 2026) proved disc(T) ≤ n − 2⌈n/3⌉ for all n using the balanced four-colour theorem,
and the sharper U(n) = n − 2⌈(n+2)/3⌉ for n ≢ 5 (mod 6). For n ≡ 5 (mod 6) — where U(n)
is two below the universal bound — they write that the question "remains open", with
n = 11 checked by computer. It looked tractable because their proof fails in that class
at exactly one class-size vector of the four-colouring, and that configuration is rigid.

Write-up page: <https://fabianarevalo.com/triangulation-discrepancy> (pending; see `PAGE.md`).

**Status:** active (proved for n ≤ 23 and for ≤ 2 high-degree vertices; the general class open)
**Sessions:** 2026-09-04

## Results

| Claim | Label | Where |
|---|---|---|
| **The refined bound disc(T) ≤ n − 2⌈(n+2)/3⌉ holds for every triangulation on n = 11, 17 and 23 vertices** — the first three orders of the open residue class — and, for every n ≡ 5 (mod 6), whenever the balanced 4-colouring's big class has at most two vertices of degree ≥ 5; a counterexample needs n ≥ 29 | PROVED | NOTE Theorem 3 (Lemmas 1–8) |
| Structure theorem: a triangulation on n = 6m+5 vertices with disc(T) ≥ 2m+1 has a proper 4-colouring with class sizes (3m+2, m+1, m+1, m+1) whose big class is *fully mixed* (every link shows all three colour pairs), has ≥ 2m+3 vertices of degree 3, between 3 and m−1 of degree ≥ 5 and none of degree 4, total degree excess ≤ 2m−1; every other vertex lies on a face avoiding the big class; no vertex has more than 2m+1 degree-3 neighbours in the big class; and every "single flip" (Lemma 7) fails | PROVED | NOTE §1–§4, Theorem 2 |
| **disc(T) ≤ 3 = U(17) for all 129,664,753 triangulations on 17 vertices**, by exhaustive census (independent confirmation of Theorem 3 at n = 17); exactly 2,652 attain it | CERTIFIED | NOTE Theorem 4; `data/n17_disc3.txt` |
| **disc(T) ≤ 5 = U(23) for every triangulation on 23 vertices** by the structural enumeration (independent confirmation of Theorem 3 at n = 23, ≈ 6·10¹⁰ triangulations, unreachable by census): 109,507,132 two-connected plane graphs on 12 vertices from plantri, 948,057 configurations passing the necessary conditions, all of discrepancy 1, every one admitting a single flip (277 s / 365 s) | CERTIFIED | NOTE Theorem 5; `struct_enum.c`, `results_struct_m3.txt`, `results_struct_m3_flip.txt` |
| Exact discrepancy distribution for all triangulations with 13 ≤ n ≤ 17 (the published table stopped at n = 12): the refined bound is attained at every order (4, 422, 89, 14, 2,652 extremal triangulations) | CERTIFIED | NOTE Theorem 4; `results_census_13_17.txt`, `data/` |
| The published Table 2 (4 ≤ n ≤ 12) reproduced exactly by two independent implementations | CERTIFIED | `disc.c`, `brute.py` |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `disc.c` | exact disc(T) for every triangulation in plantri `planar_code` on stdin (backtracking with monochromatic-face pruning); `-q` histogram only, `-d D` dumps every T with disc ≥ D as adjacency lists | ~4 μs per graph; n = 17 in 4 × 4 min | the distributions of NOTE Theorem 4 |
| `brute.py` | independent brute force over all 2^{n−1} red sets (the paper's method) | n ≤ 11 in a minute | agrees with `disc.c` |
| `struct_enum.c m` | the structural enumeration of NOTE §5: reads 2-connected plane graphs on 3m+3 vertices from plantri, applies the structure theorem's filters, enumerates equitable 3-colourings and empty-face sets, rebuilds T and computes disc(T); prints any counterexample | m = 2: seconds; m = 3: 277 s on one core | NOTE Theorem 5 |
| `census.sh` | the n = 14..17 census driver (n = 17 in four `res/mod` parts) | 15 min, one core | `results_census_13_17.txt` |

Build (plantri 5.5 from <https://users.cecs.anu.edu.au/~bdm/plantri/>, placed in `./plantri55/`):

```bash
cd conjectures/triangulation-discrepancy
gcc -O2 -o disc disc.c && gcc -O2 -o struct_enum struct_enum.c
./plantri55/plantri 12 | ./disc -q                      # reproduces [BC] Table 2, n = 12
./plantri55/plantri 17 0/4 | ./disc -q -d 3 > part0.txt  # census, part 0 of 4
./plantri55/plantri -p -c2 -e18:21 -f6 9 | ./struct_enum 2   # control at n = 17
./plantri55/plantri -p -c2 -e25:30 -f8 12 | ./struct_enum 3  # n = 23
```

Python 3.11 for `brute.py`; C99 otherwise; no other dependencies.

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `results_census_13_17.txt` | `census.sh` | the exact discrepancy histograms and generated counts for 13 ≤ n ≤ 17 (counts equal OEIS A000109) |
| `data/n13_disc3.txt`, `data/n15_disc3.txt`, `data/n16_disc4.txt`, `data/n17_disc3.txt` | `disc -d 3` | every triangulation of orders 13, 15, 16, 17 attaining the refined bound (adjacency lists in rotation order, one per line: 4, 89, 14, 2,652 graphs) |
| `results_struct_m2.txt`, `results_struct_m3.txt` | `struct_enum` | the enumeration summaries for n = 17 (control) and n = 23 |

## Known defects and open threads

- The refined bound for the whole residue class n ≡ 5 (mod 6) is **not** proved: the
  case of three or more big-class vertices of degree ≥ 5 (NOTE Theorem 2 (iii)–(vi),
  possible only for n ≥ 29) is open. Lemma 8's Euler count gives σ ≤ 3h − 3 + (2/3)|N|
  there, which three disjoint links of length 5–6 can satisfy. Worse, the configuration
  in which every single flip is blocked does occur (n = 35, three periodic hexagonal
  links covering everything; `hexpants.py` constructs such triangulations by SAT) — and
  those triangulations have discrepancy 1, so the missing ingredient is a colouring
  construction beyond Lemma 7, not a sharper count.
- The n = 23 certification rests on the structure theorem (Lemmas 1–5 only) and on
  plantri generating *all* 2-connected plane graphs with the given parameters (its
  documented behaviour for `-p -c2`); it is not a brute-force census, and has been
  cross-checked only through the n = 11 and n = 17 controls.
- The balanced four-colour theorem of Kawarabayashi–Yoneda–Yoneda is used as stated in
  its arXiv abstract (the paper itself was not read); [BC] cite it as Corollary 17.
- Single-engine computations: `disc.c` is cross-validated against a Python brute force
  only for n ≤ 11; the n ≥ 12 distributions come from one implementation.
- Next orders: n = 29 needs 2-connected plane graphs on 15 vertices with 32–39 edges —
  an order of magnitude more than plantri can stream in an hour — unless the flip lemmas
  are pushed into the generation.

## Prior work

- A. Basti, T. Cremaschi, arXiv:2608.21585 (21 Aug 2026): the two bounds, the open
  residue class, the census to n = 12 (all 1,249 triangulations on 11 vertices have
  discrepancy 1). Read in full on 2026-09-04; v1, no citing work found.
- Y. Asayama, N. Matsumoto, Graphs Combin. 38 (2022): the conjecture, the (5n−16)/9 bound
  and the n/3 − 2 lower-bound family (secondary, via [BC]).
- A. Arevalo Loyola, A. Biniaz, P. Bose, T. Shermer, SWAT 2026: the (3n−16)/7 bound and
  the 2+2 merging lemma (secondary, via [BC]).
- K. Kawarabayashi, H. Yoneda, M. Yoneda, arXiv:2607.13025 (Jul 2026): the balanced
  four-colour theorem (abstract read).
- No other work on the residue class n ≡ 5 (mod 6) was found (arXiv search, 2026-09-04).
