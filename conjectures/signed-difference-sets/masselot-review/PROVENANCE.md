# Provenance of the reviewed materials

All external materials were fetched 2026-08-12 (Europe/Madrid) from the
v1.0 tag of `github.com/NicolasMasselot/certified-small-sds-census`,
following a review request emailed by Nicolas Masselot the same day.

| item | source | note |
|---|---|---|
| `witnesses/*.json` (16 files) | `artifacts/witnesses/` at tag v1.0 | pinned copies; CC BY 4.0 per the project's licensing statement. SHA-256 of the six order-32 files match the table in his note §4 exactly. |
| note (markdown) | `paper/two_small_order_classifications.md` at v1.0 | the reviewed text; a rendered PDF exists in his `output/pdf/`. |
| census | `artifacts/census/current_census.json` at v1.0 | 68 entries; sha256 `11cd6bed…` matches the note §2. |
| release v1.0 | GitHub release, published 2026-08-12 09:50 UTC | Zenodo DOI 10.5281/zenodo.21901581 resolves; archive sha256 `d982b6b5…` matches the release notes (metadata check only; the 242 MB archive was not downloaded). |

Upstream cross-checks performed the same day:

- `dmgordo/signed-difference-sets` HEAD is `e3bf810c5ee6826cf5030f983f6adf23b0ffd20e`
  (2026-04-24), exactly his frozen commit; identical to the snapshot
  pinned in this directory's `data/sds.json` (fetched 2026-08-09,
  sha256 `39bab9fc…ca85`).
- Gordon, arXiv:2212.10630 (published version Des. Codes Cryptogr. 91
  (2023) 2107–2115) and He–Chen–Ge, arXiv:2306.05631 (Des. Codes
  Cryptogr. 92 (2024)) were downloaded and read in full for the
  prior-work assessment (they had been secondary-only in session 1).

No code from the reviewed repository was executed here. All
verification in this directory uses code written for this review
(`qrlib.py`, `validate_pipeline.py`, `check_targets.py`,
`verify_witnesses.py`) plus this conjecture directory's independent
checker `sdslib.py`.
