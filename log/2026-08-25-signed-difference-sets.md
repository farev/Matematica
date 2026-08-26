# 2026-08-25 — signed-difference-sets

**Target.** Masselot answered the review with a rewritten v1.1 paper
(dated 2026-08-21; a computer failure delayed his reply) that
incorporates both review reductions, and asked one question before the
public release: is the attribution and the description of the review's
AI-assistance boundary acceptable? Check the paper's references to
this repo, and verify the revision's new numbers the same way v1.0 was
verified.

**Result.** CERTIFIED (small). Attribution checked and accurate: named
in the introduction (both simplifications), §5 (the unreduced C32
rerun with exact counts), §7 (a dedicated trust-boundary section that
states precisely what the review did and did not audit, and describes
the AI boundary in words matching the review's own disclosure),
acknowledgments ("Fabian Arévalo", spelled right), and reference [4]
pinned to commit 05f18c4, which is on origin/main and carries the
final review text. Revision verified: the six constructions printed in
Appendix A match the pinned witness JSONs set for set
(`check_v11_revision.py`); the C6×C6 rerun reproduces 36 pairs /
16,964,640 / 0; his added identity-correlation argument
(13² − 35·4 = 29) is correct. One wording nit found and explained: his
"19,152 marginal-compatible refinements" is the norm ≤ 33 slice of the
full 23,184 (his enumerator prunes above the norm target; my norm
histogram gives 19,152 at ≤ 33, 7,560 at exactly 33, 0 solutions, all
matching). Theorem 2 is now a single self-contained statement with the
DRAT trace demoted to a supplementary check. Also learned from the
acknowledgments: Gordon has checked the novelty and framing and
encouraged journal submission, which answers review question (iii) at
the strongest available level. Reply drafted
(`masselot-review/REPLY_V11_DRAFT.md`): keep attribution as is, two
optional tweaks, the 19,152 wording fix, and an offer to route the
witness-corruption audit to Gordon directly or through his channel.

**What failed.** First parse of the Appendix A coordinate lists broke
on two-digit coordinates like (0,10) (single-digit regex); fixed, then
all six sets matched. First reading of 19,152 looked like an error
until the norm histogram identified it as the norm-capped count.

**Next.** Fabian sends REPLY_V11_DRAFT. After his v1.1 goes public,
consider the arXiv question for our side (the C18 lemma and the
verification suite are now cited components of a journal-bound paper).
The method thread stands: port layered quotient refinement into
`sds_search.c` for the ~22k still-Open cells at order > 36.
