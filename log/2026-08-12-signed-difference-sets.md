# 2026-08-12 — signed-difference-sets

**Target.** Nicolas Masselot emailed asking for a bounded review of his
`certified-small-sds-census` v1.0 (released this morning), which closes
all 68 Open cells of order ≤ 36 in the same frozen Gordon snapshot this
repo censused on 08-09, including the ten cells we left open: the
(32,20,4) family at order 32 (our README's stated next target, priced
at 48 core-hours per group) and (36,29,4) in the three noncyclic
order-36 groups. Review scope he asked for: theorem framing,
completeness of the quotient reductions, earlier exact resolutions.

**Result.** CERTIFIED, three pieces. (1) His census cross-checked cell
by cell against ours: his 68 targets are exactly the snapshot's Open
cells at v ≤ 36, 58/58 verdict agreement with our census, his 10 novel
cells exactly our 10 undecided; all 16 witnesses pass `sdslib`
(hashes match his note). (2) All four nonexistence legs re-derived by
complete searches with review-owned code and no symmetry reduction,
after 4/4 known-answer controls (incl. exact 40-set equality on
(20,11,2)): C32 chain 0 of 2,985,984 refinements; [2,18] and [3,12]
quotient systems empty; [6,6] 0 of 16,964,640 marginal-consistent
vectors, making his SAT/DRAT leg non-load-bearing; every §5–§7 count
of his note (9,528/56/12/248,832/144/420/106,353/9) reproduced
exactly. Total ~52 s. (3) New: the C18 quotient system of (36,29,4)
is empty, so C36 and C2×C18 die at once and his Corollary's imported
database exhaust can be discharged (NOTE §5.1). Also resolved the
session-1 rediscovery caveat: Gordon and He–Chen–Ge read in full,
neither states the T1/T2 transfers; no earlier exact resolution of
any of his ten entries found anywhere (two censuses + both papers +
searches). Review delivered as `masselot-review/REVIEW.md` + reply
draft; PAGE.md written (page update: open question 1 is settled).

**What failed.** First control design assumed the (20,11,2) complete
enumeration held both global signs; the engine normalizes sign, so the
right expectation was 40, not 20 (fixed by demanding exact set
equality with the certificate). An open-ended two-layer EXIST control
on (36,11,2,[6,6]) was hopeless in Python (weak marginals, huge fiber
space); replaced by a witness-branch walk, which is the sharper
control anyway. Nothing else: his claims survived everything thrown at
them, which is itself the finding.

**Next.** Send the reply (draft ready; Fabian to send). Coordinate the
upstream report to Gordon jointly with Masselot: our witness audit
(147/280 invalid exports) plus his order ≤ 36 closure. Method thread:
his quotient ladder does in seconds what our flat DFS priced at
core-hours; port layered refinement into `sds_search.c` and aim it at
the smallest still-Open cells at order > 36.
