#!/usr/bin/env python3
"""Close the bottom-order gap in the session's certificate tables.

The committed tables start at n=16 (min-deg-3; NOTE quotes n=12..15 in
prose) and n=14 (cubic), but the C4-free classes are nonempty from n=10.
Here: geng scan of every order from n=4 up, each graph tested for cycles
of length exactly 8 (and 4, re-verified). Independent toolchain: Homebrew
geng 2.9.x + hand-rolled DFS cycle test (not the session's cyclecheck
binary, not networkx's cycle code). Also reproduces the session's counts
at the overlapping orders (mindeg3 12..15, cubic 14..20).

Run from this directory. Committed output:
logs/bottom_orders_2026-07-31.log
"""
import subprocess, sys, time

def g6_line(line):
    data = [ord(c) - 63 for c in line.strip()]
    n = data[0]
    bits = []
    for v in data[1:]:
        for k in range(5, -1, -1):
            bits.append((v >> k) & 1)
    adj = [[] for _ in range(n)]
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                adj[i].append(j); adj[j].append(i)
            idx += 1
    return n, adj

def has_cycle_len(adj, L):
    """existence of a cycle of length exactly L (DFS, canonical start=min)."""
    n = len(adj)
    for s in range(n):
        stack = [(s, 0, 1 << s)]
        while stack:
            u, d, vis = stack.pop()
            if d == L - 1:
                if s in adj[u]:
                    return True
                continue
            for w in adj[u]:
                if w <= s or (vis >> w) & 1:
                    continue
                stack.append((w, d + 1, vis | (1 << w)))
    return False

def scan(n, cls):
    args = ["geng", "-q", "-c", "-d3", "-f"]
    if cls == "cubic":
        args += ["-D3", str(n), f"{3*n//2}:{3*n//2}"]
    else:
        args += [str(n)]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, text=True)
    total = surv48 = 0
    survivors = []
    for line in p.stdout:
        total += 1
        nn, adj = g6_line(line)
        assert not has_cycle_len(adj, 4), "geng -f emitted a C4 graph?!"
        if not has_cycle_len(adj, 8):
            surv48 += 1
            survivors.append(line.strip())
    p.wait()
    assert p.returncode == 0
    return total, surv48, survivors

print("class mindeg3 (geng -c -d3 -f): the bottom orders + overlap check", flush=True)
for n in range(4, 16):
    t0 = time.monotonic()
    t, s, sv = scan(n, "mindeg3")
    dt = time.monotonic() - t0
    print(f"  n={n:2d}  C4free-mindeg3 = {t:8d}   {{4,8}}-free = {s}   [{dt:.1f}s]"
          + ("   " + " ".join(sv) if sv else ""), flush=True)

print("class cubic (geng -c -d3 -D3 -f): bottom orders + overlap check", flush=True)
for n in range(4, 21, 2):
    t0 = time.monotonic()
    t, s, sv = scan(n, "cubic")
    dt = time.monotonic() - t0
    print(f"  n={n:2d}  C4free-cubic   = {t:8d}   {{4,8}}-free = {s}   [{dt:.1f}s]"
          + ("   " + " ".join(sv) if sv else ""), flush=True)
