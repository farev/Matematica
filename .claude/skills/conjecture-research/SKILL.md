---
name: conjecture-research
description: Run a genuine research session on any open mathematical conjecture or problem, however famous or old — mounting a real attack, proving structural lemmas, running certified large-scale computations, engaging the current literature, and extracting publishable contributions (new exact constants, sharpened inequalities, empirical laws, audits of recent papers) whether or not the conjecture falls. Use whenever the user asks to attempt, attack, or make progress on an open conjecture or unsolved problem, to "find a conjecture and try to solve it", to extend or respond to a recent math paper (arXiv), to compute new exact values in a research model, or to do original mathematics research of any kind — even if they don't use the word "conjecture". Not for textbook problems or competition math (use math-olympiad for those).
---

# Conjecture research sessions

Aim at the conjecture itself. Attack it like it could fall — the history of
mathematics is full of "impossible" problems that yielded to an angle nobody
had tried, and an attack that pulls no punches is also the attack that
generates the best byproducts. At the same time, structure the session so
that the attempt produces *genuine, defensible results either way*:
rigorously proved lemmas, certified computations, sharp empirical laws with
out-of-sample validation, honest audits of the newest papers, sharpened
inequalities, and — when it works out — theorems. The one thing that is
never acceptable is theater: claiming a solution that isn't one, or
dressing up heuristics as proof. "The conjecture survives, here is exactly
what I established and where the wall is" is a strong outcome; a fake proof
is a worthless one.

Work through the phases below in order, but treat them as a loop, not a
pipeline: computation feeds theory, theory feeds computation, and the
literature re-aims both. Run long computations in the background and do
theory while they run — wall-clock time on compute is free thinking time.

## Phase 0 — Choose the target, then find its surfaces

**Any conjecture is fair game.** Riemann, Collatz, Goldbach, twin primes, a
problem open since 1878 or since Euclid — age and fame are not
disqualifiers, and if the user names a target, never argue it down. When
choosing freely, choose whatever is genuinely most interesting; interest
sustains the deep engagement that findings come from.

What tractability governs is not *which* problem to attack but *where to
grip it*. Every conjecture — including the ancient monsters — has surfaces
where real work can start; part of the session's job is locating them:

1. **Computational surfaces.** Instances to verify, dynamics to simulate,
   constants to compute, records to extend. Even RH has zero-counting,
   moment computations, and de Bruijn–Newman bounds.
2. **Provable micro-structure.** Parity constraints, invariants,
   propagation rules, equivalent reformulations. Prove something true and
   organizing within the first hour — it will aim everything else.
3. **The recent literature**, however sparse. The newest serious paper on
   any problem carries stated open questions, truncated computations, and
   unaudited hypotheses (Phase 5). For old problems, the newest *partial
   result* plays this role.
4. **Heuristics to quantify.** Almost every believed conjecture has a
   "why it should be true" story; measuring, testing, and sharpening that
   story is real research and sometimes reveals the mechanism.

If the direct assault stalls, that's information: record the precise
obstruction and pivot to the surface where progress is real. State why you
chose the problem and what both a maximal and a realistic win look like.

## Phase 1 — Independent exploration BEFORE deep literature reading

Explore first, read second. Two reasons: reading first anchors you to the
authors' framing and kills independent angles; and independently
rediscovering a known result is strong validation of your approach (record
it as validation, never as a contribution — see Honesty protocol).

- Compute small cases and *look* at them. Print the objects.
- Construct near-miss counterexamples: nearby sequences/structures where
  the conjectured property FAILS. This proves the conjecture is not a
  triviality and reveals which features carry it (in a Gilbreath session,
  showing that shuffled prime gaps fail instantly reframed the whole
  problem as "seed + statistics").
- Ask what is *forced* (parity, boundedness, monotonicity, symmetry,
  invariance under reversal/scaling) and prove those facts as Lemmas 1, 2,
  3 with real proofs. They will organize everything that follows.

## Phase 2 — Structural lemmas that convert computation into proof

