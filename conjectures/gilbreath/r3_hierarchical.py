"""X4 — the hierarchical growing-period construction: R3-weak counterexample test.

Construction C: segments [m_{l-1}, m_l) carry right... left-anchored periodic
parities with period P_l = 2^{l+2} (de Bruijn block of order l+2), values
conditioned geometric.  Here: m = (1024, 4096, 16384), periods (8, 16, 32).

Theory predictions tested:
  T1 (replication): lead PARITY at depth s in segment l equals lead parity at
     depth (s mod 2^{c_{l-1}}), c = log2(m_{l-1}), whenever the residue is
     >= P_l.  Exact, deterministic.
  T2 (bad leads persist): value-level bad leads (>= 2) occur at positive
     density in EVERY segment, not just the first.
  T3 (bad leads are 2-adic): deep bad leads are exactly 2 and sit in locally
     all-even patches (level-2 structure).
  T4 (statistics): k-window value counts match the i.i.d. model to
     [immature-prefix constant] + [CLT sqrt(x)]; the k <= order deviations are
     CLT-sized; single-period control has LINEAR deviation at k > order.
"""

import numpy as np
from collections import Counter
from r3_common import THETA, de_bruijn, conditioned_geometric

M = [1024, 4096, 16384]          # segment right boundaries
ORD = [3, 4, 5]                  # de Bruijn orders per segment (P = 8, 16, 32)
N = M[-1] + 2


def build_parities():
    y = np.empty(N, dtype=np.uint8)
    lo = 0
    for mb, o in zip(M, ORD):
        blk = de_bruijn(o)
        idx = np.arange(lo, min(mb, N))
        y[idx] = blk[idx % len(blk)]
        lo = mb
    if lo < N:
        y[lo:] = de_bruijn(ORD[-1])[np.arange(lo, N) % 32]
    return y


def lead_traces(a):
    """Value and parity leads for depths 1..len(a)-1."""
    x = np.asarray(a, dtype=np.int64).copy()
    p = (x & 1).astype(np.uint8)
    lv = np.empty(len(a) - 1, dtype=np.int64)
    lp = np.empty(len(a) - 1, dtype=np.uint8)
    for s in range(len(a) - 1):
        x = np.abs(x[1:] - x[:-1])
        p = p[1:] ^ p[:-1]
        lv[s] = x[0]
        lp[s] = p[0]
    return lv, lp                # index s -> depth s+1


def patch_at(a, depth, width=48, height=10):
    """Values of rows [depth-height, depth] restricted to columns [0, width]."""
    x = np.asarray(a, dtype=np.int64)[:depth + width + 2].copy()
    rows = {}
    for s in range(1, depth + 1):
        x = np.abs(x[1:] - x[:-1])
        if s >= depth - height:
            rows[s] = x[:width].copy()
    return rows


def kwindow_dev(a, kmax, x, rng_model, n_control=20):
    """Max |count - x p_v| over patterns, per k; plus i.i.d. control quantiles."""
    a = np.asarray(a[:x])
    th = THETA
    out = {}
    for k in range(1, kmax + 1):
        n = x - k + 1
        cnt = Counter()
        code = np.zeros(n, dtype=np.int64)
        for j in range(k):
            code = code * 512 + a[j:j + n]
        cnt.update(code.tolist())
        # model probability of each observed pattern + patterns w/ count 0 are
        # dominated by observed ones for max-dev at these sizes
        devs = []
        for pat, c in cnt.items():
            digs = []
            t = pat
            for _ in range(k):
                digs.append(t % 512)
                t //= 512
            p = np.prod([(1 - th) * th ** d for d in digs])
            devs.append(abs(c - n * p))
        out[k] = max(devs)
    # control: same statistic on i.i.d. sequences
    ctrl = {k: [] for k in range(1, kmax + 1)}
    for _ in range(n_control):
        b = (rng_model.geometric(1 - th, size=x) - 1).astype(np.int64)
        for k in range(1, kmax + 1):
            n = x - k + 1
            code = np.zeros(n, dtype=np.int64)
            for j in range(k):
                code = code * 512 + b[j:j + n]
            cnt = Counter(code.tolist())
            devs = []
            for pat, c in cnt.items():
                digs = []
                t = pat
                for _ in range(k):
                    digs.append(t % 512)
                    t //= 512
                p = np.prod([(1 - th) * th ** d for d in digs])
                devs.append(abs(c - n * p))
            ctrl[k].append(max(devs))
    return out, {k: (np.median(v), np.max(v)) for k, v in ctrl.items()}


