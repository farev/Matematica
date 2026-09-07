#!/bin/bash
# Run orientation analysis for the six class representatives, two chains in parallel.
D=/tmp/claude-0/-home-user-Matematica/90f87f8c-75b0-5d88-9ac6-ec4565e2dd94/scratchpad/f6probe
cd "$D"
chain() {
  for a in "$@"; do
    set -- $a
    SUB_BUDGET=5 timeout -s KILL 200 python3 "$D/orient.py" $1 $2 $3 $4 $5 > "$D/orient_$6.log" 2>&1
  done
}
chain "29 28 0 3 1 p29_g3" "29 28 0 8 1 p29_g8" "31 30 0 7 1 p31_g7" &
chain "31 30 0 10 1 p31_g10" "31 30 0 11 1 p31_g11" "31 30 0 22 1 p31_g22" &
wait
for f in p29_g3 p29_g8 p31_g7 p31_g10 p31_g11 p31_g22; do echo "##### $f"; cat "$D/orient_$f.log"; done
ls -la "$D"/*.cnf
date
