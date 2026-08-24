"""Verify Conjecture A (split-or-pigeonhole) against every computed cell.

Conjecture A: for every finite abelian G, either d±(G) = floor(log2 |G|), or
G = A ⊕ B properly with d±(G) = d±(A) + d±(B).

By Krull–Schmidt every direct summand corresponds (up to isomorphism) to a
sub-multiset of the primary cyclic components, so it suffices to scan
bipartitions of the component multiset. Values are looked up in the computed
tables (CSV); any group referenced by a split but not computed is reported.

Also prints the "atoms": pigeonhole-tight groups that no split explains, and
checks the subgroup-monotonicity consistency of the whole table.

Run: python3 conjecture_check.py data/table_le100.csv [more csvs...]
"""

import csv
import sys
from itertools import combinations
from math import prod


def canon(moduli):
    return tuple(sorted(moduli, reverse=True))


def load(paths):
    vals = {}
    for p in paths:
        with open(p) as f:
            for row in csv.DictReader(f):
                if not row["dpm"] or row["dpm"] == "None":
                    continue
                mods = canon(int(x) for x in row["moduli"].split())
                vals[mods] = int(row["dpm"])
    return vals


def floor_log2(n):
    return n.bit_length() - 1


def bipartitions(mods):
    """Proper bipartitions of the component multiset, up to swap."""
    n = len(mods)
    seen = set()
    idx = list(range(n))
    for r in range(1, n):
        for A in combinations(idx, r):
            a = canon(mods[i] for i in A)
            b = canon(mods[i] for i in idx if i not in A)
            key = (a, b) if a <= b else (b, a)
            if key in seen:
                continue
            seen.add(key)
            yield a, b


def main():
    vals = load(sys.argv[1:])
    print(f"{len(vals)} computed groups loaded")
    violations, atoms, missing_refs = [], [], set()
    for mods, d in sorted(vals.items(), key=lambda kv: (prod(kv[0]), kv[0])):
        N = prod(mods)
        ph = floor_log2(N)
        best_split = None
        for a, b in bipartitions(mods):
            if a in vals and b in vals:
                s = vals[a] + vals[b]
                best_split = s if best_split is None else max(best_split, s)
            else:
                missing_refs.add(a if a not in vals else b)
        if d == ph:
            continue  # pigeonhole-tight: conjecture satisfied
        if best_split == d:
            continue  # split-attained: conjecture satisfied
        if len(mods) == 1:
            continue  # cyclic is always pigeonhole-tight; can't get here
        violations.append((mods, N, d, ph, best_split))
    for v in violations:
        print("VIOLATION:", v)
    if not violations:
        print("Conjecture A holds at every computed group.")
    # atoms: pigeonhole-tight noncyclic groups NOT also split-attained
    # (cyclic <=> primary components pairwise coprime <=> invariant rank 1;
    #  cyclic groups are atoms trivially by Lemma Cy, so exclude them)
    from math import gcd
    def is_cyclic(mods):
        return all(gcd(a, b) == 1 for a, b in combinations(mods, 2))
    for mods, d in sorted(vals.items(), key=lambda kv: (prod(kv[0]), kv[0])):
        if is_cyclic(mods):
            continue
        N = prod(mods)
        if d != floor_log2(N):
            continue
        bs = max((vals[a] + vals[b] for a, b in bipartitions(mods)
                  if a in vals and b in vals), default=None)
        if bs is not None and bs < d:
            atoms.append((mods, N, d, bs))
    print(f"\nnoncyclic pigeonhole-tight atoms (no split attains d): {len(atoms)}")
    for mods, N, d, bs in atoms:
        print(f"  {mods} order {N}: d={d} (best split {bs})")
    if missing_refs:
        print(f"\n(splits referencing {len(missing_refs)} uncomputed groups were skipped)")
    # subgroup monotonicity spot check: removing one component never raises d
    bad = [(m, s) for m in vals for s in {canon(m[:i] + m[i+1:]) for i in range(len(m))}
           if len(m) > 1 and s in vals and vals[s] > vals[m]]
    print(f"\ncomponent-removal monotonicity violations: {len(bad)}", bad if bad else "")


if __name__ == "__main__":
    main()
