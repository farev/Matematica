# Doubly saturated Ramsey graphs (Grinstead–Roberts 1982 (secondary); Przybocki–Mackey–Heule–Subercaseaux 2026)

A graph is **R(s,t)-good** if it has no clique on `s` vertices and no independent
set on `t` vertices. It is **doubly saturated** if, on top of that, *every* single
edge flip destroys the property: adding any missing edge creates a `K_s`, and
deleting any existing edge creates an independent `t`-set (and neither the graph
nor its complement is complete). Equivalently — Proposition 8 of
[`NOTE.md`](NOTE.md) — it is an *isolated vertex* of the graph whose vertices are
the `R(s,t)`-good graphs on `n` labelled vertices and whose edges are single edge
flips. `DS(s,t)` denotes the least order at which one exists.

The fault line this session pushed on: a 2026 paper was reported to have hit a
SAT wall at `n = 19` for `(s,t) = (4,5)`, and the objects are provably invisible
to local search, which makes a prescribed-symmetry ansatz the natural instrument.

> ## ⚠ The headline of this session was a rediscovery
>
> A doubly saturated `R(4,5)`-good graph on 19 vertices **is already published**
> (arXiv:2604.21187, April 2026, as the circulant with distances `{4,5,6,8}`, and
> as the `t = 5` member of a proved infinite family on `6t−11` vertices). The
> graph found here is that graph. The secondary report that `n = 19` was open was
> a truncation: the sentence about CaDiCaL failing is the setup for the paragraph
> in which the authors make the same circulant ansatz and solve it. Details in
> [`WRITEUP.md`](WRITEUP.md) §2. Nothing at order 19 is claimed as new.

**Status:** active
**Sessions:** [2026-08-04](../../log/2026-08-04-doubly-saturated.md)
**Write-up page:** none — this session produced no page-worthy result.

## Results

| Claim | Label | Where |
|---|---|---|
| `G₁₉ = Cay(Z₁₉, ±{1,3,5,6})` is a doubly saturated `R(4,5)`-good graph; 8-regular, 76 edges, `\|Aut\| = 38`; exactly nine circulant connection sets work at `n = 19` and they form one multiplier orbit, so one graph up to isomorphism. **Published — rediscovery, no novelty claimed** | CERTIFIED | [NOTE](NOTE.md) §4, `data/cert_n19_45.txt` |
| The published `6t−11` family — circulant with distances `{t−2} ∪ [2t−3, 3t−6]` — is doubly saturated `R(4,t)`-good for `t = 4,5,6,7` (`n = 13,19,25,31`). **Independent confirmation of a published theorem** | CERTIFIED | [NOTE](NOTE.md) §4, `family.py` |
| **220 doubly saturated `R(4,5)`-good graphs on 22 vertices**, 9-regular, 99 edges, invariant under a fixed-point-free automorphism of order 11; one orbit under the family's symmetries; none is a circulant. **Not known to be new** | CERTIFIED | [NOTE](NOTE.md) §5, `data/cert_n22_45.txt` |
| `G₁₉` is the **only** doubly saturated `R(4,5)`-good circulant on `n ≤ 24` — the whole feasible range, since `R(4,5) = 25`. Partial support for the paper's unproved uniqueness suggestion | CERTIFIED | [NOTE](NOTE.md) §6, Result 13 |
| Exhaustive circulant census for `(s,t)` with `3 ≤ s ≤ t ≤ 6` plus `(3,7)…(3,9)`: doubly saturated circulants exist exactly at `n = 5` (3,3), `13` (3,5), `35` (3,9), `13, 17` (4,4), `19` (4,5), `25` (4,6), `29, 37, 41` (5,5); none for (3,4), (3,6), (3,7), (3,8) in range. Reproduces every published value we know of | CERTIFIED | [NOTE](NOTE.md) §6, `data/census_clean.txt` |
| The set of orders admitting a doubly saturated circulant is not always `{R(s,t)−1}`, not always a single order, not always non-empty | CERTIFIED | [NOTE](NOTE.md) §6, Result 14 |
| Double saturation ⟺ `G` maximal `K_s`-free **and** `Ḡ` maximal `K_t`-free ⟺ `G` isolated in the edge-flip graph; hence **no flip-based local search can ever reach one**. Self-complementary + maximal `K_s`-free ⟹ doubly saturated `(s,s)`, which accounts for every Paley entry above | PROVED (almost certainly folklore) | [NOTE](NOTE.md) §3 |

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `census.c` | exhaustive sweep of all circulants `Cay(Z_n,S)` for double saturation, `n ≤ 64` | seconds–minutes per `(s,t)`, 4 cores | `data/census_clean.txt` |
| `semireg.c` | same for graphs on `Z_m × [k]` invariant under `σ(x,i)=(x+1,i)`; `k=1` reproduces `census.c` | seconds to ~10 min at `2²⁴` | `data/semireg_out.txt` |
| `one.c` | tests one circulant, given `n s t d1,d2,…` | instant | verdict line |
| `ds.c` | first, simpler 32-bit circulant sweep; kept as the independent implementation the others were checked against | instant | verdict lines |
| `mkcert.py` | emits a witness certificate for a circulant, in pure Python from the definition | seconds–minutes | `data/cert_*.txt` |
| `decode.py` | rebuilds a `semireg.c` hit from its orbit encoding, re-checks it from the definition, emits a certificate | seconds | `data/cert_n22_45.txt` |
| `check_cert.py` | **independent verifier**: re-derives every claim from the edge list alone | seconds | OK / FAILED |
| `verify.py` | brute-force check straight from the definition, with four positive and one negative control | seconds | control table |
| `family.py` | checks the published `6t−11` family at `t = 4,5,6,7` | ~10 min | four verdicts |
| `aut.py` | `\|Aut(G₁₉)\|` by exhaustive backtracking | seconds | 38 |
| `orbit.py`, `iso22.py` | multiplier/symmetry orbits of the `n=19` and `n=22` hits | instant | 9 → 1 orbit; 220 → 1 orbit |

