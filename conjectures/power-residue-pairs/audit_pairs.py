# Independent check of a pairs file: every line "n fa fb" must satisfy prod(fa) = n,
# prod(fb) = n+1, all bases prime, exponents >= 1, and the file must be sorted with n <= L.
import sys
from sympy import isprime
fn = sys.argv[1]; bad = 0; cnt = 0; last = 0; maxp = 0
def prod(s):
    global maxp
    if s == '1': return 1
    r = 1
    for tok in s.split(','):
        p, e = tok.split('^'); p, e = int(p), int(e)
        assert e >= 1 and isprime(p), (fn, tok); maxp = max(maxp, p); r *= p ** e
    return r
for line in open(fn):
    if line[0] == '#': continue
    n, fa, fb = line.split(); n = int(n)
    assert n > last, ('unsorted', n); last = n
    if prod(fa) != n or prod(fb) != n + 1: bad += 1; print('BAD', line.strip())
    cnt += 1
print(f'{fn}: {cnt} pairs checked, {bad} bad, largest prime {maxp}, largest n {last}')
