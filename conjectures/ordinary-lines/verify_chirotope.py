#!/usr/bin/env python3
"""verify_chirotope.py -- independent check of a satisfying assignment: decode chi from the
model, then verify from scratch (no code shared with the encoder's clause generation):
  (1) simplicity: no pair is collinear with every other point; not all points collinear;
  (2) collinearity is transitive (the lines form a linear space);
  (3) the general chirotope axiom (B2) of Bjorner et al. Def. 3.5.3, checked for all
      x = (x1,x2,x3), y = (y1,y2,y3) in E^3:
        if chi(y_i, x2, x3) * chi(y1..y_{i-1}, x1, y_{i+1}..y3) >= 0 for i = 1,2,3
        then chi(x1,x2,x3) * chi(y1,y2,y3) >= 0;
  (4) the three-term GP relations for every 5-set and apex;
  (5) the number of ordinary lines and the line-type distribution.
usage: python3 verify_chirotope.py n cnf_comment_or_model_file model_file
"""
import sys, itertools, json


def load_model(path):
    lits = []
    for tok in open(path).read().split():
        v = int(tok)
        if v != 0:
            lits.append(v)
    return set(l for l in lits if l > 0)


def decode(n, model_pos):
    """variable ids follow ordlines_sat.OrdLinesEncoder: Z then P per triple in
    combinations order: id(Z_t) = 2*idx+1, id(P_t) = 2*idx+2."""
    chi = {}
    for idx, t in enumerate(itertools.combinations(range(n), 3)):
        z, p = 2 * idx + 1, 2 * idx + 2
        chi[t] = 0 if z in model_pos else (1 if p in model_pos else -1)
    return chi


def chi_ord(chi, a, b, c):
    if len({a, b, c}) < 3:
        return 0
    s = 1
    x = [a, b, c]
    for i in range(3):
        for j in range(2 - i):
            if x[j] > x[j + 1]:
                x[j], x[j + 1] = x[j + 1], x[j]
                s = -s
    return s * chi[tuple(x)]


def verify(n, chi):
    E = range(n)
    report = {}
    # (1) simplicity
    ok = True
    for i, j in itertools.combinations(E, 2):
        if all(chi_ord(chi, i, j, k) == 0 for k in E if k not in (i, j)):
            ok = False
    report['simple'] = ok and any(v != 0 for v in chi.values())
    # (2) transitivity
    ok = True
    for q in itertools.combinations(E, 4):
        trips = list(itertools.combinations(q, 3))
        zeros = sum(1 for t in trips if chi[t] == 0)
        if zeros not in (0, 1, 4):
            ok = False
    report['linear_space'] = ok
    # (3) general chirotope axiom (B2)
    ok = True
    viol = 0
    for x in itertools.product(E, repeat=3):
        if len(set(x)) < 3 or chi_ord(chi, *x) == 0:
            continue
        for y in itertools.product(E, repeat=3):
            if len(set(y)) < 3 or chi_ord(chi, *y) == 0:
                continue
            good = True
            for i in range(3):
                yi = y[i]
                left = chi_ord(chi, yi, x[1], x[2])
                yy = list(y)
                yy[i] = x[0]
                right = chi_ord(chi, *yy)
                if left * right < 0:
                    good = False
                    break
            if good and chi_ord(chi, *x) * chi_ord(chi, *y) < 0:
                ok = False
                viol += 1
    report['axiom_B2'] = ok
    report['axiom_B2_violations'] = viol
    # (4) three-term GP
    ok = True
    for five in itertools.combinations(E, 5):
        for a in five:
            w, x_, y_, z_ = [v for v in five if v != a]
            t1 = chi_ord(chi, a, w, x_) * chi_ord(chi, a, y_, z_)
            t2 = -chi_ord(chi, a, w, y_) * chi_ord(chi, a, x_, z_)
            t3 = chi_ord(chi, a, w, z_) * chi_ord(chi, a, x_, y_)
            S = {t1, t2, t3}
            if not (S == {0} or (1 in S and -1 in S)):
                ok = False
    report['gp3'] = ok
    # (5) lines
    lines = set()
    for i, j in itertools.combinations(E, 2):
        pts = {i, j} | {k for k in E if k not in (i, j) and chi_ord(chi, i, j, k) == 0}
        lines.add(tuple(sorted(pts)))
    dist = {}
    for L in lines:
        dist[len(L)] = dist.get(len(L), 0) + 1
    report['ordinary'] = dist.get(2, 0)
    report['distribution'] = dict(sorted(dist.items()))
    report['lines_ge3'] = sorted([L for L in lines if len(L) >= 3], key=lambda L: (-len(L), L))
    return report


if __name__ == '__main__':
    n = int(sys.argv[1])
    model_pos = load_model(sys.argv[2])
    chi = decode(n, model_pos)
    rep = verify(n, chi)
    print(json.dumps(rep, indent=1))
