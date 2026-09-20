# Session narrative — 2026-09-09

## Choosing the problem

The morning arXiv listing (math.CO, 9 Sep) carried Shallit's four-day-old
"An infinite walk in ℕ¹⁶, using only unit steps, with no three collinear
points". Its last section defines k_min, the least alphabet size admitting an
infinite word with no weak abelian square, states 4 ≤ k_min ≤ 16, lists four
candidate morphisms (k = 5, 6, 7, 8) the author could not prove, and invites
other researchers to improve the bound. Three things made it the pick over
the other candidates of the day (equitable total colourings of cubic graphs,
Ramsey circulants for R(4,21), Erdős–Rado digraph Ramsey numbers, Erdős
#336's h(4), and the internal generalized-Schur rung): it is a fresh,
precisely posed question; it has a computational side (exhaust the
four-letter case, test the candidates) and a theorem side (a construction
with a proof); and the proof mechanism in the paper visibly had slack — the
16 letters are the pairs (t_n, t_{n+1}) of a four-state walk, and the proof
uses the pairs only to force equal endpoint states.

## What happened, in order

**08:00–08:20. Engine and controls.** An incremental collinearity checker
(for each block ending at the new letter, walk back along the ray of its
primitive Parikh direction) in C, validated on L(1) = 1, L(2) = 3, L(3) = 7
(Brown 1971). Shallit's four candidates are 3-free to 20 000.

**08:20–08:30. The four-letter case is not a search.** The exhaustive tree
over four letters has 2.5 million nodes to length 30 and 32 million to
length 40, the counts multiplying by about 1.3 per letter (the full run to
length 46, done later, gives 28.9 M words and a ratio drifting down from
1.30 to 1.27). That killed the "certify k_min ≥ 5" plan
within ten minutes and moved the session to the upper bound.

**08:30–08:50. The dragon.** Shallit's proof needs, for the valuation lemma,
that the walk halves cleanly: {u_{2n}, u_{2n+1}} = {u_n, i u_n} with a fixed
order. Asking which orders the lemma tolerates — the descent needs equal
endpoint states to descend and the correction term to vanish or be 2·(unit)
— showed the order may depend on the parity of n and on nothing else. The
alternating order makes every turn ±90°, so only eight (direction, turn)
pairs occur; the alternating-order walk is the Heighway dragon curve. The
valuation lemma was checked on 1.1 million pairs and the eight-letter word
to 30 000 before the proof was written.

**08:50–09:05. From eight to seven.** All 4011 codings of the eight letters
onto 3…7 classes were tested to length 3000: eight survive, all with seven
classes. For the antipodal same-turn identifications a proof appeared at
once: two telescoping indicators (parity, and membership in {0,1}) force
equal endpoint states, and the walk that moves only on right turns has a
displacement computable from the merged Parikh vector.

**09:05–09:20. Priority check, and a surprise.** The Cambie–Kalviainen
repository's README says "a proposed six-dimensional upper bound awaits
independent review". Its research folder holds a Sept 5 two-page draft by
Kalviainen (alternating digit sign, Cambie's offsets, six step vectors), a
Sept 5 note by Cambie (fourteen), a Sept 6 note by Shallit on weak abelian
cubes, and an AI checkpoint asking, first of all, for an independent check of
the six-dimensional argument. So the record to beat was 6, not 16, and our 7
is a weaker bound by a different route. We read the draft line by line
(NOTE §5) and reproduced its numbers; we found no gap.

**09:20–09:45. Can the two ideas combine?** The two mechanisms — alternating
digit sign (theirs) and alternating child order (ours) — are members of one
family, parametrised per binary level by a sign and an order rule. We
enumerated all periodic patterns of period ≤ 4: only two eight-transition
words exist (theirs, coding floor 6; ours, floor 7), all others have 12–16
transitions and none codes onto five letters (to length 1200). A search for
four-letter cyclic uniform morphisms (length ≤ 16) found none; the
five-letter search recovered Shallit's length-14 candidate and eleven more.

**09:45–.** Write-up.

## What failed

- *The certified lower bound.* Exhausting four-letter 3-free words is
  hopeless (exponential growth); nothing structural over four letters came
  to mind either.
- *Merging two pairs.* No coding of the dragon word onto six letters
  survives length 3000, so the dragon route stops at seven no matter how the
  proof is organised; the natural functionals (parity, half-plane, one-turn
  walk) are exactly what the seven-letter coding preserves, and any second
  merge loses one of them.
- *The mixed merges (r,−)~(r+1,+).* Survive to 30 000, but every weight of
  the form i^r(a + bδ) that agrees on the two letters gives a displacement
  functional that collapses to boundary terms (a − ib = 0). No proof.
- *Beating six inside the family.* The sign/order family has no member with
  fewer than eight transitions (two turn values are forced: one turn value
  would make the state sequence periodic), and no coding onto five letters
  of any member.
- *Shallit's five-letter candidate.* Not attempted beyond the 20 000-letter
  check; the repository's checkpoint records extensive unsuccessful
  AI-assisted attempts at a descent proof, and the template method for
  weak abelian squares has a rational-coefficient template set that need
  not be finite. A day's project at least.

## What the session would have been without the repository read

A "k_min ≤ 7, halving Shallit's bound" headline. The honest headline is
"k_min ≤ 7 by a new mechanism, independently proved; the stronger draft
bound 6 reviewed and confirmed". The difference is one web fetch.
