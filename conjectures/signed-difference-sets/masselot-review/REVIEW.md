# Bounded review: "Two Small-Order Classification Theorems for Signed Difference Sets" (Masselot, v1.0, 2026-08-12)

Reviewer: Fabian Arévalo (farev/Matematica), with substantial AI
assistance (Claude). Every computational claim below comes from code
committed under `masselot-review/` and can be rerun with the commands
at the end. Review date: 2026-08-12. Scope, as requested: (i) theorem
framing, (ii) completeness of the quotient reductions, (iii) earlier
exact resolutions.

## Short version

Both theorems are correct. I re-derived every nonexistence claim with
my own code, written from the definition alone, and checked all
sixteen witnesses with a third validator that shares nothing with your
two. Every count in Sections 5 to 7 of your note came out exactly the
same. One extra result: the C18 quotient system of (36,29,4) is
empty. That proves the C36 and C2 x C18 cases in one step, so your
Corollary no longer needs the database entry it currently imports.
Details below.

## What I checked, and how

My code (`qrlib.py`, `check_targets.py`, `verify_witnesses.py`) was
written for this review, from the definition alone. The witness
checker is my repository's `sdslib.check_sds`, written 2026-08-09
against Gordon's convention. None of it shares code with your two
validators, with Gordon's `is_sds`, or with a SAT solver. All
arithmetic is exact (Python integers; NumPy int64 only for batch
filtering).

Before touching your claims I ran four known-answer controls. My chain
code reproduces, set for set, the 40 labeled SDS(20,11,2,[20]) from my
complete enumeration of 08-09. My two-layer code returns zero on
SDS(36,29,20,[6,6]), matching my direct exhaust, and it keeps, rather
than prunes, the branch of a known SDS(36,11,2,[6,6]) witness. The
chain also returns zero on SDS(32,28,12,[32]), again matching my
exhaust.

| your note says | I get | match |
|---|---|---|
| 16 valid witnesses, six of them the order-32 constructions | 16/16 pass `check_sds`; the six order-32 file hashes match the table in your §4 | yes |
| §5: 9,528 C8 vectors after sum and norm; 56 solutions; 5 affine orbits of sizes 8,16,8,16,8; 12 C16 survivors over orbit representatives; 248,832 final refinements; 0 solutions | same numbers; and with no orbit reduction at all: 144 C16 survivors over all 56 parents, 2,985,984 refinements, 0 solutions | yes |
| §6, C2 x C18: 144 candidates after canonical marginals and norm; 0 solutions | 144 on the canonical pair; full enumeration over every marginal pair, no normalization: 0 solutions | yes |
| §6, C3 x C12: 420 candidates; 0 solutions | 420; full unnormalized enumeration: 0 solutions | yes |
| §7: 106,353 C3^2 vectors after sum and norm; 9 projection solutions in one orbit; real side (7,2,2,2); one normalized instance; UNSAT by checked DRAT | 106,353; the 9 solutions are exactly the nine translates of (-3,2,...,2); the C2^2 system is exactly the four translates of (7,2,2,2); and a solver-free search over all 36 marginal pairs: 16,964,640 candidates, 0 pass the 35 correlation equations (43.7 s) | yes |
| census: the 68 Open entries of order <= 36 at the frozen commit; 58 replications of farev/Matematica; 10 novel | my own 2026-08-09 fetch of the same commit has exactly those 68 Open cells; cell-by-cell diff: 58 agreements, 0 disagreements; your 10 novel cells are exactly the 10 I left open | yes |

All of this runs in under a minute on a laptop. What I did not check:
your CNF/DRAT chain (on purpose: for C6 x C6 my direct search replaces
it rather than audits it), the contents of the Zenodo archive (I only
checked the record and its hashes), and where your witnesses came from
(which does not matter for whether they are valid).

## (i) Theorem framing

The framing is sound. Two things are better than what I usually see:
the acceptance boundary in Section 2 (raw UNSAT is not evidence;
witnesses must pass two validators with all normalizations forgotten),
and the Corollary openly marking the one datum it imports instead of
absorbing it silently.

