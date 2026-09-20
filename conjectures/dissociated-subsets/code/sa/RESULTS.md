# RESULTS (running record, 2026-09-08)

## 24-element set with d(A) = 5  — CERTIFIED (exact integer enumeration, two independent programs)

    A24 = {1,2,...,21, 24, 25, 27}      |A| = 24,  max A = 27

Found by `./sa 24 6 40 1 8 3000 3 0.05 0 2` (m=24, k=6, W=40, seed=1, 8 s, 3000 iters/restart,
T0=3, T1=0.05, no secondary weight, init mode 2 = random 24-subset of [1,56]) at iteration ~2048.

Verification:
- `dval` (C, DFS over the down-set of dissociated subsets):
  `d=5 n=24 witness: 1 2 4 8 16`
- `bruteforce_d.py` (Python, no shared code; enumerates ALL 24-choose-6 = 134596 six-subsets and
  finds none with 64 distinct subset sums):
  `|A|=24 d(A)=5 witness=[1, 2, 4, 8, 16] (bottom-up: no dissociated 6-subset among all 24-choose-6)`

Status: d(A24) = 5 exactly (witness {1,2,4,8,16}; no dissociated 6-subset).  The prompt states the
known record for d <= 5 is {1..23}; this set has one more element.  Literature check still required
before calling it new.
