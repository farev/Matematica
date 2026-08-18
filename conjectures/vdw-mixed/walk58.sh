#!/bin/bash
# (5,8) lower-bound walk: pure-periodic scan at increasing n; on first n with
# no periodic witness, stop (defect engine takes over from there).
cd "$(dirname "$0")"
for n in 280 290 300 310 320 330 340 350 360; do
  echo "=== (5,8) n=$n ==="
  python3 periodic_sat.py 5 8 $n 30 150 2>&1 | grep -E "PERIODIC|periods|NO exactly"
  if python3 periodic_sat.py 5 8 $n 30 150 2>/dev/null | grep -q "NO exactly"; then
    echo "walk stops at n=$n"
    break
  fi
done
