"""Re-verify Masselot's 16 census witnesses with this repository's
independent checker (sdslib.check_sds, which shares no code with either
Gordon's is_sds or Masselot's two validators).

Input: masselot-review/witnesses/*.json, pinned copies of
artifacts/witnesses/ from NicolasMasselot/certified-small-sds-census
at tag v1.0 (fetched 2026-08-12; CC BY 4.4 -- see PROVENANCE.md).

Only `group_invariant_factors` and `coefficient_vector` are read from
each file (his validator outputs are deliberately ignored). Coefficient
order per his note: lexicographic direct-product coordinates, last
coordinate varying fastest -- the same mixed-radix convention as
sdslib. Each vector is decoded to (P, M) coordinate sets and passed to
check_sds, which recomputes every one of the v-1 autocorrelations in
exact integer arithmetic.

Run from conjectures/signed-difference-sets/:
    python3 masselot-review/verify_witnesses.py
Writes masselot-review/out/witness_verification.csv and exits nonzero
on any failure.
"""

import csv
import glob
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sdslib import check_sds  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

FNAME_RE = re.compile(r"sds_(\d+)_(\d+)_(\d+)_(.+)\.json$")


def params_from_filename(path):
    m = FNAME_RE.search(os.path.basename(path))
    v, k, lam, tail = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
    return v, k, lam, tail


def decode(vec, G):
    """index -> coordinate tuple, last coordinate fastest (mixed radix)."""
    P, M = [], []
    for i, a in enumerate(vec):
        if a == 0:
            continue
        x, c = i, []
        for n in reversed(G):
            c.append(x % n)
            x //= n
        g = tuple(reversed(c)) if len(G) > 1 else c[0]
        (P if a == 1 else M).append(g)
    return P, M


def main():
    rows = []
    ok_all = True
    for path in sorted(glob.glob(os.path.join(HERE, "witnesses", "*.json"))):
        v, k, lam, _ = params_from_filename(path)
        with open(path) as f:
            w = json.load(f)
        # one file (sds_25_12_1_c5xc5.json) stores the group as "C_5 x C_5"
        # under "group" instead of an invariant-factor list
        graw = w.get("group_invariant_factors") or w["group"]
        if isinstance(graw, str):
            G = [int(x) for x in re.findall(r"\d+", graw)]
        else:
            G = list(graw)
        vec = list(w["coefficient_vector"])
        sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
        problems = []
        if len(vec) != v:
            problems.append(f"vector length {len(vec)} != v={v}")
        if any(a not in (-1, 0, 1) for a in vec):
            problems.append("coefficient outside {-1,0,1}")
        if problems:
            ok, msg = False, "; ".join(problems)
        else:
            P, M = decode(vec, G)
            ok, msg = check_sds(v, k, lam, G, P, M)
        npos = sum(1 for a in vec if a == 1)
        nneg = sum(1 for a in vec if a == -1)
        rows.append(
            {
                "file": os.path.basename(path),
                "cell": f"SDS({v},{k},{lam},{G})".replace(" ", ""),
                "n_pos": npos,
                "n_neg": nneg,
                "verdict": "VALID" if ok else "INVALID",
                "detail": msg,
                "sha256": sha,
            }
        )
        ok_all &= ok
        print(f"{'VALID  ' if ok else 'INVALID'}  SDS({v},{k},{lam},{G})  |P|={npos} |M|={nneg}  {msg if not ok else ''}")
    out = os.path.join(HERE, "out", "witness_verification.csv")
    with open(out, "w", newline="") as f:
        wcsv = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wcsv.writeheader()
        wcsv.writerows(rows)
    print(f"\n{sum(r['verdict'] == 'VALID' for r in rows)}/{len(rows)} valid -> {out}")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
