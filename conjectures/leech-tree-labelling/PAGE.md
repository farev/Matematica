# PAGE.md — handoff for the site page `fabianarevalo.com/leech-tree-labelling`

New page (no page exists for this conjecture yet). Row in the top-level README
added today.

## 1. Headline claim

**CERTIFIED.** Leech's tree-labelling number a(11) = 49: some tree on 11
vertices with positive integer edge weights has path sums covering every
integer 1..49, and no such tree covers 1..50. OEIS A007187 has carried only
"a(11) ≥ 48" since Leech's 1975 note; this is the first term past n = 10.

## 2. Contributions

1. **a(11) = 49 (CERTIFIED).** Lower bound: the tree with weighted edges
   (0,1,1) (2,3,1) (0,4,2) (5,6,4) (3,6,5) (5,7,7) (6,8,8) (5,9,11) (2,10,22)
   (0,3,24), whose 55 path sums are 1..49 with 1, 11, 23, 25, 26, 39 repeated
   (verified by an independent checker; three more witnesses found by the
   other workers). Upper bound: exhaustive search, 1 400 728 816 nodes over
   four worker prefixes, under five minutes wall on four cores, verdict "no
   tree" for k = 50; the ladder k = 55, 54, 53, 52, 51 refuted on the way
   (2.4 M, 26.5 M, 27.9 M, 121 M, 493 M nodes).
2. **a(12) ≥ 57 (CERTIFIED witness; OEIS had ≥ 55)** and
   a(12) ≤ 61 (CERTIFIED refutation of k = 62, 4 863 094 430 nodes, 78 min
   on one worker) [PENDING: k = 61]. Hunts at 58 and 59 found nothing.
3. **Method (PROVED lemmas).** Edges exposed in nondecreasing weight; the next
   weight is at most the least uncovered value (Lemma 1); the number of
   "wasted" pairs (repeats or values > k) is monotone and bounded by
   C(n,2) − k (Lemma 2); Taylor's parity count in budgeted form (Lemma 3);
   an edge-load bound (Lemma 4); Ghodsi's whole-block exact-cover condition
   for Leech trees, budgeted (Lemma 5); isomorphic components interchangeable
   (Lemma 6). All in NOTE §2 with proofs.
4. **Positive control.** The same program re-derives a(2..10) =
   1, 3, 6, 9, 15, 20, 26, 34, 41 from scratch (witnesses checked, refutations
   with recorded node counts), and an independent SAT engine (one CNF per
   tree shape) agrees at n = 7, 8 and on 17 of the 47 shapes at n = 9; a
   deliberately minimal second search engine reproduces every value of both
   variants it was run on (repeats allowed: n ≤ 10; distinct: n ≤ 12).
5. **A second sequence (CERTIFIED).** Forbidding repeated path sums (the
   maximum "Leech index" of Varghese–Lakshmanan–Arumugam over all trees of
   order n) gives 1, 3, 6, 9, 15, 20, 25, 30, 37, 45, 47 for n = 2..12, not in
   OEIS; it agrees with a(n) up to n = 7 and falls behind from n = 8 on.
6. **Excess sequence.** C(n,2) − a(n) for n = 2..11 is 0,0,0,1,0,1,2,2,4,6:
   the 11-vertex optimum wastes six of its 55 pairs, where a Leech tree
   (impossible at order 11 by Taylor's parity theorem) would waste none.

## 3. Figures

- **Figure 1 — the witness tree.** Data: `witnesses/n11_k49.txt` (edges
  (u,v,w)). Draw the tree with edge weights as labels; below it a number line
  1..49 with a tick for each path sum, doubled ticks at 1, 11, 23, 25, 26, 39.
  Sentence: "Ten weighted edges on eleven vertices produce all forty-nine
  sums, with six sums appearing twice."
- **Figure 2 — the ladder.** Data: NOTE §3 table (n, a(n), C(n,2)) and §4.
  Plot a(n) against C(n,2) for n = 2..12 (a(12) as an interval), with the
  gap C(n,2) − a(n) annotated. Sentence: "The best tree falls further behind
  the perfect count as n grows: 0, 0, 0, 1, 0, 1, 2, 2, 4, 6 pairs wasted,
  and at least 5 at n = 12."
- **Figure 3 — cost of the refutations.** Data: NOTE §4 table (k, budget,
  nodes). Log-scale bars of node count against excess budget at n = 11.
  Sentence: "Every extra wasted pair the search must allow multiplies the
  work by about four."

## 4. Caveats the page must carry

- The n = 11 and n = 12 refutations are single-engine exhaustive searches
  (one C program; two variants of it agree to the node, and a SAT engine
  replicates it only for n ≤ 9). Say "exhaustive search" with the node
  counts, not "proof", and name the single-engine caveat.
- Leech 1975 and Guy §C10 were not read (paywalled); their content is cited
  through OEIS A007187 and Ghodsi 2026 (secondary). The OEIS bound
  "a(11) ≥ 48" is unattributed there.
- Taylor 1977, Székely–Wang–Zhang 2005, Calhoun et al. 2007 are cited
  through Ghodsi 2026 (secondary).
- The witness trees are not claimed unique; four inequivalent-looking
  witnesses at k = 49 were found and not classified.
- n = 12 is open: 57 ≤ a(12) ≤ 61 [PENDING]; the hunts at 58 and 59 are
  not evidence of nonexistence.

## 5. Existing page

None.
