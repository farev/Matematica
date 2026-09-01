"""Sample chi_2(7)=5 witnesses via randomized CDCL, fingerprint them, and
SAT-test extension to chi_2(8)=5.

Split F_2^8 = H + <e8>, H = F_2^7 (points 1..127), affine part = {(v,1)}.
Lines of PG(7,2) = lines inside H (2667) + mixed lines {(v,1),(v+h,1),(h,0)}
for h in H* (8128). Given a proper 5-coloring W of H*, the extension problem
colors the 128 affine points s.t. for every affine pair {a, a+h}: not both
color W(h). Any extension = full chi_2(8)=5 witness (verified from def).

Sampling: the n=7 CNF is GL(7,2)-symmetric, so we shuffle variable indices
with a random point permutation from GL(7,2) and vary kissat --seed. Each
witness is verified from the definition before use.

Fingerprint per witness: sorted class sizes + sorted row-multiset of the
5x5 'two-in-i-one-in-j' line-count matrix (invariant under relabeling).
"""
import random
import subprocess
import sys
import os
from lines import lines, check_coloring

KISSAT = os.environ.get("KISSAT", "kissat")  # kissat 4.0.4; set KISSAT=/path/to/kissat
N7, M7 = 7, 127
N8, M8 = 8, 255
K = 5
L7 = lines(N7)
L8 = lines(N8)


def random_gl7(rng):
    """Random invertible 7x7 matrix over F_2 as a point map 1..127."""
    while True:
        rows = [rng.randrange(1, 128) for _ in range(7)]
        # check invertibility by Gaussian elimination
        basis = []
        ok = True
        for r in rows:
            v = r
            for b in basis:
                v = min(v, v ^ b)
            if v == 0:
                ok = False
                break
            basis.append(v)
        if ok:
            break
    # map: e_i -> rows[i]; point p = sum bits -> image
    img = [0] * 128
    for p in range(1, 128):
        v = 0
        for i in range(7):
            if p >> i & 1:
                v ^= rows[i]
        img[p] = v
    assert sorted(img[1:]) == list(range(1, 128))
    return img


def sample_witness(seed, rng):
    perm = random_gl7(rng)
    var = lambda p, c: (perm[p] - 1) * K + c + 1
    cls = []
    for p in range(1, M7 + 1):
        cls.append([var(p, c) for c in range(K)])
    for (x, y, z) in L7:
        for c in range(K):
            cls.append([-var(x, c), -var(y, c), -var(z, c)])
    cnf_path = f"/tmp/n7_s{seed}.cnf"
    with open(cnf_path, "w") as f:
        f.write(f"p cnf {M7 * K} {len(cls)}\n")
        for cl in cls:
            f.write(" ".join(map(str, cl)) + " 0\n")
    r = subprocess.run([KISSAT, "--sat", "-q", f"--seed={seed}", cnf_path],
                       capture_output=True, text=True, timeout=600)
    os.unlink(cnf_path)
    model = set()
    for line in r.stdout.splitlines():
        if line.startswith("v "):
            for tok in line[2:].split():
                v = int(tok)
                if v > 0:
                    model.add(v)
    if not model:
        return None
    color = [None] * (M7 + 1)
    for p in range(1, M7 + 1):
        for c in range(K):
            if (perm[p] - 1) * K + c + 1 in model:
                color[p] = c
                break
    bad = check_coloring(N7, color, K)
    assert not bad, f"sample fails verification: {bad[:2]}"
    return color


def fingerprint(color, m, ls):
    sizes = [0] * K
    for p in range(1, m + 1):
        sizes[color[p]] += 1
    pair = [[0] * K for _ in range(K)]
    for (x, y, z) in ls:
        cx, cy, cz = color[x], color[y], color[z]
        if cx == cy and cx != cz:
            pair[cx][cz] += 1
        elif cx == cz and cx != cy:
            pair[cx][cy] += 1
        elif cy == cz and cy != cx:
            pair[cy][cx] += 1
    rows = sorted((sizes[i], tuple(sorted(pair[i]))) for i in range(K))
    return tuple(rows)


def try_extend(color7):
    """Extension SAT: affine points a=0..127 represent (v=a? careful: v ranges
    over ALL of F_2^7 including 0: affine point (0,1) exists = e8 itself).
    Point ids in F_2^8: (v,1) <-> 128 + v for v in 0..127."""
    from pysat.solvers import Cadical195
    var = lambda v, c: v * K + c + 1  # v in 0..127
    cnf = [[var(v, c) for c in range(K)] for v in range(128)]
    for h in range(1, 128):
        ch = color7[h]
        for v in range(128):
            w = v ^ h
            if v < w:
                cnf.append([-var(v, ch), -var(w, ch)])
    with Cadical195(bootstrap_with=cnf) as s:
        if not s.solve():
            return None
        model = set(l for l in s.get_model() if l > 0)
        colorA = [None] * 128
        for v in range(128):
            for c in range(K):
                if var(v, c) in model:
                    colorA[v] = c
                    break
    # assemble full n=8 coloring: point p<=127 -> color7[p]; p>=128 -> colorA[p-128]
    full = [None] * (M8 + 1)
    for p in range(1, 128):
        full[p] = color7[p]
    for v in range(128):
        full[128 + v] = colorA[v]
    bad = check_coloring(N8, full, K)
    assert not bad, f"extension fails full verification: {bad[:2]}"
    return full


def main():
    nsamples = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    rng = random.Random(seed0)
    fps = {}
    next_report = 1
    for i in range(nsamples):
        w = sample_witness(seed0 + i, rng)
        if w is None:
            print(f"[{i}] no witness returned (?)", flush=True)
            continue
        fp = fingerprint(w, M7, L7)
        fps.setdefault(fp, 0)
        fps[fp] += 1
        ext = try_extend(w)
        sizes = sorted(sum(1 for p in range(1, M7 + 1) if w[p] == c) for c in range(K))
        if ext:
            print(f"[{i}] *** EXTENDS *** sizes={sizes}")
            print("FULL8:", ",".join(str(ext[p]) for p in range(1, M8 + 1)), flush=True)
            with open("witness_n8k5.txt", "w") as f:
                f.write(",".join(str(ext[p]) for p in range(1, M8 + 1)) + "\n")
            return
        else:
            if i + 1 >= next_report:
                print(f"[{i}] no-extend  sizes={sizes}  distinct_fps={len(fps)}", flush=True)
                next_report *= 2
    print(f"\ndone: {nsamples} samples, 0 extended, {len(fps)} distinct fingerprints", flush=True)
    for fp, cnt in sorted(fps.items(), key=lambda t: -t[1])[:10]:
        print(f"  count={cnt} sizes={[r[0] for r in fp]}")


if __name__ == "__main__":
    main()
