"""Certify a uniform binary Pansiot-code morphism for Theorem MC (NOTE.md
session-2 part): checks, in exact arithmetic,

  (Ha) phi0[0] != phi1[0]        (Hb) phi0[k-1] != phi1[k-1]
  (Hc) no phi(c) at offset 0<i<k inside phi(a)phi(b) for code-free ab
  (C2) g(phi_b) = pi^-1 tau_b pi for a common pi in Sym(n)
  (Hd) phi(V) code-free for every code-free V with |V| <= N0,
       P0 = ceil((2k+n-2)/(alpha-1)),
       N0 = ceil((floor(alpha P0) + 1 + (n-1))/k) + 1
       (the n-1 accounts for the covering margin in Theorem MC, case A).

By Theorem MC these imply phi maps code-free words to code-free words
(rigorous for n = 3; for n >= 4 subject to the small-period addendum stated
in the NOTE).  Usage:

  python3 pansiot_certify.py 3 0101101011101110110 1011010111011101011
"""
import sys, math
from itertools import permutations
from pansiot import (alpha_of, make_taus, comp, g_of, code_free,
                     all_codefree_upto)


def certify(n, phi0, phi1, verbose=True):
    num, den = alpha_of(n)
    k = len(phi0)
    assert len(phi1) == k
    tau0, tau1 = make_taus(n)
    out = {}
    out["Ha"] = phi0[0] != phi1[0]
    out["Hb"] = phi0[-1] != phi1[-1]
    imgs = {0: phi0, 1: phi1}
    hc = True
    for a in (0, 1):
        for b in (0, 1):
            if not code_free([a, b], n, num, den):
                continue
            cat = imgs[a] + imgs[b]
            for c in (0, 1):
                for i in range(1, k):
                    if cat[i : i + k] == imgs[c]:
                        hc = False
    out["Hc"] = hc
    g0, g1 = g_of(phi0, tau0, tau1), g_of(phi1, tau0, tau1)
    out["C2"] = None
    for pi in permutations(range(n)):
        ip = [0] * n
        for i, v in enumerate(pi):
            ip[v] = i
        ip = tuple(ip)
        if comp(comp(ip, tau0), pi) == g0 and comp(comp(ip, tau1), pi) == g1:
            out["C2"] = pi
            break
    P0 = math.ceil((2 * k + n - 2) * den / (num - den))
    N0 = math.ceil(((num * P0) // den + 1 + (n - 1)) / k) + 1
    out["P0"], out["N0"] = P0, N0
    words = all_codefree_upto(n, num, den, N0)
    hd = True
    for V in words:
        img = []
        for b in V:
            img.extend(phi1 if b else phi0)
        if not code_free(img, n, num, den):
            hd = False
            break
    out["Hd"] = hd
    out["Hd_words_checked"] = len(words)
    ok = out["Ha"] and out["Hb"] and out["Hc"] and out["C2"] is not None and hd
    out["CERTIFIED"] = ok
    if verbose:
        for kk, vv in out.items():
            print(f"  {kk}: {vv}")
    return out


if __name__ == "__main__":
    n = int(sys.argv[1])
    p0 = tuple(int(c) for c in sys.argv[2])
    p1 = tuple(int(c) for c in sys.argv[3])
    r = certify(n, p0, p1)
    sys.exit(0 if r["CERTIFIED"] else 1)
