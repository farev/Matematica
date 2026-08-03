"""Re-decide selected (n,m) instances with three independent SAT backends.

The load-bearing UNSAT verdicts of this conjecture are the n=4 late gaps
(NOTE.md Result C3).  UNSAT is the one class of claim here that is NOT
independently verifiable from a witness, so those instances -- and their
satisfiable neighbours, as a control -- are re-decided by Cadical, Glucose and
MiniSat.  Every SAT answer is additionally re-verified by the
from-the-definition checker, so a backend that returned a bogus model would be
caught rather than believed.

Usage:
    python3 crosscheck.py 4 113 146 147 148 153 154 155
    python3 crosscheck.py 4 147 --alpha 7/5
"""
import argparse
import time
from fractions import Fraction

from circspec import RT, solve, verify

SOLVERS = ('cadical153', 'glucose42', 'minisat22')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int)
    ap.add_argument('ms', type=int, nargs='+')
    ap.add_argument('--alpha', default=None)
    a = ap.parse_args()
    alpha = RT(a.n) if a.alpha is None else Fraction(a.alpha)

    print(f'n={a.n}, alpha={alpha} -- three independent SAT backends, '
          f'same exact encoding')
    disagreements = 0
    for m in a.ms:
        cells, verdicts = [], set()
        for s in SOLVERS:
            t = time.time()
            ok, w = solve(a.n, m, alpha, s)
            dt = time.time() - t
            if ok:
                good, bad = verify(w, a.n, alpha)
                if not good:
                    raise SystemExit(f'FATAL: {s} model at m={m} fails '
                                     f'the definition check: {bad}')
            verdicts.add(ok)
            cells.append(f'{s}={"SAT" if ok else "UNSAT"}({dt:.1f}s)')
        flag = ''
        if len(verdicts) > 1:
            flag = '   *** BACKENDS DISAGREE ***'
            disagreements += 1
        print(f'  m={m:5d}  ' + '  '.join(cells) + flag, flush=True)
    print(f'# instances: {len(a.ms)}   disagreements: {disagreements}')
    raise SystemExit(1 if disagreements else 0)


if __name__ == '__main__':
    main()
