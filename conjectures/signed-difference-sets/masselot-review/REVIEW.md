# Bounded review: "Two Small-Order Classification Theorems for Signed Difference Sets" (Masselot, v1.0, 2026-08-12)

Reviewer: Fabián Arévalo (farev/Matematica), with substantial AI
assistance (Claude); every computational statement below was produced
by review-owned code committed under `masselot-review/` and can be
rerun from the commands at the end. Review date: 2026-08-12. Scope as
requested by the author: (i) theorem framing, (ii) completeness of the
quotient reductions, (iii) earlier exact resolutions.

## Summary verdict

Both theorems are correct as stated, and I can say so at an unusually
strong standard for a referee report: every nonexistence leg of both
theorems was re-derived here by complete searches written independently
of your code (and of Gordon's), all sixteen existence witnesses pass a
third validator that shares no lineage with your two, and every count
your note reports in Sections 5 to 7 reproduces exactly. The one
external datum your Corollary imports (cyclic C36, from the frozen
repository) can be discharged: the C18 quotient system of (36,29,4) is
empty, which proves the C36 and C2 x C18 cases simultaneously and makes
the abelian order-36 classification self-contained. Details below.

## What was verified, and how

Independence: the verification code here (`qrlib.py`,
`check_targets.py`, `verify_witnesses.py`) was written for this review
from the definition alone. The witness referee is this repository's
`sdslib.check_sds`, written 2026-08-09 against Gordon's convention,
sharing no code with your tuple/dictionary validator, your mixed-radix
validator, or Gordon's `is_sds`. All arithmetic is exact (Python ints;
NumPy int64 only for batch correlation filtering). Machinery controls
were run before any target: the chain code reproduces, set for set, the
40 labeled SDS(20,11,2,[20]) of this repository's 2026-08-09 complete
enumeration; the two-layer code returns zero on SDS(36,29,20,[6,6]),
agreeing with this repository's direct exhaust, and provably does not
prune the branch of a known SDS(36,11,2,[6,6]) witness.

| claim in the note | my independent result | agree |
|---|---|---|
| 16 witnesses valid (6 of them the order-32 constructions) | 16/16 pass `check_sds`; the six order-32 file hashes match §4's table byte for byte | yes |
| §5: 9,528 C8 vectors after sum+norm; 56 solutions; 5 affine orbits of sizes 8,16,8,16,8; 12 C16 survivors over orbit representatives; 248,832 final refinements; 0 solutions | 9,528; 56; orbit sizes [8,8,8,16,16]; 12; and, with no orbit reduction at all: 144 C16 survivors over all 56 parents, 2,985,984 ternary refinements, 0 solutions | yes |
| §6, C2 x C18: 144 candidates on the order-12 quotient after canonical marginals and norm; 0 solutions | 144 for the canonical pair; complete enumeration over every marginal pair (no normalization): 0 solutions | yes |
| §6, C3 x C12: 420 candidates; 0 solutions | 420 for the canonical pair; complete unnormalized enumeration: 0 solutions | yes |
| §7: 106,353 C3^2 vectors after sum+norm; 9 projection solutions; one orbit, rep (-3,2,...,2); real side (7,2,2,2); one normalized instance; UNSAT by checked DRAT | 106,353; 9 solutions = exactly the nine translates; C2^2 system = exactly the four translates of (7,2,2,2); and a solver-free complete search over all 36 marginal pairs: 16,964,640 marginal-consistent ternary vectors, 0 satisfy the 35 correlation equations (43.7 s) | yes |
| census: 68 targets = the Open entries of order <= 36 at the frozen commit; 58 replications of farev/Matematica; 10 novel | this repository's independent 2026-08-09 fetch of the same commit has exactly those 68 Open cells; verdict-by-verdict diff: 58 agreements, 0 disagreements; the 10 remaining cells are exactly the ones this repository left open | yes |

Total verification cost: under one minute of laptop CPU. Not
re-verified here: your CNF/DRAT chain (deliberately; for C6 x C6 the
direct search above replaces rather than audits it), the Zenodo archive
contents (metadata and hash lines only), and the discovery provenance
of the witnesses (irrelevant to their validity).

## (i) Theorem framing

The framing is sound and, in two places, better than the field's
median practice: the acceptance boundary of Section 2 (raw UNSAT is
not evidence; positives must pass two validators after all
normalizations are forgotten) and the explicit marking of the imported
C36 datum in the Corollary rather than absorbing it silently.

