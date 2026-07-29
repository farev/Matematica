import time

import numpy as np

rng = np.random.default_rng(64646464)
t0 = time.time()
nmax, S, B = 1023, 400_000, 100_000
sums = np.zeros(nmax + 1)
sq = np.zeros(nmax + 1)
done = 0
while done < S:
    x = rng.exponential(size=(B, nmax + 1))  # float64 throughout
    for i in range(nmax + 1):
        c = x[:, 0]
        sums[i] += c.sum()
        sq[i] += (c * c).sum()
        if i < nmax:
            x = np.abs(x[:, :-1] - x[:, 1:])
    done += B
    print(f"  batch done ({time.time()-t0:.0f}s)", flush=True)
m = sums / S
se = np.sqrt(np.maximum(sq / S - m * m, 0) / S)
old = np.loadtxt("ck_montecarlo.csv", delimiter=",", skiprows=1)
print(f"float64 n<=1023 S={S} done {time.time()-t0:.0f}s")
for i in (255, 256, 511, 512, 1023):
    f32c, f32se = old[i, 1], old[i, 2]
    z = (m[i] - f32c) / np.hypot(se[i], f32se)
    print(f"i={i:>5}: f64 {m[i]:.6f}+-{se[i]:.6f}  f32 {f32c:.6f}+-{f32se:.6f}"
          f"  dev {z:+.2f} sigma")
