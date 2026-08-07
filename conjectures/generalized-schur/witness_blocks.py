#!/usr/bin/env python3
"""Structural view of extremal witnesses: run-length encoding by color.

Usage: witness_blocks.py certs/s3_3_8_n*.witness ...
Prints, per witness: n, ts, the color blocks as runs c^len, and per-color
interval decomposition (maximal runs), to expose the construction family
behind each extremal coloring.
"""
import sys


def blocks(colors):
    out = []
    i = 0
    n = len(colors)
    while i < n:
        j = i
        while j < n and colors[j] == colors[i]:
            j += 1
        out.append((colors[i], j - i))
        i = j
    return out


def main():
    for path in sys.argv[1:]:
        with open(path) as f:
            head = f.readline().split()
            n, k = int(head[0]), int(head[1])
            ts = [int(x) for x in head[2:2 + k]]
            colors = [int(c) for c in f.readline().split()]
        rle = blocks(colors)
        print(f"== {path}  n={n} ts={ts}  ({len(rle)} blocks)")
        print("   " + " ".join(f"{c}^{l}" if l > 1 else f"{c}" for c, l in rle))
        for j in range(k):
            runs = []
            i = 0
            while i < n:
                if colors[i] == j:
                    a = i
                    while i < n and colors[i] == j:
                        i += 1
                    runs.append((a + 1, i))  # 1-based inclusive
                else:
                    i += 1
            span = " ".join(f"[{a},{b}]" if a != b else f"[{a}]" for a, b in runs)
            size = sum(b - a + 1 for a, b in runs)
            print(f"   color {j} (t={ts[j]}, {size} elts): {span}")


if __name__ == "__main__":
    main()