Comments, none blocking:

1. Your definitions match Gordon's paper (his Lemma 1.1 is your
   equation (2); his |P| >= |N| convention is your sign
   normalization) and the database checker. Your equation (1) is the
   same identity my census uses, so all three projects are provably
   about the same object.
2. Theorem 1 rests on two kinds of evidence: explicit witnesses on
   one side, an exhaustive refinement on the other. Sections 4 and 5
   say this clearly, but the theorem will get quoted without them.
   One sentence in or next to the theorem statement would help.
3. The Corollary can become self-contained: see the observation
   below. Theorem 2 and the Corollary then merge into one clean
   statement: no abelian group of order 36 admits a signed (36,29,4)
   difference set.
4. Your Section 3 lemma has an ancestor worth citing: the sum and
   sum-of-squares parts of your equation (4) are Lemma 5.2 in
   Gordon's paper (intersection numbers; also standard in the design
   literature, e.g. Beth, Jungnickel and Lenz VI.5.4). Costs one
   line.
5. The evidence-type counts in Section 9 (16/13/4/9/14/12) match the
   machine-readable census exactly. I checked.
6. Two cosmetic nits. The file `sds_25_12_1_c5xc5.json` uses
   `group: "C_5 x C_5"` and `frozen_at_utc` where the other fifteen
   use `group_invariant_factors` (and one uses `frozen_date`); worth
   harmonizing before a journal submission. And your email called the
   source the "La Jolla covering repository", which is a different
   database; the note's name is the right one.
7. A remark for your discussion section, if you want it: at
   (32,20,4), existence splits exactly at cyclic versus noncyclic. In
   my census, (32,28,12) splits at containing Z4 x Z4 (it exists only
   in [4,8] and [2,4,4]). So no single subgroup rule explains order
   32.

## (ii) Completeness of the quotient reductions

I tested this three ways: I checked your arguments as written, I
re-proved the facts they depend on, and I reran every reduction with
the symmetry arguments removed, so completeness no longer depends on
them.

1. The projection lemma and its constants are right: kernel size m
   gives cells in [-m, m], peak k + (m-1)lambda, off-peak m lambda.
   My systems use exactly these and get your counts, so we agree on
   the actual constraint systems, not just the prose.
2. Section 5 (C32). Your completeness argument needs three things.
   (a) The C8 enumeration is complete: confirmed, 9,528 and then 56
   as complete counts from my own search. (b) The affine reduction
   is sound because the group actions lift: true. Translations lift
   along any surjection, and the unit maps
   (Z/32)^x -> (Z/16)^x -> (Z/8)^x are onto, so multiplying by a
   unit of Z8 extends to an automorphism of C32. (c) Every survivor
   gets refined explicitly: confirmed, and also made irrelevant,
   because my rerun refines all 56 C8 solutions with no orbit
   reduction anywhere (144 C16 survivors, 2,985,984 refinements,
   zero solutions). Your ledger records a symmetry bug you caught
   and removed (quotienting a normalized slice by the full
   translation group). That is exactly the kind of bug reviewers
   fear in these ladders. The released pipeline does not have it,
   and the unreduced rerun confirms its output.
3. Section 6. The normalization step needs two facts the note uses
   without stating: the marginal systems have exactly the claimed
   solutions, and the two translation normalizations do not
   interfere. Both are true. Complete enumeration gives exactly
   {(1,6,6) and its rotations} for C3, {(4,9),(9,4)} for C2, the
   four translates of (7,2,2,2) for C2^2, and the nine translates of
   (-3,2,...,2) for C3^2, with your 106,353 as the sum-and-norm
   count. Independence holds because the translation group splits by
   CRT into the two directions. My reruns then loop over every
   marginal pair instead of canonical ones, so the exclusions hold
   with no normalization argument at all. Your normalized counts
   (144 and 420) both reproduce.
