# Finch's regularity conjecture for 1-additive sequences (Finch, 1991–92)

Start with two numbers `a < b` and keep writing down the smallest number bigger
than the last one that can be written as a sum of two *different* earlier
numbers in **exactly one** way. That is the 1-additive sequence `U(a,b)`.
Ulam's original `U(1,2) = 1, 2, 3, 4, 6, 8, 11, 13, 16, 18, 26, …` looks
completely disordered and is believed to be so. But some `U(a,b)` are secretly
periodic: their gaps eventually repeat forever. Those are called **regular**,
and Finch conjectured exactly which `(a,b)` are.

Only two families have ever been proved regular — `U(2,v)` for odd `v ≥ 5`
(Schmerl–Spiegel 1994) and `U(4,v)` for `v ≡ 1 (mod 4)` (Cassaigne–Finch 1995).
Nothing has been added in thirty years. `U(4,v)` for `v ≡ 3 (mod 4)`, and every
`a ≥ 6`, are open.

The fault line this session pushed on: if `U(a,b)` has only **finitely many even
elements**, then membership of an odd number depends on a *bounded window* of
earlier values. That turns the tail of the sequence into a deterministic
finite-state automaton — and a repeated state is a *proof* of periodicity, not
an observation of one. The whole problem becomes a finite, exactly checkable
certificate.

**Status:** active
**Sessions:** [2026-08-02](../../log/2026-08-02-finch-regularity.md)

## Results

| Claim | Label | Where |
|---|---|---|
| **Theorem 1** (certificate theorem): three finite, exactly-checkable conditions (P), (C), (F) imply `U(a,b)` is regular, its even set is exactly `E`, and its period is `P`. Self-correcting: cannot be satisfied with an incomplete even set | **PROVED** | [`NOTE.md`](NOTE.md) §3 |
| Regularity of **32 sequences**, each with an exact certificate, **20 of them in cases reported open**: `U(4,b)`, `b ≡ 3 (mod 4)`, `b ∈ {7,11,19,23,27,35,39,43}`; `U(6,7)`, `U(6,11)`; `U(8,9)`, `U(8,11)`; `U(10,11)`, `U(10,13)`, `U(10,17)`; `U(12,13)`, `U(12,17)`; `U(14,15)`; `U(16,17)`; `U(18,19)` | **CERTIFIED** | [`NOTE.md`](NOTE.md) §4, [`data/certificates.csv`](data/certificates.csv) |
| The other 12 certificates reproduce Cassaigne–Finch (`a=4`, `b ≡ 1 mod 4`, `5 ≤ b ≤ 49`) — used as controls | **CERTIFIED** | same |
| **Exceptional family.** For all 255 odd `b` with `5 ≤ b ≤ 513`, the even elements of `U(4,b)` below `6b²+4000` are exactly `{4, 2b+4, 4b+4}` — except for the seven values `b = 2^k − 1` (`k = 3..9`), where one more appears, always exactly `4b² + 2b − 4` | **CERTIFIED** (range-limited; absolute for `b = 7`) | [`NOTE.md`](NOTE.md) §5, [`data/a4_even_elements.csv`](data/a4_even_elements.csv) |
| `U(4,7)` certified outright: exactly four even elements `{4,18,32,206}`, and fundamental difference `P = 11,301,098` — about **5000×** any neighbouring `U(4,b)`, `b ≤ 49` | **CERTIFIED** | [`NOTE.md`](NOTE.md) §5, §8 |
| 2-adic period law `P(4,b) = 2^{⌊log₂(b−1)⌋+3}(b+1)`, holding for all twelve tested `b ≡ 1 (mod 4)` and for `b = 19`, and failing for every other tested `b ≡ 3 (mod 4)` (whose periods carry a large prime factor) | **CERTIFIED** for the 13 values; the *law* is conjectural | [`NOTE.md`](NOTE.md) §6 |
| Schmerl–Spiegel reproduced: `U(2,v)` has even set exactly `{2, 2v+2}` for all 98 odd `v` with `5 ≤ v ≤ 199` | **CERTIFIED** (range-limited) | `survey.c` |

Nothing here proves Finch's conjecture, and nothing here claims to.

**Novelty caveat, prominently:** the claim that these 20 cases are *open* rests
on search-engine summaries only — the sandbox could not reach arxiv.org,
oeis.org or any other scholarly host (see [`NOTE.md`](NOTE.md) §7). Every
citation in this directory is secondary. If a primary source shows these cases
were already settled, the results remain correct but become rediscoveries and
must be relabelled.

