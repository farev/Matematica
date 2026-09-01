#!/usr/bin/env python3
"""Prototype: decide winning-da-tree existence for all lattices with n elements.

Pipeline: nauty-genposetg k t  ->  k-element posets (Hasse, digraph6, topological
order)  ->  keep those whose bounded extension (add bottom, top) is a lattice
(n = k+2 elements)  ->  decide whether the lattice has a winning da-tree
(Wilhelm, arXiv:2608.27416, Def. 3.1).

Da-tree semantics: states buildable by some da-tree = closure of
{emptyset} u {S_v : mu(v) != 0} under disjoint union and guarded difference
(A\\B only when B subset A).  Winning iff P\\{top} is in the closure.

All arithmetic exact (integers/bitmasks).  This is the reference
implementation; the C engine must agree with it everywhere.
"""
import subprocess, sys
from collections import Counter

def parse_digraph6(line):
    """Return (k, rows) where rows[i] = bitmask of j with edge i->j."""
    assert line.startswith('&'), line[:10]
    s = line[1:]
    n = ord(s[0]) - 63
    assert n < 63
    bits = []
    for c in s[1:]:
        v = ord(c) - 63
        bits.extend((v >> (5 - t)) & 1 for t in range(6))
    rows = []
    for i in range(n):
        m = 0
        for j in range(n):
            if bits[i * n + j]:
                m |= 1 << j
        rows.append(m)
    return n, rows