4. Section 7 (C6 x C6). The reduction to one normalized instance is
   complete for the same two reasons, which I verified rather than
   assumed. Stronger: the SAT certificate no longer carries the
   result. A direct search over all 36 marginal pairs (16,964,640
   candidates, exact integer filtering through the 35 correlation
   equations) finds nothing. Your DRAT proof and my search are fully
   independent, and they agree.
5. On trust, to be explicit: I did not audit your CNF encoder or
   your drat-trim run, and my own searches have their own trust
   surface (my code), controlled by the known-answer checks above.
   The two pipelines share no code, which is what makes the
   agreement meaningful.

Verdict on (ii): the reductions are complete as claimed, and the
result survives with every symmetry argument stripped out.

## (iii) Earlier exact resolutions

I know of none, and I am in a good position to say so: my repository
censused the same 68 cells three days before you froze yours.

- Gordon's paper (read in full for this review): the sporadic table
  has no order-32 or order-36 rows, the only noncyclic SDS in it is
  (18,13,4) in Z2 x Z3 x Z3, and his searches ran on cyclic groups.
  His database, at the commit you froze (still HEAD today), lists all
  seven (32,20,4) cells and the three noncyclic (36,29,4) cells as
  Open. The cyclic (36,29,4) "No" you import is his orbit exhaust.
- He, Chen and Ge (read in full): their families are (v, v-1, -1),
  (243,242,161), a 3-group family (3^{2m+1}, 3^{2m}+1, 1), and
  fourth-order cyclotomic parameters. Nothing at order 32 or 36 with
  your parameters.
- My repository (farev/Matematica, sessions of 2026-08-09): decided
  58 of the 68 cells. The ten you call novel are exactly the ten I
  left open, and my README said so, with a cost estimate of
  5.5 * 10^11 nodes per group for (32,20,4). Your census agrees with
  all 58 of my decided cells, zero conflicts, now confirmed from my
  side as well.
- Web and literature searches (2024 to 2026, several phrasings,
  including the ternary-sequence and perfect-ternary-array
  literature, which lives at lambda = 0 and does not touch these
  parameters): nothing.

So, as far as two independent censuses and the field's two papers can
tell, your ten entries have no earlier exact resolution. Your
"novelty-supported, search is not proof" framing is the right level.
One suggestion: Gordon maintains the database we both froze. An
upstream report of your ten decisions (and, if you want, jointly with
my audit of the database's stored witnesses, 147 of 280 of which fail
the defining equation as exported) would put the novelty question in
front of the one person most likely to know of unpublished prior
work.

## An observation you may want for a revision

The datum your Corollary imports can be proved inside your own
framework in one line of computation: for (36,29,4), the C18 quotient
system (kernel C2, cells in [-2,2], sum 13, norm 33, every nonzero
shift 8) is empty. I verified this by complete enumeration (0.6 s; it
also drops out of the C9 x C2 hierarchy: the C9 system has 9
solutions and none extends). An empty C18 system rules out every
abelian group of order 36 with a C18 quotient, which means C36 and
C2 x C18 at once. Combined with your Sections 6 and 7, the statement
"no abelian group of order 36 admits a signed (36,29,4) difference
set" then rests entirely on your own certified computations, and the
database entry becomes a cross-check instead of a dependency. Take it
with or without attribution; the code is in my repository under
`conjectures/signed-difference-sets/masselot-review/`.

## Rerunning this review

From `conjectures/signed-difference-sets/` at farev/Matematica:

    python3 masselot-review/verify_witnesses.py     # 16/16 VALID, ~2 s
    python3 masselot-review/validate_pipeline.py    # 4 controls, ~10 s
    python3 masselot-review/check_targets.py        # all legs, ~55 s

Outputs land in `masselot-review/out/` (witness verdicts, control
results, the per-leg report with every count above, and the run log).
Pinned copies of your sixteen witness files, with hashes, are in
`masselot-review/witnesses/` under your CC BY 4.0.
