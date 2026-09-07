#!/bin/bash
D=/tmp/claude-0/-home-user-Matematica/90f87f8c-75b0-5d88-9ac6-ec4565e2dd94/scratchpad/f6probe
cd "$D"
run() { timeout -s KILL $(( $3 + 120 )) python3 "$D/solve.py" "$D/$1" $2 $3 "$D/sat_$4" > "$D/sat_$4.log" 2>&1; echo "[$(date +%T)] finished $4 (exit $?)" >> "$D/sat_chain.log"; }
run p29_t28_0_g8_1_strong.cnf cadical195 150 p29g8_strong_cadical
run p31_t30_0_g22_1_strong.cnf cadical195 150 p31g22_strong_cadical
run p31_t30_0_g7_1_strong.cnf cadical195 240 p31g7_strong_cadical
run p29_t28_0_g3_1_strong.cnf cadical195 480 p29g3_strong_cadical
