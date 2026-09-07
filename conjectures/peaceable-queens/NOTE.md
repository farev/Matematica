# Certified computation for the peaceable queens problem

**Session date.** 2026-08-17. AI-assisted (Claude); disclosed per repo
policy. All proofs below were written and checked in-session; all
computations ran on the session sandbox (4 cores, 15 GB RAM, Ubuntu
24.04, gcc 13.3, cadical 1.7.3 apt binary, python-sat 1.8.dev17).

## Abstract

The peaceable queens number a(n) (OEIS A250000) is the largest m such
that m white and m black queens can be placed on an n × n board with no
queen attacking a queen of the opposite color. We give an exact
branch-and-bound in a line-labeling reformulation (Lemma 1), with all
pruning rules proved here (Lemmas 3–5) and a color-swap canonical form
(Lemma 6). Two independent implementations agree node-for-node; the
method is cross-validated against a SAT pipeline (40/40 verdict
agreements on all army sizes for n ≤ 8) whose boundary instances carry
DRUP proofs checked by an independent reverse-unit-propagation checker;
every SAT witness is re-verified by a from-the-definition checker
sharing no code with the search. With this machinery we re-derive the
complete known ladder a(1..15) from scratch — including a(14) = 28 and
a(15) = 32, for which we could locate no published proof artifact —
and then decide the smallest open case: **a(16) = 37** (Theorem D), by
an exhaustive 5.03-billion-node refutation of army size 38 paired with
a checker-verified 37 + 37 witness. The OEIS-recorded finite bracket
at n = 16 had stood at [37, 64] (Pratt 2014, (secondary)).

## 1. The problem

Queens attack along rows, columns and the two diagonal directions; in
this problem (Bosch 1999 (secondary); OEIS A250000) attacks are not
blocked by intervening pieces, so the constraint is simply that no white
queen and black queen share a row, column, or diagonal. Known exact
values (all (secondary): OEIS A250000; Clinch–Drescher–Huynh–Saffidine,
arXiv:2406.06974, state that only the first 15 terms are known):

    n     1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    a(n)  0  0  1  2  4  5  7  9  12 14 17 21 24 28 32

a(1)–a(13) were confirmed by Rob Pratt by integer programming
(2014-12-01, OEIS entry (secondary)); Pratt recorded only bounds for
n = 14..20, namely 28 ≤ a(14) ≤ 43, 32 ≤ a(15) ≤ 53, 37 ≤ a(16) ≤ 64,
42 ≤ a(17) ≤ 72. The values a(14) = 28, a(15) = 32 are reported as
known in arXiv:2406.06974 (secondary); from this sandbox we could not
determine who first established them or locate a proof artifact for
them, and we phrase our contribution for those two values as an
independent derivation. Lower bounds for n ≤ 30 come from Ainley's 1977
constructions, never surpassed except at n = 27 (secondary). The best
published upper bound of the right order is a(n) ≤ (2 − √2)/2 · n² ≈
0.1716 n² **for all sufficiently large n** (arXiv:2406.06974
(secondary)); it is asymptotic and, as far as we can tell from the
abstract and snippets, not claimed at n = 16.

Everything below is self-contained: no external value is assumed
anywhere in the computations; the published ladder is used only as a
cross-check after the fact.

## 2. The line-labeling reformulation

Index lines: rows r ∈ [0, n), columns c ∈ [0, n), sum-diagonals
s = r + c ∈ [0, 2n − 1), difference-diagonals d = r − c + n − 1 ∈
[0, 2n − 1). Every cell lies on exactly one line of each of the four
families. Call a placement *peaceable* if no white and black queen
share a line.

**Lemma 1 (reformulation).** For m ≥ 1, the following are equivalent:

1. there is a peaceable placement with ≥ m white and ≥ m black queens;
2. there is a labeling ℓ of all 6n − 2 lines by {W, B} such that at
   least m cells have all four of their lines labeled W, and at least
   m cells have all four labeled B.

*Proof.* (1 ⇒ 2) Fix a peaceable placement. No line contains both
colors, so the partial labeling "label a line by the color it contains"
is well defined; label queen-free lines arbitrarily, say W. Every white
queen's four lines contain a white queen, hence are labeled W; so every
white queen sits on an all-W cell, giving ≥ m all-W cells; likewise
black.

