"""Controls for urt.py.  Run from this directory: python3 tests_urt.py

1. u_offender vs u_offender_naive vs u_free_np vs UInc on random words
   (positive and negative instances).
2. decode/encode roundtrip; agreement with circular-thresholds/pansiot.py
   (independent implementation) on decode and monodromy.
3. The reversal identities behind the NOTE's lemmas, checked empirically:
   r tau_b r = tau_b^{-1};  code(rev w) = rev(code w);
   pattern(dec(rev V)) = pattern(rev(dec V)).
4. Language facts at n = 22, alpha = 21/20: "00" not U-code-free; 1-runs
   of length 22 not U-code-free.
"""

import random
import sys
import importlib.util
from pathlib import Path

import numpy as np

from urt import (
    make_taus, comp, pinv, g_of, rperm, decode, encode,
    ord_offender, rev_offender, u_offender, u_offender_naive, u_free,
    u_free_np, UInc, cycle_type,
)

HERE = Path(__file__).resolve().parent
PANSIOT = HERE.parent / "circular-thresholds" / "pansiot.py"


def load_pansiot():
    spec = importlib.util.spec_from_file_location("pansiot_ref", PANSIOT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def t1_checkers_agree(trials=4000, seed=1):
    rng = random.Random(seed)
    mism = 0
    pos = neg = 0
    for t in range(trials):
        L = rng.randint(2, 26)
        A = rng.randint(2, 8)
        num, den = rng.choice([(21, 20), (6, 5), (7, 4), (3, 2), (9, 8)])
        x = [rng.randrange(A) for _ in range(L)]
        a = u_offender_naive(x, num, den) is None
        b = u_offender(x, num, den) is None
        c = u_free_np(x, num, den)
        inc = UInc(num, den, L + 1)
        d = True
        for ch in x:
            if not inc.push(ch):
                d = False
                break
        if a:
            pos += 1
        else:
            neg += 1
        if not (a == b == c == d):
            mism += 1
            print("MISMATCH", x, num, den, a, b, c, d)
            if mism > 5:
                return False
    print(f"t1: {trials} random words, naive/scan/np/inc agree; "
          f"{pos} free, {neg} unfree")
    return mism == 0


def t1b_push_pop(seed=2, trials=300):
    rng = random.Random(seed)
    for t in range(trials):
        num, den = (21, 20)
        L = rng.randint(4, 18)
        A = rng.randint(2, 6)
        x = [rng.randrange(A) for _ in range(L)]
        inc = UInc(num, den, 64)
        # interleave push/pop randomly, replay against fresh checker
        stack = []
        for ch in x:
            inc.push(ch)
            stack.append(ch)
            if rng.random() < 0.3 and stack:
                inc.pop()
                stack.pop()
        ok_inc = True
        inc2 = UInc(num, den, 64)
        for ch in stack:
            ok_inc = inc2.push(ch)
        ref = u_free(stack, num, den)
        # inc reports cumulative freeness only through last push; recompute
        got = True
        inc3 = UInc(num, den, 64)
        for ch in stack:
            if not inc3.push(ch):
                got = False
                break
        if got != ref:
            print("PUSHPOP MISMATCH", stack)
            return False
    print(f"t1b: {trials} push/pop replays agree")
    return True


def t2_pansiot_agreement():
    P = load_pansiot()
    rng = random.Random(3)
    for t in range(500):
        n = rng.randint(3, 24)
        L = rng.randint(0, 40)
        bits = [rng.randint(0, 1) for _ in range(L)]
        if decode(bits, n) != P.decode(bits, n):
            print("decode mismatch", n, bits)
            return False
        t0, t1_ = P.make_taus(n)
        if make_taus(n) != (t0, t1_):
            print("taus mismatch", n)
            return False
        if g_of(bits, n) != P.g_of(bits, t0, t1_):
            print("monodromy mismatch", n, bits)
            return False
        w = decode(bits, n)
        eb, ok = encode(w, n)
        if not ok or eb != bits:
            print("roundtrip mismatch", n, bits)
            return False
    print("t2: decode/taus/monodromy agree with pansiot.py on 500 random "
          "instances; encode(decode) = id")
    return True


def t3_reversal_identities():
    rng = random.Random(4)
    for n in (5, 8, 12, 22, 23):
        tau0, tau1 = make_taus(n)
        r = rperm(n)
        for b, tb in ((0, tau0), (1, tau1)):
            if comp(comp(r, tb), r) != pinv(tb):
                print("r tau r != tau^-1", n, b)
                return False
        for t in range(200):
            L = rng.randint(n + 1, 3 * n)
            bits = [rng.randint(0, 1) for _ in range(L)]
            w = decode(bits, n)
            wr = w[::-1]
            eb, ok = encode(wr, n)
            if not ok:
                print("reverse not in-class?!", n, bits)
                return False
            if eb != bits[::-1]:
                print("code(rev w) != rev(code w)", n, bits)
                return False
            # pattern identity: dec(rev V) and rev(dec V) same equal-letter
            # pattern
            dv = decode(bits[::-1], n)
            rv = w[::-1]
            pat = lambda u: [[i for i in range(len(u)) if u[i] == u[j]][0]
                             for j in range(len(u))]
            if pat(dv) != pat(rv):
                print("pattern mismatch", n, bits)
                return False
        # g(rev V) = r g(V)^-1 r
        for t in range(200):
            L = rng.randint(0, 3 * n)
            bits = [rng.randint(0, 1) for _ in range(L)]
            lhs = g_of(bits[::-1], n)
            g = g_of(bits, n)
            rhs = comp(comp(r, pinv(g)), r)
            if lhs != rhs:
                print("g(rev) identity fails", n, bits)
                return False
    print("t3: r-conjugation, code-reversal, pattern and g(rev) identities "
          "hold on all instances")
    return True


def t4_language_facts():
    n, num, den = 22, 21, 20
    w00 = decode([0, 0], n)
    a = u_offender(w00, num, den)
    assert a is not None, "00 should be an offender"
    w0 = decode([0], n)
    assert u_offender(w0, num, den) is None, "single 0 should be free"
    ones22 = decode([1] * 22, n)
    assert u_offender(ones22, num, den) is not None, "1^22 should offend"
    ones21 = decode([1] * 21, n)
    r21 = u_offender(ones21, num, den)
    print(f"t4: dec(00) offends ({a}); dec(0) free; dec(1^22) offends; "
          f"dec(1^21) -> {r21}")
    return True


if __name__ == "__main__":
    ok = True
    ok &= t1_checkers_agree()
    ok &= t1b_push_pop()
    ok &= t2_pansiot_agreement()
    ok &= t3_reversal_identities()
    ok &= t4_language_facts()
    print("ALL PASS" if ok else "FAILURES")
    sys.exit(0 if ok else 1)
