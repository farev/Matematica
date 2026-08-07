# PAGE.md — handoff for the site build (new page: fabianarevalo.com/generalized-schur)

New conjecture directory; no existing page. Session 2026-08-07.
*(NUMBERS FROZEN AT: mid-session — rebuild the tables from
`data/new_values.csv` at page-build time; the counts below are a floor.)*

## 1. Headline claim

**CERTIFIED** — the first new exact generalized Schur numbers since 2016:
at least six values `S(3;s,t,u)` never before computed, each shipped with a
machine-checkable certificate on both sides of the boundary (a DRUP
unsatisfiability proof at `S`, verified by an independent checker, and an
explicit valid coloring at `S−1`, verified by an independent algorithm), on
4 CPU cores in seconds-to-minutes per value.

## 2. Contributions (labels per repository convention)

1. **CERTIFIED** — new exact values (final list in `data/new_values.csv`):
   `S(3;4,4,8) = 87` and `S(3;4,4,9) = 98`, each **confirming a previously
   open instance of Ahmed–Schaal Conjecture 2.1** (`S = stu−tu−u−1`);
   `S(3;3,3,8) = 59`, `S(3;3,3,9) = 68`, `S(3;3,4,8) = 67`,
   `S(3;3,5,8) = 91` in the `s = 3` family, where **no formula is known or
   conjectured** (Song–Mao proved only a strict lower bound in April 2026).
2. **CERTIFIED** — complete extremal structure of the `(3,3,u)` family at
   every computed size: for `u ∈ {4,5,6,8,9}` the valid colorings of
   `[1, 9u−14]` are exactly one mirror-symmetric skeleton with `u−2` free
   ternary slots at positions `2u+1+5j` — `2·3^{u−2}` colorings — with
   maximal `L(u)`-class exactly `5(u−2)`; **at `u = 7` every regularity
   breaks except the class law**: `S = 49` sits one below the line, the 846
   extremals form no single skeleton, and the deficit belongs to the Schur
   pair (`23 = 4(u−1)−1` elements at maximum).
3. **Conjecture A (new)** — `S(3;3,3,u) = 9u−13` for all `u ≥ 4` except
   `u = 7`. NUMERICAL/CERTIFIED status: certified true at every computed
   `u`; open beyond.
4. **CERTIFIED** — the validation battery: 11 published boundary values
   reproduced with full certificates; all 12 published `(3,t,u)` values
   reproduced by independent climb; all ten enumeration counts of
   Ahmed–Schaal Theorems 2.1–2.10 matched exactly (18, 54, 162, 846, 8, 1,
   112, 96, 3584, 9488), including the unique `(3,4,5)` extremal coloring
   **matching the paper's printed string character for character**.

## 3. Figure specs

1. **The value grid.** Data: `data/published_values.csv` +
   `data/new_values.csv`. A `(t,u)` grid per `s`, gray cells = the entire
   published knowledge (2016), colored cells = values first computed in this
   session, each labelled with `S`. *Reader sentence: "Every colored cell is
   a number that did not exist in the literature this morning."*
2. **The `(3,3,u)` line and the u=7 dip.** Data: the `t=3` row of the same
   files: (3,14),(4,23),(5,32),(6,41),(7,49),(8,59),(9,68)…. Plot `S` vs
   `u` with the line `9u−13`; every point on the line except `u=7`, one
   below. *Reader sentence: "The family follows a perfect line at every
   computed size except 7, where exactly one element goes missing."*
3. **Skeletons.** Data: `data/skeletons_33u.txt`. Monospace stack of the
   five skeletons, free slots highlighted, u=7 row struck through with
   "no skeleton exists". *Reader sentence: "At every size but 7, all
   extremal colorings are one rigid pattern with u−2 free cells."*

## 4. Caveats the page must carry

- The Ahmed–Schaal paper (the publication boundary and all controls) was
  read as the **author preprint** self-hosted on GitHub; page range and
  abstract match the Experimental Mathematics listing (primary,
  session-verified). The Song–Mao result is **(secondary)** — verbatim
  abstract via an arXiv-RSS mirror; the Boza–Marín–Revuelta–Sanz diagonal
  theorem is **(secondary)** — search digest, `k`-range inferred. Minor
  venues (INTEGERS full texts, theses, MathSciNet) were unreachable; an
  isolated value there could predate one of ours — phrased as "first since
  Ahmed–Schaal (2016) as far as the reachable record shows".
- Conjecture A is certified only at the computed sizes; the page must not
  imply it is proved.
- SAT verdicts are Glucose 4.2; UNSAT sides carry DRUP proofs checked by an
  independent checker; SAT sides carry witnesses checked by an independent
  algorithm; CNFs regenerate deterministically (sha256 in
  `data/results_a1.csv`, `data/cnf_hashes.txt`).

## 5. Existing page

None — this is a new conjecture directory and a new page. Add the row to
the top-level README index (done in-session) and link both ways.
