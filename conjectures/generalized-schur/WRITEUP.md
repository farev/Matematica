# Session writeup — 2026-08-07

The narrative, including what failed. Companion to `NOTE.md` (results) and
the [daily log](../../log/2026-08-07-generalized-schur.md) (selection).

## How the problem was chosen

This candidate is a resurrection. On 2026-08-05 the session scoped "compute
new generalized Schur numbers with the freshly built DRUP toolkit" as its E2
and killed it for exactly one reason: the deciding table — *which* 26 values
Ahmed–Schaal published in 2016 — sat in PDFs the sandbox proxy blocks, and
computing values without knowing the published boundary fails hard rule 3.
Today's scout found the boundary in the one place the proxy allows:
**Tanbir Ahmed hosts his own author preprint on GitHub Pages**, and
`raw.githubusercontent.com` is reachable. The paper was downloaded and read
in-session — the first primary source any session here has had since
2026-08-01 — and the entire publication boundary became checkable facts:
Table 1 transcribed to `data/published_values.csv`, conventions pinned from
the theorem proofs, enumeration counts from Theorems 2.1–2.10 banked as
controls.

Three other resurrection attempts died the usual death: graph-Ramsey tight
cases (the 2024–26 SAT wave has an active author publishing a settled case
every few months, and the one quiet pocket needs a blocked survey), BHR
per-multiset verification (the deciding caveat about a July 2025 paper is in
a blocked PDF; also a ~10 GB certificate against a 10 MB repo), and
no-three-in-line (the frontier moved twice in the last six months, both times
by specialists with more compute). The σ(n+1)=kσ(n) census (fresh May 2026
arXiv conjecture with a four-element evidence base) was the honest fallback
and was not needed.

## What happened, in order

1. **Pipeline before selection.** The generalized-Schur encoder
   (`schur3.py`), independent witness verifier, and climb driver were built
   and validated against convention-independent classics (`S(2;3,3)=5`,
   `S(3;3,3,3)=14`) *before* the publication boundary arrived — scoped prep,
   not commitment. A corrupted witness was fed to the verifier and rejected
   (negative control). The clause enumerator was cross-validated against
   brute force on 15 cells.

2. **Scaling probes on published values** doubled as boundary controls:
   `(4,4,4)=43` in 0.12 s with a verified proof; `(4,4,5)`, `(4,5,5)`,
   `(5,5,5)`, `(4,4,7)`, `(4,5,6)`, `(4,6,6)`, `(4,5,7)`, `(5,5,6)` all
   confirmed in seconds each. `(6,6,6)=173` did not finish inside 5 minutes —
   the first sight of the wall.

3. **The first new values fell during scoping.** `(4,4,8)` and `(4,4,9)` are
   not in the published table; the same probe batch that confirmed controls
   delivered `S(3;4,4,8)=87` (43 s) and `S(3;4,4,9)=98` (203 s), each with a
   RUP-verified DRUP proof at `S` and an independently verified witness at
   `S−1` — the first new values in this family since 2016, both confirming
   open instances of Conjecture 2.1.

4. **The s=3 exploration reproduced all twelve published `(3,t,u)` values**
   by Cadical climb from Song–Mao's proved lower bound (every anchor SAT, as
   their theorem requires), then the certified production lanes began walking
   into unmapped territory.

5. **Extremal enumeration.** An exactly-one encoding plus model enumeration
   reproduced every extremal-coloring count in the paper's ten enumeration
   theorems — 18, 54, 162, 846, 8, 1, 112, 96, 3584, 9488 — and the unique
   `(3,4,5)` extremal coloring **matches the paper's printed string
   character for character**. The maximal-`|C₂|` extremals for `(3,3,u)` are
   palindromes: `0110` Schur-caps, satellite structure, central `L(u)`-free
   band; max `|C₂| = 5(u−2)` exactly, for `u = 4,5,6,7`.

6. *(production results filled at session end)*

## What failed

- **Two out-of-memory crashes killed every running lane.** First: four
  concurrent solver lanes plus a `(6,6,6)`-at-`n=173` encoding (~3×10⁷
  clauses held as Python lists — several GB) exhausted 15 GB and the OOM
  killer swept all four lanes ~25 minutes in. Diagnosed, relaunched three
  lanes without the `(6,6,6)` job — and the box then *hard-restarted* on the
  second overrun (14/15 GB), losing the container state (repo files, certs,
  and the scratchpad all survived; only processes died). The final
  discipline that held: **at most two solver processes, heavies strictly
  sequential**, memory checked before launch. The `(6,6,6)=173` control
  reproduction was abandoned as not worth its footprint — it is published,
  Boza-covered, and my `(5,5,6)=113` and `(3,6,7)=107` controls already
  bracket the sizes that matter. Cost: roughly 40 minutes of lost solver
  time and two relaunches; no artifact was corrupted (append-only logs,
  atomic per-run writes).
- **Background lanes silently ran from the wrong directory** after the
  container restart reset the shell cwd — both relaunched lanes died in
  under a second on a missing `data/` path before the third relaunch pinned
  absolute paths. Caught by checking the task outputs immediately rather
  than trusting the launch.
- **`/usr/bin/time` does not exist in this sandbox**; the first wall-mapping
  batch lost its timings to that and was rerun with date-stamp arithmetic.
- **`S(3;4,4,10)` = the wall, and it is a memory wall, not a time wall.**
  Three proof-logged attempts (each 25+ minutes) were OOM-killed — pysat
  buffers the entire DRUP proof in RAM alongside the CNF, and this
  instance's proof outgrows a 15 GB box. The `(4,4,u)` ladder is anomalously
  hard for its size: `(4,4,9)` at n=98 needs ~108 s where mixed triples 15
  integers bigger — `(4,6,6)` at 101, `(5,5,6)` at 113 — certify in 14 s.
  Two short equations plus one long one give the solver the least
  propagation per decision. Fix for a future session: a standalone solver
  binary streaming the proof to disk (kissat/cadical + drat-trim), not an
  in-memory pysat run. `(4,4,10)`, `(4,4,11)`, `(4,4,12)` stay open today.
- **A correct `(3,3,8)` extremal enumeration appeared in `certs/` with no
  logged invocation** (no lane, no interactive command, no task transcript
  mentions it; created mid-flight between two container restarts). It was
  kept only after regenerating the enumeration and confirming the file is
  byte-identical to the fresh run. Recorded as a provenance defect: every
  other artifact in `certs/` traces to a logged command.
- *(mathematical dead ends filled at session end)*

## Lessons

- A publication boundary that is unreachable one week can be reachable the
  next through a side door (author self-hosting); re-checking a killed
  candidate's *kill reason* is cheap and occasionally decisive.
- Model-count agreement is a brutally strong encoder validation — ten exact
  matches plus one character-exact unique extremal leave essentially no room
  for a wrong constraint set.
- Python-side CNF construction is the memory hog at these sizes, not the
  solver; the clause count grows like the number of partitions into `t−1`
  parts, and three such encodings coresident is already 10+ GB at `n ≈ 170`.
