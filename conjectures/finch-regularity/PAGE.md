# PAGE.md — handoff for `fabianarevalo.com/finch-regularity`

New page. Nothing exists for this conjecture yet.

## 1. Headline claim

**A finite, machine-checkable certificate settles regularity for 32 Ulam-type
sequences — 20 of them in cases open since 1995 — and turns up an exceptional
family in `U(4,b)` appearing exactly when `b = 2^k − 1`.**
(Certificate theorem: PROVED. The 32 sequences and the exceptional family:
CERTIFIED.)

## 2. Contributions

1. **Theorem 1 (PROVED).** Three finite conditions — (P) a repeated window
   state, (C) a residue-cover condition mod the period, (F) a finite check on
   even numbers up to `B = 2X₁ + 4P + 2W + 4` — imply that `U(a,b)` is regular,
   that its set of even elements is exactly `E`, and that its fundamental
   difference is exactly `P`. The reduction is **self-correcting**: it cannot be
   satisfied with an incomplete even set.
2. **32 certified sequences (CERTIFIED), 20 in cases reported open:** `U(4,b)`
   for `b ≡ 3 (mod 4)`, `b ∈ {7, 11, 19, 23, 27, 35, 39, 43}`; `U(6,7)`,
   `U(6,11)`; `U(8,9)`, `U(8,11)`; `U(10,11)`, `U(10,13)`, `U(10,17)`;
   `U(12,13)`, `U(12,17)`; `U(14,15)`; `U(16,17)`; `U(18,19)`. The remaining 12
   reproduce Cassaigne–Finch (`a = 4`, `b ≡ 1 mod 4`, `5 ≤ b ≤ 49`) as controls.
3. **The exceptional family (CERTIFIED).** For all 255 odd `b` with
   `5 ≤ b ≤ 513`, no gaps, the even elements of `U(4,b)` below `6b² + 4000` are
   exactly `{4, 2b+4, 4b+4}` — except for the seven values `b = 2^k − 1`,
   `k = 3..9`, where exactly one more appears, always equal to
   **`4b² + 2b − 4`**: 206, 926, 3902, 15998, 64766, 260606, 1045502.
4. **`U(4,7)` closed outright (CERTIFIED):** exactly four even elements
   `{4, 18, 32, 206}`, and fundamental difference **`P = 11,301,098`** — about
   **5000×** that of any neighbouring `U(4,b)` with `b ≤ 49`.
5. **2-adic period law (CERTIFIED for the 13 values tested; the law itself is
   conjectural):** `P(4,b) = 2^{⌊log₂(b−1)⌋+3}(b+1)`, exact for all twelve
   tested `b ≡ 1 (mod 4)` with `5 ≤ b ≤ 49` — and also for `b = 19`. Every other
   tested `b ≡ 3 (mod 4)` has a period carrying a large prime factor:
   `P(4,23) = 2·14929`, `P(4,39) = 2²·3·11·4703`.
6. **Why it matters for the open case.** Every `2^k − 1` is `≡ 3 (mod 4)` — the
   residue class Cassaigne–Finch omit — and their argument is reported to run
   through "`U(4,v)` has precisely three even terms", which is exactly what
   fails on the exceptional family.

## 3. Figures

**Figure 1 — the exceptional family.** Data:
`data/a4_even_elements.csv` (columns `b`, `n_even`, `even_elements`). Plot the
number of even elements of `U(4,b)` against odd `b ∈ [5, 513]`: a flat line at 3
with exactly seven spikes to 4, at `b = 7, 15, 31, 63, 127, 255, 511`.
Reader's sentence: *"`U(4,b)` always has three even elements, except at the
Mersenne-shaped values of `b`, where it has four."*

**Figure 2 — the window automaton.** Schematic, no data file. Show an odd
integer `x` with arrows reaching back to `x − e` for each `e ∈ E` inside a
shaded window of width `W = max E`, and the rule "`x` joins iff exactly one
arrow lands on a member". Reader's sentence: *"Once the even elements run out,
whether a number belongs depends only on a fixed-width window behind it — so the
sequence is a machine, and machines repeat."*

**Figure 3 — smooth versus wild periods.** Data: `data/certificates.csv`
(columns `b`, `P`, restricted to `a = 4`). Two-series plot of `P` against `b` on
a log axis, one series for the `b` obeying the 2-adic law (12 values plus
`b = 19`), one for those that do not. Reader's sentence: *"For half the `b` the
period is a power of two times `b+1`; for the rest it is large and carries a big
prime factor — and `b = 19` sits on the wrong side of the obvious dividing
line."*

Skip any figure of the raw sequence: it looks like noise and carries no reader
sentence.

## 4. Caveats the page must carry

- **Every citation is secondary; no primary source was read.** The sandbox could
  not reach `arxiv.org`, `oeis.org`, `erdosproblems.com`, `mathoverflow.net` or
  any other scholarly host — all refused with HTTP 403 at the egress proxy. The
  page must say this plainly.
- **The novelty claim is the weakest link.** That these 20 cases are open rests
  on search-engine summaries of Schmerl–Spiegel (1994) and Cassaigne–Finch
  (1995). If a primary source shows otherwise, the results stay correct but
  become rediscoveries. Do not write "first" anywhere without hedging.
- **Theorem 1 is probably not new in substance.** It is best described as a
  certificate-carrying form of Finch's 1992 criterion ("finitely many even
  elements ⇒ regular"). The contribution is the explicit finite certificate and
  the cases it settles, not the implication.
- **Conjectures A and B are conjectures.** The `b = 2^k−1` characterisation and
  the period law are patterns over a tested range, not theorems. State the
  ranges: 255 values of `b` for A, 13 values for B.
- **The exceptional-family scan is range-limited.** Even elements were computed
  exactly up to `6b² + 4000` only. The statement is absolute *only* for `b = 7`,
  where the certificate closes it.
- **`b = 19` breaks the tidy story.** It is `≡ 3 (mod 4)` and yet obeys the
  2-adic law. Do not present the dichotomy as "1 mod 4 smooth, 3 mod 4 wild".
- **`U(4,15)`, `U(4,31)`, `U(4,63)` are not certified** — no window-state cycle
  within `1.5·10⁹` steps.
- Two independent implementations (Python/hash-table, C/Brent) agree on `E`, `P`
  and `|R|` in all 32 rows; worth saying, since the whole result rests on the
  verifier.

## 5. Existing page

None. This is a new conjecture directory and a new page.
