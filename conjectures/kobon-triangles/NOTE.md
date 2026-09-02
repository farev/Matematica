# Triangles in simple arrangements of 18 pseudolines: the open entry of Bartholdi–Blanc–Loisel

*Research note, 2026-09-02. AI-assisted (Claude); see the repository README for the
disclosure policy. Result labels follow the repository convention
(PROVED / CERTIFIED / NUMERICAL).*

## Abstract

For a simple arrangement of `n` pseudolines in the Euclidean plane let `a^s_3(n)` be the
maximum number of bounded triangular faces. Bartholdi, Blanc and Loisel (2008) proved
`a^s_3(n) ≤ ⌊n(n − 7/3)/3⌋` for even `n` and tabulated `a^s_3(n)` for `n ≤ 30`; the
first entry their computation could not close is `n = 18`, where they report
`93 ≤ a^s_3(18) ≤ 94` (Bader's straight-line arrangement gives 93). We encode simple
Euclidean pseudoline arrangements as rank-3 signotopes (Felsner–Weil), express the
triangle count through the `n(n−2)` bounded segments, derive from BBL's own counting
argument that a 94-triangle arrangement of 18 pseudolines would have exactly twelve
"perfect" lines and six lines carrying exactly one unused segment each, and decide the
resulting instance by cube-and-conquer over the 561 dihedral orbits of the six-line set,
every cube carrying a DRAT proof checked by `drat-trim`.

**Prior work, found mid-session (rule 3).** The entry is *not* open. Blanc (arXiv:0801.2845,
Geombinatorics 21 (2011) 5–17), Theorem 1, proves `a_3(A) ≤ n(n − 5/2)/3` for
`n ≡ 0, 4 (mod 6)`, which is 93 at `n = 18`, and his Theorem 3 states that this bound is
reached for every `n ≤ 30` except `n = 11, 12`. So `a^s_3(18) = 93` has been a theorem
since 2008 and the computation reported here is an **independent, machine-checked
rediscovery** of one instance of it, by a method (signotope SAT + equality-case cubes)
unrelated to Blanc's. What remains open at `n = 18` is the Kobon number for arrangements
*with* concurrent triples or parallels; see §9 for what the literature actually proves
about that.

**Result (§7).** All 561 cubes are UNSAT (5.0 core-hours, median 18 s, hardest 585 s);
all 561 DRAT proofs were `drat-trim`-verified (8.2 core-hours). The pipeline's controls
(§8) reproduce every value of BBL's table for `n ≤ 16`. §9 records an audit of the upper-bound column of OEIS A006066.

## 1. The problem

Kobon Fujimura's triangle problem asks for the largest number `K(n)` of non-overlapping
triangles formed by `n` straight lines in the plane (OEIS A006066). The triangles in
question are the bounded triangular faces of the arrangement. Two relaxations are
standard: allow pseudolines instead of lines, and restrict to *simple* arrangements (no
three lines concurrent, all pairs crossing). Bartholdi–Blanc–Loisel [BBL] write
`a^s_3(n)` for the simple pseudoline maximum in the affine plane and prove

> **Theorem 1.1 [BBL].** If `n` is even then `a^s_3(n) ≤ ⌊n(n − 7/3)/3⌋`.

Their Theorem 1.4 tabulates `a^s_3(n)` for `n ≤ 30`, exact for `n ≤ 17` and for odd
`n ≤ 29`, with two-value entries where their depth-first search (their §4) could not
finish: `93–94` at `n = 18`, `116–117` at `n = 20`, `143–144` at `n = 22`, and so on.
They say explicitly that "as the unused edge budget increases, the search quickly
becomes intractable when looking for imperfect arrangements" (§5). At `n = 18` the
bound is `18·(47/3)/3 = 94`, an integer, so 94 triangles would use `282` of the `288`
bounded segments and leave an "unused edge budget" of six. This entry has stood since
the 2007 preprint (arXiv:0706.0723).

Recent activity concerns the straight-line problem: Savchuk (arXiv:2507.07951, 2025)
decides odd cases by a table-based SAT encoding (e.g. `K(11) = 32`, `K(23) = 161`,
`K(27) = 225`); Parpalak–Utkin (arXiv:2604.22035, 2026) give `K(20) = 117` and the
series `n = 18·2^t + 1`; Maiorana (OEIS A006066, Aug 2026) attains `K(14) = 54` *with
triple points*, one more than the simple-pseudoline value `a^s_3(14) = 53` of [BBL].
As of 2026-09-01 the OEIS entry lists `K(18) ≥ 93` with upper bound 94.

**Scope of this note.** We work with *simple* arrangements of *pseudolines*. Every
simple arrangement of straight lines is one, so a negative answer for pseudolines is a
negative answer for lines in general position; it says nothing about arrangements with
concurrent triples or parallel lines, which the Kobon problem allows and which [BBL]'s
Theorem 1.1 does not cover.

## 2. Signotopes

Label the pseudolines `1, …, n` by their vertical order at `x = −∞` (bottom to top);
since every pair crosses exactly once, the order at `x = +∞` is reversed.

**Definition.** A *3-signotope* on `[n]` is a map `σ` from 3-subsets `{i<j<k}` to
`{+, −}` such that for every 4-subset `a<b<c<d` the sequence
`σ(abc), σ(abd), σ(acd), σ(bcd)` changes sign at most once.

**Theorem 2.1 (Felsner–Weil [FW], Section 4).** Marked simple arrangements of `n`
pseudolines in the Euclidean plane are in bijection with 3-signotopes on `[n]`, the
sign `σ(ijk)` recording the orientation of the triangle formed by lines `i, j, k`.
(Checked against the paper, fetched 2026-09-02 from Felsner's page; the text is
typographically damaged but the statement and the proof's closing sentence "the triangle
induced by lines `l_i, l_j, l_k` in `A` is a + triangle exactly when `σ(ijk) = +`; this
proves the bijection" are unambiguous.)

We fix the sign convention `σ(ijk) = +` iff line `j` passes *above* the crossing point of
lines `i` and `k`.

**Lemma 2.2 (order along a line).** For a line `r` and two other lines `a < b`,
`a` crosses `r` before `b` (left to right) iff `σ(sorted{r,a,b}) = −`.

*Proof.* Let `i < j < k` be the sorted triple. At `x = −∞` the vertical order is
`i, j, k`. *Case `r = i`:* if `j` is below the crossing `P = i∩k` (`σ = −`) then at the
abscissa of `P` line `j` is already below `i`, so `j` crossed `i` before `k` did; if `j`
is above `P` it has not yet crossed `i`, so `k` crosses `i` first. *Case `r = j`:* if `j`
is above `P` (`σ = +`) it is above both `i` and `k` there, so it has crossed `k` and not
`i`: `k` before `i` along `j`; if below `P`, `i` before `k`. *Case `r = k`:* if `j` is
above `P` (`σ = +`) it has already crossed `k`: `j` before `i` along `k`; otherwise `i`
before `j`. In all three cases the smaller-labelled line comes first iff `σ = −`. ∎

The local sequence of each line (the order of its `n − 1` crossings) is therefore a
function of `σ`; the signotope axiom is exactly what makes these orders consistent.

**Computational check.** The number of 3-signotopes on `[n]` computed by enumerating the
models of the axiom clauses is `8, 62, 908, 24698` for `n = 4, 5, 6, 7`, matching OEIS
A006245 ("simple arrangements of `n` pseudolines in the Euclidean plane", Scheucher's
comment), and a greedy left-to-right sweep realised every one of them as a wiring
diagram (`kobon_sym.py validate`).

## 3. Triangles and segments

Each line carries `n − 1` crossings and hence `n − 2` bounded segments; there are
`n(n − 2)` bounded segments in all.

**Lemma 3.1.** Lines `i < j < k` bound a triangular face iff the crossings with `j` and
`k` are adjacent along `i`, those with `i` and `k` adjacent along `j`, and those with
`i` and `j` adjacent along `k`.

*Proof.* A triangular face with vertices `i∩j, i∩k, j∩k` has as sides the three
segments joining them, and a side is a segment iff no other line crosses it, i.e. iff
the two crossings are adjacent. Conversely, if the three crossings are pairwise adjacent
the three segments form a closed curve; a fourth line meeting its interior would have to
cross the boundary (it is unbounded and the region is bounded), contradicting adjacency;
so the interior is a face. ∎

**Lemma 3.2.** A bounded segment is a side of at most one triangular face.

*Proof.* Let `s` be a segment of line `r` with endpoints `r∩a` and `r∩b`. A triangle with
side `s` has its other two sides on `a` and `b` and its third vertex at `a∩b`, which lies
on one side of `r`. Two triangles with side `s` would need `a∩b` on both sides. ∎

**Corollary 3.3.** A simple arrangement of `n` pseudolines has at least `t` triangular
faces iff at most `n(n − 2) − 3t` of its bounded segments are not sides of a triangle
("unused"). For `n = 18, t = 94` the budget is `288 − 282 = 6`.

## 4. The tight structure at `n = 18`

Call a line *perfect* if all its `n − 2` segments are used. The proof of Theorem 1.1 in
[BBL] rests on:

**Lemma 4.1 (BBL association lemma; even `n`).** Let `L` be a perfect line of a simple
arrangement of an even number `n` of pseudolines, and let `M`, `N` be the lines through
the first and last crossing of `L`. Then one of the two segments of `M` starting at
`M∩L`, or one of the two segments of `N` starting at `N∩L`, is unused.

*Proof (after [BBL]).* The `n − 2` triangles `t_1, …, t_{n−2}` along `L` lie alternately
inside and outside the region `Δ` bounded by `L, M, N`; as `n − 2` is even, `t_1` and
`t_{n−2}` lie on opposite sides, so one of them, say `t_{n−2}`, is outside `Δ`. Its side on
`N` is one of the two segments of `N` at `N∩L`. The other segment `s` of `N` at `N∩L`
points into `Δ`; a triangle with side `s` would have a side on `L` starting at `L∩N`,
which can only be the last bounded segment of `L` — already the side of `t_{n−2}` and, by
Lemma 3.2, of no other triangle. So `s` is unused. ∎

(The parity is essential: for odd `n` the lemma fails, and our checker finds violations
exactly there — 406 among the 2,520 perfect-line instances of the 24,698 arrangements
with `n = 7`, and none among all 908 arrangements with `n = 6`, 30,000 arrangements with
`n = 8`, or the extremal arrangements found by SAT for `n = 8, 10, 12, 14`.)

The lemma associates to each perfect line an unused segment starting at one of its
extreme crossings on the line through that crossing. An unused segment `s ⊂ N` with
endpoints `N∩L` and `N∩X` can be associated in this way only to `L` (via `N∩L`) or to `X`
(via `N∩X`), so to at most two perfect lines. With `m` perfect lines this gives
`#unused ≥ m/2`, while `#used ≤ m(n−2) + (n−m)(n−3) = n(n−3) + m`; these two
inequalities are the whole proof of Theorem 1.1.

**Proposition 4.2 (T1).** A simple arrangement of 18 pseudolines with 94 triangular faces
has exactly 12 perfect lines, and each of the other 6 lines has exactly one unused
segment.

*Proof.* `#used = 282` and `#unused = 6`. From `282 ≤ 270 + m` we get `m ≥ 12`; from
`6 ≥ m/2`, `m ≤ 12`. The `18 − m = 6` imperfect lines carry the 6 unused segments, at
least one each, hence exactly one each. ∎

**Proposition 4.3 (T2).** In such an arrangement every unused segment lies on an
imperfect line `N`, and both lines `L, X` through its endpoints are perfect, with `N∩L`
the first or last crossing along `L` and `N∩X` the first or last crossing along `X`.

*Proof.* The association of Lemma 4.1 maps the 12 perfect lines injectively into the
12 endpoint-slots of the 6 unused segments (each slot — an endpoint `N∩L` of a segment
`s ⊂ N` — can be the image only of the other line `L` through it). So it is a bijection:
every endpoint of every unused segment is the extreme crossing of a perfect line. The
carrying line is imperfect because it carries an unused segment. ∎

Both propositions use nothing beyond Lemma 4.1 and counting. They are *consequences*, so
adding them as clauses to a search for a 94-triangle arrangement is sound: any such
arrangement satisfies them.

## 5. Symmetries of the model

A Euclidean pseudoline arrangement determines a signotope only after a sweep direction
is chosen, i.e. a cut of the cyclic sequence of its `2n` unbounded rays.

**Proposition 5.1.** Moving the cut past the ray of line `n` at `−∞` ("shift") relabels
`n ↦ 1` (direction reversed) and `i ↦ i + 1`, and acts on signotopes by

    shift:  σ'(i+1, j+1, k+1) =  σ(i, j, k)   (k < n),
            σ'(1, i+1, j+1)   = −σ(i, j, n)   (i < j < n);

reflection in a horizontal axis ("mirror") acts by `σ'(n+1−k, n+1−j, n+1−i) = −σ(i, j, k)`.
`shift^n` is the global sign flip (rotation by `π`), `shift^{2n} = id`, and shift and
mirror generate a dihedral group of order `4n` acting on signotopes, preserving the number
of triangular faces, and acting on the labels `1..n` as the dihedral group of the
`n`-cycle.

*Proof sketch.* The shift is a re-sweep of the same arrangement from the next direction:
the local sequence of the moved line is reversed and all others are unchanged; the sign
rules follow from Lemma 2.2 applied to the new labels (for a triple `{i, j, n}`, "`n`
before `j` along `i`" is the negation of "`j` before `n` along `i`"). The mirror reverses
the vertical order and flips every orientation. Triangular faces are properties of the
cell complex and are preserved. ∎

**Computational check** (`kobon_sym.py`): for `n = 4, 5, 6, 7` all `4n` maps send every
signotope to a signotope of the same triangle count, the `4n` maps are distinct, and
`shift^n` equals the flip. Orbit-size histograms are recorded in `data/`.

## 6. Encodings

All encodings share the signotope variables `σ(ijk)` and the axiom clauses (eight
3-clauses per 4-subset). Adjacency variables `Adj(r; {a,b})` are made equivalent to "no
line crosses `r` between `a` and `b`" via Lemma 2.2 and auxiliary conjunction variables.

* **v1** (`kobon_sat.py`): triangle variables `T(ijk) → Adj(i;{j,k}) ∧ Adj(j;{i,k}) ∧
  Adj(k;{i,j})` and a totalizer `ΣT ≥ t`. Correct but weak: the solver must rediscover
  the segment counting (n = 11, t = 33 unsolved after 12 min; Savchuk's table encoding:
  1.67 s).
* **v2** (`kobon_sat2.py`): unused-segment variables `U(r;{a,b})` with
  `U → Adj`, `Adj ∧ ¬U → Adj(a;{r,b})`, `Adj ∧ ¬U → Adj(b;{r,a})`,
  `Adj ∧ Adj(a;{r,b}) ∧ Adj(b;{r,a}) → ¬U`, and a sequential counter `ΣU ≤ n(n−2) − 3t`.
  Symmetry breaking: `σ(123) = −` and lex-leader constraints for all `4n − 1` non-trivial
  group elements on a prefix of 60 variables.
* **tight** (`--tight`, `n = 18` only): adds (T1) at most one `U` per line and `ΣU ≥ 6`,
  and (T2) `U(N;{L,X}) → Perf(L) ∧ Perf(X) ∧ Ext(L;N) ∧ Ext(X;N)`, where `Perf(L)` implies
  every `U` on `L` false and `Ext(L;N)` is "`N` is first or last along `L`", each defined by
  implications from Lemma 2.2.

**Lemma 6.1 (soundness).** (i) Every model of v2 (with or without tight clauses) decodes
to a simple arrangement with at least `t` triangular faces. (ii) Every simple arrangement
with at least `t` faces (for tight: `n = 18, t = 94`) extends to a model.

*Proof.* (i) `σ` is a signotope, hence an arrangement (Theorem 2.1). `Adj` equals real
adjacency (both directions are clauses). A real segment not marked `U` has both partner
adjacencies, so it is a triangle side (Lemma 3.1); thus at most `budget` real segments are
unused, and Corollary 3.3 gives `≥ t` faces. (ii) Take `σ` from the arrangement, `Adj` the
real adjacencies, `U` the real unused segments (at most `budget` by Corollary 3.3, and
each has a missing partner adjacency, so the implication clauses hold; a used segment has
all three adjacencies, so `¬U` holds). Tight clauses hold by Propositions 4.2–4.3, with
`Perf`, `First`, `Last` set to their real values. Symmetry-breaking clauses hold for the
lex-minimal element of the orbit, which has the same triangle count (Proposition 5.1). ∎

## 7. Cube-and-conquer and the main result

By (T1) the set `S` of imperfect lines of a 94-triangle arrangement is a 6-subset of
`[18]`; by Proposition 5.1 we may replace the arrangement by its image under the group
element that sends `S` to the lexicographically least member of its `D_18`-orbit, and by a
further flip assume `σ(123) = −` (the flip fixes all labels). There are 561 orbits
(covering all `C(18,6) = 18,564` subsets; `cubes.py gen` enumerates them by canonical
forms, and Burnside's lemma for `D_18` on 6-subsets of the 18-cycle gives 561 independently;
the label action of the `4n` signotope maps was checked to coincide with `D_18`). Cube `S` is the tight instance
without lex-leader clauses, plus "`U` false on every line outside `S`" and "some `U` true
on every line of `S`".

**Theorem 7.1 (CERTIFIED; an instance of Blanc's Theorem 1).** No simple arrangement of
18 pseudolines in the Euclidean plane has 94 bounded triangular faces; with Bader's
straight-line arrangement, `a^s_3(18) = 93`.

*Certificate.* All 561 cubes are UNSAT (kissat 4.0.4, one core each; 5.0
core-hours in total, median 18 s, hardest cube #503 at 585 s);
all 561 DRAT proofs were checked by `drat-trim` (8.2 core-hours; 27.75 GB of proofs
in total, deleted after verification; SHA-256 and size of every proof are listed with its
cube in `data/cubes_T2.csv`, and each is regenerable by `cubes.py`). Encodings, cubes and checker are in this directory; the
`n = 12, t = 38` and `n = 14, t = 54` controls (budget 6, not tight) and the plain
`n = 18` instance (no structural lemma) were not finished, so the certificate depends on
Lemma 4.1 through Propositions 4.2–4.3 as stated. The lemma-free cube variant
(`CUBE_VARIANT=plain`, 955 orbit representatives of the set of lines carrying unused
segments, `|S| ≤ 6`) was generated but not run.

*Prior work.* This is Corollary 2.0.5 / Theorem 1 of [Bl] at `n = 18` (see the abstract);
the argument there is a short counting proof, ours is a machine search. The value of the
computation is as a validated pipeline (§8) and as an independent check of [Bl].

## 8. Controls

Signotope counts (§2). Triangle maxima against [BBL] Theorem 1.4, v2 encoding, kissat
4.0.4, one core (`data/ctrl2_*.log`; every SAT model decoded and its triangle count
recomputed twice, by the adjacency test and by counting three-sided faces of the sweep):

| n | a^s_3(n) [BBL] | SAT at value | UNSAT at value+1 |
|---|---|---|---|
| 8 | 14 | 0.2 s | 0.2 s |
| 9 | 21 | 0.1 s | (odd; bound n(n−2)/3) |
| 10 | 25 | 1.2 s | 1.8 s |
| 11 | 32 | 2.5 s | 0.7 s |
| 12 | 37 | 1.7 s | 392 s |
| 13 | 47 | 1.9 s | — |
| 14 | 53 | 150 s | not finished in 40 min (killed) |
| 15 | 65 | 21 s | — |
| 16 | 72 | 236 s | — |

The `n = 12, t = 38` and `n = 14, t = 54` instances are the closest analogues of `n = 18,
t = 94` (budget 6 each) but are *not* tight — at `n = 12` the counting only gives
`6 ≤ m ≤ 12` — which is why the plain instance grows hard while the tight cubes at
`n = 18` are fast.

## 9. What is and is not shown; an audit of the upper-bound column

* The result concerns simple arrangements of pseudolines; it transfers to straight lines
  in general position but not to arrangements with concurrent triples or parallels, which
  the Kobon problem allows.
* **Blanc's theorem closes the simple case.** Theorem 1 of [Bl] gives, for even `n`,
  `a^s_3(n) ≤ n(n − 5/2)/3` (`n ≡ 0, 4 mod 6`) and `(n(n − 5/2) − 2)/3` (`n ≡ 2 mod 6`),
  and Theorem 3 gives the exact values for all `n ≤ 30`. His Conjecture 1.0.1 (bounds
  reached for all `n ≥ 21`) was open at `n = 31, 32, 37, 38, …` in 2008; the straight-line
  constructions now on OEIS A006066 — Wood (`n = 31`, 299), Zarzuelo (`n = 32`, 314),
  Parpalak–Utkin (`n = 37`, 431, simple by their Theorem 5.1) — meet his affine bound at
  31, 32, 37 *if* they are in general position (not checked here); at `n = 38` the
  recorded `K(38) ≥ 450` exceeds Blanc's simple bound `(38·35.5 − 2)/3 = 449`, so that
  arrangement must have multiple points or parallels.
* **The general-position assumption is essential and is being dropped silently.** Simple
  arrangements are beaten by non-simple ones at `n = 8` (`K = 15 > 14`), `n = 12`
  (`38 > 37`) and `n = 14` (`54 > 53`, Maiorana 2026, triple points). The proofs of the
  even-`n` bounds of [BBL] and [Bl] use simplicity (BBL: "As the arrangement is simple, a
  segment cannot be associated to more than two pseudo-lines"; the alternation of
  triangles along a perfect line also fails at a triple point, where two consecutive
  triangles can lie on the same side). The only bound we found *stated* for general
  configurations is the Clément–Bader draft (OEIS-cached, dated 2007-12-21; its
  Proposition 1 and Lemma 1 account for segments lost at multiple points): `(n+1)(n−3)/3`
  for `n ≡ 0, 2 (mod 6)`, i.e. **95** at `n = 18` and **55** at `n = 14` (their Table I
  lists exactly these). Yet OEIS A006066's upper-bound column gives 94 at `n = 18` and 54
  at `n = 14` — these are [BBL]'s simple-arrangement values `⌊n(n − 7/3)/3⌋` (the entry's
  formula section says so) — and Wikipedia's table labels the same numbers
  "Clément–Bader". Consequently the OEIS statement that `a(14) = 54` is exact "since 54
  equals the known upper bound" rests on applying a simple-arrangement theorem to
  arrangements with triple points; on the cited literature alone, `54 ≤ K(14) ≤ 55` and
  `93 ≤ K(18) ≤ 95`. We have not found a proof of the even-`n` bound for non-simple
  arrangements, and we have not tried to produce one; this is flagged, not settled.
* Cited facts checked against the primary source today: [BBL] (arXiv:0706.0723, Theorems
  1.1, 1.4, §§4–5), [Bl] (arXiv:0801.2845, Theorems 1–3, Corollary 2.0.5, §5), [FW]
  (statement of the bijection), Savchuk 2025 (Table 1, Appendix C), Parpalak–Utkin 2026
  (Theorem 5.1), Clément–Bader 2007 (OEIS-cached draft, abstract, Prop. 1, Lemmas 1–2,
  Table I), OEIS A006066 and A006245.

## References

* [BBL] N. Bartholdi, J. Blanc, S. Loisel, *On simple arrangements of lines and
  pseudo-lines in P² and R² with the maximum number of triangles*, Contemp. Math. 453
  (2008) 105–116; arXiv:0706.0723.
* [Bl] J. Blanc, *The best polynomial bounds for the number of triangles in a simple
  arrangement of n pseudo-lines*, Geombinatorics 21 (2011) 5–17; arXiv:0801.2845.
* [CB] G. Clément, J. Bader, *Tighter upper bound for the number of Kobon triangles*,
  draft, 2007-12-21 (cached at OEIS A006066).
* [FW] S. Felsner, H. Weil, *Sweeps, arrangements and signotopes*, Discrete Appl. Math.
  109 (2001) 67–94.
* P. Savchuk, *Constructing optimal Kobon triangle arrangements via table encoding, SAT
  solving, and heuristic straightening*, arXiv:2507.07951 (2025).
* R. Parpalak, D. Utkin, *The 18·2^t+1 triangle-maximal series of straight lines*,
  arXiv:2604.22035 (2026).
* OEIS A006066 (Kobon triangles), A006245 (pseudoline arrangements), A002071.