Specific comments, none blocking:

1. Definitions and conventions match Gordon's paper (his Lemma 1.1 is
   your equation (2); his |P| >= |N| convention is your global sign
   normalization) and match the database checker. Your equation (1) is
   the same group-ring identity used by this repository's census, so
   the three projects are provably about the same object.
2. Theorem 1's "if and only if" carries two different evidence types
   (constructive witnesses vs. exhaustive refinement). The note says
   this clearly in Sections 4 and 5; consider one sentence inside the
   theorem environment or its proof pointer, since the theorem will be
   quoted without the surrounding prose.
3. The Corollary can now be upgraded: see "an observation you may want"
   below. With it, Theorem 2 plus Corollary collapse into one
   self-contained statement ("no abelian group of order 36 admits a
   signed (36,29,4) difference set") with no database dependency.
4. Section 3's projection lemma deserves its ancestry: the sum and
   sum-of-squares moments of your equation (4) are Lemma 5.2 of
   Gordon's paper (intersection numbers, used there for his orbit
   exhausts, and standard in the difference-set literature, e.g.
   Beth, Jungnickel and Lenz VI.5.4). Citing that connects your
   full-convolution version to the classical tool and costs nothing.
5. Section 9's evidence-type accounting (16/13/4/9/14/12) matches the
   machine-readable census exactly; I checked the histogram against
   `current_census.json`.
6. Two cosmetic nits. The witness file `sds_25_12_1_c5xc5.json` uses
   `group: "C_5 x C_5"` and `frozen_at_utc` where the other fifteen
   use `group_invariant_factors` and (in one case) `frozen_date`;
   harmonizing the schema will spare downstream parsers. And your
   email called the source the "La Jolla covering repository"; the
   note's name ("La Jolla Signed Difference Set Repository") is the
   right one, the Covering Repository being a different database.
7. A remark you may enjoy for the discussion section: at (32,20,4)
   existence splits exactly at cyclicity, while this repository's
   (32,28,12) row splits at containment of Z4 x Z4 (exists in [4,8]
   and [2,4,4] only). So no single subgroup-containment criterion
   explains order 32; whatever the mechanism is, it is
   parameter-dependent.

## (ii) Completeness of the quotient reductions

I probed this three ways: checking your stated arguments, re-deriving
the ingredient facts they rely on, and re-running every reduction with
the symmetry arguments removed so that completeness no longer depends
on them.

1. The projection lemma and its constants are correct: for kernel size
   m the projected vector has cells in [-m, m], peak k + (m-1)lambda
   and off-peak m lambda. My systems use exactly these and reproduce
   your counts, so we agree at the level of the actual constraint
   systems, not just the prose.
2. Section 5 (C32). Your completeness argument has three load-bearing
   claims. (a) The C8 enumeration is complete: confirmed, 9,528 and
   then 56 as complete counts from a bound-and-prune DFS written
   independently. (b) The affine reduction is sound because the
   actions lift: true, since translations lift along surjections and
   the unit-group reductions (Z/32)^x -> (Z/16)^x -> (Z/8)^x are
   surjective, so multiplication by a unit of Z8 extends to an
   automorphism of C32. (c) Every survivor is refined explicitly:
   confirmed, and made moot here, because my re-run refines all 56
   C8 solutions with no orbit reduction anywhere (144 C16 survivors,
   2,985,984 refinements, zero solutions). Your ledger's record of the
   caught-and-removed symmetry bug (quotienting a normalized slice by
   the full translation group) is exactly the failure mode reviewers
   fear in such ladders; the released pipeline does not contain it,
   and the unreduced re-run confirms its outputs.
3. Section 6 (C2 x C18 and C3 x C12). The normalization step rests on
   two facts the note asserts implicitly: that the marginal systems
   have the claimed solutions and no others, and that the two
   translation normalizations are independent. Both are true: complete
   enumeration gives exactly {(1,6,6) and rotations} for the C3 system,
   {(4,9),(9,4)} for C2, exactly the four translates of (7,2,2,2) for
   C2^2, and exactly the nine translates of (-3,2,...,2) for C3^2
   (with your 106,353 as the sum+norm count); independence is the CRT
   splitting of the translation group. My re-runs then iterate over
   every marginal pair rather than canonical representatives, so the
   exclusions hold with no normalization argument at all. Your
   normalized candidate counts (144 and 420) both reproduce on the
   canonical pair.
