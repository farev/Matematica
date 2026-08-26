# Strong truncations (Kardoš, C&C 2025, Problem 4.1)

**Statement.** Is every diamond-free claw-free cubic graph strongly
6-edge-colorable — equivalently (per the problem's own gloss), is
χ′ₛ(T(G)) = 6 for every cubic graph G, where T is truncation (replace
each vertex by a triangle)? Posed by F. Kardoš, *Open problems of the
33rd Workshop on Cycles and Colourings*, arXiv:2511.02892 (Nov 2025)
(secondary). Known before this session: χ′ₛ ∈ {6,7} for connected
claw-free cubic ≠ prism, tight examples all containing diamonds
(Lin–Lin (secondary)); truncated prisms are 6 (Han–Cui (secondary)).

**Status:** active — the diamond-free phrasing is **refuted**; the
characterization conjecture and the simple-quotient reading are open.
**Sessions:** [2026-08-26](../../log/2026-08-26-strong-truncations.md)

## Results (2026-08-26)

| Claim | Label | Where |
|---|---|---|
| Diamond-free claw-free cubic = K₄ ∪ {T(H) : H connected cubic loopless multigraph}, H unique (folklore-adjacent, flagged) | PROVED | NOTE §0 |
| Dart model: strong 6-colorings of T(H) ⟺ proper 6-edge-coloring of H + per-dart bijections with local disjointness; interface lemma for pendant pieces | PROVED | NOTE §1 |
| **Balloon Lemma**: H ⊇ balloon (doubled edge + common third neighbour = expanded loop) ⇒ T(H) has no strong 6-edge-coloring | PROVED | NOTE §2 |
| Dumbbell transfer relation: across a doubled edge with distinct stem ends, both stems export the same spare pair, stem colors distinct (180 labelled pairs, closed form = enumeration) | PROVED | NOTE §2 |
| **G₁₈** = T(H₆), 18 vertices, claw-free diamond-free cubic, **χ′ₛ = 7**: UNSAT@6 with DRUP proof checked by `tools/satcert/rup_check`, verified 7-coloring, both enumeration paths agree (canonical forms equal) | CERTIFIED (χ′ₛ ≥ 7 also PROVED via Balloon Lemma) | `certs/G18.*` |
| G₁₈ is the unique smallest (prism χ′ₛ = 9 aside); counterexamples exist at every DFCF-admissible order ≥ 18 (chain family, certified k ≤ 8, ≥ 7 proved for all k) | PROVED + CERTIFIED | NOTE §3, `data/family_results.txt` |
| Census of **all 36,093** truncations of cubic multigraphs of order ≤ 16: χ′ₛ = 6 for 29,787 (witness verified from the definition per instance, plus a conflict 6-clique ⇒ exactly 6); χ′ₛ = 7 for 6,305 = 1, 4, 19, 102, 682, 5497 by order (UNSAT@6 by two independent engines, verified 7-coloring each); **7 ⟺ balloon exactly** (sole balloon-free failure: triple edge → prism, χ′ₛ = 9) | CERTIFIED | `data/census*.txt`, `data/chi7_*.txt` |
| Intended reading verified: T(G) strongly 6-edge-colorable for **all 556,471 simple** connected cubic G on ≤ 20 vertices (T ≤ 60 vertices); 509,950 order-20 witnesses re-verified from the definition, 539 engine-capped instances SAT-resolved | CERTIFIED | `data/simpleq_*`, `data/simpleq20_*` |
| Conjecture C: for H ≠ triple edge, χ′ₛ(T(H)) = 6 ⟺ H balloon-free (open half: balloon-free ⇒ 6); GF(2) sufficient condition recorded | conjecture + PROVED partial | NOTE §4–6 |

Openness and novelty are asserted at **search-snippet confidence only**
(sandbox egress-blocked from arXiv/OEIS/erdosproblems/MO): every
citation here is (secondary), and the primary sources must be read
before any public claim. See NOTE §7.

## Scripts

| file | what it does | cost |
|---|---|---|
| `build_nauty.sh` | fetch + build nauty 2.8.8 generators (geng, multig, labelg) from the pynauty sdist on PyPI | 2 min |
| `strong6.c` | Engine A: builds T(H) from `multig -T` lines (or reads graph6 with `-g6`), exhaustive backtracking on the conflict graph; complete search, exact χ′ₛ escalation | µs–s per graph |
| `engine_b.py` | Engine B: independent construction + definition-level CNF + SAT (CaDiCaL/Glucose42), witnesses re-checked internally; `--proof` emits DRUP | ~0.1–2 s per graph |
| `verify_census.py` | third-implementation verifier: rebuilds each graph from the raw line, checks family membership (cubic, connected, claw/diamond-free), witness validity, and a conflict 6-clique; rejects corrupted witnesses (negative control in WRITEUP) | ~1 ms per record |
| `resolve_undecided.py` | pipeline stage 2: Engine-B decides capped records, independently confirms every NOT6 | |
| `chi7_pass.py` | verified 7-coloring for every NOT6 record ⇒ χ′ₛ = 7 certified per instance | |
| `dfcf_filter.py` | definition-level claw/diamond filter over geng output (independent enumeration path) | |
| `g6_to_T.py` | graph6 (simple cubic) → `multig -T` line, for the simple-quotient runs | |
| `certify_ce.py` | DRUP-certified UNSAT@6 + verified 7-witness for one graph6 (used for G₁₈) | seconds |
| `boundary.py` | boundary-state calculus: balloon states (zero), dumbbell relation (180), chain-family closure | 30 s |
| `make_family.py` | chain-family quotients C_k | instant |
| `classify.py` | tabulates verdict × balloon over census files; flags any off-diagonal instance | |

Reproduce (from inside this directory; `./build_nauty.sh` first):

```bash
gcc -O2 -o strong6 strong6.c
printf '2 1  0 1 3\n' | ./strong6                     # prism control: NOT6 chi=9
python3 certify_ce.py G18 'Q??CA?_cAOA_DC@`PO@OOOW?`_?'   # the counterexample
./geng -c -d1 -D3 -q 14 | ./multig -r3 -T -q | ./strong6 -cap 2000000 -nochi \
  > /tmp/c14.txt && python3 resolve_undecided.py /tmp/c14.txt > c14.txt \
  && python3 verify_census.py c14.txt                  # order-14 census end-to-end
python3 boundary.py                                    # balloon = 0 states
```

## Data and certificates

| file | what it is |
|---|---|
| `certs/G18.cnf`, `certs/G18.drup`, `certs/G18_7col.txt` | the 18-vertex counterexample: CNF, checked DRUP proof of UNSAT@6, verified 7-coloring |
| `data/census{02..16}.txt` | full census records with witnesses, orders 2–16 (every record re-verified; NOT6 lines carry A+B confirmation) |
| `data/chi7_upto14.txt`, `data/chi7_16.txt` | verified 7-colorings for all 6,305 χ′ₛ = 7 instances |
| `data/family_results.txt` | chain family C₀..C₈ verdicts |
| `data/boundary_states.txt` | balloon/dumbbell state enumeration output |
| `data/simpleq_{04..16}.txt`, `data/simpleq_18.txt.gz` | simple-quotient runs, orders 4–18, full records |
| `data/simpleq20_counts.txt`, `data/simpleq20_verify.txt`, `data/simpleq20_caps_resolved.txt`, `data/simpleq20_sample2000.txt` | order 20: engine counts, in-session verification record of all 509,950 witnesses, the 539 SAT-resolved caps, and a 2000-record verified sample. The full 205 MB record file is not committed (repo size rule); regenerate with `./geng -qc -d3 -D3 20 \| python3 g6_to_T.py \| ./strong6 -cap 5000000 -nochi` (~35 min on 4 cores) |

Engine anchors: C₅ = 5, C₆ = 3, C₇ = 4, K₃,₃ = 9, Petersen = 5,
prism = 9 (published values (secondary)) all reproduced. Generator
cross-check: geng/multig counts match A002851 / A000421 at every order
used (A000421 read from the oeisdata git mirror, primary text).

## Known defects and open threads

- All literature is (secondary): the sandbox cannot reach arXiv/OEIS
  proper. Read Kardoš, Lin–Lin, Han–Cui in the original and re-run the
  novelty search before any public claim; then consider a short arXiv
  note and/or writing Kardoš.
- Conjecture C's open half (balloon-free ⇒ 6). Tools in place: dumbbell
  transfer relation, GF(2) sufficient condition (NOTE §6).
- Order-18 multigraph census was still running at session close (not
  claimed here; see the log).
- The with-diamonds half of the claw-free class (which need 7 —
  Lin–Lin's characterization question) is a one-command pipeline
  extension, not run today.
- Counting sequence 1, 4, 19, 102, 682, 5497 not found in OEIS by
  search; check properly, consider submitting.
