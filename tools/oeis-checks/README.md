# oeis-checks — independent re-implementations of OEIS entries whose conjectures a session tested

| file | entry | what it does | result (2026-09-06) |
|---|---|---|---|
| `a398259.c N` | A398259 (Van Eck-like, digit-sum key) | recomputes the sequence from the entry's definition, lists zeros, checkpoints a(10^4), a(10^5), a(10^6) | reproduces the 26 listed zeros and all checkpoints; finds a 27th zero a(700000442) = 0, refuting the entry's "these are all the zeros" conjecture (34 s wall to N = 7.1·10^8, 2.8 GB) |

`gcc -O2 -o a398259 a398259.c && ./a398259 710000000`
