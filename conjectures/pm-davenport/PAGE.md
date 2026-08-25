# PAGE.md — handoff for the local page build (research-page skill)

New conjecture directory; new page at `fabianarevalo.com/pm-davenport`;
new row in the top-level README (added this session).

## 1. Headline claim (one sentence)

**CERTIFIED** — The plus–minus weighted Davenport constant of `C₅ ⊕ C₁₅`
— the single group of order at most 100 left undetermined by
Marchan–Ordaz–Schmid in 2013, "either 6 or 7" — is **6**: three
independent exhaustive searches (one a full brute force over all
2,324,784 candidate 6-subsets) show no dissociated 6-set exists, while
85,155 dissociated 5-sets do.

## 2. Contributions (numbered, labelled)

1. **CERTIFIED** — `D±(C₅ ⊕ C₁₅) = 6`, the last open group of order
   ≤ 100 from Marchan–Ordaz–Schmid (IJNT 2014, bracket {6,7},
   (secondary)): no dissociated 6-subset among the 2,324,784 candidate
   class-rep 6-subsets; the census of 85,155 extremal 5-sets is
   reproduced identically by all three engines (Python set-DFS, C
   flag-DFS with 139,051 nodes agreeing exactly, and unpruned ternary
   brute force).
2. **CERTIFIED** — `D±(C₇ ⊕ C₂₁) = 8` (first determination found for
   this group; order 147 is outside every published range located): a
   verified 7-element dissociated witness attains the pigeonhole bound,
   whose proof is one line (2⁸ = 256 > 147); 2,016 extremal 7-sets,
   engine node counts agreeing at 16,528,741.
3. **CERTIFIED** — census of `μ(G)` (maximum dissociated subset =
   `D±(G) − 1`) for **every** abelian group of order ≤ 192: attainment
   of `⌊log₂|G|⌋` is the rule; the deficient groups in range are
   ⟨FINAL LIST + COUNT from sweep.csv⟩ — including the three
   exceptional values published by MOS, reproduced exactly (C₃² → 3,
   C₃³ → 4, C₃²⊕C₉ → 6).
4. **PROVED** — a checksum construction lemma: `μ(C_m ⊕ H) ≥ ν_m(H)`,
   where `ν_m(H)` allows internal relations of sign-weight ≢ 0 mod m;
   it explains every bound-attaining witness found (`ν₃(C₇²) = 7` vs
   `μ(C₇²) = 5`), plus self-contained proofs of the
   Adhikari–Grynkiewicz–Sun bracket, `μ(C_p^r) = r` for p ∈ {2,3}, and
   a graded counting bound that eliminates all but four CRT profiles of
   any hypothetical `C₅⊕C₁₅` 6-set.
5. **CERTIFIED** — family values beyond order 192: ⟨FINAL: C₃⊕C₃ₙ
   through n = 32, C₅⊕C₅ₙ at n = 11, 12, C₇⊕C₂₈, C₁₃², and (if
   finished) C₇⊕C₄₂, C₇⊕C₄₉, C₇³, C₅²⊕C₁₅⟩.
6. ⟨IF CONFIRMED BY orbit_analysis: **CERTIFIED** — the 2,016 extremal
   sets of `C₇⊕C₂₁` form a single orbit of the automorphism group — the
   attaining configuration is unique up to symmetry.⟩

## 3. Figure specs

- **F1 (the census).** Scatter/strip: x = |G| (2…192, one mark per
  group), y = deficiency `t(G) − μ(G)` (0 for attained, jittered), the
  deficient groups highlighted and labelled. Data:
  `conjectures/pm-davenport/sweep.csv` (columns N, mu, t_log2N,
  deficiency, invariant_factors). Reader sentence: "Across all abelian
  groups of order up to 192, the maximum dissociated set has size
  exactly ⌊log₂|G|⌋, except for a handful of small 3-heavy groups and
  C₅⊕C₁₅."
- **F2 (the two open cases).** Side-by-side: the bracket {6,7} for
  C₅⊕C₁₅ resolving DOWN vs bracket {7,8} for C₇⊕C₂₁ resolving UP; under
  C₇⊕C₂₁ show its witness as the CRT table (rows = 7 elements, columns =
  C₃ checksum coordinate | C₇² coordinates), checksum column highlighted.
  Data: NOTE.md §3 (Theorems 7–8), witness in
  `certs/c3p7p7_extremal_7sets.txt` line 1. Reader sentence: "The two
  groups reported open resolve in opposite directions — and the one that
  attains the upper bound does it through a mod-3 checksum coordinate."
- **F3 (near-miss counting).** Bar chart: the four surviving profiles
  k₁ = 3,4,5,6 with their subset-count margins (24, 24, 22, 22 against
  capacity 25), and the eliminated profiles k₁ = 0,1,2 (64, 32, 32).
  Data: NOTE.md Lemma 6 remark (numbers exact, from binomial sums).
  Reader sentence: "Counting kills three of the seven ways a 6-set could
  sit over the checksum coordinate; the other four survive counting by
  a margin of 1-to-3 and die only by exhaustive search."

## 4. Caveats the page must carry

- **Every literature citation is (secondary)** — reconstructed from
  WebSearch snippets on 2026-08-25; the sandbox could not open any
  paper. In particular the framing claim — "C₅⊕C₁₅ is the single
  undetermined group of order ≤ 100 in MOS 2013, bracket {6,7}" — rests
  on three agreeing snippet syntheses of arXiv:1308.3316 and must be
  checked against the actual paper (open access) before the page ships;
  NOTE.md §8 lists all mandatory checks (including MathSciNet/zbMATH,
  unchecked).
- If MOS 2013 turns out to determine C₅⊕C₁₅ after all, contribution 1
  downgrades to an independent verification and the page headline must
  change.
- The checksum lemma (contribution 4) may coincide with MOS's own
  lower-bound technique ("mainly lower bounds" per their abstract); the
  page should claim the computations, not the lemma, as the novelty.
- MOS's exceptions list is quoted from a snippet that may be truncated
  (our census adds C₃⁴ → 5, which is classical).
- Runtimes were recorded under CPU oversubscription; they are upper
  bounds.
- ⟨IF ANY heavy runs did not finish: list them as "running at session
  close, value not claimed".⟩

## 5. Existing page

None — this is a new conjecture directory and a new page.
