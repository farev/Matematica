#!/bin/bash
D=/tmp/claude-0/-home-user-Matematica/90f87f8c-75b0-5d88-9ac6-ec4565e2dd94/scratchpad/f6probe
cd "$D"
# core A: after the cadical chain (run_sat2.sh) ends, probe p31 (11,1) strengthened with cadical for 300 s
( until grep -q "finished p29g3_strong_cadical" sat_chain.log; do sleep 5; done
  timeout -s KILL 420 python3 "$D/solve.py" "$D/p31_t30_0_g11_1_strong.cnf" cadical195 300 "$D/sat_p31g11_strong_cadical" > "$D/sat_p31g11_strong_cadical.log" 2>&1
  echo "[$(date +%T)] finished p31g11_strong_cadical (exit $?)" >> sat_chain.log ) &
# core B: after kissat on the original p29 (3,1) ends, probe p31 (7,1) strengthened with kissat for 300 s
( until grep -q "kissat p29g3 finished" sat_chain.log; do sleep 5; done
  timeout -s KILL 300 python3 "$D/solve.py" "$D/p31_t30_0_g7_1_strong.cnf" kissat404 300 "$D/sat_p31g7_strong_kissat" > "$D/sat_p31g7_strong_kissat.log" 2>&1
  echo "[$(date +%T)] finished p31g7_strong_kissat (exit $?)" >> sat_chain.log ) &
wait
