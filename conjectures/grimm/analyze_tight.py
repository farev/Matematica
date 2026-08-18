#!/usr/bin/env python3
"""Analysis of the tight gaps (Hall margin <= 0) mined by mine_stats.py.

For every gap in data/tight.csv, re-derives the margin from the census rows
and finds a WITNESS subset achieving it, then classifies:

  prime-power   the minimum is achieved by a singleton {p^a} (member with a
                single distinct prime factor <= k)
  interaction   the minimum needs >= 2 members (genuinely interacting
                criticals sharing a small prime pool)

Prints per-decade counts of each class, the largest tight gap of each class,
and the top-10 largest tight gaps overall. Also verifies the standing
prediction that the largest prime power p^a <= 1e12 with p small (3^25 =
847288609443) sits in a tight gap, if the census contains it.

Exact integer arithmetic only.
"""
import csv
from collections import defaultdict
from itertools import combinations

def main():
    gaps = defaultdict(list)
    with open("data/tight.csv") as f:
        for row in csv.DictReader(f):
            p, k = int(row["p"]), int(row["k"])
            fac = tuple(int(x) for x in row["factorization"].split("*"))
            gaps[(p, k)].append((int(row["m"]), fac))
    perdec = defaultdict(lambda: [0, 0])   # decade -> [prime-power, interaction]
    largest = {"prime-power": (0, None), "interaction": (0, None)}
    allt = []
    for (p, k), mem in sorted(gaps.items()):
        s = len(mem)
        best, bestT = 10**9, None
        for r in range(1, s + 1):
            for T in combinations(range(s), r):
                uni = set()
                for u in T: uni.update(mem[u][1])
                d = len(uni) - len(T)
                if d < best: best, bestT = d, T
        cls = "prime-power" if len(bestT) == 1 else "interaction"
        assert best <= 0, (p, k, best)
        d = len(str(p)) - 1
        perdec[d][0 if cls == "prime-power" else 1] += 1
        if p > largest[cls][0]:
            largest[cls] = (p, dict(k=k, s=s, margin=best,
                                    witness=[mem[u][0] for u in bestT]))
        allt.append((p, k, best, cls, [mem[u][0] for u in bestT]))
    print("tight gaps by decade (10^d <= p < 10^(d+1)):")
    print("decade  prime-power  interaction")
    for d in sorted(perdec):
        print(f"  {d:2d}      {perdec[d][0]:7d}    {perdec[d][1]:7d}")
    for cls, (p, info) in largest.items():
        print(f"largest {cls} tight gap: p={p} {info}")
    allt.sort(reverse=True)
    print("top-10 tight gaps by p:")
    for p, k, marg, cls, wit in allt[:10]:
        print(f"  p={p} k={k} margin={marg} class={cls} witness={wit}")
    # prediction check: 3^25
    t = 3**25
    hit = [(p, k) for (p, k) in gaps if p < t < p + k + 1]
    print(f"3^25 = {t}: {'in tight gap ' + str(hit[0]) if hit else 'NOT among tight gaps (check!)'}")
    # margin < 0 would be a counterexample
    neg = [(p, k, marg) for p, k, marg, _, _ in allt if marg < 0]
    print(f"gaps with margin < 0 (counterexamples): {len(neg)}")

if __name__ == "__main__":
    main()
