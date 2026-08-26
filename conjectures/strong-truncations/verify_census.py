#!/usr/bin/env python3
"""Independent verifier for strong6 census output.

Shares no graph/conflict code with strong6.c: rebuilds each graph from the
raw input line echoed in the R record, then checks every claim from the
definitions:

  * the witness uses colors {0..5} and has one color per edge,
  * every color class is an induced matching (no two same-colored edges
    share a vertex or are joined by an edge)  ==>  chi'_s <= 6,
  * the conflict graph contains a 6-clique (a triangle's three edges plus
    its three emanating edges, located by search)  ==>  chi'_s >= 6,
  * for truncation mode: the built graph is connected cubic simple,
    claw-free and diamond-free (definition-level family membership).

NOT6/CAP records are collected and reported, never silently accepted.

Usage: verify_census.py results.txt [...]   (or - for stdin)
Exit 0 iff every record verifies and there were no parse errors.
"""
import sys
from itertools import combinations


def build_truncation(raw):
    toks = raw.split()
    nv, ne = int(toks[0]), int(toks[1])
    vals = [int(x) for x in toks[2:]]
    assert len(vals) == 3 * ne, "bad -T line"
    slots = [0] * nv
    edges = []  # canonical order: triangles first, then links in instance order
    for u in range(nv):
        edges += [(3 * u, 3 * u + 1), (3 * u, 3 * u + 2), (3 * u + 1, 3 * u + 2)]
    for t in range(ne):
        a, b, mult = vals[3 * t], vals[3 * t + 1], vals[3 * t + 2]
        assert 0 <= a < nv and 0 <= b < nv and a != b and mult >= 1
        for _ in range(mult):
            sa, sb = slots[a], slots[b]
            assert sa < 3 and sb < 3, "H not subcubic"
            slots[a] += 1
            slots[b] += 1
            edges.append((3 * a + sa, 3 * b + sb))
    assert all(s == 3 for s in slots), "H not cubic"
    return 3 * nv, edges


def build_graph6(raw):
    s = raw.strip()
    n = ord(s[0]) - 63
    assert 1 <= n <= 62
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        assert 0 <= v < 64
        bits += [(v >> b) & 1 for b in range(5, -1, -1)]
    need = n * (n - 1) // 2
    assert len(bits) >= need
    edges = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                edges.append((i, j))
            k += 1
    return n, edges


def neighbors(n, edges):
    nb = [set() for _ in range(n)]
    for a, b in edges:
        assert a != b and b not in nb[a], "loop or multi-edge in built graph"
        nb[a].add(b)
        nb[b].add(a)
    return nb


def connected(n, nb):
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for w in nb[u]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


def check_family(n, nb):
    """cubic, claw-free, diamond-free — straight from the definitions."""
    for u in range(n):
        assert len(nb[u]) == 3, "not cubic"
        a, b, c = sorted(nb[u])
        inner = (b in nb[a]) + (c in nb[a]) + (c in nb[b])
        assert inner >= 1, "claw at %d" % u
        # a diamond K4-e contains a vertex with two edges among its
        # neighbours but not three (deg-3 => whole K4 present instead)
        assert inner != 2, "diamond at %d" % u


def check_witness(n, edges, nb, colors):
    assert len(colors) == len(edges)
    assert all(0 <= c <= 5 for c in colors)
    for cls in range(6):
        members = [e for e, c in zip(edges, colors) if c == cls]
        ends = []
        for a, b in members:
            ends += [a, b]
        endset = set(ends)
        assert len(ends) == len(endset), "class %d shares a vertex" % cls
        for a, b in members:
            assert nb[a] & endset == {b}, "class %d not induced" % cls
            assert nb[b] & endset == {a}, "class %d not induced" % cls


def conflict(e, f, nb):
    a, b = e
    c, d = f
    return (a in f or b in f or c in nb[a] or d in nb[a]
            or c in nb[b] or d in nb[b])


def has_conflict_6clique(edges, nb):
    """find 6 pairwise conflicting edges: try each triangle + its links."""
    idx = {}
    for e in edges:
        idx.setdefault(e[0], []).append(e)
        idx.setdefault(e[1], []).append(e)
    eset = set(edges)
    for (x, y) in edges:
        for z in nb[x] & nb[y]:
            tri = [(min(x, y), max(x, y)), (min(x, z), max(x, z)),
                   (min(y, z), max(y, z))]
            if any(t not in eset for t in tri):
                continue
            out = [e for v in (x, y, z) for e in idx[v] if e not in tri]
            six = tri + out
            if len(six) != 6:
                continue
            if all(conflict(e, f, nb) for e, f in combinations(six, 2)):
                return True
    return False


def main():
    files = sys.argv[1:] or ["-"]
    n_ok = n_not6 = n_cap = 0
    bad = 0
    not6_lines = []
    for fn in files:
        fh = sys.stdin if fn == "-" else open(fn)
        for line in fh:
            if not line.startswith("R "):
                continue
            head, _, raw = line.partition(" | ")
            toks = head.split()
            lineno, nT, m, verdict = toks[1], int(toks[2]), int(toks[3]), toks[4]
            raw = raw.strip()
            try:
                if raw[0].isdigit():
                    n, edges = build_truncation(raw)
                    family = True
                else:
                    n, edges = build_graph6(raw)
                    family = False
                assert n == nT and len(edges) == m, "size mismatch"
                nb = neighbors(n, edges)
                assert connected(n, nb), "not connected"
                if family:
                    check_family(n, nb)
                if verdict == "6":
                    colors = [int(x) for x in toks[6:6 + m]]
                    check_witness(n, edges, nb, colors)
                    assert has_conflict_6clique(edges, nb), "no 6-clique found"
                    n_ok += 1
                elif verdict.startswith("NOT"):
                    n_not6 += 1
                    not6_lines.append(line.rstrip())
                elif verdict == "CAP":
                    n_cap += 1
                    not6_lines.append(line.rstrip())
                else:
                    raise AssertionError("unknown verdict %r" % verdict)
            except AssertionError as exc:
                bad += 1
                print("FAIL line %s: %s" % (lineno, exc))
        if fh is not sys.stdin:
            fh.close()
    print("verified: %d witnesses OK (chi_s = 6 certified both sides), "
          "%d NOT6, %d CAP, %d FAILED" % (n_ok, n_not6, n_cap, bad))
    for line in not6_lines:
        print("ATTENTION:", line)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
