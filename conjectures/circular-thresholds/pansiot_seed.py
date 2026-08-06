"""Seed check / search and pump-and-verify for Lemma PC (NOTE.md session-2).

A seed for (n, phi) is a cyclic bit-word c0 of length m0 with
  (M) g(c0) = id in Sym(n), and
  (S2) every bit-window of c0^w of length m0+2 is code-free.
Given Theorem MC for phi, Lemma PC then yields circular RT(n)+-free words of
length k^j m0 for every j >= 0.

Modes:
  check:  python3 pansiot_seed.py check 3 <bits>
  encode: python3 pansiot_seed.py encode 3 <word over Sigma_n, cyclic>
  pump:   python3 pansiot_seed.py pump 3 <phi0> <phi1> <bits> <jmax>
          decodes and verifies each pumped cycle directly from Definition 1
          (numpy-accelerated; independent of the lemma).
"""
import sys
import numpy as np
from pansiot import (alpha_of, make_taus, comp, g_of, code_free, encode,
                     decode_cycle)


def check_seed(bits, n):
    num, den = alpha_of(n)
    tau0, tau1 = make_taus(n)
    m0 = len(bits)
    okM = g_of(bits, tau0, tau1) == tuple(range(n))
    cyc = list(bits) * 3
    okS = all(code_free(cyc[i : i + m0 + 2], n, num, den) for i in range(m0))
    return okM, okS


def circular_afree_np(w, num, den):
    m = len(w)
    a = np.array(w, dtype=np.int8)
    d = np.concatenate([a, a])
    for p in range(1, m):
        Lp = (num * p) // den + 1
        if Lp > m:
            break
        qq = Lp - p
        eq = d[:m] == d[p : p + m]
        ee = np.concatenate([eq, eq[:qq]])
        v = ee.view(np.int8)
        dd = np.diff(np.concatenate(([0], v, [0])))
        st = np.flatnonzero(dd == 1)
        en = np.flatnonzero(dd == -1)
        if len(st) and (en - st).max() >= qq:
            return False, p
    return True, None


def main():
    mode = sys.argv[1]
    n = int(sys.argv[2])
    num, den = alpha_of(n)
    if mode == "check":
        bits = [int(c) for c in sys.argv[3]]
        okM, okS = check_seed(bits, n)
        print(f"m0={len(bits)} monodromy_id={okM} S2_windows_code_free={okS}")
    elif mode == "encode":
        w = [int(c) for c in sys.argv[3]]
        bits, ok = encode(w + w[: n - 1], n)
        print("encodable:", ok)
        if ok:
            print("cyclic codeword:", "".join(map(str, bits)))
            okM, okS = check_seed(bits, n)
            print(f"monodromy_id={okM} S2_windows_code_free={okS}")
    elif mode == "pump":
        phi0 = tuple(int(c) for c in sys.argv[3])
        phi1 = tuple(int(c) for c in sys.argv[4])
        bits = [int(c) for c in sys.argv[5]]
        jmax = int(sys.argv[6])
        tau0, tau1 = make_taus(n)
        cj = list(bits)
        for j in range(jmax + 1):
            gid = g_of(cj, tau0, tau1) == tuple(range(n))
            w = decode_cycle(cj, n)
            ok, off = circular_afree_np(w, num, den)
            print(f"j={j} len={len(cj)} monodromy_id={gid} "
                  f"circular_free={ok}" + (f" OFFENDER p={off}" if not ok else ""),
                  flush=True)
            if not ok:
                sys.exit(1)
            cj = [b for x in cj for b in (phi1 if x else phi0)]
    else:
        raise SystemExit("unknown mode")


if __name__ == "__main__":
    main()
