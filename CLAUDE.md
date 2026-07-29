# Matematica — working instructions

A research log. Every day, one session against an open conjecture. Most
sessions fail; the failures get written down too.

Use the `conjecture-research` skill for any session that attempts, extends, or
audits open mathematics here.

## The claim discipline

Every result carries exactly one label. Never blur them.

- **PROVED** — theorem with a written proof, valid for all cases in scope.
- **CERTIFIED** — exact computation (rational/integer arithmetic, no float in
  the critical path), reproducible, ships a verifiable certificate. True only
  for the range actually computed.
- **NUMERICAL** — Monte Carlo, fits, heuristics, floating point. Evidence only.

Hard rules:

1. A computation is never a proof. Write "verified for n ≤ N", never "proved".
2. A fit is never a law. Write "R² = 0.98 on i ∈ [64, 1023]", never "the c_i
   satisfy". State the range fitted and the range tested.
3. If a result might be known already, say so prominently and go look. An
   honest rediscovery is a fine outcome; an unmarked one is misconduct.
4. Downgrade freely. If a certificate breaks, the label changes that day, and
   the old claim is struck through rather than deleted.
5. Never assert what a cited paper says without checking the actual paper.
   Citations get verified before they go in a note.

Claim inflation is the characteristic failure mode of AI-assisted daily
research. These rules exist specifically to counter it.

## Layout

```
conjectures/<name>/   self-contained: README, NOTE, WRITEUP, code, data, certs
log/YYYY-MM-DD-<conjecture>.md
tools/                utilities shared across conjectures
```

Each conjecture directory must stand alone — it should survive
`git subtree split` into its own repo without edits. Shared code goes in
`tools/`, never imported sideways between conjecture directories.

New conjecture: copy `conjectures/TEMPLATE.md` into
`conjectures/<name>/README.md` and fill it in.

## Where writing goes

The top-level `README.md` is an **index, not a summary**. It carries the status
vocabulary, the layout, and one table row per conjecture — statement, status,
session count, and a single-line strongest result linking to the conjecture
directory. Nothing conjecture-specific beyond that line, ever. It has to stay
one screen when there are thirty conjectures in it.

All detail — the statement, the labelled results table, script tables, data
files, reproduction commands, defects, prior work — lives in
`conjectures/<name>/README.md`. When a session produces a result, update the
conjecture README fully and touch the top-level table only if the strongest
result changed.

Each conjecture also gets a public write-up page on the site, indexed at
<https://fabianarevalo.com/math> and served at `fabianarevalo.com/<name>` —
note the flat path, not `/math/<name>`. Link it from the index row in the
top-level README and from the conjecture README header. The `research-page`
skill builds these. The repository is the code and certificates; the page is
the readable version, plain-language explanation first.

## Per-conjecture documents

- `README.md` — one screen. Statement, current status, table of scripts and
  what each produces, reproduction commands, known defects.
- `NOTE.md` — the paper-shaped artifact: abstract, numbered theorems, proofs,
  numerical methodology, open questions. This is what becomes a preprint.
- `WRITEUP.md` — the session narrative, including what failed and why. Never
  edited to look smarter in hindsight.

## Reproducibility

- Every number that appears in a note has a script that emits it.
- Record runtime, core count, RAM and seed for anything expensive.
- Exact computations ship their certificate as a committed file.
- Commit small CSVs and certificates — they are results. Anything above ~10 MB
  goes to Zenodo and gets referenced from the conjecture README.

## Running code

Scripts reference data files by bare relative name, so they must be run from
inside their own conjecture directory:

```bash
cd conjectures/gilbreath && python3 verify.py 1e6
```

The Gilbreath scripts import each other as flat sibling modules
(`from verify import primes_up_to`). Do not reorganise them into `src/` and
`scripts/` subdirectories without updating every import and every bare filename
in an `open()` or `np.loadtxt()` call — the certified results depend on those
paths resolving.

Known defect: `ck_analysis.py` reads `c6_exact.txt`, which does not exist; the
certified value lives in `c6_certified.txt`. Fix before relying on that script.

## Daily log

One entry per session, `log/YYYY-MM-DD-<conjecture>.md`:

```markdown
# YYYY-MM-DD — <conjecture>

**Target.** What I went after and why it looked tractable.
**Result.** Labelled PROVED / CERTIFIED / NUMERICAL / nothing.
**What failed.** The approaches that did not work, and the reason.
**Next.** The sharpest open thread.
```

"Nothing" is a valid result and gets logged like any other.

## Publishing

Preprints go to arXiv (`math.NT`, cross-list `math.PR` where relevant), LaTeX
with `amsart`, MSC 2020 codes, proofs in `amsthm` environments. First-time
submission to an archive needs an endorsement. New integer sequences go to
OEIS. Code and data snapshots get a Zenodo DOI so notes can cite an immutable
artifact.

AI assistance is disclosed in every note and preprint. AI systems are never
listed as authors.
