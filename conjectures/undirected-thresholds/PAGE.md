# PAGE.md — handoff for the site build (new page: `fabianarevalo.com/undirected-thresholds`)

New conjecture directory, first session (2026-08-18). No page exists yet.

## 1. Headline claim (one sentence, labelled)

**CERTIFIED** — At the open frontier `k = 22` of the Currie–Mol conjecture
on undirected repetition thresholds, the threshold exponent `21/20` is
sharp on both sides: every word over 22 letters of length 26 contains an
undirected repetition of exponent ≥ 21/20 (a 451-node exhaustive
certificate), while a certified word of length 20 000 avoids everything
above 21/20.

## 2. Contributions (numbered, with the numbers, each labelled)

1. **CERTIFIED.** Undirected exponents `≥ (k−1)/(k−2)` are unavoidable
   over `k` letters beyond length exactly `k+3`, for `k = 22, 23, 24, 25`
   (exhaustive canonical trees of 451, 483, 516, 550 nodes; < 1 s total).
   Corollary: `URT(k) ≥ (k−1)/(k−2)` at these `k`, independent of the
   literature (re-derives that leg of Currie–Mol's theorem in-repo).
2. **CERTIFIED.** The lexicographically least canonical
   `(21/20)⁺`-free word over 22 letters of length **20 000**, verified by
   four independent checkers (incremental, run-scan, numpy batch, brute
   prefix); lengths 5 000 for `k = 23, 24, 25`; and 1 606 755 canonical
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
7. **Conjecture C3** (new, data-backed at `k = 22..25` only): the maximal
   length of a word over `Σ_k` avoiding undirected exponents
   `≥ (k−1)/(k−2)` is exactly `k+3` for all `k ≥ 22`.

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
- **Fig 3 (optional) — the k+3 law.** Data: the four (k, max-length)
  pairs from `data/lower_bound_certificates.txt`. Reader sentence: "The
  maximal length at the non-strict threshold is k+3 in every computed
  case." Skip if it reads as too little data for a plot; a table is fine.

## 4. Caveats the page must carry

- **Every literature statement is (secondary).** The session ran with all
  primary sources blocked (egress); the status "open for `k ≥ 22`", the
  confirmed range `4..21`, the lower-bound theorem attribution, and even
  the URT definition conventions come from search snippets of
  arXiv:1904.10029, arXiv:2006.07474 (TCS 2021), and Shur (ToCS 2024).
  Must be re-verified against the papers before any publication claim.
- The conjecture at `k = 22` is **not settled** by this session, and the
  certified lower bounds re-derive a known theorem at four values of `k`
  (novelty of the certificates: the sharp `k+3` lengths and their
  smallness appear unrecorded, but that too is (secondary)).
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
