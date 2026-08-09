#!/usr/bin/env python3
"""Attempt to repair the 147 invalid stored witness sets by small
P<->M swap perturbations (the mechanism identified on SDS(20,11,2,[20])).

For each invalid stored set: try all single swaps (p,m) -> exchange
signs; if none fixes it and the cell is small enough, try all double
swaps. A repaired set is re-verified with the independent checker and
written to data/repaired_witnesses.csv.
"""

import csv
from itertools import combinations

import sdslib


def correlations_ok(A, v, lam, add, neg):
    for d in range(1, v):
        nd = neg[d]
        c = 0
        for g in range(v):
            if A[g]:
                c += A[g] * A[add[g][nd]]
        if c != lam:
            return False
    return True


def main():
    db = sdslib.load_db()
    out = []
    for name, entry in sorted(db.items()):
        sets = entry.get("sets") or []
        if not sets:
            continue
        v, k, lam, G = sdslib.parse_name(name)
        Guse = sdslib.cell_group(entry, G)
        order = 1
        for n in Guse:
            order *= n
        if order != v:
            continue
        add = sdslib.index_add_table(Guse)
        neg = sdslib.neg_index(Guse)
        for i, (P, M) in enumerate(sets):
            ok, msg0 = sdslib.check_sds(v, k, lam, Guse, P, M)
            if not ok and "does not match group" in msg0:
                # undeclared-coordinate entry; valid under a refinement
                for Galt in sdslib.refinements(Guse):
                    if sdslib.check_sds(v, k, lam, Galt, P, M)[0]:
                        ok = True
                        break
            if ok:
                continue
            Pi = [sdslib.elt_to_index(g, Guse) for g in P]
            Mi = [sdslib.elt_to_index(g, Guse) for g in M]
            A0 = [0] * v
            for g in Pi:
                A0[g] = 1
            for g in Mi:
                A0[g] = -1
            found = None
            # single swaps
            for p in Pi:
                for m in Mi:
                    A0[p], A0[m] = -1, 1
                    if correlations_ok(A0, v, lam, add, neg):
                        found = ("1swap", [(p, m)])
                    A0[p], A0[m] = 1, -1
                    if found:
                        break
                if found:
                    break
            # double swaps on small cells
            if not found and len(Pi) * len(Mi) <= 700:
                for (p1, p2) in combinations(Pi, 2):
                    for (m1, m2) in combinations(Mi, 2):
                        A0[p1] = A0[p2] = -1
                        A0[m1] = A0[m2] = 1
                        if correlations_ok(A0, v, lam, add, neg):
                            found = ("2swap", [(p1, m1), (p2, m2)])
                        A0[p1] = A0[p2] = 1
                        A0[m1] = A0[m2] = -1
                        if found:
                            break
                    if found:
                        break
            if found:
                kind, swaps = found
                Pr = set(Pi)
                Mr = set(Mi)
                for (p, m) in swaps:
                    Pr.discard(p); Mr.discard(m)
                    Pr.add(m); Mr.add(p)
                okr, msg = sdslib.check_sds(
                    v, k, lam, Guse,
                    [list(x) if len(Guse) > 1 else x for x in
                     ([coords(g, Guse) for g in sorted(Pr)])],
                    [list(x) if len(Guse) > 1 else x for x in
                     ([coords(g, Guse) for g in sorted(Mr)])])
                out.append([name, i, kind, str(swaps), okr,
                            sorted(Pr), sorted(Mr)])
                print(f"{name} set {i}: REPAIRED by {kind} {swaps} "
                      f"(re-verified: {okr}{'' if okr else ' — ' + msg})")
            else:
                out.append([name, i, "unrepaired", "", False, "", ""])
    nrep = sum(1 for r in out if r[2] != "unrepaired")
    print(f"\n{nrep} of {len(out)} invalid sets repaired by <=2 swaps")
    with open("data/repaired_witnesses.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "set_index", "repair", "swaps",
                    "reverified", "P_indices", "M_indices"])
        w.writerows(out)


def coords(idx, G):
    c = []
    for n in reversed(G):
        c.append(idx % n)
        idx //= n
    return tuple(reversed(c)) if len(G) > 1 else c[0]


if __name__ == "__main__":
    main()
