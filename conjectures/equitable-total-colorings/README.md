# Equitable 4-total colourings of small cubic graphs (Adauto–de Figueiredo–Sasaki–Schneider, Question 7.1, 2026)

A total colouring colours vertices and edges so that adjacent or incident elements get
different colours; a cubic graph is Type 1 if 4 colours suffice. A 4-total colouring is
*equitable* if its four colour classes (counted over all `5n/2` elements) differ in size
by at most one, and `χ''_e` is the least number of colours of an equitable total
colouring. Dantas et al. exhibited a Type 1 cubic graph `R` of order 20 with
`χ''_e(R) = 5`, and arXiv:2609.05259 (4 Sep 2026) asks, as Question 7.1, whether every
Type 1 cubic graph of order less than 20 admits an equitable 4-total colouring —
equivalently, whether `R` has minimum order — remarking that the question "is within
reach of a systematic computational verification over the catalogue of connected cubic
graphs of order at most 18". It was: one SAT instance per graph, with checkable proofs.

Page: *(none yet — `PAGE.md` is the handoff)*.

**Status:** active (hedge computation of the 2026-09-08 session, run by a subagent)
**Sessions:** 2026-09-08

## Results

| Claim | Label | Where |
|---|---|---|
| Question 7.1 has a **negative** answer: exactly 23 connected Type 1 cubic graphs of order < 20 have `χ''_e = 5` — 16 of order 16 and 7 of order 18 (three bipartite); every Type 1 cubic graph of order ≤ 14 has an equitable 4-total colouring; the minimum order is 16, not 20 | CERTIFIED (every SAT witness independently verified; every equitable-UNSAT with DRUP proofs checked by `tools/satcert/rup_check`, with and without symmetry breaking; SAT-free enumeration agrees) | NOTE §3–4, `data/cx_n16.g6`, `data/cx_n18.g6`, `certs/` |
| Census of connected cubic graphs of order ≤ 18 by type: Type 2 counts 1, 1, 1, 10, 25, 48, 227, 2103 for `n = 4, …, 18`, every Type 2 verdict DRUP-certified | CERTIFIED | `data/t2_n*.g6`, `certs/cert_type2_*.json` |
| Every 4-total colouring of each order-16 counterexample has colour-class configuration (11,10,10,9) (16 to 240 colourings each, enumerated) | CERTIFIED (SAT-free enumeration) | `data/brute_cx16_all.txt` |
| Order 20, 3 of 10 generator residue classes (161 130 of 510 489 graphs): 20 further Type 1 graphs with `χ''_e = 5`, all with configuration (14,12,12,12) like `R` | CERTIFIED per graph, partial census | `data/cx_n20.g6`, `certs/cert_cx_n20_*.json` |

See [`NOTE.md`](NOTE.md) for the definitions as read from the paper and the certification
scope, [`WRITEUP.md`](WRITEUP.md) for the narrative including what failed.

## Scripts

| file | what it does | cost | headline output |
|---|---|---|---|
| `code/tc.py` | definition-level SAT encoding of (equitable) 4-total colouring; CaDiCaL verdicts, Glucose DRUP proofs | ms per graph | — |
| `code/verify_tc.py` | independent witness checker written from the definition | — | — |
| `code/scan.py`, `code/scan20.py` | the census over `geng -c -d3 -D3 n` (nauty 2.8.8 built from the pynauty sdist) | `n ≤ 18`: 411 s, one core | `data/results_n*.tsv`, `data/summary_n*.json` |
| `code/cert.py`, `code/cert_nosb.py`, `code/post.sh` | DRUP proof generation and `rup_check` verification, with and without symmetry breaking | 8 min | `certs/*.json` |
| `code/brute.py` | SAT-free backtracking enumerator of all 4-total colourings (optionally equitable only) | seconds per graph | `data/brute_*.txt` |
| `code/controls.py` | positive controls: K4, K3,3, ladders, Petersen, generalized Petersen, the paper's H16/H18 certificates, `R` reconstructed from its Figure 1 | seconds | all match the paper |

Run from inside this directory (needs python-sat, nauty's `geng`, and the compiled
`tools/satcert/rup_check`):

```bash
cd conjectures/equitable-total-colorings/code
python3 brute.py --equitable "$(head -1 ../data/cx_n16.g6)"   # 0 equitable colourings
python3 brute.py "$(head -1 ../data/cx_n16.g6)"               # all 4-total colourings, configuration (11,10,10,9)
python3 scan.py 16                                             # the order-16 census (30 s)
```

## Data and certificates

| file | produced by | what it is |
|---|---|---|
| `data/cx_n16.g6`, `data/cx_n18.g6` | `scan.py` | the 23 counterexamples (graph6) |
| `data/cx_n20.g6` | `scan20.py` | 20 order-20 examples from 3 of 10 residue classes (partial) |
| `data/t2_n*.g6` | `scan.py` | all Type 2 connected cubic graphs of order ≤ 18 |
| `data/results_n*.tsv`, `data/summary_n*.json` | `scan.py` | per-graph verdicts and per-order counts |
| `certs/proofs_counterexamples/*.drup` | `cert.py`, `cert_nosb.py` | the 48 checked DRUP proofs for the 23 counterexamples (with and without symmetry breaking) and for `R` (13.6 MB) |
| `certs/cert_*.json` | `cert.py`, `cert_nosb.py` | proof manifests (file, lines, seconds) for all 4 920 checked proofs; the 4 832 Type 2 proofs (520 MB) are not committed — regenerate with `post.sh` |
| `data/brute_*.txt` | `brute.py` | SAT-free cross-checks |
| `data/oeis_A002851.txt` | OEIS | the cubic-graph counts used to validate `geng` |

## Known defects and open threads

- **Priority is unchecked.** Adauto's 2022 M.Sc. dissertation [1 in the paper] and
  Stemock [9] were not accessible; the paper says the orders ≤ 18 were *not* checked,
  but the 23 graphs could appear elsewhere. Verify before claiming novelty.
- `R` was reconstructed from Figure 1 of the paper (two outer ports clipped, their
  colours forced); its isomorphism with the graph of Dantas et al. (DAM 209) is not
  verified, only its stated properties (Type 1, no equitable 4-total colouring, the
  Figure-1 colouring valid with configuration (14,12,12,12)).
- Type 2 verdicts at order 20 are solver verdicts without proofs; the order-20 census
  covers 3 of 10 residue classes and `R`'s class was not scanned.
- SAT witnesses were verified in-process but not stored; `scan.py` regenerates them.
- Connected graphs only (the paper's own reduction, quoted in NOTE §1); the
  counterexamples are connected, so the negative answer does not depend on it.

## Prior work

- arXiv:2609.05259 (Adauto, de Figueiredo, Sasaki, Schneider, 4 Sep 2026): Question 7.1
  and Theorems 4.1, 5.3, 5.4 on the possible class configurations (all consistent with
  the census). Read in full on 2026-09-08.
- Dantas, de Figueiredo, Mazzuoccolo, Preissmann, dos Santos, Sasaki (DAM 2016, [5] in
  the paper): the graph `R` (secondary; not accessible).
- OEIS A002851 (connected cubic graphs), fetched live.
