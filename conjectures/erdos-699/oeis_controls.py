#!/usr/bin/env python3
"""oeis_controls.py — validate the Kummer-carry machinery used by the #699
sweep against OEIS ground truth (sequence files pinned in data/, fetched
from the oeis/oeisdata git mirror on 2026-08-11).

Controls:
  A129488  smallest odd prime dividing C(2n,n)          (carry criterion)
  A263922  highest exponent in C(2n,n) = max #carries   (Legendre/Kummer)
  A030979  k with C(2k,k) coprime to 3,5,7 — all listed terms <= 25000
           must be reproduced, no extras
  A005250/A002386  record prime gaps: the sweep's maxg values must equal
           (largest record gap with starting prime in range) - 1
           (checked separately in check_summaries.py once chunks finish)

Every check recomputes from scratch with exact integer arithmetic and
compares against the %S/%T/%U term lines of the pinned .seq files.
Exit 0 iff all controls pass.
"""
import sys, re


def seq_terms(path):
    terms = []
    for line in open(path):
        m = re.match(r"^%[STU] A\d+ (.*)$", line.strip())
        if m:
            terms += [int(x) for x in m.group(1).rstrip(",").split(",") if x]
    return terms


def carries(n, k, p):
    """number of carries when adding k and n-k in base p (= v_p(C(n,k)))"""
    c = 0
    pt = p
    while pt <= n:
        if k % pt > n % pt:
            c += 1
        pt *= p
    return c


def primes_up_to(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = b"\x00" * len(range(p * p, n + 1, p))
    return [i for i in range(n + 1) if sieve[i]]


def main():
    ok = True

    # --- A129488: smallest odd prime dividing C(2n,n), offset 2 (%O line) ---
    ref = seq_terms("data/A129488.seq")
    P = primes_up_to(2 * (len(ref) + 2) + 10)
    mine = []
    for n in range(2, len(ref) + 2):
        val = next(p for p in P if p >= 3 and carries(2 * n, n, p) >= 1)
        mine.append(val)
    if mine == ref:
        print(f"A129488 control PASS ({len(ref)} terms)")
    else:
        ok = False
        print(f"A129488 control FAIL: first mismatch at n={1+min(i for i in range(len(ref)) if mine[i]!=ref[i])}")

    # --- A263922: highest exponent in C(2n,n) = max carries over p <= 2n ---
    ref = seq_terms("data/A263922.seq")
    P = primes_up_to(2 * len(ref) + 10)
    mine = []
    for n in range(1, len(ref) + 1):
        mine.append(max(carries(2 * n, n, p) for p in P if p <= 2 * n))
    if mine == ref:
        print(f"A263922 control PASS ({len(ref)} terms)")
    else:
        ok = False
        print(f"A263922 control FAIL")

    # --- A030979: C(2k,k) coprime to 3,5,7 ---
    ref = [t for t in seq_terms("data/A030979.seq") if t <= 25000]
    mine = [k for k in range(0, 25001)
            if carries(2 * k, k, 3) == 0 and carries(2 * k, k, 5) == 0
            and carries(2 * k, k, 7) == 0]
    if mine == ref:
        print(f"A030979 control PASS (all {len(ref)} listed terms <= 25000 reproduced, no extras)")
    else:
        ok = False
        print(f"A030979 control FAIL: mine={mine} ref={ref}")

    print("OEIS CONTROLS", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