See [`NOTE.md`](NOTE.md) for statements and proofs, [`WRITEUP.md`](WRITEUP.md)
for the session narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `ulam.py` | reference generator, written straight from the definition — the positive control | ms | reproduces `U(1,2)` exactly |
| `survey.c` | exact even-element landscape over a rectangle of `(a,b)` | 0.7 s for 4403 pairs at `N=10⁴` | `E(a,b)` patterns |
| `evens.c` | exact even elements of one `U(a,b)` up to `N` | ~1 s at `N = 10⁶` | the exceptional family |
| `certify.py` | certificate of Theorem 1; hash-table cycle detection | s–min | `data/certificates.csv` |
| `verify_cert.c` | **independent** verifier: Brent cycle detection, O(1) memory, written from the theorem rather than ported | s–20 min | all 32 rows; agrees with `certify.py` on `E`, `P`, `nR` on the 23 both could reach |
| `certsweep.py` | drives `certify.py` over a list of `b` | — | `cs*.jsonl` |

Run from inside this directory:

```bash
cd conjectures/finch-regularity
gcc -O2 -o evens evens.c && gcc -O2 -o survey survey.c
gcc -O2 -o verify_cert verify_cert.c

python3 ulam.py 1 2 300              # positive control: Ulam's sequence
./evens 4 63 27814                   # the exceptional even element 15998
./verify_cert 4 11 4000 60000000     # a certificate in an open case
./verify_cert 4 63 4000 60000000     # REJECTS: even-15998-has-exactly-one-rep
python3 certify.py 6 7 4000          # the same, independently, in Python
```

The last two commands are the ones to run first: one shows the verifier
accepting, the other shows it refusing a sequence whose even set was truncated.

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/certificates.csv` | `verify_cert.c` + `certify.py` | the 32 certificates: `a, b, E, W, X₀, X₁, P, |R|, B`, and whether the case was previously known |
| `data/a4_even_elements.csv` | `evens.c` | even elements of `U(4,b)` for all 255 odd `b ∈ [5,513]`, with the scan horizon and the predicted `4b²+2b−4` |

## Known defects and open threads

- **Every citation is secondary.** No primary source was read; the network was
  blocked. Verifying the Schmerl–Spiegel, Cassaigne–Finch and Finch references,
  and above all the open/closed status of the 20 new cases, is the first job of
  the next session. `oeis.org/FinchSadd.html` is Finch's own table of cases and
  periods and is the single most important page to read: Conjecture A and the
  period law may already be there.
- `U(4,15)`, `U(4,31)`, `U(4,63)` are **not** certified. For `U(4,15)` and
  `U(4,31)`, Brent's algorithm closed no cycle within `1.5·10⁹` automaton steps,
  so `max(preperiod, period) > 1.5·10⁹` for both — against periods in the
  thousands for neighbouring `b`. Their windows are `~4b²` bits wide.
- Conjecture A (fourth even element iff `b = 2^k−1`) and Conjecture B (the
  period law) are unproved. They are patterns over a tested range, not theorems.
- The certificate is per-pair. It gives no uniform statement in `b`, which is
  what an actual theorem for `b ≡ 3 (mod 4)` would need.
- The `(C)` residue check in `verify_cert.c` enumerates pairs from `R` and stops
  once every even class is covered; worst-case it is `O(|R|²)`. It has not been
  stress-tested on a case where the sumset genuinely fails to cover.
- **Only 23 of the 32 certificates are doubly implemented.** `U(4,7)`,
  `U(4,43)`, `U(8,11)`, `U(10,11)`, `U(10,17)`, `U(12,17)`, `U(14,15)`,
  `U(16,17)` and `U(18,19)` rest on `verify_cert.c` alone — `certify.py`'s memory
  use grows with the period and it could not reach them. Those nine rows carry
  strictly less evidence than the other 23.

## Prior work

Schmerl–Spiegel (JCTA 66, 1994), Cassaigne–Finch (Experimental Math. 4, 1995),
Finch (JCTA 60, 1992 — the "finitely many evens ⇒ regular" criterion; Fibonacci
Quart. 29, 1991 and Experimental Math. 1, 1992 — the conjecture). Full details
and the exact wording of what each is reported to say are in
[`NOTE.md`](NOTE.md) §7. **All secondary.**

Theorem 1 is best understood as a certificate-carrying, machine-checkable form
of Finch's criterion. We do not claim the implication itself is new; what the
session contributes is the explicit finite certificate, the 20 new certified
cases, and the exceptional family of §5.
