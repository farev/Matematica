# Additive squares (Pirillo–Varricchio 1994; Halbeisen–Hungerbühler)

A word contains an **additive square** if two adjacent blocks of the same length
have the same sum — for example `2 5 | 3 4`. The PVHH problem asks whether there
is an **infinite** word over some finite set of integers with no additive square
anywhere in it. It has been open since the 1990s. The cube version is settled
(there is an infinite additive-cube-free word over `{0,1,3,4}`); the square
version is not.

Write `L(A)` for the length of the longest additive-square-free word over the
alphabet `A`, or `∞` if arbitrarily long ones exist. PVHH asks: is `L(A) = ∞`
for some finite `A ⊂ ℤ`?

The fault line this session pushed on: whether a word is additive-square-free
depends on the alphabet **only through the integer relations among its letters**.
That turns statements about infinitely many alphabets into single finite
computations over an alphabet of integer *vectors*.

**Status:** active
**Sessions:** 2026-08-01
**Page:** <https://fabianarevalo.com/additive-squares>

## Results

| Claim | Label | Where |
|---|---|---|
| Quotient Lemma: `L(A) ≤ L(A_M)` for any sublattice `M` of the relation lattice `Λ(A)` | PROVED | [`NOTE.md`](NOTE.md) §3 |
| `L(A) = 7` for **every** 3-element alphabet in characteristic 0 | PROVED | [`NOTE.md`](NOTE.md) §4 |
| `L(A) ≤ 60` for every 4-element alphabet with `a+d = b+c` — reproduces **Freedman's published bound** in three lines | PROVED reduction, CERTIFIED constant | [`NOTE.md`](NOTE.md) §5 |
| That bound is **attained**: `L({0,1,5,6}) = 60` | CERTIFIED | [`NOTE.md`](NOTE.md) §5 |
| Exact `L(A)` for 51 four-letter integer alphabets, incl. `L({0,1,2,3}) = 50`, `L({0,1,2,4}) = 62`, `L({0,1,2,5}) = 86`, `L({0,1,3,5}) = 88` | CERTIFIED | [`NOTE.md`](NOTE.md) §6, `data/sweep4_c18.csv` |
| Over all 50 degenerate alphabets with `c ≤ 18`, `L` takes only the four values 50, 55, 58, 60 — and 60 in 45 of them | CERTIFIED | [`NOTE.md`](NOTE.md) §6 |
| Freedman's relation `(1,1,-1)` is the **only** one of the 11 relation classes of sup-norm ≤ 2 whose search tree closes: 60, against ≥ 418…≥ 3000 for the other ten | CERTIFIED | [`NOTE.md`](NOTE.md) §8, `data/relations_n2.csv` |

Nothing here resolves PVHH, and nothing here claims to.

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `afsf.c` | exhaustive / randomised DFS for the longest additive-square-free word over an **integer** alphabet | ms to minutes per alphabet | `L({0,1,5,6}) = 60` |
| `afsfv.c` | the same over an alphabet of integer **vectors** in `ℤ^d` — this is what makes uniform theorems possible | 0.2 s for the generic degenerate alphabet | `L(A_M) = 60`, 7,707,828 nodes |
| `verify_word.py` | independent `O(n²)` verifier written from the definition, not from the incremental test | instant | cross-check of every extremal word |
| `sweep4.py` | sweeps normalised 4-letter integer alphabets `{0,a,b,c}`, `c ≤ MAXC` | ~40 min, 3 cores, `MAXC = 18` | `data/sweep4_c18.csv` |
| `relation_quotient.py` | builds the universal vector alphabet `A_v` for each primitive relation `v` and computes `L(A_v)` | minutes per class | `data/relations_n2.csv` |

Run from inside this directory:

```bash
cd conjectures/additive-squares
gcc -O2 -o afsf afsf.c && gcc -O2 -o afsfv afsfv.c
python3 verify_word.py --selftest
./afsfv exhaust 2 "0,0|1,0|0,1|1,1" 500 20000000000   # the Freedman constant, 60
./afsf  exhaust "0,1,5,6"           500 20000000000   # attained, 60
python3 sweep4.py 18 400000000 4000 3 data/sweep4_c18.csv
```

The two binaries are gitignored; rebuild them with the `gcc` line above.

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/sweep4_c18.csv` | `sweep4.py` | one row per normalised alphabet: `L`, whether exact, node count, extremal word |
| `data/relations_n2.csv` | `relation_quotient.py` | `L(A_v)` per primitive relation class of sup-norm ≤ 2 |
| `data/extremal_words.txt` | extracted from the sweep | the extremal words, in the input format of `verify_word.py` |
| `data/nondegen_exact.log` | `afsf` | exact runs and node counts for `{0,1,2,5}`, `{0,1,3,5}` |

Every number in `NOTE.md` comes from one of these files. All arithmetic is exact
integer arithmetic; there is no floating point in any critical path.

## Known defects and open threads

- **No primary source was read.** The sandbox blocked arXiv, OEIS,
  erdosproblems.com and MathOverflow at the proxy (403). Every citation in
  `NOTE.md` §7 is marked **(secondary)** and rests on web-search synthesis.
  Freedman's paper in particular has an unresolved venue (INTEGERS 16 (2016)?
  Math. Magazine 49 (1976)?) and must be checked before any of this is repeated
  in a preprint.
- Theorem 4 (`L = 7` on three letters) is **very likely folklore**. We claim no
  novelty for it; it is included because Lemma 2 makes it a one-liner and it
  calibrates the method.
- Theorem 5 is a **clean-room reproduction** of Freedman, not a new bound. Only
  the attainment at `{0,1,5,6}` was not found in reachable literature, and that
  is a weak claim under a blocked network.
- Rows in `data/sweep4_c18.csv` with `exact=0` are **budget-limited lower
  bounds**. The depth reached is an artifact of the node budget and is not a
  measurement of `L(A)`; it must not be read as growth data.
- Sharpest open thread: close the tree for the 3-term-AP class `v = (1,1,0)`.
  Two independent searches (budget-limited exhaustive: 440; randomised, seed 11,
  depth cap 200,000: 437) agree to within three letters, so `L` there is very
  likely finite and would be a **second** Freedman-type theorem. Meanwhile
  `v = (2,1,0)` and `v = (2,2,1)` ran to the depth cap and look infinite. See
  `NOTE.md` §8.

## Prior work

Fully sourced, and marked (secondary) throughout, in [`NOTE.md`](NOTE.md) §7.
In brief: PVHH is open (Pirillo–Varricchio; Halbeisen–Hungerbühler);
Cassaigne–Currie–Schaeffer–Shallit settled the **cube** case over `{0,1,3,4}`
and Lietard–Rosenfeld classified four-letter alphabets for cubes; Freedman
proved `L ≤ 60` for `a+d = b+c`; Rao–Rosenfeld showed additive squares **are**
avoidable over a finite subset of `ℤ²`; Keränen showed abelian squares are
avoidable on four letters. Ochem's heuristic reportedly suggests PVHH has a
negative answer.
