#!/usr/bin/env python3
"""Regularity certificates for 1-additive (Ulam-type) sequences U(a,b).  v2.

See NOTE.md for the theorem this implements.  Everything is exact integer
arithmetic; there is no floating point anywhere in the critical path.
"""
import sys
from ulam import ulam


def certify(a, b, X0=4000, horizon=400000, want_period_only=False):
    terms = ulam(a, b, X0)
    E = [x for x in terms if x % 2 == 0]
    if not E:
        return {"ok": False, "why": "no even elements"}
    W = max(E)
    if W > X0 // 4:
        return {"ok": False, "why": f"W={W} too close to X0={X0}; raise X0"}

    # ---- extend by the window rule, maintaining the state incrementally ----
    inU = bytearray(horizon + 2)
    for t in terms:
        inU[t] = 1
    half = W // 2
    mask = (1 << half) - 1
    offs = [e // 2 - 1 for e in E]          # bit index of offset e

    x = X0 + 1 if X0 % 2 == 0 else X0 + 2   # first odd x > X0
    # initial window at x: bit j = [x-2(j+1) in U*]
    win = 0
    for j in range(half):
        y = x - 2 * (j + 1)
        if y > 0 and inU[y]:
            win |= 1 << j

    seen = {}
    X1 = P = None
    while x <= horizon:
        if x > X0 + W + 2:                  # window entirely inside the automaton region
            if win in seen:
                X1, P = seen[win], x - seen[win]
                if want_period_only:
                    return {"ok": None, "E": E, "W": W, "X1": X1, "P": P}
                break
            seen[win] = x
        c = 0
        for o in offs:
            if (win >> o) & 1:
                c += 1
                if c > 1:
                    break
        hit = 1 if c == 1 else 0
        if hit:
            inU[x] = 1
        win = ((win << 1) | hit) & mask
        x += 2
    if P is None:
        return {"ok": False, "why": f"no window-state repeat below {horizon}",
                "E": E, "W": W}

    # continue filling inU past the cycle point, out to the bound we need
    B = 2 * X1 + 4 * P + 2 * W + 4
    if B > horizon:
        return {"ok": False, "why": f"B={B} exceeds horizon {horizon}",
                "E": E, "W": W, "X1": X1, "P": P}
    while x <= B:
        c = 0
        for o in offs:
            if (win >> o) & 1:
                c += 1
                if c > 1:
                    break
        hit = 1 if c == 1 else 0
        if hit:
            inU[x] = 1
        win = ((win << 1) | hit) & mask
        x += 2

    # ---- (C) residue analysis ----
    R = set()
    for y in range(X1, X1 + P, 2):
        if inU[y]:
            R.add(y % P)
    small_odds = [t for t in terms if t % 2 == 1 and t < X1]
    # odd elements of U* in [X0, X1) too -- they are also "small"
    for y in range(X0 + 1 if X0 % 2 == 0 else X0 + 2, X1, 2):
        if inU[y]:
            small_odds.append(y)
    small_odds = sorted(set(small_odds))

    bad_classes = []
    for cc in range(0, P, 2):
        big = any(((cc - r) % P) in R for r in R)
        if big:
            continue                         # A(x) >= 2 for x >= B
        beta = sum(1 for u0 in small_odds if ((cc - u0) % P) in R)
        if beta == 1:
            bad_classes.append((cc, beta))
    if bad_classes:
        return {"ok": False, "why": f"classes with exactly one forced rep: {bad_classes[:6]}",
                "E": E, "W": W, "X1": X1, "P": P, "R": len(R)}

    # ---- (F) finite check: every even x in (X0, B] has != 1 representations ----
    pos = [i for i in range(1, min(B, horizon) + 1) if inU[i]]
    posset = set(pos)
    bad = []
    for xx in range(X0 + 2 if X0 % 2 == 0 else X0 + 1, B + 1, 2):
        cnt = 0
        for u in pos:
            if u * 2 >= xx:
                break
            if (xx - u) in posset:
                cnt += 1
                if cnt > 1:
                    break
        if cnt == 1:
            bad.append(xx)
            if len(bad) > 3:
                break
    if bad:
        return {"ok": False, "why": f"even x with exactly one representation: {bad}",
                "E": E, "W": W, "X1": X1, "P": P}

    return {"ok": True, "a": a, "b": b, "E": E, "W": W, "X0": X0,
            "X1": X1, "P": P, "nR": len(R), "B": B}


if __name__ == "__main__":
    a = int(sys.argv[1]); b = int(sys.argv[2])
    X0 = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    H = int(sys.argv[4]) if len(sys.argv) > 4 else 400000
    print(f"U({a},{b}): {certify(a, b, X0, H)}")