if __name__ == "__main__":
    y = build_parities()
    rng = np.random.default_rng(1878)

    # ---- T1: exact parity replication (deterministic, one build suffices)
    a = conditioned_geometric(y, rng)
    lv, lp = lead_traces(a)
    dep = np.arange(1, N)        # lv[s] is depth s+1 -> dep aligns
    lp_by_depth = np.empty(N, dtype=np.uint8)
    lp_by_depth[1:] = lp
    lp_by_depth[0] = 0
    ok2 = all(lp_by_depth[s] == lp_by_depth[s % 1024]
              for s in range(M[0], M[1]) if s % 1024 >= 16)
    ok3 = all(lp_by_depth[s] == lp_by_depth[s % 4096]
              for s in range(M[1], M[2]) if s % 4096 >= 32)
    print(f"T1 replication: segment 2 mod 1024: {'PASS' if ok2 else 'FAIL'}; "
          f"segment 3 mod 4096: {'PASS' if ok3 else 'FAIL'}")

    # ---- T2: bad-lead density per segment, over seeds
    ranges = [(64, M[0]), (M[0], M[1]), (M[1], M[2])]
    dens = {r: [] for r in ranges}
    maxbad = []
    for sd in range(200, 210):
        r = np.random.default_rng(sd)
        aa = conditioned_geometric(y, r)
        lvv, _ = lead_traces(aa)
        lvd = np.empty(N, dtype=np.int64)
        lvd[1:] = lvv
        lvd[0] = 0
        for rg in ranges:
            seg = lvd[rg[0]:rg[1]]
            dens[rg].append(np.mean(seg >= 2))
        maxbad.append(int(np.max(np.nonzero(lvd >= 2)[0])))
    for rg in ranges:
        print(f"T2 bad-lead density, depths [{rg[0]:>5}, {rg[1]:>5}): "
              f"{np.mean(dens[rg]):.3f} +- {np.std(dens[rg]):.3f}")
    print(f"T2 deepest bad lead over seeds: min {min(maxbad)}, max {max(maxbad)} "
          f"(construction depth {N - 2})")

    # ---- T3: inspect one deep bad lead
    lvd = np.empty(N, dtype=np.int64)
    lvd[1:] = lv
    lvd[0] = 0
    deep_bad = [s for s in range(M[1] + 200, M[2]) if lvd[s] >= 2]
    print(f"T3 deep bad leads (segment 3): {len(deep_bad)} depths; "
          f"values at first five: {[int(lvd[s]) for s in deep_bad[:5]]}")
    s0 = deep_bad[0]
    rows = patch_at(a, s0, width=40, height=6)
    allev = all((rows[s] % 2 == 0).all() for s in rows)
    sup = sorted({int(v) for s in rows for v in rows[s]})
    print(f"T3 patch around depth {s0}: all-even {allev}, value support {sup}")

    # ---- T4: window statistics vs model, at two truncations, vs iid control
    for x in (M[1], M[2]):
        devs, ctrl = kwindow_dev(a, 6, x, np.random.default_rng(9), 20)
        print(f"T4 x={x}: max|count - x p_v| per k  "
              "(construction | iid control median/max):")
        for k in range(1, 7):
            print(f"    k={k}: {devs[k]:8.1f}   | {ctrl[k][0]:7.1f} /"
                  f" {ctrl[k][1]:7.1f}   sqrt(x)={np.sqrt(x):.0f}")

    # ---- T4b: single-period control (P=32 everywhere): k=6 linear growth
    y32 = de_bruijn(5)[np.arange(N) % 32]
    a32 = conditioned_geometric(y32, np.random.default_rng(3))
    for x in (M[1], M[2]):
        devs, _ = kwindow_dev(a32, 6, x, np.random.default_rng(9), 0)
        print(f"T4b single-period P=32, x={x}: k=5 dev {devs[5]:.1f}, "
              f"k=6 dev {devs[6]:.1f} (linear in x if periodic forever)")
