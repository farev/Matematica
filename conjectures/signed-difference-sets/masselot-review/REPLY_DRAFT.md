# Draft reply to Nicolas Masselot (send from fabiareor@gmail.com)

Subject: Re: bounded review of the small-SDS census

Nicolas,

Happy to do the review. Your ten novel entries are exactly the ten
cells my census left open on 08-09. My README even called the
(32,20,4) family the natural next target and priced it at about 48
core-hours per group. So I had both the motivation and the data to
check this properly.

Short version: both theorems hold up. I re-derived every nonexistence
claim with my own code and got the same answers everywhere.

What I did:

1. All 16 of your witnesses pass my independent checker (written
   08-09 against Gordon's convention, no code shared with your two
   validators). The six order-32 files hash exactly to the table in
   your Section 4.
2. I rebuilt your quotient systems from the definition and ran every
   reduction as a complete search, with no symmetry arguments at all.
   C32: all 56 C8 solutions refined through C16, 2,985,984 final
   refinements, zero solutions. C2xC18 and C3xC12: the quotient
   systems are empty over every marginal pair. C6xC6: a direct search
   over all 36 marginal pairs, 16,964,640 candidates, zero pass the
   35 correlation equations, about 44 seconds. So your DRAT
   certificate now has a solver-free second proof standing next to
   it.
3. Every count in your Sections 5 to 7 reproduces exactly: 9,528, 56,
   the orbit sizes 8/16/8/16/8, the 12 C16 survivors, 248,832, 144,
   420, 106,353, and the nine C3^2 solutions. Your marginal patterns
   ((1,6,6), (4,9), (7,2,2,2), (-3,2,...,2)) are the only ones, which
   I checked by enumerating those systems completely.
4. Your three questions. Framing: sound, small suggestions below.
   Completeness of the quotient reductions: yes. I checked the
   lifting arguments, then reran everything without them.
   Earlier resolutions: none that I know of, and I looked from a
   good spot: two independent censuses of the same 68 cells, plus
   Gordon's paper and He-Chen-Ge read in full this week. Gordon's
   table has no order-32 or 36 rows, and his only noncyclic set is
   (18,13,4). He-Chen-Ge's families miss these parameters. Your
   "novelty-supported, search is not proof" framing is right. I can
   also confirm the other direction: your 58 replicated entries
   agree with my census cell for cell, zero conflicts.

One thing you may want for a revision. Your Corollary imports the
cyclic C36 case from the frozen repository. You can prove it inside
your own framework in one line: the C18 quotient system for (36,29,4)
(cells in [-2,2], sum 13, norm 33, every nonzero shift 8) is empty.
That kills C36 and C2xC18 at once, so "no abelian group of order 36
admits a signed (36,29,4) difference set" becomes fully
self-contained. I think that is worth having. My 08-09 audit found
147 of the 280 stored witness sets in that database fail the defining
equation as exported (the statuses look fine, the corruption is in
the witness export, but fewer dependencies is better). Take it with
or without attribution.

Small things, none blocking: the sum and sum-of-squares parts of your
Section 3 lemma are Gordon's Lemma 5.2, worth citing; a sentence near
Theorem 1 noting the two kinds of evidence would help, since theorems
get quoted alone; sds_25_12_1_c5xc5.json uses a different schema than
the other fifteen witness files; and your email said "La Jolla
covering repository", which is a different database. The note has the
right name.

The full review, pinned copies of your witnesses, and the
verification code (three scripts, about a minute to rerun) are here:

https://github.com/farev/Matematica/tree/main/conjectures/signed-difference-sets/masselot-review

One suggestion beyond the review. Gordon maintains the database we
both froze, and I had an upstream report queued about the witness
corruption. Your census closes the whole order <= 36 shelf. Want to
send him one joint report (dmgordo@gmail.com per his README)? One
email with your ten decisions plus my audit and repairs is more
useful to him than two.

Disclosure, since we clearly work the same way: this review was done
with substantial AI assistance (Claude), under the same boundary you
use. Nothing model-generated was treated as evidence. Every claim
above is backed by the committed code and its outputs.

Fabian
