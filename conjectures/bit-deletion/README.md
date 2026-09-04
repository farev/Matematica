# Bit Deletion game (OEIS A398916, Do Thanh Nhan, 2026)

Two players take turns deleting one binary digit of a positive integer;
leading zeros are then discarded; whoever removes the last nonzero digit
wins. OEIS A398916 (added 14 Aug 2026) lists the Sprague–Grundy values and
records two conjectures: the values never exceed 3 (checked to 5·10^6), and
a(4n) = a(n) (checked to 10^6). The game looked tractable for a session
because the only structure a deletion can see is the pattern of zeros, and
the values at each bit-length split exactly 3 : 1 — a sign of a finite
rule hiding in the block structure.

**Write-up page:** pending (`PAGE.md` handoff in this directory).

**Status:** closed — the Sprague–Grundy function is determined completely.
**Sessions:** 2026-09-03

## Results

| Claim | Label | Where |
|---|---|---|
| **Theorem 1.** For n ≥ 1 write the binary expansion as `1 0^{z_1} 1 0^{z_2} 1 ⋯ 1 0^{z_{m+1}}` (blocks may be empty); let L be the bit-length and t the number of initial blocks of odd length. Then `G(n) = (L mod 2) + 2·[t odd]`. | PROVED | NOTE §2 |
| Both A398916 conjectures: `G(n) ≤ 3` for all n, and `G(4n) = G(n)`; also `G(2n) ≢ G(n) (mod 2)`, so the period along n, 2n, 4n, … is exactly 2. | PROVED | NOTE Cor. 1 |
| Outcome classes: n is a P-position iff L is even and t is even. **Rediscovery**: this P/N rule (and the base-b reduction below) is folklore among Project Euler 961 solvers — unrefereed write-ups, cited as (secondary). | PROVED (known) | NOTE Cor. 2 |
| Exactly `2^{L−3}` of the L-bit numbers (L ≥ 3) have value 2 or 3; the number of P-positions below `4^k` is `2^{2k−1} − 1`. | PROVED | NOTE Cor. 3 |
| **Theorem 2 (misère).** The misère P-positions are exactly the n with normal value `G(n) = 1` (L odd, t even); there are `4^k` of them below `2^{2k+1}`. | PROVED | NOTE §4 |
| Base b ≥ 2 digit deletion has the same Grundy function evaluated on the zero/nonzero pattern (folklore reduction, secondary). | PROVED (known) | NOTE Rem. 3 |
| Theorems 1 and 2 hold for every `n < 2^32` (4,294,967,296 positions recomputed from the definition; 0 mismatches; no value > 3; exact `2^{L−3}` counts at every level). | CERTIFIED | `data_grundy_check_2e32.txt` |
| Induction step of Theorem 1 and Lemma D exhaustively checked for all strings of length ≤ 18 (524,287 strings; 0 failures); closed form vs definition for `n < 2^20`; 34 published terms reproduced. | CERTIFIED | `grundy.py` output in WRITEUP |

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `grundy.py` | pure-Python reference: Grundy values from the definition, the closed form, the induction-step and lemma checks | `python3 grundy.py 20`: ~7 s | 0 mismatches below 2^20; 0 induction-step/lemma failures for |u| ≤ 18 |
| `grundy_check.c` | OpenMP exhaustive check of Theorem 1 (normal play) and Theorem 2 (misère) from the definition, level by bit-length | `./grundy_check 32`: 177 s, 4 threads, 4 GB RAM | 0 mismatches for all n < 2^32 |
| `variants.py` | misère outcomes from the definition vs "P ⟺ G = 1" (n < 2^20, with the `4^k` counts), and base-3/4/5/10 digit deletion from the definition vs the binary zero-pattern formula | `python3 variants.py 20`: ~1 min | 0 disagreements in every check |

Run from inside this directory:

```bash
cd conjectures/bit-deletion
python3 grundy.py 20
gcc -O3 -march=native -fopenmp -o grundy_check grundy_check.c && ./grundy_check 32 | tee data_grundy_check_2e32.txt
```

`grundy_check 28` (1 GB, ~8 s) is enough to see the full pattern; the
argument is the number of bits.

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data_grundy_check_2e32.txt` | `grundy_check 32` | per-bit-length value counts, misère P-counts, mismatch counters (all 0), timing; the CERTIFIED record |

No random seeds are involved; every computation is deterministic and exact
(small integers only).

## Known defects and open threads

- The P/N characterization and the base-b reduction were already known
  informally (Project Euler 961 community write-ups, unrefereed, *secondary*);
  no refereed source states them. The Grundy values, the bound, the `4n`
  invariance and the misère theorem have no prior source we could find
  (search record in `WRITEUP.md`).
- The C run's storage assumes values ≤ 3; the program detects and reports any
  overflow (none occurred), so the check is sound but would need re-running
  with wider storage if a variant with larger values were studied.
- Open: variants with two deletions per move, deletion of a run of equal
  digits, and partizan digit-deletion (Project Euler 963 type) — none
  analysed here.

## Prior work

- OEIS A398916 (Do Thanh Nhan, 14 Aug 2026; approved 20 Aug 2026): the
  definition, the formula `a(2^k) = (k mod 2) + 1` with proof, both conjectures
  with their checked ranges. Fetched 2026-09-03 via the OEIS text interface.
- Project Euler Problem 961 "Removing Digits" (21 Sep 2025): the decimal
  version of the game (linked from the OEIS entry). Public unrefereed
  solution write-ups (e.g. github.com/cirosantilli/project-euler-solutions,
  `solvers/961.md`; eulersolve.org/problem/961) state the zero-pattern
  reduction and the P/N rule of Corollary 2 — *secondary*; the PE forum itself
  is login-walled and was not read.
- Conway's "Digit Deletions" (ONAG, 2nd ed., pp. 190–192; known to us only
  through OEIS A120442 — *secondary*) is a different game (moves lower a
  digit or delete a zero together with everything after it).
- Searches of the arXiv API, Fraenkel's *Combinatorial Games: Selected
  Bibliography* (EJC DS2), MathOverflow/Math.SE and competition archives found
  no Sprague–Grundy analysis of one-symbol deletion games with leading-zero
  normalization (details in `WRITEUP.md`).
