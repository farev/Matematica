"""Fourier/Hoffman analysis of extension obstructions.

For a class S subset F_2^7*, Cay(F_2^7, S) is |S|-regular on 128 vertices
with integer eigenvalues lam_x = sum_{h in S} (-1)^{x.h} (x in F_2^7),
computable exactly by a Walsh-Hadamard transform over Z.
Hoffman ratio bound: alpha <= 128 * m / (|S| + m) where m = -lam_min >= 0.
(Exact rational comparison; floor.) Necessary for extension of the witness:
sum_c alpha_c >= 128; so sum_c hoffman_c < 128 certifies non-extendability.

Also reports greedy lower bounds to gauge tightness.
"""
import sys
import random
from fractions import Fraction
from sample_extend import sample_witness, try_extend, M7, K


def wht_eigs(S):
    """Exact eigenvalues of Cay(F_2^7,S): array over x in 0..127."""
    f = [0] * 128
    for h in S:
        f[h] = 1
    # in-place WHT (exact ints)
    a = f[:]
    h = 1
    while h < 128:
        for i in range(0, 128, h * 2):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j], a[j + h] = x + y, x - y
        h *= 2
    return a  # a[0] = |S|; a[x] = lam_x


def hoffman_ub(S):
    eig = wht_eigs(S)
    d = eig[0]
    lam_min = min(eig[1:])
    assert lam_min < 0
    m = -lam_min
    # alpha <= 128*m/(d+m), take floor of exact fraction
    fr = Fraction(128 * m, d + m)
    return fr.numerator // fr.denominator, d, lam_min


def greedy_lb(S, tries=60, rng=None):
    rng = rng or random.Random(1)
    best = 0
    for _ in range(tries):
        order = list(range(128))
        rng.shuffle(order)
        cur = set()
        for v in order:
            if all((v ^ h) not in cur for h in S):
                cur.add(v)
        best = max(best, len(cur))
    return best


def main():
    nsamples = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 555000
    rng = random.Random(seed0)
    n_cert_blocked = 0
    n_ext = 0
    print("sizes | hoffmanUBs (sum) | greedyLBs (sum) | verdict")
    for i in range(nsamples):
        w = sample_witness(seed0 + i, rng)
        classes = [[p for p in range(1, M7 + 1) if w[p] == c] for c in range(K)]
        ubs, lbs = [], []
        for cl in classes:
            ub, d, lm = hoffman_ub(cl)
            ubs.append(ub)
            lbs.append(greedy_lb(cl, 40, rng))
        sizes = [len(c) for c in classes]
        sub, slb = sum(ubs), sum(lbs)
        ext = try_extend(w)
        verdict = "EXTENDS!" if ext else ("cert-blocked" if sub < 128 else "blocked(packing)")
        if ext:
            n_ext += 1
            print("FULL8:", ",".join(str(ext[p]) for p in range(1, 256)))
        if sub < 128:
            n_cert_blocked += 1
        print(f"{sorted(sizes)} | {sorted(ubs)} ({sub}) | {sorted(lbs)} ({slb}) | {verdict}", flush=True)
    print(f"\n{n_cert_blocked}/{nsamples} certifiably blocked by Hoffman sum < 128; {n_ext} extended")


if __name__ == "__main__":
    main()
