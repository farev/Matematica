#!/usr/bin/env python3
"""Record a certificate file in certs/MANIFEST.csv (append-only).

Columns: file, kind, s, t, n, bytes, sha256, verdict, solver, note
The manifest is the committed record for proofs too large for git; committed
small proofs are also listed so every certificate has exactly one row.
"""
import csv
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(HERE, "certs", "MANIFEST.csv")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def record(path, kind, s, t, n, verdict, solver, note=""):
    new = not os.path.exists(MAN)
    with open(MAN, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["file", "kind", "s", "t", "n", "bytes", "sha256",
                        "verdict", "solver", "note"])
        w.writerow([os.path.basename(path), kind, s, t, n,
                    os.path.getsize(path), sha256(path), verdict, solver, note])


if __name__ == "__main__":
    # manifest.py <path> <kind> <s> <t> <n> <verdict> <solver> [note]
    record(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
           sys.argv[6], sys.argv[7], sys.argv[8] if len(sys.argv) > 8 else "")
    print("recorded", sys.argv[1])
