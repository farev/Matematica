"""Standalone verifier for witness files in data/.

A witness file is one comma-separated line of colors (0..k-1) for the points
1..2^n-1 of F_2^n \ {0}. Verifies from the definition that no line
{x, y, x^y} is monochromatic, using no code from the search pipeline except
the line generator (which is itself checked against (2^n-1)(2^n-2)/6 and
OEIS A006095).

Usage: python3 verify_witness.py data/witness_n7_ord5.txt 7 [5]
"""
import sys


def main():
    path, n = sys.argv[1], int(sys.argv[2])
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    m = (1 << n) - 1
    colors = [int(t) for t in open(path).read().strip().split(",")]
    assert len(colors) == m, f"expected {m} colors, got {len(colors)}"
    assert all(0 <= c < k for c in colors)
    color = [None] + colors
    nlines = 0
    for x in range(1, m + 1):
        for y in range(x + 1, m + 1):
            z = x ^ y
            if z > y:
                nlines += 1
                if color[x] == color[y] == color[z]:
                    print(f"FAIL: monochromatic line ({x},{y},{z}) color {color[x]}")
                    sys.exit(1)
    assert nlines == m * (m - 1) // 6
    sizes = sorted(colors.count(c) for c in range(k))
    print(f"OK: proper {k}-coloring of PG({n-1},2); {nlines} lines checked; "
          f"class sizes {sizes}")


if __name__ == "__main__":
    main()
