# Matematica

Daily attempts at open problems in mathematics.

Every day I pick an unsolved conjecture — or an open thread in a recent paper —
and spend a session on it. Most days produce nothing but a record of what
failed. Occasionally a session produces something real: a new exact constant, a
sharpened inequality, an empirical law, or an audit of someone else's recent
work. Everything goes in this repository, successes and dead ends alike.

The failures are the point as much as the results. A research log that only
shows the wins is not a research log.

## Status vocabulary

Every claim in this repository carries exactly one of three labels. This is the
most important convention here, and it is not negotiable.

| Label | Meaning |
|---|---|
| **PROVED** | A theorem with a written proof. Holds for all cases in its stated scope. |
| **CERTIFIED** | An exact computation — rational or integer arithmetic, no floating point in the critical path — that is reproducible and ships a verifiable certificate. True for the range computed, not beyond. |
| **NUMERICAL** | Monte Carlo, curve fits, heuristics, floating-point exploration. Evidence, not proof. May be wrong. |

A computation is never described as a proof. "Verified for all n ≤ N" is a
CERTIFIED statement; it is not evidence that a conjecture is true, only that no
counterexample lives below that bound.

## Conjectures

Every conjecture has a write-up page at **[fabianarevalo.com/math](https://fabianarevalo.com/math)**
— the readable version, with the plain-language explanation first. This
repository is the code, data and certificates behind those pages.

One directory per conjecture, each with its own README carrying the full
statement, labelled results, scripts and reproduction commands.

| Conjecture | Status | Sessions | Strongest result so far |
|---|---|---|---|
| [**Chowla's conjecture**](conjectures/chowla/) · [page ↗](https://fabianarevalo.com/chowla) | active | 2 | **PROVED** exact 2-adic descent reducing two-point Chowla to its odd core, plus **CERTIFIED** correlation/pattern census to 10^12 and sign-pattern coverage to length 33 (N_33 = 196,202,853,829; all thirty earlier coverage values reproduced exactly by an independent clean-room implementation), and the parity-barrier gap measured at ~5·10^6 |
| [**Erdős–Gyárfás conjecture**](conjectures/erdos-gyarfas/) · [page ↗](https://fabianarevalo.com/erdos-gyarfas) | active | 1 | **CERTIFIED** — no counterexample has ≤ 18 vertices (prior reported bound: 17; 8.3×10⁸ graphs scanned at n = 18), plus a {4,8}-free cubic graph on 56 vertices with only 56 sixteen-cycles from annealing in the first cubic window [54, 62] |
| [**Additive squares (PVHH)**](conjectures/additive-squares/) · [page ↗](https://fabianarevalo.com/additive-squares) | active | 1 | **PROVED** a quotient lemma making additive-square-freeness depend only on the alphabet's relation lattice — it re-derives Freedman's bound `L ≤ 60` for `a+d=b+c` from one relation vector and gives `L = 7` for every 3-letter alphabet — plus **CERTIFIED** exact maxima for 51 four-letter integer alphabets (first such table) with 60 shown attained at `{0,1,5,6}` |
| [**Finch's regularity conjecture**](conjectures/finch-regularity/) · [page ↗](https://fabianarevalo.com/finch-regularity) | active | 1 | **PROVED** a self-correcting certificate theorem reducing regularity of a 1-additive sequence `U(a,b)` to three exactly-checkable finite conditions, giving **CERTIFIED** regularity for 32 sequences — 20 in cases reported open, including every `a = 6,…,18` attempted and `U(4,b)` for `b ≡ 3 (mod 4)` — plus the exceptional family: `U(4,b)` has a fourth even element exactly when `b = 2^k−1`, always equal to `4b²+2b−4` (all 255 odd `b ≤ 513`) |
| [**Circular repetition thresholds**](conjectures/circular-thresholds/) · [page ↗](https://fabianarevalo.com/circular-thresholds) | active | 2 | **PROVED** — `CRT_W(6) = RT(6) = 6/5`, an open case of the Currie–Mol–Rampersad conjecture settled (openness (secondary)), and `CRT_W(5) = 5/4` (possible Tunev-2025 overlap), via new Pansiot-code machinery — exact repetition transfer, a finite preservation certificate, circular pumping in the code — with certified `k = 21` binary generators and seeds mined from the session-1 spectra; plus **CERTIFIED** — the same ansatz is empty at `n = 4` through `k ≤ 46`, and the session-1 spectra, late gaps (147, 154) and Theorem N′ stand |
| [**Doubly saturated Ramsey graphs**](conjectures/doubly-saturated/) | active | 1 | **Rediscovery, marked as such** — the 19-vertex doubly saturated `R(4,5)` graph found here, `Cay(Z₁₉,±{1,3,5,6})`, turned out to be already published. What survives is **CERTIFIED**: 220 such graphs on **22** vertices (invariant under an order-11 fixed-point-free automorphism, none circulant, *not known to be new*); an exhaustive circulant census for `3 ≤ s ≤ t ≤ 6` that independently reproduces every published value; and that the 19-vertex graph is the *only* such circulant across the whole feasible range `n ≤ 24`. Plus **PROVED** (folklore) that these graphs are isolated vertices of the edge-flip graph, so no local search can ever reach one |
| [**Gilbreath's conjecture**](conjectures/gilbreath/) · [page ↗](https://fabianarevalo.com/gilbreath) | active | 3 | **PROVED** — no fixed-order statistical axiom system can imply eventual Gilbreath, now with bounded entries at every finite order (R2, R3.5) and a proof that Chase–Hunter–Tao's 2-separated axiom is necessary; plus thirteen unconditional covering lenses, a factor-2 sharpening of their lower bound, and **CERTIFIED** exact c₄–c₆ |
| [**Powerful progressions**](conjectures/powerful-progressions/) · [page ↗](https://fabianarevalo.com/powerful-progressions) | active | 1 | **CERTIFIED** — complete census of 3-term APs of consecutive powerful numbers to 10^19 (346 triples; the published table stopped at 18 below 10^14), collapsing to 16 primitives up to scaling with **PROVED** multiplier lemmas, the first squareless triple, and no 4-term AP below 10^19 |
| [**Generalized Schur numbers**](conjectures/generalized-schur/) · [page ↗](https://fabianarevalo.com/generalized-schur) | active | 1 | **CERTIFIED** — eleven new exact values `S(3;s,t,u)`, the first in the family since 2016, every boundary carrying a DRUP-checked proof and an independently verified witness: four open instances of Ahmed–Schaal's Conjecture 2.1 all **confirmed** (87, 98, 111, 118), seven values mapping the formula-less s=3 family; the complete extremal structure of (3,3,u) — one rigid skeleton, u−2 free ternary slots, 2·3^(u−2) colorings — at every computed size except the anomalous u=7; new **Conjecture A** (S(3;3,3,u)=9u−13, u≠7) predicted the u=10 and u=11 results before computation |
| [**Reciprocal Rado numbers**](conjectures/reciprocal-rado/) · [page ↗](https://fabianarevalo.com/reciprocal-rado) | active | 1 | **CERTIFIED** — independent certified proofs (DRUP + re-verified witness) for nine reciprocal Rado values f_r(k), 1/x₁+⋯+1/x_k = 1/x_{k+1}, already reported without a certificate by Myers–Parrish and Gaiser–Ramezanpour (f₂(2..8) = 60, 40, 48, 80, 108, **150**, **192**; f₃(2) = 3276, f₃(3) = 585): their bound 3k²+1 is never attained at an odd prime power in range (Δ = 13, 5, 3), as their own table already showed; plus a structural mechanism (not itself new — an even-k restriction of their Conjecture 1.3) certified at k = 4, 6, 8 with **f₂(8) = 192 predicted before the run**, and a new bound f₄(2) > 60000 |
| [**Signed difference sets**](conjectures/signed-difference-sets/) · [page ↗](https://fabianarevalo.com/signed-difference-sets) | active | 2 | **PROVED** two classical nonexistence criteria transfer to Gordon's signed difference sets, closing **45,328 of the 67,823 Open cells** of his database (zero conflicts against every known-existing cell), plus **CERTIFIED** exhaustive decisions of **58 more** — including **10 new signed difference sets with verified witnesses** (a λ=1 set in Z₅×Z₅; existence decided by group structure at orders 27, 32, 36) — dropping the Open shelf to 22,453; a **CERTIFIED audit**: 147 of 280 stored witnesses in the published database fail its defining equation, 22 repaired; and session 2: Masselot's 2026 closure of the ten cells this census left open ((32,20,4) exists iff noncyclic; no abelian (36,29,4)) **CERTIFIED**-verified leg by leg, with a new C18-quotient proof removing the last database dependency |
| [**Distinct subset sums (Erdős #1)**](conjectures/distinct-subset-sums/) | active | 1 | **CERTIFIED** — first movement of the `f(10)` frontier on Erdős's distinct-subset-sums problem since Grossman's `f(9)`: no 10-element set with distinct subset sums has largest element ≤ **262** (OEIS recorded > 220; Conway–Guy gives ≤ 309), via 166.9×10⁹ search nodes across four cross-verified engines; plus the full ladder `f(1..9)` re-derived from scratch with all optimal sets (the optimal 9-set is unique), and a 19.1M-set exclusion of near-Conway–Guy witnesses below 309 |

Daily entries, including the sessions that produced nothing, are in
[`log/`](log/).

## Layout

```
conjectures/<name>/   one directory per conjecture, self-contained
log/                  daily entries, YYYY-MM-DD-<conjecture>.md
tools/                utilities shared across conjectures
```

Each conjecture directory holds its own README, research note, writeup, code,
data and certificates. They are deliberately self-contained so any one of them
can be split out later with `git subtree split` if it grows into its own paper
or package.

## Running things

```bash
python3 -m pip install -e .
```

Requires Python 3.11+, NumPy and SciPy. Developed on Python 3.12.6 with
NumPy 2.3.5 and SciPy 1.17.0.

Scripts read and write data files by relative name, so **run them from inside
their own conjecture directory**:

```bash
cd conjectures/gilbreath && python3 verify.py 1e6
```

Each conjecture's README lists what every script does, what it produces, and
roughly what it costs to run — some finish in seconds, others want multiple
cores and several GB of RAM.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Corrections are especially welcome — if
something here is wrong, or rediscovers known work without saying so, please
open an issue.

## On AI assistance

These sessions are run with substantial AI assistance (Claude). This is
disclosed here, in each research note, and in any preprint that comes out of
this work. AI systems are not listed as authors, consistent with COPE guidance
and publisher policy. Every proof is checked by hand; every computational claim
ships code you can rerun.

## License

Code is [MIT](LICENSE-CODE). Prose, research notes and writeups are
[CC BY 4.0](LICENSE-PROSE) — compatible with the arXiv distribution license.
