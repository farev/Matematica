# PAGE handoff — chromatic-ramsey (new page)

Page path: `fabianarevalo.com/chromatic-ramsey`. New conjecture; no page exists.

## 1. Headline claim

**PROVED:** Sawin's chromatically constrained Ramsey numbers F(3,k) — the
largest n such that K_n splits into k triangle-free 3-colourable graphs —
satisfy F(3,k) ≥ max_t C(k,t)·2^{k−t} ≥ 3^k/(k+1), so their exponential growth
rate is exactly 3 (the trivial upper bound), improving the rate 2^{3/2} of the
OpenAI/Morris palette recursion; and, for every fixed j, F(j,k) ≥ j^k/poly(k)
(unconditional for j ≤ 4).

## 2. Contributions

1. **PROVED** — Theorem 3.1: F(3,k) ≥ C(k,t)2^{k−t} for every t; hence
   F(3,k) ≥ 3^k/(k+1) and F(3,k) ≥ (1+o(1))·3^k·3/(2√(πk)); lim F(3,k)^{1/k} = 3.
   Half-page construction (blocks indexed by t-subsets of the colour set, a
   binary cube in each block, cross edges coloured by comparing one sign from
   each block); mechanically verified up to K_1792 with 8 colours.
2. **PROVED** — Corollary 4.4: F(j,k) ≥ j^k/(2k+2)^{d_j} with d_2 = 0, d_3 = 1,
   d_4 = 3; lim F(j,k)^{1/k} = j for every j (j ≥ 5 uses a cited lemma).
   The j = 3 → 4 step uses an explicit 9-entry "saturated map" gadget found by
   SAT; checked on K_56 (6 colours) and K_98 (7 and 8 colours).
3. **CERTIFIED** — first exact values beyond F(2,k) = 2^k: F(3,3) = 14 (DRUP
   proof checked by the repository's own checker), F(3,4) = 41 (cube-and-
   conquer over the certified census of the 33,831 extremal 14-sets; 37
   DRUP-checked refutations), F(4,3) = 16; bounds F(3,5) ≥ 122, F(3,6) ≥ 365,
   F(4,4) ≥ 44 (witnesses with explicit proper colourings, all verified from
   the definition).
4. **CERTIFIED** — Wiesner's conjecture F(j,k) ≥ Σ_{i≤j} S(k+1,i) is exact at
   (3,3) and (3,4), a strict lower bound at (4,3) (15 < 16), and its j = 3
   value (3^k+1)/2 is realised for k ≤ 6 by the set E_k of ternary words with
   an even number of 2's; E_3 is one of 37 inequivalent extremal 14-sets.
5. **PROVED** — an LYM barrier: antichain palette constructions cannot exceed
   max_t C(k,t)2^{k−t}; density 1/2 needs nested palettes (E_k has them). Every
   local colouring rule tried for E_k fails (documented), so Wiesner's j = 3
   conjecture — which would give lim F(3,k)/3^k ≥ 1/2 — stays open.
6. **CERTIFIED** — no circulant 4-colouring of K_46, K_50 or K_51 with
   triangle-free classes and no circulant witness for F(4,4) ≥ 45; the
   quartic-residue colouring of K_41 has 4-chromatic classes.

## 3. Figure specs

- **Figure 1 — the ratio F(3,k)/3^k.** Data: the exact values 2/3, 5/9,
  14/27, 41/81 (k = 1..4) and the lower bounds 122/243, 365/729 (k = 5, 6),
  from the `README.md` results table; the Theorem 3.1 curve
  max_t C(k,t)2^{k−t}/3^k for k = 1..12 (compute from the formula: 2/3, 4/9,
  12/27, 32/81, 80/243, 240/729, …), and the line 1/2. Sentence: "The known
  values sit on Wiesner's (3^k+1)/2 and decrease toward 1/2, while the proved
  construction (the lower curve) decays like 1/√k — the gap between the two
  is exactly what is open."
- **Figure 2 — the antichain construction for k = 3, t = 1.** Data: `code/antichain.py 3 1`
  (12 vertices in three blocks of 4; block P = {c} is the square {±1}^2 on the
  other two coordinates). Draw the three blocks, the binary-cube colouring
  inside each, and the cross rule "colour a if u_a = v_b, else b" on one pair
  of blocks. Sentence: "Inside a block only two labels occur per colour, so
  triangles cannot form; between blocks the colour is chosen so that the
  active endpoint's label is determined by the other endpoint, which kills
  the mixed triangles."
- **Figure 3 — the even-weight set E_3 and its colouring.** Data:
  `data/witnesses/col_sym_k3.txt` (14 points of [3]^3, the Z_2 × Z_3-invariant
  colouring). Show the 3×3×3 grid with the 14 points and the three colour
  classes as three 14-vertex graphs, each with the coordinate as its proper
  3-colouring. Sentence: "Fourteen of the twenty-seven cells — those with an
  even number of 2's — admit a colouring in which no line carries three
  points and each colour class is triangle-free and 3-coloured by its own
  coordinate."
- **Figure 4 — the K_14 circulant.** Data: `data/witnesses/circ_14_3_3.json`
  (Z_14 with difference classes ±{1,4,7}, ±{2,3}, ±{5,6}). Sentence: "The
  smallest exact value, F(3,3) = 14, is attained by a circulant colouring:
  three sum-free difference classes, each a 3-colourable triangle-free
  circulant graph."

## 4. Caveats the page must carry

- Sawin's question asks about the constant lim F(j,k)/j^k; the theorems here
  settle only the exponential rate (polynomial loss). They do not answer his
  question.
- Corollary 4.4 for j ≥ 5 depends on the saturated-map lemma (OpenAI *Ten
  Advances* Ch. 9, Lemma 2.2, attributed there to Alon–Ben-Eliezer–Shangguan–
  Tamo, JCTB 144 (2020)); the JCTB paper was not read (secondary). For j ≤ 4
  everything is self-contained.
- The palette-block recursion itself is the OpenAI chapter's (Aug 2026); the
  new observations are the trivial binary cover (s = 1) and the polynomial-loss
  analysis for fixed j. Morris's rate 2^{3/2} for three-colourable classes is
  quoted from his exposition (erdosproblems.com/static/183-Morris.pdf, Theorem
  2.1), read in full.
- r_3(3) = 17 (Greenwood–Gleason 1955) and r_3(4) ≤ 62 (Fettes–Kramer–
  Radziszowski 2004) are cited through Radziszowski's dynamic survey
  (secondary); Kalbfleisch–Stanton's uniqueness of the K_16 colourings
  likewise.
- The F(3,3) ≤ 14 and F(3,4) ≤ 41 refutations and the completeness of the
  14-set census are certified (DRUP checked by `tools/satcert/rup_check.c`);
  the two large proof collections (109 MB and 380 MB) are not in the
  repository — hashes are, and the scripts regenerate them; the circulant
  non-existence statements are SAT verdicts without proof logs.
- Wiesner's conjecture is exact in all cells computed for j = 3 but not at
  (4,3); the page must not present it as a theorem or as "verified".
- F(3,5) ∈ {122, 123} and F(4,4) ∈ [44, 61] are open; "no circulant witness"
  is not "no witness".

## 5. Existing page

None. Add the index row (top-level README) and link the page from the
conjecture README header once live.
