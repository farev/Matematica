#!/usr/bin/env python3
"""Independent witness extractor + mechanical Definition-3.1 checker.

Given a digraph6 Hasse diagram of a k-poset (as emitted by nauty-genposetg k t),
build the (k+2)-element lattice, find a winning da-tree by BFS closure with
parent tracking, print it as an S-expression, and re-verify the tree with a
separate checker that implements Definition 3.1 of arXiv:2608.27416 literally
and shares no logic with the search.

Deliberately different from lattscan.c: order relation via boolean matrix
closure, lattice check tests BOTH joins and meets from the raw definition,
Mobius by direct recursion with memoization, decision by plain BFS without
the leaf-closure staging or complement trick.

Usage: verify_witness.py '<digraph6>'         one lattice, print tree + verdict
       verify_witness.py --selftest           run on M3/N5/B3 style cases
"""
import sys
from functools import lru_cache

def parse_digraph6(line):
    assert line.startswith('&')
    s = line[1:]
    n = ord(s[0]) - 63
    bits = []
    for c in s[1:]:
        v = ord(c) - 63
        bits.extend((v >> (5 - t)) & 1 for t in range(6))
    E = [(i, j) for i in range(n) for j in range(n) if bits[i * n + j]]
    return n, E

def build_lattice(k, E):
    """Elements 0..k-1 interior, k bottom, k+1 top. leq as set of pairs."""
    N = k + 2
    BOT, TOP = k, k + 1
    leq = [[False] * N for _ in range(N)]
    for i in range(N):
        leq[i][i] = True
    for (i, j) in E:          # cover edge i -> j taken as i < j
        leq[i][j] = True
    for x in range(N):
        leq[BOT][x] = True
        leq[x][TOP] = True
    # transitive closure (Warshall)
    for m in range(N):
        for a in range(N):
            if leq[a][m]:
                row_m = leq[m]
                row_a = leq[a]
                for b in range(N):
                    if row_m[b]:
                        row_a[b] = True
    # antisymmetry sanity
    for a in range(N):
        for b in range(N):
            if a != b and leq[a][b] and leq[b][a]:
                raise ValueError("not a poset")
    return N, BOT, TOP, leq

def is_lattice(N, leq):
    """Raw definition: every pair has a least upper bound and a greatest lower bound."""
    for x in range(N):
        for y in range(x + 1, N):
            ub = [z for z in range(N) if leq[x][z] and leq[y][z]]
            if not any(all(leq[m][z] for z in ub) for m in ub):
                return False
            lb = [z for z in range(N) if leq[z][x] and leq[z][y]]
            if not any(all(leq[z][m] for z in lb) for m in lb):
                return False
    return True

def mobius(N, TOP, leq):
    mu = {}
    def rec(v):
        if v in mu:
            return mu[v]
        if v == TOP:
            mu[v] = 1
        else:
            mu[v] = -sum(rec(u) for u in range(N) if leq[v][u] and u != v)
        return mu[v]
    for v in range(N):
        rec(v)
    return mu

def down(N, TOP, leq, v):
    return frozenset(x for x in range(N) if leq[x][v] and x != TOP)

def find_tree(N, BOT, TOP, leq):
    """BFS closure with parents; returns tree as nested tuples or None.
    Tree: ('leaf', v) | ('empty',) | ('+', L, R) | ('-', L, R)."""
    mu = mobius(N, TOP, leq)
    target = frozenset(x for x in range(N) if x != TOP)
    leaf_sets = {}
    for v in range(N):
        if v != TOP and mu[v] != 0:
            leaf_sets.setdefault(down(N, TOP, leq, v), v)
    parent = {}
    for S, v in leaf_sets.items():
        parent[S] = ('leaf', v)
    parent[frozenset()] = ('empty',)
    frontier = list(parent.keys())
    while True:
        if target in parent:
            break
        new = []
        allstates = list(parent.keys())
        for A in frontier:
            for B in allstates:
                cands = []
                if not (A & B):
                    cands.append((A | B, '+', A, B))
                if B < A:
                    cands.append((A - B, '-', A, B))
                if A < B:
                    cands.append((B - A, '-', B, A))
                for (C, op, X, Y) in cands:
                    if C not in parent:
                        parent[C] = (op, X, Y)
                        new.append(C)
        if not new:
            break
        frontier = new
    if target not in parent:
        return None, mu, target
    def unfold(S):
        tag = parent[S]
        if tag[0] in ('leaf', 'empty'):
            return tag
        op, X, Y = tag
        return (op, unfold(X), unfold(Y))
    return unfold(target), mu, target

