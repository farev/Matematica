# PAGE.md — handoff for fabianarevalo.com/graham-105 (new page)

## 1. Headline claim

**CERTIFIED** — The complete list of n with C(2n,n) coprime to 105 —
Graham's $1000 problem — now reaches 3^600 ≈ 1.9·10^286 (585,823,270
terms), 216 orders of magnitude past the previous complete census
(10^70, 1374 terms, Thompson 2015), and the new counts reveal that the
sequence grows in rare bursts separated by certified deserts of up to 27
decimal orders of magnitude.

## 2. Contributions

1. **CERTIFIED.** Complete census of OEIS A030979 below 3^600:
   585,823,270 terms (was: 1374 below 10^70). Five implementations across
   two algorithm families agree node-for-node on every overlapping range;
   the 3^600 rung reconciles 73,906,945,791 tree nodes across a composite
   of 3753 + 4906 exhaustive tasks. Whole ladder: ≈ 12.5 core-hours.
2. **CERTIFIED.** The largest known term of A030979 is now a 286-digit
   number (was 66 digits): `data/max600.txt`.
3. **CERTIFIED.** n = 3160 is the last n < 3^600 with C(2n,n) coprime to
   1155 = 3·5·7·11 — Graham predicted it is the last ever; the strongest
   published verification we could source was the 10^70 census.
   **NUMERICAL companion:** under the independence heuristic the expected
   number of further 1155-terms was 0.81 (72% of it below n = 60,000);
   observing none has probability ≈ 0.44 — the prediction stands on
   structure, and the census converts it to certainty below 3^600.
4. **CERTIFIED.** First counts of G(N) = #terms ≤ N beyond 10^70, at
   every power of 3 up to the 600th (`data/counts600.txt`), with the
   burst structure (`data/structure600.txt`): only 82 of 601 base-3
   lengths inhabited; [3^474, 3^530) entirely term-free (26.7 decimal
   orders); then 39,030,864 terms at length 531 alone; 82.6% of all
   terms have length ≥ 564. **NUMERICAL:** global fit
   G(N) ≈ 48.2·N^0.0248 over 3^100..3^600 versus the predicted
   N^0.02595; local 50-level band exponents swing 0.0144–0.0408.
5. **CERTIFIED (replication).** Thompson's 1374-term census re-derived
   from scratch (0.7 s in the Python reference — the published frontier
   of a $1000 Erdős–Graham problem fits in under a second once the
   right tree is searched), and the bottom range below 3.66·10^19
   independently re-verified by an algorithmically unrelated engine.

## 3. Figure specs

- **Figure A — the staircase.** Data: `data/counts600.txt` (columns k,
  G(3^k), log10(3^k)). Plot log10 G against log10 N for k = 20..600,
  with the heuristic slope 0.02595 as a reference line through the
  10^70 anchor. The reader should be able to say: *"The count climbs
  along the predicted power law for 280 orders of magnitude — but as a
  staircase of cliffs and plateaus, not a smooth curve."*
- **Figure B — bursts and deserts.** Data: `data/structure600.txt` (top
  spikes; empty runs) and the per-length histogram reconstructible from
  `data/counts600.txt` first differences. Horizontal bar/stem chart of
  terms-per-base-3-length for k = 400..600, deserts visible as long
  empty stretches, spikes labelled (531, 564, 567, 589, 600). Reader
  sentence: *"Between 3^474 and 3^530 — a span of twenty-seven orders of
  magnitude — there is not a single new term; then thirty-nine million
  arrive at once."*
- No figure for the 1155 companion (one sentence suffices; a figure
  would dress up a null result).

## 4. Caveats the page must carry

- Every literature claim is **(secondary)** — the sandbox could not read
  oeis.org, arxiv.org, erdosproblems.com, or Pomerance's papers. In
  particular: Thompson's "complete up to 10^70 / 1374 terms / Nov 2015"
  (five consistent snippets + our exact count match), Alekseyev's 3^41
  (single snippet), the erdosproblems #376 status text, and the
  Pomerance/EGRS attributions must be re-checked against primary
  sources before this page ships; adjust wording if any fails.
- An unconfirmed "searched to 10^104" claim for the 1155 companion
  surfaced once (AI-generated summary over blocked PDFs); the page must
  not present 10^70 as certainly the best prior 1155 bound — say
  "strongest bound we could source", as the note does.
- The burst/desert phenomenon: we could not source any prior observation
  (the counts did not exist), but the *mechanism* sketch is heuristic
  and adjacent to Pomerance's §4 discussion — check his AMM 2015 and
  Integers 2026 papers before claiming novelty for anything beyond the
  certified counts themselves.
- The infinitude question is untouched and untouchable by computation;
  the page must say so plainly (erdosproblems marks it "cannot be
  resolved with a finite computation").
- Enumeration method (top-down digit DFS with interval pruning) is
  folklore-adjacent; novelty is claimed for the range, the counts, the
  1155 height, and the public cross-verified form — not the technique.
- Full term lists are committed only to 3^250 (the 3^600 list is
  ~150 GB); larger rungs ship heads/samples/extremes/histograms/
  fingerprints, and every rung is reproducible by one command.

## 5. Existing page

None — this is a new conjecture directory and a new page.