Run from inside this directory:

```bash
cd conjectures/doubly-saturated
gcc -O3 -march=native -fopenmp -o census census.c && ./census 4 5 5 24
python3 check_cert.py data/cert_n19_45.txt
python3 check_cert.py data/cert_n22_45.txt
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/cert_n19_45.txt` | `mkcert.py` | the 19-vertex `(4,5)` graph, 76 edges + 171 witnesses |
| `data/cert_n22_45.txt` | `decode.py` | the 22-vertex `(4,5)` graph, 99 edges + 231 witnesses |
| `data/cert_n5_33, n13_35, n13_44, n17_44, n25_46, n29_55, n35_39.txt` | `mkcert.py` | the other census hits (`C₅`, `C₁₃(1,5)`, Paley(13), Paley(17), `(4,6)@25`, Paley(29), `(3,9)@35`) |
| `data/census_clean.txt` | `census.c` | the full circulant census, all ranges |
| `data/semireg_out.txt` | `semireg.c` | prescribed-symmetry sweeps at `n = 16,18,20,22,24` |

Certificate format: an edge list, then one `ADD u v …` line per non-edge giving
the `K_s` that appears when `uv` is added, and one `DEL u v …` line per edge
giving the independent `t`-set that appears when `uv` is deleted.
`check_cert.py` trusts nothing but the edge list.

## Known defects and open threads

- **No primary source was read.** The sandbox blocked arXiv, OEIS,
  erdosproblems.com, MathOverflow and Wikipedia at the proxy (HTTP 403). Every
  citation is **(secondary)** and rests on web-search summaries. One formula
  transcribed from those summaries was demonstrably garbled ([`NOTE.md`](NOTE.md)
  §8) — a direct measurement of how much they can be trusted. **Verifying
  arXiv:2604.21187 against the actual PDF is the first job of any follow-up**,
  in particular whether the order-22 examples are new and whether the
  Grinstead–Roberts attribution is right.
- **The `(5,5)` census rows at `n = 37` and `n = 41` have no independent
  certificate.** They rest on `census.c` alone; the Python check at `n = 41`
  times out, since it rescans `C(41,5)` subsets per edge flip. Every other census
  row, including `(3,9)` at `n = 35` (which does enumerate all `C(35,9) ≈ 7·10⁷`
  subsets), ships a verified certificate.
- **The equal `R(4,5)`-good counts at `n = 20` and `n = 22` (both 1430)** in
  `data/semireg_out.txt` are unexplained. Probably coincidence; worth re-deriving
  before either number is quoted.
- **`n ≤ 18` non-existence was not reproduced.** Our corroboration is only that
  none of 5211 structured `R(4,5)`-good graphs on 18 vertices is doubly
  saturated, and that no circulant works for `n ≤ 18`.
- Sharpest open thread: the paper's **Question 1**, whether `DS(4,t) = 6t−11` for
  all `t ≥ 4`. Existence at `6t−11` is proved there and confirmed here at four
  values; minimality is open, and minimality is a non-existence statement over
  all graphs of smaller order — exactly the direction Corollary 9 says local
  search cannot help with.

## Prior work

Everything here is **(secondary)** — no PDF was opened.

- Przybocki, Mackey, Heule, Subercaseaux, *Doubly Saturated Ramsey Graphs: A Case
  Study in Computer-Assisted Mathematical Discovery*, arXiv:2604.21187, CICM 2026.
  Reported to prove `DS(4,5) = 19`, the `6t−11` family for all `t ≥ 4`
  (Lean-formalised), uniqueness of `C₅` for `(3,3)`, `(3,7)` at 20 and `(3,8)` at
  25, `DS(s,t) ≥ 2s+2t−7`, a Paley table `s → p` of `5, 13, 29, 53`, and to leave
  open Question 1 and a `(3,t)` conjecture. **The order-19 result of this session
  is a rediscovery of theirs.**
- Attributed origin: a 1982 question of Grinstead and Roberts, *On the Ramsey
  numbers R(3,8) and R(3,9)*, JCTB 33, 27–51. **Unverified.**
- The notion appears to have no earlier name. "Ramsey saturated"
  (Balister–Lehel–Schelp 2006), "`R(s,t)`-critical", "Ramsey-minimal" and
  "`K_r`-saturated" (Erdős–Hajnal–Moon 1964) are all different notions; the last
  is the one-sided ancestor.
- `R(4,5) = 25` (McKay–Radziszowski 1995) is used only to bound sweep ranges.
