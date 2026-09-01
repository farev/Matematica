"""Lines of PG(n-1,2) as XOR-triples on F_2^n \ {0} = {1..2^n-1}.

A line is {x, y, x^y}. Enumerated once as (x, y, z) with x < y < z, z == x^y.
A proper coloring assigns colors so no line is monochromatic; color classes
are exactly sum-free sets in F_2^n (no a+b=c with a,b,c in the class).
"""


def lines(n):
    m = (1 << n) - 1
    out = []
    for x in range(1, m + 1):
        for y in range(x + 1, m + 1):
            z = x ^ y
            if z > y:
                out.append((x, y, z))
    return out


def check_coloring(n, color, k):
    """color: dict/list mapping point (1..2^n-1) -> 0..k-1. Returns list of
    monochromatic lines (empty = proper). Exact integer arithmetic only."""
    bad = []
    for (x, y, z) in lines(n):
        if color[x] == color[y] == color[z]:
            bad.append((x, y, z))
    return bad


if __name__ == "__main__":
    for n in range(2, 9):
        L = lines(n)
        m = (1 << n) - 1
        formula = m * (m - 1) // 6
        assert len(L) == formula, (n, len(L), formula)
        print(f"n={n}: {len(L)} lines (matches (2^n-1)(2^n-2)/6)")
