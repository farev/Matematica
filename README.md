# Matematica

Daily attempts at open problems in mathematics.

Every day I pick an unsolved conjecture — or an open thread in a recent paper —
and spend a session on it. Most days produce nothing but a record of what
failed. Occasionally a session produces something real: a new exact constant, a
sharpened inequality, an empirical law, or an audit of someone else's recent
work. Everything goes in this repository, successes and dead ends alike.

The failures are the point as much as the results. A research log that only
shows the wins is not a research log.

## Status vocabulary

Every claim in this repository carries exactly one of three labels. This is the
most important convention here, and it is not negotiable.

| Label | Meaning |
|---|---|
| **PROVED** | A theorem with a written proof. Holds for all cases in its stated scope. |
| **CERTIFIED** | An exact computation — rational or integer arithmetic, no floating point in the critical path — that is reproducible and ships a verifiable certificate. True for the range computed, not beyond. |
| **NUMERICAL** | Monte Carlo, curve fits, heuristics, floating-point exploration. Evidence, not proof. May be wrong. |

A computation is never described as a proof. "Verified for all n ≤ N" is a
CERTIFIED statement; it is not evidence that a conjecture is true, only that no
counterexample lives below that bound.

## Conjectures

Every conjecture has a write-up page at **[fabianarevalo.com/math](https://fabianarevalo.com/math)**
— the readable version, with the plain-language explanation first. This
repository is the code, data and certificates behind those pages.

One directory per conjecture, each with its own README carrying the full
statement, labelled results, scripts and reproduction commands.

| Conjecture | Status | Sessions | Strongest result so far |
|---|---|---|---|
| [**Gilbreath's conjecture**](conjectures/gilbreath/) · [page ↗](https://fabianarevalo.com/gilbreath) | active | 1 | **PROVED** — a factor-2 sharpening of the Chase–Hunter–Tao lower bound, plus **CERTIFIED** exact values of the first three uncomputed constants of their continuous model |

Daily entries, including the sessions that produced nothing, are in
[`log/`](log/).

## Layout

```
conjectures/<name>/   one directory per conjecture, self-contained
log/                  daily entries, YYYY-MM-DD-<conjecture>.md
tools/                utilities shared across conjectures
```

Each conjecture directory holds its own README, research note, writeup, code,
data and certificates. They are deliberately self-contained so any one of them
can be split out later with `git subtree split` if it grows into its own paper
or package.

## Running things

```bash
python3 -m pip install -e .
```

Requires Python 3.11+, NumPy and SciPy. Developed on Python 3.12.6 with
NumPy 2.3.5 and SciPy 1.17.0.

Scripts read and write data files by relative name, so **run them from inside
their own conjecture directory**:

```bash
cd conjectures/gilbreath && python3 verify.py 1e6
```

Each conjecture's README lists what every script does, what it produces, and
roughly what it costs to run — some finish in seconds, others want multiple
cores and several GB of RAM.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Corrections are especially welcome — if
something here is wrong, or rediscovers known work without saying so, please
open an issue.

## On AI assistance

These sessions are run with substantial AI assistance (Claude). This is
disclosed here, in each research note, and in any preprint that comes out of
this work. AI systems are not listed as authors, consistent with COPE guidance
and publisher policy. Every proof is checked by hand; every computational claim
ships code you can rerun.

## License

Code is [MIT](LICENSE-CODE). Prose, research notes and writeups are
[CC BY 4.0](LICENSE-PROSE) — compatible with the arXiv distribution license.
