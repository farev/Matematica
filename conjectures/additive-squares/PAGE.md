# PAGE.md — handoff for the public write-up at fabianarevalo.com/additive-squares

Status: **new page**. No page exists for this conjecture yet.

Plain-language hook for the page opening: a word has an *additive square* when
two neighbouring blocks of the same length add up to the same total — `2 5 | 3 4`
has one. Ask for a word over a fixed finite set of numbers with no additive
square anywhere, and you can always manage a short one. Nobody knows whether you
can manage an infinite one. That is the Pirillo–Varricchio / Halbeisen–
Hungerbühler problem, open since the 1990s. This session did not solve it. It
found a way to answer the question for *infinitely many alphabets at once*, and
used it to re-derive the one known theorem in three lines and to compute the
first table of exact answers.

## 1. Headline claim

**PROVED** — whether a word is additive-square-free depends on its alphabet only
through the integer relations among the letters, so quotienting by any group of
relations can only lengthen the longest such word (`L(A) ≤ L(A_M)`); this turns
statements about infinitely many alphabets into single finite computations, and
it re-derives Freedman's bound `L ≤ 60` for alphabets with `a+d = b+c` from one
relation vector `(1,1,−1)` — a bound this session also shows is **attained**, at
`{0,1,5,6}`.

## 2. Contributions

1. **PROVED — the Quotient Lemma.** For an alphabet `A` with `0 ∈ A`, let
   `Λ(A)` be the lattice of integer vectors `δ` with `Σ δᵢ xᵢ = 0`. For any
   subgroup `M ⊆ Λ(A)`, `L(A) ≤ L(A_M)`, where `A_M` is the image of the
   standard basis in `ℤ^(m−1)/M` — an alphabet of integer **vectors**. Four
   lines, no machinery. `NOTE.md` §3.
2. **PROVED — `L(A) = 7` for every three-element alphabet** in any field of
   characteristic 0. Upper bound: quotient to the free `ℤ²` alphabet, where the
   whole search tree closes in **354 nodes**. Lower bound: the single word
   `0, 1, 0, t, 0, 1, 0` works for *every* `t`, by twelve hand-checked
   inequalities that degenerate only at `t = 0` and `t = 1`. **Almost certainly
   folklore** — included because it calibrates the method, not as a claim.
3. **PROVED reduction + CERTIFIED constant — `L(A) ≤ 60` whenever `a+d = b+c`.**
   Such an alphabet always satisfies the relation `(1,1,−1)`, so one computation
   over one universal `ℤ²` alphabet covers the entire infinite family. The
   constant comes from closing a tree of **7,707,828 nodes** in 0.03 s of exact
   integer arithmetic. **This reproduces Freedman's published theorem** — it is a
   clean-room reproduction, not a new bound.
4. **CERTIFIED — the bound is attained.** `L({0,1,5,6}) = 60` exactly, and **29**
   alphabets in the sweep reach 60. Whether attainment is already published could
   not be determined (network blocked).
5. **CERTIFIED — exact values for 34 four-letter integer alphabets**, apparently
   the first such table: `L({0,1,2,3}) = 50`, `L({0,1,3,4}) = 55`,
   `L({0,3,4,7}) = 58`, `L({0,1,5,6}) = 60`, `L({0,1,2,4}) = 62`,
   `L({0,1,2,5}) = 86` (1,198,387,276 nodes), `L({0,1,3,5}) = 88`.
6. **CERTIFIED — the search trees saturate.** For degenerate alphabets the node
   count rises to exactly **7,707,828** and then stops changing, from
   `{0,1,9,10}` onward: once the letters are spread far enough, the concrete
   integer alphabet's search tree is *identical* to the universal one.
7. **CERTIFIED negative result — Freedman's relation looks singular.** Of the
   primitive relation classes of sup-norm ≤ 2, `(1,1,−1)` is the only one whose
   tree closes (at 60). The 3-term-arithmetic-progression class `(1,1,0)` reached
   ≥ 440 and `a+b+c = 0` reached ≥ 996 without closing. Why `(1,1,−1)` is special
   is open.

## 3. Figures

**Figure 1 — the wall at 60.** Data: `data/sweep4_c18.csv`, columns
`a,b,c,L,exact,degenerate`. Scatter of `L` against the largest letter `c`, with
degenerate alphabets (`c = a+b`) in one colour and the rest in another; draw a
horizontal rule at `L = 60`. Only points with `exact = 1` should be plotted as
solid; `exact = 0` rows are budget-limited lower bounds and must be drawn as
open/arrow markers if drawn at all.
*Sentence a reader should be able to say:* "If one letter is the sum of two
others, the word can never pass 60 — and plenty of alphabets sit exactly on that
line; every other alphabet has already climbed past it."

**Figure 2 — the longest word over {0,1,5,6}.** Data: the `word` field of the
`0,1,5,6` row in `data/sweep4_c18.csv` (also in `data/extremal_words.txt`).
Render the 60 letters as a strip of 60 coloured cells, four colours.
*Sentence:* "This is the longest additive-square-free word that exists over
`{0,1,5,6}` — no fifth-letter choice extends it, and no other word over this
alphabet is longer."

**Figure 3 — the trees become the same tree.** Data: `nodes` column of
`data/sweep4_c18.csv`, restricted to `degenerate = 1` and `exact = 1`, plotted
against `c`. Rises from 751,156 at `{0,1,2,3}` and flattens onto the horizontal
line 7,707,828.
*Sentence:* "Past a certain spread the computer is doing exactly the same search
for a concrete alphabet as for the abstract one — which is why the bound 60 is
reached and not merely approached."

No fourth figure. The relation-class table (`data/relations_n2.csv`) has only
five rows so far and belongs in the page as a small table, not a chart.

## 4. Caveats the page must carry

- **The page must not say PVHH was solved, advanced, or approached.** It was not.
  The correct framing is: a tool for handling infinitely many alphabets at once,
  applied to the one family where the answer was already known, plus the first
  exact numbers.
- **Contribution 3 reproduces Freedman's published bound.** It must be described
  as a clean-room reproduction with a shorter proof, never as new. Freedman's
  paper is *Sequences on sets of four numbers* (possibly with Tom C. Brown);
  **the venue is unresolved** — reported inconsistently as INTEGERS 16 (2016) and
  as Math. Magazine 49 (1976). Do not print a venue or year until it is checked.
- **No primary source was read.** arXiv, OEIS, erdosproblems.com and MathOverflow
  were all blocked at the sandbox's egress proxy (HTTP 403). Every citation is
  **(secondary)**, from web-search synthesis. This must appear on the page, not
  only in the repository.
- **Contribution 2 is very likely folklore.** Say so plainly.
- **Contribution 5's novelty is a weak claim.** "No published table was found"
  under a blocked network is not "no published table exists".
- **`exact = 0` rows are not measurements of `L`.** They record how deep a fixed
  node budget reached. If any of the large numbers (≥ 111, 134, 290, 350) appear
  on the page they must be labelled as certified lower bounds and must not be
  used to suggest a growth law.
- **The constant 60 is CERTIFIED, not PROVED.** It rests on a 7.7-million-node
  tree closure, not on a hand argument. The *reduction* to that computation is
  what is proved. The page should keep those two apart — that distinction is the
  whole point of the repository's labelling.
- Ochem reportedly has a heuristic arguing additive squares are **unavoidable**,
  i.e. that PVHH has a negative answer. Unverified (secondary), but worth a line
  so the page does not imply the expected answer is "yes".
