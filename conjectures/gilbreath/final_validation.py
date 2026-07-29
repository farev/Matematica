"""Final out-of-sample validation of the submask law on i in [1024, 4095].

The law c_i = C * i^-alpha * sum_{m subset i} q^m is fitted ONLY on
i in [64, 1023] (the data that existed when the law was proposed), then
evaluated as a pure prediction on the new deep-MC data i in [1024, 4095].
"""

import numpy as np


def submask_factor(i, q):
    f = 1.0
    j = 0
    while (1 << j) <= i:
        if i >> j & 1:
            f *= 1.0 + q ** (1 << j)
        j += 1
    return f


def adj_pairs(i):
    return bin(i & (i >> 1)).count("1")


def fit(i_arr, c, se, lo, hi, with_runs=True):
    m = (i_arr >= lo) & (i_arr <= hi) & (c > 0)
    ii, cc, ss = i_arr[m], c[m], se[m]
    w = cc / ss
    y = np.log(cc)
    best = None
    for q in np.arange(0.4, 0.95, 0.0025):
        g = np.log([submask_factor(int(v), q) for v in ii])
        cols = [np.ones(len(ii)), -np.log(ii)]
        if with_runs:
            cols.append(np.array([adj_pairs(int(v)) for v in ii], float))
        X = np.column_stack(cols)
        coef, *_ = np.linalg.lstsq(X * w[:, None], (y - g) * w, rcond=None)
        pred = X @ coef + g
        ssr = (((y - pred) * w) ** 2).sum()
        if best is None or ssr < best[0]:
            best = (ssr, q, coef)
    return best[1], best[2]


def predict(i, q, coef):
    g = np.log(submask_factor(int(i), q))
    v = coef[0] - coef[1] * np.log(i) + g
    if len(coef) > 2:
        v += coef[2] * adj_pairs(int(i))
    return np.exp(v)


if __name__ == "__main__":
    deep = np.loadtxt("ck_mc_deep.csv", delimiter=",", skiprows=1)
    i_arr, c, se = deep[:, 0].astype(int), deep[:, 1], deep[:, 2]

    q, coef = fit(i_arr, c, se, 64, 1023)
    print(f"law fitted on [64,1023] ONLY: q={q:.4f}, alpha={coef[1]:.4f}, "
          f"C={np.exp(coef[0]):.4f}, tau={coef[2]:.4f}")

    m = (i_arr >= 1024) & (i_arr <= 4095) & (c > 0) & (se > 0)
    ii, cc = i_arr[m], c[m]
    pred = np.array([predict(v, q, coef) for v in ii])
    y, p = np.log(cc), np.log(pred)
    r2 = 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    rel = np.abs(np.exp(y - p) - 1)
    print(f"\nOUT-OF-SAMPLE [1024,4095]: n={m.sum()}, R^2 = {r2:.4f}, "
          f"mean |rel err| = {rel.mean()*100:.1f}%, median = "
          f"{np.median(rel)*100:.1f}%")

    print("\nheadline predictions vs measurement:")
    for v in (1024, 1025, 1535, 2047, 2048, 3071, 4095):
        if v <= i_arr.max() and c[v] > 0:
            pr = predict(v, q, coef)
            print(f"  i={v:>5} ({bin(v)[2:]}): predicted {pr:.6f}   "
                  f"measured {c[v]:.6f} +- {se[v]:.6f}   ratio "
                  f"{c[v]/pr:.3f}")

    print("\ndigit-sum ladder at the new scale (i in [2048, 4095]):")
    s = np.array([bin(int(v)).count("1") for v in i_arr])
    for sv in range(1, 13):
        g = m & (i_arr >= 2048) & (s == sv)
        if g.sum() >= 2:
            vals = i_arr[g] * c[g]
            print(f"  s={sv:>2}: mean i*c_i = {vals.mean():7.3f} (n={g.sum()})")

    print("\npartial sums to 4095:")
    S = np.cumsum(c)
    for n in (1023, 2047, 4095):
        print(f"  n={n}: S_n = {S[n]:.3f}   10.84 n^0.2 - 11.43 = "
              f"{10.84*n**0.2-11.43:.3f}")