The single highest-leverage step: find and prove a lemma that turns a
finite computation into a rigorous infinite family of statements — a
propagation/absorption criterion ("if row k has property P, all deeper
rows inherit it"), a descent principle ("defects never appear
spontaneously"), or a reduction to a minimal equivalent form ("the
conjecture holds iff this one boundary quantity stays ≤ 1"). Without such
a lemma, large computation is anecdote; with it, computation is a
certificate. Also derive the exact equivalent form of the conjecture in
your notation and keep it visible — every later experiment should be
phrased against it.

## Phase 3 — Scaled computation, and empirical laws with predictions

- Verify the conjecture as far as practical **via the Phase-2 criterion**,
  and state precisely what is now proven ("holds for the first N rows"),
  and how it compares to existing records (verify the record via
  literature; do not claim records casually).
- Measure the dynamics: decay rates, growth exponents, thresholds. Fit
  empirical laws — then use them to **predict the next, bigger run before
  it finishes**. An out-of-sample prediction that lands (or misses — also
  informative) is worth ten retrospective fits. Report the law with its
  drift and misfit, not just the best case.
- Size the compute: check RAM/cores first (`sysctl hw.memsize hw.ncpu`
  on macOS, `nproc` and `free -g` on the Linux cloud sandbox), use NumPy
  vectorization, segmented sieves, tiered sampling
  (many samples shallow, few samples deep), and background jobs. See
  [references/computational-patterns.md](references/computational-patterns.md)
  for recipes (sieves, tiered Monte Carlo, run-length scans, exact
  rational integration, background-job orchestration).

## Phase 4 — Read the literature: primary sources, in full

- Search for the newest work (arXiv, Annals/Math. Comp./Math. Ann., expert
  blogs). Recent-months papers are gold.
- **Download the actual PDF and read it** — multiple page batches, main
  theorems verbatim, their notation mapped onto yours. Never build on a
  secondhand summary of a math paper; summaries garble quantifiers and
  constants, and your contribution claims will inherit the garble.
- Cross-check every planned claim against the paper's full text (grep the
  extracted text for the relevant constants/terms). Check the OEIS for any
  sequence or constant you believe is new.
- Rewrite your positioning honestly: what of yours is replication, what is
  new measurement, what is genuinely absent from the record.

## Phase 5 — Mine the newest paper for attack surfaces

Recent papers advertise their own soft spots. Look for, in order of value:

1. **Stated open questions and "we cannot prove" admissions** — e.g.
   "we cannot even prove the sequence is bounded". These are invitations.
2. **Computations the authors stopped early** ("with more effort one can
   compute…"). Extending an exact computation the authors truncated is a
   concrete, citable contribution — new constants, new terms.
3. **Hypotheses never audited against real data.** If a criterion needs
   "no block longer than L" in real primes, *measure the actual maximal
   block* and report the margin. First empirical audits are contributions.
4. **Inequalities with structural slack.** If their key bound uses one
   channel/direction/term of a symmetric situation, try using both — a
   symmetry the proof ignores often gives a constant-factor sharpening.
5. **Models with a knob** (tail weight, distribution, parameter) the
   authors fixed. Turning the knob (e.g. bounded vs exponential tails)
   isolates the mechanism and can kill or confirm their heuristics.

## Phase 6 — Exact results demand machine-checkable certificates

When claiming an *exact* value (a rational constant, an exact count):

- **Design the certificate before the computation**: an algebraic identity
  the output must satisfy exactly in ℚ (a partition of unity, a total
  measure, a sum rule). "Monte Carlo agrees" is corroboration, NOT a
  certificate — in a real session, an exact-value bug of size 1.25×10⁻⁷
  sat 0.8σ from the Monte Carlo and only the exact identity caught it.
- **Validate the pipeline on all known values first**; only then produce
  new ones.
- Use exact arithmetic (`fractions.Fraction`, integer linear algebra —
  Bareiss determinants, fraction-free elimination). Floating point may
  choose combinatorics (which triangulation, which pivot) but never
  values; cross-check float-guided combinatorics two independent ways and
  fall back to a fully exact method on disagreement.
- If a result's certificate fails, **publish it as uncertified** with the
  failure disclosed, or fix the pipeline. Never silently promote it.

## Phase 7 — The empirical-discovery loop

When data hints at structure, escalate deliberately:

1. Flexible regression (many free parameters) to detect the signal.
2. Collapse to the most parsimonious law — the moment a one- or
   two-parameter formula matches a many-parameter fit, you have found
   structure, not noise.
3. Model-free confirmation: subsequence exponents, ratio tables at special
   indices — things no fit can fake.
4. Cross-validate (fit half, predict half), then **out-of-sample on new
   scales**: fit on existing data, predict, *then* run the bigger
   computation. Report systematic deviations as findings, not failures —
   "the law under-predicts the extremes" is itself a discovery.
5. Mechanism tests: change one knob (initial distribution, tail, modulus)
   and check the structure responds as the proposed mechanism demands.
6. Precision audits: chaotic iterations decorrelate float32 from float64
   pathwise, so audit *statistically* (independent runs, σ-comparison),
   never by pairing trajectories; state the bias bound next to the effect
   size.

## Phase 8 — Theory attempts

- Attack where your proven machinery composes: symmetry + telescoping +
  independence + Jensen carried a factor-2 sharpening of a published key
  inequality in one session. Ask "what does the published proof throw
  away?" (an absolute value used one-sidedly, a max bounded by one term, a
  symmetry unused).
