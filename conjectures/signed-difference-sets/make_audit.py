#!/usr/bin/env python3
"""Write data/witness_audit.csv: per stored witness, does it satisfy the
defining equation? (The audit artifact behind NOTE §6.)"""

import csv

import sdslib


def main():
    db = sdslib.load_db()
    rows = []
    for name, entry in sorted(db.items()):
        sets = entry.get("sets") or []
        v, k, lam, G = sdslib.parse_name(name)
        Guse = sdslib.cell_group(entry, G)
        for i, (P, M) in enumerate(sets):
            ok, msg = sdslib.check_sds(v, k, lam, Guse, P, M)
            note = ""
            if not ok and "does not match group" in msg:
                for Galt in sdslib.refinements(Guse):
                    ok2, _ = sdslib.check_sds(v, k, lam, Galt, P, M)
                    if ok2:
                        ok, note = True, f"verifies under undeclared coordinates {Galt}"
                        break
            rows.append([name, entry.get("status"), entry.get("comment", ""),
                         i, "VALID" if ok else "INVALID",
                         note if ok else msg])
    bad = [r for r in rows if r[4] == "INVALID"]
    badcells = sorted(set(r[0] for r in bad))
    with open("data/witness_audit.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "status", "comment", "set_index", "verdict", "detail"])
        w.writerows(rows)
    print(f"{len(rows)} stored sets audited: {len(rows)-len(bad)} valid, "
          f"{len(bad)} invalid across {len(badcells)} cells")
    print("affected cells:", ", ".join(badcells))


if __name__ == "__main__":
    main()
