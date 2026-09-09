# Unit-step walks with no three collinear points (Shallit's k_min, 2026)

Page: <https://fabianarevalo.com/collinear-walks> (pending; see `PAGE.md`).

Shallit (arXiv:2609.05780, 5 Sep 2026) proved that an infinite walk in ℕ¹⁶
using only standard unit steps can avoid three collinear points, and asked
for the least dimension k_min for which this is possible; 4 ≤ k_min ≤ 16 was
all that was known on arXiv. Equivalently, k_min is the least alphabet size
admitting an infinite word with no two adjacent blocks of equal
letter-frequency vector (no "weak abelian square"; here: *3-free*). It looked
tractable because Shallit's proof is a 2-adic valuation argument on a
Gaussian-integer walk that costs a factor of four in the alphabet (it needs
all sixteen pairs of consecutive states), and a walk whose consecutive
states differ by ±1 only would pay a factor of two.

**Status:** active
**Sessions:** 2026-09-09

## Results

| Claim | Label | Where |
|---|---|---|
| k_min ≤ 8: the Heighway dragon curve's (direction, turn) word over 8 letters is 3-free; it is the fixed point of the 2-uniform morphism 0→02, 1→03, 2→52, 3→53, 4→46, 5→47, 6→16, 7→17 | **PROVED** | `NOTE.md` Thm 1 |
| k_min ≤ 7: identifying the letters (0,+) and (2,+) (opposite directions, same turn) keeps the word 3-free — an infinite unit-step walk in ℕ⁷ with no three collinear vertices | **PROVED** | `NOTE.md` Thm 2 |
| Lemma: the dragon walk Z_n satisfies ν₂(\|Z_n − Z_m\|²) = ν₂(n − m) whenever the endpoint directions are not antipodal | **PROVED** | `NOTE.md` Lemmas 2, 2′ |
| Kalviainen's unpublished six-dimensional construction (repository draft, 5 Sep 2026) reviewed: no gap found; six step vectors, all-pairs valuation identity on 3.1 M pairs, word 3-free to 30 000 all reproduced | review (not our result) | `NOTE.md` §5 |
| No coding of the 8-letter dragon word onto ≤ 6 letters is 3-free beyond length 3000; exactly 8 of the 4011 codings onto 3…7 letters survive, all with 7 | **CERTIFIED** | `data/codings_3000.txt` |
| In the periodic sign/order family of Gaussian digit walks (period ≤ 4), the only 8-transition words are the dragon type (best coding 7) and Kalviainen's alternating-sign type (best coding 6); no member codes onto ≤ 5 letters | **CERTIFIED** (to length 1500 / 1200) | `data/family_1500.txt`, `data/family12_p3_full.txt` |
| No cyclic uniform morphism of length ≤ 16 over 4 letters has a 3-free fixed point beyond length 1500; over 5 letters none of length ≤ 13, and 12 of length 14 (Shallit's among them) | **CERTIFIED** (to 1500) | `data/morph4.txt`, `data/morph5_ctrl.txt` |
| L(1)=1, L(2)=3, L(3)=7 (controls; Brown 1971); 28 861 282 canonical 3-free words of length 46 over 4 letters, consecutive-count ratio ≈ 1.27–1.30 and slowly falling, so L(4) is not decidable by search and k_min = 4 is not excluded | **CERTIFIED** (counts) / **NUMERICAL** (extrapolation) | `data/tf4_46.txt` |
| Shallit's four candidate morphisms (k = 5, 6, 7, 8) 3-free to 20 000; the 7-letter word to 100 000; the mixed identifications (r,−)~(r+1,+) to 30 000 | **NUMERICAL** | `NOTE.md` §6.3 |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

**Priority note.** The best bound in the literature is Kalviainen's draft
k_min ≤ 6 (github.com/ekalvi/erdos-193, `paper/unit_step_walk_N6_short.tex`,
5 Sep 2026, "independent review pending"), together with Cambie's 14 (same
repository). Our 7 is weaker; it is an independent proof by a different walk
(alternating child order instead of alternating digit sign), and the review
in NOTE §5 supports the 6.

## Scripts

Run from inside `code/` (C programs: `gcc -O2 -o name name.c`).

