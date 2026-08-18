"""Machine corroboration of Theorem T1's parametric case tree.

For each n, builds the tree of extensions of the forced distinct head
0..n-2 under the non-strict checker (undirected exponents >= (n-1)/(n-2)
forbidden), with every candidate letter tried at every node, and encodes
nodes by back-distance symbols (A = distance n-1, B = n, C = n+1,
F = fresh).  Verifies the tree is identical to the n = 22 tree and that
the maximal tail length is 4 (total n+3), unique tail A,F,B,A.

python3 case_tree.py            # checks n in {5..31, 40, 60, 100}
"""

import sys

from urt import UInc


def case_tree(n, maxsteps=8):
    num, den = n - 1, n - 2
    head = list(range(n - 1))
    tree = {}

    def rec(tail, depth):
        if depth > maxsteps:
            return
        word = head + list(tail)
        viable = []
        used = max(word) + 1
        for c in range(min(used + 1, n)):
            inc = UInc(num, den, len(word) + 2, strict=False)
            if all(inc.push(ch) for ch in word + [c]):
                viable.append(c)
        tree[tuple(tail)] = viable
        for c in viable:
            rec(tail + [c], depth + 1)

    rec([], 0)
    return tree


def signature(tree, n):
    out = {}
    for tail, viable in tree.items():
        word = list(range(n - 1)) + list(tail)

        def sym(w2, pos):
            c = w2[pos]
            occ = [i for i in range(pos) if w2[i] == c]
            if not occ:
                return "F"
            d = pos - occ[-1]
            return {n - 1: "A", n: "B", n + 1: "C", n + 2: "D"}.get(d, f"d{d}")

        nt = tuple(sym(word, n - 1 + i) for i in range(len(tail)))
        out[nt] = sorted(sym(word + [v], len(word)) for v in viable)
    return out


if __name__ == "__main__":
    ns = list(range(5, 32)) + [40, 60, 100]
    ref = signature(case_tree(22), 22)
    ok = True
    for n in ns:
        t = case_tree(n)
        s = signature(t, n)
        maxtail = max(len(k) for k in t)
        tails4 = [k for k in t if len(k) == 4]
        same = s == ref
        ok &= same and maxtail == 4 and len(tails4) == 1
        print(f"n={n}: tree {'==' if same else '!='} n=22 tree, "
              f"max tail {maxtail}, length-4 tails {tails4}")
    print("ALL IDENTICAL, max length n+3, unique extremal tail (A,F,B,A)"
          if ok else "MISMATCH")
    sys.exit(0 if ok else 1)
