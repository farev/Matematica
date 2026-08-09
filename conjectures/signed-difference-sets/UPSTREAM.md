# Draft upstream report to D. M. Gordon (not yet sent)

*Prepared 2026-08-09 by the research session; to be sent from a machine
with email/GitHub access (his README requests reports to
dmgordo@gmail.com). Everything below is checkable from the files in this
directory against the snapshot `data/sds.json`, sha256
`39bab9fce78d5c4353c22ba482ff5c3bb8b8b9931edc5ca0fc60062dfe80ca85`,
fetched from `dmgordo/signed-difference-sets` on 2026-08-09.*

Dear Dr. Gordon,

Three findings about the signed-difference-set repository, in decreasing
order of urgency.

**1. 147 of the 280 stored witness sets do not satisfy the SDS
equation.** Running your `is_sds` definition (reimplemented
independently; our checker agrees with yours on the other 133 sets,
including all Paley, Paley-and-zero, quartic-residue and He–Chen–Ge
sets) against every `sets` entry in `sds.json` shows 147 invalid sets
concentrated in 21 cells, all cyclic:
SDS(20,11,2), SDS(35,21,10), SDS(51,19,3), SDS(61,49,36), SDS(78,53,28),
SDS(104,29,4), SDS(111,66,17), SDS(167,84,40), SDS(181,136,11),
SDS(182,38,2), SDS(182,101,20), SDS(191,96,46), SDS(199,100,48),
SDS(200,151,102), SDS(247,127,63), SDS(277,208,17), SDS(347,174,85),
SDS(379,190,93), SDS(443,222,109), SDS(491,246,121), SDS(499,250,123).
Per-set verdicts: `data/witness_audit.csv`. These are not
differently-encoded equivalent sets: translation, Aut(G), inversion and
global sign change all preserve the off-peak correlation multiset, and
the failing sets have non-constant profiles.

The corruption looks like an export-stage sign scramble, not a search
error: for SDS(20,11,2) in Z₂₀ we re-enumerated completely — exactly 40
labeled sets, 2 translation classes — and your stored set 0 is a true
set with 9 and 11 exchanged between P and N (stored
P=[0,4,6,7,8,11,12,13,15], N=[1,9]; true
P=[0,4,6,7,8,9,12,13,15], N=[1,11]). The "All"/"Yes" statuses of the
affected cells may therefore all be correct; the listed sets need
regeneration. (Also, one intact entry — SDS(18,13,4,[3,6]) — stores its
set in Z₃×Z₃×Z₂ coordinates without a `G_rep` field.)

**2. 45,328 of the 67,823 Open cells follow from two classical
nonexistence tests.** For any nontrivial character χ, |χ(A)|² = k−λ.
Hence (i) if |G| is even, k−λ must be a perfect square (order-2
character — e.g. SDS(18,15,2,[3,6]), currently Open, has k−λ = 13 and
is impossible); (ii) Turyn's self-conjugacy test: if m | exp(G), m > 2,
p ∤ m, p^j ≡ −1 (mod m) and v_p(k−λ) is odd, the cell is impossible.
Applying both to the snapshot closes 23,997 Open cells by (i) and
21,331 more by (ii) — the full list with per-cell parameters is
`data/theory_closures.csv`. (The tests never contradict any Yes/All
cell, and retro-cover 984 of the 2,574 No cells.) Very possibly these
tests are in your paper — we could not reach the PDF from this
environment — but the database does not appear to apply them.

**3. New decisions of small Open cells by validated exhaustive
search.** Final list in `data/values.csv` with certificates in
`certs/` (engine validated by reproducing all 42 decided cells at
v ≤ 24 and by exact witness-list agreement with an independent
implementation). At first freeze: SDS(9,8,1,[3,3]),
SDS(18,15,2,[3,6]), SDS(20,17,8,[2,10]), SDS(20,11,2,[2,10]),
SDS(24,18,2,[2,12]), SDS(24,18,2,[2,2,6]) — all nonexistent.

Code (MIT) and data are at [repository URL]; we would be glad to help
fold any of this into the database.
