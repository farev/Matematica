"""Produce and certify long undirected-free witness words.

For alphabet k (= n) and alpha = (k-1)/(k-2), builds the lexicographically
least canonical U-alpha+-free word of length L (DFS in lex order with
backtracking; the first depth-L word found in lex-order DFS is the lex-least
one), then verifies it with three further independent checkers:

  1. UInc            (incremental, used during generation)
  2. u_offender      (pure-python batch scan, separate logic)
  3. u_free_np       (numpy batch, separate logic)
  4. u_offender_naive on a prefix (brute triple loop)

Writes data/witness_n<k>_L<L>.txt and prints a verification transcript.

Usage: python3 certify_witness.py <k> <L> [prefix_for_naive]
"""

import sys
import time

from urt import UInc, u_offender, u_free_np, u_offender_naive


def lex_least(n, num, den, L, max_backtracks=2_000_000):
    inc = UInc(num, den, L + 2)
    word = []
    used = 0
    stack = []
    bt = 0
    while len(word) < L:
        recent = set(word[-(n - 3):]) if len(word) >= n - 3 else set(word)
        cands = [c for c in range(min(used + 1, n)) if c not in recent]
        placed = False
        for ci, c in enumerate(cands):
            if inc.push(c):
                word.append(c)
                stack.append(cands[ci + 1:])
                used = max(used, c + 1)
                placed = True
                break
            inc.pop()
        if not placed:
            while stack:
                bt += 1
                if bt > max_backtracks:
                    return None, bt
                rest = stack.pop()
                word.pop()
                inc.pop()
                used = max([0] + [x + 1 for x in word])
                pl2 = False
                for ci, c in enumerate(rest):
                    if inc.push(c):
                        word.append(c)
                        stack.append(rest[ci + 1:])
                        used = max(used, c + 1)
                        pl2 = True
                        break
                    inc.pop()
                if pl2:
                    break
            else:
                return None, bt  # language exhausted below L
    return word, bt


if __name__ == "__main__":
    k = int(sys.argv[1])
    L = int(sys.argv[2])
    naiveL = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    num, den = k - 1, k - 2
    t0 = time.time()
    w, bt = lex_least(k, num, den, L)
    t1 = time.time()
    if w is None:
        print(f"k={k}: FAILED to reach {L} (backtracks {bt})")
        sys.exit(1)
    print(f"k={k} alpha={num}/{den}: lex-least canonical word of length {L} "
          f"built, {bt} backtracks [{t1-t0:.0f}s]")
    o1 = u_offender(w, num, den)
    t2 = time.time()
    print(f"  u_offender (pure python):  {o1}  [{t2-t1:.0f}s]")
    ok2 = u_free_np(w, num, den)
    t3 = time.time()
    print(f"  u_free_np (numpy batch):   {'free' if ok2 else 'OFFENDER'}  [{t3-t2:.0f}s]")
    o3 = u_offender_naive(w[:naiveL], num, den)
    t4 = time.time()
    print(f"  naive brute on prefix {naiveL}: {o3}  [{t4-t3:.0f}s]")
    assert o1 is None and ok2 and o3 is None
    fn = f"data/witness_n{k}_L{L}.txt"
    with open(fn, "w") as f:
        f.write(f"# lexicographically least canonical undirected-({num}/{den})+-free word, alphabet {k}, length {L}\n")
        f.write(f"# generated+verified 2026-08-18; checkers: UInc, u_offender, u_free_np, naive(prefix {naiveL})\n")
        f.write(",".join(map(str, w)) + "\n")
    print(f"  wrote {fn}")
