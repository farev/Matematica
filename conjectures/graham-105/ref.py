"""Reference DFS: enumerate all sums of distinct powers of 3 up to T
(= all n with base-3 digits in {0,1}), filter by base-5/base-7 digit
conditions at the leaves.  Exact integer arithmetic throughout.
Also emits the leaf count, which must equal the closed-form count of
base-3-valid n <= T, and the count of n passing base-3+base-5 (full)."""
import sys

def digits_ok(n, b, dmax):
    while n:
        if n % b > dmax:
            return False
        n //= b
    return True

def count_base3_valid(T):
    """#{n in [0,T] : base-3 digits all <= 1} by digit DP (exact)."""
    if T < 0:
        return 0
    digs = []
    t = T
    while t:
        digs.append(t % 3)
        t //= 3
    digs.reverse()          # most significant first
    total = 0
    for i, d in enumerate(digs):        # count n < T with prefix < digs[:i+1]
        below = min(d, 2)               # digits we may place here strictly below d: {0..d-1} ∩ {0,1}
        total += min(d, 2) * (2 ** (len(digs) - 1 - i))
        if d > 1:                       # T itself has a digit 2 somewhere: everything after is free... but prefix already < T handled; T not valid; stop
            return total
    return total + 1                    # T itself valid (all digits <= 1)

def enumerate_terms(T):
    pows = []
    p = 1
    while p <= T:
        pows.append(p)
        p *= 3
    pows.reverse()
    suffix = [0] * (len(pows) + 1)
    for i in range(len(pows) - 1, -1, -1):
        suffix[i] = suffix[i + 1] + pows[i]
    hits, leaves, full35 = [], 0, 0
    stack = [(0, 0)]
    while stack:
        i, s = stack.pop()
        # prune: whole subtree fits under T?  iterate fully anyway (need leaves); only prune impossible adds
        if i == len(pows):
            leaves += 1
            if digits_ok(s, 5, 2):
                full35 += 1
                if digits_ok(s, 7, 3):
                    hits.append(s)
            continue
        stack.append((i + 1, s))
        if s + pows[i] <= T:
            stack.append((i + 1, s + pows[i]))
    return sorted(hits), leaves, full35

if __name__ == "__main__":
    T = int(float(sys.argv[1]))
    hits, leaves, full35 = enumerate_terms(T)
    cf = count_base3_valid(T)
    assert leaves == cf, (leaves, cf)
    print(" ".join(map(str, hits)))
    print(f"T={T} leaves={leaves} closed_form={cf} full35={full35} hits={len(hits)}", file=sys.stderr)
