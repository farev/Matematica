# Draft reply on the v1.1 revision (send from fabiareor@gmail.com)

Subject: Re: bounded review of the small-SDS census

Nicolas,

The attribution and the AI-boundary description are both accurate as
written. Keep them as they are. Section 7 says exactly what my review
did and did not do, the acknowledgment has my name right, and the
pinned commit resolves to the final version of the review. No changes
needed from my side. Two optional tweaks if you are editing anyway:
reference [4] could link the tree at the pinned commit instead of
/tree/main (the hash already pins it, so this is cosmetic), and you
could name the assistant (Claude) in the boundary sentence for
symmetry with your Codex disclosure. Both are your call.

I also checked the revision the same way I checked v1.0. Results:

1. The six constructions printed in Appendix A match the v1.0 witness
   files exactly, all P and N sets, all six groups. So the printed
   vectors are faithful to the artifacts.
2. Your C18 numbers reconcile, with one wording nit. I get 23,184
   parity-matching refinements in total; your 19,152 is exactly the
   count with squared norm at most 33, so your enumerator evidently
   prunes above the norm target on the way (sound, and the norm
   histogram confirms it: 19,152 at norm <= 33, of which 7,560 at
   exactly 33, then 0 solutions, matching my run). A reader who
   regenerates "marginal-compatible refinements" without the norm cap
   will get 23,184 and stumble. Suggested one-line fix: "There are
   19,152 marginal-compatible refinements with squared norm at most
   33, of which 7,560 attain exactly 33."
3. Your C6xC6 rerun numbers match mine (36 pairs, 16,964,640, zero),
   and the identity-correlation argument you added (13^2 - 35*4 = 29,
   so no separate support filter is needed) is correct. That was the
   one unstated subtlety in my filter, so I am glad it is now in
   print.

The revision reads well. Theorem 2 as a single self-contained
statement is much cleaner, and I think retaining the DRAT trace as a
supplementary check is the right call.

Good to see Gordon has looked at the novelty and framing; that answers
the strongest open part of my question (iii) better than any search
could. Since you are in contact with him: my audit of the stored
witness exports (147 of 280 fail the defining equation as stored, 22
repairable by small swaps) is still unreported. If it is useful I can
send it to him directly, or fold a summary into whatever you send next.
Whichever is less noise for him.

My check scripts for the revision are committed in the same directory
as the review (check_v11_revision.py, output in out/), so you can cite
or rerun them if you want the v1.1 numbers externally confirmed too.

Fabian