4. Section 7 (C6 x C6). The reduction to one normalized instance is
   complete for the same two reasons (single translation orbits on
   both sides, CRT independence), which I verified rather than
   assumed. The stronger statement is that the SAT certificate is no
   longer load-bearing: a direct complete search over all 36 marginal
   pairs (16,964,640 marginal-consistent ternary vectors, exact
   integer filtering through the 35 correlation equations) finds
   nothing. Your DRAT chain and this search now fail independently or
   stand independently; they stand.
5. Residual trust surface, stated for completeness: nothing above
   audits your CNF encoder or the drat-trim run, and my searches have
   their own trust surface (the review code), controlled by the
   known-answer checks listed earlier. The two pipelines share no
   code, which is the point.

Verdict on (ii): the reductions are complete as claimed, and the
classification survives removal of every symmetry argument.

## (iii) Earlier exact resolutions

I know of none, and I looked from a better position than a search
engine: this repository ran a census of the same 68 cells three days
before you froze yours.

- Gordon's paper (read in full for this review): the sporadic table
  has no order-32 or order-36 rows; the only noncyclic SDS reported is
  (18,13,4) in Z2 x Z3 x Z3; his machinery (multiplier orbits,
  intersection numbers) was run on cyclic groups. The database he
  maintains, at the same commit you froze (still HEAD today), lists
  all seven (32,20,4) cells and the three noncyclic (36,29,4) cells
  as Open; the cyclic (36,29,4) "No" you import is his orbit exhaust.
- He, Chen and Ge (read in full): constructions cover (v, v-1, -1)
  families, (243,242,161), a 3-group family (3^{2m+1}, 3^{2m}+1, 1),
  and fourth-order cyclotomic parameters; nothing at order 32 or 36
  with your parameters.
- This repository (farev/Matematica, sessions of 2026-08-09): decided
  58 of the 68 cells; the ten you call novel are exactly the ten it
  left open, and its README recorded the (32,20,4) family as beyond
  that session's exhaust budget with a naive cost estimate of
  5.5 * 10^11 nodes per group. Your census agrees with all 58 decided
  cells, zero conflicts, which we can now confirm from our side as
  well.
- Web and literature searches (2024 to 2026, several phrasings,
  including the ternary-sequence and perfect-ternary-array literature,
  which lives at lambda = 0 and does not touch these parameters):
  nothing.

So: to the best of two independent censuses and the two papers that
constitute the field's literature, your ten entries have no earlier
exact resolution, and your "novelty-supported, search is not proof"
framing is exactly the right epistemic level. One suggestion: Gordon
maintains the database you both froze; an upstream report of your ten
decisions (and, if you wish, jointly with this repository's audit of
the database's stored witnesses, 147 of 280 of which fail the defining
equation as exported) would put the novelty question in front of the
one person most likely to know of unpublished prior work.

## An observation you may want for a revision

The Corollary's imported datum can be proved in your own framework in
one line of computation: for (36,29,4) the C18 quotient system (kernel
C2, cells in [-2,2], peak 33, off-peak 8, sum 13) is empty. I verified
this by complete enumeration (it also falls out of the C9 x C2
hierarchy: the C9 system has 9 solutions, none extends). Emptiness at
C18 excludes every abelian group of order 36 with a C18 quotient, that
is, C36 and C2 x C18 at once. Combined with your Sections 6 and 7,
the full statement "no abelian group of order 36 admits a signed
(36,29,4) difference set" then rests entirely on your own certified
computations, with the database entry demoted to a concordance check.
You are welcome to this observation with or without attribution; the
regenerating code is in this repository under
`conjectures/signed-difference-sets/masselot-review/`.

## Reproducibility of this review

From `conjectures/signed-difference-sets/` at farev/Matematica:

    python3 masselot-review/verify_witnesses.py     # 16/16 VALID, ~2 s
    python3 masselot-review/validate_pipeline.py    # 4 controls, ~10 s
    python3 masselot-review/check_targets.py        # all legs, ~55 s

Outputs land in `masselot-review/out/` (witness verdicts, control
results, the per-leg report with every count above, and the run log).
The pinned copies of your sixteen witness files, with hashes, are in
`masselot-review/witnesses/` under your CC BY 4.0.
