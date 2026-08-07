"""Exhaustive letterwise search: uniform binary Pansiot-code morphism pairs
(phi0, phi1) over valid k-blocks, pooled by every monodromy-compatibility
class sufficient for Lemma PC --

  C2   : g(phi_b) = pi^-1 tau_b pi (common pi)      [theta injective]
  SIGN : theta factors through the sign character
  col1 : g(phi_0) = g(phi_1) = id                    (collapse at level 1)
  col2 : g(phi(phi(b))) = id for b = 0,1             (collapse at level 2)

-- then filtered by: the fixed point of phi (or phi^2 when phi is not
prolongable) decodes alpha+-free to depth 4000 (a NECESSARY condition for
either route to Lemma PC; an offender found in a fixed-point prefix is an
exact refutation of that candidate).

Usage: python3 pansiot_search.py <n> <kmin> <kmax>
Output: one line per k with pool size and surviving candidates.
"""
import sys, time
import numpy as np
from itertools import permutations
from collections import defaultdict
from pansiot import alpha_of, make_taus, comp, g_of, decode, valid_blocks


def sign_of(perm):
    n = len(perm)
    seen = [False] * n
    s = 1
    for i in range(n):
        if not seen[i]:
            j, c = i, 0
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                c += 1
            if c % 2 == 0:
                s = -s
    return s


def max_run_ok(x, num, den):
    L = len(x)
    for p in range(1, L - 1):
        qq = (num * p) // den + 1 - p
        eq = x[:-p] == x[p:]
        if not eq.any():
            continue
        d = np.diff(np.concatenate(([0], eq.view(np.int8), [0])))
        st = np.flatnonzero(d == 1)
        en = np.flatnonzero(d == -1)
        if len(st) and (en - st).max() >= qq:
            return False
    return True


def fp_prefix(phi0, phi1, L):
    if phi0[0] == 0:
        w = list(phi0)
        sub = {0: list(phi0), 1: list(phi1)}
    elif phi1[0] == 1:
        w = list(phi1)
        sub = {0: list(phi0), 1: list(phi1)}
    else:
        p20 = [b for x in phi0 for b in (phi1 if x else phi0)]
        p21 = [b for x in phi1 for b in (phi1 if x else phi0)]
        if p20[0] == 0:
            w, sub = list(p20), {0: p20, 1: p21}
        elif p21[0] == 1:
            w, sub = list(p21), {0: p20, 1: p21}
        else:
            return None
    while len(w) < L:
        nw = []
        for b in w:
            nw.extend(sub[b])
            if len(nw) >= L + len(sub[0]):
                break
        if len(nw) == len(w):
            return None
        w = nw
    return w[:L]


def pool_v2(n, num, den, k, tau0, tau1, idp):
    blocks = valid_blocks(n, num, den, k)
    gs = {b: g_of(b, tau0, tau1) for b in blocks}
    byg = defaultdict(list)
    for b in blocks:
        byg[gs[b]].append(b)
    pairs = defaultdict(set)
    for pi in permutations(range(n)):
        ip = [0] * n
        for i, v in enumerate(pi):
            ip[v] = i
        ip = tuple(ip)
        t0c = comp(comp(ip, tau0), pi)
        t1c = comp(comp(ip, tau1), pi)
        for a in byg.get(t0c, []):
            for c in byg.get(t1c, []):
                pairs[(a, c)].add("C2")
    s0, s1 = sign_of(tau0), sign_of(tau1)
    for a in blocks:
        ga = gs[a]
        oka = (ga == idp) if s0 == 1 else (comp(ga, ga) == idp)
        if not oka:
            continue
        for c in blocks:
            gc = gs[c]
            okc = (gc == idp) if s1 == 1 else (comp(gc, gc) == idp)
            if not okc:
                continue
            if s0 == -1 and s1 == -1 and ga != gc:
                continue
            pairs[(a, c)].add("SIGN")
    for a in byg.get(idp, []):
        for c in byg.get(idp, []):
            pairs[(a, c)].add("col1")
    for a in blocks:
        for c in blocks:
            g20 = idp
            for bit in a:
                g20 = comp(g20, gs[c] if bit else gs[a])
            if g20 != idp:
                continue
            g21 = idp
            for bit in c:
                g21 = comp(g21, gs[c] if bit else gs[a])
            if g21 == idp:
                pairs[(a, c)].add("col2")
    return blocks, pairs


def main(n, kmin, kmax, L1=600, L2=4000):
    num, den = alpha_of(n)
    tau0, tau1 = make_taus(n)
    idp = tuple(range(n))
    total = 0
    for k in range(kmin, kmax + 1):
        t0 = time.time()
        blocks, pairs = pool_v2(n, num, den, k, tau0, tau1, idp)
        surv = []
        for (a, c), tags in pairs.items():
            w = fp_prefix(a, c, L1)
            if w is None:
                continue
            x = np.array(decode(w, n), dtype=np.int8)
            if not max_run_ok(x, num, den):
                continue
            w = fp_prefix(a, c, L2)
            x = np.array(decode(w, n), dtype=np.int8)
            if max_run_ok(x, num, den):
                surv.append((a, c, sorted(tags)))
        dt = time.time() - t0
        print(f"n={n} k={k}: |V_k|={len(blocks)} pool={len(pairs)} "
              f"cand={len(surv)} [{dt:.1f}s]", flush=True)
        for a, c, tags in surv:
            print(f"   CAND n={n} k={k} {tags}\n     phi0={''.join(map(str,a))}"
                  f"\n     phi1={''.join(map(str,c))}", flush=True)
            total += 1
    print(f"n={n}: TOTAL {total}", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
