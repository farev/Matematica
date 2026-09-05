#!/usr/bin/env python3
"""cubes.py -- enumerate, up to relabeling of the points, all ways to place the lines of size
>= 4 prescribed by a line-type distribution on n points as a partial linear space (two lines
share at most one point).  Each placement is a cube for ordlines_sat.py (--big ...).

Canonical form: a placement is described completely by the multiset of point incidence
vectors (which big lines each point lies on), so two placements are isomorphic iff some
permutation of the lines maps one multiset onto the other.  We take the minimum over line
permutations of the sorted tuple of incidence rows.
"""
import sys, itertools
from distributions import distributions


def canon(n, lines):
    L = len(lines)
    best = None
    for perm in itertools.permutations(range(L)):
        rows = []
        for p in range(n):
            rows.append(tuple(1 if p in lines[perm[q]] else 0 for q in range(L)))
        rows.sort()
        key = tuple(rows)
        if best is None or key < best:
            best = key
    return best


def placements(n, sizes):
    """all non-isomorphic partial linear spaces on n points with big lines of the given sizes
    (sizes: list, e.g. [5,4,4]).  Returned as lists of sorted point tuples."""
    sizes = sorted(sizes, reverse=True)
    results = {}

    def rec(idx, lines, used_max):
        if idx == len(sizes):
            key = canon(n, lines)
            if key not in results:
                results[key] = [tuple(sorted(L)) for L in lines]
            return
        k = sizes[idx]
        # to limit redundancy: new line's points chosen from 0..used_max+k (fresh points get
        # consecutive labels); canonicalization removes the remaining duplicates
        hi = min(n, used_max + k)
        for pts in itertools.combinations(range(hi), k):
            S = set(pts)
            if any(len(S & set(L)) > 1 for L in lines):
                continue
            new_max = max(used_max, max(pts) + 1)
            rec(idx + 1, lines + [S], new_max)

    rec(0, [], 0)
    return list(results.values())


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    total = 0
    for d in distributions(n, m):
        sizes = []
        for k, t in d.items():
            if k >= 4:
                sizes += [k] * t
        pl = placements(n, sizes) if sizes else [[]]
        total += len(pl)
        print(f"distribution t_3={d[3]} big={sizes}: {len(pl)} cube(s)")
        for lines in pl:
            print("   ", ' '.join('--big ' + ','.join(map(str, L)) for L in lines) if lines else "   (no big lines)")
    print("total cubes:", total)