- **Verify every step of a claimed proof numerically before writing it
  up** — pointwise on millions of samples where the step is an inequality
  between random quantities, exactly where it is an identity. A proof that
  survives a 4-million-sample pointwise check of each lemma is a proof you
  can defend.
- Know the boundary of the technique and say it: if the argument needs
  independence that fails for middle terms, state that as the precise
  obstruction and leave it as a formulated open problem — a well-posed
  problem is a contribution.
- Budget honestly: derivation sketches that would take "a page of careful
  probability" you cannot verify should be stated as conjectures, not
  theorems.

## Phase 9 — Deliverables

Produce, in the conjecture's own directory (`conjectures/<name>/`, which
must stand alone, no sideways imports between conjectures):

1. **WRITEUP.md** — the session narrative: lemmas with proofs, all
   experiments, failures included. This is the lab notebook.
2. **NOTE.md** — a preprint-style research note: abstract, numbered
   propositions/theorems with proofs, tables, honest caveats ("fits
   describe range X and carry no asymptotic guarantee"), references,
   reproducibility section. This is the presentable artifact; keep it
   free of session chronology.
3. **README.md** — index: file → what it does → headline result.
4. **Runnable scripts** with fixed seeds; data as CSV; certificates as
   files (e.g. `c6_certified.txt`).
5. When new constants/sequences arise: an **OEIS submission draft**.
6. **log/YYYY-MM-DD-<conjecture>.md** — the daily log entry, in the exact
   format CLAUDE.md fixes: Target, Result, What failed, Next. "Nothing" is
   a valid result and gets logged like any other session.
7. **PAGE.md** — the handoff to the local publishing pass, written only
   when the session's strongest result would change the conjecture's row
   in the top-level README. Follow the contract in CLAUDE.md: headline
   claim with its label, numbered contributions carrying the actual
   numbers, a spec per figure with the one sentence that figure earns,
   caveats a referee would poke, and, if a page already exists, what
   changed since it was written.

**Never build the page itself in a cloud session.** The sandbox holds the
repository and CPU and nothing else: no site source, no deploy
credentials, no browser to verify in. Site HTML written from here comes out
in the wrong style and gets discarded (this has happened once already).
PAGE.md is the whole handoff, and the `research-page` skill builds the page
afterwards on the machine that has the site source. Put publication paths
in the writeup instead: contacting the paper's authors (theorem and data
speak to their sections), OEIS, an arXiv note.

**Writing style for all prose deliverables:** avoid em-dashes. Use one
only when absolutely necessary or when it clearly improves the sentence;
otherwise reach for a comma, colon, period, or parentheses. (Fabian's
standing preference, 2026-07-29.)

## Honesty protocol (load-bearing — this is what makes the work citable)

- **Novelty check before every claim.** Before presenting anything as new,
  re-read the relevant section of the primary source. When a "new"
  inequality turns out to be the paper's own key lemma found
  independently, record it prominently as a rediscovery — it validates
  the mechanism and it is not a contribution. The correction belongs in
  the writeup.
- **Certified / uncertified / conjectural** are three different labels;
  never blur them. State each result's label explicitly.
- Keep failed attempts and their exact obstruction in the writeup — the
  epsilon you could not cross is information for the next session.
- Empirical laws get validity ranges and the caveat that asymptotic
  turnover cannot be excluded, especially when the known theorems only
  force weaker growth.
- Verification claims name their certificate ("rows 1..N by the
  propagation criterion"), not just their size.

## Session mechanics

- Run every computation expected to exceed ~2 minutes in the background;
  interleave: launch compute → do theory/literature → collect. Keep 2–4
  jobs in flight when the machine allows.
- Cross-validate the *machine* too: check RAM before sizing arrays; time a
  small run before launching the big one.
- When a background result lands, update the running documents
  immediately — placeholders (`[PENDING: out-of-sample]`) in the NOTE keep
  the document truthful at every instant.
- End the session only when the deliverables exist and every claim in
  them carries its correct label.
