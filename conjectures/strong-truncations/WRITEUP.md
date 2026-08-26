# Session narrative — 2026-08-26

The mandate was to pick a new external problem. Three scouts ran over
the Erdős database, OEIS conjectures, and recent arXiv open-problem
sections; the sandbox turned out to have every primary mathematics site
egress-blocked (arXiv, OEIS, erdosproblems.com, MathOverflow), which
shaped the whole day: literature only through search snippets, OEIS only
through its git mirror on raw.githubusercontent.com, and nauty only
because the pynauty *source* distribution on PyPI carries the full nauty
2.8.8 tree, generators included. Kardoš's Problem 4.1 won the selection
on tractability: decide strong 6-edge-colorability of truncations of
cubic (multi)graphs, a family whose exhaustive generation is a solved
problem (geng/multig, counts pinned to A002851/A000421) and whose
instances are 60–90-edge coloring problems.

The plan was a verification census — the expected outcome was "all
6-colorable to order N, extending Han–Cui". The first full run at
quotient order 12 instead reported 57 quotients whose truncations were
not 6-colorable, plus 46 the engine couldn't decide under its node cap.
The immediate suspicion was an engine bug: the literature (via
snippets) said Lin–Lin's 7-attaining claw-free cubic graphs all contain
diamonds, and truncations are diamond-free, so dozens of 36-vertex
counterexamples would mean either a new result or a broken conflict
builder. An independent Python+CaDiCaL engine, sharing no code, built
straight from the induced-matching definition, confirmed UNSAT on the
three instances tried. Sweeping the skipped small orders found the real
headline: at quotient order 6 there is already one bad quotient — two
doubled edges, each pair sharing a common neighbour — whose truncation
is an 18-vertex diamond-free claw-free cubic graph with strong
chromatic index 7.

Verification was then made deliberately excessive, because a small
counterexample to a posed problem is exactly the kind of claim that
dies of embarrassment: definitional anchors (C₅ = 5, C₆ = 3, C₇ = 4,
K₃,₃ = 9, Petersen = 5, prism = 9) reproduced; the geng path (all
41,301 cubic graphs on 18 vertices, claw/diamond filtered by
definition, colored) agreeing with the multig+truncation path on both
the count (six DFCF graphs, matching A000421(6)) and the unique
exception, with equal nauty canonical forms; a DRUP proof of UNSAT at 6
colors checked by this repo's own from-the-definition RUP checker; a
verified 7-coloring; and a corrupted-witness negative control against
the verifier itself.

The pattern in the data — every bad quotient contained a doubled edge
whose endpoints share a neighbour — suggested a local obstruction, and
the dart reformulation (worked out in the morning as an engine design
aid, then promoted to a lemma) made it provable in ten lines: across a
doubled edge the two triangle-side colors are forced onto the two
colors missing from both endpoint palettes, and at a common third
neighbour those two forced colors have nowhere to live. The
machine-enumerated boundary-state calculus independently reports the
balloon piece has zero realizable interface states, and as a bonus the
same enumeration gave the dumbbell transfer relation in closed form
(both stems export the same spare pair; 15·12 = 180 labelled pairs,
matching the hand count exactly).

What was expected to be the result — the verification census — became
the supporting cast: full double-verified censuses to quotient order 16
with the balloon characterization holding exactly (the sole
balloon-free failure being the triple edge, i.e. the prism), a
7-coloring certified for every single χ′ₛ = 7 instance so no step leans
on the (secondary) literature bound, and the intended reading of the
problem (simple quotients) verified for all 556,471 simple cubic graphs
on ≤ 20 vertices — the first systematic check beyond Han–Cui's prisms.

Failures worth recording: the first bulk run wasted nine minutes on
inline exact-χ′ₛ escalation and node-cap thrashing (fixed by a
decide-then-resolve pipeline); a sed negative control that silently
didn't corrupt anything (the verifier looked good for a vacuous
reason — recut in Python); an empty leftover file that shadowed the
order-10 census in the χ′ₛ = 7 pass, caught only because 789 ≠ 808; and
the attempted uniform construction for the converse (3-edge-coloring ×
signs), which reduces to three GF(2) parity systems that are not always
solvable and so proves only a sufficient condition — the converse of
the balloon characterization stays a conjecture.

What this session did not do: read any primary source (every citation
is marked (secondary) and the novelty claim is at search-snippet
confidence); prove the balloon-free direction; run the with-diamond
half of the claw-free class; or check the counting sequence 1, 4, 19,
102, 682 against OEIS proper. Those are the next session's threads, and
the first local session with real egress should start by reading
Kardoš, Lin–Lin, and Han–Cui in the original before anything is said
out loud.