def analyze(k, rows):
    """rows: Hasse edges among interior elements (direction as genposetg emits).

    Returns None if bounded extension is not a lattice, else a dict with the
    lattice data needed for the decision."""
    # up[i] = bitmask of interior elements strictly above i (transitive), plus i itself
    # First determine edge direction: genposetg t = topological order. We treat
    # edge i->j as "i covered by j" i.e. i < j; verified by count validation.
    up = [0] * k          # up-closure including self, interior only
    # topological order: with edges i->j meaning i<j, process from top down
    order = range(k - 1, -1, -1)
    for i in order:
        u = 1 << i
        m = rows[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            u |= up[j]
        up[i] = u
    # lattice check: every incomparable interior pair needs a least common
    # interior upper bound, or none (then join = top).
    for x in range(k):
        for y in range(x + 1, k):
            if up[x] & (1 << y) or up[y] & (1 << x):
                continue  # comparable
            U = up[x] & up[y] & ~((1 << x) | (1 << y))
            U = up[x] & up[y]
            if U == 0:
                continue  # join is top
            # least element of U: some m in U with U subset up[m]
            ok = False
            mm = U
            while mm:
                j = (mm & -mm).bit_length() - 1
                mm &= mm - 1
                if U & ~up[j] == 0:
                    ok = True
                    break
                # optimization: only minimal elements can qualify; but keep simple
            if not ok:
                return None
    # lattice with n = k+2 elements: indices 0..k-1 interior, k = bottom, top implicit
    # ground set for states: P \ {top} = interior + bottom -> bits 0..k (bit k = bottom)
    nfull = k + 1
    target = (1 << nfull) - 1
    # down-sets S_v within P\{top}: for interior v: v + interior strictly below + bottom
    dn = [0] * nfull
    for i in range(k):
        d = 1 << i
        for j in range(k):
            if j != i and (up[j] >> i) & 1:  # i in up[j] means j <= i... careful
                d |= 1 << j
        dn[i] = d | (1 << k)  # bottom below everything
    dn[k] = 1 << k  # S_bottom = {bottom}
    # mu over all elements including top. mu[top]=1; process interior in
    # decreasing height: mu[v] = -sum_{u>v} mu[u]. up[i] includes i itself.
    mu = [0] * (nfull + 1)  # index nfull = top
    mu[nfull] = 1
    # order interior by size of up-set (smaller = higher)
    for i in sorted(range(k), key=lambda t: bin(up[t]).count('1')):
        s = mu[nfull]  # top is above everything
        m = up[i] & ~(1 << i)
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            s += mu[j]
        mu[i] = -s
    mu[k] = -(mu[nfull] + sum(mu[j] for j in range(k)))  # bottom: everything above it
    # sanity: total sum over P must be 0 (n>=2)
    assert mu[nfull] + mu[k] + sum(mu[j] for j in range(k)) == 0
    leaves = sorted({dn[v] for v in range(nfull) if mu[v] != 0})
    return dict(k=k, up=up, dn=dn, mu=mu, leaves=leaves, target=target)

def decide(leaves, target):
    """Closure under disjoint-union and guarded difference; return (win, nstates)."""
    if target in leaves:
        return True, len(leaves)
    seen = set(leaves)
    states = list(leaves)
    i = 0
    while i < len(states):
        A = states[i]
        for j in range(i + 1):
            B = states[j]
            AB = A & B
            if AB == 0:
                C = A | B
                if C not in seen:
                    if C == target:
                        return True, len(states)
                    seen.add(C)
                    states.append(C)
            else:
                if AB == B and A != B:
                    C = A ^ B
                    if C not in seen:
                        if C == target:  # cannot happen (C<A<=target) unless A>target
                            return True, len(states)
                        seen.add(C)
                        states.append(C)
                elif AB == A and A != B:
                    C = B ^ A
                    if C not in seen:
                        if C == target:
                            return True, len(states)
                        seen.add(C)
                        states.append(C)
        i += 1
    return target in seen, len(states)

def decide_ll(leaves, target):
    """Left-linear winnability: BFS from {leaves, 0} under A|L (disjoint) and
    A^L (L subset of A), leaf always the right operand.  Independent of the C
    engine's implementation."""
    if target in leaves:
        return True
    seen = set(leaves)
    seen.add(0)
    q = list(seen)
    i = 0
    while i < len(q):
        A = q[i]
        i += 1
        for L in leaves:
            al = A & L
            if al == 0:
                C = A | L
            elif al == L:
                C = A ^ L
            else:
                continue
            if C not in seen:
                if C == target:
                    return True
                seen.add(C)
                q.append(C)
    return False

def run(k, expect_posets=None, expect_lattices=None, stats=False):
    proc = subprocess.Popen(['nauty-genposetg', str(k), 't', 'q'],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            text=True)
    nposet = nlat = nwin = nllwin = 0
    closure_sizes = Counter()
    worst = (0, None)
    for line in proc.stdout:
        line = line.strip()
        if not line or not line.startswith('&'):
            continue
        nposet += 1
        kk, rows = parse_digraph6(line)
        L = analyze(kk, rows)
        if L is None:
            continue
        nlat += 1
        win, ns = decide(L['leaves'], L['target'])
        llwin = decide_ll(L['leaves'], L['target'])
        if llwin:
            nllwin += 1
            assert win, f"LL-win without general win (impossible): {line}"
        elif win:
            print(f"SEPARATING LATTICE n={k+2}: {line}")
        if win:
            nwin += 1
        else:
            print(f"NON-WINNING LATTICE FOUND n={k+2}: {line}")
        if stats:
            closure_sizes[min(ns, 10**9)] += 1
            if ns > worst[0]:
                worst = (ns, line)
    proc.wait()
    out = f"k={k} n={k+2}: posets={nposet} lattices={nlat} winning={nwin} llwinning={nllwin}"
    if expect_posets is not None:
        out += f" [posets {'OK' if nposet==expect_posets else 'MISMATCH exp '+str(expect_posets)}]"
    if expect_lattices is not None:
        out += f" [lattices {'OK' if nlat==expect_lattices else 'MISMATCH exp '+str(expect_lattices)}]"
    print(out)
    if stats and nlat:
        szs = sorted(closure_sizes.items())
        tot = sum(closure_sizes.values())
        mx = szs[-1][0]
        med = None
        c = 0
        for s, cnt in szs:
            c += cnt
            if med is None and c >= tot / 2:
                med = s
        print(f"   closure states: median={med} max={mx} worst_line={worst[1]}")
    return nposet, nlat, nwin

if __name__ == '__main__':
    # unit controls first
    # M3 diamond: interior = antichain a,b,c -> k=3 rows all 0
    L = analyze(3, [0, 0, 0])
    assert L is not None and decide(L['leaves'], L['target'])[0], "M3 must win"
    assert sorted(L['mu']) == [-1, -1, -1, 1, 2], f"M3 mu wrong: {L['mu']}"
    # N5 pentagon: interior a; b<c  -> k=3, edge 1->2
    L = analyze(3, [0, 1 << 2, 0])
    assert L is not None and decide(L['leaves'], L['target'])[0], "N5 must win"
    assert sorted(L['mu']) == [-1, -1, 0, 1, 1], f"N5 mu wrong: {L['mu']}"
    # artificial negative control: 3-chain with leaf S_a removed
    win, _ = decide([0b10], 0b11)  # leaves {bottom}, target {a,bottom}
    assert not win, "negative control failed"
    print("unit controls OK")
    A112 = {1:1,2:2,3:5,4:16,5:63,6:318,7:2045,8:16999,9:183231,10:2567284}
    A6966 = {3:1,4:2,5:5,6:15,7:53,8:222,9:1078,10:5994,11:37622,12:262776}
    for k in range(1, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 9):
        run(k, A112.get(k), A6966.get(k + 2), stats=True)
