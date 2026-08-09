#!/usr/bin/env python3
"""Control battery: verify EVERY witness in Gordon's database with the
independent checker, then corrupted-witness negative controls.

Run from inside conjectures/signed-difference-sets/.
"""

import copy
import random
import sys
from collections import Counter

import sdslib


def main():
    db = sdslib.load_db()
    statuses = Counter(e.get("status") for e in db.values())
    print(f"entries: {len(db)}  statuses: {dict(statuses)}")

    tested = passed = 0
    failures = []
    with_sets = 0
    for name, entry in sorted(db.items()):
        sets = entry.get("sets") or []
        if not sets:
            continue
        with_sets += 1
        v, k, lam, G = sdslib.parse_name(name)
        Guse = sdslib.cell_group(entry, G)
        for i, (P, M) in enumerate(sets):
            tested += 1
            ok, msg = sdslib.check_sds(v, k, lam, Guse, P, M)
            if not ok and "does not match group" in msg:
                # data quirk: witness stored in an undeclared isomorphic
                # coordinate system (seen once: SDS(18,13,4,[3,6]) in
                # Z3xZ3xZ2 coordinates); try prime-power refinements
                for Galt in sdslib.refinements(Guse):
                    ok2, msg2 = sdslib.check_sds(v, k, lam, Galt, P, M)
                    if ok2:
                        ok, msg = True, f"ok under refinement {Galt}"
                        print(f"  note: {name} set {i} verifies under "
                              f"undeclared coordinates {Galt}")
                        break
            if ok:
                passed += 1
            else:
                failures.append((name, i, msg))
    print(f"witness control: {passed}/{tested} verified "
          f"({with_sets} entries with sets)")
    for f in failures[:20]:
        print("  FAIL:", f)

    # negative controls: corrupt witnesses, checker must reject
    rng = random.Random(20260809)
    names = [n for n, e in db.items() if e.get("sets")]
    rejected = 0
    trials = 0
    for name in rng.sample(names, 8):
        entry = db[name]
        v, k, lam, G = sdslib.parse_name(name)
        Guse = sdslib.cell_group(entry, G)
        P, M = copy.deepcopy(entry["sets"][0])
        if P and M:
            # swap a plus to a minus (breaks correlations or s)
            M.append(P.pop())
        elif P:
            M.append(P.pop())
        else:
            P.append(M.pop())
        trials += 1
        ok, _ = sdslib.check_sds(v, k, lam, Guse, P, M)
        if not ok:
            rejected += 1
    print(f"negative control (sign-flip corruption): {rejected}/{trials} rejected")

    if failures or rejected != trials:
        print("CONTROL BATTERY FAILED")
        sys.exit(1)
    print("CONTROL BATTERY OK")


if __name__ == "__main__":
    main()
