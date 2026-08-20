"""dis_reference.py — clean-room Python reference for the dissociated-set
maximum dis(G) and the plus-minus weighted Davenport constant
D_pm(G) = dis(G) + 1 of a finite abelian group G = Z_n1 x ... x Z_nr.

Definitions (NOTE.md, Lemma L1): a subset S of G is *dissociated* iff all
2^|S| subset sums are distinct, iff S has no nonempty {+1,-1}-weighted
zero-sum subsequence. dis(G) = max |S|.

Two independent routines:
  dis(mods)                — DFS over {g,-g}-representatives with a
                             signed-sum reachability mask (same predicate
                             as dis_search.c, independent implementation)
  check_dissociated(mods,S)— literal definition: enumerate all 2^|S|
                             subset sums, verify distinct. Used to verify
                             every witness this directory commits.

CLI:
  python3 dis_reference.py max 5 15         -> dis, witness
  python3 dis_reference.py check 5 15 "(0,1),(0,2),(0,4),(1,0),(2,0)"
"""
import sys
from itertools import product


def group(mods):
    els = list(product(*[range(m) for m in mods]))
    idx = {e: i for i, e in enumerate(els)}
    return els, idx


def dis(mods, want_witness=False):
    els, idx = group(mods)
    N = len(els)
    zero = idx[tuple(0 for _ in mods)]

    def add(a, b):
        return tuple((x + y) % m for x, y, m in zip(a, b, mods))

    reps = []
    for i, e in enumerate(els):
        if i == zero:
            continue
        n = tuple((-x) % m for x, m in zip(e, mods))
        if i <= idx[n]:
            reps.append(i)

    shift = {}
    for g in reps:
        ge = els[g]
        gn = tuple((-x) % m for x, m in zip(ge, mods))
        shift[g] = ([idx[add(els[s], ge)] for s in range(N)],
                    [idx[add(els[s], gn)] for s in range(N)], idx[gn])

    best = [0]
    best_set = [[]]
    zbit = 1 << zero

    def apply(mask, g):
        tbl_p, tbl_m, gneg = shift[g]
        new = mask
        m = mask
        while m:
            low = m & (-m)
            s = low.bit_length() - 1
            new |= (1 << tbl_p[s]) | (1 << tbl_m[s])
            m ^= low
        return new | (1 << g) | (1 << gneg)

    def dfs(start, mask, chosen):
        if len(chosen) > best[0]:
            best[0] = len(chosen)
            best_set[0] = list(chosen)
        for j in range(start, len(reps)):
            g = reps[j]
            new = apply(mask, g)
            if new & zbit:
                continue
            chosen.append(g)
            dfs(j + 1, new, chosen)
            chosen.pop()

    dfs(0, 0, [])
    if want_witness:
        return best[0], [els[i] for i in best_set[0]]
    return best[0]


def check_dissociated(mods, S):
    """Literal definition. Independent of everything above."""
    sums = set()
    for pick in product([0, 1], repeat=len(S)):
        t = tuple(sum(c * e[k] for c, e in zip(pick, S)) % m
                  for k, m in enumerate(mods))
        if t in sums:
            return False
        sums.add(t)
    return True


def parse_set(s, rank):
    s = s.strip()
    if rank == 1:
        return [(int(x),) for x in s.replace("(", "").replace(")", "").split(",")]
    out = []
    for part in s.replace("),(", ");(").split(";"):
        nums = part.strip("()").split(",")
        out.append(tuple(int(x) for x in nums))
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "max":
        mods = [int(x) for x in sys.argv[2:]]
        d, w = dis(mods, want_witness=True)
        print(f"group={'x'.join(map(str, mods))} dis={d} Dpm={d+1} witness={w}")
    elif mode == "check":
        *mods_s, setstr = sys.argv[2:]
        mods = [int(x) for x in mods_s]
        S = parse_set(setstr, len(mods))
        ok = check_dissociated(mods, S)
        print(f"group={'x'.join(map(str, mods))} |S|={len(S)} dissociated={ok}")
        sys.exit(0 if ok else 1)
    else:
        print(__doc__)
        sys.exit(2)