(2 ⇒ 1) Given ℓ, place a white queen on every all-W cell and a black
queen on every all-B cell. No cell is both (its row cannot be labeled
both ways). If a white and a black queen shared a line, that line would
be labeled both W and B, impossible. So the placement is peaceable,
with ≥ m queens of each color; discard extras to make the armies equal.
∎

Consequently a(n) = max over labelings of min(#all-W cells, #all-B
cells), and deciding "a(n) ≥ m" is a finite search over 2^(6n−2)
labelings. The search below organizes this as: choose the row labels
(a set S of W-rows), then the column labels T, then the two diagonal
families by depth-first search.

Given (S, T), call WG = S × T the *white grid* (cells whose row and
column are both W) and BG = S̄ × T̄ the *black grid*. During the
diagonal DFS, a WG cell is *live* if neither of its diagonals is
labeled B; a BG cell is live if neither is labeled W. Write w = #live
WG cells, b = #live BG cells for the current node.

**Lemma 2 (leaf test).** If at some node every unlabeled diagonal has
live cells of at most one color, then the labeling can be completed so
that exactly the live cells are the all-W (resp. all-B) cells. In
particular, if also w ≥ m and b ≥ m, condition (2) of Lemma 1 holds.

*Proof.* Label each unlabeled diagonal by the color of its live cells
(arbitrarily if none). This kills no live cell: a live white cell dies
only when one of its diagonals is labeled B, but any unlabeled diagonal
through a live white cell has a live white cell on it, hence was
labeled W; symmetrically for black. Dead cells stay dead (labels are
never retracted). A live white cell now has row and column in S, T
(labeled W) and both diagonals labeled W, so it is all-W. ∎

## 3. Pruning bounds

All bounds are exact integer statements about any completion of the
current partial labeling; each is checked at every node.

**Lemma 3 (product bound).** Any labeling with ≥ m all-W and ≥ m all-B
cells has m ≤ |S|·|T| and m ≤ (n − |S|)(n − |T|), where S, T are the
W-labeled rows and columns.

*Proof.* All-W cells lie in S × T, which has |S|·|T| cells; all-B cells
lie in S̄ × T̄. ∎

**Lemma 4 (cell bound / monotonicity).** In any completion of the
current node, the all-W cells form a subset of the currently live WG
cells; hence if w < m or b < m the node is dead.

*Proof.* Labeling more diagonals can only kill cells, never revive
them: a cell with a B-labeled diagonal has that label forever. ∎

