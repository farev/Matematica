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
| [**Distinct subset sums (Erdős #1)**](conjectures/distinct-subset-sums/) · [page ↗](https://fabianarevalo.com/distinct-subset-sums) | active | 1 | **CERTIFIED** — first movement of the `f(10)` frontier on Erdős's distinct-subset-sums problem since Grossman's `f(9)`: no 10-element set with distinct subset sums has largest element ≤ **262** (OEIS recorded > 220; Conway–Guy gives ≤ 309), via 166.9×10⁹ search nodes across four cross-verified engines; plus the full ladder `f(1..9)` re-derived from scratch with all optimal sets (the optimal 9-set is unique), and a 19.1M-set exclusion of near-Conway–Guy witnesses below 309 |
| [**Graham's 105 problem (Erdős #376)**](conjectures/graham-105/) · [page ↗](https://fabianarevalo.com/graham-105) | active | 1 | **CERTIFIED** — complete census of `C(2n,n)` coprime to 105 below `3^600 ≈ 1.9·10^286`: **585,823,270 terms**, a 216-order-of-magnitude extension of the published 10^70 frontier (1374 terms, Thompson 2015), five-way cross-verified; Graham's "3160 is the last n also coprime to 11" verified to the same height; and the first counts beyond 10^70 show G growing in rare bursts — only 82 of 601 base-3 lengths inhabited, with a certified 26.7-decimal-order term-free desert `[3^474, 3^530)` — while the global exponent tracks the 0.02595 heuristic (fit 0.0248) |
| [**Grimm's conjecture**](conjectures/grimm/) · [page ↗](https://fabianarevalo.com/grimm) | active | 1 | **CERTIFIED** — verified for all n ≤ 10¹² (52× the 2006 record), with the first census of *critical* gap members: **18,575,022** of them factored, matched, with exact Hall margins — no margin negative, and **every Hall-tight gap below 10¹² is prime-power tight** (the largest holds 31⁸; interaction tightness, the only way Grimm can fail, never occurs in range); plus **PROVED** tight gaps recur infinitely often (2^a, a ≡ 3 mod 6) |
| [**Mixed van der Waerden numbers**](conjectures/vdw-mixed/) · [page ↗](https://fabianarevalo.com/vdw-mixed) | active | 1 | **CERTIFIED** — first proof-carrying derivations of seven cells of the mixed van der Waerden table (through `w(2;4,7)=109`, an 18.4M-line RUP-verified proof, and `w(2;5,5)=178`; the published values shipped no checkable certificates), plus the first bound on the open cell past Ahmed's 2013 frontier: **`w(2;5,8) > 295`** via an exactly-74-periodic witness passing two independent verifiers, with the extremal-witness periodicity structure (0/1/many defects along the ladder) mapped and a resumable cube-and-conquer campaign opened |
| [**Peaceable queens**](conjectures/peaceable-queens/) · [page ↗](https://fabianarevalo.com/peaceable-queens) | active | 1 | **CERTIFIED** — **a(16) = 37**: the smallest open case of OEIS A250000 decided (the bracket had been [37, 64] since 2014) via a 5.03×10⁹-node exhaustive refutation of 38+38 and a verified 37+37 witness, from a **PROVED** line-labeling reformulation with proved pruning lemmas; plus the whole ladder a(1..15) re-derived from scratch — the first reproducible derivation artifacts for a(14) = 28 and a(15) = 32 |
| [**Undirected repetition thresholds**](conjectures/undirected-thresholds/) · [page ↗](https://fabianarevalo.com/undirected-thresholds) | active | 1 | **PROVED** — for every `n ≥ 5` the longest word over `n` letters with no undirected repetition of exponent `≥ (n−1)/(n−2)` has length exactly **`n+3`**, with a unique extremal word — an elementary sharp form of the Currie–Mol lower bound `URT(n) ≥ (n−1)/(n−2)` — plus a finite-check descent criterion (Theorem D) and exact Pansiot reversal-transfer identities; **CERTIFIED** at the open case `k = 22`: a quadruply-verified `(21/20)⁺`-free word of length **20 000**, and emptiness of both the binary Pansiot class and the whole affine-morphism ansatz |
| [**Strong truncations (Kardoš P4.1)**](conjectures/strong-truncations/) · [page ↗](https://fabianarevalo.com/strong-truncations) | active | 1 | **PROVED + CERTIFIED** — the diamond-free claw-free phrasing of Kardoš's 2025 strong-edge-coloring problem is **false as posed**: a proved local obstruction (Balloon Lemma) and **G₁₈**, the unique smallest claw-free diamond-free cubic graph with χ′ₛ = 7 (18 vertices, DRUP-certified, counterexamples at every admissible order ≥ 18, diamonds not needed for the tight 7). Every such counterexample is **bridged** (Prop. 6, proved), so the 2-edge-connected reading is untouched and instead supported: all 26,867 bridgeless quotients of order ≤ 16 are 6-colorable. Census of all 36,093 quotient multigraphs to order 16 finds **χ′ₛ = 7 ⟺ balloon, exactly**, and all 556,471 truncations of *simple* cubic graphs on ≤ 20 vertices are strongly 6-edge-colorable |
| [**Balanced colourings (Erdős #617)**](conjectures/balanced-colorings/) · [page ↗](https://fabianarevalo.com/balanced-colorings) | active | 1 | **PROVED + CERTIFIED** — first computational attack on the Erdős–Gyárfás balanced-colouring conjecture at its open frontier r = 5: a certified balanced 5-colouring of K₂₅ (affine plane, T(5) ≥ 25, verified over all 177,100 six-subsets); every colour class of a hypothetical K₂₆ witness proved a (6,6)-Ramsey graph, with the per-class counting barrier **sharp** — E*(10,4) = 31 misses the r = 3 threshold by one edge, E*(26,6) ≥ 265 vs threshold 260; the affine family proved non-extendable to K₂₆ (DRUP-certified) and **no vertex-regular witness exists** (Z₂₆ arithmetic + exhaustive D₁₃, 0/3,198 classes pass) — in contrast to r = 2, whose counterexample is a circulant; plus the r = 3 theorem machine-reproduced (3 s after symmetry breaking) and the direct instances diagnosed pigeonhole-hard (135-var UNSAT defeats four modern solvers) |
| [**Chromatic number of PG(7,2)**](conjectures/projective-chromatic/) | active | 1 | **PROVED + CERTIFIED** — first computational attack on χ₂(8) ∈ {5,6} (Bishnoi–Cames van Batenburg–Ravi Problem 1; 5 would give R(3;5) ≥ 257): **Theorem — every proper 5-coloring of PG(7,2), if any exists, has a 2-group automorphism group** (Mersenne orders 3/7/31/127 killed by a proved orbit obstruction valid for all n, k; orders 17 and 5 by certified UNSATs, the order-5 [C,I] leg with a rup_check-verified DRUP; provisos in NOTE §4) — while an order-5-invariant witness **exists at n = 7**, and 1,000/1,000 sampled hyperplane restrictions fail to extend (50 DRUP-certified) |
| [**Odd Giuga numbers**](conjectures/odd-giuga/) · [page ↗](https://fabianarevalo.com/odd-giuga) | active | 1 | **CERTIFIED + PROVED** — every odd Giuga number and every odd primary pseudoperfect number has **at least 14 prime factors**: exhaustion of `Σ1/pᵢ ± 1/n = 1` over all sets of ≤ 12 distinct odd primes plus a parity lemma (odd solutions have evenly many factors); equals the recorded 1996 Giuga bound with the first open certified derivation, and lifts the odd-PPN/Znám bound from 9; plus both even censuses (12 Giuga numbers, 8 PPNs, complete to 8 factors) reproduced exactly with a 29/29 independent verification, and the m = 13 wall quantified at ~10¹⁵ against 2.8×10¹⁰ for m ≤ 12 |

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