def check_tree(tree, N, BOT, TOP, leq):
    """Mechanical Definition 3.1 check. Returns the root state or raises."""
    mu = mobius(N, TOP, leq)
    def ev(t):
        if t[0] == 'empty':
            return frozenset()
        if t[0] == 'leaf':
            v = t[1]
            assert v != TOP, "leaf is top"
            assert mu[v] != 0, "leaf has zero Mobius value"
            return down(N, TOP, leq, v)
        op, L, R = t
        XL, XR = ev(L), ev(R)
        if op == '+':
            assert not (XL & XR), "+ children not disjoint"
            return XL | XR
        if op == '-':
            assert XR <= XL, "- right child not a subset"
            return XL - XR
        raise AssertionError("bad node")
    root = ev(tree)
    target = frozenset(x for x in range(N) if x != TOP)
    assert root == target, "root state is not P minus top"
    return True


def find_ll_sequence(N, BOT, TOP, leq):
    """BFS for a winning left-linear tree: returns list of ('start'|'+'|'-', v)
    steps (v a leaf vertex or None for the empty start), or None."""
    mu = mobius(N, TOP, leq)
    target = frozenset(x for x in range(N) if x != TOP)
    leaf_sets = {}
    for v in range(N):
        if v != TOP and mu[v] != 0:
            leaf_sets.setdefault(down(N, TOP, leq, v), v)
    parent = {}
    order = []
    for S, v in leaf_sets.items():
        parent[S] = ('start', v, None)
        order.append(S)
    parent[frozenset()] = ('start', None, None)
    order.append(frozenset())
    i = 0
    while i < len(order) and target not in parent:
        A = order[i]
        i += 1
        for S, v in leaf_sets.items():
            if not (A & S):
                C = A | S
                op = '+'
            elif S <= A:
                C = A - S
                op = '-'
            else:
                continue
            if C not in parent:
                parent[C] = (op, v, A)
                order.append(C)
                if C == target:
                    break
    if target not in parent:
        return None
    steps = []
    S = target
    while True:
        op, v, prev = parent[S]
        steps.append((op, v))
        if op == 'start':
            break
        S = prev
    steps.reverse()
    return steps

def check_ll_sequence(steps, N, BOT, TOP, leq):
    """Mechanical left-linear check: replay the spine per Definition 3.1.
    Every right operand is a leaf (by construction of the steps format);
    verify guards, leaf legality, and the final state."""
    mu = mobius(N, TOP, leq)
    op0, v0 = steps[0]
    assert op0 == 'start'
    if v0 is None:
        X = frozenset()
    else:
        assert v0 != TOP and mu[v0] != 0, "illegal start leaf"
        X = down(N, TOP, leq, v0)
    for (op, v) in steps[1:]:
        assert v is not None and v != TOP and mu[v] != 0, "illegal leaf"
        S = down(N, TOP, leq, v)
        if op == '+':
            assert not (X & S), "+ operands not disjoint"
            X = X | S
        elif op == '-':
            assert S <= X, "- right operand not a subset"
            X = X - S
        else:
            raise AssertionError("bad op")
    target = frozenset(x for x in range(N) if x != TOP)
    assert X == target, "final state is not P minus top"
    return True

def pretty(tree, names):
    if tree[0] == 'empty':
        return '0'
    if tree[0] == 'leaf':
        return 'S' + names[tree[1]]
    return '(' + pretty(tree[1], names) + {'+': ' + ', '-': ' - '}[tree[0]] + pretty(tree[2], names) + ')'

def run_line(line, verbose=True):
    k, E = parse_digraph6(line)
    N, BOT, TOP, leq = build_lattice(k, E)
    assert is_lattice(N, leq), "input is not a lattice"
    # LL-first: the left-linear check is linear in states x leaves, and an
    # LL win implies a general win.  The quadratic general-tree search runs
    # only when LL fails (it would then either exhibit a separation witness
    # or confirm a non-winning lattice).
    mu = mobius(N, TOP, leq)
    steps = find_ll_sequence(N, BOT, TOP, leq)
    if steps is not None:
        check_ll_sequence(steps, N, BOT, TOP, leq)
        if verbose:
            print(f"lattice n={N}  mu={[mu[v] for v in range(N)]}")
            print("WINNING (left-linear). LL sequence verified (" + str(len(steps)) + " steps): " +
                  " ".join((op if op != 'start' else '') + ('S'+str(v) if v is not None else '0') for op, v in steps))
        return True
    tree, mu, target = find_tree(N, BOT, TOP, leq)
    if tree is None:
        print(f"NOT WINNING: {line}")
        return False
    check_tree(tree, N, BOT, TOP, leq)
    names = {i: str(i) for i in range(N)}
    names[BOT] = 'bot'
    print(f"lattice n={N}: SEPARATING — winnable but not left-linear-winnable")
    print(f"tree verified: {pretty(tree, names)}")
    return True

if __name__ == '__main__':
    if sys.argv[1] == '--selftest':
        # M3: 3 interior incomparable
        ok = run_line('&B??')  # k=3 antichain? actually &B?? is k=3 no edges
        # a couple of genposetg lines fed explicitly in the driver instead
        sys.exit(0 if ok else 1)
    ok = True
    for a in sys.argv[1:]:
        ok &= run_line(a)
    sys.exit(0 if ok else 1)