**Lemma 5 (family-sum bound).** Fix one diagonal family (say the
sum-diagonals). In any completion, every all-W cell lies on exactly one
sum-diagonal, which must be labeled W, and then contributes no all-B
cell to that diagonal. Hence, writing aw(s), ab(s) for the numbers of
currently live WG/BG cells on diagonal s,

    (#all-W) + (#all-B) ≤ Σ_s  cap(s),   where
    cap(s) = aw(s) if s is labeled W, ab(s) if labeled B,
             max(aw(s), ab(s)) if s is unlabeled.

If Σ_s cap(s) < 2m the node is dead. The same holds for the
difference-diagonal family.

*Proof.* In the completion, diagonal s labeled W carries only all-W
cells, all of which are live now (Lemma 4), so it carries ≤ aw(s) of
the total; likewise labeled-B diagonals carry ≤ ab(s). Unlabeled s
ends up one or the other, carrying ≤ max(aw(s), ab(s)). Summing over
the family counts every all-W and all-B cell exactly once. ∎

**Lemma 6 (canonical form).** If some labeling has ≥ m all-W and ≥ m
all-B cells, then some labeling with row 0 labeled W does.

*Proof.* If not already so, swap the two labels everywhere; all-W and
all-B cells exchange, both counts still ≥ m. ∎

**Lemma 6′ (orbit canonical form, SYM16 engine).** Let G be the group
(order 16) generated by row reversal, column reversal, transposition,
and the color swap. Each g ∈ G maps a labeling to a labeling with the
same pair {#all-W, #all-B} (as a set), because the three board maps
are bijections of the board sending lines to lines (row reversal maps
rows to rows, columns to columns, and exchanges the two diagonal
families up to index reversal; similarly for the others), and the
color swap exchanges the two counts. The induced action on the pair
(S, T) = (W-rows, W-cols) is: (S,T) ↦ (Ŝ, T̂), (Ŝ, T̂) ∈
{(A,B), (B,A), (Ā,B̄), (B̄,Ā) : A ∈ {S, rev S}, B ∈ {T, rev T}},
which is exactly the 16 keys tested by the engine. Hence if any
labeling achieves both counts ≥ m, so does one whose (S,T) is
key-minimal in its G-orbit, and it suffices to run the diagonal DFS
only at key-minimal pairs. ∎

The plain engine uses Lemma 6 (color swap only, "row 0 is white"); the
SYM16 engine uses Lemma 6′. Both were validated to give identical
verdicts on every boundary instance of the ladder (16/16 instances,
n = 3..13, both sides); node counts are intentionally comparable only
within one engine variant.

The search enumerates all S ∋ row 0, all T, and DFS over diagonals,
branching only on diagonals with live cells of both colors (by Lemma 2
none remaining means SAT), always checking Lemmas 3–5. It is therefore
exact: "UNSAT at m" proves a(n) ≤ m − 1, and "SAT at m" comes with an
explicit witness. Branching heuristic (does not affect correctness):
pick the unlabeled diagonal maximizing min(aw, ab), scanning
sum-diagonals before difference-diagonals, ascending index, first
maximum; try W before B.

## 4. Verification architecture

1. **Two implementations, node-count equality.** A pure-Python
   reference (`bnb.py`) and a C port (`bnb.c`) with intentionally
   identical semantics (same canonical form, bounds, branching rule,
   node accounting). On the validation battery (all boundary instances
   n ≤ 8, both SAT and UNSAT sides) they return identical verdicts with
   identical node counts (156 / 200 / 4178 / 16796 / 107042 on
   n = 5..8 boundaries; full table in `results/`).
2. **SAT cross-validation.** An independent CNF encoding of the
   *original* cell-level definition (`encode.py`; pairwise line-sharing
   clauses, same-cell exclusion, sequential-counter cardinality) and a
   second CNF encoding of the line-labeling formulation
   (`encode_lines.py`) were solved with CaDiCaL. The B&B agrees with
   the SAT verdicts on all 40 instances (n = 3..8, every m up to
   a(n) + 2): `results/validation_bnb_vs_sat.csv`.
3. **DRUP-certified anchors.** For n = 3..7 the boundary UNSAT
   instances (cell-level encoding, m = a(n) + 1) were solved by
   `cadical --plain` with proof logging, and each proof was verified by
   the repo's from-the-definition RUP checker
   (`tools/satcert/rup_check.c`); the SAT sides ship witness files.
   Certificates in `certs/`.
4. **Independent witness checking.** Every witness (from SAT models or
   B&B leaves) is verified by `check_peaceable.c`, which re-derives all
   attacks by scanning every white–black pair from the definition and
   shares no code with either encoder or the B&B. This checker caught
   a genuine bug during the session: the first B&B witness extractor
   read the live-sets after DFS unwinding had restored them (90
   attacking pairs at n = 11). Verdicts were unaffected (they had been
   validated separately); the extractor now snapshots at the SAT leaf,
   and every witness in `witnesses/` passes the checker.
5. **No external inputs.** The engines take (n, m) only. Published
   values enter solely as post-hoc cross-checks.

## 5. Results: the known ladder, re-derived from scratch

**Theorem A (CERTIFIED).** For 1 ≤ n ≤ 15, the peaceable queens numbers
are a(1..15) = 0, 0, 1, 2, 4, 5, 7, 9, 12, 14, 17, 21, 24, 28, 32,
with explicit witnesses (in `witnesses/`, all checker-verified) and
exhaustive B&B refutations at m = a(n) + 1.

This agrees with every published value (a(1)–a(13): Pratt via ILP,
(secondary)) and gives what appears to be the first independently
reproducible derivation with published artifacts for a(14) = 28 and
a(15) = 32 (see §1 caveat on their provenance). Runtimes in
`results/ladder_bnb.csv`. The largest refutations: a(13) at m = 25,
477,786,646 nodes, 99 s serial (plain engine; identical total from the
4-way stride partition); a(14) at m = 29, 2,264,952,960 nodes, 231 s
wall on 4 workers (plain); a(15) at m = 33, 1,476,498,420 nodes, 156 s
wall on 4 workers (SYM16 engine, 8 resumable chunks, all UNSAT).

## 6. Results at the open case n = 16

**Theorem B (CERTIFIED).** a(16) ≥ 37: the engine found a 37 + 37
peaceable placement on 16 × 16 (177,220,136 nodes, 29 s, plain
engine), independently of Ainley's construction; the witness
(`witnesses/witness_n16_m37.txt`) passes the from-definition checker.

**Theorem C (CERTIFIED).** a(16) ≤ 41: exhaustive refutation of army
size 42 by the SYM16 engine — 607,406,702 nodes, 174 s wall on 4
workers, 8 resumable chunks, every chunk UNSAT
(`results/n16_m42_bnb_sym_chunk*.txt`). The best previously recorded
finite upper bound at n = 16 was a(16) ≤ 64 (Pratt 2014, OEIS,
(secondary); the 0.1716 n² bound of arXiv:2406.06974 is asymptotic
only). This tightens the recorded bracket from [37, 64] to [37, 41].

**Theorem D (CERTIFIED).** a(16) = 37. The upper half is the
exhaustive refutation of army size 38: SYM16 engine, 16 resumable
chunks, every chunk UNSAT, 5,032,610,558 nodes in 462 s wall on 4
workers (`results/n16_m38_bnb_sym_chunk*.txt`); the lower half is
Theorem B's verified witness. The sym engine also reproduces the
witness (89,333,324 nodes, 17 s, same canonical row/column sets
S = 127, T = 3615). A full second exhaustion of m = 38 by the plain
engine (independent canonical form — color swap only, Lemma 6 — and an
independent outer-loop code path) **completed and agrees**:
45,021,245,984 nodes, 3691 s wall on 4 workers, all 16 chunks UNSAT
(`results/n16_m38_bnb_chunk*.txt`). The node ratio between the two
exhaustions, 45,021,245,984 / 5,032,610,558 ≈ 8.95, matches the
symmetry-group order ratio 16/2 = 8 up to orbit boundary effects — an
internal consistency check on the canonicalization.

To our knowledge — with the connectivity caveats of §1, and the OEIS
entry and the 2024 survey as the ledger — this is the first
determination of a(16), the smallest open case of A250000. It confirms
the value conjectured from Ainley's construction and extends the
exact-value table of Clinch–Drescher–Huynh–Saffidine (secondary).

## 6b. Results at n = 17 (session 2, 2026-09-03)

**Theorem E (CERTIFIED).** a(17) ≤ 42: exhaustive refutation of army
size 43 by the SYM16 engine — 21,454,699,264 nodes, 1712 s wall on
4 workers (6,086 s of engine time; largest chunk 2.56·10⁹ nodes, 588 s),
16 resumable chunks, every chunk UNSAT
(`results/n17_m43_bnb_sym_chunk*.txt`; driver log
`results/n17_m43_run.log`). The best previously recorded finite upper
bound was a(17) ≤ 72 (Pratt 2014, OEIS, (secondary)).

**Theorem F (CERTIFIED).** a(17) ≥ 42: the 42 + 42 placement published
by Kamenetsky in the OEIS A250000 link file `a250000_3.txt` (15 Oct
2019, attributing the value to Ainley 1977; fetched 2026-09-03) passes
the from-definition checker: 42 white, 42 black, no attacking pair
(`witnesses/witness_n17_m42_kamenetsky.txt`). Independently, the SYM16
engine found a 42 + 42 placement of its own (`./bnb_sym 17 42`:
678,816,342 nodes, 116 s, canonical row/column sets S = 255, T = 7199),
also checker-verified (`witnesses/witness_n17_m42.txt`); it is a
different placement from Kamenetsky's. The plain engine reproduces the
same placement (same S, T) in 1,357,765,356 nodes, 212 s
(`results/n17_m42_sat_plain.txt`).

**Corollary.** a(17) = 42, confirming Ainley's 1977 value and
⌊7·17²/48⌋ = 42.

*Growth and caveat.* The boundary refutation cost ×4.26 in nodes over
n = 16 (5.03·10⁹ → 2.15·10¹⁰) and ×3.7 in wall time (462 s → 1712 s),
inside the ×3–5 per rung seen on the ladder; the sub-optimum hardening
feared at n = 15 did not appear. Unlike n = 16, the exhaustion was run on
**one engine only**: the plain-engine replication (independent canonical
form) is projected at ≈ 9× the SYM16 node count — about 1.9·10¹¹ nodes,
4–5 h on this hardware — and was not attempted in the session. Theorem E
therefore rests on Lemma 6′ and the §4 validation battery (plain/SYM16
agreement on every ladder boundary and on both n = 16 instances), not on
a second independent exhaustion.

## 6c. Results at n = 18 (session 3, 2026-09-04)

**Theorem G (CERTIFIED).** a(18) ≤ 47: exhaustive refutation of army
size 48 by the SYM16 engine — 119,110,352,726 nodes, 15,431 s wall on
4 workers (32,695 s of engine time; largest chunk 14,077,925,460 nodes,
2,838 s (slowest chunk 3,150 s); smallest 455,221,604 nodes), 16 resumable chunks, every chunk
UNSAT (`results/n18_m48_bnb_sym_chunk*.txt`; driver log
`results/n18_m48_run.log`). The best previously recorded finite upper
bound was a(18) ≤ 81 (Pratt 2014, OEIS, (secondary)).

**Theorem H (CERTIFIED).** a(18) ≥ 47: the placement published by
Kamenetsky in the OEIS A250000 link file `a250000_3.txt` (2019,
attributing the value to Ainley 1977; fetched 2026-09-04) carries 47
white and 48 black queens with no attacking pair and passes the
from-definition checker (`witnesses/witness_n18_m47_kamenetsky.txt`);
deleting any black queen leaves a 47 + 47 placement.

**Corollary.** a(18) = 47, confirming Ainley's 1977 value and
⌊7·18²/48⌋ = 47.

*Growth and caveats.* The boundary refutation cost ×5.55 in nodes over
n = 17 (2.15·10¹⁰ → 1.19·10¹¹), above the ×4 projected from the n = 16 → 17
step but inside the ladder's range; the wall time (15,431 s against 1712 s
at n = 17) is not comparable because the cores were shared with other jobs
of the session for about two of the four hours (engine time 32,695 s is
the honest figure). As at n = 17 the exhaustion was run on **one engine
only**: the plain-engine replication is projected at ≈ 9× the SYM16 node
count (≈ 1.1·10¹² nodes, ≈ 25 h on this hardware) and was not
attempted; Theorem G rests on Lemma 6′ and the §4 validation battery. No
engine search for a 47-witness was run this time: the lower bound is the
checker-verified literature placement alone.

## 7. Open questions

1. ~~a(17)~~ Done in session 2 (§6b): a(17) = 42. ~~a(18)~~ Done in
   session 3 (§6c): a(18) = 47. Next rung: a(19), recorded bracket
   [52, ?] (Ainley's 52 = ⌊7·19²/48⌋; secondary). At ×4–5 per rung the
   m = 53 refutation is ≈ 5.4–6.6·10¹¹ nodes, 13–16 h on 4 dedicated
   cores. Also pending: the plain-engine replications of the n = 17 and
   n = 18 refutations (≈ 4–5 h and ≈ 25 h), to restore the
   two-engine standard of n = 16.
2. The B&B's family-sum bound (Lemma 5) treats the two diagonal
   families independently. A joint bound (e.g. LP over both families)
   would cut deeper near the optimum; can it be kept exact and cheap?
3. Port the engine to the torus (A279405), where the odd case is
   reported open (Harries 2026 is reported to have settled even tori
   with an exact parity formula (secondary); unread from this sandbox).
4. Submit a(16) = 37 to OEIS A250000 (with the witness and the chunk
   certificates as the linked artifacts) — a decision for the local
   session, per repo policy on external submissions.

## Reproducibility

    gcc -O2 -march=native -o bnb bnb.c
    gcc -O2 -o check_peaceable check_peaceable.c
    ./bnb 15 33            # UNSAT => a(15) <= 32
    ./bnb 15 32            # SAT + witness => a(15) >= 32
    ./bnb 15 32 | tail -n +2 | ./check_peaceable
    python3 drive.py 16 44 # 4-way parallel UNSAT run
    python3 validate_bnb.py

cadical is deterministic for fixed input and options; the B&B is
deterministic; no seeds anywhere. Runtime/host details per run in
`results/`.
