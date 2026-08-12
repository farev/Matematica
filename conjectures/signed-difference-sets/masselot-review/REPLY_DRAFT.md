# Draft reply to Nicolas Masselot (send from fabiareor@gmail.com)

Subject: Re: bounded review of the small-SDS census

Nicolas,

Happy to do the review. Your ten novel entries are exactly the ten
cells my census left open on 08-09 (my README even priced the
(32,20,4) family at ~48 core-hours per group and called it the natural
next target), so I had both the motivation and the data to check this
properly. Short version: both theorems hold up, and I can say that
with more than a referee's confidence because I re-derived every
nonexistence leg with my own code and it all came back the same.

What I did, concretely:

1. All 16 of your witnesses pass my independent checker (written
   2026-08-09 against Gordon's convention, no code shared with either
   of your validators). The six order-32 witness files hash exactly to
   the table in your Section 4.
2. I rebuilt your quotient systems from the definition alone and ran
   every reduction as a complete search with no symmetry arguments at
   all: all 56 C8 solutions refined through C16 to C32 (2,985,984
   final refinements, zero solutions), the order-12 and order-18
   quotient systems for C2xC18 and C3xC12 over every marginal pair
   (zero solutions each), and for C6xC6 a direct search over all 36
   marginal pairs (16,964,640 marginal-consistent vectors, zero
   survive the 35 correlation equations, about 44 seconds). So your
   DRAT certificate now has a solver-free second proof next to it.
3. Every count in your Sections 5 to 7 reproduces exactly: 9,528, 56,
   the orbit sizes 8/16/8/16/8, the 12 C16 survivors, 248,832, 144,
   420, 106,353, and the nine C3^2 solutions. Your implicit uniqueness
   claims for the marginals ((1,6,6), (4,9), (7,2,2,2), (-3,2,...,2))
   are all true; I enumerated the systems completely.
4. On your three questions: the framing is sound (a few small
   suggestions below), the reductions are complete (I checked the
   lifting arguments and then made them unnecessary by rerunning
   unreduced), and I know of no earlier exact resolution of any of the
   ten entries. That last answer comes from a decent vantage point:
   two independent censuses of the same 68 cells, plus Gordon's paper
   and He-Chen-Ge read in full this week (Gordon's sporadic table has
   no order-32 or 36 rows and his only noncyclic set is (18,13,4);
   He-Chen-Ge's families don't touch these parameters). Your
   "novelty-supported, search is not proof" framing is exactly right.
   And I can confirm the other direction of your screen: your 58
   replicated entries agree with my census verdict for verdict, zero
   conflicts.

One observation you may want for a revision. Your Corollary imports
the cyclic C36 nonexistence from the frozen repository. You can prove
it inside your own framework in one line: the C18 quotient system for
(36,29,4) (cells in [-2,2], sum 13, norm 33, every nonzero shift 8) is
empty. That kills C36 and C2xC18 simultaneously, so "no abelian group
of order 36 admits a signed (36,29,4) difference set" becomes fully
self-contained, with the database entry demoted to a concordance
check. Worth having, I think, given that my 08-09 audit found 147 of
the 280 stored witness sets in that database fail the defining
equation as exported (statuses look fine, the corruption is in the
witness export, but fewer trust dependencies is better). Take the
observation with or without attribution.

Small things, none blocking: your Section 3 lemma's sum and
sum-of-squares moments are Gordon's Lemma 5.2 (intersection numbers),
worth citing; consider a sentence in or next to Theorem 1 noting the
two evidence types, since theorems get quoted without their
surroundings; the witness file sds_25_12_1_c5xc5.json uses a different
schema than the other fifteen (group string instead of
group_invariant_factors); and your email said "La Jolla covering
repository", which is a different database, the note's name is the
right one.

The full review, the pinned copies of your witnesses, and the
verification code (three scripts, about a minute total to rerun) are
in my repo:

https://github.com/farev/Matematica/tree/main/conjectures/signed-difference-sets/masselot-review

One suggestion beyond the review: Gordon maintains the database we
both froze, and I had an upstream report queued about the witness
corruption. Your census closes the whole order <= 36 shelf. Want to
coordinate a joint report to him (dmgordo@gmail.com per his README)?
One email covering your ten decisions plus my audit and repairs is
more useful to him than two.

Disclosure, since we clearly run the same way: this review was done
with substantial AI assistance (Claude), with the same boundary you
use. Nothing model-generated was treated as evidence; every claim
above is backed by the committed code and its outputs.

Fabián
