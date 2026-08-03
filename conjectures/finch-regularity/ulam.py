#!/usr/bin/env python3
"""Reference (slow, obviously-correct) generator for 1-additive sequences U(a,b).

A 1-additive sequence: start a < b.  Each subsequent term is the least integer
greater than the last term having EXACTLY ONE representation as u+v with
u < v both earlier terms of the sequence.

This is the positive control: dead simple, no cleverness, used to validate the
fast implementations.
"""
import sys


def ulam(a, b, N):
    """All terms of U(a,b) that are <= N.  O(k^2) with a count array."""
    assert 0 < a < b
    cnt = [0] * (N + 2)          # cnt[x] = #{u<v in seq : u+v == x}, saturating not needed here
    terms = []

    def add(t):
        for s in terms:
            if s + t <= N:
                cnt[s + t] += 1
        terms.append(t)

    add(a)
    add(b)
    x = b
    while True:
        x += 1
        if x > N:
            break
        if cnt[x] == 1:
            add(x)
    return terms


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    N = int(float(sys.argv[3])) if len(sys.argv) > 3 else 200
    t = ulam(a, b, N)
    print(f"U({a},{b}) up to {N}: {len(t)} terms")
    print(t[:60])
    ev = [x for x in t if x % 2 == 0]
    print(f"even terms ({len(ev)}): {ev[:40]}")