| file | what it does | cost | headline output |
|---|---|---|---|
| `tf.c` | exhaustive DFS for 3-free words over k letters; `./tf k maxlen [cap]` | k ≤ 3 instant; k = 4 to length 46 ≈ 5 min | L(3) = 7; count table |
| `checkmorph.c` | tests a word (file, or fixed point of a cyclic morphism) for 3-freeness to N | O(N² log N): 30 000 letters ≈ 50 s | every "3-free to N" line |
| `dragon.py` | builds the dragon words (8 and 4 letters) and checks Lemma 2 on all equal-direction pairs below M | `python3 dragon.py 100000 3000`: 1 min | 1 123 622 pairs, 0 failures |
| `codings.c` | all set partitions of the 8 letters, 3-freeness of each coding to N | 2 s | 8 survivors, all with 7 classes |
| `family.c` | periodic sign/order Gaussian digit walks, minimal 3-free coding per pattern | period ≤ 4, ≤ 6 classes: 2 min; 12-letter alphabets ≤ 5 classes: 20 min | floor 6 in the family |
| `morphsearch.c` | cyclic uniform morphisms of length L over Z_k with 3-free fixed point to N | k=4, L ≤ 16: 1 min; k=5, L=14: 5 min | none over 4 letters; 12 over 5 |
| `g85.py` | Kalviainen's six-vector walk: vectors, all-pairs identity, six-letter word | 1 min | 6 vectors, 0 failures on 3 123 750 pairs |
| `defect.py` | valuation defect ν(Z_n − Z_m) − ν₂(n − m) by endpoint-direction class | 30 s | zero except for antipodal endpoints |

Reproduce the theorems' numerical checks:

```bash
cd conjectures/collinear-walks/code && gcc -O2 -o checkmorph checkmorph.c
python3 dragon.py 30000 3000            # writes dragon8.txt, checks Lemma 2
./checkmorph 8 30000 -f dragon8.txt     # 3-free to N=30000 (k=8)
python3 g85.py 30000 2500 && ./checkmorph 6 30000 -f g85_6.txt
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/dragon8_prefix4096.txt`, `data/dragon7_prefix4096.txt` | `dragon.py` | first 4096 letters of the 8- and 7-letter words (digits 2r+[δ=−]; coding 4→0) |
| `data/kalviainen6_prefix4096.txt` | `g85.py` | first 4096 letters of the six-vector word |
| `data/codings_3000.txt` | `codings.c` | the 8 surviving codings of the dragon word (length 3000) |
| `data/family_1500.txt`, `data/family12_p3_full.txt` | `family.c` | transition alphabets and minimal codings for every pattern |
| `data/morph4.txt`, `data/morph5.txt`, `data/morph5_ctrl.txt` | `morphsearch.c` | candidate counts and survivors per (k, L) |
| `data/tf4_46.txt` | `tf.c` | canonical 3-free word counts over 4 letters by length |
| `data/check7a_1e5.txt` | `checkmorph.c` | the 7-letter word 3-free to 100 000 |

## Known defects and open threads

- Theorem 2 gives 7; the draft bound 6 (Kalviainen) is stronger and, on our
  reading, correct. Nothing here reaches 5.
- The four mixed identifications (r,−)~(r+1,+) are 3-free to 30 000 with no
  proof; the natural displacement functional degenerates for them.
- No lower bound beyond k_min ≥ 4 (Brown 1971). The 4-letter growth data is
  extrapolation, not evidence for a construction.
- The 12 five-letter length-14 morphisms are unreduced modulo symmetry and
  unproved, like Shallit's.
- All "3-free to N" statements are prefix checks; only Theorems 1–2 (and, if
  accepted, the drafts of §1) say anything about infinity.

## Prior work

Brown, AMM 78 (1971) 886–888 (ternary abelian squares, k_min ≥ 4);
Gerver–Ramsey, Pacific J. Math. 83 (1979) (planar and ℤ³ walks);
Lidbetter, Discrete Math. 347 (2024); Korsky, arXiv:2607.02832 and
arXiv:2608.07906 (L(d), doubly exponential lower bound); Cambie–Kalviainen,
arXiv:2609.01766 (Erdős #193, the Gaussian valuation lemma); Shallit,
arXiv:2609.05780 (k_min ≤ 16, the word formulation, candidates); repository
drafts by Cambie (14) and Kalviainen (6), 5 Sep 2026, and Shallit's
four-letter weak-abelian-cube note (6 Sep 2026), all read on 2026-09-09 from
github.com/ekalvi/erdos-193. The dragon curve / paperfolding facts used are
classical (Davis–Knuth 1970); we prove what we use. Nothing here is known to
be a rediscovery; the seven-letter word does not appear in the sources above.
