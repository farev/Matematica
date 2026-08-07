# PAGE handoff — circular-thresholds (session 2026-08-06)

A page for this conjecture **already exists**; this is an **update**, and a
major one: the strongest result changed from "no open case settled" to an
open case settled.

## 1. Headline claim

**PROVED.** `CRT_W(6) = RT(6) = 6/5`: circular 6-letter threshold words
exist at infinitely many lengths (`39·21^j` for every `j ≥ 0`) — settling
the `n = 6` case of the weak Currie–Mol–Rampersad conjecture, which
Mol–Rampersad (2020) list as open for `4 ≤ n ≤ 44` *(openness is
secondary-sourced; see caveats)*.

## 2. Contributions (labelled)

1. **PROVED** — Theorem P6: `C(6) ⊇ {39·21^j : j ≥ 0}`, hence
   `CRT_W(6) = RT(6) = 6/5`. Generator: a certified 21-uniform binary
   morphism in Pansiot's encoding; seed: the session-1 certified spectrum
   witness at length 39, re-encoded. First pumped words (lengths 39, 819,
   17 199) verified directly from the definition, independently of the
   theorems.
2. **PROVED** — Theorem P5: `C(5) ⊇ {28·21^j}`, hence
   `CRT_W(5) = RT(5) = 5/4`. **Must carry the flag:** possibly a
   rediscovery — Tunev (arXiv:2512.24581, Dec 2025, in Russian) reportedly
   constructs circular threshold words for some odd `n ≥ 5`; unread here.
3. **PROVED** — the machinery (new, elementary, one page each): the slot
   lemma (decoded equal-letter patterns are intrinsic to the code bits); an
   exact transfer lemma (`period-p` letter stretches of length
   `ℓ ≥ p+n−1` correspond exactly, with gap `n−1`, to bit-periodic
   stretches whose period block has trivial monodromy in `Sym(n)`); Theorem
   MC (a finite certificate — five checks — that a uniform binary code
   morphism preserves code-freeness); Lemma PC (circular pumping in the
   code). Together: a decidable route `morphism + seed ⟹ CRT_W(n) = RT(n)`.
4. **PROVED** (control; result known) — the same pipeline re-derives
   `CRT_W(3) = 7/4` with `k = 19` binary generators, seeded by the
   session-1 seed re-encoded; verified to length 137 180.
5. **CERTIFIED** — the `n = 4` dichotomy: the identical search
   (all monodromy classes, `k ≤ 46`; a two-level substitution engine; a
   stronger preservation filter to `k ≤ 26`) finds **nothing** at `n = 4` —
   every one of tens of thousands of pooled pairs per length is refuted by
   an explicit offender — while `n = 3, 5, 6` yield theorems. Pansiot's
   exceptional alphabet (`RT(4) = 7/5`) resists inside its own encoding.
6. **CERTIFIED** — `n = 8` intermediate state: 44 viable pairs at `k = 28`,
   none passing the certificate's injectivity hypotheses — the identified
   next tool (a synchronization-based variant) would plausibly unlock
   `n = 8, 10, 12, …`.

## 3. Figure specs

* **Figure A (the dichotomy).** Data: `data/pansiot_sweep_n{3,4,5,6,8}.log`
  (per-`k` lines: pool size, candidate count). Plot candidates-per-`k` for
  `n = 3, 4, 5, 6, 8` (log-y, `k` on x; zeros marked). Reader's sentence:
  "Under the identical search, alphabets 3, 5, 6 and 8 light up from
  `k ≈ 7–28`, while `n = 4` stays at zero through `k = 46`."
* **Figure B (the theorem's object).** Data: `data/pansiot_certified.txt`
  (the `n = 6` `k = 21` pair and the `m_0 = 39` seed);
  render the seed cycle and its first pumped image (length 819) as circular
  color rings (6 colors). Reader's sentence: "One certified morphism and one
  39-letter cyclic seed generate circular threshold words at every length
  `39·21^j`."
* **Figure C (why it works — optional).** A schematic of the transfer lemma:
  a period-`p` letter stretch above, its bit shadow below, the `n−1`-letter
  left extension marked, `g = id` on the period block. Reader's sentence:
  "Repetitions in the word are exactly trivial-monodromy periodicities in
  its code, with a fixed bookkeeping gap of `n−1` letters."

## 4. Caveats the page must carry

* **Openness of `n = 6` is secondary-sourced** (Mol–Rampersad 2020 snippet;
  no primary read — egress blocked both sessions). The mathematical theorem
  is unconditional; its *novelty* is not.
* **Tunev, arXiv:2512.24581 (Dec 2025, Russian), unread:** reportedly covers
  some odd `n ≥ 5`; `n = 5` here may be a rediscovery; `n = 6` (even) is
  outside its reported scope. Must be read before any priority language.
* **The three session-2 lemmas were proved and checked within one session**;
  the `n = 3` end-to-end control and the direct verification of pumped words
  are the independent evidence. No second human or formal verification yet.
* Moulin Ollagnier's Dejean-conjecture machinery (unread) works in the same
  encoding and relates repetitions to the symmetric-group identity; the
  transfer lemma should be presumed to overlap it in content until checked.
* The `n = 4` emptiness is a **bounded certified search** (`k ≤ 46`, stated
  engine ranges, one disclosed capped cell), not an impossibility theorem.
* All session-1 caveats (single-solver UNSAT verdicts for the bulk of the
  spectra) still apply to the session-1 results the page describes.

## 5. What changed since the existing page

* The strongest result line: from "machinery + spectra, no open case
  settled" to "**`n = 6` settled** (and `n = 5`, flagged), `n = 4`
  certified-empty for the ansatz".
* New: the whole Pansiot-code section (transfer lemma, certificate, pumping)
  and the `n=3/4/5/6/8` dichotomy data.
* The session-1 spectra gained a new role: their certified witnesses are the
  *seeds* of the new theorems (the `m = 39` witness at `n = 6`, `m = 28` at
  `n = 5`).
* The prior-work section must now name Tunev (Dec 2025) prominently.
