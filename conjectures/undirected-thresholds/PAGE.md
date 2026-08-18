# PAGE.md — handoff for the site build (new page: `fabianarevalo.com/undirected-thresholds`)

New conjecture directory, first session (2026-08-18). No page exists yet.

## 1. Headline claim (one sentence, labelled)

**PROVED** — For every alphabet size `n ≥ 5`, the longest word containing
no undirected repetition of exponent `≥ (n−1)/(n−2)` has length exactly
`n+3`, and the extremal word is unique up to renaming — a sharp,
elementary form of the lower-bound half of the Currie–Mol conjecture on
undirected repetition thresholds.

## 2. Contributions (numbered, with the numbers, each labelled)

1. **PROVED (Theorem T1).** For every `n ≥ 5` the maximal length of a
   word over `Σ_n` with no undirected exponent `≥ (n−1)/(n−2)` is exactly
   `n+3`, with unique extremal word `0 1 ⋯ (n−2) 0 (n−1) 1 3`; hence
   `URT(n) ≥ (n−1)/(n−2)` for all `n ≥ 5` by a one-page case analysis
   (three elementary inequalities; a 10-node case tree). Corroborated by
   machine at every `n ∈ {5..31, 40, 60, 100}` and by the independent
   exhaustive certificates below. *The inequality is Currie–Mol's theorem
   (secondary); the sharp extremal length and uniqueness appear new
   (secondary).*
1b. **CERTIFIED.** Independent exhaustive certificates of the same at
   `k = 22, 23, 24, 25` (canonical trees of 451, 483, 516, 550 nodes;
   < 1 s total), found before the proof.
2. **CERTIFIED.** The lexicographically least canonical
   `(21/20)⁺`-free word over 22 letters of length **20 000**, verified by
   four independent checkers (incremental, run-scan, numpy batch, brute
   prefix); lengths 5 000 for `k = 23, 24, 25`; and at least 1 606 755 canonical
   free words of length 55 at `k = 22`.
3. **CERTIFIED.** The binary Pansiot class (all `(n−1)`-windows rainbow)
   is empty at `α = (n−1)/(n−2)` for every `n ∈ {20, 21, 22, 23}`: no
   codeword of length 5 exists (20-node trees; longest codeword `0110`).
   Consequence: undirected-threshold witnesses must contain equal letters
   at distance exactly `n−2` — the classical binary Dejean/Pansiot route
   cannot carry them.
4. **PROVED.** Exact reversal-transfer identities for the binary Pansiot
   code: `code(wᴿ) = code(w)ᴿ`, `r τ_b r = τ_b^{−1}`,
   `g(Vᴿ) = r·g(V)^{−1}·r`, and the anti-gid correspondence for reversed
   matches (one lemma at sketch level, so marked).
5. **PROVED.** Theorem D, a finite-check descent criterion: for a fixed
   point `W = φ(W)` of any `k`-uniform morphism over 22 letters, three
   checkable conditions (block synchronization, reversed-block exclusion,
   U-freeness of factors up to `L₀ = 42k−20`) imply `W` is
   `(21/20)⁺`-free.
6. **CERTIFIED.** The affine sub-ansatz `φ(x) = m·x + B₀ (mod 22)` —
   digit-sum words generalizing Thue–Morse — is empty at block lengths
   `k = 22, 23, 24` for all ten multipliers `m ∈ (Z/22)^×` (exhausted
   searches dying by depth `3k`), and for `m = 1` at further `k ≤ 36`
   (exact set in the committed scan logs).
(The session's interim Conjecture C3 — the `k+3` law from four data
points — was upgraded to Theorem T1 the same day and is no longer a
separate contribution.)

## 3. Figure specs

- **Fig 1 — the two-sided threshold.** Data: `data/lower_bound_certificates.txt`
  (deaths at `k+3`) and `data/witness_n22_L20000.txt` (aliveness); render
  as a number line at `k = 22` with the two exponent cutoffs `≥ 21/20`
  (dead at 25) and `> 21/20` (alive at 20 000). Reader sentence: "At the
  conjectured threshold the language dies instantly on one side and is
  effectively infinite on the other."
- **Fig 2 — gap spectrum of a witness.** Data: compute letter-recurrence
  gaps of `data/witness_n22_L20000.txt` (script one-liner; gaps lie in a
  narrow band starting at 20). Reader sentence: "A 22-letter word avoiding
  undirected repetitions above 21/20 must reuse every letter within a few
  positions of the minimum legal distance 20 — including at distance
  exactly 20, which is why the classical binary coding fails."
- **Fig 3 — the extremal word.** Data: render `w* = 0 1 ⋯ (n−2) 0 (n−1)
  1 3` at `n = 22` (26 cells, color by letter, arcs marking its three
  equal-letter pairs at distances 21, 22, 21). Reader sentence: "This is
  the unique longest word over 22 letters avoiding undirected repetitions
  of exponent at least 21/20 — one cell longer and any word breaks."

## 4. Caveats the page must carry

- **Every literature statement is (secondary).** The session ran with all
  primary sources blocked (egress); the status "open for `k ≥ 22`", the
  confirmed range `4..21`, the lower-bound theorem attribution, and even
  the URT definition conventions come from search snippets of
  arXiv:1904.10029, arXiv:2006.07474 (TCS 2021), and Shur (ToCS 2024).
  Must be re-verified against the papers before any publication claim.
- The Currie–Mol conjecture at `k = 22` (the **upper** bound
  `URT(22) ≤ 21/20`) is **not settled** by this session. Theorem T1's
  inequality `URT(n) ≥ (n−1)/(n−2)` is Currie–Mol's published theorem
  ((secondary)); the new content is the elementary proof, the sharp
  extremal length `n+3`, and the uniqueness of the extremal word — and
  the claim that these are new is itself (secondary), unverifiable from
  this sandbox. Rediscovery is possible and must be checked against the
  primary papers.
- Theorem T1 was proved late in the session; the proof is one-session-old
  and its case tree, though machine-corroborated at 30 alphabet sizes,
  deserves an independent read.
- Theorem D and the reversal identities are one-session-old proofs with
  machine spot-checks; no independent verification yet. Lemma R4 is
  explicitly sketch-level.
- The general uniform-morphic search is **inconclusive** (node-capped at a
  forcing wall), so no ansatz-emptiness claim beyond binary + affine.
- All searches are single-implementation exhaustions except where the NOTE
  says otherwise; the four-checker cross-validation covers the freeness
  verdicts, not the DFS drivers.

## 5. Existing page

None — this is a new conjecture directory; add the row/link on
`fabianarevalo.com/math` and create the page.
