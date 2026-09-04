#!/usr/bin/env python3
"""Check the Bartholdi-Blanc-Loisel association lemma on concrete arrangements.

Lemma (BBL 2008, proof of Thm 1.1): if line L is perfect (all its n-2 bounded segments are
triangle sides), let M, N be the lines through its first and last crossings.  Then one of
the segments of M starting at M∩L, or of N starting at N∩L, is unused.

Usage: bbl_check.py <cnf-file-from-kobon_sat2> <kissat-model-file or '-'>  (or import check()).
"""
import itertools
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kobon_sat import local_sequences, triangles


def segments_status(n, seqs):
    """dict (r, a, b) -> True if segment {a,b} on r (adjacent crossings) is a triangle side."""
    tri = set(triangles(n, seqs))
    st = {}
    for r in seqs:
        s = seqs[r]
        for p in range(len(s) - 1):
            a, b = s[p], s[p + 1]
            key = (r,) + tuple(sorted((a, b)))
            st[key] = tuple(sorted((r, a, b))) in tri
    return st


def check(n, sigma):
    seqs = local_sequences(n, sigma)
    st = segments_status(n, seqs)
    perfect = [r for r in seqs if all(st[k] for k in st if k[0] == r)]
    violations = []
    for L in perfect:
        cands = []
        for X in (seqs[L][0], seqs[L][-1]):          # lines through the extreme crossings of L
            s = seqs[X]
            p = s.index(L)
            for q in (p - 1, p + 1):
                if 0 <= q < len(s):
                    cands.append((X,) + tuple(sorted((L, s[q]))))
        if not any(not st[k] for k in cands):
            violations.append(L)
    unused = [k for k, v in st.items() if not v]
    return {'n': n, 'triangles': len(triangles(n, seqs)), 'perfect': len(perfect),
            'unused': len(unused), 'violations': violations}


if __name__ == '__main__':
    from kobon_sat2 import Encoder2
    cnf, model = sys.argv[1], sys.argv[2]
    hdr = open(cnf).readline()
    kv = dict(x.split('=') for x in hdr[2:].split() if '=' in x)
    n, t = int(kv['n']), int(kv['tmin'])
    E = Encoder2(n, t, symbreak=kv['sym'] == 'True', lexdepth=int(kv['lexdepth']), card=kv['card'],
                 tight=kv.get('tight', 'False') == 'True')
    lits = []
    for line in (sys.stdin if model == '-' else open(model)):
        if line.startswith('v '):
            lits += [int(x) for x in line[2:].split()]
    print(check(n, E.decode([l for l in lits if l != 0])))
